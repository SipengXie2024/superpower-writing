import path from "node:path";

import { codexConfig, runImageRequest } from "../codex/client.js";
import type {
  CodexRequestBody,
  ImageGenerationTool,
  InputContent,
  InputMessage,
} from "../codex/types.js";
import { logger } from "../util/log.js";
import { writeMeta, writeOutput } from "./generate.js";
import { promises as fs } from "node:fs";

export interface VariantOptions {
  prompt: string;
  input: string;
  output: string;
  size?: string;
  quality?: "standard" | "high" | "auto";
  imageModel?: string;
  outerModel?: string;
}

export interface VariantResult {
  pngPath: string;
  metaPath: string;
  meta: Record<string, unknown>;
}

export async function variantImage(opts: VariantOptions): Promise<VariantResult> {
  const tool: ImageGenerationTool = {
    type: "image_generation",
    model: opts.imageModel ?? codexConfig.imageModel,
    input_image_index: 0,
  };
  if (opts.size) tool.size = opts.size;
  if (opts.quality) tool.quality = opts.quality;

  const buf = await fs.readFile(opts.input);
  const ext = path.extname(opts.input).toLowerCase();
  const media =
    ext === ".jpg" || ext === ".jpeg"
      ? "image/jpeg"
      : ext === ".webp"
        ? "image/webp"
        : "image/png";

  const content: InputContent[] = [
    { type: "input_text", text: opts.prompt },
    {
      type: "input_image",
      image: { base64: buf.toString("base64"), media_type: media },
      detail: "high",
    },
  ];
  const messages: InputMessage[] = [{ role: "user", content }];
  const body: CodexRequestBody = {
    model: opts.outerModel ?? codexConfig.outerModel,
    stream: true,
    store: false,
    tools: [tool],
    instructions: "Create a variant of the image as described by the user.",
    input: messages,
  };

  logger.info(`Generating variant (input=${path.basename(opts.input)})`);
  const image = await runImageRequest({ body });

  await writeOutput(opts.output, image.base64);
  const meta = {
    op: "variant" as const,
    prompt: opts.prompt,
    input: path.resolve(opts.input),
    requested_model: tool.model,
    reported_model: image.model,
    request_id: image.requestId,
    media_type: image.mediaType,
    timestamp: new Date().toISOString(),
    size: opts.size,
    quality: opts.quality,
    source_events: image.sourceEvents,
  };
  const metaPath = await writeMeta(opts.output, meta);
  return { pngPath: opts.output, metaPath, meta };
}
