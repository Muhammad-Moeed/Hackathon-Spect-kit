"""
Custom exceptions for the Book RAG System
Defines application-specific error types and handlers
"""
from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class RAGException(Exception):
    """Base exception for RAG system errors"""
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class RetrievalException(RAGException):
    """Exception raised when retrieval fails"""
    pass


class GenerationException(RAGException):
    """Exception raised when response generation fails"""
    pass


class ValidationException(RAGException):
    """Exception raised when input validation fails"""
    pass


class VectorStoreException(RAGException):
    """Exception raised when vector store operations fail"""
    pass


class DatabaseException(RAGException):
    """Exception raised when database operations fail"""
    pass


# HTTP Exception Models for API responses
class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str
    message: str
    error_code: Optional[str] = None


# FastAPI HTTP Exceptions
def raise_validation_error(message: str, error_code: Optional[str] = "validation_error") -> HTTPException:
    """Raise a validation error with 400 status code"""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorResponse(error=error_code, message=message).dict()
    )


def raise_retrieval_error(message: str, error_code: Optional[str] = "retrieval_error") -> HTTPException:
    """Raise a retrieval error with 500 status code"""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=ErrorResponse(error=error_code, message=message).dict()
    )


def raise_generation_error(message: str, error_code: Optional[str] = "generation_error") -> HTTPException:
    """Raise a generation error with 500 status code"""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=ErrorResponse(error=error_code, message=message).dict()
    )


def raise_not_found_error(message: str, error_code: Optional[str] = "not_found") -> HTTPException:
    """Raise a not found error with 404 status code"""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrorResponse(error=error_code, message=message).dict()
    )


# Error handling middleware
async def handle_exception(request, call_next, exc):
    """Global exception handler"""
    import logging
    logger = logging.getLogger(__name__)

    if isinstance(exc, RAGException):
        logger.error(f"RAG Exception: {exc.message} (Code: {exc.error_code})")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(error=exc.error_code or "rag_error", message=exc.message).dict()
        )

    # Log other exceptions
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(error="internal_error", message="An unexpected error occurred").dict()
    )


# Import JSONResponse for the error handler
from fastapi.responses import JSONResponse