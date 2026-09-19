import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUT = ROOT / "data-science" / "outputs"
df = pd.read_csv(CSV)

checks = {
    "record_id_complete": bool(df["record_id"].notna().all()),
    "record_ids_unique": bool(df["record_id"].is_unique),
    "duplicate_full_rows_zero": bool(df.duplicated().sum() == 0),
    "observed_at_complete": bool(df["observed_at"].notna().all()),
    "entity_id_complete": bool(df["entity_id"].notna().all()),
    "metric_name_complete": bool(df["metric_name"].notna().all()),
    "metric_value_complete": bool(df["metric_value"].notna().all()),
    "metric_unit_complete": bool(df["metric_unit"].notna().all()),
    "source_name_complete": bool(df["source_name"].notna().all()),
    "source_record_id_complete": bool(df["source_record_id"].notna().all()),
    "data_version_complete": bool(df["data_version"].notna().all()),
}

quality = {
    "rows": int(len(df)),
    "columns": int(len(df.columns)),
    "completeness": {
        "missing_by_column": {c: int(df[c].isna().sum()) for c in df.columns}
    },
    "uniqueness": {
        "duplicate_record_ids": int(df["record_id"].duplicated().sum()),
        "duplicate_full_rows": int(df.duplicated().sum()),
    },
    "validity": {
        "metric_value_missing": int(df["metric_value"].isna().sum()),
        "metric_value_min": float(df["metric_value"].min()),
        "metric_value_max": float(df["metric_value"].max()),
    },
    "consistency": {
        "record_types": df["record_type"].value_counts().to_dict(),
        "data_versions": df["data_version"].value_counts().to_dict(),
        "source_names": df["source_name"].value_counts().to_dict(),
    },
    "provenance": {
        "source_name_complete": bool(df["source_name"].notna().all()),
        "source_record_id_complete": bool(df["source_record_id"].notna().all()),
        "synthetic_records": int(df["is_synthetic"].sum()),
    },
    "checks": checks,
    "overall_status": "PASS" if all(checks.values()) else "REVIEW",
}

with open(OUT / "quality_assessment.json", "w", encoding="utf-8") as f:
    json.dump(quality, f, indent=2, default=str)

print("quality_assessment.json generated")
print("Overall status:", quality["overall_status"])
