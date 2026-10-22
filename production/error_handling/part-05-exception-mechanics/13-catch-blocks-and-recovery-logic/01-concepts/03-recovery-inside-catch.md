# Recovery Inside Catch

> Part V · Chapter 13 · Sections 13.6, 13.7, 13.8, 13.14, 13.15, 13.16 · _Estimated reading time: 18 min_
> **Prerequisite:** [Catching Specific Types and Categories](./02-catching-specific-types-and-categories.md)

## In one sentence

Recovery inside a catch block must **check its preconditions, leave state valid, and be explicit
about whether it recovers, partially recovers (rethrows), translates to a domain result, or
terminates** — never assume recovery is safe just because it is possible.

## Why this matters in production

Recovery bugs are the worst class: they turn a clean failure into corrupted data. Retrying an
operation that already had side effects double-charges a card. "Recovering" a read from a
connection that is actually dead returns garbage. Translating a partial recovery into a plain
success hides the part that did not finish. Recovery is powerful and dangerous in equal measure.

## Core concept

Four distinct outcomes for a catch block:

| Outcome | When | Caller sees |
| ------- | ---- | ----------- |
| **Full recovery** | Operation completed via an alternative | Success |
| **Partial recovery + rethrow** | Some work redone/undone, but op still failed | Failure (with notes) |
| **Translate** | Recovered enough to classify; map to domain result | A typed failure |
| **Terminate** | State cannot be trusted | Process/request abort |

### Recovery inside catch (13.6)

Recovery means: retry, fallback to an alternative, use a cache, or compensate. Each requires that
you **know the operation's side-effect state**. If you cannot tell whether the first attempt
committed, retrying may duplicate (Chapter 28 idempotency).

### Rethrow after partial recovery (13.7)

If you undo one step but cannot complete the whole operation, the operation is still failed. Rethrow
— do not report success. Note what was already done/undone so the caller and logs know.

### Translate to domain result (13.8)

At a domain boundary, a caught infrastructure error becomes a **domain outcome**: `NotFound`,
`Conflict`, `InsufficientFunds`. This is translation (Chapter 16), and the original must be kept as
cause for observability.

### Recovery preconditions (13.14)

State the conditions under which recovery is valid, and check them:

- **Idempotency** — is a retry safe? (idempotency key present / operation naturally idempotent)
- **Resource liveness** — is the connection/transaction still usable?
- **State consistency** — has the operation partially mutated anything?
- **Budget** — is there time and retry budget left?

### Recovery not corrupting state (13.15)

Recovery must preserve invariants. Before recovering, ensure any partial mutation is rolled back
or bracketed, so the recovered path starts from a known-good state.

### Recovery vs propagation vs termination (13.16)

```text
Can I complete the operation safely?      ──yes──▶ recover
Cannot complete, but state is safe?       ──yes──▶ translate/rethrow
State is unknown or corrupt?              ──yes──▶ terminate (fail-fast, alert)
```

## How it works (mechanics)

A safe retry-recovery, step by step:

1. **Classify** the caught error: transient and idempotent?
2. **Verify preconditions**: retry budget > 0, resource alive, no partial commit.
3. **Reset** to a known-good state (rollback transaction, re-acquire connection).
4. **Retry** the *same logical operation* (not a hand-rolled partial re-do).
5. On success → return success. On repeated failure → propagate the **final** error with the
   original cause and attempt count (Chapter 27.19).

```text
catch transient:
  if not idempotent: terminate with clear message
  if budget exhausted: rethrow final error
  rollback(); sleep(backoff); attempts++
  goto retry
```

## Worked example

`Checkout` charge with a timeout. The charge is remote and **not** safely retryable without an
idempotency key — so recovery must verify that first.

```ts
async function chargeWithRecovery(cmd: CheckoutCmd) {
  let attempt = 0;
  while (true) {
    attempt++;
    try {
      return await gateway.charge(cmd.payment, { idempotencyKey: cmd.idempotencyKey });
    } catch (err) {
      if (!isTransient(err)) throw err;                 // permanent → propagate

      if (!cmd.idempotencyKey) {                        // R14: precondition
        throw new ChargeUnsafeToRetry({ cause: err });  // ambiguous outcome risks double charge
      }
      if (attempt >= 3) {
        throw new ChargeFailed(cmd.payment.id, { cause: err, attempts: attempt }); // final
      }
      await sleep(backoffWithJitter(attempt));          // bounded backoff (Ch. 27)
    }
  }
}
```

Partial recovery + rethrow, with explicit bookkeeping:

```ts
async function reserveThenCharge(cmd: CheckoutCmd) {
  const reservation = await inventory.reserve(cmd.items); // side effect #1
  try {
    return await chargeWithRecovery(cmd);
  } catch (err) {
    // Partial recovery: undo #1, then rethrow — the operation is still failed.
    try {
      await inventory.release(reservation.id);
    } catch (releaseErr) {
      throw new CheckoutFailed("charge failed; inventory release ALSO failed", {
        cause: err,
        suppressed: releaseErr, // keep both (Ch. 14.13)
      });
    }
    throw err; // charge remains the primary failure
  }
}
```

Translation to a domain result:

```ts
function toDomain(err: unknown): CheckoutOutcome {
  if (err instanceof InventoryShortage) return { type: "out_of_stock" };
  if (err instanceof CardDeclined) return { type: "payment_declined", reason: err.reason };
  throw err; // unknown stays an error, not a domain outcome
}
```

## Key data / numbers

- **Idempotency key**: required to retry a payment safely; Stripe uses the `Idempotency-Key`
  header and caches the result for 24 hours.
- **Retry budget**: cap attempts (commonly 3–5) and total time; unlimited retries is a storm
  (Chapter 27).
- **Backoff**: exponential with jitter; honour `Retry-After` on `429`/`503`.
- **Top-level retry ownership**: exactly one layer; nested retries multiply attempts (e.g. 3×3=9).
- **Transaction rollback before retry**: a serialization failure (`40001`) requires rolling back
  the transaction before re-running.

## Real-world use case — Acme SaaS

Acme's `Checkout` retried gateway timeouts without an idempotency key. A timeout is *ambiguous* —
the charge may have succeeded. On the second attempt, some customers were charged twice. The fix:
every charge carries a client-generated idempotency key, and a timeout without a key is treated as
**unsafe to retry** (fail with a clear "outcome unknown" status and reconcile asynchronously). The
duplicate-charge rate went to zero.

## Trade-offs

| Recovery | Safe when | Risky when |
| -------- | --------- | ---------- |
| Retry | Idempotent + transient + budget | Non-idempotent or ambiguous outcome |
| Fallback (cache/alternate) | Data acceptable if stale | Fallback masks a serious failure |
| Compensation (undo) | Undo is itself idempotent | Undo fails or partially applies |
| Translate | Boundary with a stable contract | Domain can no longer act on the error |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Verify idempotency before retrying | Retry charges/creates blindly |
| Roll back before re-running | Retry on top of a dirty transaction |
| Rethrow after partial recovery | Report success after undoing a step |
| Attach the cleanup failure as suppressed | Lose the original when cleanup fails |
| Bound attempts and time | Retry until "it works" |

## Common mistakes

- **Retrying a non-idempotent operation** — duplicate side effects.
- **Reporting success after partial recovery** — hides the unfinished part.
- **Retrying without resetting state** — the retry fails for the same stale reason.
- **Treating "I caught it" as "I recovered it"** — a catch is not a fix.
- **Recovering without checking the resource is alive** — writing to a dead connection.

## Checklist

- [ ] Every recovery names its preconditions and checks them.
- [ ] Retries are idempotent (key or naturally).
- [ ] State is reset to known-good before re-running.
- [ ] Partial recovery rethrows; it does not report success.
- [ ] Recovery failures are attached as suppressed, not thrown over the primary.

## Related

- [Catch Anti-Patterns](./04-catch-anti-patterns.md)
- [Recovery Failure and Recursion](../02-deep-dive/02-recovery-failure-and-recursion.md)
- [Retry Policies (Part XI)](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Idempotency and Duplicate-Operation Safety (Part XI)](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
