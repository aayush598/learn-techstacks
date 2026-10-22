# Chapter 3 — Do's and Don'ts

> Part I · Chapter 3 · Rules, anti-patterns, and the chapter checklist.

## The golden rules

1. **Derive requirements** from stage + architecture + risk; never copy them from a blog.
2. **Lift the cost-of-failure floor** — money, data, and safety override "we're an MVP."
3. **Respect profiles:** every specialized profile adds a non-optional obligation.
4. **Choose the lowest maturity level** that covers your real risks.
5. **Abstract on the third occurrence**, and only if smaller than the duplication.
6. **Move one rung per concrete trigger** — evidence, not ambition.

## Master do / don't table

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep cheap non-negotiables at every stage | Defer explicit errors and request IDs |
| Add idempotency when money arrives | Retry charges without keys |
| Scope every query/log/cache by tenant | Derive tenant from request input |
| Set timeouts below caller budgets | Leave external calls unbounded |
| Bound AI cost, time, and output | Let LLM calls run unrestricted |
| Checkpoint and DLQ long jobs | Restart jobs from scratch forever |
| Version public contracts before enterprise | Break partners silently |
| Build the smallest sufficient mechanism | Build a framework on the first case |
| Justify safeguards by named risk | Justify by aspiration |
| Extend handling across stages | Rebuild it each stage |

## Anti-pattern catalogue

| # | Anti-pattern | Symptom | Obligation violated | Fix |
| - | ------------ | ------- | ------------------- | --- |
| 1 | **`200` for errors** | Ambiguous responses | MVP non-negotiable | Use `4xx` + codes |
| 2 | **Stage as excuse** | MVP skips payment safety | 3.6 financial / 3.2 | Add idempotency on money |
| 3 | **Unscoped query** | Cross-tenant leak | 3.4 multi-tenant | Derive tenant from session |
| 4 | **Shared cache key** | Wrong tenant's data | 3.4 | Prefix keys with tenant |
| 5 | **No per-tenant limits** | Noisy neighbor | 3.4 | Fair-share quota |
| 6 | **Unbounded external call** | Cascading outage | 3.5 | Timeout + breaker |
| 7 | **Everything fails fast** | Cosmetic dep takes site down | 3.5 | Assign postures |
| 8 | **LLM runs unbounded** | Cost/time runaway | 3.7 | Token cap + timeout |
| 9 | **Late result = success** | Stale real-time data | 3.8 | Deadline + discard |
| 10 | **No DLQ** | Poison message blocks queue | 3.9 | DLQ + max attempts |
| 11 | **Framework-first** | Unused abstraction | 3.10/3.11 | Rule of three |
| 12 | **Maturity theater** | Level-5 words, Level-1 basics | 3.12 | Move one rung |

## Recognition cheat sheet

| When you see… | Suspect… | Check… |
| ------------- | -------- | ------ |
| `WHERE id = $1` with no tenant | Unscoped query (3.4) | Is `tenant_id` in the WHERE? |
| Cache key without tenant prefix | Cross-tenant leak (3.4) | Key composition |
| Shared pool, no per-tenant cap | Noisy neighbor (3.4) | Per-tenant concurrency |
| External call with no timeout | Cascade risk (3.5) | Timeout < budget? |
| Optional feature on the critical path | No posture assigned (3.5) | Fail-fast vs degrade |
| Charge call without idempotency key | Double-charge risk (3.6) | Key present? |
| Job loop with no checkpoint | Restart cost (3.9) | Resume point? |
| A "framework" used by one caller | Premature abstraction (3.11) | Call-site count |

## Requirement quick-derivation

| If your product is… | Then you must have… |
| ------------------- | ------------------- |
| MVP with users | explicit errors, one boundary, request IDs |
| Growing startup | + envelope, registry, retries, idempotency |
| Enterprise | + contracts, SLA/SLO, audit, isolation, DR |
| Multi-tenant | tenant-scoped everything + fair share |
| High-availability | timeouts, breakers, degradation, load shedding |
| Financial | idempotency, compensation, immutable audit |
| AI-powered | provider abstraction, limits, honest fallback |
| Real-time | deadlines, backpressure, resume |
| Background | bounded retries, DLQ, checkpoint |

## Chapter checklist

- [ ] Can you state your stage, architecture, and profiles?
- [ ] Does cost-of-failure set a floor above the stage baseline?
- [ ] Are MVP non-negotiables present (explicit errors, one boundary, request IDs)?
- [ ] Is every query/cache/queue tenant-scoped with fair-share limits?
- [ ] Do all external calls have timeouts below their caller's budget?
- [ ] Are money operations idempotent, compensable, and audited?
- [ ] Are AI calls bounded and their failures classified?
- [ ] Do real-time paths enforce deadlines and backpressure?
- [ ] Do background jobs checkpoint and route poison messages to a DLQ?
- [ ] Is your maturity level the lowest that covers your risks?
- [ ] Was every abstraction earned by a repeated need?

## Related

- [Requirements by Product Stage](../01-concepts/01-requirements-by-product-stage.md)
- [Requirements by Architecture and Risk Profile](../01-concepts/02-requirements-by-architecture-and-risk-profile.md)
- [Chapter 3 Reference](../05-reference/README.md)
- [Glossary](../../../GLOSSARY.md)
