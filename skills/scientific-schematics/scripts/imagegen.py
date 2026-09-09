#!/usr/bin/env python3
"""Generate or edit a figure PNG with the Codex CLI's built-in image tool.

  imagegen.py generate --prompt-file brief.txt --out fig.png [--count 3]
  imagegen.py edit --image fig-2.png --prompt "..." --out fig.png

Each call is one non-interactive `codex exec` turn: Codex calls its image_gen
tool (gpt-image-2 on the ChatGPT subscription), copies the PNG to --out, and
the script writes a sidecar <stem>.imagegen.json holding the Codex thread id
(`edit` resumes that thread so the model still sees the original image), the
prompt Codex actually sent to the image model, the size, and the wall time.
"""
import argparse
import functools
import glob
import json
import os
import struct
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))

GENERATE_TASK = """Generate exactly one image with the built-in image_gen tool. Pass the prompt \
below to the tool verbatim: do not rewrite, shorten, or expand it, and do not read any skill \
files first. Then copy the generated PNG to {out} (create parent directories as needed) and \
reply with only that absolute path.

PROMPT:
{prompt}"""

EDIT_TASK = """Edit the {which} with the built-in image_gen tool, applying exactly this change \
and nothing else:

{prompt}

Keep every other element, label, color, position, arrow, and the canvas size exactly as in \
that image. Copy the edited PNG to {out} (create parent directories as needed) and reply \
with only that absolute path."""


@functools.lru_cache(maxsize=None)
def codex_version() -> str:
    try:
        return subprocess.run(["codex", "--version"], capture_output=True, text=True).stdout.strip()
    except FileNotFoundError:
        sys.exit("error: codex CLI not found on PATH")


def png_size(path: Path) -> str:
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit(f"error: {path} is not a PNG")
    width, height = struct.unpack(">II", head[16:24])
    return f"{width}x{height}"


def sidecar_for(image: Path) -> Path:
    return image.with_name(image.stem + ".imagegen.json")


def image_gen_provenance(thread_id: str) -> dict:
    """The last completed image_gen item in the thread's rollout file."""
    pattern = str(CODEX_HOME / "sessions" / "*" / "*" / "*" / f"rollout-*-{thread_id}.jsonl")
    last: dict = {}
    for rollout in glob.glob(pattern):
        with open(rollout, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if '"image_gen.generation"' not in line:
                    continue
                item = json.loads(line).get("payload", {}).get("item", {})
                if item.get("kind") == "image_gen.generation" and item.get("status") == "completed":
                    last = {"image_gen_id": item.get("id"), "revised_prompt": item.get("revisedPrompt")}
    return last


def run_codex(task: str, out: Path, timeout: int, resume: str | None, attach: Path | None) -> str:
    cmd = ["codex", "exec"]
    if attach:
        # -i takes a list of files, so it must sit before a flag that ends the list
        cmd += ["-i", str(attach)]
    cmd += ["--json", "--color", "never", "--skip-git-repo-check",
            "-C", os.getcwd(), "-s", "workspace-write", "--add-dir", str(out.parent),
            "-c", 'model_reasoning_effort="low"']
    if resume:
        cmd += ["resume", resume]
    cmd.append(task)
    out.unlink(missing_ok=True)
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              stdin=subprocess.DEVNULL)
    except FileNotFoundError:
        sys.exit("error: codex CLI not found on PATH")
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"codex exec timed out after {timeout}s")
    thread_id, last_message = resume or "", ""
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "thread.started":
            thread_id = event.get("thread_id", thread_id)
        item = event.get("item") or {}
        if event.get("type") == "item.completed" and item.get("type") == "agent_message":
            last_message = item.get("text", "")
    if proc.returncode != 0:
        raise RuntimeError(f"codex exec exited {proc.returncode}: {proc.stderr.strip()[-800:]}")
    if not out.is_file():
        raise RuntimeError(f"codex finished but {out} does not exist; its last message: {last_message[-800:]}")
    return thread_id


def attempt(task: str, out: Path, args, resume: str | None = None, attach: Path | None = None) -> str:
    for n in range(args.retries + 1):
        try:
            return run_codex(task, out, args.timeout, resume, attach)
        except RuntimeError as exc:
            if n >= args.retries:
                sys.exit(f"error: {exc}")
            print(f"retrying after: {exc}", file=sys.stderr)
    raise AssertionError("unreachable")


def save(out: Path, request: dict, thread_id: str, started: float) -> None:
    size = png_size(out)
    seconds = round(time.time() - started, 1)
    record = {"backend": "codex-cli", "codex_version": codex_version(), "thread_id": thread_id,
              "request": request, "size": size, "seconds": seconds, **image_gen_provenance(thread_id)}
    sidecar_for(out).write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    print(f"OK {out}  {size}  {seconds}s  thread={thread_id}")


def read_prompt(args) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text()
    if args.prompt:
        return args.prompt
    sys.exit("error: give --prompt-file or --prompt")


def cmd_generate(args) -> None:
    prompt = read_prompt(args)
    out = Path(args.out).resolve()
    outs = [out] if args.count == 1 else [
        out.with_name(f"{out.stem}-{i}{out.suffix}") for i in range(1, args.count + 1)
    ]

    def one(target: Path) -> None:
        started = time.time()
        target.parent.mkdir(parents=True, exist_ok=True)
        thread_id = attempt(GENERATE_TASK.format(out=target, prompt=prompt), target, args)
        save(target, {"mode": "generate", "prompt": prompt}, thread_id, started)

    with ThreadPoolExecutor(max_workers=len(outs)) as pool:
        list(pool.map(one, outs))


def cmd_edit(args) -> None:
    prompt = read_prompt(args)
    image = Path(args.image).resolve()
    if not image.is_file():
        sys.exit(f"error: no such image: {image}")
    out = Path(args.out).resolve()
    if out == image:
        sys.exit("error: --out must differ from --image")
    thread_id = args.thread
    if not thread_id and sidecar_for(image).is_file():
        thread_id = json.loads(sidecar_for(image).read_text()).get("thread_id")
    if thread_id:
        task = EDIT_TASK.format(which="most recent image in this thread", prompt=prompt, out=out)
        attach = None
    else:
        task = EDIT_TASK.format(which="attached image", prompt=prompt, out=out)
        attach = image
    started = time.time()
    out.parent.mkdir(parents=True, exist_ok=True)
    thread_id = attempt(task, out, args, resume=thread_id, attach=attach)
    save(out, {"mode": "edit", "image": str(image), "prompt": prompt}, thread_id, started)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, fn in (("generate", cmd_generate), ("edit", cmd_edit)):
        p = sub.add_parser(name)
        p.add_argument("--prompt-file")
        p.add_argument("--prompt")
        p.add_argument("--out", required=True)
        p.add_argument("--timeout", type=int, default=600, help="seconds per codex exec turn")
        p.add_argument("--retries", type=int, default=1)
        p.set_defaults(fn=fn)
        if name == "generate":
            p.add_argument("--count", type=int, default=1, help="parallel attempts, saved as <stem>-1..N")
        else:
            p.add_argument("--image", required=True)
            p.add_argument("--thread", help="Codex thread to resume; default: the image's sidecar")
    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
