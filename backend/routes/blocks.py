from fastapi import APIRouter, HTTPException

from services.mempool_service import MempoolService


router = APIRouter(
    prefix="/api/blocks",
    tags=["Blocks"],
)

mempool_service = MempoolService()


@router.get("/")
def recent_blocks():
    try:
        return {
            "data": mempool_service.get_blocks()
        }
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/tip")
def block_tip():
    try:
        return {
            "height": mempool_service.get_block_height()
        }
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/{height}")
def block_by_height(height: int):
    try:
        return {
            "data": mempool_service.get_blocks(
                start_height=height
            )
        }
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )