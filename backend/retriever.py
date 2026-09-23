"""
retriever.py — Thin wrapper around the ai-engine's StandardsRetriever.

Handles path resolution so Flask can find the FAISS index and metadata
files regardless of which directory Flask is launched from.

Usage (in app.py or any route):
    from retriever import get_retriever
    retriever = get_retriever()          # call once at app startup
    results   = retriever.search(query)  # call per request
"""

import os
import sys

# ---------------------------------------------------------------------------
# Resolve the ai-engine directory relative to THIS file's location.
# This means paths work whether Flask is launched from backend/, the repo
# root, or anywhere else.
# ---------------------------------------------------------------------------
_BACKEND_DIR   = os.path.dirname(os.path.abspath(__file__))
_AI_ENGINE_DIR = os.path.abspath(os.path.join(_BACKEND_DIR, "..", "ai-engine"))

# Add ai-engine to sys.path so we can "from retrieve import StandardsRetriever"
if _AI_ENGINE_DIR not in sys.path:
    sys.path.insert(0, _AI_ENGINE_DIR)

from retrieve import StandardsRetriever  # noqa: E402  (import after path setup)

_retriever_instance = None


def get_retriever() -> StandardsRetriever:
    """
    Returns a singleton StandardsRetriever.

    The model + FAISS index are loaded on the FIRST call (~3-5 seconds).
    Every call after that returns the already-loaded instance instantly.
    Never call StandardsRetriever() directly inside a route — always use
    this function so you don't reload the model on every request.
    """
    global _retriever_instance
    if _retriever_instance is None:
        index_path    = os.path.join(_AI_ENGINE_DIR, "standards.index")
        metadata_path = os.path.join(_AI_ENGINE_DIR, "standards_metadata.csv")

        _retriever_instance = StandardsRetriever(
            index_path=index_path,
            metadata_path=metadata_path,
        )
    return _retriever_instance
