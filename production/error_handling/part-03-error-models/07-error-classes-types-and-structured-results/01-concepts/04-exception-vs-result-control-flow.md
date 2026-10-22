# Exception vs Result Control Flow

> Part III · Chapter 7 · Sections 7.11–7.13 · _Estimated reading time: 17 min_
> **Prerequisite:** [Result Types and Algebraic Data Types](./03-result-types-and-adts.md)

## In one sentence

Exceptions are an **out-of-band jump** to the nearest handler, while results are **in-band values**
that flow through the normal return path — and the right choice depends on whether the failure is
expected and locally recoverable or unexpected and boundary-handled.

## Why this matters in production

The same feature can be written with either mechanism, but mixing them without a rule produces the
worst of both: business logic hidden in catch blocks, and `Result` values that callers ignore. A
stated convention — "expected failures return `Result`; unexpected failures throw; translate at the
boundary" — makes control flow predictable and reviewable.

## The two control flows (7.11)

```text
EXCEPTIONS                              RESULTS
call() ──▶ call() ──▶ throw ──╮         call() ──▶ Ok(v) ──▶ continue
                              │
            (unwinds stack)   │         call() ──▶ Err(e) ──▶ must handle
                              ▼
                        nearest catch
```

- **Exceptions** unwind the stack to the nearest `try`. They are *implicit*: a call that can throw
  looks identical to one that cannot. Great for unexpected failures and deep propagation; poor for
  ordinary control flow (they bypass signatures and exhaustiveness).
- **Results** return through the normal path. They are *explicit*: the type says a failure is
  possible. Great for expected outcomes; verbose when a failure is far from where it is handled.

## The decision rule (7.12)

| Question | If yes → |
| -------- | -------- |
| Is this an expected outcome of normal operation? | `Result` |
| Can the immediate caller act on it locally? | `Result` |
| Is it a validation/business rule failure? | `Result` (or a typed return) |
| Is it a bug / broken invariant? | Exception (fail fast) |
| Is it an infrastructure/unexpected runtime failure far from a meaningful handler? | Exception |
| Would threading it through 8 layers add only noise? | Exception (catch at boundary) |

A compact mnemonic: **"Expected = value, unexpected = throw."**

```ts
// Expected → Result
function findByEmail(email: string): Result<User, "NOT_FOUND"> { /* ... */ }

// Unexpected → throw
function assertInvariant(cond: boolean, msg: string): asserts cond {
  if (!cond) throw new InvariantError("INTERNAL_INVARIANT", msg);
}
```

## Choosing a consistent approach (7.12)

Pick a **primary** convention and a **boundary rule**. Three workable profiles:

| Profile | Domain | Infrastructure | Transport | Notes |
| ------- | ------ | -------------- | --------- | ----- |
| **A. Exception-first** | throws typed errors | throws typed errors | global handler | Most JS/Java/Node shops |
| **B. Result-first** | returns `Result` | returns/throws wrapped | unwraps to response | FP-leaning, TS/Rust/Go |
| **C. Mixed** | `Result` for expected | exceptions for infra | translate both | Common in large TS apps |

Profile C is common and fine **if the boundary is explicit**: expected failures are `Result`; native
and unexpected errors are exceptions; the transport/application boundary converts both into one
response. The failure mode is not mixing — it is mixing **without a rule**.

## Hybrid approaches (7.13)

A practical hybrid:

1. **Domain**: return `Result<T, DomainError>` for business/validation outcomes.
2. **Application service**: orchestrate; convert a `Result.Err` into either a recoverable response
   or a thrown application error when the failure is unrecoverable here.
3. **Infrastructure adapters**: catch native/driver errors and either return `Err(InfraError)` or
   throw a wrapped `InfrastructureError` (team's choice — but consistent).
4. **Transport boundary**: a single global handler maps *any* escaping error to the external
   contract, and unwraps `Result` if a handler returns one.

```ts
// Application service: unwrap Result, escalate what it cannot recover.
async function inviteMember(cmd: InviteMember): Promise<Result<Member, InviteError>> {
  const user = await repo.findByEmail(cmd.email);
  if (user.ok) return err({ code: "EMAIL_TAKEN", email: cmd.email });

  const created = await repo.create(cmd);          // may throw InfrastructureError
  if (!created.ok) throw created.error;            // unexpected here → boundary handles
  await mailer.sendInvite(created.value);          // may throw → boundary handles
  return ok(created.value);
}
```

```ts
// Transport boundary: one place converts everything.
async function handler(req: Request): Promise<Response> {
  const result = await inviteMember(parse(req));
  if (result.ok) return json(200, { id: result.value.id });
  return problemResponse(result.error);            // business result → 4xx
  // thrown InfrastructureError → caught by global handler → 5xx
}
```

The rule is **one conversion point per direction**. Never half-unwrap a `Result` and let the rest
throw `undefined`.

## When each is clearly wrong

- **Exceptions for ordinary flow**: using a thrown "not found" as a loop control mechanism; slow
  (stack capture) and invisible.
- **Results for bugs**: `Result<T, Bug>` forces callers to handle conditions that should never
  occur, adding noise and hiding real defects.
- **Mixing with no rule**: one module throws a `NotFoundError`, another returns `Err("NOT_FOUND")`;
  the boundary handles only one shape.

## Worked example

```ts
// BAD: exception-driven business flow
function applyDiscount(order: Order): void {
  if (order.total < 100) throw new NoDiscountError(); // expected, but thrown
  order.total *= 0.9;
}

// GOOD: expected failure as a value
function applyDiscount(order: Order): Result<Order, { code: "NO_DISCOUNT_ELIGIBLE" }> {
  if (order.total < 100) return err({ code: "NO_DISCOUNT_ELIGIBLE" });
  return ok({ ...order, total: order.total * 0.9 });
}
```

The second version cannot be silently ignored, does not rely on a catch to detect a normal
condition, and returns in O(1) without capturing a stack.

## Key data / numbers

- **Stack capture cost:** constructing an `Error` (which captures a stack) is markedly more
  expensive than returning a value; avoid exceptions in hot loops and high-volume validation.
- **High-volume business errors** (e.g. validation on millions of requests) benefit most from
  `Result` because they are frequent and expected (Chapter 57).
- **`Promise.allSettled`** and Go's `(T, error)` are language-provided in-band failure forms.
- **Global handlers** catch only **escaping** errors; a swallowed exception or an ignored `Err`
  never reaches them — the basis of the "success-shaped failure" anti-pattern.

## Real-world use case — WebhookIngest

Acme's `WebhookIngest` treated duplicate events as expected but threw a `DuplicateEventError`,
caught it, and returned `200`. A new developer refactored the catch away; duplicates then hit
`500` and triggered Stripe retries, amplifying traffic. After switching to a `Result<Processed,
IngestOutcome>` with explicit `duplicate | ignored | processed` variants, the outcome was visible in
the signature and could not be accidentally removed. Stripe retry storms stopped.

## Trade-offs

| Mechanism | In type signature | Propagation | Cost | Best for |
| --------- | ----------------- | ----------- | ---- | -------- |
| Exception | ❌ (hidden) | Automatic, deep | Stack capture | Unexpected, boundary-handled |
| `Result` | ✅ | Manual (`?`/`flatMap`) | Cheap | Expected, locally handled |
| Hybrid | Mixed, rule-based | Both | Both | Large layered apps |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| "Expected = value, unexpected = throw" | Throw for ordinary not-found/validation flow |
| State the boundary where conversion happens | Half-unwrap a `Result`, let the rest throw |
| Use `Result` in hot validation paths | Use exceptions as loop control |
| Keep one conversion point per direction | Convert in three different places |

## Common mistakes

- **Exception-driven business flow** — invisible, slow, easily refactored away.
- **Ignored `Err`** — the success-shaped-failure anti-pattern.
- **No boundary rule** — two dialects collide at the edge.
- **`Result` for bugs** — noise that hides real defects.

## Checklist

- [ ] Is there a documented rule for expected vs unexpected failures?
- [ ] Is the `Result`/exception conversion boundary explicit and singular?
- [ ] Are high-volume expected failures modeled as values?
- [ ] Can an ignored `Err` be detected (lint/exhaustiveness)?
- [ ] Are bugs allowed to throw and fail fast?

## Related

- [Result Types and Algebraic Data Types](./03-result-types-and-adts.md)
- [Hierarchies, Composition, and Naming](./05-hierarchies-composition-and-naming.md)
- [Chapter 12 — Exception Propagation and Control Flow](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
