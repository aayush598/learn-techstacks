# Network Error Classification Code

> Part X · Chapter 26 · Sections 26.1–26.11, 26.18 · _Estimated reading time: 18 min_

## In one sentence

**A runnable-ish classifier mapping errno/OS errors, TLS failures, and gateway codes to internal network error categories with phase and retryability hints** for use in HTTP clients.

## Why this matters in production

For **Acme SaaS**, centralizing network error classification ensures consistent behavior across all external calls. The classifier captures phase (connect/write/read/handshake), marks ambiguity, and provides hints for retry logic.

## Worked example

### Types
```ts
export type NetPhase = "dns" | "handshake" | "connect" | "write" | "read" | "unknown";
export interface InternalNetErr extends Error {
  category: string;
  phase: NetPhase;
  retryable: boolean;
  ambiguous: boolean;
  idempotentOnly: boolean;
  alert?: string;
  cause?: unknown;
}

export function isNetworkErr(e: unknown): e is InternalNetErr {
  return typeof e === "object" && e !== null && "category" in e && "phase" in e;
}
```

### Classifier
```ts
export function classifyNetworkError(e: any): InternalNetErr {
  const code = e?.code || e?.errno;
  const msg = (e?.message || "").toLowerCase();
  const phase = (e?.phase as NetPhase) || inferPhase(e);

  // TLS/handshake
  if (phase === "handshake" || /tls|ssl|certificate|handshake/.test(msg)) {
    if (/certificate.*(expired|invalid)|cert.*fail/.test(msg)) {
      return netErr("tls_cert_invalid", phase, false, false, false, "config", e);
    }
    if (/hostname|cn.*mismatch|subject alternative/.test(msg)) {
      return netErr("tls_hostname_mismatch", phase, false, false, false, "config", e);
    }
    return netErr("tls_handshake_failed", phase, false, false, false, "config", e);
  }

  // DNS
  if (code === "ENOTFOUND" || code === "EAI_NONAME" || code === "EAI_NODATA") {
    return netErr("dns_failure", "dns", false, false, false, "config", e);
  }
  if (code === "EAI_AGAIN") {
    return netErr("dns_timeout", "dns", true, false, true, undefined, e);
  }

  // TCP
  if (code === "ECONNREFUSED") {
    return netErr("connection_refused", "connect", true, false, true, undefined, e);
  }
  if (code === "ECONNRESET") {
    const ambiguous = phase === "read" || phase === "write";
    return netErr("connection_reset", phase, true, ambiguous, true, undefined, e);
  }
  if (code === "ECONNABORTED") {
    return netErr("connection_aborted", phase, true, phase !== "connect", true, undefined, e);
  }
  if (code === "ETIMEDOUT" || code === "ECONNTIMEOUT") {
    return classifyTimeout(phase, e);
  }
  if (code === "EHOSTUNREACH" || code === "ENETUNREACH") {
    return netErr("network_unreachable", "connect", true, false, true, undefined, e);
  }

  // HTTP/2
  if (/goaway/.test(msg)) {
    return netErr("connection_terminated", phase, true, phase === "read", true, undefined, e);
  }

  return netErr("unknown_network", phase, false, false, false, undefined, e);
}

function classifyTimeout(phase: NetPhase, e: any): InternalNetErr {
  if (phase === "connect") {
    return netErr("connect_timeout", phase, true, false, true, undefined, e);
  }
  if (phase === "write") {
    // Ambiguous if full request sent
    return netErr("write_timeout", phase, false, true, true, undefined, e);
  }
  if (phase === "read") {
    return netErr("read_timeout", phase, false, true, true, undefined, e);
  }
  return netErr("timeout", phase, false, true, true, undefined, e);
}

function netErr(cat: string, phase: NetPhase, retryable: boolean, ambiguous: boolean, idempotentOnly: boolean, alert?: string, cause?: unknown): InternalNetErr {
  const err = new Error(cat) as InternalNetErr;
  err.category = cat;
  err.phase = phase;
  err.retryable = retryable;
  err.ambiguous = ambiguous;
  err.idempotentOnly = idempotentOnly;
  err.alert = alert;
  err.cause = cause;
  return err;
}

function inferPhase(e: any): NetPhase {
  if (e?.phase) return e.phase;
  const msg = (e?.message || "").toLowerCase();
  if (/connect/.test(msg)) return "connect";
  if (/write|send/.test(msg)) return "write";
  if (/read|response/.test(msg)) return "read";
  if (/handshake|tls/.test(msg)) return "handshake";
  if (/dns|lookup/.test(msg)) return "dns";
  return "unknown";
}
```

### Gateway mapping
```ts
export function classifyGatewayError(status: number, headers: Headers): InternalNetErr {
  if (status === 503) {
    const ra = parseRetryAfter(headers.get("retry-after"));
    const err = netErr("gateway_unavailable", "read", true, false, true, undefined, undefined);
    (err as any).retryAfterSec = ra;
    return err;
  }
  if (status === 504) {
    return netErr("gateway_timeout", "read", false, true, true, undefined, undefined);
  }
  if (status === 502) {
    return netErr("bad_gateway", "read", true, false, true, undefined, undefined);
  }
  return netErr("gateway_error", "read", status >= 500, false, true, undefined, undefined);
}
```

**Key data:**
- `ECONNREFUSED`, `ECONNRESET`, `ETIMEDOUT`, `ENOTFOUND`, TLS errors, `GOAWAY`, `502/503/504`.

## Real-world use case

**Acme SaaS HTTP client:** All external calls pass through a client that catches errors, calls `classifyNetworkError`, and makes retry decisions based on `phase`, `retryable`, `ambiguous`, `idempotentOnly`. This ensures **Checkout** never blindly retries on read timeouts.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Ad-hoc classification** | Quick | Inconsistent | Never |
| **Central classifier** | Consistent, testable | Needs maintenance | **Recommended** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Track phase explicitly | Guess phase |
| Mark ambiguity | Assume safe to retry |
| Handle TLS separately | Mix with TCP |
| Map gateways separately | Treat as origin errors blindly |

## Common mistakes

- **Missing phase** — can't determine ambiguity.
- **Retrying TLS errors** — wasteful.
- **Treating 504 same as 503** — 504 is ambiguous.

## Checklist

- [ ] Classifier covers errno, TLS, GOAWAY, gateways.
- [ ] Phase inferred or passed.
- [ ] Ambiguity flags set correctly.
- [ ] Used by all HTTP clients.

## Related

- [TCP/TLS Failure Taxonomy](../02-deep-dive/01-tcp-tls-failure-taxonomy.md)
- [Handling Lost Responses Safely](./02-handling-lost-responses-and-retries-safely.md)
- [Chapter 25 — Stripe Error Mapping](../../25-third-party-api-error-handling/03-practical-examples/01-stripe-error-mapping-adapter.md)
- [Glossary](../../../GLOSSARY.md)
