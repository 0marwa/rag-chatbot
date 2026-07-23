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
    embedding_provider: str = _get("EMBEDDING_PROVIDER", "huggingface")

    # llm
    groq_api_key: str = _get("GROQ_API_KEY", "")
    groq_model: str = _get("GROQ_MODEL", "llama-3.3-70b-versatile")
    gemini_api_key: str = _get("GEMINI_API_KEY", "")
    gemini_model: str = _get("GEMINI_MODEL", "gemini-2.0-flash")

    # embeddings -- huggingface inference api, free tier, no card needed, same model as local (384 dims)
    hf_token: str = _get("HF_TOKEN", "")
    embedding_model: str = _get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # chunking
    chunk_size: int = int(_get("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(_get("CHUNK_OVERLAP", "50"))

    # retrieval
    top_k: int = int(_get("TOP_K", "4"))
    similarity_threshold: float = float(_get("SIMILARITY_THRESHOLD", "0.3"))

    # supabase
    supabase_url: str = _get("SUPABASE_URL", "")
    supabase_service_role_key: str = _get("SUPABASE_SERVICE_ROLE_KEY", "")
    supabase_bucket: str = _get("SUPABASE_BUCKET", "documents")


settings = Settings()
