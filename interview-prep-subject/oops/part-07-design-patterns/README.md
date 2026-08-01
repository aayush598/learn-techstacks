# Part: Design Patterns

## What this part covers
The complete catalog of **Gang-of-Four (GoF) object-oriented design patterns** — the time-tested solutions to recurring design problems that every production OO system is built from. You will learn why patterns exist (they codify *principled reuse of good design* rather than code), how the 23 GoF patterns are categorized into **creational** (how objects are made), **structural** (how classes/objects are composed), and **behavioral** (how objects communicate), and — critically — how each one maps to the Java standard library and to real frameworks you will be quizzed on at FAANG/MAANG (Spring singleton/proxy/factory, Java I/O decorator, `java.util.Observable`, etc.). The part ends with pattern *selection*: how to pick the right pattern (and, just as important, how to recognize when a pattern is the *wrong* tool).

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Design Patterns Fundamentals | what & why patterns exist, GoF overview & categorization | Define a pattern (context/problem/solution), name the GoF 3×3 categorization, spot when a "solution" is an anti-pattern |
| ch-02 Creational Patterns | Singleton, Factory Method + Abstract Factory, Builder, Prototype + Object Pool | Explain **when a constructor is not enough**; guarantee one instance thread-safely; defer/abstract object creation; build complex objects stepwise; clone vs pool |
| ch-03 Structural Patterns | Adapter, Decorator, Facade, Proxy, Composite + Bridge | Wrap/compose objects to change interface or behavior; distinguish adapter/decorator/proxy; hide subsystem complexity; treat trees uniformly |
| ch-04 Behavioral Patterns | Strategy, Observer, Command, State + Template Method, Iterator + Memento | Encapsulate algorithms/requests/state; decouple event producers from consumers; undo/redo; traverse collections without exposing structure; snapshot object state |
| ch-05 Patterns in Practice | Patterns in Java & Spring libraries, how to choose the right pattern | Map each GoF pattern to real JDK/framework usage; run a pattern-selection decision procedure; defend pattern choices in LLD design reviews |

## Study order
1. **ch-01** first — it gives the vocabulary (pattern = context/problem/solution, and the anti-pattern concept) you need to reason about all 23 patterns.
2. **ch-02 (creational)** — creation is where most OO mistakes live; master singleton + factory before anything else.
3. **ch-03 (structural)** — adapters/decorators/proxies are the most common in real code and the most frequently confused in interviews.
4. **ch-04 (behavioral)** — strategy/observer/command carry the most design weight in interviews and in framework internals.
5. **ch-05 last** — mapping patterns to JDK/Spring and running the selection procedure turns pattern *recognition* into pattern *application*, which is exactly what interviewers test.

Read every section in numbered order within a chapter; each section assumes the previous one.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — design patterns are the single most commonly probed OO topic in senior-level interviews, and they are the backbone of **Low-Level Design (LLD)** rounds.
- **Emphasized by**: every FAANG/MAANG (Google, Meta, Amazon, Microsoft, Apple) LLD rounds; **back-end/platform teams** (Uber, Stripe, LinkedIn, Airbnb, Spotify) ask Spring/framework pattern questions; **all Java shops** assume fluent knowledge of the patterns the JDK itself uses.
- Typical asked: "Implement a thread-safe singleton", "which GoF pattern does Spring's `@Autowired` rely on?", "decorator vs adapter vs proxy — differ them", "design a notification system (observer/strategy)", "when would you *not* use a singleton?".

## How the parts connect (roadmap)
- **Part 06 (SOLID & design principles)** is the *why*; this part is the *how*. SOLID gives you the laws (open-closed, dependency inversion), patterns give you the reusable mechanisms that obey those laws. If you haven't done Part 06, patterns will feel like memorization; after Part 06 they feel like inevitable consequences.
- **Part 08 (Language-Specific Advanced OOPs)** deepens everything here with language mechanics — `synchronized`/`volatile` for the singleton double-checked-locking, JMM and immutability for safe pattern implementations, vtables/RTTI which make polymorphic patterns (strategy, state, template method) cheap in C++.
- **Part 09 (Interview Question Bank)** gives you the 100-question QA + LLD walkthroughs that stress-test the pattern knowledge built here.
- Together Parts 06→09 form the complete "design maturity" arc of the OOPs subject: principles → patterns → language mechanics → interview application.

---

# Chapter: Design Patterns Fundamentals

## What you'll learn
- The precise definition of a design pattern and the three-part structure **Context → Problem → Solution**.
- Why patterns exist: they are *documented, vetted solutions* that compress decades of collective experience into a reusable vocabulary.
- The GoF categorization: 23 patterns split into **creational (5)**, **structural (7)**, and **behavioral (11)** — and the finer sub-splits (class vs object patterns).
- What a pattern is *not*: an algorithm, a framework, or a silver bullet — and the difference between a pattern and an anti-pattern.

## Prerequisites (linked)
- [Part 06 — SOLID and Design Principles](../../part-06-solid-and-design-principles/README.md) — patterns are concrete mechanisms that implement the SOLID laws.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md) — most patterns lean on interfaces and run-time dispatch.
- [Part 02 — Encapsulation and Abstraction](../../part-02-encapsulation-and-abstraction/README.md) — every pattern is an exercise in encapsulation of some kind (creation, behavior, structure).

## Sections (linked table)
1. [Section 01: What Are Design Patterns and Why They Exist](chapter-01-design-patterns-fundamentals/section-01-what-are-design-patterns-and-why-they-exist.md)
2. [Section 02: GoF Patterns Overview and Categorization](chapter-01-design-patterns-fundamentals/section-02-gof-patterns-overview-and-categorization.md)

## One-paragraph narrative connecting all sections
Section 01 builds the definition: a pattern is a *named, reusable solution* to a recurring design problem, expressed as context/problem/solution with a consequence analysis — the point being that good OO designers don't reinvent solutions, they *recognize* problems and apply vetted shapes. Section 02 lays out the full GoF catalog as a decision map: **creational** patterns abstract *how objects are instantiated* (constructor → factory → builder), **structural** patterns compose *classes and objects* into larger structures (adapter, decorator, proxy), and **behavioral** patterns assign *responsibility and communication* between objects (strategy, observer, command). Together they give you the complete vocabulary that every later chapter in this part uses by name.

## Common interview trap in this chapter
**Candidates memorize names and class diagrams but cannot state the *problem* a pattern solves.** Interviewers immediately detect this by asking "What problem does the Builder pattern solve, and what would happen if you didn't use it?" — a memorizer has no answer. Study every pattern as **problem → solution → trade-off**, never as a diagram to reproduce. The second trap is confusing *intent* with *implementation*: the singleton's intent is "one instance and a global access point", not "a static `getInstance()` method" — interviews test the intent.

## Checklist before moving on
- [ ] I can define a design pattern and name its three parts (context/problem/solution).
- [ ] I can classify all 23 GoF patterns into creational / structural / behavioral.
- [ ] I can explain, for any pattern I name, the exact problem it solves and the trade-off it accepts.
- [ ] I can distinguish a pattern (a reusable shape) from an algorithm (a procedure) and from a framework (a concrete system).
- [ ] I can name at least one real library/framework example for each of the 23 patterns.
