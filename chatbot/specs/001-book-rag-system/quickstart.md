# Quickstart Guide: Book RAG System

## Overview
This guide provides a quick introduction to setting up and using the Book RAG System. The system enables users to ask questions about book content and receive accurate, contextually relevant answers based on the book's text.

## Prerequisites
- Python 3.11+
- Access to OpenAI API
- Qdrant Cloud account
- Neon Postgres database
- Book content in text format

## Environment Setup

1. Create a `.env` file with the following variables:
```bash
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_POSTGRES_URL=your_neon_postgres_connection_string
```

2. Install dependencies:
```bash
pip install fastapi uvicorn openai qdrant-client asyncpg python-dotenv tiktoken
```

## Initial Setup

### 1. Ingest Book Content
Before using the RAG system, you need to ingest your book content:

```bash
python scripts/ingest_book.py path/to/your/book.txt
```

This script will:
- Chunk the book content into semantic segments
- Generate embeddings for each chunk
- Store the chunks in Qdrant vector database
- Log the ingestion in Postgres

### 2. Start the API Server
```bash
uvicorn backend.src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage Examples

### Full-Book Query
Ask questions about the entire book content:

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "query": "What is the main theme of this book?",
    "mode": "full_book"
  }'
```

### Selected Text Query
Ask questions about specific text selected by the user:

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "query": "What does this text say about AI ethics?",
    "mode": "selected_text",
    "selected_text": "The book discusses various ethical considerations in AI development..."
  }'
```

## API Endpoints

### POST /api/v1/query
Main endpoint for asking questions about book content.

**Request Body:**
- `query`: The question to ask (required)
- `mode`: "full_book" or "selected_text" (required)
- `selected_text`: Text selected by user (required for "selected_text" mode)
- `user_id`: Optional user identifier

**Response:**
- `answer`: The generated answer
- `sources`: List of sources used
- `confidence`: Confidence score (0.0-1.0)
- `retrieval_time`: Time taken for retrieval
- `total_time`: Total response time

### POST /api/v1/ingest
Endpoint for ingesting book content.

**Request Body:**
Array of chunk objects with id, content, and metadata.

### GET /api/v1/health
Health check endpoint to verify API status.

## Testing

Run the test suite:
```bash
pytest tests/
```

For specific testing:
- Unit tests: `pytest tests/unit/`
- Integration tests: `pytest tests/integration/`
- Contract tests: `pytest tests/contract/`

## Performance Considerations

- The system is optimized for <3 second response times
- Full-book queries typically return results faster than selected-text queries
- Caching is implemented for frequently asked questions
- Monitor response times to ensure SLA compliance

## Troubleshooting

### Common Issues:
1. **"No relevant information found"**: Verify the book content was properly ingested
2. **High latency**: Check API key quotas and database connection pooling
3. **Authentication errors**: Verify all environment variables are set correctly

### Monitoring:
- Check query logs in Postgres for analytics
- Monitor vector database performance in Qdrant dashboard
- Track API response times and error rates