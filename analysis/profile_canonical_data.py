from pathlib import Path
import pandas as pd

# ---------------------------------------------------------
# POC-88 PHASE 3 — CANONICAL DATA PROFILING
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Correct Phase 3 canonical dataset
DATA_FILE = PROJECT_ROOT / "data" / "canonical" / "intelligence_data.csv"

# Output report
REPORT_DIR = PROJECT_ROOT / "analysis" / "reports"
REPORT_FILE = REPORT_DIR / "data_profile_report.txt"

print("=" * 70)
print("POC-88 PHASE 3 — CANONICAL DATA PROFILING")
print("=" * 70)

# ---------------------------------------------------------
# 1. Check dataset
# ---------------------------------------------------------

if not DATA_FILE.exists():
    print()
    print("ERROR: Canonical CSV not found:")
    print(DATA_FILE)
    raise SystemExit(1)

print()
print(f"Dataset: {DATA_FILE}")

# ---------------------------------------------------------
# 2. Load dataset
# ---------------------------------------------------------

df = pd.read_csv(DATA_FILE)

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# ---------------------------------------------------------
# Start report
# ---------------------------------------------------------

report = []

report.append("=" * 70)
report.append("POC-88 PHASE 3 — CANONICAL DATA PROFILE REPORT")
report.append("=" * 70)
report.append("")

report.append("DATASET")
report.append("-" * 70)
report.append(f"File: {DATA_FILE}")
report.append(f"Rows: {df.shape[0]}")
report.append(f"Columns: {df.shape[1]}")
report.append("")

# ---------------------------------------------------------
# 3. Column inventory
# ---------------------------------------------------------

report.append("1. COLUMN INVENTORY")
report.append("-" * 70)

for i, column in enumerate(df.columns, start=1):
    report.append(f"{i:02d}. {column}")

report.append("")

# ---------------------------------------------------------
# 4. Data types
# ---------------------------------------------------------

report.append("2. DATA TYPES")
report.append("-" * 70)

for column in df.columns:
    report.append(f"{column}: {df[column].dtype}")

report.append("")

# ---------------------------------------------------------
# 5. Missing values
# ---------------------------------------------------------

report.append("3. MISSING VALUES")
report.append("-" * 70)

missing = df.isna().sum()

for column, value in missing.items():
    report.append(f"{column}: {value}")

report.append("")
report.append(f"Total missing cells: {int(missing.sum())}")
report.append("")

# ---------------------------------------------------------
# 6. Unique values
# ---------------------------------------------------------

report.append("4. UNIQUE VALUE COUNTS")
report.append("-" * 70)

for column in df.columns:
    report.append(f"{column}: {df[column].nunique(dropna=True)}")

report.append("")

# ---------------------------------------------------------
# 7. Numeric profile
# ---------------------------------------------------------

report.append("5. NUMERIC PROFILE")
report.append("-" * 70)

numeric_columns = df.select_dtypes(include="number").columns.tolist()

if numeric_columns:
    for column in numeric_columns:
        series = df[column].dropna()

        report.append(f"\n{column}")
        report.append(f"  Count : {len(series)}")
        report.append(f"  Min   : {series.min()}")
        report.append(f"  Max   : {series.max()}")
        report.append(f"  Mean  : {series.mean()}")
        report.append(f"  Median: {series.median()}")
else:
    report.append("No numeric columns detected.")

report.append("")

# ---------------------------------------------------------
# 8. Timestamp profile
# ---------------------------------------------------------

report.append("6. TIMESTAMP PROFILE")
report.append("-" * 70)

timestamp_column = None

for column in df.columns:
    if column.lower() in [
        "observed_at",
        "timestamp",
        "created_at",
        "updated_at"
    ]:
        timestamp_column = column
        break

if timestamp_column:
    timestamps = pd.to_datetime(
        df[timestamp_column],
        errors="coerce",
        utc=True
    )

    report.append(f"Timestamp column: {timestamp_column}")
    report.append(f"Valid timestamps: {timestamps.notna().sum()}")
    report.append(f"Invalid timestamps: {timestamps.isna().sum()}")

    if timestamps.notna().any():
        report.append(f"Minimum timestamp: {timestamps.min()}")
        report.append(f"Maximum timestamp: {timestamps.max()}")
else:
    report.append("No recognized timestamp column found.")

report.append("")

# ---------------------------------------------------------
# 9. Duplicate check
# ---------------------------------------------------------

report.append("7. DUPLICATE CHECK")
report.append("-" * 70)

duplicate_rows = int(df.duplicated().sum())

report.append(f"Duplicate rows: {duplicate_rows}")

if "record_id" in df.columns:
    duplicate_record_ids = int(df["record_id"].duplicated().sum())
    report.append(f"Duplicate record_id values: {duplicate_record_ids}")

report.append("")

# ---------------------------------------------------------
# 10. Record type distribution
# ---------------------------------------------------------

report.append("8. RECORD TYPE DISTRIBUTION")
report.append("-" * 70)

if "record_type" in df.columns:
    counts = df["record_type"].value_counts(dropna=False)

    for value, count in counts.items():
        report.append(f"{value}: {count}")
else:
    report.append("record_type column not found.")

report.append("")

# ---------------------------------------------------------
# 11. Category distribution
# ---------------------------------------------------------

report.append("9. CATEGORY DISTRIBUTION")
report.append("-" * 70)

if "category" in df.columns:
    counts = df["category"].value_counts(dropna=False)

    for value, count in counts.items():
        report.append(f"{value}: {count}")
else:
    report.append("category column not found.")

report.append("")

# ---------------------------------------------------------
# 12. Subcategory distribution
# ---------------------------------------------------------

report.append("10. SUBCATEGORY DISTRIBUTION")
report.append("-" * 70)

if "subcategory" in df.columns:
    counts = df["subcategory"].value_counts(dropna=False)

    for value, count in counts.items():
        report.append(f"{value}: {count}")
else:
    report.append("subcategory column not found.")

report.append("")

# ---------------------------------------------------------
# 13. Metric inventory
# ---------------------------------------------------------

report.append("11. METRIC INVENTORY")
report.append("-" * 70)

if "metric_name" in df.columns:
    metrics = df["metric_name"].value_counts(dropna=False)

    for value, count in metrics.items():
        report.append(f"{value}: {count}")
else:
    report.append("metric_name column not found.")

report.append("")

# ---------------------------------------------------------
# 14. Preview
# ---------------------------------------------------------

report.append("12. SAMPLE RECORDS")
report.append("-" * 70)

report.append(df.head(5).to_string(index=False))

report.append("")
report.append("=" * 70)
report.append("END OF REPORT")
report.append("=" * 70)

# ---------------------------------------------------------
# Save report
# ---------------------------------------------------------

REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE.write_text(
    "\n".join(report),
    encoding="utf-8"
)

print()
print("=" * 70)
print("PROFILE COMPLETE")
print("=" * 70)
print()
print(f"Report saved to:")
print(REPORT_FILE)
print()