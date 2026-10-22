# OOP Principles — One-Page Revision Sheet

> Section 4 · Java · OOP Principles · _Estimated reading time: 5 min_
> **Prerequisite:** [Overloading vs overriding](../01-concepts/02-overloading-vs-overriding.md)

## In one sentence

If you can reproduce the four tables on this page from memory, you own the OOP-principles
questions — they are the cheapest marks in the Java section.

## Why the pre-test tests this

- Concept questions are the fast 1-markers in a 25-question section.
- This page is the whole revision surface for the topic. Five minutes here buys 3–4 questions.
- Print it. Do not re-read the concept files the morning of the test.

## Core concept

### Table 1 — The four pillars

| Pillar | Hides / does | Java mechanism |
|---|---|---|
| **Encapsulation** | Hides **data** | `private` fields + accessors |
| **Abstraction** | Hides **implementation**, exposes behaviour | abstract classes, interfaces |
| **Inheritance** | Reuses via a parent-child type relation | `extends`, `implements` |
| **Polymorphism** | One reference, many behaviours | overloading + overriding |

**Not pillars:** compilation, optimization, parallelism, serialization, modularity.

### Table 2 — Overloading vs overriding

| | Overloading | Overriding |
|---|---|---|
| Where | Same class | Parent → child |
| Signature | Same name, **different parameters** | Same name, **same parameters** |
| Also called | Compile-time polymorphism | Run-time polymorphism |
| Resolved by | The compiler | The JVM |
| Return type | Independent | Same or **covariant** (narrower) |
| Access | Any | Same or **wider** only |
| Exceptions | Any | No **new checked** exceptions |
| `static` / `final` / `private` | Overloadable | **Never overridable** |

**Override requires all four:** same name · same parameters · parent method is not `private`,
`static` or `final` · and the child version must respect access and exception rules.

### Table 3 — Modifier matrix

| Target | `final` means | `abstract` allowed? | `static` allowed? |
|---|---|---|---|
| Class | Cannot be extended | ✅ (then not instantiable) | ❌ (top-level class) |
| Method | Cannot be overridden | ✅ (no body) | ❌ **together with `abstract`** |
| Field | Assigned exactly once | ❌ | ✅ |

**Illegal combos:** `abstract static`, `abstract final`, `abstract private` on a method;
`abstract` on a field.

### Table 4 — `this` / `super` / `static` context

| Keyword | Points to | In a static method |
|---|---|---|
| `this` | Current object | ❌ compile error |
| `super` | Immediate parent | ❌ compile error |
| `this(args)` | Another constructor of this class | Must be the **first** statement |
| `super(args)` | The parent's constructor | Must be the **first** statement |

`this(...)` and `super(...)` cannot both appear in one constructor.

### Table 5 — Static vs instance dispatch

| Call | Which method runs | Bound when |
|---|---|---|
| `ref.instanceMethod()` | The **runtime class** of the object | Run time |
| `ref.staticMethod()` | The **declared type** of the reference | Compile time |
| `Parent p = new Child(); p.display();` | `Child.display()` | Run time |
| `Parent p = new Child(); p.show();` (`show` static) | `Parent.show()` | Compile time |

## Worked example

**Q. Which of these is NOT an OOP principle? (A) Encapsulation (B) Polymorphism (C) Compilation
(D) Inheritance**

**Solution:** the four pillars are E, A, I, P. Compilation is a build step, not a design principle.

**Answer: C.** (35 seconds. Do not re-read the stem.)

## Quick rules

- Four pillars, letter by letter: **E A I P**.
- Data hidden = encapsulation. Implementation hidden = abstraction.
- One class extended, many interfaces implemented.
- Interface: no constructors, no instance fields, `public static final` fields only.
- Class method beats interface default method. No error.
- Overload: strict → boxing → varargs.
- Static binds to the reference; instance binds to the object.
- `final` fixes the reference, blocks extension, blocks overriding.
- Abstract class: constructors ✅, state ✅, concrete methods ✅, cannot be instantiated.

## Common traps

| Trap | Fix |
|---|---|
| Abstraction = hiding data | Data → encapsulation |
| `Child.show` for a static call | Reference's type decides |
| Unboxing in phase 1 | Strict phase first |
| `final` = immutable | Reference only |
| Interface can hold constructors | It cannot |
| "Optimisation" as a pillar | It is not |

## Checklist

- [ ] I can write the four pillars in 5 seconds.
- [ ] I can write the 4 override conditions in 20 seconds.
- [ ] I can name the 3 illegal `abstract` combinations.
- [ ] I can state the "class wins" default-method rule.
- [ ] I can predict the `Parent p = new Child()` output both for a static and an instance method.
- [ ] I know the three phrases that are never pillars.

## Related

- [The four pillars](../01-concepts/01-the-four-pillars.md)
- [Overloading vs overriding](../01-concepts/02-overloading-vs-overriding.md)
- [`this`, `super` and the modifier matrix](../01-concepts/03-this-super-and-modifiers.md)
- [Abstract class vs interface](../02-techniques/02-abstract-class-vs-interface.md)
- [8 solved OOP questions](../03-worked-examples/01-solved-oop-questions.md)
- [OOP principles traps](../04-pitfalls/01-oop-principles-traps.md)
- [Topic overview](../README.md)
