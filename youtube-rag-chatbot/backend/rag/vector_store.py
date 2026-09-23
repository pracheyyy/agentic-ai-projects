import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")


class HuggingFaceAPIEmbeddings(Embeddings):

    def __init__(self):
        self.client = InferenceClient(
            provider="hf-inference",
            api_key=HF_TOKEN
        )

        self.model = "BAAI/bge-small-en-v1.5"

    def embed_documents(self, texts):

        embeddings = []

        for text in texts:

            embedding = self.client.feature_extraction(
                text,
                model=self.model
            )

            embeddings.append(
                embedding.tolist()
            )

        return embeddings

    def embed_query(self, text):

        embedding = self.client.feature_extraction(
            text,
            model=self.model
        )

        return embedding.tolist()


def create_vector_store(chunks):

    embeddings = HuggingFaceAPIEmbeddings()

    vector_store = FAISS.from_texts(
        chunks,
        embeddings
    )

    return vector_store


def create_retriever(chunks, k=6):

    vector_store = create_vector_store(chunks)

    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    return retriever


def search_with_scores(vector_store, question, k=6):

    results = vector_store.similarity_search_with_score(
        question,
        k=k
    )

    return results


if __name__ == "__main__":

    test_chunks = [
        "RAG stands for Retrieval Augmented Generation.",
        "RAG retrieves relevant information before generating an answer.",
        "The retrieved information is provided to the language model.",
        "Python is a popular programming language."
    ]

    # Create FAISS vector store
    vector_store = create_vector_store(test_chunks)

    print("FAISS vector store created successfully!")

    # Search with similarity scores
    results = search_with_scores(
        vector_store,
        "How does RAG retrieve information?",
        k=2
    )

    print("\nMost relevant chunks:")

    for document, score in results:

        print("Score:", score)
        print("Chunk:", document.page_content)
        print()
    

    