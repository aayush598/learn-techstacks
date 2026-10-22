# TLS, Timeouts, and Transmission

> Part X · Chapter 26 · Sections 26.4, 26.5, 26.6, 26.7, 26.8 · _Estimated reading time: 14 min_

## In one sentence

**TLS errors, connect/read/write timeouts, and transmission/reception failures** must be classified precisely because timeouts are ambiguous and TLS failures are usually not retryable without fixing configuration.

## Why this matters in production

**Checkout** calling a payment gateway may hit TLS certificate errors (misconfiguration) — retrying won't help. Connect timeout means couldn't establish TCP+TLS. Read timeout means sent request but didn't receive response in time — the operation may have succeeded on the server side. This is the core ambiguity discussed in later sections.

## Core concept

| Failure | Phase | Retryable? | Notes |
| ------- | ----- | ---------- | -----|
| **TLS handshake failure** | TLS | Usually no | Bad cert, expired, hostname mismatch, wrong TLS version. Config issue. |
| **Certificate verification error** | TLS | No | Trust issues. |
| **Connect timeout** | TCP+TLS | Often yes if idempotent | Couldn't establish connection. |
| **Write timeout** | Transmission | Sometimes | Failed to send request body completely. |
| **Read timeout** | Reception | **Ambiguous** | Request sent, no response received — may have succeeded. |
| **Request transmission failure** | Write | Depends | Connection broken while sending. |

## How it works

### TLS
- **Certificate expired/invalid** — configuration error.
- **Hostname mismatch** — SNI/cert issue.
- **Protocol/version mismatch** — TLS version/cipher issues.
- **Self-signed/untrusted** — CA trust issues.

### Timeouts
- **Connect timeout**: Time to establish TCP connection (and TLS handshake). Usually safe to retry if idempotent.
- **Request/write timeout**: Time to send the full request. If connection breaks during write, ambiguity exists.
- **Response/read timeout**: Time to receive response after request sent. **Highest ambiguity** — server may have processed request.

### Transmission/reception
- **Partial write**: Request not fully sent — server likely didn't process complete request.
- **Full write, no read**: Server may have processed; response lost.

## Worked example

```ts
function classifyTimeout(err: any, phase: "connect"|"write"|"read"): InternalNetErr {
  if (phase === "connect") {
    return { category: "connect_timeout", retryable: true, idempotentOnly: true };
  }
  if (phase === "write") {
    // Ambiguous if request partially sent
    return { category: "write_timeout", retryable: false, ambiguous: true, reason: "partial_transmission" };
  }
  if (phase === "read") {
    // Highest ambiguity
    return { category: "read_timeout", retryable: false, ambiguous: true, reason: "lost_response_after_send" };
  }
  return { category: "timeout", retryable: false };
}
```

**Key data:**
- **gRPC `DEADLINE_EXCEEDED`**: Often maps to timeout; check if deadline exceeded before/after send.
- **HTTP**: Client/read timeout vs server timeout different.

## Real-world use case

**Checkout creating payment intent:** Connect timeout → retryable with idempotency key. Read timeout after sending POST → **do not blindly retry** unless operation is idempotent AND you can safely determine outcome or use idempotency keys that make retry safe (server deduplicates). This is why idempotency is critical (Part XI).

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Retry all timeouts** | Simple | Dangerous for non-idempotent writes | Never |
| **Never retry timeouts** | Safe | Misses recoverable connect failures | Too conservative |
| **Retry by phase + idempotency** | Correct | Complex | **Recommended** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify timeouts by phase (connect/write/read) | Treat all timeouts same |
| Fail fast on TLS cert errors | Retry TLS configuration errors |
| Treat read timeout as ambiguous | Retry blindly after read timeout |
| Use idempotency keys before retrying writes | Retry non-idempotent on read timeout |

## Common mistakes

- **TLS retry loops:** Invalid cert retried forever.
- **Read timeout = failure:** Assuming request failed when it may have succeeded.
- **No phase tracking:** Can't make correct retry decisions.

## Checklist

- [ ] TLS errors classified as non-retryable (config).
- [ ] Timeouts tracked by phase.
- [ ] Read timeouts marked ambiguous.
- [ ] Retry decisions consider idempotency + phase.

## Related

- [DNS, Connection, and Termination](./01-dns-connection-and-termination.md)
- [Pools, Partitions, and Duplicate Delivery](./03-pools-partitions-and-duplicate-delivery.md)
- [TCP/TLS Failure Taxonomy](../02-deep-dive/01-tcp-tls-failure-taxonomy.md)
- [Ambiguous Remote Outcomes](../02-deep-dive/02-ambiguous-remote-outcomes.md)
- [Glossary](../../../GLOSSARY.md)
