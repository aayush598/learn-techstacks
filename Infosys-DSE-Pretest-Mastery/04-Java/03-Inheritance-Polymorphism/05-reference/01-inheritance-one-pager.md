# Inheritance & Polymorphism — One-Page Revision Sheet

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 5 min_
> **Prerequisite:** [The method resolution procedure](../02-techniques/01-method-resolution-order.md)

## In one sentence

Six tables cover the topic — if you can redraw them, the inheritance questions are free marks.

## Why the pre-test tests this

- Inheritance is the biggest single source of output-prediction questions in the Java section.
- Five minutes on this page covers 3–5 questions.
- Print it. Do not re-read the concept files on the morning of the test.

## Core concept

### Table 1 — The binding rule

| | **Instance method** | **Static method** |
|---|---|---|
| Bound by | The **runtime class** of the object | The **declared type** of the reference |
| When | Run time | Compile time |
| In a subclass | **Overridden** | **Hidden** |
| `final` | Cannot be overridden | Cannot be overridden or hidden |
| `private` | Not inherited | Not inherited |

### Table 2 — The 6-step resolution

```
1. Declared type of the reference → 2. Does it declare an applicable, accessible method?
3. Is it static? → bind now. Instance? → go to 4.
4. Runtime class of the object. 5. Walk UP the hierarchy — most derived wins.
6. Otherwise a `default` interface method. Class beats default.
```

### Table 3 — What cannot be overridden

| Parent member | Overridable? |
|---|---|
| `public` / `protected` instance method | ✅ |
| package-private instance method | ✅ only from the **same package** |
| `private` instance method | ❌ not inherited → a **new** method |
| `static` method | ❌ **hidden**, not overridden |
| `final` method | ❌ compile error |
| Constructor | ❌ not inherited |

### Table 4 — Override restrictions

| Rule | Allowed |
|---|---|
| Access modifier | Same or **wider** only |
| Return type | Same or **covariant** (narrower) |
| Checked exceptions | Same or a **subset** only |

### Table 5 — Casting and type checks

| Item | Behaviour |
|---|---|
| Upcast (child → parent) | Implicit, **always safe** |
| Downcast (parent → child) | Explicit, **may throw** `ClassCastException` |
| `ClassCastException` | A **run-time** failure, not a compile error |
| `null instanceof X` | **`false`**, never throws |
| `instanceof` and subclasses | **Included** — `new Puppy() instanceof Dog` is `true` |
| `instanceof ArrayList<String>` | ❌ compile error — type arguments are erased |
| `List<Dog>` → `List<Animal>` | ❌ generics are **invariant** |

### Table 6 — Abstract and final

| Item | Rule |
|---|---|
| Abstract class | Cannot be instantiated; **may** have constructors; **may** have zero abstract methods |
| Abstract method | No body; never `private`/`static`/`final`/`synchronized` |
| Illegal combos | `abstract final`, `abstract static`, `abstract private`, `abstract synchronized`, `abstract` on a field |
| `final` class | Cannot be extended |
| `final` method | Cannot be overridden (overloading still fine) |
| `final` field | Assigned exactly once |
| Constructor chain | **Top-down**: `Object()` first, then each subclass |

## Worked example

**Q. `Parent p = new Child(); p.instanceMethod(); p.staticMethod();` → what runs?**

**Solution:** the **instance** method runs on the runtime class → `Child.instanceMethod()`. The
**static** method binds to the declared type → `Parent.staticMethod()`.

**Answer: `Child.instanceMethod()` then `Parent.staticMethod()`.** (20 seconds.)

## Quick rules

- Instance → runtime class. Static → declared type.
- Not overridable: `private`, `static`, `final`, constructors.
- Static = hidden; private = not inherited; final = compile error.
- Abstract class: cannot be instantiated; may have constructors; may have zero abstract methods.
- Constructor bodies run **top-down**.
- Covariant return = legal; wider return = compile error.
- Override may widen access, never narrow it.
- `null instanceof X` → `false`.

## Common traps

| Trap | Fix |
|---|---|
| Static dispatch | Declared type |
| Private is overridable | Not inherited |
| Abstract needs an abstract method | Zero is legal |
| Chain is bottom-up | Top-down |
| Covariant illegal | Legal |
| Downcast failure = compile error | Run-time failure |

## Checklist

- [ ] I can redraw the 6-step resolution.
- [ ] I can fill in Table 3 from memory.
- [ ] I know the four override restrictions.
- [ ] I know `instanceof` is null-safe.
- [ ] I can write the constructor chain order.
- [ ] I can state the abstract-class facts without hesitating.

## Related

- [Inheritance basics and dynamic dispatch](../01-concepts/01-inheritance-basics-and-dispatch.md)
- [Casts, type checks and ClassCastException](../01-concepts/02-casts-type-checks-and-errors.md)
- [Abstract, final and the constructor chain](../01-concepts/03-abstract-final-and-the-constructor-chain.md)
- [The method resolution procedure](../02-techniques/01-method-resolution-order.md)
- [Override vs hide triage](../02-techniques/02-override-vs-hide-triage.md)
- [8 solved inheritance questions](../03-worked-examples/01-solved-inheritance-questions.md)
- [Inheritance traps](../04-pitfalls/01-inheritance-traps.md)
- [Topic overview](../README.md)
