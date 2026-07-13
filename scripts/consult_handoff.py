from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


class HandoffValidationError(ValueError):
    pass


HANDOFF_KINDS = {
    "general",
    "ideation",
    "novelty",
    "manuscript-draft",
    "venue-review",
    "results-claims-matrix",
    "experiment-plan",
    "adversarial-attack",
    "adversarial-adjudication",
}

_TOP_LEVEL_FIELDS = {
    "schema_version",
    "handoff_kind",
    "status",
    "summary",
    "payload",
    "evidence",
    "uncertainties",
    "verification_needed",
}
_STATUS_VALUES = {"complete", "partial", "blocked"}
_CONFIDENCE_VALUES = {"high", "medium", "low"}
_EPISTEMIC_VALUES = {
    "source_fact",
    "model_inference",
    "recommendation",
    "unverified",
}
_RELATION_VALUES = {"supports", "contradicts", "mixed", "unresolved", "context"}
_SOURCE_TYPES = {
    "primary_research",
    "systematic_review",
    "meta_analysis",
    "narrative_review",
    "preprint",
    "dataset",
    "software",
    "manuscript",
    "web",
    "other",
}
_ACCESS_SCOPES = {"full_text", "abstract", "metadata", "local_artifact"}
_VERIFICATION_VALUES = {"verified", "unverified"}
_IDENTIFIER_PREFIXES = ("doi:", "pmid:", "arxiv:", "url:", "zotero:", "file:")


def build_handoff_instruction(handoff_kind: str, marker: str) -> str:
    if handoff_kind not in HANDOFF_KINDS:
        raise ValueError(f"unsupported handoff kind: {handoff_kind}")
    schema = _example_handoff(handoff_kind)
    return (
        "\n\nReturn your normal, complete analysis first. Then finish with a compact "
        f"academic handoff. Put `{marker}` on its own line, followed by exactly one "
        "JSON object using this shape:\n"
        f"{json.dumps(schema, ensure_ascii=False, indent=2)}\n"
        f"Put `{marker}_END` on its own line immediately after the JSON. "
        "Do not silently truncate the requested academic deliverable. Use status `partial` "
        "and list what remains in verification_needed when the handoff is incomplete. "
        "Distinguish source facts, model inferences, recommendations, and unverified items. "
        "Never invent citations, identifiers, locators, sample sizes, methods, procedures, "
        "datasets, hyperparameters, statistical tests, effect estimates, confidence intervals, "
        "limitations, or bias assessments. Preserve reproducibility details when the source "
        "supports them. Evidence locators must point to original sources or real project files, "
        "not to this response. Do not copy long source passages; cite a precise locator instead."
    )


def extract_handoff(raw_text: str, marker: str) -> dict[str, Any]:
    start_token = f"\n{marker}\n"
    end_token = f"\n{marker}_END"
    start = raw_text.rfind(start_token)
    if start < 0:
        raise HandoffValidationError("missing handoff marker")
    json_start = start + len(start_token)
    end = raw_text.find(end_token, json_start)
    if end < 0 or raw_text[end + len(end_token) :].strip():
        raise HandoffValidationError("missing or non-final handoff end marker")
    try:
        data = json.loads(raw_text[json_start:end])
    except json.JSONDecodeError as exc:
        raise HandoffValidationError("invalid handoff JSON") from exc
    validate_handoff(data)
    return data


def validate_handoff(data: Any) -> None:
    _require_exact_dict(data, _TOP_LEVEL_FIELDS, "handoff")
    if data["schema_version"] != 2:
        raise HandoffValidationError("unsupported handoff schema")
    kind = _require_enum(data["handoff_kind"], "handoff kind", HANDOFF_KINDS)
    status = _require_enum(data["status"], "status", _STATUS_VALUES)
    _require_string(data["summary"], "summary", 1600)

    evidence = _validate_evidence(data["evidence"])
    verification_ids = _validate_verification_items(data["verification_needed"])
    if status == "partial" and not verification_ids:
        raise HandoffValidationError("partial handoff requires verification_needed")
    _validate_uncertainties(data["uncertainties"])

    validator = {
        "general": _validate_general,
        "ideation": lambda payload, evidence: _validate_ideation(
            payload, evidence, allow_partial=status == "partial"),
        "novelty": lambda payload, evidence: _validate_novelty(
            payload, evidence, allow_partial=status == "partial"),
        "manuscript-draft": _validate_manuscript_draft,
        "venue-review": _validate_venue_review,
        "results-claims-matrix": _validate_results_claims_matrix,
        "experiment-plan": _validate_experiment_plan,
        "adversarial-attack": _validate_adversarial_attack,
        "adversarial-adjudication": lambda payload, evidence: _validate_adversarial_adjudication(
            payload, evidence, allow_partial=status == "partial"),
    }[kind]
    referenced_ids, unverified_item_ids = validator(data["payload"], evidence)
    _require_known_evidence(referenced_ids, evidence)
    unverified_evidence_ids = {
        evidence_id for evidence_id, item in evidence.items()
        if item["verification_status"] == "unverified"
    }
    missing_queue = (unverified_item_ids | unverified_evidence_ids) - verification_ids
    if missing_queue:
        raise HandoffValidationError(
            "unverified evidence or items missing from verification_needed: "
            + ", ".join(sorted(missing_queue))
        )


def persist_artifacts(
    *,
    provider: str,
    handoff_kind: str,
    prompt: str,
    raw_response: str,
    working_directory: str,
    external_exit_code: Optional[int],
    session_id: Optional[str],
    parse_status: str,
    temp_root: Optional[str] = None,
) -> dict[str, Any]:
    run_dir = Path(tempfile.mkdtemp(prefix="superpower-writing-handoff-", dir=temp_root))
    if os.name == "posix":
        os.chmod(run_dir, 0o700)
        if stat.S_IMODE(run_dir.stat().st_mode) != 0o700:
            raise PermissionError("could not secure handoff directory")

    raw_bytes = raw_response.encode("utf-8")
    raw_path = run_dir / "raw-response.txt"
    metadata_path = run_dir / "metadata.json"
    _secure_write(raw_path, raw_bytes)
    metadata = {
        "schema_version": 2,
        "provider": provider,
        "handoff_kind": handoff_kind,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "working_directory": working_directory,
        "external_exit_code": external_exit_code,
        "session_id": session_id,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "raw_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "raw_bytes": len(raw_bytes),
        "handoff_parse_status": parse_status,
    }
    _secure_write(
        metadata_path,
        json.dumps(metadata, ensure_ascii=False, indent=2).encode("utf-8"),
    )
    return {
        "raw_path": str(raw_path),
        "metadata_path": str(metadata_path),
        "sha256": metadata["raw_sha256"],
        "bytes": metadata["raw_bytes"],
    }


def fallback_guidance() -> str:
    return (
        "The complete response was preserved, but the structured academic handoff could not "
        "be trusted. Do not expose the raw artifact automatically, weaken the evidence rules, "
        "or repeatedly rephrase the request to force a different result."
    )


def _example_handoff(kind: str) -> dict[str, Any]:
    evidence = {
        "id": "E1",
        "citation": "Author, title, venue or repository, year",
        "identifier": "doi:10.xxxx/example or file:path/to/source",
        "locator": "p. 7, Section 4.2, Table 3, or file:line",
        "source_type": "primary_research",
        "access_scope": "full_text",
        "verification_status": "verified",
    }
    ideation_candidates = [
        {
            "id": f"C{index}",
            "title": f"Candidate title {index}",
            "hypothesis": "Testable hypothesis",
            "method": "Concrete method",
            "cheapest_test": "Cheapest decisive test",
            "contribution_type": "empirical_finding",
            "finer": {
                "feasible": 4,
                "interesting": 4,
                "novel": 3,
                "ethical": 5,
                "relevant": 4,
            },
            "strongest_objection": "Strongest objection",
            "failure_mode": "Likely failure mode",
            "recommendation": "pursue" if index == 1 else "hold",
            "evidence_ids": ["E1"],
        }
        for index in range(1, 16)
    ]
    novelty_claims = [
        {
            "id": f"N{index}",
            "claim": f"Atomic novelty claim {index}",
            "novelty": "MED",
            "contribution_type": "finding",
            "closest_work_evidence_ids": ["E1"],
            "delta": "One-line delta",
        }
        for index in range(1, 4)
    ]
    adjudication_points = [
        {
            "id": f"P{index}",
            "attack_claim": f"Atomic attack point {index}",
            "ruling": "unresolved",
            "evidence_ids": ["E1"],
            "severity": "critical" if index == 1 else "major",
            "needs_experiment": True,
            "recommended_fix": "One concrete fix",
        }
        for index in range(1, 4)
    ]
    examples = {
        "general": {
            "findings": [
                {
                    "id": "F1",
                    "statement": "One atomic, independently checkable finding.",
                    "epistemic_status": "source_fact",
                    "confidence": "high",
                    "evidence_links": [{"evidence_id": "E1", "relation": "supports"}],
                }
            ]
        },
        "ideation": {
            "candidates": ideation_candidates,
            "ranked_candidate_ids": [candidate["id"] for candidate in ideation_candidates],
        },
        "novelty": {
            "claims": novelty_claims,
            "overall_assessment": "Advisory assessment",
        },
        "manuscript-draft": {
            "draft": "Candidate prose",
            "claim_ids": ["claim-1"],
            "citation_evidence_ids": ["E1"],
            "unresolved_items": [],
        },
        "venue-review": {
            "strengths": [{"id": "S1", "statement": "Strength", "evidence_ids": ["E1"]}],
            "weaknesses": [
                {
                    "id": "W1",
                    "statement": "Weakness",
                    "severity": "major",
                    "evidence_ids": ["E1"],
                }
            ],
            "questions": ["Question for the authors"],
            "score": "borderline",
            "reviewer_confidence": {"level": "high", "rationale": "Relevant expertise"},
            "accept_lift_conditions": ["Smallest change that could improve the verdict"],
        },
        "results-claims-matrix": {
            "rows": [
                {
                    "id": "R1",
                    "outcomes": ["Outcome X"],
                    "defensible_claims": ["Defensible claim"],
                    "unsupported_claims": ["Unsupported claim"],
                    "evidence_ids": ["E1"],
                }
            ]
        },
        "experiment-plan": {
            "experiments": [
                {
                    "id": "X1",
                    "title": "Experiment",
                    "datasets": ["Dataset"],
                    "baselines": ["Baseline"],
                    "model_scales": ["Scale"],
                    "hyperparameters": ["Parameter"],
                    "ablations": ["Ablation"],
                    "metrics": ["Metric and statistical test"],
                    "budget": "Compute or time budget",
                    "priority": 1,
                    "evidence_ids": ["E1"],
                }
            ]
        },
        "adversarial-attack": {
            "memo": "Single strongest rejection argument",
            "evidence_ids": ["E1"],
        },
        "adversarial-adjudication": {
            "points": adjudication_points,
            "net_assessment": "Assessment without a top-level verdict",
        },
    }
    return {
        "schema_version": 2,
        "handoff_kind": kind,
        "status": "complete",
        "summary": "Compact conclusion",
        "payload": examples[kind],
        "evidence": [evidence],
        "uncertainties": [],
        "verification_needed": [],
    }


def _validate_evidence(value: Any) -> dict[str, dict[str, Any]]:
    items = _require_list(value, "evidence", 40)
    fields = {
        "id",
        "citation",
        "identifier",
        "locator",
        "source_type",
        "access_scope",
        "verification_status",
    }
    result: dict[str, dict[str, Any]] = {}
    for item in items:
        _require_exact_dict(item, fields, "evidence item")
        evidence_id = _require_string(item["id"], "evidence id", 64)
        if evidence_id in result:
            raise HandoffValidationError("duplicate evidence id")
        _require_string(item["citation"], "evidence citation", 1000)
        identifier = _require_string(item["identifier"], "evidence identifier", 1000)
        if not identifier.lower().startswith(_IDENTIFIER_PREFIXES):
            raise HandoffValidationError("unsupported evidence identifier")
        _require_string(item["locator"], "evidence locator", 1000)
        _require_enum(item["source_type"], "source type", _SOURCE_TYPES)
        _require_enum(item["access_scope"], "access scope", _ACCESS_SCOPES)
        _require_enum(item["verification_status"], "verification status", _VERIFICATION_VALUES)
        result[evidence_id] = item
    return result


def _validate_verification_items(value: Any) -> set[str]:
    items = _require_list(value, "verification_needed", 20)
    result: set[str] = set()
    for item in items:
        _require_exact_dict(item, {"item_ids", "action"}, "verification item")
        result.update(_require_string_list(item["item_ids"], "verification item ids", 20, 64))
        _require_string(item["action"], "verification action", 1000)
    return result


def _validate_uncertainties(value: Any) -> None:
    items = _require_list(value, "uncertainties", 20)
    for item in items:
        _require_exact_dict(item, {"item_ids", "statement"}, "uncertainty")
        _require_string_list(item["item_ids"], "uncertainty item ids", 20, 64)
        _require_string(item["statement"], "uncertainty statement", 1000)


def _validate_general(payload: Any, evidence: dict[str, dict[str, Any]]) -> tuple[set[str], set[str]]:
    _require_exact_dict(payload, {"findings"}, "general payload")
    findings = _require_list(payload["findings"], "findings", 20)
    fields = {"id", "statement", "epistemic_status", "confidence", "evidence_links"}
    referenced: set[str] = set()
    unverified: set[str] = set()
    seen: set[str] = set()
    for finding in findings:
        _require_exact_dict(finding, fields, "finding")
        finding_id = _unique_id(finding["id"], seen, "finding")
        _require_string(finding["statement"], "finding statement", 1400)
        status = _require_enum(finding["epistemic_status"], "epistemic status", _EPISTEMIC_VALUES)
        _require_enum(finding["confidence"], "confidence", _CONFIDENCE_VALUES)
        links = _require_list(finding["evidence_links"], "evidence links", 20)
        link_ids: list[str] = []
        supporting_verified = False
        for link in links:
            _require_exact_dict(link, {"evidence_id", "relation"}, "evidence link")
            evidence_id = _require_string(link["evidence_id"], "evidence link id", 64)
            relation = _require_enum(link["relation"], "evidence relation", _RELATION_VALUES)
            referenced.add(evidence_id)
            link_ids.append(evidence_id)
            if (
                relation == "supports"
                and evidence_id in evidence
                and evidence[evidence_id]["verification_status"] == "verified"
            ):
                supporting_verified = True
        if status == "source_fact" and not supporting_verified:
            raise HandoffValidationError("source_fact requires verified support")
        if status == "model_inference" and not link_ids:
            raise HandoffValidationError("model_inference requires evidence")
        if status == "unverified":
            unverified.add(finding_id)
    return referenced, unverified


def _validate_ideation(
    payload: Any,
    evidence: dict[str, dict[str, Any]],
    *,
    allow_partial: bool = False,
) -> tuple[set[str], set[str]]:
    _require_exact_dict(payload, {"candidates", "ranked_candidate_ids"}, "ideation payload")
    candidates = _require_list(payload["candidates"], "candidates", 20)
    minimum = 1 if allow_partial else 15
    if not minimum <= len(candidates) <= 20:
        raise HandoffValidationError("ideation requires 15-20 candidates")
    fields = {
        "id",
        "title",
        "hypothesis",
        "method",
        "cheapest_test",
        "contribution_type",
        "finer",
        "strongest_objection",
        "failure_mode",
        "recommendation",
        "evidence_ids",
    }
    referenced: set[str] = set()
    seen: set[str] = set()
    for candidate in candidates:
        _require_exact_dict(candidate, fields, "ideation candidate")
        _unique_id(candidate["id"], seen, "candidate")
        for key in ("title", "hypothesis", "method", "cheapest_test", "strongest_objection", "failure_mode"):
            _require_string(candidate[key], key, 1200)
        _require_enum(
            candidate["contribution_type"],
            "contribution type",
            {"empirical_finding", "method", "theory", "diagnostic", "dataset", "system"},
        )
        _require_enum(candidate["recommendation"], "recommendation", {"pursue", "hold", "drop"})
        finer = candidate["finer"]
        _require_exact_dict(finer, {"feasible", "interesting", "novel", "ethical", "relevant"}, "FINER")
        for score in finer.values():
            if not isinstance(score, int) or isinstance(score, bool) or not 1 <= score <= 5:
                raise HandoffValidationError("FINER scores must be integers from 1 to 5")
        referenced.update(_require_string_list(candidate["evidence_ids"], "candidate evidence ids", 20, 64))
    ranking = _require_string_list(payload["ranked_candidate_ids"], "ranked candidate ids", 20, 64)
    if len(ranking) != len(set(ranking)) or set(ranking) != seen:
        raise HandoffValidationError("ranking must contain every candidate exactly once")
    return referenced, set()


def _validate_novelty(
    payload: Any,
    evidence: dict[str, dict[str, Any]],
    *,
    allow_partial: bool = False,
) -> tuple[set[str], set[str]]:
    _require_exact_dict(payload, {"claims", "overall_assessment"}, "novelty payload")
    claims = _require_list(payload["claims"], "novelty claims", 5)
    minimum = 1 if allow_partial else 3
    if not minimum <= len(claims) <= 5:
        raise HandoffValidationError("novelty requires 3-5 claims")
    fields = {"id", "claim", "novelty", "contribution_type", "closest_work_evidence_ids", "delta"}
    referenced: set[str] = set()
    seen: set[str] = set()
    for claim in claims:
        _require_exact_dict(claim, fields, "novelty claim")
        _unique_id(claim["id"], seen, "novelty claim")
        _require_string(claim["claim"], "novelty claim", 1400)
        _require_enum(claim["novelty"], "novelty", {"HIGH", "MED", "LOW"})
        _require_enum(claim["contribution_type"], "contribution type", {"method", "finding", "both"})
        referenced.update(_require_string_list(claim["closest_work_evidence_ids"], "closest work evidence ids", 12, 64))
        _require_string(claim["delta"], "novelty delta", 1200)
    _require_string(payload["overall_assessment"], "overall assessment", 1600)
    return referenced, set()


def _validate_manuscript_draft(payload: Any, evidence: dict[str, dict[str, Any]]) -> tuple[set[str], set[str]]:
    fields = {"draft", "claim_ids", "citation_evidence_ids", "unresolved_items"}
    _require_exact_dict(payload, fields, "manuscript draft payload")
    _require_string(payload["draft"], "draft", 30000)
    _require_string_list(payload["claim_ids"], "claim ids", 50, 128)
    referenced = set(_require_string_list(payload["citation_evidence_ids"], "citation evidence ids", 50, 64))
    _require_string_list(payload["unresolved_items"], "unresolved items", 30, 1000)
    return referenced, set()


def _validate_venue_review(payload: Any, evidence: dict[str, dict[str, Any]]) -> tuple[set[str], set[str]]:
    fields = {"strengths", "weaknesses", "questions", "score", "reviewer_confidence", "accept_lift_conditions"}
    _require_exact_dict(payload, fields, "venue review payload")
    referenced: set[str] = set()
    for name, limit in (("strengths", 10), ("weaknesses", 10)):
        items = _require_list(payload[name], name, limit)
        seen: set[str] = set()
        expected = {"id", "statement", "evidence_ids"}
        if name == "weaknesses":
            expected.add("severity")
        for item in items:
            _require_exact_dict(item, expected, name[:-1])
            _unique_id(item["id"], seen, name[:-1])
            _require_string(item["statement"], f"{name} statement", 1400)
            if name == "weaknesses":
                _require_enum(item["severity"], "severity", {"critical", "major", "minor"})
            referenced.update(_require_string_list(item["evidence_ids"], f"{name} evidence ids", 20, 64))
    _require_string_list(payload["questions"], "review questions", 10, 1000)
    _require_string(payload["score"], "review score", 200)
    confidence = payload["reviewer_confidence"]
    _require_exact_dict(confidence, {"level", "rationale"}, "reviewer confidence")
    _require_enum(confidence["level"], "reviewer confidence level", _CONFIDENCE_VALUES)
    _require_string(confidence["rationale"], "reviewer confidence rationale", 1000)
    _require_string_list(payload["accept_lift_conditions"], "accept lift conditions", 10, 1000)
    return referenced, set()


def _validate_results_claims_matrix(payload: Any, evidence: dict[str, dict[str, Any]]) -> tuple[set[str], set[str]]:
    _require_exact_dict(payload, {"rows"}, "results claims matrix payload")
    rows = _require_list(payload["rows"], "matrix rows", 32)
    fields = {"id", "outcomes", "defensible_claims", "unsupported_claims", "evidence_ids"}
    referenced: set[str] = set()
    seen: set[str] = set()
    for row in rows:
        _require_exact_dict(row, fields, "matrix row")
        _unique_id(row["id"], seen, "matrix row")
        _require_string_list(row["outcomes"], "outcomes", 12, 1000)
        _require_string_list(row["defensible_claims"], "defensible claims", 20, 1200)
        _require_string_list(row["unsupported_claims"], "unsupported claims", 20, 1200)
        referenced.update(_require_string_list(row["evidence_ids"], "matrix evidence ids", 20, 64))
    return referenced, set()


def _validate_experiment_plan(payload: Any, evidence: dict[str, dict[str, Any]]) -> tuple[set[str], set[str]]:
    _require_exact_dict(payload, {"experiments"}, "experiment plan payload")
    experiments = _require_list(payload["experiments"], "experiments", 4)
    if not 1 <= len(experiments) <= 4:
        raise HandoffValidationError("experiment plan requires 1-4 experiments")
    fields = {
        "id",
        "title",
        "datasets",
        "baselines",
        "model_scales",
        "hyperparameters",
        "ablations",
        "metrics",
        "budget",
        "priority",
        "evidence_ids",
    }
    referenced: set[str] = set()
    seen: set[str] = set()
    priorities: set[int] = set()
    for experiment in experiments:
        _require_exact_dict(experiment, fields, "experiment")
        _unique_id(experiment["id"], seen, "experiment")
        _require_string(experiment["title"], "experiment title", 500)
        for key in ("datasets", "baselines", "model_scales", "hyperparameters", "ablations", "metrics"):
            _require_string_list(experiment[key], key, 30, 1000)
        _require_string(experiment["budget"], "experiment budget", 500)
        priority = experiment["priority"]
        if not isinstance(priority, int) or isinstance(priority, bool) or priority < 1:
            raise HandoffValidationError("experiment priority must be a positive integer")
        priorities.add(priority)
        referenced.update(_require_string_list(experiment["evidence_ids"], "experiment evidence ids", 20, 64))
    if len(priorities) != len(experiments):
        raise HandoffValidationError("experiment priorities must be unique")
    return referenced, set()


def _validate_adversarial_attack(payload: Any, evidence: dict[str, dict[str, Any]]) -> tuple[set[str], set[str]]:
    _require_exact_dict(payload, {"memo", "evidence_ids"}, "adversarial attack payload")
    _require_string(payload["memo"], "attack memo", 4000)
    referenced = set(_require_string_list(payload["evidence_ids"], "attack evidence ids", 20, 64))
    return referenced, set()


def _validate_adversarial_adjudication(
    payload: Any,
    evidence: dict[str, dict[str, Any]],
    *,
    allow_partial: bool = False,
) -> tuple[set[str], set[str]]:
    _require_exact_dict(payload, {"points", "net_assessment"}, "adversarial adjudication payload")
    points = _require_list(payload["points"], "adjudication points", 7)
    minimum = 1 if allow_partial else 3
    if not minimum <= len(points) <= 7:
        raise HandoffValidationError("adjudication requires 3-7 points")
    base_fields = {"id", "attack_claim", "ruling", "evidence_ids"}
    extra_fields = {"severity", "needs_experiment", "recommended_fix"}
    referenced: set[str] = set()
    seen: set[str] = set()
    for point in points:
        if not isinstance(point, dict):
            raise HandoffValidationError("adjudication point must be an object")
        ruling = point.get("ruling")
        expected = base_fields if ruling == "answered_by_current_text" else base_fields | extra_fields
        _require_exact_dict(point, expected, "adjudication point")
        _unique_id(point["id"], seen, "adjudication point")
        _require_string(point["attack_claim"], "attack claim", 1200)
        _require_enum(ruling, "ruling", {"answered_by_current_text", "partially", "unresolved"})
        referenced.update(_require_string_list(point["evidence_ids"], "point evidence ids", 20, 64))
        if ruling != "answered_by_current_text":
            _require_enum(point["severity"], "severity", {"critical", "major", "minor"})
            if not isinstance(point["needs_experiment"], bool):
                raise HandoffValidationError("needs_experiment must be boolean")
            _require_string(point["recommended_fix"], "recommended fix", 1200)
    _require_string(payload["net_assessment"], "net assessment", 2000)
    return referenced, set()


def _require_known_evidence(ids: set[str], evidence: dict[str, dict[str, Any]]) -> None:
    unknown = ids - set(evidence)
    if unknown:
        raise HandoffValidationError("unknown evidence id: " + ", ".join(sorted(unknown)))


def _unique_id(value: Any, seen: set[str], name: str) -> str:
    item_id = _require_string(value, f"{name} id", 64)
    if item_id in seen:
        raise HandoffValidationError(f"duplicate {name} id")
    seen.add(item_id)
    return item_id


def _secure_write(path: Path, content: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise
    if os.name == "posix":
        os.chmod(path, 0o600)
        if stat.S_IMODE(path.stat().st_mode) != 0o600:
            raise PermissionError("could not secure handoff file")


def _require_exact_dict(value: Any, fields: set[str], name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise HandoffValidationError(f"invalid {name} fields")
    return value


def _require_enum(value: Any, name: str, allowed: set[str]) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise HandoffValidationError(f"invalid {name}")
    return value


def _require_string(value: Any, name: str, max_length: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > max_length:
        raise HandoffValidationError(f"invalid {name}")
    return value


def _require_list(value: Any, name: str, max_items: int) -> list[Any]:
    if not isinstance(value, list) or len(value) > max_items:
        raise HandoffValidationError(f"invalid {name}")
    return value


def _require_string_list(value: Any, name: str, max_items: int, max_length: int) -> list[str]:
    items = _require_list(value, name, max_items)
    for item in items:
        _require_string(item, name, max_length)
    return items
