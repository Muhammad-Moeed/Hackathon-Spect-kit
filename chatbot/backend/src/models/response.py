"""
Response model for the Book RAG System
Represents the system's answer to a user's query
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
import datetime


class Response(BaseModel):
    """Model representing a response to a query"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    query_id: str
    answer: str
    sources: List[str]  # List of chunk IDs or references used to generate the answer
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score (0.0-1.0) in the answer")
    retrieval_time: float = Field(ge=0, description="Time taken for retrieval phase in seconds")
    total_time: float = Field(ge=0, description="Total response time in seconds")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"


class ResponseRequest(BaseModel):
    """Request model for creating responses (internal use)"""
    query_id: str
    answer: str
    sources: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    retrieval_time: float
    total_time: float


class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str
    message: str
    query_id: Optional[str] = None