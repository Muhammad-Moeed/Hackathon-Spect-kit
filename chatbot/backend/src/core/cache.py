"""
Caching module for the Book RAG System
Provides caching functionality for improved performance
"""
import asyncio
import time
from typing import Any, Optional, Dict
from collections import OrderedDict
import hashlib


class InMemoryCache:
    """
    Simple in-memory cache with TTL (Time To Live) support
    """
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):  # 5 minutes default
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: Dict[str, tuple] = OrderedDict()  # key -> (value, expiry_time)
        self._lock = asyncio.Lock()

    def _is_expired(self, expiry_time: float) -> bool:
        """Check if a cached item has expired"""
        return time.time() > expiry_time

    def _make_key(self, *args, **kwargs) -> str:
        """Create a cache key from arguments"""
        key_str = f"{args}_{sorted(kwargs.items())}"
        return hashlib.md5(key_str.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        async with self._lock:
            if key in self._cache:
                value, expiry_time = self._cache[key]
                if self._is_expired(expiry_time):
                    # Remove expired item
                    del self._cache[key]
                    return None
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                return value
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in cache with optional TTL"""
        if ttl is None:
            ttl = self.default_ttl

        expiry_time = time.time() + ttl

        async with self._lock:
            # If key already exists, update it
            if key in self._cache:
                self._cache[key] = (value, expiry_time)
                self._cache.move_to_end(key)
            else:
                # Add new item
                self._cache[key] = (value, expiry_time)

            # If cache is too large, remove oldest items
            while len(self._cache) > self.max_size:
                self._cache.popitem(last=False)

    async def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    async def clear(self) -> None:
        """Clear all items from cache"""
        async with self._lock:
            self._cache.clear()

    async def exists(self, key: str) -> bool:
        """Check if a key exists and is not expired"""
        value = await self.get(key)
        return value is not None


class CacheManager:
    """
    Cache manager to handle different types of caching in the application
    """
    def __init__(self):
        self.query_cache = InMemoryCache(max_size=500, default_ttl=600)  # 10 min for queries
        self.embedding_cache = InMemoryCache(max_size=1000, default_ttl=3600)  # 1 hour for embeddings
        self.chunk_cache = InMemoryCache(max_size=200, default_ttl=1800)  # 30 min for chunks

    async def cache_query_result(self, query: str, user_id: str, result: Any, ttl: int = 600):
        """Cache a query result"""
        key = f"query:{hashlib.md5((query + user_id).encode()).hexdigest()}"
        await self.query_cache.set(key, result, ttl)

    async def get_cached_query_result(self, query: str, user_id: str):
        """Get a cached query result"""
        key = f"query:{hashlib.md5((query + user_id).encode()).hexdigest()}"
        return await self.query_cache.get(key)

    async def cache_embedding(self, text: str, embedding: list, ttl: int = 3600):
        """Cache an embedding"""
        key = f"embedding:{hashlib.md5(text.encode()).hexdigest()}"
        await self.embedding_cache.set(key, embedding, ttl)

    async def get_cached_embedding(self, text: str):
        """Get a cached embedding"""
        key = f"embedding:{hashlib.md5(text.encode()).hexdigest()}"
        return await self.embedding_cache.get(key)

    async def cache_chunk(self, chunk_id: str, chunk_data: Any, ttl: int = 1800):
        """Cache a chunk"""
        key = f"chunk:{chunk_id}"
        await self.chunk_cache.set(key, chunk_data, ttl)

    async def get_cached_chunk(self, chunk_id: str):
        """Get a cached chunk"""
        key = f"chunk:{chunk_id}"
        return await self.chunk_cache.get(key)

    async def invalidate_query_cache(self, query_prefix: str = None):
        """Invalidate query cache (optionally for a specific prefix)"""
        if query_prefix:
            # In a real implementation, we'd have a way to identify related keys
            # For now, we'll just clear the entire query cache
            await self.query_cache.clear()
        else:
            await self.query_cache.clear()


# Global cache instance
cache_manager = CacheManager()


# Helper functions for easy access
async def get_cache_result(query: str, user_id: str = ""):
    """Get cached result for a query"""
    return await cache_manager.get_cached_query_result(query, user_id)


async def cache_result(query: str, user_id: str = "", result: Any = None, ttl: int = 600):
    """Cache a result for a query"""
    await cache_manager.cache_query_result(query, user_id, result, ttl)


async def get_cached_embedding_for_text(text: str):
    """Get cached embedding for text"""
    return await cache_manager.get_cached_embedding(text)


async def cache_embedding_for_text(text: str, embedding: list):
    """Cache embedding for text"""
    await cache_manager.cache_embedding(text, embedding)