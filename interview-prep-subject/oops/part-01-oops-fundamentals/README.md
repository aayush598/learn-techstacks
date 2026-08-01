# Part: OOPs Fundamentals

## What this part covers
This part answers the very first questions in any OOP interview: *What is object-oriented programming and why was it invented?* It builds the vocabulary — objects, classes, identity, state, behavior, and the four pillars — that every other part of this OOP subject reuses. You will learn why OOP replaced pure procedural code, exactly how a class and object differ (and how that maps to memory), the full anatomy of a class in Java, how constructors/destructors control object lifecycle, how access modifiers decide visibility, and how `this`, `static`, and `final` behave with precision. This is the "first 30 seconds" foundation: getting these definitions crisp and correct is what separates a pass from a hire.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Introduction to OOPs | what is OOP, procedural vs OOP, objects and classes, four pillars overview, identity/state/behavior | Define OOP in one sentence, contrast it with procedural code with a real example, draw the class-vs-object relationship, name the 4 pillars and which pillar powers which keyword, distinguish identity from state from behavior |
| ch-02 Classes and Objects in Depth | class design/members/anatomy, constructors & destructors, object memory & lifecycle, access modifiers & scope, `this`/`static`/`final` | Design a class with the right members, reason about constructor chains and destructor timing, predict where an object lives (stack vs heap) and when it dies, apply Java's access rules correctly, use `this`/`static`/`final` without mistakes |

## Study order
1. **ch-01 first** — it builds the vocabulary (object, class, pillar, identity) used by every later part.
2. **ch-02 next** — the same classes/objects become concrete: memory layout, constructors, visibility, modifiers.
3. Read every section in numbered order within a chapter; each section assumes the previous one.
4. Parts 02–06 assume you know the four pillars by name — come back here to re-anchor.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — this is the *opening* of almost every OOP interview, and "difference between class and object" / "what are the 4 pillars" are the two most-asked warm-up questions in the industry.
- **Emphasized by**: every general SDE loop (Amazon, Google, Microsoft, Meta, Apple), Java backend shops (Amazon, LinkedIn, Splunk, Flipkart), and C++ systems teams (NVIDIA, Apple, Bloomberg, trading firms). Interviewers at Amazon/Flipkart often spend the first 3–5 minutes here before moving to SOLID and design.
- Typical asked: "What is OOP?", "class vs object", "the four pillars with examples", "what does `static` mean in Java?", "why can't a constructor be `final` or `abstract`?", "what happens when an object goes out of scope in C++?".

## How the parts connect (roadmap)
- Part 01 is the **foundation**: it establishes objects, classes, and the pillar vocabulary used everywhere.
- **Part 02 (Encapsulation & Abstraction)** makes two of the pillars precise: how state is hidden (`private` + getters/setters) and how interfaces contract behavior (`abstract`, `interface`).
- **Part 03 (Inheritance)** extends classes: `extends`/`super`, overriding, the diamond problem, and composition-vs-inheritance decisions.
- **Part 04 (Polymorphism)** explains *why* inheritance matters: dynamic dispatch via vtables, overloading, and the "program to an interface" mindset.
- **Part 05 (Association/Aggregation/Composition)** categorizes *non-inheritance* object relationships and UML.
- **Part 06 (SOLID & Design Principles)** turns all of the above into professional judgment: SRP/OCP/LSP/ISP/DIP, DRY/KISS/YAGNI, and refactoring.
- After Part 06 you will be ready for the design-heavy rounds (LLD) that FAANG/MAANG run after the OOP screen.
