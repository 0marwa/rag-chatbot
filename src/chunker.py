from src.config import settings


def chunk_text(text: str, source: str = "") -> list[dict]:
    """split text into overlapping chunks, return list of {text, source}"""
    size = settings.chunk_size
    overlap = settings.chunk_overlap
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({"text": chunk, "source": source})
        start += size - overlap
    return chunks


def chunk_docs(docs: list[dict]) -> list[dict]:
    chunks = []
    for doc in docs:
        chunks.extend(chunk_text(doc["text"], source=doc["filename"]))
    return chunks
