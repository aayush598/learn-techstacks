# Chapter 44 — Do's and Don'ts

> Part XVI · Chapter 44 · All sections

A condensed rule set for AI, LLM, and tool-calling features. Use it as a review checklist
for any change that calls a model or exposes a tool.

## Provider errors

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every provider code once, in one adapter | Branch on provider error strings in feature code |
| Translate to your own stable `AppErrorCode` vocabulary | Leak provider codes to your API clients |
| Honor `Retry-After` exactly when present | Sleep a fixed interval and hope |
| Distinguish a rate limit (retryable) from quota exhaustion (not retryable) | Retry `insufficient_quota` forever |
| Page on a provider `400` — your request is malformed | Retry a `400` |
| Fall back on `503`/`529`, `429`, `401`/`403`/`404` | Fall back on `content_filter` or `length` |
| Cap the retry budget at 3 attempts, jittered | Retry forever inside a request |

## Rate limits and quotas

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Put a token bucket **in front of** the provider adapter | Give each tenant its own limiter |
| Read `x-ratelimit-remaining-requests` and the reset headers | Guess the rate from memory |
| Queue within a bounded budget for interactive features | Fail the user immediately on `429` |
| Share the budget fairly across tenants | Let one tenant exhaust the credential |
| Track tokens per minute, not just requests per minute | Ignore `x-ratelimit-remaining-tokens` |

## Token limits

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check `finish_reason` before reading the body | Assume HTTP 200 means the content is usable |
| Treat `finish_reason: length` as a **failure** | Accept a truncated answer |
| Reserve output tokens when checking the context window | Check the input size only |
| Budget ~20% over the token estimate (~4 chars/token) | Trust the estimate exactly |
| Record `prompt_tokens` / `completion_tokens` / `total_tokens` | Skip usage accounting |
| Pin the embedding model and dimension in the index manifest | Re-embed silently on a model change |

## Timeouts

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify timeouts by kind (connect, first byte, stream idle, total) | Use one timeout for everything |
| Treat a timeout as an **ambiguous** outcome | Treat a timeout as "nothing happened" |
| Use a stream idle timeout measured between chunks | Use a total timeout for a long stream |
| Give every tool its own deadline, shorter than the model timeout | Let a tool inherit the model timeout |
| Propagate `AbortSignal` to the provider and every tool | Cancel only the HTTP request |

## Output validation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate in layers: parse → schema → semantic | `JSON.parse` deep inside business logic |
| Strip Markdown fences and prose preambles | Assume the body is bare JSON |
| Use schema mode with `strict: true` and `additionalProperties: false` | Leave required fields out of the schema |
| Bound the repair turn at one attempt | Loop repairs until one passes |
| Feed the concrete validation errors into the repair prompt | Say "your output was invalid" |
| Map an unknown `finish_reason` to `unknown` | Treat unknown as `stop` |
| Validate tool arguments as a JSON **string** | Treat `tool_calls[].function.arguments` as an object |

## Tool calling

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return tool failures as structured tool results | Throw out of the loop |
| Give every tool a deadline and an `AbortSignal` | Let a hung tool block the run |
| Cap tool results (~8 KB) and say what was dropped | Return the whole dataset |
| Enforce exposure, entitlement, argument scope, and approval | Rely on the prompt to keep the model in bounds |
| Validate tenant scope **inside** the tool as well as the authorizer | Trust the model's document id |
| Capture the exact arguments with an approval request | Re-generate arguments after approval |
| Fix the tool description when arguments are repeatedly invalid | Add retries for a bad tool contract |
| Return the valid tool list for an unknown tool name | Crash the run |

## The agent loop

| ✅ Do | ❌ Don't |
| ----- |--------|
| Bound steps, tool calls, tokens, and wall clock | Let the loop run until it "concludes" |
| Detect repetition using canonicalized arguments | Stop at the first repeated tool name |
| Return partial results with a reason | Discard everything on failure |
| Freeze the plan once a mutating tool succeeds | Re-plan after a write |
| Log the five fingerprint fields per run | Log only the prompt |
| Assert on effects in tests, not on model wording | Assert on identical model output |
| Cancel between turns for server-side agents | Cancel mid-turn and waste the tokens |

## Duplicate side effects

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Claim the effect in a ledger **before** applying it | Apply, then check |
| Use a single atomic `INSERT ... ON CONFLICT DO NOTHING` | `SELECT` then `INSERT` |
| Derive the key from the **business operation** | Derive it from the model's arguments |
| Canonicalize arguments before hashing | Hash the raw JSON string |
| Pass an idempotency key to the downstream provider too | Rely on your ledger alone |
| Record the result so a replay returns it | Record only "done" |
| Reconcile by business object | Discover duplicates from customers |

## Anti-patterns in the wild

1. **The Catch-All Adapter** — `catch { retry() }` around every provider call. Turns a 429
   into four times the request volume.
2. **The 200 Is A Success** — the body is used without checking `finish_reason`. Truncated
   and refused answers ship to users.
3. **The Prompt Is The Permission** — the model decides which tool to call, so it also
   decides whose data to read. One injected document becomes a cross-tenant read.
4. **The Fallback List** — models are tried in order of price, not capability. The cheap
   one does not support structured output, and the feature breaks during a fallback.
5. **The Retried Loop** — the whole agent turn is retried after a provider timeout, and
   the write inside it happens twice.
6. **The Unbounded Run** — no step budget. One vague question cost 41 minutes and 1.2M
   tokens.
7. **The Fingerprint-Free Log** — the prompt is stored, but not the model version, the
   tool schema hash, or the retrieved ids. "It worked yesterday" is undebuggable.

## Chapter checklist

- [ ] One adapter classifies every provider error into your stable vocabulary.
- [ ] `Retry-After` is honored, and rate limits are distinguished from quota exhaustion.
- [ ] A provider-scoped token bucket sits in front of the adapter.
- [ ] `finish_reason` is checked before the body is used.
- [ ] Output is validated in layers, and the repair turn is bounded at one.
- [ ] Tool arguments are parsed and schema-validated before dispatch.
- [ ] Every tool has a deadline, a result cap, and permission checks.
- [ ] The agent loop has budgets for steps, tool calls, tokens, and wall clock.
- [ ] The plan is frozen once a mutating tool succeeds.
- [ ] Every write effect is claimed in a ledger with a business-operation key.
- [ ] Runs record the model version, tool schema hash, and retrieved ids.
- [ ] Fallbacks are capability-filtered, and refusals never route around policy.

## Related

- [Chapter 44 Reference](../05-reference/README.md)
- [Chapter 25 — Third-Party API Error Handling](../../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)
- [Chapter 28 — Idempotency and Duplicate Operation Safety](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)
- [Part XVI Index](../../README.md)
