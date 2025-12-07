"""
Script to ingest book content into vector database
Usage: python scripts/ingest_book.py <book_file_path> <book_id> [section]
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.chunking_service import ChunkingService
from src.services.vector_store_service import VectorStoreService
from src.core.config import validate_settings


async def ingest_book(book_file_path: str, book_id: str, section: str = None):
    """
    Ingest book content from a text file into vector database
    
    Args:
        book_file_path: Path to the book text file
        book_id: Unique identifier for the book
        section: Optional section name (e.g., "Chapter 1")
    """
    # Validate environment variables
    try:
        validate_settings()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set up your .env file with required variables:")
        print("  - OPENAI_API_KEY")
        print("  - QDRANT_URL")
        print("  - QDRANT_API_KEY")
        print("  - NEON_POSTGRES_URL")
        return
    
    # Check if file exists
    if not os.path.exists(book_file_path):
        print(f"❌ Error: File not found: {book_file_path}")
        return
    
    try:
        # Read book content
        print(f"📖 Reading book file: {book_file_path}")
        with open(book_file_path, 'r', encoding='utf-8') as f:
            book_content = f.read()
        
        if not book_content.strip():
            print("❌ Error: Book file is empty")
            return
        
        print(f"✅ Read {len(book_content)} characters from file")
        
        # Initialize services
        print("\n🔧 Initializing services...")
        chunking_service = ChunkingService()
        vector_store_service = VectorStoreService()
        
        # Chunk the book content
        print(f"\n✂️  Chunking book content (book_id: {book_id})...")
        chunks = chunking_service.chunk_book_content(book_content, book_id, section)
        print(f"✅ Created {len(chunks)} chunks")
        
        # Generate embeddings
        print(f"\n🧮 Generating embeddings using OpenAI...")
        embedded_chunks = await vector_store_service.embed_chunks(chunks)
        print(f"✅ Generated embeddings for {len(embedded_chunks)} chunks")
        
        # Store in vector database
        print(f"\n💾 Storing chunks in Qdrant vector database...")
        await vector_store_service.store_chunks(embedded_chunks)
        print(f"✅ Successfully stored {len(embedded_chunks)} chunks in vector database")
        
        print(f"\n🎉 Book ingestion completed successfully!")
        print(f"   Book ID: {book_id}")
        print(f"   Section: {section or 'N/A'}")
        print(f"   Total Chunks: {len(embedded_chunks)}")
        print(f"\nYou can now query the book using the /api/v1/query endpoint")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point for the script"""
    if len(sys.argv) < 3:
        print("Usage: python scripts/ingest_book.py <book_file_path> <book_id> [section]")
        print("\nExample:")
        print("  python scripts/ingest_book.py data/book.txt book-001")
        print("  python scripts/ingest_book.py data/book.txt book-001 'Chapter 1'")
        sys.exit(1)
    
    book_file_path = sys.argv[1]
    book_id = sys.argv[2]
    section = sys.argv[3] if len(sys.argv) > 3 else None
    
    asyncio.run(ingest_book(book_file_path, book_id, section))


if __name__ == "__main__":
    main()

