from __future__ import annotations

from typing import Any


def validate_grounded_response(
    response: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:

    if response.get("status") != "answered":
        return response

    references = response.get(
        "evidence_references",
        [],
    )

    evidence_type = evidence.get("type")

    if evidence_type not in {
        "summary",
        "comparison_groups",
        "freshness",
        "not_found",
    }:
        item = evidence.get("item")

        if item is None:
            raise ValueError(
                "Grounded response is missing source evidence."
            )

        if item["result_id"] not in references:
            raise ValueError(
                "Grounded response does not reference "
                "its source result."
            )

    metadata = evidence.get(
        "package_metadata",
        {},
    )

    response["metadata"] = {
        "data_version": metadata.get(
            "data_version",
            response.get("metadata", {}).get(
                "data_version"
            ),
        ),
        "method_version": metadata.get(
            "method_version",
            response.get("metadata", {}).get(
                "method_version"
            ),
        ),
        "quality_status": metadata.get(
            "quality_status",
            response.get("metadata", {}).get(
                "quality_status"
            ),
        ),
    }

    if not response.get("answer"):
        raise ValueError(
            "Grounded response contains no answer."
        )

    if not response.get("limitation"):
        raise ValueError(
            "Grounded response is missing a limitation."
        )

    return response
