# Choosing a Maturity Level Without Over-Engineering

> Part I · Chapter 3 · Sections 3.10, 3.11, 3.12 · _Estimated reading time: 22 min_

## In one sentence

You reach the right maturity by **adding one safeguard at a time, driven by a concrete failure**,
and by preferring the smallest mechanism that removes a real risk over the most complete mechanism
you can imagine.

## Why this matters in production

Over-engineering is not a neutral mistake: a bespoke error framework adds **new failure modes,
onboarding cost, and upgrade burden** while often covering risks you do not have. Under-engineering
is equally costly: an unscoped retry, a missing idempotency key, a swallowed error that corrupts
data. The discipline of this deep dive is choosing the rung by *evidence* and *risk*, and moving
one rung per trigger.

## Core concept — the maturity ladder, in full

| Level | Name | Evidence you are here | Evidence it is time to move up |
| ----- | ---- | --------------------- | ------------------------------ |
| 1 | **Ad hoc** | Different handling per file; errors often swallowed | First real users; a silent bug shipped |
| 2 | **Conventions** | Explicit errors, one boundary, request IDs | Clients need to act on errors; drift appears |
| 3 | **Contracts** | Registry, envelope, stable codes | Dependency outages or money/scale arrive |
| 4 | **Resilience** | Retries, idempotency, degradation, DLQ | A second product re-implements the policy |
| 5 | **Reusable** | Shared library + docs + cross-project policy | — (stay here; evolve, don't redesign) |

Your **level = the lowest level whose obligations cover your profiles** (Chapter 3 concepts). A small
multi-tenant financial product can sit at Level 4 while a large internal tool sits at Level 2.

## How it works (mechanics) — the anti-over-engineering loop

```text
  observe a real failure
        │
        ▼
  name the risk it represents
        │
        ▼
  find the SMALLEST mechanism that removes the risk
        │
        ▼
  apply it at the owning layer
        │
        ▼
  add a regression test
        │
        ▼
  stop  ← do NOT generalize further until the pattern repeats
```

The critical step is **stop**. Most over-engineering happens because the loop continues past the
point where the risk was removed.

## The over-engineering smell test

| Smell | Diagnosis | Simpler alternative |
| ----- | --------- | ------------------- |
| A "framework" used by 1–2 call sites | Premature abstraction | A function |
| Config for cases that never occur | Speculative | Hard-code the known cases |
| A base class every error must inherit | Framework gravity | A record/struct + codes |
| A retry engine with 3 strategies for 1 dependency | Overkill | One `withRetry` |
| A saga orchestrator for single-transaction writes | Overkill | A DB transaction |
| A plugin system for error handlers | Overkill | A registry table |
| A "policy DSL" no one reads | Abstraction cost > value | A documented table |

> **Rule of three.** Abstract on the third occurrence, not the first. If the abstraction is not
> *smaller* than the duplication it removes, do not build it.

## Edge cases — when more maturity is genuinely warranted

| Situation | Justification to move up early |
| --------- | ------------------------------ |
| Payments/PHI/money | Irreversible; financial profile forces Level 4 |
| Regulatory audit | Codes and trails are contractually required |
| Multi-tenant with enterprise clients | Isolation + SLA obligations |
| Public API with third parties | Versioned contracts before launch |
| High-frequency provider failures | Retries/idempotency earn their keep |

Note the pattern: move up early because of **risk profile**, never because of **ambition**.

## Worked example — right-sizing a retry layer

A service calls one flaky dependency. Three candidate designs:

```ts
// Level 1 — none (fragment): ad hoc, inconsistent
try { await dep.call(); } catch { /* ignore */ }

// Level 2–3 — appropriate: a small helper at the adapter
async function withRetry<T>(op: () => Promise<T>, attempts = 4): Promise<T> {
  let last: unknown;
  for (let i = 1; i <= attempts; i++) {
    try { return await op(); }
    catch (e) { last = e; if (!isRetryable(e)) throw e; await sleep(backoffWithJitter(i)); }
  }
  throw last; // preserve final failure (Chapter 27)
}

// Level 5 — overkill for ONE dependency, right if MANY share the policy
// class RetryOrchestrator { /* strategies, jitter policies, budgets, metrics hooks, ... */ }
```

The middle option removes the real risk (transient failure) with a mechanism smaller than the
problem's complexity budget. The third becomes worth it only when many call sites share the policy.

## Key data / numbers

| Item | Value | Note |
| ---- | ----- | ---- |
| Rule of three | abstract on 3rd occurrence | Avoids premature abstraction |
| Retry attempts | 3–5, exp backoff + jitter | Level 4 default |
| Error budget (99.9%) | ~43 min/month | Governs maturity needs |
| Timeout | below caller's deadline | Cheap, Level 2+ |
| Abstraction rule | smaller than duplication? | If no, don't build |
| Level-2 minimum | 1 boundary + request IDs | Nearly free |

## Real-world use case — Acme SaaS

After deleting its six-week "error governance framework," Acme adopted an explicit rule: **a new
error-handling abstraction must be smaller than the duplication it replaces, and must be justified
by two existing call sites.** Over the next quarter they added exactly three things — a `DomainError`
base, a registry file, and `withRetry` — each time a concrete failure demanded it. Velocity rose
(fewer abstractions to satisfy), and incidents did not. The maturity ladder, climbed by evidence,
delivered more reliability than the framework ever had.

## Trade-offs

| Approach | Reliability | Velocity | Maintenance | Choose when |
| -------- | ----------- | -------- | ----------- | ----------- |
| Add on evidence | Right-sized | High | Low | Default |
| Pre-build framework | Possibly high | Low | High | Never, before repetition |
| Never add | Low | Highest | Lowest | Prototypes only |
| Buy/adopt library | High | Medium | External | Level 5, proven need |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Move one rung per concrete trigger | Skip rungs to look mature |
| Pick the smallest sufficient mechanism | Build for imagined cases |
| Abstract on the third occurrence | Abstract on the first |
| Justify abstractions by call sites | Justify by elegance |
| Keep the loop's "stop" step | Generalize forever |

## Common mistakes

- **Speculative generality** — config and hooks for cases that never occur.
- **Framework gravity** — a base class everything must inherit.
- **Maturity theater** — adopting Level-5 vocabulary without Level-2 basics.
- **Never adding** — calling it "avoiding over-engineering" while data is lost.

## Checklist

- [ ] Did a real failure trigger each safeguard?
- [ ] Is every abstraction smaller than the duplication it removes?
- [ ] Have you abstracted only after the third occurrence?
- [ ] Does each safeguard sit at the layer that owns the decision?
- [ ] Did you stop once the risk was removed?

## Related

- [Balancing and Choosing Your Maturity Level](../01-concepts/03-balancing-and-choosing-your-maturity-level.md)
- [Chapter 61 — Error-Handling Maturity Model](../../../part-24-repeatable-blueprint/61-error-handling-maturity-model/README.md)
- [Chapter 54 — Reusable Error-Handling Infrastructure](../../../part-21-maintainability/54-reusable-error-handling-infrastructure/README.md)
- [Chapter 53 — Reducing Error-Handling Complexity](../../../part-21-maintainability/53-reducing-error-handling-complexity/README.md)
