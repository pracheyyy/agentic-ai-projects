# text splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(transcript):

    # Combine all transcript text
    full_text = " ".join(
        item["text"] for item in transcript
    )

    # Create text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    # Split transcript into chunks
    chunks = splitter.split_text(full_text)

    return chunks

# test 
if __name__ == "__main__":

    sample_transcript = [
        {
            "text": "RAG stands for Retrieval Augmented Generation.",
            "start": 0,
            "duration": 3
        },
        {
            "text": "It allows an AI system to retrieve relevant information.",
            "start": 3,
            "duration": 4
        },
        {
            "text": "The retrieved information is then given to the language model.",
            "start": 7,
            "duration": 5
        }
    ]

    chunks = create_chunks(sample_transcript)

    for i, chunk in enumerate(chunks):

        print(f"\n--- Chunk {i + 1} ---")
        print(chunk)