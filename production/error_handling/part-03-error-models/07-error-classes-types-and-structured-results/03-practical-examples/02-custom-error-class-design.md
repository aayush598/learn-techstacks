# Practical: Custom Error Class Design

> Part III · Chapter 7 · Sections 7.1–7.6, 7.14–7.17 · _Estimated reading time: 20 min_
> **Prerequisite:** [Hierarchies, Composition, and Naming](../01-concepts/05-hierarchies-composition-and-naming.md)

## In one sentence

This file is a **flat, two-level class set** — one base plus category classes built by composition —
that gives you precise `instanceof` checks and stable codes without a deep, brittle hierarchy.

## Why this matters in production

Custom classes are worth having when they carry behavior (chaining, formatting), when a category
check is useful (`instanceof ExternalError`), or when they make a layer's vocabulary explicit. The
mistake is letting them multiply into a tree. This design keeps the useful parts and removes the
tree.

## The base class

```ts
export type ErrorCategory =
  | "validation" | "auth"     | "business" | "payment"
  | "database"   | "external" | "resource" | "unexpected";

export type Severity = "info" | "warning" | "error" | "critical";

export interface AppErrorInit {
  code: string;
  category: ErrorCategory;
  message: string;
  severity?: Severity;
  recoverable?: boolean;
  retryable?: boolean;
  cause?: unknown;
  metadata?: Record<string, unknown>;
  correlationId?: string;
  operation?: string;
  details?: FieldError[];
}

export interface FieldError { field: string; code: string; message: string; meta?: Record<string, unknown> }

const DEFAULTS: Record<ErrorCategory, { severity: Severity; retryable: boolean; recoverable: boolean }> = {
  validation: { severity: "info",    retryable: false, recoverable: true  },
  auth:       { severity: "warning", retryable: false, recoverable: true  },
  business:   { severity: "info",    retryable: false, recoverable: true  },
  payment:    { severity: "warning", retryable: false, recoverable: true  },
  database:   { severity: "error",   retryable: true,  recoverable: true  },
  external:   { severity: "warning", retryable: true,  recoverable: true  },
  resource:   { severity: "warning", retryable: true,  recoverable: true  },
  unexpected: { severity: "error",   retryable: false, recoverable: false },
};

export class AppError extends Error {
  readonly code: string;
  readonly category: ErrorCategory;
  readonly severity: Severity;
  readonly retryable: boolean;
  readonly recoverable: boolean;
  readonly metadata: Readonly<Record<string, unknown>>;
  readonly details?: readonly FieldError[];
  readonly correlationId?: string;
  readonly operation?: string;
  readonly timestamp = new Date().toISOString();

  constructor(init: AppErrorInit) {
    super(init.message, init.cause !== undefined ? { cause: init.cause } : undefined);
    this.name = new.target.name;
    const d = DEFAULTS[init.category];
    this.code = init.code;
    this.category = init.category;
    this.severity = init.severity ?? d.severity;
    this.retryable = init.retryable ?? d.retryable;
    this.recoverable = init.recoverable ?? d.recoverable;
    this.metadata = Object.freeze(init.metadata ?? {});
    this.details = init.details ? Object.freeze(init.details) : undefined;
    this.correlationId = init.correlationId;
    this.operation = init.operation;
    Error.captureStackTrace?.(this, new.target);
  }
}
```

## The category classes (flat, one level)

Each category class fixes `category` and offers a narrow constructor. Note they **compose** the base
rather than deepening it with behavior.

```ts
export class ValidationError extends AppError {
  constructor(code: string, message: string, details: FieldError[], init?: Partial<AppErrorInit>) {
    super({ code, category: "validation", message, details, ...init });
  }
}

export class BusinessRuleError extends AppError {
  constructor(code: string, message: string, init?: Partial<AppErrorInit>) {
    super({ code, category: "business", message, ...init });
  }
}

export class PaymentError extends AppError {
  constructor(code: string, message: string, init?: Partial<AppErrorInit>) {
    super({ code, category: "payment", message, ...init });
  }
}

export class ExternalError extends AppError {
  constructor(code: string, message: string, init?: Partial<AppErrorInit>) {
    super({ code, category: "external", message, ...init });
  }
}

export class InfrastructureError extends AppError {
  constructor(code: string, message: string, init?: Partial<AppErrorInit>) {
    super({ code, category: "database", message, ...init });
  }
}
```

Five focused classes. No `BillingError extends PaymentError extends ...`.

## Domain vocabulary via named factories

Instead of a class per condition, use **factory functions** that fix code + category. This keeps the
class set small while making domain meaning readable.

```ts
export const CardDeclined = (declineCode: string) =>
  new PaymentError("PAYMENT_CARD_DECLINED", "Card was declined", {
    metadata: { declineCode },
  });

export const InsufficientFunds = (accountId: string) =>
  new BusinessRuleError("BILLING_INSUFFICIENT_FUNDS", `Account ${accountId} has insufficient funds`, {
    metadata: { accountId },
  });

export const EmailTaken = (email: string) =>
  new BusinessRuleError("USER_EMAIL_TAKEN", `Email ${email} is already registered`, {
    metadata: { email },
  });

export const ProviderTimeout = (provider: string, cause: unknown) =>
  new ExternalError("PAYMENT_PROVIDER_TIMEOUT", `Provider ${provider} timed out`, {
    cause, metadata: { provider },
  });
```

Callers write `throw CardDeclined("do_not_honor")` — readable, stable code, no class explosion.

## Narrowing and handling

```ts
function classify(e: unknown): AppError {
  if (e instanceof AppError) return e;
  if (e instanceof TypeError) {
    return new AppError({ code: "INTERNAL_TYPE_ERROR", category: "unexpected", message: e.message, cause: e });
  }
  return new AppError({
    code: "INTERNAL_UNEXPECTED", category: "unexpected",
    message: e instanceof Error ? e.message : "Unknown error", cause: e,
  });
}

function policy(e: AppError): "retry" | "conflict" | "client" | "escalate" {
  switch (e.category) {
    case "database":
    case "external":
    case "resource":   return e.retryable ? "retry" : "escalate";
    case "validation": return "client";
    case "business":
    case "payment":    return "conflict";
    case "auth":       return "client";
    case "unexpected": return "escalate";
  }
}
```

`policy` is exhaustive over the closed category set; the compiler flags a missing category.

## Layer boundaries in practice

```ts
// Infrastructure: wrap driver errors, keep SQLSTATE contained.
try {
  await db.query("INSERT INTO users ...");
} catch (native) {
  if (isUniqueViolation(native)) throw EmailTaken(email);
  throw new InfrastructureError("DB_QUERY_FAILED", "User insert failed", { cause: native });
}

// Domain service: throw business errors.
if (balance < amount) throw InsufficientFunds(account.id);

// Transport boundary: translate once.
try {
  const user = await createUser(body);
  return json(201, { id: user.id });
} catch (e) {
  return problemResponse(classify(e));
}
```

## Key data / numbers

- **Two levels max**: `AppError` → category class. Factories cover per-condition specifics.
- **PostgreSQL SQLSTATE**: `23505` unique_violation (→ `EMAIL_TAKEN`/conflict), `40001`
  serialization_failure (→ retry), `40P01` deadlock_detected (→ retry), `57014` query_canceled.
- **`Error.captureStackTrace`** (V8) hides internal frames for cleaner stacks.
- **`instanceof` is realm-bound** — at worker/HTTP boundaries, rehydrate and check `code`.

## Real-world use case — Acme SaaS

Acme had 40 error classes in a 5-level tree; `catch (ServiceError)` caught payments, users, and
exports alike, so all three took the same retry path. The rewrite collapsed them to five category
classes plus a dozen factory functions. Retry logic keyed on `category` + `retryable`, HTTP mapping
keyed on `code`, and the UI keyed on `code`. The class count dropped from 40 to 5 while precision
increased, and new conditions became a factory function plus a registry row — not a new node in a
tree.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Flat categories + factories | Precise, small, readable | Factories to maintain | Default |
| One class + codes | Simplest | No category `instanceof` | Tiny apps |
| Class per condition | "Explicit" | Explosion, maintenance | Rarely |
| Deep hierarchy | Feels organized | Over-broad catches, brittle | Avoid |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep ≤ 2 levels | Build `Domain→Billing→Invoice→Tax` |
| Use factories for domain conditions | Create a class per message |
| Fix category in the subclass | Pass category at every call site manually |
| Wrap infra errors at the adapter | Leak SQLSTATE to the domain |
| Depend on `code`/`category` for policy | Depend on `instanceof` depth |

## Common mistakes

- **Class explosion** — 40 types, no `instanceof` uses them.
- **Deep hierarchy** — a base catch grabs unrelated failures.
- **Ambiguous names** (`DataError`, `ServiceError`).
- **Category set ad hoc** — a new category per feature, breaking total functions.
- **`instanceof` across realms** silently false.

## Checklist

- [ ] Is the hierarchy flat (≤ 2 levels)?
- [ ] Are per-condition errors expressed as factories with stable codes?
- [ ] Does `category` come from the class, not the caller?
- [ ] Are infrastructure errors wrapped at the adapter?
- [ ] Is `policy()` exhaustive over categories?
- [ ] Are `instanceof` checks avoided across process boundaries?

## Related

- [Native vs Custom Exceptions](../01-concepts/01-native-vs-custom-exceptions.md)
- [Hierarchies, Composition, and Naming](../01-concepts/05-hierarchies-composition-and-naming.md)
- [Result Type and Union Errors in Practice](./01-result-type-and-union-errors.md)
