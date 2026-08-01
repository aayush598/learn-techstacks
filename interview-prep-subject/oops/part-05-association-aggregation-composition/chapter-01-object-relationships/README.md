# Chapter: Object Relationships

## What you'll learn
- The precise difference between the four relationship kinds: **dependency** (uses), **association** (knows/has-a, neither side owns the other), **aggregation** (has-a, shared/loose ownership — parts outlive the whole), and **composition** (has-a, strict ownership — the whole owns the part's lifecycle).
- How to map each relationship to real Java/C++/Python code: fields, constructor injection, factories, `new`, weak vs strong references, and garbage-collection/lifetime consequences.
- How to decide between **aggregation and composition** in a design — ownership is a life-or-death (lifecycle) decision, not a style choice.
- How to **read and draw UML class diagrams**: class boxes, association/aggregation/composition/dependency notation, multiplicity (1, 0..*, 1..*), roles, and navigability arrows.

## Prerequisites (linked)
- [Part 01 — OOPs Fundamentals](../../part-01-oops-fundamentals/README.md): what an object *is* — a relationship is just an object holding references to others.
- [Part 03 — Inheritance](../../part-03-inheritance/README.md): generalization (inheritance) is the fifth UML relationship, drawn as an open triangle.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Association, Aggregation, and Composition](section-01-association-aggregation-and-composition.md) | The relationship taxonomy: dependency → association → aggregation → composition, and ownership/lifecycle semantics |
| [Section 02 — UML Class Diagrams for OOPs](section-02-uml-class-diagrams-for-oops.md) | The diagram language: boxes, relationships, multiplicity, roles, navigability — read and draw it |

## One-paragraph narrative connecting all sections
A relationship in code is simply *one object holding a reference to another* — but the *kind* of that reference encodes real design decisions (Section 01): a dependency is "uses and forgets", an association is "knows about", aggregation is "has, but shares", and composition is "owns, and will destroy with me" — the difference between aggregation and composition is **lifecycle ownership**, which is why `Car` composes `Engine` but only aggregates `Wheel` suppliers and merely associates with `Driver`. Once you've chosen the semantics, you express them on paper in **UML class diagrams** (Section 02): a class box per type, an open-diamond for aggregation, a filled-diamond for composition, plain lines for association, dashed arrows for dependency, with multiplicities (`1`, `*`, `0..1`) and role labels making the intent unambiguous — the universal diagram language that lets you design an object model *before* writing it and discuss it with other engineers (and interviewers).

## Common interview trap in this chapter
Candidates blur aggregation and composition — "both mean has-a, what's the difference?" The difference is **ownership and lifecycle**: in composition the whole creates/destroys the part (part cannot exist alone — a `House` composes `Room`), in aggregation the whole merely references the part and the part can outlive it (a `House` aggregates `Furniture`). Second trap: treating association as a distinct concrete relationship vs it being the *umbrella* term for has-a links, with aggregation/composition being the two specializations. Third trap: forgetting that in **UML, the diamond is on the *owning/whole* side** — the filled diamond sits next to the composite class, not the part.

## Checklist before moving on
- [ ] I can rank the four relationships weak→strong (dependency → association → aggregation → composition) with one example each.
- [ ] I can state the exact aggregation-vs-composition difference (ownership/lifecycle) and give a concrete code example of each.
- [ ] I can map each relationship to code: constructor-injected field, `new` in constructor, method-local use, static method use.
- [ ] I can explain when composition is worth it vs aggregation (lifecycle, sharing, GC implications).
- [ ] I can read a UML class diagram and draw one: boxes, diamonds, arrows, multiplicity, roles.
- [ ] I can draw generalization (inheritance) as the open-triangle arrow in UML.
