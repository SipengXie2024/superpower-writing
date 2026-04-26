import { promises as fs } from "node:fs";
import path from "node:path";

import { codexConfig, runTextRequest } from "../codex/client.js";
import type { CodexRequestBody, InputContent, InputMessage } from "../codex/types.js";
import { logger } from "../util/log.js";

export const DOC_TYPE_THRESHOLDS: Record<string, number> = {
  journal: 8.5,
  conference: 8.0,
  thesis: 8.0,
  grant: 8.0,
  preprint: 7.5,
  report: 7.5,
  poster: 7.0,
  presentation: 6.5,
};

const DEFAULT_THRESHOLD = 7.5;

const REVIEW_SYSTEM_PROMPT = `You are a scientific diagram quality reviewer. Analyze the provided diagram image.

Score on 5 criteria (0-2 points each, total 0-10):
- accuracy: correct representation of concepts, proper notation/symbols, accurate relationships
- clarity: easy to understand at a glance, clear visual hierarchy, no ambiguous elements
- labels: all important elements labeled, labels readable (appropriate font size), consistent labeling style
- layout: logical flow (top-to-bottom or left-to-right), balanced use of space, no overlapping elements
- appearance: publication-ready quality, clean crisp lines and shapes, appropriate colors/contrast

Respond with ONLY a JSON object (no markdown fences, no commentary outside the JSON):
{"scores":{"accuracy":<0-2>,"clarity":<0-2>,"labels":<0-2>,"layout":<0-2>,"appearance":<0-2>},"total":<0-10>,"strengths":["<strength>","..."],"issues":["<issue>","..."],"passes":<true|false>}

Quality threshold for this review: {THRESHOLD}/10. Set "passes" to true if total >= threshold, false otherwise.`;

export interface ReviewOptions {
  input: string;
  threshold?: number;
  docType?: string;
  customPrompt?: string;
  output?: string;
  outerModel?: string;
}

export interface ReviewResult {
  reviewPath: string;
  meta: {
    op: "review";
    input: string;
    threshold: number;
    doc_type: string;
    requested_model: string;
    reported_model?: string;
    request_id?: string;
    timestamp: string;
    review_text: string;
    review_json: Record<string, unknown> | null;
    passes?: boolean;
    total?: number;
    source_events: string[];
  };
}

export async function reviewImage(opts: ReviewOptions): Promise<ReviewResult> {
  const threshold =
    opts.threshold ??
    (opts.docType ? DOC_TYPE_THRESHOLDS[opts.docType] : undefined) ??
    DEFAULT_THRESHOLD;
  const docType = opts.docType ?? "default";

  // Read image as base64.
  const buf = await fs.readFile(opts.input);
  const ext = path.extname(opts.input).toLowerCase();
  const media =
    ext === ".jpg" || ext === ".jpeg"
      ? "image/jpeg"
      : ext === ".webp"
        ? "image/webp"
        : "image/png";

  const systemPrompt = opts.customPrompt
    ? opts.customPrompt.replace("{THRESHOLD}", String(threshold))
    : REVIEW_SYSTEM_PROMPT.replace("{THRESHOLD}", String(threshold));

  const content: InputContent[] = [
    {
      type: "input_text",
      text: "Review this scientific diagram.",
    },
    {
      type: "input_image",
      image_url: `data:${media};base64,${buf.toString("base64")}`,
      detail: "high",
    },
  ];

  const input: InputMessage[] = [{ role: "user", content }];
  const body: Omit<CodexRequestBody, "tools"> & { tools?: CodexRequestBody["tools"] } = {
    model: opts.outerModel ?? codexConfig.outerModel,
    stream: true,
    store: false,
    tools: [],
    instructions: systemPrompt,
    input,
  };

  logger.info(
    `Reviewing image (input=${path.basename(opts.input)}, threshold=${threshold}, docType=${docType})`,
  );

  const result = await runTextRequest({ body });

  // Try to parse the text as JSON (GPT may wrap in markdown fences).
  let reviewJson: Record<string, unknown> | null = null;
  const cleaned = result.text
    .replace(/^```(?:json)?\s*\n?/m, "")
    .replace(/\n?```\s*$/m, "")
    .trim();
  try {
    const parsed = JSON.parse(cleaned);
    if (typeof parsed === "object" && parsed !== null) {
      reviewJson = parsed as Record<string, unknown>;
    }
  } catch {
    logger.debug("Review response is not valid JSON, storing as raw text.");
  }

  const outputPath =
    opts.output ??
    `${opts.input.replace(/\.[^.]+$/, "")}_review.json`;

  const meta: ReviewResult["meta"] = {
    op: "review",
    input: path.resolve(opts.input),
    threshold,
    doc_type: docType,
    requested_model: codexConfig.outerModel,
    reported_model: result.model,
    request_id: result.requestId,
    timestamp: new Date().toISOString(),
    review_text: result.text,
    review_json: reviewJson,
    passes: typeof reviewJson?.passes === "boolean" ? reviewJson.passes : undefined,
    total: typeof reviewJson?.total === "number" ? reviewJson.total : undefined,
    source_events: result.sourceEvents,
  };

  await fs.writeFile(outputPath, JSON.stringify(meta, null, 2));
  logger.info(`Review: ${outputPath}`);

  return { reviewPath: outputPath, meta };
}
