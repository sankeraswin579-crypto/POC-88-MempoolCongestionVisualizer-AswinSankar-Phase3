# POC-88 Phase 3 — Canonical Data Profile

## Dataset Overview

- Canonical dataset: `data/canonical/intelligence_data.csv`
- Rows: 48
- Columns: 20
- Record type: measurement
- Data version: 1.0.1
- Source: mempool.space
- Synthetic records: 0

## Structure

The canonical package contains 48 unique record IDs and 0 duplicate full rows.

## Missingness

The following fields are completely populated for the current measurement records:
- record_id
- observed_at
- entity_id
- entity_name
- category
- subcategory
- status
- metric_name
- metric_value
- metric_unit
- source_name
- source_record_id
- is_synthetic
- data_version

The following fields contain null values across the dataset:
- related_entity_id
- stage
- latitude
- longitude

These fields are retained as part of the canonical schema and are not populated because the current records are operational Bitcoin mempool, fee, and block measurements.

## Dataset Composition

- bitcoin_block: 40 records
- fees: 5 records
- mempool: 3 records

## Temporal Coverage

There are 11 unique observation timestamps in the canonical package.

## Analytical Character

The package is a compact, time-stamped operational measurement dataset covering Bitcoin mempool, fee, and recent-block observations.
