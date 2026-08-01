# Part: Association, Aggregation, and Composition

## What this part covers
Objects in a real system don't live alone — they cooperate, and the *kind* of cooperation matters. This part is about **object relationships**: association (a plain uses/knows link), aggregation (a "has-a" where parts can outlive the whole), composition (a stronger "has-a" where the whole owns the part's lifecycle), and dependency (the weakest, use-only link). Beyond the vocabulary, you'll learn how to *read and write* relationships in **UML class diagrams** — multiplicity, roles, navigability — so you can design and communicate object models precisely. The line between aggregation and composition is subtle (ownership vs sharing), and interviewers love asking "what's the difference?" and "which do you use for a `List<Order>`?" After this part you'll answer confidently and, just as important, you'll know how these relationships map to real code (fields, constructors, `new`, factory wiring) and to garbage-collection/lifetime semantics.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Object Relationships | association/aggregation/composition in depth; UML class diagrams for OOPs | Distinguish the four relationship kinds precisely, model ownership vs sharing, map relationships to code (fields/constructors/lifecycle), read and draw UML class diagrams with correct multiplicity/navigability |

## Study order
1. **ch-01** is the whole part — read the two sections in order: relationships first (the semantics), then UML (how to draw what you just learned).
2. Section 01 is the interview-critical one: the association/aggregation/composition distinction is an evergreen question.
3. Section 02 gives you the *language* to draw the design you're about to use in Part 06 (SOLID) — design diagrams assume UML fluency.
4. Assumes **Part 01** (objects) and **Part 03** (inheritance) — relationships often involve inheritance hierarchies.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐ (4/5)** — the association/aggregation/composition question is a staple junior/intermediate round question, and relationship modeling appears in every system-design round (why a `Car` *owns* its engine but only *knows* its driver).
- **Emphasized by**: Amazon, Google, Meta (design + core OOPs rounds); backend teams (Java/Spring, .NET) test ownership/lifecycle reasoning; UML-reading questions appear in consulting and architecture interviews.
- Typical asked: "Difference between association, aggregation, composition?", "Is a `Car` and `Engine` aggregation or composition?", "Which one uses a weak reference?", "Draw a UML class diagram for X.", "What's multiplicity in UML?".

## How the parts connect (roadmap)
- Relationships build on **Part 01's** objects/classes (a relationship is just fields of other objects) and **Part 03's** inheritance (a subtype relationship is itself a relationship in UML — generalization).
- **Part 06 (SOLID)** uses these relationships constantly: DIP says "depend on abstractions, not concrete associations"; LSP governs generalization correctness.
- **Design patterns (Part 07+)** are mostly *relationship recipes* — Composite is a tree of associations, Observer is an association, Facade wraps associations.
- After this part you can design any object graph and draw it in UML — the prerequisite for the pattern-heavy and system-design parts ahead.
