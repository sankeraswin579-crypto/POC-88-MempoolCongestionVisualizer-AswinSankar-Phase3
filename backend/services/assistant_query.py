from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from services.assistant_intents import Intent


REPO_ROOT = Path(__file__).resolve().parents[2]

RESULTS_PATH = (
    REPO_ROOT
    / "data-science"
    / "outputs"
    / "intelligence_results.json"
)

SUMMARY_PATH = (
    REPO_ROOT
    / "data-science"
    / "outputs"
    / "intelligence_summary.json"
)


APPROVED_LIMITATION = (
    "The approved comparative analysis does not establish "
    "temporal trends, forecasting, or predictive capability."
)


def load_approved_package() -> tuple[dict[str, Any], dict[str, Any]]:
    with RESULTS_PATH.open("r", encoding="utf-8") as handle:
        results = json.load(handle)

    with SUMMARY_PATH.open("r", encoding="utf-8") as handle:
        summary = json.load(handle)

    # --------------------------------------------------
    # Approved analytical track validation
    # --------------------------------------------------

    if results.get("primary_track") != "Track A — Comparative":
        raise RuntimeError(
            "Approved assistant source is not Track A — Comparative."
        )

    if summary.get("primary_track") != results.get("primary_track"):
        raise RuntimeError(
            "Track mismatch between intelligence sources."
        )

    # --------------------------------------------------
    # Data-version consistency validation
    # --------------------------------------------------

    for item in results.get("results", []):
        if item.get("data_version") != summary.get("data_version"):
            raise RuntimeError(
                "Data version mismatch in approved intelligence package."
            )

    return results, summary


def _find_result(
    results: dict[str, Any],
    metric_name: str | None,
    category: str | None,
    result_id: str | None,
) -> dict[str, Any] | None:

    candidates = results.get("results", [])

    # Explicit result ID takes priority.
    if result_id:
        for item in candidates:
            if item.get("result_id") == result_id:
                return item

    # Filter by metric.
    if metric_name:
        candidates = [
            item
            for item in candidates
            if item.get("metric_name") == metric_name
        ]

    # Filter by category.
    if category:
        candidates = [
            item
            for item in candidates
            if item.get("category") == category
        ]

    return candidates[0] if candidates else None


def _evidence(item: dict[str, Any]) -> dict[str, Any]:
    """
    Return only approved evidence fields required by the
    deterministic assistant and grounded explanation layer.

    The canonical dataset is never passed through this function.
    """

    return {
        "result_id": item["result_id"],
        "metric_name": item["metric_name"],
        "category": item["category"],
        "result_value": item["result_value"],
        "result_unit": item["result_unit"],
        "finding": item["finding"],
        "finding_type": item["finding_type"],
        "evidence": item["evidence"],
        "method_version": item["method_version"],
        "baseline_method": item["baseline_method"],
        "data_version": item["data_version"],
        "quality_status": item["quality_status"],
        "limitation": item["limitation"],
        "generated_at": item["generated_at"],
    }


def _package_metadata(
    results: dict[str, Any],
    summary: dict[str, Any],
) -> dict[str, Any]:

    items = results.get("results", [])

    method_versions = sorted(
        {
            item["method_version"]
            for item in items
            if item.get("method_version")
        }
    )

    return {
        "data_version": summary["data_version"],
        "method_version": method_versions,
        "quality_status": summary["validation_status"],
        "primary_track": summary["primary_track"],
        "limitation": APPROVED_LIMITATION,
    }


def query_approved_evidence(
    intent: Intent,
) -> dict[str, Any]:

    results, summary = load_approved_package()

    items = results.get("results", [])

    package_metadata = _package_metadata(
        results,
        summary,
    )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    if intent.name == "get_summary":
        return {
            "type": "summary",
            "summary": summary,
            "package_metadata": package_metadata,
            "evidence_references": [
                item["result_id"]
                for item in items
            ],
        }

    # --------------------------------------------------
    # COMPARISON GROUPS
    # --------------------------------------------------

    if intent.name == "list_comparison_groups":

        groups = [
            {
                "result_id": item["result_id"],
                "metric_name": item["metric_name"],
                "category": item["category"],
                "unit": item["result_unit"],
                "data_version": item["data_version"],
                "method_version": item["method_version"],
                "quality_status": item["quality_status"],
            }
            for item in items
        ]

        return {
            "type": "comparison_groups",
            "groups": groups,
            "package_metadata": package_metadata,
            "evidence_references": [
                item["result_id"]
                for item in items
            ],
        }

    # --------------------------------------------------
    # RESULT LOOKUP
    # --------------------------------------------------

    item = _find_result(
        results=results,
        metric_name=intent.metric_name,
        category=intent.category,
        result_id=intent.result_id,
    )

    if item is None:
        return {
            "type": "not_found",
            "package_metadata": package_metadata,
            "evidence_references": [],
        }

    # --------------------------------------------------
    # BASELINE
    # --------------------------------------------------

    if intent.name == "get_group_baseline":

        return {
            "type": "baseline",
            "item": _evidence(item),
            "value": item["evidence"]["baseline_value"],
            "package_metadata": package_metadata,
        }

    # --------------------------------------------------
    # RANGE
    # --------------------------------------------------

    if intent.name == "get_group_range":

        evidence = item["evidence"]

        return {
            "type": "range",
            "item": _evidence(item),
            "minimum": evidence["minimum"],
            "maximum": evidence["maximum"],
            "range": evidence["range"],
            "package_metadata": package_metadata,
        }

    # --------------------------------------------------
    # EXTREME
    # --------------------------------------------------

    if intent.name == "get_group_extreme":

        evidence = item["evidence"]

        value = (
            evidence["maximum"]
            if intent.extreme == "highest"
            else evidence["minimum"]
        )

        return {
            "type": "extreme",
            "item": _evidence(item),
            "extreme": intent.extreme,
            "value": value,
            "package_metadata": package_metadata,
        }

    # --------------------------------------------------
    # RECORD COMPARISON
    # --------------------------------------------------

    if intent.name == "compare_record_to_baseline":

        baseline = item["evidence"]["baseline_value"]
        current = item["result_value"]

        return {
            "type": "comparison",
            "item": _evidence(item),
            "value": current,
            "baseline": baseline,
            "difference": current - baseline,
            "package_metadata": package_metadata,
        }

    # --------------------------------------------------
    # RESULT EXPLANATION
    # --------------------------------------------------

    if intent.name == "explain_result":

        return {
            "type": "result_explanation",
            "item": _evidence(item),
            "package_metadata": package_metadata,
        }

    # --------------------------------------------------
    # APPROVED METHOD
    # --------------------------------------------------

    if intent.name == "explain_method":

        return {
            "type": "method",
            "item": _evidence(item),
            "primary_track": summary["primary_track"],
            "package_metadata": package_metadata,
        }

    # --------------------------------------------------
    # APPROVED LIMITATION
    # --------------------------------------------------

    if intent.name == "explain_limitation":

        return {
            "type": "limitation",
            "item": _evidence(item),
            "primary_track": summary["primary_track"],
            "summary_limitation": APPROVED_LIMITATION,
            "package_metadata": package_metadata,
        }

    # --------------------------------------------------
    # DATA FRESHNESS
    # --------------------------------------------------

    if intent.name == "get_data_freshness":

        method_versions = sorted(
            {
                item["method_version"]
                for item in items
                if item.get("method_version")
            }
        )

        return {
            "type": "freshness",
            "data_version": summary["data_version"],
            "method_versions": method_versions,
            "generated_at": summary["generated_at"],
            "validation_status": summary["validation_status"],
            "primary_track": summary["primary_track"],
            "package_metadata": package_metadata,
            "evidence_references": [],
        }

    raise ValueError(
        f"Unsupported assistant intent: {intent.name}"
    )