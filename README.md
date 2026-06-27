## rag-chatbot

little rag chatbot skeleton. feed it some documents & it answers questions using only those.

### retrieval augmented generation workflow

1. chop the given docs into chunks
2. turn each chunk into a vector (a list of numbers to capture its meaning)
3. store vectors in database
4. when you ask a question, turn the question into a vector too
5. grab the chunks closest to your question within given threshold
6. paste resulting chunks into the prompt and let the llm answer using only them

### why it doesn't hallucinate (in theory)

good retrieval. if the right chunk never gets pulled, the model has nothing to work with and starts filling gaps on its own. so this skeleton leans hard on:

- showing the retrieved chunks (debug mode) so you can actually see what the model saw
- a similarity threshold so junk matches get dropped
- returning sources with every answer
- zero internet access for the model 

### stack

- python
- groq for the llm by default (free tier is solid and fast). swappable though
- local embeddings via sentence-transformers (free, no api key, local)
- chroma for the vector store (lives on disk, no server)
- fastapi for the api layer (POST /ingest, POST /ask)
- cli first, react + next.js ui in `frontend/`

### swapping models

the llm and the embeddings are two separate swappable layers -> mix & match possible

- pick your provider in the config
- drop api key in a `.env` file
- run it

### setup

```bash
# clone it
git clone <this-repo>
cd rag-chatbot

# install stuff
pip install -r requirements.txt

# add your keys
cp .env.example .env
# open .env and paste your groq api key

# drop your documents in data/
cp your-doc.txt data/

# ingest your docs (run once, or again when docs change)
python -m src.cli ingest

# start chatting
python -m src.cli chat

# want to see what chunks the model actually saw?
python -m src.cli chat --debug

# or run the api
uvicorn src.api:app --reload
# POST /ingest  -> ingests docs from data/
# POST /ask     -> body: {"question": "your question"}
# POST /upload  -> multipart file upload, saves to data/ and auto-ingests

# frontend (separate terminal)
cd frontend
cp .env.local.example .env.local   # edit if your api runs elsewhere
npm install
npm run dev
# open http://localhost:3000
```

### structure

```
src/
  config.py     pick your providers, read the .env
  loader.py     read documents from the data folder (txt, md, pdf)
  chunker.py    split text into chunks
  embedder.py   turn text into vectors (swappable provider)
  store.py      chroma wrapper for saving and searching vectors
  llm.py        talk to the llm (swappable provider)
  rag.py        ties it all together: ingest docs + answer questions
  cli.py        terminal chat to test it out
  api.py        fastapi app (POST /ingest, POST /ask, POST /upload)
data/           drop your context docs here
frontend/       next.js chat ui
  app/page.js   main chat component
```

### roadmap

- [x] config (load .env, pick providers, hold settings)
- [x] llm provider (groq, swappable, answers from context only)
- [x] embedding provider (local sentence-transformers, swappable)
- [x] vector store (chroma, persists to disk, cosine similarity search)
- [x] loader (reads txt/md from data/) + chunker (overlapping chunks from config)
- [x] rag pipeline (ingest: load, chunk, embed, store / ask: retrieve top-k, inject context, return answer + sources)
- [x] cli (ingest command + chat loop with --debug flag)
- [x] fastapi layer (POST /ingest, POST /ask)
- [x] react + next.js frontend (terminal look, drag-and-drop upload, pink accents, shows sources)
- [x] dedup: ingest skips files already in chroma, so re-uploading or re-running ingest doesn't create duplicate chunks
- [x] pdf support: loader handles .pdf files (text-based, no OCR)
- [x] gemini provider: set `LLM_PROVIDER=gemini` + `GEMINI_API_KEY` in .env to swap llm

### notes

this is a skeleton, not a prod-ready thingie :p 
