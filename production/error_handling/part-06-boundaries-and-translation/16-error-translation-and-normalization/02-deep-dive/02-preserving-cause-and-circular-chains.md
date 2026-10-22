# Preserving Cause and Avoiding Circular Chains

> Part VI · Chapter 16 · Sections 16.10, 16.11, 16.17 · _Estimated reading time: 20 min_
> **Prerequisite:** [Preserving Cause and Recoverability](../01-concepts/03-preserving-cause-and-recoverability.md)

## In one sentence

Cause chaining is how translation stays lossless for debugging, but it must be **directed and
acyclic** — every translated error points exactly one level down to its origin, never to itself and
never in a loop.

## Why this matters in production

A preserved cause is the difference between a 5-minute root-cause and an hour of guessing. A
*circular* cause is worse than none: `toString()`, stack renderers, and serializers that walk
`cause` loop forever or overflow, turning a log statement into an outage. Translation is the most
common place cycles are introduced because every hop is a wrap opportunity.

## The chain as a directed acyclic graph

```text
TransportError: "request failed"        (depth 0)
   └─cause─▶ DomainError: EMAIL_ALREADY_USED   (depth 1)
                └─cause─▶ PgError: 23505 "duplicate key ... users_email_key"  (depth 2)
                              └─cause─▶ (none — the origin)
```

Read top-down: the *outermost* error is the most abstract; the *innermost* is the origin. A good
chain has 2–4 links. Rules:

- **Each node has at most one `cause`.**
- **No node's `cause` (transitively) equals itself.**
- **The chain terminates at an error with no cause** (a leaf origin or an OS/driver error).

## Language mechanics (preserve correctly)

| Language | Create with cause | Read the chain | Guard for cycle |
| -------- | ----------------- | -------------- | --------------- |
| TS/JS | `new Error(m, { cause })` | `err.cause` | `Set` walk |
| Python | `raise New(...) from orig` | `e.__cause__` (`__context__`) | `Set` walk |
| Go | `fmt.Errorf("...: %w", err)` | `errors.Unwrap` / `errors.Is` | visited set on `errors.Unwrap` |
| Java | `new X(m, cause)` | `getCause()` | `Set` walk with null stop |
| .NET | `new X(m, inner)` | `InnerException` | `Set` walk |
| Rust | `#[source]` / `anyhow::Context` | `error.source()` | `chain()` is acyclic by construction |

> ⚠️ **Hazard.** Python's `raise New from None` **suppresses** the chain (`__suppress_context__`),
> and a bare `raise New` inside an `except` sets `__context__` implicitly. Know which you want:
> suppression hides the cause; implicit context can surprise.

## How cycles get introduced

### 1. Re-wrapping an already-normalized error

```ts
// ❌ A generic wrap applied at every layer wraps AppError inside AppError.
function wrap(err: unknown, msg: string) {
  return new AppError({ code: "INTERNAL_ERROR", safeMessage: msg, cause: err }); // no type check
}
```

If `wrap` runs at three boundaries over the same `AppError`, you get a 3-deep chain of identical
`INTERNAL_ERROR`s — noise, and a step toward a cycle if any step points upward.

```ts
// ✅ Do not re-wrap what is already normalized.
function wrap(err: unknown, msg: string) {
  if (err instanceof AppError) return err;      // already normalized — keep it
  return new AppError({ code: "INTERNAL_ERROR", safeMessage: msg, cause: err });
}
```

### 2. Self-referential cause

```python
# ❌ Always a bug: the node points to itself.
err.__cause__ = err
```

This is most often a typo in a generic helper: `wrapped.cause = wrapped` instead of
`wrapped.cause = original`.

### 3. Retry that re-wraps into itself

```ts
// ❌ Each attempt wraps the previous error, eventually forming a loop under a shared reference.
let last = initialError;
for (const attempt of attempts) {
  last = new RetryError(`attempt ${attempt}`, { cause: last });
}
```

Usually a chain, not a cycle, but under shared mutable references (or a retried object reused as
its own cause) it becomes one.

### 4. Serializer that mutates

A serializer that "helpfully" sets `err.cause = err.cause ?? err` to render a single node creates a
self-loop.

## Detecting and breaking cycles

### Runtime detection

```python
def chain_depth(err, limit=32):
    seen, depth, cur = set(), 0, err
    while cur is not None:
        if id(cur) in seen:
            return -1          # cycle detected
        seen.add(id(cur)); depth += 1
        if depth > limit:
            return -1          # runaway chain
        cur = getattr(cur, "__cause__", None)
    return depth
```

### Build-time / test guard

Add a test that walks the cause chain of every error produced by each translator and fails on a
cycle or depth > 4:

```ts
test.each(CASES)("translator produces an acyclic, bounded chain", (src) => {
  const app = translate(src.source, src.err);
  expect(hasCycle(app)).toBe(false);
  expect(chainDepth(app)).toBeLessThanOrEqual(4);
});
```

### Breaking a cycle at runtime

If a cycle is detected in production (defensively, before logging), sever it:

```ts
function safeChain(err: unknown): unknown {
  const seen = new Set<unknown>();
  let cur: any = err;
  while (cur && typeof cur === "object") {
    if (seen.has(cur)) { delete cur.cause; return err; } // cut the loop
    seen.add(cur);
    cur = cur.cause;
  }
  return err;
}
```

## Preserving retry class across the chain

The retry class (16.11) must survive every hop. A useful invariant: **the outermost error's
`transient` must equal the origin's retry classification.** Test it:

```ts
test("transient is preserved through translation", () => {
  const origin = { code: "40001" }; // serialization failure — transient
  const app = translate("postgres", origin);
  expect(app.transient).toBe(true);
});
```

If a translation *changes* `transient`, that is a deliberate policy decision — document it in the
rule and test it. Accidental changes are the bug.

## Cause vs context vs suppressed context

| Field | Purpose | Crosses network? |
| ----- | ------- | ---------------- |
| `cause` | The wrapped origin | ❌ server-side only |
| `context` / `__context__` | Implicit (Python) surrounding error | ❌ server-side only |
| details/meta | Safe structured context | ✅ if allowlisted |

Never serialize `cause` or `context`. Add a serializer test asserting the JSON body contains only
allowlisted fields (Ch. 15.14).

## Key data / numbers

- Target chain depth: **2–4** links; hard fail beyond **4**.
- Cycle-detector default max depth: **32** (guards runaway chains too).
- Python: `__cause__` (explicit `from`) vs `__context__` (implicit) vs `__suppress_context__`.
- Go: `%w` chains; `%v` does not — using `%v` silently breaks `errors.Is/As`.

## Real-world use case — ExportJob

An `ExportJob` DLQ replay path called a generic `wrap()` helper that re-wrapped every error at three
layers. When the log formatter rendered the chain, two attempts shared a reference and the `cause`
pointer looped, hanging the worker and filling the queue. The fix: `wrap()` returns early if the
error is already an `AppError`, a `hasCycle` guard runs before formatting, and a unit test asserts
depth ≤ 4 for every translator. The DLQ became inspectable, and the hang class disappeared.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Point each node's `cause` one level down | Set `cause` to itself |
| Skip re-wrapping already-normalized errors | Wrap `AppError` inside another `AppError` |
| Keep chains ≤ 4 links | Chain every boundary's wrap |
| Preserve `transient` through the chain | Let a hop silently flip retryability |
| Detect cycles before logging | Trust that no cycle exists |

## Common mistakes

- **Generic `wrap()`** re-wrapping normalized errors.
- **`err.cause = err`** from a helper typo.
- **`except: raise New()`** in Python without `from`, creating confusing implicit context.
- **Go `%v` instead of `%w`**, silently breaking the chain for `errors.Is`.

## Checklist

- [ ] Each cause node points one level down; chains terminate at an origin.
- [ ] Translation skips already-normalized errors.
- [ ] A cycle/depth guard runs before formatting or serializing.
- [ ] `transient` is preserved (or deliberately changed and tested) across hops.
- [ ] `cause`/`context` never cross the network boundary.

## Related

- [Translation Tables and Policies](./01-translation-tables-and-policies.md)
- [Preserving Cause and Recoverability](../01-concepts/03-preserving-cause-and-recoverability.md)
- [Part V — Exception Propagation and Control Flow](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
