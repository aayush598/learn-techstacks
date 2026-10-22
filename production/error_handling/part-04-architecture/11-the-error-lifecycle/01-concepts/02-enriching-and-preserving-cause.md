# Enriching with Safe Context and Preserving the Cause

> Part IV · Chapter 11 · Sections 11.5, 11.6 · _Estimated reading time: 17 min_
> **Prerequisite:** [The Lifecycle: Origin Through Classification](./01-lifecycle-overview.md)

## In one sentence

Stage 5 **enriches** an error with safe, structured context (who, what, where — never secrets),
and stage 6 **preserves the original cause** underneath every wrapper — the two stages that
decide whether an incident takes ten minutes or ten hours.

## Why this matters in production

An error without context is a riddle; an error with *leaked* context is a security incident.
Both failures come from the same two stages done carelessly:

- **Missing enrichment:** "`DB_UNAVAILABLE` on `/exports`" — which tenant? which query? which
  attempt? On-call redeploys and greps instead of acting.
- **Unsafe enrichment:** context includes the request body, an auth header, or a Stripe payload —
  now your logs are a PII store and your error envelope is a disclosure channel (Chapter 34).
- **Broken cause chain:** the repository re-threw `new Error("db failed")`, discarding the
  driver error. Triage now depends on log correlation *hoping* it captured the right lines.

Enrichment and cause preservation are what make the rest of the lifecycle **operable**.

## Stage 5 — Enriching with safe context (11.5)

Add structured, **allowlisted** fields as the error moves up — never dump whatever is nearby:

| Context field | Source | Why it's safe |
| ------------- | ------ | ------------- |
| `operation` | the code path (`createCheckout`) | not user data |
| `tenantId` | authenticated context | identifier, not content |
| `correlationId` | middleware (Ch. 10) | opaque ID |
| `attempt` / `maxAttempts` | worker envelope | numbers |
| `resourceType`/`resourceId` | the aggregate being worked on | identifier |
| `durationMs` | timer around the operation | number |

Explicitly forbidden in context by default: request bodies, auth headers/tokens, query strings,
payment payloads, emails/names, raw SQL with literals, file contents.

```ts
// ✅ allowlisted enrichment — explicit fields only
throw new PersistenceError("DB_UNAVAILABLE", {
  cause: err,
  context: { operation: "exports.insertBatch", tenantId, batch: 12, rows: 500 },
});

// ❌ whole-object dumps — the classic leak
throw new PersistenceError("DB_UNAVAILABLE", { context: { req, user, body, headers } });
```

Enforcement options, from cheap to strict: an allowlist in the serializer, a lint rule banning
`context: { ...spread }`, and a schema (`context` must match a per-code JSON schema) asserted in
tests. Redaction (Ch. 10 utilities) is the last line, not the first.

## Stage 6 — Preserving the original cause (11.6)

The **cause chain** is the error's history: every translation attaches, never replaces.

```text
  AppError DB_UNAVAILABLE  ──cause──▶  repository Error  ──cause──▶  Postgres error
  (stage 3 representation)             (translation)                  (origin, stage 1)
```

Mechanics by language: JS/TS `new Error(msg, { cause })`; Python `raise X from Y`; Go wraps with
`fmt.Errorf("...: %w", err)`; .NET `ExceptionDispatchInfo`/inner exceptions; Rust `thiserror`'s
`#[from]` preserves via `source()`. Whichever you use, the rules are the same:

1. **Every translation attaches a cause** — including "unknown third-party blob" translations.
2. **Cause is for logs and support, never for the public envelope** — sanitize at render (Ch. 10
   `toProblem`), keep the chain intact internally.
3. **Depth is fine; breakage is not.** A five-link chain that reconstructs the story beats a
   one-link chain that says "failed."

```ts
export function normalize(err: unknown): AppError {
  if (isAppError(err)) return err;
  return { code: "INTERNAL_ERROR", retryable: false, cause: err };   // always attach, never replace
}
```

## The combined rule

**Enrich upward, preserve downward.** Each layer adds facts above and keeps history below:

```text
 layer        adds (stage 5)              keeps (stage 6)
 repo         operation, batch            driver error as cause
 app          tenantId, attempt           repo error as cause
 worker       jobId, attempt/max          app error as cause
 filter       correlationId (already set) full chain in logs only
```

## Key data / numbers

- Cause chain access: JS `err.cause` (ES2022 standard), Python `__cause__`, Go `%w` + `errors.Is/As`,
  .NET `InnerException`, Rust `source()`.
- Chain-depth recommendation: **no practical limit internally**, but cap what you *print* —
  renderers show the top-level code + a correlation ID; full chains go to logs.
- Redaction defaults worth adopting: never serialize `authorization`, `cookie`, `set-cookie`,
  `x-api-key` headers; mask values matching card-like patterns (Chapter 36).
- Correlation ID placement: on the error at stage 5 (from middleware), never regenerated later.

## Real-world use case — Acme SaaS support workflow

A support engineer got a ticket: "export failed." The log line read
`code=EXPORT_FAILED tenant=tnt_8412 operation=exports.streamBatch attempt=3 correlationId=corr_5b8`.
Thirty seconds later the chain read:

```text
EXPORT_FAILED
 └─ STORAGE_UPLOAD_FAILED (infra/s3.ts)
     └─ NetworkingError: Connection reset during upload (AWS SDK)
```

Total triage: under a minute — because stage 5 attached `operation`/`attempt` and stage 6 kept
the SDK error. The same bug pre-fix had been "fixed" by a wrapper that rethrew
`new Error("export failed")`; the previous occurrence took **two engineer-days** and a staging
repro to identify a flaky NAT gateway. The only change between those incidents was lifecycle
discipline at stages 5–6.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Allowlisted structured context + full cause chain (recommended) | Fast triage, safe | Requires context schema discipline | Default |
| Message-only errors | Tiny | Untriageable; incidents cost days | Never |
| Dump-everything context | Great logs (until audit) | PII/secrets exposure; compliance risk | Never |
| Sanitize by deleting the cause | "Safe" but blind | Loses the only history you had | Never — sanitize the render, not the chain |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Attach context from an allowlist per code | Spread `req`/`user`/`body` into context |
| Attach `cause` on every translation/wrap | Re-threw bare `new Error("failed")` |
| Correlate via one ID set at stage 5 | Mint fresh IDs per layer |
| Keep chains internal; sanitize at render | Send `cause` chains to clients |

## Common mistakes

- **Enrichment by interpolation** — `message: \`failed for ${JSON.stringify(body)}\`` smuggles PII
  past any context schema; forbid body interpolation in review/lint.
- **Double-cause clobbering** — wrapping an `AppError` in another `AppError` *without* `cause`
  overwrites history; always chain.
- **Context on the wrong object** — enriching the log line but not the error object means
  non-logging paths (DLQ records, alert payloads) lose it; enrich the error, then log the error.

## Checklist

- [ ] Every code has an allowlisted context schema.
- [ ] No serialization path emits forbidden headers/fields.
- [ ] Every translation/wrap attaches `cause` (test: chain reaches the origin).
- [ ] Renderers emit code + correlation ID only; full chains stay in logs.

## Related

- [The Lifecycle: Origin Through Classification](./01-lifecycle-overview.md)
- [Propagation, Translation, and Recovery](./03-propagation-translation-and-recovery.md)
- [Chapter 6 — Designing the Application's Error Model](../../../part-03-error-models/06-designing-the-applications-error-model/README.md)
- [Chapter 36 — Sensitive Data and Error Context](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
