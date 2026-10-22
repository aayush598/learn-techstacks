# Standards and ADR Templates

> Part XIX · Chapter 50 · Sections 50.1–50.8, 50.10 · _Estimated reading time: 26 min_
> **Prerequisite:** [What an Error-Handling Standard Contains](../01-concepts/01-what-a-standard-contains.md)

## In one sentence

A working standard is a **short list of numbered rules with a mechanical check for each**, and the
decisions it encodes are recorded as **ADRs that say what the rule protects and what it does not
cover**.

## Why this matters in production

Most teams do not lack error-handling conventions — they lack a *written, shared, enforceable* one.
The conventions live in the head of the person who wrote the first service, in a Slack thread from
two years ago, and in a mixin nobody remembers. New services then invent their own names and
shapes, and when an incident happens there is no document to point at, so the fix stays local and
the lesson is lost.

The opposite failure is a 200-page standard, forcing a choice between uncheckable prose and a rule
set that fits on one page. This file is the **workable middle** — an excerpt you can copy, and the
ADR template that keeps it honest.

## Core concept

### The shape of a standard excerpt

A standard is not a document to be admired; it is a **lookup table applied under time pressure**.
So each rule is one line of statement, one line of check, and one line of reason. Everything
else — examples, trade-offs, background — lives in guidance *around* the rules.

```text
R-STRUCT-3  Every error type MUST live in the shared error module for its service.
            Checked by: CI import-lint — rejects an error class declared outside
                         src/errors/.
            Reason:     error types scattered across a service are duplicated, renamed,
                        and never found by search.
```

Three properties make that work:

| Property | Why it matters |
| -------- | -------------- |
| **Numbered** | A PR comment says "violates R-STRUCT-3", not "this is wrong somehow" |
| **Checked by** | The decision is already made, so the reviewer only applies it |
| **Reason** | A rule nobody can justify is deleted at the next review |

### 50.1–50.3 — Structure, naming, and code conventions

The structural and naming rules exist to make errors **findable**. Here is the excerpt Acme
shipped first, because it is the part that changes least:

```text
R-NAME-1   Error codes MUST be SCREAMING_SNAKE_CASE, with no HTTP status, class name, or suffix.
R-NAME-2   A code MUST be globally unique and registered in the error registry before it ships.
R-NAME-3   A code MUST NOT be reused; a retired code MUST be marked with its date and successor.
R-NAME-4   Error names MUST describe the condition, not the mechanism:
            USER_NOT_FOUND, not SELECT_USER_RETURNED_NO_ROWS.
R-NAME-5   An expected, business-relevant condition MUST have its own code, not an internal error.
R-NAME-6   A code MUST NOT encode severity; severity belongs to the context, not the condition.

R-STRUCT-1 Every service MUST expose a single error module; no second one may be created.
R-STRUCT-2 Every error MUST carry: code, message, retryable (boolean), and details (object).
R-STRUCT-3 Every error type MUST live in the shared error module for its service.
R-STRUCT-4 Errors MUST NOT carry stack traces, SQL text, file paths, or hostnames across a
            process boundary.
R-STRUCT-5 An error MUST NOT be built from a dynamic string; the message MUST come from a
            code catalog or a template.
```

⚠️ **Hazard.** R-NAME-3 (no reuse) is the rule teams fight hardest, because "the old code still
works for our mobile client". It is still right: a retired code that is reused makes the error
history untrustworthy, and an error log becomes unsearchable.

### 50.4–50.7 — Behavioral conventions

Propagation, retry, response, and recovery are where the standards actually pay for themselves,
because these are the rules that decide whether a dependency outage becomes an outage.

```text
R-PROP-1   A service MUST NOT swallow an error; a deliberate ignore MUST be logged.
R-PROP-2   A service MUST translate upstream errors at its boundary, never re-export them.
R-PROP-3   A translated error MUST carry the originating error as its cause.
R-PROP-4   A retried operation MUST be idempotent or MUST carry an idempotency key.
R-PROP-5   A service MUST NOT retry a request it cannot identify.
R-PROP-6   A partial failure MUST be reported as a partial failure, never as success.

R-RETRY-1  A retry MUST only be attempted for codes explicitly marked retryable.
R-RETRY-2  Every retry call site MUST use a policy from the shared registry, declaring
            maxAttempts, baseDelayMs, backoff, jitter, totalDeadlineMs, and eligible codes.
R-RETRY-3  A literal attempt count greater than 5 MUST be rejected by CI.
R-RETRY-4  Every retry MUST use exponential backoff with jitter.
R-RETRY-5  A retry MUST NOT be attempted for a non-idempotent operation without a key.
R-RETRY-6  Retries MUST NOT consume more than 10% of the request deadline.

R-RESP-1   An error response MUST use the standard problem body: type, title, status, code,
            detail, requestId.
R-RESP-2   An error response MUST NOT contain a stack trace, SQL text, or a hostname.
R-RESP-3   A response MUST NOT distinguish "not found" from "not visible to you".
R-RESP-4   A 4xx MUST be actionable by the caller; a 5xx MUST mean "may be retried".
R-RESP-5   A throttled response MUST be 429 and MUST carry Retry-After.
R-RESP-6   A validation failure MUST return field-level details, not the first error only.
R-RESP-7   An error response MUST carry the request id that appears in the logs.
R-RESP-8   An error response MUST NOT be cached as a success by intermediaries.

R-RECOV-1  Every operation MUST declare a recovery posture: fail-closed or fail-open.
R-RECOV-2  A fail-closed dependency MUST time out before the caller's own budget.
R-RECOV-3  A fail-open dependency MUST have an observable fallback and MUST be logged.
R-RECOV-4  A compensating action MUST be idempotent.
R-RECOV-5  A degraded mode MUST be visible to the caller, not just to the operator.
R-RECOV-6  A recovery action MUST NOT exceed the declared retry ceiling.
```

The recovery posture is the rule teams forget most often, so it is worth stating plainly:

```text
FAIL-CLOSED  the caller must not proceed without the dependency (payments, auth, balance)
             → timeout, 503, no partial state
FAIL-OPEN   the caller may proceed with degraded data (analytics, exports)
             → fallback value, log, expose a degraded flag
```

### 50.8 — The security floor

Security rules are the **non-negotiable tier**: they are not exceptable, and changing them
requires a security review.

```text
R-SEC-1     A public error response MUST NOT contain personal data, credentials, tokens, or
             internal identifiers.
R-SEC-2     An error message MUST NOT reveal whether an account exists (enumeration
             resistance).
R-SEC-3     A log line MUST NOT contain a secret, a full card number, or an access token.
R-SEC-4     An error MUST NOT carry the stack trace of an internal frame to a caller.
R-SEC-5     A user-supplied value MUST NOT be echoed into an error message without
             neutralisation.
R-SEC-6     A security-relevant failure MUST raise a security event, not only an error log.
R-SEC-7     An authentication failure MUST NOT be distinguishable from an authorisation
             failure in the response body.
R-SEC-8     An error registry entry MUST NOT contain customer data or examples taken from
             production.
```

### 50.10 — Decisions as records

A standard is a **sequence of decisions**. When someone asks "why does our API return `409`
instead of `422`?", the answer must not be "because of a meeting". An ADR (architecture decision
record) is the smallest container that answers it.

The template Acme uses for every rule or rule change:

```markdown
# ADR-0xx — <decision in one line>

Status:   proposed | accepted | superseded by ADR-0yy
Date:     YYYY-MM-DD
Scope:    R-XXX-N | standard v1.2 | service X
Deciders: <roles, not names of one person>

## Context
What forced the decision: the incident, the new constraint, the migration. Factual, no narrative.

## Decision
The rule, in normative language, with the exact check that enforces it.

## Alternatives considered
Each with one line on why it was rejected.

## Consequences
What becomes easier, what becomes harder, what the team must now do.

## Evidence
The number that justifies it: skip rate, incident count, RPN, latency budget.

## Revisit when
A measurable trigger, not "if it becomes a problem".
```

Worked ADR, filled in:

```markdown
# ADR-031 — Webhook surfaces answer 5xx for transient dependency failures

Status:   accepted
Date:     2026-04-02
Scope:    R-RETRY-1, webhook surface profile

## Context
Stripe redelivers any 5xx for up to 3 days. Returning 4xx for a transient dependency failure
drops a real payment event permanently, but our internal retry marker says "not retryable".

## Decision
A sender-driven retry is governed by the surface profile's status policy, not by the internal
retry marker. Webhook surfaces answer 503 for transient dependency failure and 400 for a permanent
one. The registry gains a sender-retryable flag.

## Alternatives considered
- Mark all dependency errors retryable — rejected: breaks the internal retry policy.
- File a permanent exception — rejected: an exception that never expires is a hole.

## Consequences
The webhook surface can answer 5xx for non-retryable codes, exactly what R-RETRY-1 forbids, so
the rule is amended instead. Webhook handlers must be idempotent.

## Evidence
Duplicate webhook delivery was 0.4% of events; 37 payment events were lost in 2025 Q4.

## Revisit when
The retry marker and the sender contract can be reconciled in one registry field.
```

## How it works (mechanics)

Publishing a standard is a four-step loop, and it repeats quarterly:

1. **Draft the rule** with its check. If you cannot write the check, it is guidance.
2. **Run it in warning mode** for two releases and count the violations.
3. **Fix or except** each violation. The exception file is the same one used by CI.
4. **Promote to error**, and record the decision as an ADR.

Step 2 is where most standards die, and it is the step that saves them: the warning-mode
violation count tells you whether the rule is achievable *before* you make it binding.

## Key data / numbers

- **Standard size:** **30–50 numbered rules** is the working range; a new organisation starts at
  **12–15**. Guidance is unlimited.
- **Rule fields:** 6 — id · normative statement · applies-to · checked-by · reason · exception.
- **Normative keywords:** MUST / MUST NOT (binding) · SHOULD / SHOULD NOT (expected, deviation
  needs a reason) · MAY (optional).
- **Warning mode:** **2 releases** before a rule can fail a build; **90 days** notice before a
  rule is removed.
- **Retry ceilings:** `maxAttempts` ≤ **5**, `totalDeadlineMs` ≤ **30 s** on a synchronous surface,
  and the retry budget ≤ **10%** of the request deadline.
- **Timeout rule:** the dependency timeout MUST be **shorter** than the caller's remaining
  budget; a typical chain is 30 s total → 10 s → 3 s → 1 s.
- **SLO and error budget:** a **99.9%** availability SLO allows **43.8 min** of downtime per
  month; a rule that breaks more than **10%** of that budget needs the SLO owner's sign-off.
- **HTTP status codes the standard fixes:** `400` permanent client error · `401` unauthenticated
  · `403` forbidden · `404` absent *or* invisible · `409` conflict · `422` semantically invalid
  · `429` throttled (with `Retry-After`) · `500` unexpected bug · `503` transient, retryable.
- **SQLSTATE classes the standard fixes:** `08` connection (transient, retryable) · `23`
  constraint violation (permanent) · `40` rollback and deadlock, e.g. `40001`
  serialization_failure (retryable after rollback) · `42` syntax or access error (permanent).
- **Risk framing:** a rule's priority is scored like a failure mode — **risk = severity × likelihood**
  on a 1–5 matrix (max **25**) and **RPN = severity × occurrence × detection**, each factor 1–10
  (max **1000**); RPN ≥ **200** needs an owner, ≥ **400** blocks the release.

## Real-world use case — Acme SaaS

Acme had 40 services, three languages, and no shared error conventions. Duplicate codes numbered
61; four teams had four different retry policies; and in Q1 a support agent emailed a customer a
raw error message containing an internal hostname and a customer id.

The rollout was deliberately small. In the first quarter the standards group wrote **12 rules** —
naming, structure, response format, and the security floor — and shipped them as a CI package each
service adopted voluntarily. Warning mode ran for two releases; the counts came back: **78%** of
violations were three missing imports, so the tooling was fixed instead of the rule.

The second quarter added the behavioural rules: retry, timeout, propagation, recovery. The retry
rule needed the most work, because two services had genuinely different needs — a payment service
that must never retry a charge, and a pricing service that should always retry. The solution was
not an exception each; it was one **retry registry** with named policies and one rule pointing at
it.

By the third quarter the exception register held **9** entries, all with expiry dates, and the
duplicate-code count had fallen from 61 to **3**. The security floor was never negotiable: the
rule blocking raw internal details in a response body caught **11** leaks in its first warning
week, and each became a ticket with a named owner.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Few rules, all mechanical | Unambiguous; cheap to enforce | Leaves some judgement to reviewers | Every organisation |
| Many rules, mostly reviewable | Captures nuance | Skip rate climbs; reviews slow down | Tiny teams with one reviewer |
| One standard for every service | Consistent; easy to search | Some services need other shapes | Start here; add profiles later |
| Rules in a shared package | One update reaches everyone | Version conflicts; slower changes | Multi-language orgs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write the check before the rule | Write a rule and hope someone checks it |
| Give every rule a number and a reason | Publish anonymous guidance as a rule |
| Run new rules in warning mode first | Switch on a rule as an error on day one |
| Express service differences as profiles | Change a global rule to fit one caller |
| Record decisions as ADRs | Let a meeting be the only record |
| Make the security floor non-exceptable | Let a team waive a security rule locally |
| Version the standard and publish a changelog | Edit the standard silently in a pull request |
| Retire rules that stop paying for themselves | Let the rule count grow forever |

## Common mistakes

- **The Wall of Prose.** A 200-page standard with no rule numbers and no checks; nobody can
  cite it, so nobody applies it.
- **The Unnumbered Rule.** "Errors must be handled consistently" — without an id it cannot appear
  in a review comment, a violation report, or an exception.
- **The Exception Ratchet.** Every quarter adds exceptions and none close, because exceptions
  have no expiry.
- **The Silent Edit.** The standard changes in a pull request between two services, and only one
  of them learns about it.

## Checklist

- [ ] Every rule has an id, a normative statement, a check, a reason, and an exception answer; the
  security floor is non-exceptable and needs a security review to change.
- [ ] New rules run in warning mode for two releases before they can fail a build.
- [ ] Every exception has an owner, compensating controls, and an expiry date.
- [ ] HTTP status codes and SQLSTATE classes are fixed by the standard, not by each service.
- [ ] Every decision that changed a rule has an ADR, and the standard is versioned, changelogged,
  and reviewed quarterly.

## Related

- [What an Error-Handling Standard Contains](../01-concepts/01-what-a-standard-contains.md)
- [Behavioral Standards: Propagation, Retry, Response, Recovery](../01-concepts/02-behavioral-standards.md)
- [Security Requirements and Exceptions to the Standard](../01-concepts/03-security-and-exceptions.md)
- [Durable Rules, Exceptions, and Change Management](../02-deep-dive/01-durable-vs-ceremonial-rules.md)
- [Chapter 49 — Error Contract Design and Versioning](../../49-error-contract-design-and-versioning/README.md)
