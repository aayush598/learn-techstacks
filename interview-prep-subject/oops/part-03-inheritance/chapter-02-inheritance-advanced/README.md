# Chapter: Inheritance Advanced

## What you'll learn
- **Composition vs inheritance**: the has-a vs is-a decision, the "favor composition over inheritance" rule, and when inheritance is genuinely the right tool.
- The **diamond problem** in multiple inheritance: why it's ambiguous, and how Java (bans class MI), C++ (virtual inheritance), and Python (MRO/C3) resolve it.
- How **access specifiers** interact with inheritance in Java (`protected`, `public`, package-private) and C++ (`public`/`protected`/`private` inheritance — what each grants).
- **Upcasting/downcasting and polymorphic assignment**: implicit upcasts, explicit downcasts, `instanceof`, `ClassCastException`, and the "program to the base" discipline.

## Prerequisites (linked)
- [Chapter 01 — Inheritance Basics](../chapter-01-inheritance-basics/README.md): you must know `extends`, `super`, and overriding before the advanced material.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md) pairs with upcasting/downcasting.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Composition vs Inheritance](section-01-composition-vs-inheritance.md) | has-a vs is-a; fragile base class; delegation; when inheritance wins |
| [Section 02 — Multiple Inheritance and the Diamond Problem](section-02-multiple-inheritance-and-the-diamond-problem.md) | The diamond, Java's interface-only answer, C++ virtual inheritance, Python MRO |
| [Section 03 — Access Specifiers in Inheritance](section-03-access-specifiers-in-inheritance.md) | Java protected rules; C++ public/protected/private inheritance meaning |
| [Section 04 — Upcasting, Downcasting, and Polymorphic Assignment](section-04-upcasting-downcasting-and-polymorphic-assignment.md) | Implicit upcast, checked downcast, `instanceof`, `ClassCastException`, null-safety |

## One-paragraph narrative connecting all sections
Once you know how inheritance *works*, the advanced material is about *when it's wise*. Inheritance should mirror a true is-a; otherwise composition (has-a) wins — and the "fragile base class" explains why (Section 01). The most dangerous inheritance shape is multiple inheritance, whose diamond ambiguity each language resolves differently (Section 02). Whatever hierarchy you build, access specifiers decide who sees what up and down the tree (Section 03), and casting decides how references move between levels — with `instanceof` guarding every downcast (Section 04). Master these four, and inheritance becomes a deliberate tool instead of a source of design accidents.

## Common interview trap in this chapter
Candidates say "inheritance gives code reuse, so it's good for reuse." The trap: reuse is *not* the primary justification — is-a typing is; using inheritance purely for reuse creates the fragile-base-class and LSP violations. Second trap: "downcasting is fine." Unchecked downcasts throw `ClassCastException` at runtime — the reason LSP + "program to the base" exists. Third: in C++, "private inheritance is like nothing is inherited" — private inheritance *is* inheritance (a private base), just with a private interface; it's mostly a composition alternative.

## Checklist before moving on
- [ ] I can argue composition-over-inheritance with a concrete example and name the one case inheritance genuinely wins.
- [ ] I can draw the diamond and explain Java/C++/Python resolutions in 3 sentences each.
- [ ] I can state Java's `protected` rule and C++'s three inheritance specifiers.
- [ ] I can upcast implicitly, downcast with `instanceof` + cast, and explain when `ClassCastException` occurs.
- [ ] I can explain "program to the base" and why it prevents cast bugs.
- [ ] I can name the fragile base class problem and two mitigations.
