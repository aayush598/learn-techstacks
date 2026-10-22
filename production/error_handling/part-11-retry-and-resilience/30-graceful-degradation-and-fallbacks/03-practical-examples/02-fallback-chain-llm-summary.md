# Fallback Chain for LLM Summary

> Part XI · Chapter 30 · Sections 30.3–30.11 · _Estimated reading time: 23 min_
> **Prerequisite:** [Fallback Chains](../02-deep-dive/01-fallback-chains.md)

## In one sentence

`AgentRun` generates a summary through a **four-step chain** — large model, small model, extractive
summary, static template — sharing one 8-second budget and returning provenance for every result.

## Why this matters in production

LLM calls are slow, expensive, rate-limited, and occasionally unavailable. A single-model summary
endpoint turns every provider incident into a failed product surface. A chain keeps the feature useful:
a smaller model is usually good enough, an extractive summary is always available, and a template
never fails. The hard part is not the models — it is the budget, the fallback quality, and telling the
user which one they got.

## The chain

| Step | Source | Model/technique | p99 | Budget | Quality |
| ---- | ------ | --------------- | --- | ------ | ------- |
| 1 | `large` | 70B model | 4.2s | 5.0s | High |
| 2 | `small` | 8B model | 1.1s | 2.0s | Medium |
| 3 | `extractive` | First sentences + headings | 15ms | 300ms | Low but factual |
| 4 | `template` | "Summary unavailable for this item." | 0ms | 0ms | None |

The user budget is **8s**, leaving 3s of the page's 11s deadline for rendering and other calls.

## Implementation

```ts
type SummarySource = "large" | "small" | "extractive" | "template";

interface Summary {
  text: string;
  source: SummarySource;
  degraded: boolean;
  asOf: number;
  tokens?: { input: number; output: number };
  model?: string;
}

const USER_BUDGET_MS = 8_000;
const SAFETY_MS = 150;

export async function summarize(
  doc: Document,
  opts: { deadline?: number; tenantId: string; quality?: "high" | "normal" },
): Promise<Summary> {
  const deadline = opts.deadline ?? Date.now() + USER_BUDGET_MS;
  const steps: Step<Summary>[] = [
    {
      name: "large",
      minUsefulMs: 1_200,
      needs: "llm-large",
      run: (signal) => callModel("large", doc, signal),
    },
    {
      name: "small",
      minUsefulMs: 600,
      needs: "llm-small",
      run: (signal) => callModel("small", doc, signal),
    },
    {
      name: "extractive",
      minUsefulMs: 50,
      run: async () => extractiveSummary(doc),
    },
    {
      name: "template",
      minUsefulMs: 0,
      run: async () => ({
        text: "A summary is not available for this item right now.",
        source: "template" as const,
        degraded: true,
        asOf: Date.now(),
      }),
    },
  ];

  // High-quality tenants skip the small model but still fall through.
  if (opts.quality === "high") {
    steps.splice(1, 1);
  }

  const result = await evaluateChain(steps, deadline, {
    breakers: llmBreakers,
    perStepCapMs: 5_000,
    safetyMs: SAFETY_MS,
  });

  metrics.increment("summary_source_total", { source: result.source });
  if (result.degraded) metrics.increment("summary_degraded_total", { source: result.source });

  return { ...result.value, degraded: result.source !== "large", asOf: result.value.asOf };
}
```

## Calling the model with a hard budget

```ts
async function callModel(
  size: "large" | "small",
  doc: Document,
  signal: AbortSignal,
): Promise<Summary> {
  const input = truncate(doc.text, size === "large" ? 12_000 : 6_000);
  const started = Date.now();

  try {
    const res = await llm.chat(
      {
        model: size === "large" ? "llm-70b" : "llm-8b",
        messages: [
          { role: "system", content: SYSTEM_PROMPT_V7 },
          { role: "user", content: `Summarize in 3 bullets:\n\n${input}` },
        ],
        max_tokens: 220,
        temperature: 0.2,
      },
      { signal, timeoutMs: 5_000 },
    );

    return {
      text: res.choices[0].message.content.trim(),
      source: size,
      degraded: size !== "large",
      asOf: Date.now(),
      tokens: res.usage,
      model: res.model,
    };
  } catch (err) {
    metrics.increment("llm_call_failed_total", { size, reason: classify(err) });
    throw err;
  } finally {
    metrics.observe("llm_latency_ms", Date.now() - started, { size });
  }
}
```

Notes:

- The model call receives the **remaining chain budget**, not a fresh 5s.
- `signal` aborts the HTTP request on timeout; the SDK must honor it.
- Prompt version (`V7`) is pinned so a prompt change does not silently alter fallback behavior.

## Extractive fallback

The extractive step is deterministic and cheap, so it is always eligible:

```ts
function extractiveSummary(doc: Document): Summary {
  const headings = doc.sections.slice(0, 3).map((s) => s.heading);
  const firstSentences = doc.sections
    .slice(0, 3)
    .map((s) => s.text.split(/(?<=[.!?])\s/)[0])
    .filter(Boolean);

  const lines = headings.map((h, i) => `- ${h}: ${firstSentences[i] ?? ""}`).join("\n");

  return {
    text: lines || doc.text.slice(0, 280),
    source: "extractive",
    degraded: true,
    asOf: Date.now(),
  };
}
```

Extractive output is factual by construction; it is lower quality, not lower truth. That is why it is
preferred over a hallucinated small-model summary when the small model is also unavailable.

## Caching summaries

Summaries are expensive and change only when the document changes:

```ts
const key = `summary:v7:${doc.id}:${doc.version}:${quality}`;
const cached = await cache.get<Summary>(key);
if (cached) {
  return { ...cached, degraded: true, source: cached.source }; // served from cache
}

const result = await summarize(doc, { tenantId, quality });
if (result.source !== "template") {
  await cache.set(key, result, { ttlSeconds: 86_400 });
}
return result;
```

Cache rules:

- **Do not cache** the template fallback.
- Include the **prompt version** in the key so old summaries are not served after a prompt change.
- Include the document version so edits invalidate.
- A cache hit is technically degraded (not generated now), but it is high quality; the UI can say
  "Saved summary" without alarming the user.

## Communication

```json
{
  "summary": "• Revenue grew 12%...",
  "summary_source": "small",
  "degraded": true,
  "degraded_reason": "primary_model_unavailable",
  "notice": "Generated with reduced quality while our main model recovers."
}
```

| Source | UI treatment |
| ------ | ------------ |
| `large` | Normal |
| `small` | Subtle "reduced quality" label |
| `extractive` | "Key points extracted from the document" |
| `template` | "Summary unavailable" |
| cache | "Saved summary" |

Never present `template` text as if a model wrote it.

## Failure and observability

```text
summary_source_total{source}
summary_degraded_total{source}
llm_call_failed_total{size,reason}
llm_latency_ms{size}
summary_chain_exhausted_total
```

Alerts:

- `summary_chain_exhausted_total > 0` for 5m → page (the feature is fully down).
- `summary_source_total{source="template"} > 5%` for 10m → investigate provider.
- `llm_latency_ms{size="large"}` p99 > 5s for 10m → step 1 will always time out.

## Testing

```ts
it("falls back to the small model when the large model times out", async () => {
  llm.fail("large", new TimeoutError());
  const result = await summarize(doc, { tenantId: "t1" });
  expect(result.source).toBe("small");
  expect(result.degraded).toBe(true);
});

it("uses extractive when both models fail", async () => {
  llm.fail("large", new Error("down"));
  llm.fail("small", new Error("down"));
  const result = await summarize(doc, { tenantId: "t1" });
  expect(result.source).toBe("extractive");
  expect(result.text.length).toBeGreaterThan(0);
});

it("respects the 8s budget", async () => {
  llm.delay("large", 5_000).delay("small", 2_000);
  const started = Date.now();
  await summarize(doc, { tenantId: "t1" });
  expect(Date.now() - started).toBeLessThan(8_200);
});
```

## Cost profile

| Source | Relative cost | Relative latency |
| ------ | ------------- | ---------------- |
| large | 1.0× | 1.0× |
| small | 0.08× | 0.25× |
| extractive | ~0 | ~0 |
| cache hit | ~0 | ~0.02× |

Routing routine traffic to the small model first would cut cost, but Acme keeps the large model first
for quality and uses the chain only as a failure path. The cost of the chain is dominated by step 1;
steps 2–4 are single-digit percentages.

## Key data / numbers

- User budget **8s**; safety **150ms**.
- Step 1: **5s** cap, p99 **4.2s**.
- Step 2: **2s** cap, p99 **1.1s**.
- Step 3: **300ms** cap, p99 **15ms**.
- Step 4: **0ms**.
- Cache TTL **24h**, keyed by `prompt version + doc version`.
- Template share above **5%** for 10m → alert.

## Real-world use case — Acme SaaS

Acme's `AgentRun` summaries were failing ~9% of the time on a single 30s model call, and each failure
also held a worker for the full timeout. The chain reduced hard failures to 0.3% (mostly documents
where even extraction failed), cut p99 to 6.1s, and saved cost during incidents because the small model
handled most degraded traffic. The `summary_source_total` metric became the earliest signal of provider
degradation — it moved minutes before the provider's own status page updated.

## Trade-offs

| Choice | Benefit | Cost |
| ------ | ------- | ---- |
| Large-first | Best quality | Slow, expensive |
| Small-first | Cheap, fast | Lower quality always |
| Extractive before template | Factual | Less readable |
| Cache in front | Cost/latency | Staleness, invalidation |
| High-quality skips small | Simpler chain | Fewer fallback options |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Share one deadline across steps | Give each model its own 30s |
| Abort the HTTP request on timeout | Let the call continue after fallback |
| Label the source and quality | Present template text as AI output |
| Cache only real summaries | Cache the template |
| Key cache by prompt + doc version | Serve summaries from an old prompt |
| Alert on template share | Wait for user complaints |

## Common mistakes

- **No abort signal**, so timed-out calls keep consuming tokens.
- **Caching degraded output**, making a temporary failure permanent.
- **Extractive step that throws** on malformed documents.
- **No prompt version in the cache key**, so prompt changes do not take effect.
- **Template step returning an empty string**, which the UI renders as blank.

## Checklist

- [ ] Chain order and budgets are documented.
- [ ] All steps share one deadline.
- [ ] Model calls honor the abort signal.
- [ ] Extractive fallback is deterministic and total.
- [ ] Template fallback always succeeds and is labelled.
- [ ] Cache excludes template and is keyed by prompt/doc version.
- [ ] Source and degraded flag are returned to the client.
- [ ] Tests cover each failing step and the 8s budget.

## Related

- [Fallback Chains](../02-deep-dive/01-fallback-chains.md)
- [Fallback Failure, Silent Inaccuracy, and Communication](../01-concepts/04-fallback-failure-silent-inaccuracy-and-communication.md)
- [Degraded Mode for Acme](./01-degraded-mode-for-acme.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../29-timeouts-circuit-breakers-and-bulkheads/README.md)
