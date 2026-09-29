from fastapi import APIRouter, HTTPException

from services.mempool_service import MempoolService


router = APIRouter(
    prefix="/api/fees",
    tags=["Fees"],
)

mempool_service = MempoolService()


@router.get("/buckets")
def fee_buckets():
    try:
        fees = mempool_service.get_recommended_fees()

        return {
            "fastest": fees.get("fastestFee", 0),
            "half_hour": fees.get("halfHourFee", 0),
            "hour": fees.get("hourFee", 0),
            "economy": fees.get("economyFee", 0),
            "minimum": fees.get("minimumFee", 0),
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )