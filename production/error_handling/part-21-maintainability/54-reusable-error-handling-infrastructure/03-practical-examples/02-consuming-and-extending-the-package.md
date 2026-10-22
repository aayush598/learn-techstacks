# Consuming and Extending the Package

> Part XXI · Chapter 54 · Sections 54.11–54.15 (applied) · _Estimated reading time: 19 min_
> **Prerequisite:** [The `@acme/errors` Package Skeleton](./01-the-acme-errors-package-skeleton.md), [Multiple Frameworks, Languages, and Scope](../01-concepts/05-multiple-frameworks-languages-and-scope.md)

## In one sentence

Three Acme services consume the same package in three different ways — a **TypeScript
service**, a **Python worker**, and a **Go gateway** — and none of them forks the core.

## Why this matters in production

A shared package is only shared if consuming it is cheap. The moment a team has to fork
it, patch it, or copy a file out of it, the sharing has ended and you have three
codebases with the same name.

Consumption is therefore a design problem, not an install problem. The package has to
answer three questions for a consumer that is not the author:

1. **How do I add my own codes without changing the package?**
2. **How do I map a vendor error without the core learning about my vendor?**
3. **How do I stay on the current major without a migration project?**

The skeleton answers the first two in code. This file answers the third, and shows what the
three consumers actually look like.

## Core concept

### The extension model in one table

| You want to… | Extend the | Not the | Blast radius |
| ------------- | ---------- | ------- | ------------ |
| Add a failure mode | The **registry** (your codes) | The core | None |
| Change the wording of a code | The **registry row** | The core | None |
| Map a new vendor | An **adapter** in your service | The core | None |
| Change a status for a category | Propose a **category** to the package | The core | Major |
| Change the retry policy for a category | Propose a **policy** to the package | The core | Minor |
| Add a whole transport | An **adapter** in the package | Your service | Minor |

The rule underneath the table: **the package grows by proposals, and consumers grow by
configuration of data they own.** A consumer that needs a new category has to argue for it,
which is slow — and correctly so, because a new category is a new status and a new policy
for every consumer.

### Consumer A — the TypeScript service (`checkout-api`)

```ts
// src/platform/errors.ts — the whole integration, 3 lines of wiring
import { toProblemDetails } from "@acme/errors/adapters/http";
import { postgresMapper } from "@acme/errors/adapters/pg";
import { stripeMapper } from "@acme/errors/adapters/stripe";

export const mappers = [postgresMapper, stripeMapper];
export const toProblem = (err: unknown, ctx: BoundaryContext) => toProblemDetails(err, ctx, mappers);
```

```ts
// src/features/checkout/codes.ts — the service's own codes
import { defineRegistry } from "@acme/errors/core";

export const checkoutCodes = defineRegistry("checkout", {
  ORDER_NOT_FOUND:        { category: "not_found",    publicMessage: "Order not found",           owner: "checkout" },
  ORDER_ALREADY_PAID:     { category: "conflict",     publicMessage: "Order is already paid",     owner: "checkout" },
  CARD_DECLINED:          { category: "external_api_permanent", publicMessage: "Your card was declined", owner: "checkout" },
  CARD_GATEWAY_UNREACHABLE: { category: "external_api_transient", publicMessage: "Payment service unavailable", owner: "checkout" },
});
```

Four codes, two categories that are Acme-wide and two that are payment-specific. The
service never writes a status literal, and the package never learns what a "declined card"
is.

### Consumer B — the Python worker (`export-worker`)

The worker is a different language and a different transport, but the **same contract**:

```python
# workers/export_worker/errors.py
from acme_errors import category_policy, to_app_error, JobFailure

CATEGORY = category_policy()          # generated from the shared YAML contract

def handle_export_failure(exc: Exception, attempts: int, max_attempts: int) -> JobFailure:
    app = to_app_error(exc)
    policy = CATEGORY[app.category]
    status = "retryable" if policy.recovery == "retry" and attempts < max_attempts else "failed"
    return JobFailure(
        status=status,
        code=app.code,
        category=app.category,
        reason=app.message,
        attempts=attempts,
        max_attempts=max_attempts,
    )
```

What is shared and what is not:

| Shared (generated from the contract) | Local to the worker |
| ------------------------------------- | ------------------- |
| The 15 categories and their statuses | The worker's own codes (`export.*`) |
| The public body shape | The worker's job-loop plumbing |
| The job-failure field names | The queue library it uses |
| The retry tables | The worker's own backoff preference |

The Python package is **generated** from the same contract, so it cannot drift. Its
generator produces `acme_errors/categories.py` — 15 rows, 4 retry policies, 3 recovery
actions — from the YAML the TypeScript package also reads.

### Consumer C — the Go gateway (`edge-gateway`)

A Go service that never registers codes of its own, because it is a gateway: it maps
upstream responses to the shared contract and nothing else.

```go
// edge-gateway/errors.go
func MapUpstream(status int, body []byte) (int, Problem) {
    var p Problem
    if err := json.Unmarshal(body, &p); err == nil && p.Code != "" {
        return status, p                     // already a shared problem body
    }
    if status == http.StatusTooManyRequests {
        return 429, Problem{
            Type:   problemType("rate_limit"),
            Title:  "Rate limited",
            Status: 429,
            Detail: "Too many requests.",
            Code:   "RATE_LIMITED",
        }
    }
    return 500, Problem{Type: problemType("internal"), Title: "Internal error", Status: 500, Code: "INTERNAL_ERROR"}
}
```

The gateway consumes **the contract, not the library**: it validates and re-emits problem
bodies. This is the "reuse is optional by design" case from the chapter — a consumer that
wants only the table gets only the table.

## How it works (mechanics)

The sequence when a new error code is needed in `checkout-api`:

```text
  1. Add the row to features/checkout/codes.ts
        → category comes from the shared table, publicMessage is local
  2. Raise it:  throw createError("checkout.ORDER_ALREADY_PAID", "order 42 already paid")
  3. The boundary maps it:  409 + the shared body
  4. The CI check runs:
        a. every code in the repo is registered          → pass
        b. every registered code is reachable in a test  → pass
        c. the generated contract is unchanged           → pass
  5. Nothing else changes. No package release is needed.
```

Step 4 is the enforcement. The three checks are the difference between a registry that is
*maintained* and a registry that is *stale*. A code that is registered but never raised is
documentation nobody reads; the reachability check turns it into a failing test.

### The three checks

```ts
// packages/errors/test/coverage.test.ts
import { listRegisteredCodes, scanRaisedCodes } from "@acme/errors/testing";

it("every raised code is registered", async () => {
  const raised = await scanRaisedCodes(repo);       // grep the AST, not the text
  const registered = new Set(listRegisteredCodes());
  const missing = raised.filter((c) => !registered.has(c));
  expect(missing).toEqual([]);
});

it("every registered code is exercised", async () => {
  const exercised = await exercisedCodes(repo);
  const orphans = listRegisteredCodes().filter((c) => !exercised.has(c));
  expect(orphans).toEqual([]);                       // orphans fail the build
});
```

The scan is **AST-based**, not a text grep: a code mentioned in a comment is not a raised
code, and a code built by string concatenation is flagged as dynamic and must be
registered explicitly.

### Staying on the current major

The deep dive covers the semver rules; the consumption rule is simpler:

| Situation | Consumer action | Time |
| --------- | --------------- | ---- |
| Minor upgrade (`1.4.2` → `1.5.0`) | Bump the lockfile; read the changelog | 0 |
| New major available | Read the migration note; run the contract test | 1 h |
| Major changes a status | Update the golden bodies in the consumer's test | 2 h |
| Major removes a code | Migrate to the replacement code; the old one still works | 4 h |

The package publishes a **migration note** with every major, and the note is a table of
"before → after" per affected code. Acme's `2.0.0` note was **14 rows**; the migration
across 11 services took **3 days** in total.

## Worked example — one incident, three consumers

A Stripe outage at 09:14 produces a `429` from the payment gateway. The same failure
reaches three services, and the shared contract keeps the three responses identical.

| Consumer | What it returns | Where it is classified |
| --------- | --------------- | ---------------------- |
| `checkout-api` | `503` + `DEPENDENCY_UNAVAILABLE`, `code: checkout.CARD_GATEWAY_UNREACHABLE` | `external_api_transient` → `503` |
| `export-worker` | Job failure, `status: retryable`, retried 3 times, then dead-lettered | `external_api_transient` → `retry` |
| `edge-gateway` | `503` + the same body, forwarded | forwarded unchanged |

Before the package, the three answers were `500`, "job failed", and `502`. The client's
retry logic could not be written against that. After the package, one status, one code, one
body — and the client's rule is simply "retry `503` with `Retry-After`".

## Key data / numbers

- **Consumers: 3** in this file (TypeScript API, Python worker, Go gateway); **11** at Acme
  in total.
- **Wiring per consumer: 3 lines** in the TypeScript service; **~12 lines** in the Python
  worker; **~20 lines** in the Go gateway.
- **Categories generated per language: 15**; retry policies: **4**; recovery actions: **6**.
- **Consumer-owned codes:** checkout **4**, export **6**, gateway **0**.
- **CI checks: 3** (registered, exercised, contract-unchanged); runtime **4 s**.
- **Migration effort for `2.0.0`: 14 affected rows**, **3 days** across 11 services.
- **Common upgrade cost: 0** for a minor bump, **1 h** for a major bump.
- **Codes added per service per quarter: 8–14**, none of which required a package release.
- **Forks of the package across the estate: 0** since the `1.0.0` release.

## Real-world use case — Acme SaaS, the fork that never happened

In Acme's second year, the `export-worker` team needed to distinguish a **retryable**
provider error from a **terminal** one, and the shared taxonomy did not have the
granularity. The instinct was to fork `packages/errors` into the worker repository.

The rule that stopped it: **a category means a status and a policy**, and the team did not
want a new status — they wanted better metadata on an existing category. So they changed
the extension point instead of the code:

1. They registered **6 worker-local codes** under `export.*` with categories drawn from the
   shared table.
2. They added a `meta` field (`{ provider: "openai", model: "gpt-4o-mini" }`) to the
   registry rows — a field the core already supported and never used.
3. They added a **worker-local adapter** for the provider, implementing the shared
   `ErrorMapper` interface.

Result: **0 lines forked**, **1 adapter of 80 lines** in the worker, and the shared package
was unchanged. The new codes are visible to the platform team through the same telemetry
as every other code, and the next worker that hits the same provider copies an adapter
instead of writing a mapper.

Six months later the platform team **promoted** the worker adapter into the package,
because by then two services needed it — which is the only condition under which the
package should grow.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Generated clients from one contract | Cannot drift | Generation step; language quirks | Multiple languages (this design) |
| Hand-written per language | Full control | Drifts within weeks | One language only |
| HTTP-only consumption (contract, no library) | Zero coupling; works anywhere | Re-implements mapping | Gateways, BFFs, SDKs |
| Fork the package | Instant change | Divergence; nobody merges upstream | Never |
| Service-local error library | No coordination | Two systems to maintain | < 3 services |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Generate per-language clients from one contract | Hand-maintain the same table three times |
| Add codes locally; propose categories upstream | Invent a local category with a new status |
| Consume only the contract where a library does not fit | Force a full library into a gateway |
| Run the reachability check in CI | Let unused codes accumulate for years |
| Publish a migration note with every major | Ship a major with a prose changelog |
| Copy an adapter rather than forking the core | Patch `node_modules` |

## Common mistakes

- **The generated client that nobody regenerates.** The generator exists, but the CI job
  that checks the generated output is not committed — so the "generated" file drifts and
  the drift is invisible.
- **The category added locally.** One service needed a new status, added it, and now three
  clients see four possible statuses for the same failure.
- **The upgrade that was deferred.** Three services stayed on `1.x` for a year, and the
  `2.0.0` migration eventually took a week instead of three days.
- **The gateway that forced the library.** An edge service pulled in a 1,240-line package
  to re-emit a body it never constructed.

## Checklist

- [ ] Every consumer uses the same contract, generated or imported — never re-typed.
- [ ] Consumer-local codes use shared categories only.
- [ ] New categories are proposed to the package, with a status and a policy.
- [ ] CI runs the registered / exercised / contract-unchanged checks.
- [ ] Generated output is committed and verified in CI.
- [ ] Every major release ships a before → after migration table.
- [ ] No consumer forks, patches, or vendored-copies the package.

## Related

- [The `@acme/errors` Package Skeleton](./01-the-acme-errors-package-skeleton.md)
- [Multiple Frameworks, Languages, and Scope](../01-concepts/05-multiple-frameworks-languages-and-scope.md)
- [Versioning Shared Packages Without Breaking Consumers](../02-deep-dive/01-versioning-shared-packages-without-breaking-consumers.md)
- [The Starter Template and Customization Rules](../02-deep-dive/02-starter-template-and-customization-rules.md)
