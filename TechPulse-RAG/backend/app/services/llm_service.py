import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


SYSTEM_PROMPT = """You are TechPulse AI, an IT and technology knowledge assistant.

You answer questions using ONLY the supplied TechPulse context.

The context can contain:
1. Technical knowledge such as programming, AI/ML, web development,
   backend, databases, cloud, DevOps, cybersecurity and CS fundamentals.
2. Current technology news from permitted RSS sources.

Rules:
- Do not invent facts that are not supported by the context.
- If the context is insufficient, clearly say that TechPulse does not have
  enough information in its knowledge base.
- For technical questions, explain concepts clearly and practically.
- For news questions, distinguish current news from general technical knowledge.
- Do not treat an unrelated retrieved document as evidence.
- Use the retrieved context as the source of truth.
- Keep answers useful and reasonably concise.
- When discussing news, mention the source/article when useful.
"""


def fallback_answer(question: str, sources: list[dict]) -> str:
    if not sources:
        return (
            "I don't have enough information in my TechPulse knowledge base "
            "to answer that reliably."
        )

    lines = [
        "I found relevant information in the TechPulse knowledge base:"
    ]

    for source in sources[:3]:
        lines.append(
            f"• {source.get('title', 'Untitled')} — "
            f"{source.get('summary', 'No summary available.')}"
        )

    lines.append(
        "Hugging Face is not configured, so this is a retrieval-based response."
    )

    return "\n".join(lines)


def _build_context(sources: list[dict]) -> str:
    return "\n\n---\n\n".join(
        f"""SOURCE {i}
Title: {source.get('title', '')}
Type: {source.get('type', '')}
Category: {source.get('category', '')}
Source: {source.get('source', '')}
Published: {source.get('published', '')}
Content: {source.get('summary', '')}
URL: {source.get('url', '')}
"""
        for i, source in enumerate(sources, start=1)
    )


def generate_answer(question: str, sources: list[dict]) -> str:
    """Generate a grounded answer with an open-weight model via HF Inference Providers.

    The frontend and RAG pipeline remain unchanged. Only the final generation
    provider is Hugging Face instead of Gemini.
    """
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        return fallback_answer(question, sources)

    model = os.getenv("LLM_MODEL", "openai/gpt-oss-20b:fastest")
    base_url = os.getenv("HF_BASE_URL", "https://router.huggingface.co/v1")

    try:
        client = OpenAI(
            base_url=base_url,
            api_key=hf_token,
        )

        context = _build_context(sources)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"USER QUESTION:\n{question}\n\n"
                        f"RETRIEVED TECHPULSE CONTEXT:\n{context}"
                    ),
                },
            ],
            temperature=0.2,
            max_tokens=700,
        )

        answer = response.choices[0].message.content
        return answer.strip() if answer else fallback_answer(question, sources)

    except Exception as exc:
        print(f"[HUGGING FACE LLM ERROR] {exc}")
        return fallback_answer(question, sources)
