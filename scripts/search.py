
import argparse

def main():
    p=argparse.ArgumentParser()
    p.add_argument("query")
    args=p.parse_args()
    print("TODO: integrate SemanticSearchService")
    print("Query:",args.query)

if __name__=="__main__":
    main()
