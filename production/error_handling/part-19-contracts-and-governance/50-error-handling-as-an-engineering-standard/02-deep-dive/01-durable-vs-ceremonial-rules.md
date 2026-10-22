# Durable Rules, Exceptions, and Change Management

> Part XIX · Chapter 50 · Sections 50.9, 50.11–50.12 · _Estimated reading time: 18 min_
> **Prerequisite:** [Security Requirements and Exceptions to the Standard](../01-concepts/03-security-and-exceptions.md)

## In one sentence

A standard survives contact with a deadline only when every rule is **decidable in under a
minute**, every deviation is a **recorded exception with an expiry**, and every change is a
**versioned, announced, staged event**.

## Why this matters in production

Standards do not fail in the drafting meeting. They fail in the last week of the quarter, when
three teams are shipping and the fastest path to a merged pull request is to ignore the thing nobody
will notice until review. Three things compound: a **ceremonial rule** gets skipped because
objecting would need judgement the reviewer does not have; the skip is **not recorded**, so nobody
can tell whether the organisation has one exception or four hundred; and the rule is **still cited**
in the next incident review, where everybody moves on.

The cure is structural. A rule a tool can check cannot be skipped quietly, because the skip is a
red build. A rule a reviewer cannot decide in under a minute will be skipped, so it must not be a
rule. A deviation that is not written down will be invisible, so it must be *recorded* — and one
with no expiry is a permanent hole, so it must *expire*.

> Chapter 49 asks **which** compatibility rules earn enforcement. This one asks **how to write a
> rule so it can be enforced**, what to do when it cannot be met, and how to change the rule set.

## Core concept

### 50.9 — Three levels of a rule, and which ones survive

The deadline test is simple: **would a tired engineer under release pressure still be able to
comply, and would anyone be able to tell?**

| Level | Who decides | Can it be skipped? | Enforcement |
| ----- | ------------ | ------------------ | ----------- |
| **Mechanical** | A tool | No — the build fails | CI check |
| **Reviewable** | A reviewer | Yes, but visibly | Review checklist item |
| **Documentary** | Whoever reads it | Yes, invisibly | Documentation only |

A rule belongs at the lowest level it can survive at. If a rule cannot be a mechanical check, it
can still be reviewable — but only if a reviewer can decide it **in under a minute**. A rule that
needs system context is documentary: label it guidance rather than dress it up as a rule.

```text
❌ "Retries must be justified in the code."  → judgement on every PR; skipped silently
✅ "Every retry call site MUST pass a policy object from the shared registry;
    a literal attempt count greater than 5 is rejected by CI."  → decidable in seconds
```

The rewrite is not a weakening: it moves the decision from *the reviewer* to *the registry*,
where it is made once, in the open, and enforced everywhere at once. Every rule should also
carry the same six fields — id, normative statement, applies-to, checked-by, reason, exception.
The `reason` makes a rule durable (a rule nobody can name a failure for is folklore); the
`exception` tells a reviewer whether "no" is an answer.

### The rule budget

Rules are not free. Each costs a CI check, a review comment, or a line of documentation somebody
has to keep true, so **adding a rule requires demoting or removing one**. A new organisation starts
at **12 enforceable rules**; a mature one holds around **40**. Guidance (how to choose, trade-offs,
examples) is unlimited and is not a rule.

| Category | Target | Typical enforcement |
| -------- | ------ | ------------------- |
| Structural (shape, naming, registry, headers) | 15–25 | CI |
| Behavioural (retry, timeout, propagation, recovery) | 10–20 | CI where possible, review otherwise |
| Security floor | 10–15 | CI + security review on change |

### 50.11 — Exceptions: the recorded, owned, expiring deviation

An exception is **not** a waiver. A waiver says "this rule does not apply"; an exception says
"this rule does not apply *here*, for a stated reason, until a stated date". The expiry is the
difference. Without one, exceptions accumulate into a shadow standard nobody wrote and nobody
defends.

```yaml
# standards/error-handling/exceptions.yaml
exceptions:
  - id: EX-021
    rule: R-RETRY-1                       # retries only for codes marked retryable
    scope: ingest/webhook-ingest          # the webhook surface only
    justification: >
      Stripe redelivers any 5xx for up to 3 days. A 4xx for a transient dependency failure
      would drop a real payment event, so this surface must answer 5xx for non-retryable codes.
    compensating_controls:
      - a 5xx to Stripe is alerted on after 5 occurrences in 10 minutes
      - a DLQ holds the event for manual replay
    approved_by: platform-guild
    approved_on: 2026-04-02
    expires_on: 2026-10-02                 # review_on defaults to the expiry date
    status: active
```

The mechanism that keeps this honest is boring and mechanical — a status flag and a date:

```ts
export function isExceptionActive(ex: Exception, now = new Date()): boolean {
  return ex.status === "active" && new Date(ex.expires_on) > now;
}
```

A CI job runs that check daily. When an exception expires, the exemption lapses and the rule applies
again — the build breaks for the team that filed it, not for the standard's owner. That inversion
matters: **the cost of not renewing lands on whoever asked for the exception**.

**Not exceptable:** the security floor (disclosure, redaction, enumeration), idempotency and
no-duplicate-effects rules, and data-integrity rules — these encode incidents already paid for.
**Exceptable:** naming, code shape, registry membership, and default timeout and retry values.
Recovery posture (fail-open vs fail-closed) is exceptable only with a security review.

The dividing line is **safety vs shape**: safety rules encode lessons, shape rules encode current
preferences. Shape rules can bend; safety rules do not get waived.

### 50.12 — Avoiding rigidity

Rigidity is the failure mode of a standard that is doing its job too well.

| Form | Symptom | Cure |
| ---- | ------- | ---- |
| **Implementation lock-in** | Two of three languages cannot comply | Write rules about observable behaviour only |
| **Context blindness** | The same rule is right for a payment and for an analytics sink | Allow per-surface profiles and exceptions |
| **Rule accretion** | Eighty rules, four of them checked | Budget the rules; prune on a schedule |

The cure for all three is the same: **specify behaviour, not implementation**, and let context be
a *profile* rather than a rule exception.

| Surface profile | Retry budget | Deadline | Posture |
| --------------- | ------------ | -------- | ------- |
| `public-api` | 10% | 30 s timeout | fail closed |
| `webhook` | 0% (sender retries) | none | `5xx` on transient, fail closed |
| `background-job` | 25% | no wall clock | fail closed, DLQ required |
| `batch-analytics` | 25% | no wall clock | fail open, skip the batch |

A profile changes *parameters*, never the *guarantees*. The security floor applies to all of them
identically — which is what lets one standard serve a payment API and a nightly export.

## How it works (mechanics)

### The rule lifecycle

A rule moves through **proposed → reviewed → warning mode → enforced → retired**. The two gates
are the interesting ones: it cannot be reviewed without a named failure it prevents and an
exception answer, and it cannot be enforced until it has spent two releases in warning mode
without a failure being blamed on it. The enforcement mode of each rule (`off` / `warning` /
`error`) is stored next to it, with the version it was introduced in and the release in which it
is promoted.

### The change process

A standard is a **versioned artifact**. Changes to it are announced, dated, and sequenced — like
a public error contract (Chapter 49).

| Change class | Examples | Version bump | Announcement | Notice period |
| ------------ | -------- | ------------ | ------------ | ------------- |
| **Tightening** | A new mechanical rule, a stricter default value | MINOR | Changelog + email to affected teams | **2 releases** |
| **Removal** | A rule retired because it stopped paying for itself | MAJOR | Changelog + per-team notice | **90 days** |

The two-release window for tightening is the whole trick: a rule that appears as a build failure in
the same week it was proposed gets skipped, while one that arrives as a warning gets *adopted*.

### Retiring a rule

Rules die. A rule skipped on most pull requests for a year is noise; a rule skipped twice and
mattered twice is worth keeping. The procedure is evidence-based: count the skips over the last
**90 days**; if the skip rate is above **20%** and nobody can name a failure it prevented, demote
it to guidance; if the skip rate is low and it did prevent real failures, keep it and fix the
tooling instead. Record the retirement: what was retired, why, and what replaces it. ⚠️ **Hazard:**
demoting a rule because it is annoying is how you lose a real guarantee — the evidence bar is the
skip rate *plus* the absence of a named incident.

### Measuring a standard

Four numbers, reviewed quarterly, tell you whether the standard is working: the
**mechanically enforced share of rules** (healthy ≥ **60%**; below 40% it is just a document),
the **number of active exceptions** (healthy < **10 per 100 rules**), the **skip rate per rule**
(healthy < **20%**; a persistent outlier means the rule is wrong), and the **average exception
lifetime** (healthy < **180 days**).

A standard whose exception count rises every quarter is **telling you it is wrong in that area**:
amend the standard rather than approve more exceptions.

## Worked example — the quarter-end triage

Acme's standard was written in six weeks and was, at first, admired. Then Q4 arrived, and the
standards group triaged one quarter of pull requests:

| Rule (original wording) | Skip rate | A failure it prevents | Decision |
| ------------------------ | --------- | --------------------- | -------- |
| "Error handling should be consistent across services." | 64% | None named | **Delete.** Undecidable. |
| "Retries should be justified." | 38% | Inconsistent backoff | **Rewrite.** Became R-RETRY-3. |
| "Public error responses must not contain stack traces, SQL, or internal hostnames." | 0% | Credential and topology leakage | **Keep.** CI-enforced. |
| "All error messages must be under 120 characters." | 41% | None named | **Demote** to guidance. |
| "Every dependency call must have a timeout." | 12% | Hanging requests, pool exhaustion | **Keep.** CI-enforced; 3 legacy call sites grandfathered. |
| "Every error must carry a unique error id." | 3% | Duplicate log lines | **Delete.** The request id already covers it. |

Six rules in: **two rewritten, two deleted, two kept**. The two deleted rules had been quoted in two
incident reviews that year — and in both reviews the cause was something they could not catch.

The rewrite that mattered:

```text
BEFORE (ceremonial)
  "Retries should be justified."

AFTER (durable)
  R-RETRY-3  Every retry call site MUST use a policy from the shared registry, declaring
             maxAttempts, baseDelayMs, backoff, jitter, totalDeadlineMs, and the eligible
             error codes.
             Checked by: CI retry-policy-lint — rejects literal attempt counts > 5 and any
                          call site whose eligible list is empty.
             Reason:     three teams each implemented their own backoff, so a provider outage
                         produced three different retry shapes.
             Exception:  one active exception (EX-019, nightly batch importer).
```

The rule got **stricter** and cost **less** review time, because the decision moved out of the
reviewer and into a registry the reviewer can read.

## Key data / numbers

- **Rule budget:** ~**40 enforceable rules**; a new organisation starts at **12**. Structural
  15–25, behavioural 10–20, security floor 10–15, guidance unlimited.
- **Rule fields:** 6 (id · statement · applies-to · checked-by · reason · exception); adding a
  rule requires demoting or removing one.
- **Enforcement stages:** `off` → `warning` → `error`; a new rule runs in warning mode for
  **2 releases** before it can fail a build.
- **Exception record fields:** 8 required (rule · scope · justification · compensating controls
  · approver · approval date · review date · expiry date); default lifetime **180 days**, and
  < **10 active** exceptions per 100 rules — above 25, amend the standard.
- **Rule removal window:** **90 days** notice; tightening needs 2 releases; the standard is
  reviewed quarterly; rules are retired when the skip rate exceeds **20%** and no failure is
  named. **≥ 60%** of rules should be mechanically enforced.
- **Retry ceilings:** a retry policy MUST declare `maxAttempts` ≤ **5** and a
  `totalDeadlineMs` ≤ **30 s** for synchronous surfaces; the retry budget for a request is
  **≤ 10%** of its end-to-end timeout.
- **SLO and error budget:** a **99.9%** availability SLO on the public API yields **43.8 min**
  of error budget per month; a rule that consumes more than **10%** of the budget is a
  tightening that needs the SLO owner's sign-off.
- **Risk framing:** judge a rule like a failure mode — **risk = severity × likelihood** on a 1–5
  matrix (max **25**), and **RPN = severity × occurrence × detection**, each factor 1–10 (max
  **1000**); RPN ≥ **200** needs an owner, ≥ **400** blocks the release.
- **HTTP status codes the standard fixes:** `400` permanent client error · `409` conflict ·
  `422` unprocessable · `429` throttled (with `Retry-After`) · `503` transient, retryable ·
  `500` unexpected bug, never a planned response.
- **SQLSTATE codes the standard fixes:** class `08` connection (transient, retryable) · `23`
  constraint violation (permanent, never retryable) · `40` rollback and deadlock (retryable
  after rollback) · `42` syntax or access error (permanent).

## Real-world use case — `WebhookIngest`

Acme's standard had two rules the webhook surface could not obey: **R-RETRY-1** (retry only
codes marked retryable) and **R-RESP-1** (error responses use the standard problem body).
Stripe does not read error bodies; it reads the **status code**: `2xx` means done, `4xx` means
drop it forever, `5xx` means try again later for up to three days. So the webhook surface had to
answer `5xx` for transient dependency failures — which were not marked retryable, because the
marker describes *our* retry policy, not Stripe's.

Two teams then did what teams do: one filed a broad exception for the whole webhook service, and
the other stopped marking codes retryable on that surface — which quietly broke the internal retry
policy of the webhook *consumer* as well.

The standards group did the boring, correct thing. It **rejected the broad exception** (it covered
40 rules instead of one), **split R-RETRY-1** to name *which* layer owns the retry (the layer that
owns the idempotency key; a sender-driven retry is governed by the surface profile's status policy
instead), and **added a webhook surface profile** with its own status policy — transient dependency
failure ⇒ `503`, permanent failure ⇒ `400` — so Stripe's behaviour is defined rather than
accidental.

One narrow exception (`EX-021`) remained for the genuine deviation: the webhook surface may answer
`5xx` for a code that is not marked retryable, because Stripe's retry contract requires it. It had
compensating controls (alerting, DLQ, replay) and an expiry **180 days** out. Six months later it
was still active and still justified — so the standards group amended the standard instead, adding
a `sender-retryable` flag to the registry so the exception became unnecessary. That amendment was
the standard working: the rule was precise enough that the deviation was *visible*, *owned*, and
*resolvable*.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Encode as CI before writing the rule | Rules survive; no wasted debate | Slower to start | Long-lived standards |
| Profiles instead of exceptions | Context fits without breaking the rules | Two documents to keep in sync | Multi-surface orgs |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write rules a tool or a reviewer can decide in a minute | Write rules needing system context |
| Record the failure each rule prevents | Add a rule because an incident happened |
| Budget the rule count; prune on evidence | Grow the standard without pruning |
| Give every rule an owner and a `Reason` | Publish anonymous guidance |
| Narrow an exception to the smallest scope | File one exception for a whole service |
| Give every exception an expiry and a CI check | Renew exceptions silently |
| Prefer a surface profile to a rule change | Change a global rule to fit one caller |
| Promote a new rule through warning mode | Switch on a rule as an error on day one |

## Common mistakes

- **The Decorative Standard.** Sixty pages, four CI checks, quoted in two incident reviews it
  could not have prevented.

## Checklist

- [ ] Every rule has all six fields, including a named failure it prevents, and can be decided
  mechanically or by a reviewer in under a minute.
- [ ] The enforceable-rule count is inside the budget, and new rules run in warning mode for two
  releases before they fail a build.
- [ ] Every exception is narrow, owned, has compensating controls, and expires; expired
  exceptions break the build for the team that filed them.
- [ ] The standard is versioned, changelogged, and reviewed quarterly.

## Related

- [Security Requirements and Exceptions to the Standard](../01-concepts/03-security-and-exceptions.md)
- [Behavioral Standards: Propagation, Retry, Response, Recovery](../01-concepts/02-behavioral-standards.md)
- [Standards and ADR Templates](../03-practical-examples/01-standards-and-adr-templates.md)
- [Chapter 49 — Error Contract Design and Versioning](../../49-error-contract-design-and-versioning/README.md)
- Chapter 61 — Error-Handling Maturity Model (planned)
