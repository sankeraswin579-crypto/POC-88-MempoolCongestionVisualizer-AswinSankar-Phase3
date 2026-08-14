# Phase 2 — Database VARCHAR Specification

## Mempool Congestion Visualizer

**PoC ID:** POC-88
**Phase:** Phase 2
**Developer:** Aswin Sankar P.S.

---

## 1. Purpose

This document defines the database fields used to store processed Bitcoin mempool analytics and specifies appropriate `VARCHAR` sizes for textual fields.

`VARCHAR` should be used for variable-length textual data.

Numerical blockchain metrics should use numerical data types rather than `VARCHAR`.

---

## 2. Proposed Database Table

```sql
CREATE TABLE mempool_analysis (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME NOT NULL,
    network VARCHAR(20) NOT NULL,
    transaction_count BIGINT,
    mempool_size BIGINT,
    congestion_score DECIMAL(5,2),
    congestion_level VARCHAR(20),
    congestion_status VARCHAR(50),
    fee_priority VARCHAR(30),
    intelligence_signal VARCHAR(255),
    summary VARCHAR(500)
);
```

---

## 3. Column Specification

| Column                | Data Type | Size | Description                   |
| --------------------- | --------- | ---: | ----------------------------- |
| `id`                  | BIGINT    |    — | Unique record identifier      |
| `timestamp`           | DATETIME  |    — | Date/time of data collection  |
| `network`             | VARCHAR   |   20 | Bitcoin network identifier    |
| `transaction_count`   | BIGINT    |    — | Number of transactions        |
| `mempool_size`        | BIGINT    |    — | Mempool size in bytes         |
| `congestion_score`    | DECIMAL   |  5,2 | Calculated congestion score   |
| `congestion_level`    | VARCHAR   |   20 | Congestion classification     |
| `congestion_status`   | VARCHAR   |   50 | Human-readable network status |
| `fee_priority`        | VARCHAR   |   30 | Fee priority classification   |
| `intelligence_signal` | VARCHAR   |  255 | Important network signal      |
| `summary`             | VARCHAR   |  500 | Network condition summary     |

---

## 4. VARCHAR Fields

### `network`

```sql
network VARCHAR(20)
```

Example values:

```text
bitcoin
testnet
signet
```

Maximum length: **20 characters**

---

### `congestion_level`

```sql
congestion_level VARCHAR(20)
```

Example values:

```text
Low
Moderate
High
Critical
```

Maximum length: **20 characters**

---

### `congestion_status`

```sql
congestion_status VARCHAR(50)
```

Example:

```text
Elevated network congestion
```

Maximum length: **50 characters**

---

### `fee_priority`

```sql
fee_priority VARCHAR(30)
```

Example values:

```text
Low
Normal
High
Urgent
```

Maximum length: **30 characters**

---

### `intelligence_signal`

```sql
intelligence_signal VARCHAR(255)
```

Example:

```text
Increased transaction pressure detected
```

Maximum length: **255 characters**

---

### `summary`

```sql
summary VARCHAR(500)
```

Example:

```text
Bitcoin mempool activity is currently elevated with increased transaction pressure.
```

Maximum length: **500 characters**

---

## 5. Recommended Data Types

Not every field should use `VARCHAR`.

| Data                | Recommended Type | Reason                   |
| ------------------- | ---------------- | ------------------------ |
| Record ID           | BIGINT           | Large numeric identifier |
| Timestamp           | DATETIME         | Date/time storage        |
| Transaction Count   | BIGINT           | Numeric calculation      |
| Mempool Size        | BIGINT           | Large numeric value      |
| Congestion Score    | DECIMAL(5,2)     | Precise numerical score  |
| Network             | VARCHAR(20)      | Short text               |
| Congestion Level    | VARCHAR(20)      | Classification text      |
| Congestion Status   | VARCHAR(50)      | Status description       |
| Fee Priority        | VARCHAR(30)      | Priority classification  |
| Intelligence Signal | VARCHAR(255)     | Short analytical message |
| Summary             | VARCHAR(500)     | Human-readable summary   |

---

## 6. Example Insert

```sql
INSERT INTO mempool_analysis (
    timestamp,
    network,
    transaction_count,
    mempool_size,
    congestion_score,
    congestion_level,
    congestion_status,
    fee_priority,
    intelligence_signal,
    summary
)
VALUES (
    '2026-08-14 22:30:00',
    'bitcoin',
    125430,
    245000000,
    72.50,
    'High',
    'Elevated network congestion',
    'High',
    'Increased transaction pressure detected',
    'Bitcoin mempool activity is currently elevated.'
);
```

---

## 7. VARCHAR Validation

Application-level validation should ensure that text does not exceed the defined database limits.

| Field                 | Maximum Length |
| --------------------- | -------------: |
| `network`             |             20 |
| `congestion_level`    |             20 |
| `congestion_status`   |             50 |
| `fee_priority`        |             30 |
| `intelligence_signal` |            255 |
| `summary`             |            500 |

---

## 8. Validation Rules

Before inserting data into the database:

* Remove unnecessary leading/trailing whitespace.
* Validate required fields.
* Validate maximum string length.
* Validate numerical fields separately.
* Reject invalid or malformed values.
* Handle `NULL` values according to application requirements.
* Use parameterized SQL queries.

---

## 9. Database Design Principle

The project follows the principle:

```text
Text Data
    ↓
VARCHAR / TEXT

Numeric Data
    ↓
INT / BIGINT / DECIMAL / FLOAT

Date & Time
    ↓
DATETIME
```

This prevents numerical blockchain metrics from being incorrectly stored as strings and allows efficient filtering, sorting, aggregation, and analysis.

---

## 10. Future Database Expansion

Future versions may add tables for:

* Historical mempool records
* Fee-rate history
* Block history
* Congestion history
* Network alerts
* User-defined monitoring rules

A possible future relationship could be:

```text
Mempool Analysis
       │
       ├── Congestion History
       │
       ├── Fee History
       │
       ├── Block History
       │
       └── Network Alerts
```

---

## 11. Database Documentation Status

```text
Database Schema:     Defined
VARCHAR Fields:      Defined
Numeric Fields:      Defined
Validation Rules:    Defined
UAT Integration:     Ready
```
