# A Global Handler and Local Recovery, Together

> Part IV · Chapter 10 · Sections 10.1–10.11 · _Estimated reading time: 24 min_
> **Prerequisite:** [Centralized and Local Handling](../01-concepts/01-centralized-vs-local-handling.md)

## In one sentence

One endpoint — Acme's `AgentRun` (LLM tool-calling agent) — showing the **central handler doing
only mechanical work** and **local recovery doing every business decision**, with a line-by-line
account of what each layer may and may not touch.

## Why this matters in production

Teams argue about centralization in the abstract and then ship a 400-line filter. This file is
the concrete counter-example: the same failure set handled twice — once correctly (local
decision + central rendering) and once incorrectly (everything in the handler) — so you can
review your own filter against a working baseline.

## The endpoint

```http
POST /api/v1/agent-runs
{ "agentId": "agt_22", "input": "Summarize last week's incidents for Acme", "tools": ["search_incidents"] }
```

Failure classes we must handle:

| Failure | Class (Part II) | Desired behavior |
| ------- | --------------- | ---------------- |
| missing/invalid `input` | validation | `422` + field errors |
| tool timeout (2 s) | transient | local fallback: skip tool, continue with prompt-only |
| LLM provider `429` | transient, remote | local: one wait honoring `Retry-After`, then degrade |
| token limit exceeded | expected, local | local: retry once with truncated prompt |
| provider 5xx sustained | operational | central-safety outcome: `503` + `Retry-After` |
| unclassified exception | bug | central safety net: `500` + correlation ID |

## Part 1 — Local recovery (needs context the center lacks)

```ts
// app/agent-run.ts — decisions live where the state lives
export async function runAgent(input: AgentInput, corrId: string): Promise<AgentResult> {
  const prompt = await buildPrompt(input);                 // may throw VALIDATION_* (propagate)

  let toolFacts: Fact[] = [];
  try {
    toolFacts = await withTimeout(runTools(input.tools), 2_000);   // 2 s tool budget
  } catch (err) {
    const e = normalize(err);
    if (e.code === "TOOL_TIMEOUT") {                    // LOCAL recovery #1: degrade, don't fail
      await events.record(corrId, "tool_skipped", { tools: input.tools });
      toolFacts = [];                                   // prompt-only mode
    } else throw e;                                     // anything else keeps traveling
  }

  try {
    const summary = await llm.complete(promptWith(prompt, toolFacts));
    return { status: "ok", summary };
  } catch (err) {
    const e = normalize(err);
    if (e.code === "LLM_RATE_LIMITED") {                // LOCAL recovery #2: one polite wait
      await sleep((e.retryAfterSec ?? 2) * 1000);
      const summary = await llm.complete(promptWith(prompt, toolFacts));
      return { status: "ok", summary, degraded: "rate_limit_wait" };
    }
    if (e.code === "LLM_TOKEN_LIMIT" && !input.truncated) {   // LOCAL recovery #3: shrink, retry once
      return runAgent({ ...input, truncated: true, input: truncate(input.input) }, corrId);
    }
    if (e.code === "LLM_UNAVAILABLE") {                 // sustained outage: degrade with notice
      return { status: "degraded", summary: null, code: "AGENT_PROVIDER_DEGRADED" };
    }
    throw e;                                            // unclassified or non-recoverable
  }
}
```

Every branch here uses information the global handler can never have: whether tools were
optional, how many times we already waited, whether the prompt was already truncated. That is
the whole argument for local recovery (10.2, 10.9).

## Part 2 — The global handler (mechanical only)

```ts
// http/error-filter.ts — imports: registry, normalize, toProblem. Nothing else.
app.use((err: unknown, req: Request, res: Response, next: NextFunction) => {
  if (res.headersSent) return next(err);                      // ordering hazard (deep dive)
  const e = normalize(err);                                   // shape → AppError (utility 10.8)
  const status = STATUS[e.code] ?? 500;                       // mechanical map only
  logger.warn({ code: e.code, reqId: req.id, cause: e.cause }, "request failed");
  res.status(status).json(toProblem(e, req.id));              // one envelope, RFC 9457-shaped
});
```

What it contains and why each line is legal:

| Line | Central? | Reason |
| ------ | -------- | ------ |
| `headersSent` guard | ✅ mechanical | prevents double-write |
| `normalize()` | ✅ mechanical | shared utility, no business branch |
| `STATUS[code]` map | ✅ mechanical | registry-driven, context-free |
| log with cause + ID | ✅ mechanical | observability contract |
| `toProblem()` | ✅ mechanical | one serializer |

Notice what is **absent**: no `retry`, no `if (e.code === "LLM_...")`, no fallbacks, no tenant
checks (10.10).

## Part 3 — What the same endpoint looked like fully centralized (the anti-baseline)

```ts
// ❌ the 400-line filter Acme actually shipped first
if (err.message?.includes("rate limit")) { await sleep(2000); return retryOriginal(req, res); }
if (err.code === "LLM_TOKEN_LIMIT") { req.body.input = truncate(req.body.input); return retryOriginal(req, res); }
if (err.scope === "agent") { return res.status(200).json({ summary: null }); }   // failure→success!
```

Three defects, all predictable from 10.10–10.11: the handler retried **without idempotency
knowledge** (duplicate provider spend), truncated input **without knowing it was already
truncated** (infinite loop on a persistently long prompt — the recursion guard lived below), and
converted outages into `200 { summary: null }` so the UI showed "no summary" instead of an
error, hiding a provider incident for **3 hours**.

## Side-by-side verdict table

| Failure | Local (correct) | Global (correct) | Global-only (broken) |
| ------- | --------------- | ---------------- | -------------------- |
| tool timeout | skip tool, continue | — | 500 (over-fail) or 200-empty (over-degrade) |
| provider `429` | one wait + retry | — | blind retry loop |
| token limit | truncate once, retry | — | unbounded truncate-retry |
| provider down | degrade with `AGENT_PROVIDER_DEGRADED` | renders it if thrown | `200 summary:null` (hidden outage) |
| validation | — | `422` via registry | duplicated per-route shapes |
| unknown bug | — | `500` + correlation ID | depends on message text |

## Key data / numbers

- Tool timeout budget used above: **2 000 ms** per tool group (recommendation; make it a config,
  never a literal in business logic paths without an owner).
- Rate-limit courtesy wait: `Retry-After` seconds × 1000, **one** attempt only.
- Token-limit retry: **exactly one** truncation attempt; the recursion guard (`input.truncated`)
  is mandatory — unbounded retry loops are the classic agent bug (Chapter 44).
- Registry codes used: `VALIDATION_FAILED` (422), `LLM_RATE_LIMITED` (429 + `Retry-After`),
  `LLM_TOKEN_LIMIT` (422-class, non-retryable as-is), `LLM_UNAVAILABLE` (503),
  `AGENT_PROVIDER_DEGRADED` (200-with-flag on the *result object*, not on a thrown error —
  degradation is a **successful** outcome with reduced content, decided locally).
- Central filter size budget: **≤ ~30 lines** of code; if it grows, a decision is hiding (10.13).

## Real-world use case — Acme SaaS `AgentRun`

After the split above, three months of production data: provider-degraded outcomes accounted for
**1.9 %** of runs, all visible in product analytics via the `degraded` flag; unclassified `500`s
dropped **71 %** (many former 500s were token limits now handled locally); and the filter file's
diff frequency fell to roughly one change per quarter — the surest sign centralization is
mechanical again.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Local recovery + mechanical center (shown) | Correct decisions, boring center | Recovery logic distributed by design | Default |
| All in the filter | One file to skim | Wrong on every context-dependent case | Never |
| All local, no center | No center to misuse | Envelope drift, no safety net | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Recover where context lives (tools, retries, truncation) | Recreate context in the filter |
| Mark degradation as a *result*, not a thrown error | Convert thrown errors into `200` in the center |
| Keep the filter under a size budget; review growth | Let the filter accumulate incident patches |
| Give every local recovery a counter/event | Recover silently without observability |

## Common mistakes

- **Degradation without a flag** — the client cannot distinguish "no summary exists" from
  "provider down"; always carry `degraded`/`code`.
- **Recovery loops without attempt guards** — one truncation, one wait; never `while (!ok)`.
- **Testing only the filter** — each local recovery needs its own unit test with the provider
  failure injected (Chapters 51–52 will hold you to it).

## Checklist

- [ ] The filter file has zero business branches (grep-verified).
- [ ] Each optional dependency has a local boundary + degraded result shape.
- [ ] Every local recovery has an attempt guard and an event/counter.
- [ ] Unknown errors still reach the safety net as `500` + correlation ID.

## Related

- [Limits of the Global Handler](../01-concepts/03-limits-of-a-global-handler.md)
- [Consistent Contracts Across Three Services](./02-consistent-contracts-across-services.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
- [Chapter 44 — AI, LLM, and Tool-Calling Errors](../../../part-16-specialized-saas-scenarios/44-ai-llm-and-tool-calling-application-errors/README.md)
