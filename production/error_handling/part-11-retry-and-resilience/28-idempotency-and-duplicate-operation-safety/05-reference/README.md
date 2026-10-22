# Chapter 28 — Reference

> Part XI · Chapter 28 · Key lifecycle, TTL defaults, duplicate-response mapping, and glossary.

## Cheat sheet — the key contract

```text
IdempotencyKey {
  value        opaque UUID/ULID, stable across retries
  scope        (tenant_id, operation)
  payload_hash canonical semantic fields
  state        in_progress | completed | failed_retryable | failed_terminal | unknown
  result       status + body + resource_id
  ttl          24h typical (>= retry + reconciliation window)
}
```

## Decision tree — does this write need a key?

```text
Is the operation a write with an external effect?
│
├─ No (read-only) → no key needed
│
└─ Yes → Does a natural unique identity exist?
    ├─ Yes → enforce a unique constraint (tenant_id, slug) / (order_id)
    │        └─ Still add a key if clients retry and need the original response
    └─ No  → require an Idempotency-Key
              ├─ derive from the business operation when possible
              └─ otherwise accept a client UUID, scoped to the tenant
```

## Decision tree — duplicate request handling

```text
Request with key K arrives.
│
├─ No record → CLAIM K → execute
│
└─ Record exists →
    ├─ payload_hash differs → 422 KEY_REUSED_WITH_DIFFERENT_PAYLOAD
    ├─ state = completed   → replay original status + body
    ├─ state = in_progress → 409 REQUEST_IN_PROGRESS (or short wait)
    ├─ state = failed_terminal → replay the terminal error
    ├─ state = failed_retryable → RETRY under K
    └─ state = unknown     → RECONCILE before retrying
```

## Key state reference

| State | Meaning | Duplicate behavior | Next transition |
| ----- | ------- | ------------------ | --------------- |
| `in_progress` | Claimed, not finished | `409` / wait | complete / fail / unknown |
| `completed` | Side effect committed | Replay | expired |
| `failed_retryable` | Failed before effect | Retry under K | in_progress |
| `failed_terminal` | Permanent failure | Replay failure | expired |
| `unknown` | Outcome unknown | `409`, reconcile | completed / retryable / terminal |
| `expired` | Past TTL | Treated as absent | — |

## TTL defaults

| Operation | TTL | Rationale |
| --------- | --- | --------- |
| API create | 24h | Covers client and gateway retries |
| Payment | 24h | Matches common provider key retention |
| Refund | 7d | Finance reconciliation |
| Job step | Job duration + 7d | Late retries and replays |
| Webhook event | 7–30d | Provider redelivery windows |
| Distributed child key | Parent TTL + margin | Workflow retries |

## Natural keys by domain

| Domain | Natural key |
| ------ | ----------- |
| Payments | `tenant:order:charge` |
| Refunds | `tenant:payment:refund:<request_id>` |
| Jobs | `job_id:step:input_hash` |
| Webhooks | provider `event_id` (`evt_...`) |
| Distributed | parent key + deterministic child suffix |
| Idempotent creates | `(tenant_id, slug)` unique index |

## Response mapping

| Situation | Status | Code |
| --------- | ------ | ---- |
| First success | `201`/`200` | original |
| Replay success | original status | `Idempotent-Replay: true` |
| In progress | `409` | `REQUEST_IN_PROGRESS` |
| Payload mismatch | `422` | `KEY_REUSED_WITH_DIFFERENT_PAYLOAD` |
| Unknown outcome | `409` or `202` | `OUTCOME_UNKNOWN` |
| Terminal failure replay | original `4xx` | original code |
| Missing key on required endpoint | `400` | `IDEMPOTENCY_KEY_REQUIRED` |

## Storage reference

| Store | Atomic with effect | TTL | Notes |
| ----- | ------------------ | --- | ----- |
| Postgres same tx | Yes | Manual | Preferred for local writes |
| Outbox + Postgres | Yes (intent) | Manual | Preferred for external calls |
| Redis | No | Native `EX` | Disable eviction for keys |
| DynamoDB | Conditional writes | Native TTL | Good at scale |
| Provider key | N/A | Provider-defined | In addition to your store |

## Reconciliation checklist

```text
[ ] unknown rows have a provider/correlation reference
[ ] reconciler queries by your key or provider key
[ ] succeeded → complete and replay
[ ] not found after consistency window → allow retry
[ ] declined → terminal
[ ] resolved events are emitted idempotently
[ ] alert on charges without key rows
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Idempotency | N executions have the same effect as one |
| Idempotency key | Client-supplied token identifying a logical operation |
| Payload hash | Canonical digest detecting key reuse with different content |
| Claim | Atomic insert that reserves a key |
| Replay | Returning the stored original result to a duplicate |
| Lease | Time window after which an unfinished claim becomes unknown |
| Unknown outcome | Cannot determine whether the effect occurred |
| Reconciliation | Querying the provider to resolve an unknown outcome |
| Child key | Deterministic key derived from a parent for a sub-step |
| At-least-once | Delivery guarantee requiring dedup for single effect |

## Signposts

- Retry policy → [Ch. 27](../../27-retry-policies/README.md)
- Transactions and outbox → [Ch. 23](../../../part-09-database-and-transactions/23-transaction-and-rollback-error-handling/README.md)
- Webhooks and delivery → [Ch. 33](../../../part-12-async-and-background-jobs/33-events-webhooks-and-message-processing/README.md)
- Billing workflows → [Ch. 42](../../../part-16-specialized-saas-scenarios/42-auth-billing-and-subscription-workflows/README.md)
- Final reference → [Ch. 62](../../../part-24-repeatable-blueprint/62-final-reference-materials/README.md)

## Related

- [Chapter 28 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Idempotency Key Store](../03-practical-examples/01-idempotency-key-store.md)
- [Idempotency Key Lifecycle](../02-deep-dive/01-idempotency-key-lifecycle.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
