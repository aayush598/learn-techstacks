# Provider and Quota Failures

> Part XVI · Chapter 44 · Sections 44.1–44.4 · _Estimated reading time: 28 min_
> **Prerequisite:** [Chapter 25 — Third-Party API Error Handling](../../../part-10-external-dependencies/25-third-party-api-error-handling/README.md)

## In one sentence

Provider failures are **transport-shaped**: a status code, a rate-limit header, a timeout —
and the whole job of your adapter is to turn each one into a **classified, retryable-or-not
decision** before it reaches the rest of your code.

## Why this matters in production

An AI feature's user-visible failure rate is dominated by a very small set of provider
conditions: quota exhausted, request rate exceeded, model overloaded, and a context window
that was too small. None of them are your bug, and all of them look like a 500 if you let
the raw response through. But they need **opposite** handling: a 429 wants a delay, a 400
wants a code change, an overloaded 529 wants a fallback model, and a quota error wants a
ticket to finance — not three identical exponential backoffs.

The failure mode that costs the most is the "polite" adapter that catches everything and
retries three times. Under load it turns a provider's 429 into 4× the request volume, the
provider's overload into a longer queue, and the user's 30-second wait into a timeout.

## The provider error surface

Most major providers converge on a similar shape even though the names differ:

| HTTP | Provider code (typical) | What it means | Class |
| ---- | ----------------------- | ------------- | ----- |
| 400 | `invalid_request_error` | Malformed request: bad JSON, missing required field, unknown model param | **Terminal** (bug) |
| 401 | `authentication_error` | Missing, malformed, or revoked API key | **Terminal** (config) |
| 403 | `permission_error` | Key valid but not allowed: region, tier, or feature gate | **Terminal** (config) |
| 404 | `not_found_error` | Model or deployment id does not exist | **Terminal** (config) |
| 422 | `unprocessable` | Well-formed but semantically rejected | **Terminal** |
| 429 | `rate_limit_error` | Rate or quota exceeded | **Retryable** |
| 500 | `api_error` | Provider internal error | **Retryable** |
| 502 / 504 | `bad_gateway` / gateway timeout | Provider edge failure | **Retryable** |
| 503 | `service_unavailable` | Temporarily unavailable | **Retryable** |
| 529 | `overloaded_error` | Model capacity exhausted | **Retryable** (prefer fallback) |

> ⚠️ **Hazard.** Providers reuse `400` for *two* very different things: "your request is
> malformed" (a bug) and "your context window is too big" (a user input problem). Never
> collapse both into one 400. Inspect the error body for the specific subtype before
> choosing the user-facing code.

**Key data:** `429` is the only status with a standard retry contract — `Retry-After`, in
seconds or as an HTTP date. `529` is the modern "overloaded" signal and appears on some
providers; treat it as retryable but with a **fallback** preferred over a wait.

## 44.1 — Provider failures

The first rule: **one adapter owns every provider code.** Nothing else in your codebase
should branch on `err.code === "rate_limit_error"`.

```ts
export type ProviderErrorClass =
  | "retryable"        // retry the same request, same inputs
  | "terminal"         // do not retry; fix the code or the config
  | "config"           // key/model/region/permission problem
  | "overloaded"       // retry once, or fall back to another model
  | "quota_exhausted"  // account-level: not a per-request retry
  | "cancelled";       // the caller went away

export class ProviderError extends Error {
  constructor(
    readonly provider: string,
    readonly providerCode: string,
    readonly httpStatus: number,
    readonly cls: ProviderErrorClass,
    readonly detail: Record<string, unknown> = {},
    readonly retryAfterMs?: number,
  ) {
    super(`${provider}:${providerCode}`);
    this.name = "ProviderError";
  }
}

export function classifyProviderError(provider: string, status: number, body: unknown,
                                     headers: Record<string, string>): ProviderError {
  const code = readProviderCode(body);          // "rate_limit_error", "overloaded_error", …
  const retryAfter = parseRetryAfter(headers["retry-after"]);
  if (status === 429) {
    // 429 splits into a *rate* limit and a *quota* limit. Only one is retryable.
    const isQuota = /quota|billing|credit/i.test(code) || readQuotaExhausted(body);
    return new ProviderError(provider, code, status,
      isQuota ? "quota_exhausted" : "retryable", {}, retryAfter);
  }
  if (status === 529 || status === 503) return new ProviderError(provider, code, status, "overloaded", {}, retryAfter);
  if (status >= 500)  return new ProviderError(provider, code, status, "retryable", {}, retryAfter);
  if (status === 401) return new ProviderError(provider, code, status, "config");
  if (status === 403) return new ProviderError(provider, code, status, "config");
  if (status === 404) return new ProviderError(provider, code, status, "config");
  return new ProviderError(provider, code, status, "terminal");   // 400 / 422
}
```

**Key data:** a `429` carrying `insufficient_quota` is **not** retryable. Retrying it burns
latency and, on some providers, counts against a stricter abuse limit. Detect it and fail
fast with `PROVIDER_QUOTA_EXHAUSTED` (HTTP 402 to your caller, or 503 if the customer is
prepaid).

### The retry contract

```ts
export function retryDecision(err: ProviderError, attempt: number): "retry" | "fallback" | "stop" {
  if (err.cls === "cancelled") return "stop";
  if (err.cls === "quota_exhausted" || err.cls === "config" || err.cls === "terminal") return "stop";
  if (err.cls === "overloaded") return attempt >= 1 ? "fallback" : "retry";
  return attempt < 3 ? "retry" : "stop";     // plain transient: up to 3 attempts
}
```

**Key data:** the recommended default budget is **3 attempts** with jittered exponential
backoff, capped at ~10 s per wait, plus **honoring `Retry-After` exactly** when the header
is present. `Retry-After` is a contract, not a hint.

## 44.2 — Rate limits and quotas

Rate limiting has two distinct regimes and confusing them is the single most common bug in
LLM integrations.

| Regime | Symptom | Meaning | Correct response |
| ------ | ------- | ------- | ---------------- |
| **Request rate** | 429 with `x-ratelimit-remaining-requests: 0` | You are sending too fast | Wait `retry-after`, then resume |
| **Token rate** (TPM) | 429 with `x-ratelimit-remaining-tokens: 0` | Your requests are too large | Shrink the request or wait |
| **Daily/monthly quota** | 429 with `insufficient_quota`, no `retry-after` | The account is out of budget | **Stop** — escalate to billing |

### Read the headers, do not guess

```text
x-ratelimit-limit-requests: 500
x-ratelimit-remaining-requests: 0
x-ratelimit-reset-requests: 1.5s
x-ratelimit-limit-tokens: 40000
x-ratelimit-remaining-tokens: 0
x-ratelimit-reset-tokens: 12s
retry-after: 2
```

A correct client derives its next send time from the **reset** header, not from a
backoff guess:

```ts
export function nextSendAt(headers: Record<string, string>, now = Date.now()): number {
  const retryAfter = parseRetryAfter(headers["retry-after"]);
  if (retryAfter != null) return now + retryAfter;
  const reset = headers["x-ratelimit-reset-requests"];      // "1.5s" | "12s" | "2026-01-01T00:00:00Z"
  if (reset) {
    if (/^\d+(\.\d+)?(ms|s|m)$/.test(reset)) return now + parseDuration(reset);
    const at = Date.parse(reset);
    if (!Number.isNaN(at)) return at;
  }
  return now + 500;      // last-resort default, not a policy
}
```

> ⚠️ **Hazard.** A **global** limiter in front of a shared provider key is the only thing
> that protects you from your own traffic. Ten tenants each with their own client-side
> limiter still produce 10× the rate. Put the token bucket **in front of the provider
> adapter**, keyed by provider + credential + tenant, and share it.

**Key data:** the `x-ratelimit-*` headers are provider-specific but follow a common shape;
treat unknown headers defensively. Recommended per-tenant default: a **token bucket** sized
from the provider's `x-ratelimit-limit-requests` per minute, refilled continuously rather
than in fixed windows (a fixed window lets you burst 2× at the boundary).

### Queuing beats failing

Under sustained load, the right behavior for a rate limit is to **queue** within a bounded
budget, not to fail the user:

```ts
const budgetMs = 8_000;          // total time the caller is willing to wait
const deadline = Date.now() + budgetMs;
while (true) {
  const wait = limiter.reserve(1);              // token bucket, provider-scoped
  if (wait > deadline) throw new ProviderError("local", "RATE_LIMIT_BUDGET_EXCEEDED",
    429, "retryable", { budgetMs });
  await sleep(wait);
  try {
    return await send();
  } catch (err) {
    if (!(err instanceof ProviderError) || err.cls !== "retryable") throw err;
    await sleep(err.retryAfterMs ?? nextSendAt(err.headers) - Date.now());
  }
}
```

## 44.3 — Token limits

Token limits are limits on **sizes**, and they fail silently.

| Limit | Typical values | Failure shape |
| ----- | -------------- | ------------- |
| Context window (input + output) | 8k / 128k / 200k | 400 `invalid_request_error` — often misread as a bug |
| Max output tokens | 4096 / 8192 / 16384 | 200 OK, `finish_reason: length` — **truncated** |
| Max input tokens | provider-specific | 400 or a truncated prompt |
| Requests per minute | 500 / 1000 / 10,000 | 429 |
| Tokens per minute | 20k / 40k / 200k | 429 |

### Token accounting

```ts
export type TokenUsage = {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
};

/** ~4 characters per token for English prose; ~1 token ≈ 0.75 words. */
export function estimateTokens(text: string): number {
  return Math.ceil(text.length / 4);
}
```

**Key data:** budget with a **safety margin of ~20%** over the estimate, because estimates
under-count JSON, code, and non-English text. The authoritative number arrives in the
response `usage` object as `prompt_tokens`, `completion_tokens`, and `total_tokens` — always
record it; it is the only way to attribute cost.

### Truncation: the failure with a 200

```ts
const res = await client.complete({ model, messages, maxTokens: 4096 });
if (res.finishReason === "length") {
  // The model wanted to keep writing. The output is a prefix, not an answer.
  throw new AppError("OUTPUT_TRUNCATED", {
    model, requested: 4096, used: res.usage.completionTokens,
  });
}
```

A truncated answer can be syntactically valid JSON and semantically incomplete — the worst
combination, because a validator will accept it. Always check `finish_reason` **before**
validating the body.

**Key data:** `finish_reason` values to handle explicitly: `stop` (complete),
`length` (truncated — **a failure**), `tool_calls` (model wants a tool),
`content_filter` (blocked by the provider), `refusal` (model declined), and the legacy
`function_call`.

### Oversized context: fail with a useful code

```ts
export function checkContext(model: ModelSpec, messages: Message[]): void {
  const used = estimateTokens(messages.map((m) => m.content).join("\n"));
  const reserve = Math.floor(model.maxOutputTokens * 1.2);   // room for the answer
  if (used + reserve > model.contextWindow) {
    throw new AppError("CONTEXT_WINDOW_EXCEEDED", {
      estimatedTokens: used, contextWindow: model.contextWindow,
    });
  }
}
```

**Key data:** the check must include the **output reservation**, or you will send requests
that pass your input check and fail at the provider. 20% over the estimate is a common
default; measure against your real `usage` numbers rather than trusting the heuristic.

## 44.4 — Timeouts

A timeout is an **ambiguous** error: you do not know whether the provider finished the work.
That matters for billing and for side effects, so give timeouts their own identity.

| Timeout | Bounds | Typical default |
| ------- | ------ | --------------- |
| Connect | TCP + TLS handshake | 5 s |
| Read (first byte) | Time to the response headers | 30–60 s |
| Read (streaming idle) | Gap between SSE chunks | 30 s |
| Total | Whole request wall clock | 60–300 s |
| Tool | Each tool invocation | 5–30 s, **your own** deadline |

```ts
export type TimeoutKind = "connect" | "first_byte" | "stream_idle" | "total" | "tool";

export class TimeoutError extends Error {
  constructor(readonly kind: TimeoutKind, readonly elapsedMs: number,
              readonly ambiguous: boolean) {
    super(`timeout:${kind}`);
    this.name = "TimeoutError";
  }
}
```

The ambiguity rule:

| Timeout | Ambiguous? | Why | Safe to retry? |
| ------- | ---------- | --- | ------------- |
| Connect | ❌ No | The request never left the process | ✅ Yes |
| First byte | ⚠️ Yes | The provider may have started work | ✅ Only if the call has no side effect |
| Stream idle | ⚠️ Yes | Partial output already delivered | ⚠️ Resume/partial, not blind retry |
| Total | ⚠️ Yes | Work may have completed and been billed | ⚠️ Only with idempotency |
| Tool | Depends | Your tool decides | Tool-specific |

**Key data:** streaming idle timeout should be measured **between chunks**, not from the
request start — a 2-minute generation that emits every 200 ms must not trip a 60-second
total timeout. Recommended: connect 5 s, first byte 30 s, stream idle 30 s, total 300 s for
long generations, and an independent tool deadline of 10–30 s.

> ⚠️ **Hazard.** Aborting an HTTP request does not cancel the provider's work. The model
> keeps generating and you still pay for the tokens. Treat a timeout as "the result is
> unknown", not as "the work stopped".

## Worked example — the summarize feature under load

Acme's `AgentRun` feature summarizes a customer's project notes. During a launch week,
requests tripled and the error rate went to 12%. The dashboard showed only `500`. The
diagnosis took an afternoon:

- 60% of the failures were provider `429` with `retry-after: 2` — the client slept a
  fixed 250 ms and retried three times, turning one request into four.
- 25% were `503` from a region that had no capacity — a fallback model in another region
  would have served them.
- 15% were context-window 400s, because the notes feature concatenated every comment in
  the project without a cap.

The fix was three small changes and one structural one: read `retry-after` instead of
sleeping a fixed interval; add a provider-scoped token bucket in front of the adapter;
route 503/529 to a fallback model; and cap the notes input by tokens, not by characters.
The user-visible error rate fell from 12% to 0.4% and the remaining 0.4% were genuine
quota exhaustion, which now surfaced as `PROVIDER_QUOTA_EXHAUSTED` to the account owner
rather than a 500.

## Key data

| Fact | Value |
| ---- | ----- |
| Retryable provider statuses | 429 (rate), 500, 502, 503, 504, 529 |
| Terminal provider statuses | 400 (except context/code variants), 422 |
| Configuration provider statuses | 401, 403, 404 |
| Standard retry header | `Retry-After` (seconds or HTTP-date) |
| Rate-limit headers | `x-ratelimit-limit-requests`, `-remaining-requests`, `-reset-requests`, plus `-tokens` variants |
| Recommended retry budget | 3 attempts, jittered, ≤ 10 s per wait, honoring `Retry-After` |
| Context windows | 8k / 128k / 200k tokens |
| Max output tokens | 4096 / 8192 / 16384 |
| Usage fields | `prompt_tokens`, `completion_tokens`, `total_tokens` |
| Token estimate | ~4 characters per token; 1 token ≈ 0.75 words; budget +20% |
| Truncation signal | `finish_reason: length` |
| Refusal signals | `finish_reason: content_filter` / `refusal` |
| Recommended timeouts | connect 5 s, first byte 30 s, stream idle 30 s, total 300 s |

## Real-world use case

A multi-tenant project-management SaaS ships an "summarize this project" feature. Tenants
share one provider credential. On a Tuesday morning a partner's integration starts
retrying hard, and the shared credential's per-minute request limit is exhausted. Every
tenant now sees a 500. Because the adapter had no quota detection, the team throttled the
retry loop "to be safe" and, for two hours, the feature was down for everyone while a
single misbehaving integration consumed the budget.

The rebuilt adapter classifies the `429` by body (`insufficient_quota` vs `rate_limit`),
reads `retry-after`, and applies a provider-scoped token bucket with a per-tenant share so
one tenant cannot starve the others. Quota exhaustion now returns `PROVIDER_QUOTA_EXHAUSTED`
to the account owner and a `402` to the API caller, and the retry path is bounded to three
attempts. The next quarter, a single tenant's 40× traffic increase degraded that tenant
to a slow lane instead of taking the feature down for the other nine.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Honor `Retry-After` exactly | Matches the provider's own accounting | Adds latency you might avoid | ✅ Always when the header exists |
| Fixed exponential backoff | Simple, no header parsing | Amplifies 429 storms | Only when no header is available |
| Client-side token bucket per tenant | Prevents one tenant starving others | Needs shared state | ✅ Multi-tenant apps |
| Single global limiter | Simplest, protects the credential | One tenant can still dominate | Single-tenant apps |
| Fail fast on 429 | Honest latency | User-visible errors during bursts | Non-interactive features |
| Queue within a budget | Keeps the feature working | Needs a deadline and a queue | ✅ Interactive features |
| Estimate tokens before sending | Avoids 400s and waste | Estimate is approximate | ✅ Always, then verify with `usage` |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every provider code in one adapter | Branch on provider codes in feature code |
| Honor `Retry-After` when present | Sleep a fixed interval and hope |
| Distinguish rate limit from quota exhaustion | Retry `insufficient_quota` forever |
| Check `finish_reason` before reading the body | Assume HTTP 200 means success |
| Reserve output tokens when checking the context window | Check input size only |
| Record `usage` on every call | Skip token accounting |
| Give streaming an idle timeout, not only a total timeout | Use one total timeout for a 5-minute stream |
| Treat a timeout as an ambiguous outcome | Treat a timeout as "the work stopped" |
| Keep one provider-scoped limiter in front of the adapter | Let every tenant send its own burst |

## Common mistakes

- **Retrying a 400.** Context-window and schema errors are not transient; retrying them
  burns the budget and delays the real error.
- **Sleeping past the `Retry-After`.** You get another 429 and the backoff compounds.
- **Confusing 429 with quota.** `insufficient_quota` needs an escalation path, not a retry.
- **Ignoring `finish_reason: length`.** The output is a prefix; downstream code treats it as
  an answer.
- **Validating the body before checking truncation.** A truncated JSON object often passes
  a loose schema.
- **Using a total timeout for streaming.** Long legitimate generations get killed.
- **One limiter per tenant with a shared key.** The aggregate still exceeds the limit.

## Checklist

- [ ] One adapter classifies every provider code into retryable / terminal / config /
      overloaded / quota_exhausted / cancelled.
- [ ] `Retry-After` is honored exactly when present.
- [ ] A provider-scoped token bucket exists in front of the adapter.
- [ ] Rate limit (retryable) and quota exhaustion (not retryable) are distinct internal codes.
- [ ] `finish_reason` is inspected before the body is used.
- [ ] Context-window checks reserve output tokens and use a margin over the estimate.
- [ ] `usage` is persisted per call for cost attribution.
- [ ] Timeouts are classified by kind and their ambiguity is recorded.
- [ ] Streaming uses an idle timeout measured between chunks.

## Related

- [Output Validation and Structured Output](./02-output-validation-and-structured-output.md)
- [Tool-Calling Failures](./03-tool-calling-failures.md)
- [Retry Safety and Nondeterminism](../02-deep-dive/01-retry-safety-and-nondeterminism.md)
- [Chapter 44 Reference](../05-reference/README.md)
