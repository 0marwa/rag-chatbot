from supabase import create_client

from src.config import settings

# use service role key so we can read/write without RLS restrictions
_client = create_client(settings.supabase_url, settings.supabase_service_role_key)


class VectorStore:
    def __init__(self, session_id: str = "default") -> None:
        self.session_id = session_id

    def add(self, chunks: list[str], embeddings: list[list[float]], sources: list[str]) -> None:
        rows = [
            {"session_id": self.session_id, "source": src, "content": txt, "embedding": emb}
            for txt, emb, src in zip(chunks, embeddings, sources)
        ]
        _client.table("documents").insert(rows).execute()

    def get_sources(self) -> set[str]:
        """return all unique source filenames already ingested for this session."""
        resp = (
            _client.table("documents")
            .select("source")
            .eq("session_id", self.session_id)
            .execute()
        )
        return {row["source"] for row in resp.data}

    def search(self, query_vec: list[float], top_k: int, threshold: float) -> list[dict]:
        # pgvector rpc for cosine similarity search
        resp = _client.rpc(
            "match_documents",
            {
                "query_embedding": query_vec,
                "match_session_id": self.session_id,
                "match_count": top_k,
                "match_threshold": threshold,
            },
        ).execute()
        return [
            {"text": r["content"], "source": r["source"], "score": round(r["similarity"], 4)}
            for r in resp.data
        ]
