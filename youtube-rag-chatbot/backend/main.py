from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
import re

from rag.processor import create_chunks
from rag.vector_store import create_vector_store
from rag.llm import GeminiLLM


app = FastAPI()


# Store the current video's vector store
vector_store = None

# Gemini
llm = GeminiLLM()


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REQUEST MODELS
# =========================

class VideoRequest(BaseModel):
    youtube_url: str


class ChatRequest(BaseModel):
    question: str


# =========================
# EXTRACT VIDEO ID
# =========================

def extract_video_id(url: str):

    patterns = [
        r"(?:v=|youtu\.be/|youtube\.com/embed/)([^&?/]+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "YouTube RAG API is running 🚀"
    }


# =========================
# LOAD VIDEO
# =========================

@app.post("/video/load")
def load_video(request: VideoRequest):

    global vector_store

    video_id = extract_video_id(
        request.youtube_url
    )

    if not video_id:

        return {
            "success": False,
            "message": "Invalid YouTube URL"
        }

    try:

        # =========================
        # 1. FETCH TRANSCRIPT
        # =========================

        ytt_api = YouTubeTranscriptApi()

        transcript_list = ytt_api.list(
            video_id
        )

        transcript = transcript_list.find_transcript(
            ["en"]
        )

        transcript_data = transcript.fetch()

        transcript_data = transcript_data.to_raw_data()

        print("1. Transcript fetched")


        # =========================
        # 2. CREATE CHUNKS
        # =========================

        chunks = create_chunks(
            transcript_data
        )

        print(
            f"2. Created {len(chunks)} chunks"
        )


        # =========================
        # 3. CREATE FAISS VECTOR STORE
        # =========================

        vector_store = create_vector_store(
            chunks
        )

        print(
            "3. FAISS vector store created"
        )


        return {

            "success": True,

            "video_id": video_id,

            "language": transcript.language,

            "is_generated": transcript.is_generated,

            "transcript": transcript_data

        }


    except Exception as e:

        return {

            "success": False,

            "message": str(e)

        }


# =========================
# CHAT
# =========================

@app.post("/chat")
def chat(request: ChatRequest):

    if vector_store is None:

        return {
            "success": False,
            "message": "Please load a YouTube video first."
        }

    try:

        # ==========================================
        # 1. FAISS → TOP 10
        # ==========================================

        results = vector_store.similarity_search_with_score(
            request.question,
            k=10
        )

        print("\n==============================")
        print("QUESTION:", request.question)
        print("==============================")


        # ==========================================
        # 2. PRINT RETRIEVED CHUNKS
        # ==========================================

        for i, (document, score) in enumerate(results):

            print(f"\nChunk {i + 1}")
            print("Score:", score)
            print(
                "Text:",
                document.page_content[:200]
            )


        # ==========================================
        # 3. COMBINE ALL 10 CHUNKS
        # ==========================================

        context = "\n\n".join(
            document.page_content
            for document, score in results
        )


        # ==========================================
        # 4. ASK GEMINI TO ANSWER FROM RAG
        # ==========================================

        answer = llm.generate_rag_answer(
            request.question,
            context
        )


        # ==========================================
        # 5. CHECK IF RAG FOUND THE ANSWER
        # ==========================================

        if answer.strip() == "NOT_FOUND":

            print(
                "\n→ ANSWER NOT FOUND IN VIDEO"
            )

            print(
                "→ Using Gemini general knowledge"
            )

            answer = llm.generate_general_answer(
                request.question
            )

            source = "general"


        else:

            print(
                "\n→ ANSWER FOUND IN VIDEO"
            )

            print(
                "→ Using RAG + Gemini"
            )

            source = "video"


        # ==========================================
        # 6. RETURN RESPONSE
        # ==========================================

        return {

            "success": True,

            "question": request.question,

            "answer": answer,

            "source": source,

            "context": [
                document.page_content
                for document, score in results
            ]

        }


    except Exception as e:

        return {

            "success": False,

            "message": str(e)

        }