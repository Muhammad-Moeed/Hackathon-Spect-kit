"""
RAG (Retrieval-Augmented Generation) service for the Book RAG System
Handles the full RAG pipeline: retrieval -> generation
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..models.query import Query, QueryRequest
from ..models.response import Response
from ..services.chunking_service import ChunkingService
from ..services.vector_store_service import VectorStoreService
from ..services.agent_service import AgentService
from ..core.config import settings
from ..core.database import log_query, log_error
import asyncio
import logging


class RAGService:
    """Service for implementing the RAG pipeline"""

    def __init__(self):
        self.chunking_service = ChunkingService()
        self.vector_store_service = VectorStoreService()
        self.agent_service = AgentService()
        self.logger = logging.getLogger(__name__)

    async def query_full_book(self, query_request: QueryRequest) -> Response:
        """
        Process a query against the full book content
        """
        start_time = datetime.now()
        query_obj = Query(
            query_text=query_request.query,
            mode=query_request.mode,
            user_id=query_request.user_id
        )

        try:
            # Step 1: Search for relevant chunks
            retrieval_start = datetime.now()
            search_results = await self.vector_store_service.search(
                query_request.query,
                limit=5
            )
            retrieval_time = max(0.001, (datetime.now() - retrieval_start).total_seconds())  # Ensure minimum value

            if not search_results:
                # No relevant information found
                answer = "No relevant information found in the book section you selected."
                total_time = max(0.001, (datetime.now() - start_time).total_seconds())
                response = Response(
                    query_id=query_obj.id,
                    answer=answer,
                    sources=[],
                    confidence=0.0,
                    retrieval_time=retrieval_time,
                    total_time=total_time
                )
            else:
                # Step 2: Extract content from search results
                context_chunks = [result["content"] for result in search_results]
                sources = [result["id"] for result in search_results]

                # Step 3: Generate response using agent
                generation_start = datetime.now()
                agent_response = None
                try:
                    # Call generate_response and ensure we await it properly
                    response_coro = self.agent_service.generate_response(
                        query_request.query,
                        context_chunks,
                        "full_book"
                    )
                    # Ensure we await the coroutine
                    if asyncio.iscoroutine(response_coro):
                        agent_response = await response_coro
                    else:
                        agent_response = response_coro
                    
                    generation_time = (datetime.now() - generation_start).total_seconds()

                    # Final check - ensure agent_response is a dict
                    if not isinstance(agent_response, dict):
                        self.logger.error(f"Agent response is not a dict: {type(agent_response)}, value: {agent_response}")
                        raise ValueError(f"Agent response is not a dict: {type(agent_response)}")
                        
                except Exception as e:
                    self.logger.error(f"Error in agent service: {e}", exc_info=True)
                    agent_response = {
                        "answer": f"Error generating response: {str(e)}",
                        "confidence": 0.0
                    }
                    generation_time = (datetime.now() - generation_start).total_seconds()

                total_time = max(0.001, (datetime.now() - start_time).total_seconds())
                response = Response(
                    query_id=query_obj.id,
                    answer=str(agent_response.get("answer", "No answer generated")),
                    sources=sources,
                    confidence=float(agent_response.get("confidence", 0.0)),
                    retrieval_time=retrieval_time,
                    total_time=total_time
                )

            # Log the query
            await log_query(
                query_request.query,
                query_request.user_id,
                query_request.mode,
                response.answer,
                response.total_time
            )

            return response

        except Exception as e:
            self.logger.error(f"Error processing full-book query: {e}")

            # Log the error
            await log_error(
                query_request.query,
                query_request.user_id,
                str(e)
            )

            # Return error response
            total_time = max(0.001, (datetime.now() - start_time).total_seconds())
            error_response = Response(
                query_id=query_obj.id,
                answer=f"Error processing query: {str(e)}",
                sources=[],
                confidence=0.0,
                retrieval_time=0.001,  # Minimum value for validation
                total_time=total_time
            )
            return error_response

    async def query_selected_text(self, query_request: QueryRequest) -> Response:
        """
        Process a query against user-selected text only
        """
        start_time = datetime.now()

        if not query_request.selected_text:
            raise ValueError("Selected text is required for selected_text mode")

        query_obj = Query(
            query_text=query_request.query,
            mode=query_request.mode,
            selected_text=query_request.selected_text,
            user_id=query_request.user_id
        )

        try:
            # Step 1: Process selected text and create temporary embeddings
            chunks = self.chunking_service.chunk_selected_text(
                query_request.selected_text,
                query_request.user_id or "temp_session"
            )
            embedded_chunks = await self.vector_store_service.embed_chunks(chunks)

            # Store temporarily in vector store
            session_id = query_request.user_id or f"session_{int(datetime.now().timestamp())}"
            await self.vector_store_service.store_selected_text_chunks(embedded_chunks, session_id)

            # Step 2: Search within the selected text chunks
            retrieval_start = datetime.now()
            search_results = await self.vector_store_service.search_selected_text(
                query_request.query,
                session_id,
                limit=3
            )
            retrieval_time = max(0.001, (datetime.now() - retrieval_start).total_seconds())  # Ensure minimum value

            # Clean up temporary chunks after search
            await self.vector_store_service.cleanup_session_chunks(session_id)

            if not search_results:
                # No relevant information found in selected text
                answer = "No relevant information found in the book section you selected."
                total_time = max(0.001, (datetime.now() - start_time).total_seconds())
                response = Response(
                    query_id=query_obj.id,
                    answer=answer,
                    sources=[],
                    confidence=0.0,
                    retrieval_time=retrieval_time,
                    total_time=total_time
                )
            else:
                # Step 3: Extract content from search results
                context_chunks = [result["content"] for result in search_results]
                sources = [result["id"] for result in search_results]

                # Step 4: Generate response using agent
                generation_start = datetime.now()
                agent_response = None
                try:
                    # Call generate_response and ensure we await it properly
                    response_coro = self.agent_service.generate_response(
                        query_request.query,
                        context_chunks,
                        "selected_text"
                    )
                    # Ensure we await the coroutine
                    if asyncio.iscoroutine(response_coro):
                        agent_response = await response_coro
                    else:
                        agent_response = response_coro
                    
                    generation_time = (datetime.now() - generation_start).total_seconds()

                    # Final check - ensure agent_response is a dict
                    if not isinstance(agent_response, dict):
                        self.logger.error(f"Agent response is not a dict: {type(agent_response)}, value: {agent_response}")
                        raise ValueError(f"Agent response is not a dict: {type(agent_response)}")
                        
                except Exception as e:
                    self.logger.error(f"Error in agent service: {e}", exc_info=True)
                    agent_response = {
                        "answer": f"Error generating response: {str(e)}",
                        "confidence": 0.0
                    }
                    generation_time = (datetime.now() - generation_start).total_seconds()

                total_time = max(0.001, (datetime.now() - start_time).total_seconds())
                response = Response(
                    query_id=query_obj.id,
                    answer=str(agent_response.get("answer", "No answer generated")),
                    sources=sources,
                    confidence=float(agent_response.get("confidence", 0.0)),
                    retrieval_time=retrieval_time,
                    total_time=total_time
                )

            # Log the query
            await log_query(
                query_request.query,
                query_request.user_id,
                query_request.mode,
                response.answer,
                response.total_time
            )

            return response

        except Exception as e:
            self.logger.error(f"Error processing selected-text query: {e}")

            # Log the error
            await log_error(
                query_request.query,
                query_request.user_id,
                str(e)
            )

            # Return error response
            total_time = max(0.001, (datetime.now() - start_time).total_seconds())
            error_response = Response(
                query_id=query_obj.id,
                answer=f"Error processing query: {str(e)}",
                sources=[],
                confidence=0.0,
                retrieval_time=0.001,  # Minimum value for validation
                total_time=total_time
            )
            return error_response

    async def process_query(self, query_request: QueryRequest) -> Response:
        """
        Main method to process a query based on the mode
        """
        if query_request.mode == "full_book":
            return await self.query_full_book(query_request)
        elif query_request.mode == "selected_text":
            return await self.query_selected_text(query_request)
        else:
            raise ValueError(f"Invalid mode: {query_request.mode}. Must be 'full_book' or 'selected_text'")

    async def health_check(self) -> Dict[str, Any]:
        """
        Check if the RAG service is healthy
        """
        vector_store_healthy = await self.vector_store_service.health_check()
        agent_healthy = await self.agent_service.health_check()

        return {
            "status": "healthy" if (vector_store_healthy and agent_healthy) else "unhealthy",
            "checks": {
                "vector_store": "healthy" if vector_store_healthy else "unhealthy",
                "agent": "healthy" if agent_healthy else "unhealthy"
            }
        }