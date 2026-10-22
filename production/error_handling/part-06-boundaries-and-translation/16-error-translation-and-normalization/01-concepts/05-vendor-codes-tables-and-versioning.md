# Vendor Codes, Translation Tables, and Versioning

> Part VI · Chapter 16 · Sections 16.15–16.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Avoiding Overgeneralization and Handling Unknowns](./04-avoiding-overgeneralization-and-unknowns.md)

## In one sentence

**Vendor codes** are volatile and must map to **stable application codes**; a **translation table**
is the data structure that records those mappings; **circular chains** must be prevented; and the
whole mapping needs **versioning rules** so changes never break consumers.

## Why this matters in production

A codebase that maps vendor codes inline, ad hoc, becomes impossible to audit: nobody can answer
"which application code does an S3 `SlowDown` produce?" A table makes the mapping reviewable,
testable, and replaceable. Versioning rules make adding a new vendor or deprecating a code a
non-event instead of a breaking change.

## 16.15 — Vendor → stable codes

The rule: **consumers see stable internal codes; vendor codes exist only inside the adapter.**

```text
Stripe "card_declined"            ─┐
Adyen  "Refused"                   ├─▶ PAYMENT_CARD_DECLINED   (stable)
Braintree "2000 Do Not Honor"     ─┘
```

| Property | Vendor code | Stable app code |
| -------- | ----------- | --------------- |
| Stability | Changes with provider | Yours to define and version |
| Audience | Adapter only | Domain, API, clients, retry |
| Example | `card_declined`, `SlowDown`, `context_length_exceeded` | `PAYMENT_CARD_DECLINED`, `STORAGE_THROTTLED`, `TOKEN_LIMIT_EXCEEDED` |

Stable codes follow the naming conventions of Ch. 8 (domain-prefixed, machine-readable,
`SCREAMING_SNAKE_CASE`). The mapping from vendor → stable is what enables **provider replacement**
without touching downstream code (Ch. 25.20).

## 16.16 — Translation tables and policies

A translation table is a **declarative mapping** from source error signatures to a target error
spec. It beats a `switch` because it is inspectable, testable, and user-extensible.

### Shape of a table entry

```ts
interface Rule {
  match: { source: "postgres" | "stripe" | "s3" | "openai"; code?: string; http?: number; codeClass?: string };
  to: {
    code: string;
    category: Category;
    transient: boolean;
    httpStatus?: number;
    safeMessage: string;
    withDetails?: (src: any) => Record<string, unknown>; // derive safe details
  };
}
```

### A worked table

```ts
const RULES: Rule[] = [
  { match: { source: "postgres", code: "23505" },
    to: { code: "ALREADY_EXISTS", category: "CONFLICT", transient: false, httpStatus: 409,
          safeMessage: "That value already exists.",
          withDetails: (e) => ({ field: fieldFromConstraint(e.constraint) }) } },
  { match: { source: "postgres", code: "40001" },
    to: { code: "RETRYABLE_CONFLICT", category: "DEPENDENCY", transient: true, httpStatus: 409,
          safeMessage: "A concurrent update occurred; retry." } },
  { match: { source: "stripe", code: "card_declined" },
    to: { code: "PAYMENT_CARD_DECLINED", category: "BUSINESS", transient: false, httpStatus: 402,
          safeMessage: "Your card was declined." } },
  { match: { source: "s3", code: "SlowDown" },
    to: { code: "STORAGE_THROTTLED", category: "DEPENDENCY", transient: true, httpStatus: 503,
          safeMessage: "Storage is temporarily throttled." } },
  { match: { source: "openai", code: "context_length_exceeded" },
    to: { code: "TOKEN_LIMIT_EXCEEDED", category: "BUSINESS", transient: false, httpStatus: 422,
          safeMessage: "The request exceeded the model's context window." } },
];

function translate(source: SourceKind, err: any): AppError {
  const rule = RULES.find((r) => r.match.source === source && r.match.code === err?.code);
  if (!rule) return unknown(source, err);   // 16.14
  return {
    code: rule.to.code,
    category: rule.to.category,
    transient: rule.to.transient,
    httpStatus: rule.to.httpStatus,
    safeMessage: rule.to.safeMessage,
    details: rule.to.withDetails?.(err) ?? {},
    cause: err,                             // preserved
  };
}
```

### Policy hooks

A table entry can also declare policy: retry eligibility (`transient`), whether to **alert** (e.g.
`SCHEMA_ERROR`), whether to **degrade** (optional dependency), and **redaction** rules. Keep policy
in the table so it is co-located with the mapping — this is the "translation policy" in one place.

### Testing a table

Every table entry is a unit test: feed the vendor signature, assert `code`, `category`,
`transient`, and `httpStatus`. A **coverage test** should assert that every known vendor code is
mapped (no accidental fall-through to `unknown`). This catches upstream changes at test time.

## 16.17 — Preventing circular chains

A circular cause chain is when an error's `cause` (transitively) points back to itself. It causes
infinite loops in `toString()`, stack rendering, and serializers that walk `cause`.

Common causes:

- A translation function that wraps an already-translated error **again**.
- Identity-preserving wraps: `err.cause = err` (a bug in a generic `wrap()`).
- A retry loop that re-wraps the previous attempt's error, chaining attempts into itself.

### Detection

```ts
function hasCycle(err: unknown): boolean {
  const seen = new Set<unknown>();
  let cur: any = err;
  while (cur && typeof cur === "object") {
    if (seen.has(cur)) return true;
    seen.add(cur);
    cur = cur.cause ?? cur.__cause__;
  }
  return false;
}
```

### Prevention rules

1. **Do not wrap an error that is already normalized.** Check `instanceof AppError` first.
2. **Never set `cause` to the same object** (`err.cause = err` is always a bug).
3. **Bound the chain depth.** If `depth(err) > 4`, stop wrapping and log a translation-smell.
4. **Retry by re-running, not by re-wrapping** the previous attempt's error as the new one's cause.

```python
# ❌ Circular / self-referential cause.
err.__cause__ = err
# ✅ Add a distinct wrapper that points one level down.
raise RetryExhausted("after 3 attempts") from last_attempt_error
```

## 16.18 — Versioning rules

The internal error model and the public codes are contracts (Ch. 49). Translation must respect
versioning:

| Change | Compatible? | Rule |
| ------ | ----------- | ---- |
| Add a new internal code | Yes | Add table entries; never reuse an existing code |
| Change a mapping (`409` → `422`) | **Breaking** | Version the API; document; migrate clients |
| Change a `safeMessage` wording | Usually safe | Clients must not depend on message text |
| Remove/deprecate a code | Breaking | Keep it, mark deprecated, map to a successor |
| Add a vendor | Safe | Add an adapter + table entries; consumers unchanged |
| Provider changes its code string | Adapter change only | Add the new string to the table; keep stable target |

Rules for evolving a table:

- **Never reuse a code for a different meaning.** `ALREADY_EXISTS` must not silently become a
  validation error later.
- **Add, don't mutate.** New vendor codes get new table rows; the stable target stays unless you
  deliberately version it.
- **Deprecate explicitly.** Keep `OLD_CODE` mapped to `NEW_CODE` for at least one contract version
  (Ch. 49.8).
- **Version the public mapping, not the internal adapter.** Internal adaptations are free;
  changes that alter the public `code`/status are versioned contract changes.

## Key data / numbers

- Vendor codes that recur: Stripe `card_declined` / `rate_limit_error`; AWS S3 `SlowDown` /
  `AccessDenied` / `NoSuchKey`; OpenAI `rate_limit_exceeded` / `context_length_exceeded`;
  Anthropic `overloaded_error` (`529`).
- Stable target codes should be `SCREAMING_SNAKE_CASE`, domain-prefixed, and unique (Ch. 8).
- Chain depth target 2–4 links; hard-stop wrapping beyond 4.
- Deprecation window: keep a deprecated code for one contract version minimum.

## Real-world use case — WebhookIngest

`WebhookIngest` ingests events produced by Stripe but also calls S3 and OpenAI. A single
`RULES` table now covers all three vendors. When Stripe introduced a new decline subtype, the team
added one row — no downstream code changed. A **coverage test** fails CI if a known vendor code has
no row, so provider drift is caught before deploy. A circular-chain detector runs over the DLQ
replay path after an incident where re-wrapping created a self-referential cause that hung the
log formatter.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map vendor → stable code in one table | Scatter inline `switch` mappings everywhere |
| Reject wrapping an already-normalized error | Re-wrap an `AppError` into another `AppError` |
| Keep chains shallow (2–4) | Set `cause = self` or wrap endlessly |
| Add new codes; never reuse old ones | Change a code's meaning in place |
| Test every table entry + coverage | Rely on production to find drift |

## Common mistakes

- **Inline vendor mappings** that no one can audit.
- **A generic `wrap()`** that re-wraps normalized errors → circular chains.
- **Reusing a stable code** for a new meaning, breaking clients.
- **No coverage test**, so a new vendor code falls through to a vague error.

## Checklist

- [ ] Vendor codes are mapped to stable codes in one reviewable table.
- [ ] Every table entry has a unit test; coverage asserts no known code falls through.
- [ ] Translation refuses to wrap an already-normalized error.
- [ ] Chain depth is bounded; cycles are detected.
- [ ] Codes are added/deprecated, never redefined in place.

## Related

- [Translation Tables and Policies (deep dive)](../02-deep-dive/01-translation-tables-and-policies.md)
- [Versioning and Backward Compatibility (deep dive)](../02-deep-dive/03-versioning-and-backward-compatibility.md)
- [Part III — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
