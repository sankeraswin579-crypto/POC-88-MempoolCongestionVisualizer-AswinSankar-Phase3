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
        )

        self.timeout = int(
            os.getenv(
                "REQUEST_TIMEOUT",
                "20"
            )
        )

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent":
                "POC-88-Mempool-Congestion-Visualizer/1.0"
        })

    def get(
        self,
        endpoint: str
    ) -> Any:

        url = (
            f"{self.base_url}"
            f"{endpoint}"
        )

        response = self.session.get(
            url,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json()

    # ------------------------------------------
    # Current mempool
    # ------------------------------------------

    def get_mempool(self):

        return self.get(
            "/mempool"
        )

    # ------------------------------------------
    # Recent transactions
    # ------------------------------------------

    def get_recent_transactions(self):

        return self.get(
            "/mempool/recent"
        )

    # ------------------------------------------
    # Recommended fees
    # ------------------------------------------

    def get_recommended_fees(self):

        return self.get(
            "/v1/fees/recommended"
        )

    # ------------------------------------------
    # Precise fees
    # ------------------------------------------

    def get_precise_fees(self):

        return self.get(
            "/v1/fees/precise"
        )

    # ------------------------------------------
    # Projected mempool blocks
    # ------------------------------------------

    def get_mempool_blocks(self):

        return self.get(
            "/v1/fees/mempool-blocks"
        )

    # ------------------------------------------
    # Recent blocks
    # ------------------------------------------

    def get_blocks(
        self,
        start_height=None
    ):

        if start_height:

            return self.get(
                f"/blocks/{start_height}"
            )

        return self.get(
            "/blocks"
        )

    # ------------------------------------------
    # Current block height
    # ------------------------------------------

    def get_block_height(self):

        return self.get(
            "/blocks/tip/height"
        )

    # ------------------------------------------
    # Current block hash
    # ------------------------------------------

    def get_block_hash(self):

        return self.get(
            "/blocks/tip/hash"
        )

    # ------------------------------------------
    # Transaction
    # ------------------------------------------

    def get_transaction(
        self,
        txid: str
    ):

        return self.get(
            f"/tx/{txid}"
        )

    # ------------------------------------------
    # Transaction status
    # ------------------------------------------

    def get_transaction_status(
        self,
        txid: str
    ):

        return self.get(
            f"/tx/{txid}/status"
        )