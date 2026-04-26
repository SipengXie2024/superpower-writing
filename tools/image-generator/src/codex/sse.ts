export interface SSEEvent {
  /** Event name from `event:` line, or "message" when absent. */
  event: string;
  /** Concatenated `data:` lines, joined by `\n`. May be empty string. */
  data: string;
  /** `id:` line if present. */
  id?: string;
}

/**
 * Async-iterate SSE events from a fetch body stream.
 *
 * Buffers bytes, splits on `\n\n` (event boundary per spec), then on `\n`
 * within an event for per-field parsing. Tolerant of `\r\n` line endings.
 * Stops cleanly at end of stream; throws on truncated final event only if the
 * caller asks for `strict`.
 */
export async function* parseSSE(
  body: ReadableStream<Uint8Array>,
  opts: { strict?: boolean } = {},
): AsyncGenerator<SSEEvent, void, void> {
  const reader = body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (value) buffer += decoder.decode(value, { stream: true });
      if (done) {
        buffer += decoder.decode();
        if (buffer.length > 0) {
          if (opts.strict) {
            throw new Error("SSE stream ended mid-event");
          }
          const event = parseEventBlock(buffer);
          if (event) yield event;
        }
        return;
      }

      let boundary = findBoundary(buffer);
      while (boundary !== -1) {
        const block = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + boundaryLength(buffer, boundary));
        const event = parseEventBlock(block);
        if (event) yield event;
        boundary = findBoundary(buffer);
      }
    }
  } finally {
    reader.releaseLock();
  }
}

function findBoundary(buf: string): number {
  const a = buf.indexOf("\n\n");
  const b = buf.indexOf("\r\n\r\n");
  if (a === -1) return b;
  if (b === -1) return a;
  return Math.min(a, b);
}

function boundaryLength(buf: string, idx: number): number {
  return buf.startsWith("\r\n\r\n", idx) ? 4 : 2;
}

function parseEventBlock(block: string): SSEEvent | null {
  if (!block) return null;
  let event = "message";
  let id: string | undefined;
  const dataLines: string[] = [];

  for (const rawLine of block.split(/\r?\n/)) {
    if (!rawLine || rawLine.startsWith(":")) continue;
    const sep = rawLine.indexOf(":");
    const field = sep === -1 ? rawLine : rawLine.slice(0, sep);
    let value = sep === -1 ? "" : rawLine.slice(sep + 1);
    if (value.startsWith(" ")) value = value.slice(1);
    switch (field) {
      case "event":
        event = value;
        break;
      case "data":
        dataLines.push(value);
        break;
      case "id":
        id = value;
        break;
      default:
        // ignore unknown fields per SSE spec
        break;
    }
  }

  if (dataLines.length === 0) return null;
  return { event, data: dataLines.join("\n"), id };
}
