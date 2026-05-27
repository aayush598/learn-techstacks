# Chapter 05: Microservices & Service Mesh

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Service Decomposition Strategy](sec-01-service-decomposition-strategy.md) | Domain-driven boundaries: Agent Service, Call Service, Voice Service, AI Service, Billing Service, etc. |
| 02 | [Service Communication Patterns](sec-02-service-communication-patterns.md) | REST for sync, Kafka for async events, WebSocket for real-time, gRPC for internal high-throughput |
| 03 | [Message Broker (Apache Kafka)](sec-03-message-broker-apache-kafka.md) | Topic design, event schema (Avro), producer/consumer patterns, partitions, retention |
| 04 | [Service Mesh (Istio/Linkerd)](sec-04-service-mesh-istio-linkerd.md) | Traffic management, service discovery, mTLS, observability, circuit breaking |
| 05 | [Event-Driven Architecture](sec-05-event-driven-architecture.md) | Event storming, event catalog, CQRS implementation, event sourcing for call state |
| 06 | [Service Boundaries & Contracts](sec-06-service-boundaries-contracts.md) | Each service's responsibility, API contracts, data ownership, shared kernel vs bounded context |
| 07 | [Inter-Service Auth & Security](sec-07-inter-service-auth-security.md) | mTLS, service accounts, JWT between services, network policies, secret propagation |

---

## Service Boundaries

| Service | Responsibility | Data Store |
|---------|---------------|------------|
| Agent Service | Agent CRUD, builder, versioning | PostgreSQL |
| Call Service | Call lifecycle, routing, state machine | PostgreSQL |
| Voice Service | STT, TTS, VAD, audio processing | Ephemeral |
| AI Service | LLM orchestration, RAG, memory | PostgreSQL + pgvector |
| Campaign Service | Outbound dialing, contact management | PostgreSQL |
| Billing Service | Usage metering, invoicing, plans | PostgreSQL + Redis |
| Notification Service | Alerts, webhooks, emails | Redis + PostgreSQL |

---

## Key Takeaways

- 7 core microservices plus supporting services (auth, notification, file)
- Kafka as event backbone for async, reliable communication
- gRPC for high-throughput internal communication (voice pipeline)
- Istio for service mesh with mTLS, observability, and traffic control
- Each service owns its data store (database-per-service pattern)
- Event sourcing for call state machine ensures auditability
