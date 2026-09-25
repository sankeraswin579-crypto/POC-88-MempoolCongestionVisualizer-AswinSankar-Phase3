# Intelligence Output Contract

## 1. Purpose

This document defines the machine-readable output contract for Phase 3 analytical intelligence results.

## 2. Result Output

Primary result file:

`data-science/outputs/intelligence_results.json`

## 3. Result Fields

Core result fields:

- `result_id`
- `result_type`
- `metric_name`
- `result_value`
- `result_unit`
- `category`
- `finding`
- `evidence`
- `method_version`
- `data_version`
- `generated_at`
- `quality_status`
- `limitation`

## 4. Field Semantics

`result_id` identifies the analytical result.

`result_type` identifies the result type.

`metric_name` identifies the measured metric.

`result_value` contains the calculated analytical value.

`result_unit` identifies the measurement unit.

`category` identifies the canonical data category.

`finding` provides the analytical interpretation.

`evidence` records supporting analytical information.

`method_version` identifies the analytical method.

`data_version` identifies the canonical dataset version.

`generated_at` records result generation time.

`quality_status` records validation status.

`limitation` records important interpretation boundaries.

## 5. Summary Output

Summary file:

`data-science/outputs/intelligence_summary.json`

The summary contains:

- analysis type
- data version
- record count
- unique observed timestamp count
- metric group count
- validation status
- interpretation boundary
- generation timestamp

## 6. Current Quality Status

Current analytical validation:

`PASS`

Validation evidence:

`data-science/outputs/validation_metrics.json`

## 7. Interpretation Boundary

The intelligence output represents observed temporal variation across captured timestamps.

It must not be interpreted as:

- forecasting
- prediction
- causal inference
- continuous historical time-series reconstruction

## 8. Versioning

Data version:

`1.0.1`

Method version:

`comparative-track-v1.0`

## 9. Reproducibility

Run:

`python .\data-science\scripts\run_analytical_track.py`

Then:

`python .\data-science\scripts\validate_analytical_track.py`

Then:

`python .\data-science\scripts\export_intelligence_results.py`

