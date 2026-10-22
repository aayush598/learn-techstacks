# Classes, Objects & Constructors — Topic Guide

> Section 4 · Java · Classes, Objects & Constructors · _Estimated reading time: 70 min for the full topic_

## What the pre-test asks in this topic

Java's 25-question section is dominated by two archetypes: **"does this code compile?"** and
**"what does this program print?"**. The classes-and-objects topic supplies the raw material for
both. Typical questions:

- "If a class does not declare any constructor, what does the compiler generate?"
- "Which of these code snippets will compile?" — decided entirely by constructor rules
- "What is the output of this program?" — a class with static blocks, instance blocks and
  field initialisers
- "Which method is used to create an object dynamically?" / "Which method is deprecated?"
- "What does `clone()` return? Is it a deep copy?"
- "If two objects are equal, what must be true of their hash codes?"
- "Which singleton implementation is thread-safe without `synchronized`?"

None of these need more than one table. All of them are lost to a half-remembered rule.

## Learning objectives

After this topic you should be able to:

- State the **default-constructor rule** and the visibility of the generated constructor.
- Explain why a constructor has **no return type**, and why constructors are **not inherited**.
- Apply the **three constructor rules** — first-statement placement, mutual exclusivity of
  `this()`/`super()`, and definite assignment of blank finals — to any snippet.
- Write the **7-step object-creation order** from memory and use it to predict any
  static/instance-block output.
- Explain the difference between **instance initialiser blocks** and **static initialiser blocks**
  and when each runs.
- Distinguish **`new`**, **reflection** (`getDeclaredConstructor().newInstance()`) and the
  deprecated `Class.newInstance()`.
- Say what **`clone()`** returns, why `Cloneable` is required, and what **shallow** means.
- State the **`equals`/`hashCode` contract**, and why overriding one without the other is a bug.
- Explain what **`finalize()`** does, that it is **deprecated**, and that it is **never
  guaranteed** to run.
- Choose between **eager**, **lazy**, **holder-idiom** and **double-checked** singletons, and
  between **factory method** and **builder**.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-object-lifecycle-and-construction.md](01-concepts/01-object-lifecycle-and-construction.md) | 241 | The default-constructor rule, constructor chaining, the 7-step creation order, instance vs static blocks, blank finals, `this` escape |
| [01-concepts/02-object-creation-copying-and-identity.md](01-concepts/02-object-creation-copying-and-identity.md) | 210 | `new` vs reflection vs `newInstance()`, shallow vs deep copy, the `equals`/`hashCode` contract, serialization basics, deprecated `finalize()` |
| [02-techniques/01-constructor-rules-and-compile-errors.md](02-techniques/01-constructor-rules-and-compile-errors.md) | 232 | The 6-step constructor scan, the 5 illegal variants and their fixes, the ordering template, a 60-second budget |
| [02-techniques/02-creation-patterns.md](02-techniques/02-creation-patterns.md) | 156 | The 4 singleton variants, the 5-rule immutability checklist, factory method vs builder, related idioms |
| [03-worked-examples/01-solved-construction-questions.md](03-worked-examples/01-solved-construction-questions.md) | 399 | 8 solved questions with full distractor breakdowns |
| [04-pitfalls/01-construction-and-object-traps.md](04-pitfalls/01-construction-and-object-traps.md) | 199 | 8 traps: the phantom default constructor, `super()` placement, the two ordering traps, shallow-copy depth, the equals/hashCode pairing, `finalize()` reliability, the singleton race |
| [05-reference/01-construction-one-pager.md](05-reference/01-construction-one-pager.md) | 152 | 7 printable tables — the whole topic on one page |

## Quick 5-step solving procedure

1. **Classify (10 s).** Compile-or-not, output prediction, or concept question?
2. **If compile-or-not:** run the **6-step constructor scan** (20 s) — return type, `this`/`super`
   present, first statement, both-or-neither, parent constructor, blank finals.
3. **If output prediction:** run the **creation-order template** (20 s) — static phase, then
   object phase, then the constructor body last.
4. **If concept:** open the **one relevant table** in the one-pager (15 s) — no more than one.
5. **Commit (15 s).** Pick the option you can defend in one sentence. **Total ≈ 80 s.**

## Key takeaways

- ✅ **A default constructor is generated only if the class declares none.** Its visibility
  matches the class's.
- ✅ **`this(...)` and `super(...)` must be the first statement**, and you may use **one or the
  other, never both**. An explicit `super(...)` replaces the implicit one.
- ✅ **Creation order:** static (superclass first) → superclass instance state → subclass
  instance state → subclass constructor body. The body is always **last**.
- ✅ **Instance blocks run per object; static blocks run per class** — they never interleave.
- ✅ **A blank `final` must be assigned in every constructor** (or in an instance initialiser
  block). Assigning a `final` once is legal, not an error.
- ✅ **`clone()` is shallow** and requires `Cloneable`, otherwise
  `CloneNotSupportedException`. Primitives copy by value; references are shared.
- ✅ **Override `equals` and `hashCode` together.** Equal objects ⇒ equal hash codes; the
  converse is not required.
- ✅ **`finalize()` is deprecated** and **never guaranteed** to run. `transient` and `static`
  fields are skipped by serialization.
- ✅ **The holder idiom is the thread-safe lazy singleton** with no `synchronized` keyword.
- ⚠️ **Meera's warning:** she reads every line of the snippet and runs out of time. For output
  questions, find the **constructor body** first — that is usually the last line printed.

## Related

- [OOP Principles](../01-OOP-Principles/README.md) — the pillars that define what a class *is*
- [Inheritance & Polymorphism](../03-Inheritance-Polymorphism/README.md) — the `super()` chain in
  depth
- [Interfaces, Abstract & Inner Classes](../04-Interfaces-Abstract-Inner-Classes/README.md) —
  abstract classes compared against interfaces
- [Packages & Access Modifiers](../05-Packages-Access-Modifiers/README.md) — where `private`
  fields actually live
- [Collections Framework](../06-Collections-Framework/README.md) — the other big Java cluster
- [Master README](../../README.md)
