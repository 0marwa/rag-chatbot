import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default: str) -> str:
    # env vars come in as strings, fall back to default if unset or empty
    val = os.getenv(key)
    return val if val else default


@dataclass
class Settings:
    # which providers to use
    llm_provider: str = _get("LLM_PROVIDER", "groq")
    embedding_provider: str = _get("EMBEDDING_PROVIDER", "local")

    # llm
    groq_api_key: str = _get("GROQ_API_KEY", "")
    groq_model: str = _get("GROQ_MODEL", "llama-3.3-70b-versatile")
    gemini_api_key: str = _get("GEMINI_API_KEY", "")
    gemini_model: str = _get("GEMINI_MODEL", "gemini-2.0-flash")

    # embeddings
    embedding_model: str = _get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # chunking
    chunk_size: int = int(_get("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(_get("CHUNK_OVERLAP", "50"))

    # retrieval
    top_k: int = int(_get("TOP_K", "4"))
    similarity_threshold: float = float(_get("SIMILARITY_THRESHOLD", "0.3"))

    # where chroma persists
    db_path: str = _get("DB_PATH", "chroma_db")


settings = Settings()
