# Balancing Reliability, Speed, and Complexity — and Choosing a Maturity Level

> Part I · Chapter 3 · Sections 3.10, 3.11, 3.12 · _Estimated reading time: 22 min_

## In one sentence

Every error-handling investment trades **reliability** against **build speed** and **complexity**,
so the correct maturity level is the **lowest one that covers your real risks** — reached by
adding safeguards one rung at a time, never by pre-building abstractions you have not yet earned.

## Why this matters in production

Error handling has a cost curve: the first 80% of reliability is cheap (explicit errors, one
boundary, no fake success); the last 20% is expensive and can itself introduce failure (a bespoke
retry framework, a saga orchestrator, a global god handler). Teams that over-invest slow delivery
and ship more bugs; teams that under-invest lose data and customers. The skill is knowing which
rung you are on and what the *next* one buys.

## Core concept

### 3.10 Balancing reliability, speed, and complexity

These three pull against each other:

```text
        reliability
           ▲
           │        ← over-engineering lives here
           │          (complex, slow, brittle)
           │
   "good      ●  the appropriate point
    enough"   │   (covers real risks, simple)
           │
           │        ← under-engineering lives here
           └──────────────►───── complexity ─────►
        ▲                    
        │  fast to build (but fragile)
        speed
```

You cannot maximize all three. You **minimize complexity subject to meeting the required
reliability**. Speed is the leftover.

Decision inputs:

| Input | Tilts toward more reliability | Tilts toward less |
| ----- | ----------------------------- | ----------------- |
| Cost of failure | Money, data, safety, breach | Cosmetic, internal |
| Frequency of failure | Common (network, provider) | Rare (never seen) |
| Detectability | Silent failures | Loud, obvious |
| Reversibility | Irreversible (payout) | Reversible (draft) |
| Team capability | Experienced, on-call | Tiny, learning |

### 3.11 Avoiding premature abstraction

The most common error-handling own-goal: building a **framework** before you have the repeating
problem. Symptoms:

- A `ErrorHandlerFactory` configured for cases that do not exist yet.
- A retry engine nobody fully understands.
- A universal base class every error must inherit, fighting the language.

The rule: **abstract on the third occurrence, not the first.** And only when the abstraction is
*smaller* than the duplication it removes (Chapter 53).

```ts
// ❌ Premature: a configurable retry framework for two call sites.
const retry = new RetryOrchestrator({ backoff: new ExponentialStrategy({ jitter: new FullJitter() }), ... });

// ✅ Appropriate: a small helper once the pattern repeats.
async function withRetry<T>(op: () => Promise<T>, opts: { attempts: number }): Promise<T> {
  for (let i = 1; ; i++) {
    try { return await op(); }
    catch (e) { if (i >= opts.attempts || !isRetryable(e)) throw e; await sleep(backoffMs(i)); }
  }
}
```

### 3.12 Defining an appropriate maturity level

Maturity is not "how advanced" but "how well-matched to risk." Levels (expanded in Chapter 61):

| Level | Name | You have | Appropriate when |
| ----- | ---- | -------- | ---------------- |
| 1 | Ad hoc | try/catch, inconsistent | Throwaway prototype |
| 2 | Conventions | explicit errors, one boundary, request IDs | MVP with users |
| 3 | Contracts | registry, envelope, stable codes | Growing startup |
| 4 | Resilience | retries, idempotency, degradation, DLQ | Scaled, high-availability |
| 5 | Reusable | shared library, cross-project policy | Multiple products/teams |

**Choose the lowest level whose obligations cover your profiles.** Financial and multi-tenant
profiles can force Level 4 even at a small stage.

## How it works (mechanics) — moving one rung

```text
  Level 1 ──► Level 2   trigger: first real users / first silent bug
  Level 2 ──► Level 3   trigger: clients need to act on errors; drift appears
  Level 3 ──► Level 4   trigger: dependency outages, money, scale
  Level 4 ──► Level 5   trigger: a second product re-implements the same policy
```

Each transition is triggered by **evidence** (an incident, a type of failure, a second consumer),
not by ambition. This keeps you on the appropriate point of the trade-off triangle.

## Worked example — right-sizing for Acme's stage

Acme is a **growing startup** (Level 2–3), multi-tenant (3.4), with background exports (3.9).

```text
  REJECTED (over-engineering): a full saga orchestrator with compensation for every write.
  REASON: Acme's failures are mostly transient; most operations are single-transaction.

  CHOSEN (appropriate):
    • Level 3: registry + one envelope              (clients act on codes)
    • isolation: per-tenant rate limits + scoped queries   (multi-tenant obligation)
    • bounded retries + DLQ for ExportJob            (background obligation)
    • idempotency for the Checkout charge only       (financial obligation where it exists)
```

The list is short and each item is justified by a risk — not by a framework's feature set.

## Key data / numbers

| Item | Value | Use |
| ---- | ----- | --- |
| First boundary | 1 per request + 1 per worker | Level 2 minimum |
| Retry attempts | 3–5, exp backoff + jitter | Level 4 |
| Error budget (99.9%) | ~43 min/month | Governs fail vs degrade |
| Abstract-on-third | rule of three | Avoid premature abstraction |
| Registry growth | one entry per code | Level 3 |
| DLQ max attempts | commonly 5 | Level 4 background |

## Real-world use case — Acme SaaS

Acme once built an elaborate "error governance framework" — plugin handlers, a policy DSL, and a
retry engine — before it had paying customers. It took six weeks, was used by two endpoints, and
was deleted when it slowed every PR. They replaced it with a `DomainError` base, one registry file,
and a 20-line `withRetry`. Same reliability for the cases that existed, far less complexity. The
framework had been an attempt to skip rungs; the appropriate point was lower.

## Trade-offs

| Choice | Reliability | Speed | Complexity |
| ------ | ----------- | ----- | ---------- |
| Ad hoc | Low | Highest | Lowest |
| Conventions | Medium | High | Low |
| Contracts | High | Medium | Medium |
| Resilience | Very high | Low | High |
| Reusable library | Very high | Low (initial) | High (amortized) |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Minimize complexity for required reliability | Maximize reliability regardless of cost |
| Abstract on the third occurrence | Build a framework on the first |
| Move a rung on evidence | Move a rung on ambition |
| Let profiles raise the floor | Let stage cap requirements |

## Common mistakes

- **Framework-first** — abstraction before repetition.
- **Skipping rungs** — resilience machinery without Level-2 basics.
- **Choosing by aspiration** — "we should be Level 5."
- **Confusing maturity with quantity** of error code.

## Checklist

- [ ] Can you name your current maturity level and justify it?
- [ ] Does every safeguard map to a named risk?
- [ ] Have you abstracted only after the third repetition?
- [ ] Do your profiles force a level above your stage baseline?
- [ ] Is your next rung triggered by evidence, not ambition?

## Related

- [Requirements by Product Stage](./01-requirements-by-product-stage.md)
- [Choosing a Maturity Level Without Over-Engineering — Deep Dive](../02-deep-dive/02-choosing-a-maturity-level-without-over-engineering.md)
- [Chapter 61 — Error-Handling Maturity Model](../../../part-24-repeatable-blueprint/61-error-handling-maturity-model/README.md)
- [Chapter 53 — Reducing Error-Handling Complexity](../../../part-21-maintainability/53-reducing-error-handling-complexity/README.md)
