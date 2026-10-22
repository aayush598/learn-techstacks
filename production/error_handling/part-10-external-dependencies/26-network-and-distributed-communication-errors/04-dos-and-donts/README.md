# Chapter 26 — Dos and Don'ts

> Part X · Chapter 26 · All subsections 26.1–26.20 · _Estimated reading time: 10 min_

## Dos

| ✅ Do | Rationale |
| ----- | --------- |
| **Classify by phase** (connect/write/read/handshake/dns) | Enables correct retry/ambiguity decisions. |
| **Treat read/write timeouts after send as ambiguous** | Remote may have succeeded. |
| **Use idempotency keys for mutations** | Required for safe retries. |
| **Do status lookup on ambiguity** | Safest way to resolve for critical ops. |
| **Validate pooled connections** | Avoid half-open issues. |
| **Expect duplicates** (webhooks/queues) | Implement deduplication. |
| **Handle LB/gateway errors explicitly** | 504 is ambiguous, different from 503. |
| **Set timeouts everywhere** | Connect, read, pool acquire. |
| **Use bulkheads per dependency** | Prevent cascading failures. |
| **Translate at boundaries** | Keep transport separate from domain. |

## Don'ts

| ❌ Don't | Why |
| -------- | --- |
| **Retry TLS/cert errors** | Configuration issues, won't fix. |
| **Retry DNS config errors** | Usually misconfiguration. |
| **Blindly retry read timeouts** | Risk of double side effects. |
| **Retry non-idempotent on ambiguity** | Dangerous for money/state. |
| **Treat all network errors same** | Wrong policy. |
| **Ignore GOAWAY/connection termination** | Causes retry on closed connections. |
| **Assume ordering** | Distributed systems don't guarantee. |
| **Trust pooled connections blindly** | Half-open causes loops. |
| **Conflate 503 and 504** | Different semantics/ambiguity. |
| **Assume partitions won't happen** | Design for them. |

## Quick checklist

- [ ] Phase-aware classification in place.
- [ ] Ambiguity handling for critical mutations.
- [ ] Idempotency + deduplication strategies.
- [ ] Pools validated, timeouts set, bulkheads configured.

## Related

- [Chapter 26 README](../README.md)
- [Ambiguous Remote Outcomes](../02-deep-dive/02-ambiguous-remote-outcomes.md)
- [Network Error Classification Code](../03-practical-examples/01-network-error-classification-code.md)
- [Glossary](../../../GLOSSARY.md)
