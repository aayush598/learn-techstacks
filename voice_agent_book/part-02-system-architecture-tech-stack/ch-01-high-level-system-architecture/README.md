# Chapter 01: High-Level System Architecture

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [System Architecture Overview](sec-01-system-architecture-overview.md) | End-to-end architecture diagram, component breakdown, data flow, boundaries |
| 02 | [Next.js Application Layer](sec-02-nextjs-application-layer.md) | App Router, server components, client components, API routes, middleware, edge functions |
| 03 | [Voice Processing Pipeline](sec-03-voice-processing-pipeline.md) | Real-time audio streaming, STT/TTS/VAD services, media server, WebRTC gateway |
| 04 | [AI Orchestration Layer](sec-04-ai-orchestration-layer.md) | LLM router, RAG engine, memory manager, tool execution, conversation state machine |
| 05 | [Telephony Integration Layer](sec-05-telephony-integration-layer.md) | SIP gateway, media server, IVR engine, WebRTC signaling, telephony abstraction |
| 06 | [Data & Storage Layer](sec-06-data-storage-layer.md) | PostgreSQL, Redis, MinIO, Kafka, ClickHouse — data flow and responsibility per service |
| 07 | [API Gateway & External Communication](sec-07-api-gateway-external-communication.md) | API gateway for external APIs, WebSocket server for real-time events, webhook dispatcher |
| 08 | [Monitoring & Observability Stack](sec-08-monitoring-observability-stack.md) | Prometheus metrics, structured logging (pino/loki), distributed tracing (OpenTelemetry), dashboards |

---

## Architecture Diagram (Simplified)

```
[Browser/Phone] ←→ [WebRTC/SIP] ←→ [Media Server] ←→ [Voice Pipeline]
                                        ↓
[Next.js App] ←→ [API Gateway] ←→ [Microservices] ←→ [Databases]
    ↓                    ↓                 ↓
[Dashboard]        [WebSocket]       [AI Engine/LLM]
```

---

## Key Takeaways

- Next.js serves as orchestration layer with API routes handling business logic
- Voice processing runs on separate media servers for real-time performance
- Services communicate via Kafka for async, WebSocket for real-time, REST for sync
- PostgreSQL as primary DB, Redis for caching/state, MinIO for recordings, ClickHouse for analytics
- Every component is designed for horizontal scaling from day one
