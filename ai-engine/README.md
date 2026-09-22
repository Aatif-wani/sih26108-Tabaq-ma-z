# Track 2 — AI Recommendation Engine (Embeddings + FAISS)

Turns a procurement query into a ranked list of matching Indian Standards.

## Files

| File | What it does |
|---|---|
| `standards_dataset.csv` | Input data from Ilha + Basit (standard_id, title, scope, category, department, keywords, official_url, status, year) |
| `build_embeddings.py` | Combines title + scope + keywords + category into one text per standard, embeds it, saves `standards_embeddings.npy` + `standards_metadata.csv` |
| `build_index.py` | Builds a FAISS index from the saved embeddings, saves `standards.index` |
| `retrieve.py` | The actual search function — `StandardsRetriever().search(query, top_k=5)`. **This is the module Muhaimin imports into Flask.** Also runnable standalone: `python retrieve.py "your query here"` |
| `eval_queries.csv` | 15 test queries with the expected correct standard, mixing easy/medium/hard/no-match cases |
| `evaluate.py` | Runs every query in `eval_queries.csv` through the retriever and prints Recall@3 / Recall@5 plus a failure log |
| `requirements.txt` | `pip install -r requirements.txt` |

## How to run it (in order)

```bash
pip install -r requirements.txt

python build_embeddings.py   # step 1: embed the standards
python build_index.py        # step 2: build the FAISS index
python retrieve.py "cement for building construction"   # step 3: try a query
python evaluate.py           # step 4: check retrieval quality
```

Re-run `build_embeddings.py` + `build_index.py` any time `standards_dataset.csv`
changes (new standards, edited scope text, etc). `retrieve.py` and `evaluate.py`
just load the saved files — they're fast and don't need to be re-run at the
same time.

## Model

Using `all-MiniLM-L6-v2` from Sentence-Transformers — small, fast, good
baseline for a prototype. No training involved, no cloud vector DB — just a
local FAISS flat index, which is exact (not approximate) and plenty fast for
a dataset this size (fine up into the tens of thousands of standards).

## ⚠️ One thing to know before you run this

I built and wrote all of this code in this chat, but **I could not actually
run `build_embeddings.py` here** — this sandbox's internet access is locked
to package registries (PyPI, npm, GitHub) and can't reach `huggingface.co`,
which is where the embedding model itself gets downloaded from on first run.
I confirmed FAISS itself works fine in here (index build/save/load all
tested clean with dummy vectors) — it's only the model download that's
blocked in this environment.

So: **the code is complete and correct, but genuinely untested end-to-end.**
When you run it on your own laptop or Google Colab (normal internet), the
first run of `build_embeddings.py` will download the model (~90MB, one-time,
then cached) and everything should just work. If something breaks on your
machine, paste me the error and I'll fix it — I just can't pre-verify that
last mile from here.

## Current dataset size

22 sample standards (from Ilha + Basit's first batch). Good enough to prove
the pipeline works end-to-end; ask them for the fuller batch once Track 1
grows past this sample, then just re-run steps 1–2 above — nothing else
needs to change.
