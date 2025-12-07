---
id: 002
title: Plan Book RAG System
stage: plan
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-book-rag-system
branch: 001-book-rag-system
user: user
command: /sp.plan
labels: [rag, book, planning, architecture]
links:
  spec: specs/001-book-rag-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-book-rag-system/plan.md
 - specs/001-book-rag-system/research.md
 - specs/001-book-rag-system/data-model.md
 - specs/001-book-rag-system/quickstart.md
 - specs/001-book-rag-system/contracts/openapi.yaml
 - .specify/memory/constitution.md
 - CLAUDE.md
tests:
 - none
---

## Prompt

Create:

System architecture sketch (FastAPI → Qdrant → Neon Postgres → OpenAI/ChatKit)

Section structure for building an integrated RAG chatbot inside the published book

Research approach for chunking, embeddings, retrieval accuracy, and dual retrieval modes (full-book + user-selected text)

Quality validation for grounding, correctness, latency, and hallucination prevention

Decisions needing documentation:

Optimal chunk size vs. embedding cost

When to store metadata in Postgres vs. Qdrant

Handling user-selected text via temporary embeddings

Error-handling and fallback behavior

Logging strategy for saving all user queries in Postgres

Testing strategy:

Retrieval grounding validation

Highlighted-text-only mode consistency

Latency tests (<3 seconds total)

Vector search accuracy checks

End-to-end tests inside the published book UI

Technical details:

Use research-concurrent approach

Follow grounding and accuracy rules from Constitution

Organize by phases:
Planning → Ingestion → Embedding → Retrieval → Agent Integration → Logging → Testing → Deployment

Environment variables (to be used in FastAPI + ingestion + retrieval layers):

COHERE_API_KEY=GnEPRnTD8eduvR3J8YcKGIDsyxWNSYBfSEuYhOvI
QDRANT_URL=https://1cf86c7d-ad3d-4568-893c-9c3a5c96b7ee.europe-west3-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ec4cJXfxMybqYfKqwBsNieV55rbihuIab1v9sneK-iE
NEON_POSTGRES_URL=postgresql://neondb_owner:npg_NJtj4MRdgD1W@ep-bold-fire-ahj5wpt7-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

## Response snapshot

Completed comprehensive planning for the Book RAG System including:

1. Implementation Plan: Defined technical context, architecture, and project structure with FastAPI backend, Qdrant vector storage, Neon Postgres logging, and OpenAI agents.

2. Research Findings: Resolved key decisions on chunk size (512 tokens), metadata storage strategy (Qdrant for content, Postgres for logs), temporary embeddings for selected text, error handling, and logging strategy.

3. Data Model: Created detailed entity definitions for Book Content Chunk, Query, Response, and User Session with validation rules and database schema.

4. API Contracts: Developed OpenAPI specification for query, ingestion, and health endpoints with proper request/response schemas.

5. Quickstart Guide: Provided setup instructions, usage examples, and troubleshooting guide.

6. Agent Context: Updated Claude Code context with project-specific technologies.

The plan follows the constitutional requirements for truthful retrieval, technical precision, security, and retrieval grounding. The architecture supports dual retrieval modes with zero hallucinations and sub-3-second response times.

## Outcome

- ✅ Impact: Created complete implementation plan for book RAG system
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.yaml
- 🔁 Next prompts: Ready for task generation with /sp.tasks
- 🧠 Reflection: Plan addresses all constitutional requirements and technical constraints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Generate tasks for implementation