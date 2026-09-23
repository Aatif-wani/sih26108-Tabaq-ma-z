"""
Track 2 - Step C: Query-time retrieval module.

This is the piece Muhaimin's Flask backend imports directly - it should
NOT duplicate this logic inside a route. Loads the model + FAISS index +
metadata once, then answers search(query, top_k) calls cheaply.

Usage (standalone test):
    python retrieve.py "cement for building construction"

Usage (as a module, e.g. from Flask):
    from retrieve import StandardsRetriever
    retriever = StandardsRetriever()
    results = retriever.search("cement for building construction", top_k=5)
"""

import sys
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "standards.index"
METADATA_PATH = "standards_metadata.csv"


class StandardsRetriever:
    def __init__(self,
                 model_name: str = MODEL_NAME,
                 index_path: str = INDEX_PATH,
                 metadata_path: str = METADATA_PATH):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_path)
        self.metadata = pd.read_csv(metadata_path).fillna("")

        if self.index.ntotal != len(self.metadata):
            raise ValueError(
                f"Index has {self.index.ntotal} vectors but metadata has "
                f"{len(self.metadata)} rows - rebuild embeddings/index together."
            )

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Returns a list of up to top_k dicts, each with the standard's
        metadata plus a similarity_score (0-1, higher = more relevant).
        """
        query = (query or "").strip()
        if not query:
            return []

        q_emb = self.model.encode([query], normalize_embeddings=True)
        q_emb = np.asarray(q_emb, dtype="float32")

        scores, indices = self.index.search(q_emb, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            row = self.metadata.iloc[idx]
            year_val = row["year"]
            if hasattr(year_val, "item"):
                year_val = year_val.item()

            results.append({
                "standard_id": str(row["standard_id"]),
                "title": str(row["title"]),
                "category": str(row["category"]),
                "department": str(row["department"]),
                "official_url": str(row["official_url"]),
                "status": str(row["status"]),
                "year": year_val,
                "similarity_score": round(float(score), 4),
            })
        return results


def main():
    query = " ".join(sys.argv[1:]) or "cement for building construction"
    retriever = StandardsRetriever()
    results = retriever.search(query, top_k=5)

    print(f"\nQuery: {query!r}\n")
    if not results:
        print("No results.")
        return
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['similarity_score']}] {r['standard_id']} - {r['title']}")
        print(f"   Category: {r['category']} | Status: {r['status']} | Year: {r['year']}")
        print(f"   {r['official_url']}\n")


if __name__ == "__main__":
    main()
