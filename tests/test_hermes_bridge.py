import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


BRIDGE_PATH = (
    Path(__file__).parents[1]
    / "skills"
    / "collaborating-with-hermes"
    / "scripts"
    / "hermes_bridge.py"
)


def load_bridge():
    spec = importlib.util.spec_from_file_location("hermes_bridge", BRIDGE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class HermesBridgeTest(unittest.TestCase):
    def handoff(self):
        return {
            "schema_version": 2,
            "handoff_kind": "general",
            "status": "complete",
            "summary": "The evidence supports a scoped conclusion.",
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

    def test_command_is_stateless_oneshot_with_whitelisted_flags(self):
        bridge = load_bridge()
        command = bridge.build_command(
            "analyze this",
            worktree=True,
            ignore_rules=True,
            toolsets="web,terminal",
            skills="research",
        )

        self.assertEqual(command[:3], ["hermes", "--cli", "-z"])
        self.assertEqual(command[3], "analyze this")
        self.assertIn("--worktree", command)
        self.assertIn("--ignore-rules", command)
        self.assertIn("-t", command)
        self.assertIn("--skills", command)
        self.assertNotIn("--resume", command)
        self.assertNotIn("--continue", command)
        self.assertNotIn("cd", command)

    def test_run_uses_cwd_and_ten_minute_internal_timeout(self):
        bridge = load_bridge()
        calls = []

        def fake_run(command, **kwargs):
            calls.append((command, kwargs))
            return subprocess.CompletedProcess(command, 0, "answer", "")

        with mock.patch.object(bridge.subprocess, "run", side_effect=fake_run):
            bridge.run_hermes(["hermes", "--cli", "-z", "prompt"], "/workspace")

        _, kwargs = calls[0]
        self.assertEqual(kwargs["cwd"], "/workspace")
        self.assertEqual(kwargs["timeout"], 600)
        self.assertFalse(kwargs["check"])

    def test_direct_result_returns_full_answer_without_session(self):
        bridge = load_bridge()
        result = bridge.build_hermes_result(
            prompt="analyze",
            working_directory="/workspace",
            stdout="full answer",
            stderr="",
            exit_code=0,
            consult_handoff=False,
            handoff_kind="general",
            marker=None,
            workspace_changed=False,
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["agent_messages"], "full answer")
        self.assertNotIn("SESSION_ID", result)

    def test_consult_result_returns_only_validated_handoff(self):
        bridge = load_bridge()
        marker = "ACADEMIC_HANDOFF_TEST"
        canary = "private-canary-hermes-632"
        raw = f"{canary}\n{marker}\n{json.dumps(self.handoff())}\n{marker}_END"
        with tempfile.TemporaryDirectory() as temp_root:
            result = bridge.build_hermes_result(
                prompt="review",
                working_directory="/workspace",
                stdout=raw,
                stderr="",
                exit_code=0,
                consult_handoff=True,
                handoff_kind="general",
                marker=marker,
                workspace_changed=False,
                temp_root=temp_root,
            )

            self.assertTrue(result["success"])
            self.assertEqual(result["handoff"], self.handoff())
            self.assertNotIn("agent_messages", result)
            self.assertNotIn(canary, json.dumps(result))
            self.assertEqual(
                Path(result["artifact"]["raw_path"]).read_text(encoding="utf-8"), raw
            )

    def test_blocked_handoff_is_not_reported_as_success(self):
        bridge = load_bridge()
        marker = "ACADEMIC_HANDOFF_TEST"
        handoff = self.handoff()
        handoff["status"] = "blocked"
        handoff["summary"] = "The named manuscript file was unavailable."
        raw = f"analysis\n{marker}\n{json.dumps(handoff)}\n{marker}_END"
        with tempfile.TemporaryDirectory() as temp_root:
            result = bridge.build_hermes_result(
                prompt="review",
                working_directory="/workspace",
                stdout=raw,
                stderr="",
                exit_code=0,
                consult_handoff=True,
                handoff_kind="general",
                marker=marker,
                workspace_changed=False,
                temp_root=temp_root,
            )

        self.assertFalse(result["success"])
        self.assertEqual(result["error_code"], "handoff_blocked")
        self.assertEqual(result["handoff"]["status"], "blocked")

    def test_process_failure_and_stderr_do_not_leak(self):
        bridge = load_bridge()
        result = bridge.build_hermes_result(
            prompt="review",
            working_directory="/workspace",
            stdout="private response",
            stderr="credential secret",
            exit_code=2,
            consult_handoff=False,
            handoff_kind="general",
            marker=None,
            workspace_changed=False,
        )

        self.assertFalse(result["success"])
        self.assertEqual(result["error_code"], "hermes_process_failed")
        self.assertNotIn("private response", json.dumps(result))
        self.assertNotIn("credential secret", json.dumps(result))

    def test_consult_fails_if_workspace_changes(self):
        bridge = load_bridge()
        marker = "ACADEMIC_HANDOFF_TEST"
        raw = f"analysis\n{marker}\n{json.dumps(self.handoff())}\n{marker}_END"
        with tempfile.TemporaryDirectory() as temp_root:
            result = bridge.build_hermes_result(
                prompt="review",
                working_directory="/workspace",
                stdout=raw,
                stderr="",
                exit_code=0,
                consult_handoff=True,
                handoff_kind="general",
                marker=marker,
                workspace_changed=True,
                temp_root=temp_root,
            )

        self.assertFalse(result["success"])
        self.assertEqual(result["error_code"], "workspace_modified")
        self.assertNotIn("handoff", result)

    def test_workspace_fingerprint_detects_tracked_content_change(self):
        bridge = load_bridge()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            tracked = root / "paper.txt"
            tracked.write_text("before", encoding="utf-8")
            subprocess.run(["git", "add", "paper.txt"], cwd=root, check=True)
            before = bridge.workspace_fingerprint(str(root))
            tracked.write_text("after", encoding="utf-8")
            after = bridge.workspace_fingerprint(str(root))

        self.assertNotEqual(before, after)

    def test_workspace_fingerprint_detects_change_outside_git_repository(self):
        bridge = load_bridge()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "paper.txt"
            document.write_text("before", encoding="utf-8")
            before = bridge.workspace_fingerprint(str(root))
            document.write_text("after", encoding="utf-8")
            after = bridge.workspace_fingerprint(str(root))

        self.assertNotEqual(before, "unavailable")
        self.assertNotEqual(before, after)

    def test_workspace_fingerprint_detects_ignored_file_change(self):
        bridge = load_bridge()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / ".gitignore").write_text("private-notes.txt\n", encoding="utf-8")
            ignored = root / "private-notes.txt"
            ignored.write_text("before", encoding="utf-8")
            before = bridge.workspace_fingerprint(str(root))
            ignored.write_text("after", encoding="utf-8")
            after = bridge.workspace_fingerprint(str(root))

        self.assertNotEqual(before, after)

    def test_workspace_fingerprint_detects_permission_change(self):
        bridge = load_bridge()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "paper.txt"
            document.write_text("unchanged content", encoding="utf-8")
            document.chmod(0o600)
            before = bridge.workspace_fingerprint(str(root))
            document.chmod(0o400)
            after = bridge.workspace_fingerprint(str(root))

        self.assertNotEqual(before, after)

    def test_workspace_fingerprint_detects_index_only_change(self):
        bridge = load_bridge()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            tracked = root / "paper.txt"
            tracked.write_text("same worktree content", encoding="utf-8")
            subprocess.run(["git", "add", "paper.txt"], cwd=root, check=True)
            subprocess.run(
                [
                    "git",
                    "-c",
                    "user.name=Test",
                    "-c",
                    "user.email=test@example.com",
                    "commit",
                    "-m",
                    "base",
                    "-q",
                ],
                cwd=root,
                check=True,
            )
            before = bridge.workspace_fingerprint(str(root))
            subprocess.run(["git", "rm", "--cached", "-q", "paper.txt"], cwd=root, check=True)
            after = bridge.workspace_fingerprint(str(root))

        self.assertNotEqual(before, after)

    def test_workspace_fingerprint_detects_a_commit_created_by_hermes(self):
        bridge = load_bridge()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "--allow-empty", "-m", "before", "-q"],
                cwd=root,
                check=True,
            )
            before = bridge.workspace_fingerprint(str(root))
            (root / "paper.txt").write_text("committed by provider", encoding="utf-8")
            subprocess.run(["git", "add", "paper.txt"], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "provider change", "-q"],
                cwd=root,
                check=True,
            )
            after = bridge.workspace_fingerprint(str(root))

        self.assertNotEqual(before, after)


if __name__ == "__main__":
    unittest.main()
