from app.bootstrap.container import container

def main():
    query = "white ceiling fan"
    vector = container.embedder.encode_query(query)
    hybrid = container.hybrid_retriever.retrieve(
        vector=vector,
        query=query,
    )
    fused = container.rrf.fuse(
        hybrid["semantic"],
        hybrid["bm25"],
    )
    print("Total:", len(fused))
    for item in fused[:10]:
        payload = item["payload"]
        print(payload.get("sku"))
        print(payload.get("title"))
        print(item.get("rrf_score"))
        print()

if __name__ == "__main__":
    main()
