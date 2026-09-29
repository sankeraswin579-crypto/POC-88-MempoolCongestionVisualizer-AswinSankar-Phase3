from __future__ import annotations

from typing import Any


def _metadata(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "data_version": item["data_version"],
        "method_version": item["method_version"],
        "quality_status": item["quality_status"],
    }


def _package_metadata(
    evidence: dict[str, Any],
) -> dict[str, Any]:
    metadata = evidence.get(
        "package_metadata",
        {},
    )

    return {
        "data_version": metadata.get("data_version"),
        "method_version": metadata.get("method_version"),
        "quality_status": metadata.get("quality_status"),
    }


def compose_response(
    intent_name: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:

    evidence_type = evidence["type"]

    # ---------------------------------------------------------
    # NOT FOUND
    # ---------------------------------------------------------
    if evidence_type == "not_found":
        return {
            "status": "unavailable",
            "answer": (
                "No approved comparative result matched the "
                "requested metric or category."
            ),
            "evidence_references": [],
            "key_values": [],
            "metadata": _package_metadata(evidence),
            "limitation": (
                "The assistant only answers from the approved "
                "Track A comparative evidence package."
            ),
            "suggested_follow_ups": [
                "List the available comparison groups.",
                "Ask for the baseline of a supported metric.",
            ],
        }

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------
    if evidence_type == "summary":
        summary = evidence["summary"]

        metadata = _package_metadata(evidence)

        if not metadata["data_version"]:
            metadata["data_version"] = summary["data_version"]

        if not metadata["method_version"]:
            metadata["method_version"] = (
                "dynamic-from-approved-results"
            )

        if not metadata["quality_status"]:
            metadata["quality_status"] = (
                summary["validation_status"]
            )

        return {
            "status": "answered",
            "answer": summary["interpretation"],
            "evidence_references": evidence["evidence_references"],
            "key_values": [
                {
                    "name": "canonical_records",
                    "value": summary["record_count"],
                },
                {
                    "name": "comparative_groups",
                    "value": summary["comparative_group_count"],
                },
                {
                    "name": "findings",
                    "value": summary["finding_count"],
                },
            ],
            "metadata": metadata,
            "limitation": summary["temporal_context"],
            "suggested_follow_ups": [
                "List the available comparison groups.",
                "Ask for the baseline of a metric.",
                "Ask about the approved limitations.",
            ],
        }

    # ---------------------------------------------------------
    # COMPARISON GROUPS
    # ---------------------------------------------------------
    if evidence_type == "comparison_groups":
        groups = evidence["groups"]

        names = ", ".join(
            f'{item["metric_name"]} ({item["category"]})'
            for item in groups
        )

        metadata = _package_metadata(evidence)

        if not metadata["data_version"] and groups:
            metadata["data_version"] = groups[0].get(
                "data_version"
            )

        if not metadata["method_version"] and groups:
            metadata["method_version"] = groups[0].get(
                "method_version"
            )

        if not metadata["quality_status"] and groups:
            metadata["quality_status"] = groups[0].get(
                "quality_status"
            )

        return {
            "status": "answered",
            "answer": (
                f"The approved comparative package contains "
                f"{len(groups)} supported metric groups: {names}."
            ),
            "evidence_references": evidence["evidence_references"],
            "key_values": [
                {
                    "name": item["metric_name"],
                    "value": item["metric_name"],
                    "unit": item.get("result_unit"),
                }
                for item in groups
            ],
            "metadata": metadata,
            "limitation": (
                "Only compatible metric groups from the approved "
                "comparative package are supported."
            ),
            "suggested_follow_ups": [
                "Ask for the baseline of a supported metric.",
                "Ask for the range of a supported metric.",
            ],
        }

    # ---------------------------------------------------------
    # RESULT-SPECIFIC EVIDENCE
    # ---------------------------------------------------------
    item = evidence["item"]

    # ---------------------------------------------------------
    # BASELINE
    # ---------------------------------------------------------
    if evidence_type == "baseline":
        return {
            "status": "answered",
            "answer": (
                f'The approved comparative baseline for '
                f'{item["metric_name"]} is '
                f'{evidence["value"]} {item["result_unit"]}.'
            ),
            "evidence_references": [item["result_id"]],
            "key_values": [
                {
                    "name": "baseline",
                    "value": evidence["value"],
                    "unit": item["result_unit"],
                },
                {
                    "name": "observations",
                    "value": item["evidence"]["observation_count"],
                },
            ],
            "metadata": _metadata(item),
            "limitation": item["limitation"],
            "suggested_follow_ups": [
                f'Ask for the range of {item["metric_name"]}.',
                f'Ask what finding was recorded for {item["metric_name"]}.',
            ],
        }

    # ---------------------------------------------------------
    # RANGE
    # ---------------------------------------------------------
    if evidence_type == "range":
        return {
            "status": "answered",
            "answer": (
                f'{item["metric_name"]} ranges from '
                f'{evidence["minimum"]} to '
                f'{evidence["maximum"]} {item["result_unit"]}, '
                f'with a range of {evidence["range"]}.'
            ),
            "evidence_references": [item["result_id"]],
            "key_values": [
                {
                    "name": "minimum",
                    "value": evidence["minimum"],
                    "unit": item["result_unit"],
                },
                {
                    "name": "maximum",
                    "value": evidence["maximum"],
                    "unit": item["result_unit"],
                },
                {
                    "name": "range",
                    "value": evidence["range"],
                    "unit": item["result_unit"],
                },
            ],
            "metadata": _metadata(item),
            "limitation": item["limitation"],
            "suggested_follow_ups": [
                f'Ask for the baseline of {item["metric_name"]}.',
            ],
        }

    # ---------------------------------------------------------
    # EXTREME
    # ---------------------------------------------------------
    if evidence_type == "extreme":
        return {
            "status": "answered",
            "answer": (
                f'The {evidence["extreme"]} observed value for '
                f'{item["metric_name"]} is '
                f'{evidence["value"]} {item["result_unit"]}.'
            ),
            "evidence_references": [item["result_id"]],
            "key_values": [
                {
                    "name": evidence["extreme"],
                    "value": evidence["value"],
                    "unit": item["result_unit"],
                }
            ],
            "metadata": _metadata(item),
            "limitation": item["limitation"],
            "suggested_follow_ups": [
                f'Ask for the baseline of {item["metric_name"]}.',
            ],
        }

    # ---------------------------------------------------------
    # RECORD COMPARISON
    # ---------------------------------------------------------
    if evidence_type == "comparison":
        direction = (
            "above"
            if evidence["difference"] > 0
            else "below"
            if evidence["difference"] < 0
            else "equal to"
        )

        return {
            "status": "answered",
            "answer": (
                f'The approved result for {item["metric_name"]} '
                f'is {evidence["value"]} {item["result_unit"]}, '
                f'which is {abs(evidence["difference"])} '
                f'{item["result_unit"]} {direction} the '
                f'comparative baseline of {evidence["baseline"]} '
                f'{item["result_unit"]}.'
            ),
            "evidence_references": [item["result_id"]],
            "key_values": [
                {
                    "name": "observed_value",
                    "value": evidence["value"],
                    "unit": item["result_unit"],
                },
                {
                    "name": "baseline",
                    "value": evidence["baseline"],
                    "unit": item["result_unit"],
                },
                {
                    "name": "difference",
                    "value": evidence["difference"],
                    "unit": item["result_unit"],
                },
            ],
            "metadata": _metadata(item),
            "limitation": item["limitation"],
            "suggested_follow_ups": [
                f'Ask for the range of {item["metric_name"]}.',
            ],
        }

    # ---------------------------------------------------------
    # RESULT EXPLANATION
    # ---------------------------------------------------------
    if evidence_type == "result_explanation":
        return {
            "status": "answered",
            "answer": item["finding"],
            "evidence_references": [item["result_id"]],
            "key_values": [
                {
                    "name": "observation_count",
                    "value": item["evidence"]["observation_count"],
                },
                {
                    "name": "baseline",
                    "value": item["evidence"]["baseline_value"],
                    "unit": item["result_unit"],
                },
            ],
            "metadata": _metadata(item),
            "limitation": item["limitation"],
            "suggested_follow_ups": [
                f'Ask for the range of {item["metric_name"]}.',
            ],
        }

    # ---------------------------------------------------------
    # APPROVED METHOD
    # ---------------------------------------------------------
    if evidence_type == "method":
        return {
            "status": "answered",
            "answer": (
                f'This result belongs to '
                f'{evidence["primary_track"]}. '
                f'The approved baseline method is '
                f'{item["baseline_method"]}. '
                f'The current method version is '
                f'{item["method_version"]}.'
            ),
            "evidence_references": [item["result_id"]],
            "key_values": [
                {
                    "name": "track",
                    "value": evidence["primary_track"],
                },
                {
                    "name": "baseline_method",
                    "value": item["baseline_method"],
                },
                {
                    "name": "method_version",
                    "value": item["method_version"],
                },
            ],
            "metadata": _metadata(item),
            "limitation": item["limitation"],
            "suggested_follow_ups": [
                "Ask about the approved analytical limitations.",
            ],
        }

    # ---------------------------------------------------------
    # LIMITATION
    # ---------------------------------------------------------
    if evidence_type == "limitation":
        return {
            "status": "answered",
            "answer": evidence["summary_limitation"],
            "evidence_references": [item["result_id"]],
            "key_values": [
                {
                    "name": "approved_track",
                    "value": "Track A — Comparative",
                }
            ],
            "metadata": _metadata(item),
            "limitation": item["limitation"],
            "suggested_follow_ups": [
                "Ask for the approved method.",
                "Ask for the baseline of a supported metric.",
            ],
        }

    # ---------------------------------------------------------
    # DATA FRESHNESS
    # ---------------------------------------------------------
    if evidence_type == "freshness":
        return {
            "status": "answered",
            "answer": (
                f'The approved package uses data version '
                f'{evidence["data_version"]}, was generated at '
                f'{evidence["generated_at"]}, and has validation '
                f'status {evidence["validation_status"]}.'
            ),
            "evidence_references": [],
            "key_values": [
                {
                    "name": "data_version",
                    "value": evidence["data_version"],
                },
                {
                    "name": "method_versions",
                    "value": evidence["method_versions"],
                },
                {
                    "name": "generated_at",
                    "value": evidence["generated_at"],
                },
            ],
            "metadata": {
                "data_version": evidence["data_version"],
                "method_version": evidence["method_versions"],
                "quality_status": evidence["validation_status"],
            },
            "limitation": (
                "Freshness describes the captured approved "
                "evidence package; it does not establish a "
                "continuous live analytical trend."
            ),
            "suggested_follow_ups": [
                "List the available comparison groups.",
            ],
        }

    raise ValueError(
        f"Unsupported evidence type: {evidence_type}"
    )