## rag-chatbot

little rag chatbot skeleton. feed it some documents & it answers questions using only those.

### stack

- python
- groq for the llm by default (free tier is solid and fast). swappable though
- embeddings via together.ai api by default (keeps ram low for deployment). sentence-transformers still available for local dev
- supabase pgvector for the vector store (session-isolated, hosted)
- supabase storage for uploaded files
- fastapi for the api layer, deployed on railway
- react + next.js ui in `frontend/`, deployed on vercel

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

### notes

meow  
