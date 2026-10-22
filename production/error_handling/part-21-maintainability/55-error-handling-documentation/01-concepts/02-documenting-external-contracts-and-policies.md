# Documenting External Contracts and Policies

> Part XXI · Chapter 55 · Sections 55.4, 55.5, 55.6 · _Estimated reading time: 18 min_
> **Prerequisite:** [The Documentation Set and Its Layers](./01-the-documentation-set-and-its-layers.md)

## In one sentence

The external contract document states **what a caller sees and may do**, and the policy
document states **what the system does on failure** — retry, recovery, fallback, ownership —
each in a table that can be checked against the code.

## Why this matters in production

Two audiences need the truth at the worst possible moment: the **caller** deciding whether to
retry, and the **on-call engineer** deciding what to do. Both are reading documentation
during an incident, when a vague sentence costs minutes.

The classic failure is the retry rule. A contract that says "some errors are retryable" is
useless; a contract that says "retry on `503` with exponential backoff, up to 3 attempts,
total 10 s; do not retry `409`" can be implemented by a client in an afternoon — and it can
be **checked**.

## Core concept

### 55.4 — Public API errors

The public API error contract answers six questions, in this order:

1. What does an error response look like?
2. Which codes can I receive?
3. Which of them should I retry, and how?
4. What does a code I do not recognise mean?
5. What must never appear in a response?
6. What changes, and how will I know?

#### 1. The shape

The body is RFC 9457 problem details plus two Acme fields:

```json
{
  "type": "https://acme.dev/problems/conflict",
  "title": "Conflict",
  "status": 409,
  "detail": "Order is already paid.",
  "instance": "/v1/orders/ord_8812",
  "code": "checkout.ORDER_ALREADY_PAID",
  "request_id": "req_7f2c9ab1"
}
```

| Field | Type | Guaranteed |
| ----- | ---- | ---------- |
| `type` | URI | yes — a stable URI per category |
| `title` | string | yes — the public code of the category |
| `status` | number | yes — the HTTP status |
| `detail` | string | yes — a human-readable, safe message |
| `instance` | string | when a resource path is known |
| `code` | string | yes — the registered, namespaced code |
| `request_id` | string | yes — quote it in a support request |

The contract states that `detail` is **not** a stable string to match on: it may be
reworded. The stable identifiers are `code` and `status`.

#### 2. The code list

The contract lists the codes a client can receive, grouped by what the client should do
about them:

| Do not retry | Retry with backoff | Do not retry, escalate | Never expected |
| ------------ | ------------------ | ---------------------- | -------------- |
| `validation.*` | `external_api_transient.*` | `data_integrity.*` | anything unregistered |
| `business.*` | `database_transient.*` | `internal.*` | |
| `conflict.*` | `dependency_unavailable.*` | | |
| `auth.*` | `resource_exhausted.*` | | |
| `not_found.*` | `rate_limit.*` | | |
| `external_api_permanent.*` | | | |
| `external_api_ambiguous.*` (poll instead) | | | |

The "Never expected" column exists because of the next question.

#### 3. Unknown codes

This is the paragraph most contracts omit and most clients need:

```text
  If you receive a `code` you do not recognise:
    • Treat it as `internal` — do not retry automatically, and do not parse `detail`.
    • Treat `status` as authoritative: retry only 503 and 429, with backoff.
    • Log the `code` and the `request_id`; they identify the failure exactly.
    • Do not treat the response as a malformed response — the request was processed.
```

Why this matters: the contract is **versioned separately from the implementation**. A client
written against version 3 will meet codes added in version 5. The rule that keeps that safe
is the status-code rule, because HTTP statuses are a much smaller set than Acme's codes.

#### 4. What never appears

The contract promises what will not be disclosed, which is a promise a client can rely on:

| Never in a response | Why |
| ------------------- | --- |
| A stack trace | Leaks implementation structure |
| The internal `message` | Leaks vendor wording, IDs, and sometimes PII |
| The `cause` chain | Leaks internal calls and, sometimes, credentials |
| A database table or column name | Leaks schema |
| A raw provider payload | Leaks another vendor's contract and data |
| A stack of internal services | Leaks topology |

#### 5. The stability promise

| Change | Client impact | Version |
| ------ | ------------- | ------- |
| A new code is added | Possible | minor |
| A new category is added | Possible | major |
| A status changes | **Breaking** | major |
| A `detail` is reworded | None | minor |
| A field is added to the body | Possible | minor |
| A field is removed | **Breaking** | major |

### 55.5 — Retry policies

The retry document is a table, and every column in it is a number a reader can act on:

| Category | Attempts | Base delay | Max delay | Total deadline | Honours `Retry-After` | Retries the same request |
| -------- | -------- | ---------- | --------- | -------------- | --------------------- | ------------------------ |
| `external_api_transient` | 3 | 250 ms | 4 s | 10 s | yes | only if idempotent |
| `database_transient` | 3 | 100 ms | 1 s | 5 s | no | only if idempotent |
| `dependency_unavailable` | 2 | 500 ms | 2 s | 6 s | yes | only if idempotent |
| `rate_limit` | 2 | 1 s | 5 s | 15 s | yes | no — the request is counted |

Four columns do the real work, and they are the ones that are usually missing:

- **Total deadline**, because "3 attempts" with unbounded backoff is not a bound.
- **`Retry-After` honoured**, because a provider's hint is better than your guess.
- **"Only if idempotent"**, because this is the column that prevents duplicate charges.
- **The `rate_limit` exception**, because a rate-limited request that is retried immediately
  makes the limit worse.

The document also states the two rules that the table cannot express:

1. **Never retry a non-idempotent write** unless the request carries an idempotency key.
2. **Never retry `external_api_ambiguous`.** The provider may have accepted the request; the
   correct action is to poll for the outcome, not to send it again.

### 55.6 — Recovery behavior

Retry is one recovery action out of six. The policy document lists them all, and says what
the system does in each case:

| Action | Meaning | Example | User-visible result |
| ------ | ------- | ------- | ------------------- |
| `fail` | Stop; return the error | Card declined | An error response |
| `retry` | Try again under the retry policy | Deadlock | An error response after the retries |
| `degrade` | Serve a reduced result | Search index down | Partial results, flagged |
| `compensate` | Undo the earlier half of a saga | Payment succeeded, provisioning failed | The order is cancelled |
| `terminate` | Stop the process or job | Data-integrity violation | The job is dead-lettered; a human is paged |
| `resolve_later` | Defer the decision | Unknown provider outcome | `202` + a status the client polls |

Two details make the difference between a useful policy document and a decorative one:

- **`degrade` is not silent.** A degraded response says so: a `partial: true` flag, or a
  header, or a `X-Degraded: search` header. A degraded result that looks complete is a lie
  the client will act on.
- **`resolve_later` has a poll contract.** The `202` response includes a status URL and a
  `Retry-After`, and the status endpoint returns `pending` or `resolved`. "We will sort it
  out later" is not a behaviour; a poll endpoint is.

## How it works (mechanics)

How the policy tables stay true:

```text
  the code                          the document
  ───────────────────────────────   ──────────────────────────────
  CATEGORY_POLICY (package)    ──▶ CATEGORY-POLICY.md  (generated)
  RETRY_POLICIES  (package)    ──▶ POLICIES.md retry table (generated)
  recovery.action (package)    ──▶ POLICIES.md recovery table (generated)
  codes + description (service)──▶ REGISTRY.md (generated)
  ───────────────────────────────   ──────────────────────────────
  hand-written: the "what it means" column, the rationale, the
  client-facing rules that no table expresses
```

The split is the same as everywhere else in this part: **tables are generated, reasoning is
written**. The CI check regenerates and diffs; a mismatch fails the build.

The client-facing rules that no table can express are the ones a human must write, and they
are short: the unknown-code paragraph, the idempotency rule, the "do not retry
`external_api_ambiguous`" rule, and the stability promise.

## Worked example

A partner integrates against the Acme API and hits an error they do not understand. Their
integration retries everything with a `503` rule copied from a blog post.

The partner's log:

```text
  2024-11-03 10:22:14  POST /v1/orders          → 409 checkout.ORDER_ALREADY_PAID
  2024-11-03 10:22:14  POST /v1/orders          → 409 checkout.ORDER_ALREADY_PAID
  2024-11-03 10:22:19  POST /v1/orders          → 409 checkout.ORDER_ALREADY_PAID
  2024-11-03 10:22:24  POST /v1/orders          → 409 checkout.ORDER_ALREADY_PAID
```

Four identical orders. The contract says, in the "do not retry" column, that `conflict` is
not retryable, and in the "unknown codes" paragraph that `status` is authoritative — `409`
is not `503` or `429`.

Had the contract been generated correctly, the partner's client would have been:

```text
  status 503 or 429  → retry with backoff
  status 409         → do not retry; treat as a business outcome
  any other status   → do not retry; log code + request_id
```

The value of the contract is not that it explains errors. It is that it makes a **correct
client implementable without reading the source**.

## Key data / numbers

- **Contract questions: 6**; **body fields: 7**; guaranteed fields: **6** of 7.
- **Code list in the contract:** 4 groups by client action, covering all 15 categories.
- **Never disclosed: 6** classes of information.
- **Retry table: 4 columns of numbers per row** (attempts, base delay, max delay, deadline)
  plus 2 policy columns.
- **Retry limits:** max **3** attempts, max delay **4 s**, max total deadline **15 s**.
- **Recovery actions: 6** (`fail`, `retry`, `degrade`, `compensate`, `terminate`,
  `resolve_later`).
- **Rules no table can express: 3** (unknown code, idempotency, ambiguous outcome).
- **Contract version:** the API contract is versioned with the API, not with the code.
- **Measured effect at Acme:** partner retry storms on `409` went from **6 incidents/quarter**
  to **0** after the contract was published with an explicit "do not retry" column.

## Real-world use case — Acme SaaS, the `503` that was not retryable

Acme's billing service returned `503` for two very different conditions, because the code
translated a "circuit open" and a "deadlock" and a "provider quota exceeded" all into
`DEPENDENCY_UNAVAILABLE`.

A client with the standard rule — "retry `503` up to 5 times" — then retried a **quota
exceeded** error, which:

1. Wasted the client's quota budget and made the exhaustion worse.
2. Delayed the response by **up to 40 s** (5 attempts with backoff), turning a fast failure
   into a timeout.
3. Generated **31% of all inbound requests** during a 12-minute incident window.

The fix was three-part, and only the first was a code change:

| Fix | What it changed |
| ---- | --------------- |
| Split the categories | `resource_exhausted` (429-style, do not retry) is now distinct from `dependency_unavailable` (503, retry) |
| Documented it | The contract's "do not retry" and "retry with backoff" columns now place them in different groups |
| Checked it | The contract table is generated from `CATEGORY_POLICY`, so the two cannot disagree again |

The second and third fixes are this chapter's point: the code change alone would have been
undone by the next provider integration, because the *documented* rule would still have
said "retry `503`".

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Generated tables + hand-written rules | Cannot drift on the data | Two kinds of content to maintain | The default |
| Fully hand-written contract | Total control of wording | Drifts; 200-row tables | Only for small contracts |
| Machine-readable contract only (OpenAPI) | Generates client code | Not readable by humans | Alongside the prose contract |
| Prose only | Readable | Uncheckable | Never alone |
| Changelog only | Easy to publish | No current-state reference | As an addition |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Publish the "do not retry" group explicitly | Leave retryability to be inferred |
| State the total deadline, not just attempts | Say "retries a few times" |
| Say what happens for an unknown code | Assume the client knows your codes |
| Say what is never disclosed | Let "we don't leak internals" be implied |
| Mark a degraded response as degraded | Return partial results that look complete |
| Give `resolve_later` a poll contract | Say "it will be resolved later" |
| Version the contract with the API | Version the contract with the implementation |

## Common mistakes

- **The retry table without a deadline.** Three attempts with 30 s backoff is a 90-second
  request, and the client times out before the server gives up.
- **The contract that lists codes but not actions.** 200 codes with no guidance is a data
  dump.
- **The stability promise that is not kept.** A `detail` string that clients match on is a
  de facto API, and it will be changed.
- **The silent degradation.** A partial response without a marker, and the client treats the
  missing rows as "no data".
- **The ambiguous outcome treated as failure.** An `external_api_ambiguous` returned as `500`
  leads the client to retry a payment that already succeeded.

## Checklist

- [ ] The body shape is documented, with the guarantee level of every field.
- [ ] Codes are grouped by what the client should do, not by subsystem.
- [ ] The unknown-code rule is written down.
- [ ] The never-disclosed list is written down.
- [ ] The retry table has attempts, delays, max delay, and a total deadline.
- [ ] The idempotency rule and the ambiguous-outcome rule are stated.
- [ ] All six recovery actions are described, with their user-visible result.
- [ ] Degraded and deferred results are marked as such.

## Related

- [The Documentation Set and Its Layers](./01-the-documentation-set-and-its-layers.md)
- [Ownership, Propagation, and Boundaries](./03-ownership-propagation-and-boundaries.md)
- [Chapter 49 — Error Contract Design and Versioning](../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
