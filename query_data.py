import argparse

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CHROMA_PATH = "chroma"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
    )

    results = db.similarity_search_with_score(query_text, k=3)

    if len(results) == 0:
        print("Unable to find matching results.")
        return

    print("\nQuery:")
    print(query_text)

    print("\nTop matching results:")

    for i, (doc, score) in enumerate(results, start=1):
        source = doc.metadata.get("source", "unknown")
        start_index = doc.metadata.get("start_index", "unknown")

        print(f"\n--- Result {i} ---")
        print(f"Source: {source}")
        print(f"Start index: {start_index}")
        print(f"Distance score: {score}")
        print("\nContent:")
        print(doc.page_content)


if __name__ == "__main__":
    main()