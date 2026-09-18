# Sampling and Reduction Report

## 1. Source

- Source: mempool.space public Bitcoin API
- Source type: Point-in-time public API snapshot
- Dataset: POC-88 Mempool Congestion Visualizer
- Source sample file: `data/source-sample/source_sample.csv`

## 2. Original Source Size

- Original source snapshot records: 48
- Canonical records retained: 48
- Canonical columns: 20

## 3. Sampling / Reduction Decision

The complete committed 48-record local source snapshot was retained.

No row reduction was performed.

Therefore:

- `is_sampled`: `false`
- `sampling_method`: `full_local_source_snapshot_retained`
- Original records: 48
- Sample records: 48
- Canonical records: 48

The configured random seed is 42, but no random sampling operation was executed because the complete 48-record snapshot was retained.

## 4. Data Coverage

The retained snapshot contains records covering:

- Current Bitcoin mempool measurements
- Fee-estimation measurements
- Recent-block measurements

All 48 source timestamps were preserved during canonical standardization.

The canonical dataset contains 48 populated `observed_at` values.

## 5. Timestamp Preservation

The canonicalization pipeline preserves the source `observed_at` timestamps.

The source snapshot contains 48 non-null timestamps, and the canonical dataset contains 48 non-null timestamps.

The timestamp normalization handles mixed ISO-8601 timestamp precision, including timestamps with fractional seconds and timestamps without fractional seconds.

## 6. Point-in-Time Limitation

This dataset represents a committed point-in-time snapshot of the mempool and related Bitcoin network measurements.

It is not a continuously collected historical time series.

Therefore, analytical conclusions should be interpreted within the scope of the captured snapshot.

## 7. Reproducibility

The Phase 3 data pipeline can be reproduced using the committed pipeline scripts.

Recommended execution order:

```powershell
python scripts/data_pipeline/extract_data.py
python scripts/data_pipeline/sample_data.py
python scripts/data_pipeline/standardize_data.py
python scripts/data_pipeline/profile_data.py
python scripts/data_pipeline/publish_data.py
python scripts/data_pipeline/validate_data.py