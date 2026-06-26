# rag-chatbot

a little rag chatbot skeleton. you feed it some documents, it answers questions using only those documents. that's the whole vibe. no making stuff up, no "well actually" from the void, just answers grounded in what you gave it.

think of it like giving someone a stack of notes and saying "only answer from these". if it's not in the notes, the bot says it doesn't know instead of hallucinating nonsense.

## what is rag anyway

rag = retrieval augmented generation. fancy words for a simple idea:

1. take your docs, chop them into chunks
2. turn each chunk into a vector (a list of numbers that captures its meaning)
3. shove those vectors in a little database
4. when you ask a question, turn the question into a vector too
5. grab the chunks closest to your question
6. paste those chunks into the prompt and let the llm answer using only them

so the model never answers from its own memory. it only sees the chunks we hand it. that's the trick to keeping it honest.

## why it doesn't hallucinate (in theory)

the secret sauce isn't a strict prompt. it's good retrieval. if the right chunk never gets pulled, the model has nothing to work with and starts filling gaps on its own. so this skeleton leans hard on:

- showing you the retrieved chunks (debug mode) so you can actually see what the model saw
- a similarity threshold so junk matches get dropped
- returning sources with every answer
- zero internet access for the model. its only world is the chunks

## stack

- python
- groq for the llm by default (free tier is solid and fast). swappable though
- local embeddings via sentence-transformers (free, no api key, stays on your machine)
- chroma for the vector store (lives on disk, no server to babysit)
- cli first. react + next.js ui and an api come later

## swapping models

the whole point is you're not locked in. the llm and the embeddings are two separate swappable layers, so you can mix and match.

- pick your provider in the config
- drop your api key in a `.env` file
- run it

no code changes needed. wanna use openai instead of groq? cool. wanna run everything local with ollama? also cool. you bring the key, it works.

## getting started

(coming once the code's actually here, hang tight)

```bash
# clone it
git clone <this-repo>
cd rag-chatbot

# install stuff
pip install -r requirements.txt

# add your keys
cp .env.example .env
# then open .env and paste your key

# drop your documents in data/
# then run the cli
python -m src.cli
```

## structure

```
src/
  config.py     pick your providers, read the .env
  loader.py     read documents from the data folder
  chunker.py    split text into chunks
  embedder.py   turn text into vectors (swappable provider)
  store.py      chroma wrapper for saving and searching vectors
  llm.py        talk to the llm (swappable provider)
  rag.py        ties it all together: ingest docs + answer questions
  cli.py        terminal chat to test it out
data/           drop your context docs here
```

## roadmap

- [x] config (load .env, pick providers, hold settings)
- [x] llm provider (groq, swappable, answers from context only)
- [x] embedding provider (local sentence-transformers, swappable)
- [x] vector store (chroma, persists to disk, cosine similarity search)
- [x] loader (reads txt/md from data/) + chunker (overlapping chunks from config)
- [ ] ingest pipeline (load, chunk, embed, store)
- [ ] retrieval + answer with sources
- [ ] cli with debug mode
- [ ] fastapi layer
- [ ] react + next.js frontend

## notes

this is a skeleton, not a production thing. it's meant to be easy to read and easy to extend. if something feels overengineered, it probably is, call it out.
