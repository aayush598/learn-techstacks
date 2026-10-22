# Fallback Model Selection

> Part XVI · Chapter 44 · Sections 44.3, 44.15, 44.17 · _Estimated reading time: 24 min_
> **Prerequisite:** [Agent Loop Failures and Recovery](../01-concepts/04-agent-loop-failures-and-recovery.md)

## In one sentence

A fallback is a **capability decision**, not a "next model down" decision: filter by what
the run actually needs — tools, structured output, context window, region — and only then
by cost and health.

## Why this matters in production

Model fallback is usually a list: `["acme-large", "acme-medium", "acme-small"]`. That list
is wrong the moment one of the models lacks a feature the run needs. The flagship supports
JSON-schema mode and the medium model does not; the run falls back to the medium model,
the response comes back as prose, and your parser throws — a *fallback-induced* failure
that looks like a model outage but is a routing bug.

The other half is **when** to fall back. Falling back on a content filter bypasses your
own policy. Falling back on a malformed request fixes nothing. Falling back on a truncated
response to a *smaller* model makes truncation worse.

## The model registry

```ts
export type ModelSpec = {
  id: string;                  // "acme-large-2026-03"
  provider: string;
  contextWindow: number;       // tokens
  maxOutputTokens: number;
  supportsTools: boolean;
  supportsJsonSchema: boolean;
  supportsStreaming: boolean;
  supportsVision: boolean;
  costPerMTokIn: number;
  costPerMTokOut: number;
  regions: string[];
  priority: number;            // lower = preferred
};

export const REGISTRY: ModelSpec[] = [
  { id: "acme-large-2026-03", provider: "alpha", contextWindow: 200_000, maxOutputTokens: 16_384,
    supportsTools: true, supportsJsonSchema: true, supportsStreaming: true, supportsVision: true,
    costPerMTokIn: 3.0, costPerMTokOut: 15.0, regions: ["us-east-1"], priority: 0 },
  { id: "acme-medium-2026-02", provider: "alpha", contextWindow: 128_000, maxOutputTokens: 8_192,
    supportsTools: true, supportsJsonSchema: true, supportsStreaming: true, supportsVision: false,
    costPerMTokIn: 0.8, costPerMTokOut: 4.0, regions: ["us-east-1", "eu-west-1"], priority: 1 },
  { id: "other-mini-2026-01", provider: "beta", contextWindow: 128_000, maxOutputTokens: 4_096,
    supportsTools: true, supportsJsonSchema: false, supportsStreaming: true, supportsVision: false,
    costPerMTokIn: 0.15, costPerMTokOut: 0.6, regions: ["us-east-1"], priority: 2 },
];
```

**Key data:** pin the **version** in the id (`acme-large-2026-03`). An unpinned alias lets
a provider-side change silently alter behaviour with no fingerprint to explain it.

## Declaring what the run needs

```ts
export type RunRequirements = {
  tools: boolean; jsonSchema: boolean; vision: boolean;
  minContextTokens: number;   // input + reserved output
  region: string;
  maxCostPerMTok: number;     // optional ceiling
};

export function eligibleModels(req: RunRequirements, registry: ModelSpec[]): ModelSpec[] {
  return registry.filter((m) =>
    (!req.tools || m.supportsTools) &&
    (!req.jsonSchema || m.supportsJsonSchema) &&
    (!req.vision || m.supportsVision) &&
    m.contextWindow >= req.minContextTokens &&
    m.regions.includes(req.region) &&
    m.costPerMTokIn <= (req.maxCostPerMTok ?? Infinity));
}
```

**Key data:** `minContextTokens` must include the **output reservation** (44.3): a run
needing a 4,000-token answer cannot use a 4,096-token window even if the input is tiny.

## The routing decision

```text
  requirements ──▶ filter by capability ──▶ drop unhealthy ──▶ sort by priority, then cost
```

```ts
export function buildChain(req: RunRequirements, registry: ModelSpec[],
                           health: HealthView): ModelSpec[] {
  return eligibleModels(req, registry)
    .filter((m) => health.isHealthy(m.id))
    .sort((a, b) => a.priority - b.priority
                 || (a.costPerMTokIn + a.costPerMTokOut) - (b.costPerMTokIn + b.costPerMTokOut));
}
```

Health matters as much as capability: a provider returning 529 is *not* a good fallback
target, and a circuit breaker is how you know.

## Which failures trigger a fallback

```ts
export type ProviderOutcome =
  | { kind: "ok" }
  | { kind: "overloaded"; status: number }     // 503 / 529
  | { kind: "rate_limited"; retryAfterMs: number }
  | { kind: "quota_exhausted" } | { kind: "timeout" }
  | { kind: "misconfigured"; status: number }   // 401 / 403 / 404
  | { kind: "bad_request"; status: number }     // 400 / 422 — YOUR bug
  | { kind: "truncated" } | { kind: "refused" };

export function shouldFallBack(outcome: ProviderOutcome, attempt: number): boolean {
  switch (outcome.kind) {
    case "overloaded":      return attempt === 0;   // one retry, then switch
    case "rate_limited":    return true;           // another quota pool may exist
    case "quota_exhausted": return true;
    case "timeout":         return attempt === 0;
    case "misconfigured":   return true;           // this key/model is wrong
    case "bad_request":     return false;          // another model will not help
    case "truncated":       return false;          // needs MORE output tokens
    case "refused":         return false;          // policy — do not route around it
    case "ok":              return false;
  }
}
```

| Outcome | Fall back? | Reason |
| ------- | ---------- | ------ |
| `503` / `529` overloaded | ✅ After one retry | Another model may have capacity |
| `429` rate limited | ✅ | A different provider has a different quota pool |
| `429` quota exhausted | ✅ | Your budget for that provider is gone |
| `401` / `403` / `404` | ✅ | The key or model id is wrong; another provider may work |
| Timeout | ✅ After one retry | The provider may be degraded |
| `400` / `422` | ❌ | Your request is malformed; it fails everywhere |
| `finish_reason: length` | ❌ | Needs a **higher** `maxOutputTokens`, not a different brain |
| `content_filter` / `refusal` | ❌ | Routing around a refusal bypasses your policy |
| Invalid output after a repair turn | ⚠️ Only if the fallback shares the format | Otherwise you trade one invalid output for another |

> ⚠️ **Hazard.** `truncated` and `refused` are the two most commonly mishandled. A
> truncated answer needs a model with a **larger `maxOutputTokens`** — falling back to a
> smaller model guarantees a shorter, more truncated answer. A refusal must never be
> routed to a provider with weaker safety behaviour.

## The fallback loop

```ts
export async function completeWithFallback(
  provider: ProviderAdapter, chain: ModelSpec[], req: CompletionRequest,
): Promise<CompletionResponse> {
  let attempt = 0;
  const tried: string[] = [];
  for (const model of chain) {
    tried.push(model.id);
    try {
      const res = await provider.complete(model, req);
      if (res.finishReason === "length") {
        throw new AppError("OUTPUT_TRUNCATED", { model: model.id, maxOutput: model.maxOutputTokens });
      }
      return { ...res, model: model.id };
    } catch (err) {
      const outcome = toOutcome(err);
      if (!shouldFallBack(outcome, attempt)) throw toAppError(outcome, { model: model.id, tried });
      attempt += 1;
      metrics.increment("llm.fallback.attempt", { model: model.id, reason: outcome.kind });
    }
  }
  throw new AppError("PROVIDER_UNAVAILABLE", { tried });
}
```

**Key data:** the chain is walked **at most once per model**, with a total attempt budget
of **3–4**. Log every fallback attempt with its reason — "the fallback served 40% of
traffic" is invisible without it.

## Fallback and context limits (44.3)

The fallback must satisfy the **same** context requirement as the primary:

```ts
export function assertContextFits(model: ModelSpec, estimatedInputTokens: number): void {
  const reserve = Math.ceil(model.maxOutputTokens * 1.2);   // room for the answer
  if (estimatedInputTokens + reserve > model.contextWindow) {
    throw new AppError("CONTEXT_WINDOW_EXCEEDED", {
      model: model.id, estimatedTokens: estimatedInputTokens,
      contextWindow: model.contextWindow, required: estimatedInputTokens + reserve,
    });
  }
}
```

**Key data:** budget **~20% over the token estimate** (~4 characters per token, 1 token ≈
0.75 words). The authoritative count arrives in `usage` as `prompt_tokens`,
`completion_tokens`, and `total_tokens` — record it on every call, including fallbacks.

## One contract, many providers (44.17)

The fallback only works because both providers are wrapped in the same adapter:

```ts
export interface ProviderAdapter {
  readonly name: string;
  models(): ModelSpec[];
  complete(model: ModelSpec, req: CompletionRequest, opts?: { signal?: AbortSignal }):
    Promise<CompletionResponse>;
  normalizeError(err: unknown): ProviderOutcome;      // one place per provider
}
```

Because `normalizeError` returns the **same `ProviderOutcome` union** for every provider,
the routing logic above is provider-agnostic. A third provider is one adapter plus one
registry entry — no change to `shouldFallBack`, `buildChain`, or feature code.

**Key data:** the normalized shape has four parts: the **finish reason**, the **usage
counters**, the **tool-call array**, and the **error class**. Everything else is provider
detail.

## Worked example — the summarization feature

Acme's "summarize this project" feature used a single flagship model. When that provider
had a bad afternoon, 9% of requests failed and the feature was down.

The rebuild added a registry and a chain. The requirements filter is what made it
correct: the feature requires JSON schema, so `other-mini` — the cheapest model, and the
one with spare capacity — is **excluded** because it does not support schema mode. The
chain is large → medium, and the feature degrades to a slightly worse answer rather than
to a crash.

One more rule earned its keep: `finish_reason: length` does **not** trigger a fallback.
The feature retries once with a doubled `maxOutputTokens` on the same model, because a
shorter model would have produced a shorter, still-truncated answer.

Measured result: the failure rate during the provider's bad afternoon dropped from 9% to
0.3%. The fallback-attempt metric showed 41% of traffic on the medium model that week,
which is how the team learned the primary was degraded long before the invoice did.

## Key data

| Fact | Value |
| ---- | ----- |
| Registry entries | Pin the version: `acme-large-2026-03` |
| Requirements | tools, JSON schema, vision, min context, region, cost ceiling |
| Context requirement | Input estimate + `maxOutputTokens` + ~20% margin |
| Fallback triggers | 503/529, 429 (rate or quota), 401/403/404, timeout (once) |
| Never triggers | 400/422, `length`, `content_filter`, `refusal` |
| Chain budget | 3–4 attempts total across the whole chain |
| Pricing order | Filter by capability → drop unhealthy → priority → cost |
| Context windows | 8k / 128k / 200k tokens; max output 4,096 / 8,192 / 16,384 |
| Usage fields | `prompt_tokens`, `completion_tokens`, `total_tokens` |
| Token estimate | ~4 characters per token; 1 token ≈ 0.75 words |
| Metrics | `llm.fallback.attempt{model,reason}`, `llm.model.used` |

## Real-world use case

A multi-tenant SaaS runs an AI assistant on two providers so neither outage can take the
feature down. The team kept a hard-coded model list until a support engineer noticed the
cheap model serving 22% of traffic during a routine fallback and returning prose where
the UI expected structured data.

The rebuild introduced a registry with capability flags and a requirements filter. The
run declares `tools: true, jsonSchema: true, minContextTokens: 32_000`; the router
filters to the models that satisfy all three, drops any model whose circuit breaker is
open, then orders the remainder by cost. The cheap model — which lacks JSON schema — is
now **never** selected for that feature. The team also added a per-feature rule that
`content_filter` never triggers a fallback, because a refusal is a policy decision.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Hard-coded fallback list | Simple | Ignores capability, breaks formats | Never |
| Capability-filtered chain | Correct outputs | More configuration | ✅ Always |
| Filter + health + cost | Resilient and cheap | Needs a registry and metrics | ✅ Production |
| Same provider only | One contract, one bill | An outage kills the feature | Low-criticality features |
| Multi-provider | Real redundancy | Two adapters to maintain | ✅ Important features |
| Fall back on truncation | Simple | Gives a shorter answer | ❌ Raise `maxOutputTokens` |
| Fall back on refusal | "Sneaks past" safety | Bypasses your own policy | ❌ Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Declare what the run needs and filter by it | Pick the fallback from a list |
| Pin model versions in the registry | Track aliases |
| Include the output reservation in the context requirement | Check the input size only |
| Drop models whose circuit breaker is open | Fall back into a degraded provider |
| Log every fallback attempt with its reason | Leave fallbacks invisible |
| Retry truncation with a higher `maxOutputTokens` | Fall back to a smaller model |
| Never fall back on `content_filter` | Route around a refusal |
| Keep one normalized response shape for all providers | Branch on provider fields |

## Common mistakes

- **Fallback by list order.** The fallback does not support the required format.
- **Excluding the output reservation.** The fallback is chosen, then the provider rejects
  the request for exceeding its context window.
- **Falling back on truncation.** You get a shorter, still-truncated answer.
- **Falling back on a refusal.** You bypassed your own policy.
- **No fallback metrics.** The degradation is invisible until the invoice.
- **Unpinned model ids.** A provider update changes behaviour with no fingerprint.
- **No capability filter.** The most common cause of a fallback-induced outage.

## Checklist

- [ ] A registry records capabilities, cost, regions, and pinned versions.
- [ ] Each run declares its requirements before a model is chosen.
- [ ] The context requirement includes the output reservation plus a margin.
- [ ] Unhealthy models are removed by a circuit breaker before ordering.
- [ ] The chain is walked once per model, with a total budget of 3–4 attempts.
- [ ] `400`, `length`, and `content_filter` never trigger a fallback.
- [ ] Truncation retries with a higher `maxOutputTokens` on the same model.
- [ ] Every provider normalizes to the same four shapes.
- [ ] Fallback attempts and per-model usage are logged as metrics.
- [ ] `usage` is recorded for fallback calls too.

## Related

- [Agent Loop Failures and Recovery](../01-concepts/04-agent-loop-failures-and-recovery.md)
- [Provider Contracts and Retrieval Failures](../01-concepts/05-provider-contracts-and-retrieval-failures.md)
- [Chapter 44 Reference](../05-reference/README.md)
