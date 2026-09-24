"""
POC-88 Phase 3
Temporal Analytical Track

Canonical dataset:
    data/canonical/intelligence_data.csv

Canonical version:
    1.0.1

Purpose:
    Analyze observed variation in Bitcoin mempool, fee, and block
    measurements across the captured observation timestamps.

Scope:
    - Uses only the canonical dataset.
    - Performs deterministic temporal comparison.
    - Does not perform forecasting.
    - Does not perform predictive modeling.
    - Does not introduce an alternate dataset.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

# temporal_track.py
#     -> track-specific
#     -> scripts
#     -> data-science
#     -> PROJECT ROOT
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
    / "temporal_track_raw.json"
)

EXPECTED_VERSION = "1.0.1"


# ---------------------------------------------------------------------------
# Required canonical columns
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Timestamp formatting helper
# ---------------------------------------------------------------------------

def format_timestamp(timestamp) -> str:
    """
    Convert a timestamp to canonical UTC ISO-8601 format.

    Example:
        2026-09-17T09:15:22Z
    """

    return pd.Timestamp(timestamp).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


# ---------------------------------------------------------------------------
# Load and validate canonical data
# ---------------------------------------------------------------------------

def load_canonical() -> pd.DataFrame:
    """Load and validate the canonical dataset."""

    if not CANONICAL_PATH.exists():
        raise FileNotFoundError(
            f"Canonical dataset not found: {CANONICAL_PATH}"
        )

    df = pd.read_csv(CANONICAL_PATH)

    # Validate required columns
    missing_columns = REQUIRED_COLUMNS.difference(
        df.columns
    )

    if missing_columns:
        raise ValueError(
            "Missing required canonical columns: "
            f"{sorted(missing_columns)}"
        )

    # Validate canonical version
    versions = set(
        df["data_version"]
        .astype(str)
        .unique()
    )

    if versions != {EXPECTED_VERSION}:
        raise ValueError(
            "Unexpected data_version values: "
            f"{sorted(versions)}. "
            f"Expected only {EXPECTED_VERSION}."
        )

    # Validate record IDs
    if df["record_id"].duplicated().any():
        raise ValueError(
            "Duplicate record_id values detected."
        )

    # Parse observation timestamps
    df["observed_at"] = pd.to_datetime(
        df["observed_at"],
        utc=True,
        errors="raise",
    )

    # Validate metric values
    df["metric_value"] = pd.to_numeric(
        df["metric_value"],
        errors="raise",
    )

    # Validate source provenance
    if df["source_name"].isna().any():
        raise ValueError(
            "Missing source_name values detected."
        )

    # Validate synthetic flag
    if not df["is_synthetic"].isin(
        [True, False]
    ).all():
        raise ValueError(
            "Invalid is_synthetic values detected."
        )

    # Deterministic ordering
    df = df.sort_values(
        [
            "observed_at",
            "category",
            "metric_name",
            "record_id",
        ]
    ).reset_index(drop=True)

    return df


# ---------------------------------------------------------------------------
# Timestamp summary
# ---------------------------------------------------------------------------

def build_timestamp_summary(
    df: pd.DataFrame,
) -> list[dict]:
    """
    Build a deterministic summary for every observed timestamp.
    """

    timestamp_summary = []

    for timestamp, group in df.groupby(
        "observed_at",
        sort=True,
    ):
        timestamp_text = format_timestamp(timestamp)

        metrics = []

        for _, row in group.iterrows():
            metrics.append(
                {
                    "record_id": str(
                        row["record_id"]
                    ),
                    "category": str(
                        row["category"]
                    ),
                    "metric_name": str(
                        row["metric_name"]
                    ),
                    "metric_value": float(
                        row["metric_value"]
                    ),
                    "metric_unit": str(
                        row["metric_unit"]
                    ),
                }
            )

        timestamp_summary.append(
            {
                "observed_at": timestamp_text,
                "record_count": int(
                    len(group)
                ),
                "category_counts": {
                    str(category): int(count)
                    for category, count
                    in (
                        group["category"]
                        .value_counts()
                        .sort_index()
                        .items()
                    )
                },
                "metrics": metrics,
            }
        )

    return timestamp_summary


# ---------------------------------------------------------------------------
# Metric-level temporal summary
# ---------------------------------------------------------------------------

def build_metric_summary(
    df: pd.DataFrame,
) -> list[dict]:
    """
    Summarize each compatible metric independently.

    Metrics are grouped by:
        category
        metric_name
        metric_unit

    This prevents incompatible units from being
    directly compared.
    """

    summaries = []

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

        first_time = group[
            "observed_at"
        ].min()

        last_time = group[
            "observed_at"
        ].max()

        summaries.append(
            {
                "category": str(category),
                "metric_name": str(metric_name),
                "metric_unit": str(metric_unit),
                "observations": int(
                    len(group)
                ),
                "unique_timestamps": int(
                    group[
                        "observed_at"
                    ].nunique()
                ),
                "first_observed_at": (
                    format_timestamp(
                        first_time
                    )
                ),
                "last_observed_at": (
                    format_timestamp(
                        last_time
                    )
                ),
                "minimum": float(
                    values.min()
                ),
                "maximum": float(
                    values.max()
                ),
                "mean": float(
                    values.mean()
                ),
                "range": float(
                    values.max()
                    - values.min()
                ),
            }
        )

    return summaries


# ---------------------------------------------------------------------------
# Timestamp coverage
# ---------------------------------------------------------------------------

def build_timestamp_coverage(
    df: pd.DataFrame,
) -> dict:
    """
    Describe timestamp coverage.

    This does not treat the dataset as a continuous
    historical time series.
    """

    timestamps = sorted(
        format_timestamp(timestamp)
        for timestamp
        in df["observed_at"].unique()
    )

    if not timestamps:
        raise ValueError(
            "No observation timestamps found."
        )

    return {
        "unique_timestamps": len(
            timestamps
        ),
        "first_timestamp": timestamps[0],
        "last_timestamp": timestamps[-1],
        "timestamps": timestamps,
        "coverage_interpretation": (
            "Captured observation timestamps "
            "with limited temporal coverage; "
            "not a continuous historical time series."
        ),
    }


# ---------------------------------------------------------------------------
# Main analytical output
# ---------------------------------------------------------------------------

def build_temporal_analysis(
    df: pd.DataFrame,
) -> dict:
    """
    Build the complete deterministic temporal analysis.
    """

    timestamp_summary = (
        build_timestamp_summary(df)
    )

    metric_summary = (
        build_metric_summary(df)
    )

    timestamp_coverage = (
        build_timestamp_coverage(df)
    )

    category_counts = {
        str(category): int(count)
        for category, count
        in (
            df["category"]
            .value_counts()
            .sort_index()
            .items()
        )
    }

    return {
        "analysis_type": (
            "temporal_observed_measurement_comparison"
        ),

        "data_version": EXPECTED_VERSION,

        "dataset_path": (
            "data/canonical/"
            "intelligence_data.csv"
        ),

        "record_count": int(
            len(df)
        ),

        "category_counts": category_counts,

        "timestamp_coverage": (
            timestamp_coverage
        ),

        "timestamp_summary": (
            timestamp_summary
        ),

        "metric_summary": (
            metric_summary
        ),

        "interpretation_scope": (
            "Observed measurement variation "
            "across captured timestamps. "
            "Results do not establish forecasting "
            "or predictive capability."
        ),

        "limitations": [
            (
                "Only 11 unique observation "
                "timestamps are available."
            ),
            (
                "The dataset is a captured "
                "operational sample rather than "
                "a continuous historical time series."
            ),
            (
                "All records originate from "
                "mempool.space."
            ),
            (
                "Latitude and longitude are "
                "not populated."
            ),
            (
                "Different metric names and units "
                "are not treated as directly "
                "comparable measurements."
            ),
            (
                "The analysis does not establish "
                "predictive or forecasting capability."
            ),
        ],
    }


# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------

def write_output(
    results: dict,
) -> None:
    """Write the analytical results to JSON."""

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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print(
        "POC-88 Phase 3 — "
        "Temporal Analytical Track"
    )

    print("-" * 60)

    print(
        f"Project root: {PROJECT_ROOT}"
    )

    print(
        f"Canonical input: {CANONICAL_PATH}"
    )

    print(
        f"Expected version: {EXPECTED_VERSION}"
    )

    print("-" * 60)

    # Load and validate
    df = load_canonical()

    print(
        f"Records loaded: {len(df)}"
    )

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

    print(
        "Data version:",
        ", ".join(
            sorted(
                df["data_version"]
                .astype(str)
                .unique()
            )
        ),
    )

    # Build analysis
    results = build_temporal_analysis(
        df
    )

    # Write results
    write_output(results)

    print("-" * 60)

    print(
        "Temporal analytical track "
        "completed successfully."
    )

    print(
        f"Output: {OUTPUT_PATH}"
    )


# ---------------------------------------------------------------------------
# Script entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
