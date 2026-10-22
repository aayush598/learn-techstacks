# Provider Contracts and Retrieval Failures

> Part XVI · Chapter 44 · Sections 44.17–44.20 · _Estimated reading time: 28 min_
> **Prerequisite:** [Agent Loop Failures and Recovery](./04-agent-loop-failures-and-recovery.md)

## In one sentence

Your API must speak **one stable error vocabulary** regardless of which provider is behind
it — and the retrieval pipeline underneath the model is a **separate distributed system**
whose failures deserve the same rigor as the model call.

## Why this matters in production

Two things break the illusion that "the AI feature" is one thing.

The first is **provider swap**. A model provider prices change, a region goes dark, a
feature you need is only on one vendor's API. When your error handling is written against
`err.code === "rate_limit_error"`, every one of those vendor strings is scattered through
your codebase, and swapping providers becomes a refactor of the whole feature.

The second is **retrieval**. In a RAG feature, the user's answer depends on an embedding
API, a vector store, an indexer, and a ranking step — none of which is the model. When
the answer is wrong, the first question is "did the model fail, or did the context fail?"
and the honest answer is usually: you cannot tell, because you never recorded which
documents were retrieved.

## 44.17 — Distinguishing provider errors from application errors

The distinction drives three decisions: **who gets paged**, **whether to retry**, and **what
the user sees**.

| Layer | Who owns it | User sees | Retry? | Pages? |
| ----- | ----------- | ---------- | ------ | ------ |
| Provider transport (429/5xx/timeouts) | Vendor | "We're having trouble, try again" | ✅ Yes | ✅ Yes, if sustained |
| Provider request validation (400) | **You** | Nothing — it is a bug | ❌ | ✅ Yes, immediately |
| Provider config (401/403/404) | **You** | Nothing — it is a config bug | ❌ | ✅ Yes, immediately |
| Model output (truncated, refused, invalid) | Mix | A specific message | ⚠️ Sometimes | ❌ |
| Your tool | **You** | A specific message | Tool-specific | ✅ If systemic |
| Your business logic | **You** | A specific message | ❌ | Depends |

The rule: **if the provider rejected your request because of what you sent, it is your
bug** — page someone, never retry it, and never show the user a raw provider message.

### The translation boundary

```ts
export type AppErrorCode =
  | "PROVIDER_UNAVAILABLE"        // 503 — vendor is down or overloaded
  | "PROVIDER_RATE_LIMITED"       // 429 — retry after the stated delay
  | "PROVIDER_QUOTA_EXCEEDED"     // 402 — account budget exhausted
  | "PROVIDER_TIMEOUT"            // 504 — ambiguous outcome
  | "PROVIDER_MISCONFIGURED"      // 500 — but it is a config bug: page
  | "PROVIDER_REQUEST_INVALID"    // 400 — your request is wrong: page
  | "OUTPUT_TRUNCATED"            // 502 — the model hit the output cap
  | "MODEL_REFUSED"               // 422 — content filter / refusal
  | "OUTPUT_INVALID"              // 502 — failed schema validation
  | "CONTEXT_WINDOW_EXCEEDED"     // 413 — the prompt is too big
  | "TOOL_FAILED"                 // 502 — your tool failed
  | "TOOL_TIMEOUT"                // 504 — your tool did not answer
  | "TOOL_FORBIDDEN"              // 403 — permission denied
  | "TOOL_ARGS_INVALID"           // 422 — the model produced bad arguments
  | "EMBEDDING_FAILED"            // 503 — the embedding provider failed
  | "RETRIEVAL_FAILED"            // 503 — the vector store failed
  | "AGENT_BUDGET_EXCEEDED"       // 429 — the run hit its step or token budget
  | "AGENT_LOOP_DETECTED";        // 422 — the model repeated itself
```

That list is your **contract**. It is provider-agnostic, versioned by your team, and the
only thing your feature code, your API layer, and your dashboards are allowed to branch on.

**Key data:** every provider error maps to exactly one `AppErrorCode` and one HTTP status.
The mapping lives in one table in one adapter. If a second provider is added, you extend
the table — you do not touch feature code.

## 44.18 — Retrieval and embedding failures

A RAG feature has a supply chain:

```text
documents ──▶ chunker ──▶ embedding API ──▶ vector store ──▶ retriever ──▶ prompt
                 │              │                │              │
              chunking      429 / 5xx        timeout        empty result
              error         quota           connection      stale index
```

Each stage has its own failure mode, and they need different responses.

| Stage | Failure | Signal | Response |
| ----- | ------- | ------ | -------- |
| Chunker | Malformed document | Parse error | Skip the document, record it |
| Embedding API | 429 / 503 / timeout | Provider error | Retry with backoff; **degrade to keyword search** |
| Embedding API | Model version changed | Index mismatch | Re-embed the corpus before serving |
| Vector store | Timeout / connection error | Client error | Retry, then serve without retrieval |
| Retriever | Zero results | Empty list | **Not an error** — answer from the model, say so |
| Retriever | Stale index | Index version mismatch | Rebuild or fall back to lexical search |
| Ranking | Garbage scores | NaN / out-of-range | Clamp and re-rank, log it |

### The zero-result case is not an error

An empty retrieval result means "I found nothing", not "the system failed". Returning a
502 for it means the user sees an error for a question your product simply cannot answer.
The correct behavior is to answer from the model's own knowledge, **and say that the
knowledge base had nothing on it**:

```ts
const chunks = await retriever.search(query, { topK: 8 });
const answer = await client.complete({
  messages: [
    { role: "system", content: chunks.length
        ? "Answer only from the CONTEXT below. If the context is insufficient, say so."
        : "You have no context for this question. Answer from general knowledge and " +
          "state that this is not from the customer's knowledge base." },
    { role: "user", content: query },
    ...(chunks.length ? [{ role: "user", content: formatContext(chunks) }] : []),
  ],
});
```

### Degradation, in order of preference

```text
full retrieval (hybrid search + rerank)
   └─ fails ──▶ vector search only
        └─ fails ──▶ keyword search only
             └─ fails ──▶ no context, model answers alone (say so)
```

**Key data:** the degradation ladder is a **product decision**, not just an engineering one.
"Answer without the knowledge base" can be right (general questions) and dangerous
(regulated content, support policy). Decide per feature which rungs are allowed, and make
the model *say* which rung answered.

### Index staleness

The trap nobody plans for: you upgrade the embedding model, and the vectors in your store
were produced by the old model. Queries are embedded with the new model and compared
against old vectors — the distances are meaningless, and retrieval quality collapses
without a single error.

```ts
export type IndexManifest = {
  corpusVersion: string;
  embeddingModel: string;      // including version
  dimension: number;
  builtAt: string;
  documentCount: number;
};

export function assertIndexUsable(manifest: IndexManifest, currentModel: string): void {
  if (manifest.embeddingModel !== currentModel) {
    throw new AppError("RETRIEVAL_FAILED", {
      reason: "embedding model mismatch: index was built with " + manifest.embeddingModel,
      currentModel, remedy: "re-embed the corpus",
    });
  }
}
```

**Key data:** store the **embedding model, its version, and the vector dimension** in the
index manifest and check them on every query (or at query time at least hourly). Dimension
mismatches are loud; *same dimension, different model* is silent and much worse.

## 44.19 — Duplicate side effects

This is the failure the whole chapter has been building toward: **a retry that repeats a
side effect**. A refund twice, an email twice, a row inserted twice, a webhook fired
twice.

The mechanism is always the same:

```text
call 1: tool runs ──▶ side effect happens ──▶ provider call times out (ambiguous)
call 2 (retry): tool runs again ──▶ side effect happens again
```

Three defenses, in order of strength:

1. **Idempotency key on the operation.** The tool derives a key from the *business
   operation* (not the HTTP request), stores the result, and returns the stored result on
   a repeat. This is the real fix.
2. **A durable effect ledger.** Every tool effect is recorded with its key before the
   effect is applied; a repeat is detected and the recorded result returned.
3. **Make the effect naturally idempotent.** `PUT /documents/{id}` is idempotent;
   `POST /documents` is not.

**Key data:** the idempotency key must be derived from the *business operation* —
`(runId, toolName, canonicalArgs)` or `(orderId, "refund", amount)` — and must be
**checked before** the effect, not after. The deep dive covers the ledger mechanics.

## 44.20 — Stable contracts across providers

### The adapter interface

```ts
export interface LlmProvider {
  readonly name: string;
  readonly models: ModelSpec[];
  complete(req: CompletionRequest, opts?: { signal?: AbortSignal }): Promise<CompletionResponse>;
  embed(req: EmbeddingRequest, opts?: { signal?: AbortSignal }): Promise<EmbeddingResponse>;
  /** Translate a provider-specific error into your stable contract. */
  normalizeError(err: unknown): AppError;
}
```

The interface is small on purpose. Everything provider-specific — parameter names, the
shape of `finish_reason`, the error body, the streaming protocol — stays **inside** the
adapter.

### Normalizing `finish_reason`

Different providers use different names for the same four outcomes. Normalize once:

| Your code | Provider A | Provider B | Provider C |
| --------- | ---------- | ---------- | ---------- |
| `stop` | `stop` | `end_turn` | `stop` |
| `length` | `length` | `max_tokens` | `length` |
| `tool_calls` | `tool_calls` | `tool_use` | `tool_calls` |
| `refused` | `content_filter` | `refusal` | `content_filter` |
| `stop` (legacy) | `function_call` | — | — |

```ts
export function normalizeFinishReason(raw: string): FinishReason {
  switch (raw) {
    case "stop": case "end_turn": case "function_call": return "stop";
    case "length": case "max_tokens": return "length";
    case "tool_calls": case "tool_use": return "tool_calls";
    case "content_filter": case "refusal": return "refused";
    default: return "unknown";
  }
}
```

> ⚠️ **Hazard.** An **unknown** `finish_reason` must not be treated as `stop`. If a
> provider adds a new reason, treating it as success means you ship half-formed output.
> Map unknown reasons to `unknown` and handle them conservatively — validate the output
> anyway, and log the raw value so you can add the mapping.

**Key data:** normalize `finish_reason`, error codes, token-usage field names, and the
tool-call shape. **Four** places: finish reason, error class, usage fields, tool calls.

### The capability contract

```ts
export type Capability =
  | "tools" | "json_schema" | "streaming" | "vision" | "parallel_tool_calls" | "seed";

export function capabilitiesOf(model: ModelSpec): Set<Capability> { /* ... */ }
```

Feature code asks for capabilities, never model names:

```ts
if (!capabilitiesOf(selected).has("json_schema")) {
  // fall back to JSON mode + schema validation on our side
}
```

**Key data:** the stable contract has three parts: a **stable error vocabulary**
(`AppErrorCode`), a **normalized response shape** (finish reason, usage, tool calls), and
a **capability descriptor**. A provider adapter that cannot supply all three is not a
drop-in replacement, and the capability descriptor is how you find out before production.

## Worked example — the provider migration

Acme's summary feature was built on one provider. When that provider raised prices by 4×,
the team added a second. The migration took three weeks instead of one, because the
feature code contained 37 references to provider-specific error strings and four places
that read `finish_reason` directly.

The rebuild put a single `LlmProvider` implementation behind an interface, moved all 37
error checks into one normalization table, and replaced every `finish_reason` comparison
with a normalized enum. The second provider's adapter was then written against the same
interface: one file, two days, zero changes to feature code.

The same rebuild surfaced a second problem. The new provider's embedding model produced
**1,536-dimension** vectors while the index held **1,024-dimension** vectors from the old
one. The retrieval code did not check the dimension, so queries returned nothing and the
feature degraded to "no context" answers. The dimension check and the index manifest
turned a silent quality collapse into a loud `RETRIEVAL_FAILED`.

## Key data

| Fact | Value |
| ---- | ----- |
| Your error contract | One `AppErrorCode` per failure mode, one HTTP status each |
| Provider bug vs your bug | A 400 on a well-formed request is **your** bug: page, don't retry |
| Normalized fields | `finish_reason`, error class, usage, tool calls — four places |
| `finish_reason` mapping | `stop`/`end_turn` → stop; `length`/`max_tokens` → length; `tool_calls`/`tool_use` → tool calls; `content_filter`/`refusal` → refused |
| Unknown `finish_reason` | Map to `unknown`; validate anyway; log the raw value |
| Retrieval degradation | hybrid → vector → keyword → no context (say so) |
| Empty retrieval | **Not** an error; answer without context and disclose it |
| Index manifest | corpus version, embedding model **+ version**, dimension, built-at, doc count |
| Embedding model change | Requires re-embedding; the old vectors are silently incompatible |
| Idempotency key | Derived from the business operation, checked before the effect |

## Real-world use case

A multi-tenant SaaS sells an AI assistant whose answers come from each customer's
documents. The team runs two providers: a flagship for complex questions and a cheaper
one for simple ones, with automatic fallback when the flagship is overloaded.

The fallback originally picked by list order, so when the flagship was down, the cheap
model answered — and the cheap model did not support the structured-output mode the
feature required. The fallback produced prose where the UI expected JSON, and the
frontend crashed on about 3% of requests during the fallback window. The capability
filter fixed it: the run declares what it needs (`tools`, `json_schema`, a minimum context
window), and the router only considers models that satisfy it.

The retrieval failure surfaced next. The team added a second embedding provider for cost,
and the index was built with the first one's model. Queries stopped matching documents,
and because the dimension check did not exist, nothing failed — the answers just got
worse. The index manifest and its guard turned that into an explicit `RETRIEVAL_FAILED`
with the remedy ("re-embed the corpus") instead of a slow slide in answer quality that
nobody could explain.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Feature code reads provider codes | Zero adapter work | Couples the feature to one vendor | Never |
| One adapter + stable codes | Portable, testable | One place to maintain the mapping | ✅ Always |
| Normalize `finish_reason` | Portable | New provider reasons need a mapping | ✅ Always |
| Capability descriptors | Correct fallbacks | Must be maintained per model | ✅ Always |
| Feature code names the model | Simple | No fallback safety | Fixed-model features only |
| Always retrieve, fail on error | Simple | One flaky dependency kills the feature | Non-critical features |
| Degrade to keyword search | Works without the vector store | Lower quality | ✅ When allowed by policy |
| Answer without context | Always available | May be wrong; must be disclosed | ✅ With disclosure |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Expose one `AppErrorCode` vocabulary to the whole app | Branch on provider error strings |
| Page on provider 400s — they are your bugs | Retry a 400 |
| Normalize `finish_reason`, errors, usage, and tool calls | Read provider fields in feature code |
| Map unknown `finish_reason` to `unknown` | Treat unknown as `stop` |
| Declare capabilities instead of naming models | Pick the fallback by list order |
| Treat empty retrieval as a normal outcome | Return 502 when nothing was retrieved |
| Disclose when the answer came without the corpus | Pass off a no-context answer as grounded |
| Store the embedding model and dimension in an index manifest | Re-embed silently on model change |
| Check the idempotency key before applying an effect | Apply the effect, then check |

## Common mistakes

- **Provider strings leaking into feature code.** The most expensive coupling in AI apps.
- **Retrying your own bug.** A 400 from the provider is usually your malformed request.
- **Unknown `finish_reason` treated as success.** New provider reasons ship your
  half-formed output.
- **Fallback by list order.** The fallback may not support the required format.
- **Empty retrieval treated as an error.** The user sees an error for an unanswerable
  question.
- **No disclosure on degraded answers.** Users trust a grounded answer more than an
  ungrounded one.
- **Silent re-embedding.** The same dimension with a different model breaks retrieval
  invisibly.
- **Idempotency checked after the effect.** Too late.

## Checklist

- [ ] One stable `AppErrorCode` vocabulary covers every failure mode.
- [ ] The provider → app-code → HTTP-status mapping lives in exactly one table.
- [ ] `finish_reason` is normalized, and unknown values map to `unknown`.
- [ ] Feature code declares required capabilities, never model names.
- [ ] Fallbacks are capability-filtered, and `content_filter` never falls back.
- [ ] Retrieval has an explicit degradation ladder.
- [ ] Empty retrieval returns a disclosed, non-error answer.
- [ ] The index manifest records the embedding model, version, and dimension.
- [ ] Idempotency keys are checked before effects are applied.
- [ ] Runs log the model version, tool schema hash, and retrieved document ids.

## Related

- [Agent Loop Failures and Recovery](./04-agent-loop-failures-and-recovery.md)
- [Provider and Quota Failures](./01-provider-and-quota-failures.md)
- [Duplicate Side Effects During Agent Retries](../02-deep-dive/02-duplicate-side-effects-during-agent-retries.md)
- [Chapter 44 Reference](../05-reference/README.md)
