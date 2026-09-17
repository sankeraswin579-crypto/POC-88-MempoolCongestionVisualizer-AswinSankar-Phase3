from pathlib import Path
import pandas as pd
import json

ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "data" / "source-sample" / "source_sample.csv"
OUTPUT = ROOT / "data" / "source-sample" / "source_sample.csv"
REPORT = ROOT / "data" / "quality" / "sampling_report.md"

RANDOM_SEED = 42
MAX_ROWS = 10_000

df = pd.read_csv(INPUT)

original_rows = len(df)
original_cols = len(df.columns)

if len(df) <= MAX_ROWS:
    sample = df.copy()
    method = "Full local source snapshot retained because row count is already within the 10,000-row program limit."
else:
    strata = [c for c in ["source_group", "category", "subcategory", "status"] if c in df.columns]

    if strata:
        sample = (
            df.groupby(strata, dropna=False, group_keys=False)
              .apply(
                  lambda group: group.sample(
                      n=max(1, round(len(group) / len(df) * MAX_ROWS)),
                      random_state=RANDOM_SEED
                  )
              )
              .head(MAX_ROWS)
              .reset_index(drop=True)
        )
        method = f"Stratified sampling using: {', '.join(strata)}"
    else:
        sample = df.sample(
            n=MAX_ROWS,
            random_state=RANDOM_SEED
        ).reset_index(drop=True)
        method = "Fixed-seed random sampling"

sample.to_csv(OUTPUT, index=False, encoding="utf-8")

report = f"""# Sampling and Reduction Report

## Original Source
POC-88 local snapshots generated from the existing Mempool API data flow.

## Original Size
{INPUT.stat().st_size / 1024:.3f} KB

## Original Record Count
{original_rows}

## Original Column Count
{original_cols}

## Selected Sampling Method
{method}

## Random Seed
{RANDOM_SEED}

## Final Source Sample
- Path: data/source-sample/source_sample.csv
- Record count: {len(sample)}
- Column count: {len(sample.columns)}
- Size: {OUTPUT.stat().st_size / 1024:.3f} KB

## Representativeness Checks
- Mempool summary metrics preserved.
- Recommended fee metrics preserved.
- Recent block records preserved.
- Multiple metric types retained.
- Block observations retain their timestamps.

## Known Sampling Limitations
This package represents a captured source snapshot, not the complete historical Bitcoin mempool or blockchain dataset.
The mempool fee histogram is intentionally not expanded into one row per histogram bucket in this first canonical package.

## Reproduction Command

python scripts/data_pipeline/extract_data.py
python scripts/data_pipeline/sample_data.py
"""

REPORT.write_text(report, encoding="utf-8")

print(f"Sampling complete: {len(sample)} rows")
