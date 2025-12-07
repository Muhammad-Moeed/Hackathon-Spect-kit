"""
Database module for the Book RAG System
Handles PostgreSQL connections using asyncpg
"""
import asyncpg
import os
from typing import Optional
from contextlib import asynccontextmanager


class DatabaseConnection:
    """Database connection manager for PostgreSQL using asyncpg"""

    def __init__(self):
        # Use settings instead of os.getenv to ensure .env file is loaded
        from .config import settings
        self.connection_string = settings.NEON_POSTGRES_URL
        if not self.connection_string:
            raise ValueError("NEON_POSTGRES_URL environment variable is required")
        self._connection_pool = None

    async def initialize_pool(self):
        """Initialize the connection pool"""
        self._connection_pool = await asyncpg.create_pool(
            dsn=self.connection_string,
            min_size=1,
            max_size=10,
            command_timeout=60
        )

    async def get_connection(self):
        """Get a connection from the pool"""
        if not self._connection_pool:
            await self.initialize_pool()
        return self._connection_pool

    @asynccontextmanager
    async def get_db_connection(self):
        """Context manager for database connections"""
        pool = await self.get_connection()
        async with pool.acquire() as connection:
            yield connection

    async def close_pool(self):
        """Close the connection pool"""
        if self._connection_pool:
            await self._connection_pool.close()

    async def execute_query(self, query: str, *args):
        """Execute a query with parameters"""
        pool = await self.get_connection()
        async with pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute_command(self, command: str, *args):
        """Execute a command (INSERT, UPDATE, DELETE) with parameters"""
        pool = await self.get_connection()
        async with pool.acquire() as conn:
            return await conn.execute(command, *args)


# Global database instance
db_instance = DatabaseConnection()


async def init_db_tables():
    """Initialize required database tables"""
    # Query logs table
    query_logs_table = """
    CREATE TABLE IF NOT EXISTS query_logs (
        id SERIAL PRIMARY KEY,
        query_text TEXT NOT NULL,
        user_id VARCHAR(255),
        mode VARCHAR(50) NOT NULL,
        response TEXT,
        processing_time FLOAT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Error logs table
    error_logs_table = """
    CREATE TABLE IF NOT EXISTS error_logs (
        id SERIAL PRIMARY KEY,
        query TEXT,
        user_id VARCHAR(255),
        error_message TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Create indexes for performance
    timestamp_index = """
    CREATE INDEX IF NOT EXISTS idx_query_logs_timestamp ON query_logs(timestamp);
    CREATE INDEX IF NOT EXISTS idx_error_logs_timestamp ON error_logs(timestamp);
    """

    # Execute table creation
    await db_instance.execute_command(query_logs_table)
    await db_instance.execute_command(error_logs_table)
    await db_instance.execute_command(timestamp_index)


# Helper functions for logging
async def log_query(query_text: str, user_id: Optional[str], mode: str, response: str, processing_time: float):
    """Log query to database"""
    query = """
    INSERT INTO query_logs (query_text, user_id, mode, response, processing_time)
    VALUES ($1, $2, $3, $4, $5)
    """
    await db_instance.execute_command(query, query_text, user_id, mode, response, processing_time)


async def log_error(query: str, user_id: Optional[str], error_message: str):
    """Log error to database"""
    query = """
    INSERT INTO error_logs (query, user_id, error_message)
    VALUES ($1, $2, $3)
    """
    await db_instance.execute_command(query, query, user_id, error_message)