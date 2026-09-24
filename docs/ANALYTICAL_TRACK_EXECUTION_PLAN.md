# Analytical Track Execution Plan

## Phase 3 — Analytical Track Development, Validation & Intelligence Output

## 1. Objective

Develop and validate the Temporal Analytical Track using the approved Phase 3 canonical intelligence dataset.

## 2. Analytical Question

How do observed Bitcoin mempool, transaction, block, and fee measurements vary across the captured observation timestamps?

## 3. Track Scope

Selected analytical track:

**Temporal Analytical Track**

The track is aligned with the Phase 3 analytical readiness assessment, which identified temporal analysis as READY WITH LIMITATIONS.

## 4. Mandatory Input

Authoritative input:

`data/canonical/intelligence_data.csv`

Data version:

`1.0.1`

Expected dataset:

- 48 records
- 20 columns
- 11 unique observation timestamps
- Source: mempool.space

## 5. Execution Sequence

1. Load the canonical dataset.
2. Parse `observed_at`.
3. Sort observations chronologically.
4. Establish timestamp coverage.
5. Identify compatible metric groups.
6. Calculate metric-level temporal summaries.
7. Validate the analytical output.
8. Review weak cases and limitations.
9. Export intelligence results.
10. Export intelligence summary.
11. Perform a clean rerun.
12. Preserve reproducible evidence.

## 6. Analytical Method

The temporal track compares observed measurements across captured timestamps.

Compatible metric groups are summarized using:

- observation count
- minimum
- maximum
- mean
- metric name
- metric unit
- category

Metrics with incompatible units remain separated.

## 7. Validation

The validation process checks:

- canonical data version
- expected record count
- expected timestamp count
- timestamp summary presence
- metric summary presence
- metric range validity

Expected result:

`PASS`

## 8. Weak-Case Review

The review covers:

- limited timestamp coverage
- metric compatibility
- predictive interpretation

The dataset is treated as a captured operational sample.

## 9. Execution Scripts

Analytical execution:

`data-science/scripts/run_analytical_track.py`

Validation:

`data-science/scripts/validate_analytical_track.py`

Intelligence export:

`data-science/scripts/export_intelligence_results.py`

Track implementation:

`data-science/scripts/track-specific/temporal_track.py`

## 10. Output Artifacts

- `temporal_track_raw.json`
- `validation_metrics.json`
- `intelligence_results.json`
- `intelligence_summary.json`
- `weak_case_review.json`

## 11. Interpretation Boundary

The output describes observed temporal variation in the captured sample.

It does not establish:

- forecasting capability
- predictive capability
- causal relationships
- continuous historical time-series behavior

## 12. Reproducibility

The analytical pipeline can be executed from the repository using the track runner, validator, exporter, and track-specific implementation.

The evidence package contains implementation, validation, intelligence results, summary output, and limitation review.
