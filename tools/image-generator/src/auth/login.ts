import { spawn } from "node:child_process";
import { createInterface } from "node:readline/promises";
import { stdin, stdout } from "node:process";

import { saveCredentials, type StoredCredentials } from "./store.js";
import { logger } from "../util/log.js";

interface PiAiOAuthCredentials {
  refresh: string;
  access: string;
  expires: number;
  [key: string]: unknown;
}

interface LoginOptions {
  onAuth(info: { url: string; instructions?: string }): void;
  onPrompt(prompt: { message: string; secret?: boolean }): Promise<string>;
  onProgress?(message: string): void;
  onManualCodeInput?(): Promise<string>;
  originator?: string;
}

type LoginFn = (options: LoginOptions) => Promise<PiAiOAuthCredentials>;

async function loadPiAi(): Promise<{ login: LoginFn }> {
  const mod = await import("@mariozechner/pi-ai/oauth");
  const login = (mod as unknown as { loginOpenAICodex?: LoginFn }).loginOpenAICodex;
  if (typeof login !== "function") {
    throw new Error(
      "Installed @mariozechner/pi-ai/oauth does not export loginOpenAICodex. " +
        "Pin the dependency to ^0.70.2 or update the wrapper.",
    );
  }
  return { login };
}

function openBrowser(url: string): void {
  const platform = process.platform;
  const cmd =
    platform === "darwin" ? "open" : platform === "win32" ? "start" : "xdg-open";
  try {
    const child = spawn(cmd, [url], { detached: true, stdio: "ignore" });
    child.unref();
  } catch {
    // best-effort; the URL is also printed for manual copy.
  }
}

export interface RunLoginOptions {
  noBrowser?: boolean;
}

export async function runLogin(
  opts: RunLoginOptions = {},
): Promise<StoredCredentials> {
  const { login } = await loadPiAi();
  const rl = createInterface({ input: stdin, output: stdout });
  try {
    const creds = await login({
      onAuth: ({ url, instructions }) => {
        logger.info("Open this URL in a browser to authorize:");
        logger.info(url);
        if (instructions) logger.info(instructions);
        if (!opts.noBrowser) openBrowser(url);
      },
      onPrompt: async ({ message }) => rl.question(`${message} `),
      onProgress: (msg) => logger.debug(msg),
      onManualCodeInput: async () =>
        rl.question("Paste the authorization code from the browser: "),
      originator: "superpower-writing",
    });

    const stored: StoredCredentials = {
      refresh: creds.refresh,
      access: creds.access,
      expires: creds.expires,
      chatgpt_account_id:
        typeof creds.chatgpt_account_id === "string"
          ? creds.chatgpt_account_id
          : undefined,
    };
    await saveCredentials(stored);
    return stored;
  } finally {
    rl.close();
  }
}
