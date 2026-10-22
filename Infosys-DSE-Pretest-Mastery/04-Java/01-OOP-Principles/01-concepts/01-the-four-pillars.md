# The Four Pillars of OOP — and the Traps Around Them

> Section 4 · Java · OOP Principles · _Estimated reading time: 9 min_
> **Prerequisite:** none

## In one sentence

Java's four pillars are **encapsulation, abstraction, inheritance and polymorphism**, and every
"which of the following is NOT an OOP principle" question is decided by the fact that
**abstraction hides behaviour while encapsulation hides data**.

## Why the pre-test tests this

- The Java section is 25 questions. "Which of these is NOT an OOP principle?" and
  "Which is a feature of object-oriented programming?" are cheap 1-mark questions that appear
  in almost every Java paper.
- They are cheap because they look verbal — and that is exactly why candidates pick the
  plausible-sounding wrong option.
- The follow-up questions (overloading vs overriding, abstract class vs interface, `this` vs
  `super`) are where the marks are. Those are in the sibling files.

## Core concept

### The four pillars, defined precisely

| Pillar | One-line definition | Java mechanism | Question it wins |
|---|---|---|---|
| **Encapsulation** | Bind data and the methods that operate on it, and **restrict direct access to the data** | `private` fields + `public` getters/setters | "Which OOP concept restricts access to data?" |
| **Abstraction** | Expose **what** a type does, hide **how** it does it | abstract classes, interfaces | "Which concept hides implementation details?" |
| **Inheritance** | Derive a new type from an existing type and reuse its members | `extends`, `implements` | "Which concept allows code reuse through a parent-child relation?" |
| **Polymorphism** | One reference, many possible behaviours | overloading (compile-time) + overriding (run-time) | "Which concept allows a single interface to be implemented by different classes?" |

### Encapsulation vs abstraction — the single most-tested pair

| | Encapsulation | Abstraction |
|---|---|---|
| Hides | **Data** (state) | **Implementation** (logic) |
| Achieved with | access modifiers, getters/setters | abstract classes, interfaces |
| Answers the question | "How is the data protected?" | "What does the object promise to do?" |
| Typical exam option | "Data is hidden inside the class" | "Only the essential features are shown to the user" |

If the option says *"data is hidden behind access modifiers"*, it is **encapsulation**.
If the option says *"implementation details are hidden and only behaviour is exposed"*, it is
**abstraction**. Candidates swap these constantly.

### Class vs object vs instance

| Term | What it is | When it exists | Example |
|---|---|---|---|
| **Class** | A blueprint / type. A blueprint for creating objects | Compile time (as a `.class` file) | `class Car { }` |
| **Object** | A concrete instance created from a class | Run time | `new Car()` |
| **Instance** | A synonym for object, used to stress the class relation | Run time | "an instance of `Car`" |

Practical exam framing: **the class is the type, the object is the value.** "How many objects of
`Car` exist?" counts `new Car()` calls, not class declarations.

### The four pillars are not the whole story — but the exam only asks about them

These are *features/goals* of OOP, not pillars. They are the classic "NOT a principle" distractors:

| Not a pillar | Why it appears as a distractor |
|---|---|
| **Compilation** | Sounds technical, is a build step, not a design principle |
| **Optimization** | A performance goal of OOP, not one of the four |
| **Parallelism / concurrency** | Orthogonal to OOP design |
| **Serialization** | A Java library feature, not a principle |
| **Modularity** | A real OOP *feature*, but not one of the four pillars |

The canonical answer to *"Which of the following is NOT a feature of object-oriented programming?"*
is **Compilation** (with **Optimization** as the runner-up).

### Coupling and cohesion — the design-quality pair

| Term | Definition | Good design wants |
|---|---|---|
| **Coupling** | How much one class depends on another | **Low** coupling (loose) |
| **Cohesion** | How strongly the parts of one class belong together | **High** cohesion |

The exam phrasing is almost always: *"High cohesion and low coupling is a sign of ______"*
→ **good design**. And the converse: *"Low cohesion and high coupling"* → **bad design**.

### SOLID — the 5-letter refresher

The pre-test rarely asks SOLID by name, but the "good design" questions are SOLID-shaped.

| Letter | Name | In one line |
|---|---|---|
| **S** | Single Responsibility | A class has one reason to change |
| **O** | Open/Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | A subclass must be usable wherever the parent is |
| **I** | Interface Segregation | Small, focused interfaces beat one fat interface |
| **D** | Dependency Inversion | Depend on abstractions, not on concrete classes |

**L** is the one that connects to inheritance: if a subclass breaks a parent's contract, the
subclass violates Liskov Substitution, and a `List` that holds it throws
`ClassCastException` at a distance from the bug. See
[Inheritance & Polymorphism](../03-inheritance-polymorphism/README.md).

## Worked example

**Q1. Which of the following is NOT a principle of object-oriented programming?**

A. Encapsulation
B. Inheritance
C. Compilation
D. Polymorphism

**Solution**

The four pillars are encapsulation, abstraction, inheritance and polymorphism. "Compilation" is
the Java compiler's job — a build step, not a design principle.

**Answer: C.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | Encapsulation is pillar #1 — hiding data behind access modifiers |
| B | Inheritance is pillar #3 — the parent/child type relation |
| D | Polymorphism is pillar #4 — one reference, many behaviours |
| C (correct) | Compilation happens before OOP code ever runs; it is not a design principle |

**Q2. Which concept is used to hide the internal implementation of a class while exposing only
its public behaviour?**

A. Encapsulation
B. Abstraction
C. Polymorphism
D. Inheritance

**Solution**

"Hide the internal implementation, expose only behaviour" is the textbook definition of
**abstraction**. Encapsulation hides *data* and protects its integrity; it is about the state,
not the implementation of the logic.

**Answer: B.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | Encapsulation = bundling data with methods and restricting direct data access |
| C | Polymorphism = one interface, many implementations |
| D | Inheritance = deriving a child type from a parent type |

## Quick rules

- Four pillars: **E**ncapsulation, **A**bstraction, **I**nheritance, **P**olymorphism. Nothing else.
- Data hidden behind access modifiers = **encapsulation**.
- Implementation hidden, behaviour exposed = **abstraction**.
- "Compilation", "optimization", "serialization", "parallelism" are never pillars.
- A **class** is the type; an **object** is a created instance of it; **instance** means the same
  thing as object.
- Good design = **high cohesion + low coupling**.
- Multiple inheritance of classes is impossible; multiple implementation of interfaces is fine.
- SOLID exists to make "good design" questions answerable — **L** is the one inheritance touches.

## Common traps

| Trap | The option it produces | Fix |
|---|---|---|
| Calling encapsulation "hiding implementation" | Abstract class / interface as the encapsulation answer | Data vs implementation: ask what is being hidden |
| Picking "abstraction" for "protects the data" | B on an encapsulation question | Access modifiers + getters/setters = encapsulation |
| Picking "Compilation" as an OOP principle | The classic NOT-a-principle error | Four letters: E, A, I, P |
| Picking "Modularity" as NOT a principle | Modularity *is* an OOP feature, just not a pillar | If the option is a real OOP feature, it is a better distractor |
| Confusing object with class when counting | "3 objects" when there are 3 class declarations | Count `new` expressions |
| Answering "low cohesion, low coupling" for good design | Both halves must be right | High cohesion + low coupling |

## Checklist

- [ ] I can write the four pillars in order without hesitating.
- [ ] I can separate encapsulation from abstraction in one sentence each.
- [ ] I know the three "NOT a principle" distractors by heart: compilation, optimization, parallelism.
- [ ] I know that "high cohesion + low coupling" = good design, and that both halves must be right.
- [ ] I can explain in one line why compilation is not an OOP principle.
- [ ] I can state SOLID's five letters and the one-line meaning of each.

## Related

- [Overloading vs overriding](02-overloading-vs-overriding.md)
- [`this`, `super` and the modifier matrix](03-this-super-and-modifiers.md)
- [Identifying the pillar behind a code snippet](../02-techniques/01-identifying-a-pillar-procedure.md)
- [Abstract class vs interface](../02-techniques/02-abstract-class-vs-interface.md)
- [8 solved OOP questions](../03-worked-examples/01-solved-oop-questions.md)
- [OOP principles traps](../04-pitfalls/01-oop-principles-traps.md)
- [OOP principles one-pager](../05-reference/01-oop-principles-one-pager.md)
- [Topic overview](../README.md)
