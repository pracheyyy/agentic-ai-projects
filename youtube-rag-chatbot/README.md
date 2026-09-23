# 🎥 YouTube RAG Chatbot

An AI-powered chatbot that allows users to paste a YouTube video URL and ask questions about the video's content.

The system extracts the YouTube transcript, splits it into chunks, generates vector embeddings using Hugging Face, stores them in FAISS, retrieves relevant context, and uses Gemini to generate answers.

---

## 🚀 Features

- 🎥 Load YouTube videos using a URL
- 📝 Automatically fetch YouTube transcripts
- ✂️ Split transcripts into overlapping chunks
- 🧠 Generate embeddings using Hugging Face
- 🔎 Semantic search using FAISS
- 🤖 Retrieval-Augmented Generation (RAG)
- 💬 Ask natural-language questions about videos
- 🌐 Gemini API for answer generation
- 🔄 Gemini general-knowledge fallback when information is not found in the video
- ⚡ FastAPI backend
- 🎨 HTML, CSS and JavaScript frontend
- 🔐 Secure API key management using `.env`

---

## 🏗️ Architecture

```text
                    User
                     │
                     ▼
              YouTube Video URL
                     │
                     ▼
              FastAPI Backend
                     │
                     ▼
          YouTube Transcript API
                     │
                     ▼
               Transcript
                     │
                     ▼
              Text Chunking
             1000 chars / 150 overlap
                     │
                     ▼
          Hugging Face Embeddings
          BAAI/bge-small-en-v1.5
                     │
                     ▼
                   FAISS
              Vector Store
                     │
              User Question
                     │
                     ▼
              Semantic Search
                     │
                     ▼
              Top 10 Chunks
                     │
                     ▼
                 Gemini
                     │
          ┌──────────┴──────────┐
          │                     │
       FOUND                 NOT FOUND
          │                     │
          ▼                     ▼
   RAG + Gemini          Gemini General
     Answer              Knowledge
          │                     │
          └──────────┬──────────┘
                     ▼
                   Answer
```

---

## 🧠 How It Works

### 1. Transcript Extraction

The user provides a YouTube URL.

The backend extracts the video ID and retrieves the transcript using the YouTube Transcript API.

```text
YouTube URL
     ↓
Video ID
     ↓
Transcript
```

### 2. Text Chunking

The transcript is divided into smaller overlapping chunks.

Current configuration:

```text
Chunk Size: 1000 characters
Chunk Overlap: 150 characters
```

The overlap helps preserve context between neighboring chunks.

### 3. Embeddings

Each chunk is converted into a vector using:

```text
BAAI/bge-small-en-v1.5
```

through the Hugging Face API.

Embedding dimension:

```text
384
```

### 4. FAISS Vector Store

The generated embeddings are stored in FAISS.

FAISS is used to find the chunks most semantically related to the user's question.

### 5. Retrieval

When the user asks a question:

```text
User Question
     ↓
FAISS Similarity Search
     ↓
Top 10 Relevant Chunks
```

### 6. Answer Generation

Gemini checks all retrieved chunks.

If the answer is present in the video:

```text
FAISS → Relevant Context → Gemini → Answer
```

If the answer is not present:

```text
FAISS → NOT_FOUND
              ↓
       Gemini General Knowledge
              ↓
            Answer
```

---

## 🛠️ Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- FastAPI
- Uvicorn

### RAG

- LangChain
- FAISS
- Hugging Face Embeddings
- Recursive Character Text Splitter

### AI / APIs

- YouTube Transcript API
- Hugging Face API
- `BAAI/bge-small-en-v1.5`
- Google Gemini API
- `gemini-3.6-flash`

---

## 📁 Project Structure

```text
youtube-rag-chatbot/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   ├── .gitignore
│   │
│   └── rag/
│       ├── __init__.py
│       ├── processor.py
│       ├── embedding_test.py
│       ├── vector_store.py
│       └── llm.py
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd youtube-rag-chatbot
```

### 2. Navigate to the backend

```bash
cd backend
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```powershell
.\venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install fastapi uvicorn python-dotenv youtube-transcript-api langchain langchain-community langchain-text-splitters faiss-cpu huggingface-hub google-genai
```

Or:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file inside the `backend` folder.

```env
HF_TOKEN=your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit `.env` to GitHub.

Your `.gitignore` should contain:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the Backend

From the `backend` folder:

```bash
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Test the API:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "YouTube RAG API is running 🚀"
}
```

---

## 🖥️ Run the Frontend

Open:

```text
frontend/index.html
```

in your browser.

Then:

1. Paste a YouTube video URL.
2. Click **Load Video**.
3. Wait for the transcript and FAISS vector store to be created.
4. Ask questions about the video.

Example questions:

```text
Who is she?
```

```text
Is she an actor?
```

```text
What does she do?
```

```text
What did she say about her parents?
```

---

## 🔌 API Endpoints

### GET `/`

Checks whether the backend is running.

Response:

```json
{
  "message": "YouTube RAG API is running 🚀"
}
```

---

### POST `/video/load`

Loads a YouTube video and creates its FAISS vector store.

Request:

```json
{
  "youtube_url": "https://youtu.be/example"
}
```

Process:

```text
YouTube URL
     ↓
Extract Video ID
     ↓
Fetch Transcript
     ↓
Create Chunks
     ↓
Generate Embeddings
     ↓
Create FAISS Vector Store
```

---

### POST `/chat`

Answers questions using the loaded video's knowledge.

Request:

```json
{
  "question": "Who is she?"
}
```

Response:

```json
{
  "success": true,
  "question": "Who is she?",
  "answer": "......",
  "source": "video",
  "context": [
    "relevant transcript chunk..."
  ]
}
```

The `source` field can be:

```text
video
```

or:

```text
general
```

---

## 🧩 Core Components

### `processor.py`

Responsible for transcript processing and chunking.

```text
Transcript
    ↓
Text
    ↓
Chunks
```

Current configuration:

```text
chunk_size = 1000
chunk_overlap = 150
```

---

### `vector_store.py`

Responsible for embeddings and FAISS.

```text
Text Chunks
    ↓
Hugging Face API
    ↓
Embeddings
    ↓
FAISS
```

---

### `llm.py`

Responsible for Gemini.

It contains:

```python
generate_rag_answer()
```

for answering using retrieved video context.

And:

```python
generate_general_answer()
```

for questions that are not supported by the video transcript.

---

### `main.py`

Acts as the main backend controller.

```text
YouTube
   ↓
Transcript
   ↓
Chunking
   ↓
Embeddings
   ↓
FAISS
   ↓
Gemini
   ↓
Response
```

---

## 🧪 Example

Suppose the video transcript contains:

```text
"I'm an actor. I'm a singer. I'm an author."
```

User asks:

```text
Is she an actor?
```

The system:

```text
Question
   ↓
FAISS Search
   ↓
Relevant Transcript Chunk
   ↓
Gemini
   ↓
Answer from Video
```

---

If the user asks:

```text
What is the capital of France?
```

and the information is not present in the video:

```text
Question
   ↓
FAISS Search
   ↓
NOT_FOUND
   ↓
Gemini General Knowledge
   ↓
Paris
```

---

## ⚠️ Current Limitations

- Requires an available English YouTube transcript.
- The current vector store is stored in memory.
- Only one active video's vector store is maintained at a time.
- FAISS data is not permanently persisted yet.
- Gemini API availability and quotas can affect answer generation.
- Transcript timestamps are not yet integrated into the RAG chunks.
- Multiple videos are not yet supported simultaneously.
- Frontend and backend currently run locally.

---

## 🚧 Future Improvements

### Timestamp-Aware RAG

Preserve transcript timestamps during chunking.

```text
Answer
  ↓
Timestamp
  ↓
Click Timestamp
  ↓
Jump to YouTube Position
```

### Gemini Failure Fallback

If Gemini is temporarily unavailable:

```text
FAISS
  ↓
Relevant Transcript
  ↓
RAG-only Fallback
```

### Persistent Vector Store

Save FAISS indexes instead of rebuilding them every time.

```text
YouTube Video
      ↓
Generate Embeddings
      ↓
Save FAISS Index
      ↓
Reuse Later
```

### Conversation Memory

Support follow-up questions:

```text
User:
Who is she?

Bot:
She is an actor and singer.

User:
What else does she do?

Bot:
She is also an author and producer.
```

### Multiple Video Support

Allow users to load and query multiple YouTube videos.

### Better Retrieval

Future improvements:

- Query rewriting
- Hybrid search
- Reranking
- Metadata filtering
- Improved chunking strategies

---

## 🔐 Security

Never hardcode API keys.

Use environment variables:

```env
HF_TOKEN=...
GEMINI_API_KEY=...
```

Keep `.env` inside `.gitignore`.

---

## 🎯 Project Goal

The goal of this project is to build a practical Retrieval-Augmented Generation system that allows users to interact conversationally with YouTube videos.

Instead of sending the complete transcript directly to an LLM, the system retrieves only the most relevant information before generating an answer.

```text
Retrieve → Augment → Generate
```

This makes the chatbot more focused on the video's actual content while still allowing Gemini to answer questions outside the video's scope.

---

## 👨‍💻 Author

**Prachi Patil**

B.Tech Information Technology  
JSPM Rajarshi Shahu College of Engineering, Pune

### Interests

- Software Development
- Data Structures & Algorithms
- Machine Learning
- Generative AI
- RAG
- AI Agents
- Full-Stack Development