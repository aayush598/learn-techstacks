# Idempotency Key Lifecycle

> Part XI · Chapter 28 · Sections 28.4–28.10 · _Estimated reading time: 22 min_
> **Prerequisite:** [Idempotency Keys and Duplicate Detection](../01-concepts/02-idempotency-keys-and-duplicate-detection.md)

## In one sentence

An idempotency key moves through a small, explicit **state machine** — absent → in-progress →
completed / failed / unknown → expired — and every transition is a decision about whether a
duplicate may execute, replay, or be rejected.

## Why this matters in production

Most bugs in idempotency are lifecycle bugs, not storage bugs. A key stuck in `in_progress` after a
crash blocks retries forever. A key marked `completed` before the side effect commits loses work. A
key with no `unknown` state reports a pending payment as failed. Drawing the state machine first
makes these cases visible in review, before they become incidents.

## The states

```text
                          ┌──────────────────────────────┐
                          │            ABSENT            │
                          └──────────────┬───────────────┘
                                         │ claim (INSERT ... ON CONFLICT)
                                         ▼
                          ┌──────────────────────────────┐
              ┌──────────▶│         IN_PROGRESS          │
              │           │  owner=req_id, lease_until   │
              │           └───┬───────────┬──────────┬───┘
              │               │           │          │
              │      success  │   terminal│  crash / │
              │               ▼   failure │  timeout │
              │      ┌──────────────┐  ┌──▼──────────────┐
              │      │  COMPLETED   │  │ FAILED_TERMINAL │
              │      └──────┬───────┘  └────────┬────────┘
              │             │                   │
              │             │  retryable error  │
              │             ▼                   ▼
              │      ┌──────────────┐  ┌─────────────────┐
              │      │ (replay)     │  │ FAILED_RETRYABLE│
              │      └──────────────┘  └────────┬────────┘
              │                                  │ retry under same key
              │                                  └──────────▶ IN_PROGRESS
              │
              │  lease expires without completion
              │           ┌──────────────────────────────┐
              └───────────│           UNKNOWN            │
                          │  reconcile before retrying   │
                          └──────────────┬───────────────┘
                                         │ resolution
                          ┌──────────────┼──────────────┐
                          ▼              ▼              ▼
                     COMPLETED   FAILED_RETRYABLE  FAILED_TERMINAL

  All states ──(expires_at passes)──▶ EXPIRED / purged
```

## Transition table

| From | Event | To | Duplicate request behavior |
| ---- | ----- | -- | -------------------------- |
| absent | claim | `in_progress` | — |
| `in_progress` | duplicate arrives | `in_progress` | `409` or short wait |
| `in_progress` | success + commit | `completed` | replay status + body |
| `in_progress` | terminal error | `failed_terminal` | replay the error |
| `in_progress` | transient error | `failed_retryable` | allow retry under key |
| `in_progress` | crash / lease expiry | `unknown` | reconcile first |
| `failed_retryable` | retry | `in_progress` | — |
| `unknown` | reconcile: succeeded | `completed` | replay success |
| `unknown` | reconcile: not found | `failed_retryable` | allow retry |
| `unknown` | reconcile: failed | `failed_terminal` | replay failure |
| any | TTL passes | `expired` | treated as absent (new operation) |

## Claiming the key atomically

The claim must be a single atomic insert. This is the only reliable guard against concurrent
duplicates.

```sql
INSERT INTO idempotency_keys (tenant_id, key, payload_hash, state, owner, lease_until)
VALUES ($1, $2, $3, 'in_progress', $4, now() + interval '30 seconds')
ON CONFLICT (tenant_id, key) DO NOTHING
RETURNING id;
```

If no row is returned, the key already exists. Read it and apply the transition table. Do **not**
retry the insert in a loop hoping to win.

## Leases and crash recovery

A worker can die while holding `in_progress`. Without a lease, the key is stuck. Use a short lease and
a sweeper:

```text
lease_until = now() + max_expected_operation_time
sweeper: UPDATE ... SET state='unknown' WHERE state='in_progress' AND lease_until < now()
```

The lease must be **longer than the normal operation** (otherwise healthy work is marked unknown) and
**shorter than the client retry window** (otherwise retries are blocked too long). A range of 30s–5min
is common, depending on the operation.

> ⚠️ **Hazard.** A lease shorter than the provider call causes the sweeper to mark a still-running
> charge as `unknown`; a concurrent retry then races the original call. Set leases from the P99
> duration, not the average.

## TTL and expiry

```text
expires_at = created_at + ttl
ttl >= max_retry_window + reconciliation_window + margin
```

| Operation | Suggested TTL |
| --------- | ------------- |
| API create | 24h |
| Payment | 24h (matches common provider retention) |
| Refund | 7 days (finance reconciliation) |
| Job step | Duration of the job + 7 days |
| Webhook event | 7–30 days |

Expiry is **not** a state transition you perform on read; purge lazily or with a scheduled job.
Treat an expired key as absent, and accept that a very late duplicate may re-execute — which is why
the TTL must exceed every legitimate retry window.

## Replay semantics

Replay is not "return 200." It returns the **stored original outcome**:

```ts
function replay(row: KeyRow) {
  return {
    status: row.status_code,          // original, e.g. 201
    body: row.response_body,          // original body
    headers: { "Idempotent-Replay": "true" },
  };
}
```

Do not re-run validation, re-read the resource, or regenerate ids. The replay must be
indistinguishable from the first response except for the replay header and timing.

## Failure transitions in detail

### Transient before the side effect

The operation failed before any external effect. Record `failed_retryable`; the next request may
reuse the key.

### Transient after a partial side effect

The operation may have partially applied. Record `unknown`; reconcile before allowing a retry.

### Terminal

Validation, auth, or a business decline. Record `failed_terminal` with the status/body so duplicates
replay the same rejection. Do not allow a retry under the same key with the same payload.

### Different payload

Hash mismatch is not a state transition; it is a rejection (`422`). The existing key record is
unchanged.

## Worked example — a crash mid-charge

```text
t=0    claim K → in_progress, lease_until=t+45s
t=1    create local charge(pending, K)
t=2    provider charge succeeds
t=3    process crashes before marking completed
t=46   sweeper marks K → unknown
t=60   client retries with K
       → state=unknown → reconciler queries provider by K
       → provider returns succeeded
       → K=completed, charge=succeeded
       → replay original success
```

No second charge. Without the `unknown` state, the retry would either be blocked forever or would
re-execute.

## Key data / numbers

- Lease: **30s–5min**, derived from P99 operation duration.
- TTL: **24h** typical; payments commonly match provider retention (24h).
- Sweeper interval: 1–5 minutes.
- Concurrent duplicate: `409`; payload mismatch: `422`.
- Replay header: `Idempotent-Replay: true`.
- Reconciliation query: by your key or provider idempotency key.

## Real-world use case — Acme SaaS

Acme's key table had only two states: `in_progress` and `completed`. When a worker was killed during
a deploy mid-charge, the key stayed `in_progress` forever; every retry returned `409` until support
manually deleted the row. After adding a lease, an `unknown` state, and a reconciler, the same deploy
scenario self-healed within a minute: the sweeper marked the key unknown, the reconciler found the
provider charge, and the client received the original success.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Short lease | Fast recovery | False `unknown` on slow ops |
| Long lease | Fewer false unknowns | Blocked retries after crash |
| DB + same transaction | Atomic | Hard with external calls |
| Outbox + async | Reliable | Eventual, more moving parts |
| Long TTL | Safe retries | Storage, privacy |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Model `unknown` explicitly | Collapse it into failed |
| Use a lease + sweeper | Leave `in_progress` forever |
| Derive lease from P99 | Use the average duration |
| Store status + body | Store only a boolean |
| Reject payload mismatches | Overwrite the record |
| Purge expired keys lazily | Delete keys on failure |

## Common mistakes

- **Marking completed before commit**, losing work but blocking retry.
- **No lease**, so a crash blocks the key indefinitely.
- **Lease shorter than the operation**, causing false unknowns and races.
- **TTL shorter than provider retention**, allowing duplicates in the gap.
- **Replay re-executes validation**, returning a different error than the original.

## Checklist

- [ ] All states are modeled, including `unknown`.
- [ ] Claim is one atomic `INSERT ... ON CONFLICT`.
- [ ] Leases exist with a sweeper for crashed workers.
- [ ] Terminal failures are persisted and replayed.
- [ ] TTL exceeds retry + reconciliation windows.
- [ ] Replay returns the stored status and body.
- [ ] Payload mismatch is rejected without changing state.

## Related

- [Idempotency Keys and Duplicate Detection](../01-concepts/02-idempotency-keys-and-duplicate-detection.md)
- [Failure Contracts and Uncertain Outcomes](../01-concepts/03-failure-contracts-and-uncertain-outcomes.md)
- [Idempotency Key Store](../03-practical-examples/01-idempotency-key-store.md)
- [Distributed Idempotency and Storage](./02-distributed-idempotency-and-storage.md)
