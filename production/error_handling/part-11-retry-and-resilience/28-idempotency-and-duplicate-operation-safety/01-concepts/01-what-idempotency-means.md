# What Idempotency Means

> Part XI · Chapter 28 · Sections 28.1–28.3 · _Estimated reading time: 17 min_
> **Prerequisite:** [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)

## In one sentence

An operation is **idempotent** when applying it multiple times produces the same final state and
response as applying it once — and retries are only safe when that property holds or is simulated
with an idempotency key.

## Why this matters in production

The network cannot tell you the difference between "the request never arrived" and "the request
succeeded but the response was lost." Both look like a timeout. If you retry, one of those cases is
fine and the other is a duplicate. Idempotency is how you make both cases safe without giving up on
retries. Without it, every timeout on a write is a potential double charge, duplicate record, or
second email.

## 28.1 — The meaning

Formally, an operation `f` is idempotent if:

```text
f(f(x)) = f(x)
```

Applied to distributed systems:

| Property | Meaning |
| -------- | ------- |
| **Same final state** | Repeating the operation does not change the resource further |
| **Same observable result** | A duplicate returns the original outcome, not a new error |
| **No additional side effects** | No second charge, email, or row |

Idempotency is about **effect**, not about whether the request is accepted. A second `DELETE` may
return `404` or the original `204`; either is fine as long as no second deletion happens.

## 28.2 — Why retries need it

Consider a client that sends `POST /charges`, the server charges the card, and the response is lost
to a network reset. The client sees a timeout. Two choices:

```text
Retry without idempotency:
  client ── POST /charges ──▶ server ── charge #1 ✅
         ◀── timeout ───────
  client ── POST /charges ──▶ server ── charge #2 ❌ duplicate

Retry with an idempotency key:
  client ── POST /charges (key=K) ──▶ server ── charge #1 ✅, store K→result
         ◀── timeout ──────────────
  client ── POST /charges (key=K) ──▶ server ── lookup K → replay result ✅
```

The key converts "maybe it happened" into "we can find out and return the same answer."

### The three duplicate sources

| Source | Example |
| ------ | ------- |
| **Client retry** | Timeout, then retry |
| **Infrastructure retry** | Gateway, queue redelivery, SDK |
| **User action** | Double-click, resubmitted form |

All three are normal. Idempotency is the common defense.

## 28.3 — Idempotent vs not

### Naturally idempotent

| Operation | Why |
| --------- | --- |
| `GET`, `HEAD` | Read-only |
| `PUT /resource` with full state | Last write wins with the same state |
| `DELETE /resource/:id` | Deleting twice leaves it deleted |
| Set a field to an absolute value | `status = "paid"` |
| Upsert by natural key | `INSERT ... ON CONFLICT DO UPDATE` |

### Not naturally idempotent

| Operation | Why |
| --------- | --- |
| `POST /charges` | Creates a new charge each time |
| `POST /projects` | Creates a new project each time |
| Increment (`count = count + 1`) | Each call adds |
| `POST /emails` | Sends another email |
| Append to a log/stream | Adds another entry |
| Publish an event | Another event is emitted |

### Making a non-idempotent operation safe

You do not need to change the operation; you need a **deduplication layer**:

1. Client sends a unique key with the request.
2. Server records the key before performing the side effect.
3. On duplicate, the server returns the stored result instead of re-executing.

That is the entire idea behind 28.4–28.9.

## The ambiguous-success problem

The hardest case is not a clean failure. It is this:

```text
client → server: "charge $50"
server → provider: charged ✅
server → client: ✕ response lost
```

The client cannot know whether it was charged. The server *can* know if it recorded the outcome
transactionally with the charge. That is why the key and the side effect must be committed **together**
or reconciled afterward (28.15).

> ⚠️ **Hazard.** A retry without a key turns an ambiguous outcome into a *guaranteed* duplicate in
> the case where the first attempt succeeded.

## Worked example

```ts
// NOT idempotent: a retry appends a second row.
async function createProjectBad(name: string) {
  return db.insert("projects", { id: uuid(), name });
}

// Idempotent by natural key: same name in the same tenant yields one row.
async function createProjectUpsert(tenantId: string, slug: string, name: string) {
  return db.query(
    `INSERT INTO projects (id, tenant_id, slug, name)
     VALUES ($1, $2, $3, $4)
     ON CONFLICT (tenant_id, slug) DO UPDATE SET name = EXCLUDED.name
     RETURNING *`,
    [uuid(), tenantId, slug, name],
  );
}

// Keyed: arbitrary writes become safe even without a natural key.
async function createProjectKeyed(tenantId: string, key: string, name: string) {
  return idempotency.run(tenantId, key, () =>
    db.insert("projects", { id: uuid(), tenant_id: tenantId, name }),
  );
}
```

Prefer **natural keys** (`tenant_id`, `slug`) when they exist; use an **idempotency key** when the
operation has no natural identity.

## Key data / numbers

- HTTP methods considered idempotent by RFC 9110: `GET`, `HEAD`, `OPTIONS`, `TRACE`, `PUT`,
  `DELETE` (not `POST`, not `PATCH`).
- Common key TTL: **24 hours**; must exceed the maximum retry window.
- Stripe's idempotency keys are retained for **24 hours** by default.
- A duplicate should replay the original status code, not necessarily `200`.
- Store a **payload hash** alongside the key to detect reuse with different content.

## Real-world use case — Checkout

Checkout's "Pay now" button issued `POST /checkout/:id/pay`. A slow response led users to click
again, and mobile clients retried on timeout. The endpoint created a new charge each time; support
saw a steady trickle of double charges. The team added a per-cart idempotency key generated when the
checkout page loaded, stored `key → {status, chargeId}` transactionally with the charge, and replayed
the stored result on duplicates. Double charges went to zero, and the retry logic from Chapter 27
became safe to enable.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Natural key / upsert | No extra storage | Requires a unique identity | Slugs, emails, external ids |
| Idempotency key | Works for any write | Needs storage + TTL | Payments, creates, jobs |
| Conditional request (`If-Match`) | Prevents lost updates | Not duplicate detection | Optimistic concurrency |
| No dedup | Simple | Duplicates | Truly idempotent operations only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Treat retries as duplicates by default | Assume a timeout means "not done" |
| Prefer natural keys when available | Invent a key when a unique column exists |
| Store the result, not just a lock | Record only "in progress" forever |
| Replay the original status/body | Return a different success shape |
| Include a payload hash | Accept any payload under the same key |

## Common mistakes

- **Confusing "safe" with "idempotent."** `GET` is safe; `PUT` is idempotent but not safe.
- **Making the client generate a new key on retry**, which defeats the whole mechanism.
- **Deduplicating only at the UI layer.** Retries come from infrastructure too.
- **Forgetting the ambiguous-success case**, the one that actually causes duplicates.
- **Assuming `POST` can be made idempotent by adding `Retry-After`.** It cannot.

## Checklist

- [ ] Every non-idempotent write has a dedup strategy.
- [ ] Natural keys are used where they exist.
- [ ] Keyed operations store the result, not just presence.
- [ ] The key is stable across retries.
- [ ] A payload hash detects key reuse.
- [ ] The design handles "succeeded but response lost."

## Related

- [Idempotency Keys and Duplicate Detection](./02-idempotency-keys-and-duplicate-detection.md)
- [Idempotency Key Lifecycle](../02-deep-dive/01-idempotency-key-lifecycle.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
- [Chapter 26 — Network and Distributed Communication Errors](../../../part-10-external-dependencies/26-network-and-distributed-communication-errors/README.md)
