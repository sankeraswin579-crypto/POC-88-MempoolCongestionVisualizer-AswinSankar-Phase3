import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUT = ROOT / "data-science" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CSV)

profile = {
    "dataset_path": str(CSV.relative_to(ROOT)),
    "rows": int(len(df)),
    "columns": int(len(df.columns)),
    "column_names": df.columns.tolist(),
    "dtypes": {c: str(df[c].dtype) for c in df.columns},
    "missing_values": {c: int(df[c].isna().sum()) for c in df.columns},
    "duplicate_full_rows": int(df.duplicated().sum()),
    "duplicate_record_ids": int(df["record_id"].duplicated().sum()),
    "unique_record_ids": int(df["record_id"].nunique()),
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

print("canonical_profile.json generated")
print("Rows:", len(df))
print("Columns:", len(df.columns))
