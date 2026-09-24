from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "temporal_track_raw.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "validation_metrics.json"
)

EXPECTED_VERSION = "1.0.1"


def main() -> None:
    print("Validating temporal analytical track...")

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Analytical output not found: {INPUT_PATH}"
        )

    data = json.loads(
        INPUT_PATH.read_text(
            encoding="utf-8"
        )
    )

    errors = []

    if data.get("data_version") != EXPECTED_VERSION:
        errors.append(
            "Unexpected data_version."
        )

    if data.get("record_count") != 48:
        errors.append(
            f"Expected 48 records, found "
            f"{data.get('record_count')}."
        )

    coverage = data.get(
        "timestamp_coverage",
        {}
    )

    if coverage.get("unique_timestamps") != 11:
        errors.append(
            "Expected 11 unique observation timestamps."
        )

    if not data.get("timestamp_summary"):
        errors.append(
            "timestamp_summary is empty."
        )

    if not data.get("metric_summary"):
        errors.append(
            "metric_summary is empty."
        )

    for item in data.get(
        "metric_summary",
        []
    ):
        if item["observations"] <= 0:
            errors.append(
                f"Metric {item.get('metric_name')} "
                "has no observations."
            )

        if item["minimum"] > item["maximum"]:
            errors.append(
                f"Metric {item.get('metric_name')} "
                "has invalid min/max values."
            )

    status = (
        "PASS"
        if not errors
        else "FAIL"
    )

    validation = {
        "validation_type": (
            "temporal_analytical_track_validation"
        ),
        "data_version": EXPECTED_VERSION,
        "input": (
            "data-science/outputs/"
            "temporal_track_raw.json"
        ),
        "status": status,
        "record_count": data.get(
            "record_count"
        ),
        "unique_timestamps": coverage.get(
            "unique_timestamps"
        ),
        "metric_groups": len(
            data.get(
                "metric_summary",
                []
            )
        ),
        "errors": errors,
        "checks": {
            "canonical_version": (
                data.get("data_version")
                == EXPECTED_VERSION
            ),
            "expected_record_count": (
                data.get("record_count")
                == 48
            ),
            "expected_timestamp_count": (
                coverage.get(
                    "unique_timestamps"
                )
                == 11
            ),
            "timestamp_summary_present": bool(
                data.get("timestamp_summary")
            ),
            "metric_summary_present": bool(
                data.get("metric_summary")
            ),
            "metric_ranges_valid": not any(
                item["minimum"]
                > item["maximum"]
                for item in data.get(
                    "metric_summary",
                    []
                )
            ),
        },
    }

    OUTPUT_PATH.write_text(
        json.dumps(
            validation,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Validation status: {status}"
    )
    print(
        f"Output: {OUTPUT_PATH}"
    )

    if errors:
        raise SystemExit(
            "Analytical validation failed."
        )


if __name__ == "__main__":
    main()