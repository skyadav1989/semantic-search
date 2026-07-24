from app.bootstrap.container import container

def main():
    vector = container.embedder.encode_query("white ceiling fan")
    results = container.retriever.retrieve(vector, limit=10)
    for i,item in enumerate(results,1):
        payload = item["payload"]
        print(i)
        print(payload.get("sku"))
        print(payload.get("title"))
        print(item.get("score"))
        print()

if __name__ == "__main__":
    main()
