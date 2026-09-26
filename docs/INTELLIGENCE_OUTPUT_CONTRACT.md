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

Comparative summary fields:

- `comparative_group_count`
- `finding_count`
- `comparative_interpretation`

## 4. Field Semantics

`result_id` identifies the analytical result.

`result_type` identifies the analytical result type.

`metric_name` identifies the measured metric.

`result_value` contains the calculated analytical value.

`result_unit` identifies the measurement unit.

`category` identifies the canonical data category.

`finding` provides the comparative analytical interpretation.

`evidence` records supporting analytical information.

`method_version` identifies the analytical method.

`data_version` identifies the canonical dataset version.

`generated_at` records result generation time.

`quality_status` records validation status.

`limitation` records important interpretation boundaries.

`comparative_group_count` records the number of compatible comparative metric groups evaluated.

`finding_count` records the number of validated comparative findings produced.

`comparative_interpretation` records the interpretation derived from the validated comparative findings.

## 5. Summary Output

Summary file:

`data-science/outputs/intelligence_summary.json`

The summary contains:

- analysis type
- data version
- record count
- unique observed timestamp count
- comparative group count
- finding count
- validation status
- comparative interpretation
- interpretation boundary
- generation timestamp

## 6. Current Analytical Track

The approved analytical track for Phase 3 Post #3 is:

`Track A — Comparative`

The implementation compares compatible metric groups within the captured operational sample.

Current validated output:

- validation status: `PASS`
- comparative groups: `12`
- findings: `12`

## 7. Interpretation Boundary

The intelligence output represents validated comparative findings across compatible metric groups in the captured operational sample.

Captured observation timestamps provide dataset context and coverage information only. The approved implementation is Track A — Comparative.

The output must not be interpreted as:

- trend interpretation beyond the captured comparative sample
- forecasting
- prediction
- causal inference
- continuous historical time-series reconstruction

Comparative findings are limited to compatible metric groups in the captured operational sample.

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


