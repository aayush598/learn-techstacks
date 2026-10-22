# Interfaces, Abstract & Inner Classes — Topic Guide

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 75 min for the full topic_

## What the pre-test asks in this topic

This topic has two halves that the exam treats as one. The first is the **interface contract** —
what an interface may contain, and what happens when two interfaces disagree. The second is the
**nested class family** — static nested, inner, local and anonymous classes, and the rules that
decide which one you are looking at. Typical wording:

- "Which of the following can an interface contain in Java 8?"
- "Which of the following is a marker interface / a functional interface?"
- "Can the following code be replaced by a lambda expression?"
- "What does this program print?" — a class implementing two interfaces, or a lambda, or an inner
  class
- "Which of the following is TRUE about inner classes?"
- "What is the output when an inner class accesses an outer field with the same name?"

Every one of these is decided by four facts: **implicit modifiers**, the **conflict rules**,
**lambda eligibility**, and **the outer-instance attachment**.

## Learning objectives

After this topic you should be able to:

- List every member an interface may contain in **Java 8**, and the **implicit modifiers** each one
  gets.
- State which interface features arrived in **Java 8**, **Java 9** and **Java 17**, and say which
  version the pre-test assumes.
- Explain why an interface has **no constructors**, **no instance fields** and **no instance
  initialisers**.
- Compare an interface with an abstract class across **six** dimensions, and know which one to pick
  for "capability across unrelated hierarchies" versus "shared code and shared state".
- Apply the **3 conflict rules** in order — class wins, sub-interface wins, otherwise you must
  override — and write the `InterfaceName.super.method()` disambiguation.
- Decide whether an interface is a **functional interface** and therefore a valid **lambda**
  target, counting only **abstract** methods.
- Write a lambda and all **four** method-reference forms, and explain that a method reference is
  shorthand for a lambda.
- Distinguish a **static nested class**, an **inner class**, a **local class** and an **anonymous
  class** by outer-instance attachment, static-member rules and creation syntax.
- Explain **shadowing** and use `Outer.this.field` to reach the outer field.
- Choose between an **anonymous class**, a **lambda** and a **named class** for a given
  requirement.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-interface-anatomy.md](01-concepts/01-interface-anatomy.md) | 198 | Implicit modifiers for every member, the Java-version timeline, interface vs abstract class table, marker and functional interfaces, `sealed` in brief |
| [01-concepts/02-lambdas-and-functional-interfaces.md](01-concepts/02-lambdas-and-functional-interfaces.md) | 208 | Lambda syntax, target typing, the four method-reference forms, the common functional interfaces, anonymous class vs lambda |
| [01-concepts/03-nested-and-inner-classes.md](01-concepts/03-nested-and-inner-classes.md) | 237 | The four nested-class kinds, creation syntax, `Outer.this`, shadowing, access rules |
| [02-techniques/01-default-method-conflict-resolution.md](02-techniques/01-default-method-conflict-resolution.md) | 244 | The 3 rules in order, 4 worked traces, `I.super.m()`, the diamond, the two hard limits on `default` methods |
| [02-techniques/02-choosing-anonymous-lambda-or-named-class.md](02-techniques/02-choosing-anonymous-lambda-or-named-class.md) | 205 | The capability matrix, the 4-step choice procedure, 3 worked examples, the exact limit on lambda mutation |
| [03-worked-examples/01-solved-interfaces-inner-questions.md](03-worked-examples/01-solved-interfaces-inner-questions.md) | 400 | 8 solved questions with full distractor breakdowns |
| [04-pitfalls/01-interfaces-inner-traps.md](04-pitfalls/01-interfaces-inner-traps.md) | 250 | 12 traps: the Java 1.4 beliefs and the inner-class misconceptions |
| [05-reference/01-interfaces-inner-one-pager.md](05-reference/01-interfaces-inner-one-pager.md) | 151 | 6 printable tables — the whole topic on one page |

## Quick 5-step solving procedure

1. **Identify the member kind** (10 s). Field, abstract method, `default`, `static`, or nested
   class? Write down the **implicit modifiers** the compiler adds.
2. **Check the Java version** (10 s). The pre-test is **Java 8**: `default` and `static` exist,
   `private` interface methods do not, and inner classes cannot have static members.
3. **If two defaults collide, run the 3 rules** (20 s). Class → sub-interface → must override.
4. **If a lambda appears, count abstract methods** (10 s). Exactly one? Then it compiles. Zero or
   two? Then it does not.
5. **Commit** (15 s). **Total ≈ 65 s.**

## Key takeaways

- ✅ **Every interface field is `public static final`; every interface method is `public`.** There
  are no instance fields and no constructors in an interface.
- ✅ **`default` and `static` interface methods are Java 8; `private` ones are Java 9; `sealed` is
  Java 17.** The pre-test runs Java 8.
- ✅ **A class method beats an interface `default`.** A **sub**-interface beats its super-interface.
  Two **unrelated** defaults are a **compile error** unless you override and call `I.super.m()`.
- ✅ **A lambda target must have exactly one abstract method.** `default` methods do not count.
  Zero abstract methods is not a functional interface either.
- ✅ **A method reference is shorthand for a lambda** — `Type::static`, `Type::instance` (first
  argument), `instance::instance` (bound), `Type::new` (constructor).
- ✅ **A lambda has no fields and no `this` of its own.** It captures effectively final locals and
  can mutate captured objects, but it cannot declare state.
- ✅ **An inner class carries an outer instance.** Create it with `outer.new Inner()`; reach the
  outer field with `Outer.this.field`.
- ✅ **The inner field shadows the outer one.** The innermost scope wins for a simple name.
- ✅ **Static nested classes need no outer instance** — `new Outer.Nested()`.
- ⚠️ **Meera's warning:** she writes a lambda for everything because "it is modern". She then
  loses a mark on the interface with two abstract methods. Count the abstract methods first.

## Related

- [OOP Principles](../01-OOP-Principles/README.md) — abstract class vs interface in its simplest
  form
- [Classes, Objects & Constructors](../02-Classes-Objects-Constructors/README.md) — nested classes
  are still classes
- [Inheritance & Polymorphism](../03-Inheritance-Polymorphism/README.md) — where `default` methods
  and `super` calls fit in
- [Packages & Access Modifiers](../05-Packages-Access-Modifiers/README.md) — how `public` and
  `default` visibility is enforced across packages
- [Collections Framework](../06-Collections-Framework/README.md) — the other big Java cluster
- [Master README](../../README.md)
