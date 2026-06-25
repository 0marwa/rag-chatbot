# rag-chatbot — Project Tracker

A skeleton RAG chatbot: give it any context (documents), it answers questions **solely from that context**. Swappable LLM and embedding providers — pick one, drop your API key in `.env`, no code changes.

This file is the shared tracker for both of us. What we decided, what's done, what's next.

---

## How RAG works (quick reference)

**Ingest (once):** docs → chunk → embed each chunk → store vectors in a DB.
**Query (each question):** embed question → similarity-search top-k chunks → inject chunks into prompt → LLM answers using only them.

The strict "answer only from context" prompt is the **last 10%**. Retrieval quality is the other 90%. Most hallucinations come from bad retrieval (the right chunk never reached the model) or the model having web/training access instead of being limited to the injected context. Guardrails we'll use: show retrieved chunks in debug mode, similarity threshold, return sources, no internet access for the model.

---

## Decisions made

- **Scope:** generic skeleton, not domain-specific. Any context in, grounded answers out.
- **LLM provider:** abstraction layer, swappable. Dev default = **Groq** (best free tier, fast, OpenAI-compatible).
- **Embedding provider:** separate swappable layer. Default = **local sentence-transformers** (free, no key, private). Independent from the LLM choice.
- **Vector store:** **Chroma** (local, persists to disk, no server).
- **Config:** `.env` for API keys + small config module to select providers.
- **Language:** Python, type hints, minimal deps.
- **Interface order:** CLI first → then React + Next.js UI + API (FastAPI) later. RAG core stays a clean module; interfaces sit on top.
- **Docs:** detailed `README.md` (setup, provider selection, add your key, ingest, run).

## Open questions

- Which providers to ship in the LLM interface at launch besides Groq? (OpenAI / Gemini / Mistral / Ollama — likely add incrementally)
- Chunk size + overlap defaults — to be tuned once we test on real docs.
- Document formats to support first (txt / md / pdf?).

---

## Status: structure scaffolded. README + config files written. src/ files are empty stubs. First commit pending (user commits manually).

## Done

- Project structure: `src/` (config, loader, chunker, embedder, store, llm, rag, cli + __init__) and `data/`.
- `README.md` — all lowercase, casual voice, no emojis/em dashes.
- `.env.example` — provider keys + LLM_PROVIDER / EMBEDDING_PROVIDER switches.
- `.gitignore` — ignores .env, chroma_db, data contents (keeps .gitkeep).
- `requirements.txt` — groq, sentence-transformers, chromadb, python-dotenv.

## Next steps

1. Fill in provider interfaces: `llm.py` (Groq first), `embedder.py` (sentence-transformers first).
2. Pipeline modules: `loader.py`, `chunker.py`, `store.py` (Chroma), `rag.py` (ingest + ask).
3. `cli.py` — terminal chat with debug mode (show retrieved chunks + sources).
4. Later: FastAPI layer + React/Next.js frontend.
