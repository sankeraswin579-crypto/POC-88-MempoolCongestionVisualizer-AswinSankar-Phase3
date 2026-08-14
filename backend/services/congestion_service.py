from services.mempool_service import MempoolService

from utils.calculations import (
    calculate_congestion_score,
    calculate_mempool_usage,
    congestion_level
)


class CongestionService:

    def __init__(self):

        self.mempool_service = (
            MempoolService()
        )

    def get_congestion(self):

        mempool = (
            self.mempool_service
            .get_mempool()
        )

        tx_count = mempool.get(
            "count",
            0
        )

        vsize = mempool.get(
            "vsize",
            0
        )

        score = calculate_congestion_score(
            tx_count,
            vsize
        )

        usage = calculate_mempool_usage(
            vsize
        )

        level = congestion_level(
            score
        )

        return {

            "score": score,

            "level": level,

            "transaction_count":
                tx_count,

            "virtual_size":
                vsize,

            "memory_usage_percent":
                usage,

            "total_fee":
                mempool.get(
                    "total_fee",
                    0
                ),

            "mempool_min_fee":
                mempool.get(
                    "mempoolminfee",
                    0
                ),

            "incremental_relay_fee":
                mempool.get(
                    "incrementalrelayfee",
                    0
                )
        }

    def get_congestion_summary(self):

        data = self.get_congestion()

        return {

            "level":
                data["level"],

            "score":
                data["score"],

            "message":
                self._generate_message(
                    data["level"]
                )
        }

    def _generate_message(
        self,
        level: str
    ):

        messages = {

            "Low":
                "The Bitcoin mempool is relatively clear.",

            "Moderate":
                "The mempool has moderate transaction pressure.",

            "High":
                "The mempool is experiencing high transaction pressure.",

            "Critical":
                "The mempool is heavily congested."
        }

        return messages.get(
            level,
            "Mempool status unavailable."
        )