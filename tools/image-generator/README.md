# image-generator

Standalone Node/TypeScript tool for generating paper illustrations and beautifying
evaluation figures via the OpenAI Codex backend (`gpt-image-2`).

This is **internal infrastructure** for the `superpower-writing` plugin. It is not a
slash command or skill. Other scripts and (eventually) the drafting workflow will call
the CLI or import from `dist/index.js` directly.

## Auth model

Uses the reverse-engineered Codex OAuth flow against `auth.openai.com` (PKCE on a
local callback at `127.0.0.1:1455`). Requires a ChatGPT Plus/Pro account. Tokens are
stored at `~/.config/superpower-writing/codex-tokens.json` with file mode `0600` and
auto-refreshed on every call.

The OAuth pieces are reused verbatim from `@mariozechner/pi-ai` (MIT). Image
generation is a thin custom client because pi-ai does not expose the
`image_generation` builtin tool.

## Stability disclaimer

The Codex backend is not a public OpenAI surface. Authentication, request shapes, and
streaming event names can change without notice and the path may be shut down at any
time. If that happens this tool stops working until the new shape is reverse-
engineered or until we add a fallback to the official Images API.

## Setup

```sh
cd tools/image-generator
npm install
npm run build
```

First run requires an interactive browser login:

```sh
node dist/cli.js login
```

This opens a browser, completes PKCE, and writes the token file.

## CLI

```
image-gen login                                                  # one-time login
image-gen logout                                                 # delete token file
image-gen status                                                 # token expiry, account id (token redacted)

image-gen generate --prompt "..." --output figures/foo.png \
                   [--size 1024x1024] [--quality standard|high] \
                   [--background transparent]

image-gen edit --input src.png --mask mask.png --prompt "..." \
               --output dst.png

image-gen variant --input src.png \
                  --prompt "redraw in flat line-art style" \
                  --output dst.png

image-gen vectorize --input src.png --output dst.svg [--threshold 128]
```

`generate`, `edit`, and `variant` write a sidecar `<output>.meta.json` containing the
prompt, model echoed by the response, timestamp, and request id.

## Library API

For in-process consumers:

```ts
import {
  generateImage,
  editImage,
  variantImage,
  vectorize,
  ensureAuth,
} from "@superpower-writing/image-generator";

await generateImage({
  prompt: "minimalist diagram of a transformer block",
  output: "figures/transformer.png",
});
```

## Vectorize

`vectorize` shells out to the `potrace` binary. Install via your package manager
(`apt install potrace` on Debian/Ubuntu). It is best-effort: works well on line art and
diagrams with clean edges, poorly on photographic or gradient-heavy images.

## File layout

```
src/
  index.ts                # public Node API
  cli.ts                  # commander entry
  auth/{login,refresh,store}.ts
  codex/{client,sse,types}.ts
  ops/{generate,edit,variant,vectorize}.ts
  util/{log,errors}.ts
```

## Where things live at runtime

| What                     | Path                                                       |
|--------------------------|------------------------------------------------------------|
| Tokens                   | `~/.config/superpower-writing/codex-tokens.json` (mode 600) |
| SSE diagnostic dumps     | `$TMPDIR/image-gen-sse-<unix>.log` (only when `IMAGE_GEN_DEBUG=1`) |
| Per-image metadata       | sidecar `<output>.meta.json`                               |
