# Deep Dive — Nested Causes and Leakage via Chains

> Part XIII · Chapter 36 · Sections 36.12–36.13 (mechanics) · _Estimated reading time: 19 min_
> **Prerequisite:** [Redaction, Omission, Sanitization, and Allowlists](../01-concepts/05-redaction-omission-sanitization-and-allowlists.md)

## In one sentence

Sensitive data hides in **nested causes** and leaks through **error chains**, because a top-level
sanitized error keeps a raw `.cause` (or a `cause` of a `cause`) that a careless serializer walks —
so chain serialization must apply the same allowlist and bounds at **every depth**.

## Why this matters in production

Chaining (`new Error("...", { cause })`) is the *correct* way to preserve the root cause — Chapter 34
wants you to keep it. But the preserved cause is often the *rawest* object in the system: a database
driver exception with SQL, an HTTP client error with headers and URL, a provider payload with PII. If
your external serializer or your logger walks `.cause` and emits it, all the sanitization on the outer
error is undone. This is one of the most common "we sanitized it, but it still leaked" bugs.

## How causes hide sensitive data

```text
OuterError (sanitized: code=PAYMENT_DECLINED, message=generic)
  └─ cause: UpstreamError (sanitized: provider=stripe)
       └─ cause: StripeError  <-- raw: request echo, card details, API key in URL
            └─ cause: AxiosError  <-- raw: request headers incl. Authorization
```

Three nesting traps:

1. **The outer error is safe, the innermost is raw.** Sanitizing only the outer error is insufficient.
2. **Aggregate causes.** `AggregateError.errors` is an array of causes; iterating it re-exposes raw
   errors.
3. **Cyclic causes.** A cause that references an ancestor (directly or via `cause` loops) breaks naive
   walkers or loops forever.

## The chain serializer

```ts
type Sink = "response" | "log" | "tracker";

const MAX_DEPTH = 6;
const MAX_CHAIN = 10; // total nodes across an aggregate

function isAppError(e: unknown): e is AppError {
  return e instanceof Error && "code" in (e as any);
}

export function serializeChain(
  err: unknown,
  sink: Sink,
  depth = 0,
  seen = new Set<unknown>(),
  budget = { nodes: 0 },
): unknown {
  if (depth > MAX_DEPTH || budget.nodes >= MAX_CHAIN) return "[truncated]";
  if (seen.has(err)) return "[cycle]";
  seen.add(err);
  budget.nodes++;

  // Only sanitized app errors may be represented at all.
  if (!isAppError(err)) {
    // The tracker may see native errors (still no secret guarantee — sanitize text).
    if (sink === "tracker" && err instanceof Error) {
      return { code: "UNKNOWN", message: sanitizeText(err.message) };
    }
    return "[non-app error omitted]";
  }

  const node = sanitize(err, sink); // per-sink allowlist projection

  // Aggregate causes: bound the array too.
  if (err instanceof AggregateError && Array.isArray(err.errors)) {
    (node as any).errors = err.errors
      .slice(0, MAX_CHAIN)
      .map((c) => serializeChain(c, sink, depth + 1, seen, budget));
  }

  if ((err as any).cause !== undefined) {
    (node as any).cause = serializeChain((err as any).cause, sink, depth + 1, seen, budget);
  }

  return node;
}
```

The invariants: **sanitize per node**, **bound depth and node count**, **detect cycles**, and **never
emit a raw native error to a non-tracker sink**.

## Why the tracker is still careful

The tracker is the sanctioned full-detail sink, but it must still avoid secrets, because trackers are
sometimes broadly readable and often export to third parties. So even in the tracker:

- **Secrets are never collected** (non-collection, not redaction).
- **PAN is never collected.**
- Native error messages are **sanitized** (control chars stripped, length bounded) before storage.

The tracker gets `class`, `provider`, `requestId`, `tenantId`, `stack`, and sanitized text — not the
raw provider payload.

## Aggregates and multi-error chains

Parallel operations produce `AggregateError` (Node) or a list of errors:

```ts
// ❌ Dumping the aggregate leaks every raw sub-error.
throw new AggregateError(rawErrors, "batch failed");

// ✅ Wrap each sub-error as a sanitized app error first.
throw new AggregateError(
  rawErrors.map((e) => toAppError(e)), // each sanitized
  "batch failed",
);
```

Convert raw errors to app errors **at the boundary**, before aggregation; then the chain serializer has
only safe nodes to walk.

## Detecting chain leaks

- **Canary test** on a nested chain: inject a secret at depth 3 and assert no sink sees it.
- **Static check** for `.cause` walkers that do not bound depth.
- **Serialization test**: feed a cyclic cause and assert termination with a `[cycle]` marker.

## Key data / numbers

- **CWE-209 / CWE-532**: nested raw errors are the classic mechanism for these weaknesses.
- **Cause depth bound**: commonly 5–10; truncate with a marker beyond it.
- **Chain node budget**: bound total nodes (e.g. 10) to avoid quadratic/aggregate blowup.
- **`AggregateError`**: standard in modern JS runtimes; `.errors` is the array to bound.

## Real-world use case — Acme SaaS

Acme sanitized the outer `PaymentError` correctly, but its logger walked `.cause` and emitted every
nested level. The innermost `AxiosError` carried the Stripe request with the customer's card number and
the API key in the URL — all of which reached the log despite the outer error being clean. Fix: the
logger uses `serializeChain(err, "log")`, which sanitizes per node, converts raw errors to
`[non-app error omitted]` for non-tracker sinks, and bounds depth; a canary test injects a secret at
depth 3 and asserts it appears in no sink. The "we sanitized it but it still leaked" bug was the nested
cause.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Sanitize per node + bound depth | No chain leak | Slightly more code | All chain serialization |
| Sanitize outer only | Simple | Nested raw errors leak | Never |
| Drop `cause` entirely | Safe | Loses root-cause debugging | If causes are never needed |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Sanitize every node in the chain | Trust that the outer error is enough |
| Bound depth and node count | Walk unbounded |
| Detect cycles | Risk infinite loops |
| Convert raw errors at the boundary | Aggregate raw errors then serialize |
| Sanitize native messages in the tracker | Store raw native errors wholesale |

## Common mistakes

- **One sanitize call on the outer error.** The chain leaks.
- **Unbounded `.cause` walk.** Cycles and blowup.
- **Ignoring `AggregateError.errors`.** An array of raw leaks.
- **Assuming the tracker can hold secrets.** Non-collection still applies.
- **No canary at depth.** The nested leak ships.

## Checklist

- [ ] Does the serializer sanitize **every** node, not just the outer error?
- [ ] Are cause depth and total node count bounded?
- [ ] Are cycles detected?
- [ ] Are raw errors converted to app errors at the boundary?
- [ ] Is `AggregateError.errors` bounded?
- [ ] Does a canary test inject a secret at depth > 1?

## Related

- [Safe Serialization and Context Allowlists](./02-safe-serialization-and-context-allowlists.md)
- [Redaction, Omission, Sanitization, and Allowlists](../01-concepts/05-redaction-omission-sanitization-and-allowlists.md)
- [Practical: Context Allowlist for Errors](../03-practical-examples/02-context-allowlist-for-errors.md)
- [Chapter 6 §6.14 — Chaining/Causal Relationships](../../../part-03-error-models/06-designing-the-applications-error-model/README.md)
- [Glossary](../../../GLOSSARY.md)
