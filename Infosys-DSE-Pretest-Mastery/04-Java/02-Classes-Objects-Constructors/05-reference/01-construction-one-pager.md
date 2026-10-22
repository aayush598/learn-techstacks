# Classes & Objects — One-Page Revision Sheet

> Section 4 · Java · Classes, Objects & Constructors · _Estimated reading time: 5 min_
> **Prerequisite:** [Constructor rules and compile errors](../02-techniques/01-constructor-rules-and-compile-errors.md)

## In one sentence

Six tables cover the whole topic — if you can redraw them from memory, the construction questions
are free marks.

## Why the pre-test tests this

- Construction questions are the "does it compile / what does it print" backbone of the Java
  section.
- This page is the whole revision surface. Five minutes here covers 3–5 questions.
- Print it. Do not re-read the concept files on the morning of the test.

## Core concept

### Table 1 — Constructor rules

| Rule | Statement |
|---|---|
| Return type | **None.** `void Foo()` is a method, not a constructor |
| Default constructor | Generated **only** if the class declares no constructor; same visibility as the class |
| `this(...)` / `super(...)` | Must be the **first statement**; **one or the other**, never both |
| No explicit call | The compiler inserts `super()` at the top |
| Inheritance | Constructors are **not** inherited |
| Overloading | ✅ allowed |

### Table 2 — The creation order

```
CLASS PHASE (once)
  superclass static fields + static blocks   ← superclass FIRST
  this class's static fields + static blocks (textual order)

OBJECT PHASE (per new)
  1. superclass instance fields + instance blocks (textual order)
  2. superclass constructor body
  3. this class's instance fields + instance blocks (textual order)
  4. this constructor body                       ← LAST
```

### Table 3 — Instance vs static initialisers

| | Instance block `{ }` | Static block `static { }` |
|---|---|---|
| Runs | Once per **object** | Once per **class** |
| `this` / `super` | ✅ | ❌ |
| Order | After the superclass constructor, before this constructor's body | At class load, superclass first |

### Table 4 — `final` fields

| Declaration | Rule |
|---|---|
| `final int x = 5;` | Assigned once at declaration; never again |
| `final int x;` (blank) | Assigned exactly once, in **every** constructor or an instance initialiser block |
| `static final int X;` (blank) | Assigned in a `static` initialiser block or at the declaration |

### Table 5 — Identity, equality and copying

| Item | Behaviour |
|---|---|
| `==` on objects | Compares **references** |
| Default `equals` | **Reference identity** |
| `hashCode` default | Identity hash |
| Contract | `equals` ⇒ equal hash codes. Override **both** together |
| `clone()` | `protected`, needs `Cloneable`, **shallow** |
| Deep copy | You must copy the nested objects yourself |
| `transient` / `static` fields | Never serialized |

### Table 6 — Creation patterns

| Pattern | When | Thread-safe? |
|---|---|---|
| **Eager singleton** | Cheap construction, needed immediately | ✅ |
| **Lazy singleton (naive)** | — | ❌ race |
| **Holder-idiom singleton** | Lazy + safe | ✅ **without `synchronized`** |
| **Double-checked locking** | Lazy + safe | ✅ only with `volatile` |
| **Immutable class** | Value objects | `private final` + no setters + `final` class + defensive copies + no mutable statics |
| **Factory method** | Few, fixed parameters; hides the concrete type | n/a |
| **Builder** | Many / optional parameters | n/a |

### Table 7 — Deprecated / modern APIs

| Old | Modern |
|---|---|
| `Class.newInstance()` (deprecated Java 9) | `clazz.getDeclaredConstructor().newInstance()` |
| `finalize()` (deprecated Java 9) | `close()` via try-with-resources |
| — | `Cleaner` (Java 9+) if you truly cannot |

## Worked example

**Q. What does this print?**

```java
class C {
    int x = 5;
    { x = x * 2; }
    C() { x = x + 1; }
}
new C().x
```

**Solution:** field initialiser → `5`; instance block → `10`; constructor body → `11`.

**Answer: `11`.** (25 seconds. Textual order, body last.)

## Quick rules

- Default constructor only when no constructor is declared.
- `this(...)` / `super(...)`: first statement, one of them.
- Textual order for fields and blocks; constructor body last.
- Superclass static first; superclass instance state before subclass instance state.
- Blank final assigned in every constructor.
- `clone()` is shallow; `Cloneable` required.
- `equals` and `hashCode` go together.
- `finalize()` is deprecated and never guaranteed.
- Holder idiom = the thread-safe lazy singleton.

## Common traps

| Trap | Fix |
|---|---|
| Default constructor always exists | Only if none declared |
| `super()` after a statement | Must be first |
| Initialiser after the body | Before |
| Subclass static first | Superclass first |
| `clone()` is deep | Shallow |
| `equals` implies `hashCode` | Override both |
| `finalize()` guaranteed | Never guaranteed |
| Naive singleton is safe | It races |

## Checklist

- [ ] I can redraw the creation-order template.
- [ ] I can name the three automatic Java actions.
- [ ] I know the `equals` contract rule 4 verbatim.
- [ ] I know `clone()` is shallow and needs `Cloneable`.
- [ ] I can write the holder-idiom singleton.
- [ ] I can list the 5 immutability rules.

## Related

- [Object lifecycle and construction](../01-concepts/01-object-lifecycle-and-construction.md)
- [Object creation, copying and identity](../01-concepts/02-object-creation-copying-and-identity.md)
- [Constructor rules and compile errors](../02-techniques/01-constructor-rules-and-compile-errors.md)
- [Creation patterns: singleton, immutable, factory, builder](../02-techniques/02-creation-patterns.md)
- [8 solved construction questions](../03-worked-examples/01-solved-construction-questions.md)
- [Construction traps](../04-pitfalls/01-construction-and-object-traps.md)
- [Topic overview](../README.md)
