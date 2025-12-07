# Data Model: Book RAG System

## Core Entities

### Book Content Chunk
- **chunk_id**: string (UUID) - Unique identifier for the chunk
- **content**: string - The actual text content of the chunk
- **embedding**: array of floats - Vector representation of the content (1536-dimensional for OpenAI ada model)
- **token_count**: integer - Number of tokens in the content
- **metadata**: object
  - **book_id**: string - Identifier for the book
  - **section**: string - Section or chapter name
  - **page_number**: integer - Page number in the original book
  - **position**: integer - Sequential position in the book
  - **selected_text**: boolean - Whether this chunk is from user-selected text (for filtering)
  - **session_id**: string (optional) - Session ID if this is temporary selected text
  - **expires_at**: timestamp (optional) - Expiration time for temporary chunks

### Query
- **query_id**: string (UUID) - Unique identifier for the query
- **user_id**: string (optional) - Identifier for the user (if available)
- **query_text**: string - The original question asked by the user
- **mode**: string (enum: "full_book", "selected_text") - Retrieval mode used
- **selected_text**: string (optional) - Text selected by user (in selected_text mode)
- **timestamp**: timestamp - When the query was made
- **session_id**: string (optional) - Session identifier

### Response
- **response_id**: string (UUID) - Unique identifier for the response
- **query_id**: string - Reference to the associated query
- **answer**: string - The generated answer to the query
- **sources**: array of strings - List of chunk IDs or references used to generate the answer
- **confidence**: float - Confidence score (0.0-1.0) in the answer
- **retrieval_time**: float - Time taken for retrieval phase in seconds
- **total_time**: float - Total response time in seconds
- **timestamp**: timestamp - When the response was generated

### User Session
- **session_id**: string (UUID) - Unique identifier for the session
- **user_id**: string (optional) - Identifier for the user
- **created_at**: timestamp - When the session was created
- **last_activity**: timestamp - When the session was last used
- **selected_text_chunks**: array of objects - Temporary chunks created from user selection
  - **chunk_id**: string - ID of the temporary chunk
  - **original_text**: string - The selected text
  - **embedding**: array of floats - Vector representation of the selected text
  - **expires_at**: timestamp - When this temporary chunk expires

## Database Schema (PostgreSQL)

### query_logs table
- id: SERIAL PRIMARY KEY
- query_text: TEXT NOT NULL
- user_id: VARCHAR(255)
- mode: VARCHAR(50) NOT NULL
- response: TEXT
- processing_time: FLOAT
- timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### error_logs table
- id: SERIAL PRIMARY KEY
- query: TEXT
- user_id: VARCHAR(255)
- error_message: TEXT
- timestamp: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## Vector Storage Schema (Qdrant)

### Collection: book_chunks
- Point ID: chunk_id (UUID)
- Vector: embedding (1536 dimensions for OpenAI ada model)
- Payload:
  - content: string
  - token_count: integer
  - metadata: object with book-specific information
    - book_id, section, page_number, position, selected_text, session_id, expires_at

## Validation Rules

### Book Content Chunk
- content must not be empty
- token_count must be positive
- embedding must have exactly 1536 elements (for OpenAI ada model)
- If selected_text is true, session_id must be present
- If expires_at is present, it must be in the future

### Query
- query_text must not be empty
- mode must be either "full_book" or "selected_text"
- If mode is "selected_text", selected_text must not be empty

### Response
- answer must not be empty
- confidence must be between 0.0 and 1.0
- retrieval_time and total_time must be positive
- query_id must reference an existing query

### User Session
- session_id must be unique
- created_at must be before last_activity
- selected_text_chunks items must have valid expires_at timestamps