"""
test_api.py — Quick test script to verify the Flask backend.

Make sure the backend is running first:
    python app.py

Then in a second terminal run:
    python test_api.py
"""

import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:5000"


def test_health():
    print("\n[1] Testing GET /health ...")
    url = f"{BASE_URL}/health"
    try:
        with urllib.request.urlopen(url) as response:
            status = response.getcode()
            body = json.loads(response.read().decode())
            print(f"    Status: {status}")
            print(f"    Response: {body}")
            assert status == 200
            assert body.get("status") == "ok"
            print("    --> PASS: Health check works!")
    except urllib.error.URLError as e:
        print(f"    --> FAILED: Cannot connect to {url}.")
        print("    Did you start the backend with `python app.py`?")
        return False
    return True


def test_search():
    print("\n[2] Testing POST /search ...")
    url = f"{BASE_URL}/search"
    payload = {
        "query": "cement for building construction",
        "top_k": 3
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = json.loads(response.read().decode())
            print(f"    Status: {status}")
            print(f"    Query: '{body.get('query')}'")
            print(f"    Results returned: {body.get('count')}")
            for item in body.get("results", []):
                print(f"      - Rank {item['rank']}: [{item['standard_id']}] {item['title']}")
                print(f"        Score: {item['similarity_score']} | Category: {item['category']}")
            assert status == 200
            assert len(body.get("results", [])) > 0
            print("    --> PASS: Search API works!")
    except urllib.error.HTTPError as e:
        print(f"    --> FAILED with HTTP {e.code}: {e.read().decode()}")
        return False
    except urllib.error.URLError as e:
        print(f"    --> FAILED: Connection error ({e})")
        return False
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("SIH26108 Backend Verification Test")
    print("=" * 60)

    if test_health():
        test_search()
        print("\n" + "=" * 60)
        print("All basic checks passed! Backend is ready for Dayan's frontend.")
        print("=" * 60)
