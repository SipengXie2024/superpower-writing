#!/usr/bin/env node
import { Command } from "commander";

import { runLogin } from "./auth/login.js";
import { deleteCredentials, loadCredentials, redactedSummary } from "./auth/store.js";
import { generateImage } from "./ops/generate.js";
import { editImage } from "./ops/edit.js";
import { variantImage } from "./ops/variant.js";
import { vectorize } from "./ops/vectorize.js";
import { AuthError, CodexApiError, MissingBinaryError, StreamParseError } from "./util/errors.js";
import { logger } from "./util/log.js";

const program = new Command();
program.name("image-gen").description("Generate and edit paper figures via OpenAI Codex (gpt-image-2)").version("0.1.0");

// ── login ──────────────────────────────────────────────────────────────
program
  .command("login")
  .description("Authenticate with OpenAI via PKCE (opens browser)")
  .option("--no-browser", "Print the URL instead of opening a browser")
  .action(async (opts: { browser: boolean }) => {
    await handle(runLogin({ noBrowser: !opts.browser }).then(async (creds) => {
      const summary = redactedSummary(creds);
      logger.info("Login successful.");
      logger.info(`  Account: ${summary.account_id ?? "(unknown)"}`);
      logger.info(`  Token expires at: ${summary.expires_at}`);
    }));
  });

// ── logout ─────────────────────────────────────────────────────────────
program
  .command("logout")
  .description("Delete saved credentials")
  .action(async () => {
    await handle((async () => {
      const deleted = await deleteCredentials();
      logger.info(deleted ? "Credentials deleted." : "No saved credentials found.");
    })());
  });

// ── status ─────────────────────────────────────────────────────────────
program
  .command("status")
  .description("Show credential status (token redacted)")
  .action(async () => {
    await handle((async () => {
      const creds = await loadCredentials();
      if (!creds) {
        logger.info("No saved credentials. Run `image-gen login` first.");
        return;
      }
      const s = redactedSummary(creds);
      logger.info(`Account:        ${s.account_id ?? "(unknown)"}`);
      logger.info(`Access token:   ${s.access_token_preview}`);
      logger.info(`Expires at:     ${s.expires_at}`);
      logger.info(`Expires in:     ${s.expires_in_seconds}s`);
    })());
  });

// ── generate ───────────────────────────────────────────────────────────
program
  .command("generate")
  .description("Generate an image from a text prompt")
  .requiredOption("-p, --prompt <text>", "Image generation prompt")
  .requiredOption("-o, --output <path>", "Output PNG path")
  .option("--size <WxH>", "Image size (e.g. 1024x1024)")
  .option("--quality <level>", "Quality: standard | high | auto", "standard")
  .option("--background <bg>", "Background: transparent | opaque | auto")
  .option("--format <fmt>", "Output format: png | jpeg | webp", "png")
  .action(async (opts: {
    prompt: string;
    output: string;
    size?: string;
    quality: string;
    background?: string;
    format: string;
  }) => {
    await handle(
      generateImage({
        prompt: opts.prompt,
        output: opts.output,
        size: opts.size,
        quality: opts.quality as "standard" | "high" | "auto",
        background: opts.background as "transparent" | "opaque" | "auto" | undefined,
        outputFormat: opts.format as "png" | "jpeg" | "webp",
      }).then((r) => {
        logger.info(`Generated: ${r.pngPath}`);
        logger.info(`Metadata:  ${r.metaPath}`);
      }),
    );
  });

// ── edit ───────────────────────────────────────────────────────────────
program
  .command("edit")
  .description("Edit an image with a prompt and optional mask")
  .requiredOption("-i, --input <path>", "Source image")
  .requiredOption("-p, --prompt <text>", "Edit instructions")
  .requiredOption("-o, --output <path>", "Output PNG path")
  .option("-m, --mask <path>", "Mask image (white=edit, black=keep)")
  .option("--size <WxH>", "Image size")
  .option("--quality <level>", "Quality: standard | high | auto", "standard")
  .action(async (opts: {
    input: string;
    prompt: string;
    output: string;
    mask?: string;
    size?: string;
    quality: string;
  }) => {
    await handle(
      editImage({
        prompt: opts.prompt,
        input: opts.input,
        mask: opts.mask,
        output: opts.output,
        size: opts.size,
        quality: opts.quality as "standard" | "high" | "auto",
      }).then((r) => {
        logger.info(`Edited:  ${r.pngPath}`);
        logger.info(`Metadata: ${r.metaPath}`);
      }),
    );
  });

// ── variant ────────────────────────────────────────────────────────────
program
  .command("variant")
  .description("Create a variant of an image with a new prompt")
  .requiredOption("-i, --input <path>", "Source image")
  .requiredOption("-p, --prompt <text>", "Style / variant instructions")
  .requiredOption("-o, --output <path>", "Output PNG path")
  .option("--size <WxH>", "Image size")
  .option("--quality <level>", "Quality: standard | high | auto", "standard")
  .action(async (opts: {
    input: string;
    prompt: string;
    output: string;
    size?: string;
    quality: string;
  }) => {
    await handle(
      variantImage({
        prompt: opts.prompt,
        input: opts.input,
        output: opts.output,
        size: opts.size,
        quality: opts.quality as "standard" | "high" | "auto",
      }).then((r) => {
        logger.info(`Variant:  ${r.pngPath}`);
        logger.info(`Metadata: ${r.metaPath}`);
      }),
    );
  });

// ── vectorize ──────────────────────────────────────────────────────────
program
  .command("vectorize")
  .description("Convert a PNG to SVG via potrace (best for line art)")
  .requiredOption("-i, --input <path>", "Source PNG")
  .requiredOption("-o, --output <path>", "Output SVG path")
  .option("--threshold <n>", "Binarization threshold (0–255)", parseInt, 128)
  .action(async (opts: { input: string; output: string; threshold: number }) => {
    await handle(
      vectorize({
        input: opts.input,
        output: opts.output,
        threshold: opts.threshold,
      }).then((r) => {
        logger.info(`Vectorized: ${r.svgPath}`);
      }),
    );
  });

// ── error handling ─────────────────────────────────────────────────────

const EXIT_AUTH = 3;
const EXIT_API = 4;
const EXIT_STREAM = 5;
const EXIT_BINARY = 6;

async function handle(promise: Promise<void>): Promise<void> {
  try {
    await promise;
  } catch (err: unknown) {
    if (err instanceof AuthError) {
      logger.error(err.message);
      process.exit(EXIT_AUTH);
    }
    if (err instanceof CodexApiError) {
      logger.error(`Codex API error (HTTP ${err.status}): ${err.bodyPreview}`);
      process.exit(EXIT_API);
    }
    if (err instanceof StreamParseError) {
      logger.error(`Stream parse error: ${err.message}`);
      process.exit(EXIT_STREAM);
    }
    if (err instanceof MissingBinaryError) {
      logger.error(err.message);
      process.exit(EXIT_BINARY);
    }
    logger.error(err instanceof Error ? err.message : String(err));
    if (err instanceof Error && err.stack) {
      logger.debug(err.stack);
    }
    process.exit(1);
  }
}

program.parse();
