"""
Metrics module for the Book RAG System
Provides performance monitoring and metrics collection
"""
import time
import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging


@dataclass
class QueryMetrics:
    """Metrics for a single query"""
    query_id: str
    start_time: float
    end_time: Optional[float] = None
    retrieval_time: Optional[float] = None
    generation_time: Optional[float] = None
    total_time: Optional[float] = None
    tokens_used: int = 0
    success: bool = True
    error_message: Optional[str] = None
    user_id: Optional[str] = None
    mode: Optional[str] = None


class MetricsCollector:
    """Collects and manages application metrics"""

    def __init__(self):
        self.queries: List[QueryMetrics] = []
        self._lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)

    async def record_query_start(self, query_id: str, user_id: Optional[str] = None, mode: Optional[str] = None) -> float:
        """Record the start of a query and return the start time"""
        start_time = time.time()
        query_metrics = QueryMetrics(
            query_id=query_id,
            start_time=start_time,
            user_id=user_id,
            mode=mode
        )

        async with self._lock:
            self.queries.append(query_metrics)

        return start_time

    async def record_query_end(self, query_id: str, retrieval_time: float = None,
                              generation_time: float = None, tokens_used: int = 0,
                              success: bool = True, error_message: Optional[str] = None):
        """Record the end of a query"""
        end_time = time.time()

        async with self._lock:
            for query in self.queries:
                if query.query_id == query_id and query.end_time is None:
                    query.end_time = end_time
                    query.retrieval_time = retrieval_time
                    query.generation_time = generation_time
                    query.total_time = end_time - query.start_time
                    query.tokens_used = tokens_used
                    query.success = success
                    query.error_message = error_message
                    break

    async def get_average_response_time(self, minutes: int = 5) -> Optional[float]:
        """Get average response time for the last N minutes"""
        cutoff_time = time.time() - (minutes * 60)

        async with self._lock:
            recent_queries = [
                q for q in self.queries
                if q.end_time and q.end_time > cutoff_time and q.success
            ]

        if not recent_queries:
            return None

        total_time = sum(q.total_time for q in recent_queries)
        return total_time / len(recent_queries)

    async def get_queries_per_minute(self, minutes: int = 5) -> float:
        """Get average queries per minute for the last N minutes"""
        cutoff_time = time.time() - (minutes * 60)

        async with self._lock:
            recent_queries = [
                q for q in self.queries
                if q.start_time > cutoff_time
            ]

        if minutes == 0:
            return 0

        return len(recent_queries) / minutes

    async def get_success_rate(self, minutes: int = 5) -> float:
        """Get success rate for the last N minutes"""
        cutoff_time = time.time() - (minutes * 60)

        async with self._lock:
            recent_queries = [
                q for q in self.queries
                if q.start_time > cutoff_time
            ]

        if not recent_queries:
            return 1.0  # 100% if no queries

        successful_queries = [q for q in recent_queries if q.success]
        return len(successful_queries) / len(recent_queries)

    async def get_p95_response_time(self, minutes: int = 5) -> Optional[float]:
        """Get 95th percentile response time for the last N minutes"""
        cutoff_time = time.time() - (minutes * 60)

        async with self._lock:
            recent_queries = [
                q for q in self.queries
                if q.end_time and q.end_time > cutoff_time and q.success
            ]

        if not recent_queries:
            return None

        # Sort by total time and get 95th percentile
        sorted_times = sorted(q.total_time for q in recent_queries)
        index = int(0.95 * len(sorted_times))

        if index >= len(sorted_times):
            index = len(sorted_times) - 1

        return sorted_times[index]

    async def get_metrics_summary(self, minutes: int = 5) -> Dict:
        """Get a summary of metrics for the last N minutes"""
        avg_response_time = await self.get_average_response_time(minutes)
        queries_per_min = await self.get_queries_per_minute(minutes)
        success_rate = await self.get_success_rate(minutes)
        p95_response_time = await self.get_p95_response_time(minutes)

        async with self._lock:
            total_queries = len([q for q in self.queries if q.start_time > time.time() - (minutes * 60)])
            successful_queries = len([q for q in self.queries if q.start_time > time.time() - (minutes * 60) and q.success])

        return {
            "period_minutes": minutes,
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "failed_queries": total_queries - successful_queries,
            "average_response_time": avg_response_time,
            "queries_per_minute": queries_per_min,
            "success_rate": success_rate,
            "p95_response_time": p95_response_time,
            "timestamp": datetime.now().isoformat()
        }


class MetricsMiddleware:
    """Middleware to automatically collect metrics"""

    def __init__(self, collector: MetricsCollector):
        self.collector = collector
        self.logger = logging.getLogger(__name__)

    async def record_query_start(self, query_id: str, user_id: Optional[str] = None, mode: Optional[str] = None):
        """Record the start of a query"""
        await self.collector.record_query_start(query_id, user_id, mode)

    async def record_query_end(self, query_id: str, retrieval_time: float = None,
                              generation_time: float = None, tokens_used: int = 0,
                              success: bool = True, error_message: Optional[str] = None):
        """Record the end of a query"""
        await self.collector.record_query_end(
            query_id, retrieval_time, generation_time, tokens_used, success, error_message
        )


# Global metrics instance
metrics_collector = MetricsCollector()
metrics_middleware = MetricsMiddleware(metrics_collector)


# Helper functions for easy access
async def record_query_start(query_id: str, user_id: Optional[str] = None, mode: Optional[str] = None) -> float:
    """Record the start of a query"""
    return await metrics_collector.record_query_start(query_id, user_id, mode)


async def record_query_end(query_id: str, retrieval_time: float = None,
                          generation_time: float = None, tokens_used: int = 0,
                          success: bool = True, error_message: Optional[str] = None):
    """Record the end of a query"""
    await metrics_collector.record_query_end(
        query_id, retrieval_time, generation_time, tokens_used, success, error_message
    )


async def get_metrics_summary(minutes: int = 5) -> Dict:
    """Get metrics summary"""
    return await metrics_collector.get_metrics_summary(minutes)