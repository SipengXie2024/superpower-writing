import hashlib
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path

from scripts.consult_handoff import (
    HANDOFF_KINDS,
    HandoffValidationError,
    _example_handoff,
    build_handoff_instruction,
    extract_handoff,
    persist_artifacts,
    validate_handoff,
)


class ConsultHandoffTest(unittest.TestCase):
    def evidence(self, *, evidence_id="E1", verified=True):
        return {
            "id": evidence_id,
            "citation": "Doe et al., Example Study, ExampleConf, 2026",
            "identifier": "doi:10.1000/example",
            "locator": "p. 7, Section 4.2, Table 3",
            "source_type": "primary_research",
            "access_scope": "full_text",
            "verification_status": "verified" if verified else "unverified",
        }

    def base(self, kind, payload, *, evidence=None):
        return {
            "schema_version": 2,
            "handoff_kind": kind,
            "status": "complete",
            "summary": "The provider returned an evidence-linked academic assessment.",
            "payload": payload,
            "evidence": [self.evidence()] if evidence is None else evidence,
            "uncertainties": [],
            "verification_needed": [],
        }

    def general(self):
        return self.base(
            "general",
            {
                "findings": [
                    {
                        "id": "F1",
                        "statement": "The reported result uses five random seeds.",
                        "epistemic_status": "source_fact",
                        "confidence": "high",
                        "evidence_links": [
                            {"evidence_id": "E1", "relation": "supports"}
                        ],
                    }
                ]
            },
        )

    def response(self, marker, handoff):
        return f"private analysis\n{marker}\n{json.dumps(handoff)}\n{marker}_END"

    def test_accepts_general_source_fact_with_verified_support(self):
        validate_handoff(self.general())

    def test_requires_verified_support_for_source_fact(self):
        handoff = self.general()
        handoff["evidence"][0]["verification_status"] = "unverified"

        with self.assertRaisesRegex(HandoffValidationError, "verified support"):
            validate_handoff(handoff)

    def test_model_inference_requires_evidence_but_not_verified_source_fact(self):
        handoff = self.general()
        finding = handoff["payload"]["findings"][0]
        finding["epistemic_status"] = "model_inference"
        handoff["evidence"][0]["verification_status"] = "unverified"
        handoff["verification_needed"] = [
            {"item_ids": ["E1"], "action": "Verify the cited source and locator."}
        ]
        validate_handoff(handoff)

        finding["evidence_links"] = []
        with self.assertRaisesRegex(HandoffValidationError, "requires evidence"):
            validate_handoff(handoff)

    def test_unverified_evidence_requires_verification_queue(self):
        handoff = self.general()
        finding = handoff["payload"]["findings"][0]
        finding["epistemic_status"] = "model_inference"
        handoff["evidence"][0]["verification_status"] = "unverified"

        with self.assertRaisesRegex(HandoffValidationError, "unverified evidence"):
            validate_handoff(handoff)

        handoff["verification_needed"] = [
            {"item_ids": ["E1"], "action": "Verify the cited source and locator."}
        ]
        validate_handoff(handoff)

    def test_requires_unverified_finding_in_verification_queue(self):
        handoff = self.general()
        finding = handoff["payload"]["findings"][0]
        finding["epistemic_status"] = "unverified"
        finding["evidence_links"] = []

        with self.assertRaisesRegex(HandoffValidationError, "verification_needed"):
            validate_handoff(handoff)

        handoff["verification_needed"] = [
            {"item_ids": ["F1"], "action": "Verify the citation and locator."}
        ]
        validate_handoff(handoff)

    def test_accepts_conflicting_evidence_relations_without_merging_them(self):
        handoff = self.general()
        handoff["evidence"].append(self.evidence(evidence_id="E2"))
        handoff["payload"]["findings"][0]["evidence_links"] = [
            {"evidence_id": "E1", "relation": "supports"},
            {"evidence_id": "E2", "relation": "contradicts"},
        ]

        validate_handoff(handoff)

    def test_accepts_all_academic_payload_profiles(self):
        candidates = []
        for index in range(15):
            candidates.append(
                {
                    "id": f"C{index + 1}",
                    "title": f"Candidate {index + 1}",
                    "hypothesis": "A testable hypothesis.",
                    "method": "Run a controlled benchmark with five seeds.",
                    "cheapest_test": "One dataset and one strong baseline.",
                    "contribution_type": "empirical_finding",
                    "finer": {
                        "feasible": 4,
                        "interesting": 4,
                        "novel": 3,
                        "ethical": 5,
                        "relevant": 4,
                    },
                    "strongest_objection": "The setting may be too narrow.",
                    "failure_mode": "The gain disappears against the strongest baseline.",
                    "recommendation": "pursue" if index == 0 else "hold",
                    "evidence_ids": ["E1"],
                }
            )
        payloads = {
            "ideation": {
                "candidates": candidates,
                "ranked_candidate_ids": [candidate["id"] for candidate in candidates],
            },
            "novelty": {
                "claims": [
                    {
                        "id": f"N{index}",
                        "claim": f"Atomic novelty claim {index}.",
                        "novelty": "HIGH" if index == 1 else "MED",
                        "contribution_type": "finding",
                        "closest_work_evidence_ids": ["E1"],
                        "delta": "The proposed test covers a missing regime.",
                    }
                    for index in range(1, 4)
                ],
                "overall_assessment": "Proceed with caution.",
            },
            "manuscript-draft": {
                "draft": "A candidate paragraph grounded in the supplied evidence.",
                "claim_ids": ["claim-1"],
                "citation_evidence_ids": ["E1"],
                "unresolved_items": [],
            },
            "venue-review": {
                "strengths": [
                    {"id": "S1", "statement": "Clear question.", "evidence_ids": ["E1"]}
                ],
                "weaknesses": [
                    {
                        "id": "W1",
                        "statement": "Evaluation is narrow.",
                        "severity": "major",
                        "evidence_ids": ["E1"],
                    }
                ],
                "questions": ["Does the result hold on another workload?"],
                "score": "borderline",
                "reviewer_confidence": {"level": "high", "rationale": "Direct expertise."},
                "accept_lift_conditions": ["Add the missing workload."],
            },
            "results-claims-matrix": {
                "rows": [
                    {
                        "id": "R1",
                        "outcomes": ["X improves", "Y is flat"],
                        "defensible_claims": ["The scoped X claim remains supported."],
                        "unsupported_claims": ["The general X-and-Y claim."],
                        "evidence_ids": ["E1"],
                    }
                ]
            },
            "experiment-plan": {
                "experiments": [
                    {
                        "id": "X1",
                        "title": "Cross-hardware validation",
                        "datasets": ["Dataset A"],
                        "baselines": ["Baseline B"],
                        "model_scales": ["7B"],
                        "hyperparameters": ["batch_size=128", "learning_rate=3e-4"],
                        "ablations": ["remove component C"],
                        "metrics": ["throughput", "95% confidence interval"],
                        "budget": "8 GPU-days",
                        "priority": 1,
                        "evidence_ids": ["E1"],
                    }
                ]
            },
            "adversarial-attack": {
                "memo": "The headline claim exceeds the measured regime.",
                "evidence_ids": ["E1"],
            },
            "adversarial-adjudication": {
                "points": [
                    {
                        "id": "P1",
                        "attack_claim": "The scope is broader than the evidence.",
                        "ruling": "unresolved",
                        "evidence_ids": ["E1"],
                        "severity": "critical",
                        "needs_experiment": True,
                        "recommended_fix": "Add a second hardware platform.",
                    },
                    {
                        "id": "P2",
                        "attack_claim": "The method lacks motivation.",
                        "ruling": "answered_by_current_text",
                        "evidence_ids": ["E1"],
                    },
                    {
                        "id": "P3",
                        "attack_claim": "The baseline is weak.",
                        "ruling": "partially",
                        "evidence_ids": ["E1"],
                        "severity": "major",
                        "needs_experiment": False,
                        "recommended_fix": "Add the current strongest baseline.",
                    },
                ],
                "net_assessment": "One headline issue remains unresolved.",
            },
        }

        for kind, payload in payloads.items():
            with self.subTest(kind=kind):
                validate_handoff(self.base(kind, payload))

    def test_rejects_silently_truncated_complete_ideation_payload(self):
        handoff = self.base(
            "ideation",
            {"candidates": [], "ranked_candidate_ids": []},
            evidence=[],
        )

        with self.assertRaisesRegex(HandoffValidationError, "15-20"):
            validate_handoff(handoff)

    def test_accepts_explicit_partial_profile_with_remaining_work_queued(self):
        handoff = self.base(
            "ideation",
            {
                "candidates": [
                    {
                        "id": "C1",
                        "title": "Candidate 1",
                        "hypothesis": "A testable hypothesis.",
                        "method": "Run a controlled benchmark.",
                        "cheapest_test": "One dataset and one baseline.",
                        "contribution_type": "empirical_finding",
                        "finer": {
                            "feasible": 4,
                            "interesting": 4,
                            "novel": 3,
                            "ethical": 5,
                            "relevant": 4,
                        },
                        "strongest_objection": "The scope may be narrow.",
                        "failure_mode": "The gain disappears.",
                        "recommendation": "hold",
                        "evidence_ids": ["E1"],
                    }
                ],
                "ranked_candidate_ids": ["C1"],
            },
        )
        handoff["status"] = "partial"
        handoff["verification_needed"] = [
            {
                "item_ids": ["remaining-candidates"],
                "action": "Generate and assess the remaining candidates.",
            }
        ]

        validate_handoff(handoff)

    def test_adjudication_payload_is_compatible_with_verdict_script(self):
        handoff = self.base(
            "adversarial-adjudication",
            {
                "points": [
                    {
                        "id": "P1",
                        "attack_claim": "Claim one.",
                        "ruling": "answered_by_current_text",
                        "evidence_ids": ["E1"],
                    },
                    {
                        "id": "P2",
                        "attack_claim": "Claim two.",
                        "ruling": "partially",
                        "evidence_ids": ["E1"],
                        "severity": "minor",
                        "needs_experiment": False,
                        "recommended_fix": "Clarify the scope.",
                    },
                    {
                        "id": "P3",
                        "attack_claim": "Claim three.",
                        "ruling": "unresolved",
                        "evidence_ids": ["E1"],
                        "severity": "critical",
                        "needs_experiment": True,
                        "recommended_fix": "Run the missing experiment.",
                    },
                ],
                "net_assessment": "The defense does not survive.",
            },
        )

        validate_handoff(handoff)
        points = handoff["payload"]["points"]
        self.assertTrue(all("id" in point and "ruling" in point for point in points))

    def test_all_instruction_examples_satisfy_their_validators(self):
        for kind in HANDOFF_KINDS:
            with self.subTest(kind=kind):
                validate_handoff(_example_handoff(kind))

    def test_instruction_preserves_reproducibility_details(self):
        instruction = build_handoff_instruction("experiment-plan", "ACADEMIC_TEST")

        self.assertIn("ACADEMIC_TEST", instruction)
        self.assertIn('"handoff_kind": "experiment-plan"', instruction)
        self.assertIn("sample sizes", instruction)
        self.assertIn("hyperparameters", instruction)
        self.assertIn("statistical tests", instruction)
        self.assertNotIn("Do not include commands, payloads, procedures, or parameters", instruction)

    def test_extracts_only_final_marked_handoff(self):
        marker = "ACADEMIC_TEST"
        handoff = self.general()

        result = extract_handoff(self.response(marker, handoff), marker)

        self.assertEqual(result, handoff)

    def test_persists_raw_response_privately_without_plaintext_prompt(self):
        raw = "private-canary-7f41\ncomplete response"
        prompt = "Review the unpublished paper."
        with tempfile.TemporaryDirectory() as temp_root:
            artifact = persist_artifacts(
                provider="hermes",
                handoff_kind="venue-review",
                prompt=prompt,
                raw_response=raw,
                working_directory="/workspace",
                external_exit_code=0,
                session_id=None,
                parse_status="valid",
                temp_root=temp_root,
            )

            raw_path = Path(artifact["raw_path"])
            metadata_path = Path(artifact["metadata_path"])
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            self.assertEqual(raw_path.read_text(encoding="utf-8"), raw)
            self.assertEqual(artifact["sha256"], hashlib.sha256(raw.encode()).hexdigest())
            self.assertEqual(artifact["bytes"], len(raw.encode()))
            self.assertEqual(metadata["provider"], "hermes")
            self.assertEqual(metadata["handoff_kind"], "venue-review")
            self.assertNotIn(prompt, metadata_path.read_text(encoding="utf-8"))
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE(raw_path.parent.stat().st_mode), 0o700)
                self.assertEqual(stat.S_IMODE(raw_path.stat().st_mode), 0o600)
                self.assertEqual(stat.S_IMODE(metadata_path.stat().st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
