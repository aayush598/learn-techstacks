# Deep Dive — Information Disclosure Channels

> Part XIII · Chapter 34 · Sections 34.1–34.7 (mechanics) · _Estimated reading time: 20 min_
> **Prerequisite:** [Errors as a Disclosure Channel](../01-concepts/01-errors-as-a-disclosure-channel.md)

## In one sentence

An error leaks through **channels**, not fields — the same exception object reaches a response, a
log stream, a metric, a queue record, and a support tool, and each channel has its own audience,
retention, and export boundary, so **you must map the channel before you can close it**.

## Why this matters in production

Teams that "sanitize the response" often still leak through five other channels. A stack trace you
never send to a user still leaves through a **metric label** you never wanted indexed. A secret you
strip from the body still lands in the **dead-letter queue**. Closing disclosure means enumerating
channels and giving each an explicit policy — this file is the map.

## The seven channels

```text
                     ┌────────────────────────────────────────────┐
   thrown error ────▶│ envelope / error object                     │
                     └───────┬─────────┬──────────┬────────┬──────┘
                             ▼         ▼          ▼        ▼
                        response    log     metric    queue   support
                          (a)       (b)      (c)      (d)      (e)
                             │         │          │        │
                             ▼         ▼          ▼        ▼
                          also:     exception   tracing   webhook
                          headers   tracker      spans     retries
                          (f)        (g)
```

| # | Channel | Audience | Retention | Export risk | Primary control |
| - | ------- | -------- | --------- | ----------- | --------------- |
| a | HTTP/API response | Caller (untrusted) | None | Public | Allowlist serializer |
| b | Structured logs | Wide internal | Days–months | Often to 3rd parties | Structured + PII minimization |
| c | Metric labels | Dashboards | Long | Often SaaS-hosted | No high-cardinality PII |
| d | Queue / DLQ record | Operators | Days–weeks | Dumped to tickets | Secret-strip payloads |
| e | Support tooling | Support agents | Long | Broad read | Tenant scoping + RBAC |
| f | Response headers | Caller + proxies | None | Public | Strip version banners |
| g | Exception tracker | Engineers | Months | Access-controlled | Full detail OK (RBAC) |

## Channel mechanics and controls

### (a) Response body — the only channel users see

Controlled by the serializer. Must contain only policy-approved fields. See
[the sanitizer example](../03-practical-examples/01-error-sanitizer-allowlist-serializer.md).

### (b) Logs — the channel that leaves your building

Logs are the highest-volume leakage channel because they are *meant* to be verbose. Two rules:
structured records (no interpolation) and PII minimization. Secrets must never enter logs.

### (c) Metrics — the channel nobody audits

The single most overlooked channel. A metric like `login_failed{email="alice@corp.com"}` turns a
private dashboard into a searchable PII index, and the metrics backend is often a third-party SaaS.

### (d) Queue / DLQ records — the channel that outlives the request

Failed jobs keep their payload for days, and DLQ records are frequently pasted into incidents. Treat
the payload as semi-public: strip secrets before enqueue, scope by tenant.

### (e) Support tooling — the channel with the widest human access

Support agents need context, but "the error object, verbatim" gives them another tenant's data and
secrets. Serve a **tenant-scoped, redacted** projection, not the raw record.

### (f) Response headers

`Server`, `X-Powered-By`, and stack-bearing debug headers leak the stack. Remove at the proxy.

### (g) Exception tracker — the sanctioned full-detail channel

This is where verbosity belongs. Its control is **RBAC and audit**, not redaction — but the
integration must still avoid credentials, because trackers are sometimes broadly readable.

## Worked example — one error, seven channels

Consider a failed Stripe charge inside `Checkout`:

```ts
// The error carries: provider message, provider requestId, the idempotency key,
// the customer email, and the raw params (including last4).
const err = new PaymentError({
  providerMessage: stripeErr.message,
  providerRequestId: stripeErr.requestId,
  idempotencyKey,        // semi-secret
  customerEmail,         // PII
  params,                // includes payment method details
  cause: stripeErr,
});
```

| Channel | What it may receive | Why |
| ------- | ------------------- | --- |
| (a) response | `{ code:"PAYMENT_DECLINED", requestId }` | Caller learns outcome + a support ref |
| (b) log | `{ provider, status, requestId, tenantId }` — **no email, no params, no key** | Structured, minimized |
| (c) metric | `checkout_failed_total{provider="stripe", code="declined"}` — **no tenant** | Bounded cardinality |
| (d) DLQ | payload with `idempotencyKey` and `params` **stripped** | Survives in tickets |
| (e) support UI | tenant-scoped view: outcome, requestId, timestamp | No cross-tenant, no secrets |
| (f) headers | normal headers only | Nothing added |
| (g) tracker | the full object | Engineers debug the real cause |

The same exception is **routed differently per channel** — that routing table *is* your disclosure
policy in executable form.

## Implementing a per-channel router

```ts
interface ErrorContext {
  tenantId: string;
  correlationId: string;
  userId?: string;
  provider?: string;
}

function toChannel(err: AppError, channel: Channel, ctx: ErrorContext) {
  switch (channel) {
    case "response":
      return { code: err.publicCode, message: err.safeMessage, requestId: ctx.correlationId };
    case "log":
      return {
        code: err.code,
        class: err.class,
        tenantId: ctx.tenantId,
        provider: ctx.provider,
        requestId: ctx.correlationId,
      };
    case "metric":
      return { provider: ctx.provider, code: err.code }; // bounded labels only
    case "tracker":
      return err; // full detail; RBAC-controlled sink
  }
}
```

The invariant: **every channel has an explicit `toChannel` branch.** No channel receives `err`
directly except the tracker.

## Key data / numbers

- **OWASP A09: Security Logging and Monitoring Failures** treats logs as security-sensitive because
  they are read and exported widely.
- **Cardinality rule**: metric labels must not carry user/tenant/email values; high-cardinality
  labels also break most metrics backends operationally, so security and performance agree here.
- **Retention varies by channel**: responses 0, logs days–months, DLQ days–weeks, tracker months.
  Longer retention = higher disclosure risk; keep secrets out of the longest-lived channels.
- **CWE-532** (sensitive info into logs) is the canonical weakness for channels (b)–(e).

## Real-world use case — Acme SaaS

Acme's `ExportJob` failure metric was `export_failed{tenant="acme-corp", email="ops@acme-corp.com"}`.
The metrics backend was a third-party SaaS, so every export failure shipped a tenant name and an
email to an external vendor — a PII export no one had reviewed. Discovery came from a vendor
questionnaire. Fix: labels reduced to `{code, size_bucket}` (bounded), per-tenant detail moved to the
tenant-scoped job record, and a review gate now requires any new metric label to be from a documented
allowlist. The disclosure policy table gained a metrics row that previously did not exist.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Per-channel `toChannel` router | Explicit, auditable | More code | All production error paths |
| One sanitizer for response, raw `err` elsewhere | Less code | Leaks in logs/DLQ/metrics | Never |
| Tracker-only full detail | Single verbose sink | Requires solid RBAC | Default |

## Common mistakes

- **Auditing only the response.** Six other channels exist.
- **Metric labels with user data.** Bounded-cardinality rule and security align; honor both.
- **Assuming logs are private.** They are exported to vendors, dashboards, and tickets.
- **Forgetting DLQ payloads.** They persist and get pasted around.
- **Over-restricting the tracker.** Engineers need the real cause; that is why it exists.

## Checklist

- [ ] Have you listed all channels an error reaches in your system?
- [ ] Does each channel have an explicit, reviewed projection?
- [ ] Are metric labels free of user/tenant identifiers?
- [ ] Are secrets stripped before enqueue (DLQ)?
- [ ] Is the support view tenant-scoped and redacted?
- [ ] Is the exception tracker RBAC-controlled and audited?

## Related

- [Redaction Strategy](./03-redaction-strategy.md)
- [Errors as a Disclosure Channel](../01-concepts/01-errors-as-a-disclosure-channel.md)
- [Secrets, PII, and Tenant Leakage](../01-concepts/03-secrets-pii-and-tenant-leakage.md)
- [Chapter reference: Disclosure policy matrix](../05-reference/README.md)
- [Glossary](../../../GLOSSARY.md)
