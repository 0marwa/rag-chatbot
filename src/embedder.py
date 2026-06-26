from sentence_transformers import SentenceTransformer

from src.config import settings


class EmbeddingProvider:
    # swap-in point for other providers later (openai, gemini...)
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]


class LocalEmbedder(EmbeddingProvider):
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.embedding_model)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()


def get_embedder() -> EmbeddingProvider:
    if settings.embedding_provider == "local":
        return LocalEmbedder()
    raise ValueError(f"unknown embedding provider: {settings.embedding_provider}")
