"""
Unit tests for the RAG Service
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.rag_service import RAGService
from src.models.query import QueryRequest


class TestRAGService:
    """Test cases for the RAGService"""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a RAGService with mocked dependencies
        self.rag_service = RAGService()

        # Mock the dependencies to avoid external calls
        self.rag_service.vector_store_service = AsyncMock()
        self.rag_service.agent_service = AsyncMock()
        self.rag_service.chunking_service = MagicMock()

    @pytest.mark.asyncio
    async def test_query_full_book_success(self):
        """Test successful full-book query"""
        # Mock the search results
        mock_search_results = [
            {
                "id": "chunk-1",
                "content": "This is relevant content for the query",
                "score": 0.8,
                "metadata": {"book_id": "test-book"}
            }
        ]
        self.rag_service.vector_store_service.search = AsyncMock(return_value=mock_search_results)

        # Mock the agent response
        mock_agent_response = {
            "answer": "This is the answer based on the book content",
            "confidence": 0.85,
            "generation_time": 0.2
        }
        self.rag_service.agent_service.generate_response = AsyncMock(return_value=mock_agent_response)

        # Create a query request
        query_request = QueryRequest(
            query="What is the main topic?",
            mode="full_book"
        )

        # Execute the query
        response = await self.rag_service.query_full_book(query_request)

        # Verify the response
        assert response.answer == "This is the answer based on the book content"
        assert response.confidence == 0.85
        assert len(response.sources) > 0

    @pytest.mark.asyncio
    async def test_query_full_book_no_results(self):
        """Test full-book query with no relevant results"""
        # Mock empty search results
        self.rag_service.vector_store_service.search = AsyncMock(return_value=[])

        # Create a query request
        query_request = QueryRequest(
            query="What is the main topic?",
            mode="full_book"
        )

        # Execute the query
        response = await self.rag_service.query_full_book(query_request)

        # Verify the response for no results
        assert response.answer == "No relevant information found in the book section you selected."
        assert response.confidence == 0.0
        assert len(response.sources) == 0

    @pytest.mark.asyncio
    async def test_query_selected_text_success(self):
        """Test successful selected-text query"""
        # Mock chunking service
        from src.models.chunk import Chunk, ChunkMetadata
        mock_chunk = Chunk(
            content="Selected text content",
            metadata=ChunkMetadata(book_id="selected_text", selected_text=True, session_id="test-session")
        )
        self.rag_service.chunking_service.chunk_selected_text = MagicMock(return_value=[mock_chunk])
        self.rag_service.chunking_service.embed_chunks = AsyncMock(return_value=[mock_chunk])

        # Mock search results for selected text
        mock_search_results = [
            {
                "id": "chunk-1",
                "content": "Selected text content",
                "score": 0.9,
                "metadata": {"book_id": "selected_text", "selected_text": True}
            }
        ]
        self.rag_service.vector_store_service.search_selected_text = AsyncMock(return_value=mock_search_results)

        # Mock the agent response
        mock_agent_response = {
            "answer": "This is the answer based on the selected text",
            "confidence": 0.9,
            "generation_time": 0.15
        }
        self.rag_service.agent_service.generate_response = AsyncMock(return_value=mock_agent_response)

        # Create a query request for selected text
        query_request = QueryRequest(
            query="What does this text say?",
            mode="selected_text",
            selected_text="Selected text content"
        )

        # Execute the query
        response = await self.rag_service.query_selected_text(query_request)

        # Verify the response
        assert response.answer == "This is the answer based on the selected text"
        assert response.confidence == 0.9
        assert len(response.sources) > 0

    @pytest.mark.asyncio
    async def test_process_query_full_book_mode(self):
        """Test process_query with full_book mode"""
        # This test verifies the main entry point method
        self.rag_service.query_full_book = AsyncMock()

        query_request = QueryRequest(
            query="Test query",
            mode="full_book"
        )

        await self.rag_service.process_query(query_request)

        # Verify that query_full_book was called
        self.rag_service.query_full_book.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_query_selected_text_mode(self):
        """Test process_query with selected_text mode"""
        # This test verifies the main entry point method
        self.rag_service.query_selected_text = AsyncMock()

        query_request = QueryRequest(
            query="Test query",
            mode="selected_text",
            selected_text="Test selected text"
        )

        await self.rag_service.process_query(query_request)

        # Verify that query_selected_text was called
        self.rag_service.query_selected_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test health check functionality"""
        # Mock the health checks of dependencies
        self.rag_service.vector_store_service.health_check = AsyncMock(return_value=True)
        self.rag_service.agent_service.health_check = AsyncMock(return_value=True)

        health_status = await self.rag_service.health_check()

        assert health_status["status"] == "healthy"
        assert health_status["checks"]["vector_store"] == "healthy"
        assert health_status["checks"]["agent"] == "healthy"