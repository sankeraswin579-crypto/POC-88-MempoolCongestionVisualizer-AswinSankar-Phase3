import json
import os
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv


load_dotenv()


BASE_URL = os.getenv(
    "MEMPOOL_API_URL",
    "https://mempool.space/api"
)

DATA_DIR = "data"


def fetch(
    endpoint: str
):

    url = (
        f"{BASE_URL}"
        f"{endpoint}"
    )

    response = requests.get(
        url,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


def save_json(
    filename: str,
    data
):

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    filepath = os.path.join(
        DATA_DIR,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2
        )

    print(
        f"Saved: {filepath}"
    )


def main():

    print(
        "Fetching Mempool.space data..."
    )

    mempool = fetch(
        "/mempool"
    )

    fees = fetch(
        "/v1/fees/recommended"
    )

    blocks = fetch(
        "/blocks"
    )

    save_json(
        "sample_mempool.json",
        mempool
    )

    save_json(
        "sample_fees.json",
        fees
    )

    save_json(
        "sample_blocks.json",
        blocks
    )

    print(
        "Data fetch completed successfully."
    )

    print(
        "Timestamp:",
        datetime.now(
            timezone.utc
        ).isoformat()
    )


if __name__ == "__main__":

    main()