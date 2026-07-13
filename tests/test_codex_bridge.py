import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


BRIDGE_PATH = (
    Path(__file__).parents[1]
    / "skills"
    / "collaborating-with-codex"
    / "scripts"
    / "codex_bridge.py"
)
SPEC = importlib.util.spec_from_file_location("codex_bridge", BRIDGE_PATH)
codex_bridge = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(codex_bridge)


class CodexBridgeTest(unittest.TestCase):
    def handoff(self):
        return {
            "schema_version": 2,
            "handoff_kind": "general",
            "status": "complete",
            "summary": "The evidence supports a scoped academic conclusion.",
            "payload": {
                "findings": [
                    {
                        "id": "F1",
                        "statement": "The manuscript reports five random seeds.",
                        "epistemic_status": "source_fact",
                        "confidence": "high",
                        "evidence_links": [
                            {"evidence_id": "E1", "relation": "supports"}
                        ],
                    }
                ]
            },
            "evidence": [
                {
                    "id": "E1",
                    "citation": "Local manuscript",
                    "identifier": "file:paper.tex",
                    "locator": "paper.tex:42",
                    "source_type": "manuscript",
                    "access_scope": "local_artifact",
                    "verification_status": "verified",
                }
            ],
            "uncertainties": [],
            "verification_needed": [],
        }

    def lines(self, answer):
        return [
            json.dumps({"type": "thread.started", "thread_id": "thread-123"}),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": answer},
                }
            ),
            json.dumps({"type": "turn.completed"}),
        ]

    def test_consult_command_forces_read_only_without_bypass(self):
        command = codex_bridge.build_command(
            "review the manuscript",
            working_directory="/workspace",
            consult_handoff=True,
        )

        self.assertEqual(command[:4], ["codex", "exec", "--sandbox", "read-only"])
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)
        self.assertNotIn("--skip-git-repo-check", command)

    def test_consult_command_rejects_write_sandbox_and_bypass(self):
        with self.assertRaises(ValueError):
            codex_bridge.build_command(
                "review",
                working_directory="/workspace",
                consult_handoff=True,
                sandbox="workspace-write",
            )
        with self.assertRaises(ValueError):
            codex_bridge.build_command(
                "review",
                working_directory="/workspace",
                consult_handoff=True,
                bypass_sandbox=True,
            )

    def test_direct_command_preserves_resume_images_and_explicit_options(self):
        command = codex_bridge.build_command(
            "draw the figure",
            working_directory="/workspace",
            consult_handoff=False,
            sandbox="workspace-write",
            session_id="thread-123",
            skip_git_repo_check=True,
            images=["a.png", "b.png"],
            model="explicit-model",
            profile="explicit-profile",
            bypass_sandbox=True,
        )

        image_index = command.index("--image")
        self.assertEqual(command[image_index + 1 : image_index + 3], ["a.png", "b.png"])
        self.assertNotIn("a.png,b.png", command)
        self.assertIn("--model", command)
        self.assertIn("explicit-model", command)
        self.assertIn("--profile", command)
        self.assertIn("explicit-profile", command)
        self.assertIn("--skip-git-repo-check", command)
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", command)
        self.assertIn("resume", command)
        self.assertIn("thread-123", command)

    def test_direct_result_contract_is_preserved(self):
        parsed = codex_bridge.parse_codex_lines(self.lines("full answer"))
        result = codex_bridge.build_codex_result(
            parsed,
            prompt="analyze",
            working_directory="/workspace",
            consult_handoff=False,
            handoff_kind="general",
            marker=None,
            return_all_messages=True,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["SESSION_ID"], "thread-123")
        self.assertEqual(result["agent_messages"], "full answer")
        self.assertIn("all_messages", result)

    def test_consult_result_returns_only_validated_handoff(self):
        marker = "ACADEMIC_HANDOFF_TEST"
        canary = "private-canary-codex-921"
        answer = f"{canary}\n{marker}\n{json.dumps(self.handoff())}\n{marker}_END"
        parsed = codex_bridge.parse_codex_lines(self.lines(answer))
        with tempfile.TemporaryDirectory() as temp_root:
            result = codex_bridge.build_codex_result(
                parsed,
                prompt="review",
                working_directory="/workspace",
                consult_handoff=True,
                handoff_kind="general",
                marker=marker,
                return_all_messages=False,
                temp_root=temp_root,
            )

            self.assertTrue(result["success"])
            self.assertEqual(result["handoff"], self.handoff())
            self.assertNotIn("agent_messages", result)
            self.assertNotIn("all_messages", result)
            self.assertNotIn(canary, json.dumps(result))
            self.assertEqual(
                Path(result["artifact"]["raw_path"]).read_text(encoding="utf-8"),
                answer,
            )

    def test_blocked_handoff_is_not_reported_as_success(self):
        marker = "ACADEMIC_HANDOFF_TEST"
        handoff = self.handoff()
        handoff["status"] = "blocked"
        handoff["summary"] = "The named manuscript file was unavailable."
        answer = f"analysis\n{marker}\n{json.dumps(handoff)}\n{marker}_END"
        parsed = codex_bridge.parse_codex_lines(self.lines(answer))
        with tempfile.TemporaryDirectory() as temp_root:
            result = codex_bridge.build_codex_result(
                parsed,
                prompt="review",
                working_directory="/workspace",
                consult_handoff=True,
                handoff_kind="general",
                marker=marker,
                return_all_messages=False,
                temp_root=temp_root,
            )

        self.assertFalse(result["success"])
        self.assertEqual(result["error_code"], "handoff_blocked")
        self.assertEqual(result["handoff"]["status"], "blocked")

    def test_invalid_format_and_damaged_stream_fail_closed(self):
        parsed = codex_bridge.parse_codex_lines(
            self.lines("private raw answer")
            + [json.dumps({"type": "turn.failed", "error": {"message": "boom"}})]
        )
        with tempfile.TemporaryDirectory() as temp_root:
            result = codex_bridge.build_codex_result(
                parsed,
                prompt="review",
                working_directory="/workspace",
                consult_handoff=True,
                handoff_kind="general",
                marker="ACADEMIC_HANDOFF_TEST",
                return_all_messages=False,
                temp_root=temp_root,
            )

        self.assertFalse(result["success"])
        self.assertEqual(result["error_code"], "damaged_event_stream")
        self.assertNotIn("private raw answer", json.dumps(result))
        self.assertNotIn("handoff", result)

    def test_truncated_stream_without_turn_completed_fails_closed(self):
        lines = self.lines("partial answer")[:-1]
        parsed = codex_bridge.parse_codex_lines(lines)
        result = codex_bridge.build_codex_result(
            parsed,
            prompt="analyze",
            working_directory="/workspace",
            consult_handoff=False,
            handoff_kind="general",
            marker=None,
            return_all_messages=False,
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["error_code"], "damaged_event_stream")

    def test_non_json_noise_is_ignored_but_non_object_json_is_damage(self):
        clean = codex_bridge.parse_codex_lines(
            ["Reading additional input from stdin..."] + self.lines("answer")
        )
        damaged = codex_bridge.parse_codex_lines(["42"] + self.lines("answer"))

        self.assertFalse(clean["had_parse_error"])
        self.assertTrue(damaged["had_parse_error"])


if __name__ == "__main__":
    unittest.main()
