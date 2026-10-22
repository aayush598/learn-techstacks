# Model Invariants — Properties Every Error Must Hold

> Part III · Chapter 6 · Section 6.19 · _Estimated reading time: 18 min_
> **Prerequisite:** [Immutability, Serialization, and Safety](../01-concepts/05-immutability-serialization-and-safety.md)

## In one sentence

A **model invariant** is a property that must be true of *every* error object the moment it is
constructed — non-empty code, known category, safe metadata, bounded chain — and it must be
enforced by the constructor, not hoped for by reviewers.

## Why this matters in production

Invariants are what make the model *reliable at scale*. When every error is guaranteed to have a
code, a small closed category, and safe metadata, downstream code can assume those facts instead of
defensively checking. Without them, you get the classic failure: the one error path that skipped
the constructor and returned `{ message: undefined }`, which then crashed the global handler during
an outage — the worst time to discover a broken error path.

## The invariant set

| # | Invariant | Why it exists | Enforced by |
| - | --------- | ------------- | ----------- |
| 1 | `code` is a non-empty string from the registry | Every routing decision keys on it | Constructor + registry lookup |
| 2 | `category` ∈ closed set | Policy grouping must be total | Type + runtime check |
| 3 | `message` is non-empty, single line, secret-free | Logs and humans must read it | Constructor sanitizer |
| 4 | `severity`, `retryable`, `recoverable` are set | Policy needs them | Category defaults + override |
| 5 | `metadata` keys are allowlisted and values scalar | Safe, indexable logs | Allowlist check |
| 6 | `cause` is preserved and chain depth ≤ N | Debuggability, memory bound | Wrap helper |
| 7 | `timestamp` is valid ISO-8601 UTC | Ordering and correlation | Constructor |
| 8 | Object is frozen (immutable) | Concurrency safety | `Object.freeze` |
| 9 | Object is cycle-free | Serializable | Store IDs, not objects |
| 10 | `details`, if present, have `field` + `code` | Client mapping | Validator |

## Where enforcement lives

Invariants must be enforced at the **single choke point** through which all errors pass. If there
are three ways to create an error, there are three places an invariant can be skipped.

```ts
const CATEGORIES = new Set<ErrorCategory>([
  "validation", "auth", "business", "payment",
  "database", "external", "resource", "unexpected",
]);

interface AppErrorInit {
  code: string;
  message: string;
  category: ErrorCategory;
  severity?: Severity;
  recoverable?: boolean;
  retryable?: boolean;
  details?: FieldError[];
  cause?: unknown;
  metadata?: Record<string, unknown>;
  correlationId?: string;
  operation?: string;
}

class AppError extends Error {
  readonly code!: string;
  readonly category!: ErrorCategory;
  readonly severity!: Severity;
  readonly recoverable!: boolean;
  readonly retryable!: boolean;
  readonly details?: readonly FieldError[];
  readonly metadata!: Readonly<Record<string, unknown>>;
  readonly correlationId?: string;
  readonly operation?: string;
  readonly timestamp: string;

  constructor(init: AppErrorInit) {
    // Invariant 1 + 2
    if (!init.code || typeof init.code !== "string") {
      throw new Error("AppError: code must be a non-empty string");
    }
    if (!CATEGORIES.has(init.category)) {
      throw new Error(`AppError: unknown category '${init.category}'`);
    }
    // Invariant 3
    const message = sanitizeMessage(init.message);
    super(message, init.cause !== undefined ? { cause: init.cause } : undefined);
    this.name = new.target.name;

    // Invariant 4 — defaults from category, explicit overrides win
    const defaults = CATEGORY_DEFAULTS[init.category];
    this.severity = init.severity ?? defaults.severity;
    this.recoverable = init.recoverable ?? defaults.recoverable;
    this.retryable = init.retryable ?? defaults.retryable;

    // Invariant 5
    this.metadata = Object.freeze(assertSafeMetadata(init.metadata ?? {}));

    // Invariant 10
    this.details = init.details ? Object.freeze(validateDetails(init.details)) : undefined;

    this.correlationId = init.correlationId;
    this.operation = init.operation;

    // Invariant 7
    this.timestamp = new Date().toISOString();

    // Invariant 8
    Object.freeze(this);
  }
}
```

All creation paths (native wrap, translation, domain throw, job failure) route through this
constructor or a small factory that calls it.

## Invariant 6 in detail — bounded, preserved chains

```ts
const MAX_CHAIN = 20;

function chainDepth(err: unknown): number {
  let depth = 0;
  const seen = new WeakSet<object>();
  for (let e: unknown = err; e && typeof e === "object"; ) {
    if (seen.has(e as object)) return MAX_CHAIN + 1; // cycle
    seen.add(e as object);
    depth++;
    e = (e as { cause?: unknown }).cause;
  }
  return depth;
}

function wrap(code: string, message: string, cause: unknown, init: Partial<AppErrorInit>) {
  if (chainDepth(cause) >= MAX_CHAIN) {
    // Stop growing; log the rest out-of-band, keep the model bounded.
    return new AppError({ code, message, category: "unexpected", ...init });
  }
  return new AppError({ code, message, cause, category: "unexpected", ...init });
}
```

## Invariant 2 in detail — total category functions

A category set is only useful if every policy function is **total** over it. If you add a category,
every `switch` without a `default` becomes a compile error (in TypeScript with exhaustiveness
checks) — which is exactly what you want.

```ts
function defaultHttpStatus(category: ErrorCategory): number {
  switch (category) {
    case "validation": return 422;
    case "auth":       return 403;
    case "business":   return 409;
    case "payment":    return 402;
    case "database":   return 503;
    case "external":   return 502;
    case "resource":   return 429;
    case "unexpected": return 500;
    default: {
      const _exhaustive: never = category; // forces update when a category is added
      return _exhaustive;
    }
  }
}
```

## Invariant 3 in detail — message hygiene

```ts
function sanitizeMessage(message: string): string {
  if (!message || !message.trim()) return "An error occurred"; // never empty
  const singleLine = message.replace(/\s+/g, " ").trim();      // single line
  return redactSensitive(singleLine);                          // secret-free
}
```

## Worked example — invariant test

Invariants are testable. This is the real prize: you can assert the model holds across *every*
error path.

```ts
import { describe, it, expect } from "vitest";

const CASES = [
  new AppError({ code: "PAYMENT_CARD_DECLINED", message: "declined", category: "payment" }),
  new AppError({ code: "DB_DEADLOCK", message: "deadlock", category: "database" }),
  toErrorObject(new TypeError("boom")),
];

describe("AppError invariants", () => {
  it.each(CASES)("holds for %o", (err) => {
    expect(err.code).toBeTruthy();
    expect(CATEGORIES.has(err.category)).toBe(true);
    expect(err.message).not.toMatch(/\n/);
    expect(Object.isFrozen(err)).toBe(true);
    expect(() => JSON.stringify(err)).not.toThrow();
  });
});
```

## Key data / numbers

- **Chain depth cap:** 10–20 links (20 is a common default; Node's default `cause` has no cap).
- **Metadata value limits:** scalars or small arrays; total payload ≤ 8 KB.
- **Message length:** cap at ~2 KB to avoid log truncation but keep the code field always present.
- **Category count:** 8–12; every addition requires updating all total functions.

## Real-world use case — Checkout

Acme's `Checkout` once threw a hand-rolled `{ error: "capture_failed", retry: true }` literal that
bypassed the model. During a Stripe outage, the global handler tried to read `.code` on it,
received `undefined`, and mapped everything to `500` with no correlation ID. The retry flag was
also ignored, so transient failures were never retried. After routing every throw through the
invariant-enforcing constructor — with a test asserting the invariants on every error factory in
the codebase — that class of bug disappeared, and a single CI check caught future bypasses.

## Trade-offs

| Enforcement | Pros | Cons |
| ----------- | ---- | ---- |
| Constructor throws on violation | Fails loudly in dev, impossible to bypass | Must ensure no throw during error handling |
| Constructor silently coerces | Never breaks the error path | Hides bugs, weakens guarantees |
| Lint/type-only | Cheap | Runtime data (JS) still violates |
| Test-only | Catches regressions | Does not prevent production violation |

> ⚠️ **Hazard.** A constructor that *throws* on invalid input can itself fail while handling a
> failure (Chapter 58, §58.1). In production, prefer **coercing to safe defaults** for
> non-critical invariants and **asserting in development/tests** for the rest. The one invariant
> that must never fail is "produce a usable error."

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Enforce invariants at one choke point | Rely on reviewer discipline |
| Test invariants across every factory | Test only the happy-path error |
| Coerce safely in prod, assert in dev | Let a broken invariant crash the handler |
| Keep category set closed and total | Allow ad-hoc categories |

## Common mistakes

- **Multiple creation paths** that each re-implement (or forget) validation.
- **Throwing from the error constructor** in production and breaking the error path.
- **Non-total category switches** silently returning `undefined`.
- **No invariant test**, so a refactor reintroduces bypasses.

## Checklist

- [ ] Is there exactly one way to construct an `AppError`?
- [ ] Are all ten invariants enforced or asserted there?
- [ ] Is chain depth bounded and cycle-safe?
- [ ] Are category policy functions total (exhaustive)?
- [ ] Is there a test asserting invariants over every error factory?

## Related

- [Immutability, Serialization, and Safety](../01-concepts/05-immutability-serialization-and-safety.md)
- [Versioning the Internal Contract](./02-versioning-the-internal-contract.md)
- [The Complete Error Object Spec](../03-practical-examples/01-error-object-spec.md)
