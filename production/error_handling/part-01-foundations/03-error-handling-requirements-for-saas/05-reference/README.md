# Chapter 3 — Reference

> Part I · Chapter 3 · Requirement matrix, maturity ladder, and chapter glossary.

## Cheat sheet — requirements by stage

| Capability | MVP | Startup | Enterprise |
| ---------- | --- | ------- | ---------- |
| Explicit errors | ✅ | ✅ | ✅ |
| One boundary | ✅ | ✅ | ✅ |
| Request IDs | ✅ | ✅ | ✅ |
| Standard envelope | — | ✅ | ✅ |
| Code registry | — | ✅ | ✅ |
| Retries + backoff | — | ✅ | ✅ |
| Idempotency (writes) | — | ✅ (money) | ✅ |
| Versioned contracts | — | — | ✅ |
| SLA/SLO + error budget | — | informal | ✅ |
| Audit trail | — | — | ✅ |
| Tenant isolation tiers | — | basic | ✅ |
| DR / failover / runbooks | — | — | ✅ |

## Cheat sheet — obligations by risk profile

| Profile | One-line obligation | Key mechanism |
| ------- | ------------------- | ------------- |
| Multi-tenant (3.4) | One tenant never affects another | Session-scoped queries + fair-share quotas |
| High-availability (3.5) | One component never takes down all | Timeouts + breakers + degradation |
| Financial (3.6) | No duplicate or lost money | Idempotency + compensation + audit |
| AI-powered (3.7) | Bounded cost, honest output | Provider abstraction + limits + fallback |
| Real-time (3.8) | No stale success | Deadlines + backpressure + resume |
| Background (3.9) | No lost/blocked job | Bounded retries + DLQ + checkpoints |

## Decision table — is this safeguard warranted now?

| Question | Yes → | No → |
| -------- | ----- | ---- |
| Does a real failure argue for it? | Add it | Wait for evidence |
| Does a profile require it? | Add it now | Defer if cheap |
| Is the cost of failure irreversible? | Add it now | Defer |
| Has the pattern occurred 3+ times? | Abstract it | Use a function |
| Is the abstraction smaller than the dup? | Build it | Keep duplication |

## Error budget reference

| SLO | Downtime/month | Implication |
| --- | -------------- | ----------- |
| 99.0% | ~7.2 h | Loose; fail-fast acceptable |
| 99.9% | ~43 min | Standard SaaS; degrade optional paths |
| 99.95% | ~22 min | Aggressive; load-shed early |
| 99.99% | ~4.3 min | Requires redundancy + isolation |

An exhausted budget tilts decisions toward **reliability over feature velocity**; a healthy budget
allows more risk-taking.

## Maturity ladder

| Level | Name | You have | Move up when |
| ----- | ---- | -------- | ------------ |
| 1 | Ad hoc | try/catch, inconsistent | First real users |
| 2 | Conventions | explicit errors, one boundary, request IDs | Clients need codes; drift |
| 3 | Contracts | registry, envelope, stable codes | Outages, money, scale |
| 4 | Resilience | retries, idempotency, degradation, DLQ | Second product re-implements policy |
| 5 | Reusable | shared library + docs | — evolve, don't redesign |

## Profile matrix — quick audit

| Profile | Present? | Artifact to check |
| ------- | -------- | ----------------- |
| Multi-tenant | [ ] | `tenant_id` in every query/cache/queue |
| High-availability | [ ] | timeout < budget; breakers; postures |
| Financial | [ ] | idempotency keys; compensation; audit |
| AI-powered | [ ] | token/time caps; provider/tool/app codes |
| Real-time | [ ] | deadlines; backpressure; sequence numbers |
| Background | [ ] | max attempts; DLQ; checkpoint |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| MVP | Earliest stage; learn fast; cheap non-negotiables stay |
| Growing startup | First paying customers; consistency + recovery |
| Enterprise SaaS | Contractual reliability, compliance, isolation |
| Noisy neighbor | One tenant degrading others via shared resources |
| Blast radius | How far a failure spreads |
| Idempotency key | Token collapsing duplicate operations |
| Compensation | Business-level undo of a completed step |
| Deadline | Maximum time before a result is discarded |
| Backpressure | Rejecting/coalescing work instead of stalling |
| Checkpoint | Saved resume point for a long job |
| Error budget | Allowed unreliability from an SLO |
| Premature abstraction | Abstraction before a repeated need |
| Rule of three | Abstract on the third occurrence |

## Signposts

- Taxonomy for the codes you must define → [Ch. 4](../../../part-02-error-taxonomy/04-designing-a-comprehensive-error-taxonomy/README.md)
- Error envelope / contracts → [Ch. 20](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md), [Ch. 49](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
- Resilience mechanics → [Ch. 27](../../../part-11-retry-and-resilience/27-retry-policies/README.md)–[Ch. 30](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- Specialized scenarios → [Ch. 42](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md), [Ch. 44](../../../part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)
- Maturity model → [Ch. 61](../../../part-24-repeatable-blueprint/61-error-handling-maturity-model/README.md)

## Related

- [Chapter 3 — Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 3 — Chapter overview](../README.md)
- [Part I — Foundations](../../README.md)
- [Glossary](../../../GLOSSARY.md)
