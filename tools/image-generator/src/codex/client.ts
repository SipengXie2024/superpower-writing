import { promises as fs } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";

import { ensureFreshCredentials } from "../auth/refresh.js";
import { AuthError, CodexApiError, StreamParseError } from "../util/errors.js";
import { debugEnabled, logger } from "../util/log.js";
import { parseSSE } from "./sse.js";
import type { CodexRequestBody, ParsedImage } from "./types.js";

const CODEX_RESPONSES_URL = "https://chatgpt.com/backend-api/codex/responses";
const DEFAULT_OUTER_MODEL = "gpt-5.5";
const DEFAULT_IMAGE_MODEL = "gpt-image-2";

export const codexConfig = {
  responsesUrl: CODEX_RESPONSES_URL,
  outerModel: DEFAULT_OUTER_MODEL,
  imageModel: DEFAULT_IMAGE_MODEL,
};

export interface RunImageRequestArgs {
  body: CodexRequestBody;
  /** When true, every received SSE event is appended to a debug file. */
  debugDump?: boolean;
}

export async function runImageRequest({
  body,
  debugDump,
}: RunImageRequestArgs): Promise<ParsedImage> {
  const creds = await ensureFreshCredentials();

  const headers: Record<string, string> = {
    Authorization: `Bearer ${creds.access}`,
    "Content-Type": "application/json",
    Accept: "text/event-stream",
    "OpenAI-Beta": "responses=experimental",
  };
  if (creds.chatgpt_account_id) {
    headers["ChatGPT-Account-Id"] = creds.chatgpt_account_id;
  }

  logger.debug(`POST ${CODEX_RESPONSES_URL} (model=${body.model}, tools=${body.tools.length})`);

  const res = await fetch(CODEX_RESPONSES_URL, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (res.status === 401 || res.status === 403) {
    const text = await res.text().catch(() => "");
    throw new AuthError(
      "unauthorized",
      `Codex backend rejected the access token (HTTP ${res.status}). ` +
        `Run \`image-gen login\` again. Body: ${preview(text)}`,
    );
  }
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new CodexApiError(res.status, preview(text));
  }
  if (!res.body) {
    throw new StreamParseError("Codex response had no body");
  }

  const dumpPath =
    debugDump || debugEnabled()
      ? path.join(tmpdir(), `image-gen-sse-${Date.now()}.log`)
      : null;
  if (dumpPath) {
    await fs.writeFile(dumpPath, "", { mode: 0o600 });
    logger.debug(`Dumping SSE events to ${dumpPath}`);
  }

  return await consumeStream(res.body, dumpPath);
}

async function consumeStream(
  body: ReadableStream<Uint8Array>,
  dumpPath: string | null,
): Promise<ParsedImage> {
  const collected: ParsedImage = {
    base64: "",
    mediaType: "image/png",
    sourceEvents: [],
  };

  for await (const evt of parseSSE(body)) {
    if (dumpPath) {
      const line = `event: ${evt.event}\ndata: ${evt.data.slice(0, 4096)}\n\n`;
      await fs.appendFile(dumpPath, line);
    }

    let parsed: unknown = null;
    try {
      parsed = evt.data ? JSON.parse(evt.data) : null;
    } catch {
      // Some SSE events ship `data: [DONE]` or other non-JSON markers; ignore.
      continue;
    }
    if (!parsed || typeof parsed !== "object") continue;

    extractFromAny(parsed, evt.event, collected);

    if (evt.event === "response.completed" || evt.event === "response.done") {
      const root = parsed as Record<string, unknown>;
      const response = (root.response as Record<string, unknown> | undefined) ?? root;
      const id = response.id;
      if (typeof id === "string") collected.requestId = id;
      const model = response.model;
      if (typeof model === "string") collected.model = model;
    }
  }

  if (!collected.base64) {
    const hint = dumpPath
      ? ` See SSE dump at ${dumpPath}.`
      : " Set IMAGE_GEN_DEBUG=1 to capture the SSE stream and identify the event shape.";
    throw new StreamParseError(`Codex stream completed without an image payload.${hint}`);
  }

  return collected;
}

/**
 * Walk an arbitrary parsed event payload looking for fields that match the
 * known shapes for image data the Codex/Responses API uses. We accept any of:
 *
 *   { type: "image_generation_call.result", result: { b64_json, ... } }
 *   { type: "output_image", image: { base64, media_type } }
 *   { partial_image_b64: "..." }              (gpt-image-* streaming partials)
 *   { b64_json: "...", revised_prompt? }      (final image payload)
 *
 * The newest matching `base64` blob wins (final payloads supersede partials).
 */
function extractFromAny(
  node: unknown,
  eventName: string,
  out: ParsedImage,
  depth = 0,
): void {
  if (depth > 8 || node === null || typeof node !== "object") return;

  if (Array.isArray(node)) {
    for (const item of node) extractFromAny(item, eventName, out, depth + 1);
    return;
  }

  const obj = node as Record<string, unknown>;

  const directFields: Array<[string, string]> = [
    ["b64_json", "image/png"],
    ["partial_image_b64", "image/png"],
    ["base64", "image/png"],
  ];
  for (const [field, defaultMime] of directFields) {
    const value = obj[field];
    if (typeof value === "string" && value.length > 0) {
      out.base64 = value;
      const mt = obj.media_type ?? obj.mime_type;
      out.mediaType = typeof mt === "string" ? mt : defaultMime;
      if (!out.sourceEvents.includes(eventName)) out.sourceEvents.push(eventName);
    }
  }

  const image = obj.image;
  if (image && typeof image === "object") {
    const img = image as Record<string, unknown>;
    const b64 = img.base64 ?? img.b64_json;
    if (typeof b64 === "string" && b64.length > 0) {
      out.base64 = b64;
      out.mediaType =
        typeof img.media_type === "string"
          ? img.media_type
          : typeof img.mime_type === "string"
            ? img.mime_type
            : "image/png";
      if (!out.sourceEvents.includes(eventName)) out.sourceEvents.push(eventName);
    }
  }

  for (const value of Object.values(obj)) {
    if (value && typeof value === "object") {
      extractFromAny(value, eventName, out, depth + 1);
    }
  }
}

function preview(text: string): string {
  const trimmed = text.trim();
  return trimmed.length > 400 ? `${trimmed.slice(0, 400)}…` : trimmed;
}
