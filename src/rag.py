from src.chunker import chunk_docs
from src.config import settings
from src.embedder import get_embedder
from src.llm import get_llm
from src.loader import load_docs
from src.store import VectorStore


def ingest(data_dir: str = "data", session_id: str = "default") -> int:
    """load docs, chunk, embed, store. returns number of chunks stored."""
    docs = load_docs(data_dir)
    if not docs:
        print(f"no supported files found in {data_dir}/")
        return 0

    store = VectorStore(session_id=session_id)
    already_ingested = store.get_sources()

    # skip files already in chroma
    new_docs = [d for d in docs if d["filename"] not in already_ingested]
    if not new_docs:
        return 0

    chunks = chunk_docs(new_docs)
    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]

    embedder = get_embedder()
    embeddings = embedder.embed(texts)

    store.add(texts, embeddings, sources)
    return len(chunks)


def ask(question: str, session_id: str = "default", debug: bool = False) -> dict:
    """embed question, retrieve top-k chunks, ask llm. returns {answer, sources}."""
    embedder = get_embedder()
    query_vec = embedder.embed_one(question)

    store = VectorStore(session_id=session_id)
    results = store.search(query_vec, top_k=settings.top_k, threshold=settings.similarity_threshold)

    if not results:
        return {"answer": "no relevant context found in the loaded documents.", "sources": []}

    if debug:
        print("\n--- retrieved chunks ---")
        for r in results:
            print(f"[{r['source']} | score={r['score']}] {r['text'][:120]}...")
        print("---\n")

    context = "\n\n".join(r["text"] for r in results)
    sources = list(dict.fromkeys(r["source"] for r in results))  # unique, order preserved

    llm = get_llm()
    answer = llm.answer(question, context)
    return {"answer": answer, "sources": sources}
