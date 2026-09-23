import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")


class GeminiLLM:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = "gemini-3.6-flash"


    # ==========================================
    # GEMINI REQUEST WITH RETRY
    # ==========================================

    def _generate(self, prompt, retries=3):

        for attempt in range(retries):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                return response.text.strip()

            except Exception as e:

                print(
                    f"Gemini request failed "
                    f"(attempt {attempt + 1}/{retries}): {e}"
                )

                if attempt == retries - 1:
                    raise

                time.sleep(2 ** attempt)


    # ==========================================
    # RAG ANSWER
    # ==========================================

    def generate_rag_answer(self, question, context):

        prompt = f"""
You are the answering system for a YouTube RAG chatbot.

The user asked a question about a YouTube video.

You are given the top retrieved transcript chunks from
that video.

IMPORTANT RULES:

1. Search ALL of the retrieved chunks.

2. The answer may be present in ANY chunk, not necessarily
   the first one.

3. Combine information from multiple chunks if necessary.

4. If the transcript contains enough information to answer
   the question, answer it directly.

5. Do NOT use outside knowledge when answering from the
   transcript.

6. Do NOT invent information.

7. If the transcript does NOT contain enough information,
   return exactly:

NOT_FOUND

Retrieved Transcript:
--------------------------------
{context}
--------------------------------

User Question:
{question}

Answer:
"""

        return self._generate(prompt)


    # ==========================================
    # GENERAL GEMINI FALLBACK
    # ==========================================

    def generate_general_answer(self, question):

        prompt = f"""
You are a helpful AI assistant.

The YouTube transcript did not contain enough information
to answer the user's question.

Answer using your general knowledge.

Do not claim that the answer came from the YouTube video.

User Question:
{question}

Answer:
"""

        return self._generate(prompt)