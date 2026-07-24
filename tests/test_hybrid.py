from app.bootstrap.container import container

def main():
    query = "white ceiling fan"
    vector = container.embedder.encode_query(query)
    results = container.hybrid_retriever.retrieve(
        vector=vector,
        query=query,
    )
    print("Semantic:", len(results["semantic"]))
    print("BM25:", len(results["bm25"]))

if __name__ == "__main__":
    main()
