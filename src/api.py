import os
import tempfile

from fastapi import FastAPI, HTTPException, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client

from src.config import settings
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

_storage = create_client(settings.supabase_url, settings.supabase_service_role_key).storage


class AskRequest(BaseModel):
    question: str


@app.post("/ingest")
def ingest_docs(x_session_id: str = Header(default="default")):
    # list files in the session's storage folder and ingest them
    files = _storage.from_(settings.supabase_bucket).list(x_session_id)
    if not files:
        raise HTTPException(status_code=400, detail="no files found for this session")

    # download each file to a temp dir and ingest
    with tempfile.TemporaryDirectory() as tmp:
        for f in files:
            path = f"{x_session_id}/{f['name']}"
            data = _storage.from_(settings.supabase_bucket).download(path)
            with open(os.path.join(tmp, f["name"]), "wb") as out:
                out.write(data)
        count = ingest(data_dir=tmp, session_id=x_session_id)

    if count == 0:
        raise HTTPException(status_code=400, detail="all files already ingested")
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

    contents = await file.read()

    # store under session_id/filename so sessions are isolated in the bucket
    storage_path = f"{x_session_id}/{file.filename}"
    _storage.from_(settings.supabase_bucket).upload(
        path=storage_path,
        file=contents,
        file_options={"content-type": "application/octet-stream", "upsert": "true"},
    )

    # ingest directly from the uploaded bytes via a temp file
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = os.path.join(tmp, file.filename)
        with open(tmp_path, "wb") as f:
            f.write(contents)
        count = ingest(data_dir=tmp, session_id=x_session_id)

    return {"filename": file.filename, "chunks_stored": count}
