from __future__ import annotations

import re
from dataclasses import dataclass


SUPPORTED_INTENTS = {
    "get_summary",
    "list_comparison_groups",
    "get_group_baseline",
    "get_group_range",
    "get_group_extreme",
    "compare_record_to_baseline",
    "explain_result",
    "explain_method",
    "explain_limitation",
    "get_data_freshness",
}


PREDICTION_PATTERNS = [
    r"\bforecast\b",
    r"\bforecasting\b",
    r"\bpredict\b",
    r"\bpredictive\b",
    r"\btomorrow'?s?\b",
    r"\bnext\s+(hour|day|week|month)\b",
    r"\bfuture\s+(congestion|value|trend|price|activity)\b",
]


def is_unsupported_prediction(question: str) -> bool:
    normalized = question.strip().lower()

    return any(
        re.search(
            pattern,
            normalized,
            flags=re.IGNORECASE,
        )
        for pattern in PREDICTION_PATTERNS
    )


@dataclass(frozen=True)
class Intent:
    name: str
    metric_name: str | None = None
    category: str | None = None
    extreme: str | None = None
    result_id: str | None = None


METRIC_ALIASES = {
    "difficulty": "difficulty",
    "block difficulty": "difficulty",
    "size": "size",
    "block size": "size",
    "transaction count": "tx_count",
    "transaction": "tx_count",
    "tx count": "tx_count",
    "tx_count": "tx_count",
    "weight": "weight",
    "economy fee": "economy_fee",
    "economy_fee": "economy_fee",
    "fastest fee": "fastest_fee",
    "fastest_fee": "fastest_fee",
    "half hour fee": "half_hour_fee",
    "half_hour_fee": "half_hour_fee",
    "hour fee": "hour_fee",
    "hour_fee": "hour_fee",
    "minimum fee": "minimum_fee",
    "minimum_fee": "minimum_fee",
    "total fee": "total_fee",
    "total_fee": "total_fee",
    "virtual size": "virtual_size",
    "virtual_size": "virtual_size",
    "mempool transaction count": "transaction_count",
    "mempool transactions": "transaction_count",
}


CATEGORY_ALIASES = {
    "block": "bitcoin_block",
    "bitcoin block": "bitcoin_block",
    "bitcoin_block": "bitcoin_block",
    "fees": "fees",
    "fee": "fees",
    "mempool": "mempool",
}


def extract_metric(question: str) -> str | None:
    normalized = question.lower()

    for alias, metric in sorted(
        METRIC_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if alias in normalized:
            return metric

    return None


def extract_category(question: str) -> str | None:
    normalized = question.lower()

    for alias, category in sorted(
        CATEGORY_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        if alias in normalized:
            return category

    return None


def classify_question(question: str) -> Intent | None:
    normalized = question.strip().lower()

    metric = extract_metric(question)
    category = extract_category(question)

    result_match = re.search(
        r"\bPOC88-COMP-\d{4}\b",
        question,
        flags=re.IGNORECASE,
    )

    result_id = (
        result_match.group(0).upper()
        if result_match
        else None
    )

    if any(
        phrase in normalized
        for phrase in [
            "how fresh",
            "data freshness",
            "when was the data",
            "data version",
            "method version",
            "what version",
        ]
    ):
        return Intent("get_data_freshness")

    if any(
        phrase in normalized
        for phrase in [
            "what is the approved track",
            "what is the approved comparative method",
            "what is the approved analytical method",
            "approved comparative method",
            "approved analytical method",
            "what method",
            "which method",
            "what track",
            "how was this calculated",
            "how is the baseline calculated",
            "baseline method",
            "comparative method",
        ]
    ):
        return Intent(
            "explain_method",
            metric,
            category,
            None,
            result_id,
        )

    if any(
        phrase in normalized
        for phrase in [
            "limitation",
            "limitations",
            "what can this analysis not",
            "what can't this analysis",
            "can this predict",
            "can this forecast",
        ]
    ):
        return Intent(
            "explain_limitation",
            metric,
            category,
            None,
            result_id,
        )

    if any(
        phrase in normalized
        for phrase in [
            "summary",
            "summarize",
            "overall result",
            "overall findings",
            "what does the analysis show",
        ]
    ):
        return Intent("get_summary")

    if any(
        phrase in normalized
        for phrase in [
            "what groups",
            "which groups",
            "comparison groups",
            "available metrics",
            "available comparisons",
        ]
    ):
        return Intent("list_comparison_groups")

    if any(
        phrase in normalized
        for phrase in [
            "highest",
            "lowest",
            "maximum",
            "minimum",
        ]
    ) and metric:
        extreme = (
            "highest"
            if any(
                word in normalized
                for word in [
                    "highest",
                    "maximum",
                ]
            )
            else "lowest"
        )

        return Intent(
            "get_group_extreme",
            metric,
            category,
            extreme,
            result_id,
        )

    if any(
        phrase in normalized
        for phrase in [
            "range",
            "minimum and maximum",
            "min and max",
            "min/max",
        ]
    ):
        return Intent(
            "get_group_range",
            metric,
            category,
            None,
            result_id,
        )

    if any(
        phrase in normalized
        for phrase in [
            "compare",
            "compared with",
            "compared to",
            "difference from baseline",
            "against the baseline",
        ]
    ):
        return Intent(
            "compare_record_to_baseline",
            metric,
            category,
            None,
            result_id,
        )

    if any(
        phrase in normalized
        for phrase in [
            "baseline",
            "average",
            "mean",
        ]
    ):
        return Intent(
            "get_group_baseline",
            metric,
            category,
            None,
            result_id,
        )

    if any(
        phrase in normalized
        for phrase in [
            "explain this result",
            "explain the finding",
            "why does this result",
            "what does this finding mean",
        ]
    ):
        return Intent(
            "explain_result",
            metric,
            category,
            None,
            result_id,
        )

    return None