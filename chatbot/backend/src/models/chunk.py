"""
Chunk model for the Book RAG System
Represents a segment of book content with embeddings
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
import datetime


class ChunkMetadata(BaseModel):
    """Metadata for a content chunk"""
    book_id: str
    section: Optional[str] = None
    page_number: Optional[int] = None
    position: Optional[int] = None
    selected_text: bool = False  # Whether this chunk is from user-selected text
    session_id: Optional[str] = None  # Session ID if this is temporary selected text
    expires_at: Optional[datetime.datetime] = None  # Expiration time for temporary chunks


class Chunk(BaseModel):
    """Model representing a content chunk"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    embedding: Optional[List[float]] = None  # Vector representation of the content
    token_count: Optional[int] = None
    metadata: ChunkMetadata

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"


class ChunkRequest(BaseModel):
    """Request model for creating chunks"""
    content: str
    book_id: str
    section: Optional[str] = None
    page_number: Optional[int] = None
    position: Optional[int] = None
    selected_text: bool = False
    session_id: Optional[str] = None
    expires_at: Optional[datetime.datetime] = None


class ChunkResponse(BaseModel):
    """Response model for chunk operations"""
    id: str
    content: str
    token_count: Optional[int] = None
    metadata: ChunkMetadata
    created: bool = True