# Why Translate and Normalize

> Part VI · Chapter 16 · Sections 16.1–16.2 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 15 — Error Boundaries](../../15-error-boundaries/README.md)

## In one sentence

**Translation** changes an error's representation at a boundary; **normalization** reduces many
incompatible formats into one internal shape — together they let every downstream consumer make a
decision **without knowing which dialect the error came from**.

## Why this matters in production

Your system receives errors in at least six dialects: a Postgres driver, the OS (`errno`), a
framework, an HTTP client, a vendor SDK, and the language runtime. If those dialects reach your
domain, then every service, retry policy, and API handler must understand all six — and a seventh
whenever you add a provider. Translation is the seam that keeps that count at **one**. Get it wrong
and you either leak vendor identity to clients or flatten distinct failures into a blind
`SOMETHING_FAILED`.

## The two operations

```text
TRANSLATION   one representation ─────────────▶ another representation
              (psycopg2.UniqueViolation)        (DomainError EMAIL_ALREADY_USED)

NORMALIZATION many representations ──────────▶ one canonical shape
              (Stripe card_error, S3 AccessDenied, LLM 429,
               Node ECONNRESET, SQLSTATE 23505 …)
                              │
                              ▼
                        AppError { code, category, transient, httpStatus, cause }
```

- **Translation** answers: *"What does this specific error mean here?"*
- **Normalization** answers: *"How do all our errors look the same to consumers?"*

They compose: each boundary translates its dialect into the canonical model; the canonical model
is what gets normalized consistently across the codebase.

## 16.1 — Why translate

### 1. Decoupling

If the domain imports `psycopg2`, the domain depends on Postgres. Swapping the driver, adding a
read replica, or unit-testing without a DB all become rewrites. Translation keeps the domain
portable.

### 2. Stable contracts

A client must not break because you changed `pg` → `pgx` or Stripe → Adyen. Translation maps
volatile vendor details to **stable application codes** (Ch. 8).

### 3. Correct classification

A driver error does not tell you whether it is *transient*, *business*, or *operational* in your
sense. `SQLSTATE 40001` is transient; `23505` is a business conflict. Only translation can attach
the retry class and category your recovery logic needs.

### 4. Security

Raw errors routinely carry SQL, hostnames, paths, and secrets. Translation produces a **safe
representation** (stable code + curated message) while preserving the raw error as `cause` for logs.

### 5. A single decision surface

Downstream code (`if err.transient`, `switch err.code`) works uniformly only if every error was
normalized. This is what makes retry, HTTP mapping, and logging policy trivial.

## 16.2 — Normalizing formats

Normalization means defining **one internal error shape** (Part III) and forcing every input
dialect into it. A minimal canonical model:

```ts
interface AppError {
  code: string;            // stable, machine-readable (e.g. EMAIL_ALREADY_USED)
  category: Category;      // VALIDATION | AUTH | CONFLICT | DEPENDENCY | INTERNAL | ...
  transient: boolean;      // retry signal (classification, not optimism)
  httpStatus: number;      // transport mapping (may be omitted for non-HTTP paths)
  safeMessage: string;     // curated, user-safe
  cause?: unknown;         // ORIGINAL error; server-side only, never serialized outward
  meta: Record<string, unknown>; // allowlisted context (requestId, tenantId, ...)
}
```

Normalization has three jobs:

| Job | Before | After |
| --- | ------ | ----- |
| **Shape unification** | Six different classes/objects | One `AppError` type |
| **Field normalization** | `code` vs `errno` vs `sqlstate` vs `type` | One `code` field |
| **Classification** | Implicit in the vendor | Explicit `category` + `transient` |

### A normalization function per boundary

```python
from enum import Enum

class Category(str, Enum):
    VALIDATION = "VALIDATION"
    CONFLICT = "CONFLICT"
    AUTH = "AUTH"
    DEPENDENCY = "DEPENDENCY"
    INTERNAL = "INTERNAL"

def normalize(err: Exception) -> AppError:
    # Each branch maps a specific dialect into the canonical shape.
    state = getattr(err, "pgcode", None)
    if state == "23505":
        return AppError(code="ALREADY_EXISTS", category=Category.CONFLICT,
                        transient=False, safe_message="That value already exists.", cause=err)
    if state in ("40001", "40P01"):
        return AppError(code="RETRYABLE_CONFLICT", category=Category.DEPENDENCY,
                        transient=True, safe_message="Temporary conflict, retry.", cause=err)
    if isinstance(err, TimeoutError):
        return AppError(code="TIMEOUT", category=Category.DEPENDENCY,
                        transient=True, safe_message="The operation timed out.", cause=err)
    if isinstance(err, DomainError):
        return err  # already normalized
    return AppError(code="INTERNAL_ERROR", category=Category.INTERNAL,
                    transient=False, safe_message="An unexpected error occurred.", cause=err)
```

Any consumer — retry engine, HTTP mapper, logger — now reads `err.code`, `err.transient`,
`err.category` and never inspects the concrete class.

## The cost of skipping translation

| Symptom | Root cause |
| ------- | ---------- |
| `if (err.code === "card_declined" \|\| err.sqlState === "23505" ...)` everywhere | No normalization |
| `DB_ERROR` for every database problem | Over-collapsed translation |
| Client breaks when provider changes | Vendor coupling |
| Transient errors returned as `500` | Lost retry class |
| SQL/hostnames in API responses | Translation skipped at a boundary |

## Key data / numbers

- Canonical fields to normalize: `code`, `category`, `transient`, `httpStatus`, `safeMessage`,
  `cause`, `meta`.
- Input dialects to normalize: `SQLSTATE` (Postgres), `errno`/`err.code` (OS), HTTP status, gRPC
  status, vendor `type` (Stripe), service `Code` (AWS), framework exception class.
- `transient` doubles as the retry eligibility signal (Ch. 27) — a boolean you must set correctly.

## Real-world use case — WebhookIngest

`WebhookIngest` receives events from Stripe, and processes them through adapters that also talk to
S3 and an LLM. Before normalization, three different error shapes propagated: Stripe's `type`, S3's
`Code`, and OpenAI's error `code`. Retry logic had a `switch` over all three. After defining one
`AppError`, each adapter normalizes at its edge; the retry engine checks `err.transient`. Adding a
second payment provider later required **only a new adapter**, not touching retry, HTTP, or logging.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Define one canonical error shape | Let each subsystem invent its own |
| Translate at each boundary | Translate at the consumer (too late) |
| Normalize `transient` explicitly | Infer retryability from the message |
| Preserve the original as `cause` | Discard the original error |
| Keep vendor dialects in adapters | Let vendor strings into the domain |

## Common mistakes

- **Normalizing too late.** By the time logging sees the error, the dialect is already everywhere.
- **Normalizing the message only.** The shape stays inconsistent; consumers still branch on class.
- **One giant `normalize()` at the top.** Loses the boundary's local knowledge of what the error means.
- **Forgetting `transient`.** The most expensive omission — retries silently disabled.

## Checklist

- [ ] The codebase defines exactly one canonical error type.
- [ ] Each boundary translates its input dialect into it.
- [ ] `code`, `category`, and `transient` are always populated.
- [ ] The original error is preserved as `cause`.
- [ ] Downstream code never `switch`es on vendor formats or exception classes.

## Related

- [Translation Directions](./02-translation-directions.md)
- [Preserving Cause and Recoverability](./03-preserving-cause-and-recoverability.md)
- [Part III — Designing the Application's Error Model](../../../part-03-error-models/06-designing-the-applications-error-model/README.md)
