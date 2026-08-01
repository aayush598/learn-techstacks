# Part: Inheritance

## What this part covers
Inheritance is the pillar that lets a class **derive from another** — acquiring state and behavior, specializing it, and being used wherever its parent is. This part covers it end to end: what inheritance is and when it's legitimate (genuine IS-A, not convenience); the type matrix (single, multilevel, hierarchical, multiple) and why Java bans multiple class inheritance while C++ allows it; the `super` keyword and construction order; method overriding vs static method hiding (and their rules); the composition-vs-inheritance decision; the diamond problem and how each language resolves it; how access specifiers interact with inheritance; and upcasting/downcasting with polymorphic assignment. After this part you'll be able to design hierarchies deliberately, defend inheritance choices, and spot the is-a/has-a errors that plague production code.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Inheritance Basics | inheritance in depth, types of inheritance, `super` & base construction, overriding & hiding | Define IS-A, name the four type categories, order base/derived construction, apply override rules & `@Override`, distinguish overriding from hiding |
| ch-02 Inheritance Advanced | composition vs inheritance, multiple inheritance & diamond, access specifiers in inheritance, upcasting/downcasting | Decide composition over inheritance, explain the diamond problem + Java/C++/Python resolutions, apply protected/private inheritance nuances, use casts safely with `instanceof` |

## Study order
1. **ch-01 first** — the mechanism: what inheritance is, its shapes, construction, and overriding.
2. **ch-02 next** — the judgment: when *not* to inherit (composition), what breaks (diamond), who can see what (specifiers), and how references move up/down the hierarchy (casting).
3. Within each chapter, read sections in numbered order; each assumes the previous.
4. Parts 04 (Polymorphism) and 06 (SOLID — LSP) are the payoff: inheritance *enables* polymorphism, and LSP tells you whether your inheritance is *correct*.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — "composition vs inheritance" and "why no multiple inheritance in Java" are among the most common OOP follow-ups, and overriding rules produce a steady stream of Java trivia questions.
- **Emphasized by**: Java/C++ heavy loops (Amazon, Bloomberg, trading firms, Apple, NVIDIA); Android roles (every `Activity` extends framework classes); OO design rounds at Meta, Google, Microsoft.
- Typical asked: "Composition or inheritance?", "What is the diamond problem?", "Can you override a static method?", "Why is multiple inheritance dangerous?", "What's the order of constructor calls?", "What does `super` do?".

## How the parts connect (roadmap)
- Inheritance builds on **Part 01's** classes/objects and **Part 02's** access modifiers (`protected` was designed *for* inheritance).
- **Part 04 (Polymorphism)** is inheritance's runtime payoff — overriding produces the dynamic dispatch covered there; **Part 05** covers the *has-a* relationships that compete with inheritance.
- **Part 06 (SOLID)** — Liskov Substitution is literally "is your inheritance correct?"; OCP/ISP/DIP steer you toward composition + interfaces.
- After this part you're ready for the LLD rounds where "should this extend or compose?" is asked constantly.
