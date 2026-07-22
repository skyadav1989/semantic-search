# 🚀 Semantic Product Search Engine

An AI-powered Semantic Product Search Engine built using **FastAPI**, **Qdrant**, **BGE-M3**, and **CrossEncoder Reranking**. The engine understands user intent, performs semantic retrieval, applies metadata filters, and returns highly relevant product recommendations.

---

## ✨ Features

### 🔍 Semantic Search
- BGE-M3 sentence embeddings
- Semantic similarity search using Qdrant
- Natural language query support

### 🧠 Query Understanding
- Query Normalization
- Query Expansion
- Intent Detection
- Attribute Extraction

### 🎯 Metadata Filtering
- Price Filter
- Color Filter
- Category Filter (Ready)
- Brand Filter (Ready)

Example:

```
ceiling fans below 5000
```

↓

```
Price <= 5000
Category = Ceiling Fans
```

---

## 🏆 Intelligent Ranking

Search Results are ranked using multiple stages.

```
User Query
      │
      ▼
Query Processor
      │
      ▼
Query Expansion
      │
      ▼
Metadata Filters
      │
      ▼
BGE-M3 Embedding
      │
      ▼
Qdrant Vector Search
      │
      ▼
CrossEncoder Reranking
      │
      ▼
Business Ranking
      │
      ▼
Final Results
```

---

## 📦 Product Intelligence

During indexing every product is enriched with

- Keywords
- Benefits
- Use Cases
- Search Document
- Technical Document

This significantly improves semantic retrieval quality.

---

## 📂 Rich Product Indexing

Each indexed product stores

- SKU
- Product Title
- Category
- Subcategory
- Price
- MRP
- Product URL
- Product Image
- Brand
- Stock Status
- Keywords
- Benefits
- Use Cases
- Search Document
- Technical Document

---

## 🏗 Architecture

```
                 User
                  │
                  ▼
           FastAPI REST API
                  │
                  ▼
           Search Service
                  │
      ┌───────────┴────────────┐
      │                        │
Query Processor         Query Expander
      │                        │
      └───────────┬────────────┘
                  │
         Metadata Filter Builder
                  │
                  ▼
          BGE-M3 Embedder
                  │
                  ▼
          Qdrant Vector DB
                  │
                  ▼
     CrossEncoder Reranker
                  │
                  ▼
        Business Ranker
                  │
                  ▼
            JSON Response
```

---

## 📁 Project Structure

```
app/
│
├── api/
├── bootstrap/
├── catalog/
├── cli/
├── embedding/
├── intelligence/
├── knowledge/
├── search/
├── services/
│
scripts/
knowledge/
config/
data/
tests/
```

---

## ⚙️ Technology Stack

- Python 3.12+
- FastAPI
- Qdrant
- BGE-M3 Embeddings
- Sentence Transformers
- CrossEncoder
- Pydantic
- Uvicorn

---

## 🔍 Search Workflow

```
User Query
      │
      ▼
Normalize Query
      │
      ▼
Extract Attributes
      │
      ▼
Expand Query
      │
      ▼
Generate Embedding
      │
      ▼
Search Qdrant
      │
      ▼
Rerank Results
      │
      ▼
Business Ranking
      │
      ▼
Return Products
```

---

## 📦 Indexing Workflow

```
Raw Product JSON
        │
        ▼
Catalog Loader
        │
        ▼
Knowledge Registry
        │
        ▼
Product Intelligence Pipeline
        │
        ▼
Generate Search Document
        │
        ▼
Generate Embeddings
        │
        ▼
Store into Qdrant
```

---

## 🌐 REST API

### Search

```
GET /search?q=wall fans
```

Example

```
GET /search?q=ceiling fans below 5000
```

Returns

- Semantic Match
- Product Image
- Product URL
- Price
- Discount
- Stock Status

---

## 📈 Current Capabilities

✅ Semantic Search

✅ AI Query Expansion

✅ Query Normalization

✅ Intent Detection

✅ Price Filtering

✅ Color Filtering

✅ Metadata Search

✅ CrossEncoder Reranking

✅ Business Ranking

✅ Rich Product Payload

✅ Product Intelligence

✅ FastAPI REST API

✅ Qdrant Vector Search

---

## 🚀 Future Roadmap

- Hybrid Search (BM25 + Vector)
- Brand Detection
- Feature Detection
- Recommendation Engine
- AI Shopping Assistant
- Search Suggestions
- Faceted Search
- Next.js Modern UI
- Search Analytics Dashboard

---

## 🤝 Contributing

Contributions, feature requests and pull requests are welcome.

---

## 📄 License

MIT License