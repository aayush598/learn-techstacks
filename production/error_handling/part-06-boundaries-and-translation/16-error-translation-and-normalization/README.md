# Chapter 16 — Error Translation and Normalization

> Part VI · _Estimated reading time: 70–95 min_
> **Prerequisite:** [Chapter 15 — Error Boundaries](../15-error-boundaries/README.md)

## One-sentence summary

**Translation** converts an error from one representation to another at a boundary, and
**normalization** reduces many vendor/format-specific formats into one consistent internal shape —
both **without losing the cause or the retry metadata**.

## Why this chapter matters

Every external system speaks its own error dialect: Postgres speaks `SQLSTATE`, the OS speaks
`errno`, Stripe speaks JSON error types, gRPC speaks numeric status codes, the browser speaks
`TypeError`. If you let these dialects reach your domain and your API, then every handler,
retry policy, and frontend must understand all of them. Translation gives you **one internal
error model** (Part III) that every consumer can act on. Done badly, translation erases the cause
("something failed") or the recovery hint (an unretryable blob), which is how transient outages
become permanent ones.

## Chapter map

The chapter has 18 sections. They are grouped into these files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-why-translate-and-normalize.md`](./01-concepts/01-why-translate-and-normalize.md) | 16.1, 16.2 | The costs of vendor leakage; what "normalizing formats" means |
| [`01-concepts/02-translation-directions.md`](./01-concepts/02-translation-directions.md) | 16.3–16.9 | Native→app, DB→domain, external→internal, framework→app, domain→transport, worker→job, OS→app |
| [`01-concepts/03-preserving-cause-and-recoverability.md`](./01-concepts/03-preserving-cause-and-recoverability.md) | 16.10–16.12 | Keeping the root cause, retry class, and completeness of information |
| [`01-concepts/04-avoiding-overgeneralization-and-unknowns.md`](./01-concepts/04-avoiding-overgeneralization-and-unknowns.md) | 16.13, 16.14 | Not collapsing distinct errors into one; handling formats you have never seen |
| [`01-concepts/05-vendor-codes-tables-and-versioning.md`](./01-concepts/05-vendor-codes-tables-and-versioning.md) | 16.15–16.18 | Vendor→stable codes, translation tables/policies, circular chains, versioning rules |
| [`02-deep-dive/01-translation-tables-and-policies.md`](./02-deep-dive/01-translation-tables-and-policies.md) | 16.16 | Designing data-driven translation tables and their policy hooks |
| [`02-deep-dive/02-preserving-cause-and-circular-chains.md`](./02-deep-dive/02-preserving-cause-and-circular-chains.md) | 16.10, 16.11, 16.17 | Chaining mechanics across languages; detecting and breaking cycles |
| [`02-deep-dive/03-versioning-and-backward-compatibility.md`](./02-deep-dive/03-versioning-and-backward-compatibility.md) | 16.18 | Evolving translation mappings without breaking clients |
| [`03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md`](./03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md) | all | Concrete SQLSTATE → domain error → HTTP status map |
| [`03-practical-examples/02-normalization-with-recurring-cast.md`](./03-practical-examples/02-normalization-with-recurring-cast.md) | all | Normalizing Stripe, S3, and LLM provider errors with the cast |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Translation rules, anti-patterns, checks |
| [`05-reference/README.md`](./05-reference/README.md) | all | Translation decision tree, boundary placement guide, mapping table |

## Learning objectives

By the end you can:

- Explain why translation belongs at the boundary and not in the domain.
- Translate in every direction: DB→domain, external→internal, framework→application,
  domain→transport, worker→job failure, OS→application.
- Preserve the original cause and the retry/recoverability classification through each hop.
- Recognize overgeneralization (many errors → one vague error) and unknown-format handling.
- Maintain a translation table and version it without breaking consumers.

## Key takeaways

1. **Translate once, at the boundary.** Downstream code should never `switch` on `SQLSTATE` or a
   vendor string.
2. **Preserve the cause.** Use native chaining (`Error.cause`, `%w`, `raise from`,
   `initCause`) so the root is one `stack`/`unwrap` away.
3. **Preserve retry metadata.** A normalized error must still know whether it is transient.
4. **Distinguish errors; do not collapse them.** `23505` (unique) and `23503` (FK) are different
   domain problems.
5. **Unknown formats get a safe, generic, non-leaking mapping** — never pass the raw payload
   through.

## Exercises

1. List every error format entering your system and the boundary where each is translated.
2. Take one translation in your code and check: is the cause preserved? Is the retry class
   preserved?
3. Find an overgeneralization bug where two distinct DB errors map to the same application code.
4. Write a translation table for one provider and mark which of its errors are transient.

## Related

- [Chapter 15 — Error Boundaries](../15-error-boundaries/README.md)
- [Part III — Designing the Application's Error Model](../../part-03-error-models/06-designing-the-applications-error-model/README.md)
- [Part IX — Database Error Classification](../../part-09-database-and-transactions/22-database-error-classification/README.md)
