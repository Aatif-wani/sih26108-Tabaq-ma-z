# Track 3 — Backend (Flask API)

**Owner:** Muhaimin  
**Depends on:** `ai-engine/` (Babar's retriever + pre-built FAISS index)

## What this does

Wraps the AI engine in a simple HTTP API so Dayan's frontend can call it.

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Confirm the server is up and running |
| `/search` | POST | Search BIS standards by natural language query |

## Setup

```bash
# From the repo root — install BOTH ai-engine and backend deps
pip install -r ai-engine/requirements.txt
pip install -r backend/requirements.txt

# Then run the server from the backend folder
cd backend
python app.py
```

Server starts at **http://localhost:5001**

> The first startup takes ~3-5 seconds while the AI model and FAISS index load.
> Every search after that is fast.

## API reference

### `GET /health`

```
GET http://localhost:5001/health
```

Response `200`:
```json
{"status": "ok", "message": "Backend is running"}
```

---

### `POST /search`

```
POST http://localhost:5001/search
Content-Type: application/json

{
  "query": "cement for building construction",
  "top_k": 5
}
```

| Field | Type | Required | Default | Max |
|---|---|---|---|---|
| `query` | string | ✅ Yes | — | — |
| `top_k` | integer | ❌ No | 5 | 20 |

Response `200`:
```json
{
  "query":   "cement for building construction",
  "top_k":   5,
  "count":   5,
  "results": [
    {
      "rank":             1,
      "standard_id":      "IS 269:2015",
      "title":            "Ordinary Portland Cement — Specification",
      "category":         "Construction & Building Materials",
      "department":       "Cement and Concrete Sectional Committee, CED 2",
      "official_url":     "https://alephindia.in/isi-product/ordinary-portland-cement-is-269-2015.php",
      "status":           "Active",
      "year":             2015,
      "similarity_score": 0.8712
    }
  ]
}
```

Error responses:

| Code | Meaning |
|---|---|
| `400` | Missing `query`, empty query, or non-JSON body |
| `500` | AI engine error (missing index files, model issue) |

## File structure

```
backend/
├── app.py           ← Entry point — run this
├── retriever.py     ← Loads StandardsRetriever with correct absolute paths
├── routes/
│   ├── __init__.py
│   └── search.py    ← /health and /search route handlers
├── requirements.txt ← flask, flask-cors
└── README.md        ← This file
```

## Notes for Dayan (frontend)

- Base URL in dev: `http://localhost:5001`
- CORS is fully enabled — call from any port, no issues
- Always include `Content-Type: application/json` header on POST
- `top_k` defaults to 5 if you don't send it
- Check `similarity_score` — scores below ~0.3 are weak matches
