# Chapter: Behavioral Patterns

## What you'll learn
- The 11 GoF behavioral patterns and the common thread: **how objects distribute responsibility and communicate** without tight coupling.
- **Strategy** — encapsulate interchangeable algorithms behind an interface and swap them at run time.
- **Observer** — a subject notifies many decoupled listeners of state changes (publish/subscribe).
- **Command** — encapsulate a request as an object (undo/redo, queuing, logging, transactionality).
- **State** — an object's behavior changes as its internal state changes (state machine as objects).
- **Template Method** — fix an algorithm's skeleton in a base class; let subclasses override steps.
- **Iterator** — traverse a collection without exposing its structure.
- **Memento** — capture and restore an object's internal state (snapshot/undo).

## Prerequisites (linked)
- [Chapter 01 — Design Patterns Fundamentals](chapter-01-design-patterns-fundamentals/README.md) — the pattern concept and the behavioral family's role.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md) — behavioral patterns are where dynamic dispatch earns its keep.
- [Part 02 — Encapsulation](../../part-02-encapsulation-and-abstraction/README.md) — behavioral patterns hide *what varies* (algorithms, state, requests).
- [Part 08 — Java Advanced OOPs](../../part-08-language-specific-advanced-oops/README.md) — lambdas/method references make Strategy and Observer lighter in modern Java.

## Sections (linked table)
1. [Section 01: Strategy Pattern](section-01-strategy-pattern.md)
2. [Section 02: Observer Pattern](section-02-observer-pattern.md)
3. [Section 03: Command Pattern](section-03-command-pattern.md)
4. [Section 04: State and Template Method Patterns](section-04-state-and-template-method-patterns.md)
5. [Section 05: Iterator and Memento Patterns](section-05-iterator-and-memento-patterns.md)

## One-paragraph narrative connecting all sections
Section 01 teaches the **Strategy** pattern — encapsulating a *family of algorithms* behind an interface so a context can swap behavior at run time (the JDK's `Comparator`, Spring's `Environment` abstraction). Section 02 teaches **Observer** — the publish/subscribe contract where a subject notifies decoupled listeners, the backbone of event-driven systems, GUI frameworks, and `java.util.Observable`. Section 03 adds **Command** — turning a *request* into an object so it can be queued, logged, undone, and made transactional (Runnable, Spring's transaction templates). Section 04 covers the pair that models *change*: **State** (behavior varies with internal state — a state machine made of objects, used by every HTTP/connection/UI state machine) and **Template Method** (a fixed algorithm skeleton with overridable steps — `JdbcTemplate`, `AbstractList`, servlet `doGet/doPost`). Section 05 finishes with the two "access/snapshot" patterns: **Iterator** (traverse collections without exposing structure — the entire Java `Iterator`/`Iterable` world) and **Memento** (capture and restore state for undo). Read in order: Strategy→Observer→Command handle "vary the algorithm / notify / capture the request", State→Template handle "behavior as state vs behavior as skeleton", and Iterator→Memento handle "traverse without revealing / snapshot without exposing". Together they cover the full spectrum of *behavior variation and communication* — the deepest and most-tested family in interviews.

## Common interview trap in this chapter
**Conflating patterns with similar shapes.** The big three traps: (1) **Strategy vs State** — Strategy is *chosen by the client* (the context selects an algorithm and keeps it); State is *changed by the object itself* as events occur (the object transitions between states). In State the context typically *replaces* its state object on every event; in Strategy the strategy stays put. (2) **Observer vs Mediator** — Observer is one-to-many broadcast (subjects don't know their observers' internals); Mediator is many-to-many centralized coordination (peers talk through the mediator). (3) **Template Method vs Strategy** — Template Method uses *inheritance* (a base class fixes the skeleton, subclasses override steps); Strategy uses *composition* (the context delegates the whole algorithm to an injected object). The second trap: candidates memorize UML but can't explain *why* the pattern is needed — e.g., why Observer beats "poll for changes" and why Command enables undo where a plain method call cannot.

## Checklist before moving on
- [ ] I can implement Strategy with a functional-interface (modern Java: lambdas) and explain when to prefer it over Template Method.
- [ ] I can implement a thread-safe Observer (copy-on-write listener list) and explain the `java.util.Observable` deprecation.
- [ ] I can implement Command with undo/redo using two stacks.
- [ ] I can distinguish State from Strategy and build a vending-machine state machine.
- [ ] I can explain Template Method's hook methods with a `JdbcTemplate`-style example.
- [ ] I can implement an Iterator for a custom collection (O(1) next, remove) and explain why iterators preserve encapsulation.
- [ ] I can implement Memento with a caretaker and explain what "narrow interface" means.
- [ ] I can name a real JDK/Spring/UI example for each of the seven patterns in this chapter.
