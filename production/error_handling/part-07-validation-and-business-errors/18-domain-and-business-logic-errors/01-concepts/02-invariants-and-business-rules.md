# Invariants, Business Rules, and Multiple Violations

> Part VII · Chapter 18 · Sections 18.2, 18.3, 18.19 · _Estimated reading time: 20 min_
> **Prerequisite:** [What Domain Errors Are](./01-what-domain-errors-are.md)

## In one sentence

An **invariant** is a statement that must be true *whenever the data exists* and is enforced by
the data's own type/aggregate, while a **business rule** is a policy enforced by a service during
an operation — and deciding how **multiple simultaneous violations** behave is part of the
contract, not an accident of code order.

## Why this matters in production

An entity that *can* be constructed in an invalid state eventually *will* be — usually by the
one code path that skipped your service-layer checks (an importer, a migration, a "temporary"
script). Then you discover `seats = -4` in production and a `CHECK` constraint firing as
`SQLSTATE 23514`, which your translation table politely turns into a `500` because nobody expected
it. Invariants at the type boundary make that impossible; rules at the service boundary make the
policy explicit; multi-violation policy makes failure responses *predictable* instead of
order-dependent.

## 18.2 — Invariants

**Definition:** an invariant is a property that holds for every *existing* instance —
`Money.amount >= 0` (minor units), `Seats in 1..5000`, `Project.name not blank`, `range.from <=
range.to`. If a state could violate it, the state must be **unrepresentable**.

Enforcement points, in increasing desperation:

| Mechanism | Example | Guarantee |
| --------- | ------- | --------- |
| **Type/value object** | `new Seats(30)` throws; no `int` for seats anywhere | Strongest — see [practical example](../03-practical-examples/01-value-object-money-and-domain-errors.md) |
| **Constructor/factory checks** | `Project.create(...)` validates before insert | Good, but bypassable if fields are mutable |
| **Command methods only** | No public setters; `project.renameTo(x)` checks | Keeps invariants through mutations |
| **DB `CHECK`/`NOT NULL`** | `CHECK (seats BETWEEN 1 AND 5000)` | Last line; translate `23514` — a **bug alarm**, not a normal path |
| Service-layer `assert` | Checks before save | Weakest; depends on every path remembering |

```ts
// Invariant violation is a *programmer* bug at this layer — alert, do not blame the user.
// (If untrusted input can trigger it, the validation layer failed — 17.x.)
if (!rule.holds(state)) {
  throw new InvariantViolation(rule.name, { state: snapshotOf(state) });  // → 500 + alert
}
```

> ⚠️ **Hazard.** Reporting invariant violations as user-facing `422`s hides bugs. The correct
> split: if the input could be at fault, it should have been stopped at validation (422, user's
> fault); if only our code could produce it, it is a `500` with alerting (our fault).

## 18.3 — Business rules

**Definition:** a business rule is a policy evaluated during an operation, usually needing state
outside the entity: "upgrade seats only while no payment is in flight", "a workspace on the Free
plan may have at most 3 projects", "exports blocked during a billing grace period".

Where they live:

| Kind | Needs | Lives in | Example |
| ---- | ----- | -------- | ------- |
| Entity rule | Own fields only | Value object / aggregate method | `endAt >= startAt` |
| Aggregate rule | Sibling entities in one consistency boundary | Aggregate root method | "invoice must be open before credit" |
| Cross-aggregate rule | Two aggregates / services | **Domain service** (18.14) | "seat count ≤ plan limit" |
| Temporal/external rule | Clock, provider, another system | Domain service + ports | "trial ended before cancel-convert" |

```ts
// Domain service: the rule is named, coded, and testable without HTTP or DB.
export function scheduleUpgrade(sub: Subscription, when: Instant): Result<Upgrade, DomainError> {
  if (sub.state !== "active")
    return err(new InvalidTransition("scheduleUpgrade", sub.state, { allowed: ["active"] }));
  if (sub.paymentInFlight)
    return err(new ConcurrencyConflict("PAYMENT_IN_FLIGHT", { subscriptionId: sub.id }));
  return ok({ subscriptionId: sub.id, effectiveAt: when });
}
```

Rule-design rules:

1. **Name the rule in the code** (`scheduleUpgrade`, `mayAddSeats`) — the name becomes the code.
2. **One rule, one error code** — not a shared `BUSINESS_ERROR`.
3. **Rules return outcomes**; they do not log, do not translate, do not know HTTP (18.12).

## 18.19 — Multiple simultaneous violations

When several rules fail at once, pick a policy per operation type — and document it:

| Policy | Behavior | Use when |
| ------ | -------- | -------- |
| **First violation (ordered)** | Evaluate rules in declared order; return the first failure | Rules have priority (safety > billing > preference) |
| **All violations (accumulate)** | Like validation aggregation, but domain-coded | Multi-step admin/bulk operations; forms over workflows |
| **Grouped by axis** | e.g. all quota issues, then all entitlement issues | Support-heavy flows where one triage answer fixes all |

```ts
// Ordered evaluation: priority is explicit, not an accident of `if` order.
const RULES: Array<[string, (s: Subscription, a: UpgradeAction) => DomainError | null]> = [
  ["payment_in_flight", (s, a) => s.paymentInFlight ? new PaymentInFlight(s.id) : null],
  ["state",             (s, a) => s.state !== "active" ? new InvalidTransition("upgrade", s.state) : null],
  ["quota",             (s, a) => a.seats > s.plan.maxSeats
                                    ? new SeatQuotaExceeded(a.seats, s.plan.maxSeats) : null],
  ["entitlement",       (s, a) => !s.plan.features.has("sso") && a.wantsSso
                                    ? new EntitlementMissing("sso") : null],
];
```

Key mechanics:

- **Never report a *dependent* violation** when its precondition already failed (mirror of 17.7):
  if the subscription is `canceled` (state error), do not *also* report quota for it.
- **Accumulation cap** still applies (domain errors in a bulk flow: cap + truncation, as 17.11).
- **HTTP shape:** one primary code at the top level; additional violations either as
  `details.violations[]` (recommended for admin tools) or logged-only (consumer flows).

## Key data / numbers

- Invariant breach surfacing as `SQLSTATE 23514` / `ERRCODE_CHECK_VIOLATION` = **translation
  alarm** → map to `500` + alert, not routine `422`.
- Multi-violation HTTP shape: primary `code` + optional `details.violations: [{code, details}]`.
- Rule order is a contract-adjacent decision: changing it changes which error clients see first —
  treat reorders as behavior changes (18.20).
- Value-object invariant ranges belong in **one place** (the type), reused by validation *and*
  domain (single source: `Seats.MIN`/`Seats.MAX`).

## Real-world use case — Acme SaaS

Acme's `Project.create` trusted its callers: `seats` was a plain `int` in five call sites, and a
new importer wrote `seats = 0` for rows with empty cells. The DB `CHECK` rejected them as
`23514`; the repository mapped check violations to `500`, and the nightly import alerted for
three weeks before anyone read the alert text. Two changes fixed the class, not the instance:
`Seats` value object (invariant at construction) plus repository mapping of `23514` →
`INVARIANT_BREACH` + **page**, because the domain promised that error could not legitimately
arrive from user input. Importer rows became `422` at the DTO (`out_of_range`), and `23514`
returned to its proper role: an alarm for broken code.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Value objects for all invariants | Impossible states unrepresentable | Type count; mapping boilerplate | ✅ Money, seats, ranges, dates |
| Service asserts only | Less code now | Bypassable paths; late detection | Prototypes |
| DB CHECK as the rule | Catches everything | Wrong layer for UX; alerts or wrong 422s | ✅ As backstop only, with alerting |
| Ordered first-failure | Predictable, cheap | Hides secondary issues | ✅ Consumer flows |
| Accumulate all | Complete | Needs caps; complex HTTP shape | Admin/bulk flows |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make invariants unrepresentable via types | Store `seats` as bare `int` "for convenience" |
| Alert on invariant breaches; never blame users | Translate `23514` into a routine `422` |
| Declare rule order explicitly; test it | Let `if`-order accidents pick the winner |
| Suppress dependent violations | Report "canceled subscription" + "quota exceeded" for a dead sub |

## Common mistakes

- **Business rule in the constructor that needs the DB** — untestable, layered wrongly; move to a
  domain service.
- **Mutable public fields + constructor-only checks** — invariants break on the second method.
- **Accumulating without suppressing dependents** — noise overwhelms the real answer.
- **Changing rule order in a patch release** — clients see different primary codes; treat as a
  contract change.

## Checklist

- [ ] Every invariant is enforced by a type or aggregate boundary, with a DB backstop that alerts.
- [ ] Every business rule has a name that matches its error code.
- [ ] Multi-violation policy (ordered vs accumulated) is documented per operation.
- [ ] Dependent violations are suppressed when preconditions fail.
- [ ] Invariant breaches page; they never masquerade as user `422`s.

## Related

- [State Transitions and Lifecycle](./03-state-transitions-and-lifecycle.md)
- [Domain Services, Aggregates, and DDD](../02-deep-dive/01-domain-services-aggregates-and-ddd.md)
- [Value Object and Domain Error Examples](../03-practical-examples/01-value-object-money-and-domain-errors.md)
- [Chapter 22 — Database Error Classification (23514)](../../../part-09-database-and-transactions/22-database-error-classification/README.md)
