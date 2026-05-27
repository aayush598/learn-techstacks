# Part 13: Knowledge Base & RAG Engine

> **Duration:** Knowledge Phase (Weeks 14-22)  
> **Goal:** Build a production-grade Retrieval-Augmented Generation (RAG) system with document ingestion, vector search, and knowledge management.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [RAG Architecture & Pipeline](ch-01-rag-architecture-pipeline/README.md) | Ingestion → Chunking → Embedding → Indexing → Retrieval → Generation pipeline |
| 02 | [Document Ingestion System](ch-02-document-ingestion-system/README.md) | PDF/DOCX/TXT parsing (pdf-parse, mammoth), web scraping, Notion/Confluence connectors |
| 03 | [Text Chunking Strategies](ch-03-text-chunking-strategies/README.md) | Fixed-size, semantic, recursive, document-aware chunking, overlap strategies, chunk metadata |
| 04 | [Vector Embeddings & Model Selection](ch-04-vector-embeddings-model-selection/README.md) | Open-source embedding models (BGE, E5, Instructor), OpenAI embeddings, embedding dimensions, batching |
| 05 | [Vector Database with pgvector](ch-05-vector-database-pgvector/README.md) | pgvector setup, index types (IVFFlat, HNSW), similarity search, hybrid search, metadata filtering |
| 06 | [Semantic Search & Retrieval](ch-06-semantic-search-retrieval/README.md) | Query embedding, top-K retrieval, similarity scoring, hybrid keyword+vector search, re-ranking |
| 07 | [Knowledge Base Management UI](ch-07-knowledge-base-management-ui/README.md) | Document upload, status tracking, chunk preview, re-indexing, version history, search testing |
| 08 | [Confidence Thresholds & Flagging](ch-08-confidence-thresholds-flagging/README.md) | Relevance scoring, confidence threshold, low-confidence flags, fallback handling, hallucination prevention |
| 09 | [FAQ Auto-Generation](ch-09-faq-auto-generation/README.md) | FAQ extraction from documents, Q&A pair generation, category detection, FAQ publishing |
| 10 | [Knowledge Gap Detection](ch-10-knowledge-gap-detection/README.md) | Unanswered question tracking, gap analysis reports, suggested document topics, coverage scoring |

---

## RAG Pipeline Flow

```
Document Upload → Parse → Chunk → Embed → Store (pgvector)
                                            ↓
User Query → STT → Embed Query → Vector Search → Retrieve Chunks
                                            ↓
                                        Context Assembly
                                            ↓
                                        LLM Generation
                                            ↓
                                        Response → TTS
```

---

## Key Open-Source Tools

- **pgvector** (PostgreSQL) — Vector similarity search
- **LangChain** (MIT) — RAG orchestration
- **Transformers.js** (Apache 2.0) — Embedding models
- **pdf-parse** (MIT) — PDF parsing
- **Mammoth** (MIT) — DOCX parsing
- **Cheerio** (MIT) — Web scraping
- **BGE-small-en** (MIT) — Open-source embedding model

---

## Learning Objectives

- Design a complete RAG pipeline from ingestion to generation
- Build a document ingestion system supporting multiple formats
- Implement optimal chunking strategies for different document types
- Select and deploy open-source embedding models
- Configure pgvector for efficient similarity search at scale
- Build semantic search with hybrid keyword+vector retrieval
- Create a knowledge base management UI for non-technical users
- Implement confidence thresholds to prevent hallucination
- Build auto-FAQ generation from existing documents
- Detect and report knowledge gaps for continuous improvement
