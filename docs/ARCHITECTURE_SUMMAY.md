# Architecture Summary

## POC-88 — Mempool Congestion Visualizer

## 1. System Overview

POC-88 is a real-time Bitcoin network analytics and intelligence dashboard.

The system retrieves live Bitcoin network information, processes deterministic metrics, and presents the results through an interactive intelligence-focused frontend.

The architecture separates:

- External blockchain data
- Backend API processing
- Deterministic analytics
- Frontend visualization
- Intelligence interpretation

---

## 2. High-Level Architecture

```text
┌──────────────────────────────┐
│       Mempool.space API      │
│                              │
│  Mempool / Fees / Blocks     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           FastAPI            │
│           Backend            │
│                              │
│  API / Data Processing       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│    Deterministic Analytics   │
│                              │
│ • Congestion Score           │
│ • Congestion Level           │
│ • Fee Analysis               │
│ • Network Metrics            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Next.js Frontend      │
│                              │
│ • Dashboard                  │
│ • KPIs                       │
│ • Charts                     │
│ • Recent Blocks              │
│ • Intelligence Panel         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Intelligence Layer      │
│                              │
│ • Why This Matters           │
│ • Fee Market Signal          │
│ • Intelligence Summary       │
│ • What To Watch              │
│ • Intelligence Questions     │
│ • Congestion Trend           │
└──────────────────────────────┘