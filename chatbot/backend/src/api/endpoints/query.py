"""
Query endpoints for the Book RAG System
Handles the main query functionality
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional
from ...models.query import QueryRequest, QueryResponse
from ...services.rag_service import RAGService
from ...core.exceptions import raise_validation_error, raise_retrieval_error
from ...core.config import settings
import time
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/query", response_model=QueryResponse, summary="Query the book RAG system")
async def query_endpoint(request: QueryRequest):
    """
    Submit a question to the RAG system and receive an answer based on book content
    """
    start_time = time.time()

    # Validate the request
    if not request.query or not request.query.strip():
        raise raise_validation_error("Query cannot be empty")

    if request.mode not in ["full_book", "selected_text"]:
        raise raise_validation_error("Mode must be either 'full_book' or 'selected_text'")

    if request.mode == "selected_text" and (not request.selected_text or not request.selected_text.strip()):
        raise raise_validation_error("Selected text is required for selected_text mode")

    try:
        # Initialize the RAG service
        rag_service = RAGService()

        # Process the query
        response = await rag_service.process_query(request)

        # Calculate total time
        total_time = time.time() - start_time

        # Check if response time exceeds the limit
        if total_time > settings.RESPONSE_TIMEOUT:
            logger.warning(f"Response time exceeded limit: {total_time}s")

        # Return the formatted response
        return QueryResponse(
            answer=response.answer,
            sources=response.sources,
            confidence=response.confidence,
            retrieval_time=response.retrieval_time,
            total_time=total_time
        )

    except ValueError as e:
        logger.error(f"Validation error in query endpoint: {e}")
        raise raise_validation_error(str(e))
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise raise_retrieval_error(f"Error processing query: {str(e)}")


@router.post("/query-debug", summary="Debug query endpoint with detailed response")
async def query_debug_endpoint(request: QueryRequest):
    """
    Debug version of the query endpoint that returns additional information
    """
    start_time = time.time()

    try:
        rag_service = RAGService()

        # Process the query
        response = await rag_service.process_query(request)

        total_time = time.time() - start_time

        return {
            "answer": response.answer,
            "sources": response.sources,
            "confidence": response.confidence,
            "retrieval_time": response.retrieval_time,
            "total_time": total_time,
            "debug_info": {
                "query_mode": request.mode,
                "query_length": len(request.query),
                "processing_time": total_time
            }
        }

    except Exception as e:
        logger.error(f"Error in debug query endpoint: {e}")
        raise raise_retrieval_error(f"Error processing query: {str(e)}")