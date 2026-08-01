# Chapter: Introduction to OOPs

## What you'll learn
- A precise, one-sentence definition of object-oriented programming and the historical problem (procedural spaghetti + poor data modeling) it was invented to solve.
- The concrete differences between procedural and object-oriented code — data vs. behavior, top-down flow vs. message passing — with a worked example of the same program in both styles.
- Exactly what a **class** is (blueprint/template) versus an **object** (living instance with memory), and how to reason about each.
- The four pillars — **Encapsulation, Abstraction, Inheritance, Polymorphism** — with one killer example each, and which Java keyword powers which pillar.
- How every object has **identity, state, and behavior**, why they are distinct concepts, and how each maps to memory (`==` vs `.equals()`).

## Prerequisites (linked)
- None beyond basic programming in any language (a variable, a function, a `for` loop). If you are rusty, skim any CS101 material first.
- This chapter feeds directly into [Chapter 02 — Classes and Objects in Depth](../chapter-02-classes-and-objects-in-depth/README.md) and every later part of the subject.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — What is Object-Oriented Programming?](section-01-what-is-object-oriented-programming.md) | The definition, origins (Simula 67, Smalltalk), and the "data + behavior in one unit" paradigm shift |
| [Section 02 — Procedural vs Object-Oriented Programming](section-02-procedural-vs-object-oriented-programming.md) | Same problem, two solutions: functions-owning-data vs objects-owning-both |
| [Section 03 — Objects and Classes](section-03-objects-and-classes.md) | Blueprint vs instance; `new`, heap allocation, and the class-vs-object relationship |
| [Section 04 — Four Pillars of OOPs Overview](section-04-four-pillars-of-oops-overview.md) | Encapsulation, Abstraction, Inheritance, Polymorphism — each with a pillar-to-keyword map |
| [Section 05 — Identity, State, and Behavior](section-05-identity-state-and-behavior.md) | The three properties of every object; `==` vs `.equals()`; mutable vs immutable state |

## One-paragraph narrative connecting all sections
OOP exists because procedural code scattered data away from the functions that act on it, causing coupling and duplication as programs grew (Sections 01–02). The remedy is to bundle data and behavior into **classes** that stamp out **objects** at runtime (Section 03). Once you have objects, you immediately need the rules that make them safe and reusable: hiding details (Encapsulation), exposing contracts (Abstraction), sharing behavior (Inheritance), and substituting implementations (Polymorphism) — the four pillars (Section 04). Finally, to use objects correctly you must separate what an object *is* (identity), what it *knows* (state), and what it *does* (behavior), because each maps to a different part of the runtime and a different equality rule (Section 05).

## Common interview trap in this chapter
Candidates say "a class is an object" or "encapsulation is the same as abstraction." They are not: a class is a *template*, an object is a *living instance*; encapsulation is *hiding implementation details*, abstraction is *exposing only the essential contract*. Another classic trap: claiming `==` compares objects in Java. It compares *references*; only `.equals()` (correctly overridden) compares *state*. Fixing these two confusions in the first 30 seconds builds instant credibility.

## Checklist before moving on
- [ ] I can define OOP in one sentence and name the two languages that originated it.
- [ ] I can rewrite the same small program procedurally and with objects, and explain why the OOP version wins.
- [ ] I can explain "class is a blueprint, object is an instance" with a `Car`/`myCar` example and `new` keyword.
- [ ] I can name the four pillars and give a real-world analogy for each.
- [ ] I can say where identity, state, and behavior live in memory and when `==` and `.equals()` agree/disagree.
- [ ] I can answer "what is the difference between class and object?" in under 30 seconds without hesitating.
