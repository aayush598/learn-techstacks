# Ownership, Propagation, and Boundaries

> Part XXI · Chapter 55 · Sections 55.7, 55.8, 55.9 · _Estimated reading time: 17 min_
> **Prerequisite:** [The Documentation Set and Its Layers](./01-the-documentation-set-and-its-layers.md)

## In one sentence

Three rules make error handling navigable: **every code has an owner**, **every error
crosses exactly one boundary on its way out**, and **nothing translates in the middle** — the
middle only propagates.

## Why this matters in production

Most "who owns this error?" conversations are really "whose code is this?" questions in
disguise. The answer is usually in a file nobody remembers, and the incident burns twenty
minutes while three engineers read each other's code.

Propagation and boundary rules solve a different problem: the one where the same error
becomes five different errors on its way up the stack, and nobody can tell which one is
real. A stack trace that shows `Error: unknown` at the top and `PgError: duplicate key` at
the bottom has lost the information that matters.

## Core concept

### 55.7 — Ownership

Ownership is documented per **code**, not per service, and it answers two questions at once:
who is paged, and who decides to change the code.

| Column | Meaning | Example |
| ------ | ------- | ------- |
| `owner` | The team paged when this code fires | `payments` |
| `steward` | The team that decides its category and wording | `payments` |
| `reviewers` | Who must approve a change to it | `payments`, `platform` |
| `source` | The file where the code is defined | `src/features/checkout/codes.ts` |

The `owner` and the `steward` are usually the same team, and the split only matters when
they are not — which is exactly when an error crosses an organisational boundary.

The documentation rule is simple: **an error belongs to the domain that decided, not the
domain that detected.** A `checkout.ORDER_ALREADY_PAID` belongs to `checkout` even though it
was raised by the payment adapter, because checkout decided what an already-paid order
means. The `owner` is who gets paged; the `steward` is who decides.

The consequence for the registry is a rule that can be checked:

| Rule | Check |
| ---- | ----- |
| Every code has an owner | The registry check fails on a missing `owner` |
| The owner is a team, not a person | A validation step rejects a name that is not a team |
| A code's owner is the deciding domain | Reviewed, not mechanically checkable |
| An error from a dependency keeps the dependency's owner for the *cause* | The `cause` records the provider, not a team |

That last row is the subtle one. A `stripe` error inside a checkout flow has two owners:

- The **cause** is owned by `payments` (the team that owns the Stripe integration).
- The **mapping** — deciding that a Stripe decline becomes `checkout.CARD_DECLINED` — is
  owned by `checkout`.

The documentation says so explicitly, because at 3 a.m. "who do I page" is answered by the
*category*, not by the stack frame.

### 55.8 — Propagation rules

Propagation rules describe **what happens to an error as it moves up**. There are exactly
five behaviours, and each one is a decision the code makes:

| Behaviour | What happens | When to use it |
| --------- | ------------ | -------------- |
| **Pass through** | The error is re-thrown unchanged | The layer has nothing to add |
| **Enrich** | Context is added; the category and code stay the same | The layer knows something the caller does not |
| **Translate** | The error becomes a different code or category | The layer converts an external failure into a domain one |
| **Wrap** | A new error is raised with the original as `cause` | The layer adds a *decision* ("we cannot proceed") |
| **Handle** | The error is absorbed and a fallback is returned | The layer has a better answer than an error |

And three rules that constrain the choices:

| Rule | Statement | Why |
| ---- | --------- | --- |
| **P1** | **Translation happens exactly once**, at a boundary | Two translations produce a code that means neither thing |
| **P2** | **Enrichment never changes the category** | If it does, it was a translation, and it belongs at a boundary |
| **P3** | **Handling requires a fallback that is documented** | An undocumented fallback is a silent behaviour change |

The propagation rules are documented as a table of layers, because that is the form a
reader needs:

| Layer | May | Must not | Typical behaviour |
| ----- | --- | -------- | ----------------- |
| HTTP handler | Translate, handle | Enrich (the boundary has no upstream to inform) | Translate to the public body |
| Service / use case | Enrich, translate | Handle unless a fallback is documented | Translate a provider error into a domain code |
| Repository | Enrich | Translate, handle | Enrich with the query name and row count |
| Adapter | Translate | Handle | Translate a vendor error into a category |
| Domain | Enrich | Translate, handle | Enrich with the entity and the operation |

That table is the whole of "how do I raise an error here" for a new engineer, and it is
checkable in review because each row is a verb.

### 55.9 — Boundary placement

A boundary is **where an error stops being internal and becomes a response, a job failure,
or an event**. Every service has several; each one is a place where the shape of the error
changes.

| Boundary | Input | Output | What changes |
| -------- | ----- | ------ | ------------ |
| HTTP request | An exception | A problem-details body | Code → body, category → status, everything else dropped |
| Queue job | An exception | A job-failure record | Category → `failed` / `retryable` / `dead_lettered` |
| Event publish | An exception | An outbox row or a failed publish | Category → `defer` / `fail` |
| Scheduled task | An exception | A task-run record | Category → the task's own outcome |
| Third-party callback | An incoming request | An acknowledgement | Their code → our code, with a public body they can read |

The placement rules:

| Rule | Statement |
| ---- | --------- |
| **B1** | **One translation per boundary.** The boundary is the only place a code becomes a status. |
| **B2** | **The boundary is the only place that logs.** One log line per failed request, with the request id. |
| **B3** | **The boundary is the only place that redacts.** The factory redacts context; the boundary decides what is disclosed. |
| **B4** | **A boundary never invents a code.** It maps an existing code to a response; an unmapped code becomes `internal`. |
| **B5** | **The boundary is the only place with a default.** Unmapped, unknown, and unmappable all become `internal` — explicitly, in one place. |

B4 and B5 together are the rule that makes the "unknown code" question answerable: a code
that is not in the registry does not exist, and the boundary says so with `internal`.

The documentation shows the boundary as a diagram, because a diagram answers "where does
this happen" in one glance:

```text
  HTTP request
      │
      ▼
  ┌──────────────┐   translate   ┌─────────────────┐
  │ handler      │ ────────────▶ │ toProblemDetails│
  │ (enrich)     │               └────────┬────────┘
  └──────┬───────┘                        │ 500 + INTERNAL_ERROR
         │                                ▼
         ▼
  ┌──────────────┐   translate   ┌─────────────────┐
  │ service      │ ────────────▶ │ category → code │
  │ (domain)     │               └─────────────────┘
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐   translate   ┌─────────────────┐
  │ adapter      │ ────────────▶ │ vendor → category│
  └──────────────┘               └─────────────────┘
```

Each arrow is one translation, and each one is in exactly one place. This is the picture
that stops the "same error, five shapes" problem.

## How it works (mechanics)

The documentation set's three rules-oriented documents are written from the same three
tables, and each table is generated or checked:

| Document | Source of truth | Check |
| -------- | --------------- | ----- |
| Ownership table | The registry's `owner` column | Every code has an owner; the owner is a known team |
| Propagation table | A hand-written layer table | A CI check compares the listed layers with the directory layout |
| Boundary diagram | A hand-written diagram | A test asserts each boundary has exactly one translator registered |

The last check is the interesting one. Acme's boundary test counts translators by kind:

```ts
it("registers exactly one translator per boundary kind", async () => {
  const counts = countTranslators();
  expect(counts.http).toBe(1);
  expect(counts.job).toBe(1);
  expect(counts.event).toBe(1);
  expect(counts.callback).toBe(1);
});
```

It exists because a service once had **two** HTTP translators — one added during a
framework migration — and they disagreed on the `rate_limit` status. The count check found
it in four seconds.

## Worked example

A new service, `notifications`, has a "send email" feature that calls a third-party
provider. The team writes its propagation rules before the code:

```text
  src/features/notification/adapter.ts
      raises:        translate   provider error → notification.PROVIDER_UNREACHABLE
                    (external_api_transient)
  src/features/notification/service.ts
      raises:        enrich      add { notificationId, channel } to the context
                    (no translation)
  src/http/notification-handler.ts
      boundary:      translate   AppError → problem body (409, 422, 503)
```

Now a question from review — "should `service.ts` translate a provider error into
`notification.PROVIDER_UNREACHABLE`?" — has a documented answer: **no, the adapter
translates; the service enriches**. The service is not allowed to re-map, because then the
adapter and the service would both translate, and the code in the response would depend on
which one ran last.

The benefit shows up in the incident review, six weeks later. A `503` arrives, the log line
is:

```text
  code=notification.PROVIDER_UNREACHABLE category=external_api_transient
  provider=mailgun attempt=2 request_id=req_7f2c9ab1
```

The reader does not need to know which layer raised it, because the propagation table
guarantees that a code means the same thing wherever it was raised.

## Key data / numbers

- **Ownership columns: 4** (owner, steward, reviewers, source); **2** are mechanically
  checked.
- **Propagation behaviours: 5** (pass through, enrich, translate, wrap, handle).
- **Propagation constraints: 3** (P1–P3); **boundary rules: 5** (B1–B5).
- **Layer table: 5 rows** (HTTP handler, service, repository, adapter, domain), each with a
  "may / must not / typical" triple.
- **Boundary kinds: 5** (HTTP, job, event, scheduled task, callback).
- **Translation count per boundary: exactly 1** — enforced by a test.
- **Teams owning codes at Acme: 9**; codes with no owner: **0**.
- **Drift the boundary test found:** 2 duplicate translators in 2 years, in **4 s** of
  runtime.
- **Documentation cost:** the propagation and boundary documents are **2 pages** together.

## Real-world use case — Acme SaaS, the error that changed on the way up

A `WebhookIngest` failure reached the HTTP boundary as `INTERNAL_ERROR` (500), and the
on-call engineer spent **25 minutes** discovering that the actual cause was a
`authentication failure` in the payment provider's webhook verification — because two
layers translated the same error and the inner one won.

The translation chain was:

```text
  stripe error  (StripeError: signature verification failed)
      │  translated by the adapter      → category: auth, code: webhook.SIGNATURE_INVALID
      ▼
  service layer
      │  "the webhook is not ours"        → translated again, code: webhook.UNKNOWN_EVENT
      ▼
  HTTP boundary
      │  unknown code                    → default: INTERNAL_ERROR, status 500
      ▼
  client
```

Two violations, both of which the documentation now prevents:

- **P1 broken:** translation happened twice, at two layers.
- **B4 broken:** the boundary invented a code for an unmapped case instead of mapping the
  code it was given.

The fix was a one-line change in the service (do not re-translate) plus the two rules that
made the fix permanent. The on-call runbook gained a line:

```text
  A webhook failure with status 401 is a signature problem, not an auth problem.
  A webhook failure with status 500 means the code was not mapped — check the propagation
  table before you check the provider.
```

The measurable result: the next similar incident was diagnosed in **4 minutes** instead of
25, because the runbook told the reader which layer to look at first.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Ownership per code | Precise paging | Many rows | The default |
| Ownership per service | Simple | Pages the wrong team | Small services, one team |
| Ownership per category | Few rows | Blurs team boundaries | Only when teams are the same |
| Central translation | One place | The middle cannot adapt | Small systems |
| Per-layer translation | Flexible | Translation drift (P1) | Never without P1 |
| Enrich everywhere | Rich context | Context can contradict the code | With P2 |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Assign ownership per code | Leave codes with no owner |
| Own the error where the decision was made | Own it where it was detected |
| Translate once, at a boundary | Translate at every layer |
| Enrich without changing the category | Re-map an error in a layer that "knows better" |
| Document the layer verbs | Leave "how do I raise an error here" to tribal knowledge |
| Log once, at the boundary | Log at every level as the error propagates |
| Map an unmapped code to `internal` explicitly | Invent a new code at the boundary |

## Common mistakes

- **The boundary that invents a code.** The default path usually skips the registry, and the
  client sees a code that means nothing.
- **The two translators.** A framework migration adds one and forgets to remove the other.
- **The log at every layer.** The same failure produces five log lines, and the fifth is
  the one an engineer reads, and it is the least useful.
- **The owner that is a person.** People leave; teams do not.
- **The propagation table that is prose.** "Errors should be wrapped as appropriate" tells a
  reader nothing they can apply.

## Checklist

- [ ] Every code has an owner, and the owner is a team.
- [ ] The ownership column is generated and checked for completeness.
- [ ] The five propagation behaviours are defined and the layer table names the allowed verb
  per layer.
- [ ] Translation happens at exactly one place per boundary.
- [ ] The boundary rules are documented (B1–B5).
- [ ] Exactly one translator is registered per boundary kind.
- [ ] Logging happens once, at the boundary.
- [ ] The ownership and propagation documents are under 2 pages together.

## Related

- [The Documentation Set and Its Layers](./01-the-documentation-set-and-its-layers.md)
- [Transactional Failure, Limitations, and Exceptions](./04-transactional-failure-limitations-and-exceptions.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
