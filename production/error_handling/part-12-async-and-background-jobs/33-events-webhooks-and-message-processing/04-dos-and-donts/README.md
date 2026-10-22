# Chapter 33 — Do's and Don'ts

> Part XII · Chapter 33 · all sections · _Estimated reading time: 8 min_

## In one sentence

Treat every event as **untrusted, duplicated, late, and possibly a version you do not understand** —
verify, dedupe, isolate, and quarantine before you apply it.

## The rules

| # | ✅ Do | ❌ Don't |
| - | ----- | -------- |
| 1 | Verify webhook signatures on the raw body | Verify after JSON parsing |
| 2 | Compare signatures in constant time | Use `===` |
| 3 | Enforce a timestamp tolerance | Accept arbitrarily old signatures |
| 4 | Ack after durable receipt | Ack before recording |
| 5 | Return `5xx` for transient internal failures | Return `200` to stop retries |
| 6 | Return `4xx` for invalid signatures/payloads | Retry untrusted input |
| 7 | Dedupe on the event's stable id | Dedupe on payload or arrival time |
| 8 | Commit dedupe with the effect | Check and write in separate steps |
| 9 | Retain dedupe keys past the replay window | Use a 1-hour TTL |
| 10 | Assume at-least-once delivery | Claim exactly-once delivery |
| 11 | Version every event/schema | Rely on "it hasn't changed" |
| 12 | Tolerate unknown fields | Reject additive producer changes |
| 13 | Upcast old versions | Branch the handler per version |
| 14 | Quarantine unknown versions/types | Crash the consumer loop |
| 15 | Partition by aggregate for ordering | Assume global order |
| 16 | Skip stale versions with a guard | Blindly overwrite state |
| 17 | Isolate each record in a batch | Fail the whole batch on one record |
| 18 | Return partial batch failures | Retry successes with failures |
| 19 | Quarantine poison events | Requeue them until exhaustion |
| 20 | Label eventual-consistency windows | Promise synchronous projections |
| 21 | Compensate completed downstream effects | Assume you can unconsume |
| 22 | Alert on signature rejects and DLQ depth | Wait for a customer report |

## Anti-patterns with symptoms

### ❌ Process inline, then `200`

```ts
await projector.apply(event);   // 30 s
res.status(200).end();
```

**Symptom:** sender timeouts, parallel retries, duplicate side effects.
**Fix:** verify → insert inbox → `200`; process asynchronously.

### ❌ `express.json()` before verification

```ts
app.use(express.json());
app.post("/webhooks/stripe", handler); // raw body gone
```

**Symptom:** every signature check fails, or worse, verification is skipped.
**Fix:** route-specific `express.raw()`.

### ❌ Dedupe in memory / short TTL

```ts
const seen = new Set<string>();
```

**Symptom:** duplicates after every deploy and after the TTL.
**Fix:** durable inbox with a unique constraint.

### ❌ All-or-nothing batch

```ts
for (const r of records) await handle(r); // throws -> entire batch retries
```

**Symptom:** 99 good records re-applied because 1 failed.
**Fix:** per-record try/catch + `batchItemFailures`.

### ❌ Poison in the retry list

```ts
failures.push({ itemIdentifier: r.id }); // even for InvalidSchema
```

**Symptom:** the same batch retries until exhaustion, blocking progress.
**Fix:** quarantine permanent errors; retry only transient ones.

### ❌ No version guard

```ts
await projection.upsert(event); // late event overwrites newer state
```

**Symptom:** canceled subscriptions reactivate; refunded orders return to paid.
**Fix:** `WHERE version < incoming` or an explicit state machine.

### ❌ Unknown types silently acked

```ts
if (!HANDLED.has(type)) return; // no record
```

**Symptom:** silent data loss; nobody knows which events were dropped.
**Fix:** quarantine + metric per unknown type.

## Code-review questions

1. Where is the signature verified, and is it the raw body?
2. What is the dedupe key, and is it durable?
3. Are dedupe and the effect in one transaction?
4. What happens to a duplicate delivery?
5. What happens to an unknown schema version?
6. Is ordering required, and is the partition key the aggregate?
7. Does the projection guard against stale versions?
8. Does a batch failure retry only failed records?
9. Where do poison events go, and who replays them?
10. What is the consistency window, and is it visible to users?

## Minimal consumer contract

```yaml
consumer:
  delivery: at-least-once
  dedupeKey: event.id
  dedupeStore: durable-inbox
  dedupeTTL: 30d
  ackAfter: durable-effect
  retryable: [transient]
  nonRetryable: [input, schema, unsupported-version, programming]
  dlq: per-consumer
  batch: partial-failure-response
  ordering: per-aggregate-key
  schemaSupport: [N, N-1]
```

## Related

- [Publish and Consume Failures](./../01-concepts/01-publish-and-consume-failures.md)
- [Webhook Signatures, Retries, and Timeouts](./../01-concepts/04-webhook-signatures-retries-timeouts.md)
- [Chapter 33 Reference](../05-reference/README.md)
- [Chapter 31 — Async Do's and Don'ts](../../31-asynchronous-error-handling/04-dos-and-donts/README.md)
