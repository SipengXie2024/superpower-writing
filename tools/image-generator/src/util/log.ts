type Level = "debug" | "info" | "warn" | "error";

const LEVEL_ORDER: Record<Level, number> = {
  debug: 10,
  info: 20,
  warn: 30,
  error: 40,
};

function resolveMinLevel(): Level {
  const env = (process.env.IMAGE_GEN_LOG ?? "info").toLowerCase();
  if (env === "debug" || process.env.IMAGE_GEN_DEBUG === "1") return "debug";
  if (env === "warn") return "warn";
  if (env === "error") return "error";
  return "info";
}

const minLevel = resolveMinLevel();

function emit(level: Level, args: unknown[]): void {
  if (LEVEL_ORDER[level] < LEVEL_ORDER[minLevel]) return;
  const tag = `[image-gen ${level}]`;
  // All log output goes to stderr so stdout stays usable for piped data.
  // eslint-disable-next-line no-console
  console.error(tag, ...args);
}

export const logger = {
  debug: (...args: unknown[]) => emit("debug", args),
  info: (...args: unknown[]) => emit("info", args),
  warn: (...args: unknown[]) => emit("warn", args),
  error: (...args: unknown[]) => emit("error", args),
};

export function debugEnabled(): boolean {
  return minLevel === "debug";
}
