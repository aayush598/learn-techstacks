# Chapter 25 — Dos and Don'ts

> Part X · Chapter 25 · All subsections 25.1–25.20 · _Estimated reading time: 10 min_

## Purpose

Quick rules for third-party API error handling. Use in code reviews for **Acme SaaS** integrations.

## Dos

| ✅ Do | Rationale |
| ----- | --------- |
| **Translate at the boundary** | Keep domain vendor-agnostic via adapters. |
| **Classify by origin** (http/payload/network) | Enables correct retry/fallback policy. |
| **Parse provider payloads** even on 4xx/5xx and check 200-with-error | Prevents treating failures as success. |
| **Respect `Retry-After` on 429/503** | Follow provider throttling instructions. |
| **Use idempotency keys for non-idempotent operations** | Critical for safe retries during outages. |
| **Distinguish critical vs optional dependencies** | Fail closed for critical, degrade for optional. |
| **Preserve `cause` and use safe messages** | Debuggable without leaking vendor details. |
| **Pin API versions** | Avoid surprise breaks. |
| **Plan for outages** (timeouts, circuit breaker, budgets, feature flags) | Prevent retry storms. |
| **Make adapters replaceable** | Future-proof vendor swaps. |

## Don'ts

| ❌ Don't | Why |
| -------- | --- |
| **Propagate vendor errors to domain** | Creates tight coupling and leaks details. |
| **Trust status codes alone** | Misses 200-with-error and misleading semantics. |
| **Retry `401`/`403`/card declines blindly** | Wastes resources, no recovery. |
| **Retry non-idempotent ops without keys** | Risks duplicate charges/side effects. |
| **Guess on critical timeouts** | Can create paid orders without confirmed charge. |
| **Degrade critical flows** | Risks financial/state inconsistency. |
| **Log full provider payloads with PII** | Security/compliance risk. |
| **Use latest API version unpinned** | Breaking changes hit without warning. |
| **Retry forever during outage** | Amplifies load and worsens incident. |
| **Assume JSON on all error paths** | HTML error pages cause parse failures. |

## Quick checklist

- [ ] All vendor calls go through adapters.
- [ ] Translation tables exist and tested.
- [ ] Critical vs optional documented per dependency.
- [ ] Idempotency strategy defined for mutations.
- [ ] Outage controls in place (timeouts/circuit breaker/budgets).

## Related

- [Chapter 25 README](../README.md)
- [Translation, Adapters, and Outages](../01-concepts/04-translation-adapters-and-outages.md)
- [Stripe Error Mapping Adapter](../03-practical-examples/01-stripe-error-mapping-adapter.md)
- [Glossary](../../../GLOSSARY.md)
