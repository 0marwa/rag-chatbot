import chromadb

from src.config import settings


class VectorStore:
    def __init__(self, session_id: str = "default") -> None:
        client = chromadb.PersistentClient(path=settings.db_path)
        # one collection per session so users don't see each other's docs
        self.col = client.get_or_create_collection(
            name=f"docs_{session_id}",
            # chroma computes its own embeddings by default; we pass ours in
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, chunks: list[str], embeddings: list[list[float]], sources: list[str]) -> None:
        # ids are just positional, chroma needs unique strings
        start = self.col.count()
        ids = [str(start + i) for i in range(len(chunks))]
        metadatas = [{"source": s} for s in sources]
        self.col.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)

    def get_sources(self) -> set[str]:
        """return all unique source filenames already in the collection."""
        if self.col.count() == 0:
            return set()
        # get all metadata without fetching embeddings or documents
        result = self.col.get(include=["metadatas"])
        return {m["source"] for m in result["metadatas"] if "source" in m}

    def search(self, query_vec: list[float], top_k: int, threshold: float) -> list[dict]:
        if self.col.count() == 0:
            return []
        results = self.col.query(
            query_embeddings=[query_vec],
            n_results=min(top_k, self.col.count()),
            include=["documents", "distances", "metadatas"],
        )
        docs = results["documents"][0]
        # chroma returns cosine distance (0=identical, 2=opposite); convert to similarity
        dists = results["distances"][0]
        metas = results["metadatas"][0]
        out = []
        for doc, dist, meta in zip(docs, dists, metas):
            similarity = 1 - dist
            if similarity >= threshold:
                out.append({"text": doc, "source": meta.get("source", ""), "score": round(similarity, 4)})
        return out
