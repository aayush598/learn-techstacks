# What an Error Object Represents

> Part III · Chapter 6 · Sections 6.1–6.2 · _Estimated reading time: 16 min_
> **Prerequisite:** [Error, Fault, Failure, and Exception](../../../part-01-foundations/01-understanding-errors-and-failures/01-concepts/01-error-fault-failure-exception.md)

## In one sentence

An error object is a **self-contained, inspectable record of a failure** — including what it means,
what caused it, and what context it happened in — designed so that any handler, logger, or
boundary can decide what to do without parsing a human string.

## Why this matters in production

If the error object is only a message string, every downstream decision degrades to string
matching. You cannot reliably retry, redact, map to HTTP, or alert, because the information was
never structured. The cost shows up as duplicated `if (err.message.includes("timeout"))` checks
that break when a vendor changes wording, and as incident reviews where the only evidence is
`"fetch failed"`.

## What it represents (6.1)

An error object is a **data carrier** for three irreducible facts:

| Fact | Field family | Example |
| ---- | ------------ | ------- |
| **What condition occurred** | code, category, message | `PAYMENT_CARD_DECLINED`, `payment`, "Card was declined" |
| **Why it occurred** | cause, chain | `cause: StripeCardError(card_declined)` |
| **Under what circumstances** | context, correlation, time | tenant `t_42`, request `req_8f3`, `2026-03-01T10:22:01Z` |

It is *not*:

- A replacement for logging (it is the payload a logger consumes).
- A user-facing message (that is derived later, at the boundary, usually from the code).
- A status code (that is a transport mapping, see Chapter 8).
- A control signal (cancellation is not an error — see Chapter 31).

> ⚠️ **Hazard.** Treating the object as "the exception" ties it to a language. In Go an error is
> just a value; in Rust it is an enum. The *model* must survive all of those.

## The standard internal structure (6.2)

Think of the model as **four layers**, from most stable to most volatile:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. IDENTITY      code, name, category, subcategory, severity │  ← stable contract
├─────────────────────────────────────────────────────────────┤
│ 2. EXPLANATION   message (human), details (field-level)      │  ← semi-stable
├─────────────────────────────────────────────────────────────┤
│ 3. CAUSALITY     cause, errorChain                           │  ← diagnostic
├─────────────────────────────────────────────────────────────┤
│ 4. CONTEXT       metadata, correlationId, tenant, timestamp  │  ← per-occurrence
└─────────────────────────────────────────────────────────────┘
```

A canonical shape (TypeScript):

```ts
interface AppError {
  name: string;              // class/type name, e.g. "PaymentError"
  code: string;              // stable machine code, e.g. "PAYMENT_CARD_DECLINED"
  category: ErrorCategory;   // e.g. "business" | "database" | "external"
  severity: Severity;        // "info" | "warning" | "error" | "critical"
  recoverable: boolean;      // can the caller continue/retry safely?
  retryable: boolean;        // explicit retry eligibility
  message: string;           // human-readable, never parsed by code
  details?: FieldError[];    // validation / field-level issues
  cause?: unknown;           // the original error, preserved
  metadata?: Record<string, unknown>; // SAFE, redacted context only
  correlationId?: string;    // ties the failure to a request/workflow
  timestamp: string;         // ISO-8601 creation time
}
```

The exact field set is yours, but every field must answer a question *some handler asks*. Fields
nobody reads are noise and a leakage risk.

## Why a single structure

| Property | One model | Ad-hoc shapes |
| -------- | --------- | ------------- |
| Routing | `switch (err.code)` | string matching per handler |
| Redaction | One allowlist | Audit every call site |
| Logging | Fixed schema | Unpredictable log lines |
| HTTP mapping | Table lookup | Scattered `if` chains |
| Onboarding | One doc | Tribal knowledge |

## Worked example

```ts
function toErrorObject(err: unknown): AppError {
  if (isAppError(err)) return err;
  return {
    name: "UnknownError",
    code: "INTERNAL_UNEXPECTED",
    category: "unexpected",
    severity: "error",
    recoverable: false,
    retryable: false,
    message: "An unexpected error occurred",
    cause: err,
    timestamp: new Date().toISOString(),
  };
}
```

One function guarantees that even an untranslated native error still becomes a well-formed record
before it reaches a boundary.

## Key data / numbers

- **RFC 9457 (Problem Details)** defines the *external* analogue: `type`, `title`, `status`,
  `detail`, `instance`. Your internal model is the source these are projected from (Chapter 20).
- **DOMException/`Error`** expose `name`, `message`, `stack`, and (modern JS) `cause` — the
  minimum a native error already provides.
- Common severity vocabularies: `debug`, `info`, `warning`, `error`, `critical`.
- Keep codes **≤ 64 chars** and metadata values **scalar or small arrays** so the object stays
  cheap to log and serialize.

## Real-world use case — Acme SaaS

Acme's early code returned `{ error: "failed" }` from every layer. When they added Stripe billing,
support could not tell a declined card from a network blip, so engineers grepped logs for
`"failed"` and found 40,000 hits. Introducing one error model, with `code`, `category`, and
`retryable`, let them split that string into `PAYMENT_CARD_DECLINED` (business, no retry) and
`PAYMENT_PROVIDER_TIMEOUT` (external, retry). Support tickets dropped because the UI could now
render an actionable message per code.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Full model on every error | Complete routing + diagnostics | Boilerplate to construct | Default for application code |
| Minimal `{ code, message }` | Cheap | No cause/context | Edge adapters, tiny scripts |
| Raw native errors | Zero effort | No stable code, no context | Never at a boundary |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Model errors as data with stable fields | Parse `err.message` in handlers |
| Keep the model language-agnostic | Couple it to one framework's exception class |
| Reserve fields no one reads | Add fields "just in case" |

## Common mistakes

- **Message-as-code.** Storing meaning only in prose; breaks on rewording and localization.
- **No category.** Handlers cannot distinguish business from infrastructure failures.
- **Losing context at creation.** By the time it reaches the boundary, the tenant ID is gone.
- **Leaking the mechanism.** Designing around `try/catch` instead of around the data shape.

## Checklist

- [ ] Does every error in your system conform to one shape?
- [ ] Can you route without reading `message`?
- [ ] Does the shape have a stable identity layer and a diagnostic layer?
- [ ] Is there a `toErrorObject()` funnel for untranslated natives?

## Related

- [Core Identity Fields](./02-core-identity-fields.md)
- [Cause, Context, and Correlation](./03-cause-context-and-correlation.md)
- [The Complete Error Object Spec](../03-practical-examples/01-error-object-spec.md)
