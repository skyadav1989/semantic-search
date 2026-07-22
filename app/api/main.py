from __future__ import annotations

import logging
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.bootstrap.container import container

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