from fastapi import (
    APIRouter,
    HTTPException
)

from services.mempool_service import (
    MempoolService
)

from services.fee_service import (
    FeeService
)

from services.intelligence_service import (
    IntelligenceService
)


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


mempool_service = (
    MempoolService()
)

fee_service = (
    FeeService()
)

intelligence_service = (
    IntelligenceService()
)


@router.get("/dashboard")
def dashboard():

    try:

        mempool = (
            mempool_service
            .get_mempool()
        )

        fees = (
            fee_service
            .get_fees()
        )

        return {

            "mempool": mempool,

            "fees": fees
        }

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/intelligence")
def intelligence():

    try:

        return (
            intelligence_service
            .generate_insight()
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/summary")
def summary():

    try:

        congestion = (
            intelligence_service
            .generate_insight()
        )

        return {

            "congestion":
                congestion[
                    "congestion_level"
                ],

            "score":
                congestion[
                    "congestion_score"
                ],

            "recommendation":
                congestion[
                    "recommendation"
                ]
        }

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )