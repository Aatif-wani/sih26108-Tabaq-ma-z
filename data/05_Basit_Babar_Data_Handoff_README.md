**BIS Data Handoff — README**

From: Ilha & Basit (Data Collection + BIS Research) → To: Babar (AI
Engine — Embeddings + FAISS)

1\. Project

SIH 2026 — AI Recommendation Engine for Indian Standards in Procurement.
A search & recommendation tool (not a chatbot): a user types a
procurement need and gets matching Indian Standards, ranked by
relevance.

2\. Problem ID

SIH26108 — Ministry of Consumer Affairs, Food and Public Distribution.

3\. Purpose of this data package

To let you (Babar) start building embeddings + FAISS immediately, using
real, BIS-sourced data, without needing to ask us what any field means.
Everything here was collected and cross-checked against official BIS
sources — see File 03 for exactly what that means for how we're allowed
to use it.

4\. Files included

|                                         |                                                                                                                                                                           |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **File**                                | **What it is / why it exists**                                                                                                                                            |
| 01_BIS_Data_Field_Specification.xlsx    | Defines every candidate data field (Field Specification sheet), which minimal set to embed (Recommended Babar Input sheet), and a coding-reference Data Dictionary sheet. |
| 02_BIS_Sample_Standards_20_30.xlsx      | 22 real, sourced Indian Standards across 12 procurement categories, in spreadsheet form, with a Collection Summary sheet.                                                 |
| 03_BIS_Copyright_and_Data_Use_Note.docx | What's safe to use/store/display vs. what needs BIS permission. Read before building any UI that shows standard text.                                                     |
| 04_BIS_Category_Taxonomy.docx           | 12 practical categories for filtering/search, with guidance on how to use them in the AI engine.                                                                          |
| 05_Basit_Babar_Data_Handoff_README.docx | This document — read it first.                                                                                                                                            |
| 07_BIS_Standards_Master_Dataset.xlsx    | The clean, machine-ready dataset — one row per standard, includes embedding_text and metadata_json, plus a Validation Report sheet. THIS is the file to load in Python.   |

5\. What each file contains

Covered in the table above — File 01 tells you what each field means,
File 02/07 hold the actual standards, File 03 covers legal/copyright
boundaries, and File 04 gives you a ready-made category list.

6\. Recommended MVP data structure

standard_number + title + description_or_scope + keywords, concatenated
into embedding_text (already pre-built for you in File 07). category and
official_bis_url are kept as metadata alongside the vector, not embedded
into it.

7\. Which fields you should use for embeddings

- embedding_text — the ONLY field to feed into the embedding model. It's
  already built from title + description_or_scope + keywords using the
  template: \[STANDARD NUMBER\] \[TITLE\]. \[DESCRIPTION_OR_SCOPE\].
  \[KEYWORDS\].

- Do not embed official_bis_url, source, or metadata_json — these are
  for display/filtering, not semantic search.

8\. Which fields should remain metadata

- standard_number, official_bis_url — always return these with a result
  so the user can click through to the real standard.

- category, sector, certification_relevance — useful for filtering (see
  File 04) or for showing a “why this matched” line in the UI (Dayan's
  job).

- metadata_json — a bundled convenience field for Muhaimin's backend if
  he wants secondary fields without extra columns.

9\. Category usage

See File 04 in full. Short version: treat category as a metadata filter
first; only fold it into embedding_text later if testing shows it's
needed (unlikely for a 20–30-standard MVP).

10\. How to handle missing fields

Several rows have fields marked NULL in File 07 (or “Not available on
reviewed BIS page” in File 02) — this means we could not confirm that
detail on an official BIS page in the time available, NOT that we
guessed and left it blank by mistake. Treat NULL as “unknown,” never as
zero, empty-string-means-false, or any other silent assumption.
embedding_text is built to gracefully skip a NULL description_or_scope
rather than embedding the literal word “NULL” — check File 07's
Validation Report sheet, which confirms zero empty embedding_text rows.

11\. How to handle duplicate standards

File 07's Validation Report confirms zero duplicate standard_numbers in
this batch. If you add more standards later and find a duplicate (e.g.
two rows for the same IS number but different years), keep the most
recent edition unless you specifically need to compare historical
versions, and note the older one as superseded rather than deleting it
outright.

12\. How to handle revisions/amendments

Indian Standards get revised and sometimes withdrawn (see IS 2062:2011
in File 02/07, which is flagged as being split into Part 1/Part 2 as of
2026). status_revision/revision_information notes what we found at
collection time, but this is not something to snapshot once and forget —
before the SIH demo, it's worth spot-checking that the standards we're
showing haven't been superseded.

13\. How to use official BIS links

Always preserve official_bis_url and show it with every result returned
to the user (Dayan's frontend job card explicitly asks for this: “Link
out to the official BIS page instead of showing full copyrighted text”).
Never replace it with a scraped/cached copy of the standard's content —
see File 03.

14\. Copyright/usage precautions

Full detail in File 03. The short version: we can store and show
metadata (numbers, titles, our own short paraphrases, links) — we should
not store or display full standard text, and the app should always say
results are similarity-based, not legal or compliance confirmation.

15\. Known limitations

- 22 standards collected, not the full 20–30 target headroom — a
  deliberate tradeoff to keep every single one real and sourced rather
  than padding the count. See Section 17 for how to extend it.

- Update: the description_or_scope gap has been closed — all 22 rows now
  carry a real, sourced scope summary (see File 07's Validation Report:
  NULL cells dropped from 28 to 17 across the whole dataset).
  department_division and amendment_information remain unavailable for
  some rows and are honestly marked NULL rather than guessed — a
  follow-up lookup can fill these later if the team wants richer
  metadata, but nothing blocks Babar on this.

- Fixed: IS 269:2015's official_bis_url previously pointed to a
  third-party consultancy summary — it now points to an official BIS
  ‘Standard Review’ page (services.bis.gov.in). Two other rows' status
  was corrected during the same pass: IS 4990:2011 and IS 2347:2017 were
  found to be superseded by newer editions (IS 4990:2024 and IS
  2347:2023 respectively) — both are now flagged in their
  status_revision column rather than presented as current.

- Category assignments (File 04) are our own team-created taxonomy, not
  an official BIS classification — reasonable, but not authoritative.

16\. What Babar can start building immediately

Everything. File 07 is machine-ready right now — 22 valid rows, zero
duplicates, zero broken/malformed URLs, zero empty embedding_text,
consistent field names throughout.

17\. Questions/uncertainties requiring team confirmation

- Whether to prioritise widening category coverage (more sectors) or
  deepening existing rows (filling the NULL description_or_scope fields)
  before the demo — worth a quick team call.

- The three open legal questions listed at the end of File 03.

- Whether IS 2062:2011's in-progress Part 1/Part 2 split (flagged in
  File 02/07) should be reflected now or left as-is for the MVP demo.

START HERE — Babar

Open 07_BIS_Standards_Master_Dataset.xlsx.

Read the embedding_text column — it's already built for you.

Load the sheet with pandas/openpyxl in Python.

Generate embeddings from embedding_text using a ready-made Hugging Face
model (per your own job card — don't build your own model).

Build a FAISS index over those embeddings.

Keep standard_number, official_bis_url, category and the rest as
metadata alongside the FAISS index — not inside it.

Return the top 3–5 matches with similarity scores.

Always include the official_bis_url for every result you return, so the
frontend can link out to it.
