from services.congestion_service import (
    CongestionService
)

from services.fee_service import (
    FeeService
)


class IntelligenceService:

    def __init__(self):

        self.congestion_service = (
            CongestionService()
        )

        self.fee_service = (
            FeeService()
        )

    def generate_insight(self):

        congestion = (
            self.congestion_service
            .get_congestion()
        )

        fees = (
            self.fee_service
            .get_fees()
        )

        level = congestion[
            "level"
        ]

        score = congestion[
            "score"
        ]

        fastest = fees[
            "fastest"
        ]

        economy = fees[
            "economy"
        ]

        if level == "Critical":

            recommendation = (
                "Network congestion is very high. "
                "Use a competitive fee rate if fast "
                "confirmation is important."
            )

        elif level == "High":

            recommendation = (
                "Transaction demand is elevated. "
                "Consider using the recommended fee "
                "rate for timely confirmation."
            )

        elif level == "Moderate":

            recommendation = (
                "The network has moderate activity. "
                "Standard fee rates should generally "
                "be sufficient."
            )

        else:

            recommendation = (
                "The mempool is relatively clear. "
                "Economy fee rates may be sufficient "
                "if confirmation time is flexible."
            )

        return {

            "congestion_level":
                level,

            "congestion_score":
                score,

            "fastest_fee":
                fastest,

            "economy_fee":
                economy,

            "recommendation":
                recommendation
        }

    def get_explanation(self):

        data = self.generate_insight()

        return {

            "title":
                "Mempool Intelligence",

            "summary":
                (
                    f"Current congestion is "
                    f"{data['congestion_level']} "
                    f"with a score of "
                    f"{data['congestion_score']}/100."
                ),

            "recommendation":
                data["recommendation"]
        }