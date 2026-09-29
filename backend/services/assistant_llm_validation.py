from __future__ import annotations

import re
from typing import Any


NUMBER_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])[-+]?(?:\d+(?:\.\d+)?)(?![A-Za-z0-9_])"
)


def _allowed_numbers(value: Any) -> set[str]:
    if isinstance(value, bool) or value is None:
        return set()

    if isinstance(value, (int, float)):
        return {
            str(value),
            f"{value:g}",
        }

    if isinstance(value, str):
        return set(
            NUMBER_PATTERN.findall(value)
        )

    if isinstance(value, list):
        output: set[str] = set()
        for item in value:
            output.update(_allowed_numbers(item))
        return output

    if isinstance(value, dict):
        output: set[str] = set()
        for item in value.values():
            output.update(_allowed_numbers(item))
        return output

    return set()


def validate_llm_output(
    llm_result: dict[str, Any] | None,
    evidence: dict[str, Any],
    deterministic_response: dict[str, Any],
) -> str | None:

    if not isinstance(llm_result, dict):
        return None

    answer = llm_result.get("answer")

    if not isinstance(answer, str) or not answer.strip():
        return None

    allowed_references = set(
        deterministic_response.get(
            "evidence_references",
            [],
        )
    )

    supplied_references = llm_result.get(
        "evidence_references",
        deterministic_response.get(
            "evidence_references",
            [],
        ),
    )

    if not isinstance(supplied_references, list):
        return None

    if not set(supplied_references).issubset(
        allowed_references
    ):
        return None

    allowed_numbers = _allowed_numbers(evidence)
    allowed_numbers.update(
        _allowed_numbers(
            deterministic_response.get(
                "key_values",
                [],
            )
        )
    )

    answer_numbers = set(
        NUMBER_PATTERN.findall(answer)
    )

    if not answer_numbers.issubset(allowed_numbers):
        return None

    return answer.strip()
