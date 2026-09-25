# Analytical Method Report

## 1. Analytical Track

Track:

**Track A - Comparative Analytical Track**

Primary analytical question:

> How do observed Bitcoin mempool, transaction, block, and fee measurements vary across the captured observation timestamps?

## 2. Input Dataset

Authoritative source:

`data/canonical/intelligence_data.csv`

Data version:

`1.0.1`

Dataset:

- 48 records
- 20 columns
- 11 unique observation timestamps
- Categories: bitcoin_block, fees, mempool
- Source: mempool.space

## 3. Method

The analytical process:

1. Load the canonical intelligence dataset.
2. Parse `observed_at`.
3. Order observations chronologically.
4. Group compatible measurements.
5. Compare observations across captured timestamps.
6. Calculate minimum, maximum, mean, and observation count for metric groups.
7. Preserve category and unit information.
8. Export structured analytical intelligence.

## 4. Metric Compatibility

Metrics are summarized using:

- category
- metric name
- metric unit

Measurements with incompatible units are not combined into one numerical series.

## 5. Versioning

Data version:

`1.0.1`

Method version:

`comparative-track-v1.0`

## 6. Interpretation Boundary

The analysis describes observed temporal variation in the captured sample.

It does not establish:

- forecasting
- prediction
- causal inference
- continuous historical time-series behavior

## 7. Reproducibility

Analytical runner:

`data-science/scripts/run_analytical_track.py`

Track implementation:

`data-science/scripts/track-specific/comparative_track.py`

Validation:

`data-science/scripts/validate_analytical_track.py`

Export:

`data-science/scripts/export_intelligence_results.py`

