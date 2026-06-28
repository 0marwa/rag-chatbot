from src.config import settings


class EmbeddingProvider:
    # swap-in point for other providers
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]


class TogetherEmbedder(EmbeddingProvider):
    """calls together.ai embeddings api -- no local model, no ram spike."""
    _BASE = "https://api.together.xyz/v1/embeddings"

    def __init__(self) -> None:
        import requests
        self._requests = requests
        self._key = settings.together_api_key
        self._model = settings.embedding_model

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = self._requests.post(
            self._BASE,
            headers={"Authorization": f"Bearer {self._key}", "Content-Type": "application/json"},
            json={"model": self._model, "input": texts},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        return [item["embedding"] for item in sorted(data, key=lambda x: x["index"])]


class LocalEmbedder(EmbeddingProvider):
    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(settings.embedding_model)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()


def get_embedder() -> EmbeddingProvider:
    if settings.embedding_provider == "together":
        return TogetherEmbedder()
    if settings.embedding_provider == "local":
        return LocalEmbedder()
    raise ValueError(f"unknown embedding provider: {settings.embedding_provider}")
