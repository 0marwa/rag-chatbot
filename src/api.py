from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag import ask, ingest

app = FastAPI()


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
