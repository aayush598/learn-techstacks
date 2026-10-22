# Code Naming and Scoping

> Part III · Chapter 8 · Sections 8.3–8.5 · _Estimated reading time: 15 min_
> **Prerequisite:** [Why Codes, and What Makes Them Stable](./01-why-codes-and-stable-identifiers.md)

## In one sentence

Adopt **one naming convention** (`DOMAIN_REASON`, uppercase snake case), decide whether codes are
**domain-prefixed or globally unique**, and draw a clear line between **internal and public** codes
— then apply the decision everywhere.

## Why this matters in production

Inconsistent naming is how collisions happen. If one team writes `cardDeclined`, another
`PAYMENT_CARD_DECLINED`, and a third `payment.card.declined`, no registry can deduplicate them,
no dashboard can group them, and every consumer needs per-code special cases. Naming and scoping
are cheap decisions that prevent expensive drift.

## Naming conventions (8.3)

The recommended default:

```text
<DOMAIN>_<OBJECT>_<REASON>
SCREAMING_SNAKE_CASE
Uppercase A–Z, digits, underscore only
2–5 segments, ≤ 64 chars
```

Examples:

```text
PAYMENT_CARD_DECLINED
PAYMENT_PROVIDER_TIMEOUT
DB_UNIQUE_VIOLATION
USER_EMAIL_TAKEN
EXPORT_STORAGE_UNAVAILABLE
WEBHOOK_SIGNATURE_INVALID
AGENT_TOKEN_LIMIT_EXCEEDED
RATE_LIMIT_EXCEEDED
VALIDATION_REQUIRED_FIELD
```

Rules:

- **`DOMAIN_REASON` minimum.** Domain groups codes for filtering (see registry).
- **Add `OBJECT` when it disambiguates** within a domain (`EXPORT_STORAGE_UNAVAILABLE`).
- **Verb/state in the reason**, not a sentence: `_DECLINED`, `_TIMEOUT`, `_TAKEN`, `_EXCEEDED`,
  `_INVALID`, `_NOT_FOUND`, `_CONFLICT`.
- **No punctuation** (dots, colons, slashes) — they break in some logs, metrics, and headers.
- **No spaces, no camelCase, no lowercase.** Case-insensitivity causes collisions (`_id` vs `_ID`).

| Convention | Example | Verdict |
| ---------- | ------- | ------- |
| SCREAMING_SNAKE | `PAYMENT_CARD_DECLINED` | ✅ Default |
| Dot-namespaced | `payment.card.declined` | ⚠️ Fine internally; awkward in headers/metrics |
| camelCase | `paymentCardDeclined` | ❌ Case collisions |
| Sentence | `"Card declined"` | ❌ It is a message |
| Numeric | `E42` | ❌ Opaque, no grouping |

## Domain-prefixed vs globally unique (8.4)

Two viable schemes; pick one and enforce it.

| Scheme | Example | Pros | Cons |
| ------ | ------- | ---- | ---- |
| **Domain-prefixed** | `PAYMENT_*`, `DB_*`, `EXPORT_*` | Codes group by domain; ownership clear; easy filtering | Prefixes can collide if two teams pick the same domain name |
| **Globally unique** | `ACME_PAYMENT_CARD_DECLINED` | No collisions ever | Verbose; discourages reuse |

**Recommendation for most SaaS:** domain-prefixed, with a **reserved domain list** owned by the
registry (so two teams cannot both claim `PAYMENT`). Add a product/org prefix only when codes are
**public** and shared across products.

```text
RESERVED DOMAINS (registry-owned):
VALIDATION · AUTH · USER · BILLING · PAYMENT · DB · EXPORT · WEBHOOK · AGENT · RATE · SYSTEM · INTERNAL
```

Rule: **a code's prefix must be in the reserved list**; adding a domain is a governance event
(Chapter 8, §8.8), not a per-feature choice.

## Internal vs public codes (8.5)

Not every code should be visible to clients.

| Class | Audience | Example | Exposed in API? |
| ----- | -------- | ------- | --------------- |
| **Public** | Clients, third parties | `PAYMENT_CARD_DECLINED` | ✅ Yes |
| **Internal** | Ops, engineers, internal services | `DB_DEADLOCK`, `INTERNAL_INVARIANT` | ❌ Map to a generic public code |
| **Sensitive** | Restricted | `AUTH_TENANT_MISMATCH` details | ❌ Never; map + redact |

Rules:

- **Public codes are a contract.** Stable, documented, versioned (Chapter 8, §8.10).
- **Internal codes never cross the trust boundary.** Map them to a public code at the API edge
  (e.g. `DB_DEADLOCK` → `SERVICE_UNAVAILABLE`), preserving the internal one in logs only.
- **Mark each code's visibility in the registry** so the boundary mapper knows whether to pass it
  through or substitute.
- **Do not leak existence.** An `AUTH_INVALID_USER` vs `AUTH_WRONG_PASSWORD` split enables user
  enumeration; expose one public code (Chapter 35).

```ts
// Boundary mapping: internal → public.
function toPublicCode(code: ErrorCode): PublicErrorCode {
  const entry = REGISTRY[code];
  if (entry.visibility === "public") return code as PublicErrorCode;
  return entry.publicAlias ?? "SERVICE_UNAVAILABLE"; // safe default
}
```

## Worked example

```ts
// A small slice of the registry declaring prefix, visibility, and alias.
export const REGISTRY = {
  PAYMENT_CARD_DECLINED:    { domain: "PAYMENT", visibility: "public"   },
  PAYMENT_PROVIDER_TIMEOUT: { domain: "PAYMENT", visibility: "internal",
                              publicAlias: "SERVICE_UNAVAILABLE" },
  DB_UNIQUE_VIOLATION:      { domain: "DB",      visibility: "internal",
                              publicAlias: "CONFLICT" },
  AUTH_INVALID_CREDENTIALS: { domain: "AUTH",    visibility: "public"   },
} as const;
```

The prefix comes from the reserved domain list; the visibility drives the boundary; the alias
protects internals.

## Key data / numbers

- **Reserved domain list:** typically 10–20 prefixes; each new one is a governance decision.
- **HTTP header safety:** codes travel in `type` URIs or JSON fields; avoid characters outside
  `A–Z0–9_` to stay safe in headers, metric names, and URLs.
- **gRPC** uses a fixed enum (`UNAVAILABLE`, `DEADLINE_EXCEEDED`) — a model for behavior-derived,
  transport-stable names.
- **Postel's robustness principle** applies: producers send stable codes; consumers ignore unknown
  codes with a safe fallback.

## Real-world use case — Acme SaaS

Three Acme teams independently shipped `RATE_LIMITED`, `RATE_LIMIT_EXCEEDED`, and
`rate_limit_hit`. Dashboards under-counted rate limits, and the frontend only handled one spelling.
The registry team fixed it by reserving `RATE` as a domain, standardizing on
`RATE_LIMIT_EXCEEDED`, marking it public, and adding a CI check that rejects codes outside reserved
domains or outside SCREAMING_SNAKE_CASE. Dashboards and clients stopped needing per-spelling
special cases, and new teams no longer invented overlapping codes.

## Trade-offs

| Decision | Option A | Option B | Recommendation |
| -------- | -------- | -------- | -------------- |
| Separator | `_` | `.` | `_` (header/metric-safe) |
| Scope | Domain-prefixed | Globally unique | Domain-prefixed with reserved list |
| Visibility | Public by default | Internal by default | Internal by default; publish deliberately |
| Granularity | Coarse (`PAYMENT_FAILED`) | Fine (`PAYMENT_CARD_DECLINED_DO_NOT_HONOR`) | Fine enough to route, not per decline code |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use one SCREAMING_SNAKE convention | Mix camel/dot/sentence styles |
| Reserve domains centrally | Let teams invent prefixes ad hoc |
| Default codes to internal | Expose every code to clients |
| Map internal codes to public aliases | Leak SQLSTATE/deadlock codes |
| Keep codes header/metric-safe | Use `.`/`:`/spaces |

## Common mistakes

- **Style drift** across teams → collisions.
- **Unreserved domains** → two teams claim `PAYMENT`.
- **Internal codes exposed** → leak implementation and attack surface.
- **Over-fine granularity** → hundreds of near-duplicate codes.
- **Enumeration via code split** → distinct auth codes reveal existence.

## Checklist

- [ ] Is every code SCREAMING_SNAKE and header-safe?
- [ ] Is the domain prefix from a reserved, registry-owned list?
- [ ] Is each code marked public or internal?
- [ ] Do internal codes map to a public alias at the boundary?
- [ ] Are auth/security codes free of enumeration leaks?

## Related

- [Why Codes, and What Makes Them Stable](./01-why-codes-and-stable-identifiers.md)
- [Uniqueness and Registry Structure](./03-uniqueness-and-registry-structure.md)
- [The Sample Error Registry](../03-practical-examples/01-sample-error-registry.md)
