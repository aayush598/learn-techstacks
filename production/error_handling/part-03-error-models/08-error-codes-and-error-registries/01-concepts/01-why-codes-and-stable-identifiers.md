# Why Codes, and What Makes Them Stable

> Part III · Chapter 8 · Sections 8.1–8.2, 8.17 · _Estimated reading time: 16 min_
> **Prerequisite:** [Core Identity Fields](../../06-designing-the-applications-error-model/01-concepts/02-core-identity-fields.md)

## In one sentence

An **error code** is a short, stable, machine-readable identifier for one condition — the thing
clients, handlers, and dashboards branch on — and its value is that it **does not change** even
when classes, messages, or implementation details do.

## Why this matters in production

Consider the alternative: a client that shows a specific message when `res.error.message ===
"Card was declined"`. The day a copy editor changes the wording, the client breaks. Multiply that
by every handler, dashboard, and retry rule keyed on prose or on an implementation detail, and you
get a system where a refactor silently changes behavior. Codes remove that coupling: change the
wording, refactor the class, swap the provider — the code stays, and everything keeps working.

## Why codes (8.1)

| Consumer | Uses the code to… |
| -------- | ----------------- |
| API boundary | Map to HTTP status |
| Retry engine | Decide retryable vs permanent |
| Frontend | Choose message + UI action |
| Support tooling | Group incidents, find runbooks |
| Analytics | Count failures by type |
| Tests | Assert specific conditions |

A code answers "**which condition is this?**" separate from "what is it called?" and "what
happened?". It is the join key across all systems.

## What makes a code stable (8.2)

A stable code satisfies five properties:

1. **Fixed string.** Once assigned, never renamed.
2. **Single meaning.** One condition, forever (see 8.17 below).
3. **Append-only.** New conditions get new codes; old codes are deprecated, not reused.
4. **Environment-independent.** Same code in prod, staging, and tests.
5. **Version-independent.** Same code before and after refactors/migrations.

```text
GOOD                            BAD
PAYMENT_CARD_DECLINED           "Card declined"           ← a message
DB_UNIQUE_VIOLATION             "23505"                   ← implementation detail
VALIDATION_REQUIRED_FIELD       "ValidationError:line42"  ← ephemeral noise
EXPORT_UPLOAD_FAILED            err_{tenant}_{timestamp}  ← per-occurrence
```

## Codes vs adjacent identifiers

Do not confuse a code with other identifiers in the model.

| Identifier | Scope | Example | Lifetime |
| ---------- | ----- | ------- | -------- |
| **Error code** | A condition | `PAYMENT_CARD_DECLINED` | Permanent contract |
| Correlation ID | One operation | `01HQ8Z...` | One request |
| Event ID | One event | `evt_1Nx...` | One event |
| HTTP status | Transport class | `402` | Per response (mapped) |
| Message | Human text | "Card was declined" | Until edited |

Only the code is a long-lived contract.

## Avoiding implementation-derived codes (8.17)

The most common stability failure is deriving a code from an implementation detail. When the
implementation changes — a provider swap, a library upgrade, a schema rename — the code changes
too, and every consumer breaks.

| ❌ Implementation-derived | ✅ Behavior-derived |
| ------------------------- | ------------------- |
| `PG_23505` | `DB_UNIQUE_VIOLATION` |
| `STRIPE_CARD_DECLINED` | `PAYMENT_CARD_DECLINED` |
| `ECONNRESET` | `EXTERNAL_CONNECTION_RESET` |
| `HTTP_429_FROM_VENDOR_X` | `RATE_LIMIT_EXCEEDED` |
| `NULL_POINTER_AT_LINE_88` | `INTERNAL_UNEXPECTED` |

Rules:

- **Name the behavior, not the mechanism.** The mechanism belongs in `cause`/metadata.
- **Vendor codes go in metadata**, not in your code string. Map `card_declined` →
  `PAYMENT_CARD_DECLINED` and keep the vendor's word as `metadata.providerCode`.
- **Never encode line numbers, file names, SQL states, or HTTP status** in the code itself.

```ts
// The vendor's raw code is preserved as context; our code is stable.
throw new PaymentError("PAYMENT_CARD_DECLINED", "Card declined", {
  metadata: { provider: "stripe", providerCode: "card_declined", declineCode: "do_not_honor" },
});
```

## Worked example

```ts
// Round 1: implementation-derived (fragile)
throw new AppError({ code: "PG_23505", category: "database", message: "duplicate key" });

// Round 2: provider-coupled (fragile)
throw new AppError({ code: "STRIPE_DUPLICATE", category: "payment", message: "duplicate" });

// Round 3: behavior-derived (stable)
export const EmailTaken = (email: string) =>
  new AppError({
    code: "USER_EMAIL_TAKEN",          // meaning of the condition
    category: "business",
    message: `Email ${email} is already registered`,
    metadata: { email },               // detail lives in metadata
  });
```

A future move from Postgres to another store, or from Stripe to another PSP, changes metadata and
adapter code — not a single consumer's switch statement.

## Key data / numbers

- **Length:** keep codes ≤ 64 chars; common style is `SCREAMING_SNAKE_CASE` with 2–5 segments
  (e.g. `PAYMENT_CARD_DECLINED`).
- **PostgreSQL SQLSTATE** codes (`23505`, `40001`) are implementation-derived — always translate.
- **Stripe decline codes** (`card_declined`, `insufficient_funds`) are provider-specific — map to
  your own `PAYMENT_*` codes.
- **gRPC status codes** are a stable, small enum (e.g. `DEADLINE_EXCEEDED`, `UNAVAILABLE`) — a good
  model for behavior-derived naming.

## Real-world use case — Acme SaaS

Acme originally used raw vendor codes (`stripe_card_declined`, `pg_23505`) as their error codes.
When they added a second payment provider, every handler broke because it keyed on the Stripe code.
They migrated to behavior-derived codes (`PAYMENT_CARD_DECLINED`, `DB_UNIQUE_VIOLATION`) and pushed
vendor specifics into metadata. The second provider integration required touching only the adapter;
the frontend, retry engine, and analytics — all keyed on stable codes — did not change at all.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Behavior-derived codes | Stable, provider-agnostic | Requires mapping layer | Always for app codes |
| Vendor codes as codes | Zero mapping | Coupled, breaks on swap | Never (store in metadata) |
| Implementation codes (SQLSTATE) | No translation | Leaks internals, unstable | Never (translate at adapter) |
| Free-form messages | Fast | Unroutable | Never as the contract |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name the behavior, not the mechanism | Encode `23505`/`ECONNRESET` in the code |
| Keep vendor codes in metadata | Use the vendor's code as your code |
| Treat codes as append-only contracts | Rename/reuse codes |
| Keep codes short and uppercase | Generate per-occurrence codes |
| Make codes environment-independent | Branch behavior on the environment |

## Common mistakes

- **Provider-coupled codes** that break on a vendor swap.
- **SQLSTATE/vendor codes** leaking into the contract.
- **Per-occurrence codes** (`ERR_1738...`) that group nothing.
- **Renamed codes** that silently break consumers.
- **Messages used as codes**, so wording changes are breaking changes.

## Checklist

- [ ] Are codes behavior-derived, not implementation-derived?
- [ ] Are vendor-specific codes kept in metadata?
- [ ] Are codes append-only and environment-independent?
- [ ] Is each code short, uppercase, and readable?
- [ ] Does every consumer branch on codes, not messages?

## Related

- [Code Naming and Scoping](./02-code-naming-and-scoping.md)
- [Uniqueness and Registry Structure](./03-uniqueness-and-registry-structure.md)
- [The Sample Error Registry](../03-practical-examples/01-sample-error-registry.md)
