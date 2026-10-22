# OOP Principles — Topic Guide

> Section 4 · Java · OOP Principles · _Estimated reading time: 60 min for the full topic_

## What the pre-test asks in this topic

The Java section is **25 questions in ~35 minutes** — the biggest section of the paper, and the
one where a single careless choice costs you a stream. The **OOP principles** cluster is the
conceptual core of that section. Typical archetypes:

- "Which of the following is NOT a principle of object-oriented programming?" (4 options, 1 mark)
- "Which OOP concept is demonstrated by this code?" — a 6-line snippet, 1 mark
- "Overloading vs overriding" — one of the highest-frequency Java MCQ families
- "Which modifier combination is a compile error?" / "Does this code compile?"
- Output prediction on a superclass/subclass pair where a `static` method and an overridden method
  are called through the same reference
- "Abstract class vs interface" — the single most-tested comparison in the Java section

Every one of these is answerable in **under 90 seconds** if you own the tables in this topic.
Every one of them is lost by picking the plausible option instead of the correct one.

## Learning objectives

After this topic you should be able to:

- List the four pillars of OOP and define each one in a single sentence, with **no overlap**
  between encapsulation and abstraction.
- Say why "compilation", "optimization" and "parallelism" are not OOP principles, and recognise
  them as negative-answer distractors.
- Distinguish **class** from **object** from **instance**, and count objects correctly in code.
- Explain the difference between **overloading** and **overriding** in terms of location,
  signature, binding time and the four conditions an override requires.
- Run the **3-phase overload resolution algorithm** (strict → loose → varargs) on any call.
- Predict the output of `Parent p = new Child(); p.instanceMethod(); p.staticMethod();` correctly.
- Apply the **modifier matrix**: know exactly which of `abstract` / `final` / `static` / `private`
  may be combined, and on what.
- Explain what `this` and `super` point to, when each is illegal, and how field shadowing resolves.
- Choose between an **abstract class** and an **interface** using the 5-question procedure, and
  state the "one class, many interfaces" rule.
- Explain **high cohesion + low coupling**, and map the SOLID letters to one line each.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-the-four-pillars.md](01-concepts/01-the-four-pillars.md) | 189 | The four pillars, class vs object vs instance, coupling/cohesion, SOLID, and the "NOT a principle" kill list |
| [01-concepts/02-overloading-vs-overriding.md](01-concepts/02-overloading-vs-overriding.md) | 219 | Compile-time vs run-time polymorphism, the 4 override conditions, 3-phase overload resolution, hiding vs overriding, covariant returns |
| [01-concepts/03-this-super-and-modifiers.md](01-concepts/03-this-super-and-modifiers.md) | 189 | `this` vs `super`, shadowing, the legal/illegal modifier matrix, what `final` actually blocks |
| [02-techniques/01-identifying-a-pillar-procedure.md](02-techniques/01-identifying-a-pillar-procedure.md) | 181 | The 4-check procedure, the tie-break table, the negative-stem kill list, a 55-second budget |
| [02-techniques/02-abstract-class-vs-interface.md](02-techniques/02-abstract-class-vs-interface.md) | 215 | Full comparison table, the 3 hard rules, a 5-question decision procedure, the "class wins" rule |
| [03-worked-examples/01-solved-oop-questions.md](03-worked-examples/01-solved-oop-questions.md) | 394 | 8 solved questions with full distractor breakdowns |
| [04-pitfalls/01-oop-principles-traps.md](04-pitfalls/01-oop-principles-traps.md) | 166 | 6 half-true traps: the abstraction swap, static-as-polymorphic, early unboxing, `final` ≠ immutable, modifier combos, interface over-claiming |
| [05-reference/01-oop-principles-one-pager.md](05-reference/01-oop-principles-one-pager.md) | 126 | 5 printable tables — the whole topic on one page |

## Quick 5-step solving procedure

1. **Classify the question (10 s).** Concept (which principle?) / compile-or-not / output
   prediction / comparison (abstract vs interface). The classification tells you which table to open.
2. **Read the stem's verb (10 s).** "Demonstrated by" → the concept in the code. "Allowed" →
   the compile rule. "Prints" → the binding rule.
3. **Open the one table you need (20 s).** Pillars, overload/override, modifier matrix, or the
   abstract-class-vs-interface table. Do not read all four.
4. **Eliminate 2 options (20 s).** Negative stems: hunt the kill list. Positive stems: apply the
   4 checks in order and kill the options that do not fire.
5. **Commit (15 s).** If two options survive, pick the one you can defend in one sentence, mark
   it, and move. **Total ≈ 75 s.**

## Key takeaways

- ✅ **The four pillars are Encapsulation, Abstraction, Inheritance, Polymorphism.** Nothing else
  makes the list. Compilation, optimization and parallelism are the traps.
- ✅ **Encapsulation hides data; abstraction hides implementation.** These two get swapped on
  roughly every paper — memorise the difference, not just the words.
- ✅ **Overloading = compiler, same class, different parameters. Overriding = JVM, parent/child,
  same parameters.** A method is overridden only if the parent's is visible, non-`static` and
  non-`final`.
- ✅ **Static binds to the reference's declared type; instance methods bind to the object's runtime
  type.** This one pair of lines is the most-asked output question in the Java section.
- ✅ **Overload resolution runs strict → boxing → varargs, in that order.** Never jump to varargs.
- ✅ **`abstract` cannot sit with `static`, `final` or `private` on a method.** `abstract` on a
  field is illegal too.
- ✅ **`this` = current object, `super` = immediate parent.** Neither is legal in a static method;
  `this(...)` and `super(...)` must be the first statement of a constructor, and never both.
- ✅ **One class extended, unlimited interfaces implemented.** An interface has no constructors and
  no instance fields.
- ✅ **A superclass method beats an interface `default` method** — no compile error, no
  `@Override` needed. Remember this and Q8 above is free.
- ⚠️ **Rahul's warning:** he knows the theory but re-reads all four options. Two options are
  decoys by construction. Eliminate, then choose — never read every word of every option.

## Related

- [Classes, Objects & Constructors](../02-Classes-Objects-Constructors/README.md) — how objects
  actually come into existence
- [Inheritance & Polymorphism](../03-Inheritance-Polymorphism/README.md) — the dynamic dispatch
  machinery in full
- [Interfaces, Abstract & Inner Classes](../04-Interfaces-Abstract-Inner-Classes/README.md) — the
  other half of the abstraction question
- [Packages & Access Modifiers](../05-Packages-Access-Modifiers/README.md) — where `private` and
  `protected` actually reach
- [Collections Framework](../06-Collections-Framework/README.md) — the other 25-question-scale
  Java cluster
- [Master README](../../README.md)
