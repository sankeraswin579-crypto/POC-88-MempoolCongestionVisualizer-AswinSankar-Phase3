# AI / Intelligence Data Summary

## Project

**POC-88 — Mempool Congestion Visualizer**

## Purpose

The intelligence layer converts live Bitcoin network metrics into contextual explanations that are easier to understand than raw blockchain data.

The system separates deterministic analytics from user-facing intelligence.

---

## Intelligence Inputs

The intelligence layer uses:

- Pending transaction count
- Mempool virtual size
- Congestion score
- Congestion level
- Recommended fee rates
- Economy fee
- Fast confirmation fee
- Memory usage
- Recent block activity
- Current congestion trend

---

## Deterministic Analytics

Core network calculations are deterministic.

Examples include:

```text
Transaction Count
        ↓
Mempool Size
        ↓
Congestion Score
        ↓
Congestion Level
        ↓
Fee Pressure
        ↓
Congestion Trend