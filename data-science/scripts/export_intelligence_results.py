from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "comparative_track_raw.json"
)

VALIDATION_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "validation_metrics.json"
)

RESULTS_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "intelligence_results.json"
)

SUMMARY_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "intelligence_summary.json"
)

WEAK_CASE_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "weak_case_review.json"
)

DATA_VERSION = "1.0.1"


def utc_now() -> str:
    return datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def main() -> None:

    print(
        "Exporting Track A — Comparative "
        "intelligence results..."
    )

    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Comparative output not found: {RAW_PATH}"
        )

    if not VALIDATION_PATH.exists():
        raise FileNotFoundError(
            f"Validation output not found: "
            f"{VALIDATION_PATH}"
        )

    raw = json.loads(
        RAW_PATH.read_text(
            encoding="utf-8"
        )
    )

    validation = json.loads(
        VALIDATION_PATH.read_text(
            encoding="utf-8"
        )
    )

    generated_at = utc_now()

    quality_status = validation.get(
        "status",
        "UNKNOWN",
    )

    intelligence_results = []

    result_counter = 1

    for finding in raw.get(
        "findings",
        []
    ):

        result = {
            "result_id": (
                f"POC88-COMP-{result_counter:04d}"
            ),
            "result_type": (
                "comparative_metric_baseline"
            ),
            "primary_track": (
                "Track A — Comparative"
            ),
            "metric_name": finding[
                "metric_name"
            ],
            "result_value": finding[
                "baseline_value"
            ],
            "result_unit": finding[
                "metric_unit"
            ],
            "category": finding[
                "category"
            ],
            "finding_type": finding[
                "finding_type"
            ],
            "finding": finding[
                "finding"
            ],
            "evidence": {
                "observation_count": finding[
                    "observation_count"
                ],
                "baseline_value": finding[
                    "baseline_value"
                ],
                "minimum": finding[
                    "minimum"
                ],
                "maximum": finding[
                    "maximum"
                ],
                "range": finding[
                    "range"
                ],
            },
            "method_version": (
                "comparative-track-v1.0"
            ),
            "baseline_method": (
                "arithmetic_mean"
            ),
            "data_version": DATA_VERSION,
            "generated_at": generated_at,
            "quality_status": quality_status,
            "limitation": (
                "Comparative findings are limited "
                "to compatible metric groups in "
                "the captured operational sample. "
                "They do not establish temporal "
                "trends, forecasting, or predictive "
                "capability."
            ),
        }

        intelligence_results.append(
            result
        )

        result_counter += 1

    RESULTS_PATH.write_text(
        json.dumps(
            {
                "primary_track": (
                    "Track A — Comparative"
                ),
                "results": intelligence_results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    summary = {
        "summary_type": (
            "comparative_analytical_track_summary"
        ),
        "primary_track": (
            "Track A — Comparative"
        ),
        "data_version": DATA_VERSION,
        "analysis_type": raw.get(
            "analysis_type"
        ),
        "record_count": raw.get(
            "record_count"
        ),
        "comparative_group_count": len(
            raw.get(
                "comparative_groups",
                []
            )
        ),
        "finding_count": len(
            raw.get(
                "findings",
                []
            )
        ),
        "validation_status": quality_status,
        "interpretation": (
            "The analytical track establishes "
            "deterministic comparative baselines "
            "for compatible metric groups and "
            "compares observed measurements against "
            "those baselines."
        ),
        "temporal_context": (
            "Timestamps are retained as supporting "
            "evidence only. No unsupported temporal "
            "trend is claimed."
        ),
        "predictive_capability": (
            "Rejected; the analysis does not establish "
            "forecasting or predictive capability."
        ),
        "generated_at": generated_at,
    }

    SUMMARY_PATH.write_text(
        json.dumps(
            summary,
            indent=2,
        ),
        encoding="utf-8",
    )

    weak_case_review = {
        "review_type": (
            "comparative_analytical_weak_case_review"
        ),
        "primary_track": (
            "Track A — Comparative"
        ),
        "data_version": DATA_VERSION,
        "status": quality_status,
        "reviewed_cases": [
            {
                "case": (
                    "Metric compatibility"
                ),
                "assessment": (
                    "Each comparison is restricted "
                    "to the same category, metric "
                    "name, and metric unit."
                ),
                "impact": (
                    "Prevents inappropriate comparison "
                    "of incompatible measurements."
                ),
            },
            {
                "case": (
                    "Comparative baseline"
                ),
                "assessment": (
                    "Each compatible metric group "
                    "uses an arithmetic-mean baseline."
                ),
                "impact": (
                    "Provides a deterministic reference "
                    "for comparative findings."
                ),
            },
            {
                "case": (
                    "Temporal interpretation"
                ),
                "assessment": (
                    "Observation timestamps remain "
                    "supporting evidence only."
                ),
                "impact": (
                    "Prevents unsupported claims of "
                    "continuous temporal trends."
                ),
            },
            {
                "case": (
                    "Predictive interpretation"
                ),
                "assessment": (
                    "No forecasting or predictive model "
                    "is produced."
                ),
                "impact": (
                    "Results remain descriptive and "
                    "comparative."
                ),
            },
        ],
        "overall_limitation": (
            "The dataset is a captured operational "
            "sample. Comparative findings are limited "
            "to compatible observed measurements and "
            "do not establish predictive capability."
        ),
    }

    WEAK_CASE_PATH.write_text(
        json.dumps(
            weak_case_review,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        "Track A intelligence results exported."
    )

    print(
        f"Results: {RESULTS_PATH}"
    )

    print(
        f"Summary: {SUMMARY_PATH}"
    )

    print(
        f"Weak-case review: {WEAK_CASE_PATH}"
    )


if __name__ == "__main__":
    main()

