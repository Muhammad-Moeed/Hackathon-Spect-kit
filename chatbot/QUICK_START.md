# Quick Start Guide - Book RAG Chatbot

## 🚀 Setup in 5 Steps

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Create .env File
Create `backend/.env` file:
```env
OPENAI_API_KEY=sk-your-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-key
NEON_POSTGRES_URL=postgresql://user:pass@host/db?sslmode=require
```

### 3. Start Server
```bash
uvicorn src.api.main:app --reload --port 8000
```

### 4. Ingest Book Content
**Option A: Using Python Script**
```bash
python scripts/ingest_book.py path/to/book.txt book-001
```

**Option B: Using API**
```bash
curl -X POST http://localhost:8000/api/v1/ingest-book \
  -H "Content-Type: application/json" \
  -d '{
    "book_content": "Your book text here...",
    "book_id": "book-001",
    "section": "Chapter 1"
  }'
```

### 5. Query the Book
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main theme?",
    "mode": "full_book"
  }'
```

## 📋 Environment Variables Required

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `OPENAI_API_KEY` | OpenAI API key for embeddings | https://platform.openai.com/api-keys |
| `QDRANT_URL` | Qdrant Cloud cluster URL | https://cloud.qdrant.io |
| `QDRANT_API_KEY` | Qdrant Cloud API key | https://cloud.qdrant.io |
| `NEON_POSTGRES_URL` | Postgres connection string | https://neon.tech |

## 🔄 How It Works

1. **Ingestion**: Book → Chunks → Embeddings → Vector DB (Qdrant)
2. **Query**: Question → Embedding → Similar Chunks → Answer (OpenAI)

## 📚 API Endpoints

- `POST /api/v1/ingest-book` - Upload book content
- `POST /api/v1/query` - Ask questions
- `GET /api/v1/health` - Check system health

## 📖 Detailed Guide

See `SETUP_GUIDE_URDU.md` for complete Urdu/Hindi guide with detailed explanations.

