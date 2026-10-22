# Chapter 26 — Network and Distributed Communication Errors

> Part X · _Estimated reading time: 50–60 min_  
> **Prerequisite:** [Chapter 25 — Third-Party API Error Handling](../25-third-party-api-error-handling/README.md), [Part IV — Error-Handling Architecture and System Boundaries](../../part-04-architecture/README.md)

## One-sentence summary

**Treat transport failures and distributed ambiguity as first-class errors**: distinguish DNS/TCP/TLS/timeouts from application errors, recognize half-open connections, and safely handle the case where a request may have succeeded on the remote even if you never received a response.

## Why this chapter matters

For **Acme SaaS**, **Checkout**'s call to a payment gateway can time out after writing to a remote system. **WebhookIngest** may see network resets mid-ack. **ExportJob** workers hitting object storage see `ECONNRESET` and `ETIMEDOUT`. Without a disciplined taxonomy, teams retry non-idempotent writes and create duplicates, or they never retry when it's safe. In distributed systems, **ambiguity** is often the hardest part.

## Learning objectives

By the end of this chapter you can:

- **Classify** network failures: DNS, `ECONNREFUSED`, `ECONNRESET`, TLS/cert errors, connect/read/write timeouts.
- **Reason** about connection pools, half-open connections, and remote termination.
- **Handle** partitions, duplicate delivery, out-of-order messages, and lost responses after success.
- **Treat** ambiguous outcomes correctly with idempotency and uncertainty-aware logic.
- **Map** LB/gateway errors and service discovery failures to internal categories.

## Chapter map (files and coverage)

| File | Subsections (from TOC) | What you learn |
| ---- | ----------------------- | -------------- |
| [`01-concepts/01-dns-connection-and-termination.md`](./01-concepts/01-dns-connection-and-termination.md) | 26.1, 26.2, 26.3, 26.11 | DNS resolution, connection refused/reset, remote termination semantics. |
| [`01-concepts/02-tls-timeouts-and-transmission.md`](./01-concepts/02-tls-timeouts-and-transmission.md) | 26.4, 26.5, 26.6, 26.7, 26.8 | TLS/cert errors, connect/read/write timeouts, request transmission/response reception. |
| [`01-concepts/03-pools-partitions-and-duplicate-delivery.md`](./01-concepts/03-pools-partitions-and-duplicate-delivery.md) | 26.9, 26.10, 26.12, 26.13, 26.14 | Pool exhaustion, half-open connections, network partitions, duplicates, out-of-order. |
| [`01-concepts/04-ambiguous-outcomes-and-service-boundaries.md`](./01-concepts/04-ambiguous-outcomes-and-service-boundaries.md) | 26.15, 26.16, 26.17, 26.18, 26.19, 26.20 | Lost responses after success, ambiguous outcomes, service discovery, LB/gateway errors, partial failures, cross-service boundaries. |
| [`02-deep-dive/01-tcp-tls-failure-taxonomy.md`](./02-deep-dive/01-tcp-tls-failure-taxonomy.md) | 26.1–26.6 | Concrete errno/OS errors, TLS failure modes, mapping to retry classes. |
| [`02-deep-dive/02-ambiguous-remote-outcomes.md`](./02-deep-dive/02-ambiguous-remote-outcomes.md) | 26.13–26.16 | The "timeout after write" problem, idempotency keys, uncertainty, and safe patterns. |
| [`02-deep-dive/03-partial-network-failures-and-gateways.md`](./02-deep-dive/03-partial-network-failures-and-gateways.md) | 26.12, 26.17, 26.18, 26.19, 26.20 | Partitions, LB/gateway errors (502/503/504), service discovery, partial failures. |
| [`03-practical-examples/01-network-error-classification-code.md`](./03-practical-examples/01-network-error-classification-code.md) | 26.1–26.11, 26.18 | Runnable-ish classifier mapping `errno`/errors to internal categories with retry hints. |
| [`03-practical-examples/02-handling-lost-responses-and-retries-safely.md`](./03-practical-examples/02-handling-lost-responses-and-retries-safely.md) | 26.13–26.16 | **Checkout** example with idempotency, uncertainty, and avoiding duplicate charges. |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all 26.1–26.20 | Rules and anti-patterns. |
| [`05-reference/README.md`](./05-reference/README.md) | all 26.1–26.20 | Network error cheat sheet (errno, TLS, gRPC, HTTP gateway codes), decision table. |

## Key takeaways

1. **Transport ≠ application.** Map `ECONNREFUSED` differently from HTTP `400`; don't conflate them.
2. **Timeouts are ambiguous.** A connect timeout is usually safe to retry; a read timeout after sending a non-idempotent body may mean the operation already happened.
3. **Half-open is real.** Connection pools must validate/recreate dead connections; don't blindly reuse.
4. **Plan for loss.** Use idempotency keys, client-generated request IDs, and "get-or-create" patterns when outcome is uncertain.
5. **Gateways lie in effect.** `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout` often reflect upstream/network issues — translate carefully.

## Exercises

1. **Classify:** Given errors `{code:'ECONNRESET'}`, `{code:'ETIMEDOUT', phase:'read'}`, TLS cert expiry, map to internal category and retryability.
2. **Ambiguity:** Design logic for **Checkout** charge where `POST /charges` times out at read — when is retry safe?
3. **Pool:** Explain half-open connections and how to avoid retry storms.
4. **Partition:** Describe behavior when **WebhookIngest** can't reach its DB due to network partition.

## Related

- [Chapter 25 — Third-Party API Error Handling](../25-third-party-api-error-handling/README.md)
- [Part XI — Retry Logic and Resilience](../../part-11-retry-and-resilience/README.md)
- [Part XV — Advanced Distributed-System Failure Handling](../../part-15-distributed-failures/README.md)
- [Glossary](../../../GLOSSARY.md)
