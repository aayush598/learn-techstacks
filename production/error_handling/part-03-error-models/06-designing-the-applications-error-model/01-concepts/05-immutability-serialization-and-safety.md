# Immutability, Serialization, and Safety

> Part III · Chapter 6 · Sections 6.15–6.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Cause, Context, and Correlation](./03-cause-context-and-correlation.md)

## In one sentence

Treat an error object as an **immutable, deliberately serializable, cycle-free record that never
contains sensitive data** — because it will be logged, copied, queued, and shown to someone you
did not anticipate.

## Why this matters in production

Error objects travel further than most data: into log pipelines, trace spans, dead-letter queues,
webhooks, support dashboards, and HTTP responses. Mutable errors corrupt under concurrent handling;
undeliberate serialization leaks internals or throws mid-serialization (the worst possible time);
circular references crash `JSON.stringify` in your error path; and sensitive data in messages is a
breach. Each of these ten failure modes has shipped in real systems.

## Immutable vs mutable (6.15)

**Immutable** means: once constructed, fields are not reassigned. New information means a **new**
error object whose `cause` is the old one.

Why:

- **Concurrency.** The same error may be handled by multiple catch blocks; mutation races.
- **Auditing.** A mutable error can be silently "sanitized" before logging, losing evidence.
- **Predictability.** Handlers can read any field and trust it has not changed.

```ts
class AppError extends Error {
  readonly code: string;
  readonly category: ErrorCategory;
  readonly severity: Severity;
  readonly retryable: boolean;
  readonly metadata: Readonly<Record<string, unknown>>;
  constructor(...) { /* ... */ Object.freeze(this.metadata); }
}

// Adding context = wrapping, not mutating.
const enriched = new AppError("EXPORT_UPLOAD_FAILED", "S3 upload failed", { cause: original });
```

If you need to add context, prefer a **named constructor** or builder that produces a fresh object.

## Serializable vs non-serializable (6.16)

An error may contain fields that cannot or must not cross a boundary. Separate them.

| Field | Serializable? | Crosses HTTP? | Crosses queue? |
| ----- | ------------- | ------------- | -------------- |
| `code`, `category`, `severity`, `retryable` | Yes | Yes (mapped) | Yes |
| `message` | Yes | Maybe (public version) | Yes |
| `details` | Yes | Yes (public fields) | Yes |
| `cause` | Often no (native objects) | **No** | Sanitized form only |
| `stackTrace` | Text, but sensitive | **No** | **No** (logs only) |
| `metadata` | If scalars only | Allowlisted subset | Allowlisted subset |

Provide an explicit **serializer** that emits a known shape:

```ts
function toLogJSON(err: AppError): Record<string, unknown> {
  return {
    code: err.code,
    category: err.category,
    severity: err.severity,
    retryable: err.retryable,
    message: err.message,
    details: err.details,
    metadata: err.metadata,
    correlationId: err.correlationId,
    timestamp: err.timestamp,
    stack: err.stackTrace,
    cause: err.cause instanceof Error ? { name: err.cause.name, message: err.cause.message }
                                       : undefined,
  };
}

function toClientJSON(err: AppError): Record<string, unknown> {
  return {
    code: err.code,
    message: publicMessageFor(err.code),
    details: err.details?.map(({ field, code, message }) => ({ field, code, message })),
    correlationId: err.correlationId,
  };
}
```

Two serializers, two audiences. The client serializer is a **projection**, not `JSON.stringify(err)`.

> ⚠️ **Hazard.** `JSON.stringify(error)` is almost always wrong: it drops `message` on some
> runtimes, includes enumerable internals, and can throw on cycles.

## Avoiding circular references (6.17)

Cycles appear when `metadata` references a request object that references the error, or when a
cause chain loops. `JSON.stringify` throws `TypeError: Converting circular structure to JSON`.

Prevention:

- **Never store live objects** (request, response, socket, user) in `metadata`; store IDs.
- **Cap and validate the cause chain**; detect a repeated node.
- **Use a cycle-safe stringifier** only as a last resort, never as the primary design.

```ts
function serializeSafe(err: AppError): string {
  const seen = new WeakSet<object>();
  return JSON.stringify(err, (_key, value) => {
    if (typeof value === "object" && value !== null) {
      if (seen.has(value)) return "[Circular]";
      seen.add(value);
    }
    return value;
  });
}
```

Cycle-safe serialization is a guardrail, not a license to embed arbitrary objects.

## Preventing sensitive data (6.18)

The error model is a disclosure surface. Enforce safety at **construction**, not at serialization.

- **Allowlist metadata keys** at the call site; reject unknown keys in development.
- **Never** put credentials, tokens, cookies, auth headers, PII, full request bodies, or payment
  data in `message`, `metadata`, or details.
- **Redact or omit** in `toString`/log-of-last-resort paths.
- **Review the cause chain** — sensitive data hides in nested vendor errors.
- **Fail safe:** an unknown error becomes a generic, safe `INTERNAL_UNEXPECTED`, never a passthrough
  of the raw message.

```ts
const SENSITIVE = /password|token|secret|authorization|cookie|card[_-]?number/i;
function assertSafeKey(key: string): void {
  if (SENSITIVE.test(key)) throw new Error(`Sensitive key rejected from error metadata: ${key}`);
}
```

(Full redaction policy is Chapter 36; here, the rule is that the *model* makes leakage hard.)

## Worked example

```ts
// Before: leaks and crashes.
catch (e) {
  logger.error("failed", { err: e, body: req.body, headers: req.headers });
  // body may hold the password; headers hold the token; req→error cycle throws.
}

// After: explicit, safe, cycle-free.
catch (e) {
  const appErr = toErrorObject(e, {
    correlationId: ctx.correlationId,
    metadata: { tenantId: ctx.tenantId, route: req.route, method: req.method },
  });
  logger.error(appErr.message, toLogJSON(appErr)); // no body, no headers
}
```

## Key data / numbers

- **`Object.freeze`** is shallow; freeze nested `metadata` explicitly or use a readonly type.
- **`WeakSet`** is the standard cycle-detection tool for serializers.
- **Log payload budgets:** aim to keep error payloads **≤ 8 KB**; large payloads get truncated (and
  truncation can hide the useful part).
- **Common sensitive key patterns:** `password`, `token`, `secret`, `authorization`, `cookie`,
  `ssn`, `card_number`, `cvv`.
- **OWASP** categorizes "sensitive data exposure" via error messages as a top API risk
  (API Security Top 10).

## Real-world use case — AgentRun

Acme's `AgentRun` logged the full LLM prompt in error metadata to debug tool-call failures. The
prompt sometimes contained a customer's pasted API key and personal data, which then landed in the
log store and a support tool. After enforcing an allowlist (`model`, `toolName`, `tokenCount`,
`attempt`) and rejecting sensitive keys at construction, the same diagnostics were possible without
ever storing prompt content. The cycle-safe serializer also stopped intermittent
`Converting circular structure to JSON` crashes that spiked whenever a retry wrapped an already
wrapped error.

## Trade-offs

| Decision | Strict (fail on violation) | Lenient (redact silently) |
| -------- | -------------------------- | ------------------------- |
| Sensitive key in metadata | Throw in dev, strip in prod | Always strip |
| Unknown error passthrough | Map to generic code | Echo raw message |
| Serialization | Explicit per-audience serializers | Generic stringify |
| Best for | Safety-critical, financial | Rapid prototyping |

For most production SaaS, **strict in development, strip-in-production** is the safest default:
you catch leaks during testing and never ship them.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Freeze error objects | Mutate fields after creation |
| Write per-audience serializers | `JSON.stringify(error)` for clients |
| Store IDs, not live objects | Put `req`/`res`/socket in metadata |
| Allowlist metadata keys | Spread arbitrary objects into metadata |
| Redact sensitive values in causes too | Assume only `message` matters |

## Common mistakes

- **Mutable errors** sanitized away before logging.
- **Cycle crash** at serialization time during an incident.
- **`JSON.stringify(err)`** as the client response — leaks or loses data.
- **Sensitive keys in nested cause** that redaction missed.
- **Unbounded payloads** that get truncated and lose the code.

## Checklist

- [ ] Are error fields immutable after construction?
- [ ] Is there a separate log serializer and client serializer?
- [ ] Can `JSON.stringify` run on every error without throwing?
- [ ] Is metadata built from an allowlist of safe keys?
- [ ] Are causes redacted, not just top-level fields?
- [ ] Are unknown errors mapped to a safe generic code?

## Related

- [Validation Details and Chaining](./04-validation-details-and-chaining.md)
- [Model Invariants](../02-deep-dive/01-model-invariants.md)
- [Chapter 36 — Sensitive Data and Error Context](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
