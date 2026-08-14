# POC-88 — Mempool Congestion Visualizer

## Real-Time Bitcoin Network Congestion Intelligence Dashboard

POC-88 is a real-time Bitcoin network analytics and intelligence dashboard that transforms live mempool, fee-market, congestion, and block data into an interactive command-center interface.

The project goes beyond displaying raw Bitcoin statistics by providing contextual intelligence about:

- Current network congestion
- Mempool pressure
- Fee-market conditions
- Congestion trends
- Recent Bitcoin blocks
- Network signals users should monitor

---

## Project Information

| Field | Details |
|---|---|
| POC ID | POC-88 |
| Project | Mempool Congestion Visualizer |
| Network | Bitcoin Mainnet |
| Category | Blockchain Analytics / Intelligence Dashboard |
| Frontend | Next.js, React, TypeScript |
| Styling | Tailwind CSS |
| Visualization | Recharts |
| Animation | Framer Motion |
| Backend | FastAPI / Python |
| Primary Data Source | Mempool.space |
| Developer | Aswin Sankar P.S |

---

# 1. Problem Statement

Bitcoin transactions compete for limited block space.

When network activity increases:

- Pending transactions can accumulate.
- Fee competition can increase.
- Lower-fee transactions may take longer to confirm.
- Users need better visibility into current network conditions.

Raw blockchain APIs provide the data, but users still need to understand what those numbers mean.

POC-88 addresses this by converting live Bitcoin network data into an understandable analytics and intelligence dashboard.

---

# 2. Project Objective

The main objective is to answer:

> **What is happening in the Bitcoin mempool, why does it matter, and what should users watch next?**

The dashboard provides:

- Real-time mempool monitoring
- Congestion scoring
- Fee-market analysis
- Congestion trend detection
- Recent block monitoring
- Contextual network intelligence
- Interactive intelligence questions
- Manual and automatic refresh

---

# 3. Key Features

## 3.1 Real-Time Mempool Monitoring

The dashboard displays live network metrics including:

- Pending transactions
- Mempool size
- Total mempool fees
- Memory usage
- Fee distribution
- Network status

---

## 3.2 Congestion Score

The application represents network pressure using a 0–100 congestion score.

### Congestion Classification

| Score | Level |
|---:|---|
| 0–29 | Low |
| 30–59 | Moderate |
| 60–79 | High |
| 80–100 | Critical |

The score provides a simple representation of current Bitcoin mempool pressure.

---

## 3.3 Congestion Trend

POC-88 records actual congestion observations during the active browser session.

Each observation contains:

```text
score
timestamp