"""
User Session model for the Book RAG System
Represents a user's interaction session with temporary selected text chunks
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from uuid import uuid4
import datetime


class SelectedTextChunk(BaseModel):
    """Model representing a temporary chunk from user-selected text"""
    chunk_id: str = Field(default_factory=lambda: str(uuid4()))
    original_text: str
    embedding: Optional[List[float]] = None
    expires_at: datetime.datetime


class UserSession(BaseModel):
    """Model representing a user session with temporary selected text chunks"""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_activity: datetime.datetime = Field(default_factory=datetime.datetime.now)
    selected_text_chunks: List[SelectedTextChunk] = Field(default_factory=list)

    class Config:
        # Allow extra fields for flexibility
        extra = "allow"

    def add_chunk(self, text: str, expires_in_minutes: int = 30) -> SelectedTextChunk:
        """Add a selected text chunk to the session"""
        chunk = SelectedTextChunk(
            original_text=text,
            expires_at=datetime.datetime.now() + datetime.timedelta(minutes=expires_in_minutes)
        )
        self.selected_text_chunks.append(chunk)
        self.last_activity = datetime.datetime.now()
        return chunk

    def get_active_chunks(self) -> List[SelectedTextChunk]:
        """Get chunks that haven't expired yet"""
        now = datetime.datetime.now()
        return [chunk for chunk in self.selected_text_chunks if chunk.expires_at > now]

    def cleanup_expired_chunks(self):
        """Remove expired chunks from the session"""
        now = datetime.datetime.now()
        self.selected_text_chunks = [chunk for chunk in self.selected_text_chunks if chunk.expires_at > now]
        self.last_activity = datetime.datetime.now()


class SessionRequest(BaseModel):
    """Request model for session operations"""
    user_id: Optional[str] = None
    selected_text: Optional[str] = None


class SessionResponse(BaseModel):
    """Response model for session operations"""
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime.datetime
    active_chunks_count: int