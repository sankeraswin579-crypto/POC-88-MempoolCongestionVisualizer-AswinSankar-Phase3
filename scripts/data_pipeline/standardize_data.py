from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "data" / "source-sample" / "source_sample.csv"
OUTPUT = ROOT / "data" / "canonical" / "intelligence_data.csv"

DATA_VERSION = "1.0.0"

MANDATORY_COLUMNS = [
    "record_id",
    "record_type",
    "observed_at",
    "entity_id",
    "related_entity_id",
    "entity_name",
    "category",
    "subcategory",
    "status",
    "stage",
    "metric_name",
    "metric_value",
    "metric_unit",
    "text_value",
    "latitude",
    "longitude",
    "source_name",
    "source_record_id",
    "is_synthetic",
    "data_version",
]

source = pd.read_csv(INPUT)

canonical = pd.DataFrame()

canonical["record_id"] = [
    f"POC88-{i:05d}" for i in range(1, len(source) + 1)
]

canonical["record_type"] = source["record_type"].astype("string")
canonical["observed_at"] = pd.to_datetime(
    source["observed_at"],
    errors="coerce",
    utc=True
).dt.strftime("%Y-%m-%dT%H:%M:%SZ")

canonical["entity_id"] = source["entity_id"].astype("string")
canonical["related_entity_id"] = pd.NA
canonical["entity_name"] = source["entity_name"].astype("string")
canonical["category"] = source["category"].astype("string")
canonical["subcategory"] = source["subcategory"].astype("string")
canonical["status"] = source["status"].astype("string")
canonical["stage"] = pd.NA
canonical["metric_name"] = source["metric_name"].astype("string")
canonical["metric_value"] = pd.to_numeric(
    source["metric_value"],
    errors="coerce"
)
canonical["metric_unit"] = source["metric_unit"].astype("string")
canonical["text_value"] = (
    source["source_group"]
    .astype("string")
    .fillna("")
    .str.slice(0, 500)
)
canonical["latitude"] = pd.NA
canonical["longitude"] = pd.NA
canonical["source_name"] = source["source_name"].astype("string")
canonical["source_record_id"] = source["source_record_id"].astype("string")
canonical["is_synthetic"] = (
    source["is_synthetic"]
    .astype("boolean")
    .fillna(False)
    .astype(bool)
)
canonical["data_version"] = DATA_VERSION

canonical = canonical[MANDATORY_COLUMNS]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

canonical.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8"
)

print(f"Canonical dataset generated: {OUTPUT}")
print(f"Rows: {len(canonical)}")
print(f"Columns: {len(canonical.columns)}")
