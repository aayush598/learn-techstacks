# Primary vs Secondary Errors

> Part V · Chapter 14 · Sections 14.12–14.13 (mechanics) · _Estimated reading time: 18 min_
> **Prerequisite:** [Multiple Errors and Primary Preservation](../01-concepts/04-multiple-errors-and-primary-preservation.md)

## In one sentence

The **primary error** is the first failure and is what the caller must act on; every subsequent
failure in the same operation — cleanup, rollback, notification — is **secondary** and must be
attached (suppressed/joined/noted) so it informs without overwriting.

## Why this matters in production

Error ordering is a small decision with enormous operational consequences. Get it wrong and every
incident in a degraded window reports a misleading secondary message; the true cause is erased and
MTTR balloons. Get it right and the log reads as a story: *what failed, then what also failed while
cleaning up*.

## Core concept

A single operation can produce a **tree** of errors:

```text
Primary: CheckoutFailed (charging card)
├── Suppressed: rollback failed (connection lost)
├── Suppressed: notification failed (SMTP timeout)
└── Cause: GatewayHTTPError 502
       └── Cause: TLSHandshakeTimeout
```

Rules that define the tree:

1. **First failure is primary.** It represents the operation's outcome.
2. **Later failures are suppressed.** They are context, not the outcome.
3. **Cause chains nest within an error.** A primary may itself have a `cause` (the underlying
   reason) *and* suppressed siblings (other concurrent failures).
4. **Never reorder for "severity".** A scary cleanup error does not become primary.

### Multiple errors (14.12)

Two flavors:

- **Sequential** (body then cleanup): primary + suppressed.
- **Parallel** (N independent tasks): aggregate, typically with the first as primary and the rest
  joined, or a collection of results (Chapter 12.9).

## How it works (mechanics)

### Cause vs suppressed — the distinction

| Relationship | Meaning | Set by |
| ------------ | ------- | ------ |
| **cause** (`__cause__`, `%w`, `cause`, `getCause`) | "this happened *because of* that" | wrapping |
| **suppressed** (`getSuppressed`, `errors.Join`, notes) | "this *also* happened" | cleanup/aggregation |

A cause is a *vertical* link (deeper reason); suppressed errors are *horizontal* siblings (other
things that went wrong around the same time). Do not mix them up.

### Java: the reference implementation

```java
public void process() throws ServiceException {
    try {
        riskyWork();
    } catch (Exception primary) {
        try {
            releaseResources();
        } catch (Exception secondary) {
            primary.addSuppressed(secondary);      // horizontal sibling
        }
        throw primary;                              // vertical: primary propagates
    }
}
```

Try-with-resources applies the same rule automatically.

### Go: join siblings, wrap causes

```go
if err := work(); err != nil {
    primary := err                                   // "caused by" already inside via %w
    if rerr := cleanup(); rerr != nil {
        return errors.Join(primary, rerr)            // siblings joined
    }
    return primary
}
```

### Python: `__cause__` + `add_note`

```python
try:
    work()
except WorkError as primary:
    try:
        cleanup()
    except Exception as secondary:
        primary.add_note(f"cleanup also failed: {secondary!r}")  # 3.11+
    raise primary
```

### TypeScript: explicit field

```ts
catch (primary) {
  let suppressed: unknown[] = [];
  try { await cleanup(); }
  catch (e) { suppressed.push(e); }
  throw new OperationFailed("work failed", { cause: primary, suppressed });
}
```

## Worked example — before/after log views

**Before — cleanup overwrites the primary:**

```java
try {
    transferFunds();
} finally {
    conn.close();          // throws after a network failure
}
```

```text
SQLException: connection is closed
    at Connection.close (Connection.java:212)
```

The `transferFunds` failure is gone.

**After — primary leads, secondary attached:**

```java
try {
    transferFunds();
} catch (Exception primary) {
    try {
        conn.close();
    } catch (Exception secondary) {
        primary.addSuppressed(secondary);
    }
    throw primary;
}
```

```text
TransferFailed: transferring 4200 from acct 12 to acct 88
    at transferFunds (Ledger.java:41)
    Caused by: GatewayHTTPError: 502 Bad Gateway
        at Gateway.post (Gateway.java:77)
        Suppressed: SQLException: connection is closed
            at Connection.close (Connection.java:212)
```

Now the story reads: *the transfer failed because the gateway returned 502, and while cleaning up,
the connection close also failed.*

## Ordering rules (write these down)

| Situation | Primary | Secondary |
| --------- | ------- | --------- |
| body fails, cleanup fails | body | cleanup (suppressed) |
| body fails, cleanup succeeds | body | — |
| body succeeds, cleanup fails | cleanup | — (no primary existed) |
| parallel tasks, several fail | first/defined winner | others (joined) |
| rollback fails during a saga | original step failure | rollback failure (suppressed) |

## Key data / numbers

- **Java**: `getSuppressed()` returns an ordered array; try-with-resources adds the primary's
  close failure automatically. `initCause` is legacy; prefer constructors.
- **Go 1.20+**: `errors.Join` returns a multi-error; `errors.Is`/`As` traverse *all* children, so
  classification still finds the primary cause.
- **Python 3.11+**: `add_note` is free-form; `__cause__` is the cause link, `__context__` is the
  implicit one set during `except`/`finally`.
- **Cap suppressed lists** to keep logs bounded (e.g. first 10 + count).

## Real-world use case — Acme SaaS

Acme's `Checkout` saga had three compensating steps. When compensation for step 3 failed, the code
threw the compensation error and lost the original charge failure. Support saw "release reservation
failed" for incidents actually caused by a card-network outage. They restructured to keep the
charge failure as primary and attach each failed compensation as suppressed (with a cap), producing
one record that named both the cause and the cleanup fallout. Triage time fell sharply.

## Trade-offs

| Approach | Pros | Cons | When |
| -------- | ---- | ---- | ---- |
| Suppress secondary | Both preserved | Needs structured logging | Default |
| Log secondary only | Works everywhere | Not machine-parseable | Fallback |
| Throw combined multi-error | Single object | Larger type; reader must unpack | Aggregations |
| Throw secondary (wrong) | Simple | Erases primary | ❌ Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the first failure primary | Promote cleanup errors to primary |
| Distinguish cause from suppressed | Use `cause` for sibling failures |
| Cap the suppressed list | Attach unbounded errors |
| Make the log read top-down as a story | Emit several unrelated error lines |
| Preserve cause through wrapping | Replace the cause when rethrowing |

## Common mistakes

- **Plain `finally` that throws** — silently overwrites the primary.
- **Using `cause` for a sibling failure** — misrepresents the relationship.
- **Throwing the cleanup error because the connection "really died"** — the caller needed the
  operation outcome.
- **Dropping secondary errors entirely** — no record that cleanup failed.
- **Unbounded suppression** — one log line with thousands of children.

## Checklist

- [ ] The first failure is reported first.
- [ ] Cleanup/rollback failures are attached, not thrown over.
- [ ] Cause and suppressed are used correctly (vertical vs horizontal).
- [ ] Aggregations are capped.
- [ ] The log reads as a single coherent story.

## Related

- [Multiple Errors and Primary Preservation](../01-concepts/04-multiple-errors-and-primary-preservation.md)
- [Scoped Cleanup Mechanics](./01-scoped-cleanup-mechanics.md)
- [Errors During Cleanup (Part XXIII)](../../../part-23-special-cases/58-less-obvious-error-handling-scenarios/README.md)
- [Transaction and Rollback Error Handling (Part IX)](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
