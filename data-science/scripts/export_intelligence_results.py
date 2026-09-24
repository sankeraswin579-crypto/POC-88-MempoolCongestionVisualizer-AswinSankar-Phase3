from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "temporal_track_raw.json"
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
    return (
        datetime.now(timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    )


def main() -> None:
    print(
        "Exporting standardized intelligence results..."
    )

    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Raw analytical output not found: {RAW_PATH}"
        )

    if not VALIDATION_PATH.exists():
        raise FileNotFoundError(
            f"Validation output not found: {VALIDATION_PATH}"
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

    # ---------------------------------------------------------------
    # Intelligence results
    # ---------------------------------------------------------------

    intelligence_results = []

    result_counter = 1

    for metric in raw.get(
        "metric_summary",
        []
    ):
        result = {
            "result_id": (
                f"POC88-TEMP-{result_counter:04d}"
            ),
            "result_type": (
                "temporal_metric_summary"
            ),
            "metric_name": metric[
                "metric_name"
            ],
            "result_value": metric[
                "mean"
            ],
            "result_unit": metric[
                "metric_unit"
            ],
            "category": metric[
                "category"
            ],
            "finding": (
                f"{metric['metric_name']} "
                f"was observed across "
                f"{metric['unique_timestamps']} "
                f"timestamps with a range of "
                f"{metric['range']} "
                f"{metric['metric_unit']}."
            ),
            "evidence": {
                "observations": metric[
                    "observations"
                ],
                "minimum": metric[
                    "minimum"
                ],
                "maximum": metric[
                    "maximum"
                ],
                "first_observed_at": metric[
                    "first_observed_at"
                ],
                "last_observed_at": metric[
                    "last_observed_at"
                ],
            },
            "method_version": "temporal-track-v1.0",
            "data_version": DATA_VERSION,
            "generated_at": generated_at,
            "quality_status": quality_status,
            "limitation": (
                "Observed temporal variation in a "
                "limited captured sample; not a "
                "forecast or prediction."
            ),
        }

        intelligence_results.append(
            result
        )

        result_counter += 1

    RESULTS_PATH.write_text(
        json.dumps(
            {
                "results": intelligence_results
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # ---------------------------------------------------------------
    # Intelligence summary
    # ---------------------------------------------------------------

    summary = {
        "summary_type": (
            "temporal_analytical_track_summary"
        ),
        "data_version": DATA_VERSION,
        "analysis_type": raw.get(
            "analysis_type"
        ),
        "record_count": raw.get(
            "record_count"
        ),
        "unique_observed_timestamps": raw.get(
            "unique_observed_timestamps",
            raw.get(
                "timestamp_coverage",
                {}
            ).get(
                "unique_timestamps"
            ),
        ),
        "metric_group_count": len(
            raw.get(
                "metric_summary",
                []
            )
        ),
        "validation_status": quality_status,
        "interpretation": (
            "The analytical track describes "
            "observed variation across captured "
            "timestamps. It does not establish "
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

    # ---------------------------------------------------------------
    # Weak case / limitation review
    # ---------------------------------------------------------------

    weak_case_review = {
        "review_type": (
            "temporal_analytical_weak_case_review"
        ),
        "data_version": DATA_VERSION,
        "status": quality_status,
        "reviewed_cases": [
            {
                "case": (
                    "Limited timestamp coverage"
                ),
                "assessment": (
                    "The dataset contains 11 "
                    "unique observation timestamps."
                ),
                "impact": (
                    "Limits interpretation as a "
                    "continuous historical time series."
                ),
            },
            {
                "case": (
                    "Metric compatibility"
                ),
                "assessment": (
                    "Metrics are summarized by "
                    "category, metric name, and unit."
                ),
                "impact": (
                    "Prevents inappropriate comparison "
                    "between incompatible measurements."
                ),
            },
            {
                "case": (
                    "Predictive interpretation"
                ),
                "assessment": (
                    "No forecasting model is produced."
                ),
                "impact": (
                    "Results must be interpreted as "
                    "observed temporal variation only."
                ),
            },
        ],
        "overall_limitation": (
            "The dataset is a captured operational "
            "sample and does not establish "
            "predictive capability."
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
        "Intelligence results exported successfully."
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