# Validation Details and Causal Chaining

> Part III · Chapter 6 · Sections 6.13–6.14 · _Estimated reading time: 15 min_
> **Prerequisite:** [Cause, Context, and Correlation](./03-cause-context-and-correlation.md)

## In one sentence

**Field-level details** describe *which parts of the input* were invalid in a structured,
client-actionable way, while **causal chaining** links an error to the sequence of errors that
produced it so the whole story is reconstructable.

## Why this matters in production

Two failures look identical at the top level but need opposite handling. A single `VALIDATION_
FAILED` with no details forces the frontend to guess which field to highlight; a bare message
string loses the ability to map errors back to form inputs. And an error chain that stops at the
outer wrap hides the actual culprit — the vendor's `ECONNRESET` buried two layers down. Both are
representation problems, both are solved by structure.

## Field-level validation details (6.13)

A validation error is rarely about one thing. Represent it as an **array of field details** so a
client can attach each message to the right input and a handler can return all problems at once.

```ts
interface FieldError {
  field: string;        // JSON pointer or dot path: "email", "items[2].sku"
  code: string;         // stable: "REQUIRED", "INVALID_FORMAT", "OUT_OF_RANGE"
  message: string;      // human-readable, localizable
  value?: unknown;      // the rejected value (ONLY if safe to echo)
  meta?: Record<string, unknown>; // e.g. { min: 1, max: 10 }
}
```

```ts
const err: AppError = {
  name: "ValidationError",
  code: "VALIDATION_FAILED",
  category: "validation",
  severity: "info",
  recoverable: true,
  retryable: false,
  message: "2 fields failed validation",
  details: [
    { field: "email", code: "INVALID_FORMAT", message: "Enter a valid email address" },
    { field: "items[2].quantity", code: "OUT_OF_RANGE", message: "Quantity must be 1–10",
      meta: { min: 1, max: 10 } },
  ],
  timestamp: new Date().toISOString(),
};
```

Design rules:

- **Stable per-field codes**, not prose. `INVALID_FORMAT`, `REQUIRED`, `OUT_OF_RANGE`.
- **Paths follow the request shape.** `items[2].quantity` lets the client find the input.
- **Do not echo sensitive values.** For `password` or `token` fields, omit `value`.
- **Aggregate, don't fail on the first field** unless there is a binding reason (Chapter 17).
- **Avoid duplicates** for the same field+code; deduplicate before returning.

> ⚠️ **Hazard.** Echoing the rejected `value` can reflect untrusted input back into a UI (XSS) and
> leak data into logs. Echo only when the value is non-sensitive and the client will render it
> safely.

## Causal relationships and chaining (6.14)

A **causal chain** is the ordered set of errors from the original fault to the current
representation. Each wrap links to its cause; traversing the links reconstructs the sequence.

```text
AppError(PAYMENT_PROVIDER_TIMEOUT)
  └─ cause: StripeSDKError("Request timed out after 10000ms")
        └─ cause: FetchError("ETIMEDOUT")
              └─ cause: SocketError("connect ETIMEDOUT 10.0.0.1:443")
```

```ts
function walk(err: unknown, depth = 0): string[] {
  const out: string[] = [];
  for (let e = err; e && depth < 20; e = (e as { cause?: unknown }).cause, depth++) {
    out.push(describe(e));
  }
  return out;
}
```

Chaining rules:

- **Append meaning, never mutate the cause.** Each layer adds context (which step, which provider).
- **Cap depth** (10–20) and detect cycles.
- **Mark ownership.** A chain often crosses domains (network → SDK → application); the top error
  should state the application meaning.
- **Keep one primary error.** When wrapping for a multi-error scenario (e.g. `AggregateError`), mark
  which cause is the *primary* one so retry/alert decisions are unambiguous.

```ts
// AggregateError: many failures, one primary.
throw new AppError("EXPORT_PARTIAL_FAILURE", "3 of 100 shards failed", {
  cause: new AggregateError(failures, "shard failures"),
  metadata: { primaryShard: "shard_7", failedCount: 3, totalCount: 100 },
});
```

## Worked example

```ts
// Inbound create-project request, validated then persisted.
function validateCreateProjectDTO(input: unknown): CreateProjectDTO {
  const problems: FieldError[] = [];
  if (typeof input !== "object" || input === null) {
    throw new ValidationError("VALIDATION_MALFORMED_BODY", "Request body must be an object");
  }
  const { name, members } = input as Record<string, unknown>;
  if (!name || typeof name !== "string") {
    problems.push({ field: "name", code: "REQUIRED", message: "name is required" });
  } else if (name.length > 120) {
    problems.push({ field: "name", code: "OUT_OF_RANGE", message: "name must be ≤ 120 chars",
      meta: { max: 120 } });
  }
  if (!Array.isArray(members)) {
    problems.push({ field: "members", code: "REQUIRED", message: "members must be an array" });
  }
  if (problems.length) {
    throw new ValidationError("VALIDATION_FAILED", `${problems.length} field(s) invalid`, {
      details: problems,
    });
  }
  return input as CreateProjectDTO;
}
```

The client receives one `422` with an array it can map directly to inputs — no guessing, no
second round-trip to discover the next error.

## Key data / numbers

- **RFC 9457** has no standard field-array member; the common extension is `errors` or `details`,
  each entry with `pointer`/`field`, `detail`, and an app `code`.
- **JSON Pointer (RFC 6901)** is the standard way to point at a sub-value (`/items/2/quantity`);
  many APIs use dot/bracket notation as a friendlier alias.
- **Cap** the number of returned details (commonly 20–100) to bound response size; summarize the
  rest (`truncated: true`).
- **Common field codes:** `REQUIRED`, `INVALID_TYPE`, `INVALID_FORMAT`, `OUT_OF_RANGE`,
  `NOT_UNIQUE`, `UNKNOWN_FIELD`.

## Real-world use case — Acme SaaS

Acme's "invite members" form accepted a bulk list. Early validation returned a single
`"Invalid input"` message, so users fixed one error per submit. After representing `details` as an
array of `{ field, code, message }`, the UI highlights every bad row at once and renders a
localized message per code. Support tickets mentioning "won't save" dropped sharply, and the
frontend mapped codes to messages without ever parsing the server prose.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Aggregate all field errors | One round-trip, best UX | Larger payloads | Default for forms/bulk |
| Fail on first error | Simple, least data | Poor UX, repeated submits | Streaming/expensive validation only |
| Details as free text | Fast to write | Not machine-mappable | Never for APIs |
| Deep causal chain | Full diagnosis | Memory, may include internals | Internally; redact externally |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use stable codes per field | Return "invalid" with no field |
| Point fields at request paths | Use human labels like "the second item" |
| Cap detail count and chain depth | Return unbounded arrays/chains |
| Mark the primary error in aggregates | Make handlers guess which failed |

## Common mistakes

- **Flat validation error.** One message, no fields; clients cannot map to inputs.
- **Echoing sensitive values** back in `value`.
- **Chain that stops at the wrap,** losing the vendor/network cause.
- **Duplicate details** for the same field and code.
- **Cycle in the chain** from an error whose cause eventually points back to itself.

## Checklist

- [ ] Do validation errors carry a structured `details` array?
- [ ] Are field paths resolvable against the request shape?
- [ ] Are field codes stable and duplicate-free?
- [ ] Is the original cause always reachable through the chain?
- [ ] Is chain depth bounded and cycle-safe?
- [ ] Is the primary cause marked for aggregates?

## Related

- [Core Identity Fields](./02-core-identity-fields.md)
- [Immutability, Serialization, and Safety](./05-immutability-serialization-and-safety.md)
- [Chapter 17 — Input Validation Error Handling](../../../part-07-validation-and-business-errors/17-input-validation-error-handling/README.md)
