"""
Track 2 - Step C: Query-time retrieval module.

Flask backend usage:
    from retrieve import StandardsRetriever
    retriever = StandardsRetriever()          # load once at startup
    results = retriever.search("cement for building construction", top_k=5)

Standalone test:
    python retrieve.py "cement for building construction"
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

# Paths are relative to THIS file, so it works no matter which folder
# you start Flask or Python from.
BASE_DIR = Path(__file__).resolve().parent

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = BASE_DIR / "standards.index"
METADATA_PATH = BASE_DIR / "standards_metadata.csv"

# Results scoring below this are flagged as "not confident".
# Tune it after checking real scores (correct matches vs. no-match queries).
MIN_SCORE = 0.40


class StandardsRetriever:
    def __init__(self,
                 model_name: str = MODEL_NAME,
                 index_path=INDEX_PATH,
                 metadata_path=METADATA_PATH,
                 min_score: float = MIN_SCORE):
        self.min_score = min_score
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(str(index_path))
        self.metadata = pd.read_csv(metadata_path).fillna("")

        if self.index.ntotal != len(self.metadata):
            raise ValueError(
                f"Index has {self.index.ntotal} vectors but metadata has "
                f"{len(self.metadata)} rows - rebuild embeddings/index together."
            )

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Returns up to top_k dicts with the standard's metadata, a
        similarity_score (higher = more relevant) and a 'confident' flag
        (True if the score is at or above min_score).
        """
        query = (query or "").strip()
        if not query:
            return []

        top_k = max(1, min(int(top_k), self.index.ntotal))

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

            score = float(score)
            results.append({
                "standard_id": str(row["standard_id"]),
                "title": str(row["title"]),
                "category": str(row["category"]),
                "department": str(row["department"]),
                "official_url": str(row["official_url"]),
                "status": str(row["status"]),
                "year": year_val,
                "similarity_score": round(score, 4),
                "confident": score >= self.min_score,
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

    if not results[0]["confident"]:
        print(f"(No confident match - top score is below {retriever.min_score})\n")

    for i, r in enumerate(results, 1):
        flag = "" if r["confident"] else "  [low confidence]"
        print(f"{i}. [{r['similarity_score']}] {r['standard_id']} - {r['title']}{flag}")
        print(f"   Category: {r['category']} | Status: {r['status']} | Year: {r['year']}")
        print(f"   {r['official_url']}\n")


if __name__ == "__main__":
    main()