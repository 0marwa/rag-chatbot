from pathlib import Path
import pdfplumber


SUPPORTED = {".txt", ".md", ".pdf"}


def _load_pdf(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def load_docs(data_dir: str = "data") -> list[dict]:
    """return list of {filename, text} for all supported files in data_dir"""
    docs = []
    for path in sorted(Path(data_dir).iterdir()):
        if path.suffix not in SUPPORTED:
            continue
        if path.suffix == ".pdf":
            text = _load_pdf(path)
        else:
            text = path.read_text(encoding="utf-8")
        docs.append({"filename": path.name, "text": text})
    return docs
