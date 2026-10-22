# TCP/TLS Failure Taxonomy

> Part X · Chapter 26 · Sections 26.1–26.6 · _Estimated reading time: 14 min_

## In one sentence

**A precise taxonomy mapping OS-level TCP/TLS errors (errno, TLS alerts) to internal categories with retryability and phase** helps **Acme SaaS** make safe decisions without guessing.

## Why this matters in production

Operating systems expose `ECONNREFUSED`, `ECONNRESET`, `ETIMEDOUT`, `ENOTFOUND` etc. TLS libraries expose handshake/cert errors. Mapping these consistently prevents retry loops on configuration errors and unsafe retries on ambiguous transport failures.

## Core taxonomy

| Error/Signal | Layer | Phase | Category | Retryable | Notes |
| ------------ | ----- | ----- | -------- | ---------- | -----|
| `ENOTFOUND`, `EAI_NONAME` | DNS | resolve | `dns_failure` | Usually no (config) | NXDOMAIN |
| `ECONNREFUSED` | TCP | connect | `connection_refused` | Yes if transient | No listener |
| `ECONNRESET` | TCP | any after connect | `connection_reset` | Idempotent only | Peer reset |
| `ETIMEDOUT`, `ECONNTIMEOUT` | TCP | connect/read/write | `timeout` | Phase-dependent | See timeouts |
| `EHOSTUNREACH`, `ENETUNREACH` | IP | connect | `network_unreachable` | Sometimes | Routing issues |
| `ECONNABORTED` | TCP | any | `connection_aborted` | Idempotent only | App aborted |
| TLS cert expired | TLS | handshake | `tls_cert_invalid` | No | Config |
| TLS hostname mismatch | TLS | handshake | `tls_hostname_mismatch` | No | Config |
| TLS handshake failure | TLS | handshake | `tls_handshake_failed` | Usually no | Version/cipher |
| HTTP/2 GOAWAY | HTTP/2 | any | `connection_terminated` | Case-dependent | Server closing |

## How it works (mapping)
- **DNS first** — classify before TCP.
- **Phase matters** — connect vs write vs read changes ambiguity.
- **TLS before HTTP** — handshake errors take precedence.

## Worked example

```ts
function mapNetworkError(e: any): InternalNetErr {
  const code = e.code || e.errno;
  const phase = e.phase as "connect"|"write"|"read"|"handshake";
  if (phase === "handshake") {
    if (/certificate|cert/i.test(e.message)) return { cat: "tls_cert_invalid", retryable: false };
    if (/hostname|cn/i.test(e.message)) return { cat: "tls_hostname_mismatch", retryable: false };
    return { cat: "tls_handshake_failed", retryable: false };
  }
  switch (code) {
    case "ENOTFOUND": return { cat: "dns_failure", retryable: false, alert: "config" };
    case "ECONNREFUSED": return { cat: "connection_refused", retryable: true };
    case "ECONNRESET": return { cat: "connection_reset", retryable: true, idempotentOnly: true, ambiguous: phase === "read" || phase === "write" };
    case "ETIMEDOUT": return timeoutByPhase(phase);
    default: return { cat: "unknown_network", retryable: false };
  }
}
```

**Key data:**
- **gRPC codes**: `UNAVAILABLE` maps to connectivity; `DEADLINE_EXCEEDED` to timeout.
- **errno values** platform-dependent but common.

## Real-world use case

**AgentRun** calling external model API: TLS cert expiry → non-retryable, alerts ops. `ECONNRESET` during streaming (read phase) → ambiguous; only retry if request is idempotent.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Flat mapping** | Simple | Loses phase | Insufficient |
| **Phase-aware mapping** | Correct | More complex | **Recommended** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Include phase in classification | Ignore write/read distinction |
| Treat TLS handshake errors as non-retryable | Retry config errors |
| Map errno explicitly | Coarse-grain all as "network" |

## Common mistakes

- **Retrying cert errors** — never succeeds.
- **Same policy for ENOTFOUND and ECONNRESET** — different root causes.

## Checklist

- [ ] All common errno mapped.
- [ ] TLS errors separated by subtype.
- [ ] Phase recorded for timeouts/resets.
- [ ] Retryability considers idempotency for ambiguous cases.

## Related

- [Ambiguous Remote Outcomes](./02-ambiguous-remote-outcomes.md)
- [Partial Network Failures and Gateways](./03-partial-network-failures-and-gateways.md)
- [Network Error Classification Code](../03-practical-examples/01-network-error-classification-code.md)
- [Glossary](../../../GLOSSARY.md)
