# POC-88 — Canonical Data Mapping

## Purpose

This document records how the POC-88 source fields are transformed into
the Phase 3 universal canonical schema.

## Mappings

| Source | Source Field | Canonical Field | Transformation |
|---|---|---|---|
| Mempool | count | metric_value | Numeric transaction count |
| Mempool | vsize | metric_value | Numeric virtual-size value |
| Mempool | total_fee | metric_value | Numeric fee value |
| Fees | fastestFee | metric_value | Numeric fee rate |
| Fees | halfHourFee | metric_value | Numeric fee rate |
| Fees | hourFee | metric_value | Numeric fee rate |
| Fees | economyFee | metric_value | Numeric fee rate |
| Fees | minimumFee | metric_value | Numeric fee rate |
| Blocks | id | entity_id / source_record_id | Stable block identifier |
| Blocks | height | entity_name | Human-readable block reference |
| Blocks | timestamp | observed_at | Unix timestamp converted to ISO-8601 UTC |
| Blocks | tx_count | metric_value | Numeric transaction count |
| Blocks | size | metric_value | Numeric block size |
| Blocks | weight | metric_value | Numeric block weight |
| Blocks | difficulty | metric_value | Numeric difficulty value |

## Record Type

Source measurements are represented using:

measurement

## Category Mapping

### Mempool
- category: mempool
- subcategory: current_snapshot

### Fees
- category: fees
- subcategory: recommended_rates

### Blocks
- category: bitcoin_block
- subcategory: recent_block

## Status

- Mempool: observed
- Fees: observed
- Blocks: confirmed

## Units

- transaction counts: transactions
- virtual size: vbytes
- fees: sats or sat/vbyte as represented by the source metric
- block size: bytes
- block weight: weight_units
- difficulty: difficulty

## Generated Fields

### record_id
Generated deterministically using the format:

POC88-00001
POC88-00002
...

### related_entity_id
Not applicable to the current measurement records.

### stage
Not applicable to the current measurement records.

### text_value
Contains a short source-group descriptor and is limited to 500 characters.

### latitude / longitude
Not applicable because the POC-88 dataset is not geographic.

### is_synthetic
Set to false because the records originate from captured public source data.

### data_version
Set to:

1.0.0

## Removed / Not Canonicalized Fields

The complete source block metadata is not represented as separate metrics in
this first canonical package when it is not needed for the selected analytical
foundation.

The mempool fee histogram is retained in the raw source snapshot but is not
expanded into separate canonical records in this package.

## Reproducibility

The canonical CSV must be regenerated from the source sample through:

python scripts/data_pipeline/extract_data.py
python scripts/data_pipeline/sample_data.py
python scripts/data_pipeline/standardize_data.py
