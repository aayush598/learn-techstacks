# Chapter: Abstraction

## What you'll learn
- The precise definition of **abstraction** — hiding implementation details and exposing only the essential contract — and how it differs from encapsulation (the dedicated comparison section).
- The mechanics of `abstract` classes and `interface` in Java: what each can/cannot contain, when to choose which, and the modern "prefer interfaces" guidance (plus its exceptions).
- How **interfaces** work in Java, Go (structural interfaces, implicit satisfaction), and C# (interface + default methods, `IComparable` culture).
- How to "program to an interface, not an implementation" — the discipline that makes DI, testing, and SOLID work.

## Prerequisites (linked)
- [Chapter 01 — Encapsulation](../../part-02-encapsulation-and-abstraction/chapter-01-encapsulation/README.md): abstraction sits on top of hidden state.
- [Part 01, Chapter 01 — Four Pillars](../../part-01-oops-fundamentals/chapter-01-introduction-to-oops/section-04-four-pillars-of-oops-overview.md): pillars vocabulary.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Abstraction in Depth](section-01-abstraction-in-depth.md) | What abstraction is, what it hides, levels of abstraction, "program to an interface" |
| [Section 02 — Abstract Classes vs Interfaces](section-02-abstract-classes-vs-interfaces.md) | Decision table: state/constructors/code-reuse vs contract/polymorphism; Java rules |
| [Section 03 — Interfaces in Java, Go, and C#](section-03-interfaces-in-java-go-and-c-sharp.md) | Nominal vs structural typing; default methods; Go's implicit satisfaction |
| [Section 04 — Encapsulation vs Abstraction](section-04-encapsulation-vs-abstraction.md) | The two pillars, contrasted precisely; one-line answers for interviews |

## One-paragraph narrative connecting all sections
Abstraction is the design strategy that says "show what it *does*, hide how it *does it*" (Section 01). In Java the tool set is two-fold: `abstract` classes (partial implementation + shared state, for genuine is-a with code) and `interface` (pure contract, for capabilities and polymorphism) — the choice is a decision table, not a preference (Section 02). Languages differ in how they realize the contract — Java's nominal interfaces with default methods, Go's structural interfaces that are satisfied implicitly, C#'s interface + extension culture — but the *purpose* is identical (Section 03). Finally, abstraction and encapsulation get sharply distinguished so you can answer the most-asked comparison question without blurring the two (Section 04).

## Common interview trap in this chapter
Candidates conflate the three: (1) "encapsulation = abstraction" — no; (2) "interfaces are just abstract classes with no state" — partially true, but the design intent differs (capability contract vs partial implementation); (3) "Go has no interfaces" — Go *has* interfaces, they're just *structural* (satisfied implicitly), which is a bigger difference than most candidates realize. Also, "always prefer interfaces" has real exceptions (shared state + template methods legitimately need abstract classes).

## Checklist before moving on
- [ ] I can define abstraction in one sentence with a real-world analogy.
- [ ] I can fill the abstract-class-vs-interface decision table (state? constructors? multiple? template method?).
- [ ] I can write a Java `interface` with a `default` method and explain Java 9 private methods.
- [ ] I can explain Go's structural typing and why a type "satisfies" an interface implicitly.
- [ ] I can compare Java, Go, and C# interfaces in 3 bullets.
- [ ] I can give the 30-second "encapsulation vs abstraction" answer.
