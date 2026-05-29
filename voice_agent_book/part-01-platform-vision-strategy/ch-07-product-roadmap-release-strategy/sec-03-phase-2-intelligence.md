# Section 03: Phase 2 — Intelligence (Months 4-6)

## Phase Overview

Phase 2 enhances the core voice agent with intelligence features: LLM orchestration, knowledge base (RAG), sentiment analysis, and a visual agent builder. This phase transforms the platform from a basic voice pipeline into an intelligent conversational AI system.

```
Phase 2 Intelligence Features
┌─────────────────────────────────────────────────────────────────────────┐
│ Month 4: LLM & RAG              Month 5: Visual Builder + Sentiment    │
│ ┌────────────────────────────┐  ┌────────────────────────────┐        │
│ │ BYO LLM support            │  │ Visual agent builder       │        │
│ │ (OpenAI, Anthropic, Llama) │  │ (React Flow-based)        │        │
│ │ RAG knowledge base         │  │ Conditional logic          │        │
│ │ Document ingestion         │  │ Variable injection         │        │
│ │ Qdrant vector database     │  │ Real-time sentiment         │        │
│ │ Unstructured.io parsing    │  │ Emotion detection          │        │
│ │ Multi-language support (10)│  │ Agent templates            │        │
│ └────────────────────────────┘  └────────────────────────────┘        │
├─────────────────────────────────────────────────────────────────────────┤
│ Month 6: Recording + IVR + Multi-Tenant                                │
│ ┌────────────────────────────┐  ┌────────────────────────────┐        │
│ │ Call recording & search    │  │ IVR menu system            │        │
│ │ Transcript viewer          │  │ Multi-level menus          │        │
│ │ Full-text search (Elastic) │  │ DTMF + voice recognition   │        │
│ │ Recording download/export  │  │ Agent routing              │        │
│ │ Basic multi-tenant         │  │ Context passing            │        │
│ │ Tenant isolation           │  │ Queue management           │        │
│ └────────────────────────────┘  └────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Deliverables

### RAG Knowledge Base
- **Document ingestion:** Upload PDF, DOCX, TXT, website scraping → chunk → vectorize
- **Vector database:** Qdrant (self-hosted, open-source)
- **Retrieval:** Hybrid search (semantic + keyword), re-ranking, context window management
- **Sources:** Auto-updating document sync, URL monitoring
- **Use case:** Customer FAQ, product documentation, policy manuals

### Visual Agent Builder
- **Node-based flow builder:** React Flow with custom voice AI nodes
- **Node types:** Message, condition, action (CRM update, webhook), transfer-to-human, API call
- **Testing:** In-builder voice testing (simulate call)
- **Templates:** Pre-built agent templates for common use cases
- **Export/Import:** JSON export of agent configurations

### Sentiment Analysis
- **Real-time:** Per-turn sentiment scoring during call
- **Models:** Fine-tuned RoBERTa or API-based (Hume AI, Affectiva)
- **Visualization:** Sentiment trend per call, aggregate trends
- **Alerts:** Negative sentiment threshold alerts (real-time)

### Multi-Tenant (Basic)
- **Tenant isolation:** Separate database schemas per tenant
- **User management:** Users belong to tenants
- **Data isolation:** Recordings, transcripts, agents isolated per tenant
- **Tenant customization:** Basic branding (logo, colors)

## Intelligence Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Phase 2 System Architecture                          │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│ │ Knowledge    │  │ Sentiment    │  │ Visual       │                  │
│ │ Base (RAG)   │  │ Engine       │  │ Agent Builder│                  │
│ │ • Qdrant     │  │ • RoBERTa    │  │ • React Flow │                  │
│ │ • Ingest     │  │ • Hume API   │  │ • Node types │                  │
│ └──────────────┘  └──────────────┘  └──────────────┘                  │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│ │ Multi-Tenant │  │ Search       │  │ IVR Engine   │                  │
│ │ • Isolation  │  │ (Elastic)    │  │ • Menus      │                  │
│ │ • Branding   │  │ • Full-text  │  │ • DTMF       │                  │
│ └──────────────┘  └──────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Phase 2 Technical Decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| Vector DB | Qdrant, Pinecone, Weaviate | Qdrant | Open-source, self-hosted, good perf |
| Embeddings | OpenAI, Cohere, BGE | OpenAI text-embedding-3-large | Best quality |
| Visual builder | React Flow, Blockly, Rete | React Flow | Good ecosystem, voice-specific nodes |
| Search | Elasticsearch, Meilisearch, Typesense | Elasticsearch | Full-text + analytics |
| Sentiment | RoBERTa, Hume AI, Affectiva | RoBERTa (self-host) + Hume API (fallback) | Data privacy option |

## Phase 2 Team Growth

| Role | Phase 1 | Phase 2 Addition | Total |
|------|---------|-----------------|-------|
| Full-stack engineer | 2 | +1 | 3 |
| ML engineer | 1 | +1 | 2 |
| Product manager | 1 | 0 | 1 |
| Designer | 0.5 | +0.5 | 1 |
| DevOps | 0.5 | 0 | 0.5 |

## Phase 2 Budget

| Category | Monthly Cost |
|----------|-------------|
| Infrastructure | $5K-8K |
| GPU compute | $3K-5K |
| SaaS | $2K-3K |
| Compensation (6.5 FTE) | $100K-130K |
| **Total monthly** | **$110K-146K** |

## Phase 2 Exit Criteria

- [ ] RAG knowledge base operational with <500ms retrieval time
- [ ] Visual agent builder with 10+ node types
- [ ] Sentiment analysis with >85% accuracy
- [ ] Multi-tenant isolation verified (no cross-tenant data leaks)
- [ ] IVR system with multi-level menus
- [ ] 200+ active users
- [ ] 100K+ total call minutes processed
- [ ] CSAT score >4.0/5.0

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| RAG quality poor | High | 40% | Chunking optimization, re-ranking |
| Visual builder UX complex | Medium | 50% | User testing iterations, templates |
| Multi-tenant data leak | Critical | 10% | Isolation testing, pen test |
| Sentiment accuracy low | Medium | 30% | Domain fine-tuning |

## Open Source Tools Added

| Tool | Purpose | Alternative |
|------|---------|-------------|
| Qdrant | Vector database | Milvus, Weaviate |
| React Flow | Visual builder | Blockly |
| Elasticsearch | Full-text search | Meilisearch |
| Unstructured.io | Document parsing | LangChain document loaders |
| RoBERTa | Sentiment model | BERT, DistilBERT |

## Production Considerations

- RAG response time budget: <500ms (embed + retrieve + re-rank)
- Vector DB scaling: Sharded by tenant
- Agent builder performance: Lazy load node types, optimize React Flow rendering
- Sentiment processing: Batch sentiment for post-call, real-time for critical alerts
- Multi-tenant: Row-level security in PostgreSQL, tenant ID in every query
