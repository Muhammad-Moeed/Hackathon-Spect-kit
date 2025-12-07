"""
Query model for the Book RAG System
Represents a user's question to the RAG system
"""
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from uuid import uuid4
import datetime


class QueryRequest(BaseModel):
    """Request model for querying the RAG system"""
    query: str = Field(..., min_length=1, description="The question to ask about the book content")
    mode: str = Field(..., pattern=r"^(full_book|selected_text)$", description="The retrieval mode to use")
    selected_text: Optional[str] = Field(None, description="The text selected by user (required for selected_text mode)")
    user_id: Optional[str] = Field(None, description="Optional user identifier for analytics")

    @model_validator(mode='after')
    def validate_selected_text(self):
        """Validate that selected_text is provided when mode is selected_text"""
        if self.mode == 'selected_text' and not self.selected_text:
            raise ValueError('selected_text is required when mode is selected_text')
        return self


class Query(BaseModel):
    """Model representing a query"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    query_text: str
    mode: str = Field(..., pattern=r"^(full_book|selected_text)$")
    selected_text: Optional[str] = None
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    session_id: Optional[str] = None

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"


class QueryResponse(BaseModel):
    """Response model for query operations"""
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)
    retrieval_time: float
    total_time: float