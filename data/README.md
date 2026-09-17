# POC-88 Phase 3 — Canonical Data Foundation

## Project
POC-88 Mempool Congestion Visualizer

## Phase
Real Rails — Batch 7 — Phase 3 — Data Science & Decision Intelligence

## Purpose
This package provides the controlled canonical data foundation for later
Phase 3 analysis.

## Source
The existing POC-88 application uses the Mempool API and captures local
source snapshots for reproducible Phase 3 processing.

Source:
https://mempool.space/api

Captured source files:
- backend/data/sample_mempool.json
- backend/data/sample_fees.json
- backend/data/sample_blocks.json

## Canonical Source of Truth

data/canonical/intelligence_data.csv

All later Phase 3 analytical work must read from this canonical dataset
or from outputs generated directly from it.

## Pipeline

1. extract_data.py
2. sample_data.py
3. standardize_data.py
4. validate_data.py
5. publish_data.py

## Controlled Limits

- Total /data directory: <= 10 MB
- Main files: <= 5 MB each
- Default rows: <= 10,000
- Default columns: <= 50
- text_value: <= 500 characters
- Binary/media files: not included

## Data Safety

The package contains public blockchain/mempool information and does not
intentionally contain personal, confidential, restricted, or secret data.

## Reproducibility

The canonical dataset is generated through the committed Python pipeline
rather than maintained through manual CSV editing.

Random seed:
42

Data version:
1.0.0
