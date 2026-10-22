# Process Recovery Limits and When to Terminate (41.16–41.18)

> Part XV · Chapter 41 · Sections 41.16–41.18 (mechanics) · _Estimated reading time: 25 min_
> **Prerequisite:** [Initialization, Startup, and Shutdown (41.10–41.18)](../01-concepts/04-initialization-startup-and-shutdown.md)

## In one sentence

The question is **not** "can I catch this error?" but **"is this process still a valid executor?"**
— and when the answer is no, **terminating is the repair**, provided the replacement can rebuild
correct state from durable storage.

## Why this matters in production

Recovery is where error handling becomes dangerous: the *instinct* after a crash is to keep the
process alive and carry on — right for a failed request, wrong for a failed *process*. Once the
invariants are unknown, every later request runs on state nobody can reason about, and the visible
symptom is never the crash but the *quiet divergence* three hours later: a customer reports wrong
data and the logs show a clean restart.

The other half: "just restart it" is only correct when the process is **restart-safe** — restarting a
process that reads state from a corrupt durable store reproduces the corruption exactly.

## Core concept

### 41.16 The three invariants a process must hold

A process is a valid executor only while all three of these hold:

| Invariant | Broken by | Observable signal |
|-----------|-----------|-------------------|
| **Memory integrity** | native crash, heap OOM, stack overflow, a bug that corrupts shared state | `SIGSEGV` (**139**), `SIGABRT` (**134**), `137` with `OOMKilled` |
| **Resource capacity** | fd exhaustion, pool exhaustion, port exhaustion, OOM | `EMFILE`, `ENOMEM`, pool `waiting` pinned, `137` |
| **Logical integrity** | a partial write, a lost transaction, a poisoned cache, a half-applied migration | no crash at all — only divergence |

The first two are *loud*: the process dies or degrades visibly. The third is **silent**, and it is
the reason "the crash was handled" is not the same as "the system is fine".

### The recovery taxonomy

```text
                 Can this process still produce correct results?
                    │                        │
                   YES                       NO
                    ▼                        ▼
          recover in-process        Can a fresh process rebuild
          (bound the resource,      correct state from durable
           reset the component,     storage?
           fail one request)           │            │
                                      YES           NO
                                       ▼            ▼
                              terminate + restart   ESCALATE
                              (rebuild from         (corrupt durable
                               durable storage)      state → human)
```

### 41.17 The restart-safety test

Before you terminate, ask one question about the *replacement* process:

> **Can a fresh process, with no memory of this one, rebuild correct state from durable
> storage — and produce no duplicate side effects?**

| State the process holds | Restart-safe? | Mechanism required |
|------------------------|---------------|--------------------|
| In-memory cache | ✅ | rebuild from the DB/Redis; never treat the cache as the source of truth |
| Consumed queue messages | ✅ | **acknowledgement after the effect**, plus a visibility timeout |
| A job in progress | ✅ | checkpoint + lease + idempotent resume |
| A DB transaction | ✅ | the DB rolls it back; the *external* side effects need idempotency keys |
| A Stripe charge already sent | ✅ | idempotency key on the provider call |
| A file being written | ⚠️ | write to a temp file + atomic rename; a half-written file is corrupt state |
| A Webhook already delivered | ⚠️ | the receiver must be idempotent; you cannot unsend it |
| A mutable global registry | ❌ | the process died holding state nobody else has |
| A half-applied schema migration | ❌ | **forward fix required**; restarting repeats it |

The two warning rows are where "restart to recover" quietly becomes "restart to duplicate" — a small window, but the effect is financial or customer-visible.

### 41.18 Unsafe recovery from corrupted state

Three forms of corrupted state, with three different responses:

```text
1. IN-MEMORY corruption (poisoned cache, broken singleton)
   → restart rebuilds it  ✅  (this is the good case)

2. DURABLE corruption (corrupt file, bad WAL, poisoned snapshot that is also the source)
   → restart reproduces it  ❌  → refuse to start, escalate

3. LOGICALLY INCONSISTENT state (half-applied migration, two systems disagree)
   → restart reproduces it  ❌  → forward fix (or rollback) required
```

The distinction between (1) and (2) is *where the truth lives*. If the truth is in the database
and the process holds a derived copy, restarting is safe. If the truth is in the file the process
just corrupted, restarting is a loop.

**The startup validation rule:** after a crash, the replacement process must **verify its invariants
before serving**, refusing to start when they fail — a crash loop on corrupt state must escalate to a
human, not to the restart policy.

### The termination decision table

| Condition | In-process recovery? | Action |
|-----------|--------------------|--------|
| A single request failed with a domain error | ✅ | handle at the boundary, return the error |
| A dependency is down; the rest of the service works | ✅ | degrade, shed, or fail that path only |
| The heap is exhausted | ❌ | terminate immediately, no cleanup |
| The descriptor table is exhausted | ❌ | terminate immediately |
| A native crash occurred | ❌ | terminate; collect a core dump |
| A bug may have corrupted in-memory state | ❌ | terminate fast — do not run "cleanup" on it |
| Durable state is corrupt | ❌ | terminate; refuse to restart automatically; page |
| The event loop is wedged | ❌ | `SIGKILL` from outside |
| The process is correct but slow | ✅ | shed load, scale out |

### Crash loops

A restart policy applied to a *deterministic* failure produces a loop, not a recovery:

```text
Kubernetes restart backoff: 10 s → 20 s → 40 s → 80 s … capped at 5 min
each restart re-runs the same boot path → same failure → same log line
```

The signal that a crash loop is happening is the **restart count**, and it must alert — a pod
that restarted 5 times in 10 minutes is an incident, not a retry. Two rules:

1. **Distinguish "crashed repeatedly" from "crashed once".** The orchestrator should count
   restarts in a window and escalate above a threshold (commonly 5 restarts in 10 minutes).
2. **Never let the restart policy hide a corrupt state.** If the boot path detects corrupt durable
   state, it must exit with a code that says "do not restart me automatically" — and the
   deployment must gate on it.

### Dedicated fault domains

The strongest way to make a failure recoverable is to **not let it share a process with the good
path**. A component that can crash the runtime (native parsers, regex engines, image decoders,
LLM tool parsers) belongs in its own process, where crashing it costs one job instead of the
whole service.

```text
Acme API process: HTTP + Checkout + billing      ← must never crash
   └── AgentRun tool-call parser → isolated worker process (separate PID)
        └─ crash (stack overflow / native decode) = one job fails, service survives
```

This converts "terminate to recover" from a global event into a local one, and it is the
difference between a degraded feature and an outage.

## How it works (mechanics)

### The decision procedure

```text
A failure occurred.
│
├─ EXPECTED error (validation, 404, declined card, dependency 503)?
│    └─ YES → handle at the boundary. Do NOT terminate.
├─ Are all three invariants intact (memory, resource capacity, logical integrity)?
│    ├─ YES → recover in-process: reset the component, bound the resource, fail the one
│    │        request. Log it as degraded, not fatal.
│    └─ NO  → continue ↓
├─ Would a fresh process rebuild correct state?
│    ├─ YES → TERMINATE. Log, flush, exit non-zero. Let the orchestrator restart.
│    └─ NO  → TERMINATE but BLOCK automatic restart. Escalate to a human.
```

### Making the death diagnosable

A fatal exit should leave three things behind: **what happened**, **what state the process was in**, and **what it was doing**:

```ts
function fatalExit(reason: unknown, context: Record<string, unknown>): never {
  const err = reason instanceof Error ? reason : new Error(String(reason));
  log.error({
    err, context, pid: process.pid,
    uptime_s: Math.round(process.uptime()),
    rss_mb: Math.round(process.memoryUsage().rss / 1024 / 1024),
    openFds: countOpenFds(), inFlight: inFlightCount,
    version: process.env.APP_VERSION,
  }, "fatal: terminating process");
  flushLogs().finally(() => process.exit(1));
}
```

For native crashes, enable core dumps (`ulimit -c unlimited` plus a core-pattern that writes to a
volume) — the JavaScript log line will not tell you why the native addon segfaulted.

## Worked example

The decision procedure applied to a real component:

```python
def run_agent_tool_call(agent_run_id: str, payload: dict) -> ToolResult:
    try:
        return parse_tool_call(payload)          # may recurse over nested arguments
    except RecursionError as exc:
        # "Recovering" in-process: reuse the cached context.
        context_cache.pop(agent_run_id, None)
        log.warning({"agent_run_id": agent_run_id}, "tool-call parse failed, cache cleared")
        return ToolResult(error="TOOL_CALL_INVALID")
```

The bug: `parse_tool_call` recurses over nested tool arguments. A deeply nested (or cyclic)
payload overflows the stack. The `except RecursionError` catches it — and then the code
**continues serving with a poisoned in-memory context**: `context_cache` still holds the
half-mutated conversation for that run, and the *next* tool call reads it.

The corrected version treats the recursion guard as **fatal for the run**, not for the process:

```python
def run_agent_tool_call(agent_run_id: str, payload: dict) -> ToolResult:
    try:
        return parse_tool_call(payload)
    except RecursionError as exc:
        # 1. The run's state is suspect → drop it.
        context_cache.pop(agent_run_id, None)
        # 2. Mark the run as failed, explicitly. No half-built context survives.
        agent_runs.mark_failed(agent_run_id, reason="TOOL_CALL_TOO_DEEP")
        # 3. This is a bug, not a business outcome → metric, not a silent degradation.
        metrics.increment("agent_tool_call_recursion_error")
        raise ToolCallInvalid(agent_run_id) from exc
```

And because `parse_tool_call` is the component that can crash the runtime, it runs in an isolated
worker process, so a crash costs one job instead of the whole service.

## Key data / numbers

- **Exit codes**: `1` fatal (uncaught exception, failed shutdown), `134` `SIGABRT` (V8 heap OOM
  abort), `137` `128 + 9` `SIGKILL` (OOM-kill **or** grace-period expiry — never normal),
  `139` `128 + 11` `SIGSEGV`, `143` `128 + 15` `SIGTERM` (a normal orchestrated stop).
- **Kubernetes restart backoff**: **10 s → 20 s → 40 s → 80 s …**, capped at **5 min**; a pod that
  restarts more than **5 times in 10 minutes** should alert, not retry silently.
- **cgroup memory limit**: `memory.max` (v2) / `memory.limit_in_bytes` (v1); exceeding it means
  `SIGKILL` → exit **137** with `reason: OOMKilled`.
- **Python** recursion limit default **1000** (`sys.setrecursionlimit`); catching `RecursionError`
  is possible but the stack is still nearly exhausted — treat it as fatal for the operation.
- **Go**: an unrecovered `panic` in any goroutine exits the process with status **2**; a goroutine
  stack overflow is a fatal runtime error (exit **2**), not a recoverable exception.
- **Restart-safety primitives**: idempotency keys (provider calls), ack-after-effect (queues),
  leases + fencing tokens (long jobs), checkpoint + resume (batch work), temp file + atomic rename.
- **Signal escalation budget**: a `SIGTERM` handler that has not finished when the grace period
  expires is replaced by `SIGKILL` — nothing runs, no cleanup, no logs.

## Real-world use case — Acme SaaS

Acme's `AgentRun` feature summarized support threads with an LLM. The tool-call parser recursed
over nested arguments, and a customer pasted a deeply nested JSON blob into a support thread; the
parser overflowed the stack.

The team's first fix made things *worse*. They caught `RecursionError` in the request handler and
returned a friendly error — the incident was closed. But the exception was raised mid-way through
building the run's message list, so the run's **in-memory context was left half-built**. The next
turn reused it, and the summarizer produced a summary of a conversation truncated mid-sentence.
Twelve customers received summaries quoting text they never wrote, and nothing in the logs showed
an error: the run *succeeded*.

The second fix changed the failure class:

1. The parser moved into a **separate worker process** with a depth guard (`maxDepth = 32`) that
   fails with a normal error long before the stack is at risk; a native crash costs one job.
2. The run is marked **failed** and its context **discarded** — no half-built state survives.
3. An `agent_tool_call_invalid` metric replaced "no metric at all"; the depth guard turned a crash
   into a validation error for every malformed input that previously caused it.

The general lesson: **the recovery was "correct" in the sense that no exception escaped — and it
was still the bug.** Catching an error preserves the *program*, not the *data*.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| **Terminate and restart** | clean state, fast | loses in-flight work; needs restart-safety | when invariants are broken |
| **Recover in-process** | no downtime | risks continuing on corrupt state | when the failure is bounded and isolated |
| **Isolate the risky component** in its own process | the crash is local | more moving parts | native parsers, decoders, tool runners |
| **Fail the request and keep serving** | preserves availability | wrong for a process-wide fault | expected, per-request errors |
| **Block restart on corrupt durable state** | stops a destructive loop | needs an escape hatch for humans | corrupt WAL, bad migrations |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ask "is the process still a valid executor?" | Ask "can I catch this?" |
| Discard suspect in-memory state when you catch an error | Continue with a half-built context |
| Make restart-safety a property of every durable effect | Assume "restart" means "no duplicate side effects" |
| Alert on restart counts and crash loops | Let the backoff hide a deterministic bug |
| Isolate crash-prone components in their own process | Run a native parser in the request path |
| Verify invariants at startup after a crash | Serve whatever the durable store contains |
| Exit non-zero so the crash is visible | Exit `0` after a fatal error |
| Collect a core dump for native crashes | Lose the evidence to a bare stack trace |

## Common mistakes

- **Treating a catch as a recovery** — the exception was handled; the *state* was not.
- **Restarting a process that reads corrupt durable state** — the restart reproduces the
  corruption, and the backoff hides it.
- **Idempotency only at the API boundary** — the duplicate that matters is the provider call
  (a second charge), and it needs its own idempotency key.
- **Running crash-prone code in the request process** — one malformed input takes down checkout.
- **Recovering the process but not the *run*** — the failed unit of work needs an explicit failed
  state, not a retry with the same bad state.

## Checklist

- [ ] Every fatal path ends in a log + flush + non-zero exit.
- [ ] The final fatal log includes pid, uptime, RSS, open fds, and in-flight count.
- [ ] Every durable side effect has an idempotency key or an acknowledgement-after-effect.
- [ ] In-progress jobs checkpoint, lease, and resume idempotently.
- [ ] Restart counts are alerted on (commonly 5 restarts in 10 minutes).
- [ ] Startup validates durable state and refuses to serve when it is corrupt.
- [ ] Crash-prone components run in an isolated process.
- [ ] Core dumps are enabled for native crashes.
- [ ] Exit codes distinguish clean (`0`), fatal (`1`), OOM-kill (`137`), and SIGTERM (`143`).

## Related

- [Graceful Shutdown Sequencing with SIGTERM — deep dive](./02-graceful-shutdown-sequencing.md)
- [Initialization, Startup, and Shutdown (41.10–41.18)](../01-concepts/04-initialization-startup-and-shutdown.md)
- [Python and Go: OOM and Resource-Limit Handling](../03-practical-examples/02-python-and-go-resource-limit-handling.md)
- [Idempotency in Payments, Jobs, and Webhooks](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/01-concepts/04-idempotency-in-payments-jobs-and-webhooks.md)
- [Worker Failures, Timeouts, Shutdown, and Isolation](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/01-concepts/04-worker-failures-timeouts-and-isolation.md)
