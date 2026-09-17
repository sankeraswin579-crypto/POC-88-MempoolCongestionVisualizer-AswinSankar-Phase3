# POC-88 — Data Source Inventory

## Project
POC-88 Mempool Congestion Visualizer

## Existing Application Data Flow

The existing application obtains Bitcoin mempool-related data through the
Mempool API and processes it through the backend service layer.

### Sources

| Source | Type | Access Method | Current Usage | Sensitivity | Phase 3 Decision |
|---|---|---|---|---|---|
| mempool.space mempool endpoint | Public API / JSON | Existing backend API flow | Mempool statistics | Public | Use after local capture |
| mempool.space recommended fees | Public API / JSON | Existing backend API flow | Fee metrics | Public | Use after local capture |
| mempool.space blocks endpoint | Public API / JSON | Existing backend API flow | Recent block metrics | Public | Use after local capture |

## Local Source Snapshots

- backend/data/sample_mempool.json
- backend/data/sample_fees.json
- backend/data/sample_blocks.json

These local snapshots provide a stable input for reproducible Phase 3
processing instead of requiring a live API for every processing run.

## Selected Phase 3 Source

The selected Phase 3 source is the captured local source package generated
from the existing POC-88 Mempool API data flow.

## Data Characteristics

### Mempool
Contains current snapshot metrics including:
- transaction count
- virtual size
- total fee
- fee histogram

### Fees
Contains:
- fastest fee
- half-hour fee
- hour fee
- economy fee
- minimum fee

### Blocks
Contains recent block observations including:
- block ID
- block height
- timestamp
- transaction count
- block size
- block weight
- difficulty
- additional blockchain metadata

## Data Risks

- Live API responses may change between runs.
- The captured package represents a point-in-time source snapshot.
- The mempool fee histogram is not expanded into individual canonical
  records in this first package.
- The canonical package must remain within the program size limits.

## Licensing / Access Notes

The data is obtained from a public API used by the existing application.
Only the supplied/captured source data is used for this Phase 3 package.
