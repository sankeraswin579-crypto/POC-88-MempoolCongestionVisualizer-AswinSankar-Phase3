
from pathlib import Path
import json
import math
import pandas as pd


# ============================================================
# ROOT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"

CANONICAL = DATA_DIR / "canonical" / "intelligence_data.csv"
PUBLISHED = DATA_DIR / "published" / "intelligence_data.json"
MANIFEST = DATA_DIR / "manifest.json"
SOURCE_SAMPLE = DATA_DIR / "source-sample" / "source_sample.csv"

PROFILE = DATA_DIR / "quality" / "data_profile.json"
REPORT = DATA_DIR / "quality" / "validation_report.json"

SAMPLING_REPORT = ROOT / "docs" / "SAMPLING_AND_REDUCTION_REPORT.md"
REQUIREMENTS_DATA = ROOT / "requirements-data.txt"


# ============================================================
# LIMITS
# ============================================================

MAX_DATA_MB = 10
MAX_FILE_MB = 5
MAX_ROWS = 10_000
MAX_COLS = 50

EXPECTED_DATA_VERSION = "1.0.1"
EXPECTED_CANONICAL_ROWS = 48
EXPECTED_CANONICAL_COLS = 20


# ============================================================
# MANDATORY CANONICAL COLUMNS
# ============================================================

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


errors = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_error(message):
    errors.append(message)


def reject_json_constant(value):
    """
    Reject non-standard JSON constants such as:
    NaN
    Infinity
    -Infinity
    """
    raise ValueError(f"Invalid JSON constant: {value}")


def load_strict_json(path):
    """
    Load JSON while explicitly rejecting NaN / Infinity.
    """
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=reject_json_constant,
        )
    except Exception as exc:
        add_error(f"Invalid strict JSON in {path}: {exc}")
        return None


# ============================================================
# REQUIRED PATHS
# ============================================================

required_paths = [
    DATA_DIR / "README.md",
    MANIFEST,
    DATA_DIR / "schema.json",
    SOURCE_SAMPLE,
    CANONICAL,
    PUBLISHED,
    PROFILE,
    SAMPLING_REPORT,
    REQUIREMENTS_DATA,
]

for path in required_paths:
    if not path.exists():
        add_error(f"Missing required path: {path}")


# ============================================================
# DATA SIZE VALIDATION
# ============================================================

total_bytes = sum(
    p.stat().st_size
    for p in DATA_DIR.rglob("*")
    if p.is_file()
)

if total_bytes > MAX_DATA_MB * 1024 * 1024:
    add_error("Total /data size exceeds 10 MB")


if CANONICAL.exists():
    if CANONICAL.stat().st_size > MAX_FILE_MB * 1024 * 1024:
        add_error("Canonical CSV exceeds 5 MB")


# ============================================================
# LOAD CANONICAL DATA
# ============================================================

df = None

if CANONICAL.exists():

    try:
        df = pd.read_csv(CANONICAL)
    except Exception as exc:
        add_error(f"Unable to read canonical CSV: {exc}")


# ============================================================
# CANONICAL STRUCTURE VALIDATION
# ============================================================

if df is not None:

    if len(df) > MAX_ROWS:
        add_error("Canonical row count exceeds 10,000")

    if len(df.columns) > MAX_COLS:
        add_error("Canonical column count exceeds 50")

    if len(df) != EXPECTED_CANONICAL_ROWS:
        add_error(
            f"Canonical row count mismatch: "
            f"expected {EXPECTED_CANONICAL_ROWS}, got {len(df)}"
        )

    if len(df.columns) != EXPECTED_CANONICAL_COLS:
        add_error(
            f"Canonical column count mismatch: "
            f"expected {EXPECTED_CANONICAL_COLS}, got {len(df.columns)}"
        )

    if list(df.columns) != MANDATORY_COLUMNS:
        add_error("Canonical columns are missing or out of order")


# ============================================================
# RECORD ID VALIDATION
# ============================================================

if df is not None:

    if df["record_id"].isna().any():
        add_error("record_id contains null values")

    if df["record_id"].duplicated().any():
        add_error("record_id contains duplicates")


# ============================================================
# REQUIRED FIELD VALIDATION
# ============================================================

if df is not None:

    for required in [
        "record_type",
        "source_name",
        "is_synthetic",
        "data_version",
    ]:
        if df[required].isna().any():
            add_error(
                f"{required} contains missing values"
            )


# ============================================================
# DATA VERSION VALIDATION
# ============================================================

if df is not None:

    versions = (
        df["data_version"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if versions != [EXPECTED_DATA_VERSION]:
        add_error(
            "Canonical data_version mismatch: "
            f"expected only {EXPECTED_DATA_VERSION}, got {versions}"
        )


# ============================================================
# OBSERVED_AT VALIDATION
# ============================================================

canonical_timestamp_count = 0

if df is not None:

    canonical_timestamp_count = int(
        df["observed_at"].notna().sum()
    )

    if canonical_timestamp_count != len(df):
        add_error(
            "observed_at contains null values: "
            f"{len(df) - canonical_timestamp_count}"
        )

    parsed_dates = pd.to_datetime(
        df["observed_at"],
        errors="coerce",
        utc=True,
        format="mixed",
    )

    invalid_date_mask = (
        df["observed_at"].notna()
        & parsed_dates.isna()
    )

    if invalid_date_mask.any():
        add_error(
            "observed_at contains invalid datetime values"
        )


# ============================================================
# SOURCE TIMESTAMP COVERAGE
# ============================================================

source_timestamp_count = 0

if SOURCE_SAMPLE.exists():

    try:
        source_df = pd.read_csv(SOURCE_SAMPLE)

        if "observed_at" not in source_df.columns:
            add_error(
                "source_sample.csv does not contain observed_at"
            )
        else:
            source_timestamp_count = int(
                source_df["observed_at"].notna().sum()
            )

            if (
                df is not None
                and source_timestamp_count
                != canonical_timestamp_count
            ):
                add_error(
                    "Timestamp coverage changed during "
                    "canonical standardization: "
                    f"source={source_timestamp_count}, "
                    f"canonical={canonical_timestamp_count}"
                )

    except Exception as exc:
        add_error(
            f"Unable to read source_sample.csv: {exc}"
        )


# ============================================================
# METRIC VALUE VALIDATION
# ============================================================

if df is not None:

    numeric_values = pd.to_numeric(
        df["metric_value"],
        errors="coerce",
    )

    invalid_numeric_mask = (
        df["metric_value"].notna()
        & numeric_values.isna()
    )

    if invalid_numeric_mask.any():
        add_error(
            "metric_value contains invalid numeric values"
        )


# ============================================================
# TEXT VALUE VALIDATION
# ============================================================

if df is not None:

    if (
        df["text_value"]
        .fillna("")
        .astype(str)
        .str.len()
        .gt(500)
        .any()
    ):
        add_error(
            "text_value exceeds 500 characters"
        )


# ============================================================
# MANIFEST VALIDATION
# ============================================================

manifest = None

if MANIFEST.exists():

    manifest = load_strict_json(MANIFEST)

    if isinstance(manifest, dict):

        manifest_version = str(
            manifest.get("data_version", "")
        )

        if manifest_version != EXPECTED_DATA_VERSION:
            add_error(
                "Manifest data_version mismatch: "
                f"expected {EXPECTED_DATA_VERSION}, "
                f"got {manifest_version}"
            )

        manifest_rows = manifest.get(
            "canonical_record_count"
        )

        if df is not None and manifest_rows != len(df):
            add_error(
                "Manifest canonical_record_count mismatch: "
                f"manifest={manifest_rows}, "
                f"canonical={len(df)}"
            )

        manifest_cols = manifest.get(
            "canonical_column_count"
        )

        if df is not None and manifest_cols != len(df.columns):
            add_error(
                "Manifest canonical_column_count mismatch: "
                f"manifest={manifest_cols}, "
                f"canonical={len(df.columns)}"
            )

        original_count = manifest.get(
            "original_record_count"
        )

        sample_count = manifest.get(
            "sample_record_count"
        )

        if original_count != EXPECTED_CANONICAL_ROWS:
            add_error(
                "Manifest original_record_count mismatch: "
                f"expected {EXPECTED_CANONICAL_ROWS}, "
                f"got {original_count}"
            )

        if sample_count != EXPECTED_CANONICAL_ROWS:
            add_error(
                "Manifest sample_record_count mismatch: "
                f"expected {EXPECTED_CANONICAL_ROWS}, "
                f"got {sample_count}"
            )

        is_sampled = manifest.get("is_sampled")

        if is_sampled is not False:
            add_error(
                "Manifest is_sampled must be false "
                "because the full 48-row snapshot is retained"
            )

        canonical_path = str(
            manifest.get("canonical_path", "")
        )

        published_path = str(
            manifest.get("published_path", "")
        )

        if canonical_path:
            expected_canonical_path = (
                "data/canonical/intelligence_data.csv"
            )

            if canonical_path.replace("\\", "/") != expected_canonical_path:
                add_error(
                    "Manifest canonical_path does not match "
                    "the canonical artifact"
                )

        if published_path:
            expected_published_path = (
                "data/published/intelligence_data.json"
            )

            if published_path.replace("\\", "/") != expected_published_path:
                add_error(
                    "Manifest published_path does not match "
                    "the published artifact"
                )

        synthetic_flag = manifest.get("is_synthetic")

        if synthetic_flag is not None:

            if df is not None:

                canonical_synthetic_values = (
                    df["is_synthetic"]
                    .dropna()
                    .astype(str)
                    .str.lower()
                    .unique()
                    .tolist()
                )

                if (
                    str(synthetic_flag).lower()
                    not in canonical_synthetic_values
                ):
                    add_error(
                        "Manifest is_synthetic value is "
                        "inconsistent with canonical data"
                    )


# ============================================================
# PUBLISHED JSON VALIDATION
# ============================================================

published = None

if PUBLISHED.exists():

    published = load_strict_json(PUBLISHED)

    if published is not None:

        if not isinstance(published, list):
            add_error(
                "Published JSON must contain a list of records"
            )

        elif df is not None:

            if len(published) != len(df):
                add_error(
                    "Published JSON record count does not "
                    "match canonical CSV: "
                    f"published={len(published)}, "
                    f"canonical={len(df)}"
                )

            else:

                # ------------------------------------------------
                # Record ID consistency
                # ------------------------------------------------

                published_ids = [
                    record.get("record_id")
                    for record in published
                    if isinstance(record, dict)
                ]

                canonical_ids = (
                    df["record_id"]
                    .astype(str)
                    .tolist()
                )

                published_ids = [
                    str(record_id)
                    for record_id in published_ids
                ]

                if published_ids != canonical_ids:
                    add_error(
                        "Published JSON record_id order/content "
                        "does not match canonical CSV"
                    )

                # ------------------------------------------------
                # Data version consistency
                # ------------------------------------------------

                published_versions = {
                    str(record.get("data_version"))
                    for record in published
                    if isinstance(record, dict)
                }

                if published_versions != {
                    EXPECTED_DATA_VERSION
                }:
                    add_error(
                        "Published JSON data_version mismatch: "
                        f"expected only {EXPECTED_DATA_VERSION}, "
                        f"got {published_versions}"
                    )

                # ------------------------------------------------
                # Timestamp consistency
                # ------------------------------------------------

                published_timestamps = [
                    record.get("observed_at")
                    for record in published
                    if isinstance(record, dict)
                ]

                canonical_timestamps = (
                    df["observed_at"]
                    .astype(str)
                    .tolist()
                )

                if published_timestamps != canonical_timestamps:
                    add_error(
                        "Published JSON observed_at values "
                        "do not match canonical CSV"
                    )


# ============================================================
# PROFILE VALIDATION
# ============================================================

if PROFILE.exists():

    profile = load_strict_json(PROFILE)

    if isinstance(profile, dict):

        # Support common profile structures.

        profile_rows = profile.get("row_count")

        if profile_rows is None:
            profile_rows = profile.get(
                "record_count"
            )

        if (
            profile_rows is not None
            and profile_rows != EXPECTED_CANONICAL_ROWS
        ):
            add_error(
                "Data profile row count mismatch: "
                f"expected {EXPECTED_CANONICAL_ROWS}, "
                f"got {profile_rows}"
            )

        profile_cols = profile.get("column_count")

        if (
            profile_cols is not None
            and profile_cols != EXPECTED_CANONICAL_COLS
        ):
            add_error(
                "Data profile column count mismatch: "
                f"expected {EXPECTED_CANONICAL_COLS}, "
                f"got {profile_cols}"
            )


# ============================================================
# REQUIRED SAMPLING REPORT
# ============================================================

if not SAMPLING_REPORT.exists():
    add_error(
        "Missing required docs/SAMPLING_AND_REDUCTION_REPORT.md"
    )


# ============================================================
# PIPELINE DEPENDENCY
# ============================================================

if not REQUIREMENTS_DATA.exists():
    add_error(
        "Missing required requirements-data.txt"
    )


# ============================================================
# FINAL VALIDATION RESULT
# ============================================================

result = {
    "status": "PASS" if not errors else "FAIL",
    "errors": errors,

    "expected": {
        "data_version": EXPECTED_DATA_VERSION,
        "canonical_record_count": EXPECTED_CANONICAL_ROWS,
        "canonical_column_count": EXPECTED_CANONICAL_COLS,
        "observed_at_null_count": 0,
        "is_sampled": False,
    },

    "actual": {
        "canonical_record_count": (
            len(df) if df is not None else None
        ),
        "canonical_column_count": (
            len(df.columns) if df is not None else None
        ),
        "canonical_observed_at_populated": (
            canonical_timestamp_count
        ),
        "source_observed_at_populated": (
            source_timestamp_count
        ),
        "published_record_count": (
            len(published)
            if isinstance(published, list)
            else None
        ),
    },

    "total_data_size_mb": round(
        total_bytes / 1024 / 1024,
        3,
    ),
}


# ============================================================
# WRITE VALIDATION REPORT
# ============================================================

REPORT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

REPORT.write_text(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ),
    encoding="utf-8",
)


# ============================================================
# TERMINAL OUTPUT
# ============================================================

print()
print("=" * 60)
print("PHASE 3 CANONICAL DATA VALIDATION")
print("=" * 60)

print(
    f"Canonical rows: "
    f"{len(df) if df is not None else 'N/A'}"
)

print(
    f"Canonical columns: "
    f"{len(df.columns) if df is not None else 'N/A'}"
)

print(
    f"Source timestamps: "
    f"{source_timestamp_count}"
)

print(
    f"Canonical timestamps: "
    f"{canonical_timestamp_count}"
)

print(
    f"Published records: "
    f"{len(published) if isinstance(published, list) else 'N/A'}"
)

print(
    f"Expected version: "
    f"{EXPECTED_DATA_VERSION}"
)

print(
    f"Validation errors: "
    f"{len(errors)}"
)

print("=" * 60)


if errors:

    print("VALIDATION RESULT: FAIL")
    print()

    for error in errors:
        print(f"- {error}")

    print()
    print(f"Report written to: {REPORT}")

    raise SystemExit(1)


print("VALIDATION RESULT: PASS")
print()
print("Canonical data validation passed.")
print(f"Report written to: {REPORT}")

