# Inheritance & Polymorphism — Topic Guide

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 70 min for the full topic_

## What the pre-test asks in this topic

Inheritance is where the Java section turns from recall into execution. The archetype that
dominates the 25-question paper is **"predict the output"** on a class hierarchy, plus a steady
stream of **"can this be overridden?"** and **"does this cast throw?"** questions. Typical wording:

- "Which of the following methods can be overridden by a subclass?"
- "What does this program print?" — a superclass and a subclass, a static method and an overridden
  method, called through a superclass-typed reference
- "Which statement about abstract classes is TRUE?"
- "What is the output when an object is cast to the wrong type?"
- "In what order do the constructors of a three-level hierarchy execute?"
- "Can a covariant return type be used in an override?"

Every one of these is decided by **one procedure** — the 6-step method resolution order.

## Learning objectives

After this topic you should be able to:

- State the **single inheritance, multiple implementation** rule, and what `super` refers to.
- Explain the difference between **static** and **dynamic binding**, and say which type of
  reference decides the answer in each case.
- Run the **6-step method resolution procedure** on any call and name the method that runs.
- List the **four members that cannot be overridden** — `private`, `static`, `final`, constructors —
  and say why each one is excluded.
- State the **four rules an override must obey** (same signature, visible parent, access widening
  only, no new checked exceptions) and that a **covariant** return type is allowed.
- Explain **upcasting vs downcasting**, and exactly when `ClassCastException` is thrown.
- Answer "what does `null instanceof X` return?" correctly and instantly.
- Explain why an abstract class **may have zero abstract methods** and **may have constructors**.
- Write the **constructor chain order** for a multi-level hierarchy from memory.
- Explain the **"class wins"** rule for interface `default` methods.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-inheritance-basics-and-dispatch.md](01-concepts/01-inheritance-basics-and-dispatch.md) | 242 | Vocabulary, single inheritance, `super`, static vs dynamic binding, the 6-step resolution, overriding vs hiding, covariant returns, what cannot be overridden, the constructor chain |
| [01-concepts/02-casts-type-checks-and-errors.md](01-concepts/02-casts-type-checks-and-errors.md) | 173 | Upcasting vs downcasting, `ClassCastException` triggers, `instanceof` semantics, Java 16 pattern matching, the safe-cast idiom, generic invariance |
| [01-concepts/03-abstract-final-and-the-constructor-chain.md](01-concepts/03-abstract-final-and-the-constructor-chain.md) | 220 | Abstract classes and methods, the complete illegal-modifier list, `final` semantics, the top-down constructor chain, abstract class vs interface table |
| [02-techniques/01-method-resolution-order.md](02-techniques/01-method-resolution-order.md) | 304 | The 6-step procedure, 5 fully traced examples, the "which method runs" decision table, a 45-second budget |
| [02-techniques/02-override-vs-hide-triage.md](02-techniques/02-override-vs-hide-triage.md) | 174 | The overridability triage table, the 3 legal-override conditions, restrictions and permissions, covariant legality, override vs overload |
| [03-worked-examples/01-solved-inheritance-questions.md](03-worked-examples/01-solved-inheritance-questions.md) | 398 | 8 solved questions with full distractor breakdowns |
| [04-pitfalls/01-inheritance-traps.md](04-pitfalls/01-inheritance-traps.md) | 196 | 8 traps: the wrong binding, the wrong verdict, and the abstract-class beliefs |
| [05-reference/01-inheritance-one-pager.md](05-reference/01-inheritance-one-pager.md) | 129 | 6 printable tables — the whole topic on one page |

## Quick 5-step solving procedure

1. **Find the reference's declared type** (15 s). Write it down. It decides accessibility and, for
   static methods, which method runs.
2. **Is the method static or instance?** (5 s). This is the fork. Static → bind now. Instance →
   go to step 3.
3. **Find the runtime class** of the object (10 s) — the `new` expression tells you.
4. **Walk up the hierarchy** from the runtime class (10 s). The most derived implementation wins.
   If none exists in the class chain, look for an interface `default`.
5. **Commit** (15 s). Pick the option you can defend in one sentence. **Total ≈ 55 s.**

## Key takeaways

- ✅ **Instance methods dispatch on the runtime class; static methods bind to the declared type.**
  Everything else in this topic follows from that one sentence.
- ✅ **Static methods are hidden, never overridden.** The same rule for `private` (not inherited)
  and `final` (compile error) and constructors (not inherited).
- ✅ **The most derived implementation wins** when you walk up the hierarchy.
- ✅ **A `default` interface method is the last resort** — and a class method always beats it.
- ✅ **Upcasting is implicit and safe; downcasting is explicit and can throw
  `ClassCastException` at run time.** `instanceof` is the guard.
- ✅ **`null instanceof X` is `false`** — it never throws a `NullPointerException`.
- ✅ **An abstract class may have zero abstract methods** and **may have constructors**. It only
  cannot be instantiated.
- ✅ **The constructor chain runs top-down** — `Object()` first, the subclass last.
- ✅ **Covariant (narrower) return types are legal** in an override; wider ones are not.
- ⚠️ **Meera's warning:** she tries to "understand" the whole hierarchy. You do not need to. Find
  the declared type, find the runtime class, walk up. That is three facts, not a mental model.

## Related

- [OOP Principles](../01-OOP-Principles/README.md) — overloading vs overriding, and the binding rules
  in their simplest form
- [Classes, Objects & Constructors](../02-Classes-Objects-Constructors/README.md) — the
  constructor chain in detail
- [Interfaces, Abstract & Inner Classes](../04-Interfaces-Abstract-Inner-Classes/README.md) — where
  `default` methods and functional interfaces fit in
- [Packages & Access Modifiers](../05-Packages-Access-Modifiers/README.md) — why `private` parent
  members break subclass calls
- [Collections Framework](../06-Collections-Framework/README.md) — the other big Java cluster
- [Master README](../../README.md)
