# Practical — Cancellation and Cleanup in AgentRun

> Part XII · Chapter 31 · Sections 31.8–31.9, 31.14 · _Estimated reading time: 18 min_
> **Prerequisite:** [Cancellation and Timeout Propagation](../02-deep-dive/02-cancellation-and-timeout-propagation.md)

## Scenario

`AgentRun` is Acme's background LLM agent. For each run it:

1. loads the conversation and tenant policy,
2. calls up to four tools in parallel (search, CRM lookup, calendar, code interpreter),
3. streams a synthesized answer to the client over SSE.

Runs are expensive: tool calls hit metered providers, and the model bills per token. Users cancel
runs frequently (closing the tab, editing the prompt). The old implementation kept all tool calls
running after cancellation and sometimes continued the LLM stream, billing the tenant for work
nobody would see.

## Goals

- **Cancellation stops provider work**, not just the response.
- **Timeouts are enforced per run** even if the client never disconnects.
- **Cleanup always runs**: release the per-tenant concurrency slot, mark the run `cancelled`,
  persist partial tool results for audit.
- **Cancellation is not retried** and is not counted as a failure.

## Step 1 — Model the run state

```ts
type RunStatus = "running" | "succeeded" | "failed" | "cancelled" | "timed_out";

type RunRecord = {
  id: string;
  tenantId: string;
  status: RunStatus;
  startedAt: string;
  finishedAt?: string;
  failureCode?: string;
  partial?: { completedTools: string[]; failedTools: string[] };
};
```

`cancelled` and `timed_out` are **terminal states distinct from `failed`**. This matters for
retries, dashboards, and billing.

## Step 2 — Build a run-scoped signal

```ts
const RUN_DEADLINE_MS = 25_000;

function runSignal(client: AbortSignal) {
  const controller = new AbortController();
  const onClientAbort = () => controller.abort(new DOMException("client cancelled", "AbortError"));

  client.addEventListener("abort", onClientAbort, { once: true });

  const timer = setTimeout(
    () => controller.abort(new DOMException("run deadline", "TimeoutError")),
    RUN_DEADLINE_MS,
  );

  return {
    signal: controller.signal,
    dispose: () => {
      clearTimeout(timer);
      client.removeEventListener("abort", onClientAbort);
    },
  };
}
```

`dispose()` prevents a leaked timer and listener on every completed run — a subtle memory leak in
long-lived workers.

## Step 3 — Run tools with per-tool failure isolation

```ts
type ToolOutcome =
  | { tool: string; ok: true; value: unknown }
  | { tool: string; ok: false; code: string; retryable: boolean };

async function runTools(signal: AbortSignal): Promise<ToolOutcome[]> {
  const tools = [
    { name: "search", run: (s: AbortSignal) => toolSearch({ signal: s }) },
    { name: "crm", run: (s: AbortSignal) => toolCrm({ signal: s }) },
    { name: "calendar", run: (s: AbortSignal) => toolCalendar({ signal: s }) },
    { name: "code", run: (s: AbortSignal) => toolCode({ signal: s }) },
  ];

  return Promise.all(
    tools.map(async (t) => {
      try {
        return { tool: t.name, ok: true as const, value: await t.run(signal) };
      } catch (err) {
        if (isAbortError(err)) throw err; // cancellation aborts the whole run
        return { tool: t.name, ok: false as const, code: classifyTool(err), retryable: true };
      }
    }),
  );
}
```

Cancellation rethrows so `Promise.all` rejects immediately; **ordinary tool errors are isolated** so
one failed tool does not discard the other three results.

## Step 4 — Handle the terminal outcome

```ts
export async function executeRun(run: RunRecord, client: AbortSignal) {
  const { signal, dispose } = runSignal(client);
  const slot = await concurrency.acquire(run.tenantId, { signal });

  try {
    await runs.markRunning(run.id);

    const outcomes = await runTools(signal);
    const completed = outcomes.filter((o) => o.ok).map((o) => o.tool);
    const failed = outcomes.filter((o) => !o.ok).map((o) => o.tool);

    const answer = await llm.complete({
      prompt: buildPrompt(outcomes),
      signal,
    });

    await runs.complete(run.id, { status: "succeeded", answer });
    return answer;
  } catch (err) {
    if (isAbortError(err)) {
      const status = signal.reason?.name === "TimeoutError" ? "timed_out" : "cancelled";
      await runs.complete(run.id, { status });          // terminal, not a failure
      metrics.increment(`agentrun_${status}`);
      return null;
    }

    const code = classifyRun(err);
    await runs.complete(run.id, { status: "failed", failureCode: code });
    throw err;                                          // let the worker retry if eligible
  } finally {
    dispose();
    await slot.release().catch((e) => log.error({ e }, "slot release failed"));
  }
}
```

Ordering in `finally` matters: dispose the timer, then release the slot. Both are idempotent and
must never mask the primary outcome.

## Step 5 — Propagate to the streaming response

```ts
app.get("/runs/:id/stream", async (req, res) => {
  const controller = new AbortController();
  req.on("close", () => controller.abort());  // client disconnected

  res.on("close", () => controller.abort());
  res.writeHead(200, { "content-type": "text/event-stream" });

  const answer = await executeRun(await runs.get(req.params.id), controller.signal);
  if (answer) res.write(`data: ${JSON.stringify({ answer })}\n\n`);
  res.end();
});
```

The HTTP request lifetime becomes the cancellation source. When the browser closes the tab, every
tool and the LLM call abort within the same event-loop turn.

## Failure-mode review

| Event | Run status | Provider work | Retry? |
| ----- | ---------- | ------------- | ------ |
| Client closes tab | `cancelled` | Aborted | No |
| 25 s deadline | `timed_out` | Aborted | Policy-dependent |
| One tool `500` | `succeeded` (partial) | Other tools continue | Tool-level only |
| LLM `429` | `failed` (`LLM_RATE_LIMITED`) | Aborted | Yes, backoff |
| Worker `SIGTERM` | `cancelled` (drain) | Aborted | Redelivered |
| Slot acquisition timeout | `failed` (`TENANT_BUSY`) | None | Yes, delayed |

## Real-world use case — AgentRun

After the change, Acme's per-run provider spend during cancellations dropped by **~70%** because
tool calls actually stopped. The audit log also improved: cancelled runs retain `partial.completedTools`,
so support can tell whether a user saw partial output before cancelling. Cancelled runs stopped
appearing in the retry queue, which removed a recurring duplicate-tool-call incident.

## Key data / numbers

- Run deadline: **25 s**, inside a 30 s worker/HTTP budget.
- Tenant concurrency slot: acquired with the same signal, so a queued run can be cancelled before
  it starts.
- Cancellation classification: `AbortError` → `cancelled`; `TimeoutError` → `timed_out`.
- `dispose()` is called once per run; missing it leaks one timer + one listener per run.
- Tool failures are isolated; only cancellation aborts the whole `Promise.all`.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Abort provider calls on client disconnect | Only stop writing to the response |
| Distinguish `cancelled`/`timed_out` from `failed` | Record cancellation as an error |
| Isolate ordinary tool failures | Fail the whole run on one tool `500` |
| Dispose timers/listeners in `finally` | Leak a timer per run |
| Release concurrency slots on every path | Hold a tenant slot after cancellation |

## Checklist

- [ ] Is the HTTP request lifetime wired to an `AbortController`?
- [ ] Does every tool and LLM call receive the run signal?
- [ ] Are `cancelled` and `timed_out` distinct terminal states?
- [ ] Are ordinary tool failures isolated from the run outcome?
- [ ] Does cleanup dispose timers, listeners, and concurrency slots?
- [ ] Are cancelled runs excluded from retries?
- [ ] Is cancellation measured as a metric separate from failures?

## Related

- [Cancellation and Timeout Propagation](../02-deep-dive/02-cancellation-and-timeout-propagation.md)
- [Cancellation, Timeouts, and Event-Driven Errors](../01-concepts/03-cancellation-timeouts-and-events.md)
- [Cancellation, Timeouts, and Events](../01-concepts/03-cancellation-timeouts-and-events.md)
- [Chapter 32 — Background Jobs](../../../part-12-async-and-background-jobs/32-background-jobs-queues-and-scheduled-tasks/README.md)
