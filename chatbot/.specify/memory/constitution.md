<!-- Sync Impact Report:
Version change: N/A → 1.0.0
Added sections: All principles and sections based on project requirements
Removed sections: Template placeholders
Templates requiring updates: N/A (new constitution)
Follow-up TODOs: None
-->
# Integrated RAG Chatbot for Published Book Constitution


## Core Principles

### Truthful Retrieval
Chatbot answers must only use retrieved book text or user-selected text. No hallucinations allowed.

### Technical Precision
Architecture & code must follow correct usage of OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud Free Tier.

### User-Centric Clarity
Explanations must be understandable for beginner–intermediate developers.

### Security
Do not expose API keys, internal configs, or unsafe instructions.

### Retrieval Grounding
Every answer must be based strictly on retrieved chunks. If retrieval returns no relevant chunk, respond with: 'No relevant information found in the book section you selected.'

### Dual Retrieval Modes
Support both Full-book RAG retrieval and Highlighted text–only retrieval modes.


## Architecture Standards

Architecture must follow: Ingestion → Chunking → Embedding → Vector Storage → Query → Re-ranking → Generation. Code must be clean, modular, and production-ready. Qdrant is used for vector search only; Neon Postgres for metadata & logs. All FastAPI endpoints must be async when appropriate.


## Development Constraints

Chatbot answers ONLY from Project 1 book content or user-selected text. Framework lock: FastAPI + Qdrant Cloud + Neon Postgres + OpenAI Agents/ChatKit. No external unapproved libraries. Latency target: <1.5s retrieval, <3s total.


## Governance

All outputs strictly follow the user intent. Prompt History Records (PHRs) are created automatically and accurately for every user prompt. Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions. All changes are small, testable, and reference code precisely. Standardized error handling rules: retrieval failure fallback, missing embeddings fallback, and auto-expansion for too-small selected text.

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07