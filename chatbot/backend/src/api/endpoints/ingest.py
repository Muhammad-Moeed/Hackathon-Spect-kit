"""
Ingest endpoints for the Book RAG System
Handles book content ingestion and processing
"""
from fastapi import APIRouter, HTTPException, Body
from typing import List
from pydantic import BaseModel
from ...models.chunk import Chunk, ChunkRequest, ChunkResponse
from ...services.chunking_service import ChunkingService
from ...services.vector_store_service import VectorStoreService
from ...core.exceptions import raise_validation_error, raise_retrieval_error
import logging


class IngestBookRequest(BaseModel):
    """Request model for ingesting entire book content"""
    book_content: str
    book_id: str
    section: str = None


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/ingest", summary="Ingest book content")
async def ingest_endpoint(chunks: List[ChunkRequest]):
    """
    Upload and process book content for vector storage
    """
    if not chunks:
        raise raise_validation_error("At least one chunk must be provided")

    try:
        # Initialize services
        chunking_service = ChunkingService()
        vector_store_service = VectorStoreService()

        # Convert ChunkRequest to Chunk models
        chunk_models = []
        for chunk_req in chunks:
            chunk_metadata = {
                "book_id": chunk_req.book_id,
                "section": chunk_req.section,
                "page_number": chunk_req.page_number,
                "position": chunk_req.position,
                "selected_text": chunk_req.selected_text,
                "session_id": chunk_req.session_id,
                "expires_at": chunk_req.expires_at
            }

            # Import here to avoid circular imports
            from ...models.chunk import ChunkMetadata
            chunk_metadata_obj = ChunkMetadata(**chunk_metadata)

            chunk_model = Chunk(
                content=chunk_req.content,
                metadata=chunk_metadata_obj
            )
            chunk_models.append(chunk_model)

        # Generate embeddings for the chunks
        embedded_chunks = await vector_store_service.embed_chunks(chunk_models)

        # Store in vector database
        await vector_store_service.store_chunks(embedded_chunks)

        # Return success response
        return {
            "status": "success",
            "count": len(embedded_chunks),
            "processed_chunks": [chunk.id for chunk in embedded_chunks]
        }

    except ValueError as e:
        logger.error(f"Validation error in ingest endpoint: {e}")
        raise raise_validation_error(str(e))
    except Exception as e:
        logger.error(f"Error processing ingestion: {e}")
        raise raise_retrieval_error(f"Error processing ingestion: {str(e)}")


@router.post("/ingest-book", summary="Ingest entire book content")
async def ingest_book_endpoint(request: IngestBookRequest):
    """
    Ingest an entire book by automatically chunking the content
    
    Request body:
    {
        "book_content": "Full text of the book...",
        "book_id": "unique-book-id",
        "section": "Optional section name"
    }
    """
    if not request.book_content or not request.book_content.strip():
        raise raise_validation_error("Book content cannot be empty")

    if not request.book_id:
        raise raise_validation_error("Book ID is required")

    try:
        # Initialize services
        chunking_service = ChunkingService()
        vector_store_service = VectorStoreService()

        # Chunk the book content
        chunks = chunking_service.chunk_book_content(request.book_content, request.book_id, request.section)

        # Generate embeddings for the chunks
        embedded_chunks = await vector_store_service.embed_chunks(chunks)

        # Validate chunks
        valid_chunks = []
        for chunk in embedded_chunks:
            if chunking_service.validate_chunk(chunk):
                valid_chunks.append(chunk)
            else:
                logger.warning(f"Invalid chunk skipped: {chunk.id}")

        # Store in vector database
        await vector_store_service.store_chunks(valid_chunks)

        # Return success response
        return {
            "status": "success",
            "count": len(valid_chunks),
            "book_id": request.book_id,
            "section": request.section
        }

    except ValueError as e:
        logger.error(f"Validation error in ingest book endpoint: {e}")
        raise raise_validation_error(str(e))
    except Exception as e:
        logger.error(f"Error processing book ingestion: {e}")
        raise raise_retrieval_error(f"Error processing book ingestion: {str(e)}")