# Book RAG System

A production-ready RAG (Retrieval-Augmented Generation) system that answers questions strictly from book content or user-selected text.

## Features

- **Full-book RAG retrieval**: Ask questions about the entire book content
- **Selected text retrieval**: Ask questions about specific text selections only
- **Zero hallucinations**: Answers are strictly grounded in book content
- **Fast responses**: <3 second response time target
- **Secure**: No exposure of API keys or sensitive information
- **Dual mode support**: Switch between full-book and selected-text modes

## Architecture

The system follows the architecture: Ingestion → Chunking → Embedding → Vector Storage → Query → Re-ranking → Generation

- **Backend**: FastAPI for API endpoints
- **Vector Storage**: Qdrant Cloud for vector embeddings
- **Database**: Neon Postgres for metadata and logs
- **AI**: OpenAI Agents/ChatKit for response generation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Add your API keys and connection strings
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key
   NEON_POSTGRES_URL=your_neon_postgres_connection_string
   ```

3. Start the development server:
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

## API Endpoints

### Query Endpoint
- `POST /api/v1/query` - Submit questions to the RAG system

Request body:
```json
{
  "query": "Your question about the book",
  "mode": "full_book", // or "selected_text"
  "selected_text": "Text selected by user (required for selected_text mode)",
  "user_id": "Optional user identifier"
}
```

### Ingest Endpoint
- `POST /api/v1/ingest` - Ingest book content for vector storage

### Health Check
- `GET /api/v1/health` - Check system health status

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for embeddings and generation
- `QDRANT_URL`: Qdrant Cloud cluster URL
- `QDRANT_API_KEY`: Qdrant Cloud API key
- `NEON_POSTGRES_URL`: Neon Postgres connection string
- `RESPONSE_TIMEOUT`: Maximum response time in seconds (default: 3.0)
- `MAX_CONCURRENT_USERS`: Maximum number of concurrent users (default: 100)

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
# Format code with black
black .

# Check imports with isort
isort .
```

## Deployment

The system is designed for cloud deployment with:
- FastAPI application server
- Qdrant Cloud vector database
- Neon Postgres serverless database
- OpenAI API access

## Security

- API keys are stored in environment variables
- Input validation is performed on all endpoints
- Query logging for monitoring and analytics
- No sensitive data is stored in vector database

## Performance

- Target response time: <3 seconds
- Supports up to 100 concurrent users
- Caching layer for frequently asked questions
- Connection pooling for database operations
