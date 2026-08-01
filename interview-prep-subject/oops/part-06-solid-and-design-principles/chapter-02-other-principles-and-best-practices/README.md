# Chapter: Other Principles and Best Practices

## What you'll learn
- **DRY, KISS, YAGNI** — the pragmatic guardrails: don't repeat yourself (without over-abstracting), keep it simple (simplicity is the priority), don't build it until you need it; plus **composition over inheritance** as the reuse rule of thumb.
- **Law of Demeter** — "don't talk to strangers": a method should talk only to its immediate collaborators; the concrete cost of train-wreck call chains.
- **Coupling and cohesion** — the two axes that determine maintainability: minimize coupling (inter-module dependence), maximize cohesion (intra-module togetherness); the metric behind every other principle.
- **Code smells and refactoring** — how to recognize design rot (god class, feature envy, long parameter list, shotgun surgery, duplicated code) and refactor toward the SOLID/principles we've covered, safely, step by step.

## Prerequisites (linked)
- [Chapter 01 — SOLID Principles](../chapter-01-solid-principles/README.md): the smells and refactorings *target* SOLID; read the SOLID chapter first.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md): composition-over-inheritance and coupling arguments lean on polymorphic dispatch.
- [Part 05 — Relationships](../../part-05-association-aggregation-composition/README.md): coupling is literally about how many relationship arrows exist.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — DRY, KISS, YAGNI, Composition over Inheritance](section-01-dry-kiss-yagni-and-composition-over-inheritance.md) | The pragmatic triad + the reuse rule of thumb, with their traps |
| [Section 02 — Law of Demeter and Coupling/Cohesion](section-02-law-of-demeter-and-coupling-cohesion.md) | Don't talk to strangers; minimize coupling, maximize cohesion |
| [Section 03 — Code Smells and Refactoring](section-03-code-smells-and-refactoring.md) | Recognize design rot; refactor mechanically and safely |

## One-paragraph narrative connecting all sections
The SOLID chapter told you the *destination*; this chapter is the *map and the potholes*. The pragmatic principles (Section 01) calibrate SOLID — DRY says don't copy behavior, KISS says the simplest thing that works is best, YAGNI says don't build abstractions before you need them, and composition-over-inheritance is the reusable answer to "reuse but don't couple" (which is precisely the *coupling/cohesion* tension in Section 02: cohesion glues a module's parts together, coupling measures the arrows between modules, and the Law of Demeter keeps those arrows short so you don't reach through one object into another's collaborators). And when these principles are *violated* in the wild, you get the recognizable **code smells** of Section 03 — god classes, feature envy, shotgun surgery — which are then removed by *mechanical refactorings* that restore cohesion, reduce coupling, and re-apply SOLID. The chapter closes the loop: principles (Ch. 1) → pragmatism + metrics (this ch.) → detection and repair (smells/refactoring).

## Common interview trap in this chapter
Candidates parrot the acronyms and fail the *trade-offs*. The traps: (1) **DRY over-applied** — abstracting two similar (not identical) blocks into a speculative shared method creates coupling that's worse than the duplication (the "premature abstraction" smell). (2) **KISS confused with "not designing"** — KISS means simplest *correct* solution, not skipping structure you demonstrably need. (3) **YAGNI used to justify bad design** — "we might not need this" is an argument against speculative features, not against testability or a clear seam you already need. (4) **Composition-over-inheritance misread** — it's a *preference*, not a ban: when a genuine is-a with a true contract exists, inheritance is correct. (5) **The Law of Demeter as "no chained calls ever"** — it forbids *transitive* navigation (reaching through strangers), not fluent builders or value-object returns.

## Checklist before moving on
- [ ] I can define DRY/KISS/YAGNI, give one example each, and one counterexample (when NOT to apply).
- [ ] I can state composition-over-inheritance as a *preference* with the is-a/has-a test.
- [ ] I can state the Law of Demeter and refactor a train-wreck (`a.b().c().d()`) properly.
- [ ] I can define coupling and cohesion, give the ideal (low coupling, high cohesion), and name one example of each.
- [ ] I can name at least 6 code smells and state the refactoring technique for each.
- [ ] I can explain why refactoring should be done in small, behavior-preserving steps with tests.
