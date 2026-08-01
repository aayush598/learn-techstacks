# Chapter: Creational Patterns

## What you'll learn
- Why a plain `new` constructor call is often the *wrong* tool — and the five creational patterns that replace it.
- **Singleton**: guaranteeing exactly one instance, with thread-safety (synchronized, double-checked locking, static inner holder, enum), lazy vs eager, and when to *avoid* it.
- **Factory Method vs Abstract Factory**: deferring object creation to subclasses vs providing a family of related products behind an interface — and how Spring's `BeanFactory` uses both.
- **Builder**: stepwise construction of complex/immutable objects with fluent APIs; telescoping-constructor pain solved.
- **Prototype & Object Pool**: cloning expensive objects vs reusing pooled instances; when copy beats construction.

## Prerequisites (linked)
- [Chapter 01 — Design Patterns Fundamentals](chapter-01-design-patterns-fundamentals/README.md) — the pattern concept and the creational family's place in the taxonomy.
- [Part 06 — SOLID](../../part-06-solid-and-design-principles/README.md) — creational patterns are the standard mechanisms for *Dependency Inversion* and *Open-Closed*.
- [Part 02 — Encapsulation](../../part-02-encapsulation-and-abstraction/README.md) — creation logic is *encapsulated*; the client no longer names concrete classes.
- [Part 08 — Java Advanced OOPs](../../part-08-language-specific-advanced-oops/README.md) — thread-safety (JMM, `synchronized`, `volatile`) and immutability make creational implementations correct.

## Sections (linked table)
1. [Section 01: Singleton Pattern](section-01-singleton-pattern.md)
2. [Section 02: Factory Method and Abstract Factory](section-02-factory-method-and-abstract-factory.md)
3. [Section 03: Builder Pattern](section-03-builder-pattern.md)
4. [Section 04: Prototype and Object Pool](section-04-prototype-and-object-pool.md)

## One-paragraph narrative connecting all sections
Section 01 starts with the simplest and most abused creational pattern — Singleton — teaching you *both* the correct thread-safe implementations (double-checked locking, inner-class holder, enum) and the maturity to argue when NOT to use it. Section 02 tackles the workhorse of dependency inversion: Factory Method moves the "which concrete class?" decision into a subclass, and Abstract Factory escalates it to "which family of related products?" — together they make creation *extensible* instead of scattered `new` calls. Section 03 fixes the second creational pain — *complex* construction — with Builder, the fluent, stepwise, immutable-object builder that Java's own `StringBuilder` and Spring's `BuilderFactoryBean` exemplify. Section 04 closes the family with Prototype (clone the prototype instead of reconstructing) and Object Pool (reuse expensive objects) — the two "cost-driven" creational answers. Read in order: each pattern is a different answer to "who should create the object, and how?"

## Common interview trap in this chapter
Candidates know the *shape* (private constructor + static `getInstance()`) but cannot name the **problem** each pattern solves, and they butcher thread-safety. The two deadliest traps: (1) writing a Singleton `getInstance()` that is *not* thread-safe and claiming it is — interviewers probe "what if two threads call `getInstance()` simultaneously?"; (2) using Singleton for *shared mutable state* that is conceptually not single — an interview trap where the "right" answer is "don't use Singleton here." Also common: conflating Factory Method (one product, subclasses decide) with Abstract Factory (a family of products, object decides) and failing to distinguish Builder (stepwise, for complex configurable objects) from Factory (single step, for delegating which concrete type).

## Checklist before moving on
- [ ] I can write a thread-safe lazy Singleton (double-checked locking with `volatile`, or the holder class, or the enum) and explain *why* each is safe.
- [ ] I can explain the problem Factory Method solves and where Spring uses it.
- [ ] I can distinguish Factory Method from Abstract Factory with a concrete scenario.
- [ ] I can build a fluent Builder for an immutable class and justify Builder over a constructor with 8 parameters.
- [ ] I can explain Prototype (shallow vs deep copy) and Object Pool (why pools exist, when NOT to pool).
- [ ] I can argue when *not* to use a Singleton and name the alternative (DI/injected instance).
- [ ] I can map each creational pattern to a real JDK/Spring usage.
