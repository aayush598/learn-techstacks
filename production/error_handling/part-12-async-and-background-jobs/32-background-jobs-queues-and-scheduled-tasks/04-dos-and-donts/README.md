# Chapter 32 — Do's and Don'ts

> Part XII · Chapter 32 · all sections · _Estimated reading time: 8 min_

## In one sentence

A production job system is defined by its **failure policy**: bounded retries, explicit terminal
states, a DLQ with replay, idempotent effects, and a shutdown that does not orphan work.

## The rules

| # | ✅ Do | ❌ Don't |
| - | ----- | -------- |
| 1 | Give every job a terminal state | Leave jobs `running` forever |
| 2 | Classify errors before retrying | Retry every exception |
| 3 | Retry transient errors only | Retry `TypeError` or validation errors |
| 4 | Use exponential backoff with jitter | Fixed immediate retries |
| 5 | Bound attempts **and** total time | Retry indefinitely |
| 6 | Set `maxReceiveCount` + DLQ | Let poison messages loop |
| 7 | Alarm on DLQ depth | Discover poison from a customer |
| 8 | Keep the failed state queryable | Only log the failure |
| 9 | Make every effect idempotent | Assume exactly-once delivery |
| 10 | Use stable idempotency keys | Random keys per attempt |
| 11 | Checkpoint after the effect commits | Save the cursor first |
| 12 | Use keyset pagination | Use `OFFSET` for resumable work |
| 13 | Keep job deadline below the lease | Let the job outlive visibility |
| 14 | Heartbeat long jobs | Get redelivered while still running |
| 15 | Pause polling on `SIGTERM` | Claim new work during shutdown |
| 16 | Drain with a bounded budget | Kill mid-write |
| 17 | Requeue in-flight work on timeout | Drop it silently |
| 18 | Isolate queues by latency class | Mix exports and password resets |
| 19 | Cap per-tenant concurrency | Let one tenant consume all workers |
| 20 | Key scheduled jobs on the window | Key on wall-clock time |
| 21 | Alarm on missed scheduled runs | Assume cron always fires |
| 22 | Emit one standard failure contract | Ad-hoc strings per job type |
| 23 | Rate-limit DLQ replay | Replay the whole DLQ at once |
| 24 | Reuse the original job id on replay | Generate a new id |

## Anti-patterns with symptoms

### ❌ Catch-log-ack

```ts
try { await work(); }
catch (e) { log.error(e); }
// then ack the message
```

**Symptom:** customer work vanishes; job status says `succeeded`.
**Fix:** rethrow, mark failed, or route to the DLQ.

### ❌ Infinite retry on a deterministic bug

```ts
if (err) throw err; // no classification, no max
```

**Symptom:** queue depth grows; the same stack trace appears thousands of times.
**Fix:** non-retryable classification + DLQ.

### ❌ Visibility timeout shorter than the job

```yaml
visibilityTimeout: 60s   # job takes 10 minutes
maxReceiveCount: 5
```

**Symptom:** the job is redelivered 5 times, runs concurrently, and lands in the DLQ while healthy.
**Fix:** deadline < visibility, or heartbeat/renew.

### ❌ In-memory dedupe

```ts
const seen = new Set<string>();
if (seen.has(job.id)) return;
```

**Symptom:** duplicates after every deploy.
**Fix:** durable unique constraint or provider idempotency key.

### ❌ Cursor before effect

```ts
await checkpoint.save({ lastRowId });
await writeBatch(batch); // crash -> rows lost forever
```

**Symptom:** silently missing data on resume.
**Fix:** write the effect, then the checkpoint.

### ❌ Async shutdown without pause

```ts
process.on("SIGTERM", () => process.exit(0));
```

**Symptom:** orphaned `running` jobs, partial uploads.
**Fix:** pause, drain, requeue, close.

## Code-review questions

1. What are the terminal states for this job, and where are they written?
2. Which errors are retryable, and how is that decided?
3. What is the max attempt count and the max time window?
4. What happens to this message after the last attempt?
5. Is the side effect idempotent under redelivery and replay?
6. Is the checkpoint written after the effect?
7. Is the job deadline shorter than the visibility timeout?
8. Does shutdown pause, drain, and requeue?
9. What does the DLQ record contain, and who replays it?
10. Does the scheduled job have an overlap guard and a missed-run alarm?

## Minimal policy snippet

```yaml
jobPolicy:
  maxAttempts: 6
  maxAge: 6h
  backoff: { base: 500ms, cap: 60s, jitter: full }
  retryableClasses: [transient]
  visibilityTimeout: 900s
  jobDeadline: 720s
  dlq: { retention: 14d, alarmAfter: 5m }
  idempotency: jobId
```

## Related

- [Job Lifecycle and Failure States](./../01-concepts/01-job-lifecycle-and-failure-states.md)
- [Poison Messages, DLQ, and Replay](./../01-concepts/03-poison-messages-dlq-and-replay.md)
- [Chapter 32 Reference](../05-reference/README.md)
- [Chapter 33 — Event Do's and Don'ts](../../33-events-webhooks-and-message-processing/04-dos-and-donts/README.md)
