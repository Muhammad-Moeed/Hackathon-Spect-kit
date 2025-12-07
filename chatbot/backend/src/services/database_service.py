"""
Database service for the Book RAG System
Provides a service layer for database operations
"""
from typing import Optional
from ..core.database import log_query as core_log_query, log_error as core_log_error, db_instance


class DatabaseService:
    """Service layer for database operations"""

    @staticmethod
    async def log_query(query_text: str, user_id: Optional[str], mode: str, response: str, processing_time: float):
        """
        Log a query to the database
        """
        await core_log_query(query_text, user_id, mode, response, processing_time)

    @staticmethod
    async def log_error(query: str, user_id: Optional[str], error_message: str):
        """
        Log an error to the database
        """
        await core_log_error(query, user_id, error_message)

    @staticmethod
    async def execute_query(query: str, *args):
        """
        Execute a custom query
        """
        return await db_instance.execute_query(query, *args)

    @staticmethod
    async def execute_command(command: str, *args):
        """
        Execute a custom command
        """
        return await db_instance.execute_command(command, *args)