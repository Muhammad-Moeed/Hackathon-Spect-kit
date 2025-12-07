"""
Chunking service for the Book RAG System
Handles splitting book content into semantic chunks
"""
from typing import List, Dict, Any
from ..models.chunk import Chunk, ChunkRequest, ChunkMetadata
from ..core.config import settings
import tiktoken


class ChunkingService:
    """Service for chunking book content into semantic segments"""

    def __init__(self):
        self.chunk_size = settings.DEFAULT_CHUNK_SIZE
        self.overlap = settings.CHUNK_OVERLAP
        self.encoder = tiktoken.encoding_for_model("text-embedding-ada-002")

    def chunk_book_content(self, content: str, book_id: str, section: str = None) -> List[Chunk]:
        """
        Split book content into semantic chunks for vector storage
        """
        # Split content into sentences to maintain semantic boundaries
        sentences = self._split_into_sentences(content)
        chunks = []
        current_chunk = ""
        position = 0

        for i, sentence in enumerate(sentences):
            # Check if adding this sentence exceeds chunk size
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            token_count = len(self.encoder.encode(test_chunk))

            if token_count > self.chunk_size and current_chunk:
                # Finalize current chunk
                chunk = self._create_chunk(
                    content=current_chunk.strip(),
                    book_id=book_id,
                    section=section,
                    position=position
                )
                chunks.append(chunk)
                position += 1

                # Start new chunk with overlap
                overlap_sentences = current_chunk.split('. ')[-2:] if '. ' in current_chunk else [current_chunk]
                current_chunk = '. '.join([s for s in overlap_sentences if s]) + " " + sentence
            else:
                current_chunk = test_chunk

        # Add final chunk if it has content
        if current_chunk.strip():
            chunk = self._create_chunk(
                content=current_chunk.strip(),
                book_id=book_id,
                section=section,
                position=position
            )
            chunks.append(chunk)

        return chunks

    def _create_chunk(self, content: str, book_id: str, section: str = None, position: int = 0) -> Chunk:
        """
        Helper method to create a standardized chunk with metadata
        """
        token_count = len(self.encoder.encode(content))

        chunk_metadata = ChunkMetadata(
            book_id=book_id,
            section=section,
            position=position,
            page_number=None,  # Page number would need to be provided separately
            selected_text=False
        )

        return Chunk(
            content=content,
            token_count=token_count,
            metadata=chunk_metadata
        )

    def chunk_selected_text(self, selected_text: str, session_id: str) -> List[Chunk]:
        """
        Chunk user-selected text for temporary storage
        """
        # For selected text, we may want to use a different strategy
        # For now, we'll use the same approach but mark as selected_text
        chunks = self.chunk_book_content(selected_text, book_id="selected_text", section="user_selection")

        # Update metadata for selected text chunks
        for chunk in chunks:
            chunk.metadata.selected_text = True
            chunk.metadata.session_id = session_id

        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences while preserving sentence boundaries
        """
        import re
        # Split on sentence endings followed by whitespace and capital letter
        sentences = re.split(r'[.!?]+\s+', text)
        # Clean up sentences and remove empty ones
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def validate_chunk(self, chunk: Chunk) -> bool:
        """
        Validate a chunk meets requirements
        """
        if not chunk.content or not chunk.content.strip():
            return False

        if chunk.token_count and chunk.token_count <= 0:
            return False

        # If this is a selected text chunk, session_id must be present
        if chunk.metadata.selected_text and not chunk.metadata.session_id:
            return False

        return True

    def merge_chunks(self, chunks: List[Chunk], max_size: int = None) -> List[Chunk]:
        """
        Merge small chunks together to reach minimum size requirements
        """
        if not max_size:
            max_size = self.chunk_size

        if not chunks:
            return []

        merged = []
        current = chunks[0]

        for chunk in chunks[1:]:
            # Check if merging would exceed max size
            combined_content = current.content + " " + chunk.content
            combined_tokens = len(self.encoder.encode(combined_content))

            if combined_tokens <= max_size:
                # Merge the chunks
                current.content = combined_content
                current.token_count = combined_tokens
                # Update position to be the later position
                if chunk.metadata.position > current.metadata.position:
                    current.metadata.position = chunk.metadata.position
            else:
                # Keep current chunk and start a new one
                merged.append(current)
                current = chunk

        # Add the last chunk
        merged.append(current)

        return merged