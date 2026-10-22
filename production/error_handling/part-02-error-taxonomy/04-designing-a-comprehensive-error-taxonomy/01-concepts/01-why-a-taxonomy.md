# Why Every Codebase Needs a Taxonomy, and How to Structure It

> Part II · Chapter 4 · Sections 4.1–4.2 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 1 — Error, Fault, Failure, and Exception](../../../part-01-foundations/01-understanding-errors-and-failures/01-concepts/01-error-fault-failure-exception.md)

## In one sentence

A **taxonomy** is a shared, hierarchical vocabulary that assigns every failure a category — and a
category is the smallest unit that maps to a **policy** (retry, HTTP status, alert, disclosure).

## Why this matters in production

Without a taxonomy, error handling is improvised per developer and per file. Three production
consequences recur:

- **Inconsistent policy.** One handler retries a `409`; another gives up. The same class of
  failure gets opposite treatments depending on who wrote the code.
- **Unreliable routing.** A global handler cannot decide if an unknown error is business or
  technical, so it returns `500` for a declined card and pages on-call for a validation failure.
- **Unmaintainable growth.** Every new feature invents new ad-hoc error strings, and nobody can
  answer "how many kinds of failure does this system have?"

A taxonomy is the input to every downstream decision. It is the cheapest architectural investment
in this entire book.

## Core concept — taxonomy, categories, and codes

Three words are often confused. Keep them distinct:

| Term | Meaning | Example |
| ---- | ------- | ------- |
| **Taxonomy** | The whole classification *system* (axes + hierarchy + rules) | "Origin, domain, recoverability, security, …" |
| **Category** | One bucket on one axis | `authorization`, `conflict`, `timeout` |
| **Code** | A stable machine identifier for one specific condition | `AUTHZ_INSUFFICIENT_SCOPE` |

The taxonomy is the *design*. Categories and codes are its *contents*. Chapter 8 turns codes into
a registry.

## Hierarchical classification

Classify in three levels so you can route broadly and act narrowly:

```text
LEVEL 1 — FAMILY (routing, alerting, ownership)
  e.g.  INPUT | AUTH | BUSINESS | DATA | EXTERNAL | RUNTIME | ASYNC

LEVEL 2 — CATEGORY (policy: retry, HTTP class, disclosure)
  e.g.  validation | authorization | conflict | database | timeout

LEVEL 3 — CONDITION (specific, stable code + message)
  e.g.  VALIDATION_REQUIRED_FIELD | CONFLICT_VERSION_MISMATCH
```

Why a hierarchy and not a flat list?

- **Level 1** lets a global handler or dashboard reason about a small number of families.
- **Level 2** is where most policy lives (retryable? business? security-sensitive?).
- **Level 3** is where exact user messaging and support references live.

A concrete tree for one family:

```text
INPUT
├── validation            → 400/422, no retry,  field details
│   ├── VALIDATION_REQUIRED_FIELD
│   └── VALIDATION_RANGE
├── request_parsing       → 400,  no retry
│   └── REQUEST_MALFORMED_JSON
└── not_found             → 404, no retry
    └── RESOURCE_NOT_FOUND
```

## How it works (mechanics)

1. **Enumerate** the failures a component can produce (start with one service, not the whole org).
2. **Bucket** each into a family and a category using the axes from this chapter.
3. **Name** the specific condition with a stable code.
4. **Attach policy** to the *category* (not the individual throw site): retry verdict, HTTP
   class, alert severity, redaction rules.
5. **Store** the classification on the error object so no handler has to re-derive it.

The key insight: **each error is classified once, at creation, and read everywhere.** If two
handlers classify the same error differently, the taxonomy has failed.

## Worked example

Acme's `ExportJob` fails because a job's requested date range is inverted (`from > to`).

```text
Family:   INPUT
Category: validation
Condition: VALIDATION_RANGE_INVERTED
Derivable: HTTP 422, no retry, WARN log, field detail on `to`, no alert, safe to show user
```

Now the *same* `ExportJob` fails because the S3 bucket is missing (misconfiguration).

```text
Family:   RUNTIME
Category: configuration
Condition: CONFIG_DEPENDENCY_MISSING
Derivable: HTTP 500 (internal only), no retry, ERROR log, alert ops, never show detail to user
```

Two failures inside one job, two families, two complete policies — decided by classification, not
by a per-file `if`.

## Key data / numbers

- `400` vs `422`: many groups reserve `400` for **syntactic** failures and `422` for
  **semantically valid but rule-violating** requests. Both are *permanent* and non-retryable.
- A healthy starter taxonomy is **7–12 families and ~40–80 codes**; a system with 500+ hand-made
  codes usually lacks governance (Section 4.17).
- Kubernetes and gRPC both ship **fixed status enums** (`INVALID_ARGUMENT`, `DEADLINE_EXCEEDED`,
  `RESOURCE_EXHAUSTED`, …) precisely because a shared enum prevents per-service drift.

## Real-world use case — Acme SaaS

Acme's billing, uploads, and LLM features each grew their own error strings. A customer saw
`"error: 500"` for an expired card, then `"internal error"` for a missing file. Support could not
tell which failures were user-fixable. Acme introduced three families (`INPUT`, `AUTH`,
`EXTERNAL`) and mapped every existing string to a category. Support ticket triage time dropped
because each category now mapped to a fixed response playbook. The taxonomy, not new code, was the
fix.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Flat list of codes | Simple to start | No broad routing, drift | Tiny script/service |
| Three-level hierarchy | Routing + policy + message | Slightly more setup | Any SaaS with >1 team |
| Full ontology (many axes) | Rich queries | Overkill, hard to maintain | Analytics-heavy platforms only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify once at creation, read everywhere | Re-derive category in each handler |
| Keep families small and stable | Add a family per feature |
| Attach policy to categories | Hard-code policy per throw site |
| Name categories after cause/consequence | Name them after error text |

## Common mistakes

- **Classification by message string.** `err.message.includes("timeout")` breaks the moment a
  vendor rewords it.
- **One giant flat enum.** It grows forever and supports no broad routing.
- **No distinction between category and code.** Teams end up with 200 "categories" that are
  really conditions.
- **Classifying at the boundary.** By then the original meaning is often lost; classify where the
  error is created.

## Checklist

- [ ] Do you have a defined set of families and categories?
- [ ] Is classification attached to the error at creation?
- [ ] Can a global handler route on category without parsing messages?
- [ ] Is there exactly one place that decides each category's policy?

## Related

- [Classification Axes: Origin → Retry](./02-classification-axes-origin-through-retry.md)
- [Classification Axes: HTTP → Compensation](./03-classification-axes-http-through-compensation.md)
- [Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Glossary: error taxonomy](../../../GLOSSARY.md)
