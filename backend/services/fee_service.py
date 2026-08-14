from services.mempool_service import (
    MempoolService
)

from utils.calculations import (
    estimate_confirmation_time
)


class FeeService:

    def __init__(self):

        self.mempool_service = (
            MempoolService()
        )

    def get_fees(self):

        fees = (
            self.mempool_service
            .get_recommended_fees()
        )

        return {

            "fastest":
                fees.get(
                    "fastestFee",
                    0
                ),

            "half_hour":
                fees.get(
                    "halfHourFee",
                    0
                ),

            "hour":
                fees.get(
                    "hourFee",
                    0
                ),

            "economy":
                fees.get(
                    "economyFee",
                    0
                ),

            "minimum":
                fees.get(
                    "minimumFee",
                    0
                )
        }

    def get_fee_analysis(self):

        fees = self.get_fees()

        return {

            "recommended": fees,

            "estimates": {

                "fastest": {
                    "fee_rate":
                        fees["fastest"],

                    "confirmation":
                        estimate_confirmation_time(
                            fees["fastest"]
                        )
                },

                "standard": {
                    "fee_rate":
                        fees["half_hour"],

                    "confirmation":
                        estimate_confirmation_time(
                            fees["half_hour"]
                        )
                },

                "economy": {
                    "fee_rate":
                        fees["economy"],

                    "confirmation":
                        estimate_confirmation_time(
                            fees["economy"]
                        )
                }
            }
        }

    def get_precise_fees(self):

        return (
            self.mempool_service
            .get_precise_fees()
        )

    def get_projected_blocks(self):

        return (
            self.mempool_service
            .get_mempool_blocks()
        )