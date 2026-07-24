from app.search.bm25.retriever import BM25Retriever

def main():
    retriever = BM25Retriever("storage/bm25.pkl")
    query = "white ceiling fan"
    results = retriever.retrieve(query=query, top_k=10)
    print("="*80)
    print(query)
    print("="*80)
    for i,item in enumerate(results,1):
        print(f"\n{i}")
        print("SKU :", item.get("sku"))
        print("Title :", item.get("title"))
        print("Score :", round(item.get("score",0),3))

if __name__ == "__main__":
    main()
