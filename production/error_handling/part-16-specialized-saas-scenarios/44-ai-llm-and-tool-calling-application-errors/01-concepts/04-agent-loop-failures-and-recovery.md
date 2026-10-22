# Agent Loop Failures and Recovery

> Part XVI · Chapter 44 · Sections 44.11–44.16 · _Estimated reading time: 30 min_
> **Prerequisite:** [Tool-Calling Failures](./03-tool-calling-failures.md)

## In one sentence

An agent is a **loop that can fail on any step and repeat itself**, so its recovery
contract must answer three questions: how many steps are allowed, what survives a failure,
and what is safe to retry.

## Why this matters in production

A single LLM call fails loudly. An agent fails in ways you watch happen in production and
then never reproduce: the loop calls the same tool four times because the model keeps
disliking the answer; the run burns 80,000 tokens because the model found a new tool to
try; the run is cancelled by the user but the provider keeps generating and you still pay
for the tokens; the "same" request produces a different plan today than it did yesterday,
so your regression suite is green and your users are unhappy.

Every one of those is a **loop-level** problem, not a call-level one. Fixing them means
designing the loop, not the adapter.

## The agent loop

```text
  ┌──────────────────────────────────────────────────────────┐
  │  for step in 1..maxSteps:                               │
  │    result = provider.complete(messages, tools)           │
  │    if result.finish_reason == "tool_calls":              │
  │      for call in result.tool_calls:                      │
  │        outcome = dispatch(call)          ← your tool     │
  │        messages.push(toolResult(call, outcome))          │
  │      continue                                           │
  │    return result.text                                    │
  └──────────────────────────────────────────────────────────┘
```

Everything interesting is in the loop's **control flow**: how many iterations, what happens
when a tool fails, what happens when the model asks for the same tool again, and what the
run returns if it never finishes.

## 44.11 — Multi-step agent failures

The failure modes are structural, not accidental:

| Failure | Mechanism | Symptom |
| ------- | --------- | ------- |
| **Runaway loop** | The model keeps requesting tools | Step budget exhausted, huge token bill |
| **Repetition** | The model requests the same tool with the same args | Same side effect, repeated |
| **Oscillation** | Tool A → tool B → tool A → tool B | No progress, cost grows |
| **Budget exhaustion** | Context window fills with tool results | 400 on the next turn |
| **Premature answer** | The model answers without using the tool it needed | Wrong answer, no error |
| **Cascade** | Tool A's failure makes tool B's input invalid | Failure in the wrong layer |

### Bound the loop

```ts
export type AgentBudget = {
  maxSteps: number;          // total model turns
  maxToolCalls: number;      // total tool executions
  maxTokens: number;         // cumulative, prompt + completion
  deadlineMs: number;        // wall clock
};

export const DEFAULT_BUDGET: AgentBudget = {
  maxSteps: 12,
  maxToolCalls: 20,
  maxTokens: 120_000,
  deadlineMs: 120_000,
};
```

**Key data:** a practical default is **12 model turns and 20 tool calls** for a
single-task agent, with a **2-minute wall-clock deadline** and a cumulative token cap.
Customers who want "deeper" research get a different agent with a bigger budget and a
higher price, not an unbounded loop.

### Detect repetition and oscillation

```ts
function detectLoop(toolCalls: ToolCall[]): "repeat" | "oscillation" | null {
  const signatures = toolCalls.map((c) => `${c.function.name}:${canonical(c.function.arguments)}`);
  const last = signatures.at(-1);
  if (signatures.length >= 3 && signatures.at(-2) === last && signatures.at(-3) === last) {
    return "repeat";                         // same call three times running
  }
  if (signatures.length >= 4) {
    const a = signatures.at(-4)!, b = signatures.at(-3)!, c = signatures.at(-2)!, d = last!;
    if (a === c && b === d && a !== b) return "oscillation";   // A,B,A,B
  }
  return null;
}
```

When a loop is detected, **stop and return what you have** with a clear code —
`AGENT_LOOP_DETECTED` — rather than spending the rest of the budget. The user is better
served by a partial answer with a note than by a silent 3-minute burn.

> ⚠️ **Hazard.** Detecting repetition by tool name alone is wrong: calling
> `get_order` with two *different* order ids is legitimate. The signature must include the
> **canonicalized arguments**.

## 44.12 — Partial completion

A run that fails at step 4 of 6 has still learned things. Decide, per step, what is
**durable** and what is **throwaway**.

| Artifact | Durable across failure? | Why |
| -------- | ----------------------- | --- |
| A completed read tool's result | ✅ Yes | Facts do not expire on the next turn |
| A completed write tool's effect | ✅ Yes | It already happened; retrying duplicates it |
| The conversation so far | ✅ Yes | Context for a resumed run |
| A failed tool's partial output | ⚠️ Sometimes | Only if the tool marks output as complete |
| The final answer | ❌ No | It does not exist yet |

So the run's final state is a **status plus what was learned**, not a boolean:

```ts
export type AgentRunResult =
  | { status: "completed"; answer: string; steps: number; tokens: number }
  | { status: "partial"; answer: string | null; reason: string;
      completedSteps: string[]; steps: number; tokens: number }
  | { status: "failed"; code: string; message: string; steps: number; tokens: number }
  | { status: "cancelled"; reason: string; steps: number; tokens: number };
```

The key rule: **a partial result is a first-class success shape**, with the reason
attached. If your API only returns "answer" or "error", a failed agent throws away
everything it learned and the user retries from zero.

**Key data:** persist the run's messages, completed tool effects, and step count on every
step, so a resumed or inspected run can be reconstructed. The three durable facts you
always need are: **which tools had side effects, what their idempotency keys were, and what
the step count was**.

## 44.13 — Retry safety

Three different things get called "retry", and they have different safety rules.

| Retry unit | Safe? | Rule |
| ---------- | ----- | ---- |
| The **provider call** (same messages, same tools) | ⚠️ Only if no tool ran in between | Same request may produce a different plan |
| The **tool call** | Only if the tool is idempotent | Otherwise use the same idempotency key |
| The **whole run** | Only if every side effect is idempotent | Otherwise you duplicate everything |

The trap: a provider call that failed with a 429 is retried, and on the retry the model
chooses a *different* tool. Now the run has done one side effect and the caller thinks it
has done zero.

```ts
export function canRetryCall(
  call: ToolCall, registry: ToolRegistry, seen: Set<string>,
): { retry: boolean; reason?: string } {
  const tool = registry.get(call.function.name);
  if (!tool) return { retry: false, reason: "unknown tool" };
  if (tool.sideEffects === "none") return { retry: true };
  const key = tool.idempotencyKey?.(call.function.arguments);
  if (!key) return { retry: false, reason: "mutating tool without an idempotency key" };
  if (seen.has(key)) return { retry: false, reason: "side effect already applied" };
  return { retry: true };
}
```

**Key data:** a mutating tool **without an idempotency key** is not retryable, full stop.
This is the rule that turns "the provider timed out" from an incident into a non-event.

The deeper problem — that the same request can produce a *different* plan on retry — is the
subject of the next section and the
[retry safety deep dive](../02-deep-dive/01-retry-safety-and-nondeterminism.md).

## 44.14 — Nondeterminism

Two identical requests can produce two different tool plans. This is not a bug to be
eliminated; it is a property you must design around.

| Source of variation | Effect | Can you control it? |
| -------------------- | ------ | ------------------- |
| Sampling (`temperature`) | Different wording, sometimes different plan | Partially — `temperature: 0` reduces but does not remove it |
| Provider-side model updates | Same model name, different behaviour | ❌ No — pin the model **version** (`-2024-08-06` style) |
| Tool descriptions and schemas | Different tool choice | ✅ Yes — version them and log them |
| Retrieved context | Different facts retrieved → different plan | ✅ Yes — log the retrieved ids |
| Conversation ordering / tool result text | Different plan | ✅ Yes — keep the transcript deterministic |
| Provider-side infrastructure | Occasional different behaviour | ❌ No |

```ts
export type RunFingerprint = {
  model: string;             // INCLUDING the pinned version
  temperature: number;
  toolSchemaHash: string;    // hash of every tool's name + schema + description
  retrievedIds: string[];     // which documents were in context
  promptHash: string;
};

export function fingerprint(run: AgentRun): RunFingerprint { /* ... */ }
```

**Key data:** to make a failure reproducible you must log **five** things: the pinned model
version, the temperature, a hash of the tool schemas, the ids of the retrieved documents,
and a hash of the prompt. A stack trace without these is not debuggable — "it worked
yesterday" is the default conclusion.

> ⚠️ **Hazard.** `temperature: 0` is often mistaken for determinism. It makes the sampling
> greedy, which reduces variation but does not eliminate it: provider-side changes, tool
> result ordering, and floating-point differences in the infrastructure still apply. Never
> build an invariant that requires identical outputs.

### The practical consequences

1. **Never branch on the model's exact text.** Branch on parsed structure, and treat the
   parse failure as expected.
2. **Never let the model's choice be the only record of a decision.** If a tool effect
   happened, record it in *your* state, not in the transcript.
3. **Test with recorded tool results, not recorded model outputs.** Replay the transcript
   up to a point and assert on the *effects*.
4. **Expect the model to change its mind.** A plan it approved at step 2 may differ at
   step 4; the state must tolerate that.

**Key data:** pin model versions; hash tool schemas; log retrieved ids; cap the number of
plan revisions. A common pattern is to **freeze the plan after the first turn** — decide
the sequence once, then execute it — which removes most of the nondeterminism from
multi-step runs.

## 44.15 — Fallback model selection

Falling back is a **capability decision**, not a "next best model" decision. The usual
rule — try the flagship, then the smaller model — breaks as soon as the flagship is the
only one that supports structured output, tool use, or a long enough context.

```ts
export type ModelSpec = {
  id: string;
  contextWindow: number;
  maxOutputTokens: number;
  supportsTools: boolean;
  supportsJsonSchema: boolean;
  supportsStreaming: boolean;
  supportsVision: boolean;
  costPerMTokIn: number;
  costPerMTokOut: number;
  regions: string[];
};

export function selectFallback(
  primary: ModelSpec, candidates: ModelSpec[], need: {
    tools: boolean; jsonSchema: boolean; minContext: number; region: string;
  },
): ModelSpec | null {
  const eligible = candidates.filter((m) =>
    (!need.tools || m.supportsTools) &&
    (!need.jsonSchema || m.supportsJsonSchema) &&
    m.contextWindow >= need.minContext &&
    m.regions.includes(need.region) &&
    m.id !== primary.id);
  if (eligible.length === 0) return null;
  return eligible.sort((a, b) =>
    (a.costPerMTokIn + a.costPerMTokOut) - (b.costPerMTokIn + b.costPerMTokOut))[0];
}
```

### When to fall back, and when not to

| Situation | Fall back? | Why |
| --------- | ---------- | --- |
| Provider `503` / `529` (overloaded) | ✅ Yes | Capacity problem, same request |
| Provider `429` (rate limit) | ✅ Yes, if the fallback is a different provider | Different quota pool |
| Provider `429` (quota exhausted) | ✅ Yes | Your budget for that provider is gone |
| Provider `401` / `403` / `404` | ✅ Yes | The key or model id is wrong; another provider may work |
| Context window exceeded | ✅ Yes, to a **bigger** model | A smaller model cannot help |
| `finish_reason: length` | ⚠️ Only to a model with a higher `maxOutputTokens` | More tokens, not a different brain |
| `finish_reason: content_filter` | ❌ No | Another model may refuse the same content |
| Invalid output after a repair turn | ⚠️ Maybe | Only if the fallback supports the same output format |
| Your own bug (schema rejected at request time) | ❌ No | Another model will not fix your request |

> ⚠️ **Hazard.** Falling back on `content_filter` is a policy violation waiting to happen:
> the primary provider refused the content, and the fallback provider accepts it. If you
> must have a content policy, enforce it in **your** code, once, for every provider.

**Key data:** a fallback chain is typically **primary → same-provider smaller model →
different provider**, chosen by a capability filter (tools, JSON schema, context window,
region, vision) and then by cost. Log which model served every request — without that,
"the fallback served 40% of traffic" is invisible until the bill arrives.

## 44.16 — Cancellation

Cancellation must be **cheap** and must be **honoured at every layer**.

```ts
export async function runAgent(req: AgentRequest, signal: AbortSignal): Promise<AgentRunResult> {
  const controller = new AbortController();
  const onAbort = () => controller.abort();
  signal.addEventListener("abort", onAbort);
  try {
    const res = await provider.complete({ ...req }, { signal: controller.signal });
    // ... loop, passing controller.signal to every tool
  } catch (err) {
    if (signal.aborted || isAbortError(err)) {
      return { status: "cancelled", reason: "client disconnected", steps, tokens };
    }
    throw err;
  } finally {
    signal.removeEventListener("abort", onAbort);
  }
}
```

Rules:

1. **Propagate the signal** into the provider call and every tool. A tool that ignores the
   signal keeps burning money after the user leaves.
2. **Check the signal between steps**, not only inside the provider call — the gap between
   steps is where cancellation usually gets lost.
3. **Return `cancelled`, not `failed`.** A cancelled run is not an error; it is an
   outcome with its own code.
4. **Record what already happened.** A cancelled run may have executed three writes; the
   record of those writes must survive the cancellation.

> ⚠️ **Hazard.** Aborting the HTTP request does not stop the provider from generating. The
   tokens are billed. Cancellation reduces *your* waste (tools, loops, follow-up calls);
   it does not refund the tokens already spent on the in-flight generation.

**Key data:** a cancelled run still costs the tokens already generated — typically **one
full model turn (up to `maxOutputTokens`)** per uncancelled in-flight call. Cancel
**between** turns, not mid-turn, if you want to avoid a half-spent turn.

## Worked example — the research agent

Acme's `AgentRun` research agent answers a question by searching the knowledge base and
reading documents. Three incidents shaped the design:

**Incident 1 — the 40-minute run.** A vague question made the model try five different
search phrasings, then read every result, then re-search. The run took 41 minutes and
burned 1.2M tokens. The fix: a step budget (12 turns, 20 tool calls), a cumulative token
cap, and repetition detection that stopped the run at turn 6 with a partial answer and a
note — the user got a useful answer in 90 seconds instead of a timeout in 41 minutes.

**Incident 2 — the doubled email.** A "summarize and notify" agent hit a provider 503
after the notification tool had already run. The retry re-ran the whole turn and sent the
email again. The fix: the notification tool required an idempotency key derived from
`(runId, step, args)`, and the retry path reused the key — the second attempt returned the
first attempt's result instead of re-sending.

**Incident 3 — the un-reproducible bug.** A user's report ("it summarized the wrong
document") was impossible to reproduce because the logs had the prompt but not the model
version, the tool schema hash, or the retrieved document ids. The fix: the run fingerprint
now logs all five values, and the incident was traced to a provider-side model update that
changed retrieval behavior — a problem that would have been invisible without the
fingerprint.

## Key data

| Fact | Value |
| ---- | ----- |
| Default step budget | **12 model turns**, **20 tool calls** |
| Default run deadline | **120 s** wall clock |
| Cumulative token cap | ~120,000 tokens for a single-task agent |
| Repetition detection | Same tool **+ canonicalized args**, 3 in a row |
| Oscillation detection | A,B,A,B pattern over 4 calls |
| Retry safety rule | A mutating tool without an idempotency key is **not** retryable |
| Fallback filter | tools, JSON schema, context window, region, vision → then cost |
| Fallback chain | primary → same-provider smaller → different provider |
| Fallback is wrong for | `content_filter`, your own request bugs |
| Cancellation | Propagate `AbortSignal` to the provider **and** every tool |
| Reproducibility log | model version, temperature, tool schema hash, retrieved ids, prompt hash |

## Real-world use case

A multi-tenant SaaS gives each customer an AI assistant that can read their tickets,
search their docs, and post internal notes. The assistant is an agent loop with six
tools, three of them writes.

The team found the assistant retrying an entire turn after a provider 503 and posting the
note twice, because the retry re-entered the tool layer. They fixed it with one rule: the
loop's retry path may only re-execute a tool through its idempotency key, and every write
tool derives that key from `(runId, toolName, canonicalArgs)` — so a re-execution returns
the recorded result instead of performing the effect again.

The second fix was a capability filter on the fallback chain: the flagship model supports
structured output and the smaller one does not, so the fallback was silently producing
unparseable answers. With the filter in place, the fallback is now chosen only among
models that support the features the run declared, and the run's fingerprint records which
model served it. Support can now answer "which model served this run" from the log
instead of guessing.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Hard step budget | Bounds cost and latency | Truncates deep runs | ✅ Always |
| Token cap only | Bounds cost | Not latency, not runaway loops | Also always |
| Repetition detection | Stops the pathological case | Needs canonical argument hashing | ✅ Always |
| Freeze the plan after turn 1 | Removes most nondeterminism | Less adaptive | Structured workflows |
| Let the model replan | Better quality | Unpredictable cost | Open-ended research |
| Fallback by capability | Correct outputs | More configuration | ✅ Always |
| Fallback by "next best model" | Simple | Breaks on format/tool support | Never |
| Cancel mid-turn | Fastest response | Wastes the turn's tokens | Interactive UIs |
| Cancel between turns | No wasted turn | Slower to notice | ✅ Server-side agents |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Bound steps, tool calls, tokens, and wall clock | Let the loop run until it "concludes" |
| Detect repetition using arguments, not just tool names | Stop at the first repeated tool name |
| Return partial results with a reason | Discard everything on failure |
| Give every mutating tool an idempotency key | Retry a mutating tool without one |
| Pin the model version | Log the model name only |
| Filter fallbacks by capability | Fall back to the next model in a list |
| Never fall back on `content_filter` | Treat a provider refusal as provider-specific |
| Propagate `AbortSignal` to tools | Cancel only the provider request |
| Return `cancelled` as its own status | Report cancellation as failure |

## Common mistakes

- **No step budget.** One vague question, 41 minutes, 1.2M tokens.
- **Retry granularity at the wrong level.** Re-running the whole turn re-runs the tools.
- **Binary success/failure.** Everything learned in a failed run is thrown away.
- **Assuming `temperature: 0` means deterministic.** It does not.
- **Logging the prompt but not the model version.** "It worked yesterday" is undebuggable.
- **Fallback chosen by list order.** The fallback may not support the required format.
- **Falling back after a content filter.** You just bypassed your own policy.
- **Cancelling without checking between steps.** The loop keeps running one more turn.

## Checklist

- [ ] The run has a step budget, a tool-call budget, a token cap, and a deadline.
- [ ] Repetition and oscillation detection use canonicalized arguments.
- [ ] Loop detection returns a partial result with a reason, not a silent stop.
- [ ] Partial completion is a first-class result shape.
- [ ] Every mutating tool has an idempotency key.
- [ ] The run fingerprint logs model version, temperature, tool schema hash, retrieved ids,
      and prompt hash.
- [ ] Fallbacks are filtered by capability before cost.
- [ ] `content_filter` and `refusal` never trigger a fallback.
- [ ] `AbortSignal` reaches the provider call and every tool.
- [ ] Cancellation is a distinct status and is checked between steps.

## Related

- [Tool-Calling Failures](./03-tool-calling-failures.md)
- [Provider Contracts and Retrieval Failures](./05-provider-contracts-and-retrieval-failures.md)
- [Retry Safety and Nondeterminism](../02-deep-dive/01-retry-safety-and-nondeterminism.md)
- [Duplicate Side Effects During Agent Retries](../02-deep-dive/02-duplicate-side-effects-during-agent-retries.md)
