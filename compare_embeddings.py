import numpy as np

from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables. Assumes that project contains .env file with API keys
#load_dotenv()

def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def main():
    # Use a local Hugging Face embedding model.
    # No OpenAI account or API key is required.
    
    #---- Set OpenAI API key 
    # Change environment variable name from "OPENAI_API_KEY" to the name given in 
    # your .env file.

    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Get embedding for a word.
    vector = embedding_function.embed_query("apple")

    print("Vector for 'apple':")
    print(vector[:10])
    print(f"Vector length: {len(vector)}")

    # Compare vectors of two words.
    words = ("apple", "pineapple")

    vector_1 = embedding_function.embed_query(words[0])
    vector_2 = embedding_function.embed_query(words[1])

    similarity = cosine_similarity(vector_1, vector_2)
    distance = 1 - similarity

    print(f"\nComparing ({words[0]}, {words[1]}):")
    print(f"Cosine similarity: {similarity:.4f}")
    print(f"Cosine distance: {distance:.4f}")


if __name__ == "__main__":
    main()