"""
Vector Store service for the Book RAG System
Handles interactions with the vector database
"""
from typing import List, Dict, Any, Optional
from ..models.chunk import Chunk
from ..core.vector_store import VectorStore
from ..core.config import settings
from ..core.cache import cache_manager
from .embedding_service import EmbeddingService
import asyncio
import logging


class VectorStoreService:
    """Service for managing vector storage operations"""

    def __init__(self):
        # Initialize embedding service (supports both OpenAI and free models)
        self.embedding_service = EmbeddingService()
        embedding_dim = self.embedding_service.get_embedding_dimension()
        self.vector_store = VectorStore(embedding_dim=embedding_dim)
        self.logger = logging.getLogger(__name__)

    async def embed_chunks(self, chunks: List[Chunk]) -> List[Chunk]:
        """
        Generate embeddings for chunks using OpenAI with caching
        """
        if not chunks:
            return []

        # Check cache for existing embeddings
        uncached_chunks = []
        cached_results = {}

        for i, chunk in enumerate(chunks):
            # Try to get embedding from cache
            cached_embedding = await cache_manager.get_cached_embedding(chunk.content)
            if cached_embedding is not None:
                chunk.embedding = cached_embedding
                cached_results[i] = cached_embedding
            else:
                uncached_chunks.append((i, chunk))

        # Generate embeddings only for uncached chunks
        if uncached_chunks:
            texts = [chunk.content for _, chunk in uncached_chunks]

            try:
                # Use embedding service (supports both OpenAI and free models)
                embeddings = await self.embedding_service.embed_texts(texts)

                # Attach embeddings to chunks and cache them
                for idx, (orig_idx, chunk) in enumerate(uncached_chunks):
                    embedding = embeddings[idx]
                    chunk.embedding = embedding
                    # Cache the embedding for future use
                    await cache_manager.cache_embedding(chunk.content, embedding)
                    cached_results[orig_idx] = embedding

            except Exception as e:
                self.logger.error(f"Error generating embeddings: {e}")
                raise e

        # Update token counts if not already set
        for chunk in chunks:
            if not chunk.token_count:
                chunk.token_count = len(chunk.content.split())

        return chunks

    async def store_chunks(self, chunks: List[Chunk]):
        """
        Store chunks with embeddings in the vector database
        """
        if not chunks:
            return

        # Prepare chunks for storage (convert to dict format)
        chunks_for_storage = []
        for chunk in chunks:
            chunk_dict = {
                "id": chunk.id,
                "content": chunk.content,
                "embedding": chunk.embedding,
                "metadata": chunk.metadata.dict()
            }
            chunks_for_storage.append(chunk_dict)

        await self.vector_store.store_chunks(chunks_for_storage)

    async def search(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks based on query text
        """
        # Generate embedding for query
        try:
            query_embedding = await self.embedding_service.embed_text(query_text)

            # Search in vector store
            results = await self.vector_store.search(query_embedding, limit)

            return results
        except Exception as e:
            self.logger.error(f"Error during search: {e}")
            raise e

    async def search_selected_text(self, query_text: str, session_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search only within user-selected text chunks
        """
        # Generate embedding for query
        try:
            query_embedding = await self.embedding_service.embed_text(query_text)

            # Search in vector store within the specific session
            results = await self.vector_store.search_by_selected_text(query_embedding, session_id, limit)

            return results
        except Exception as e:
            self.logger.error(f"Error during selected text search: {e}")
            raise e

    async def store_selected_text_chunks(self, chunks: List[Chunk], session_id: str):
        """
        Store user-selected text chunks temporarily with session identifier
        """
        if not chunks:
            return

        # Prepare chunks for temporary storage
        chunks_for_storage = []
        for chunk in chunks:
            # Ensure the chunk is marked as selected text with proper session ID
            chunk.metadata.selected_text = True
            chunk.metadata.session_id = session_id

            chunk_dict = {
                "id": chunk.id,
                "content": chunk.content,
                "embedding": chunk.embedding,
                "metadata": chunk.metadata.dict()
            }
            chunks_for_storage.append(chunk_dict)

        await self.vector_store.store_chunks(chunks_for_storage)

    async def cleanup_session_chunks(self, session_id: str):
        """
        Remove temporary chunks associated with a session
        """
        try:
            await self.vector_store.delete_session_chunks(session_id)
        except Exception as e:
            self.logger.error(f"Error cleaning up session chunks: {e}")

    async def health_check(self) -> bool:
        """
        Check if the vector store service is healthy
        """
        try:
            return await self.vector_store.health_check()
        except Exception:
            return False