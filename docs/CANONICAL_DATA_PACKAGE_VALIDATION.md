# POC-88 — Canonical Data Package Validation

## Validation Scope

Phase 3 Post #1 — Canonical Data Foundation.

## Required Checks

- Required paths exist.
- /data <= 10 MB.
- Main files <= 5 MB.
- Canonical rows <= 10,000.
- Canonical columns <= 50.
- Required canonical columns exist in the correct order.
- record_id is non-null and unique.
- source_name is populated.
- is_synthetic is populated.
- data_version is populated.
- observed_at is valid when present.
- metric_value is numeric when present.
- text_value <= 500 characters.

## Validation Command

python scripts/data_pipeline/validate_data.py

## Publish Command

python scripts/data_pipeline/publish_data.py

## Canonical Source of Truth

data/canonical/intelligence_data.csv

## Existing Application

The existing POC-88 operational visualization is preserved.

## Post #1 Boundary

This post covers data-source inventory, local source sampling,
canonical mapping, metadata, validation, published JSON, and
build/deployment readiness.

EDA, feature engineering, machine learning, forecasting,
risk scoring, anomaly detection, Data Intelligence development,
and natural-language assistant work are outside this post.

## Current Status

Ready for Canonical Data Package Review
