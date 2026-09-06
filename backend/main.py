from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.mempool import router as mempool_router
from routes.blocks import router as blocks_router
from routes.analytics import router as analytics_router


app = FastAPI(

    title="POC-88 Mempool Congestion Visualizer",

    description=(
        "Bitcoin mempool congestion analysis, "
        "fee intelligence, transaction activity "
        "and block analytics."
    ),

    version="1.0.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# ROUTES
# ==================================================

app.include_router(
    mempool_router
)

app.include_router(
    blocks_router
)

app.include_router(
    analytics_router
)


# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():

    return {

        "project":
            "POC-88 Mempool Congestion Visualizer",

        "status":
            "running",

        "version":
            "1.0.0",

        "docs":
            "/docs",

        "endpoints": {

            "mempool":
                "/api/mempool/",

            "congestion":
                "/api/mempool/congestion",

            "recent_transactions":
                "/api/mempool/recent",

            "projected_blocks":
                "/api/mempool/blocks",

            "blocks":
                "/api/blocks/",

            "block_tip":
                "/api/blocks/tip",

            "dashboard":
                "/api/analytics/dashboard",

            "intelligence":
                "/api/analytics/intelligence",

            "summary":
                "/api/analytics/summary"
        }
    }


# ==================================================
# HEALTH
# ==================================================

@app.get("/health")
def health():

    return {

        "status":
            "healthy",

        "service":
            "mempool-congestion-backend"
    }