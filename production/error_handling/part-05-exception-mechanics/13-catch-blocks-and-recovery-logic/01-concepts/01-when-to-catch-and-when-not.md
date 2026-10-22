# When to Catch and When Not To

> Part V · Chapter 13 · Sections 13.1, 13.2, 13.17 · _Estimated reading time: 15 min_
> **Prerequisite:** [Propagation Through Call Stacks](../../12-exception-propagation-and-control-flow/01-concepts/01-propagation-through-call-stacks.md)

## In one sentence

Catch **only when you can change the outcome for the better** — recover, translate, add context,
or run mandatory cleanup — otherwise let it propagate; a catch block with no such purpose is a bug.

## Why this matters in production

Every unnecessary catch is a place a failure can be silently absorbed. Every misplaced catch
(a catch in the domain where the fallback belongs at the edge) is a boundary bug. The default
posture should be **propagate**; catching is the deliberate exception. Teams that invert this end
up with "handled" errors that never reach an observer and outages that look like successes.

## Core concept

A catch block is justified by exactly one of these purposes:

| Purpose | What it looks like | Catch level |
| ------- | ------------------ | ----------- |
| **Recover** | Provide a safe fallback; retry transient | Where the fallback is known |
| **Translate** | Map to domain/transport error | At a boundary |
| **Add context** | Wrap with operation name, rethrow | Any layer with meaning |
| **Cleanup** | Release a resource then rethrow | The acquiring frame (`finally`) |
| **Terminate** | Fail fast on corrupted state | Process/request boundary |

If a catch does none of these, **delete it**.

### When not to catch (13.2)

- **You cannot do anything useful.** Let the caller decide.
- **You only want to log.** Log at *one* boundary, not at every layer (to avoid duplicate noise).
- **You would swallow to keep going.** Continuing after an unknown error is how corruption spreads.
- **The fallback belongs to a caller.** Catching removes their ability to decide.
- **The error is expected and frequent.** Model it as a result value, not a catch.

### Catches as architectural decisions (13.17)

Where you catch *is* an architecture decision because it sets the **observable outcome** of a
failure. `catch` at the domain layer says "this domain error never reaches the API". `catch` at the
edge says "the domain exposes its errors to callers, who translate them". Those are different
architectures, and both can be correct — but they must be **chosen**, not accidental.

```text
Domain catches everything → API never sees domain errors → boundary cannot classify them
Edge catches nothing       → a single global handler guesses → business policy in the wrong place
```

## How it works (mechanics)

Decision procedure for a proposed catch:

1. **What errors can reach this frame?** Enumerate them.
2. **For each, is the safe outcome here different from propagating?** If no for all → no catch.
3. **Can this frame produce that outcome correctly?** If it lacks context → move up/down.
4. **Does recovering here leave state valid?** (Chapter 13.15) If not → don't recover here.
5. **What does the caller see?** Make that explicit — return value, rethrow, or termination.

## Worked example

```ts
// ❌ A catch with no purpose: catches, logs, rethrows the same object.
//    Adds a duplicate log, changes nothing.
async function listProjects(tenantId: string) {
  try {
    return await repo.list(tenantId);
  } catch (err) {
    logger.error(err);  // duplicate; the boundary will log too
    throw err;          // identity unchanged → net effect: log noise
  }
}

// ✅ No catch: let it propagate to the boundary.
function listProjects(tenantId: string) {
  return repo.list(tenantId);
}
```

```ts
// ✅ A catch WITH a purpose: provide a degraded fallback for an optional feature.
async function dashboard(tenantId: string) {
  const projects = await repo.list(tenantId); // required — no catch
  let summary: string | null = null;
  try {
    summary = await llm.summarize(tenantId); // optional — recover
  } catch (err) {
    logger.warn({ err }, "summary unavailable; rendering dashboard without it");
    summary = null; // safe fallback
  }
  return render(projects, summary);
}
```

The rule in one line: **catch the optional, propagate the required.**

## Key data / numbers

- **`finally` / `defer` / `with`** are the cleanup mechanism, not `catch`; use them for "run no
  matter what" (Chapter 14).
- **Structured logging**: log once per failure at the boundary; multiple layers logging the same
  error multiplies volume with no added signal.
- **HTTP boundary**: the global handler is typically the *only* place that logs a full error and
  maps it to a status (Chapters 20–21).
- **Retry ownership**: exactly one layer retries; a catch-and-retry in two layers multiplies
  attempts (Chapter 27).

## Real-world use case — Acme SaaS

Acme's `AgentRun` wrapped each LLM call in a catch that logged and rethrew. Because the boundary
also logged, every provider error produced two log lines — and the inner one lacked request
context, so it was unsearchable. On removing the inner catch (the call was required; the run
should fail), log volume dropped and the boundary record was complete. Separately, the optional
"summarize" step kept its catch and degraded cleanly. Same pattern, opposite decisions, both
correct.

## Trade-offs

| Catch posture | Pros | Cons | When |
| ------------- | ---- | ---- | ---- |
| Never catch (propagate) | Simple, complete context | No degradation | Required operations |
| Catch at boundary only | One place to classify | Coarse; no per-feature fallback | Small services |
| Catch per optional feature | Fine-grained degradation | More code | Optional dependencies |
| Catch everything everywhere | "Nothing crashes" | Silent failures; corruption | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Catch only with a stated purpose | Catch to "be safe" |
| Propagate required failures | Wrap required ops in a fallback |
| Catch optional features locally | Put optional features on the critical path |
| Decide catch placement once per module | Let each author improvise |
| Model frequent expected failures as results | Catch them as exceptions per item |

## Common mistakes

- **Catch-log-rethrow** at every layer — duplicate logs, no added value.
- **Catching in the domain** because "errors shouldn't leak" — now the boundary cannot classify.
- **Catching to keep the process alive** after an unknown error — state may be corrupt.
- **Catching a frequent expected error** instead of returning a result — cost at scale.

## Checklist

- [ ] Every catch has a one-line stated purpose.
- [ ] Required operations propagate to the boundary.
- [ ] Optional features have their own catch and fallback.
- [ ] No catch logs and rethrows the identical error.
- [ ] Catch placement is documented per module.

## Related

- [Catching Specific Types and Categories](./02-catching-specific-types-and-categories.md)
- [Recovery Inside Catch](./03-recovery-inside-catch.md)
- [Error Boundaries (Part VI)](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Avoiding Swallowing Errors (Part I)](../../../part-01-foundations/02-principles-of-high-quality-error-handling/README.md)
