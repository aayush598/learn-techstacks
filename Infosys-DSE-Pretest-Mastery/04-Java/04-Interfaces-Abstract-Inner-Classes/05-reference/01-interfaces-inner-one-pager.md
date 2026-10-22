# Interfaces & Inner Classes — One-Page Revision Sheet

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 5 min_
> **Prerequisite:** [Default method conflict resolution](../02-techniques/01-default-method-conflict-resolution.md)

## In one sentence

Six tables cover the topic — if you can redraw them, the interface and inner-class questions are
free marks.

## Why the pre-test tests this

- Interface-member questions appear 3–4 times in the paper.
- Five minutes on this page covers 3–4 questions.
- Print it. Do not re-read the concept files on the morning of the test.

## Core concept

### Table 1 — Interface members and their implicit modifiers

| Declaration | Becomes | Java version |
|---|---|---|
| `int x = 0;` | `public static final int x = 0;` | all |
| `void run();` | `public abstract void run();` | all |
| `default void run() { }` | `public default void run() { }` | **8** |
| `static void make() { }` | `public static void make() { }` | **8** |
| `private void help() { }` | `private void help() { }` | **9** |
| Constructor | ❌ **not allowed** | — |
| Instance field | ❌ **not allowed** | — |
| Instance initialiser | ❌ **not allowed** | — |

### Table 2 — Interface vs abstract class

| Dimension | Interface | Abstract class |
|---|---|---|
| Multiple parents | ✅ many interfaces | ❌ one class |
| Constructors | ❌ | ✅ |
| Instance fields | ❌ only `public static final` | ✅ any |
| Method bodies | `default` / `static` | any mix |
| `super` / `this` in initialisers | ❌ | ✅ |
| Best for | Capability | Shared code + state |

### Table 3 — The 3 conflict rules, in order

| # | Rule |
|---|---|
| 1 | **Class wins** — a concrete class method beats any interface `default` |
| 2 | **Sub-interface wins** — the more specific `default` is used |
| 3 | **Unrelated defaults → compile error** — you must override and call `I.super.m()` |

### Table 4 — The four nested-class kinds

| Kind | Outer instance? | Static members (Java 8)? | Creation |
|---|---|---|---|
| Static nested | ❌ | ✅ | `new Outer.Nested()` |
| Inner (non-static) | ✅ | ❌ | `outer.new Inner()` |
| Local class | ✅ (in an instance context) | ❌ | `new Local()` |
| Anonymous class | ✅ (in an instance context) | ❌ | `new Iface() { ... }` |

### Table 5 — Lambda eligibility

| Target type | Lambda legal? |
|---|---|
| Exactly **one** abstract method | ✅ |
| Two or more abstract methods | ❌ `not a functional interface` |
| **Zero** abstract methods | ❌ `no abstract method found` |
| `default` methods present | ✅ — they do **not** count |

| Method reference | Means |
|---|---|
| `Type::staticMethod` | A static method of `Type` |
| `Type::instanceMethod` | An instance method of the **first argument** |
| `instance::instanceMethod` | An instance method of a **bound** object |
| `Type::new` | A constructor of `Type` |

### Table 6 — Anonymous class vs lambda vs named class

| Capability | Anonymous | Lambda | Named |
|---|---|---|---|
| Implements 2+ abstract methods | ✅ | ❌ | ✅ |
| Extends a class | ✅ | ❌ | ✅ |
| Declares fields | ✅ | ❌ | ✅ |
| Declares a constructor | ❌ | ❌ | ✅ |
| Holds mutable state | ✅ | ❌ (captures only) | ✅ |
| Has a name | ❌ | ❌ | ✅ |
| `Serializable` | ✅ | ❌ | ✅ |
| Available from | Java 1.0 | **Java 8** | Java 1.0 |

## Worked example

**Q. `interface A { default void run() { print("A"); } }`, `interface B { default void run() {
print("B"); } }`, `class C implements A, B { public void run() { A.super.run(); B.super.run(); } }`
→ what prints?**

**Solution:** `A` and `B` are **unrelated** interfaces, so rule 3 applies — `C` **must** override.
The override calls `A.super.run()` then `B.super.run()`, in statement order.

**Answer: `A` then `B`.** (25 seconds.)

**Q. `class Base { public void print() { print("base"); } }`, `class Doc extends Base implements P`
where `P` has a `default print()` → what prints?**

**Solution:** rule 1 — the **class** method wins.

**Answer: `base`.** (15 seconds.)

## Quick rules

- Interface fields: `public static final`. Interface methods: `public`.
- `default`/`static` → Java 8. `private` → Java 9. `sealed` → Java 17.
- Conflict order: **class → sub-interface → must override**.
- A lambda needs **exactly one abstract method**.
- Inner class → `outer.new Inner()`. Static nested → `new Outer.Nested()`.
- The **inner** field shadows the outer; `Outer.this.field` reaches the outer.
- A local class captures **effectively final** locals.
- Static interface methods are **not inherited**.

## Common traps

| Trap | Fix |
|---|---|
| All interface methods are abstract | Java 8 added `default`/`static` |
| Interface methods are package-private | They are `public` |
| Interfaces have instance fields | Only `public static final` |
| Interfaces have constructors | They have none |
| Private interface methods in Java 8 | Java 9 |
| One interface per class | Any number |
| The default beats the class method | The class wins |
| Unrelated defaults pick one | Compile error |
| Inner classes can have statics | Not in Java 8 |
| The outer field shadows the inner | The inner wins |

## Checklist

- [ ] I can redraw all 6 tables.
- [ ] I know the Java version of every interface feature.
- [ ] I can recite the 3 conflict rules in order.
- [ ] I know the 4 nested-class kinds and their creation syntax.
- [ ] I know what counts toward the "one abstract method" limit.
- [ ] I can write `I.super.m()` and say when it is legal.

## Related

- [Interface anatomy](../01-concepts/01-interface-anatomy.md)
- [Lambdas and functional interfaces](../01-concepts/02-lambdas-and-functional-interfaces.md)
- [Nested and inner classes](../01-concepts/03-nested-and-inner-classes.md)
- [Default method conflict resolution](../02-techniques/01-default-method-conflict-resolution.md)
- [Anonymous class, lambda, or named class?](../02-techniques/02-choosing-anonymous-lambda-or-named-class.md)
- [8 solved interfaces and inner-class questions](../03-worked-examples/01-solved-interfaces-inner-questions.md)
- [Interfaces and inner-class traps](../04-pitfalls/01-interfaces-inner-traps.md)
- [Topic overview](../README.md)
