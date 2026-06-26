import chromadb

from src.config import settings


class VectorStore:
    def __init__(self) -> None:
        client = chromadb.PersistentClient(path=settings.db_path)
        # get_or_create so re-running ingest doesn't blow up
        self.col = client.get_or_create_collection(
            name="docs",
            # chroma computes its own embeddings by default; we pass ours in
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, chunks: list[str], embeddings: list[list[float]]) -> None:
        # ids are just positional, chroma needs unique strings
        start = self.col.count()
        ids = [str(start + i) for i in range(len(chunks))]
        self.col.add(documents=chunks, embeddings=embeddings, ids=ids)

    def search(self, query_vec: list[float], top_k: int, threshold: float) -> list[dict]:
        if self.col.count() == 0:
            return []
        results = self.col.query(
            query_embeddings=[query_vec],
            n_results=min(top_k, self.col.count()),
            include=["documents", "distances"],
        )
        docs = results["documents"][0]
        # chroma returns cosine distance (0=identical, 2=opposite); convert to similarity
        dists = results["distances"][0]
        out = []
        for doc, dist in zip(docs, dists):
            similarity = 1 - dist
            if similarity >= threshold:
                out.append({"text": doc, "score": round(similarity, 4)})
        return out
