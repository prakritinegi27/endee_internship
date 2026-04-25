# 📚 Book Semantic Search — powered by Endee Vector Database

A semantic search engine for books built using the [Endee](https://github.com/endee-io/endee) high-performance vector database. Unlike keyword search, this system understands the **meaning** behind your query and returns the most relevant books — even if they don't share any keywords.

---

## 🚀 Demo

```
Query: "self improvement and productivity tips"
→ Atomic Habits by James Clear        (score: 0.89)
→ Deep Work by Cal Newport            (score: 0.81)

Query: "magic school for kids"
→ Harry Potter and the Sorcerer's Stone by J.K. Rowling  (score: 0.91)

Query: "money and financial wisdom"
→ The Psychology of Money by Morgan Housel  (score: 0.92)
→ Think and Grow Rich by Napoleon Hill      (score: 0.85)
```

---

## 🧠 How It Works — System Design

```
User Query
    │
    ▼
┌─────────────────────────┐
│  Sentence Transformer   │  ← all-MiniLM-L6-v2 (384-dim embeddings)
│  (Embedding Model)      │
└─────────────────────────┘
    │  Query Vector [384 floats]
    ▼
┌─────────────────────────┐
│   Endee Vector DB       │  ← Cosine similarity search across indexed books
│   (localhost:8080)      │
└─────────────────────────┘
    │  Top-K similar vectors
    ▼
┌─────────────────────────┐
│   Ranked Results        │  ← Book title, author, description + score
└─────────────────────────┘
```

### Why Endee?
- High-performance vector storage and retrieval
- Cosine similarity support for semantic matching
- Lightweight, runs locally on a single node
- Easy REST API for upsert and search

---

## 🛠️ Setup & Installation

### Step 1: Start Endee Vector Database

**Option A — Docker (Easiest)**
```bash
docker run -p 8080:8080 endeeio/endee-server:latest
```

**Option B — Docker Compose**
```bash
# Create docker-compose.yml with:
services:
  endee:
    image: endeeio/endee-server:latest
    ports:
      - "8080:8080"
    volumes:
      - endee-data:/data
volumes:
  endee-data:

# Then run:
docker compose up -d
```

**Option C — Build from source**
```bash
git clone https://github.com/endee-io/endee.git
cd endee
chmod +x install.sh && ./install.sh --release --avx2
chmod +x run.sh && ./run.sh
```

### Step 2: Clone This Project

```bash
git clone https://github.com/YOUR_USERNAME/book-semantic-search.git
cd book-semantic-search
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Search Engine

```bash
python search.py
```

The script will:
1. Load the embedding model
2. Create a `books` index in Endee
3. Insert 10 sample books as vectors
4. Run 5 demo searches
5. Open an interactive prompt for your own queries

---

## 📁 Project Structure

```
book-semantic-search/
├── search.py          # Main semantic search engine
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## 💡 Use Cases

| Use Case | Example Query |
|----------|--------------|
| Mood-based search | "I want something inspiring" |
| Topic discovery | "books about human psychology" |
| Genre exploration | "sci-fi with deep politics" |
| Learning goals | "become better at focusing" |

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|------------|
| Vector Database | [Endee](https://github.com/endee-io/endee) |
| Embedding Model | `all-MiniLM-L6-v2` via sentence-transformers |
| Language | Python 3.8+ |
| Similarity Metric | Cosine Similarity |

---

## 📌 Acknowledgements

Built using [Endee](https://github.com/endee-io/endee) — an open-source, high-performance vector database by Endee Labs.
