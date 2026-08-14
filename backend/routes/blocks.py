from fastapi import (
    APIRouter,
    HTTPException
)

from services.mempool_service import (
    MempoolService
)

from services.congestion_service import (
    CongestionService
)


router = APIRouter(
    prefix="/api/mempool",
    tags=["Mempool"]
)


mempool_service = (
    MempoolService()
)

congestion_service = (
    CongestionService()
)


@router.get("/")
def mempool():

    try:

        return mempool_service.get_mempool()

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=f"Mempool API error: {error}"
        )


@router.get("/congestion")
def congestion():

    try:

        return (
            congestion_service
            .get_congestion()
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/recent")
def recent_transactions():

    try:

        return {
            "data":
                mempool_service
                .get_recent_transactions()
        }

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/blocks")
def projected_blocks():

    try:

        return {
            "data":
                mempool_service
                .get_mempool_blocks()
        }

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )