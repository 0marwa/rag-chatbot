from pathlib import Path


SUPPORTED = {".txt", ".md"}


def load_docs(data_dir: str = "data") -> list[dict]:
    """return list of {filename, text} for all supported files in data_dir"""
    docs = []
    for path in sorted(Path(data_dir).iterdir()):
        if path.suffix in SUPPORTED:
            docs.append({"filename": path.name, "text": path.read_text(encoding="utf-8")})
    return docs
