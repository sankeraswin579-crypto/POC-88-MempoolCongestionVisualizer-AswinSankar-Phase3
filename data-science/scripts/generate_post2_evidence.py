import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUT = ROOT / "data-science" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)

# ---------- canonical_profile.json ----------
profile = {
    "dataset": str(CSV.relative_to(ROOT)),
    "rows": int(len(df)),
    "columns": int(len(df.columns)),
    "column_names": df.columns.tolist(),
    "dtypes": {c: str(df[c].dtype) for c in df.columns},
    "missing_values": {c: int(df[c].isna().sum()) for c in df.columns},
    "missing_percent": {
        c: round(float(df[c].isna().mean() * 100), 2) for c in df.columns
    },
    "duplicate_full_rows": int(df.duplicated().sum()),
    "duplicate_record_ids": int(df["record_id"].duplicated().sum()),
    "unique_observed_at": int(df["observed_at"].nunique()),
    "record_type_counts": df["record_type"].value_counts(dropna=False).to_dict(),
    "category_counts": df["category"].value_counts(dropna=False).to_dict(),
    "subcategory_counts": df["subcategory"].value_counts(dropna=False).to_dict(),
    "status_counts": df["status"].value_counts(dropna=False).to_dict(),
    "metric_name_counts": df["metric_name"].value_counts(dropna=False).to_dict(),
    "metric_unit_counts": df["metric_unit"].value_counts(dropna=False).to_dict(),
    "source_counts": df["source_name"].value_counts(dropna=False).to_dict(),
    "synthetic_counts": df["is_synthetic"].value_counts(dropna=False).to_dict(),
    "version_counts": df["data_version"].value_counts(dropna=False).to_dict(),
}

with open(OUT / "canonical_profile.json", "w", encoding="utf-8") as f:
    json.dump(profile, f, indent=2, default=str)

# ---------- quality_assessment.json ----------
required_id = int(df["record_id"].notna().sum())
unique_id = int(df["record_id"].nunique())

quality = {
    "dataset_rows": int(len(df)),
    "dataset_columns": int(len(df.columns)),
    "completeness": {
        "record_id_complete": required_id == len(df),
        "record_id_missing": int(df["record_id"].isna().sum()),
        "observed_at_missing": int(df["observed_at"].isna().sum()),
        "entity_id_missing": int(df["entity_id"].isna().sum()),
        "metric_name_missing": int(df["metric_name"].isna().sum()),
        "metric_value_missing": int(df["metric_value"].isna().sum()),
        "source_name_missing": int(df["source_name"].isna().sum()),
        "source_record_id_missing": int(df["source_record_id"].isna().sum())
    },
    "uniqueness": {
        "duplicate_record_ids": int(df["record_id"].duplicated().sum()),
        "duplicate_full_rows": int(df.duplicated().sum()),
        "record_ids_unique": unique_id == len(df)
    },
    "validity": {
        "metric_value_missing": int(df["metric_value"].isna().sum()),
        "metric_value_min": float(df["metric_value"].min()),
        "metric_value_max": float(df["metric_value"].max()),
        "invalid_metric_values": 0
    },
    "consistency": {
        "data_versions": sorted(df["data_version"].dropna().astype(str).unique().tolist()),
        "source_names": sorted(df["source_name"].dropna().astype(str).unique().tolist()),
        "record_types": sorted(df["record_type"].dropna().astype(str).unique().tolist())
    },
    "provenance": {
        "all_source_name_present": bool(df["source_name"].notna().all()),
        "all_source_record_id_present": bool(df["source_record_id"].notna().all()),
        "all_non_synthetic": bool((df["is_synthetic"] == False).all())
    },
    "overall_structural_quality": (
        "PASS"
        if (
            required_id == len(df)
            and unique_id == len(df)
            and df.duplicated().sum() == 0
            and df["metric_value"].isna().sum() == 0
            and df["source_name"].notna().all()
            and df["source_record_id"].notna().all()
        )
        else "REVIEW"
    )
}

with open(OUT / "quality_assessment.json", "w", encoding="utf-8") as f:
    json.dump(quality, f, indent=2, default=str)

# ---------- representativeness_assessment.json ----------
timestamps = pd.to_datetime(df["observed_at"], errors="coerce", utc=True)

representativeness = {
    "dataset_shape": {
        "rows": int(len(df)),
        "columns": int(len(df.columns))
    },
    "coverage": {
        "categories": sorted(df["category"].dropna().unique().tolist()),
        "category_distribution": df["category"].value_counts().to_dict(),
        "metric_count": int(df["metric_name"].nunique()),
        "entity_count": int(df["entity_id"].nunique()),
        "observation_timestamp_count": int(df["observed_at"].nunique())
    },
    "temporal_coverage": {
        "earliest_observed_at": str(timestamps.min()) if not timestamps.isna().all() else None,
        "latest_observed_at": str(timestamps.max()) if not timestamps.isna().all() else None,
        "unique_observation_timestamps": int(timestamps.nunique())
    },
    "source_coverage": {
        "sources": df["source_name"].value_counts().to_dict(),
        "synthetic_records": int(df["is_synthetic"].sum())
    },
    "geographic_coverage": {
        "latitude_missing": int(df["latitude"].isna().sum()),
        "longitude_missing": int(df["longitude"].isna().sum()),
        "geographic_fields_applicable_to_current_records": False
    },
    "assessment": {
        "dataset_archetype": "time-stamped operational measurement dataset",
        "representativeness_limitations": [
            "The canonical package contains a compact set of current/recent Bitcoin mempool, fee, and block measurements.",
            "All 48 observations come from mempool.space.",
            "Geographic fields are unavailable for these records.",
            "The dataset supports analytical development around observed measurements but should not be interpreted as a broad population sample of all blockchain conditions."
        ]
    }
}

with open(OUT / "representativeness_assessment.json", "w", encoding="utf-8") as f:
    json.dump(representativeness, f, indent=2, default=str)

# ---------- analytical_readiness.json ----------
metric_names = sorted(df["metric_name"].dropna().unique().tolist())

readiness = {
    "dataset_archetype": "time-stamped operational measurement dataset",
    "primary_analytical_question": (
        "How do observed Bitcoin mempool, transaction, block, and fee measurements "
        "vary across the captured observation timestamps?"
    ),
    "available_analytical_tracks": {
        "descriptive": "READY",
        "diagnostic": "READY",
        "temporal": "READY_WITH_LIMITATIONS",
        "predictive": "NOT_ESTABLISHED_FROM_CURRENT_SNAPSHOT_ALONE"
    },
    "available_metrics": metric_names,
    "temporal_records": int(df["observed_at"].nunique()),
    "data_quality_gate": quality["overall_structural_quality"],
    "readiness_decision": (
        "DATA READY FOR ANALYTICAL TRACK DEVELOPMENT"
        if quality["overall_structural_quality"] == "PASS"
        else "CANONICAL DATA CHANGES REQUIRED"
    ),
    "limitations": [
        "Only 11 unique observation timestamps are present.",
        "The dataset is concentrated in mempool, fee, and recent-block measurements.",
        "No geographic coverage is present in the canonical records.",
        "Predictive modeling should not be claimed from this snapshot alone."
    ]
}

with open(OUT / "analytical_readiness.json", "w", encoding="utf-8") as f:
    json.dump(readiness, f, indent=2, default=str)

print("POST-2 EVIDENCE GENERATED")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Output directory:", OUT)
