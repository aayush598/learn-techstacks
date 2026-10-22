# Idempotency Key Store

> Part XI · Chapter 28 · Sections 28.4–28.9 · _Estimated reading time: 24 min_
> **Prerequisite:** [Idempotency Key Lifecycle](../02-deep-dive/01-idempotency-key-lifecycle.md)

## In one sentence

This is a **Postgres-backed idempotency store** that claims a key atomically, records the outcome
transactionally, replays the original response, rejects payload mismatches, and expires records
after 24 hours.

## Why this matters in production

The store is the part you reuse across every write endpoint. If it is correct, payments, project
creation, exports, and webhooks all inherit duplicate safety. If it has a read-then-write race or an
ambiguous failure state, every one of those endpoints inherits a duplicate bug. This implementation
keeps the critical path to three SQL statements and makes the state machine explicit.

## Schema

```sql
CREATE TABLE idempotency_keys (
  tenant_id      uuid        NOT NULL,
  key            text        NOT NULL,
  payload_hash   text        NOT NULL,
  state          text        NOT NULL CHECK (state IN
                    ('in_progress','completed','failed_retryable',
                     'failed_terminal','unknown')),
  status_code    integer,
  response_body  jsonb,
  resource_id    text,
  last_error     text,
  owner          text,
  lease_until    timestamptz,
  created_at     timestamptz NOT NULL DEFAULT now(),
  expires_at     timestamptz NOT NULL,
  PRIMARY KEY (tenant_id, key)
);

CREATE INDEX idempotency_expiry_idx ON idempotency_keys (expires_at);
CREATE INDEX idempotency_lease_idx
  ON idempotency_keys (lease_until)
  WHERE state = 'in_progress';
```

The composite primary key **is** the duplicate detection. No application-level locking is required.

## The store

```ts
import { createHash } from "crypto";

export type KeyState =
  | "in_progress" | "completed" | "failed_retryable"
  | "failed_terminal" | "unknown";

export interface KeyRecord {
  tenantId: string;
  key: string;
  state: KeyState;
  statusCode: number | null;
  responseBody: unknown;
  resourceId: string | null;
  payloadHash: string;
  lastError: string | null;
}

export interface Replay {
  status: number;
  body: unknown;
  headers: Record<string, string>;
}

export function canonicalHash(value: unknown): string {
  return createHash("sha256").update(stableStringify(value)).digest("hex");
}

function stableStringify(value: unknown): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(stableStringify).join(",")}]`;
  const obj = value as Record<string, unknown>;
  return `{${Object.keys(obj).sort().map((k) =>
    `${JSON.stringify(k)}:${stableStringify(obj[k])}`).join(",")}}`;
}

export class IdempotencyStore {
  constructor(private db: Pool, private ttlSeconds = 86_400) {}

  /**
   * Claim a key. Returns:
   *  - { claimed: true, record }  → caller should perform the side effect
   *  - { claimed: false, replay } → caller should return the replay
   *  - throws IdempotencyConflict for payload mismatch / in-progress
   */
  async claim(tenantId: string, key: string, payload: unknown, owner: string) {
    const payloadHash = canonicalHash(payload);
    const client = await this.db.connect();
    try {
      await client.query("BEGIN");
      const inserted = await client.query<KeyRecord>(
        `INSERT INTO idempotency_keys
           (tenant_id, key, payload_hash, state, owner, lease_until, expires_at)
         VALUES ($1, $2, $3, 'in_progress', $4, now() + interval '45 seconds',
                 now() + ($5 || ' seconds')::interval)
         ON CONFLICT (tenant_id, key) DO NOTHING
         RETURNING *`,
        [tenantId, key, payloadHash, owner, this.ttlSeconds],
      );

      if (inserted.rowCount === 1) {
        await client.query("COMMIT");
        return { claimed: true as const, record: toRecord(inserted.rows[0]) };
      }

      const existing = await client.query<KeyRecord>(
        `SELECT * FROM idempotency_keys WHERE tenant_id = $1 AND key = $2`,
        [tenantId, key],
      );
      await client.query("COMMIT");
      const row = existing.rows[0];

      if (row.payload_hash !== payloadHash) {
        throw new IdempotencyConflict(
          "KEY_REUSED_WITH_DIFFERENT_PAYLOAD", 422,
          "This idempotency key was already used with a different request.",
        );
      }
      if (row.state === "in_progress") {
        throw new IdempotencyConflict(
          "REQUEST_IN_PROGRESS", 409, "A request with this key is already in progress.",
        );
      }
      if (row.state === "unknown") {
        throw new IdempotencyConflict(
          "OUTCOME_UNKNOWN", 409, "The previous attempt has an unknown outcome; retry later.",
        );
      }
      return { claimed: false as const, replay: toReplay(row) };
    } catch (err) {
      await client.query("ROLLBACK");
      throw err;
    } finally {
      client.release();
    }
  }

  async complete(tenantId: string, key: string, status: number, body: unknown,
                 resourceId?: string) {
    await this.db.query(
      `UPDATE idempotency_keys
          SET state='completed', status_code=$3, response_body=$4,
              resource_id=$5, lease_until=NULL, last_error=NULL
        WHERE tenant_id=$1 AND key=$2`,
      [tenantId, key, status, body, resourceId ?? null],
    );
  }

  async fail(tenantId: string, key: string, kind: "retryable" | "terminal",
             status?: number, body?: unknown, error?: string) {
    const state = kind === "retryable" ? "failed_retryable" : "failed_terminal";
    await this.db.query(
      `UPDATE idempotency_keys
          SET state=$3, status_code=$4, response_body=$5, last_error=$6, lease_until=NULL
        WHERE tenant_id=$1 AND key=$2`,
      [tenantId, key, state, status ?? null, body ?? null, error ?? null],
    );
  }

  async markUnknown(tenantId: string, key: string, error: string) {
    await this.db.query(
      `UPDATE idempotency_keys
          SET state='unknown', last_error=$3, lease_until=NULL
        WHERE tenant_id=$1 AND key=$2`,
      [tenantId, key, error],
    );
  }

  /** Sweep expired leases: a crashed worker must not block a key forever. */
  async sweepLeases() {
    await this.db.query(
      `UPDATE idempotency_keys
          SET state='unknown', last_error='lease expired'
        WHERE state='in_progress' AND lease_until < now()`,
    );
  }

  async purgeExpired() {
    await this.db.query(`DELETE FROM idempotency_keys WHERE expires_at < now()`);
  }
}
```

## Wiring it around an operation

```ts
async function createProject(req: Request, tenantId: string) {
  const key = req.header("Idempotency-Key");
  if (!key) return problem(400, "IDEMPOTENCY_KEY_REQUIRED");
  const payload = { name: req.body.name, slug: req.body.slug };

  const claim = await store.claim(tenantId, key, payload, req.id);
  if (!claim.claimed) return claim.replay;

  try {
    const project = await db.transaction(async (tx) => {
      const p = await tx.insert("projects", { tenant_id: tenantId, ...payload });
      // Commit the key outcome in the SAME transaction as the side effect.
      await tx.query(
        `UPDATE idempotency_keys
            SET state='completed', status_code=201, response_body=$3,
                resource_id=$4, lease_until=NULL
          WHERE tenant_id=$1 AND key=$2`,
        [tenantId, key, { id: p.id, name: p.name, slug: p.slug }, p.id],
      );
      return p;
    });
    return json(201, { id: project.id, name: project.name, slug: project.slug });
  } catch (err) {
    if (isTerminal(err)) {
      await store.fail(tenantId, key, "terminal", 422, problemBody(err), err.code);
      return problem(422, err.code);
    }
    // Unknown whether the effect applied: do not mark terminal.
    await store.markUnknown(tenantId, key, String(err));
    return problem(503, "OUTCOME_UNKNOWN", { retryAfterMs: 1_000 });
  }
}
```

## Why the transaction matters

`complete()` is called on the **same connection** as the insert. If the process crashes between the
row insert and the key update, both roll back; the lease later marks the claim unknown, and
reconciliation decides. There is no window where the side effect commits but the key says
`in_progress`.

For external effects, replace the transaction with an outbox:

```sql
-- claim + outbox in one transaction
INSERT INTO outbox (topic, payload, idempotency_key) VALUES ('charge', $1, $2);
```

## Concurrency walkthrough

```text
t=0.000  req A claim K → INSERT wins → in_progress
t=0.001  req B claim K → conflict → state=in_progress → 409 REQUEST_IN_PROGRESS
t=0.050  req A completes → key=completed, status=201
t=0.400  req B retries  → conflict → completed → replay 201 + body
t=0.401  req C claim K, different payload → conflict → hash mismatch → 422
```

Exactly one side effect. The loser gets an actionable status, and the later retry gets the original
result.

## Key data / numbers

- Primary key: `(tenant_id, key)` — not a global key.
- Lease: **45s** in this example; tune to P99 operation duration.
- TTL: **86,400s (24h)** by default.
- Sweeper interval: **1–5 min**; purge job: hourly/daily.
- Duplicate states: `409` in progress, `422` payload mismatch, `409` unknown.
- Replay header: `Idempotent-Replay: true`.

## Real-world use case — Acme SaaS

Acme's billing endpoint used a `SELECT` then `INSERT` and marked keys complete *after* committing the
charge, in a separate query. A deploy mid-request left charges committed with keys still
`in_progress`; retries got `409` until an engineer deleted rows. This store moved the key update into
the same transaction, added leases and a sweeper, and introduced `unknown` for external-call timeouts.
Support tickets for "stuck payment" disappeared, and the billing team gained a reliable audit trail
linking each charge to its key.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Same-DB key + effect | Atomic | Only local effects |
| `409` on in-progress | Simple, safe | Client must retry |
| Wait on in-progress | Better UX | Holds connections |
| 24h TTL | Matches providers | Storage growth |
| JSONB response | Exact replay | Larger rows |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use a composite primary key | `SELECT` then `INSERT` |
| Update the key in the same transaction | Update it in a separate query |
| Persist terminal failures | Delete the key |
| Lease + sweep in-progress rows | Leave crashed keys stuck |
| Reject payload mismatch with `422` | Overwrite the existing record |
| Store the original status/body | Regenerate the response |

## Common mistakes

- **Calling `complete()` after `COMMIT`**, reopening the crash window.
- **No `expires_at`**, so the table grows forever.
- **Hash includes volatile fields** (timestamp, request id), causing false mismatches.
- **Lease shorter than the operation**, marking healthy work unknown.
- **Returning `500` for in-progress**, making clients retry aggressively.

## Checklist

- [ ] `(tenant_id, key)` is the primary key.
- [ ] Claim is one `INSERT ... ON CONFLICT DO NOTHING`.
- [ ] Completion is transactional with the local side effect.
- [ ] Terminal vs retryable failures are recorded distinctly.
- [ ] Unknown outcomes are marked, not failed.
- [ ] Lease sweeper and expiry purge run on schedule.
- [ ] Payload hash is canonical and excludes volatile fields.
- [ ] Replay returns the stored status and body.

## Related

- [Idempotency Key Lifecycle](../02-deep-dive/01-idempotency-key-lifecycle.md)
- [Idempotency Keys and Duplicate Detection](../01-concepts/02-idempotency-keys-and-duplicate-detection.md)
- [Checkout and Webhook Idempotency](./02-checkout-and-webhook-idempotency.md)
- [Chapter 23 — Transaction and Rollback Error Handling](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
