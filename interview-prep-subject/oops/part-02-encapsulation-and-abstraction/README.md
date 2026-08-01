# Part: Encapsulation and Abstraction

## What this part covers
Two of the four pillars in exacting detail. **Encapsulation** is the mechanism of *bundling data with the methods that operate on it* and *hiding the internals* behind a controlled interface (`private` fields, getters/setters/properties) so invariants cannot be broken from outside. **Abstraction** is the *design strategy* of exposing only the essential contract (`abstract` classes, interfaces) while hiding implementation. This part teaches the distinction the way interviewers expect (encapsulation = hiding *state*, abstraction = hiding *implementation behind a contract*), the precise rules of information hiding, the correct design of accessor methods (including the "leaky getter" trap), abstract-class-vs-interface decision making, and how interfaces differ across Java, Go, and C#. After this part you will never again blur "hide the data" with "expose the contract."

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Encapsulation | encapsulation in depth, information hiding & data protection, getters/setters/properties | Enforce invariants with private state, design accessors correctly (immutable types, defensive copies), avoid leaky abstractions, use properties idiomatically in C#/Python |
| ch-02 Abstraction | abstraction in depth, abstract classes vs interfaces, interfaces in Java/Go/C#, encapsulation vs abstraction | Define abstraction precisely, choose abstract class vs interface by design need, compare interface semantics across languages, articulate encapsulation-vs-abstraction in one breath |

## Study order
1. **ch-01 first** — encapsulation is the more mechanical pillar (private + accessors); you need it before abstraction makes sense as "the contract over the hidden state."
2. **ch-02 next** — abstraction sits *on top of* encapsulation: you hide state, then expose a contract.
3. Within each chapter, read sections in numbered order; they build on each other.
4. Parts 03 (Inheritance) and 04 (Polymorphism) extend abstraction into `extends`/`implements`; Part 06 (SOLID) turns these two pillars into SRP/OCP/ISP/DIP judgment.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — "Encapsulation vs abstraction" is among the top-5 most-asked OOP questions; "when abstract class vs interface" is a guaranteed question in Java-heavy loops.
- **Emphasized by**: all Java/C# backend shops (Amazon, LinkedIn, Flipkart, Splunk, Oracle), Android roles (interfaces every day), and system design interviews where "program to an interface" is expected vocabulary.
- Typical asked: "Difference between encapsulation and abstraction?", "When to use abstract class vs interface?", "Why are fields private?", "What's a leaky abstraction?", "How do interfaces work in Go?".

## How the parts connect (roadmap)
- Part 02 is built directly on **Part 01's** access modifiers (`private`) and class anatomy.
- **Part 03 (Inheritance)** implements the `abstract`/`extends` machinery abstraction describes; **Part 04 (Polymorphism)** is what abstraction buys you at runtime (interface dispatch).
- **Part 05** describes how *relationships* (has-a/uses-a) work around the encapsulated objects.
- **Part 06 (SOLID)** converts both pillars into the five principles — ISP/DIP are pure "program to abstraction"; SRP/OCP need it too.
- After Part 06 you'll be ready for low-level-design (LLD) rounds where "hide the data, expose the contract" is the baseline expectation.
