# Chapter 2 — Do's and Don'ts

> Part I · Chapter 2 · Rules, anti-patterns, and the chapter checklist.

## The golden rules

1. **State failure explicitly** — in the type, signature, or response.
2. **Handle each condition once**, at the layer that owns the decision.
3. **Preserve the cause** on every wrap and translation.
4. **Never convert a failure into a success.**
5. **Choose a posture on purpose** — fail-fast, fail-safe, or degrade.
6. **Centralize policy, localize decisions.**

## Master do / don't table

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Encode failure in the type/return | Use `null`/`false` for many meanings |
| Reuse one status mapping | Invent a status per endpoint |
| Attach `cause` / `%w` / `from exc` | `throw new Error("failed")` |
| Let a `catch` handle/translate/rethrow/record | `catch {}` or debug-only logging |
| Fail-fast on bugs and critical deps | Limp along on a corrupt invariant |
| Fail-safe on security/integrity | Fail-open an authz check |
| Degrade only with honest fallbacks | Present stale data as authoritative |
| Centralize mapping, localize fallback | A giant middleware guessing intent |
| Give each handler one job | Catch-log-retry-translate in one block |
| Add an error via one registry entry | Edit ten handlers to add a category |
| Keep the happy path readable | Bury business logic in try/catch |

## Anti-pattern catalogue

| # | Anti-pattern | Symptom | Principle violated | Fix |
| - | ------------ | ------- | ------------------ | --- |
| 1 | **Swallow** | `catch {}` / debug-only | 2.14 | Handle, translate, rethrow, or record |
| 2 | **Failure→success** | Returns OK on failure | 2.15 | Return a real failure outcome |
| 3 | **Cause-drop** | `throw new Error("x failed")` | 2.13 | Attach the original error |
| 4 | **Redundant handling** | Same error logged 3× | 2.16 | Handle once, at the owner |
| 5 | **Ceremonial rethrow** | `catch (e) { throw e }` | 2.17 | Delete, or add context |
| 6 | **Implicit contract** | `null` means 3 things | 2.1 | Explicit result/typed error |
| 7 | **Mapping drift** | 409 here, 200 there | 2.2 | Central registry |
| 8 | **God handler** | Middleware with business logic | 2.5, 2.6 | Move decisions to owner |
| 9 | **Defense everywhere** | try/catch per line | 2.10 | Defend at boundaries only |
| 10 | **Surprising behavior** | `get` that creates | 2.11 | Honest names/verbs |
| 11 | **Framework in a hurry** | Bespoke abstraction per team | 2.19, 2.20 | Shared primitives first |
| 12 | **Posture by accident** | Everything fails fast | 2.7–2.9 | Assign posture per dep |

## Recognition cheat sheet

| When you see… | Suspect… | Check… |
| ------------- | -------- | ------ |
| `catch` with no `throw`/return/record | Swallow (2.14) | Is any signal emitted? |
| 2xx on an operation that can fail | Failure→success (2.15) | Does caller act on it? |
| `new Error("something went wrong")` | Cause-drop (2.13) | Is `cause` attached? |
| The same error in 3 log lines | Redundant handling (2.16) | Who owns the decision? |
| Different status for one situation | Mapping drift (2.2) | Registry says? |
| `try { } catch (e) { throw e }` | Ceremonial (2.17) | Adds context? If not, delete |
| 20-line try/catch around a rule | Tangled (2.4) | Can the domain name it? |

## Chapter checklist

- [ ] Failures are explicit in types/signatures.
- [ ] The same situation yields the same status everywhere.
- [ ] Every error code has an owner and registry entry.
- [ ] Every wrap preserves the cause.
- [ ] No catch block swallows without a decision or record.
- [ ] No failure path returns a success-shaped result.
- [ ] The domain contains no HTTP/transport concepts.
- [ ] Policy is defined once; fallback decisions are local.
- [ ] Each handler has exactly one responsibility.
- [ ] Each fallible dependency has a written posture.
- [ ] Security/integrity decisions are fail-safe.
- [ ] Adding a new error touches one registry entry.
- [ ] The happy path is readable at a glance.

## Related

- [Chapter 2 Concepts: Explicitness and Consistency](../01-concepts/01-explicitness-consistency-and-predictability.md)
- [Chapter 2 Concepts: Preserving Signals](../01-concepts/04-preserving-and-not-swallowing-errors.md)
- [Chapter 2 Reference](../05-reference/README.md)
- [Glossary](../../../GLOSSARY.md)
