# Analytical Track Execution Plan

## Phase 3 — Analytical Track Development, Validation & Intelligence Output

## 1. Objective

Develop and validate the **Track A — Comparative Analytical Track** using the approved Phase 3 canonical intelligence dataset.

## 2. Analytical Question

How do compatible Bitcoin mempool, transaction, block, and fee measurements compare against deterministic baselines within the captured operational sample?

## 3. Track Scope

Selected analytical track:

**Track A — Comparative**

The track establishes deterministic comparative baselines for compatible metric groups.

Observation timestamps are retained as supporting evidence only and are not used to establish unsupported temporal trends.

## 4. Mandatory Input

Authoritative input:

data/canonical/intelligence_data.csv

Data version:

1.0.1

Expected dataset:

- 48 records
- 20 columns
- 11 unique observation timestamps
- Source: mempool.space

## 5. Execution Sequence

1. Load the canonical dataset.
2. Preserve observed_at as supporting observation evidence.
3. Identify compatible metric groups using category, metric name, and metric unit.
4. Calculate the arithmetic mean baseline for each compatible metric group.
5. Compare observations against their corresponding group baselines.
6. Calculate minimum, maximum, mean, and observation count.
7. Classify multi-observation comparative findings.
8. Classify single-observation groups as insufficient_comparative_evidence.
9. Validate the analytical output.
10. Review weak cases and limitations.
11. Export intelligence results.
12. Export intelligence summary.
13. Perform a clean rerun.
14. Preserve reproducible evidence.

## 6. Analytical Method

The comparative track establishes deterministic baselines for compatible metric groups.

Compatible metric groups are summarized using:

- observation count
- minimum
- maximum
- arithmetic mean baseline
- metric name
- metric unit
- category

Individual observations are compared against the corresponding group baseline.

Metrics with incompatible units remain separated.

Groups with multiple observations provide comparative evidence.

Groups with a single observation are reported as insufficient_comparative_evidence and are not interpreted as stable.

## 7. Validation

The validation process checks:

- canonical data version
- expected record count
- expected timestamp count
- comparative group presence
- observation count validity
- metric summary presence
- metric range validity
- comparative finding validity

Expected result:

PASS

## 8. Weak-Case Review

The review covers:

- single-observation groups
- metric compatibility
- limited comparative evidence
- predictive interpretation

The dataset is treated as a captured operational sample.

Single-observation groups are explicitly identified as insufficient comparative evidence.

## 9. Execution Scripts

Analytical execution:

data-science/scripts/run_analytical_track.py

Validation:

data-science/scripts/validate_analytical_track.py

Intelligence export:

data-science/scripts/export_intelligence_results.py

Track implementation:

data-science/scripts/track-specific/comparative_track.py

## 10. Output Artifacts

- comparative_track_raw.json
- alidation_metrics.json
- intelligence_results.json
- intelligence_summary.json
- weak_case_review.json

## 11. Interpretation Boundary

The output establishes deterministic comparative findings for compatible metric groups in the captured operational sample.

It does not establish:

- forecasting capability
- predictive capability
- causal relationships
- continuous historical time-series behavior
- unsupported temporal trends

Observation timestamps remain supporting evidence only.

## 12. Reproducibility

The analytical pipeline can be executed from the repository using the track runner, validator, exporter, and Track A-specific implementation.

The evidence package contains implementation, validation, intelligence results, summary output, and limitation review.

