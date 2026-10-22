# Unreachable Handlers, Failure→Success, and Conventions

> Part V · Chapter 12 · Sections 12.16, 12.17, 12.19, 12.20 · _Estimated reading time: 16 min_
> **Prerequisite:** [Rethrow, Wrap, and Preserve Cause](./04-rethrow-wrap-and-preserve-cause.md)

## In one sentence

Three propagation defects — **handlers that never run**, **failures that become successes**, and
**ignored cost** — are silent, and the cure is a small set of **propagation conventions** applied
consistently.

## Why this matters in production

These bugs do not throw; they corrupt. An unreachable `catch` means your "handled" path was never
taken. A failure→success conversion means a caller who trusted you gets invalid data. Cost matters
because exceptions are not free at scale: capturing stacks on a hot validation path can dominate
CPU. All three are invisible in code review unless you look specifically for them.

## Core concept

### Unreachable handlers (12.16)

A handler that can never run because:

- **Earlier catch swallows everything.** `catch (e) {}` above a specific handler.
- **Wrong type ordering.** Catching a supertype (`Error`) before a subtype (`ValidationError`) —
  in Java the subtype handler must come first; in JS order is author's choice but the first match
  wins.
- **Dead condition.** `catch (e) { if (e.code === 'X') ... }` where the code is never produced.
- **Async mismatch.** `try/catch` around a scheduled callback catches nothing.

| Symptom | Cause | Detection |
| ------- | ----- | --------- |
| Handler never logged | Earlier catch swallowed | Coverage/assert logging in handler |
| Subtype branch dead | Supertype caught first | Reorder; lint for `Error` first |
| "Impossible" branch | Event never emitted | Grep producers of the code |
| try/catch no-op | Callback scheduled async | Move catch into the callback |

### Avoiding failure→success conversion (12.17)

This is when failure is reported as success — often accidentally. Forms:

- Returning `null`/`[]`/`0` on error where callers cannot distinguish "none" from "failed".
- `catch { return defaultValue }` for a required operation.
- Marking a job `completed` when a step failed.
- HTTP `200` with an error body the client ignores.

### Handling costs (12.19)

Throwing is cheap until you capture a stack. At high volume:

- **Stack capture** walks the call stack and allocates — measurable under load (Chapter 57).
- **Exception-driven validation** turns a 1M-RPS validation path into a GC problem.
- Use **result types** for expected, high-frequency failures (validation, cache miss, not-found)
  and **exceptions** for exceptional ones.

### Propagation conventions (12.20)

Pick one and write it down:

1. **Throw at the lowest layer; translate at the boundary; never swallow.**
2. **Wrap with operation context; always preserve cause.**
3. **Catch only where the fallback differs.**
4. **Expected, high-rate failures use results, not exceptions.**
5. **One owner per retry decision.**

## How it works (mechanics)

Failure→success usually hides behind a default value. The bug is not the default; it is the
*ambiguity*.

```text
caller expects:   Result<T> = Ok(value) | Err(reason)
implementation:   returns null on error  →  caller sees null, treats as "empty"
```

The fix is to make the failure channel exist. Either throw, or return a discriminated result —
never a bare `null` that means two things.

For cost: measure stack-capture overhead before optimizing. A `new Error()` is roughly an order of
magnitude more expensive than returning a struct, but both are nanoseconds; only profiling on your
hot path tells you whether it matters.

## Worked example

```ts
// ❌ Failure→success: caller cannot tell "no user" from "query failed"
async function getUser(id: string): Promise<User | null> {
  try {
    return await db.findUser(id);
  } catch {
    return null; // connection error now looks like "not found"
  }
}

// ✅ Distinct channels
type Lookup = { ok: true; user: User } | { ok: false; reason: "not_found" };
async function getUser(id: string): Promise<Lookup> {
  const user = await db.findUser(id); // a connection error THROWS, is not caught here
  return user ? { ok: true, user } : { ok: false, reason: "not_found" };
}
```

```java
// ❌ Unreachable subtype handler: subtype caught by the broader clause first
try {
  process();
} catch (Exception e) {          // catches everything, including ValidationException
  handleGeneric(e);
} catch (ValidationException e) { // DEAD CODE — never reached
  handleValidation(e);
}

// ✅ Most specific first
try {
  process();
} catch (ValidationException e) {
  handleValidation(e);
} catch (Exception e) {
  handleGeneric(e);
}
```

## Key data / numbers

- **Java**: unreachable `catch` for a checked subtype is a *compile error*; for unchecked it is a
  silent logic bug. Order matters at both compile and runtime.
- **JS**: `catch` order is author-defined; a broad `catch` first makes later ones unreachable —
  no warning.
- **V8**: creating an `Error` and capturing a stack is on the order of a few microseconds in deep
  stacks; avoid in tight loops.
- **`async` in a loop with validation**: exceptions per item can dominate CPU before the DB is
  ever hit.
- **HTTP**: `200` + error body violates the contract for clients that branch on status; use `4xx`.

## Real-world use case — Acme SaaS

Acme's `ExportJob` wrapped every row write in `try/catch` and `continue`d on error. At the end it
marked the job `completed` regardless of how many rows failed. A tenant received a CSV with 18%
of rows missing and no indication. The fix: count failures, treat an all-fail chunk as a job
failure, and mark partial success explicitly in the job record. This is a **failure→success
conversion** caught in production.

Separately, Acme's validation endpoint threw an exception per invalid field. Under a 2k-RPS
import, profiler showed 60% of CPU in stack capture. They moved validation to a result type; CPU
dropped by more than half.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Exceptions for everything | Uniform control flow | Costly at volume; erodes "exceptional" | Rare, truly exceptional errors |
| Results for expected failures | Cheap; explicit; type-safe | More boilerplate | Validation, not-found, cache miss |
| Defaults on error | Simple call sites | Ambiguous; hides failure | ❌ Only genuine optional data |
| Strict "never swallow" | Observable | Slightly more code | Everywhere |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Order catches most-specific first | Catch `Exception`/`Error` first |
| Distinguish "none" from "failed" | Return `null` for both |
| Use results for high-frequency expected failures | Throw for every invalid field |
| Count and report partial failures | Mark a job "completed" regardless |
| Document propagation rules once | Let each module invent its own |

## Common mistakes

- **Broad catch above specific ones** — later handlers are dead.
- **`catch { return [] }`** for a required query — hides an outage as "empty".
- **Exception-per-item** in bulk validation — CPU cliff at scale.
- **No convention document** — every author guesses, cross-module behavior drifts.

## Checklist

- [ ] Every handler can actually be reached (no broader catch above it).
- [ ] No required operation returns a default on error.
- [ ] Partial successes are reported as partial, not complete.
- [ ] Expected hot-path failures use results, not exceptions.
- [ ] The team has one written propagation convention.

## Related

- [Concurrent and Cross-Service Propagation](./03-concurrent-and-cross-service-propagation.md)
- [Sync, Async, and Callback Propagation](./02-sync-async-and-callback-propagation.md)
- [Error-Handling Under Load and at Scale (Part XXII)](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
- [Avoiding Swallowing Errors (Part I)](../../../part-01-foundations/02-principles-of-high-quality-error-handling/README.md)
