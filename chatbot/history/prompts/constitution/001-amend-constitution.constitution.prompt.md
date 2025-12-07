---
id: 001
title: Amend Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 1-book-spec
user: user
command: /sp.constitution
labels: [constitution, spec-driven-development]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - history/prompts/constitution/001-amend-constitution.constitution.prompt.md
tests:
 - none
---

## Prompt

```
Project: Integrated RAG Chatbot for Published Book (Project 2)

Core principles:

Truthful retrieval — chatbot answers must only use retrieved book text or user-selected text.

Faithfulness — zero hallucinations; no invented facts.

Technical precision — architecture & code must follow correct usage of OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud Free Tier.

User-centric clarity — explanations must be understandable for beginner–intermediate developers.

Security — do not expose API keys, internal configs, or unsafe instructions.

Key standards:

Retrieval grounding: every answer must be based strictly on retrieved chunks.

Dual retrieval modes:

Full-book RAG retrieval

Highlighted text–only retrieval

Architecture must follow: Ingestion → Chunking → Embedding → Vector Storage → Query → Re-ranking → Generation.

Code must be clean, modular, and production-ready.

Qdrant is used for vector search only; Neon Postgres for metadata & logs.

If retrieval returns no relevant chunk, respond with:
"No relevant information found in the book section you selected."

All FastAPI endpoints must be async when appropriate.

Standardized error handling rules: retrieval failure fallback, missing embeddings fallback, and auto-expansion for too-small selected text.

Constraints:

Chatbot answers ONLY from Project 1 book content or user-selected text.

Framework lock: FastAPI + Qdrant Cloud + Neon Postgres + OpenAI Agents/ChatKit.

No external unapproved libraries.

Latency target: <1.5s retrieval, <3s total.

Success criteria:

All chatbot answers grounded strictly in book content.

Correct switching between full-book RAG mode and highlighted-text mode.

Working end-to-end backend: FastAPI + Qdrant + Postgres + OpenAI Agent.

Zero hallucinations.

All components containerized and deployable.

Smooth integration into the published book's UI.

Analytics and logs stored in Postgres.
```

## Response snapshot

Created a new constitution file for the Integrated RAG Chatbot for Published Book project with the following principles:
- Truthful Retrieval: Chatbot answers must only use retrieved book text or user-selected text. No hallucinations allowed.
- Technical Precision: Architecture & code must follow correct usage of OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud Free Tier.
- User-Centric Clarity: Explanations must be understandable for beginner–intermediate developers.
- Security: Do not expose API keys, internal configs, or unsafe instructions.
- Retrieval Grounding: Every answer must be based strictly on retrieved chunks. If retrieval returns no relevant chunk, respond with: 'No relevant information found in the book section you selected.'
- Dual Retrieval Modes: Support both Full-book RAG retrieval and Highlighted text–only retrieval modes.

Also included Architecture Standards and Development Constraints sections based on the requirements.

## Outcome

- ✅ Impact: Created new constitution file with project-specific principles
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with new content
- 🔁 Next prompts: Continue with project implementation
- 🧠 Reflection: Constitution now properly reflects the RAG chatbot project requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Begin feature specification based on constitution