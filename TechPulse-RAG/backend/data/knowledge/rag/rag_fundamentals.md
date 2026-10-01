# RAG and AI Applications

Retrieval-Augmented Generation, or RAG, combines information retrieval with language generation.

## Basic RAG Flow
A typical RAG system ingests documents, cleans them, splits them into chunks, creates embeddings, stores vectors, retrieves relevant chunks for a question, and supplies those chunks to an LLM.

## Embeddings
An embedding represents text as a numeric vector. Semantically similar text tends to have nearby vector representations.

## Vector Databases
Vector stores such as FAISS support similarity search over embeddings.

## Retrieval
A retriever selects candidate documents based on similarity to the question. A relevance threshold can prevent unrelated documents from being passed to the generator.

## Grounded Generation
A grounded generator should answer from retrieved context and avoid inventing unsupported facts. Sources should be exposed to the user when possible.

## Chunking
Chunking divides documents into smaller units. Chunks should preserve enough context to answer questions while remaining focused.
