# DNS, Connection, and Termination

> Part X · Chapter 26 · Sections 26.1, 26.2, 26.3, 26.11 · _Estimated reading time: 14 min_

## In one sentence

**Network failures start at DNS and TCP**: distinguish resolution failures, `ECONNREFUSED`, `ECONNRESET`, and remote termination — each has different implications for retryability.

## Why this matters in production

**Acme SaaS ExportJob** hitting object storage can see DNS failures due to misconfiguration, or `ECONNREFUSED` if a service is down. **Checkout** may get `ECONNRESET` mid-connection. These are transport failures, not HTTP application errors — they need separate classification and careful retry logic.

## Core concept

| Failure | Layer | Typical cause | Retryable? |
| ------- | ----- | ------------- | ---------- |
| **DNS resolution failure** | DNS | Bad hostname, DNS outage | Sometimes — if transient DNS issue; often config error. |
| **Connection refused (`ECONNREFUSED`)** | TCP | No listener, port closed | Usually retryable if service restarting, but check. |
| **Connection reset (`ECONNRESET`)** | TCP | Peer closed abruptly, LB timeout, firewall | Often retryable *if idempotent*; can happen mid-request. |
| **Remote termination** | TCP/HTTP | Server closes connection, `GOAWAY` (HTTP/2) | Depends — may mean server shutting down or overloaded. |

## How it works

### DNS
- **NXDOMAIN** / resolution failure — often configuration issue.
- **Timeout** — transient DNS latency/outage.
- **Caching** — stale DNS can cause issues during failover.

### TCP
- **SYN sent, no response** → connect timeout (see next section).
- **SYN accepted, connection established, then RST** → `ECONNRESET`.
- **Connect refused** → immediate RST.

### Termination
- **Graceful close** vs **abrupt reset**.
- **HTTP/2 `GOAWAY`** signals server wants to stop accepting new streams.
- **Idle connection closed by server/LB**.

## Worked example

```ts
function classifyTcp(err: any): InternalNetErr {
  const code = err.code || err.errno;
  if (code === "ENOTFOUND" || code === "EAI_NODATA") {
    return { category: "dns_failure", retryable: false, alert: "config" };
  }
  if (code === "ECONNREFUSED") {
    return { category: "connection_refused", retryable: true, backoff: "exponential" };
  }
  if (code === "ECONNRESET") {
    return { category: "connection_reset", retryable: true, idempotentOnly: true };
  }
  if (code === "EHOSTUNREACH" || code === "ENETUNREACH") {
    return { category: "network_unreachable", retryable: true };
  }
  return { category: "unknown_network", retryable: false };
}
```

**Key data:**
- **`ECONNREFUSED`**: No process listening.
- **`ECONNRESET`**: Connection reset by peer.
- **HTTP/2 `GOAWAY`**: Maps to connection termination.

## Real-world use case

**ExportJob uploading to S3-compatible storage:** DNS resolution fails due to misconfigured endpoint → classified as config error, fails fast with alert. If connection is refused during restart, it's retryable with backoff. If reset mid-upload of a resumable upload, retrying depends on whether upload is resumable and idempotent.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Retry DNS failures** | Can help with transient DNS | Often config issue | Only if DNS is known to be flaky; usually fail fast |
| **Retry ECONNREFUSED** | Helps during rolling restarts | Can hammer restarting service | With backoff and circuit breaker |
| **Retry ECONNRESET** | Helps with LB timeouts | Ambiguous mid-request | Only if operation is idempotent |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify DNS separately from TCP | Treat DNS as generic "network error" |
| Distinguish refused vs reset | Same retry policy for all |
| Consider idempotency for resets | Retry non-idempotent on reset blindly |
| Alert on persistent DNS failures | Retry DNS config errors forever |

## Common mistakes

- **Retrying bad hostnames:** Wastes time and logs.
- **Ignoring GOAWAY:** Not handling HTTP/2 connection closure.
- **Blind retry on reset:** Mid-write reset can mean data written.

## Checklist

- [ ] DNS failures classified and alert on config issues.
- [ ] `ECONNREFUSED` handled with backoff.
- [ ] `ECONNRESET` only retried if idempotent.
- [ ] Connection termination (GOAWAY) handled.

## Related

- [TLS, Timeouts, and Transmission](./02-tls-timeouts-and-transmission.md)
- [TCP/TLS Failure Taxonomy](../02-deep-dive/01-tcp-tls-failure-taxonomy.md)
- [Chapter 25 — Classifying Upstream Failures](../../25-third-party-api-error-handling/01-concepts/01-classifying-upstream-failures.md)
- [Glossary](../../../GLOSSARY.md)
