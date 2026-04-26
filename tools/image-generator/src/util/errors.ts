export type AuthErrorKind =
  | "no_credentials"
  | "refresh_failed"
  | "unauthorized";

export class AuthError extends Error {
  readonly kind: AuthErrorKind;
  constructor(kind: AuthErrorKind, message: string, opts?: { cause?: unknown }) {
    super(message, opts);
    this.name = "AuthError";
    this.kind = kind;
  }
}

export class CodexApiError extends Error {
  readonly status: number;
  readonly bodyPreview: string;
  constructor(status: number, bodyPreview: string, opts?: { cause?: unknown }) {
    super(`Codex backend returned HTTP ${status}: ${bodyPreview}`, opts);
    this.name = "CodexApiError";
    this.status = status;
    this.bodyPreview = bodyPreview;
  }
}

export class StreamParseError extends Error {
  constructor(message: string, opts?: { cause?: unknown }) {
    super(message, opts);
    this.name = "StreamParseError";
  }
}

export class MissingBinaryError extends Error {
  readonly binary: string;
  constructor(binary: string, hint: string) {
    super(`Required binary "${binary}" not found on PATH. ${hint}`);
    this.name = "MissingBinaryError";
    this.binary = binary;
  }
}
