from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "comparative_track_raw.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "validation_metrics.json"
)

EXPECTED_VERSION = "1.0.1"


def main() -> None:

    print(
        "Validating Track A — Comparative analytical track..."
    )

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Comparative output not found: {INPUT_PATH}"
        )

    data = json.loads(
        INPUT_PATH.read_text(
            encoding="utf-8"
        )
    )

    errors = []

    if data.get("primary_track") != (
        "Track A — Comparative"
    ):
        errors.append(
            "Primary analytical track is not "
            "Track A — Comparative."
        )

    if data.get("data_version") != EXPECTED_VERSION:
        errors.append(
            "Unexpected data_version."
        )

    if data.get("record_count") != 48:
        errors.append(
            f"Expected 48 records, found "
            f"{data.get('record_count')}."
        )

    groups = data.get(
        "comparative_groups",
        []
    )

    findings = data.get(
        "findings",
        []
    )

    if not groups:
        errors.append(
            "comparative_groups is empty."
        )

    if not findings:
        errors.append(
            "findings is empty."
        )

    if len(groups) != len(findings):
        errors.append(
            "Finding count does not match "
            "comparative group count."
        )

    baseline_valid = True
    compatibility_valid = True
    observations_valid = True

    for group in groups:

        metric_name = group.get(
            "metric_name"
        )

        metric_unit = group.get(
            "metric_unit"
        )

        observations = group.get(
            "observations",
            []
        )

        baseline = group.get(
            "baseline_value"
        )

        minimum = group.get(
            "minimum"
        )

        maximum = group.get(
            "maximum"
        )

        if not observations:
            observations_valid = False
            errors.append(
                f"{metric_name} has no observations."
            )

        if baseline is None:
            baseline_valid = False
            errors.append(
                f"{metric_name} has no baseline."
            )

        if minimum is None or maximum is None:
            baseline_valid = False
            errors.append(
                f"{metric_name} has incomplete "
                "range information."
            )

        if (
            minimum is not None
            and maximum is not None
            and minimum > maximum
        ):
            baseline_valid = False
            errors.append(
                f"{metric_name} has invalid "
                "minimum/maximum values."
            )

        for observation in observations:

            if observation.get(
                "metric_unit"
            ) != metric_unit:
                compatibility_valid = False
                errors.append(
                    f"{metric_name} contains an "
                    "incompatible metric unit."
                )

            if observation.get(
                "baseline_value"
            ) != baseline:
                baseline_valid = False
                errors.append(
                    f"{metric_name} observation "
                    "does not use the group baseline."
                )

            if observation.get(
                "metric_value"
            ) is None:
                observations_valid = False
                errors.append(
                    f"{metric_name} contains "
                    "a missing metric value."
                )

    validation = {
        "validation_type": (
            "comparative_analytical_track_validation"
        ),
        "primary_track": (
            "Track A — Comparative"
        ),
        "data_version": EXPECTED_VERSION,
        "input": (
            "data-science/outputs/"
            "comparative_track_raw.json"
        ),
        "status": (
            "PASS"
            if not errors
            else "FAIL"
        ),
        "record_count": data.get(
            "record_count"
        ),
        "comparative_group_count": len(groups),
        "finding_count": len(findings),
        "errors": errors,
        "checks": {
            "primary_track_is_comparative": (
                data.get("primary_track")
                == "Track A — Comparative"
            ),
            "canonical_version": (
                data.get("data_version")
                == EXPECTED_VERSION
            ),
            "expected_record_count": (
                data.get("record_count")
                == 48
            ),
            "comparative_groups_present": bool(
                groups
            ),
            "findings_present": bool(
                findings
            ),
            "finding_group_alignment": (
                len(groups)
                == len(findings)
            ),
            "baseline_values_valid": (
                baseline_valid
            ),
            "metric_unit_compatibility": (
                compatibility_valid
            ),
            "observations_valid": (
                observations_valid
            ),
            "predictive_capability_rejected": (
                data.get(
                    "predictive_capability",
                    {}
                ).get("status")
                == "REJECTED"
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
        f"Validation status: "
        f"{validation['status']}"
    )

    print(
        f"Comparative groups: {len(groups)}"
    )

    print(
        f"Findings: {len(findings)}"
    )

    print(
        f"Output: {OUTPUT_PATH}"
    )

    if errors:
        raise SystemExit(
            "Comparative analytical validation failed."
        )


if __name__ == "__main__":
    main()
