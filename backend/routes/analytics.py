from pathlib import Path
import json

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


@router.get("/phase3-intelligence")
def phase3_intelligence():

    try:

        project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        output_path = (
            project_root
            / "data-science"
            / "outputs"
            / "intelligence_results.json"
        )

        if not output_path.exists():

            raise HTTPException(
                status_code=404,
                detail=(
                    "Approved Phase 3 intelligence output "
                    "was not found."
                )
            )

        with output_path.open(
            "r",
            encoding="utf-8"
        ) as output_file:

            results = json.load(
                output_file
            )

        if (
            results.get("primary_track")
            != "Track A — Comparative"
        ):

            raise HTTPException(
                status_code=500,
                detail=(
                    "Phase 3 intelligence output does not "
                    "match the approved Track A — Comparative track."
                )
            )

        return results

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
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
