import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class MempoolService:
    def __init__(self):
        self.base_url = os.getenv(
            "MEMPOOL_API_URL",
            "https://mempool.space/api"
        ).rstrip("/")

        # Keep requests from hanging indefinitely.
        self.connect_timeout = int(
            os.getenv("MEMPOOL_CONNECT_TIMEOUT", "5")
        )
        self.read_timeout = int(
            os.getenv("MEMPOOL_READ_TIMEOUT", "10")
        )

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "POC-88-Mempool-Congestion-Visualizer/1.0",
            "Accept": "application/json",
        })

    def get(self, endpoint: str) -> Any:
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.get(
                url,
                timeout=(
                    self.connect_timeout,
                    self.read_timeout
                )
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.Timeout as error:
            raise RuntimeError(
                f"Mempool API timeout: {url}"
            ) from error

        except requests.exceptions.ConnectionError as error:
            raise RuntimeError(
                f"Could not connect to Mempool API: {url}"
            ) from error

        except requests.exceptions.HTTPError as error:
            status = (
                error.response.status_code
                if error.response is not None
                else "unknown"
            )

            raise RuntimeError(
                f"Mempool API returned HTTP {status}: {url}"
            ) from error

        except requests.exceptions.RequestException as error:
            raise RuntimeError(
                f"Mempool API request failed: {error}"
            ) from error

        except ValueError as error:
            raise RuntimeError(
                f"Mempool API returned invalid JSON: {url}"
            ) from error

    def get_mempool(self):
        return self.get("/mempool")

    def get_recent_transactions(self):
        return self.get("/mempool/recent")

    def get_recommended_fees(self):
        return self.get("/v1/fees/recommended")

    def get_precise_fees(self):
        return self.get("/v1/fees/precise")

    def get_mempool_blocks(self):
        return self.get("/v1/fees/mempool-blocks")

    def get_blocks(self, start_height=None):
        if start_height is not None:
            return self.get(f"/blocks/{start_height}")

        return self.get("/blocks")

    def get_block_height(self):
        return self.get("/blocks/tip/height")

    def get_block_hash(self):
        return self.get("/blocks/tip/hash")

    def get_transaction(self, txid: str):
        return self.get(f"/tx/{txid}")

    def get_transaction_status(self, txid: str):
        return self.get(f"/tx/{txid}/status")