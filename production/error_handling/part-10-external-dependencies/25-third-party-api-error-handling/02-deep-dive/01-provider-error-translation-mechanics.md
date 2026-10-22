# Provider Error Translation Mechanics

> Part X · Chapter 25 · Section 25.3, 25.14, 25.15 · _Estimated reading time: 16 min_

## In one sentence

**Systematic translation requires mapping tables, normalization, and cause preservation** so that provider-specific chaos becomes predictable internal errors without losing the root cause.

## Why this matters in production

A naive `if (err.type === 'card_error') throw new Error(...)` scattered everywhere is unmaintainable. For **Checkout** at scale, you need deterministic mapping: Stripe `rate_limit_error` → `UPSTREAM_RATE_LIMITED` with `retryAfterSec`, network errors → `UPSTREAM_UNAVAILABLE` with `retryable: true`. Translation must be testable, versionable, and safe.

## Core concept

Translation mechanics:
1. **Normalization** — extract common fields (`status`, `code`, `type`, `message`, `retryAfter`).
2. **Mapping tables** — `Map<ProviderKey, InternalMapping>` per vendor.
3. **Preserve cause** — chain original error (`cause`) for debugging without exposing to users.
4. **Enrich metadata** — add `vendor`, `operation`, `retryable`, `retryAfterSec`.
5. **Avoid info loss** — keep enough for support/ops, redact for clients.

## How it works

### Mapping strategy
Prefer table-driven mapping over giant if-else chains:
- **By error type** (e.g. Stripe `type`)
- **By error code** (e.g. provider-specific codes)
- **By HTTP status + payload combination**
- **Fallback** — unknown → `UPSTREAM_UNKNOWN` with `retryable: false` or `true` based on class

### Normalization
```ts
interface NormalizedUpstream {
  status?: number;
  vendorType?: string;
  vendorCode?: string;
  message?: string;
  retryAfterSec?: number;
  headers: Headers;
  rawSafe?: unknown; // redacted
}
```

### Cause preservation
```ts
class InternalErr extends Error {
  code: string;
  retryable: boolean;
  retryAfterSec?: number;
  cause?: unknown;
  constructor(code: string, opts: Partial<InternalErr> = {}) {
    super(code); // user-safe message set separately
    this.code = code;
    this.retryable = opts.retryable ?? false;
    this.retryAfterSec = opts.retryAfterSec;
    this.cause = opts.cause;
  }
}
```

## Worked example

```ts
// Table-driven Stripe mapping
const STRIPE_MAP: Record<string, InternalMapping> = {
  "card_error:card_declined": { code: AcmeErr.UPSTREAM_DECLINED, retryable: false },
  "rate_limit_error:*": { code: AcmeErr.UPSTREAM_RATE_LIMITED, retryable: true },
  "authentication_error:*": { code: AcmeErr.UPSTREAM_AUTH_INVALID, retryable: false },
  "api_connection_error:*": { code: AcmeErr.UPSTREAM_UNAVAILABLE, retryable: true },
  "api_error:*": { code: AcmeErr.UPSTREAM_UNAVAILABLE, retryable: true },
};

function mapStripeNormalized(n: NormalizedUpstream, cause: unknown): InternalErr {
  const key = `${n.vendorType}:${n.vendorCode || "*"}`;
  const m = STRIPE_MAP[key] || STRIPE_MAP[`${n.vendorType}:*`];
  if (m) {
    return new InternalErr(m.code, { retryable: m.retryable, retryAfterSec: n.retryAfterSec, cause });
  }
  // fallback by class
  if (n.status === 429) return new InternalErr(AcmeErr.UPSTREAM_RATE_LIMITED, { retryable: true, retryAfterSec: n.retryAfterSec, cause });
  if (n.status && n.status >= 500) return new InternalErr(AcmeErr.UPSTREAM_UNAVAILABLE, { retryable: true, cause });
  return new InternalErr(AcmeErr.UPSTREAM_UNKNOWN, { retryable: false, cause });
}
```

**Key data:**
- **Mapping tables versioned** with provider API version.
- **`cause` preserved** for logs/traces, never exposed to end users.
- **Wildcard mappings** reduce duplication.

## Real-world use case

**Checkout at Acme SaaS:** During a Stripe outage, all calls return `api_connection_error` or 503. Mapping normalizes them to `UPSTREAM_UNAVAILABLE` with `retryable: true` but the retry policy (circuit breaker + budget) prevents retry storms. Support sees the internal code and can act without parsing Stripe docs.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| **Scattered ifs** | Quick | Unmaintainable, inconsistent | Prototypes only |
| **Table-driven per vendor** | Testable, versionable | Initial setup | **Recommended** |
| **Codegen from provider schemas** | Auto-updates | Complex, may overfit | Large teams with many vendors |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Normalize first, then map | Map directly from raw vendor objects everywhere |
| Use tables with wildcards | Duplicate logic across call sites |
| Preserve `cause` | Lose original error stack/context |
| Redact raw payloads in user messages | Log full provider responses with PII |
| Have a safe fallback for unknown codes | Throw unclassified errors |

## Common mistakes

- **Info loss:** Converting everything to "unknown error" loses retryability.
- **Leaking cause:** Exposing `cause.message` (provider details) to API clients.
- **Unversioned tables:** Provider changes break silently.
- **Over-mapping:** Creating internal codes for every vendor code unnecessarily.

## Checklist

- [ ] Normalizer extracts status/type/code/retryAfter.
- [ ] Per-vendor mapping table exists and is tested.
- [ ] Fallback rules defined for unknown codes.
- [ ] `cause` chained; redaction applied.
- [ ] Mapping is versioned with provider API version.

## Related

- [Misleading Status Codes and 200 Errors](./02-misleading-status-codes-and-200-errors.md)
- [Adapters, Vendor Outages, and Replaceability](./03-adapters-vendor-outages-and-replaceability.md)
- [Stripe Error Mapping Adapter](../03-practical-examples/01-stripe-error-mapping-adapter.md)
- [Glossary](../../../GLOSSARY.md)
