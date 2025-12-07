"""
Agent service for the Book RAG System
Handles interaction with OpenAI for response generation
"""
from typing import List, Dict, Any
from openai import AsyncOpenAI
from ..core.config import settings
from ..core.cache import cache_manager
import asyncio
import logging
import time


class AgentService:
    """Service for interacting with OpenAI for response generation"""

    def __init__(self):
        self.use_openai = bool(settings.OPENAI_API_KEY)
        
        if self.use_openai:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = "gpt-3.5-turbo"  # Using gpt-3.5-turbo for faster response; can be changed to gpt-4 if needed
            self.logger = logging.getLogger(__name__)
            self.logger.info("Using OpenAI for answer generation")
        else:
            self.client = None
            self.model = None
            self.logger = logging.getLogger(__name__)
            self.logger.warning("OpenAI API key not found. Using simple template-based responses.")

    async def generate_response(self, query: str, context_chunks: List[str], mode: str) -> Dict[str, Any]:
        """
        Generate response using retrieved context with caching
        """
        start_time = time.time()

        # Try to get response from cache first
        try:
            cached_response = await cache_manager.get_cached_query_result(query, mode or "")
            if cached_response is not None and isinstance(cached_response, dict):
                self.logger.info(f"Cache hit for query: {query[:50]}...")
                # Make a copy to avoid mutating cached data
                result = dict(cached_response)
                result["generation_time"] = time.time() - start_time
                return result
        except Exception as e:
            self.logger.warning(f"Cache lookup failed: {e}, continuing without cache")

        # Build context from retrieved chunks
        context = "\n\n".join(context_chunks)

        if not context.strip():
            response_obj = {
                "answer": "No relevant information found in the book section you selected.",
                "sources": [],
                "confidence": 0.0,
                "generation_time": time.time() - start_time
            }
            # Cache the no-results response
            try:
                await cache_manager.cache_query_result(query, mode or "", response_obj)
            except Exception as e:
                self.logger.warning(f"Failed to cache result: {e}")
            # Ensure we return a dict
            if not isinstance(response_obj, dict):
                self.logger.error(f"Response object is not a dict: {type(response_obj)}")
                response_obj = {
                    "answer": "Error: Invalid response format",
                    "sources": [],
                    "confidence": 0.0,
                    "generation_time": time.time() - start_time
                }
            return response_obj

        # If OpenAI is not available, use simple template-based response
        if not self.use_openai:
            # Simple template-based answer generation
            answer = self._generate_simple_response(query, context_chunks)
            confidence = min(0.85, len(context) / 2000) if context else 0.0
            
            response_obj = {
                "answer": answer,
                "sources": [f"Chunk {i+1}" for i in range(len(context_chunks))],
                "confidence": confidence,
                "generation_time": time.time() - start_time
            }
            
            # Cache the response
            try:
                await cache_manager.cache_query_result(query, mode or "", response_obj)
            except Exception as e:
                self.logger.warning(f"Failed to cache result: {e}")
            # Ensure we return a dict
            if not isinstance(response_obj, dict):
                self.logger.error(f"Response object is not a dict: {type(response_obj)}")
                response_obj = {
                    "answer": "Error: Invalid response format",
                    "sources": [],
                    "confidence": 0.0,
                    "generation_time": time.time() - start_time
                }
            return response_obj

        # Use OpenAI for answer generation
        # Create system message based on mode
        if mode == "full_book":
            system_message = """You are a helpful assistant that answers questions based strictly on the provided book content.
            Do not invent facts or provide information outside the provided context.
            If you cannot answer based on the provided text, respond with 'No relevant information found in the book section you selected.'"""
        else:  # selected_text mode
            system_message = """You are a helpful assistant that answers questions based strictly on the provided user-selected text.
            Do not invent facts or provide information outside the provided context.
            If you cannot answer based on the provided text, respond with 'No relevant information found in the book section you selected.'"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}\n\nPlease provide an answer based only on the context provided."}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Low temperature for factual responses
                max_tokens=500
            )

            answer = response.choices[0].message.content
            # Calculate a simple confidence based on context length and relevance
            confidence = min(0.95, len(context) / 2000) if context else 0.0

            response_obj = {
                "answer": answer,
                "sources": [f"Chunk {i+1}" for i in range(len(context_chunks))],
                "confidence": confidence,
                "generation_time": time.time() - start_time
            }

            # Cache the response for future similar queries
            try:
                await cache_manager.cache_query_result(query, mode or "", response_obj)
            except Exception as e:
                self.logger.warning(f"Failed to cache result: {e}")

            # Ensure we return a dict
            if not isinstance(response_obj, dict):
                self.logger.error(f"Response object is not a dict: {type(response_obj)}")
                response_obj = {
                    "answer": "Error: Invalid response format",
                    "sources": [],
                    "confidence": 0.0,
                    "generation_time": time.time() - start_time
                }
            return response_obj
        except Exception as e:
            self.logger.error(f"Error generating response: {e}", exc_info=True)
            # Fallback to simple response if OpenAI fails
            answer = self._generate_simple_response(query, context_chunks)
            response_obj = {
                "answer": str(answer),
                "sources": [f"Chunk {i+1}" for i in range(len(context_chunks))],
                "confidence": 0.7,
                "generation_time": time.time() - start_time
            }
            # Ensure we return a dict
            if not isinstance(response_obj, dict):
                self.logger.error(f"Response object is not a dict: {type(response_obj)}")
                response_obj = {
                    "answer": "Error: Invalid response format",
                    "sources": [],
                    "confidence": 0.0,
                    "generation_time": time.time() - start_time
                }
            return response_obj
    
    def _generate_simple_response(self, query: str, context_chunks: List[str]) -> str:
        """
        Generate a simple template-based response when OpenAI is not available
        """
        if not context_chunks:
            return "No relevant information found in the book content."
        
        # Combine top 3 most relevant chunks
        combined_context = "\n\n".join(context_chunks[:3])
        
        # Create a more structured response
        answer_parts = [
            f"Based on the book content, here's what I found regarding '{query}':",
            "",
            combined_context[:800]  # Limit to 800 chars for readability
        ]
        
        if len(combined_context) > 800:
            answer_parts.append("\n\n(Content truncated. More information may be available in the book.)")
        
        return "\n".join(answer_parts)

    async def health_check(self) -> bool:
        """
        Check if the agent service is healthy
        """
        if not self.use_openai:
            # If not using OpenAI, service is always healthy (using template-based responses)
            return True
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return response is not None
        except Exception as e:
            self.logger.error(f"Agent health check failed: {e}")
            return False

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            raise e

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {e}")
            raise e