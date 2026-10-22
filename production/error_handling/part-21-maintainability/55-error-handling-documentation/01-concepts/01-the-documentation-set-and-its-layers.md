# The Documentation Set and Its Layers

> Part XXI · Chapter 55 · Sections 55.1, 55.2, 55.3 · _Estimated reading time: 18 min_
> **Prerequisite:** [Chapter 54 — Reusable Error-Handling Infrastructure](../../54-reusable-error-handling-infrastructure/README.md)

## In one sentence

Error-handling documentation is **four layers — architecture, contract, policy, and decision
— each with one audience, and the code registry is the layer everything else derives from.

## Why this matters in production

Teams do not fail at writing documentation. They fail at **writing one document and expecting
it to serve four audiences**. The result is a single `ERRORS.md` that is an architecture
overview for a new engineer, an API contract for a partner, a runbook for an operator, and a
decision guide for an implementer — none of them satisfied, all of them drifting.

The fix is not more writing. It is **layering**: separate the documents by audience, then
make the shared facts live in exactly one place.

## Core concept

### 55.1 — The four layers

```text
  ┌───────────────────────────────────────────────────────────────┐
  │  LAYER 1  ARCHITECTURE      Who owns errors, where they live  │
  │  audience: new engineer, new service, reviewer                 │
  │  file:     docs/error-handling/ARCHITECTURE.md     (~2 pages) │
  ├───────────────────────────────────────────────────────────────┤
  │  LAYER 2  CONTRACT          What clients see, and what codes  │
  │  audience: API consumer, SDK user, partner engineer           │
  │  file:     docs/error-handling/API-CONTRACT.md     (~4 pages) │
  ├───────────────────────────────────────────────────────────────┤
  │  LAYER 3  POLICY            Retry, recovery, fallback, tx    │
  │  audience: on-call engineer, SRE, incident commander         │
  │  file:     docs/error-handling/POLICIES.md         (~3 pages) │
  ├───────────────────────────────────────────────────────────────┤
  │  LAYER 4  DECISION          "What should I do when…"         │
  │  audience: implementer, mid-task, in the middle of a change  │
  │  file:     docs/error-handling/DECISION-GUIDE.md   (~2 pages) │
  └───────────────────────────────────────────────────────────────┘
              ▲
              │  all four reference
        ┌─────┴──────────────────┐
        │  THE REGISTRY           │  docs/error-handling/REGISTRY.md
        │  the single source of   │  generated from code, one row per code
        │  truth for every code   │
        └─────────────────────────┘
```

Three rules make the layering work:

| Rule | Statement |
| ---- | --------- |
| **L1** | **One fact, one home.** A status code appears in the registry and is quoted everywhere else, never re-typed. |
| **L2** | **One audience per layer.** A document that has to serve two audiences serves neither. |
| **L3** | **The registry is generated.** A table of 200 codes maintained by hand is wrong by row 30. |

The registry sits outside the four layers because it is not a document — it is **data**, and
the documents are generated from it where possible.

### The document set at Acme

| File | Pages | Audience | Checked by |
| ---- | ----- | -------- | ---------- |
| `ARCHITECTURE.md` | 2 | New engineers | Link check + code-example test |
| `API-CONTRACT.md` | 4 | API consumers | Golden-body test |
| `POLICIES.md` | 3 | On-call | Policy-table diff |
| `DECISION-GUIDE.md` | 2 | Implementers | Checklist test |
| `REGISTRY.md` | 6 | Everyone | Generated; CI diff |
| `adr/0007-error-taxonomy.md` | 1 | Future maintainers | Approval state |
| `runbook/error-contracts.md` | 2 | On-call | Reviewed quarterly |
| **Total** | **20** | — | — |

Twenty pages for a service with 214 error codes, 6 providers, and 4 transports. That is the
target: a documentation set that needs a table of contents is a documentation set that is
too big.

### 55.2 — Documenting categories

Categories are the vocabulary of the whole system, so they get the shortest document and the
strictest rules.

The category documentation is a **table with five columns**, and it is generated from the
same `CATEGORY_POLICY` object the code uses:

| Category | HTTP status | Public code | Retryable | What it means |
| -------- | ----------- | ----------- | --------- | ------------- |
| `validation` | 422 | `VALIDATION_FAILED` | no | The request is malformed or violates a field rule |
| `business` | 422 | `BUSINESS_RULE_VIOLATION` | no | The request is well-formed but not allowed right now |
| `conflict` | 409 | `CONFLICT` | no | The resource's current state conflicts with the request |
| `auth` | 401 | `UNAUTHENTICATED` | no | The request is not authenticated, or a signature failed |
| `not_found` | 404 | `NOT_FOUND` | no | The resource does not exist, or the caller may not know it |
| `external_api_permanent` | 502 | `PROVIDER_REJECTED` | no | A provider rejected the request and will keep rejecting it |
| `external_api_transient` | 503 | `DEPENDENCY_UNAVAILABLE` | yes | A provider failed temporarily and the same call may succeed |
| `external_api_ambiguous` | 202 | `RESOLUTION_PENDING` | no | The provider may have accepted the request; the outcome is unknown |
| `database_transient` | 503 | `DATABASE_UNAVAILABLE` | yes | The database failed temporarily (deadlock, serialization failure) |
| `data_integrity` | 500 | `INTERNAL_ERROR` | no | Our data was inconsistent; a human must look |
| `dependency_unavailable` | 503 | `DEPENDENCY_UNAVAILABLE` | yes | A dependency is down; a fallback may be used |
| `resource_exhausted` | 503 | `RESOURCE_EXHAUSTED` | yes | A quota, pool, or rate limit is exhausted |
| `rate_limit` | 429 | `RATE_LIMITED` | yes | The caller sent too much traffic |
| `cancellation` | 499 | `CLIENT_CLOSED_REQUEST` | no | The client went away before the work finished |
| `internal` | 500 | `INTERNAL_ERROR` | no | A bug in our code |

The fifth column — **what it means** — is the one humans actually need, and the one most
often missing. "A provider failed temporarily and the same call may succeed" tells an
engineer whether to retry. "external_api_transient" does not.

Two rules for the category table:

- **No category without a sentence.** If you cannot write the fifth column, the category is
  not understood well enough to have.
- **No category without an owner.** A category nobody owns is a category that will drift.

### 55.3 — Documenting the code registry

The registry is the largest document and the most mechanical one. It is **generated** from
the code, and its per-row description is the only hand-written part.

```text
  code                                     category                 owner    since    since
  ───────────────────────────────────────  ───────────────────────  ───────  ───────  ──────
  checkout.ORDER_NOT_FOUND                 not_found                checkout 1.0.0    ✓
  checkout.ORDER_ALREADY_PAID              conflict                 checkout 1.0.0    ✓
  checkout.CARD_DECLINED                   external_api_permanent   payments 1.0.0    ✓
  checkout.CARD_GATEWAY_UNREACHABLE        external_api_transient   payments 1.4.0    ✓
  export.EXPORT_ROW_LIMIT_EXCEEDED         resource_exhausted      exports  2.0.0    ✓
  export.UPSTREAM_TIMEOUT                  external_api_transient   exports  2.0.0    ✓
  webhook.SIGNATURE_INVALID                auth                    webhooks 1.0.0    ✓
  webhook.DUPLICATE_EVENT                  business                webhooks 1.2.0    ✓
  agent.TOOL_CALL_INVALID                  validation              agent    2.1.0    ✓
  agent.PROVIDER_CONTEXT_EXCEEDED          external_api_permanent   agent    2.1.0    ✓
```

Each row carries five fields, and the columns answer four questions:

| Column | Question it answers | Where it comes from |
| ------ | ------------------- | ------------------- |
| `code` | Which failure is this? | The registry, namespaced by domain |
| `category` | What kind of failure is it, and what should a caller do? | The registry |
| `owner` | Who is paged when it fires? | The registry |
| `since` | When did it appear? | The registry |
| `description` | In words, what happened? | **Hand-written, next to the code** |

The `description` is the only field that cannot be generated, and it is the field a reader
actually needs. It is written in the same file as the code, so the two are edited together:

```ts
// src/features/checkout/codes.ts
export const checkoutCodes = defineRegistry("checkout", {
  ORDER_ALREADY_PAID: {
    category: "conflict",
    publicMessage: "Order is already paid",
    owner: "checkout",
    description: "The order was already paid; the payment must not be captured again.",
  },
});
```

The description is **one sentence, in plain language, written from the caller's point of
view** — not a restatement of the code name. "Order was already paid" is a restatement;
"the payment must not be captured again" tells the reader what to do.

Two registry-level facts belong in the document as well:

- **The `since` column** tells a reader when a failure started existing — the fastest way to
  answer "is this new?".
- **The `deprecated` column** (when present) tells a reader that the code will disappear and
  what replaces it.

## How it works (mechanics)

The generation pipeline, which is the whole point:

```text
  src/features/*/codes.ts
        │
        │  ast scan (not a text grep)
        ▼
  ┌──────────────────────────────────┐
  │  extract: code, category,       │
  │  owner, since, description      │
  └──────────────────────────────────┘
        │
        ├──────────────▶ REGISTRY.md  (generated table)
        │
        ├──────────────▶ CATEGORY-POLICY.md  (category table, from the shared package)
        │
        └──────────────▶ api-errors.json  (machine-readable, for SDK generation)
```

The generated files are **committed** and the CI check regenerates them and fails on a diff.
Committing them means a reader can see the registry in a pull request without running
anything; the CI check means the committed copy cannot be stale.

The scan must be **AST-based**. A text grep for `createError(` finds comments, docs, and
string literals; an AST scan finds real call sites. Acme's first version was a grep, and the
generated table contained 41 rows that no code could ever raise.

## Worked example

A new engineer, `Sam`, joins the `checkout` team on a Tuesday. Sam's task: add a new error
code for "the order has already been shipped".

Sam opens `docs/error-handling/DECISION-GUIDE.md` and finds the entry:

```text
  "I need a new error code"
    1. Open src/features/<domain>/codes.ts
    2. Add a row to the registry:
         code        → <DOMAIN>.<NAME>, uppercase, snake_case
         category    → one of the 15 (see CATEGORY-POLICY.md)
         publicMessage → what the client sees; no internal wording
         owner       → the team that is paged
         description → one sentence, from the caller's point of view
    3. Raise it:  throw createError("<DOMAIN>.<NAME>", "internal message", { context: {...} })
    4. Add a test that asserts the public body.
    5. Run:  npm run check:errors
```

**Total: 25 minutes**, of which 15 were writing the code and 10 were reading the guide. No
question was asked of a human, and no wiki page was consulted.

The alternative — what actually happened the month before — is instructive: Sam's predecessor
had added the code in the boundary handler rather than the feature, so the status was `500`
instead of `409`, the code was not in the registry, and the API contract did not mention it.
The client saw `500` for a business conflict, and retried, and created a duplicate shipment.

## Key data / numbers

- **Layers: 4** (architecture, contract, policy, decision), plus the generated registry.
- **Document set at Acme: 20 pages** across 8 files for 214 codes, 6 providers, 4 transports.
- **Per-document size:** architecture 2, contract 4, policy 3, decision guide 2, registry 6.
- **Category table: 15 rows**, 5 columns, including the hand-written "what it means".
- **Registry columns: 5** (code, category, owner, since, description); 4 are generated, 1 is
  hand-written.
- **Namespacing:** every code is `<domain>.<NAME>`; the domain segment is required.
- **Acme registry: 214 codes** across 9 domains; 0 codes without an owner.
- **Generation:** 3 outputs (registry markdown, category table, machine-readable JSON).
- **Onboarding task time: 25 min** with the decision guide; the same task took 3 days before
  it existed.
- **Drift caught by the registry check: 41** false codes in the first month (the grep
  problem), then **3–6 real ones per quarter**.

## Real-world use case — Acme SaaS, the wiki that lied

Acme's `checkout-api` had a `ERRORS.md` written in 2023 by the original author. It was
**1,100 lines**, and it was wrong in ways nobody could see.

| Claim in `ERRORS.md` | Reality | When it was found |
| ------------------- | ------- | ----------------- |
| "Codes are defined in `src/errors.ts`" | Codes are in `src/features/*/codes.ts` | New engineer, day 2 |
| "`409` means a duplicate order" | `409` also covers idempotency conflicts and quota conflicts | During a client integration |
| "Database errors return `500`" | `40001` and `40P01` return `503` and are retried | During a deadlock storm |
| "Stripe errors are always `502`" | Rate-limit errors from Stripe return `429` | During a Stripe rate limit |
| "Errors are retried 3 times" | 5 in the payment path, 3 elsewhere | During a duplicate charge |
| "Unknown errors return `500` with `INTERNAL_ERROR`" | They return `502` with `PROVIDER_REJECTED` | By a partner, in production |

The replacement was **four documents totalling 11 pages** plus a generated registry, and the
`ERRORS.md` was deleted. The single-page reduction was possible because most of the 1,100
lines were a hand-maintained table of 180 codes — the same information the generator now
produces, correctly.

The interesting part is what did **not** change: nobody on the team became a better writer.
The fix was structural. The 1,100-line document was a *data* problem wearing a *document*'s
clothes, and data problems are solved by generation, not by discipline.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One `ERRORS.md` for everything | One place to look | Serves nobody; drifts fastest | Never past 50 codes |
| Four layered documents | Each serves its audience | Four files to keep in sync | The default |
| Generated everything | Cannot drift | Descriptions need a human | Use for tables; write prose |
| Wiki only | Editable by anyone | No CI check; drifts silently | Alongside, never instead |
| Docs in the code only | Cannot drift | Hard to read as a set | For single-purpose libraries |
| Diagrams only | Fast to read | Cannot be checked mechanically | As a supplement |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep one fact in one home and link to it | Re-type a status in three documents |
| Generate the registry and the category table | Maintain 214 rows by hand |
| Write a "what it means" sentence per category | Publish a table of identifiers only |
| Put the description next to the code | Keep descriptions in a separate wiki |
| Size documents by audience | Write one document for four audiences |
| Delete a document when it is replaced | Keep the old one "for reference" |

## Common mistakes

- **The prose document that describes a table.** A hand-written table of 200 codes is a
  spreadsheet with a typo rate.
- **The grep-based generator.** It finds comments and string literals; the result is a
  registry full of codes that do not exist.
- **The wiki as the source of truth.** It is the easiest place to write and the hardest place
  to check.
- **The document nobody owns.** An unowned document is stale within one release.
- **The architecture document that describes only the happy path.** Architecture documents
  about error handling must describe the failure path or they are not about error handling.

## Checklist

- [ ] The set has four layers, one audience each, plus a generated registry.
- [ ] Every category has a one-sentence "what it means".
- [ ] Every code has an owner, a `since`, and a one-sentence description.
- [ ] The registry and the category table are generated and committed.
- [ ] The generation uses an AST scan, not a text grep.
- [ ] No document exceeds 6 pages; the whole set is under 20 pages.
- [ ] Every document is owned by a team.

## Related

- [Documenting External Contracts and Policies](./02-documenting-external-contracts-and-policies.md)
- [Keeping Docs Aligned with Behavior](../02-deep-dive/01-keeping-docs-aligned-with-behavior.md)
- [Doc Drift Detection and CI Gates](../02-deep-dive/02-doc-drift-detection-and-ci-gates.md)
- [Chapter 49 — Error Contract Design and Versioning](../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
