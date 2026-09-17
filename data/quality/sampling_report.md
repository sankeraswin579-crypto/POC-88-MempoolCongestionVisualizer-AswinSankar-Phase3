# Sampling and Reduction Report

## Original Source
POC-88 local snapshots generated from the existing Mempool API data flow.

## Original Size
12.083 KB

## Original Record Count
48

## Original Column Count
14

## Selected Sampling Method
Full local source snapshot retained because row count is already within the 10,000-row program limit.

## Random Seed
42

## Final Source Sample
- Path: data/source-sample/source_sample.csv
- Record count: 48
- Column count: 14
- Size: 12.083 KB

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
