# Durable vs Ceremonial Rules

> Part XIX · Chapter 49 · Sections 49.6–49.7 · _Estimated reading time: 16 min_
> **Prerequisite:** [Contract Surfaces and Stability Guarantees](../01-concepts/01-contract-surfaces-and-stability.md)

## In one sentence

Not every compatibility rule deserves to exist: a rule is **durable** only if it is
**observable, mechanically checkable, and tied to a real blast radius** — and rules that fail
that test must be deleted, or they become ceremony that everyone ignores.

## Why this matters in production

Standards accumulate. Someone adds "never reuse a code", someone else adds "never change a
status code", someone adds "always include a request id". Three years later the standard has
forty rules, half of which are unverifiable, a quarter of which are violated constantly, and a
few of which are actively harmful because they push teams to work around the rule rather than
satisfy it.

The symptom is familiar: the standard exists, review comments reference it, nobody can point to
a tool that checks it, and the exception count grows because the rule is unworkable.

The cure is not more rules. It is a **filter**.

## The three-question test

Before a rule enters the standard, it must pass all three:

| Question | If no |
| -------- | ----- |
| **Is it observable?** Can a tool or a metric tell whether it is being followed? | It is a preference, not a rule. Move it to guidance. |
| **Is it checkable at review time?** Can a reviewer decide compliance in under a minute? | It needs automation first, or it becomes a debate. |
| **Does it have a blast radius?** Is there a concrete failure it prevents? | It is folklore. Delete it. |

A fourth, softer question keeps the list short: **would this rule still make sense in three
years?** Rules about tooling and syntax fail this; rules about semantics survive.

## Enforcement matrix

The point of the test is to decide *how* a rule is enforced, not merely whether it exists.

| Rule | Observable | Mechanism | Enforcement cost |
| ---- | ---------- | --------- | ---------------- |
| Every produced code is registered | Yes | CI: scan code literals vs registry | Low |
| Codes are unique across the org | Yes | CI: registry uniqueness test | Low |
| No consumer branches on message text | Yes | CI: lint on `detail`/`title` comparisons | Low |
| Unknown codes have a default branch | Yes | CI: lint (exhaustive switch detection) | Low |
| Public codes are never removed without a window | Yes | CI: registry `removedIn` requires an approved ADR | Low |
| Deprecation windows are respected | Yes | CI: date + telemetry check | Medium |
| New codes carry a `type` URI and a `clientAction` | Yes | CI: registry schema test | Low |
| Public error responses carry no stack traces | Yes | CI/contract test on response bodies | Low |
| Error messages are user-appropriate | Partly | Review + user-facing checklist | Medium |
| Retry decisions are justified per dependency | No | Review, architecture discussion | High |
| A code should describe behaviour, not mechanism | No | Review, naming conventions | Medium |

Notice the pattern: **the rules that can be automated are all structural**. Semantic quality
rules stay in review, because pretending otherwise produces false confidence.

## Durable rules vs ceremonial rules

| Durable (keep and enforce) | Ceremonial (delete or demote) |
| -------------------------- | ----------------------------- |
| "Every produced code exists in the registry" | "Never change an HTTP status code" (use a new code instead — that *is* the rule) |
| "Codes are append-only within a contract version" | "Every error must have a unique id" (the request id already provides this) |
| "Consumers tolerate unknown codes" | "All error messages must be under 120 characters" |
| "Public responses never include stack traces or SQL" | "Always use the exact phrasing in this document" |
| "Public codes map to a documented `type` URI" | "Error handling must be fully documented" (unverifiable) |
| "Deprecation requires a changelog entry and a sunset date" | "Retries must be justified in the code" (belongs in design review) |

The right-hand column is not nonsense — it is **the wrong shape**. Each entry is either a
guideline (useful, but guidance) or a restatement of a rule that already exists in enforceable
form.

## The rules budget

A standard with more than **~40 enforceable rules** stops being usable. Track the budget
deliberately:

```text
Adding a rule requires removing or demoting one.
```

That single rule is what keeps a standard alive. It forces every proposal to answer "what does
this displace?", which is the right question.

A practical split:

| Category | Target count | Enforcement |
| -------- | ------------ | ----------- |
| Structural (registry, shape, headers) | 15–25 | CI |
| Semantic (meaning, naming, retry posture) | 10–20 | Review |
| Guidance (how to choose, trade-offs) | unlimited | Documentation |

## Retiring a rule

Rules expire. A rule that has been violated on every PR for a year is noise; a rule that has
been violated once and mattered is worth keeping.

The retirement procedure:

```text
1. Count violations over the last 90 days (from review comments or CI skips).
2. If a rule is skipped >20% of the time and nobody can name a failure it prevented → demote
   it to guidance.
3. If a rule is skipped rarely but the failures it prevents are severe → keep it, and fix the
   tooling so it stops being skipped.
4. Record the decision (what was retired, why, what replaced it).
```

> ⚠️ **Hazard.** Demoting a rule because it is "annoying" is how you lose a real guarantee. Use
> evidence: the rule's skip rate, and whether a real incident was caused by violating it.

## Worked example — pruning Acme's error-handling standard

Acme's standard had 63 rules. A review of two quarters of pull requests found:

| Rule | Skip rate | Failure it prevents | Decision |
| ---- | --------- | ------------------- | -------- |
| "Every error code must be uppercase snake case" | 2% | Formatting drift | Keep — CI-enforced |
| "All error messages must be ≤120 characters" | 41% | None that anyone could name | **Demote** to guidance |
| "Public error responses must not include a stack trace" | 0% | Credential and internals leakage | Keep — CI-enforced |
| "Every dependency error must be documented in the catalogue" | 55% | Stale docs | **Replace** with a CI check that the catalogue is generated from the registry |
| "Retry logic must be implemented with the shared retry helper" | 18% | Inconsistent backoff | Keep — CI-enforced, with a grandfathering list |

Net result: **63 rules → 38**, of which 24 are mechanically enforced. Two engineers had been
skipping the length rule for a year because it was unworkable; nobody had noticed, because the
skip did not show up anywhere except a reviewer's memory.

## Key data / numbers

- **Rule budget:** ~**40 enforceable rules** maximum for an org-wide standard; 15–25 structural,
  10–20 semantic.
- **Rule addition rule:** adding a rule requires demoting or removing one.
- **Durability test:** observable + checkable-at-review + tied to a blast radius (+ survives
  three years).
- **Skip-rate threshold for demotion:** >**20%** of pull requests skipped the rule over **90
  days**, with no named failure it prevented.
- **Mechanically enforced target:** ≥ **60%** of enforceable rules should have a CI check; a
  standard where most rules are review-only is a document, not a standard.
- **Exception register:** every exception has an owner, a justification, and a **review date**;
  expired exceptions are re-justified or removed.

## Real-world use case — AgentRun

Acme's `AgentRun` feature adds LLM provider calls, and the platform team's error-handling
standard had to cover them. The draft had 19 new rules in a week, including:

- "Provider errors must preserve the original provider status code." (Unobservable as a
  contract: the provider is a third party whose codes change.)
- "Every agent error message must mention the model name." (Uncheckable in review, and it
  leaks configuration.)
- "The `detail` field must never exceed 200 characters." (Checkable — and enforced by a
  truncator in the serializer.)

Applying the three-question test kept two rules and dropped seventeen. What survived was the
one that mattered: **"Provider-specific codes must be mapped to Acme codes before crossing the
boundary; the provider's status code goes in metadata, never in the public `code` field."**

That rule prevented a real incident three months later when the provider renamed one of its
error strings. Because the mapping was mandatory, Acme's public contract never mentioned the
provider's vocabulary, and the change was invisible to Acme's clients. The nineteen rules that
were deleted had prevented nothing.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Few enforceable rules, rest as guidance | Usable; teams actually follow it | Some real guarantees left unenforced | Mature orgs |
| Many rules, mostly review-enforced | Looks thorough | Skip rate climbs; reviews slow down | Early, small teams |
| Rule-per-incident | Captures every lesson | Rules conflict; standard becomes a maze | Never, without pruning |
| Tooling-first (encode as CI before writing) | Rules survive | Slower to start | Long-lived standards |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Apply the three-question test to every proposed rule | Add a rule because an incident happened |
| Keep an enforceable-rule budget | Grow the standard without pruning |
| Demote rules with a high skip rate | Keep a rule everyone skips |
| Fix tooling when a valuable rule is skipped | Demote a valuable rule because it is annoying |
| Record retirements with their reason | Delete rules silently |
| Give every exception an owner and a review date | Let exceptions accumulate forever |

## Common mistakes

- **The incident-itis rule.** A new rule per outage, none of them checked.
- **The unskip-able rule.** Nobody can tell whether it is followed, so nobody knows.
- **The folklore rule.** "We always…" with no mechanism and no example.
- **The exception graveyard.** Forty approved exceptions, none with a review date.
- **The standard as a document.** Eighty rules, four CI checks.

## Checklist

- [ ] Every rule has a mechanism: CI check, review checklist item, or telemetry.
- [ ] Every rule has a named failure it prevents.
- [ ] The enforceable-rule count stays under the budget.
- [ ] Rules with a high skip rate are demoted or replaced with tooling.
- [ ] Retired rules are recorded with their reason.
- [ ] Every exception has an owner, a justification, and a review date.

## Related

- [Contract Surfaces and Stability Guarantees](../01-concepts/01-contract-surfaces-and-stability.md)
- [Ownership, Documentation, and Message Independence](../01-concepts/03-ownership-documentation-and-message-independence.md)
- [Writing Rules That Survive Review](./01-writing-rules-that-survive-review.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
