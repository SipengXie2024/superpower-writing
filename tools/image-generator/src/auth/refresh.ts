import {
  isExpired,
  loadCredentials,
  saveCredentials,
  type StoredCredentials,
} from "./store.js";
import { AuthError } from "../util/errors.js";
import { logger } from "../util/log.js";

interface PiAiOAuthCredentials {
  refresh: string;
  access: string;
  expires: number;
  [key: string]: unknown;
}

type RefreshFn = (refreshToken: string) => Promise<PiAiOAuthCredentials>;

async function loadPiAiRefresh(): Promise<RefreshFn> {
  const mod = await import("@mariozechner/pi-ai/oauth");
  const fn = (mod as unknown as { refreshOpenAICodexToken?: RefreshFn })
    .refreshOpenAICodexToken;
  if (typeof fn !== "function") {
    throw new Error(
      "Installed @mariozechner/pi-ai/oauth does not export refreshOpenAICodexToken.",
    );
  }
  return fn;
}

export async function ensureFreshCredentials(): Promise<StoredCredentials> {
  const current = await loadCredentials();
  if (!current) {
    throw new AuthError(
      "no_credentials",
      "No saved credentials. Run `image-gen login` first.",
    );
  }
  if (!isExpired(current)) return current;

  logger.debug("access token expired; refreshing");
  const refreshFn = await loadPiAiRefresh();
  let refreshed: PiAiOAuthCredentials;
  try {
    refreshed = await refreshFn(current.refresh);
  } catch (err: unknown) {
    throw new AuthError(
      "refresh_failed",
      `Token refresh failed: ${err instanceof Error ? err.message : String(err)}. ` +
        "Run `image-gen login` again.",
      { cause: err },
    );
  }

  const stored: StoredCredentials = {
    refresh: refreshed.refresh,
    access: refreshed.access,
    expires: refreshed.expires,
    chatgpt_account_id:
      typeof refreshed.chatgpt_account_id === "string"
        ? refreshed.chatgpt_account_id
        : current.chatgpt_account_id,
  };
  await saveCredentials(stored);
  return stored;
}
