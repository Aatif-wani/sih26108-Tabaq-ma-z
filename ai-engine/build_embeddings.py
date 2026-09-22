"""
Track 2 - Step B: Build embeddings for the standards dataset.

Reads standards_dataset.csv (standard_id, title, scope, category, department,
keywords, official_url, status, year), combines the useful text fields into
one string per standard, embeds them with a Sentence-Transformers model, and
saves the embeddings + row metadata to disk for build_index.py to consume.

Usage:
    python build_embeddings.py
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_PATH = "standards_dataset.csv"
MODEL_NAME = "all-MiniLM-L6-v2"   # small, fast, good baseline for a prototype
OUT_EMBEDDINGS = "standards_embeddings.npy"
OUT_METADATA = "standards_metadata.csv"


def build_embedding_text(row) -> str:
    """
    Combine title + scope + keywords + category into one text blob per
    standard. This is the text that actually gets embedded.

    Scope is often missing in this sample batch (Ilha/Basit's notes flag
    it as 'not yet retrieved' for several standards) - the model still
    gets useful signal from title, category, and keywords in that case.
    """
    parts = [
        str(row.get("title", "") or ""),
        str(row.get("scope", "") or ""),
        str(row.get("keywords", "") or ""),
        f"Category: {row.get('category', '') or ''}",
    ]
    return ". ".join(p.strip() for p in parts if p and str(p).strip())


def main():
    df = pd.read_csv(DATA_PATH).fillna("")
    print(f"Loaded {len(df)} standards from {DATA_PATH}")

    df["embedding_text"] = df.apply(build_embedding_text, axis=1)

    empty_scope = (df["scope"].str.strip() == "").sum()
    print(f"Note: {empty_scope}/{len(df)} rows have no scope text "
          f"(embedding falls back to title + keywords + category for those)")

    print(f"Loading model: {MODEL_NAME} ...")
    model = SentenceTransformer(MODEL_NAME)

    print("Encoding standards...")
    embeddings = model.encode(
        df["embedding_text"].tolist(),
        show_progress_bar=True,
        normalize_embeddings=True,  # so cosine similarity == dot product
    )
    embeddings = np.asarray(embeddings, dtype="float32")

    np.save(OUT_EMBEDDINGS, embeddings)
    df.to_csv(OUT_METADATA, index=False)

    print(f"Saved embeddings: {OUT_EMBEDDINGS}  shape={embeddings.shape}")
    print(f"Saved metadata:   {OUT_METADATA}")


if __name__ == "__main__":
    main()
