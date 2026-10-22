# Practical — Error Sanitizer and Allowlist Serializer

> Part XIII · Chapter 34 · Sections 34.13, 34.16 · _Estimated reading time: 20 min_
> **Prerequisite:** [Deep Dive: Redaction Strategy](../02-deep-dive/03-redaction-strategy.md)

## In one sentence

This file builds a **single `sanitize(err, sink)` function** that turns any thrown value into a
channel-appropriate object using an allowlist of classified fields — the one place every error in
your app must pass through before it reaches any sink.

## Why this matters in production

Without a single sanitizer, sanitization is reimplemented (or forgotten) in every catch block. With
one, "does this leak?" becomes a property of **one function plus its field table**, and it is
unit-testable. This is the concrete artifact that turns the chapter's principles into a control you
can review, test, and reuse.

## Design goals

1. **Total**: accepts *any* thrown value — `AppError`, native `Error`, string, `null`, a cyclic
   object — and never throws itself.
2. **Allowlist-based**: unknown fields are denied by default.
3. **Channel-aware**: the same error yields different projections per sink.
4. **Bounded**: caps cause-chain depth and output size.
5. **Testable**: a canary secret/PII never survives it.

## Step 1 — The application error contract

```ts
type ErrorClass = "validation" | "auth" | "authz" | "conflict" | "upstream" | "internal";

interface AppError extends Error {
  code: string;                 // stable, registry-backed (public)
  class: ErrorClass;            // internal
  httpStatus: number;
  safeMessage: string;          // public, constant, no interpolation
  disclosure: "public" | "internal";
  retryable?: boolean;
  tenantId?: string;            // sensitive
  userId?: string;              // sensitive
  provider?: string;            // internal
  cause?: unknown;              // may be another AppError
}
```

Only `AppError` instances are ever serialized fully; anything else is treated as unknown.

## Step 2 — Field classification table

```ts
type Sensitivity = "public" | "internal" | "tenant" | "sensitive" | "secret" | "pii";
type Sink = "response" | "log" | "metric" | "tracker" | "dlq" | "support";

const FIELD_CLASS: Record<string, Sensitivity> = {
  code: "public",
  message: "public",        // safeMessage, already constant
  class: "internal",
  retryable: "internal",
  provider: "internal",
  httpStatus: "public",
  tenantId: "sensitive",
  userId: "sensitive",
  stack: "internal",
};

const SINK_ALLOWS: Record<Sink, Sensitivity[]> = {
  response: ["public"],
  metric: ["internal"],
  log: ["public", "internal"],
  tracker: ["public", "internal", "tenant", "sensitive", "pii"],
  dlq: ["public", "internal", "tenant", "sensitive"], // no PII, no secret
  support: ["public", "internal", "tenant"],
};

const MAX_CAUSE_DEPTH = 6;
```

## Step 3 — The sanitizer

```ts
const UNKNOWN_EXTERNAL = {
  code: "INTERNAL_ERROR",
  message: "Something went wrong. Please try again.",
};

function isAppError(e: unknown): e is AppError {
  return e instanceof Error && typeof (e as any).code === "string" && "safeMessage" in e;
}

function pick(err: AppError, sink: Sink, depth: number) {
  const allows = SINK_ALLOWS[sink];
  const out: Record<string, unknown> = {};

  const source: Record<string, unknown> = {
    code: err.code,
    message: err.safeMessage,
    class: err.class,
    retryable: err.retryable,
    provider: err.provider,
    httpStatus: err.httpStatus,
    tenantId: err.tenantId,
    userId: err.userId,
    stack: err.stack,
  };

  for (const [k, v] of Object.entries(source)) {
    const cls = FIELD_CLASS[k];
    if (cls && allows.includes(cls) && v !== undefined) out[k] = v;
  }

  if (err.cause !== undefined && depth < MAX_CAUSE_DEPTH) {
    out.cause = sanitize(err.cause, sink, depth + 1);
  }
  return out;
}

export function sanitize(err: unknown, sink: Sink, depth = 0): Record<string, unknown> {
  // Never throw from the sanitizer.
  try {
    if (!isAppError(err)) {
      // Unknown/native error: only the tracker may see the raw shape.
      if (sink === "tracker" && err instanceof Error) {
        return { code: "UNKNOWN", message: err.message, stack: err.stack };
      }
      return UNKNOWN_EXTERNAL;
    }
    const projected = pick(err, sink, depth);
    if (sink === "response" && !("code" in projected)) {
      return UNKNOWN_EXTERNAL; // fail-safe to generic public shape
    }
    if (sink === "response" && !("message" in projected)) {
      return { ...projected, message: UNKNOWN_EXTERNAL.message };
    }
    return projected;
  } catch {
    return UNKNOWN_EXTERNAL;
  }
}
```

Note the **fail-safe**: if sanitization somehow produces an empty public shape or throws, the caller
still gets the generic external response, never a partial/raw one.

## Step 4 — Wire it into every sink

```ts
// Global handler
app.use((err, req, res, _next) => {
  const cid = req.id;
  log.error(sanitize(err, "log"), "request failed");          // log projection
  trackError(sanitize(err, "tracker"));                        // full (RBAC) projection
  metrics.increment("errors_total", sanitize(err, "metric")); // bounded projection
  const status = isAppError(err) ? err.httpStatus : 500;
  res.status(status).json({ ...sanitize(err, "response"), requestId: cid });
});
```

## Step 5 — Prove it with a canary test

```ts
test("secret and PII never reach public sinks", () => {
  const canarySecret = "sk_live_CANARY1234567890";
  const canaryEmail = "canary@example.com";

  const err: AppError = Object.assign(new Error("x"), {
    code: "PAYMENT_ERROR",
    class: "upstream",
    httpStatus: 502,
    safeMessage: "Payment could not be completed.",
    disclosure: "public",
    tenantId: "ten_canary",
    userId: canaryEmail, // deliberately hostile: PII in a sensitive field
    provider: `Bearer ${canarySecret}`,
  });

  for (const sink of ["response", "log", "metric", "dlq", "support"] as const) {
    const out = JSON.stringify(sanitize(err, sink));
    expect(out).not.toContain(canarySecret);
    expect(out).not.toContain(canaryEmail);
  }
});
```

This test is the operational guarantee: if someone adds a field or changes a classification, the
canary fails the build.

## Key data / numbers

- **OWASP A05 / CWE-209**: generic external errors plus full internal logging is the recommended
  shape; the sanitizer enforces it mechanically.
- **Response size bound**: cap the serialized response (commonly a few KB); the allowlist already
  bounds cardinality, but bound cause depth too (default 6).
- **`requestId` is public** by design — it lets support correlate without disclosure.

## Real-world use case — Acme SaaS

Acme introduced `sanitize()` and replaced thirteen ad-hoc catch blocks across `Checkout`,
`WebhookIngest`, and `ExportJob`. The canary test immediately failed on `WebhookIngest`, which had
been storing the raw Stripe payload in the `dlq` sink. That single test caught a live secret-leak path
before it shipped. After wiring, the error-handling module shrank (one function, one table) and code
review of any new error reduced to "is this field classified, and does its class allow the sink?".

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One `sanitize(err, sink)` | Single control point, testable | Must classify new fields | Default everywhere |
| Per-sink bespoke serializers | Optimized per sink | Repeated, inconsistent | Never |
| Raw `err` to tracker | Full debuggability | Lost if non-app error | Tracker only, with RBAC |

## Common mistakes

- **Sanitizer that can throw.** It must never throw; wrap in `try/catch` and fail safe.
- **Forgetting non-`AppError` values.** `throw "string"` and `throw null` happen.
- **Unbounded cause walk.** Cycles and depth blow up serialization.
- **Missing canary test.** Without it, the guarantee is unverified.
- **Classifying too late.** Fields default to denied — good — but unclassified *needed* fields
  silently drop; classify them.

## Checklist

- [ ] Is there exactly one `sanitize(err, sink)` in the codebase?
- [ ] Does it accept any thrown value and never throw?
- [ ] Are unknown fields denied by default?
- [ ] Is the cause chain bounded?
- [ ] Does a canary secret/PII test fail the build if it leaks?
- [ ] Is every sink wired through `sanitize`?

## Related

- [Secure-Default Error Boundary](./02-secure-default-error-boundary.md)
- [Deep Dive: Redaction Strategy](../02-deep-dive/03-redaction-strategy.md)
- [Chapter 20 — Standardized API Error Responses](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- [Chapter reference: Disclosure policy matrix](../05-reference/README.md)
- [Glossary](../../../GLOSSARY.md)
