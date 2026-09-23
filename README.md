# AI Recommendation Engine for Indian Standards in Procurement

**SIH 2026 | Problem ID: SIH26108 | Ministry of Consumer Affairs**

## What this project does

You type in a procurement need (e.g. "cement for building construction") and
the system recommends the most relevant Indian Standards (IS numbers), ranked
by how well they match — using AI-based semantic search, not just keyword
matching.

This is a **search / recommendation tool**, not a chatbot.

## How it works (simple version)

```
Data (BIS standards)  →  AI Engine (embeddings + FAISS)  →  Backend (Flask API)  →  Frontend (website)
      Ilha + Basit              Babar (+ Aatif)                  Muhaimin                Dayan
```

You type a query on the website → it goes to the Flask backend → the backend
asks the AI engine for the closest-matching standards → results come back
ranked, with an IS number, title, category, and a similarity score.

## Folder structure

| Folder | Owner | What's in it |
|---|---|---|
| `data/` | Ilha + Basit | Collected standards data, BIS research, legal/copyright notes |
| `ai-engine/` | Babar (built so far by Aatif while Babar was busy) | Embedding + FAISS search engine — see its own README inside |
| `backend/` | Muhaimin | Flask app and API routes, built around `ai-engine`'s retriever |
| `frontend/` | Dayan | The website / search interface, connects to the backend API |

Each folder has (or will have) its own README with setup instructions specific
to that part. This file is just the map.

## Team

| Person | Job |
|---|---|
| Ilha + Basit | Collect Indian Standards data, research BIS rules on what's legally usable |
| Babar | Build the AI search engine (embeddings + FAISS) |
| Muhaimin | Build the Flask backend and APIs |
| Dayan | Build the frontend website, stay in close contact with Muhaimin |
| Aatif | Connect everything, test it, run the SIH demo |

## Getting started (for any teammate)

```bash
git clone https://github.com/Aatif-wani/sih26108-Tabaq-ma-z.git
cd sih26108-Tabaq-ma-z
```

Then go into your own track's folder and follow the README there. For
example, to run the AI engine:

```bash
cd ai-engine
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python build_embeddings.py
python build_index.py
python retrieve.py "your query here"
```

## Ground rules

- **Talk before you merge** — if you're changing something another track
  depends on (like the API response format), message the team first.
- **Small, frequent commits** beat one giant commit at the end.
- **Pull before you start working** each day: `git pull`.
- Only add data to `data/` that Ilha + Basit have confirmed is legally safe
  to use — see their legal note before reusing anything from BIS.

## Status

- ✅ Data collection — sample batch done (Ilha + Basit)
- ✅ AI engine — working prototype, tested locally (Babar / Aatif)
- ✅ Backend — Flask API completed and verified (Muhaimin)
- ⬜ Frontend — not started (Dayan)
- ⬜ Full integration + demo — not started
