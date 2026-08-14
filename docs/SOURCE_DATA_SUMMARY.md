# Source Data Summary

## POC-88 — Mempool Congestion Visualizer

## 1. Overview

POC-88 uses live Bitcoin network information to provide real-time mempool, fee-market, congestion, and recent-block analytics.

The primary external data source is:

**Mempool.space**

The application processes the retrieved data and presents it through the Next.js dashboard.

---

## 2. Primary Data Source

### Mempool.space

Mempool.space provides publicly accessible Bitcoin network information used by the project.

The project uses network data related to:

- Mempool activity
- Transaction fees
- Fee distribution
- Recent Bitcoin blocks

---

## 3. Mempool Data

The dashboard uses mempool information including:

- Pending transaction count
- Virtual transaction size
- Total mempool fees
- Fee histogram
- Minimum relay fee
- Incremental relay fee

These values provide the primary inputs for understanding current mempool activity.

---

## 4. Fee Data

The dashboard displays recommended Bitcoin transaction fee levels.

The fee categories include:

```text
Fastest
30 Minutes
1 Hour
Economy
Minimum