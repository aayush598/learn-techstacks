# Chapter 18 — Do's and Don'ts

> Part VII · Chapter 18 · All sections

A condensed rule set distilled from the chapter. Use it as a domain-error review checklist.

## Definition and classification

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Model documented denials as coded domain errors | Throw `Error("invalid state")` / bare strings |
| Separate domain (business says no) from infrastructure (machinery failed) | Map pool exhaustion to a business code |
| Keep retry class honest: identical-request domain denials are permanent | Let clients auto-retry `409`/`402` like `429` |
| Carry structured details (`requested`, `limit`, `allowed`) | Encode data inside the message sentence |

## Invariants and rules

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make invariants unrepresentable (value objects, factory results) | Trust every caller to pass sane numbers |
| Share limit constants between DTO and value object | Hardcode `500` in two files |
| Alert on invariant breaches (they are bugs) | Render `23514`/invariant breaches as user `422`s |
| Enforce entity rules at the aggregate root; cross-aggregate in domain services | Put DB calls in constructors |
| Declare multi-violation order explicitly; suppress dependents | Let `if`-order pick the reported error |

## Lifecycle and preconditions

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Encode transitions as one auditable table; test the matrix | Scatter `if (state == …)` across services |
| Return `action`, `state`, `allowed`, `stateReason` | Bare "invalid operation" |
| Make completed-action re-invocation idempotent-success | Punish double-clicks with `409` |
| Re-read or version-check before transitions | Decide against stale caches |
| Give each gate its own code (`OPERATION_IN_PROGRESS`, …) | One `PRECONDITION_FAILED` for everything |

## Access, duplicates, quota, entitlement

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pick one existence-hiding policy per resource family | Mix `403` and `404` for the same class |
| Reserve `401` for missing/invalid credentials | Return `401` for rights problems |
| Treat the unique index as truth; translate `23505` to the same `409` code | Leak constraint/index names |
| Split `402` (money), `409` (capacity), `429` (rate) | Auto-retry money denials with backoff |
| Name the capability; list `entitledPlans` on denials | Anonymous "forbidden" dead ends |

## Outcomes and contracts

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return documented denials; throw only bugs/infra | Throw for "already subscribed" |
| Use discriminated unions for core multi-outcome flows | One `BusinessException` for all denials |
| Give SDKs an unknown-kind fallback; tombstone codes | Rename/reuse codes; change a code's status in a patch |
| Keep HTTP statuses and framework types out of the domain | `throw new HttpException(...)` from a service |
| Map code+category → status via registry at the boundary | Per-handler status `switch`es |

## Anti-patterns in the wild

1. **The 500 Launderer** — global `catch → 500` eats registered domain codes.
2. **The String Thrower** — `throw new Error("cannot cancel")` with no code or details.
3. **The God DTO** — plan limits and state machines embedded in schema constants.
4. **The Silent Resurrector** — a code path re-activates a `canceled` entity.
5. **The Retry Bait** — `402`/`409` returned where clients auto-retry (money loops).
6. **The Existence Oracle** — `403` on cross-tenant probes.
7. **The Dedupe-Later** — webhook effect applied before the event-id check.
8. **The Framework Spokesmodel** — Spring/Django exception types as the public vocabulary.
9. **The Code Renamer** — "cleanup" release that renames `SEAT_QUOTA_EXCEEDED`.
10. **The Generic Union Member** — `kind: "error"` that everyone throws, defeating exhaustiveness.

## Chapter checklist

- [ ] Every "no" in the domain has a registered code + category + details + status.
- [ ] Domain vs infrastructure classification documented per code.
- [ ] Invariants enforced by types/aggregate roots; DB backstops alert.
- [ ] Transition tables exist per stateful entity; matrix-tested.
- [ ] Idempotency of each action decided and documented.
- [ ] Existence-hiding, balance/quota/rate, and entitlement policies written down.
- [ ] Core flows use typed outcomes; client SDKs degrade on unknown kinds.
- [ ] Domain compiles without framework/HTTP dependencies (CI lint).
- [ ] Boundary mapper is registry-driven; unknown codes alert.
- [ ] Codes are tombstoned forever; additions are the only normal change.

## Related

- [Chapter 18 Reference](../05-reference/README.md)
- [Value Object and Domain Error Examples](../03-practical-examples/01-value-object-money-and-domain-errors.md)
- [Chapter 17 — Input Validation Error Handling](../../17-input-validation-error-handling/README.md)
