# Part XXI — Error Handling for Maintainability and Developer Productivity

> **Chapters 53–55.** Every previous part told you how to design correct error handling. This
> part asks the question that decides whether it survives the next two years of hiring:
> **can a developer who has never seen this codebase change it safely in ten minutes?**

## Why this part exists

Error handling has a brutal property: it is the part of a system that only becomes visible
when something is already going wrong, and it is written by whoever happened to be nearest the
incident. Left alone, it decays into three failure modes:

- **Repetition.** The same Postgres `23505` → `409` mapping is written in six places. One gets
  updated; five do not.
- **Abstraction sprawl.** A "unified error framework" grows 4,000 lines, has nine configuration
  points, and is understood by one person.
- **Documentation drift.** The wiki says retries stop at three attempts. The code says five. The
  operator's runbook is wrong, and the runbook is read at 3 a.m.

None of these are design errors in the usual sense. They are **maintenance** failures, and they
cause production failures in exactly the same way a flaky service does.

This part gives you three tools:

1. **Reduce complexity deliberately** (Chapter 53) — find the repetition, decide what deserves
   an abstraction, and keep the easiest path the correct one.
2. **Build reusable infrastructure that stays reusable** (Chapter 54) — a core library, standard
   interfaces, adapters, and a versioning policy that does not break consumers.
3. **Document the behaviour you actually have** (Chapter 55) — and keep the documents aligned
   with the code automatically.

## Learning objectives

By the end of Part XXI you will be able to:

1. **Measure** error-handling complexity (duplication ratio, decision-site count, boilerplate
   lines per feature) and use the numbers to prioritise refactors.
2. Run an **abstraction cost analysis** on a candidate helper and decide — with evidence —
   whether it earns its keep.
3. Design a **reusable error-handling package** (core type, factory, mapping interface, retry
   policies, HTTP adapter, job adapter) that a second project can adopt without a rewrite.
4. Apply **semver rules to an error package** so that adding a code, adding an adapter, or
   deprecating a code never breaks a consumer.
5. Produce an **error-handling documentation set** — architecture, categories, registry, public
   API errors, policies, ownership, propagation, boundaries, fallbacks, transactional behaviour,
   limitations, and exceptions.
6. **Detect documentation drift mechanically** in CI rather than discovering it during an
   incident.
7. Write an **onboarding guide** that takes a new engineer from "I have never seen this
   codebase" to "I can add a new error safely" in under an hour.

## Chapters

| # | Chapter | Focus | Files |
| - | ------- | ----- | ----- |
| 53 | [Reducing Error-Handling Complexity](./53-reducing-error-handling-complexity/README.md) | Duplication, policy extraction, control-flow simplification, decision locality, boilerplate, the abstraction cost model | 5 concepts, 2 deep-dives, 2 worked refactors |
| 54 | [Reusable Error-Handling Infrastructure](./54-reusable-error-handling-infrastructure/README.md) | Core library, standard interfaces, adapters, shared policies, packaging, semver, starter template, reference architecture | 5 concepts, 2 deep-dives, 2 package builds |
| 55 | [Error-Handling Documentation](./55-error-handling-documentation/README.md) | Documentation layers, registry docs, ownership, propagation and boundary rules, limitations, decision guides, onboarding, drift detection | 5 concepts, 2 deep-dives, 2 document sets |

## The maintenance loop

```text
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   ▼                                                              │
 measure ──▶ decide ──▶ extract ──▶ document ──▶ enforce ──▶ measure
 (53.1)      (53.16)     (53.2)      (55.1)       (55.16)       │
   │                                                              │
   └────────────────────── drift found ───────────────────────────┘
```

The loop is closed by **enforcement**, not by good intentions. A registry entry that nothing
checks will be wrong within two releases; a documented rule that no CI gate protects will be
broken within one sprint.

## The cast in this part

The recurring examples take on maintenance roles here:

| Name | What it teaches in Part XXI |
| ---- | --------------------------- |
| **Acme SaaS** | The multi-service codebase whose error handling was duplicated across three repos |
| **Checkout** | The flow whose translation logic was rewritten by hand in four services |
| **ExportJob** | The job whose failure vocabulary needed a shared contract, not four ad-hoc strings |
| **WebhookIngest** | The consumer whose unknown-code behaviour was never specified for partners |
| **AgentRun** | The feature whose provider-error mapping changed monthly and broke the package version |

## Key data used throughout

| Quantity | Value used in examples | Why it matters |
| -------- | ---------------------- | -------------- |
| Duplication ratio | > 3 occurrences of the same mapping = extract | The third copy is where drift starts |
| Feature error surface | ≤ 2 files, ≤ 120 LOC per feature | A feature's error contract should fit on one screen |
| Decision-site budget | ≤ 1 place per policy question | Two places means they will disagree |
| Abstraction break-even | ≥ 3 call sites **and** ≥ 80 LOC saved | Below that, the indirection costs more than the duplication |
| Package version | `@acme/errors` **2.2.0** — **10 modules**, adapters in the same package | A new adapter is additive; a changed contract is not |
| Breaking-change policy | Additive code = **minor**; contract change = **major** | Matches the blast radius, not the diff size |
| Deprecation window | **2 minor releases** minimum | Consumers need time to migrate |
| Registry sync target | CI fails if a code is missing from the registry | Docs cannot drift from code |
| Drift check | Weekly in CI, ≤ **2 min** runtime | Must be cheap enough to run every commit |
| Review-time target | Error-handling review ≤ **5 min** per PR | Down from a typical 20–30 min |
| Onboarding target | New engineer productive in **< 1 h** | The test of a documented system |

## How to study this part

- Read Chapter 53 first, and apply it to **your own repository** with the measurement
  worksheet in its reference section. Do not skip the measurement; the whole chapter is an
  argument against refactoring by taste.
- Read Chapter 54 only if you have two or more services, or a monorepo with a second package
  boundary. Otherwise, read the "when not to build a package" section and move on.
- Read Chapter 55 whenever you have more than one team consuming your error contract — internal
  teams count.
- The practical files are templates. Copy them, then edit them; do not read them as literature.

## Key takeaways

1. **Complexity in error handling is measured, not felt.** A duplicated mapping is a number
   before it is an opinion.
2. **The easiest path must be the correct path.** If adding a new error takes six edits, teams
   take the shortcut instead.
3. **An abstraction must save more than it hides.** Three call sites and 80 lines saved is the
   break-even; below that, inline the duplication.
4. **Reuse is a package, a version, and a policy** — not a folder of copy-pasted helpers.
5. **The version number is a promise.** Additive changes are minor; contract changes are major;
   deprecations get a window, not a date.
6. **Documentation that is not checked is a memory aid.** Gate the registry, the mapping table,
   and the policy tables in CI.
7. **The measure of the system is the time to change it safely.** Ten minutes to add an error,
   five minutes to review the change, one hour to onboard — those are the targets.

## Exercises

1. Measure your repository: count the files that contain a Postgres `23505` mapping, an HTTP
   status mapping, and a retry decision. Write down the three numbers.
2. Pick the most-repeated mapping in your codebase and run the abstraction cost analysis from
   [Chapter 53](./53-reducing-error-handling-complexity/02-deep-dive/01-abstraction-cost-analysis.md).
   Write down the verdict and the evidence.
3. Draft a one-page `ERRORS.md` for your service: registry table, boundary rules, retry table,
   and the "where do I add a new error" answer. Time the writing; it should be under 30 minutes.
4. Write the CI check that fails when a new error code is not in the registry. Estimate its
   runtime.

## Related

- [Part XX — Error-Handling Correctness and Validation](../part-20-correctness-and-validation/README.md)
- [Part XXII — Advanced Error-Handling Design Decisions](../part-22-design-decisions/README.md)
- [Chapter 45 — Organizing Error-Handling Modules](../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Master index](../README.md) · [Glossary](../GLOSSARY.md)
