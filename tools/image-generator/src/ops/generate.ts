import { promises as fs } from "node:fs";
import path from "node:path";

import { codexConfig, runImageRequest } from "../codex/client.js";
import type { CodexRequestBody, ImageGenerationTool, InputMessage } from "../codex/types.js";
import { logger } from "../util/log.js";

export interface GenerateOptions {
  prompt: string;
  output: string;
  size?: string;
  quality?: "standard" | "high" | "auto";
  background?: "transparent" | "opaque" | "auto";
  outputFormat?: "png" | "jpeg" | "webp";
  imageModel?: string;
  outerModel?: string;
}

export interface GenerateResult {
  pngPath: string;
  metaPath: string;
  meta: {
    op: "generate";
    prompt: string;
    requested_model: string;
    reported_model?: string;
    request_id?: string;
    media_type: string;
    timestamp: string;
    size?: string;
    quality?: string;
    background?: string;
    output_format?: string;
    source_events: string[];
  };
}

export async function generateImage(opts: GenerateOptions): Promise<GenerateResult> {
  const tool: ImageGenerationTool = {
    type: "image_generation",
    model: opts.imageModel ?? codexConfig.imageModel,
  };
  if (opts.size) tool.size = opts.size;
  if (opts.quality) tool.quality = opts.quality;
  if (opts.background) tool.background = opts.background;
  if (opts.outputFormat) tool.output_format = opts.outputFormat;

  const input: InputMessage[] = [
    { role: "user", content: opts.prompt },
  ];
  const body: CodexRequestBody = {
    model: opts.outerModel ?? codexConfig.outerModel,
    stream: true,
    store: false,
    tools: [tool],
    instructions: "Generate the image as described by the user.",
    input,
  };

  logger.info(`Generating image (model=${tool.model}, size=${tool.size ?? "default"})`);
  const image = await runImageRequest({ body });

  await writeOutput(opts.output, image.base64);
  const meta = {
    op: "generate" as const,
    prompt: opts.prompt,
    requested_model: tool.model ?? codexConfig.imageModel,
    reported_model: image.model,
    request_id: image.requestId,
    media_type: image.mediaType,
    timestamp: new Date().toISOString(),
    size: opts.size,
    quality: opts.quality,
    background: opts.background,
    output_format: opts.outputFormat,
    source_events: image.sourceEvents,
  };
  const metaPath = await writeMeta(opts.output, meta);
  return { pngPath: opts.output, metaPath, meta };
}

export async function writeOutput(outPath: string, base64: string): Promise<void> {
  await fs.mkdir(path.dirname(path.resolve(outPath)), { recursive: true });
  await fs.writeFile(outPath, Buffer.from(base64, "base64"));
}

export async function writeMeta(outPath: string, meta: object): Promise<string> {
  const metaPath = `${outPath}.meta.json`;
  await fs.writeFile(metaPath, JSON.stringify(meta, null, 2));
  return metaPath;
}
