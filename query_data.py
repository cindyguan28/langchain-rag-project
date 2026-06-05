import argparse

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


CHROMA_PATH = "chroma"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.2:3b"


PROMPT_TEMPLATE = """
You are a helpful AWS troubleshooting assistant.

Answer the question based only on the following context.

If the context does not contain enough information, say:
"I don't have enough information in the provided context."

Context:
{context}

---

Question:
{question}

Answer:
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    parser.add_argument(
        "--k",
        type=int,
        default=4,
        help="Number of relevant chunks to retrieve.",
    )
    args = parser.parse_args()

    query_text = args.query_text

    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function,
    )

    results = db.similarity_search_with_score(query_text, k=args.k)

    if not results:
        print("Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results]
    )

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=context_text,
        question=query_text,
    )

    model = ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0,
    )

    response = model.invoke(prompt)

    sources = [
        {
            "source": doc.metadata.get("source", "unknown"),
            "start_index": doc.metadata.get("start_index", "unknown"),
            "score": score,
        }
        for doc, score in results
    ]

    print("\nResponse:")
    print(response.content)

    print("\nSources:")
    for item in sources:
        print(
            f"- {item['source']} "
            f"(start_index={item['start_index']}, score={item['score']})"
        )


if __name__ == "__main__":
    main()