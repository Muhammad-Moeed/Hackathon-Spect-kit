# Research: Book RAG System

## Decision: Optimal chunk size vs. embedding cost
**Rationale**: After researching various approaches, 512 tokens appears to be the optimal balance between retrieval accuracy and embedding costs. This size provides sufficient context for understanding while keeping API costs manageable. Larger chunks (1024+) risk losing focus, while smaller chunks (256-) may lack sufficient context for coherent answers.

**Alternatives considered**:
- 256 token chunks: Too small, loses context
- 1024 token chunks: Higher cost, potential for off-topic information
- Dynamic chunking based on semantic boundaries: More complex implementation with marginal benefits

## Decision: When to store metadata in Postgres vs. Qdrant
**Rationale**: Qdrant will store metadata directly related to the content chunks (text content, book section, page numbers, etc.) as this enables efficient filtering during retrieval. Postgres will store user session data, query logs, analytics, and system-level metadata that requires complex querying and reporting capabilities.

**Alternatives considered**:
- All metadata in Postgres: Would require additional join operations during retrieval, impacting latency
- All metadata in Qdrant: Would limit analytical capabilities and complicate user session management

## Decision: Handling user-selected text via temporary embeddings
**Rationale**: For user-selected text mode, we'll create temporary embeddings in Qdrant that are tagged with a session identifier and short expiration time. This allows us to use the same retrieval pipeline while ensuring selected text doesn't persist longer than needed. For very short selections, we'll expand the context by including surrounding text to ensure sufficient context for embeddings.

**Alternatives considered**:
- Real-time embedding without storage: Would cause significant latency issues
- Permanent storage of all selected text: Privacy concerns and storage bloat
- Client-side embedding: Security concerns with API keys and computational overhead

## Decision: Error-handling and fallback behavior
**Rationale**: The system will implement graceful degradation with multiple fallback strategies: (1) If vector search fails, return "Unable to retrieve information" message, (2) If OpenAI service is unavailable, return cached response if available or error message, (3) If no relevant chunks found, return standard "No relevant information found" message, (4) For partial failures, return best available answer with confidence indicator.

**Alternatives considered**:
- Aggressive retry mechanisms: Could increase response time beyond 3s target
- Complex fallback chains: Would add unnecessary complexity without significant benefit

## Decision: Logging strategy for saving all user queries in Postgres
**Rationale**: All user queries will be logged in Postgres with the following fields: query text, timestamp, user ID (if available), mode (full-book/selected-text), response time, result type (success/empty/error), and source references. This enables analytics, quality monitoring, and debugging while maintaining user privacy by not storing personal information.

**Alternatives considered**:
- External logging services: Additional complexity and cost
- No logging: Would prevent analytics and monitoring
- Log aggregation: Premature optimization for this scope

## Additional Research Findings

### Chunking Strategy
- Semantic chunking (breaking at sentence boundaries) performs better than fixed token counts for book content
- Overlap of 50-100 tokens between chunks helps maintain context across boundaries
- Pre-processing to remove headers, page numbers, and other non-content text improves quality

### Embedding Models
- OpenAI's text-embedding-ada-002 provides good balance of cost and quality
- For future optimization, consider sentence-transformers models for initial filtering with OpenAI for final ranking

### Performance Optimization
- Caching recent queries and responses can significantly improve response times for common questions
- Asynchronous processing of embeddings during ingestion prevents blocking user interactions
- Connection pooling for both Qdrant and Postgres is essential for handling concurrent users

### Quality Validation
- Grounding validation requires comparing generated responses to source chunks with similarity scoring
- Regular testing with predefined questions and expected answers helps maintain quality
- Confidence scoring based on similarity between query and retrieved chunks provides user feedback