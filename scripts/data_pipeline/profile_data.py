from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

CANONICAL = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUTPUT = ROOT / "data" / "quality" / "data_profile.json"

df = pd.read_csv(CANONICAL)

profile = {
    "project_id": "POC-88",
    "project_title": "Mempool Congestion Visualizer",
    "data_version": "1.0.0",
    "row_count": int(len(df)),
    "column_count": int(len(df.columns)),
    "columns": list(df.columns),
    "null_counts": {
        str(k): int(v)
        for k, v in df.isna().sum().items()
    },
    "record_types": {
        str(k): int(v)
        for k, v in df["record_type"].value_counts(dropna=False).items()
    },
    "categories": {
        str(k): int(v)
        for k, v in df["category"].value_counts(dropna=False).items()
    },
    "metric_names": {
        str(k): int(v)
        for k, v in df["metric_name"].value_counts(dropna=False).items()
    },
    "synthetic_record_count": int(df["is_synthetic"].sum()),
    "source_names": {
        str(k): int(v)
        for k, v in df["source_name"].value_counts(dropna=False).items()
    }
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

OUTPUT.write_text(
    json.dumps(profile, indent=2),
    encoding="utf-8"
)

print(f"Data profile created: {OUTPUT}")
