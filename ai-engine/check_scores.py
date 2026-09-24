import pandas as pd
from retrieve import StandardsRetriever

eval_df = pd.read_csv("eval_queries.csv").fillna("")
retriever = StandardsRetriever()

rows = []
for _, r in eval_df.iterrows():
    res = retriever.search(r["query"], top_k=1)
    top = res[0]
    expected = str(r["expected_standard_id"]).strip()
    kind = "NO-MATCH" if not expected else ("correct" if top["standard_id"] == expected else "WRONG")
    rows.append((kind, top["similarity_score"], r["query"]))

for kind, score, q in sorted(rows, key=lambda x: x[1]):
    print(f"{score:.4f}  {kind:9s} {q}")