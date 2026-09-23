"""
app.py — Flask application factory for the SIH26108 backend.

Run this file to start the development server:
    python app.py

The AI model and FAISS index are loaded ONCE at startup (before the first
request). This means the server takes ~3-5 seconds to start, but every
search request after that is fast.
"""

from flask import Flask
from flask_cors import CORS
from routes.search import search_bp
from retriever import get_retriever


def create_app() -> Flask:
    """
    Application factory — creates and configures the Flask app.
    """
    app = Flask(__name__)

    # Allow requests from any origin during development so Dayan's frontend
    # (running on a different port) can reach this API without CORS errors.
    # Tighten this to the actual frontend URL before production deployment.
    CORS(app)

    # Register blueprints (groups of related routes)
    app.register_blueprint(search_bp)

    return app


# Create the app at module level so Flask's dev server can find it
app = create_app()


if __name__ == "__main__":
    # Pre-load the retriever so the very first search request is instant.
    # Without this, the first request would take ~5 seconds to load the model.
    print("=" * 50)
    print("SIH26108 Backend — Starting up")
    print("=" * 50)
    print("Loading AI model and FAISS index...")
    get_retriever()
    print("Retriever ready!")
    print("Starting Flask server on http://localhost:5000")
    print("=" * 50)

    app.run(host="0.0.0.0", port=5000, debug=True)
