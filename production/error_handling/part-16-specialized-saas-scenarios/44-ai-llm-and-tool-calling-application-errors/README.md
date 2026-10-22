# Chapter 44 — AI, LLM, and Tool-Calling Application Errors

> Part XVI · _Estimated reading time: 90–110 min_
> **Prerequisite:** [Chapter 43 — File and Media Processing Errors](../43-file-and-media-processing-errors/README.md)

## One-sentence summary

AI features fail in a way no other feature fails: the **provider** can be down, the **model**
can be wrong, and **your own tools** can be the thing that breaks — and the retry that fixes
the first one can **duplicate a side effect** in the third.

## Why this chapter matters

A conventional API either works or returns an error. An LLM feature has four failure planes
at once: the provider's transport (429, 503, timeouts), the model's behaviour (invalid
output, truncated output, refusals), your **tool layer** (a tool that times out, a tool that
is called with the wrong arguments, a tool that lacks permission), and the **agent loop**
that stitches them together (partial completion, duplicate side effects, infinite
retries). Teams that treat an LLM call like an HTTP call get the worst of both worlds: they
retry non-idempotent tool calls, they surface a raw provider stack trace to a customer, and
they cannot tell "the provider was overloaded" from "my code passed the wrong tool
arguments."

The mental shift: **the model call is a probabilistic, non-idempotent, side-effecting
operation that happens to be delivered over HTTP.** Every chapter section below maps to one
decision you have to make about that operation.

## Chapter map

The chapter has 20 sections grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-provider-and-quota-failures.md`](./01-concepts/01-provider-and-quota-failures.md) | 44.1–44.4 | Provider errors, rate limits and quotas, token limits, timeouts |
| [`01-concepts/02-output-validation-and-structured-output.md`](./01-concepts/02-output-validation-and-structured-output.md) | 44.5–44.6 | Invalid model output, structured-output schema validation |
| [`01-concepts/03-tool-calling-failures.md`](./01-concepts/03-tool-calling-failures.md) | 44.7–44.10 | Tool invocation failures, tool timeouts, tool permissions, invalid tool arguments |
| [`01-concepts/04-agent-loop-failures-and-recovery.md`](./01-concepts/04-agent-loop-failures-and-recovery.md) | 44.11–44.16 | Multi-step agents, partial completion, retry safety, nondeterminism, fallbacks, cancellation |
| [`01-concepts/05-provider-contracts-and-retrieval-failures.md`](./01-concepts/05-provider-contracts-and-retrieval-failures.md) | 44.17–44.20 | Provider vs app errors, retrieval/embedding failures, duplicate side effects, portable contracts |
| [`02-deep-dive/01-retry-safety-and-nondeterminism.md`](./02-deep-dive/01-retry-safety-and-nondeterminism.md) | 44.13, 44.14 | When a retry is safe, why identical prompts diverge, retry budgets |
| [`02-deep-dive/02-duplicate-side-effects-during-agent-retries.md`](./02-deep-dive/02-duplicate-side-effects-during-agent-retries.md) | 44.12, 44.19 | Tool-call idempotency, dedupe ledgers, compensating actions |
| [`03-practical-examples/01-agentrun-tool-calling-loop.ts`](./03-practical-examples/01-agentrun-tool-calling-loop.ts) | 44.7–44.11, 44.13, 44.19 | An `AgentRun` loop with typed tool errors and idempotent tools |
| [`03-practical-examples/02-fallback-model-selection.md`](./03-practical-examples/02-fallback-model-selection.md) | 44.3, 44.15, 44.17 | Model routing, capability-aware fallbacks, cost ceilings |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules and anti-patterns for AI features |
| [`05-reference/README.md`](./05-reference/README.md) | all | Provider error contract, token and rate-limit facts, stable internal codes |

## Learning objectives

By the end you can:

- Classify a provider error into **retryable, terminal, or configuration** and pick the
  right HTTP status for your own API.
- Reason about **rate limits** using `Retry-After` and the `x-ratelimit-*` headers instead
  of a fixed sleep.
- Detect **truncation** (`finish_reason: length`) and **refusal** (`content_filter`,
  `refusal`) as distinct outcomes, not as "empty output".
- Validate model output against a **JSON schema** and fail with a repair turn rather than a
  500.
- Design a **tool layer** with its own timeouts, permission checks, and argument
  validation — independent of the model call.
- Prove a retry of an agent loop **cannot duplicate a side effect**.
- Keep one **stable internal error contract** while swapping providers underneath.

## Key takeaways

1. **A model call is not an HTTP call.** It is non-deterministic, can be truncated, and its
   "errors" often arrive as a successful response with an unusable body.
2. **Classify the provider, then translate.** One adapter owns every provider code; the
   rest of your codebase sees only your own stable codes.
3. **Rate limits are a budget, not an obstacle.** Honor `Retry-After`; keep a token bucket
   per provider and per tenant.
4. **`finish_reason` is the most important field in the response.** `length` and
   `content_filter` are failures that arrive with HTTP 200.
5. **Tools are your code, and they fail like your code.** Validate arguments, enforce
   permissions, and give every tool its own deadline.
6. **Retries are only safe when the loop is idempotent.** A retried tool call that charges
   a card is a billing incident, not a retry.
7. **Fall back on capability, not on fame.** A smaller model may not support the tool or
   the output format you need; route by capability, then by cost.

## Exercises

1. Take your LLM feature and write down its provider error map: for every provider code,
   the class, your internal code, and your HTTP status. Find the codes you have not
   classified.
2. Force a `finish_reason: length` response and prove your code surfaces a distinct
   `OUTPUT_TRUNCATED` error instead of an empty result.
3. Add a JSON-schema validation step to one feature and count how many previously
   "successful" responses would now be rejected.
4. Write a tool that is safe to call twice — prove it with the same idempotency key.
5. Add a token-bucket limiter per provider and watch the 429 rate drop to zero.
6. Define a fallback chain and verify each fallback supports the features the primary
   does (tools, structured output, context window).

## Related

- [Chapter 43 — File and Media Processing Errors](../43-file-and-media-processing-errors/README.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Chapter 25 — Third-Party API Error Handling](../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)
- [Chapter 28 — Idempotency and Duplicate Operation Safety](../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Chapter 39 — Partial Failures and Multi-Step Operations](../../part-15-distributed-failures/39-partial-failures-and-multi-step-operations/README.md)
