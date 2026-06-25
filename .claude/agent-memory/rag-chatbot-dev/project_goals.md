---
name: project-goals
description: Core goal and scope of the rag-chatbot skeleton project
metadata:
  type: project
---

rag-chatbot is a skeleton RAG chatbot: give it any context (docs), it answers questions solely from that context. Strict "answer only from provided context, else say I don't know" behavior.

**Why:** User wants a reusable, generic skeleton — not tied to one domain. They built a quran-specific RAG bot once but have forgotten the details since.

**How to apply:** Keep it generic and extensible. Two independently swappable layers: LLM provider and embedding provider (they don't have to be the same vendor). Anyone using it should be able to pick a provider and drop in their own API key via .env, no code changes. Default dev LLM = Groq (best free tier, fast, OpenAI-compatible). Embeddings default = local sentence-transformers (free, no key). Vector store leaning Chroma (local, persistent, simple). Favor simple over clever.
