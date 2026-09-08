#!/usr/bin/env python3
"""Generate or edit a figure PNG through a sub2api gateway (OpenAI Images API shape).

  imagegen.py generate --prompt-file brief.txt --out fig.png [--count 3]
  imagegen.py edit --image fig.png --prompt "..." --out fig-v2.png

Every saved PNG gets a sidecar <stem>.imagegen.json holding the request and the
backend's response metadata (revised_prompt, usage, actual size) for provenance.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DEFAULT_BASE = "http://127.0.0.1:7234"
DEFAULT_MODEL = "gpt-image-2"
USER_AGENT = "superpower-writing-imagegen/1.0"


def token() -> str:
    for name in ("SUB2API_TOKEN", "CC_BBD_SH_TOKEN"):
        if os.environ.get(name):
            return os.environ[name]
    sys.exit("error: set SUB2API_TOKEN to a sub2api API key")


def base_url() -> str:
    return os.environ.get("SUB2API_BASE_URL", DEFAULT_BASE).rstrip("/")


def post(path: str, body: bytes, content_type: str, timeout: int, retries: int) -> dict:
    req = urllib.request.Request(
        base_url() + path,
        data=body,
        method="POST",
        headers={
            "Authorization": "Bearer " + token(),
            "Content-Type": content_type,
            "User-Agent": USER_AGENT,
        },
    )
    attempt = 0
    while True:
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:500]
            if exc.code < 500 or attempt >= retries:
                sys.exit(f"error: HTTP {exc.code} from {path}: {detail}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt >= retries:
                sys.exit(f"error: {path} failed after {attempt + 1} attempt(s): {exc}")
        attempt += 1
        time.sleep(5)


def multipart(fields: dict, files: dict) -> tuple[bytes, str]:
    boundary = "----imagegen" + uuid.uuid4().hex
    chunks = []
    for name, value in fields.items():
        chunks.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
        )
    for name, path in files.items():
        chunks.append(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; "
            f"filename=\"{path.name}\"\r\nContent-Type: image/png\r\n\r\n".encode()
        )
        chunks.append(path.read_bytes())
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def save(response: dict, out: Path, request: dict, started: float) -> None:
    items = response.get("data") or []
    if not items:
        sys.exit(f"error: no image in response: {json.dumps(response)[:500]}")
    item = items[0]
    if item.get("b64_json"):
        png = base64.b64decode(item["b64_json"])
    elif item.get("url"):
        png = urllib.request.urlopen(item["url"], timeout=120).read()
    else:
        sys.exit(f"error: image item has neither b64_json nor url: {list(item)}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(png)
    meta = {k: v for k, v in response.items() if k != "data"}
    meta["revised_prompt"] = item.get("revised_prompt")
    sidecar = out.with_name(out.stem + ".imagegen.json")
    sidecar.write_text(json.dumps({"request": request, "response": meta}, indent=2, ensure_ascii=False))
    actual = meta.get("size", "?")
    note = ""
    if request.get("size") and actual != request["size"]:
        note = f"  (backend ignored size={request['size']}; state the aspect ratio in the prompt)"
    print(f"OK {out}  {actual}  {time.time() - started:.1f}s{note}")


def read_prompt(args) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text()
    if args.prompt:
        return args.prompt
    sys.exit("error: give --prompt-file or --prompt")


def cmd_generate(args) -> None:
    prompt = read_prompt(args)
    body = {"model": args.model, "prompt": prompt, "n": 1}
    for key in ("size", "quality"):
        if getattr(args, key):
            body[key] = getattr(args, key)
    out = Path(args.out)
    outs = [out] if args.count == 1 else [
        out.with_name(f"{out.stem}-{i}{out.suffix}") for i in range(1, args.count + 1)
    ]

    def one(target: Path) -> None:
        started = time.time()
        resp = post("/v1/images/generations", json.dumps(body).encode(), "application/json",
                    args.timeout, args.retries)
        save(resp, target, {"endpoint": "generations", **body}, started)

    with ThreadPoolExecutor(max_workers=len(outs)) as pool:
        list(pool.map(one, outs))


def cmd_edit(args) -> None:
    prompt = read_prompt(args)
    image = Path(args.image)
    if not image.is_file():
        sys.exit(f"error: no such image: {image}")
    fields = {"model": args.model, "prompt": prompt, "n": "1"}
    if args.size:
        fields["size"] = args.size
    if args.quality:
        fields["quality"] = args.quality
    body, ctype = multipart(fields, {"image": image})
    started = time.time()
    resp = post("/v1/images/edits", body, ctype, args.timeout, args.retries)
    save(resp, Path(args.out), {"endpoint": "edits", "image": str(image), **fields}, started)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, fn in (("generate", cmd_generate), ("edit", cmd_edit)):
        p = sub.add_parser(name)
        p.add_argument("--prompt-file")
        p.add_argument("--prompt")
        p.add_argument("--out", required=True)
        p.add_argument("--model", default=DEFAULT_MODEL)
        p.add_argument("--size", help="e.g. 1536x1024; subscription backends may ignore it")
        p.add_argument("--quality", choices=["low", "medium", "high", "auto"])
        p.add_argument("--timeout", type=int, default=600)
        p.add_argument("--retries", type=int, default=1)
        p.set_defaults(fn=fn)
        if name == "generate":
            p.add_argument("--count", type=int, default=1, help="parallel attempts, saved as <stem>-1..N")
        else:
            p.add_argument("--image", required=True)
    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
