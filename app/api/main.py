from __future__ import annotations

import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi import Path as ApiPath
from app.chat.models import ChatRequest


from app.bootstrap.container import container
from app.agent.models import AgentRequest


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Semantic Engine",
    version="1.0.0",
    description="Semantic Product Search API",
)

# Enable CORS for external & local web frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def root():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "application": "Semantic Engine",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/chatui")
def chat_ui():
    chat_file = STATIC_DIR / "chatui.html"
    if chat_file.exists():
        return FileResponse(str(chat_file))
    raise HTTPException(
        status_code=404,
        detail="chatui.html not found",
    )


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "qdrant_collection": container.collection_name,
        "embedding_model": container.embedding_model,
    }


@app.get("/search")
def search(
    q: str = Query(
        ...,
        min_length=2,
        description="Search query",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
):

    try:

        return container.search_service.search(
            query=q,
            limit=limit,
        )

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

# ---------------------------------------------------------
# Recommendations
# ---------------------------------------------------------


@app.get("/recommendations/similar/{sku}")
def similar_products(
    sku: str = ApiPath(..., description="Product SKU"),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
):

    try:

        return container.recommendation_service.similar(
            sku=sku,
            limit=limit,
        )

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@app.get("/recommendations/alternatives/{sku}")
def alternative_products(
    sku: str = ApiPath(..., description="Product SKU"),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
):

    try:

        return container.recommendation_service.alternatives(
            sku=sku,
            limit=limit,
        )

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@app.get("/recommendations/complementary/{sku}")
def complementary_products(
    sku: str = ApiPath(..., description="Product SKU"),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
):

    try:

        return container.recommendation_service.complementary(
            sku=sku,
            limit=limit,
        )

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@app.get("/recommendations/trending/{sku}")
def trending_products(
    sku: str = ApiPath(..., description="Product SKU"),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
):

    try:

        return container.recommendation_service.trending(
            sku=sku,
            limit=limit,
        )

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# ---------------------------------------------------------
# Product Details Page (PDP) Route
# ---------------------------------------------------------


@app.get("/pdp/{sku}")
def pdp_page(
    request: Request,
    sku: str = ApiPath(..., description="Product SKU"),
    format: str | None = Query(None, description="Response format: 'json' or empty for HTML/API content-negotiation"),
):
    """
    PDP route.
    Returns HTML for browser navigation or complete product details + recommendations JSON when format=json or Accept: application/json.
    """
    accept = request.headers.get("accept", "")
    if format != "json" and "text/html" in accept:
        index_file = STATIC_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))

    return get_pdp_data(sku)


@app.get("/api/pdp/{sku}")
def get_pdp_data(
    sku: str = ApiPath(..., description="Product SKU"),
):
    """
    Returns complete product details along with similar, trending, and complementary recommendations for a SKU.
    """
    try:
        product_item = container.retriever.get_by_sku(sku)
        product_payload = product_item["payload"] if product_item and "payload" in product_item else None

        if not product_item and not product_payload:
            # Fallback placeholder if Qdrant isn't loaded or product doesn't exist
            product_payload = {"sku": sku, "title": sku, "category": "Product"}

        # Gather recommendations concurrently/sequentially
        similar = []
        trending = []
        complementary = []

        try:
            similar = container.recommendation_service.similar(sku=sku, limit=10)
        except Exception as err:
            logger.warning("Error loading similar recommendations for SKU %s: %s", sku, err)

        try:
            trending = container.recommendation_service.trending(sku=sku, limit=10)
        except Exception as err:
            logger.warning("Error loading trending recommendations for SKU %s: %s", sku, err)

        try:
            complementary = container.recommendation_service.complementary(sku=sku, limit=10)
        except Exception as err:
            logger.warning("Error loading complementary recommendations for SKU %s: %s", sku, err)

        return {
            "sku": sku,
            "product": product_payload,
            "recommendations": {
                "similar": similar,
                "trending": trending,
                "complementary": complementary,
            },
        }

    except Exception as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

@app.post("/chat")
def chat(
    body: dict = Body(...),
):
    """
    AI Shopping Assistant
    """

    try:

        query = body.get("query")

        if not query:

            raise HTTPException(
                status_code=400,
                detail="query is required",
            )

        limit = body.get("limit", 10)

        return container.search_service.chat(
            query=query,
            limit=limit,
        )

    except HTTPException:
        raise

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )




@app.post("/chat/v2")
def chat_v2(
    request: ChatRequest,
):
    """
    Conversational Shopping Assistant
    """

    try:

        return container.chat_service.chat(
            request,
        )

    except HTTPException:
        raise

    except Exception as exc:

        logger.exception(exc)

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

@app.get("/chat/v2/session/{session_id}")
def chat_session(session_id: str):

    return container.chat_service.session(
        session_id,
    )

@app.delete("/chat/v2/session/{session_id}")
def clear_chat(session_id: str):

    container.chat_service.clear(
        session_id,
    )

    return {
        "success": True,
    }

@app.post("/agent/chat")
def agent_chat(
    request: AgentRequest,
):
    return container.shopping_agent.chat(request)