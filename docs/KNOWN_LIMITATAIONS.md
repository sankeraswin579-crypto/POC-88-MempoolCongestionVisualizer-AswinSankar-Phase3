# Known Limitations

## POC-88 — Mempool Congestion Visualizer

## 1. Session-Based Congestion History

The current congestion trend is stored in React frontend state.

This means the trend history exists only during the active browser session.

If the user performs a full page reload, the collected congestion observations are cleared.

### Current Behavior

```text
Live Observation
      ↓
React State
      ↓
Previous Observation
      ↓
Trend Calculation