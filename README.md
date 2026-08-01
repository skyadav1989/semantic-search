# 🚀 Semantic Product Search Engine

An AI-powered product search and shopping assistant built with
**FastAPI**, **Qdrant**, **BGE-M3**, and **Gemini**.

## Features

-   Semantic Search
-   Hybrid Search (Vector + BM25)
-   Query Understanding
-   Metadata Filtering
-   Faceted Search
-   Business Ranking
-   AI Chat (`/chat`)
-   Shopping Agent (`/agent/chat`)
-   Knowledge Base (YAML)
-   FAQ Retrieval
-   Recommendation Engine
-   FastAPI REST APIs

## Architecture

``` text
User
 │
 ▼
FastAPI
 │
 ▼
Search Service
 │
 ├── Query Processing
 ├── Hybrid Retrieval
 ├── Reranking
 ├── Business Ranking
 └── LLM Response
```

## Agent Flow

``` text
User
 │
 ▼
Planner
 │
 ▼
Tool Executor
 │
 ▼
FAQ / Search / Recommendation
 │
 ▼
Prompt Builder
 │
 ▼
Gemini
 │
 ▼
Response
```

## Knowledge

Location:

``` text
app/knowledge/v1/
```

Main files: - taxonomy.yaml - synonyms.yaml - technical_specs.yaml -
feature_benefits.yaml - use_cases.yaml

## APIs

-   `GET /search`
-   `POST /chat`
-   `POST /agent/chat`

## Tech Stack

-   Python 3.12+
-   FastAPI
-   Qdrant
-   BGE-M3
-   Sentence Transformers
-   CrossEncoder
-   Gemini
-   Pydantic

## Project Structure

``` text
app/
├── agent/
├── api/
├── bootstrap/
├── embedding/
├── facets/
├── knowledge/
├── llm/
├── recommendation/
├── search/
└── services/
```

## Completed

-   Semantic Search
-   Hybrid Search
-   BM25 + RRF
-   CrossEncoder Reranking
-   Business Ranking
-   Recommendation Engine
-   Faceted Search
-   Knowledge Registry
-   FAQ Tool
-   AI Chat
-   Shopping Agent Framework

## Next

-   Multi-step Reasoning
-   Conversation Memory
-   Catalog Tool
-   Search Tool
-   Recommendation Tool
-   Semantic Knowledge Search
-   Explain Recommendations
-   Evaluation Framework
-   Analytics Dashboard

## License

MIT
