import { promises as fs } from "node:fs";
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

export interface EditOptions {
  prompt: string;
  input: string;
  mask?: string;
  output: string;
  size?: string;
  quality?: "standard" | "high" | "auto";
  imageModel?: string;
  outerModel?: string;
}

export interface EditResult {
  pngPath: string;
  metaPath: string;
  meta: Record<string, unknown>;
}

async function readAsBase64(filePath: string): Promise<{ base64: string; media: string }> {
  const buf = await fs.readFile(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const media =
    ext === ".jpg" || ext === ".jpeg"
      ? "image/jpeg"
      : ext === ".webp"
        ? "image/webp"
        : "image/png";
  return { base64: buf.toString("base64"), media };
}

export async function editImage(opts: EditOptions): Promise<EditResult> {
  const tool: ImageGenerationTool = {
    type: "image_generation",
    model: opts.imageModel ?? codexConfig.imageModel,
    input_image_index: 0,
  };
  if (opts.size) tool.size = opts.size;
  if (opts.quality) tool.quality = opts.quality;

  const inputImage = await readAsBase64(opts.input);
  const content: InputContent[] = [
    { type: "input_text", text: opts.prompt },
    {
      type: "input_image",
      image: { base64: inputImage.base64, media_type: inputImage.media },
      detail: "high",
    },
  ];

  if (opts.mask) {
    const maskImage = await readAsBase64(opts.mask);
    tool.mask_image_index = 1;
    content.push({
      type: "input_image",
      image: { base64: maskImage.base64, media_type: maskImage.media },
      detail: "high",
    });
  }

  const messages: InputMessage[] = [{ role: "user", content }];
  const body: CodexRequestBody = {
    model: opts.outerModel ?? codexConfig.outerModel,
    stream: true,
    store: false,
    tools: [tool],
    instructions: "Edit the image as described by the user.",
    input: messages,
  };

  logger.info(
    `Editing image (input=${path.basename(opts.input)}` +
      (opts.mask ? `, mask=${path.basename(opts.mask)}` : "") +
      `)`,
  );
  const image = await runImageRequest({ body });

  await writeOutput(opts.output, image.base64);
  const meta = {
    op: "edit" as const,
    prompt: opts.prompt,
    input: path.resolve(opts.input),
    mask: opts.mask ? path.resolve(opts.mask) : null,
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
