# Analytical Input Contract

## 1. Purpose

This document defines the input contract for the Phase 3 Temporal Analytical Track.

## 2. Authoritative Input

The analytical track consumes:

`data/canonical/intelligence_data.csv`

The analytical track must not substitute a second cleaned dataset.

## 3. Data Version

Expected:

`1.0.1`

## 4. Dataset Expectations

Expected record count:

`48`

Expected column count:

`20`

Expected unique observation timestamps:

`11`

Expected source:

`mempool.space`

## 5. Required Temporal Field

Primary temporal field:

`observed_at`

The field provides the observation timestamp used for temporal ordering.

## 6. Canonical Fields

The canonical dataset contains:

- `record_id`
- `record_type`
- `observed_at`
- `entity_id`
- `related_entity_id`
- `entity_name`
- `category`
- `subcategory`
- `status`
- `stage`
- `metric_name`
- `metric_value`
- `metric_unit`
- `text_value`
- `latitude`
- `longitude`
- `source_name`
- `source_record_id`
- `is_synthetic`
- `data_version`

## 7. Metric Compatibility

Metric values must be interpreted together with:

- `category`
- `metric_name`
- `metric_unit`

Incompatible measurement units must not be combined into one numerical series.

## 8. Temporal Semantics

`observed_at` is used for temporal ordering.

The timestamps represent observations in the available operational sample.

Event timestamps must not automatically be treated as repeated measurements without evidence supporting that interpretation.

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

The input supports descriptive temporal analysis with limitations.

The current snapshot does not establish sufficient historical coverage for predictive analysis.

## 12. Reproducibility

The analytical implementation consumes the canonical input and generates outputs through repository scripts.
