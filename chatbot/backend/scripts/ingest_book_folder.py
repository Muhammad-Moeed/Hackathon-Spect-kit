"""
Script to ingest book content from folder containing multiple .mdx files
Usage: python scripts/ingest_book_folder.py <folder_path> <book_id> [section_prefix]
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


def read_mdx_files(folder_path: Path, section_prefix: str = ""):
    """
    Recursively read all .mdx files from folder and subfolders
    Returns: List of tuples (content, section_name)
    """
    all_content = []
    
    # Find all .mdx files recursively
    mdx_files = list(folder_path.rglob("*.mdx"))
    
    if not mdx_files:
        print(f"❌ No .mdx files found in {folder_path}")
        return []
    
    print(f"📚 Found {len(mdx_files)} .mdx files")
    
    for mdx_file in sorted(mdx_files):
        try:
            # Read file content
            with open(mdx_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                print(f"⚠️  Skipping empty file: {mdx_file.name}")
                continue
            
            # Create section name from folder structure
            relative_path = mdx_file.relative_to(folder_path)
            section_name = str(relative_path.parent).replace("\\", " / ") if relative_path.parent != Path(".") else ""
            file_name = mdx_file.stem  # filename without extension
            
            if section_name and section_prefix:
                full_section = f"{section_prefix} / {section_name} / {file_name}"
            elif section_name:
                full_section = f"{section_name} / {file_name}"
            elif section_prefix:
                full_section = f"{section_prefix} / {file_name}"
            else:
                full_section = file_name
            
            all_content.append((content, full_section))
            print(f"✅ Read: {mdx_file.name} ({len(content)} chars)")
            
        except Exception as e:
            print(f"❌ Error reading {mdx_file}: {e}")
            continue
    
    return all_content


async def ingest_book_from_folder(folder_path: str, book_id: str, section_prefix: str = ""):
    """
    Ingest book content from a folder containing .mdx files
    
    Args:
        folder_path: Path to the folder containing .mdx files
        book_id: Unique identifier for the book
        section_prefix: Optional prefix for section names (e.g., "Module")
    """
    # Validate environment variables
    try:
        validate_settings()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nPlease set up your .env file with required variables:")
        print("  - COHERE_API_KEY (or OPENAI_API_KEY if using OpenAI)")
        print("  - QDRANT_URL")
        print("  - QDRANT_API_KEY")
        print("  - NEON_POSTGRES_URL")
        return
    
    # Check if folder exists
    folder = Path(folder_path)
    if not folder.exists():
        print(f"❌ Error: Folder not found: {folder_path}")
        return
    
    if not folder.is_dir():
        print(f"❌ Error: Path is not a directory: {folder_path}")
        return
    
    try:
        # Read all .mdx files
        print(f"\n📖 Reading .mdx files from: {folder_path}")
        files_content = read_mdx_files(folder, section_prefix)
        
        if not files_content:
            print("❌ No content found to ingest")
            return
        
        total_content = len(files_content)
        print(f"\n✅ Successfully read {total_content} files")
        
        # Initialize services
        print("\n🔧 Initializing services...")
        chunking_service = ChunkingService()
        vector_store_service = VectorStoreService()
        
        all_chunks = []
        
        # Process each file
        print(f"\n✂️  Chunking content from {total_content} files...")
        for idx, (content, section) in enumerate(files_content, 1):
            print(f"   Processing file {idx}/{total_content}: {section}")
            chunks = chunking_service.chunk_book_content(content, book_id, section)
            all_chunks.extend(chunks)
            print(f"   → Created {len(chunks)} chunks")
        
        print(f"\n✅ Total chunks created: {len(all_chunks)}")
        
        # Generate embeddings (in batches to avoid memory issues and rate limits)
        print(f"\n🧮 Generating embeddings using Cohere...")
        print(f"   ⚠️  Note: Cohere free tier has 100k tokens/minute limit")
        print(f"   ⚠️  Adding delays between batches to respect rate limits")
        
        batch_size = 10  # Smaller batches to avoid rate limits (10 chunks per batch)
        embedded_chunks = []
        total_batches = (len(all_chunks) - 1) // batch_size + 1
        
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i+batch_size]
            batch_num = i // batch_size + 1
            print(f"\n   Processing batch {batch_num}/{total_batches} ({len(batch)} chunks)...")
            
            try:
                embedded_batch = await vector_store_service.embed_chunks(batch)
                embedded_chunks.extend(embedded_batch)
                print(f"   ✅ Batch {batch_num} completed ({len(embedded_batch)} embeddings)")
                
                # Add delay between batches to respect rate limits (except for last batch)
                if batch_num < total_batches:
                    delay_seconds = 5  # 5 second delay between batches (safer for rate limits)
                    print(f"   ⏳ Waiting {delay_seconds} seconds before next batch...")
                    await asyncio.sleep(delay_seconds)
                    
            except ValueError as e:
                if "rate limit" in str(e).lower():
                    print(f"\n   ⚠️  Rate limit hit at batch {batch_num}")
                    print(f"   💡 Solution: Wait 60 seconds and resume from batch {batch_num}")
                    print(f"   💡 Or run with smaller batch size")
                    print(f"\n   Progress saved: {len(embedded_chunks)}/{len(all_chunks)} chunks embedded")
                    raise e
                else:
                    raise e
        
        print(f"✅ Generated embeddings for {len(embedded_chunks)} chunks")
        
        # Store in vector database (also in batches)
        print(f"\n💾 Storing chunks in Qdrant vector database...")
        store_batch_size = 100
        for i in range(0, len(embedded_chunks), store_batch_size):
            batch = embedded_chunks[i:i+store_batch_size]
            print(f"   Storing batch {i//store_batch_size + 1}/{(len(embedded_chunks)-1)//store_batch_size + 1} ({len(batch)} chunks)...")
            await vector_store_service.store_chunks(batch)
        
        print(f"\n🎉 Book ingestion completed successfully!")
        print(f"   Book ID: {book_id}")
        print(f"   Source Folder: {folder_path}")
        print(f"   Total Files: {total_content}")
        print(f"   Total Chunks: {len(embedded_chunks)}")
        print(f"\nYou can now query the book using the /api/v1/query endpoint")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point for the script"""
    if len(sys.argv) < 3:
        print("Usage: python scripts/ingest_book_folder.py <folder_path> <book_id> [section_prefix]")
        print("\nExample:")
        print('  python scripts/ingest_book_folder.py "D:\\moeed projects\\hackathon3\\Hackathon-Spect-kit\\book\\docs" book-001')
        print('  python scripts/ingest_book_folder.py "D:\\path\\to\\docs" book-001 "Module"')
        sys.exit(1)
    
    folder_path = sys.argv[1]
    book_id = sys.argv[2]
    section_prefix = sys.argv[3] if len(sys.argv) > 3 else ""
    
    asyncio.run(ingest_book_from_folder(folder_path, book_id, section_prefix))


if __name__ == "__main__":
    main()

