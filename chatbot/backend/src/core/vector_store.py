"""
Vector Store module for the Book RAG System
Handles Qdrant vector database operations
"""
import os
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, Distance, VectorParams, Filter, FieldCondition, MatchValue
import uuid


class VectorStore:
    """Qdrant vector store client for the Book RAG System"""

    def __init__(self, collection_name: str = "book_chunks", embedding_dim: int = 384):
        # Get Qdrant configuration from settings
        from .config import settings
        qdrant_url = settings.QDRANT_URL
        qdrant_api_key = settings.QDRANT_API_KEY

        if not qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")

        self.client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            # Set timeout and retry settings
            timeout=10.0
        )
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self._ensure_collection()

    def _ensure_collection(self):
        """
        Ensure the collection exists with proper configuration
        """
        try:
            # Try to get the collection info to check if it exists
            collection_info = self.client.get_collection(self.collection_name)
            # Check if embedding dimension matches
            existing_dim = collection_info.config.params.vectors.size
            if existing_dim != self.embedding_dim:
                raise ValueError(
                    f"Collection exists with dimension {existing_dim}, "
                    f"but current model has dimension {self.embedding_dim}. "
                    f"Please use a different collection name or recreate the collection."
                )
        except Exception as e:
            # Create collection if it doesn't exist or dimension mismatch
            if "not found" in str(e).lower() or "does not exist" in str(e).lower():
                # Create collection if it doesn't exist
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dim,  # Dynamic embedding dimension
                        distance=Distance.COSINE
                    )
                )
            else:
                raise e

    async def store_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Store chunks with embeddings in Qdrant
        Each chunk should have: id, content, embedding, metadata
        """
        # QdrantClient.upsert() is synchronous, so we run it in executor
        import asyncio
        loop = asyncio.get_event_loop()
        
        points = []
        for chunk in chunks:
            point = PointStruct(
                id=chunk["id"],
                vector=chunk["embedding"],
                payload={
                    "content": chunk["content"],
                    "metadata": chunk["metadata"]
                }
            )
            points.append(point)

        await loop.run_in_executor(
            None,
            lambda: self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
        )

    async def search(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks based on query embedding
        """
        # QdrantClient uses query_points() method, not search()
        import asyncio
        loop = asyncio.get_event_loop()
        
        def do_query():
            return self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=limit
            )
        
        query_results = await loop.run_in_executor(None, do_query)

        # QueryResponse has points attribute which is a list
        results = []
        if hasattr(query_results, 'points') and query_results.points:
            for point in query_results.points:
                payload = point.payload if hasattr(point, 'payload') else {}
                results.append({
                    "id": str(point.id) if hasattr(point, 'id') else "",
                    "content": payload.get("content", "") if isinstance(payload, dict) else "",
                    "score": float(point.score) if hasattr(point, 'score') else 0.0,
                    "metadata": payload.get("metadata", {}) if isinstance(payload, dict) else {}
                })
        
        return results

    async def search_by_selected_text(self, query_embedding: List[float], session_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search only within user-selected text chunks for a specific session
        """
        # Filter by session_id in metadata to find temporary selected text chunks
        # QdrantClient uses query_points() method with filter
        import asyncio
        loop = asyncio.get_event_loop()
        
        def do_query():
            return self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=limit,
                query_filter=models.Filter(
                    must=[
                        FieldCondition(
                            key="metadata.session_id",
                            match=MatchValue(value=session_id)
                        )
                    ]
                )
            )
        
        query_results = await loop.run_in_executor(None, do_query)

        # QueryResponse has points attribute which is a list
        results = []
        if hasattr(query_results, 'points') and query_results.points:
            for point in query_results.points:
                payload = point.payload if hasattr(point, 'payload') else {}
                results.append({
                    "id": str(point.id) if hasattr(point, 'id') else "",
                    "content": payload.get("content", "") if isinstance(payload, dict) else "",
                    "score": float(point.score) if hasattr(point, 'score') else 0.0,
                    "metadata": payload.get("metadata", {}) if isinstance(payload, dict) else {}
                })
        
        return results

    async def delete_session_chunks(self, session_id: str):
        """
        Delete temporary chunks associated with a session (for cleanup)
        """
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        FieldCondition(
                            key="metadata.session_id",
                            match=MatchValue(value=session_id)
                        )
                    ]
                )
            )
        )

    async def health_check(self) -> bool:
        """
        Check if the vector store is accessible
        """
        try:
            # Try to get collection info as a simple health check
            self.client.get_collection(self.collection_name)
            return True
        except:
            return False