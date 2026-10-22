# The Starter Template and Customization Rules

> Part XXI · Chapter 54 · Sections 54.18, 54.19 · _Estimated reading time: 19 min_
> **Prerequisite:** [Versioning Shared Packages Without Breaking Consumers](./01-versioning-shared-packages-without-breaking-consumers.md)

## In one sentence

A starter template is a **project that already contains a correct, minimal error-handling
setup** — and the customization rules are the contract that keeps it correct as each project
diverges.

## Why this matters in production

Most SaaS projects start with a blank repository and a team's habits, and habits are not
transferable. The result is the same five problems in every new service: a `500` for
validation errors, no request id in the response, a `catch` that logs and swallows, a retry
that retries a declined card, and a stack trace in the body.

A template fixes this once. The template's job is not to be *complete* — it is to be
**correct in the smallest number of decisions**, so that a new project inherits good
behaviour by default and only has to make choices that are genuinely its own.

The risk of a template is the opposite: it is usually too big. A template with 40 files and
a code-generation step is adopted by nobody.

## Core concept

### 54.18 — The starter template

A good starter template has **three properties**:

| Property | Test | Budget at Acme |
| -------- | ---- | -------------- |
| **Adoptable in an afternoon** | A new project is wired and running in < 4 h | 2 h 40 m |
| **Correct by default** | The happy path and one failure path work with zero edits | — |
| **Minimal** | Nothing in it is optional | **11 files, 430 lines** |

The template is **not** the shared package. That distinction matters:

| | Starter template | Shared package |
| - | -------------- | -------------- |
| What it is | A copyable project skeleton | An installed dependency |
| Who owns it | each project (it is copied) | the platform team |
| How it changes | it does not — it is a starting point | it evolves, with semver |
| What it contains | project structure + wiring + one example feature | the shared core and adapters |
| Size | 11 files, ~430 lines | 10 modules, ~1,240 lines |

The template **references the package**; it does not re-implement it. That is the rule that
keeps the template from becoming a second, divergent copy of the core.

### The template's file list

```text
  templates/minimal-service/
    README.md                          ← what this is, and the 3 steps to adopt
    package.json                       ← the dependency, one script: "check:errors"
    tsconfig.json
    .env.example
    src/
      platform/
        errors.ts                      ← 3 lines of wiring  (the whole integration)
        logger.ts                      ← one log line per failure, no more
        request-context.ts             ← correlation id + request id
      features/
        example/
          codes.ts                     ← the feature's own codes (data)
          service.ts                   ← a worked example: result type + expected failures
          handler.ts                    ← the boundary call
      http/
        server.ts                      ← the framework wiring
    test/
      error-contract.test.ts           ← asserts the response shape (copied from the package)
    docs/
      ERROR-HANDLING.md                ← 1 page: the 6 questions, filled in
```

**430 lines, 11 files.** Compare with a typical "standard" internal template: 60 files, a
code generator, a custom logger abstraction, an ORM wrapper, and a config system — the
template had become a framework with a `create-project` command.

### The three adoption steps

```text
  Step 1  cp -r templates/minimal-service my-service && cd my-service
  Step 2  npm install @acme/errors && npm run check:errors
  Step 3  Replace the example feature with your first real feature.
```

That is the whole onboarding. The template's `README.md` says exactly this and nothing else,
because a template that requires a 30-minute reading is not adopted.

### What the template gets right by default

These are the decisions a new project should not have to make:

| Decision | The template's answer |
| -------- | --------------------- |
| What a validation failure returns | `422` with the shared body |
| What an unknown error returns | `500` with `INTERNAL_ERROR` and no detail |
| Where the stack trace goes | The log, never the response |
| Is a request id present | Always, in the body and the log |
| How are errors logged | Once, at the boundary, with the category |
| What is retried | Only `*_transient` categories, per the shared policy |
| Where a new code is added | `src/features/<feature>/codes.ts` |
| What the public body looks like | The shared RFC 9457 body |

Notice what is **not** in the list: the taxonomy, the retry policy details, the framework
choice. Those come from the package or from the project, and the template does not need to
re-state them.

### 54.19 — Customization rules

A template is copied, so it *will* diverge. The rules decide whether the divergence is
**safe divergence** (a genuinely different context) or **accidental drift** (a copy that
stopped being maintained).

| # | Rule | Statement | Why |
| - | ---- | --------- | --- |
| **C1** | **Never fork the core** | The package is a dependency, always | A fork is a divergent copy with no updates |
| **C2** | **Never edit the wiring** | `src/platform/errors.ts` is 3 lines and stays 3 lines | The wiring is where the contract is established |
| **C3** | **Extend with codes, not categories** | A new code is local; a new category is a package proposal | A category means a status and a policy |
| **C4** | **Keep the example feature** | Replace it, but keep the shape | The example is the reference implementation |
| **C5** | **Keep the contract test** | `error-contract.test.ts` is not optional | It is what proves the service still honours the contract |
| **C6** | **Document deviations in one file** | `docs/ERROR-HANDLING.md` has a "Deviations" section | Drift that is written down is manageable |
| **C7** | **Re-sync annually** | Diff against the current template | A template that never syncs becomes a set of siblings |

C7 is the rule that most templates lack, and its absence is why templates rot. Acme's
template is versioned — `templates/minimal-service@2.1.0` — and the annual re-sync produces
a diff that is reviewed by the platform team and applied service by service.

C6 is the rule that makes divergence safe. A service that must answer `403` where the
shared contract says `401` writes it in the "Deviations" section of its `ERROR-HANDLING.md`
and implements it in its own registry override. The deviation is visible to the next
engineer, in the same document that explains the rest of the service's error handling.

### The customization decision table

| You need to… | Do this | Not this |
| ------------- | ------- | -------- |
| Add a new failure mode | Add a code in the feature's `codes.ts` | Add a category to the shared table |
| Change a message | Set `publicMessage` on the code's registry row | Edit the shared policy table |
| Use a different status | Define a **new category** and propose it to the package | Change the shared category's status |
| Retry more or less | Override the **retry policy** for that category in the service's registry | Change the shared retry table |
| Use a different wire format | Write a service-local boundary adapter (and document it under C6) | Edit the shared adapter |
| Add context fields | Extend the context allowlist in the service's config | Disable redaction |
| Add a new dependency | Write an adapter implementing `ErrorMapper` | Add vendor code to the feature |

## How it works (mechanics)

How a project stays aligned with the template over time:

```text
  template@1.0 ──▶ project A ─┐
  template@2.0 ──▶ project B ─┼──▶ annual re-sync ──▶ diff ──▶ apply ──▶ note deviations
  template@2.1 ──▶ project C ─┘
```

The re-sync is a **diff**, not a copy: the project keeps its own code and applies the
template's changes. The result of the re-sync is reviewed by the platform team, and any
project that cannot apply a change records it as a deviation under C6.

The annual cadence is a compromise. More often is better but costs more; less often and
the drift grows. Acme runs it **annually**, and the re-sync diffs average **40 lines** per
project — small enough to review, large enough to matter.

## Worked example

A new Acme service, `notifications`, created from the template.

```text
  Day 1, hour 1   cp -r templates/minimal-service notifications
                  npm install @acme/errors
                  npm run check:errors          → passes

  Day 1, hour 2   Replace the example feature with the real one:
                    features/notification/codes.ts   (4 codes)
                    features/notification/service.ts (result type, 3 outcomes)
                    features/notification/handler.ts (one boundary call)

  Day 1, hour 3   Write the contract test for the new codes.
                  Run the check.

  Day 1, hour 4   Deploy to staging. Send a deliberately invalid request.
                  The response is the shared body with a request id.
```

Total: **~4 hours**, and the service's error contract was already correct before the first
line of business logic was written.

Compare with the previous service Acme built, `agent`, which started from a blank
repository:

| | `notifications` (template) | `agent` (blank repo) |
| - | -------------------------- | --------------------- |
| Time to a correct error contract | **4 h** | 6 days |
| Stack traces in responses during the first month | 0 | 3 (fixed after 2 incidents) |
| Missing `request_id` | 0 | 2 services' worth of responses |
| Validation errors returned as `500` | 0 | 41 in the first week |
| Retries of non-idempotent writes | 0 | 1 (a duplicate email, then a fix) |
| Code review of error handling | 5 min/PR | 18 min/PR |

The template did not make `notifications` a better-designed service. It made its **error
contract** correct on day one, which is the part that is expensive to retrofit.

### The template's own test suite

The template ships a contract test, so a project cannot accidentally break the contract:

```ts
// test/error-contract.test.ts
import { expect, it } from "vitest";
import { validateProblemBody } from "@acme/errors/adapters/http-core";

it("every error response matches the shared contract", async () => {
  const response = await request(app).post("/example/notifications").send({});
  const body = await response.json();

  expect(response.status).toBe(422);
  expect(() => validateProblemBody(body)).not.toThrow();
  expect(body.request_id).toBeTruthy();
  expect(body.stack).toBeUndefined();
});
```

The test asserts the **contract**, not the implementation. It survives a package upgrade, a
framework change, and a rewrite of the handler. It is also the test that catches the most
common regression in a copied codebase: someone adding `stack: err.stack` to the response
"just for debugging".

## Key data / numbers

- **Template size: 11 files, ~430 lines**, plus 2 configuration files.
- **Adoption time: 2 h 40 m** median across 4 projects; target < 4 h.
- **Wiring: 3 lines** in `src/platform/errors.ts`; the rule is that it stays 3 lines.
- **Template versioning:** `templates/minimal-service@2.1.0`; re-synced **annually**.
- **Re-sync diff: ~40 lines** per project, reviewed by the platform team.
- **Customization rules: 7** (C1–C7); C1 (never fork) and C5 (keep the contract test) are
  the two that are checked in review.
- **Template contract test: 4 assertions** (status, body shape, `request_id` present, no
  stack).
- **Measured comparison (template vs blank repo):** correct contract in **4 h** vs **6
  days**; stack-trace leaks **0 vs 3**; validation-as-`500` **0 vs 41**; error-handling
  review **5 min vs 18 min** per PR.
- **Deviations:** each project records them in `docs/ERROR-HANDLING.md`; Acme has **11**
  projects and **9** recorded deviations, of which **2** were later proposed to the package.
- **Template file budget: ≤ 15 files.** Above that, the template is a framework.

## Real-world use case — Acme SaaS, the template that was too good

Acme's first template was **47 files**: a custom logger, a config loader, an ORM wrapper, a
generated client, a "base repository", and an `error/` folder with 11 files. It took **2 days**
to adopt properly and **4 hours** to copy badly.

The measurable result: **6 of 9** services created from it in a year **deleted the error
folder** and wrote their own. Two of them reinvented the mapping (and produced the
divergence the package was built to eliminate). One kept it and then had to apply the
package's `2.0.0` contract change to **11 files** by hand.

The second template was built with the opposite bias: **11 files, 430 lines, and a rule
that every behaviour comes from the package.** The adoption instructions were three lines
in the README.

The result was the opposite of the first: **9 of 11** services created from the second
template still have the template's `platform/errors.ts` **unchanged** 14 months later, and
the annual re-sync diff for them is under 20 lines.

The lesson recorded in the template's ADR:

> **A template's job is to make the correct thing the default, not to be complete.** Every
> file the template contains is a file a project must maintain, copy, or delete. If a
> project can get a behaviour from the package, the template must not contain it.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| A full "standard project" template | Complete; opinionated | 2 days to adopt; nobody adopts it | Rarely |
| A **minimal** template referencing a shared package | Adopted in hours; stays correct | Assumes the package exists | The default |
| A command-line generator | Fast, consistent | Another tool to maintain; version drift | When the package does not exist |
| Copy-paste snippets in a wiki | Zero tooling | Diverges immediately | Never as the only mechanism |
| No template; a documented standard | No artefacts to maintain | Every project re-decides | Small organisations (≤ 3 services) |
| A monorepo template | One copy to maintain | Only works in a monorepo | Monorepo organisations |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the template under 15 files | Ship a 47-file "standard project" |
| Make the template reference the package | Re-implement the core inside the template |
| Keep the wiring at 3 lines | Put configuration in the wiring |
| Keep the example feature and the contract test | Delete the contract test as "not needed yet" |
| Version the template and re-sync it | Assume copied code stays current |
| Record deviations in one file | Let deviations live in code |
| Propose a new category to the package | Add a local category table |

## Common mistakes

- **The complete template.** Every file is a maintenance obligation for every project.
- **The template that re-implements the package.** The template becomes a second core, and
  the two drift.
- **The template without a contract test.** The first "just for debugging" stack trace
  lands in production.
- **The unversioned template.** Six months later nobody can tell which projects are
  current.
- **The template that requires a decision on day one.** If adopting the template requires
  choosing a logger, a config system, and an ORM, it is a framework.

## Checklist

- [ ] The template is ≤ 15 files and ≤ 500 lines.
- [ ] The template references the shared package; it does not copy the core.
- [ ] Adoption takes under 4 hours and is 3 steps.
- [ ] The template ships a contract test that projects keep.
- [ ] The template is versioned, and there is an annual re-sync.
- [ ] Deviations are recorded in the project's `ERROR-HANDLING.md`.
- [ ] The wiring in `platform/errors.ts` is 3 lines.

## Related

- [Versioning Shared Packages Without Breaking Consumers](./01-versioning-shared-packages-without-breaking-consumers.md)
- [Multiple Frameworks, Languages, and Scope](../01-concepts/05-multiple-frameworks-languages-and-scope.md)
- [The `@acme/errors` Package Skeleton](../03-practical-examples/01-the-acme-errors-package-skeleton.md)
- [Chapter 50 — Error Handling as an Engineering Standard](../../part-19-contracts-and-governance/50-error-handling-as-an-engineering-standard/README.md)
