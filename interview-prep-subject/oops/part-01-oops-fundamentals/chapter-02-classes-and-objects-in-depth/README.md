# Chapter: Classes and Objects in Depth

## What you'll learn
- The **anatomy of a class**: fields, methods, constructors, initializers, nested types — what each member is for and the rules for declaring them.
- **Constructors and destructors**: why constructors exist, constructor overloading and chaining, copy/move constructors in C++, `finalize` vs `AutoCloseable` vs C++ destructors, and why constructors can't be `static`/`final`/`abstract`.
- **Object memory and lifecycle**: exactly where an object lives (Java heap / C++ stack vs heap), when it is created, when it becomes garbage, and the role of the GC vs RAII.
- **Access modifiers and scope**: Java's `public`/`protected`/`private`/package-private rules, the classic "protected means subclass OR same-package" trap, and `static`/instance scope.
- **`this`, `static`, and `final`**: what `this` actually is (a reference to the receiver), what `static` members share, and all the meanings of `final` (variable/method/class/parameter).

## Prerequisites (linked)
- [Chapter 01 — Introduction to OOPs](../chapter-01-introduction-to-oops/README.md): you must already know what a class and object are.
- Later parts assume this chapter: [Part 02 Encapsulation](../..//part-02-encapsulation-and-abstraction/README.md) builds on access modifiers; [Part 03 Inheritance](../../part-03-inheritance/README.md) builds on constructors and `super`.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Class Design, Members, and Anatomy](section-01-class-design-members-and-anatomy.md) | Fields, methods, constructors, static/instance members, initializers — the full skeleton of a class |
| [Section 02 — Constructors and Destructors](section-02-constructors-and-destructors.md) | Initialization guarantees, overloading, chaining, copy/move semantics, destruction order |
| [Section 03 — Object Memory and Lifecycle](section-03-object-memory-and-lifecycle.md) | Stack vs heap, references, GC vs RAII, object death and resurrection |
| [Section 04 — Access Modifiers and Scope](section-04-access-modifiers-and-scope.md) | `public`/`protected`/`private`/package-private; static vs instance scope |
| [Section 05 — `this`, `static`, and `final`](section-05-this-keyword-static-members-and-final.md) | The receiver reference, shared class-level state, and the three faces of `final` |

## One-paragraph narrative connecting all sections
Once you know what a class *is*, the interview moves to how it is *built and destroyed*. A class is a collection of members (fields, methods, constructors) that you must design deliberately so the object is always in a valid state (Section 01). Validity is enforced from the very first moment of life: constructors guarantee initialization, and their inverse — destructors/finalizers — guarantee cleanup, with strict ordering rules you must not break (Section 02). Where the object lives (stack or heap) and who reclaims it (GC in Java, RAII in C++) determines memory behavior and leaks (Section 03). Visibility decides *who can touch* each member — the four Java access modifiers plus the notorious "protected ≠ private-to-subclass" rule (Section 04). Finally, three keywords control the *shared vs instance* and *changeable vs frozen* nature of members: `this` for the current receiver, `static` for class-level state, and `final` for immutability of variables, methods, and classes (Section 05).

## Common interview trap in this chapter
Three traps appear constantly: (1) "What does `protected` mean?" — the correct Java answer is *package-private PLUS subclasses (even in other packages)*; candidates only say "subclasses". (2) "Why can't a constructor be `final`/`abstract`/`static`?" — because constructors aren't inherited and aren't dispatched, so those modifiers are meaningless. (3) "Where does an object live in Java?" — the reference lives on the stack, the object on the heap; saying "everything is on the stack" is wrong, saying "objects live on the heap" is right.

## Checklist before moving on
- [ ] I can draw a Java class showing fields, methods, constructors, and a `static` member, and say why each exists.
- [ ] I can explain constructor chaining (`this(...)` vs `super(...)`) and the order of initialization.
- [ ] I can contrast Java GC with C++ RAII and predict when `finalize()`/destructors run (and that you should never rely on `finalize()`).
- [ ] I can state Java's exact `protected` rule and the default (package-private) access rule.
- [ ] I can list every meaning of `final` in Java and why `final` methods can't be overridden but CAN be hidden.
- [ ] I can predict the stack-vs-heap placement and lifetime of any small code snippet.
