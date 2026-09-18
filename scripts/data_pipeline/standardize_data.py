from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "data" / "source-sample" / "source_sample.csv"
OUTPUT = ROOT / "data" / "canonical" / "intelligence_data.csv"

DATA_VERSION = "1.0.1"

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

# ---------------------------------------------------------
# Record ID
# ---------------------------------------------------------
canonical["record_id"] = [
    f"POC88-{i:05d}" for i in range(1, len(source) + 1)
]

# ---------------------------------------------------------
# Basic categorical/string fields
# ---------------------------------------------------------
canonical["record_type"] = source["record_type"].astype("string")

# ---------------------------------------------------------
# Timestamp normalization
# IMPORTANT:
# Source contains mixed ISO timestamp formats.
# format="mixed" preserves both fractional-second and
# whole-second timestamps.
# ---------------------------------------------------------
parsed_observed_at = pd.to_datetime(
    source["observed_at"],
    errors="coerce",
    utc=True,
    format="mixed",
)

canonical["observed_at"] = (
    parsed_observed_at
    .dt.strftime("%Y-%m-%dT%H:%M:%SZ")
)

canonical["entity_id"] = source["entity_id"].astype("string")

# These fields are intentionally missing for the current
# canonical mapping.
canonical["related_entity_id"] = pd.NA

canonical["entity_name"] = source["entity_name"].astype("string")
canonical["category"] = source["category"].astype("string")
canonical["subcategory"] = source["subcategory"].astype("string")
canonical["status"] = source["status"].astype("string")

# Stage is not supplied by the current source mapping.
canonical["stage"] = pd.NA

canonical["metric_name"] = source["metric_name"].astype("string")

canonical["metric_value"] = pd.to_numeric(
    source["metric_value"],
    errors="coerce"
)

canonical["metric_unit"] = source["metric_unit"].astype("string")

# ---------------------------------------------------------
# Text value
# ---------------------------------------------------------
canonical["text_value"] = (
    source["source_group"]
    .astype("string")
    .fillna("")
    .str.slice(0, 500)
)

# ---------------------------------------------------------
# Geographic fields
# Current source mapping does not provide coordinates.
# ---------------------------------------------------------
canonical["latitude"] = pd.NA
canonical["longitude"] = pd.NA

canonical["source_name"] = source["source_name"].astype("string")
canonical["source_record_id"] = source["source_record_id"].astype("string")

# ---------------------------------------------------------
# Synthetic-data flag
# ---------------------------------------------------------
canonical["is_synthetic"] = (
    source["is_synthetic"]
    .astype("boolean")
    .fillna(False)
    .astype(bool)
)

# ---------------------------------------------------------
# Data version
# ---------------------------------------------------------
canonical["data_version"] = DATA_VERSION

# ---------------------------------------------------------
# Enforce canonical column order
# ---------------------------------------------------------
canonical = canonical[MANDATORY_COLUMNS]

# ---------------------------------------------------------
# Output
# ---------------------------------------------------------
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

canonical.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8"
)

print(f"Canonical dataset generated: {OUTPUT}")
print(f"Rows: {len(canonical)}")
print(f"Columns: {len(canonical.columns)}")
print(
    f"observed_at populated: "
    f"{canonical['observed_at'].notna().sum()}"
)
print(
    f"observed_at null: "
    f"{canonical['observed_at'].isna().sum()}"
)
print(f"Data version: {DATA_VERSION}")