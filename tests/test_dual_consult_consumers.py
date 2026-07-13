import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class DualConsultConsumerTest(unittest.TestCase):
    def read(self, relative_path):
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_academic_consumers_route_through_paired_runner(self):
        consumers = [
            "skills/external-review/SKILL.md",
            "skills/novelty-gap-check/references/cross-model-protocol.md",
            "skills/research-ideation/SKILL.md",
            "skills/adversarial-review/SKILL.md",
        ]

        for consumer in consumers:
            with self.subTest(consumer=consumer):
                text = self.read(consumer)
                self.assertIn("paired_consult.py", text)
                self.assertNotIn("codex_bridge.py", text)

    def test_main_router_lists_both_collaboration_skills(self):
        text = self.read("skills/main/SKILL.md")

        self.assertIn("collaborating-with-codex", text)
        self.assertIn("collaborating-with-hermes", text)
        self.assertIn("paired_consult.py", text)

    def test_external_review_preserves_two_views(self):
        text = self.read("skills/external-review/SKILL.md")

        self.assertIn("Codex view", text)
        self.assertIn("Hermes view", text)
        self.assertIn("pair_status", text)

    def test_external_review_reference_has_no_legacy_single_backend_fallback(self):
        text = self.read(
            "skills/external-review/references/cadence-and-independence.md"
        )

        self.assertNotIn("Codex bridge is the core reviewer backend", text)
        self.assertNotIn("Optional manual fallback", text)
        self.assertNotIn("manual-review", text)

    def test_novelty_keeps_local_and_provider_reads_separate(self):
        text = self.read("skills/novelty-gap-check/references/cross-model-protocol.md")

        self.assertIn("Local retrieval verdict", text)
        self.assertIn("Codex novelty view", text)
        self.assertIn("Hermes novelty view", text)
        self.assertIn("verification_needed", text)

    def test_adversarial_review_has_two_independent_verdicts(self):
        text = self.read("skills/adversarial-review/SKILL.md")

        self.assertIn("Codex verdict", text)
        self.assertIn("Hermes verdict", text)
        self.assertIn("--CODEX_CONTEXT_FILE", text)
        self.assertIn("--HERMES_CONTEXT_FILE", text)

    def test_type_b_protocol_points_to_dual_consult_rule(self):
        text = self.read(
            "skills/planning-foundation/references/review-loop-protocol.md"
        )

        self.assertIn("dual-consult-protocol.md", text)

    def test_scientific_schematics_remains_direct_codex_exception(self):
        text = self.read("skills/scientific-schematics/SKILL.md")

        self.assertIn("codex_bridge.py", text)
        self.assertIn("--sandbox workspace-write", text)
        self.assertNotIn("paired_consult.py", text)


if __name__ == "__main__":
    unittest.main()
