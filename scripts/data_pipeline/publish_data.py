from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

SOURCE = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUTPUT = ROOT / "data" / "published" / "intelligence_data.json"

df = pd.read_csv(SOURCE)

records = (
    df.where(pd.notna(df), None)
      .to_dict(orient="records")
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

OUTPUT.write_text(
    json.dumps(
        records,
        ensure_ascii=False,
        separators=(",", ":")
    ),
    encoding="utf-8"
)

print(f"Published {len(records)} records to {OUTPUT}")
