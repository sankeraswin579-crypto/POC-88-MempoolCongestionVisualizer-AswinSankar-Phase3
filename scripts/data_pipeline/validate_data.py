from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
CANONICAL = DATA_DIR / "canonical" / "intelligence_data.csv"
MANIFEST = DATA_DIR / "manifest.json"
REPORT = DATA_DIR / "quality" / "validation_report.json"

MAX_DATA_MB = 10
MAX_FILE_MB = 5
MAX_ROWS = 10_000
MAX_COLS = 50

MANDATORY_COLUMNS = [
    "record_id", "record_type", "observed_at", "entity_id",
    "related_entity_id", "entity_name", "category", "subcategory",
    "status", "stage", "metric_name", "metric_value", "metric_unit",
    "text_value", "latitude", "longitude", "source_name",
    "source_record_id", "is_synthetic", "data_version",
]

errors = []

required_paths = [
    DATA_DIR / "README.md",
    MANIFEST,
    DATA_DIR / "schema.json",
    DATA_DIR / "source-sample" / "source_sample.csv",
    CANONICAL,
]

for path in required_paths:
    if not path.exists():
        errors.append(f"Missing required path: {path}")

total_bytes = sum(
    p.stat().st_size
    for p in DATA_DIR.rglob("*")
    if p.is_file()
)

if total_bytes > MAX_DATA_MB * 1024 * 1024:
    errors.append("Total /data size exceeds 10 MB")

if CANONICAL.exists():
    if CANONICAL.stat().st_size > MAX_FILE_MB * 1024 * 1024:
        errors.append("Canonical CSV exceeds 5 MB")

    df = pd.read_csv(CANONICAL)

    if len(df) > MAX_ROWS:
        errors.append("Canonical row count exceeds 10,000")

    if len(df.columns) > MAX_COLS:
        errors.append("Canonical column count exceeds 50")

    if list(df.columns) != MANDATORY_COLUMNS:
        errors.append("Canonical columns are missing or out of order")

    if df["record_id"].isna().any():
        errors.append("record_id contains null values")

    if df["record_id"].duplicated().any():
        errors.append("record_id contains duplicates")

    for required in [
        "record_type",
        "source_name",
        "is_synthetic",
        "data_version",
    ]:
        if df[required].isna().any():
            errors.append(f"{required} contains missing values")

    parsed_dates = pd.to_datetime(
        df["observed_at"],
        errors="coerce",
        utc=True
    )

    invalid_date_mask = (
        df["observed_at"].notna()
        & parsed_dates.isna()
    )

    if invalid_date_mask.any():
        errors.append("observed_at contains invalid datetime values")

    numeric_values = pd.to_numeric(
        df["metric_value"],
        errors="coerce"
    )

    invalid_numeric_mask = (
        df["metric_value"].notna()
        & numeric_values.isna()
    )

    if invalid_numeric_mask.any():
        errors.append("metric_value contains invalid numeric values")

    if (df["text_value"].fillna("").astype(str).str.len() > 500).any():
        errors.append("text_value exceeds 500 characters")

result = {
    "status": "PASS" if not errors else "FAIL",
    "errors": errors,
    "total_data_size_mb": round(
        total_bytes / 1024 / 1024,
        3
    ),
}

REPORT.parent.mkdir(parents=True, exist_ok=True)

REPORT.write_text(
    json.dumps(result, indent=2),
    encoding="utf-8"
)

if errors:
    raise SystemExit("\n".join(errors))

print("Canonical data validation passed")
