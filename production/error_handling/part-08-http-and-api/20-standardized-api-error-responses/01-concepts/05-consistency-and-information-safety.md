# Consistency and Information Safety

> Part VIII · Chapter 20 · Sections 20.14, 20.15, 20.16, 20.17 · _Estimated reading time: 17 min_
> **Prerequisite:** [The Error Envelope and RFC 9457](./01-error-envelope-and-rfc-9457.md)

## In one sentence

One envelope shape across every endpoint, version, and content path — **structurally incapable
of carrying stack traces, SQL, or infrastructure details** — is not aesthetic consistency;
it is what makes clients, support, and your own security posture scale.

## Why this matters in production

Inconsistency compounds. Each new "slightly different" error shape adds a parser branch to
every SDK, a documentation section, and a test. Within a year the error surface has a dozen
shapes, three of them undocumented, one of them leaking `err.stack` "just in staging." The
leak always ships to production — usually through the endpoint written at 2 a.m. by whoever
least knew the rules. **Consistency and safety are the same engineering problem**: both are
solved by making the correct shape the *only* shape the code can produce.

## Core concept — 20.14 / 20.15: one shape, enforced

**Consistency (20.14)** means: every 4xx/5xx body is the same base Problem Details document,
with the same extension members, the same naming, the same header pairing (`Content-Type:
application/problem+json`, optional `X-Request-Id`). Variation happens in *member values* and
*optional members*, never in top-level shape.

**Avoiding inconsistent shapes (20.15)** means attacking the known mutants:

| Mutant shape | Why it appears | Fix |
| ------------ | -------------- | --- |
| Bare string body | Quick `res.send("oops")` | Catch-all normalizes everything |
| `{message}` only | Framework default (`NotFoundError: ...`) | Translate framework errors at the boundary |
| `{error: {code, message}}` v1 legacy | Pre-RFC habit | One-time migration + versioned cutover |
| HTML error page | Framework/dev-mode default | Ensure production error renderer outputs problem JSON |
| Empty body on error | `res.status(404).end()` | Always serialize the envelope |
| Success `{data}` with embedded error | "Simpler for clients" | Error statuses carry problem documents, not data envelopes |

Enforcement mechanisms, in increasing strength:

1. **Style/lint rules** (weakest — review-dependent).
2. **A single `sendProblem()` helper** every path must use.
3. **Type-level:** handlers return `Result<Body, AppError>`; only the boundary layer owns
   serialization (Ch. 21).
4. **Contract tests** asserting shape for every error code + a fuzz of unhandled exceptions.
5. **Serializer accepts only `PublicProblem`** — the structural guarantee (next section).

## 20.16 / 20.17 — no stack traces, no DB/infra details

These are the two named sins of error bodies, and both are prevented by *construction*, not
redaction checklists:

- **No stack traces (20.16).** Stacks reveal file layout, framework versions, and internal
  method names; they also change per deploy, so any client parsing them breaks silently.
  They belong in the log keyed by `requestId`, full stop.
- **No DB/infra details (20.17).** SQL text, constraint names (`unique_constraint
  "projects_slug_key"`), ORM messages, hostnames, pod names, bucket names, queue names,
  provider SDK errors. Each is reconnaissance; together they are a system diagram handed to
  an attacker — and a confusion machine for users.

The structural pattern:

```text
  thrown: Error (full fidelity: message, stack, cause, sql, tenant)
        │
        │  classify → registry → public projection (PublicProblem)
        ▼
  sendProblem(problem)  ── serializes ONLY PublicProblem
        │                  (no err.stack field exists on this type)
        ▼
  wire: { type, title, status, detail, instance, code, requestId, errors? }
```

Two rules make it airtight:

1. **The serializer's input type has no slot for a stack.** `PublicProblem` ≠ `Error`.
2. **Unknown/unhandled errors project to a fixed generic problem** (`type:
   /problems/internal-error`, `detail: "An unexpected error occurred."`, `code:
   INTERNAL_ERROR`) — the *same* document for every bug, so bugs cannot fingerprint
   themselves through variations in message text.

> ⚠️ **Hazard.** "We only leak stacks in staging" is a configuration statement, not a design.
> Configurations roll out wrong. If staging needs richer errors, add a *separate* debug
> channel (request-header-gated, off in production, loudly logged when used) — never vary the
> production envelope's shape.

## How it works — the consistency checklist per response

For any error response your API emits, all must hold:

```text
[ ] Content-Type is application/problem+json
[ ] Body parses as a single Problem Details object (not array/string/HTML)
[ ] type ∈ the published /problems namespace (or documented about:blank exception)
[ ] title matches the fixed label for that type
[ ] status mirrors the HTTP status line exactly
[ ] code is a public registry code (alias applied if internal)
[ ] requestId present and matches X-Request-Id (if emitted)
[ ] detail is one safe sentence; no stack/SQL/host/vendor tokens
[ ] errors[] present iff the failure is field-level validation
[ ] no member names outside the documented extension set
```

Encode this as a contract test over the registry; it runs in milliseconds and outlives every
engineer's memory of the rules.

## Worked example — same bug, three shapes

The same null-pointer bug in `Checkout` under three regimes:

❌ Framework default:

```http
HTTP/1.1 500 Internal Server Error
Content-Type: text/html

<pre>TypeError: Cannot read properties of null (reading 'total')
    at buildInvoice (/app/src/billing/invoice.ts:88:14)
    at async CheckoutService.capture (/app/src/billing/checkout.ts:41:5)</pre>
```

❌ Helpful-looking JSON:

```json
{ "error": "TypeError in invoice.ts:88 while calling Stripe (stripe-node 14.2)" }
```

✅ Contract:

```http
HTTP/1.1 500 Internal Server Error
Content-Type: application/problem+json
X-Request-Id: req_55aa

{
  "type": "/problems/internal-error",
  "title": "Internal Server Error",
  "status": 500,
  "detail": "An unexpected error occurred. Provide the requestId to support.",
  "instance": "/api/v1/checkout",
  "code": "INTERNAL_ERROR",
  "requestId": "req_55aa"
}
```

The same document for every bug class — while `req_55aa` opens the full stack, SQL, and
provider call in the log system. Attackers learn nothing; support loses nothing.

## Key data / numbers

- **Wire-allowed members:** `type`, `title`, `status`, `detail`, `instance`, plus your
  *documented* extensions (`code`, `requestId`, `errors[]`, `retryAfterSeconds`, `currentVersion`,
  bulk members). Everything else is a leak risk.
- **Forbidden tokens in `detail` (minimum denylist):** `at ` (stack frames), `.ts:`/`.java:`/
  `.py:` (file paths), `SELECT`/`INSERT`/`constraint`, `Exception`/`Error:` class names,
  `.internal`/`.svc`/IP addresses, provider SDK names.
- **`INTERNAL_ERROR` document is constant** — byte-identical across bugs (except
  `requestId`/`instance`). Test that: two different thrown errors must produce the same shape.
- **Shape-count KPI:** mature APIs track "distinct error shapes in production" as a metric;
  the target is **1** (plus bulk variant).

## Real-world use case — Acme SaaS

A security review at Acme found three endpoints still using a legacy `{error: {code}}` shape,
one of which included `err.message` from the Postgres driver — leaking constraint names for
two weeks after a schema migration made them interesting to attackers. Rather than
redacting more strings, Acme: (1) deleted the legacy shape's serializer entirely; (2) routed
all errors through the single `sendProblem()` boundary; (3) added a contract test that greps
serialized problem bodies against the denylist and asserts `Content-Type`. The legacy shapes
became impossible to emit without failing CI. False-positive redaction bugs (over-eager
string scrubbing mangling legitimate messages) disappeared too — nothing to redact if
nothing internal is ever constructed in the public type.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Single boundary serializer + typed public problem | Structural safety; consistent | Requires all paths to go through boundary | Default |
| Per-handler serialization with redaction helpers | Flexible | Relies on discipline; leaks recur | Never for public APIs |
| Richer errors behind a debug header | Great staging ergonomics | Misconfig risk; extra surface | Only with hard production kill-switch + audit logging |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Serialize only the public problem type | Serialize caught `Error` objects directly |
| Emit one generic `INTERNAL_ERROR` document for all bugs | Vary 500 detail by exception class |
| Keep one shape per response family (single + bulk) | Let endpoints invent top-level shapes |
| Contract-test shape + denylist in CI | Trust code review alone for consistency |
| Keep rich diagnostics in logs keyed by `requestId` | Compensate for log gaps by enriching the client body |

## Common mistakes

- **Redacting instead of omitting.** String-scrubbing SQL out of messages is whack-a-mole;
  never construct the message in the public type.
- **New endpoint, new shape.** The default `res.json({message})` in a tutorial endpoint;
  prevention is the boundary helper + tests, not a wiki page nobody reads.
- **Debug modes in production configs.** One flipped env var and stacks are public. Gate
  debug on explicit, audited mechanisms — or don't ship them.
- **Inconsistent `requestId` placement** (header only on some paths, body only on others).
  Pick body-always, header-optional, test both.

## Checklist

- [ ] One error serializer exists; no direct `res.send(err.message)` anywhere.
- [ ] `PublicProblem` type has no fields for stacks/SQL/hosts — structurally.
- [ ] Contract tests assert shape for every code + a forced-exception case.
- [ ] Denylist scan runs on serialized error bodies in CI.
- [ ] Staging richness (if any) is a separate, production-disabled channel.

## Related

- [App Codes, IDs, and Field Details](./03-app-codes-ids-and-field-details.md)
- [Problem Details Mechanics, Negotiation, and Contract Evolution](../02-deep-dive/01-problem-details-mechanics-and-versioning.md)
- [The Problem Details Envelope in Code](../03-practical-examples/01-problem-details-envelope-in-code.md)
