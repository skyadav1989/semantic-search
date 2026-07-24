# AGENTS.md

## Purpose

This file helps AI coding agents understand the `semantic-engine` repository quickly and act consistently.

## Project overview

- Python-based semantic search and recommendation engine.
- FastAPI REST API exposed from `app/api/main.py`.
- Qdrant vector database stores semantic product vectors.
- BGE-M3 embeddings and CrossEncoder reranking are the main ranking components.
- The search workflow is implemented by `app/services/search_service.py` and wired in `app/bootstrap/container.py`.

## Key components

- `app/api/main.py`
  - FastAPI application entrypoint.
  - Health and `/search` API.
- `app/bootstrap/container.py`
  - Central dependency container.
  - Loads environment variables and constructs Qdrant, embedder, search components, and registry.
- `app/services/search_service.py`
  - Orchestrates query processing, expansion, embedding, retrieval, reranking, and business ranking.
- `app/embedding/`
  - Embedding and Qdrant collection handling.
- `app/search/`
  - Query processing, filtering, retrieval, reranking, and ranking logic.
- `knowledge/v1`
  - Knowledge registry data used for query understanding and product enrichment.

## Important runtime details

- Default Qdrant collection: `products`.
- Environment variables:
  - `QDRANT_URL` (default: `http://localhost:6333`)
  - `QDRANT_API_KEY`
  - `QDRANT_COLLECTION` (default: `products`)
  - `EMBEDDING_MODEL` (default: `BAAI/bge-m3`)
  - `EMBEDDING_DEVICE` (default: `cpu`)
  - `ENABLE_RERANKER` (`true` / `false`)
- Search behavior is hybrid by default using semantic retrieval and optional reranking.

## Recommended commands

- Start local development with Qdrant and API:
  - `docker-compose up --build`
- Run the API directly:
  - `uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000`
- Run tests:
  - `python -m pytest`
- Initialize Qdrant collection when Qdrant is available:
  - `python create_qdrant_database.py`

## Agent guidance

- Prefer changes that preserve the existing search pipeline and component boundaries.
- Avoid adding undocumented external services or frontend assumptions.
- Use `README.md` for feature and architecture summaries; do not duplicate its content verbatim.
- Validate behavior through tests in `tests/` and existing root-level test files.
- When modifying search flow, verify Qdrant filter and rerank components because correct payload and collection settings are critical.

## Notes for AI agents

- This repository has no existing `.github/copilot-instructions.md` or `AGENTS.md` file.
- `README.md` is the primary project documentation.
- The `docs/` folder is empty, so keep instructions concise and link to the README when needed.
