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

```text
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