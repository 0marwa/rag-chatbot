from groq import Groq

from src.config import settings

# keep the model on a short leash: only answer from what we hand it
SYSTEM_PROMPT = (
    "You answer questions using only the context provided below. "
    "Do not use any outside knowledge. "
    "If the answer is not in the context, say you don't know based on the "
    "given context. Keep answers short and grounded in the context."
)


class LLMProvider:
    # swap-in point for other providers later (openai, gemini, ollama...)
    def answer(self, question: str, context: str) -> str:
        raise NotImplementedError


class GroqProvider(LLMProvider):
    def __init__(self) -> None:
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is not set, add it to your .env")
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model

    def answer(self, question: str, context: str) -> str:
        prompt = f"context:\n{context}\n\nquestion: {question}"
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        return resp.choices[0].message.content.strip()


def get_llm() -> LLMProvider:
    if settings.llm_provider == "groq":
        return GroqProvider()
    raise ValueError(f"unknown llm provider: {settings.llm_provider}")
