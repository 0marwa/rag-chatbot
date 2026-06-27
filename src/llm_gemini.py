from google import genai

from src.config import settings
from src.llm import LLMProvider, SYSTEM_PROMPT


class GeminiProvider(LLMProvider):
    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set, add it to your .env")
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def answer(self, question: str, context: str) -> str:
        prompt = f"{SYSTEM_PROMPT}\n\ncontext:\n{context}\n\nquestion: {question}"
        resp = self.client.models.generate_content(model=self.model, contents=prompt)
        return resp.text.strip()
