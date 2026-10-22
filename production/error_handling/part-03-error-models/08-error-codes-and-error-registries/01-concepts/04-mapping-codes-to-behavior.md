# Mapping Codes to Behavior

> Part III · Chapter 8 · Sections 8.10–8.14 · _Estimated reading time: 18 min_
> **Prerequisite:** [Uniqueness and Registry Structure](./03-uniqueness-and-registry-structure.md)

## In one sentence

The registry's real power is that each code **derives every downstream behavior** — documentation,
HTTP status, client action, retry policy, and user message — so those decisions are made once, in
one place, instead of re-derived at each call site.

## Why this matters in production

When mappings live beside the code that throws, the same condition gets a different status in two
endpoints, retries in one path but not another, and shows the wrong message in the UI. Centralizing
the mappings in the registry makes behavior **consistent by construction** and reviewable in one
diff. It also means a new code cannot ship without a status, a retry rule, and a message — the build
simply will not pass.

## Documentation requirements (8.10)

Every registry entry documents, at minimum:

| Field | Purpose |
| ----- | ------- |
| `code` | The stable identifier |
| `domain` | Owning prefix/team |
| `category` | Routing bucket (maps to policy) |
| `http` | Status when exposed over HTTP |
| `retryable` | Retry eligibility |
| `visibility` | public / internal |
| `message` | Default user-facing text (localizable key) |
| `description` | Engineer-facing "when this happens" |
| `owner` | Team responsible |
| `since` | Version/date introduced |
| `deprecated?` | Deprecation marker |

Docs can be **generated** from the registry so the human-readable catalog never drifts from the
source. The `description` is for engineers; `message` is for users; they are different fields.

## Mapping to HTTP (8.11)

Mappings are **category-based with per-code overrides** (Chapter 19 details statuses).

| Category | Default HTTP | Common overrides |
| -------- | ------------ | ---------------- |
| validation | 422 | 400 (malformed), 413 (too large) |
| auth | 401 / 403 | 402 (payment required for entitlement) |
| business | 409 | 404 (not found), 402 |
| payment | 402 | 429 (provider rate limit) |
| database | 503 | 409 (unique violation) |
| external | 502 | 504 (upstream timeout) |
| resource | 429 | 503 |
| unexpected | 500 | — |

```ts
const HTTP: Record<ErrorCode, number> = {
  VALIDATION_REQUIRED_FIELD: 422,
  PAYMENT_CARD_DECLINED: 402,
  PAYMENT_PROVIDER_TIMEOUT: 503,
  DB_UNIQUE_VIOLATION: 409,
  RATE_LIMIT_EXCEEDED: 429,
  INTERNAL_UNEXPECTED: 500,
};
```

> ⚠️ **Hazard.** Never let an internal code's HTTP status hint at infrastructure. `DB_DEADLOCK`
> should surface as `503` (or a generic `500`), never as a bespoke status that leaks the cause.

## Mapping to client actions (8.12)

A code tells a client **what it can do**. The registry declares the action so clients stay simple.

| Action | Meaning | Example codes |
| ------ | ------- | ------------- |
| `retry` | Safe to retry (respect backoff) | `PAYMENT_PROVIDER_TIMEOUT`, `RATE_LIMIT_EXCEEDED` |
| `reauthenticate` | Re-login / refresh token | `AUTH_SESSION_EXPIRED` |
| `fix_input` | Show field errors | `VALIDATION_*` |
| `choose_alternative` | User must change choice | `PAYMENT_CARD_DECLINED`, `USER_EMAIL_TAKEN` |
| `contact_support` | Not self-service | `SYSTEM_INVARIANT_VIOLATION` |
| `none` | Informational | `EXPORT_EMPTY` |

```ts
const CLIENT_ACTION: Record<ErrorCode, ClientAction> = {
  VALIDATION_REQUIRED_FIELD: "fix_input",
  PAYMENT_CARD_DECLINED: "choose_alternative",
  PAYMENT_PROVIDER_TIMEOUT: "retry",
  AUTH_SESSION_EXPIRED: "reauthenticate",
  INTERNAL_UNEXPECTED: "contact_support",
  // ...
};
```

The client switches on the code, reads the action, and renders accordingly — no per-code hardcoding.

## Mapping to retry policies (8.13)

Retry policy is a function of context (attempt, deadline) **and** the code's classification.

```ts
type RetryPolicy = { retryable: boolean; baseMs: number; maxAttempts: number };

const RETRY: Record<ErrorCode, RetryPolicy> = {
  PAYMENT_PROVIDER_TIMEOUT: { retryable: true,  baseMs: 250, maxAttempts: 5 },
  DB_DEADLOCK:              { retryable: true,  baseMs: 50,  maxAttempts: 5 },
  DB_SERIALIZATION_FAILURE: { retryable: true,  baseMs: 100, maxAttempts: 5 },
  RATE_LIMIT_EXCEEDED:      { retryable: true,  baseMs: 1000, maxAttempts: 8 }, // honor Retry-After
  PAYMENT_CARD_DECLINED:    { retryable: false, baseMs: 0,   maxAttempts: 1 },
  VALIDATION_REQUIRED_FIELD:{ retryable: false, baseMs: 0,   maxAttempts: 1 },
};

function shouldRetry(code: ErrorCode, attempt: number, deadlineExceeded: boolean): boolean {
  const p = RETRY[code];
  return p.retryable && attempt < p.maxAttempts && !deadlineExceeded;
}
```

Rules:

- **Only transient codes retry.** Business/validation/permanent codes never.
- **Bound by attempts and deadline.** Context still matters (Chapter 27).
- **Honor server instructions** (`Retry-After`) — encode that in the policy, not the code.
- **Idempotency is independent.** Retrying a non-idempotent operation is unsafe regardless of code
  (Chapter 28).

## Mapping to user messages (8.14)

Users get a **safe, localized, actionable** message keyed by code — never the internal message.

```ts
// i18n keys, not raw strings, so localization is possible.
const MESSAGE_KEY: Record<ErrorCode, string> = {
  VALIDATION_REQUIRED_FIELD: "errors.validation.required",
  PAYMENT_CARD_DECLINED:     "errors.payment.cardDeclined",
  PAYMENT_PROVIDER_TIMEOUT:  "errors.payment.providerTimeout",
  RATE_LIMIT_EXCEEDED:       "errors.rateLimit.exceeded",
  INTERNAL_UNEXPECTED:       "errors.internal.unexpected",
};
```

Rules:

- **Map code → i18n key → localized text.** Never map code → English string inline.
- **Internal codes never get a specific user message**; they map to a generic key.
- **Messages are safe and non-disclosing** (no stack traces, SQL, hostnames — Chapter 34).
- **Validation codes carry `details`** so the UI can attach messages per field.
- **Wording may change freely**; only the code is a contract.

```ts
function userMessage(err: AppError, t: Translator): string {
  const key = MESSAGE_KEY[err.code] ?? "errors.internal.unexpected";
  return t(key); // t() handles localization + fallback
}
```

## Worked example — one code, five mappings

```ts
const REGISTRY = {
  PAYMENT_PROVIDER_TIMEOUT: {
    domain: "PAYMENT", category: "payment", http: 503,
    retryable: true, visibility: "internal", publicAlias: "SERVICE_UNAVAILABLE",
    clientAction: "retry", messageKey: "errors.payment.providerTimeout",
    description: "PSP did not respond before the deadline.",
    owner: "payments", since: "2026.03",
  },
} as const;
```

A single registry row yields: `503`, retry with backoff, a `retry` client action, a safe localized
message, and a documented description — all consistent everywhere the code appears.

## Key data / numbers

- **HTTP defaults:** 422 validation, 401/403 auth, 409 business conflict, 402 payment, 429 rate
  limit, 502/503/504 external, 500 unexpected. `Retry-After` accompanies 429/503.
- **gRPC mapping:** `UNAVAILABLE` ↔ 503, `DEADLINE_EXCEEDED` ↔ 504, `NOT_FOUND` ↔ 404,
  `INVALID_ARGUMENT` ↔ 400, `RESOURCE_EXHAUSTED` ↔ 429.
- **Retry backoff:** exponential base with jitter; base 50–1000 ms; max attempts typically 5–8.
- **Client actions:** keep the set small (`retry`, `reauthenticate`, `fix_input`,
  `choose_alternative`, `contact_support`, `none`).

## Real-world use case — Checkout

Acme's checkout had `PAYMENT_PROVIDER_TIMEOUT` mapped to `500` in one endpoint and `503` in
another, retried in the API layer but not in the job worker, and shown to users as the raw English
string. Consolidating the mappings into the registry made the status, retry policy, client action,
and localized message **derive from one row**. The two endpoints now behave identically, the worker
retries correctly, and the UI renders "Payment provider is temporarily unavailable — retrying"
without any per-code logic.

## Trade-offs

| Where mappings live | Consistency | Coupling | Notes |
| ------------------- | ----------- | -------- | ----- |
| Registry (central) | High | One shared module | Recommended |
| Per-handler | Low | None | Drifts |
| Per-domain slice | Medium-high | Domain-local | Works with central merge |
| Generated from annotations | High | Tooling | Only with strong tooling |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Derive HTTP/retry/action/message from the registry | Hardcode mappings per handler |
| Map code → i18n key | Map code → English string |
| Give internal codes generic user messages | Expose internal meaning to users |
| Retry only transient codes | Retry every failure |
| Keep client actions a small closed set | Invent an action per code |

## Common mistakes

- **Duplicate mapping tables** that disagree.
- **Internal detail in a user message** (hostnames, SQL).
- **Retry on permanent codes** causing loops.
- **Localized text hardcoded** so i18n cannot change it.
- **Status inconsistency** across endpoints for the same code.

## Checklist

- [ ] Does every code have HTTP, retry, action, and message entries?
- [ ] Are mappings derived from the registry, not per-handler?
- [ ] Are user messages keyed by i18n key and safe?
- [ ] Do internal codes map to generic public messages/aliases?
- [ ] Is retry restricted to transient codes?

## Related

- [Uniqueness and Registry Structure](./03-uniqueness-and-registry-structure.md)
- [Deprecating Codes, Compatibility, and Detection](./05-deprecation-compatibility-and-detection.md)
- [Chapter 19 — HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)
