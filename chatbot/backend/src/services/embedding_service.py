"""
Embedding service for the Book RAG System
Supports OpenAI (paid), Cohere (free tier), and Sentence-Transformers (free) models
"""
from typing import List, Optional
from ..core.config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using different models"""

    def __init__(self):
        self.embedding_type = settings.EMBEDDING_TYPE.lower()
        self.logger = logging.getLogger(__name__)
        
        # Initialize embedding model based on type
        if self.embedding_type == "openai":
            self._init_openai()
        elif self.embedding_type == "cohere":
            self._init_cohere()
        elif self.embedding_type in ["sentence-transformers", "sentence_transformer", "free"]:
            self._init_sentence_transformers()
        else:
            # Default to cohere if not specified
            self._init_cohere()
            self.embedding_type = "cohere"

    def _init_openai(self):
        """Initialize OpenAI client for embeddings"""
        try:
            from openai import AsyncOpenAI
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings")
            self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.embedding_dim = 1536  # OpenAI ada-002 dimension
            self.logger.info("Initialized OpenAI embedding service")
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")

    def _init_cohere(self):
        """Initialize Cohere client for embeddings (free tier available)"""
        try:
            import cohere
            if not settings.COHERE_API_KEY:
                raise ValueError("COHERE_API_KEY is required for Cohere embeddings")
            self.cohere_client = cohere.AsyncClient(api_key=settings.COHERE_API_KEY)
            self.model_name = getattr(settings, 'EMBEDDING_MODEL_NAME', 'embed-english-v3.0')
            
            # Cohere model dimensions mapping
            cohere_dimensions = {
                'embed-english-v3.0': 1024,
                'embed-english-light-v3.0': 384,
                'embed-multilingual-v3.0': 1024,
                'embed-multilingual-light-v3.0': 384,
                'embed-english-v2.0': 4096,
                'embed-english-light-v2.0': 1024,
                'embed-multilingual-v2.0': 768
            }
            self.embedding_dim = cohere_dimensions.get(self.model_name, 1024)  # Default to 1024
            
            self.logger.info(f"Initialized Cohere embedding service (model: {self.model_name}, dimension: {self.embedding_dim})")
        except ImportError:
            raise ImportError("cohere package not installed. Install with: pip install cohere")

    def _init_sentence_transformers(self):
        """Initialize Sentence-Transformers for free embeddings"""
        try:
            from sentence_transformers import SentenceTransformer
            # Load model in background thread to avoid blocking
            self.model_name = getattr(settings, 'EMBEDDING_MODEL_NAME', 'all-MiniLM-L6-v2')
            self.logger.info(f"Loading Sentence-Transformer model: {self.model_name}")
            
            # Load model synchronously (it's cached)
            self.model = SentenceTransformer(self.model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            self.logger.info(f"Initialized Sentence-Transformer embedding service (dimension: {self.embedding_dim})")
        except ImportError:
            raise ImportError(
                "sentence-transformers package not installed. "
                "Install with: pip install sentence-transformers"
            )

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        if self.embedding_type == "openai":
            embeddings = await self._embed_openai([text])
            return embeddings[0] if embeddings else []
        elif self.embedding_type == "cohere":
            embeddings = await self._embed_cohere([text])
            return embeddings[0] if embeddings else []
        else:
            embeddings = await self._embed_sentence_transformers([text])
            return embeddings[0] if embeddings else []

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        """
        if not texts:
            return []

        if self.embedding_type == "openai":
            return await self._embed_openai(texts)
        elif self.embedding_type == "cohere":
            return await self._embed_cohere(texts)
        else:
            return await self._embed_sentence_transformers(texts)

    async def _embed_openai(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API"""
        try:
            response = await self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=texts
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            self.logger.error(f"Error generating OpenAI embeddings: {e}")
            raise e

    async def _embed_cohere(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Cohere API (free tier available)"""
        import time
        max_retries = 3
        retry_delay = 60  # Start with 60 seconds delay
        
        for attempt in range(max_retries):
            try:
                # Cohere supports batch embedding
                # input_type: "search_document" for documents, "search_query" for queries
                response = await self.cohere_client.embed(
                    texts=texts,
                    model=self.model_name,
                    input_type="search_document",
                    truncate="END"
                )
                # Cohere returns embeddings as list of lists
                # Ensure we get the actual list, not a coroutine
                embeddings = response.embeddings
                if asyncio.iscoroutine(embeddings):
                    embeddings = await embeddings
                return embeddings if isinstance(embeddings, list) else list(embeddings)
            except Exception as e:
                error_msg = str(e)
                # Check if it's a rate limit error
                if "429" in error_msg or "rate limit" in error_msg.lower() or "too many requests" in error_msg.lower():
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)  # Exponential backoff
                        self.logger.warning(f"Rate limit hit. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        self.logger.error(f"Rate limit exceeded after {max_retries} retries. Please wait a minute and try again.")
                        raise ValueError(f"Cohere rate limit exceeded. Please wait 60 seconds and retry. Error: {error_msg}")
                else:
                    self.logger.error(f"Error generating Cohere embeddings: {e}")
                    raise e
        
        raise ValueError("Failed to generate embeddings after retries")

    async def _embed_sentence_transformers(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Sentence-Transformers (free)"""
        try:
            # Run model encoding in executor to avoid blocking event loop
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None, 
                self.model.encode, 
                texts,
                {"normalize_embeddings": True, "show_progress_bar": False}
            )
            # Convert numpy array to list
            return embeddings.tolist() if hasattr(embeddings, 'tolist') else list(embeddings)
        except Exception as e:
            self.logger.error(f"Error generating Sentence-Transformer embeddings: {e}")
            raise e

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this service"""
        return self.embedding_dim

