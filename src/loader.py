from pathlib import Path
import logging
import pdfplumber


SUPPORTED = {".txt", ".md", ".pdf"}

logger = logging.getLogger(__name__)


def _load_pdf(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    text = "\n".join(pages).strip()
    if not text:
        # pdf has no text layer -- probably a scanned document
        logger.warning("%s appears to be a scanned PDF (no text extracted). OCR is not supported yet.", path.name)
    return text


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
        if text:
            docs.append({"filename": path.name, "text": text})
    return docs
