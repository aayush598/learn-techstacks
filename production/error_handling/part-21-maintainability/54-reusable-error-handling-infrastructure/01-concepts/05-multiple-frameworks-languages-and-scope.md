# Multiple Frameworks, Languages, and Scope

> Part XXI · Chapter 54 · Sections 54.13, 54.14, 54.15, 54.19, 54.20 · _Estimated reading time: 19 min_
> **Prerequisite:** [Reusable API and Job Handling](./04-reusable-api-and-job-handling.md)

## In one sentence

A shared package supports **many frameworks and many languages** by sharing the *data* and
the *contract*, never the *code* — and it stops being reusable the moment it grows
configuration.

## Why this matters in production

Two shapes of reuse fail in organisations that have more than one service:

- **The polyglot package.** A "universal" package that tries to serve TypeScript, Go, and
  Python services. It ends up with a lowest-common-denominator API, a runtime-specific
  escape hatch, and a compatibility matrix nobody maintains. Every consumer uses the
  escape hatch, so the package provides no consistency.
- **The per-language copy.** A core package in TypeScript, a "core" in Go, and a "core" in
  Python — three implementations of the same tables. The tables drift, which is the exact
  problem the package was built to solve.

The resolution is to separate **the contract** from **the implementation**. The contract is
data: it can be a JSON file, a YAML file, or a generated table. The implementation is
per-language and small.

## Core concept

### 54.13 — Multiple frameworks

Supporting several frameworks in one language is easy, because the shared adapter is a
**pure function**. Each framework contributes a thin wrapper.

```text
  @acme/errors/adapters/http-core.ts     ← the pure function (framework-free)
        │
        ├── http-express.ts     ~20 lines
        ├── http-fastify.ts     ~20 lines
        ├── http-koa.ts         ~20 lines
        └── http-native.ts      ~20 lines
```

The cost of supporting the fourth framework is **~20 lines and one test file**. The cost of
supporting the second *language* is entirely different, and is where the design has to
change.

### 54.14 — Multiple languages

Across languages, share the **data**, not the code.

```text
  ┌──────────────────────────────────────────────────────────────┐
  │  THE SHARED ARTIFACT: a contract, expressed as data         │
  │                                                              │
  │   contracts/error-catalog.yaml   (categories, statuses,      │
  │                                  recovery, retry defaults)   │
  │   contracts/codes/<domain>.yaml  (codes, categories, owner) │
  └──────────────────────────────────────────────────────────────┘
        │                    │                     │
        ▼                    ▼                     ▼
   TypeScript core        Go core              Python core
   (@acme/errors)         (internal pkg)       (internal pkg)
```

Each language implements the **same four responsibilities**: a type, a factory, a mapper
interface, and a registry loaded from the shared data. The implementations are small
because the *decisions* — the categories, the statuses, the policies — live in the data.

The rule that makes this work: **the shared artifact is the only place a category, a status,
or a recovery action is written down.** The per-language packages implement mechanics; they
never invent a category.

| Shared in data | Implemented per language |
| -------------- | ------------------------ |
| Category list and their statuses | The `AppError` type |
| Recovery action per category | The factory and the redactor |
| Retry policy defaults | The mapper interface |
| Code registries (per domain) | The boundary adapter |
| Public message wording | The HTTP problem-details builder |

The cost of the data-driven approach: **a build step**. The YAML is compiled into each
language's registry (TypeScript: a generated `.ts` file; Go: `go:generate`; Python: a
generated module). That build step is worth it, because it turns "the tables must match"
from a convention into a **generated artefact that cannot differ**.

If a build step is unacceptable, the fallback is to publish the tables as JSON and load
them at startup, with a test that asserts the loaded tables match a checksum. That is worse
— it moves a compile-time error to a startup error — but it is still better than three
hand-maintained copies.

### 54.15 — Avoiding a universal framework

The universal framework is the failure mode that looks most like success. The test is
precise:

> **If a consumer needs a configuration option the core does not have, the core is
> wrong — or the consumer is doing something the core should not support.**

A shared core that grows an option per service is no longer shared: it is a set of
per-service configurations with a common import path. The tell-tale signs:

| Sign | What it means |
| ---- | ------------ |
| The core has a `configure()` or a settings object | It is a framework |
| Consumers pass options to the core's functions | The core's API is not stable enough |
| The core has a plugin registry | It is a platform, and it is a framework |
| The core's behaviour differs by environment | The contract is not the contract |
| The core exports a `Utils` namespace | It has no idea what it is for |
| Two consumers need different behaviour from one call | The call is doing two things |

The last row is the one to act on. A core function whose behaviour must differ per consumer
is doing two things; split it. The reason this matters is that "different behaviour per
consumer" inside a core is precisely how a shared package becomes unusable: the second
consumer's requirement changes the first consumer's behaviour, and the version bump
reaches everybody.

### 54.19 — Customization rules

Customisation is necessary — a service will need something the core does not have. The
rules decide where that something lives.

| Rule | Statement | Rationale |
| ---- | --------- | --------- |
| **R1** | Extend by **adding data** (codes, registry rows), not by overriding behaviour | Data changes are additive; behaviour changes are breaking |
| **R2** | The core's behaviour is identical in every consumer | Otherwise there is no shared contract |
| **R3** | A consumer may wrap a core function, but may not change it | Wrapping is visible; monkey-patching is not |
| **R4** | A need that recurs in **2+** consumers is proposed to the core | One consumer's need is a local extension |
| **R5** | A local extension is a separate package or module, not a patch to the core | The core stays small and upgradable |
| **R6** | The core never imports from a consumer | The dependency direction is one-way, always |
| **R7** | A new core capability requires an ADR | It changes the contract for everyone |

R4 is the rule that decides the package's future, and it is the one that requires discipline:
a need that appears twice is *evidence*, not a mandate. The correct response is a proposal
with the two use cases attached, not a silent addition.

R7 exists because core changes have a blast radius that code review does not show: a new
core capability is a new promise to every consumer, including the ones nobody asked about.

### 54.20 — The reference architecture

The whole part, assembled:

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │  CONSUMERS (11 services)                                         │
  │  checkout · billing · exports · webhooks · agent · notifications  │
  │                                                                   │
  │  Each service has:                                                │
  │    src/platform/errors.ts      ← 3 lines of wiring                │
  │    src/features/<domain>/codes.ts  ← its own codes (data only)     │
  └──────────────────────────────┬────────────────────────────────────┘
                                 │ depends on
                                 ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │  @acme/errors  (1,240 lines · 10 modules · 16 exports)             │
  │                                                                   │
  │  core/     types · factory · registry · category-policy          │
  │  adapters/ http-core · jobs · pg · stripe · llm                  │
  │  policies/ retry · recovery · fallback                            │
  └──────────────────────────────┬────────────────────────────────────┘
                                 │ reads (generated)
                                 ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │  contracts/ (data)  error-catalog.yaml · codes/*.yaml            │
  │  Owned by the platform team; changed by ADR.                     │
  └───────────────────────────────────────────────────────────────────┘
```

Five properties of the reference architecture, each of which is a decision:

1. **The core is a leaf.** It imports nothing from the services.
2. **The contracts are data.** They can be consumed by other languages.
3. **The services own their codes.** Codes are domain knowledge; the platform does not need
   to approve a new error.
4. **The platform owns the categories.** A category means a status and a policy; letting
   services define their own is how the divergence returns.
5. **The wiring is 3 lines.** The adoption cost is what determines whether the package is
   used at all.

## How it works (mechanics)

How a service adopts the package, step by step:

```text
  Day 1  npm install @acme/errors
         copy 3 lines of wiring
         run the shared adapter — you now have a consistent contract

  Day 2  move your domain codes into src/features/<domain>/codes.ts
         register them with defineRegistry()

  Day 3  replace the hand-written status mapping with statusFor(code)
         delete the old branches

  Week 2 move vendor handling into an adapter, or use a shared one
         delete the feature-level provider handling
```

The adoption is **incremental and reversible**. Nothing requires a big-bang migration, and
each step is independently valuable — which is the property that makes adoption actually
happen.

## Worked example

Acme's billing service was written in Go while everything else was TypeScript. Rather than
maintaining a Go copy of the tables, Acme made the **contract** the shared artefact.

```yaml
# contracts/error-catalog.yaml — the single source of truth
version: 3
categories:
  validation:
    httpStatus: 422
    publicCode: VALIDATION_FAILED
    recovery: fail
    retryable: false
  external_api_transient:
    httpStatus: 503
    publicCode: DEPENDENCY_UNAVAILABLE
    recovery: retry
    retryable: true
    retry:
      maxAttempts: 3
      baseDelayMs: 250
      maxDelayMs: 4000
      jitter: true
      totalDeadlineMs: 10000
```

Both languages read the same file. TypeScript gets a generated module; Go gets a generated
struct table:

```go
//go:generate go run ./tools/gen-errors -in ../../contracts/error-catalog.yaml -out internal/errscatalog
```

The Go service then does:

```go
policy := errscatalog.Category[errscatalog.ExternalAPITransient]
resp := errshttp.Write(w, err, policy)
```

The result: **one** table, two implementations of the mechanics, and a **CI check** that
regenerates both and fails if the generated files differ from the committed ones. The
check takes **4 seconds** and has caught **2** drift attempts (a hand-edited generated file
in each language) before review.

The cost: a code-generation step, and one extra repository for the contracts. The benefit:
the Go service and the TypeScript services **cannot** disagree about what a category means,
which was the whole point of the package.

## Key data / numbers

- **Framework wrapper: ~20 lines** per framework; adding a framework costs **1 file + 1
  test**.
- **Languages supported: 3** at Acme (TypeScript, Go, Python) over **~14 months**; each
  added language cost **~5 days** of work, mostly the code generator.
- **Core LOC per language: 300–450** (types, factory, mapper, registry loader). The shared
  *decisions* are in the data, so the per-language cost is mechanics, not policy.
- **Configuration points in the core: 0**; in the adapters: **1** (the mapper list).
- **Core exports: 16** (ceiling **25**).
- **Core LOC: 1,240** across **10 modules** (ceiling **2,000** before it needs splitting).
- **Customisation rules: 7** (R1–R7); R4's threshold is **2+ consumers** before a core
  proposal.
- **Generated-artifact drift check: 4 s** in CI; caught **2** hand edits.
- **Contract version:** the YAML catalog carries `version: 3`, bumped on any breaking
  change to a category's meaning.
- **Wiring per service: 3 lines**; full adoption **~3 days** of work for a mid-size service.

## Real-world use case — Acme SaaS, the framework that wanted to be everything

Acme's platform team received a proposal: make `@acme/errors` support *every* service's
needs by adding a configuration object. The proposal's list of options ran to **23 items**:
per-service status overrides, per-category retry overrides, custom public messages, custom
serialisation, custom correlation-id sources, custom logging hooks, and so on.

The signs from Chapter 54's table were all present: a `configure()` call, options passed at
every call site, a plugin registry, and behaviour that differed by consumer.

The team applied one question — *if a consumer needs a configuration option the core does not
have, is the core wrong, or is the consumer doing something the core should not support?* —
to each of the 23 options:

| Option | Verdict |
| ------ | ------- |
| Per-service status overrides (7 options) | The core is wrong: statuses are keyed by category, so a service needing a different status needs a different *category*, and that is a core proposal |
| Per-category retry overrides (5) | The core is wrong for the same reason — retry is keyed by category |
| Custom public messages (1) | Local: a service may want a different *wording* — but that is a **code** property, so it belongs in the code's own registry row |
| Custom serialisation (1) | The core is wrong: RFC 9457 is the contract, and a service that needs a different wire format has a different audience (a partner API) |
| Custom correlation-id sources (2) | Local: the adapter takes the id as input |
| Custom logging hooks (3) | Local: the core does not log; the service does |
| Everything else (4) | Local or core-proposal, per the table |

Result: **1 option** was adopted (custom wording, via the code's own registry row),
**2** became core proposals, and **20** were resolved as local customisation that required
no core change. The configuration object was never built.

The measurable outcome: the package went from `1.4.2` to `2.0.0` with **no new
configuration**, and the **11** consuming services were unaffected by the major bump because
the only breaking change was a *category rename* with a compatibility alias.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One package, one language | Simplest | Other languages drift | The default |
| Contract as data, core per language | No cross-language drift | Build step; per-language mechanics | Polyglot organisations |
| One package per language, hand-maintained | No build step | Tables drift — the original problem | Only with 1–2 languages and a strict CI check |
| A single universal framework | "One solution" | Configuration; unusable in practice | Never |
| No shared package | No coordination | Full duplication | Small organisations |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Share the contract as data across languages | Try to share the code across languages |
| Generate the registry per language | Hand-maintain the same table twice |
| Keep the core's behaviour identical everywhere | Add a setting that changes one consumer's behaviour |
| Propose a core change when 2+ consumers need it | Add a core feature for one consumer |
| Keep local extensions outside the core | Patch the core from a consumer |
| Require an ADR for a new core capability | Add a core capability in a routine PR |
| Wire the package in 3 lines | Make adoption require a migration project |

## Common mistakes

- **The polyglot attempt.** One package with a lowest-common-denominator API and a runtime
  escape hatch. Every consumer uses the escape hatch.
- **The configuration object.** 23 options that are 20 local customisations and 3 core
  proposals.
- **The "one consumer needs it" core change.** It changes the contract for 10 consumers who
  did not ask.
- **The per-language hand-maintained copy.** Three copies of the category table, drifting.
- **The migration requirement.** If adopting the package requires rewriting the service
  first, nobody adopts it.

## Checklist

- [ ] The core has zero configuration points and identical behaviour in every consumer.
- [ ] Cross-language reuse goes through a data contract, not shared code.
- [ ] Generated registries are verified in CI against the source contract.
- [ ] Local extensions live outside the core, and a 2-consumer rule governs core proposals.
- [ ] A new core capability has an ADR.
- [ ] Adoption requires 3 lines of wiring, not a migration project.

## Related

- [Reusable API and Job Handling](./04-reusable-api-and-job-handling.md)
- [Versioning Shared Packages Without Breaking Consumers](../02-deep-dive/01-versioning-shared-packages-without-breaking-consumers.md)
- [The Starter Template and Customization Rules](../02-deep-dive/02-starter-template-and-customization-rules.md)
- [Chapter 47 — Language-Level Error Semantics](../../part-18-languages-and-frameworks/47-language-level-error-semantics/README.md)
