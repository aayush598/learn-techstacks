# Chapter 44 — Reference

> Part XVI · Chapter 44 · Provider error contract, rate-limit and token facts, the stable
> internal error code table, and glossary.

## Provider error contract

| HTTP | Provider code (typical) | Class | Your code | Your HTTP |
| ---- | ----------------------- | ----- | --------- | --------- |
| 400 | `invalid_request_error` | Terminal (bug) | `PROVIDER_REQUEST_INVALID` | 400 |
| 401 | `authentication_error` | Config | `PROVIDER_MISCONFIGURED` | 500 |
| 403 | `permission_error` | Config | `PROVIDER_MISCONFIGURED` | 500 |
| 404 | `not_found_error` | Config | `PROVIDER_MISCONFIGURED` | 500 |
| 422 | `unprocessable` | Terminal | `PROVIDER_REQUEST_INVALID` | 422 |
| 429 | `rate_limit_error` | Retryable | `PROVIDER_RATE_LIMITED` | 429 |
| 429 | `insufficient_quota` | Not retryable | `PROVIDER_QUOTA_EXCEEDED` | 402 |
| 429 | context-window variant | Terminal | `CONTEXT_WINDOW_EXCEEDED` | 413 |
| 500 | `api_error` | Retryable | `PROVIDER_UNAVAILABLE` | 503 |
| 502 | `bad_gateway` | Retryable | `PROVIDER_UNAVAILABLE` | 503 |
| 503 | `service_unavailable` | Overloaded | `PROVIDER_UNAVAILABLE` | 503 |
| 504 | gateway timeout | Timeout (ambiguous) | `PROVIDER_TIMEOUT` | 504 |
| 529 | `overloaded_error` | Overloaded | `PROVIDER_UNAVAILABLE` | 503 |
| — | timeout (no response) | Timeout (ambiguous) | `PROVIDER_TIMEOUT` | 504 |

**Non-negotiables**

- A provider `400` is **your** bug: page, never retry.
- `Retry-After` is a contract, not a hint.
- `insufficient_quota` is **not** a rate limit: stop and escalate.
- Every provider code maps to exactly one internal code, in one table.

## Rate-limit and quota facts

| Fact | Value |
| ---- | ----- |
| Standard retry header | `Retry-After` (seconds or HTTP-date) |
| Rate headers | `x-ratelimit-limit-requests`, `-remaining-requests`, `-reset-requests` |
| Token headers | `x-ratelimit-limit-tokens`, `-remaining-tokens`, `-reset-tokens` |
| Common request limits | 500 / 1,000 / 10,000 per minute |
| Common token limits | 20k / 40k / 200k tokens per minute |
| Recommended retry budget | 3 attempts, jittered, ≤ 10 s per wait |
| Recommended limiter | Token bucket per provider + credential, with a per-tenant share |
| Quota exhaustion signal | `insufficient_quota`, no `retry-after` |

## Token and context facts

| Fact | Value |
| ---- | ----- |
| Context windows | 8k / 128k / 200k tokens |
| Max output tokens | 4,096 / 8,192 / 16,384 |
| Usage fields | `prompt_tokens`, `completion_tokens`, `total_tokens` |
| Estimate | ~4 characters per token; 1 token ≈ 0.75 words |
| Safety margin | Budget ~20% over the estimate |
| Default tool-result cap | ~8 KB (≈2,000 tokens) |
| Input reservation | `maxOutputTokens` + margin, included in the context check |

## `finish_reason` reference

| Value | Meaning | Your code | Your HTTP |
| ----- | ------- | --------- | --------- |
| `stop` | Completed normally | — (success) | 200 |
| `length` | Hit the output cap — **truncated** | `OUTPUT_TRUNCATED` | 502 |
| `tool_calls` | The model wants a tool | — (loop continues) | — |
| `content_filter` | Blocked by the provider | `MODEL_REFUSED` | 422 |
| `refusal` | The model declined | `MODEL_REFUSED` | 422 |
| `function_call` | Legacy tool call | — (loop continues) | — |
| anything else | Unknown | validate anyway, log the raw value | 502 |

## Tool-calling facts

| Fact | Value |
| ---- | ----- |
| Tool call shape | `tool_calls[].function.name` and `.arguments` |
| `.arguments` type | A JSON **string** |
| Tool result shape | A string (JSON-encoded data) returned with `tool_call_id` |
| Default tool deadline | 10 s (30 s for external-API tools, ≤ 60 s ceiling) |
| Invalid-argument repair | 2 consecutive turns maximum |
| Unknown tool | Return a tool result listing the valid tools |
| Permission checks | exposure → entitlement → argument scope → approval |
| Approval | Capture the exact arguments; execute what was approved |
| Side-effect classes | `none` / `read` / `write` |

## Agent loop facts

| Fact | Value |
| ---- | ----- |
| Default step budget | 12 model turns |
| Default tool-call budget | 20 |
| Default token cap | 120,000 per run |
| Default deadline | 120 s wall clock |
| Repetition signature | Tool name + canonicalized arguments, 3 in a row |
| Oscillation signature | A,B,A,B over 4 calls |
| Partial result | A first-class status with a reason and completed steps |
| Freeze boundary | The first successful mutating tool |
| Replay fingerprint | model version, temperature, tool schema hash, retrieved ids, prompt hash |

## Duplicate-effect facts

| Fact | Value |
| ---- | ----- |
| Ledger claim | Atomic `INSERT ... ON CONFLICT DO NOTHING` |
| Ledger states | `claimed` → `applied` \| `failed` |
| Key derivation | Business operation, not the request: `{tenant}:{opType}:{objectId}` |
| Canonicalization | Sorted object keys, no whitespace; array order preserved |
| Ledger TTL | 7 days |
| Stale claim threshold | ~5 minutes |
| Downstream provider | Must also accept an idempotency key |
| Metrics | `replay_suppressed`, `duplicate_suspected` per tool |

## Stable internal error codes

| Code | HTTP | Meaning | Retryable |
| ---- | ---- | ------- | --------- |
| `PROVIDER_UNAVAILABLE` | 503 | Vendor overloaded or down | ✅ |
| `PROVIDER_RATE_LIMITED` | 429 | Request rate exceeded | ✅ after `retry-after` |
| `PROVIDER_QUOTA_EXCEEDED` | 402 | Account budget exhausted | ❌ |
| `PROVIDER_TIMEOUT` | 504 | No response; outcome unknown | ⚠️ only if idempotent |
| `PROVIDER_MISCONFIGURED` | 500 | Key, model, region, or permission problem | ❌ |
| `PROVIDER_REQUEST_INVALID` | 400 | Our request is malformed | ❌ |
| `CONTEXT_WINDOW_EXCEEDED` | 413 | The prompt is too big | ❌ |
| `OUTPUT_TRUNCATED` | 502 | `finish_reason: length` | ❌ raise the cap |
| `MODEL_REFUSED` | 422 | Content filter or refusal | ❌ |
| `OUTPUT_INVALID` | 502 | Failed schema validation | ⚠️ one repair turn |
| `TOOL_NOT_FOUND` | 422 | The model invented a tool | ❌ |
| `TOOL_ARGS_INVALID` | 422 | Arguments failed the tool schema | ⚠️ 2 turns |
| `TOOL_FORBIDDEN` | 403 | Permission denied | ❌ |
| `TOOL_FAILED` | 502 | The tool threw | Depends |
| `TOOL_TIMEOUT` | 504 | The tool did not answer | ⚠️ tool-specific |
| `TOOL_RESULT_TRUNCATED` | 502 | The result exceeded the context budget | ❌ |
| `TOOL_EFFECT_IN_FLIGHT` | 409 | Another worker claimed the effect | ⚠️ wait |
| `EMBEDDING_FAILED` | 503 | The embedding provider failed | ✅ |
| `RETRIEVAL_FAILED` | 503 | The vector store failed or the index mismatched | ✅ |
| `AGENT_BUDGET_EXCEEDED` | 429 | Step, token, or time budget exhausted | ❌ |
| `AGENT_LOOP_DETECTED` | 422 | The model repeated itself | ❌ |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Provider adapter** | The one place that speaks a provider's wire format |
| **Stable contract** | Your own error and response shapes, independent of the provider |
| **Finish reason** | Why the model stopped; `length` and refusals are failures |
| **Truncation** | Output cut off at the token cap; a prefix, not an answer |
| **Repair turn** | One extra inference that fixes an invalid output using the errors |
| **Structured output** | Output constrained by a JSON Schema instead of free text |
| **Tool call** | A model's request to run one of your functions |
| **Tool result** | The data (or error) you return to the model after a tool runs |
| **Capability descriptor** | What a model supports: tools, schema, vision, context |
| **Freeze boundary** | The point after which an agent's plan may not be regenerated |
| **Effect ledger** | A durable record of applied side effects, keyed for replay |
| **Idempotency key** | A key identifying a business operation, not a request |
| **Ambiguous outcome** | A call whose success cannot be determined (timeout after send) |
| **Run fingerprint** | The five logged values that make a run reproducible |
| **Partial completion** | A run that stopped with work done and a reason |

## Signposts

- Provider errors and quotas → [Provider and Quota Failures](../01-concepts/01-provider-and-quota-failures.md)
- Output validation → [Output Validation and Structured Output](../01-concepts/02-output-validation-and-structured-output.md)
- Tool failures → [Tool-Calling Failures](../01-concepts/03-tool-calling-failures.md)
- Loop recovery → [Agent Loop Failures and Recovery](../01-concepts/04-agent-loop-failures-and-recovery.md)
- Idempotency → [Chapter 28 Idempotency](../../../part-11-retry-and-resilience/28-idempotency-and-duplicate-operation-safety/README.md)

## Related

- [Chapter 44 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Chapter 44 Overview](../README.md)
- [Part XVI Index](../../README.md)
