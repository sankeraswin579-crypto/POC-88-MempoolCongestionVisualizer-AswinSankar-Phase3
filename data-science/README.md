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

The dataset is derived from publicly available Bitcoin mempool and fee information obtained from the `mempool.space` API.

### Dataset type

**Time-Series Measurement**

The dataset contains measurements observed at multiple timestamps.

However, the current canonical dataset contains only **11 observed timestamps**. Therefore, it represents a limited temporal sample rather than a sufficiently long continuous historical time series.

### Important limitation

The available observations should be used for comparison across the observed timestamps and should not be interpreted as a complete representation of long-term Bitcoin mempool behaviour.

---

## 3. Canonical Dataset

The canonical dataset is:

```text
intelligence_data.csv
```

The canonical schema contains the standardized fields produced during Post #1.

The dataset was generated from the validated source sample and standardized into the canonical analytical structure.

### Canonical file size

The exact file size must be taken from the final committed `intelligence_data.csv` file.

Windows PowerShell:

```powershell
(Get-Item .\data\intelligence_data.csv).Length
```

Size in MB:

```powershell
"{0:N6} MB" -f ((Get-Item .\data\intelligence_data.csv).Length / 1MB)
```

Do not use a placeholder value in the final Post #2 submission.

---

## 4. Data Profiling

The profiling process examines the canonical dataset from multiple perspectives.

### 4.1 Structural profiling

The following are checked:

* number of rows;
* number of columns;
* column names;
* data types;
* missing values;
* duplicate records;
* unique-value counts;
* schema consistency.

### 4.2 Numerical profiling

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

### 4.3 Temporal profiling

Temporal fields are examined for:

* number of unique timestamps;
* earliest observation;
* latest observation;
* timestamp ordering;
* timestamp completeness;
* temporal gaps;
* available coverage.

The current dataset contains **11 observed timestamps**.

This limited coverage is an important analytical constraint.

### 4.4 Categorical profiling

Applicable categorical fields are assessed using:

* unique-value counts;
* frequency distributions;
* missing values;
* unexpected categories;
* category consistency.

### 4.5 Text profiling

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

The Post #1 validation established that the canonical dataset was structurally valid.

Post #2 extends this validation into analytical profiling and readiness assessment.

---

## 6. Representativeness

The dataset is useful for examining the observed Bitcoin mempool conditions represented by the collected snapshots.

However, the dataset has important representativeness limitations.

### Limitation 1 — Limited temporal coverage

Only **11 timestamps** are currently available.

Therefore, the dataset does not provide sufficient temporal history for reliable long-term trend analysis or predictive modelling.

### Limitation 2 — Single source

The current dataset is derived from the `mempool.space` public API.

Independent data sources have not been incorporated into the canonical dataset.

### Limitation 3 — No geographic coverage

The dataset describes Bitcoin mempool/network measurements and does not provide a geographic sample suitable for geographic population-level analysis.

### Limitation 4 — Snapshot-oriented observations

The observations represent collected measurements at specific timestamps.

They should not automatically be interpreted as a continuous high-frequency time series.

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
* long-term time-series inference is constrained;
* forecasting is not supported by the current dataset.

---

## 8. Primary Analytical Question

### Track A — Comparative

**Primary Analytical Question:**

> How do Bitcoin mempool congestion and related transaction and fee characteristics differ across the available observed timestamps in the canonical dataset?

This question is intentionally framed as a comparative question.

It does not assume that the available 11 timestamps constitute a sufficiently long historical time series.

---

# 9. Analytical Track Assessment

## Track A — Comparative

**Status: Supported**

The dataset contains multiple observations with comparable numerical and temporal measurements.

The available timestamps allow comparison of congestion, transaction, fee and related network measurements across the observed snapshots.

---

## Track B — Trend / Time-Series

**Status: Conditional**

Timestamp information is available, but only 11 timestamps are currently represented.

The data can support limited temporal comparison, but the current coverage is insufficient for making broad long-term time-series conclusions.

Additional historical observations would be required for stronger time-series analysis.

---

## Track C — Segmentation / Clustering

**Status: Conditional**

Numerical measurements may potentially be used to identify groups of observations with similar characteristics.

However, the current number of observations is small, limiting the reliability and usefulness of clustering-based segmentation.

A larger dataset would be required for robust segmentation.

---

## Track D — Anomaly / Outlier Analysis

**Status: Conditional**

The numerical measurements can be inspected for unusually high or low observations.

However, the limited number of timestamps means that detected anomalies would require careful interpretation and additional observations would improve confidence.

---

## Track E — Relationship / Association Analysis

**Status: Conditional**

Relationships between numerical variables can be explored descriptively using correlation or other association measures where appropriate.

However, the small number of observations limits statistical strength and generalization.

---

## Track F — Classification

**Status: Not Supported**

The current canonical dataset does not establish a sufficiently justified target variable and labelled training population for supervised classification.

Additional labelled observations and a clearly defined target would be required.

---

## Track G — Predictive Modelling / Forecasting

**Status: Not Supported**

Predictive modelling is rejected for the current dataset.

The primary limitat
