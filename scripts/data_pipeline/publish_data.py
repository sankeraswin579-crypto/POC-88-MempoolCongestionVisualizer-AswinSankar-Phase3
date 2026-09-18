from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

SOURCE = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUTPUT = ROOT / "data" / "published" / "intelligence_data.json"


def reject_json_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Canonical dataset not found: {SOURCE}"
        )

    df = pd.read_csv(SOURCE)

    # Convert pandas missing values to JSON null.
    records = json.loads(
        df.to_json(
            orient="records",
            force_ascii=False,
            date_format="iso",
        )
    )

    # Final strict JSON serialization.
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(
            records,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ),
        encoding="utf-8",
    )

    # Read the generated file again using a strict JSON parser.
    json.loads(
        OUTPUT.read_text(encoding="utf-8"),
        parse_constant=reject_json_constant,
    )

    print(f"Published {len(records)} records to {OUTPUT}")
    print("Strict JSON validation: PASS")


if __name__ == "__main__":
    main()