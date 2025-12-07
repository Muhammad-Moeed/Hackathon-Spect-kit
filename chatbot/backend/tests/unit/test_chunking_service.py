"""
Unit tests for the Chunking Service
"""
import pytest
from src.services.chunking_service import ChunkingService
from src.models.chunk import ChunkRequest


class TestChunkingService:
    """Test cases for the ChunkingService"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.chunking_service = ChunkingService()

    def test_chunk_book_content_simple(self):
        """Test chunking simple book content"""
        content = "This is a test sentence. Here is another sentence. And a third one."
        book_id = "test-book"

        chunks = self.chunking_service.chunk_book_content(content, book_id)

        assert len(chunks) > 0
        assert chunks[0].content == content  # With small content, it stays as one chunk
        assert chunks[0].metadata.book_id == book_id

    def test_chunk_book_content_large(self):
        """Test chunking larger content that should be split"""
        # Create content larger than default chunk size
        content = "Sentence one. " * 100  # This should exceed the default chunk size
        book_id = "test-book"

        chunks = self.chunking_service.chunk_book_content(content, book_id)

        assert len(chunks) > 1  # Should be split into multiple chunks
        assert all(chunk.metadata.book_id == book_id for chunk in chunks)

    def test_chunk_selected_text(self):
        """Test chunking selected text"""
        selected_text = "This is user selected text for analysis."
        session_id = "test-session"

        chunks = self.chunking_service.chunk_selected_text(selected_text, session_id)

        assert len(chunks) == 1
        assert chunks[0].content == selected_text
        assert chunks[0].metadata.selected_text is True
        assert chunks[0].metadata.session_id == session_id

    def test_validate_chunk_valid(self):
        """Test validating a valid chunk"""
        from src.models.chunk import Chunk, ChunkMetadata

        chunk = Chunk(
            content="This is valid content",
            metadata=ChunkMetadata(book_id="test-book")
        )

        is_valid = self.chunking_service.validate_chunk(chunk)
        assert is_valid is True

    def test_validate_chunk_invalid_empty(self):
        """Test validating an invalid chunk with empty content"""
        from src.models.chunk import Chunk, ChunkMetadata

        chunk = Chunk(
            content="",
            metadata=ChunkMetadata(book_id="test-book")
        )

        is_valid = self.chunking_service.validate_chunk(chunk)
        assert is_valid is False

    def test_merge_chunks(self):
        """Test merging small chunks"""
        from src.models.chunk import Chunk, ChunkMetadata

        chunks = [
            Chunk(content="Short text", metadata=ChunkMetadata(book_id="test-book", position=0)),
            Chunk(content="Another short text", metadata=ChunkMetadata(book_id="test-book", position=1))
        ]

        merged = self.chunking_service.merge_chunks(chunks, max_size=100)

        # With small max_size, chunks might be merged
        assert len(merged) >= 1