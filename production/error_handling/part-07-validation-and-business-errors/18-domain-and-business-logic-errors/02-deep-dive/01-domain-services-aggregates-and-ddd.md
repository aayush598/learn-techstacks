# Domain Services, Aggregates, and DDD Error Design

> Part VII · Chapter 18 · Sections 18.14–18.16 · _Estimated reading time: 22 min_
> **Prerequisite:** [Invariants, Business Rules, and Multiple Violations](../01-concepts/02-invariants-and-business-rules.md)

## In one sentence

Rules that span one entity belong in an **aggregate root**, rules that span consistency
boundaries belong in a **domain service**, and a **DDD** vocabulary (ubiquitous language,
repositories, anti-corruption) is what keeps every resulting error code *legible to the business*
and free of infrastructure dialect.

## Why this matters in production

Where the check lives decides how the error behaves: a rule in a controller returns `400`, the
same rule in a repository returns a leaked `23505`, and the same rule in a domain service returns
`SEAT_QUOTA_EXCEEDED` with the right details and one HTTP mapping. DDD is not religion here —
it is the set of placement decisions that make your error vocabulary *stable* while frameworks,
databases, and UIs churn around it.

## 18.14 — Domain services

A **domain service** hosts a business operation that does not naturally fit one entity, has no
identity of its own, and is still pure business logic (no HTTP, no SQL, no framework):

| Operation | Why a domain service | Not a… |
| --------- | --------------------- | ------ |
| `scheduleUpgrade(sub, action)` | Needs subscription + payment-in-flight + clock | entity method (cross-aggregate) |
| `quoteDowngrade(tenant, targetPlan)` | Needs usage + plan catalog + proration rules | controller (would be re-implemented per transport) |
| `canExport(tenant)` | Needs job table + plan + feature flags | repository (would return `false`, losing *why*) |

Shape of a domain service operation:

```ts
// Pure: inputs → outcome. No ctx, no logger, no HTTP types, no Date.now() without a clock port.
export interface PricingPort { proration(from: Plan, to: Plan, at: Instant): Money; }

export function changePlan(
  tenant: Tenant,
  target: Plan,
  at: Instant,
  pricing: PricingPort,
): Result<PlanChange, DomainError> {
  if (tenant.state === "suspended")
    return err(new AccountSuspended(tenant.suspendedReason ?? "unspecified"));
  if (!target.availableIn(tenant.country))
    return err(new PlanUnavailable(target.code, { country: tenant.country }));
  const proration = pricing.proration(tenant.plan, target, at);
  if (proration.isNegative && !tenant.plan.refundable)
    return err(new DowngradeBlocked("NON_REFUNDABLE_PERIOD", { credit: proration }));
  return ok({ target: target.code, charge: proration, effectiveAt: at });
}
```

Properties: **deterministic given inputs** (clock and pricing arrive as parameters/ports),
**returns coded outcomes**, **testable with fakes in milliseconds**.

## 18.15 — Aggregate operations

An **aggregate** is a consistency boundary: a root entity plus the invariants that must hold
*atomically* across it. The root is the only entry point; it enforces its invariants on every
command and raises domain errors itself.

```ts
export class Invoice {                     // aggregate root
  static create(lines: Line[], tax: TaxProfile): Result<Invoice, DomainError> {
    if (lines.length === 0) return err(new EmptyInvoice());
    const total = sum(lines);
    if (total.isNegative)   return err(new NegativeTotal(total.toString()));  // invariant
    return ok(new Invoice(id(), lines, tax.apply(total), "open"));
  }

  markPaid(ref: PaymentRef): Result<void, DomainError> {
    if (this.status !== "open")
      return err(new InvalidTransition("markPaid", this.status, { allowed: ["open"] }));
    this.status = "paid"; this.paidRef = ref;
    return ok(undefined);
  }
}
```

Why error placement inside aggregates matters:

- **Invariants are checked where the state is** — no path can mutate without the checks (18.2).
- **Cross-aggregate rules do NOT live here** — an aggregate cannot see another aggregate's
  internals; it either loads a reference id (and lets the domain service decide) or the service
  coordinates ([transaction boundaries](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)).
- **Repositories translate persistence failures to domain errors at the aggregate's edge**
  (`23505` → `ALREADY_EXISTS`), never inside the aggregate (Ch. 16/24).

```text
 controller / handler                    ← validation (Ch. 17) happens here, not inside
        │
        ▼
 application service                     ← opens tx, loads aggregates via repositories,
        │                                   calls domain service / root methods,
        │                                   maps outcome → transport (one place)
        ▼
 domain service  ──►  aggregate root     ← invariants, transitions, coded errors
        ▲                   │
        └──── repositories ─┘             ← translate DB errors at this edge only
```

## 18.16 — DDD alignment

The DDD pieces that specifically serve error handling:

| DDD concept | Error-handling payoff |
| ----------- | --------------------- |
| **Ubiquitous language** | Error codes reuse business words (`cancel`, `invoice`, `seat`), so PMs recognize denials in the registry |
| **Bounded context** | `PROJECT_ARCHIVED` in *Project* context ≠ *Billing* context's codes; contexts own vocabularies, the registry namespaces them |
| **Anti-corruption layer** | Stripe's `card_declined` becomes your `PAYMENT_CARD_DECLINED` at the adapter — vendor dialect never enters the domain (Ch. 16) |
| **Repository** | Persistence errors are translated at this edge into domain errors with cause preserved |
| **Domain event** | `SubscriptionPastDue` carries the facts; *handlers* decide UI/dunning — events are data, not errors thrown at subscribers |
| **Specification** | A named, composable rule object (`EmailNotInTenantSpec`) with one `why()` → one code |

Bounded-context namespacing, concretely:

```text
 billing:INVOICE_OPEN          (an unpaid invoice blocks a new charge)
 billing:PAYMENT_IN_FLIGHT     (a charge is currently processing)
 projects:JOB_ALREADY_RUNNING  (an export is running for the project)
```

Without prefixes, `ALREADY_EXISTS` means different things per context and the registry becomes a
collision field (Ch. 8.4 domain prefixes). With prefixes, support can route by code prefix alone.

**Domain events vs domain errors** (a recurring confusion):

| | Domain error | Domain event |
| - | ------------ | ------------ |
| Nature | This operation is rejected | This fact happened |
| Direction | Returned/thrown to the caller | Published to subscribers |
| Example | `SEAT_QUOTA_EXCEEDED` | `SeatAdded { tenantId, added }` |
| Failure handling | Caller acts | Each handler isolates its own failures (Ch. 33) |

⚠️ **Hazard.** Publishing `XFailed` events instead of returning errors turns every caller into a
subscriber and makes the happy-path contract invisible. Return denials; publish only *facts*.

## Key data / numbers

- Placement rule: validation → handler · rules/transitions → domain service & aggregate root ·
  persistence translation → repository edge · status mapping → application/transport boundary.
- Aggregate = consistency boundary; one transaction per aggregate modification (typical
  recommendation; sagas for cross-aggregate — Ch. 39).
- Namespace codes per bounded context: `context:CODE` (or a registry `context` column).
- Domain services take **clock and I/O as parameters/ports** — never call `now()` or SDKs
  directly.

## Real-world use case — Checkout

`Checkout` coordinated three aggregates (Subscription, Invoice, Payment). Originally each
controller (web, mobile BFF, admin CLI) re-implemented the sequence and its checks; the three
drifted, and one path allowed `markPaid` on an already-`void` invoice, corrupting dunning state.
The fix: a `CheckoutService` domain service owning the sequence; `Invoice.markPaid` enforcing its
own transition; repositories translating `23505`/`55000` to domain codes; controllers reduced to
"call service, map outcome". The corrupted-state bug became impossible (the aggregate rejects the
arrow), and a single exhaustiveness switch in the web client covered all three surfaces because
they finally shared one outcome vocabulary.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Logic in handlers | Fast to write | N copies, drift, transport-coupled errors | Never past prototype |
| Aggregate-root enforcement | Invariants unbreakable via API | Some ceremony per entity | ✅ Entities with state |
| Domain services for cross-cutting rules | One rule, one code, testable | Indirection | ✅ Multi-aggregate rules |
| Events instead of returned errors | Loose coupling | Invisible contracts, replay ambiguity | Only for facts, not denials |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put cross-aggregate rules in domain services | Load two aggregates into one "god entity" |
| Return coded outcomes from root methods | `assert()` that crashes with a bare error |
| Translate DB errors only at the repository edge | Reference `SQLSTATE` from aggregates |
| Namespace codes by bounded context | Share one flat `ALREADY_EXISTS` across contexts |

## Common mistakes

- **Anemic aggregate + fat service** — invariants live in the service; a new endpoint forgets
  them.
- **Domain service that injects the repository and the clock** — untestable; invert via ports.
- **Context-agnostic codes** — billing and projects emit the same code with different meanings;
  clients conflate them.
- **Treating domain events as error channels** — subscribers retry business denials forever.

## Checklist

- [ ] One placement rule documented (table above) and followed in review.
- [ ] Aggregate roots enforce invariants/transitions; no bypassing setters.
- [ ] Domain services are pure (ports for clock/IO), return coded outcomes.
- [ ] Repository is the only DB-translation edge; cause preserved.
- [ ] Codes namespaced per bounded context; events carry facts, not denials.

## Related

- [Framework Independence and Outcome Mechanics](./02-framework-independence-and-outcome-mechanics.md)
- [Invariants, Business Rules, and Multiple Violations](../01-concepts/02-invariants-and-business-rules.md)
- [Chapter 15 — Error Boundaries](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
