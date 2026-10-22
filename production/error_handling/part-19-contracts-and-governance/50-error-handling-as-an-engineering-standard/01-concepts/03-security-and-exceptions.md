# Security Requirements and Exceptions to the Standard

> Part XIX · Chapter 50 · Sections 50.8–50.9 · _Estimated reading time: 18 min_
> **Prerequisite:** [Behavioral Standards: Propagation, Retry, Response, Recovery](./02-behavioral-standards.md)

## In one sentence

The standard has a **non-negotiable security floor** that no exception may cross, and
everything above that floor is handled through a **documented exceptions register** with an
owner and an expiry date.

## Why this matters in production

Error responses are the most under-reviewed surface in most systems, because the happy path
gets the attention and the failure path gets whatever the developer typed at 02:00. That is
exactly where disclosure happens:

- A stack trace containing a connection string with a password.
- A database error echoing the SQL statement, including the row values.
- An internal hostname that reveals the region topology.
- A validation error echoing a submitted token, because the field was named `token` and the
  message template was `{{field}} is invalid`.
- A tenant-scoped query failing with "user alice@example.com not found in tenant 42" — which
  discloses both existence and tenancy.

None of these are exotic. They are the default outcome of a team without a floor, and they are
hard to detect after the fact because the response body is rarely logged.

The floor is therefore **not negotiable**. Everything else in the standard is.

## 50.8 — Security requirements

### The disclosure floor

```text
R-SEC-1  A public error response contains no stack trace, source path, or internal symbol.
R-SEC-2  A public error response contains no SQL, no database error text, and no query
         parameters.
R-SEC-3  A public error response contains no internal hostname, container name, pod, IP,
         region, or service discovery address.
R-SEC-4  A public error response contains no secret, token, key, cookie, or session id —
         including inside a nested cause chain.
R-SEC-5  A public error response contains no personal data beyond what the requester
         already supplied in this request.
R-SEC-6  A public error response for a tenant-scoped resource does not disclose whether the
         resource exists in another tenant.
R-SEC-7  A public error response reflects no untrusted input verbatim; user-supplied text
         is escaped and length-capped.
R-SEC-8  An error that is not recognised is rendered as a generic internal error. Unknown
         error kinds default to the safest output, never to a raw dump.
```

R-SEC-8 is the one that saves you from the unknown-unknown. If a new framework exception
arrives and the boundary has no mapping, the default output is a fixed, safe sentence plus a
correlation id. The detail lives in the log, keyed by that id.

### What the response may contain

```text
ALLOWED in a public response      FORBIDDEN in a public response
──────────────────────────────────────────────────────────────────────────────
code (registered)                 stack traces / exception class names
type (URI)                        SQL / query text
title (fixed per type)            connection strings / DSNs
status                            internal hostnames, IPs, regions
detail (prose, capped)            secrets, tokens, keys, cookies
instance / requestId              PII not supplied by this requester
errors[] (field paths + sub-codes)  raw provider payloads
```

### The log/response split

The standard should draw this line explicitly, because it resolves most "how much detail do I
put in the error?" arguments:

```text
LOG (internal, access-controlled, retained per policy)   RESPONSE (public, untrusted)
────────────────────────────────────────────────────────  ──────────────────────────────
full cause chain                                      code + type + status
stack trace                                           safe one-line detail
sql / query text                                      requestId
provider payload (redacted)                           nothing else
correlation id                                        —
```

If support needs the detail, they use the `requestId` to find the log. The response exists for
users and integrations, not for debugging.

### Redaction

```text
R-SEC-9  Error context is built from an allowlist of fields (ids, counts, durations,
         hashes). It is never built by serialising a request object.
R-SEC-10 Redaction applies to nested causes, not just the top-level error.
R-SEC-11 Sensitive values are redacted at construction, not at serialization, so no
         intermediate log can capture them.
```

R-SEC-11 matters more than it looks. If redaction happens at the boundary, then the error was
already written to a log, shipped to a tracing system, and included in an exception tracker
with the secret in it. Redact at the source.

### Enumeration resistance

```text
R-SEC-12 Authentication failures do not distinguish "unknown account" from "wrong password"
         in any externally visible field.
R-SEC-13 Resource-not-found responses for tenant-scoped resources do not reveal whether
         the resource exists under a different tenant.
R-SEC-14 Timing must not be a side channel for enumeration: use a constant-cost comparison
         or equalise the failure paths.
```

### The security event contract

Security-relevant failures deserve their own codes — not because the client needs the detail,
but because the operations team needs to count them:

```text
AUTH_CREDENTIALS_REJECTED   401   no detail beyond "authentication failed"
AUTH_TENANT_SCOPE_VIOLATION 403   code present, detail empty; detail only in logs
SECURITY_SIGNATURE_INVALID  401   webhook surface
```

The *client* gets a generic message; the *log* gets the specifics. The code exists so that
`auth.credentials_rejected{tenant}` can be alerted on.

### What the standard must not do

- **Do not require an error message to be helpful.** "Helpful" and "safe" are different
  objectives; safety wins.
- **Do not require internals to be exposed for debugging.** Use the correlation id.
- **Do not ban the detail field entirely.** A useful, safe message is a usability feature.

## 50.9 — Exceptions to the standard

An exception is a **recorded, owned, time-limited deviation**. It exists so that the standard
can be strict without being wrong.

### Which rules may be excepted

| Rule class | Exceptable? |
| ---------- | ----------- |
| Security floor (R-SEC-1 … R-SEC-14) | **No. Never.** |
| Data integrity, idempotency, no-duplicate-side-effects | **No** |
| Structural rules (registry, naming, shape) | Yes, with a migration plan |
| Default retry/timeout values | Yes, with a measured justification |
| Recovery posture (fail-open vs fail-closed) | Yes, with a recorded security decision |
| Layer responsibilities | Rarely — indicates a design disagreement |

The distinction is **safety vs shape**. Safety rules encode lessons paid for in incidents;
shape rules encode current preferences. Shape rules change; safety rules do not get waived.

### The exceptions register

```yaml
# standards/error-handling/exceptions.yaml
exceptions:
  - id: EX-014
    rule: R-RETRY-3            # every retry policy declares a total deadline
    scope: billing/billing-service (invoice reconciler)
    justification: >
      The invoice reconciler runs under a 6-hour SLA window and processes a queue
      whose delivery can stall for hours; a 15-minute total deadline would abort
      legitimate work. Mitigated by a per-attempt deadline of 30s and a hard cap
      of 500 attempts, plus a runbook that alerts after 100 attempts.
    approved_by: platform-guild, security-review
    approved_on: 2026-03-14
    review_on: 2026-09-14     # every exception expires
    expires_on: 2026-09-14
    compensating_controls:
      - per-attempt deadline of 30s
      - attempt cap of 500
      - alert after 100 attempts
    status: active
```

Required fields, without exception: `rule`, `scope`, `justification`, `approved_by`,
`review_on`, `expires_on`, and — for any rule touching security — `compensating_controls`.

### The process

```text
1. A team identifies a genuine conflict between the standard and its context.
2. It files an exception with a justification and a proposed expiry.
3. The standard's owner reviews it. The owning guild approves, with the security review
   required for safety-adjacent rules.
4. The exception is recorded, dated, and linked from the affected code.
5. At review_on, the exception is re-justified, made permanent (which means amending the
   standard), or closed.
6. Expired exceptions block CI: the exemption lapses and the rule applies again.
```

Step 6 is the mechanism that stops exceptions from becoming permanent. The check is trivial:

```ts
function isExceptionActive(ex: Exception): boolean {
  return ex.status === "active" && new Date(ex.expires_on) > new Date();
}
```

### Exception debt

Exceptions are a **liability**, and the count should be visible:

```text
EXCEPTION DEBT DASHBOARD
active exceptions        7
expiring within 30 days  2
expired (not closed)     1     ← CI is failing somewhere; fix it
average lifetime         94 days
permanent amendments     3     ← these became standard rules
```

A growing count means the standard is wrong in that area. The right response is to **amend
the standard**, not to add more exceptions. A standard with 40 active exceptions is a standard
nobody believes.

### The alternative to an exception

Before filing, ask three questions:

```text
1. Can the rule be scoped down?   ("applies to all writes" → "applies to public writes")
2. Can the rule be made measurable, so the exception becomes a tighter rule?
3. Is this actually a new case the standard never anticipated → amend the standard.
```

If the answer to all three is "no", file the exception.

## Worked example — the webhook signature case

Acme's `WebhookIngest` needed to return `401` with a body explaining that the Stripe signature
did not match, because their partner engineers kept asking what was wrong. The standard's
security floor said the response must not confirm or deny anything about the secret.

The exception attempt was rejected — R-SEC-12 forbids distinguishing authentication failure
kinds. Instead, the standard was **amended** to cover the case explicitly:

```text
R-SEC-15  For webhook signature failures, the response is a fixed 401 with code
          SECURITY_SIGNATURE_INVALID and the detail "Signature verification failed."
          It MUST NOT indicate which component failed, which byte differed, or the
          expected signature.
```

That amendment is now **better than the exception** would have been: it tells every team
exactly what to return, and it has a CI check (the response body is byte-identical across all
signature failures).

## Key data / numbers

- **Security floor:** 15 rules (R-SEC-1 … R-SEC-15); **not exceptable**.
- **Non-exceptable classes:** security, data integrity, idempotency, no-duplicate-side-effects.
- **Exception record fields:** 8 required (rule, scope, justification, approver, approval date,
  review date, expiry date, compensating controls).
- **Default exception lifetime:** **180 days**; longer requires a guild-level justification.
- **Review reminders:** 30 days before expiry; the check runs in CI daily.
- **Exception debt target:** < **10 active** exceptions per 100 rules; > 25 means the standard
  needs amending, not more exceptions.
- **Response size cap:** `detail` ≤ **256 characters**; `errors[]` ≤ **50 entries** (plus a
  count of the remainder).
- **Retention split:** logs keep full detail under the org's log-retention policy; responses
  keep only the safe fields.

## Real-world use case — AgentRun

Acme's `AgentRun` feature reports tool failures back to the user through the API. The first
implementation returned the tool's own error text:

```json
{ "code": "AGENT_TOOL_FAILED", "detail": "search tool: API key sk_live_8f2... quota exceeded" }
```

Two problems, one of them severe:

1. **Disclosure.** The upstream provider's message contained a truncated API key and a quota
   number — information about Acme's provider account, exposed to every tenant using the agent.
2. **Instability.** The detail text was the provider's wording, so Acme's public contract was
   accidentally the provider's contract. When the provider changed the wording, Acme's
   frontend's matching broke.

The standard fixed both without a special case: the code (`AGENT_TOOL_FAILED`) carries the
condition, `detail` is a fixed generic sentence ("The tool did not complete. Reference
<requestId>."), and the provider's message goes to the log with the secret redacted at
construction. The user gets a reference; support gets the detail.

A second standard rule earned its keep the same week: **redaction at construction**, not at
serialization. Because redaction happened where the error was created, the redacted provider
message was what reached the log, the trace, and the error tracker — not the version with the
key fragment.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Strict standard, no exceptions | Uniform; no local variation | Wrong rules get worked around silently | Only for safety rules |
| Strict standard + exceptions register | Uniform, with honest local variation | Register can rot; needs review cadence | Default recommendation |
| Guidelines only | Maximum local fit | Inconsistency; no enforcement | Never for safety |
| Standard with per-team overrides | Local fit | Divergence; "override" becomes default | Rarely |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat the security floor as non-exceptable | Waive a disclosure rule "just this once" |
| Redact at construction | Redact only at serialization time |
| Keep details in logs, keyed by request id | Ship internal detail to clients for debuggability |
| Amend the standard when a case is new | File an exception for a case the standard never saw |
| Give every exception an owner and an expiry | Let exceptions accumulate without review |
| Fail the CI check when an exception expires | Silently extend expired exceptions |
| Equalise authentication failure paths | Distinguish "unknown user" from "wrong password" |

## Common mistakes

- **The Exception Ratchet.** Every quarter adds exceptions, none expire.
- **The Waived Safety Rule.** "We need the stack trace in this one endpoint."
- **The Late Redaction.** The secret already reached three log systems.
- **The Permissive Default.** An unmapped exception is rendered with its raw message.
- **The Unbounded Detail.** A 4 000-character error body with an entire SQL statement.
- **The Enumeration Leak.** "No account with that email" versus "wrong password".

## Checklist

- [ ] The security floor exists as explicit, numbered, non-exceptable rules.
- [ ] The log/response split is written into the standard.
- [ ] Redaction happens at error construction, including nested causes.
- [ ] Context is allowlist-built, never serialised from a request object.
- [ ] Unknown error kinds render as a generic safe response.
- [ ] Authentication failures are indistinguishable to the client.
- [ ] The exceptions register has required fields, expiry, and a CI check on expiry.
- [ ] Exception debt is visible and trending down.

## Related

- [Behavioral Standards: Propagation, Retry, Response, Recovery](./02-behavioral-standards.md)
- [Durable Rules, Exceptions, and Change Management](../02-deep-dive/01-durable-vs-ceremonial-rules.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
- [Chapter 36 — Sensitive Data and Error Context](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
