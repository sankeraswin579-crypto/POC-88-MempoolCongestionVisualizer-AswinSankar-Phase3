from pathlib import Path
import json
import csv
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "backend" / "data"
OUTPUT = ROOT / "data" / "source-sample" / "source_sample.csv"

MEMPOOL_FILE = SOURCE_DIR / "sample_mempool.json"
FEES_FILE = SOURCE_DIR / "sample_fees.json"
BLOCKS_FILE = SOURCE_DIR / "sample_blocks.json"

def read_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)

def iso_from_unix(value):
    if value in (None, ""):
        return None
    return datetime.fromtimestamp(
        int(value), tz=timezone.utc
    ).isoformat().replace("+00:00", "Z")

captured_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

mempool = read_json(MEMPOOL_FILE)
fees = read_json(FEES_FILE)
blocks = read_json(BLOCKS_FILE)

rows = []

# Mempool snapshot metrics
mempool_metrics = [
    ("transaction_count", mempool.get("count"), "transactions"),
    ("virtual_size", mempool.get("vsize"), "vbytes"),
    ("total_fee", mempool.get("total_fee"), "sats"),
]

for metric_name, metric_value, metric_unit in mempool_metrics:
    rows.append({
        "source_group": "mempool",
        "observed_at": captured_at,
        "record_type": "measurement",
        "entity_id": "MEMPOOL-CURRENT",
        "entity_name": "Bitcoin Mempool",
        "category": "mempool",
        "subcategory": "current_snapshot",
        "status": "observed",
        "metric_name": metric_name,
        "metric_value": metric_value,
        "metric_unit": metric_unit,
        "source_name": "mempool.space",
        "source_record_id": "current",
        "is_synthetic": False,
    })

# Fee snapshot metrics
fee_metrics = [
    ("fastest_fee", fees.get("fastestFee"), "sat_vbyte"),
    ("half_hour_fee", fees.get("halfHourFee"), "sat_vbyte"),
    ("hour_fee", fees.get("hourFee"), "sat_vbyte"),
    ("economy_fee", fees.get("economyFee"), "sat_vbyte"),
    ("minimum_fee", fees.get("minimumFee"), "sat_vbyte"),
]

for metric_name, metric_value, metric_unit in fee_metrics:
    rows.append({
        "source_group": "fees",
        "observed_at": captured_at,
        "record_type": "measurement",
        "entity_id": "FEES-CURRENT",
        "entity_name": "Bitcoin Fee Estimates",
        "category": "fees",
        "subcategory": "recommended_rates",
        "status": "observed",
        "metric_name": metric_name,
        "metric_value": metric_value,
        "metric_unit": metric_unit,
        "source_name": "mempool.space",
        "source_record_id": "current",
        "is_synthetic": False,
    })

# Recent blocks
for block in blocks:
    block_id = block.get("id")
    timestamp = block.get("timestamp")

    block_metrics = [
        ("tx_count", block.get("tx_count"), "transactions"),
        ("size", block.get("size"), "bytes"),
        ("weight", block.get("weight"), "weight_units"),
        ("difficulty", block.get("difficulty"), "difficulty"),
    ]

    for metric_name, metric_value, metric_unit in block_metrics:
        rows.append({
            "source_group": "blocks",
            "observed_at": iso_from_unix(timestamp),
            "record_type": "measurement",
            "entity_id": block_id,
            "entity_name": f"Block {block.get('height')}",
            "category": "bitcoin_block",
            "subcategory": "recent_block",
            "status": "confirmed",
            "metric_name": metric_name,
            "metric_value": metric_value,
            "metric_unit": metric_unit,
            "source_name": "mempool.space",
            "source_record_id": block_id,
            "is_synthetic": False,
        })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "source_group",
    "observed_at",
    "record_type",
    "entity_id",
    "entity_name",
    "category",
    "subcategory",
    "status",
    "metric_name",
    "metric_value",
    "metric_unit",
    "source_name",
    "source_record_id",
    "is_synthetic",
]

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} source records to {OUTPUT}")


