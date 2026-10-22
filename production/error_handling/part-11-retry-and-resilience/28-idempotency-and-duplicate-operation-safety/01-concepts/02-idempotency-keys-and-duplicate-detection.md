# Idempotency Keys and Duplicate Detection

> Part XI · Chapter 28 · Sections 28.4–28.9 · _Estimated reading time: 22 min_
> **Prerequisite:** [What Idempotency Means](./01-what-idempotency-means.md)

## In one sentence

An idempotency key is a **unique, stable token attached to a request**; the server stores the key
with the operation's state and result, rejects concurrent duplicates, and replays the stored success
for later ones.

## Why this matters in production

The key is a contract with three parts: **who creates it**, **what it is scoped to**, and **how long
it lives**. Get any part wrong and the dedup layer either misses duplicates (key regenerated),
collides across tenants (global scope), or forgets results too early (TTL shorter than the retry
window). The implementation is small but the edge cases are where double charges live.

## 28.4 — Keys

### Who generates the key

| Generator | When | Note |
| --------- | ---- | ---- |
| Client | Before the first attempt | Best for user-initiated writes |
| Server (on form load) | Page render | Returned to the client, then echoed |
| Service (for internal calls) | Before calling a dependency | Derived from a business id |
| Never: per attempt | — | Regenerating defeats dedup |

The key must be created **once per logical operation** and reused by every retry of that operation.

### Key format and scope

- Opaque string, typically **UUIDv4** or a ULID; 16–64 characters.
- Scope it to the **tenant and operation**: `(tenant_id, key)` is unique.
- Never trust a client key as authorization; always combine with the authenticated tenant.
- Do not derive the key from mutable input (e.g. a timestamp), or retries won't match.

```http
POST /v1/checkout/42/pay
Idempotency-Key: 9f1c2e7a-3b44-4d1e-9a0f-6c2b8d1e5f30
```

Stripe popularized the `Idempotency-Key` header; it is a de facto convention, not a universal
standard.

## 28.5 — Duplicate detection

The core algorithm is a **unique constraint plus a stored result**:

```text
BEGIN
  INSERT INTO idempotency_keys (tenant_id, key, payload_hash, state)
  VALUES ($1, $2, $3, 'in_progress')
  ON CONFLICT (tenant_id, key) DO NOTHING
  RETURNING id;

  IF inserted THEN
      perform the side effect
      UPDATE ... SET state='completed', status=..., body=...
      COMMIT
  ELSE
      read the existing row
      IF payload_hash differs -> 422 KEY_REUSED_WITH_DIFFERENT_PAYLOAD
      IF state='completed'    -> replay stored status + body
      IF state='in_progress'  -> 409 CONFLICT_IN_PROGRESS (or wait/poll)
      IF state='failed'       -> apply the failure contract (28.10)
  END IF
```

The `INSERT ... ON CONFLICT` is what makes concurrent requests safe. A read-then-write check races:
two requests can both read "absent" and both proceed.

### Detection outcomes

| Existing state | Duplicate request response |
| -------------- | -------------------------- |
| `completed` | Replay original status and body |
| `in_progress` | `409` or block briefly, then replay |
| `failed_retryable` | Allow retry (same key) |
| `failed_terminal` | Replay the terminal failure |
| different payload | `422` key reuse error |

## 28.6 — Storage and expiration

### What to store

| Field | Purpose |
| ----- | ------- |
| `tenant_id`, `key` | Unique identity |
| `payload_hash` | Detect reuse with different content |
| `state` | `in_progress`, `completed`, `failed` |
| `status_code` | Replay the original HTTP status |
| `response_body` | Replay the original response |
| `resource_id` | Link to the created/charged resource |
| `created_at`, `expires_at` | TTL and auditing |
| `request_id` | Trace correlation |

### Where to store it

| Store | Pros | Cons |
| ----- | ---- | ---- |
| Postgres (same DB) | Transactional with the side effect | Adds write load |
| Redis | Fast, TTL built in | Not transactional with DB |
| DynamoDB | Managed TTL, scalable | Separate consistency domain |
| Provider-native | Provider handles it | Only for that provider |

**Preferred:** the same database as the side effect, in the same transaction, so "key recorded" and
"charge created" commit atomically. Redis is acceptable if you can tolerate reconciliation on the
rare gap.

### TTL

```text
key_ttl >= max_retry_window + reconciliation_window + safety_margin
```

A common default is **24 hours**. That comfortably covers client retries, provider retry windows,
and overnight reconciliation. TTLs shorter than the retry window produce duplicate effects after
expiry; TTLs much longer increase storage and privacy obligations.

## 28.7 — Concurrent same-key requests

Two requests with the same key arrive within milliseconds. Exactly one may perform the side effect.

Options for the loser:

| Strategy | Behavior | Use when |
| -------- | -------- | -------- |
| **Fail fast** | Return `409 Conflict` / `409 IN_PROGRESS` | Client can retry later |
| **Wait** | Poll the row for a short time, then replay | Latency-sensitive clients |
| **Replay-on-commit** | Hold the connection until the first commits | Low concurrency, short ops |

Never let the loser proceed "because the first might fail." If the first fails retryably, the key
state changes to `failed_retryable` and the loser may retry under the same key.

```ts
// Pseudocode for the loser path.
const row = await keys.get(tenantId, key);
if (row.state === "in_progress") {
  return { status: 409, code: "REQUEST_IN_PROGRESS", retryAfterMs: 500 };
}
if (row.payloadHash !== hash(payload)) {
  return { status: 422, code: "KEY_REUSED_WITH_DIFFERENT_PAYLOAD" };
}
return { status: row.statusCode, body: row.responseBody };
```

## 28.8 — Replaying success

A duplicate of a completed operation must return the **original outcome**:

- same HTTP status (including `201`, `202`, or `200`);
- same body (resource id, amount, timestamps);
- a header indicating replay, e.g. `Idempotent-Replay: true`;
- no new side effect, no new timestamp.

```http
HTTP/1.1 201 Created
Idempotent-Replay: true
Content-Type: application/json

{ "id": "ch_8f2c", "amount": 5000, "status": "succeeded" }
```

Replaying a failure is different: a terminal failure may be replayed as-is, while a retryable failure
may allow re-execution (28.10).

## 28.9 — Reused key with a different payload

A client that reuses a key with different content is either buggy or attacking. The server must
detect and reject it.

```text
key = K, payload_hash = H1  → completed
key = K, payload_hash = H2  → 422 KEY_REUSED_WITH_DIFFERENT_PAYLOAD
```

Hash a **canonical** representation of the semantically relevant fields (amount, currency, customer),
not raw bytes. Ignore headers, timestamps, and transport metadata that legitimately vary between
retries.

```python
import hashlib, json

def payload_hash(body: dict) -> str:
    canonical = json.dumps(
        {k: body[k] for k in ("amount", "currency", "customer_id", "cart_id")},
        sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode()).hexdigest()
```

Return `422 Unprocessable Content` with a stable code; never silently execute the different payload.

## Worked example — the full duplicate path

```text
1. POST /pay  key=K  hash=H   → INSERT(K, H, in_progress) wins → charge created → completed
2. POST /pay  key=K  hash=H   → conflict → completed → replay 201 + original body
3. POST /pay  key=K  hash=H2  → conflict → hash mismatch → 422 KEY_REUSED
4. POST /pay  key=K2 hash=H   → INSERT wins → new logical operation (new charge)
```

Note step 4: a new key is a **new operation**, even with an identical payload. That is intentional —
the client is asserting "this is a separate intent."

## Key data / numbers

- `Idempotency-Key` header: opaque, commonly UUID; **16–64 chars**.
- Stripe retains idempotency keys for **24 hours**.
- Default TTL: **24h**; range commonly 1h–7d depending on the operation.
- Concurrent duplicate response: `409`; payload mismatch: `422`.
- Replay header: `Idempotent-Replay: true`.
- Unique index: `(tenant_id, key)` or `(scope, key)`.

## Real-world use case — Acme SaaS

Acme's project-creation endpoint accepted an `Idempotency-Key` but implemented detection with a
`SELECT` followed by an `INSERT`. Under a client retry storm, two requests both saw "no row," both
inserted, and tenants ended up with duplicate projects. Replacing the check with a unique index and
`INSERT ... ON CONFLICT` fixed the race. They also added a payload hash after discovering that a
frontend bug reused one key for different project names, silently returning the first project for
every subsequent create. Both issues disappeared within a release.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| DB storage | Atomic with side effect | Extra writes |
| Redis storage | Fast, easy TTL | Cross-store gap |
| Wait on in-progress | Better UX | Ties up a connection |
| Fail fast on in-progress | Simple | Client must retry |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Unique-index the `(scope, key)` pair | Read-then-write check |
| Store status + body | Store only "seen" |
| Hash the semantic payload | Hash raw bytes |
| Return the original status | Return a fresh `200` |
| Scope keys per tenant | Use a global key namespace |
| Reject payload mismatch with `422` | Silently execute it |

## Common mistakes

- **Key regenerated per retry**, producing duplicates.
- **TTL shorter than the retry window**, so late retries re-execute.
- **No payload hash**, so a reused key silently maps to the wrong operation.
- **Concurrent loser proceeds anyway**, double-writing.
- **Replay changes timestamps/ids**, confusing clients and audits.

## Checklist

- [ ] Keys are generated once per logical operation.
- [ ] Keys are scoped by tenant and operation.
- [ ] A unique index enforces `(scope, key)`.
- [ ] The stored record includes state, status, body, and payload hash.
- [ ] Concurrent duplicates get `409` or wait, never execute.
- [ ] Completed duplicates replay the original response.
- [ ] Payload mismatch returns `422`.
- [ ] TTL covers the retry and reconciliation windows.

## Related

- [Idempotency Key Lifecycle](../02-deep-dive/01-idempotency-key-lifecycle.md)
- [Idempotency Key Store](../03-practical-examples/01-idempotency-key-store.md)
- [Failure Contracts and Uncertain Outcomes](./03-failure-contracts-and-uncertain-outcomes.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
