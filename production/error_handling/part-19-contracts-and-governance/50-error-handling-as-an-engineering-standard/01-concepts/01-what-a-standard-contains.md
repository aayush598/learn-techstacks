# What an Error-Handling Standard Contains

> Part XIX · Chapter 50 · Sections 50.1–50.3 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 49 — Error Contract Design and Versioning](../../49-error-contract-design-and-versioning/README.md)

## In one sentence

An org-wide standard is a **small set of decidable rules about names, codes, and structure**,
written so that an engineer in any team, in any language, can comply without asking — and so
that a tool can verify compliance without judgement.

## Why this matters in production

Standards fail in two directions, and both are common:

- **Too vague.** "Handle errors appropriately" tells a new engineer nothing, so they invent a
  pattern, and you now have six patterns across six teams.
- **Too specific.** "Always use `AppError` from `@acme/errors` with these exact fields" is
  unimplementable in a Go service and in a Python data pipeline, so half the org ignores it and
  the other half argues about it.

The sweet spot is: **rules about observable behaviour and vocabulary, guidance about
implementation**. A standard should be written so that the *same rule* can hold in TypeScript,
Python, Go, and a SQL transform.

## 50.1 — Org-wide conventions

### What belongs in the standard

| Included | Excluded |
| -------- | -------- |
| Vocabulary (code names, category names, status vocabulary) | Specific library choices per language |
| Observable shapes (what an error body contains) | Internal class hierarchies |
| Decision rules (when to retry, when to fail, when to degrade) | Exact backoff constants per dependency |
| Security floors (what may never appear in an error) | The full redaction taxonomy |
| Process (who approves, how to record, how to exception) | Code review checklists for other domains |

### The three layers

Every rule belongs to one of three layers, and the layer determines how it is enforced:

```text
POLICY      what must be true            e.g. "no stack trace in a public response"
            enforced by: CI or contract test

CONVENTION  what most code should do     e.g. "one error class per file, named <Domain>Error"
            enforced by: review checklist, scaffold templates

GUIDANCE    how to think about it        e.g. "prefer a narrow error boundary over a global catch"
            enforced by: nobody — it informs
```

Confusing these layers is the most common drafting mistake. A convention written as a policy
gets skipped; a policy written as guidance is not obeyed.

### The smallest useful standard

A new organisation should start with **one page and twelve rules**, not a document. The twelve
rules below are enough to remove most inconsistency:

```text
 1. Every error carries a stable, registered code.
 2. Codes are named <DOMAIN>_<REASON> in UPPER_SNAKE_CASE.
 3. Public codes are registered before they can be returned.
 4. Every error crossing a boundary is translated at that boundary.
 5. Unknown error kinds are never swallowed; they are propagated or converted to a generic one.
 6. A retry is only permitted for a code explicitly marked retryable.
 7. A retry is only permitted for an idempotent operation.
 8. Every outbound call has a timeout.
 9. Public error responses never contain stack traces, SQL, or internal hostnames.
10. Public error responses are application/problem+json with a stable shape.
11. Every error carries a correlation id.
12. Every deviation from this standard is registered, owned, and reviewed.
```

Everything else — deeper taxonomies, per-dependency policies, specific message catalogues —
is **guidance** or belongs in a project-specific appendix.

### Applicability

Say plainly who the standard applies to and where it does not:

```text
Applies to:   all services owned by the platform, product, and growth teams
              all public and partner-facing surfaces
              all background workers and scheduled tasks

Does not apply to:
              data pipelines where a failed batch is a normal outcome
              client-side code (see the web/mobile standard)
              third-party integrations we do not own (we translate their errors, not standardise them)
```

## 50.2 — Naming standards

Naming is the highest-leverage, lowest-cost part of a standard: it is trivially enforceable
and it removes the largest source of cross-team confusion.

### The vocabulary

The standard should fix the **words** an engineer uses, because most inconsistencies are
linguistic before they are technical.

| Concept | Standard term | Do not use |
| ------- | ------------- | --------- |
| The thing that carries a failure | **error** | exception, failure, fault (as a type name) |
| A specific condition with a code | **error code** | error type, error kind, status |
| A class/struct representing an error | **`<Domain>Error`** | `Err`, `Exception`, `Failure`, `Problem` |
| The result type when errors are values | **`Result<T, E>`** | `Either`, `Outcome`, `Response` |
| The function that maps errors to a wire shape | **serializer** | formatter, mapper, renderer |
| The place where errors are caught deliberately | **error boundary** | handler, interceptor, middleware (be specific) |
| A registry of codes | **error registry** | error table, error list, catalogue |

### Rules that are enforceable

```text
R-NAME-1  One error class per file; the file name matches the class name.
R-NAME-2  Error class names are <Domain><Reason>Error, PascalCase, no abbreviations
          (except a small allowed list: Id, Url, Http, Db, Io, Jwt, S3).
R-NAME-3  Error code names are <DOMAIN>_<REASON>, UPPER_SNAKE_CASE, 2–5 segments, ≤ 64 chars.
R-NAME-4  Reason suffixes come from a controlled list (see below).
R-NAME-5  "Error" is not a suffix on a variable: `err`, `cause`, `reason` — not `error`.
R-NAME-6  Never name a type after the mechanism that produced it
          (DbTimeoutError, StripeDeclinedError) — name it after the condition.
```

The **controlled suffix list** is what makes codes sortable and greppable:

```text
_NOT_FOUND      _EXISTS          _CONFLICT        _INVALID
_INVALID        _EXPIRED         _DECLINED        _REJECTED
_TIMEOUT        _UNAVAILABLE     _EXHAUSTED       _LIMIT_EXCEEDED
_RATE_LIMITED   _OUT_OF_RANGE    _UNSUPPORTED     _MISMATCH
_DUPLICATE      _FAILED          _REQUIRED        _FORBIDDEN
_UNAUTHENTICATED _UNAUTHORIZED   _INTERRUPTED     _CANCELLED
```

A controlled list of ~20 suffixes, enforced by a lint, eliminates an entire class of
inconsistency: `USER_NOT_FOUND` vs `USER_MISSING` vs `USER_ABSENT`.

### Naming the thing, not the mechanism

This is the rule teams break most often, and it matters because mechanisms change:

| ❌ Mechanism-named | ✅ Condition-named |
| ----------------- | ------------------ |
| `PostgresTimeoutError` | `EXPORT_STORAGE_TIMEOUT` |
| `StripeDeclinedError` | `PAYMENT_CARD_DECLINED` |
| `RedisConnectionError` | `CACHE_UNAVAILABLE` |
| `NullPointerError` | `INTERNAL_UNEXPECTED` |

Mechanism-named codes leak your architecture into a contract. When the cache moves from Redis
to a different client, the code changes — and now it is a breaking change.

## 50.3 — Code conventions

Beyond names, a standard fixes the **shape** of an error and the **procedure** for adding one.

### Structural rules

```text
R-STRUCT-1  Every error carries: code · category · retryable · cause · correlationId ·
             occurredAt · safeContext.
R-STRUCT-2  `cause` is preserved through translation; a translated error always points at
             the original.
R-STRUCT-3  `safeContext` is an allowlist of fields (ids, counts, durations) — never raw
             request bodies, headers, tokens, or SQL.
R-STRUCT-4  Errors are immutable once constructed.
R-STRUCT-5  An error's code is fixed at construction; it is never reassigned.
```

### The recipe: adding an error in five steps

A standard should make the common case **mechanical**. Here is the standard's recipe, which
every project implements in its own idiom:

```text
Step 1  Decide the CONDITION in one sentence. If the sentence needs "or", it is two errors.
Step 2  Pick the code from the registry, or register a new one (new codes need an owner,
        an HTTP mapping, a retry decision, and a message key).
Step 3  Create the error type in the domain layer — no framework imports, no HTTP types.
Step 4  Translate it at the boundary (HTTP / job / event) into the standard shape.
Step 5  Map it to a user message key and a client action. Never invent English strings.
```

Step 3's "no framework imports" rule is what keeps the domain layer testable and what allows
the same domain error to be reused by the HTTP API, a background worker, and an event
consumer.

### Where the pieces live

A standard can name a **shape** for the code layout without prescribing a specific framework:

```text
errors/
  codes.ts        the code registry (single source of truth)
  types.ts        the error types, one per file
  mapping.ts      code → http status, retry, client action, message key
  translate.ts    boundary translators (http.ts, job.ts, event.ts)
  internal.ts     the generic internal error
```

The names are conventions; the language is not. A Python service can honour the same four
responsibilities with `codes.py`, `exceptions.py`, `mapping.py`, `translate.py`.

### What the standard does not say

- Which class to extend.
- Whether you use exceptions or `Result`.
- Which HTTP framework.
- How many layers you have.

Those are **project decisions** (Chapter 56), and a standard that settles them is a standard
that only one project can obey.

## Worked example — naming a new error end to end

```text
Requirement:  Acme's ExportJob must fail when a requested column does not exist in the
               tenant's schema.

Step 1  Condition: "A requested export column does not exist in the project's schema."
        (One sentence, no "or".)

Step 2  Code:     EXPORT_COLUMN_MAPPING_INVALID
        Domain:  EXPORT (reserved prefix)
        Reason:  _INVALID from the controlled suffix list
        Registry row: http 422 · retryable false · idempotent true ·
                       clientAction contact_support · messageKey
                       errors.export.columnMappingInvalid · owner data-team

Step 3  Type:     ExportColumnMappingInvalidError (domain layer, no framework imports)

Step 4  Translate at the HTTP boundary → 422, application/problem+json, code preserved
        Translate at the job boundary    → non-retryable job failure, code preserved

Step 5  Message:  message key only. The web app renders the localized string.
        The job dashboard renders "export column missing: {column}".
```

Five steps, no debate about which layer catches what, and the same code works across the API,
the worker, and the dashboard.

## Key data / numbers

- **Standard layers:** policy (CI-enforced) · convention (review) · guidance (informative).
- **Starting size:** one page, **12 rules**, expanded only when a real gap appears.
- **Controlled suffix list:** ~**20** reason suffixes, lint-enforced.
- **Code shape:** `<DOMAIN>_<REASON>`, UPPER_SNAKE_CASE, 2–5 segments, ≤ 64 characters.
- **Error shape:** 7 required fields — code · category · retryable · cause · correlationId ·
  occurredAt · safeContext.
- **Enforcement target:** ≥ **60%** of rules mechanically checkable; the rest in review.
- **Step count for a new error:** **5** (condition → code → type → translate → message/action).
- **Exception register:** owner + justification + **review date** on every entry.

## Real-world use case — Acme SaaS

Acme's six teams each had their own error conventions. The symptoms were mundane and constant:
three different spellings of "not found" in the same API (`USER_NOT_FOUND`, `USER_NOT_EXIST`,
`USER_MISSING`), two teams using `Error` as a class-name suffix and two using `Err`, and one
team whose `ValidationError` always meant HTTP 422 — which broke the moment a validation
failure needed to be a `409`.

Acme's fix was not a rewrite. They wrote **fourteen rules**, of which nine became CI checks:

```text
CI-1  every code literal in src/ exists in the registry
CI-2  registry codes are unique and match <DOMAIN>_<REASON>
CI-3  registry codes use an allowed suffix
CI-4  domain error modules import no HTTP/framework types
CI-5  every error class file exports exactly one error class
CI-6  no consumer compares a message/detail string for branching
CI-7  every retry call site uses a code marked retryable
CI-8  every outbound client has a configured timeout
CI-9  public error responses contain no stack trace, SQL, or hostname
```

The remaining five rules became a review checklist item. Teams that disagreed with a rule had
to register an exception rather than ignore it — and in the first quarter, exactly **three**
exceptions were registered, all of them for the webhook surface, which legitimately has
different retry semantics.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One org-wide standard, implementation-neutral | Consistent across stacks; portable | Some rules cannot be enforced everywhere | Multi-stack organisations |
| Per-language standards | Precise, enforceable | Divergence; three standards to maintain | Very large orgs with distinct platform teams |
| Per-project standards | Fits the project | No consistency; no reuse | Never, for the same domain logic |
| Principles only ("handle errors well") | Short | Not decidable; not enforceable | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write rules about observable behaviour and vocabulary | Prescribe a class hierarchy for every language |
| Label each rule policy, convention, or guidance | Mix the three layers in one list |
| Fix the vocabulary (error, code, boundary) | Let "exception" and "failure" mean whatever |
| Use a controlled suffix list | Invent a new suffix per feature |
| Name conditions, not mechanisms | Name a code after a database or vendor |
| Provide a five-step recipe for adding an error | Leave the procedure to each team |
| Say where the standard does not apply | Pretend one size fits every workload |

## Common mistakes

- **The 200-page standard.** Nobody reads it; the first three pages are what survive.
- **The implementation-locked standard.** Two of three languages cannot comply.
- **The uncontrolled suffix list.** `USER_MISSING`, `USER_ABSENT`, `USER_UNKNOWN`.
- **The mechanism-named code.** The code changes when the technology changes.
- **The unlayered rule list.** Guidance and policy indistinguishable, so nobody knows what to
  enforce.
- **The standard with no exceptions process.** Deviations happen silently.

## Checklist

- [ ] The standard states its scope and where it does not apply.
- [ ] Every rule is labelled policy, convention, or guidance.
- [ ] The vocabulary is fixed: error, code, boundary, serializer, registry.
- [ ] Code naming is `<DOMAIN>_<REASON>` with a controlled suffix list.
- [ ] Naming rules forbid mechanism-derived names.
- [ ] The required error shape is specified as observable fields.
- [ ] A five-step recipe exists for adding a new error.
- [ ] ≥ 60% of rules have a mechanical check.

## Related

- [Behavioral Standards: Propagation, Retry, Response, Recovery](./02-behavioral-standards.md)
- [Security Requirements and Exceptions to the Standard](./03-security-and-exceptions.md)
- [Durable Rules, Exceptions, and Change Management](../02-deep-dive/01-durable-vs-ceremonial-rules.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../../part-17-organization/45-organizing-error-handling-modules/README.md)
