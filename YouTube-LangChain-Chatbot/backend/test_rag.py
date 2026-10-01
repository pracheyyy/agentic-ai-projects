from app.services.youtube import get_transcript, get_video_id
from app.services.rag import create_document, split_document


# Put your YouTube URL here
url = "YOUR_YOUTUBE_URL"


# -----------------------------------
# 1. Get YouTube video ID
# -----------------------------------

video_id = get_video_id(url)

print("\nVideo ID:")
print(video_id)


# -----------------------------------
# 2. Fetch transcript
# -----------------------------------

transcript = get_transcript(url)

print("\nTranscript characters:")
print(len(transcript))


# -----------------------------------
# 3. Convert transcript to Document
# -----------------------------------

document = create_document(
    transcript,
    video_id
)

print("\nLangChain Document:")
print(document)


# -----------------------------------
# 4. Split document into chunks
# -----------------------------------

chunks = split_document(document)

print("\nNumber of chunks:")
print(len(chunks))


# -----------------------------------
# 5. Show first chunk
# -----------------------------------

print("\nFirst chunk:")
print(chunks[0].page_content)