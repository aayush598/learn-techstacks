# Section 01: System Architecture Overview

## End-to-End Architecture

The AI Voice Agent SaaS platform follows a **microservices-oriented architecture** with clear separation between the voice processing pipeline, application layer, data layer, and infrastructure layer. This section provides a comprehensive overview of how all components interconnect.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Browser  │  │  Mobile  │  │  Phone   │  │  WebSocket SDK    │  │
│  │ (React)  │  │  (App)   │  │ (PSTN)   │  │  (3rd Party)      │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬──────────┘  │
│       │              │              │                 │             │
└───────┼──────────────┼──────────────┼─────────────────┼─────────────┘
        │              │              │                 │
┌───────┼──────────────┼──────────────┼─────────────────┼─────────────┐
│       ▼              ▼              ▼                 ▼             │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                  API GATEWAY LAYER                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │   │
│  │  │  Auth    │  │  Rate    │  │  Route   │  │  TLS     │     │   │
│  │  │  Proxy   │  │  Limiter│  │  Resolver│  │  Term    │     │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │   │
│  └────────────────────────────┬─────────────────────────────────┘   │
│                               │                                     │
│  ┌────────────────────────────┼─────────────────────────────────┐   │
│  │                     APPLICATION LAYER                         │   │
│  │  ┌─────────────────┐  ┌───┴──────────┐  ┌─────────────────┐  │   │
│  │  │  Next.js App    │  │  WebSocket   │  │  Media Server   │  │   │
│  │  │  (Dashboard,    │  │  Server      │  │  (Janus/Mediasoup)│  │   │
│  │  │   APIs, SSR)    │  │  (Socket.IO) │  │                 │  │   │
│  │  └────────┬────────┘  └──────┬───────┘  └────────┬────────┘  │   │
│  └───────────┼──────────────────┼────────────────────┼───────────┘   │
│              │                  │                    │               │
│  ┌───────────┼──────────────────┼────────────────────┼───────────┐   │
│  │           ▼                  ▼                    ▼           │   │
│  │                     MICROSERVICES LAYER                        │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │   │
│  │  │  Agent   │ │  Call    │ │  Voice   │ │   AI     │         │   │
│  │  │  Service │ │  Service │ │  Service │ │  Service  │         │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │   │
│  │  │ Campaign │ │  Billing │ │  Notif.  │ │  Auth    │         │   │
│  │  │  Service │ │  Service │ │  Service │ │  Service  │         │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────────────┐   │
│  │                    DATA LAYER                                  │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │   │
│  │  │PostgreSQL│ │  Redis   │ │  MinIO   │ │ClickHouse│          │   │
│  │  │(Primary) │ │(Cache)   │ │(Objects) │ │(Analytics)│         │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │   │
│  │  ┌──────────────────────────────────────────────────┐          │   │
│  │  │              Apache Kafka (Events)                │          │   │
│  │  └──────────────────────────────────────────────────┘          │   │
│  └───────────────────────────────────────────────────────────────┘   │
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────────────┐   │
│  │                OBSERVABILITY LAYER                             │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │   │
│  │  │Prometheus│ │  Loki    │ │  Tempo   │ │  Grafana │          │   │
│  │  │(Metrics) │ │(Logs)    │ │(Traces)  │ │(Dashboards)│         │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │   │
│  └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Client Layer
- **Browser Application**: Next.js 14+ React application served via CDN. Handles dashboard UI, real-time call monitoring, agent builder, and analytics views.
- **Mobile Application**: React Native app for on-the-go monitoring and call management.
- **Phone (PSTN)**: Traditional telephone network integration via SIP trunking. No client software needed — calls route through the telephony gateway.
- **WebSocket SDK**: JavaScript/TypeScript SDK for third-party integrations to receive real-time call events.

### 2. API Gateway Layer
The API Gateway (implemented via Next.js API routes and middleware) serves as the single entry point for all external traffic. It handles:
- **Authentication**: Validates API keys, JWT tokens, OAuth 2.0 tokens
- **Rate Limiting**: Tier-based (Free: 10 req/min, Enterprise: custom)
- **Request Routing**: Maps URL patterns to internal microservices
- **TLS Termination**: HTTPS termination at the edge

### 3. Application Layer
- **Next.js Application**: Serves as the orchestration hub. App Router with route groups for dashboard, admin portal, and developer portal. Server Components for data fetching, Client Components for interactive features.
- **WebSocket Server**: Socket.IO-based real-time communication for dashboard updates, call monitoring, and agent state changes.
- **Media Server**: Janus or Mediasoup handles all real-time audio processing — WebRTC termination, audio mixing, recording, and codec transcoding.

### 4. Microservices Layer
Seven core microservices, each owning its data store:
| Service | Responsibility | Technology |
|---------|---------------|------------|
| Agent Service | Agent CRUD, versioning, builder | Next.js API + PostgreSQL |
| Call Service | Call lifecycle, routing, state machine | Node.js + PostgreSQL |
| Voice Service | STT, TTS, VAD, audio pipeline | Python/Node.js + GPU |
| AI Service | LLM orchestration, RAG, memory | Node.js + pgvector |
| Campaign Service | Outbound dialing, contact mgmt | Node.js + PostgreSQL |
| Billing Service | Usage metering, invoicing | Node.js + PostgreSQL + Redis |
| Notification Service | Alerts, webhooks, emails | Node.js + Redis |

### 5. Data Layer
- **PostgreSQL 16**: Primary database with pgvector for embeddings, row-level security for multi-tenancy
- **Redis 7**: Caching, session storage, rate limiting, pub/sub for WebSocket scaling
- **MinIO**: S3-compatible object storage for call recordings, exports, and file uploads
- **ClickHouse**: Column-oriented analytics database for usage metrics and reporting
- **Apache Kafka**: Event backbone for async communication between services

### 6. Observability Layer
- **Prometheus**: Metrics collection and alerting
- **Loki**: Log aggregation via pino-structured logging
- **Tempo**: Distributed tracing with OpenTelemetry
- **Grafana**: Unified dashboards and alerting

## Data Flow Patterns

### Synchronous Flow (REST)
```
Client → API Gateway → Next.js API Route → Microservice → Database
```
Used for CRUD operations: agent configuration, campaign management, user settings.

### Real-Time Flow (WebSocket)
```
Browser ←→ WebSocket Server ←→ Redis Pub/Sub ←→ Microservices
```
Used for live call status, transcription streaming, agent state updates.

### Voice Flow (WebRTC)
```
Phone ←→ SIP Gateway ←→ Media Server ←→ Voice Service (STT/TTS/VAD)
                                        ↓
                                   AI Service (LLM)
```
Used for real-time voice conversations with AI agents.

### Event-Driven Flow (Kafka)
```
Service A → Event → Kafka Topic → Consumer Group → Service B
```
Used for async workflows: call completion triggers billing, transcription, notification.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Monorepo vs Polyrepo | Monorepo (pnpm workspaces) | Shared types, easier refactoring, unified CI |
| Next.js as orchestrator | App Router + API routes | Unified framework for dashboard and APIs |
| Database per service | PostgreSQL per service | Isolation, independent scaling, clear ownership |
| Kafka as event bus | Apache Kafka | Durability, replayability, ecosystem support |
| WebSocket vs SSE | WebSocket (Socket.IO) | Bidirectional communication, room support |

## Integration Points with Other Parts

- **Part 01 (Platform Vision)** — Architecture realizes the product vision
- **Part 03 (Dev Setup)** — Local development mirrors production architecture
- **Part 04 (Core Voice Engine)** — Voice pipeline plugs into media server
- **Part 05 (AI Conversation)** — AI orchestration layer consumes voice service output
- **Part 24 (Scaling)** — Each component designed for horizontal scaling

## Production Considerations

- **High Availability**: All services run with at least 2 replicas across availability zones
- **Disaster Recovery**: PostgreSQL streaming replication to standby, Kafka cross-region mirroring
- **Scaling Strategy**: Horizontal pod autoscaling based on CPU/memory and custom metrics (queue depth, active calls)
- **Security**: Zero-trust network with mTLS between services, all traffic encrypted in transit
- **Cost Optimization**: Spot instances for voice processing (GPU), reserved instances for databases
