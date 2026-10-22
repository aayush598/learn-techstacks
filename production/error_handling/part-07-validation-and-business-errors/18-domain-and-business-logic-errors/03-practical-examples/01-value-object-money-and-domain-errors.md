# Value Objects That Make Violations Impossible — Money, Seats, and Coded Errors

> Part VII · Chapter 18 · All sections · _Estimated reading time: 24 min_
> **Prerequisite:** [Invariants, Business Rules, and Multiple Violations](../01-concepts/02-invariants-and-business-rules.md)

## In one sentence

The complete worked pattern: **value objects** (`Money`, `Seats`, `DateRange`) whose constructors
make invalid states unrepresentable, a **typed domain error** family carrying structured details,
and the registry row that turns each code into one HTTP answer.

## Why this matters in production

This is the "show me the code" companion to 18.2/18.3. Value objects are the cheapest insurance
in a business codebase: one class each for money and quantities eliminates an entire bug genus
(float drift, negative seats, end-before-start invoices) — and the errors they *do* raise are
precise, coded, and carry the numbers support actually needs.

## Step 1 — Value objects with invariants

```ts
export class Money {
  private constructor(readonly minor: number, readonly currency: Currency) {
    if (!Number.isSafeInteger(minor)) throw new InvariantViolation("money_integer", { minor });
  }
  static of(minor: number, currency: Currency): Result<Money, DomainError> {
    if (minor < 0) return err(new AmountNegative(minor, currency.code));   // expected? see below
    return ok(new Money(minor, currency));
  }
  static zero(c: Currency) { return new Money(0, c); }
  add(o: Money): Money { this.sameCurrency(o); return new Money(this.minor + o.minor, this.currency); }
  private sameCurrency(o: Money) {
    if (o.currency !== this.currency) throw new InvariantViolation("currency_mix", { a: this.currency, b: o.currency });
  }
}

export class Seats {
  static readonly MIN = 1; static readonly MAX = 5000;
  private constructor(readonly value: number) {}
  static of(n: number): Result<Seats, DomainError> {
    if (!Number.isInteger(n)) return err(new SeatsNotInteger(n));
    if (n < Seats.MIN || n > Seats.MAX) return err(new SeatsOutOfRange(n, Seats.MIN, Seats.MAX));
    return ok(new Seats(n));
  }
}

export class DateRange {
  static of(from: Instant, to: Instant): Result<DateRange, DomainError> {
    if (to.compare(from) < 0) return err(new RangeInverted(from, to));   // 18.2 entity-level invariant
    return ok({ from, to });
  }
}
```

Two-layer detail that confuses people — decide deliberately:

| Violation | Who can trigger it? | Model |
| --------- | ------------------- | ----- |
| `seats = "5"` from JSON | The caller | **Validation** `type_mismatch` (Ch. 17) — reuse `Seats.MIN/MAX` constants in the DTO |
| `seats = -3` from a bad importer | The caller (via a path that skipped validation) | `422` from the DTO *or* domain error if it reaches the domain |
| `Money` overflow from our arithmetic | Only our code | **Invariant violation → `500` + alert** |

**Single source of limits:** export `Seats.MIN/MAX` and use them in the schema *and* the value
object so the two can never disagree (the classic drift bug: DTO says 500, domain says 5000).

## Step 2 — Typed domain errors with details

```ts
export abstract class DomainError extends Error {
  abstract readonly code: string;
  abstract readonly category: Category;
  constructor(readonly details: Record<string, unknown> = {}, cause?: unknown) {
    super(); this.cause = cause;
  }
}

export class SeatsOutOfRange extends DomainError {
  readonly code = "SEATS_OUT_OF_RANGE"; readonly category = "VALIDATION";
  constructor(n: number, min: number, max: number) { super({ value: n, min, max }); }
}

export class SeatQuotaExceeded extends DomainError {
  readonly code = "SEAT_QUOTA_EXCEEDED"; readonly category = "QUOTA";
  constructor(readonly requested: number, readonly limit: number, readonly plan: string) {
    super({ requested, limit, plan, upgradeRequired: true });
  }
}

export class RangeInverted extends DomainError {
  readonly code = "RANGE_INVERTED"; readonly category = "CONFLICT";
  constructor(from: Instant, to: Instant) { super({ from: from.iso, to: to.iso }); }
}
```

Naming check: `SEATS_OUT_OF_RANGE` (a *rule*, reused by any field with seat semantics) vs
`SeatQuotaExceeded` (a *world fact*: your plan). Different layers, different lifetimes, different
statuses — do not merge them into one "seats error".

## Step 3 — Composition in a domain service

```ts
export function createProject(cmd: CreateProject, tenant: Tenant): Result<Project, DomainError> {
  const seats = Seats.of(cmd.seats);                       // already validated at DTO; defensive
  const range = DateRange.of(cmd.start, cmd.end);          // entity invariant
  if (isErr(seats)) return seats.error;
  if (isErr(range)) return range.error;

  if (tenant.usage.projects >= tenant.plan.maxProjects)
    return err(new ProjectQuotaExceeded(tenant.usage.projects, tenant.plan.maxProjects));

  return ok(Project.create({ name: cmd.name, seats: seats.value, range: range.value }, tenant.id));
}
```

Ordering mirrors 18.19: pure invariants first (cheap, payload-owned), then stateful rules
(needs tenant) — and only one error returns.

## Step 4 — Registry and transport

```sql
INSERT INTO domain_codes(code, category, http_status, message_key, added_in) VALUES
  ('SEATS_OUT_OF_RANGE',    'VALIDATION', 422, 'domain.seats_out_of_range',    'v3.0'),
  ('SEAT_QUOTA_EXCEEDED',   'QUOTA',      402, 'domain.seat_quota_exceeded',   'v3.0'),
  ('RANGE_INVERTED',        'CONFLICT',   409, 'domain.range_inverted',        'v3.0'),
  ('PROJECT_QUOTA_EXCEEDED','QUOTA',      402, 'domain.project_quota_exceeded','v3.0');
```

```json
{
  "type": "https://errors.acme.example/quota",
  "title": "SEAT_QUOTA_EXCEEDED",
  "status": 402,
  "detail": "This change requires 30 seats; your pro plan includes 12.",
  "requestId": "req_2d91cc",
  "requested": 30,
  "limit": 12,
  "plan": "pro",
  "upgradeRequired": true
}
```

The client needs zero prose parsing: `requested − limit = 18` drives the exact upsell copy, and
`upgradeRequired` drives whether to show the billing CTA.

## Key data / numbers

- `Money` in **minor units** (cents) + currency; never floats (see Ch. 6 invariants).
- Value-object ranges exported as constants shared with DTOs (`Seats.MIN=1`, `MAX=5000` —
  recommendations; publish your real limits).
- Errors here: `SEATS_OUT_OF_RANGE` → `422`, `RANGE_INVERTED` → `409`, `SEAT_QUOTA_EXCEEDED` →
  `402`, `PROJECT_QUOTA_EXCEEDED` → `402`.
- Invariant breaches from *our* arithmetic → `500` + alert, never user-facing `422`.

## Real-world use case — Checkout

`Checkout` proration computed credits in floats: a downgrade produced `-0.0000001` cents of
rounding drift, the DB `CHECK (credit_minor >= 0)` rejected it (`23514` → mapped to `500`), and
the customer saw an outage page while attempting a *downgrade*. Two classes fixed the genus:
`Money` (integer minor units, currency-checked adds) made the negative unrepresentable, and
`proration()` returns `Result<Money, DomainError>` so the rare legit negative is an explicit
`REFUND_NOT_SUPPORTED` (`402`) instead of a crash. The `23514` alert for this path never fired
again.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Construct money/quantities only through factories | `let seats = row.seats as number` everywhere |
| Share limit constants between DTO and value object | Hardcode `500` in two places |
| Keep rule-errors (`OUT_OF_RANGE`) distinct from world-errors (`QUOTA_EXCEEDED`) | One `SEATS_ERROR` for both |
| Alert on constructor invariant breaches from internal code | Blame the user with a `422` |

## Common mistakes

- **Float money** — rounding drift becomes data corruption; use minor units.
- **Mutable value objects** — `seats.value++` defeats the whole pattern; freeze them.
- **Constructor calling the DB for a uniqueness check** — that is a domain-service rule (18.3),
  not an invariant.
- **Dropping `details` in the transport mapper** — clients fall back to parsing prose.

## Checklist

- [ ] Money/quantities/dates are value objects with factory-returned results.
- [ ] Limits are constants on the type, reused by validation and domain.
- [ ] Every constructor failure has a code + category + details.
- [ ] Registry rows exist before first emission; transport mapper is registry-driven.
- [ ] Internal invariant breaches alert instead of rendering as user errors.

## Related

- [Entitlement, Lifecycle, and Webhook Examples](./02-entitlement-lifecycle-and-webhooks.md)
- [Domain Services, Aggregates, and DDD](../02-deep-dive/01-domain-services-aggregates-and-ddd.md)
- [Validation DTO → 422 Envelope](../../17-input-validation-error-handling/03-practical-examples/01-create-project-dto-to-422-envelope.md)
- [Chapter 6 — Designing the Application's Error Model](../../../part-03-error-models/06-designing-the-applications-error-model/README.md)
