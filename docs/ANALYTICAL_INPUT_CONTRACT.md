# Analytical Input Contract

## 1. Purpose

This document defines the input contract for the Phase 3 **Track A — Comparative Analytical Track**.

## 2. Authoritative Input

The analytical track consumes:

data/canonical/intelligence_data.csv

The analytical track must not substitute a second cleaned dataset.

## 3. Data Version

Expected:

1.0.1

## 4. Dataset Expectations

Expected record count:

48

Expected column count:

20

Expected unique observation timestamps:

11

Expected source:

mempool.space

## 5. Supporting Observation Field

Supporting observation field:

observed_at

The field preserves the observation timestamp associated with each canonical record. Timestamps are retained as supporting evidence and must not be interpreted as establishing a continuous time series.

## 6. Canonical Fields

The canonical dataset contains:

- ecord_id
- ecord_type
- observed_at
- entity_id
- elated_entity_id
- entity_name
- category
- subcategory
- status
- stage
- metric_name
- metric_value
- metric_unit
- 	ext_value
- latitude
- longitude
- source_name
- source_record_id
- is_synthetic
- data_version

## 7. Metric Compatibility

Metric values must be interpreted together with:

- category
- metric_name
- metric_unit

Compatible observations may be grouped only when these dimensions match.

Incompatible measurement units must not be combined into one numerical comparison group.

## 8. Comparative Semantics

Track A uses compatible metric groups to establish deterministic comparative baselines.

For each compatible group:

- observations are grouped by category, metric_name, and metric_unit
- the arithmetic mean is used as the comparative baseline
- individual observations are compared against that baseline
- groups with multiple observations may support comparative variation or baseline-match findings
- groups with a single observation are reported as insufficient_comparative_evidence
- timestamps provide supporting evidence only and do not establish temporal trends

## 9. Input Quality

The analytical input must preserve:

- canonical version
- provenance
- metric units
- observation timestamps
- record identity

The canonical dataset has passed the Phase 3 data-quality gate.

## 10. Prohibited Inputs

The analytical track must not introduce:

- alternate cleaned datasets
- manually edited analytical values
- unapproved secondary datasets
- synthetic observations
- manually edited result JSON

## 11. Interpretation Boundary

The input supports deterministic comparative analysis of compatible metric groups.

A single observation does not provide sufficient comparative evidence for a stability interpretation.

The current snapshot does not establish continuous temporal coverage or predictive capability.

## 12. Reproducibility

The analytical implementation consumes the canonical input and generates outputs through repository scripts.

