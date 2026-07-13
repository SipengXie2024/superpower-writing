from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.consult_handoff import HandoffValidationError, validate_handoff
CODEX_BRIDGE = ROOT / "skills" / "collaborating-with-codex" / "scripts" / "codex_bridge.py"
HERMES_BRIDGE = ROOT / "skills" / "collaborating-with-hermes" / "scripts" / "hermes_bridge.py"


def _provider_prompt(objective: str, context: Optional[str]) -> str:
    if not context:
        return objective
    return (
        f"{objective}\n\nPrevious structured handoff from this same provider only:\n{context}"
    )


def _run_provider(
    *,
    provider: str,
    prompt: str,
    working_directory: str,
    handoff_kind: str,
    session_id: Optional[str],
) -> dict:
    bridge = CODEX_BRIDGE if provider == "codex" else HERMES_BRIDGE
    command = [
        sys.executable,
        str(bridge),
        "--cd",
        working_directory,
        "--PROMPT",
        prompt,
        "--consult-handoff",
        "--handoff-kind",
        handoff_kind,
    ]
    if provider == "codex" and session_id:
        command.extend(["--SESSION_ID", session_id])
    completed = subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=630,
        check=False,
    )
    if completed.returncode != 0:
        return {"success": False, "error_code": f"{provider}_bridge_failed"}
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"success": False, "error_code": f"{provider}_bridge_invalid_json"}
    if not isinstance(result, dict):
        return {"success": False, "error_code": f"{provider}_bridge_invalid_json"}
    return result


def run_paired_consult(
    *,
    prompt: str,
    working_directory: str,
    handoff_kind: str,
    codex_session_id: Optional[str] = None,
    codex_context: Optional[str] = None,
    hermes_context: Optional[str] = None,
    runner: Callable[..., dict] = _run_provider,
) -> dict:
    requests = {
        "codex": {
            "provider": "codex",
            "prompt": _provider_prompt(prompt, codex_context),
            "working_directory": working_directory,
            "handoff_kind": handoff_kind,
            "session_id": codex_session_id,
        },
        "hermes": {
            "provider": "hermes",
            "prompt": _provider_prompt(prompt, hermes_context),
            "working_directory": working_directory,
            "handoff_kind": handoff_kind,
            "session_id": None,
        },
    }
    results: dict[str, dict] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            provider: executor.submit(runner, **request)
            for provider, request in requests.items()
        }
        for provider, future in futures.items():
            try:
                result = future.result()
            except Exception:
                result = {"success": False, "error_code": f"{provider}_runner_failed"}
            results[provider] = result if isinstance(result, dict) else {
                "success": False,
                "error_code": f"{provider}_runner_invalid_result",
            }

    successes = sum(bool(results[provider].get("success")) for provider in ("codex", "hermes"))
    pair_status = "complete" if successes == 2 else "partial" if successes == 1 else "failed"
    return {
        "pair_status": pair_status,
        "codex": results["codex"],
        "hermes": results["hermes"],
    }


def _read_context(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        validate_handoff(data)
    except (OSError, json.JSONDecodeError, HandoffValidationError) as exc:
        raise ValueError("context file must contain one valid structured handoff") from exc
    return json.dumps(data, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run paired academic consultation")
    parser.add_argument("--PROMPT", required=True, help="Neutral objective for both providers.")
    parser.add_argument("--cd", required=True, help="Workspace root available to both providers.")
    parser.add_argument(
        "--handoff-kind",
        required=True,
        choices=[
            "general",
            "ideation",
            "novelty",
            "manuscript-draft",
            "venue-review",
            "results-claims-matrix",
            "experiment-plan",
            "adversarial-attack",
            "adversarial-adjudication",
        ],
    )
    parser.add_argument("--CODEX_SESSION_ID", default="")
    parser.add_argument("--CODEX_CONTEXT_FILE")
    parser.add_argument("--HERMES_CONTEXT_FILE")
    args = parser.parse_args()
    result = run_paired_consult(
        prompt=args.PROMPT,
        working_directory=args.cd,
        handoff_kind=args.handoff_kind,
        codex_session_id=args.CODEX_SESSION_ID or None,
        codex_context=_read_context(args.CODEX_CONTEXT_FILE),
        hermes_context=_read_context(args.HERMES_CONTEXT_FILE),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
