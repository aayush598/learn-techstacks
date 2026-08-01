# Chapter: Java Advanced OOPs

## What you'll learn
Everything the JVM actually does with the objects your classes declare: where objects and references live in memory, how the garbage collector decides what to collect, how to design genuinely immutable classes, what `final` really guarantees (and what it does NOT), how exceptions are modeled as an OOP hierarchy and thrown mechanically, how generics are erased so the runtime sees only `Object`, how collections use OOP (interfaces, `equals`/`hashCode`), and how lambdas/streams cooperate with, rather than replace, OOP design.

## Prerequisites (linked)
- [Part 01 — Classes & Objects](../../part-01-oops-fundamentals/README.md): you must know what a class/object is before you learn where the JVM stores them.
- [Part 02 — Encapsulation & Abstraction](../../part-02-encapsulation-and-abstraction/README.md): access modifiers and interfaces are used constantly in this chapter.
- [Part 03 — Inheritance](../../part-03-inheritance/README.md): overriding rules drive exceptions, generics bounds, and collections behavior here.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md): `@Override` + runtime dispatch reappear in every section.
- [Part 06 — SOLID](../../part-06-solid-and-design-principles/README.md): LSP and OCP are enforced by the language mechanics in this chapter.

## Sections (linked table)

| Section | Topic | Key skill |
|---|---|---|
| [01 — JVM Memory Model, Object Lifecycle & GC](section-01-java-memory-model-object-lifecycle-and-gc.md) | Stack vs heap vs metaspace, object header, GC algorithms | Trace where an object lives and when it dies |
| [02 — Immutability and the `final` Keyword](section-02-immutability-and-final-keyword.md) | `final` fields/classes/methods, defensive copies, thread-safety | Build a truly immutable class and justify each step |
| [03 — Exceptions and OOP](section-03-exceptions-and-oops.md) | Exception class hierarchy, checked vs unchecked, try/finally | Design an exception hierarchy and answer try/catch puzzles |
| [04 — Generics, Collections and OOP](section-04-generics-collections-and-oops.md) | Type erasure, wildcards, `equals`/`hashCode`, `Comparable` | Predict erasure results and write type-safe collections code |
| [05 — Functional Programming vs OOP in Java](section-05-functional-programming-vs-oops-in-java.md) | Lambdas, streams, method references, `Comparator` | Combine FP idioms with OOP classes without breaking design |

## One-paragraph narrative connecting all sections
The chapter tells one story: **a Java object is a memory block, and every OOP feature is a runtime behavior the JVM implements on that block.** Section 01 explains where that block lives and how the JVM reclaims it. Section 02 shows how the shape of the block (final fields) can make it immutable and thread-safe. Section 03 shows the language's error-handling as an OOP class hierarchy thrown through stack frames. Section 04 shows how the compile-time type system (generics) is erased to `Object` while collections rebuild the type safety via contracts like `equals`/`hashCode`. Section 05 closes with modern Java: lambdas are just objects (`FunctionalInterface`), so FP and OOP are two styles over one memory model. Understanding the mechanics first makes every interview answer about immutability, GC, or erasure land with confidence.

## Common interview trap in this chapter
Candidates say "`final` makes the object immutable" — **it does not.** `final` only makes the *reference* non-reassignable; a `final` field pointing to a `List` can still be mutated. Similarly, "generics are runtime checked" is backwards: type erasure means the JVM checks almost nothing, which is why `new T()` is illegal. Trap two: assuming checked exceptions were a good idea everywhere — the modern Java opinion (and Spring's) is that unchecked exceptions dominate production code. Know both sides.

## Checklist before moving on
- [ ] I can draw the JVM stack/heap/metaspace split and say where objects, references, and class metadata live.
- [ ] I can name the two GC mechanisms (mark-sweep phases + generational copying) and why `System.gc()` is just a hint.
- [ ] I can build an immutable class that is safe to publish to other threads.
- [ ] I can answer "what does `final` guarantee and what doesn't it?"
- [ ] I can design a checked-vs-unchecked exception hierarchy for a real library.
- [ ] I can predict the erasure of `List<String>` and explain why `List<String>` and `List<Integer>` are the same class at runtime.
- [ ] I can explain why overriding `equals` forces overriding `hashCode`.
- [ ] I can rewrite an OOP-heavy block using streams and lambdas and explain when each is cleaner.
