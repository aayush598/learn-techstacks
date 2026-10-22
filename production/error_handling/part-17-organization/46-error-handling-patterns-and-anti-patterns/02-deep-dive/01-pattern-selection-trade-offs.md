# Pattern Selection Trade-Offs

> Part XVII · Chapter 46 · Sections 46.1–46.12 (selection) · _Estimated reading time: 16 min_
> **Prerequisite:** [Structural Patterns](../01-concepts/01-structural-patterns.md), [Resilience and Control-Flow Patterns](../01-concepts/03-resilience-and-control-flow-patterns.md)

## In one sentence

Most error-handling design arguments are actually *selection* arguments between two legitimate
patterns — so this file gives explicit decision criteria for the four competitions that come up
in every design review: result vs exception, global vs local handling, retry vs compensation,
and breaker vs fallback vs "do nothing yet."

## Why this matters in production

Teams resolve these competitions by seniority or fashion, then re-litigate them a year later
when the choice hurts. Written criteria do two things: they make the choice reviewable ("which
row of the table applied?"), and they make the *reversal* reviewable ("new data crossed the
threshold — here is the data"). Without criteria, each new service re-decides independently and
your system grows five incompatible retry philosophies.

## Competition 1 — Result type (46.3) vs exceptions + boundary (46.26)

| Criterion | Choose **result** | Choose **exceptions** |
| --------- | ----------------- | --------------------- |
| Failure frequency | Expected and common (> ~1% of calls) | Exceptional (< ~1%, truly surprising) |
| Caller obligations | Compiler must force handling | Forgetting is rare and loud in tests |
| Hot path | Parse/validate loops, per-row work | Business operations with boundaries |
| Language culture | Rust/Go habit; TS teams wanting exhaustiveness | Java/C#/Python/JS default ecosystems |
| Composability | Pipelines of partial successes (`andThen`) | Simple linear happy paths |

**Decision rule:** default to exceptions caught at owned boundaries (46.26); switch a specific
function to `Result` when its failure is *frequent and expected* or when callers routinely
ignore it. Never mix within one module — pick per layer.

## Competition 2 — Global handler (46.1) vs local handling

These are complements, not rivals — the real choice is *how much* is handled locally.

| Handle locally when… | Let the global handler when… |
| -------------------- | ---------------------------- |
| The fallback is feature-specific (placeholder UI, degraded value) | The fallback is the generic contract (500 envelope, DLQ, exit code) |
| You can translate to a domain outcome cleanly | The error is unexpected or unclassified |
| Propagation would cross a trust/tenant boundary | The error type is unknown to this layer |
| Partial success semantics exist (batch, saga step) | — (there is no meaningful local decision left) |

**Decision rule:** local catch must always *decide something* (translate, degrade, compensate,
rethrow-with-context). A catch that only logs belongs to nobody — delete it and let the global
handler own the exit.

## Competition 3 — Retry (46.6) vs compensation (46.10)

| Criterion | Choose **retry** | Choose **compensation** |
| --------- | ---------------- | ----------------------- |
| Failure semantics | Transient; same attempt will likely succeed | Step completed; later step failed |
| State | No committed side effects, or side effects are idempotent | Committed steps across stores |
| Time scale | Milliseconds–seconds | Seconds–hours (workflow scale) |
| Idempotency | Required (or keyed) for anything with side effects | Each compensation must itself be safe |
| Data model | Single resource call | Saga / multi-step workflow |

**Decision rule:** retry *within* a step; compensate *across* steps. A step that is itself
multi-store may need both: internal retries, then compensation if it returns a terminal
failure. Retrying across a committed side effect without a key is anti-pattern 46.24, not
persistence.

## Competition 4 — Breaker (46.7) vs fallback (46.8) vs neither (46.26)

| Symptom you have measured | Add |
| ------------------------- | --- |
| Transient failures, no cascade risk | Retry policy only (46.6) |
| Dependency outage causes *your* resource exhaustion (pool/thread pileup) | Breaker (46.7) |
| Feature is optional and has an honest degraded value | Fallback (46.8) |
| Both pileup and optional feature | Breaker **then** fallback — breaker decides fast, fallback defines the substitute |
| Nothing measured yet | Nothing (46.26) |

**Decision rule:** mechanisms are bought with numbers, not vibes. Before adding any of the
three, write the incident or metric that justifies it. A breaker around a dependency with no
recorded outage is speculative inventory (feeds 46.25); a fallback without a defined degraded
value is a lie the UI will tell.

## Selection flowchart (the whole chapter in six questions)

```text
1. Is the failure expected & frequent in this function? ── yes ─▶ Result type (46.3)
2. Is the operation non-idempotent and the failure ambiguous? ── yes ─▶ NO retry;
        surface AMBIGUOUS_OUTCOME + reconcile (46.24)
3. Is the failure classified transient & safe to repeat? ── yes ─▶ named retry (46.6)
4. Is this a later step of a multi-step workflow? ── yes ─▶ compensate prior steps (46.10)
5. Does the feature have an honest degraded value? ── yes ─▶ boundary + fallback (46.9/46.8)
6. Otherwise ──▶ typed error, throw, boundary owns the exit (46.26 + 46.1)
```

## Key data

- **Thresholds used in the tables (recommendations, tune to your data):** result-type switch
  around ~1% expected failure rate; breaker justification requires ≥ 1 recorded incident of
  resource pileup or p99 latency collapse during a dependency event; fallback requires a
  written degraded value (including "empty list" — written down).
- **Composition order that avoids amplification:** `boundary → breaker → retry → adapter →
  vendor`. Retry inside breaker (fast-fail when open); translation at the innermost layer;
  serialization only at the boundary.
- **Acme's selection audit:** of 23 resilience decisions reviewed, 11 were "simplest pattern +
  boundary," 6 retry, 3 breaker, 2 fallback, 1 compensation saga — i.e. the majority of a real
  SaaS deliberately sits at the simple end of the catalog.

## Real-world use case — Acme SaaS

Design review for the new `AgentRun` tool-calling loop, applying the flowchart: (1) provider
rate limits are expected at ~2% of calls during business peaks → the *classification* path
uses retry, not Result, because the call crosses a network boundary where exceptions are the
ecosystem norm; (2) tool calls that send email are non-idempotent → email tools get idempotency
keys supplied by the agent harness, otherwise the loop surfaces `AGENT_TOOL_AMBIGUOUS` instead
of retrying (step 2 of the chart); (3) `LLM_RATE_LIMITED` is transient → named
`llmProvider` policy, 2 attempts; (4) multi-step agent runs record per-step results and do not
replay completed side-effecting steps (compensations for the two such tools only);
(5) the "summarize" nicety has a cached fallback; (6) everything else is a typed throw caught
by the job boundary. The review took 40 minutes and produced a table the on-call wiki now
links — subsequent designs cite rows instead of re-arguing.

## Trade-offs summary

| Competition | Cheap default | Expensive upgrade | Reverse when |
| ----------- | ------------- | ----------------- | ------------ |
| Result vs exception | Exceptions + boundary | Result at hot/expected sites | Failure frequency rises past ~1% and callers ignore it |
| Global vs local | Global + a few boundaries | More local decisions | Fallback needs become feature-specific |
| Retry vs compensate | Retry within steps | Saga + compensations | Committed cross-store steps appear |
| Breaker/fallback vs none | None | Add one, measured | Pileup or degradation data appears |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Record which table row justified each mechanism | Adopt patterns because another repo has them |
| Compose in the canonical order (boundary → breaker → retry → adapter) | Nest retry inside adapter and caller |
| Revisit selections when data changes | Treat the first selection as permanent architecture |
| Default to 46.26 until outvoted by evidence | Default to the most sophisticated pattern |

## Common mistakes

- **Result as a compromise.** "We couldn't decide, so we return Result AND throw sometimes" —
  the worst of both. Decide per layer, write it down.
- **Fallback without breaker under outage load.** The fallback itself gets hammered by the same
  clients that would have hammered the provider; add the breaker or bulkhead first if pileup
  is the measured risk.
- **Compensation for single-store flows.** A Postgres rollback is not a saga; adding
  compensating actions inside one transaction boundary is pure overhead (46.25 territory).

## Checklist

- [ ] A written layer convention exists for result vs exception.
- [ ] Every retry/compensation follows the step-vs-workflow split.
- [ ] Every mechanism traces to a table row or incident number.
- [ ] Composition order in code matches boundary → breaker → retry → adapter.

## Related

- [Anti-Pattern Compounding and Remediation](./02-anti-pattern-compounding-and-remediation.md)
- [Acme Patterns Wired In](../03-practical-examples/01-acme-patterns-wired-in.md)
- [Choosing Between Competing Approaches](../../../part-22-design-decisions/56-choosing-between-competing-approaches/README.md)
