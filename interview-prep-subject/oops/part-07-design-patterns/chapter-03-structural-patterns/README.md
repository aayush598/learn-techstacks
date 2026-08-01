# Chapter: Structural Patterns

## What you'll learn
- The seven GoF structural patterns and the common principle behind them: **compose objects and classes into larger structures without breaking flexibility**.
- **Adapter** — make an incompatible interface callable by your client (a translator between interfaces).
- **Decorator** — add behavior/responsibilities to an object *at run time* without subclassing (wrapping).
- **Facade** — a single simplified entry point over a complex subsystem.
- **Proxy** — a stand-in that controls access to (or defers the creation of) a real object.
- **Composite** — treat individual objects and their groupings uniformly (a tree of parts-and-wholes).
- **Bridge** — decouple an abstraction from its implementation so both can vary independently.
- The critical interview skill: **precisely distinguishing Adapter vs Decorator vs Proxy vs Facade** (all "wrappers", different intents).

## Prerequisites (linked)
- [Chapter 01 — Design Patterns Fundamentals](chapter-01-design-patterns-fundamentals/README.md) — the pattern concept and why "composition over inheritance" drives all structural patterns.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md) — structural patterns rely on interfaces + dynamic dispatch.
- [Part 02 — Encapsulation](../../part-02-encapsulation-and-abstraction/README.md) — wrapping hides the wrapped object's complexity.
- [Part 08 — Java Advanced OOPs](../../part-08-language-specific-advanced-oops/README.md) — `volatile`/thread-safety for lazy proxies; Java I/O class hierarchy for the Decorator examples.

## Sections (linked table)
1. [Section 01: Adapter Pattern](section-01-adapter-pattern.md)
2. [Section 02: Decorator Pattern](section-02-decorator-pattern.md)
3. [Section 03: Facade Pattern](section-03-facade-pattern.md)
4. [Section 04: Proxy Pattern](section-04-proxy-pattern.md)
5. [Section 05: Composite and Bridge Patterns](section-05-composite-and-bridge-patterns.md)

## One-paragraph narrative connecting all sections
Section 01 starts with the simplest "wrapper": the **Adapter**, which translates one interface into another so incompatible classes can cooperate — the client calls its own interface, and the adapter forwards to the adaptee. Section 02 escalates wrapping to the **Decorator**, which *adds behavior* to an object at run time by layering wrappers (Java I/O's `BufferedReader(new FileReader(...))`), the pattern that "prefers composition over inheritance" at its purest. Section 03 flips the direction: instead of matching or extending an interface, the **Facade** hides a whole subsystem behind one simple door. Section 04 covers the **Proxy**, a stand-in that controls *access* (lazy loading, security, remote, logging) rather than adding behavior — the pattern Spring's AOP and lazy-initialization are built on. Section 05 closes with the two "tree" patterns: **Composite** (uniform parts-and-wholes tree, used by UI widget trees and filesystems) and **Bridge** (decouple abstraction from implementation so *both* vary independently — the classic "shape with color" problem). Read them in order — every one is a different answer to "how do I compose objects safely?" and each builds your ability to tell the wrappers apart, which is the most frequently tested distinction in the whole OOPs curriculum.

## Common interview trap in this chapter
**Confusing the four "wrapper" patterns.** Interviewers love: "You're given a `MediaPlayer` that plays mp3 and a `AdvancedMediaPlayer` that plays vlc/mp4 — which pattern?" (Adapter, if the *interface* is incompatible; Decorator if you're *adding features*; Proxy if you're *controlling access*; Facade if you're *hiding the subsystem*). The trap: all four wrap an object, but they answer different questions — Adapter: "can I call this with my interface?"; Decorator: "can I add behavior?"; Proxy: "can I control who touches the real thing?"; Facade: "can I hide the mess behind one door?". The second trap: writing a Decorator that *modifies* the delegate instead of *adding around* it, and forgetting that Decorator works through the *same* interface while Adapter deliberately changes the interface.

## Checklist before moving on
- [ ] I can draw the class shape of Adapter, Decorator, Facade, Proxy, Composite, and Bridge.
- [ ] I can state the *intent* of each and the exact problem each solves.
- [ ] I can answer "Adapter vs Decorator vs Proxy vs Facade" with a one-line discriminator for each.
- [ ] I can write a working Java Decorator over an interface (e.g., encrypting/compressing a stream) and explain recursion of wrappers.
- [ ] I can write a lazy-loading Proxy and explain its thread-safety.
- [ ] I can identify Composite in a UI/filesystem hierarchy and Bridge in a "shape × color" design.
- [ ] I can name a real JDK/Spring usage of each pattern.
