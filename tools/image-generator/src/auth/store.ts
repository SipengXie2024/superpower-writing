import { promises as fs } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";

export interface StoredCredentials {
  refresh: string;
  access: string;
  expires: number;
  chatgpt_account_id?: string;
}

const TOKEN_DIR = path.join(homedir(), ".config", "superpower-writing");
const TOKEN_FILE = path.join(TOKEN_DIR, "codex-tokens.json");
const TOKEN_FILE_MODE = 0o600;
const TOKEN_DIR_MODE = 0o700;

export const tokenFilePath = (): string => TOKEN_FILE;

export async function loadCredentials(): Promise<StoredCredentials | null> {
  try {
    const raw = await fs.readFile(TOKEN_FILE, "utf8");
    const parsed = JSON.parse(raw) as Partial<StoredCredentials>;
    if (
      typeof parsed.refresh !== "string" ||
      typeof parsed.access !== "string" ||
      typeof parsed.expires !== "number"
    ) {
      throw new Error(`token file ${TOKEN_FILE} is malformed`);
    }
    return {
      refresh: parsed.refresh,
      access: parsed.access,
      expires: parsed.expires,
      chatgpt_account_id:
        typeof parsed.chatgpt_account_id === "string" ? parsed.chatgpt_account_id : undefined,
    };
  } catch (err: unknown) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return null;
    throw err;
  }
}

export async function saveCredentials(creds: StoredCredentials): Promise<void> {
  await fs.mkdir(TOKEN_DIR, { recursive: true, mode: TOKEN_DIR_MODE });
  // chmod existing dir too — mkdir's mode is honored only on creation.
  await fs.chmod(TOKEN_DIR, TOKEN_DIR_MODE).catch(() => undefined);
  const payload = JSON.stringify(creds, null, 2);
  await fs.writeFile(TOKEN_FILE, payload, { mode: TOKEN_FILE_MODE });
  await fs.chmod(TOKEN_FILE, TOKEN_FILE_MODE);
}

export async function deleteCredentials(): Promise<boolean> {
  try {
    await fs.unlink(TOKEN_FILE);
    return true;
  } catch (err: unknown) {
    if ((err as NodeJS.ErrnoException).code === "ENOENT") return false;
    throw err;
  }
}

export function isExpired(creds: StoredCredentials, skewMs = 60_000): boolean {
  return Date.now() >= creds.expires - skewMs;
}

export function redactedSummary(creds: StoredCredentials): {
  account_id: string | null;
  expires_at: string;
  expires_in_seconds: number;
  access_token_preview: string;
} {
  const head = creds.access.slice(0, 6);
  const tail = creds.access.slice(-4);
  return {
    account_id: creds.chatgpt_account_id ?? null,
    expires_at: new Date(creds.expires).toISOString(),
    expires_in_seconds: Math.round((creds.expires - Date.now()) / 1000),
    access_token_preview: `${head}…${tail}`,
  };
}
