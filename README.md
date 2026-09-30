# Tabaq Ma:z — Semantic Search for Indian Standards

**SIH26108 · Team Tabaq Ma:z**

> Describe what you're buying in plain words. Get the right Indian Standards, ranked, with current status, edition year and a link to the official BIS page.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/API-Flask-lightgrey)
![FAISS](https://img.shields.io/badge/Vector%20Search-FAISS-green)
![Model](https://img.shields.io/badge/Embeddings-all--MiniLM--L6--v2-orange)
![Status](https://img.shields.io/badge/Status-Working%20Prototype-brightgreen)

---

## The Problem

Somewhere in a district office, an engineer is writing a tender for 2,000 office chairs. The specification needs an Indian Standard. She searches online, finds an old PDF, a 2017 circular and a forum thread, and copies the IS number that looks right. Sometimes it is right. Sometimes it's an edition BIS replaced years ago, and nobody notices until a supplier disputes the order.

This is a **language gap**. BIS publishes around **23,890 standards**, and their titles are written for engineers ("Work Chairs - Specification"). Tenders are written the way people talk ("revolving chairs for government office"). Keyword search can't bridge the two, so references go missing, go stale or go wrong. The result: poor-quality supplies, disputes and re-tendering.

## The Solution

A semantic recommendation engine that matches **meaning, not spelling**.

| Query | Top result | Why keyword search fails |
|---|---|---|
| `Safety shoes for factory workers` | IS 15298 (Part 2):2024 | The title says "Safety **Footwear**", not shoes |
| `Code of practice for RCC structural design` | IS 456:2000 | "RCC" is only an abbreviation |

Each result includes: IS number · title · category · status · edition year · similarity score · link to the official BIS page.

## What Makes It Different

- **It knows when to say "I don't know."** If even the best match scores below **0.40** cosine similarity, the UI shows *"No confident match"* instead of a shaky list. In procurement, a confident wrong answer is worse than none.
- **It cannot invent a standard.** There is no generative model. Every result is a real row from a verified catalogue, with a link back to BIS.
- **It speaks procurement, not BIS.** Tested on how officials actually type: abbreviations (MCB, N95, XLPE, RCC), everyday phrasing ("bags for storing 50 kg wheat", "ISI helmet for bike riders") and scheme language ("fortified rice for mid day meal scheme").
- **It respects the source.** Every edition was checked on the official BIS Standards Portal. Scopes and keywords are written by our team in our own words. We store **only metadata**, never the text of a standard.
- **It runs anywhere.** Open-source model, CPU-only, no paid APIs, no cloud vector database.

## How It Works

```
                 OFFLINE (once)
 ┌──────────────┐   ┌─────────────────┐   ┌────────────────┐   ┌──────────────┐
 │ Standards    │ → │ title + scope + │ → │ all-MiniLM-L6  │ → │ FAISS        │
 │ metadata CSV │   │ keywords + cat. │   │ 384-d vectors  │   │ IndexFlatIP  │
 └──────────────┘   └─────────────────┘   └────────────────┘   └──────────────┘

                 ONLINE (per query)
 ┌──────────┐  POST /search  ┌───────────┐  embed  ┌───────────┐  top-k  ┌─────────┐
 │ Web page │ ─────────────→ │ Flask API │ ──────→ │ Retriever │ ──────→ │ Results │
 └──────────┘                └───────────┘         └───────────┘         └─────────┘
                                                        │
                                          best score < 0.40 → "No confident match"
```

1. **Collect** standards metadata and confirm the current edition on the BIS Standards Portal.
2. **Combine** title, scope, keywords and category into one text per standard.
3. **Embed** each text into a 384-number vector with `all-MiniLM-L6-v2` (Sentence-Transformers).
4. **Index** vectors in FAISS `IndexFlatIP` for exact cosine-similarity search.
5. **Query:** the same model embeds the user's query; FAISS returns the closest standards (top 3–20); the retriever abstains if the best score is under 0.40.

## Current Status

| Component | State |
|---|---|
| **Data** | 136 real standards across 19 procurement categories (133 active, 2 under revision, 1 withdrawn / being replaced) |
| **AI engine** | Embedding + indexing scripts, retriever with confidence threshold |
| **Backend** | Flask REST API: `GET /health`, `POST /search` |
| **Frontend** | Search page with example queries, result-count selector, backend status indicator, "No confident match" notice, recent searches |
| **Evaluation** | 30 hand-labelled queries (easy, paraphrase, abbreviation, no-match), scored with Recall@3 and Recall@5 |

**Categories covered:** construction, steel, cables and electrical equipment, household appliances, lighting, PPE, water supply, food products and packaging, quality testing, solar energy, fire safety, office furniture, medical supplies, textiles, transport, management systems.

Each record holds: standard number, title, scope, keywords, category, committee, status, edition year and official BIS URL.

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/Aatif-wani/sih26108-Tabaq-ma-z.git
cd sih26108-Tabaq-ma-z
pip install -r requirements.txt
```

### Build the index

```bash
python build_embeddings.py   # encode every standard into a 384-d vector
python build_index.py        # build the FAISS index
```

### Run the API

```bash
python app.py                # adjust to your backend entry point
```

### Open the web page

Open the frontend `index.html` in your browser (or serve it from the backend), then type what you're buying.

## API Reference

### `GET /health`
Returns backend status.

### `POST /search`

**Request**
```json
{
  "query": "safety shoes for factory workers",
  "top_k": 5
}
```
`top_k` accepts values up to **20**.

**Response (illustrative)**
```json
{
  "query": "safety shoes for factory workers",
  "confident": true,
  "results": [
    {
      "is_number": "IS 15298 (Part 2)",
      "title": "Safety Footwear",
      "category": "PPE",
      "status": "Active",
      "edition_year": 2024,
      "score": 0.71,
      "url": "https://..."
    }
  ]
}
```
If the best score is below 0.40, the page shows *"No confident match"* rather than a list.

> Field names above are illustrative; see the backend code for the exact schema.

## Evaluation

We score retrieval on **30 hand-labelled queries** written the way officials actually type, covering easy lookups, paraphrases, abbreviations, and a no-match case. Metrics:

- **Recall@3** — how often the correct standard is in the top 3
- **Recall@5** — how often it is in the top 5

The confidence threshold (0.40) was tuned by comparing scores for correct matches against queries with no right answer.

## Scaling the Dataset

The catalogue grew from **22 → 136 standards without changing a line of code**. The route is always the same:

1. Look up the standard's current edition on the BIS portal (`fetch_bis_standards.py` helps).
2. Write the scope and keywords in your own words.
3. Add the row to the CSV.
4. Re-run `build_embeddings.py` and `build_index.py`.

The model, API and web page don't change. The full BIS catalogue at 384 numbers per standard is roughly **37 MB** of vectors, which exact FAISS search handles on a laptop CPU. Approximate indexes (IVF, HNSW) are available if we ever need more.

## Roadmap

### Phase 1 — Language and data *(before the finale)*
- [ ] Swap to `paraphrase-multilingual-MiniLM-L12-v2` (50 languages incl. Hindi, Urdu, Marathi, Gujarati; same 384-d vectors) by changing the model name in `build_embeddings.py` and `retrieve.py`, rebuilding the index, and re-testing on translated queries. LaBSE (109 languages) is the fallback for wider coverage.
- [ ] Add current-status, superseded-by and amendment fields, synced periodically against BIS listings, so the engine flags when a cited edition has been replaced.
- [ ] Keep growing the catalogue category by category, starting with the most-procured products.

### Phase 2 — Compliance intelligence *(at the finale)*
- [ ] Certification table sourced from BIS Quality Control Orders: ISI mark (BIS Product Certification), CRS registration, Hallmarking.
- [ ] Relationship table linking each standard to its test-method, terminology, safety and installation companions, so one query returns the full compliance bundle.

### Phase 3 — Platform integration *(towards a pilot)*
- [ ] PDF and DOCX tender upload, with item-wise query splitting.
- [ ] API hardening: authentication, rate limiting, OpenAPI spec, so e-procurement portals such as GeM can call it safely.
- [ ] Feedback loop: queries where officials pick no result become new test cases.

**Finale goal:** an official uploads a tender PDF and, for each item, gets the right standard, its current edition, any mandatory certification, and the companion standards to cite with it, in the language she typed in.

## Impact

- **Officials** spend less time hunting and make fewer missed or outdated references.
- **Departments and PSEs** see fewer disputes, rejections and re-tenders, and more consistent specifications: the same query gets the same answer in every office.
- **Vendors** get clearer specifications to supply against.
- **Citizens** get safer, better-quality products bought with public money.
- The stack is free and open-source, so any department can adopt it without licence costs.

## Tech Stack

Python · Sentence-Transformers · FAISS · pandas · NumPy · Flask · flask-cors · HTML/CSS/JavaScript · Git/GitHub

*Planned:* PDF/DOCX text extraction.

## Team Tabaq Ma:z

| Member | Contribution |
|---|---|
| **Ilha & Basit** | Data collection, research on BIS usage rules |
| **Aatif** | AI engine |
| **Muhaimin** | Backend |
| **Dayan** | Frontend |
| **Babar & Aatif** | Integration and testing |

## Data Use Note

This repository stores **only metadata** about Indian Standards (number, title, category, status, edition year, URL) plus scopes and keywords written by the team in our own words. It does **not** contain the text of any standard. Always confirm the current edition on the official [BIS Standards Portal](https://standards.bis.gov.in) before citing a standard in a tender.

## Disclaimer

This is a prototype built for the Smart India Hackathon. Results are recommendations to speed up research, not a substitute for verifying the standard on the official BIS portal.
