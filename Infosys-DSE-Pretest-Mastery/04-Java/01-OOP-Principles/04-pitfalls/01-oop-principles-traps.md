# OOP Principles — Traps the Exam Sets for You

> Section 4 · Java · OOP Principles · _Estimated reading time: 8 min_
> **Prerequisite:** [Overloading vs overriding](../01-concepts/02-overloading-vs-overriding.md)

## In one sentence

Every OOP trap is a **half-true statement**: one half is correct Java, the other half is the lie
the option is selling.

## Why the pre-test tests this

- Concept distractors in the Java section are engineered, not random. Each wrong option corresponds
  to one specific misreading.
- The traps below are the recurring ones: half-right statements beat wrong statements, because you
  have to *know* the rule to spot the lie.
- A candidate who can name the trap has already stopped making the error.

## Core concept

### The six canonical OOP traps

| # | Trap | The option that sells it | The truth |
|---|---|---|---|
| 1 | **Encapsulation/abstraction swap** | "Abstraction hides the data" | Abstraction hides the **implementation**; encapsulation hides the **data** |
| 2 | **Static treated as polymorphic** | `p.show()` → `Child.show` | Static methods bind to the **reference's** type at compile time |
| 3 | **Overload phase skipping** | `add(Integer)` → `int` | Phase 1 forbids boxing; `Integer` wins in phase 2 |
| 4 | **"Final = immutable"** | "A `final` field's object can never change" | Only the **reference** is fixed |
| 5 | **"Any modifier combo goes"** | `static abstract void f();` | `abstract` + `static`/`final`/`private` = compile error |
| 6 | **Interface unlimited-anything** | "An interface can have any kind of member" | No constructors, no instance fields, `public static final` fields only |

### Trap 1 in detail — the encapsulation/abstraction swap

The single most common Java concept trap. It works because both words sound like "hiding".

| Question says | The concept is | Because |
|---|---|---|
| "hides the internal implementation of a class and exposes only behaviour" | **Abstraction** | Interfaces / abstract classes |
| "binds data and methods together and prevents direct external access to the data" | **Encapsulation** | `private` fields + accessors |
| "provides a way to access data without knowing the internal implementation" | **Encapsulation** | This is the *accessor* pattern, not abstraction |

The third row is the classic trap wording — it sounds like abstraction because it mentions
"implementation", but it is about **data access**, which is encapsulation.

### Trap 2 in detail — static vs instance dispatch

```java
class P { static void s() { System.out.println("P.s"); } }
class C extends P { static void s() { System.out.println("C.s"); } }
P p = new C();
p.s();   // prints P.s
```

Candidates who have memorised "runtime polymorphism" apply it everywhere and pick `C.s`. The
one-line fix: **static methods are bound by the compiler using the reference's declared type.
They are hidden, not overridden.**

### Trap 4 in detail — `final` is not immutability

```java
final List<String> list = new ArrayList<>();
list.add("a");            // ✅ legal — the list's *contents* changed
list = new ArrayList<>(); // ❌ compile error — the *reference* changed
```

The exam wording: *"Which is TRUE about a `final` field?"* → the correct option is always the one
about **assignment**, never about the object's contents.

### Trap 5 in detail — the modifier matrix, one row at a time

| Candidate declaration | Verdict | The error text you would see |
|---|---|---|
| `abstract void f();` in an abstract class | ✅ | — |
| `static void f() {}` in an abstract class | ✅ | — |
| `private void f() {}` in an abstract class | ✅ | — |
| `abstract static void f();` | ❌ | "illegal combination of modifiers: abstract and static" |
| `abstract final void f();` | ❌ | "illegal combination of modifiers: abstract and final" |
| `abstract private void f();` | ❌ | "illegal combination of modifiers: abstract and private" |
| `abstract int x;` (a field) | ❌ | "illegal combination of modifiers: abstract and field" |

### Trap 6 in detail — what an interface really is

The exam option is usually a *plausible list*: "An interface may contain fields, constructors and
methods." Half of it is true. Only this is true:

| Member | Allowed in an interface? | Detail |
|---|---|---|
| Abstract methods | ✅ | implicitly `public` |
| `default` methods (Java 8+) | ✅ | with a body |
| `static` methods (Java 8+) | ✅ | with a body, not inherited by implementors |
| `private` methods (Java 9+) | ✅ in Java 9+ | ❌ in Java 8 — the pre-test runs Java 8 |
| `public static final` fields | ✅ | implicitly all three |
| Non-final instance fields | ❌ | would need per-implementation state |
| Constructors | ❌ | an interface is not instantiable, so it has no constructor |
| Instance initialiser blocks | ❌ | same reason |

## Worked example

**Q. Which of the following is TRUE about the `final` keyword in Java?**

A. A `final` class cannot be instantiated.
B. A `final` method cannot be overloaded.
C. The contents of an object referenced by a `final` field can never change.
D. A `final` field can be assigned exactly once, at its declaration, in an initialiser block, or in a constructor.

**The trap:** option C is the one most candidates choose because "final" sounds like "locked".

**What a candidate who fell for it does:** picks C, reasoning "final means the value can't change".

**The right reasoning:**

| Option | Truth value | Reason |
|---|---|---|
| A | ❌ | `final` on a class blocks **extending**, not instantiation. An abstract class is the one that blocks instantiation |
| B | ❌ | `final` blocks **overriding**. Overloading a `final` method is perfectly legal |
| C | ❌ | Only the **reference** is fixed. The referenced object stays mutable |
| D | ✅ | Exactly the three permitted assignment points for a blank or initialised `final` field |

**Answer: D.**

**Second trap in the same question:** A and B are both *nearly* right, which is what makes the
question work. Both confuse one keyword's scope. If the stem had said "cannot be **overridden**",
both B and D would need re-reading: D's "assigned exactly once" would then be off-topic, and B's
"cannot be overloaded" would be wrong because `final` blocks overriding, not overloading.

## Quick rules

- Half-true options are the ones that kill you. Read the **last clause** of every option.
- Encapsulation = data. Abstraction = implementation. Nothing blurs that line.
- Static → compile-time binding to the reference's type. Instance → run-time binding to the object.
- Overload resolution: phase 1 strict, phase 2 boxing, phase 3 varargs. In that order.
- `final` = one assignment / no extension / no override. Never "the object is frozen".
- `abstract` pairs with nothing except `public`/`protected` on a method.
- Interfaces: no constructors, no instance fields, methods may have bodies since Java 8.
- If an option mentions "optimization" or "compilation" in an OOP-principle question, it is the
  negative answer.

## Common traps

| Trap | The wrong answer you would give | The right answer | Signal that you fell for it |
|---|---|---|---|
| Abstraction hides data | "Abstraction" on a data-hiding question | Encapsulation | You quoted the word "hiding" without checking *what* is hidden |
| Static dispatch | `Child.show` | `Parent.show` | You applied "runtime polymorphism" to a static method |
| Early unboxing | `int` for an `Integer` argument | `Integer` | You skipped the phase-1 rule |
| `final` = immutable | "The contents can never change" | "Assigned exactly once" | You answered about contents instead of the reference |
| Anything goes with modifiers | "All of these are legal" | the specific illegal one | You did not check the modifier matrix |
| Interfaces can hold anything | "Interfaces can have constructors" | "Interfaces have no constructors" | You answered from "abstract class" knowledge |

## Checklist

- [ ] I can give the one-line definition of encapsulation *and* of abstraction without mixing them.
- [ ] I never pick a static-method option based on the runtime type.
- [ ] I run the 3-phase overload algorithm rather than guessing.
- [ ] I read every `final` option for the word "overrid" vs "overload" vs "assign".
- [ ] I can list the three illegal `abstract` combinations.
- [ ] I know what an interface may and may not contain in Java 8.

## Related

- [The four pillars](../01-concepts/01-the-four-pillars.md)
- [Overloading vs overriding](../01-concepts/02-overloading-vs-overriding.md)
- [`this`, `super` and the modifier matrix](../01-concepts/03-this-super-and-modifiers.md)
- [Identifying the pillar behind a code snippet](../02-techniques/01-identifying-a-pillar-procedure.md)
- [8 solved OOP questions](../03-worked-examples/01-solved-oop-questions.md)
- [OOP principles one-pager](../05-reference/01-oop-principles-one-pager.md)
- [Topic overview](../README.md)
