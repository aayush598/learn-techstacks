# Part 02: System Architecture & Technology Stack

> **Duration:** Architecture Phase (Weeks 2-4)  
> **Goal:** Design the complete system architecture with all components, data flow, and technology decisions.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [High-Level System Architecture](ch-01-high-level-system-architecture/README.md) | Monorepo structure, microservices breakdown, component interaction, data flow diagrams |
| 02 | [Next.js Application Architecture](ch-02-nextjs-application-architecture/README.md) | App Router design, server components, API routes, middleware, edge functions |
| 03 | [Database Architecture & Data Modeling](ch-03-database-architecture-data-modeling/README.md) | PostgreSQL schema design, migrations, relationships, indexing strategy |
| 04 | [Real-Time Communication Layer](ch-04-real-time-communication-layer/README.md) | WebSocket architecture, WebRTC signaling, media servers, streaming pipelines |
| 05 | [Microservices & Service Mesh](ch-05-microservices-service-mesh/README.md) | Service boundaries, message queues (Kafka/RabbitMQ), inter-service communication, service mesh |
| 06 | [Frontend Architecture & Design System](ch-06-frontend-architecture-design-system/README.md) | Component library, state management, routing, SSR/ISR strategy, theme system |
| 07 | [API Gateway & Routing Strategy](ch-07-api-gateway-routing/README.md) | API versioning, rate limiting, auth middleware, request/response transformation |
| 08 | [Technology Stack Deep Dive](ch-08-technology-stack-deep-dive/README.md) | Complete tech stack justification, open-source alternatives, licensing considerations |
| 09 | [Data Flow & State Management](ch-09-data-flow-state-management/README.md) | Event-driven architecture, CQRS, event sourcing, state machines for call lifecycle |
| 10 | [Security Architecture](ch-10-security-architecture/README.md) | Zero-trust model, encryption strategy, secrets management, network segmentation |

---

## Key Technology Decisions

| Component | Primary Choice | Open-Source Alternative |
|-----------|---------------|------------------------|
| Framework | Next.js 14+ (App Router) | — |
| Database | PostgreSQL 16 | — |
| Cache/Queue | Redis Stack | — |
| Message Broker | Apache Kafka | RabbitMQ, NATS |
| Vector DB | pgvector | Qdrant, Chroma |
| Object Storage | MinIO | — |
| Container | Docker | — |
| Orchestration | Kubernetes (K3s) | Nomad, Docker Swarm |
| Monitoring | Prometheus + Grafana | — |
| LLM Gateway | Vercel AI SDK | LangChain, LlamaIndex |

---

## Learning Objectives

- Design a scalable monorepo architecture for a multi-service platform
- Understand how Next.js App Router fits into a real-time voice application
- Model complex domain relationships for voice agent data
- Design real-time communication pipelines for sub-200ms latency
- Implement event-driven architecture for call state management
- Choose the right database, cache, and queue for each use case
- Build a security-first architecture from day one
