# Phase 3 — Data Science: Profiling, Quality Assessment & Analytical Readiness

## 1. Purpose

This directory contains the Data Science preparation and analytical-readiness work for the Phase 3 canonical Bitcoin mempool dataset.

The objective of Post #2 is to establish:

* what the canonical dataset contains;
* whether the data is structurally and analytically usable;
* the numerical, temporal, categorical and applicable text characteristics;
* data-quality limitations;
* representativeness and coverage limitations;
* the appropriate data archetype;
* which analytical tracks are supported;
* which analytical tracks require additional data;
* why predictive modelling is not currently supported.

The analysis is based on the validated canonical dataset generated during Phase 3 Post #1.

---

## 2. Dataset Scope

### Source

The dataset is derived from publicly available Bitcoin mempool, transaction, block and fee information obtained from the `mempool.space` API.

### Dataset Type

**Time-Series Measurement**

The canonical dataset contains measurements associated with observed timestamps.

However, the current canonical dataset contains only **11 observed timestamps**. Therefore, it represents a limited temporal sample rather than a sufficiently long continuous historical time series.

### Important Limitation

The available observations should be used primarily for comparison across the observed timestamps.

They should not be interpreted as a complete representation of long-term Bitcoin mempool behaviour.

---

## 3. Canonical Dataset

The canonical dataset is located at:

```text
data/canonical/intelligence_data.csv
```

The dataset was generated from the validated source sample and standardized into the canonical analytical structure during Phase 3 Post #1.

### Canonical Dataset Statistics

| Property                   |                Value |
| -------------------------- | -------------------: |
| Rows                       |                   48 |
| Columns                    |                   20 |
| Unique observed timestamps |                   11 |
| Earliest observation       | 2026-09-17T07:34:19Z |
| Latest observation         | 2026-09-17T09:15:22Z |
| File size                  |         13,437 bytes |
| File size                  |          0.012815 MB |
| Duplicate rows             |                    0 |
| Invalid timestamps         |                    0 |

The canonical dataset therefore represents **48 standardized records across 11 observed timestamps**.

Because the temporal coverage is limited, the dataset should be treated as a limited measurement sample rather than a sufficiently long historical time series.

---

## 4. Data Profiling

The profiling process examines the canonical dataset from multiple perspectives.

### 4.1 Structural Profiling

The following characteristics are assessed:

* number of rows;
* number of columns;
* column names;
* data types;
* missing values;
* duplicate records;
* unique-value counts;
* schema consistency.

The current canonical dataset contains **48 rows and 20 columns**.

Duplicate-row and duplicate-record checks identified no duplicate records.

### 4.2 Numerical Profiling

Applicable numerical fields are assessed using:

* count;
* minimum;
* maximum;
* mean;
* median;
* standard deviation;
* quartiles;
* missing-value counts;
* zero-value checks where applicable.

The purpose is to understand the scale, distribution and basic statistical characteristics of the measured variables.

Numerical profiling is interpreted within the limitation of the available observation count.

### 4.3 Temporal Profiling

Temporal fields are examined for:

* number of unique timestamps;
* earliest observation;
* latest observation;
* timestamp ordering;
* timestamp completeness;
* temporal gaps;
* available coverage.

The canonical dataset contains:

* **11 unique observed timestamps**;
* earliest observation: `2026-09-17T07:34:19Z`;
* latest observation: `2026-09-17T09:15:22Z`;
* 48 valid timestamp records;
* 0 invalid timestamps.

The limited temporal coverage is an important analytical constraint.

### 4.4 Categorical Profiling

Applicable categorical fields are assessed using:

* unique-value counts;
* frequency distributions;
* missing values;
* unexpected categories;
* category consistency.

The canonical dataset includes categorical fields describing record types and related measurement categories.

The observed record-type distribution consists of measurement records, with category distributions examined as part of the profiling process.

### 4.5 Text Profiling

Where text-like fields are present, applicable checks include:

* null/empty values;
* distinct values;
* string length;
* repeated values;
* basic consistency checks.

Text profiling is only applied where the canonical schema contains suitable text attributes.

---

## 5. Data Quality Assessment

The canonical dataset is assessed for analytical quality using the following checks:

| Quality Area                 | Assessment |
| ---------------------------- | ---------- |
| Schema validity              | Checked    |
| Data types                   | Checked    |
| Missing values               | Checked    |
| Duplicate records            | Checked    |
| Numeric validity             | Checked    |
| Temporal validity            | Checked    |
| Timestamp completeness       | Checked    |
| Categorical consistency      | Checked    |
| Invalid numeric values       | Checked    |
| NaN / Infinity values        | Checked    |
| Canonical column consistency | Checked    |

Phase 3 Post #1 established that the canonical dataset was structurally valid.

Post #2 extends this validation into analytical profiling, representativeness assessment and analytical readiness.

The quality assessment should distinguish between:

1. **technical data validity**, and
2. **analytical suitability**.

A dataset can be structurally valid while still being insufficient for certain analytical objectives.

---

## 6. Representativeness and Coverage

The dataset is useful for examining the Bitcoin mempool and related network conditions represented by the collected observations.

However, important representativeness limitations must be considered.

### Limitation 1 — Limited Temporal Coverage

Only **11 observed timestamps** are currently available.

Therefore, the dataset does not provide sufficient temporal history for reliable long-term trend analysis or predictive modelling.

### Limitation 2 — Single Source

The current canonical dataset is derived from the public `mempool.space` API.

Independent data sources have not been incorporated into the canonical dataset.

### Limitation 3 — No Geographic Coverage

The dataset describes Bitcoin mempool/network measurements and does not provide geographic observations suitable for geographic population-level analysis.

### Limitation 4 — Snapshot-Oriented Observations

The observations represent measurements collected at specific timestamps.

They should not automatically be interpreted as a continuous high-frequency time series.

### Limitation 5 — Limited Observation Count

The dataset contains only 48 records distributed across 11 observed timestamps.

Consequently, statistical conclusions and generalization should be treated cautiously.

---

## 7. Data Archetype

### Selected Archetype

**Time-Series Measurement**

### Rationale

The canonical records contain measurements associated with timestamps and therefore have a temporal measurement structure.

However, the dataset currently contains only **11 observed timestamps**.

Consequently:

* timestamp-based comparison is possible;
* temporal profiling is possible;
* limited temporal comparison is possible;
* broader long-term time-series inference is constrained;
* forecasting is not supported by the current dataset.

The archetype describes the structure of the available data and does not imply that the dataset has sufficient historical depth for forecasting.

---

## 8. Primary Analytical Question

### Track A — Comparative

**Primary Analytical Question:**

> How do Bitcoin mempool congestion and related transaction and fee characteristics differ across the available observed timestamps in the canonical dataset?

This question is intentionally framed as a comparative question.

It does not assume that the available 11 timestamps constitute a sufficiently long historical time series.

The question is therefore aligned with the current evidence and the supported primary analytical direction.

---

# 9. Analytical Track Assessment

The analytical tracks are assessed individually against the current canonical dataset.

## Track A — Comparative

**Status: Supported**

The dataset contains multiple observations with comparable numerical and temporal measurements.

The available timestamps allow comparison of congestion, transaction, fee and related network measurements across the observed snapshots.

This is the primary analytical direction for the current dataset.

---

## Track B — Trend / Time-Series

**Status: Conditional**

Timestamp information is available, but only 11 timestamps are currently represented.

The data can support limited temporal comparison.

However, the current coverage is insufficient for making broad long-term time-series conclusions.

Additional historical observations would be required for stronger time-series analysis.

---

## Track C — Segmentation / Clustering

**Status: Conditional**

Numerical measurements may potentially be used to identify groups of observations with similar characteristics.

However, the current number of observations is limited, reducing the reliability and usefulness of clustering-based segmentation.

A larger dataset would be required for robust segmentation.

---

## Track D — Anomaly / Outlier Analysis

**Status: Conditional**

The numerical measurements can be inspected for unusually high or low observations.

However, the limited number of timestamps means that detected anomalies would require careful interpretation.

Additional observations would improve the confidence of anomaly identification.

---

## Track E — Relationship / Association Analysis

**Status: Conditional**

Relationships between numerical variables can be explored descriptively using correlation or other appropriate association measures.

However, the small number of observations limits statistical strength and generalization.

Additional observations would be required for stronger relationship analysis.

---

## Track F — Classification

**Status: Not Supported**

The current canonical dataset does not establish a sufficiently justified target variable and labelled training population for supervised classification.

Additional labelled observations and a clearly defined target would be required before classification could be appropriately evaluated.

---

## Track G — Predictive Modelling / Forecasting

**Status: Not Supported**

Predictive modelling and forecasting are not supported by the current canonical dataset.

The primary limitation is the restricted temporal coverage of only **11 observed timestamps**.

The current data does not provide sufficient historical depth to establish a reliable forecasting dataset.

The dataset should therefore not be used to claim predictive performance, forecast future congestion, or train a production-ready predictive model.

Additional historical observations collected across a substantially longer period would be required before predictive modelling could be appropriately evaluated.

---

## Track H — Decision / Recommendation Analysis

**Status: Conditional**

The current dataset may support limited decision-oriented interpretation based on observed comparative measurements.

For example, observed congestion and fee characteristics could be summarized to identify conditions associated with relatively higher or lower congestion across the available snapshots.

However, the current dataset does not provide sufficient historical coverage, contextual variables or decision-outcome labels to establish robust automated recommendations.

Therefore, decision or recommendation analysis remains conditional.

Additional observations, contextual variables and clearly defined decision objectives would be required for stronger decision-support analysis.

---

# 10. Overall Analytical Readiness

The canonical dataset has passed the structural validation performed during Phase 3 Post #1 and has been assessed during Post #2 for profiling, quality, representativeness and analytical suitability.

### Currently Suitable For

* canonical data profiling;
* structural assessment;
* data-quality assessment;
* numerical distribution analysis;
* categorical analysis;
* comparative analysis;
* limited temporal comparison;
* conditional relationship/association analysis;
* conditional anomaly/outlier inspection;
* conditional segmentation exploration.

### Currently Not Suitable For

* supervised classification;
* predictive modelling;
* reliable long-term forecasting;
* broad population-level generalization.

The primary analytical direction is therefore:

**Track A — Comparative**

with the primary analytical question:

> How do Bitcoin mempool congestion and related transaction and fee characteristics differ across the available observed timestamps in the canonical dataset?

---

# 11. Analytical Readiness Summary

| Area                             | Assessment                          |
| -------------------------------- | ----------------------------------- |
| Dataset structure                | Validated                           |
| Canonical schema                 | Validated                           |
| Numerical profiling              | Applicable                          |
| Temporal profiling               | Applicable                          |
| Categorical profiling            | Applicable                          |
| Text profiling                   | Applicable where schema supports it |
| Data-quality assessment          | Completed                           |
| Representativeness assessment    | Completed                           |
| Data archetype                   | Time-Series Measurement             |
| Temporal coverage                | Limited — 11 timestamps             |
| Primary analytical track         | Track A — Comparative               |
| Classification                   | Not Supported                       |
| Predictive modelling             | Not Supported                       |
| Forecasting                      | Not Supported                       |
| Decision/recommendation analysis | Conditional                         |

---

# 12. Key Data Limitations

The following limitations must remain explicit in any interpretation of the dataset:

1. Only **11 observed timestamps** are available.
2. The canonical dataset contains **48 records across 20 columns**.
3. The dataset is derived from a single public source, `mempool.space`.
4. The observations represent collected snapshots rather than a sufficiently long continuous historical series.
5. Geographic coverage is not represented.
6. The limited observation count restricts statistical strength and generalization.
7. Conditional analytical tracks require additional observations before stronger conclusions can be made.
8. Predictive modelling and forecasting are not supported by the current dataset.
9. The current dataset should not be treated as a complete representation of long-term Bitcoin mempool behaviour.

---

# 13. Recommended Analytical Progression

Based on the current evidence, the recommended analytical progression is:

### Stage 1 — Comparative Analysis

Use Track A as the primary analytical direction.

Compare:

* congestion-related measurements;
* transaction counts;
* fee-related measurements;
* block-related measurements;
* other applicable numerical characteristics;

across the available observed timestamps.

### Stage 2 — Conditional Analytical Extensions

Where justified by the evidence, investigate:

* limited temporal comparisons;
* relationships between numerical variables;
* potential outliers;
* observation segmentation.

These should remain explicitly conditional because of the limited dataset size and temporal coverage.

### Stage 3 — Future Data Expansion

Before attempting classification, forecasting or production-level predictive modelling, expand the dataset with:

* substantially more historical timestamps;
* broader temporal coverage;
* clearly defined target variables where supervised learning is required;
* additional contextual variables where decision-support analysis is required;
* additional sources where independent validation is necessary.

---

# 14. Conclusion

Phase 3 Post #2 establishes the analytical readiness of the canonical Bitcoin mempool dataset.

The dataset is classified as a:

**Time-Series Measurement**

dataset with **11 observed timestamps** and **48 standardized records across 20 columns**.

The primary supported analytical direction is:

**Track A — Comparative**

The corresponding primary analytical question is:

> How do Bitcoin mempool congestion and related transaction and fee characteristics differ across the available observed timestamps in the canonical dataset?

The current dataset supports structured profiling, quality assessment and comparative analysis.

Several additional analytical tracks remain conditional because of the limited number of observations and restricted contextual coverage.

Classification and predictive modelling/forecasting are **not supported** by the current dataset.

The purpose of this assessment is therefore to establish a defensible analytical foundation, document the current evidence, clearly identify limitations, and define which analytical directions can reasonably proceed with the available canonical data.

---

## 15. Phase 3 Post #2 Status

**POST #2 — PROFILING, QUALITY ASSESSMENT & ANALYTICAL READINESS**

**Status: COMPLETED — READY FOR FINAL REVIEW**

The Post #2 assessment documents:

* canonical dataset structure;
* numerical profiling;
* temporal profiling;
* categorical profiling;
* applicable text profiling;
* data-quality checks;
* representativeness limitations;
* Time-Series Measurement archetype;
* Track A–H analytical suitability;
* primary comparative analytical question;
* rejection of unsupported predictive modelling;
* future data requirements for conditional analytical tracks.
