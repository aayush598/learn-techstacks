# Secrets, PII, and Tenant Leakage

> Part XIII · Chapter 34 · Sections 34.5–34.7 · _Estimated reading time: 17 min_
> **Prerequisite:** [Errors as a Disclosure Channel](./01-errors-as-a-disclosure-channel.md)

## In one sentence

**Secret/credential leakage**, **PII in messages**, and **multi-tenant leakage** are the
highest-severity classes of error disclosure — a leaked key is an open door, a leaked PII field is
a compliance incident, and a leaked cross-tenant value is a broken isolation guarantee.

## Why this matters in production

These three classes do not just aid reconnaissance; they *are* the compromise.

- A Stripe secret key in an error log lets anyone charge cards.
- A customer email in an unhandled rejection log turns an internal incident into a GDPR/CCPA
  notification ("personal data breach" has a 72-hour reporting clock under GDPR Article 33).
- A tenant B row appearing in tenant A's error detail is a **cross-tenant data breach**, the one
  thing a multi-tenant SaaS must never do.

All three typically originate not from malicious intent but from convenience: `console.log(body)`
during debugging, an ORM exception that includes the entity, or a shared connection pool that
forgets the tenant scope.

## The three classes

| Class | Examples | Where it hides |
| ----- | -------- | -------------- |
| **Secrets / credentials** | API keys, OAuth tokens, session cookies, DB passwords, signing keys, private keys, webhook secrets | Config dumps, HTTP client errors, auth middleware logs, serialized request headers |
| **PII** | Email, phone, full name, address, government IDs, IP address, payment identifiers, free-text user input | Validation messages, search errors, LLM prompts/outputs, job payloads |
| **Tenant data** | Row values, tenant IDs in shared logs, object keys, cache keys, another tenant's name | Unscoped queries, shared caches, error messages that include the resolved entity |

### Secrets (CWE-532, CWE-798)

Secrets leak most often through:
- **Serialized request/response objects** that include `Authorization` or `Cookie` headers.
- **HTTP client libraries** that throw errors containing the full URL (with query-string tokens),
  request headers, or the request body.
- **Config errors** that print the parsed configuration.
- **Environment dumps** in startup failures.

### PII (CWE-359)

PII leaks through messages humans wrote for debugging:
- `throw new Error(\`No user with email ${email}\`)`
- A validation error echoing the rejected value.
- An LLM provider error that includes the prompt (and the prompt contained user text).

### Multi-tenant leakage (OWASP A01, A04)

Tenant leakage is a *context* bug more than a *message* bug:
- A shared logger without tenant scoping writes tenant-specific values into a global stream.
- A cache keyed without tenant ID serves tenant B's error detail to tenant A.
- An error message names a resolved entity that belongs to another tenant.

## How it works (mechanics)

```text
 untrusted/rich input
      │
      ▼
 [ root context ]  <-- tenantId, userId, requestId attached HERE
      │
      ▼
 business logic throws  -- message must not interpolate PII
      │
      ▼
 boundary serialization -- allowlist; never emit cause chain raw
      │
      ├─▶ external response  (no PII, no secrets, no cross-tenant)
      ├─▶ internal log       (PII minimized; secrets always stripped)
      └─▶ job/DLQ record     (secret-stripped payload; tenant-scoped)
```

**Secrets must be stripped at every sink, including internal ones.** PII may be retained
internally when there is a legitimate operational need, but it must be minimized and access
controlled. Tenant values must always carry their tenant scope and be partitioned accordingly.

## Worked example — an HTTP client that leaks a token

```ts
// ❌ Many HTTP client errors include the URL and headers.
catch (err: unknown) {
  log.error({ err }, "checkout capture failed"); // may include Authorization header, full URL
  throw new InternalError("PAYMENT_ERROR", String(err));
}

// ✅ Strip secrets from the request context before it can enter any error.
try {
  await stripe.charges.create(params, { idempotencyKey });
} catch (err: unknown) {
  log.error(
    {
      provider: "stripe",
      // explicit allowlist — no URL, no headers, no params
      status: (err as any)?.statusCode,
      requestId: (err as any)?.requestId,
      tenantId,
      correlationId,
    },
    "stripe capture failed",
  );
  throw new UpstreamError("PAYMENT_PROVIDER_ERROR", "Payment could not be completed.");
}
```

Note that even the `log.error` line does **not** pass `err` wholesale — it passes an allowlist.

## Key data / numbers

- **GDPR Article 33**: personal-data breaches must be reported to the supervisory authority within
  **72 hours** of awareness. A PII-in-logs incident is a reportable breach.
- **PCI DSS v4.0 Requirement 3.3**: the PAN (card number) must not be stored after authorization
  and must be rendered unreadable wherever stored; card data must **never** appear in logs or
  error messages. **Requirement 10** restricts log access.
- **CWE-532** (insertion of sensitive information into log file), **CWE-798** (hard-coded
  credentials), **CWE-359** (exposure of private personal information).
- **OWASP Top 10 (2021) A01: Broken Access Control** covers cross-tenant access; **A04: Insecure
  Design** covers missing tenant scoping in shared resources.
- **PII categories commonly cited**: name, email, phone, address, date of birth, government ID,
  IP address, device identifier, financial account, biometric data.

## Real-world use case — Acme SaaS

Acme ran a shared Redis cache for tenant-scoped "recent activity" lists. A cache key was built as
`recent:{userId}` without the tenant prefix. On a cache miss caused by a serialization error, the
error message included the cached JSON — which contained tenant B's activity titles — and that
message was returned in tenant A's request. Fix: cache keys became `t:{tenantId}:recent:{userId}`,
the serialization error message became generic (`ACTIVITY_UNAVAILABLE`), and an automated test now
asserts that no error message in the codebase contains a raw cache value. The incident was caught
internally before any customer report, and the fix closed the class of bug, not just the instance.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Omit PII from all logs | Strong privacy | Harder debugging | Regulated data, high-sensitivity paths |
| Redact PII (tokenize/truncate) in logs | Debuggable + safer | Need a redaction utility | Default for most internal logs |
| Allow raw payload in exception tracker | Full debuggability | Tracker must be access-controlled | Only with strong tracker RBAC |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Allowlist what goes into logs | `log.error(err)` with a rich object |
| Interpolate stable codes, not values | `throw new Error(\`bad email ${email}\`)` |
| Scope every cache key and log line by tenant | Assume a shared key is tenant-safe |
| Strip `Authorization`/`Cookie` at the HTTP boundary | Log request headers wholesale |
| Tokenize/truncate PII in logs | Store full PII "just in case" |

## Common mistakes

- **Logging the whole request object.** It contains headers, cookies, and sometimes the body.
- **Trusting the exception tracker is private.** It is often broadly readable and searchable.
- **Interpolating PII into a message you also return externally.** The same string serves two
  audiences with opposite requirements.
- **Forgetting the tenant on background paths.** Workers without tenant context write unscoped
  records.
- **Storing webhook payloads raw.** They often contain PII and financial data.

## Checklist

- [ ] Do request/response loggers strip `Authorization`, `Cookie`, and query tokens?
- [ ] Are secrets removed at *every* sink, including internal logs and DLQs?
- [ ] Does any error message interpolate a PII value?
- [ ] Are all cache keys and log records tenant-scoped?
- [ ] Can an error message name an entity from another tenant?
- [ ] Is the exception tracker access-controlled and audited?

## Related

- [Stack Traces, Schemas, and Infrastructure Leakage](./02-stack-traces-schemas-and-infrastructure-leakage.md)
- [Authorization Disclosure, Enumeration, and Timing](./04-authorization-disclosure-enumeration-and-timing.md)
- [Chapter 36 — Sensitive Data and Error Context](../../36-sensitive-data-and-error-context/README.md)
- [Deep dive: Redaction Strategy](../02-deep-dive/03-redaction-strategy.md)
- [Glossary](../../../GLOSSARY.md)
