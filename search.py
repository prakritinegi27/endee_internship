"""
Book Semantic Search using Endee Vector Database
Uses sentence-transformers to embed book descriptions and search semantically
"""

import json
import requests
from sentence_transformers import SentenceTransformer

# ─── Config ───────────────────────────────────────────────────────────────────
ENDEE_BASE_URL = "http://localhost:8080"
INDEX_NAME = "books"
VECTOR_DIM = 384  # matches all-MiniLM-L6-v2 output

# ─── Sample Books Dataset ─────────────────────────────────────────────────────
BOOKS = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho",
     "description": "A young shepherd journeys to find treasure and discovers the meaning of life and dreams."},
    {"id": 2, "title": "Atomic Habits", "author": "James Clear",
     "description": "A practical guide to building good habits and breaking bad ones using small incremental changes."},
    {"id": 3, "title": "Sapiens", "author": "Yuval Noah Harari",
     "description": "A brief history of humankind exploring how Homo sapiens came to dominate the world."},
    {"id": 4, "title": "1984", "author": "George Orwell",
     "description": "A dystopian novel about a totalitarian government that controls every aspect of life and thought."},
    {"id": 5, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald",
     "description": "A story of wealth, love, and the American Dream set in the roaring 1920s."},
    {"id": 6, "title": "Deep Work", "author": "Cal Newport",
     "description": "Rules for focused success in a distracted world — how to do your best work by eliminating distractions."},
    {"id": 7, "title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling",
     "description": "A young boy discovers he is a wizard and enrolls in Hogwarts School of Witchcraft and Wizardry."},
    {"id": 8, "title": "The Psychology of Money", "author": "Morgan Housel",
     "description": "Timeless lessons on wealth, greed, and happiness and how people think about money."},
    {"id": 9, "title": "Dune", "author": "Frank Herbert",
     "description": "An epic sci-fi saga about politics, religion, and survival on a desert planet with valuable resources."},
    {"id": 10, "title": "Think and Grow Rich", "author": "Napoleon Hill",
     "description": "A motivational book about mindset, success principles, and how thoughts can shape your financial destiny."},
]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def create_index():
    """Create a vector index in Endee"""
    payload = {
        "name": INDEX_NAME,
        "dimension": VECTOR_DIM,
        "metric": "cosine"
    }
    r = requests.post(f"{ENDEE_BASE_URL}/api/v1/index/create", json=payload)
    print(f"[Index] {r.status_code} - {r.text}")


def insert_books(model):
    """Embed and insert all books into Endee"""
    print("\n[Inserting books...]")
    for book in BOOKS:
        vector = model.encode(book["description"]).tolist()
        payload = {
            "index": INDEX_NAME,
            "id": str(book["id"]),
            "vector": vector,
            "metadata": {
                "title": book["title"],
                "author": book["author"],
                "description": book["description"]
            }
        }
        r = requests.post(f"{ENDEE_BASE_URL}/api/v1/vector/upsert", json=payload)
        print(f"  Inserted: {book['title']} → {r.status_code}")


def search_books(query: str, model, top_k: int = 3):
    """Embed query and search Endee for similar books"""
    query_vector = model.encode(query).tolist()
    payload = {
        "index": INDEX_NAME,
        "vector": query_vector,
        "top_k": top_k
    }
    r = requests.post(f"{ENDEE_BASE_URL}/api/v1/vector/search", json=payload)
    results = r.json()

    print(f"\n🔍 Query: '{query}'")
    print("─" * 50)
    for i, result in enumerate(results.get("results", []), 1):
        meta = result.get("metadata", {})
        score = result.get("score", 0)
        print(f"{i}. {meta.get('title')} by {meta.get('author')}")
        print(f"   Score: {score:.4f}")
        print(f"   {meta.get('description')}")
        print()


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Setup
    create_index()
    insert_books(model)

    # Demo searches
    queries = [
        "self improvement and productivity tips",
        "magic school for kids",
        "money and financial wisdom",
        "political control and surveillance",
        "adventure and finding yourself"
    ]

    print("\n" + "=" * 60)
    print("SEMANTIC SEARCH RESULTS")
    print("=" * 60)

    for q in queries:
        search_books(q, model, top_k=2)

    # Interactive mode
    print("\n" + "=" * 60)
    print("Try your own search! (type 'quit' to exit)")
    print("=" * 60)
    while True:
        user_query = input("\nEnter search query: ").strip()
        if user_query.lower() in ("quit", "exit", "q"):
            break
        if user_query:
            search_books(user_query, model, top_k=3)
