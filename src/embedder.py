from src.config import settings


class EmbeddingProvider:
    # swap-in point for other providers
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]


class HFEmbedder(EmbeddingProvider):
    """calls huggingface inference api -- no local model, no ram spike. free tier, no card needed."""
    # old api-inference.huggingface.co host is dead, hf moved to this router
    _BASE = "https://router.huggingface.co/hf-inference/models/"
    _SUFFIX = "/pipeline/feature-extraction"

    def __init__(self) -> None:
        import requests
        self._requests = requests
        self._key = settings.hf_token
        self._model = settings.embedding_model

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = self._requests.post(
            self._BASE + self._model + self._SUFFIX,
            headers={"Authorization": f"Bearer {self._key}"},
            json={"inputs": texts, "options": {"wait_for_model": True}},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()


class LocalEmbedder(EmbeddingProvider):
    def __init__(self) -> None:
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(settings.embedding_model)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()


def get_embedder() -> EmbeddingProvider:
    if settings.embedding_provider == "huggingface":
        return HFEmbedder()
    if settings.embedding_provider == "local":
        return LocalEmbedder()
    raise ValueError(f"unknown embedding provider: {settings.embedding_provider}")
