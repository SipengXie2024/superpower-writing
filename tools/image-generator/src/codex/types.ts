export interface InputContentText {
  type: "input_text";
  text: string;
}

export interface InputContentImage {
  type: "input_image";
  image_url?: string;
  // Some Responses-API variants accept inline base64 via { image: { base64, media_type } }.
  // We pass it through in that nested shape and let the backend ignore unknown fields.
  image?: { base64: string; media_type: string };
  detail?: "auto" | "low" | "high";
}

export type InputContent = InputContentText | InputContentImage;

export interface InputMessage {
  role: "user" | "system";
  content: string | InputContent[];
}

export interface ImageGenerationTool {
  type: "image_generation";
  model?: string;
  size?: string;
  quality?: "standard" | "high" | "auto";
  background?: "transparent" | "opaque" | "auto";
  output_format?: "png" | "jpeg" | "webp";
  // Used by edit/variant flows: identify which input image to operate on.
  // Field name is best-guess; backend tolerates extras.
  input_image_index?: number;
  mask_image_index?: number;
}

export type Tool = ImageGenerationTool;

export interface CodexRequestBody {
  model: string;
  stream: true;
  tools: Tool[];
  input: InputMessage[];
  // Forwarded fields the backend recognizes; pass-through, don't validate.
  [extra: string]: unknown;
}

export interface ParsedImage {
  /** Base64-encoded image payload, no data: URI prefix. */
  base64: string;
  /** MIME type echoed by backend, e.g. "image/png". Falls back to "image/png". */
  mediaType: string;
  /** Model the backend reports having used. May or may not be set. */
  model?: string;
  /** Backend-assigned request id, when present. */
  requestId?: string;
  /** Original SSE event names that contributed to this image. Diagnostic. */
  sourceEvents: string[];
}

export interface ParsedText {
  /** Full text content from the model response. */
  text: string;
  /** Model the backend reports having used. */
  model?: string;
  /** Backend-assigned request id. */
  requestId?: string;
  /** Original SSE event names that contributed. Diagnostic. */
  sourceEvents: string[];
}
