# Ambiguous Commits and Idempotent Retries (23.11–23.14)

> Part IX · Chapter 23 · Sections 23.11–23.14 · _Estimated reading time: 22 min_
> **Prerequisite:** [Retry Eligibility and Locking Strategies](./03-retry-eligibility-and-locking-strategies.md)

## In one sentence

When the connection dies during `COMMIT`, the result is **neither success nor failure but
unknown**, and the only safe way out is to **read back a unique marker** and make every retry
idempotent.

## Why this matters in production

This is where money is lost. Stripe captures a payment, the database commits the order, and the
socket dies before the acknowledgment reaches your app. Your code sees an error and retries:
now there are two orders, or two charges, or the customer is billed for an order you marked
failed. The same shape appears in `WebhookIngest` (event applied twice), `ExportJob` (duplicate
rows in S3), and `AgentRun` (a tool side effect applied twice). Ambiguity is not rare — it is a
normal consequence of a network boundary, and it must be **designed for**, not hoped away.

## Core concept

```text
Client                         Server
  │  INSERT …                    │
  │  COMMIT ──────────────────▶  │  writes WAL, fsync, commits
  │                              │
  ✗  socket dies ◀───────────────┘  (ack never arrives)

Client's knowledge:  UNKNOWN
Server's state:      COMMITTED (probably) or NOT COMMITTED (rare)
```

| Signal | Meaning | Correct action |
| ------ | ------- | -------------- |
| `COMMIT` returns OK | committed | return success |
| `COMMIT` returns constraint error | **not** committed | translate, no retry |
| Connection lost during `COMMIT` (`08006`, `2013`) | **unknown** | read-back by unique marker |
| `08007` `transaction_resolution_unknown` | **unknown by definition** | read-back, then decide |
| Client-side deadline while commit in flight | **unknown** | read-back |
| Process crash after commit | committed, caller gone | reconciliation / replay |

**The only resolution is a read.** The marker must be something you wrote **inside the same
transaction**, so its presence is proof the commit applied.

## How it works (mechanics)

### 23.11 Lost connection during commit

The driver cannot tell whether the server committed. Some drivers surface a generic connection
error; some expose `08007`. Do **not** map this to `DB_UNAVAILABLE` and retry the write.

### 23.12 Ambiguous outcomes

Define a third state explicitly:

```ts
type CommitOutcome<T> =
  | { status: "committed"; value: T }
  | { status: "not_committed"; error: DomainError }
  | { status: "unknown"; resolution: () => Promise<CommitOutcome<T>> };
```

Resolution procedure:

1. Reconnect (new connection, new transaction).
2. Query **by a unique business/idempotency key** written in the original transaction.
3. If the row exists → `committed`; return the stored result.
4. If the row does not exist and enough time has passed for the original to be rolled back →
   `not_committed`; retrying is now safe.
5. If you cannot determine it → leave it `unknown`, surface a `202`/`503`, and reconcile
   asynchronously. **Never** guess "failed" and retry a charge.

### 23.13 Idempotency in retries

Three complementary tools:

| Tool | Mechanism | Best for |
| ---- | --------- | -------- |
| **Idempotency key** | client-generated `Idempotency-Key` stored with the result | HTTP writes, payments |
| **Natural unique constraint** | `UNIQUE(tenant_id, external_id)` | webhooks, imports |
| **Read-back marker** | `SELECT ... WHERE request_id = $1` | resolving unknown commits |

The key must be **stored in the same transaction as the effect**. A key written *after* commit
is useless for resolving ambiguity.

### 23.14 Preventing duplicate side effects

Database transactions cannot cover Stripe, S3, email, or queues. For each external effect:

- give it its **own idempotency key** (Stripe supports `Idempotency-Key`; S3 uses deterministic
  object keys; email uses a dedupe record);
- or perform it via the **outbox** so it is retried exactly as many times as the consumer can
  dedupe;
- and record **which effects were applied** so compensation knows what to undo.

## Worked example

```python
def place_order(tx, req) -> Order:
    # The idempotency record and the order commit together.
    tx.execute("""
        INSERT INTO idempotency_keys (key, request_hash, state)
        VALUES (%s, %s, 'in_progress')
        ON CONFLICT (key) DO NOTHING
    """, (req.key, req.hash))
    if tx.rowcount == 0:
        row = tx.execute("SELECT state, response FROM idempotency_keys WHERE key=%s",
                         (req.key,)).fetchone()
        if row.state == "completed":
            return reconstruct(row.response)     # replay
        raise DomainError("REQUEST_IN_PROGRESS", http=409)

    order = tx.execute("INSERT INTO orders (...) VALUES (...) RETURNING *")
    tx.execute("UPDATE idempotency_keys SET state='completed', response=%s WHERE key=%s",
               (serialize(order), req.key))
    return order


def place_order_with_resolution(pool, req) -> Order:
    try:
        with pool.transaction() as tx:
            return place_order(tx, req)
    except DriverError as exc:
        if not is_ambiguous_commit(exc):         # 08006/08007/2013 during COMMIT
            raise classify(normalize(exc), resource="orders:create")
        # UNKNOWN: reconnect and resolve by key. Never blind-retry.
        with pool.transaction() as tx:
            row = tx.execute(
                "SELECT state, response FROM idempotency_keys WHERE key=%s", (req.key,)
            ).fetchone()
        if row and row.state == "completed":
            return reconstruct(row.response)
        if row and row.state == "in_progress":
            raise DomainError("REQUEST_IN_PROGRESS", http=409, transient=True)
        # No row: the original transaction did not commit. Safe to retry once.
        with pool.transaction() as tx:
            return place_order(tx, req)
```

```text
Trace of an ambiguous checkout:
  INSERT orders ... ; INSERT idempotency_keys ... ; COMMIT
  ✗ connection reset → is_ambiguous_commit = true
  reconnect → SELECT idempotency_keys WHERE key='ord_9f2'
  → state='completed' → return the SAME order (no duplicate)
```

## Key data / numbers

- `08007 transaction_resolution_unknown` is the standard code for this state.
- Stripe accepts an **`Idempotency-Key`** header and replays the original response for **24
  hours** by default — reuse one key per logical operation, never per attempt.
- Resolution window: if your read-back runs **before** the original transaction is resolved,
  you may see neither row nor commit. Bound it with a short delay and a second read, then go
  `unknown`.
- Store idempotency records with a **TTL** (commonly 24 h–7 days) and purge them deliberately.
- `unknown` must be **observable** (metric + log) — a rising rate means network or DB instability.

## Real-world use case — Acme SaaS

During a failover, `Checkout` lost the acknowledgment for a `COMMIT` that had in fact succeeded.
The service retried and created a second order; the customer was charged twice. The fix was an
`idempotency_keys` table written **inside** the order transaction, a distinct `unknown` outcome
mapped to `08006`/`08007`/`2013`, and a read-back resolver before any retry. The next failover
produced zero duplicate orders, and support stopped issuing refunds for a bug that had looked
like "random double billing".

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Read-back by key | resolves ambiguity correctly | extra query, needs a key | any write with an external ack |
| Blind retry | simple | duplicate charges/orders | never |
| Treat unknown as failure | easy | loses committed writes | never for money |
| Treat unknown as success | easy | invents writes when uncommitted | never |
| Async reconciliation | decouples resolution | eventual, needs a job | high-volume payments |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Model `unknown` as a third outcome | Collapse unknown into success or failure |
| Write the idempotency record in the same txn | Write the key after commit |
| Resolve by unique key before retrying | Retry a charge after a lost ack |
| Reuse one idempotency key per operation | Generate a new key per attempt |
| Alert on ambiguous-commit rate | Ignore it as a network blip |

## Common mistakes

- **Retrying after `COMMIT` connection loss** — the classic double charge.
- **Idempotency key generated inside the retry loop** — every attempt is "new".
- **Reading from a replica** to resolve an unknown commit — replication lag says "not there".
- **No TTL/purge** on idempotency records — the table grows forever.
- **Returning `500` for `unknown`** without reconciliation — the write may be applied and lost
  from the user's view.

## Checklist

- [ ] Every non-idempotent write has an idempotency key or unique marker.
- [ ] The marker is committed atomically with the effect.
- [ ] `08006`/`08007`/`2013` during commit map to `unknown`, not `failed`.
- [ ] Resolution reads from the **primary**, never a replica.
- [ ] `unknown` has a metric, a log, and a reconciliation path.
- [ ] Idempotency records have a retention policy.

## Related

- [Ambiguous Commit Outcomes — deep dive](../02-deep-dive/01-ambiguous-commit-outcomes.md)
- [After-Commit Failures, Outbox, and Cross-Store (23.15–23.20)](./05-after-commit-failures-outbox-and-cross-store.md)
- [Idempotency and Duplicate-Operation Safety (Ch. 28)](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Outbox and Compensation in Code](../03-practical-examples/02-outbox-and-compensation-in-code.md)
