# Chapter: Inheritance Basics

## What you'll learn
- The precise definition of **inheritance** (an IS-A mechanism: subclass acquires state/behavior of a superclass and may extend or replace it) and why it exists (reuse + typing).
- The **four types** of inheritance: single, multilevel, hierarchical, and (the risky ones) multiple and hybrid — with Java's single-class rule.
- How **`super`** works: `super(...)` constructor delegation, `super.method()` calls, and the exact order of construction (parent first).
- **Method overriding vs method hiding**: rules, `@Override`, `final`/`static`/`private`/constructor exclusions, covariant returns, and the "static methods can't be overridden" trap.

## Prerequisites (linked)
- [Part 02 — Encapsulation & Abstraction](../../part-02-encapsulation-and-abstraction/README.md): you should know access modifiers (`protected`) and interfaces before inheritance adds `extends`.
- [Part 01, Chapter 02 — Constructors](../../part-01-oops-fundamentals/chapter-02-classes-and-objects-in-depth/section-02-constructors-and-destructors.md): construction order builds on constructor chaining.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Inheritance in Depth](section-01-inheritance-in-depth.md) | IS-A, extends mechanics, what's inherited vs not, why inheritance exists |
| [Section 02 — Types of Inheritance](section-02-types-of-inheritance-single-multilevel-hierarchical.md) | Single, multilevel, hierarchical, multiple, hybrid; Java vs C++ vs Python |
| [Section 03 — `super` and Base Class Construction](section-03-super-keyword-and-base-class-construction.md) | `super(...)`, `super.method()`, construction order, base invariants |
| [Section 04 — Method Overriding and Method Hiding](section-04-method-overriding-and-method-hiding.md) | Override rules, `@Override`, hiding static methods, `final`/`private` exclusions |

## One-paragraph narrative connecting all sections
Inheritance lets a subclass reuse and specialize its parent (Section 01), but the *shapes* it can take differ by language — single/multilevel/hierarchical are safe, while multiple class inheritance creates ambiguity that Java bans (Section 02). When you extend, `super` is how the subclass reaches back: the constructor chain (parent first) and the parent's methods (Section 03). The subtlest mechanics live in overriding: which methods can be overridden, why `@Override` matters, and why static methods are *hidden*, not overridden (Section 04). Everything later — casting, the diamond problem, LSP — is built on these four fundamentals.

## Common interview trap in this chapter
Candidates say "private members are inherited." The precise truth: private fields *exist* in the subclass object (memory is inherited), but the subclass cannot *access* them by name — access is via public/protected parent members. Second trap: "static methods can be overridden." They cannot — they are *hidden*; the call resolves by reference type at compile time. Third: "the subclass constructor runs first." Wrong — the parent constructor always runs first (`super()` implicit first line).

## Checklist before moving on
- [ ] I can define inheritance as IS-A and give a valid and an invalid example.
- [ ] I can name single/multilevel/hierarchical/multiple/hybrid and state Java's rules.
- [ ] I can trace constructor order (parent static → child static → parent init → parent ctor → child init → child ctor).
- [ ] I can list what `super()` vs `super.method()` do and when the implicit `super()` is inserted.
- [ ] I can state all four override rules and why static/private/final/constructor methods can't be overridden.
- [ ] I can explain `@Override`'s value and covariant returns.
