import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load .env
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")


# Create Hugging Face client
client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)


# Text to convert into embedding
text = "RAG retrieves relevant information before generating an answer."


# Generate embedding
embedding = client.feature_extraction(
    text,
    model="BAAI/bge-small-en-v1.5"
)


print("Embedding generated successfully!")

print("Type:", type(embedding))

print("Number of dimensions:", len(embedding))

print("First 10 values:")
print(embedding[:10])