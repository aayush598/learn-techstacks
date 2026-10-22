# Chapter 32 — Reference

> Part XII · Chapter 32 · all sections · _Estimated reading time: 12 min_

## Standard job failure policy

### Lifecycle

| State | Terminal? | Meaning | Exit |
| ----- | --------- | ------- | ---- |
| `queued` | No | Accepted, not due | — |
| `running` | No | Claimed, lease held | — |
| `succeeded` | Yes | Effect committed | ack/delete |
| `failed` | Yes | Terminal, replayable | ack after DLQ |
| `cancelled` | Yes | Deliberate stop | ack |
| `dead` | Yes | Exhausted, in DLQ | ack after DLQ |

### Retry policy

| Rule | Default |
| ---- | ------- |
| Retry classes | `transient` only |
| Max attempts | 6 (range 3–8) |
| Max age | 6 h (adjust to business tolerance) |
| Backoff | exponential, base 500 ms, cap 60 s, full jitter |
| Server hint | Honor `Retry-After` |
| Attempt storage | Persist `attempt` on the job record |
| Exhaustion | Move to DLQ with `terminalReason: exhausted` |
| Permanent | Move to DLQ immediately with `terminalReason: permanent` |

### Error class → action

| Class | Examples | Retry | DLQ |
| ----- | -------- | ----- | --- |
| `transient` | 429/503/504, timeout, `40001`, `40P01` | ✅ | On exhaustion |
| `config` | invalid credentials, missing bucket | ❌ | ✅ |
| `input` | schema mismatch, invalid query, bad FK | ❌ | ✅ |
| `business` | suspended tenant, quota exceeded | ❌ | ✅ (notify) |
| `programming` | `TypeError`, assertion | ❌ | ✅ + alert |
| `cancelled` | operator/client cancel | ❌ | ❌ (record state) |

### Queue settings

| Setting | Typical value | Notes |
| ------- | ------------- | ----- |
| Visibility timeout | 900 s | > job deadline |
| Job deadline | 80–90% of visibility | Leave cleanup margin |
| Heartbeat | every 300 s | For runs > visibility |
| `maxReceiveCount` | 3–5 | SQS redrive |
| Message retention | 4–14 days | ≥ retry window |
| DLQ retention | 14 days | ≥ triage time |
| Delay support | 15 min max (SQS) | Longer = scheduler |

### Shutdown

| Step | Action | Budget |
| ---- | ------ | ------ |
| 1 | Stop accepting / pause consumer | immediate |
| 2 | Drain in-flight | ≤ platform grace − 5 s |
| 3 | Requeue unfinished | within drain budget |
| 4 | Close consumer, flush telemetry | remaining |
| 5 | Exit 0 | — |

## Standard job error contract

```json
{
  "jobId": "job_01HX...",
  "jobType": "ExportJob",
  "tenantId": "ten_42",
  "attempt": 5,
  "maxAttempts": 6,
  "code": "EXPORT_S3_UNAVAILABLE",
  "class": "transient",
  "retryable": true,
  "terminalReason": "exhausted",
  "message": "S3 returned 503 while appending batch",
  "checkpoint": { "lastRowId": "row_88213", "rowsWritten": 88213 },
  "occurredAt": "2026-10-21T09:22:10Z"
}
```

| Field | Required | Rules |
| ----- | -------- | ----- |
| `jobId` | ✅ | Stable across retries/replay |
| `jobType` | ✅ | Registry key |
| `tenantId` | ✅ | Required for multi-tenant triage |
| `attempt`, `maxAttempts` | ✅ | Explain exhaustion |
| `code` | ✅ | Stable, registry-backed |
| `class` | ✅ | Drives retry policy |
| `retryable` | ✅ | Consistent with `class` |
| `terminalReason` | Only when terminal | `permanent`/`exhausted`/`cancelled` |
| `message` | ✅ | Safe for operators, no secrets/PII |
| `checkpoint` | Optional | Safe to persist; enough to resume |
| `occurredAt` | ✅ | ISO 8601 UTC |

## Checkpointing rules

| Rule | Why |
| ---- | --- |
| Commit effect, then cursor | Prevent skipped work |
| Keyset cursor (`id > last`) | Stable under concurrent writes |
| Store input hash | Prevent stale resume |
| Idempotent batch writes | Bounded rework |
| Deterministic output keys | No orphan/duplicate objects |
| One-batch rework bound | Predictable recovery |

## DLQ operations

| Operation | Owner | Cadence |
| --------- | ----- | ------- |
| Triage by `code` | On-call | Daily alarm |
| Fix cause | Owning team | Per incident |
| Replay (approval-gated) | On-call + owner | As needed |
| Replay rate | Start 1–10 msg/s | Ramp on green |
| Purge/archive | Owner | After replay |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Poison message** | A message that fails deterministically on every delivery |
| **DLQ** | Dead-letter queue: quarantine for exhausted messages |
| **Redrive policy** | SQS setting linking a queue to a DLQ with `maxReceiveCount` |
| **Visibility timeout** | How long a received message stays invisible before redelivery |
| **Receive count** | Number of times a message has been delivered |
| **Checkpoint** | Durable cursor/progress for resumable work |
| **Compensation** | Business-level undo of a completed step |
| **Exhausted** | Retry budget spent; outcome unknown until replay |
| **Permanent** | Retrying cannot succeed without a fix |
| **Effectively-once** | At-least-once delivery + idempotent processing |

## Related

- [Chapter 32 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 28 — Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Glossary](../../../GLOSSARY.md)
