"""
Track 2 - Step D: Evaluate retrieval quality against eval_queries.csv.

For each labelled query, checks whether the expected standard_id shows up
in the top-3 / top-5 results, and prints a simple metrics summary plus a
failure log (queries where the expected standard did NOT show up in top-5).

Usage:
    python evaluate.py
"""

import pandas as pd
from retrieve import StandardsRetriever

EVAL_PATH = "eval_queries.csv"


def main():
    eval_df = pd.read_csv(EVAL_PATH).fillna("")
    retriever = StandardsRetriever()

    hits_at_3 = 0
    hits_at_5 = 0
    scored = 0  # queries that DO have an expected answer (skip "no match" cases)
    failures = []

    for _, row in eval_df.iterrows():
        query = row["query"]
        expected = str(row["expected_standard_id"]).strip()
        results = retriever.search(query, top_k=5)
        returned_ids = [r["standard_id"] for r in results]

        if expected:  # normal case - we know the right answer
            scored += 1
            in_top3 = expected in returned_ids[:3]
            in_top5 = expected in returned_ids[:5]
            hits_at_3 += in_top3
            hits_at_5 += in_top5
            if not in_top5:
                failures.append((query, expected, returned_ids))
        else:  # "no confident match expected" case - just log what came back
            print(f"[no-match-expected] {query!r} -> top result: "
                  f"{returned_ids[0] if returned_ids else 'none'} "
                  f"(score {results[0]['similarity_score'] if results else '-'})")

    print("\n--- Metrics ---")
    print(f"Recall@3: {hits_at_3}/{scored} = {hits_at_3/scored:.2%}")
    print(f"Recall@5: {hits_at_5}/{scored} = {hits_at_5/scored:.2%}")

    if failures:
        print("\n--- Failure log (expected standard not in top-5) ---")
        for query, expected, returned in failures:
            print(f"Query: {query!r}")
            print(f"  Expected: {expected}")
            print(f"  Got: {returned}\n")


if __name__ == "__main__":
    main()
