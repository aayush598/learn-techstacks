# Core Identity Fields

> Part III · Chapter 6 · Sections 6.3–6.7 · _Estimated reading time: 20 min_
> **Prerequisite:** [What an Error Object Represents](./01-what-an-error-object-represents.md)

## In one sentence

The identity layer — **`name`, `code`, `message`, `category`, `severity`, `recoverable`** — is the
part of the error every handler branches on, so it must be stable, typed, and never derived from
prose.

## Why this matters in production

Misidentify a failure and every downstream decision is wrong: a `500` for a validation problem, a
retry of a permanent error, an on-call page for a declined card. The identity fields are how an
error announces *what it is*. Get them right and routing becomes a lookup; get them wrong and the
whole model collapses into string matching.

## name and code (6.3)

These are deliberately **two fields** because they serve different consumers.

| Field | Audience | Stability | Example |
| ----- | -------- | --------- | ------- |
| `name` | Developers, stack traces, debugging | Medium | `PaymentError` |
| `code` | Machines, registries, clients | **High** | `PAYMENT_CARD_DECLINED` |

`name` is the class or logical type — it tells a human reading a stack trace what kind of thing
went wrong. `code` is the contract — it never changes, and clients, retry policies, and HTTP
mappings key off it (Chapter 8).

```ts
class PaymentError extends AppError {
  readonly name = "PaymentError";
  constructor(code: PaymentCode, message: string, opts?: ErrorOptions) {
    super({ code, message, category: "payment", ...opts });
  }
}
```

> ⚠️ **Hazard.** Do not reuse `name` as the code. Class names get renamed during refactors; codes
> must not. Renaming a class is a code change; renaming a code is a **contract break**.

## Human-readable message (6.4)

`message` is for **humans reading logs**, not machines and not users. It should answer "what
happened, concisely" for an engineer.

Rules:

- **One line, no trailing punctuation.** Log runners reformat; keep it clean.
- **Include the failing subject, not secrets.** `"Order ord_123 failed capture"` ✅;
  `"Card 4242...4242 failed"` ❌.
- **Never parsed by code.** If you find yourself `includes()`-ing a message, you need a code.
- **Do not make it the user message.** A separate mapping produces user text (Chapter 8, §8.14).

```ts
throw new PaymentError("PAYMENT_CARD_DECLINED", "Stripe declined capture for order ord_123");
```

## The machine-readable identifier (6.5)

`code` is the single most important field in the model. It is:

- **Stable** — append-only across versions.
- **Unique** — one meaning per code, globally or per domain (Chapter 8).
- **Opaque to users in wording, meaningful to systems** — `PAYMENT_CARD_DECLINED`, not "Error 47".
- **The pivot for every mapping** — HTTP, retry, client action, user message.

```text
code ──┬──▶ HTTP status      (500? 422? 402?)
       ├──▶ retry policy      (transient? permanent?)
       ├──▶ client action     (retry / re-auth / show field error / contact support)
       └──▶ user message      (localized, safe)
```

## category / subcategory (6.6)

Category is a **coarse routing bucket** aligned with your taxonomy (Part II). It groups codes so
cross-cutting policy can be applied without enumerating every code.

```ts
type ErrorCategory =
  | "validation"     // bad input, field errors
  | "auth"           // authentication / authorization
  | "business"       // domain rule violated (not a bug)
  | "payment"        // billing / provider outcomes
  | "database"       // persistence
  | "external"       // third-party / network
  | "resource"       // exhaustion, quota, rate limit
  | "unexpected";    // programming / unknown
```

Subcategory refines without multiplying top-level buckets, e.g. `category: "database"`,
`subcategory: "constraint"`. Categories drive **policy**; codes drive **precision**. Keep the
category set small (8–12) and closed.

## severity and recoverability metadata (6.7)

These are the two fields that most often get conflated with category, but they answer different
questions.

| Field | Question | Values | Drives |
| ----- | -------- | ------ | ------ |
| `severity` | How alarming is this? | `info` / `warning` / `error` / `critical` | Log level, alerting |
| `recoverable` | Can we continue safely? | `true` / `false` | Whether to abort/compensate |
| `retryable` | Will retry plausibly help? | `true` / `false` | Retry policy (Chapter 27) |

A **business** error (declined card) is high-severity-*for-the-user*, but `severity: "info"` for
operations and `retryable: false`. A **database deadlock** is transient: `severity: "warning"`,
`recoverable: true`, `retryable: true`. Getting this wrong means either paging humans for normal
business or silently retrying the unretryable.

```ts
const CATEGORY_DEFAULTS: Record<ErrorCategory, Pick<AppError, "severity" | "retryable" | "recoverable">> = {
  validation: { severity: "info",    retryable: false, recoverable: true  },
  auth:       { severity: "warning", retryable: false, recoverable: true  },
  business:   { severity: "info",    retryable: false, recoverable: true  },
  payment:    { severity: "warning", retryable: false, recoverable: true  },
  database:   { severity: "error",   retryable: true,  recoverable: true  },
  external:   { severity: "warning", retryable: true,  recoverable: true  },
  resource:   { severity: "warning", retryable: true,  recoverable: true  },
  unexpected: { severity: "error",   retryable: false, recoverable: false },
};
```

Defaults come from the category; a specific code may override (e.g. `DB_SERIALIZATION_FAILURE`
is retryable even though it is a `database` code, which is already `true`; `PAYMENT_PROVIDER_
CONFIG_INVALID` is `unexpected`-like but categorized `payment`).

## Worked example

```ts
// A validation failure that must NOT page anyone and must NOT be retried.
const err: AppError = {
  name: "ValidationError",
  code: "VALIDATION_REQUIRED_FIELD",
  category: "validation",
  severity: "info",
  recoverable: true,
  retryable: false,
  message: "Missing required field 'email' on create-user request",
  details: [{ field: "email", code: "REQUIRED", message: "email is required" }],
  timestamp: new Date().toISOString(),
};
```

Category = `validation` → HTTP 422, no alert, no retry, field-level UI. Every one of those
decisions came from the identity layer alone.

## Key data / numbers

- **HTTP status families** are a coarse projection of category: `validation`→`400`/`422`,
  `auth`→`401`/`403`, `business`→`409`/`402`, `external`/`database`→`502`/`503`, `unexpected`→`500`
  (Chapter 19).
- **`Retry-After`** belongs on `retryable: true` resource errors returning `429`/`503`.
- Keep the closed `ErrorCategory` set to **8–12** members; each new member needs a policy, not just
  a label.

## Real-world use case — ExportJob

Acme's `ExportJob` worker was marking jobs failed and alerting on-call for `EXPORT_NO_ROWS`
(an empty result, a normal outcome). The fix was identity metadata: `EXPORT_NO_ROWS` is
`category: "business"`, `severity: "info"`, `retryable: false`. It now completes the job with
status `empty` and never pages. Meanwhile `EXPORT_STORAGE_TIMEOUT` is `category: "external"`,
`severity: "warning"`, `retryable: true` — so it retries with backoff. Same worker, two policies,
both decided by identity fields.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Category-derived defaults | Fewer fields to set, consistent | Overrides can drift | Default everywhere |
| Per-code explicit metadata | Max precision | Repetition, drift risk | When defaults are wrong for a code |
| Message-only identity | None | Unroutable | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep `code` stable and append-only | Encode meaning only in `message` |
| Derive severity/retryable from category + override | Copy-paste the same metadata per throw |
| Use a small closed category set | Invent a new category per feature |
| Keep messages secret-free and single-line | Put PII or tokens in `message` |

## Common mistakes

- **Code equals message.** `code: "Payment failed"` — not stable, not machine-readable.
- **Retryable by optimism.** Marking business errors retryable "just in case".
- **Severity as a synonym for category.** They answer different questions.
- **Unbounded categories.** Twenty categories with overlapping meanings defeat routing.

## Checklist

- [ ] Does every error have a stable `code`, distinct from `name`?
- [ ] Is `message` free of secrets and never parsed?
- [ ] Is the category set closed and small?
- [ ] Are `severity`, `recoverable`, `retryable` set, ideally from category defaults?
- [ ] Does no business error page on-call?

## Related

- [What an Error Object Represents](./01-what-an-error-object-represents.md)
- [Cause, Context, and Correlation](./03-cause-context-and-correlation.md)
- [Chapter 8 — Error Codes and Error Registries](../../08-error-codes-and-error-registries/README.md)
