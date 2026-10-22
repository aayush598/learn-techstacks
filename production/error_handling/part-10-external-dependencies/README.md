# Part X — External Dependencies and Integration Errors

> _Estimated reading time: 90–110 min_  
> **Prerequisite:** [Part VI — Error Boundaries and Translation](../part-06-boundaries-and-translation/README.md), [Part VIII — HTTP and API Error Handling](../part-08-http-and-api/README.md)

## One-sentence summary

**Treat every network call and every third-party API as an untrusted boundary**: classify upstream failures, translate them to stable internal errors, and decide containment (retry, degrade, fallback, or fail) without leaking vendor details.

## Why this part matters in production

At **Acme SaaS**, **Checkout** calls **Stripe** to create payment intents; **WebhookIngest** receives provider callbacks; **ExportJob** may call object storage; **AgentRun** calls LLM providers. 

When you conflate a provider `429` with your own validation error, retry non-idempotently, or expose raw vendor messages, you create cross-tenant leakage, duplicate charges, and cascading outages. This part gives you a repeatable way to draw a hard line between "your system failed" and "a dependency failed", and to act on that distinction safely.

## Part objectives

By the end of Part X you can:

- **Classify** third-party failures by origin (HTTP, payload, auth, quota, timeout, connectivity, degradation).
- **Translate** vendor errors to stable internal codes without creating tight coupling to vendor types.
- **Handle** network/distributed communication failures (DNS, TCP/TLS, timeouts, half-open connections, ambiguous outcomes).
- **Decide** when to retry, when to degrade, when to fail fast, and when to use replaceable adapters.
- **Contain** vendor outages so they don't become uncoordinated retries across your fleet.

## Chapter index

| Chapter | Focus | Key outcomes |
| ------- | ----- | ------------ |
| [25. Third-Party API Error Handling](./25-third-party-api-error-handling/README.md) | Upstream HTTP/payload failures, auth, rate limits, quotas, versioning, translation, adapters. | Map provider errors to internal taxonomy; design replaceable adapters; fail safely when critical deps are down. |
| [26. Network and Distributed Communication Errors](./26-network-and-distributed-communication-errors/README.md) | DNS, connection/reset, TLS/certs, connect/read/write timeouts, pools, half-open, remote termination, partitions, ambiguous outcomes. | Distinguish transport vs application failures; handle lost responses after success; reason about partitions. |

## Core principles for this part

- **Boundary discipline:** All vendor calls live behind an integration boundary. Translation happens at the boundary, not leaked into domain services.
- **Stable contracts:** Internal errors are vendor-agnostic. You can swap **Stripe** for another provider without changing domain logic.
- **Recoverability first:** Classify as retryable/non-retryable at translation time based on the *failure mode*, not the raw status code alone.
- **Ambiguity is expected:** After a write, a timeout does not guarantee success or failure — treat "lost response" as its own category.
- **Degrade intentionally:** For optional dependencies, prefer cached/fallback behavior with clear communication; for critical dependencies, fail closed with explicit errors.

## How to use this part

1. Read Chapter 25 to learn translation and adapter design.
2. Read Chapter 26 to learn transport/distributed failure semantics.
3. Use the practical examples to write a small provider adapter and a network error classifier for **Acme SaaS**/**Checkout** scenarios.
4. Apply the dos/don'ts when designing retry/fallback behavior for **WebhookIngest** and **AgentRun**.

## Related

- [Part VI — Error Boundaries and Translation](../part-06-boundaries-and-translation/README.md)
- [Part VIII — HTTP and API Error Handling](../part-08-http-and-api/README.md)
- [Part XI — Retry Logic and Resilience](../part-11-retry-and-resilience/README.md)
- [Glossary](../GLOSSARY.md)
