import os
import shutil

from fastapi import FastAPI, HTTPException, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.rag import ask, ingest
from src.loader import SUPPORTED

app = FastAPI()

# allow the next.js dev server to call the api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*", "X-Session-Id"],
)

BASE_DATA_DIR = "data"


def _session_data_dir(session_id: str) -> str:
    path = os.path.join(BASE_DATA_DIR, session_id)
    os.makedirs(path, exist_ok=True)
    return path


class AskRequest(BaseModel):
    question: str


@app.post("/ingest")
def ingest_docs(x_session_id: str = Header(default="default")):
    data_dir = _session_data_dir(x_session_id)
    count = ingest(data_dir=data_dir, session_id=x_session_id)
    if count == 0:
        raise HTTPException(status_code=400, detail="no supported files found or all already ingested")
    return {"chunks_stored": count}


@app.post("/ask")
def ask_question(req: AskRequest, x_session_id: str = Header(default="default")):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="question cannot be empty")
    return ask(req.question, session_id=x_session_id)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), x_session_id: str = Header(default="default")):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in SUPPORTED:
        raise HTTPException(status_code=400, detail=f"unsupported file type. allowed: {', '.join(SUPPORTED)}")

    data_dir = _session_data_dir(x_session_id)
    dest = os.path.join(data_dir, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    count = ingest(data_dir=data_dir, session_id=x_session_id)
    return {"filename": file.filename, "chunks_stored": count}
