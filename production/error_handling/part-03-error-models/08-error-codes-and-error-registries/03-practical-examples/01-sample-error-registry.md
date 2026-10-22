# Practical: A Sample Error Registry

> Part III · Chapter 8 · Sections 8.1–8.18 · _Estimated reading time: 24 min_
> **Prerequisite:** [Registry-as-Code and Collision Testing](../02-deep-dive/01-registry-as-code-and-collision-testing.md)

## In one sentence

This file is a **complete sample registry** — a data table of real codes for the recurring cast,
plus the TypeScript that derives HTTP status, retry policy, client action, and user message from it,
so you can copy the pattern end to end.

## Why this matters in production

A registry is only real when it is populated and used. This sample shows the exact columns, the
ownership, the visibility, and the mappings for `Acme SaaS` across its domains. Adopt the table
shape, replace the rows with your codes, and every consumer derives its behavior from one place.

## The registry table

| Code | Domain | Category | HTTP | Retry | Visibility | Public alias | Client action | Message key | Owner |
| ---- | ------ | -------- | ---- | ----- | ---------- | ------------ | ------------- | ----------- | ----- |
| `VALIDATION_REQUIRED_FIELD` | VALIDATION | validation | 422 | no | public | — | fix_input | `errors.validation.required` | platform |
| `VALIDATION_INVALID_FORMAT` | VALIDATION | validation | 422 | no | public | — | fix_input | `errors.validation.format` | platform |
| `VALIDATION_OUT_OF_RANGE` | VALIDATION | validation | 422 | no | public | — | fix_input | `errors.validation.range` | platform |
| `AUTH_INVALID_CREDENTIALS` | AUTH | auth | 401 | no | public | — | reauthenticate | `errors.auth.invalid` | identity |
| `AUTH_SESSION_EXPIRED` | AUTH | auth | 401 | no | public | — | reauthenticate | `errors.auth.expired` | identity |
| `AUTH_FORBIDDEN` | AUTH | auth | 403 | no | public | — | contact_support | `errors.auth.forbidden` | identity |
| `USER_EMAIL_TAKEN` | USER | business | 409 | no | public | — | fix_input | `errors.user.emailTaken` | identity |
| `USER_NOT_FOUND` | USER | business | 404 | no | public | — | none | `errors.user.notFound` | identity |
| `BILLING_INSUFFICIENT_BALANCE` | BILLING | business | 402 | no | public | — | choose_alternative | `errors.billing.balance` | billing |
| `PAYMENT_CARD_DECLINED` | PAYMENT | payment | 402 | no | public | — | choose_alternative | `errors.payment.cardDeclined` | payments |
| `PAYMENT_PROVIDER_TIMEOUT` | PAYMENT | external | 503 | yes | internal | `SERVICE_UNAVAILABLE` | retry | `errors.payment.providerTimeout` | payments |
| `PAYMENT_PROVIDER_UNAVAILABLE` | PAYMENT | external | 502 | yes | internal | `SERVICE_UNAVAILABLE` | retry | `errors.payment.providerUnavailable` | payments |
| `DB_UNIQUE_VIOLATION` | DB | database | 409 | no | internal | `CONFLICT` | fix_input | `errors.db.conflict` | platform |
| `DB_DEADLOCK` | DB | database | 503 | yes | internal | `SERVICE_UNAVAILABLE` | retry | `errors.db.deadlock` | platform |
| `DB_SERIALIZATION_FAILURE` | DB | database | 503 | yes | internal | `SERVICE_UNAVAILABLE` | retry | `errors.db.serialization` | platform |
| `EXPORT_STORAGE_UNAVAILABLE` | EXPORT | external | 503 | yes | internal | `SERVICE_UNAVAILABLE` | retry | `errors.export.storage` | data |
| `EXPORT_SOURCE_QUERY_FAILED` | EXPORT | database | 503 | yes | internal | `SERVICE_UNAVAILABLE` | retry | `errors.export.query` | data |
| `EXPORT_EMPTY` | EXPORT | business | 200 | no | public | — | none | `errors.export.empty` | data |
| `WEBHOOK_SIGNATURE_INVALID` | WEBHOOK | auth | 401 | no | public | — | none | `errors.webhook.signature` | integrations |
| `WEBHOOK_DUPLICATE_EVENT` | WEBHOOK | business | 200 | no | public | — | none | `errors.webhook.duplicate` | integrations |
| `WEBHOOK_PROCESSING_FAILED` | WEBHOOK | business | 500 | no | internal | `SERVICE_UNAVAILABLE` | contact_support | `errors.webhook.processing` | integrations |
| `AGENT_TOKEN_LIMIT_EXCEEDED` | AGENT | business | 422 | no | public | — | fix_input | `errors.agent.tokenLimit` | ai |
| `AGENT_TOOL_TIMEOUT` | AGENT | external | 504 | yes | internal | `SERVICE_UNAVAILABLE` | retry | `errors.agent.toolTimeout` | ai |
| `AGENT_PROVIDER_UNAVAILABLE` | AGENT | external | 503 | yes | internal | `SERVICE_UNAVAILABLE` | retry | `errors.agent.providerUnavailable` | ai |
| `RATE_LIMIT_EXCEEDED` | RATE | resource | 429 | yes | public | — | retry | `errors.rateLimit.exceeded` | platform |
| `SYSTEM_MAINTENANCE` | SYSTEM | resource | 503 | yes | public | — | retry | `errors.system.maintenance` | platform |
| `INTERNAL_UNEXPECTED` | INTERNAL | unexpected | 500 | no | internal | `SERVICE_UNAVAILABLE` | contact_support | `errors.internal.unexpected` | platform |

> Note: `EXPORT_EMPTY` and `WEBHOOK_DUPLICATE_EVENT` map to **HTTP 200** because they are
> successful outcomes expressed as codes, not failures (Chapter 19, §19.17 discusses when returning
> `200` is legitimate).

## The registry as code (excerpt)

```ts
export const REGISTRY = {
  PAYMENT_CARD_DECLINED: {
    domain: "PAYMENT", category: "payment", http: 402, retryable: false,
    visibility: "public", clientAction: "choose_alternative",
    messageKey: "errors.payment.cardDeclined",
    description: "The card issuer declined the charge.", owner: "payments", since: "2026.01",
  },
  PAYMENT_PROVIDER_TIMEOUT: {
    domain: "PAYMENT", category: "external", http: 503, retryable: true,
    visibility: "internal", publicAlias: "SERVICE_UNAVAILABLE",
    clientAction: "retry", messageKey: "errors.payment.providerTimeout",
    description: "The PSP did not respond before the deadline.", owner: "payments", since: "2026.02",
  },
  DB_DEADLOCK: {
    domain: "DB", category: "database", http: 503, retryable: true,
    visibility: "internal", publicAlias: "SERVICE_UNAVAILABLE",
    clientAction: "retry", messageKey: "errors.db.deadlock",
    description: "A transaction deadlock was detected and can be retried.",
    owner: "platform", since: "2026.01",
  },
  EXPORT_EMPTY: {
    domain: "EXPORT", category: "business", http: 200, retryable: false,
    visibility: "public", clientAction: "none", messageKey: "errors.export.empty",
    description: "The export completed with zero rows.", owner: "data", since: "2026.02",
  },
} as const satisfies Record<string, CodeEntry>;
```

## Derived mapping tables

```ts
export type ErrorCode = keyof typeof REGISTRY;

export const HTTP: Record<ErrorCode, number> =
  mapValues(REGISTRY, (e) => e.http) as Record<ErrorCode, number>;

export const RETRYABLE: Record<ErrorCode, boolean> =
  mapValues(REGISTRY, (e) => e.retryable) as Record<ErrorCode, boolean>;

export const CLIENT_ACTION: Record<ErrorCode, ClientAction> =
  mapValues(REGISTRY, (e) => e.clientAction) as Record<ErrorCode, ClientAction>;

export const MESSAGE_KEY: Record<ErrorCode, string> =
  mapValues(REGISTRY, (e) => e.messageKey) as Record<ErrorCode, string>;

function mapValues<T, R>(o: Record<string, T>, f: (v: T) => R): Record<string, R> {
  return Object.fromEntries(Object.entries(o).map(([k, v]) => [k, f(v)]));
}
```

## The boundary: internal → public projection

```ts
export function publicCodeOf(code: ErrorCode): string {
  const e = REGISTRY[code];
  return e.visibility === "public" ? code : (e.publicAlias ?? "SERVICE_UNAVAILABLE");
}

export interface PublicError {
  code: string;
  messageKey: string;
  clientAction: ClientAction;
  retryable: boolean;
  details?: FieldError[];
  requestId?: string;
}

export function toPublicError(err: AppError): PublicError {
  const e = REGISTRY[err.code as ErrorCode];
  return {
    code: publicCodeOf(err.code as ErrorCode),
    messageKey: e?.messageKey ?? "errors.internal.unexpected",
    clientAction: e?.clientAction ?? "contact_support",
    retryable: e?.retryable ?? false,
    details: err.details?.map(({ field, code, message, meta }) => ({ field, code, message, meta })),
    requestId: err.correlationId,
  };
}
```

## The retry decision

```ts
export function shouldRetry(code: ErrorCode, attempt: number, deadlineExceeded: boolean): boolean {
  const e = REGISTRY[code];
  if (!e.retryable || deadlineExceeded) return false;
  const maxAttempts: Record<ErrorCategory, number> = {
    validation: 1, auth: 1, business: 1, payment: 1,
    database: 5, external: 5, resource: 8, unexpected: 1,
  };
  return attempt < maxAttempts[e.category];
}
```

## A worked request path

```text
1. ExportJob worker calls S3 and times out.
2. Adapter throws: code EXPORT_STORAGE_UNAVAILABLE, category external, cause FetchError.
3. Retry engine: RETRYABLE[EXPORT_STORAGE_UNAVAILABLE] === true  → retry with backoff (max 5).
4. After 5 attempts: job marked failed; error persisted with correlationId.
5. A support lookup by correlationId shows code, cause, tenant, shard.
6. If surfaced via API: publicCodeOf → SERVICE_UNAVAILABLE (503); messageKey rendered for the user.
```

One registry row drove the retry, the status, the message, and the support lookup.

## Generating docs from the table

```ts
// registry/generate-docs.ts
function toMarkdown(): string {
  const rows = Object.entries(REGISTRY).map(([code, e]) =>
    `| \`${code}\` | ${e.domain} | ${e.category} | ${e.http} | ${e.retryable} | ${e.visibility} | ${e.owner} |`,
  );
  return ["| Code | Domain | Category | HTTP | Retry | Visibility | Owner |",
          "| ---- | ------ | -------- | ---- | ----- | ---------- | ----- |",
          ...rows].join("\n");
}
```

Because docs are generated, the public catalog never drifts from the code.

## Key data / numbers

- **27 sample codes** across 12 reserved domains — a realistic mid-size SaaS surface.
- **HTTP distribution:** 422 validation, 401/403 auth, 404/409 business, 402 payment, 429 rate
  limit, 503/504 external, 500 unexpected, and two legitimate `200` outcome codes.
- **Retry max attempts by category:** database 5, external 5, resource 8, others 1.
- **Public vs internal:** roughly half the codes are internal and project to
  `SERVICE_UNAVAILABLE`; internal codes never reach clients verbatim.

## Real-world use case — Acme SaaS

Acme shipped this registry in one sprint. The frontend replaced per-endpoint error handling with a
single `switch (toPublicError(err).clientAction)`, the retry engine read `RETRYABLE`, the API
boundary read `HTTP`, and support tooling rendered `messageKey` and grouped by `code`. Adding
`AGENT_TOKEN_LIMIT_EXCEEDED` for the LLM feature took one review and one row: the status, retry
rule, client action, and message all followed automatically, and the generated docs updated on
merge. No consumer change was needed for the new code.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| One central registry | Total coverage, simple | Merge contention at scale |
| Domain-owned slices | Parallel, owned | Needs central merge validation |
| Generated docs | Never drifts | Build step required |
| Internal→public alias | Protects internals | Requires per-code alias |
| `200` outcome codes | Models "empty/duplicate" honestly | Easy to overuse |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every code all mapping fields | Leave `http`/`messageKey` blank |
| Derive tables and docs from the registry | Hand-maintain parallel lists |
| Project internal codes to public aliases | Expose `DB_DEADLOCK` to clients |
| Model empty/duplicate as outcome codes | Return `500` for a normal empty export |
| Keep one owner per domain | Leave codes ownerless |

## Common mistakes

- **Missing alias** on an internal code, leaking it to clients.
- **`500` for business outcomes** like empty exports or duplicates.
- **Hand-written docs** that disagree with the table.
- **Retrying non-retryable codes** because retryability was not centralized.
- **Codes without owners**, so nobody reviews changes.

## Checklist

- [ ] Does every code have all mapping columns filled?
- [ ] Are internal codes given a public alias?
- [ ] Are tables and docs generated from the registry?
- [ ] Are outcome codes (`EXPORT_EMPTY`) mapped to `200` deliberately?
- [ ] Does the retry engine read only `retryable` from the registry?
- [ ] Does every domain have an owner?

## Related

- [Registry-as-Code and Collision Testing](../02-deep-dive/01-registry-as-code-and-collision-testing.md)
- [Mapping Codes to Behavior](../01-concepts/04-mapping-codes-to-behavior.md)
- [Chapter 8 Overview](../README.md)
