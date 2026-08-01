# Chapter: SOLID Principles

## What you'll learn
- **S — Single Responsibility Principle (SRP)**: a class should have one reason to change; how to identify and split responsibilities; why "just do one thing" is too vague.
- **O — Open/Closed Principle (OCP)**: open for extension, closed for modification; how polymorphism and interfaces make extensions safe.
- **L — Liskov Substitution Principle (LSP)**: subtypes must be substitutable for their base type; the preconditions/postconditions/invariants contract; real-world violations (square-rectangle, fly-bird).
- **I — Interface Segregation Principle (ISP)**: no client should depend on methods it doesn't use; fat interfaces and how to split them.
- **D — Dependency Inversion Principle (DIP)**: depend on abstractions, not concretions; the difference between DIP and DI; how DIP powers OCP.
- For each: definition, motivation, violations with fixes, code, traps, and interview answers.

## Prerequisites (linked)
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md): OCP, LSP, and DIP are *built on* interfaces and overriding.
- [Part 05 — Relationships](../../part-05-association-aggregation-composition/README.md): DIP is about which side the association arrow points.
- [Part 02 — Abstraction](../../part-02-encapsulation-and-abstraction/README.md): SRP/ISP assume clean encapsulation.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Single Responsibility Principle (SRP)](section-01-single-responsibility-principle-srp.md) | One reason to change; the most violated principle |
| [Section 02 — Open/Closed Principle (OCP)](section-02-open-closed-principle-ocp.md) | Open for extension, closed for modification |
| [Section 03 — Liskov Substitution Principle (LSP)](section-03-liskov-substitution-principle-lsp.md) | Subtypes must be substitutable; behavioral contracts |
| [Section 04 — Interface Segregation Principle (ISP)](section-04-interface-segregation-principle-isp.md) | Don't force clients to depend on methods they don't use |
| [Section 05 — Dependency Inversion Principle (DIP)](section-05-dependency-inversion-principle-dip.md) | Depend on abstractions; DIP vs DI |

## One-paragraph narrative connecting all sections
SOLID is one idea in five costumes: **depend on stable contracts, keep each unit narrow and swappable.** SRP (Section 01) keeps a class narrow so it has one reason to change; OCP (Section 02) then lets you *extend* behavior without reopening that class — by plugging in new implementations behind a stable contract. That contract is safe only if subtypes honor it, which is exactly LSP's job (Section 03): if a subclass silently changes the base's guarantees, every polymorphic caller breaks. ISP (Section 04) keeps the contracts themselves narrow, so no client is coupled to methods it never calls. And DIP (Section 05) is the meta-principle: it says those narrow, stable contracts must be owned by the *client* side and the implementation must point toward them — which is what makes OCP physically achievable. Read together: narrow units (SRP), swappable behind contracts (OCP), contracts honored (LSP), contracts narrow (ISP), contracts own the dependencies (DIP).

## Common interview trap in this chapter
Candidates memorize the one-liners and fail the *application*. The four traps: (1) **SRP as "does one thing"** — SRP is about *reasons to change*, not line count; a 20-line method can still have one responsibility. (2) **OCP as "never modify anything"** — OCP means no *structural* modification for new behavior, not "the file never changes"; you still fix bugs. (3) **LSP as "same signature"** — LSP is a *behavioral* contract: `Bird`→`Ostrich` passes the type check and breaks the design because `fly()` is a precondition the subclass can't satisfy. (4) **DIP vs DI** — Dependency Inversion (a design principle) is not the same as Dependency Injection (a wiring technique that *implements* it); saying "DIP is passing dependencies through the constructor" conflates the two. And the meta-trap: applying SOLID to every three-line helper is over-engineering — principles are for units with real change pressure.

## Checklist before moving on
- [ ] I can state all five principles in one sentence each, in order.
- [ ] I can explain SRP via "reasons to change" with a concrete violation→fix.
- [ ] I can explain OCP with an interface/Strategy example and say when it's overkill.
- [ ] I can explain LSP with a behavioral (not just signature) violation, e.g., Square-Rectangle or Bird-Ostrich.
- [ ] I can explain ISP with a fat interface split and name the Java standard-library example (`java.awt.event`).
- [ ] I can distinguish DIP from DI and draw the dependency-direction diagram for a controller/service/repository.
- [ ] I can answer "which principle does this code violate?" for typical god-class, switch-statement, and fat-interface examples.
