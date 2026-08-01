# Chapter: Patterns in Practice

## What you'll learn
- How the **23 GoF patterns appear in real libraries** — Java/JDK internals, the Spring framework, and common production code — so you can *recognize* patterns, not just recite them.
- A **pattern-selection decision procedure** — how to systematically pick the right pattern (or none at all) for a design problem, the exact skill LLD interviewers score.
- How to **defend** a pattern choice in a design review: problem → candidate patterns → trade-offs → chosen pattern.
- Pattern **anti-patterns in practice**: Singleton abuse, premature abstraction, forcing patterns (Golden Hammer), and when "no pattern" is the best pattern.

## Prerequisites (linked)
- [Chapter 01 — Design Patterns Fundamentals](chapter-01-design-patterns-fundamentals/README.md) — the pattern vocabulary and taxonomy.
- [Chapter 02 — Creational Patterns](chapter-02-creational-patterns/README.md) — the creation-focused half of the pattern map.
- [Chapter 03 — Structural Patterns](chapter-03-structural-patterns/README.md) — wrapping/composition patterns used everywhere in frameworks.
- [Chapter 04 — Behavioral Patterns](chapter-04-behavioral-patterns/README.md) — communication/behavior patterns that frameworks embed.

## Sections (linked table)
1. [Section 01: Design Patterns in Java and Spring Libraries](section-01-design-patterns-in-java-and-spring-libraries.md)
2. [Section 02: How to Choose the Right Pattern](section-02-how-to-choose-the-right-pattern.md)

## One-paragraph narrative connecting all sections
Section 01 turns the abstract catalog into *recognition*: a pattern-by-pattern tour of the **JDK** (Comparator=Strategy, FilterInputStream=Decorator, Iterator=Iterator, Runtime=Singleton, Observable=Observer, HandlerAdapter-style bridging) and **Spring** (BeanFactory=Abstract Factory+Singleton, @Transactional=Proxy, ApplicationContext=Facade, @EventListener=Observer, JdbcTemplate=Template Method, HandlerAdapter=Adapter) — because interviewers ask "which pattern does X use?" as a recognition test, and framework fluency is the proof you can apply patterns in production. Section 02 then gives you the *decision procedure*: run the "tension → family → candidates → trade-offs → validate" triage, weigh pattern-vs-no-pattern, and defend the choice. Together they convert pattern *knowledge* into pattern *judgment* — the exact capability that separates a good answer from a great one in design interviews and design reviews.

## Common interview trap in this chapter
**Candidates recognize a pattern's diagram but cannot map it to the libraries they actually use**, and conversely they claim patterns "obviously" apply without running any selection procedure. The traps: (1) naming the *shape* but not the *intent* when asked "what pattern is Spring's @Transactional?" (it's Proxy — access/behavior interception — NOT Decorator, though the shapes overlap); (2) pattern-forcing: answering an LLD with a pattern "because it's impressive" instead of because the *problem* matches; (3) failing to say "no pattern here" when a simple class would do. Interviewers probe by asking "why didn't you use X instead?" — you must be ready to compare candidates and state trade-offs.

## Checklist before moving on
- [ ] I can name the GoF pattern behind at least 15 real JDK/Spring classes/APIs.
- [ ] I can answer "is Spring's `@Transactional` a Proxy or a Decorator?" with a crisp rationale.
- [ ] I can run the full pattern-selection triage on a fresh LLD scenario (tension → family → candidates → trade-off → chosen).
- [ ] I can argue *against* a pattern (state when "no pattern" is correct).
- [ ] I can compare 2-3 candidate patterns for one problem and pick with justification.
- [ ] I can identify the three classic anti-patterns (Golden Hammer, premature abstraction, Singleton abuse) in a design review.
- [ ] I can explain how pattern composition (e.g., Factory + Singleton, Composite + Iterator) works in real code.
