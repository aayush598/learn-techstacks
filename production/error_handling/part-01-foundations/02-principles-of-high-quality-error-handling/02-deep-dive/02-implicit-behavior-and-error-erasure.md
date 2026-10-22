# Implicit Behavior and Error Erasure — Mechanics and Edge Cases

> Part I · Chapter 2 · Sections 2.1, 2.4, 2.12–2.17 · _Estimated reading time: 22 min_

## In one sentence

Errors are erased not by one dramatic `catch` but by a **sequence of small, reasonable-looking
decisions** — implicit contracts, over-eager abstraction, cause-dropping wraps, and ceremonial
rethrows — and understanding the mechanics lets you stop the sequence early.

## Why this matters in production

"Error erasure" is the mechanism behind silent corruption: payments not charged, exports not
written, webhooks lost. It is subtle because every individual step looks defensible. This deep dive
walks the exact chain by which a precise root cause becomes an untraceable "something went wrong,"
and it catalogues the edge cases where the obvious fix is actually wrong.

## Core concept — the erasure pipeline

An error can be degraded at five stages. Each stage is a principle violation from Chapter 2.

```text
  ROOT CAUSE
  ECONNRESET / SQLSTATE 23505 / TypeError: x is undefined
      │
      │  (1) IMPLICIT CONTRACT     — return null, false, or undefined
      ▼
  AMBIGUOUS SIGNAL
      │
      │  (2) OVER-ABSTRACTION      — throw new Error("operation failed")
      ▼
  CONTEXT-FREE ERROR
      │
      │  (3) CAUSE DROPPED         — wrap without cause / %w / from exc
      ▼
  ORPHAN ERROR
      │
      │  (4) SWALLOW               — catch { log.debug() } / catch {}
      ▼
  NO SIGNAL
      │
      │  (5) FAILURE → SUCCESS     — catch { return ok } / res.status(200)
      ▼
  CORRUPT STATE
```

Any single stage that you break stops the chain. The cheapest place to intervene is stage 1.

## How it works (mechanics)

### Stage 1 — implicit contracts

A function that returns `null` for "absent," "failed," and "empty" forces every caller to guess.
The *caller's* guess becomes a de-facto policy that no one reviewed.

```python
# Implicit: three meanings, zero information.
def find_user(email) -> dict | None: ...

# Explicit: caller cannot guess wrong.
def find_user(email) -> Result[User, UserLookupError]: ...
```

### Stage 2 — over-abstraction

Abstraction is good for the *public contract* and bad for the *evidence*. Collapsing every failure
into one generic type makes the error unclassifiable — which then breaks retry, alerting, and
support (Chapters 8, 16).

### Stage 3 — cause dropped

The wrap is meant to add context. Done wrong, it *replaces* the cause.

```ts
// ❌ Cause replaced.
try { await call(); } catch (e) { throw new Error("call failed"); }
// ✅ Cause preserved (ES2022).
try { await call(); } catch (e) { throw new AppError("call failed", { cause: e }); }
```

### Stage 4 — swallow

The `catch` "handles" the error by doing nothing observable. The distinction between *handling* and
*swallowing* is whether any decision or record results.

```text
  catch block does at least one of: handle | translate | rethrow | record+terminate
  → not swallowed
  catch block does none:
  → swallowed (bug)
```

### Stage 5 — failure to success

The most damaging stage: the caller is *misinformed*, so it acts on false premises. This is a
correctness violation, not a style issue.

## Edge cases and counter-intuitive cases

| Case | Looks like | Reality |
| ---- | ---------- | ------- |
| Catching to **add a metric** then rethrow | Redundant | Justified — it records and propagates |
| Catching to **convert** `23505` → `ConflictError` | Redundant? | Justified — translation at a boundary |
| A `catch` that logs at `debug` and rethrows | Fine? | Log level may hide it from alerting; prefer `warn`/`error` on unexpected |
| `catch { return null }` in an **optional** lookup | Failure→success? | Only OK if `null` is a *documented* outcome, not a masquerade |
| Retry inside a wrap that also logs | Redundant? | Retry belongs to the adapter; logging to the caller — split responsibility |
| `finally` that throws | Cleanup failure | Can mask the primary error; preserve primary (Chapter 14) |

> The "optional lookup returns `null`" case is the subtle one: returning `null` is legitimate when
> *absence is a real, documented outcome*. It becomes a violation the moment `null` also means
> "the lookup failed."

## Worked example — reversing an erasure chain

**AgentRun** calls an LLM, then a tool. A bug reports "agent failed" with no detail.

```ts
// ❌ The whole erasure chain in 12 lines.
async function run(prompt: string) {
  let plan;
  try { plan = await llm.plan(prompt); }          // (3) cause dropped if it threw
  catch { return { ok: false }; }                 // (5) failure → success
  try { return await tool.call(plan.tool, plan.args); }
  catch { return null; }                          // (1)+(4) ambiguous + swallowed
}
```

```ts
// ✅ Each stage fixed: explicit, translated, cause preserved, no fake success.
async function run(prompt: string): Promise<Result<AgentOutput, AgentError>> {
  let plan: Plan;
  try {
    plan = await llm.plan(prompt);
  } catch (err) {
    return Err(new AgentProviderError({ phase: "plan", cause: err })); // cause kept
  }
  try {
    const out = await tool.call(plan.tool, plan.args);
    return Ok(out);
  } catch (err) {
    return Err(new AgentToolError({ tool: plan.tool, cause: err }));    // classified, not swallowed
  }
}
```

The result is classifiable (`AgentProviderError` vs `AgentToolError`), retryable info is preserved,
and no caller receives a false success.

## Key data / numbers

| Item | Value | Why |
| ---- | ----- | --- |
| Node `cause` support | `Error(msg, { cause })` since Node 16.9 | Native cause preservation |
| Go wrapping verb | `%w` | Enables `errors.Is` / `errors.As` |
| Python explicit cause | `raise ... from exc` | Sets `__cause__` |
| Unique violation | SQLSTATE `23505` → `409` | A translatable, preserved signal |
| Serialization failure | SQLSTATE `40001` → retryable | Must survive translation |
| LLM common limits | `429` with `Retry-After`; context-window errors | Classify provider vs tool vs app |

## Real-world use case — Acme SaaS

Acme's `AgentRun` feature returned `{ ok: false }` on any failure. Support could not distinguish
"LLM provider rate-limited" (`429`, retryable) from "tool arguments were invalid" (permanent,
user-fixable) from "our own bug." After refactoring the erasure chain — explicit `Result`, translated
provider/tool/app errors, preserved causes — the team could route: provider errors retried with
backoff, tool errors surfaced to the user as actionable messages, app errors paged the on-call. The
same failures now cost minutes instead of hours because the *signal* survived.

## Trade-offs

| Intervention point | Effort | Leverage | Prefer when |
| ------------------ | ------ | -------- | ----------- |
| Stage 1: explicit contracts | Medium | Highest | Always, for new code |
| Stage 3: preserve cause | Low | High | Every wrap |
| Stage 4: eliminate swallows | Low | High | Every catch block |
| Stage 5: no fake success | Very low | Very high | Every recovery path |
| Retrofitting legacy | High | Medium | Prioritize by risk |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make absence an explicit, documented outcome | Use `null` for absent *and* failed |
| Preserve cause at every wrap | `throw new Error("failed")` |
| Let `catch` do something observable | `catch {}` / debug-only |
| Return real outcomes | Return success when the work failed |

## Common mistakes

- **Fixing stage 5 only** (grep for `return true` in catch) and missing stage 3/4.
- **Debug-only logging** as "handling."
- **Assuming `null` is safe** when it is overloaded.
- **Over-abstracting** to a single `AppError` so nothing is classifiable.

## Checklist

- [ ] Does every lookup distinguish "absent" from "failed"?
- [ ] Does every wrap preserve the cause?
- [ ] Does every catch handle/translate/rethrow/record?
- [ ] Is there any path where failure returns a success shape?
- [ ] Can you classify an incident from its error type alone?

## Related

- [Preserving and Not Swallowing Errors](../01-concepts/04-preserving-and-not-swallowing-errors.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Chapter 58 — Less Obvious Error-Handling Scenarios](../../../part-23-special-cases/58-less-obvious-error-handling-scenarios/README.md)
- [Glossary: error translation](../../../GLOSSARY.md)
