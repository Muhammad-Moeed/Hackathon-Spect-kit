"""
Main API module for the Book RAG System
Sets up FastAPI application with routing and middleware
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from . import query, ingest
from ..core.config import settings
from ..core.database import db_instance
from ..core.vector_store import VectorStore
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI
    Initialize resources on startup and clean up on shutdown
    """
    # Startup
    logger.info("Initializing database connection pool...")
    await db_instance.initialize_pool()

    # Initialize required database tables
    from ..core.database import init_db_tables
    await init_db_tables()

    logger.info("Database initialized successfully")

    # Initialize vector store (dimension will be set by embedding service)
    logger.info("Initializing vector store...")
    from ..services.embedding_service import EmbeddingService
    embedding_service = EmbeddingService()
    embedding_dim = embedding_service.get_embedding_dimension()
    vector_store = VectorStore(embedding_dim=embedding_dim)
    app.state.vector_store = vector_store

    logger.info(f"Vector store initialized successfully (embedding dimension: {embedding_dim})")

    yield

    # Shutdown
    logger.info("Closing database connection pool...")
    await db_instance.close_pool()
    logger.info("Database connection pool closed")


# Create FastAPI app with lifespan
app = FastAPI(
    title="Book RAG System API",
    description="API for the Book RAG System that enables question answering based on book content",
    version="1.0.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])


@app.get("/api/v1/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    """
    # Check database connection
    try:
        await db_instance.execute_query("SELECT 1")
        db_healthy = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_healthy = False

    # Check vector store
    try:
        vector_store_healthy = await app.state.vector_store.health_check()
    except Exception as e:
        logger.error(f"Vector store health check failed: {e}")
        vector_store_healthy = False

    status = "healthy" if (db_healthy and vector_store_healthy) else "unhealthy"

    return {
        "status": status,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "checks": {
            "database": "healthy" if db_healthy else "unhealthy",
            "vector_store": "healthy" if vector_store_healthy else "unhealthy"
        }
    }


# Add CORS middleware if needed
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)