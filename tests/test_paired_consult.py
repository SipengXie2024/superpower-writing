import json
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

from scripts.paired_consult import _read_context, run_paired_consult


class PairedConsultTest(unittest.TestCase):
    def test_cli_help_runs_outside_repository(self):
        script = Path(__file__).parents[1] / "scripts" / "paired_consult.py"
        with tempfile.TemporaryDirectory() as directory:
            completed = subprocess.run(
                [sys.executable, str(script), "--help"],
                cwd=directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)

    def handoff(self):
        return {
            "schema_version": 2,
            "handoff_kind": "general",
            "status": "complete",
            "summary": "A scoped prior assessment.",
            "payload": {"findings": []},
            "evidence": [],
            "uncertainties": [],
            "verification_needed": [],
        }

    def test_context_files_accept_only_validated_structured_handoffs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            valid = root / "valid.json"
            invalid = root / "raw.txt"
            valid.write_text(json.dumps(self.handoff()), encoding="utf-8")
            invalid.write_text("private raw provider answer", encoding="utf-8")

            self.assertEqual(json.loads(_read_context(str(valid))), self.handoff())
            with self.assertRaises(ValueError):
                _read_context(str(invalid))

    def test_runs_both_providers_concurrently_with_same_objective(self):
        barrier = threading.Barrier(2, timeout=1)
        calls = {}

        def runner(**kwargs):
            calls[kwargs["provider"]] = kwargs
            barrier.wait()
            return {"success": True, "handoff": {"summary": kwargs["provider"]}}

        result = run_paired_consult(
            prompt="Review claim C1 against paper.tex.",
            working_directory="/workspace",
            handoff_kind="general",
            runner=runner,
        )

        self.assertEqual(result["pair_status"], "complete")
        self.assertIn("Review claim C1 against paper.tex.", calls["codex"]["prompt"])
        self.assertIn("Review claim C1 against paper.tex.", calls["hermes"]["prompt"])
        self.assertEqual(calls["codex"]["handoff_kind"], "general")
        self.assertEqual(calls["hermes"]["handoff_kind"], "general")

    def test_provider_context_and_session_never_cross_lanes(self):
        calls = {}

        def runner(**kwargs):
            calls[kwargs["provider"]] = kwargs
            return {"success": True}

        run_paired_consult(
            prompt="Reassess the review.",
            working_directory="/workspace",
            handoff_kind="venue-review",
            codex_session_id="codex-thread",
            codex_context="codex previous handoff",
            hermes_context="hermes previous handoff",
            runner=runner,
        )

        self.assertEqual(calls["codex"]["session_id"], "codex-thread")
        self.assertIsNone(calls["hermes"]["session_id"])
        self.assertIn("codex previous handoff", calls["codex"]["prompt"])
        self.assertNotIn("hermes previous handoff", calls["codex"]["prompt"])
        self.assertIn("hermes previous handoff", calls["hermes"]["prompt"])
        self.assertNotIn("codex previous handoff", calls["hermes"]["prompt"])

    def test_reports_partial_and_failed_without_combining_views(self):
        def partial_runner(**kwargs):
            return {"success": kwargs["provider"] == "codex"}

        partial = run_paired_consult(
            prompt="Review",
            working_directory="/workspace",
            handoff_kind="general",
            runner=partial_runner,
        )
        failed = run_paired_consult(
            prompt="Review",
            working_directory="/workspace",
            handoff_kind="general",
            runner=lambda **kwargs: {"success": False},
        )

        self.assertEqual(partial["pair_status"], "partial")
        self.assertEqual(failed["pair_status"], "failed")
        self.assertIn("codex", partial)
        self.assertIn("hermes", partial)
        for forbidden in (
            "combined_summary",
            "consensus",
            "winner",
            "recommended_provider",
            "verdict",
        ):
            self.assertNotIn(forbidden, partial)

    def test_slow_lane_does_not_delay_start_of_other_lane(self):
        starts = {}
        release = threading.Event()

        def runner(**kwargs):
            starts[kwargs["provider"]] = time.monotonic()
            if kwargs["provider"] == "codex":
                release.wait(timeout=0.3)
            else:
                release.set()
            return {"success": True}

        run_paired_consult(
            prompt="Review",
            working_directory="/workspace",
            handoff_kind="general",
            runner=runner,
        )

        self.assertLess(abs(starts["codex"] - starts["hermes"]), 0.2)


if __name__ == "__main__":
    unittest.main()
