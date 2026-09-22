"""
Track 2 - Step C: Build and save a FAISS index from the standards embeddings.

Run build_embeddings.py first. This script loads standards_embeddings.npy,
builds a FAISS index (cosine similarity via inner product on normalized
vectors), and saves it to disk so retrieve.py / the Flask backend can load
it instantly without re-embedding anything.

Usage:
    python build_index.py
"""

import numpy as np
import faiss

EMBEDDINGS_PATH = "standards_embeddings.npy"
INDEX_PATH = "standards.index"


def main():
    embeddings = np.load(EMBEDDINGS_PATH).astype("float32")
    n, dim = embeddings.shape
    print(f"Loaded {n} embeddings of dimension {dim}")

    # IndexFlatIP = exact inner-product search. Since embeddings are
    # normalized (see build_embeddings.py), inner product == cosine
    # similarity. Flat/exact is fine at this scale (tens-thousands of
    # standards); swap for IVF/HNSW only if the dataset grows huge.
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    print(f"Saved FAISS index: {INDEX_PATH}  (ntotal={index.ntotal})")


if __name__ == "__main__":
    main()
