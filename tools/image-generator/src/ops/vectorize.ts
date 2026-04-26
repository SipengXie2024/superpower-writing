import { spawn } from "node:child_process";
import { promises as fs } from "node:fs";
import path from "node:path";

import { MissingBinaryError } from "../util/errors.js";
import { logger } from "../util/log.js";

export interface VectorizeOptions {
  input: string;
  output: string;
  threshold?: number;
  /** Override the binary name; defaults to "potrace". */
  potraceBin?: string;
}

export interface VectorizeResult {
  svgPath: string;
}

async function which(bin: string): Promise<boolean> {
  return await new Promise<boolean>((resolve) => {
    const child = spawn("sh", ["-c", `command -v ${bin}`], { stdio: "ignore" });
    child.on("close", (code) => resolve(code === 0));
    child.on("error", () => resolve(false));
  });
}

/**
 * potrace consumes monochrome bitmap formats (PBM/PGM/BMP). For PNG input we
 * pipe through ImageMagick's `convert` if available, falling back to an error
 * with installation guidance.
 */
async function ensureMagick(): Promise<string> {
  for (const cand of ["magick", "convert"]) {
    if (await which(cand)) return cand;
  }
  throw new MissingBinaryError(
    "magick",
    "Install ImageMagick (apt install imagemagick) — needed to convert PNG → PBM for potrace.",
  );
}

export async function vectorize(opts: VectorizeOptions): Promise<VectorizeResult> {
  const bin = opts.potraceBin ?? "potrace";
  if (!(await which(bin))) {
    throw new MissingBinaryError(
      bin,
      "Install with: apt install potrace (Debian/Ubuntu) or brew install potrace (macOS).",
    );
  }
  const magick = await ensureMagick();

  const inputAbs = path.resolve(opts.input);
  const outputAbs = path.resolve(opts.output);
  await fs.mkdir(path.dirname(outputAbs), { recursive: true });

  const threshold = opts.threshold ?? 128;
  const tmpPbm = `${outputAbs}.tmp.pbm`;
  logger.debug(`Converting ${inputAbs} → ${tmpPbm} (threshold=${threshold})`);
  await runOrThrow(magick, [
    inputAbs,
    "-colorspace",
    "Gray",
    "-threshold",
    `${threshold}`,
    tmpPbm,
  ]);

  logger.debug(`potrace ${tmpPbm} → ${outputAbs}`);
  await runOrThrow(bin, ["-s", "-o", outputAbs, tmpPbm]);

  await fs.unlink(tmpPbm).catch(() => undefined);
  return { svgPath: outputAbs };
}

function runOrThrow(cmd: string, args: string[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: ["ignore", "pipe", "pipe"] });
    let stderr = "";
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });
    child.on("error", (err) => reject(err));
    child.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`${cmd} exited with code ${code}: ${stderr.trim()}`));
    });
  });
}
