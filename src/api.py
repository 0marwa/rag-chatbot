import os
import shutil

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.rag import ask, ingest

app = FastAPI()

# allow the next.js dev server to call the api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
ALLOWED_EXTENSIONS = {".txt", ".md"}


class AskRequest(BaseModel):
    question: str


@app.post("/ingest")
def ingest_docs():
    count = ingest()
    if count == 0:
        raise HTTPException(status_code=400, detail="no supported files found in data/")
    return {"chunks_stored": count}


@app.post("/ask")
def ask_question(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="question cannot be empty")
    return ask(req.question)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"unsupported file type. allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    dest = os.path.join(DATA_DIR, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # auto-ingest after upload
    count = ingest()
    return {"filename": file.filename, "chunks_stored": count}
