import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUT = ROOT / "data-science" / "outputs"
df = pd.read_csv(CSV)

ts = pd.to_datetime(df["observed_at"], errors="coerce", utc=True)

result = {
    "rows": int(len(df)),
    "unique_observation_timestamps": int(df["observed_at"].nunique()),
    "earliest_observed_at": str(ts.min()),
    "latest_observed_at": str(ts.max()),
    "category_distribution": df["category"].value_counts().to_dict(),
    "subcategory_distribution": df["subcategory"].value_counts().to_dict(),
    "status_distribution": df["status"].value_counts().to_dict(),
    "entity_count": int(df["entity_id"].nunique()),
    "metric_count": int(df["metric_name"].nunique()),
    "source_distribution": df["source_name"].value_counts().to_dict(),
    "synthetic_records": int(df["is_synthetic"].sum()),
    "geographic_coverage": {
        "latitude_non_null": int(df["latitude"].notna().sum()),
        "longitude_non_null": int(df["longitude"].notna().sum()),
        "latitude_missing": int(df["latitude"].isna().sum()),
        "longitude_missing": int(df["longitude"].isna().sum()),
    },
    "assessment": {
        "archetype": "time-stamped operational measurement dataset",
        "sample_scope": "captured Bitcoin mempool, fee, and recent-block measurements",
        "limitations": [
            "11 unique observation timestamps are present.",
            "All records originate from mempool.space.",
            "Latitude and longitude are not populated.",
            "The package is a captured operational sample rather than a complete representation of all possible Bitcoin network conditions."
        ]
    }
}

with open(OUT / "representativeness_assessment.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, default=str)

print("representativeness_assessment.json generated")
print("Unique timestamps:", df["observed_at"].nunique())
