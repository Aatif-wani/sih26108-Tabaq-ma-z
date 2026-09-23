"""
routes/search.py — Flask Blueprint with all search-related endpoints.

Endpoints
---------
GET  /health   →  Health check. Returns {"status": "ok"}.
POST /search   →  Semantic search over BIS Indian Standards.

Request body for POST /search  (JSON):
    {
        "query":  "cement for building construction",   ← required
        "top_k":  5                                     ← optional, default 5, max 20
    }

Success response (200):
    {
        "query":   "cement for building construction",
        "top_k":   5,
        "count":   5,
        "results": [
            {
                "rank":             1,
                "standard_id":      "IS 269:2015",
                "title":            "Ordinary Portland Cement — Specification",
                "category":         "Construction & Building Materials",
                "department":       "Cement and Concrete Sectional Committee, CED 2",
                "official_url":     "https://...",
                "status":           "Active",
                "year":             2015,
                "similarity_score": 0.87
            },
            ...
        ]
    }

Error responses:
    400  →  Bad request (missing / empty query, wrong Content-Type)
    500  →  AI engine crash or files missing
"""

from flask import Blueprint, request, jsonify, current_app
from retriever import get_retriever

search_bp = Blueprint("search", __name__)

DEFAULT_TOP_K = 5
MAX_TOP_K     = 20


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

@search_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    The frontend (and any deployment infrastructure) can ping this to confirm
    the backend is up and the retriever loaded correctly.
    """
    return jsonify({"status": "ok", "message": "Backend is running"}), 200


# ---------------------------------------------------------------------------
# POST /search
# ---------------------------------------------------------------------------

@search_bp.route("/search", methods=["POST"])
def search():
    """
    Semantic search endpoint.
    Accepts a JSON body with 'query' (required) and 'top_k' (optional).
    Returns a ranked list of matching Indian Standards from the BIS dataset.
    """

    # --- 1. Parse request body ---
    body = request.get_json(silent=True)
    if not body:
        return jsonify({
            "error": "Request body must be JSON. Set Content-Type: application/json."
        }), 400

    # --- 2. Validate 'query' ---
    query = (body.get("query") or "").strip()
    if not query:
        return jsonify({
            "error": "'query' is required and cannot be empty."
        }), 400

    # --- 3. Parse and clamp 'top_k' ---
    try:
        top_k = int(body.get("top_k", DEFAULT_TOP_K))
    except (TypeError, ValueError):
        top_k = DEFAULT_TOP_K
    top_k = max(1, min(top_k, MAX_TOP_K))

    # --- 4. Call the AI engine ---
    try:
        retriever    = get_retriever()
        raw_results  = retriever.search(query, top_k=top_k)
    except Exception as exc:
        current_app.logger.error("Retriever error: %s", exc, exc_info=True)
        return jsonify({
            "error": "Internal error during search. Please try again."
        }), 500

    # --- 5. Format and return response ---
    results = []
    for rank, r in enumerate(raw_results, start=1):
        # Convert pandas/numpy int64 to native Python int/str/None
        raw_year = r.get("year")
        if hasattr(raw_year, "item"):
            year_val = raw_year.item()
        else:
            try:
                year_val = int(raw_year) if raw_year not in (None, "", "NULL") else None
            except (ValueError, TypeError):
                year_val = str(raw_year)

        results.append({
            "rank":             rank,
            "standard_id":      str(r.get("standard_id", "")),
            "title":            str(r.get("title", "")),
            "category":         str(r.get("category", "")),
            "department":       str(r.get("department", "")),
            "official_url":     str(r.get("official_url", "")),
            "status":           str(r.get("status", "")),
            "year":             year_val,
            "similarity_score": float(r.get("similarity_score", 0.0)),
        })

    return jsonify({
        "query":   query,
        "top_k":   top_k,
        "count":   len(results),
        "results": results,
    }), 200
