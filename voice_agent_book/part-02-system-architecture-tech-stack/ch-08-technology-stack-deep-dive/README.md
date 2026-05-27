# Chapter 08: Technology Stack Deep Dive

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Frontend Stack](sec-01-frontend-stack.md) | Next.js 14+, React 18, TypeScript 5, Tailwind CSS, Radix UI, TanStack Query |
| 02 | [Backend Stack](sec-02-backend-stack.md) | Next.js API routes, tRPC/Hono, Prisma ORM, BullMQ, Zod validation |
| 03 | [Database & Storage Stack](sec-03-database-storage-stack.md) | PostgreSQL 16, pgvector, Redis 7, MinIO, ClickHouse, Kafka |
| 04 | [Voice & AI Stack](sec-04-voice-ai-stack.md) | Whisper, Coqui TTS, Silero VAD, Vercel AI SDK, LangChain, pgvector |
| 05 | [DevOps & Infrastructure Stack](sec-05-devops-infrastructure-stack.md) | Docker, K3s, Helm, ArgoCD, Terraform, GitHub Actions, Prometheus, Grafana |
| 06 | [Open-Source vs Proprietary Trade-offs](sec-06-open-source-vs-proprietary-tradeoffs.md) | When to use open-source, when to pay, build vs buy decision framework |
| 07 | [License Compatibility](sec-07-license-compatibility.md) | MIT, Apache 2.0, AGPL, GPL, BSD — compatibility matrix for dependencies |
| 08 | [Cost Analysis of Stack](sec-08-cost-analysis-of-stack.md) | Infrastructure costs per tier, open-source savings, scaling cost projections |

---

## Complete Stack Summary

| Layer | Technology | License | Cost |
|-------|-----------|---------|------|
| Framework | Next.js 14 | MIT | Free |
| Language | TypeScript 5 | MIT | Free |
| Database | PostgreSQL 16 | PostgreSQL | Free |
| Cache | Redis 7 | BSD | Free |
| Queue | BullMQ + Redis | MIT | Free |
| Voice Pipeline | Whisper + Coqui + Silero | MIT | Free |
| AI SDK | Vercel AI SDK | MIT | Free |
| Vector Search | pgvector | PostgreSQL | Free |
| Monitoring | Prometheus + Grafana | Apache 2.0 | Free |
| Orchestration | K3s | Apache 2.0 | Free |

---

## Key Takeaways

- Entire stack runs on open-source software with permissive licenses
- PostgreSQL as the single database for both relational and vector data
- Redis handles caching, sessions, rate limiting, and pub/sub
- MinIO replaces AWS S3 for object storage
- Prometheus + Grafana for monitoring at no license cost
- Estimated infrastructure cost: $200-500/mo for MVP scale
