"""
POC-88 Phase 3
Track A — Comparative Analytical Track

Purpose:
    Perform deterministic comparative analysis using the canonical
    Phase 3 dataset.

Primary analytical direction:
    Track A — Comparative

Method:
    - Establish a deterministic baseline for each compatible
      category + metric_name + metric_unit group.
    - Compare each observation against that baseline.
    - Keep incompatible metric names and units separate.
    - Do not treat timestamps as a continuous time series.
    - Do not perform forecasting or predictive modeling.

Canonical version:
    1.0.1
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

CANONICAL_PATH = (
    PROJECT_ROOT
    / "data"
    / "canonical"
    / "intelligence_data.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "comparative_track_raw.json"
)

EXPECTED_VERSION = "1.0.1"

REQUIRED_COLUMNS = {
    "record_id",
    "record_type",
    "observed_at",
    "entity_id",
    "entity_name",
    "category",
    "subcategory",
    "metric_name",
    "metric_value",
    "metric_unit",
    "source_name",
    "source_record_id",
    "is_synthetic",
    "data_version",
}


def format_timestamp(timestamp) -> str:
    return pd.Timestamp(timestamp).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def load_canonical() -> pd.DataFrame:
    if not CANONICAL_PATH.exists():
        raise FileNotFoundError(
            f"Canonical dataset not found: {CANONICAL_PATH}"
        )

    df = pd.read_csv(CANONICAL_PATH)

    missing_columns = REQUIRED_COLUMNS.difference(df.columns)

    if missing_columns:
        raise ValueError(
            "Missing required canonical columns: "
            f"{sorted(missing_columns)}"
        )

    versions = set(
        df["data_version"].astype(str).unique()
    )

    if versions != {EXPECTED_VERSION}:
        raise ValueError(
            "Unexpected data_version values: "
            f"{sorted(versions)}. "
            f"Expected only {EXPECTED_VERSION}."
        )

    if df["record_id"].duplicated().any():
        raise ValueError(
            "Duplicate record_id values detected."
        )

    df["observed_at"] = pd.to_datetime(
        df["observed_at"],
        utc=True,
        errors="raise",
    )

    df["metric_value"] = pd.to_numeric(
        df["metric_value"],
        errors="raise",
    )

    if df["source_name"].isna().any():
        raise ValueError(
            "Missing source_name values detected."
        )

    if not df["is_synthetic"].isin([True, False]).all():
        raise ValueError(
            "Invalid is_synthetic values detected."
        )

    return df.sort_values(
        [
            "category",
            "metric_name",
            "metric_unit",
            "observed_at",
            "record_id",
        ]
    ).reset_index(drop=True)


def build_comparative_groups(
    df: pd.DataFrame,
) -> list[dict]:

    groups = []

    grouped = df.groupby(
        [
            "category",
            "metric_name",
            "metric_unit",
        ],
        sort=True,
    )

    for (
        category,
        metric_name,
        metric_unit,
    ), group in grouped:

        values = group["metric_value"]

        baseline = float(values.mean())

        observations = []

        for _, row in group.iterrows():

            value = float(row["metric_value"])

            difference = value - baseline

            if baseline != 0:
                percent_difference = (
                    difference / abs(baseline)
                ) * 100.0
            else:
                percent_difference = None

            observations.append(
                {
                    "record_id": str(row["record_id"]),
                    "observed_at": format_timestamp(
                        row["observed_at"]
                    ),
                    "metric_value": value,
                    "metric_unit": str(metric_unit),
                    "baseline_value": baseline,
                    "difference_from_baseline": difference,
                    "percent_difference_from_baseline": (
                        percent_difference
                    ),
                }
            )

        groups.append(
            {
                "category": str(category),
                "metric_name": str(metric_name),
                "metric_unit": str(metric_unit),
                "observation_count": int(len(group)),
                "unique_timestamps": int(
                    group["observed_at"].nunique()
                ),
                "baseline_method": "arithmetic_mean",
                "baseline_value": baseline,
                "minimum": float(values.min()),
                "maximum": float(values.max()),
                "range": float(
                    values.max() - values.min()
                ),
                "observations": observations,
            }
        )

    return groups


def build_findings(
    comparative_groups: list[dict],
) -> list[dict]:

    findings = []

    for group in comparative_groups:

        baseline = group["baseline_value"]
        minimum = group["minimum"]
        maximum = group["maximum"]

        if maximum == minimum:
            finding_type = "baseline_match"
            finding = (
                f"{group['metric_name']} has a stable "
                f"observed value of {baseline} "
                f"{group['metric_unit']} across the "
                f"available compatible observations."
            )
        else:
            finding_type = "comparative_variation"
            finding = (
                f"{group['metric_name']} has a comparative "
                f"baseline of {baseline} "
                f"{group['metric_unit']}, with observed "
                f"values ranging from {minimum} to "
                f"{maximum} {group['metric_unit']}."
            )

        findings.append(
            {
                "category": group["category"],
                "metric_name": group["metric_name"],
                "metric_unit": group["metric_unit"],
                "finding_type": finding_type,
                "finding": finding,
                "baseline_value": baseline,
                "minimum": minimum,
                "maximum": maximum,
                "range": group["range"],
            }
        )

    return findings


def build_analysis(df: pd.DataFrame) -> dict:

    comparative_groups = build_comparative_groups(df)

    findings = build_findings(comparative_groups)

    category_counts = {
        str(category): int(count)
        for category, count in (
            df["category"]
            .value_counts()
            .sort_index()
            .items()
        )
    }

    compatible_group_count = len(
        comparative_groups
    )

    return {
        "analysis_type": (
            "comparative_compatible_metric_baseline"
        ),
        "primary_track": (
            "Track A — Comparative"
        ),
        "data_version": EXPECTED_VERSION,
        "dataset_path": (
            "data/canonical/intelligence_data.csv"
        ),
        "record_count": int(len(df)),
        "category_counts": category_counts,
        "compatible_metric_group_count": (
            compatible_group_count
        ),
        "comparison_rule": (
            "Comparisons are performed only within "
            "the same category, metric_name, and "
            "metric_unit."
        ),
        "baseline_rule": (
            "Baseline is the arithmetic mean of the "
            "available compatible observations for "
            "each metric group."
        ),
        "comparative_groups": comparative_groups,
        "findings": findings,
        "interpretation_scope": (
            "Deterministic comparative analysis of "
            "compatible observed measurements against "
            "their metric-specific baseline."
        ),
        "temporal_context": (
            "Observation timestamps are retained as "
            "supporting evidence only. The analysis "
            "does not interpret the captured observations "
            "as a continuous time series or establish "
            "temporal trend behavior."
        ),
        "limitations": [
            (
                "The dataset is a captured operational "
                "sample rather than a continuous "
                "historical time series."
            ),
            (
                "Comparisons are restricted to matching "
                "category, metric name, and metric unit."
            ),
            (
                "Fee, mempool, and block measurements "
                "are retained as separate metric groups."
            ),
            (
                "The arithmetic mean is used as the "
                "deterministic comparative baseline."
            ),
            (
                "The analysis does not establish "
                "forecasting or predictive capability."
            ),
            (
                "Temporal observations are supporting "
                "context and are not interpreted as "
                "validated temporal trends."
            ),
        ],
        "predictive_capability": {
            "status": "REJECTED",
            "reason": (
                "The captured dataset and analytical "
                "scope do not support forecasting or "
                "predictive modeling."
            ),
        },
    }


def main() -> None:

    print(
        "POC-88 Phase 3 — Track A Comparative Analysis"
    )
    print("-" * 60)

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Canonical input: {CANONICAL_PATH}")
    print(f"Expected version: {EXPECTED_VERSION}")

    df = load_canonical()

    print(f"Records loaded: {len(df)}")

    print(
        "Unique timestamps:",
        df["observed_at"].nunique(),
    )

    print(
        "Categories:",
        ", ".join(
            sorted(
                df["category"]
                .astype(str)
                .unique()
            )
        ),
    )

    results = build_analysis(df)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("-" * 60)
    print(
        "Comparative analytical track "
        "completed successfully."
    )
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
