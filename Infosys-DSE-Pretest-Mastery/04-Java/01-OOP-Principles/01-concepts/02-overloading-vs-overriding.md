# Overloading vs Overriding — Compile-Time vs Run-Time Polymorphism

> Section 4 · Java · OOP Principles · _Estimated reading time: 9 min_
> **Prerequisite:** [The four pillars](01-the-four-pillars.md)

## In one sentence

**Overloading = same method name, different parameter list, resolved by the compiler at compile
time; overriding = same method signature in a subclass, resolved by the JVM at run time.**

## Why the pre-test tests this

- This is the single most-repeated Java question family in the pre-test: "the difference between
  overloading and overriding", "which method does the compiler pick", "is this overriding or
  overloading".
- Output-prediction questions lean on it constantly: the same call `obj.f(5)` can dispatch to
  different methods depending on the **static type** of `obj` or the **runtime class**.
- The classic "NOT overriding" conditions (private, static, final, different return type) are
  memorised or lost.

## Core concept

### The side-by-side table

| Dimension | **Overloading** | **Overriding** |
|---|---|---|
| Also called | Compile-time polymorphism, static polymorphism | Run-time polymorphism, dynamic polymorphism |
| Happens | Inside **one** class (methods at the same level) | Between a **superclass and a subclass** |
| Signature | **Same name, different parameter list** | **Same name, same parameter list**, return type may be narrower |
| Return type | May be **any** type (independent of the overloads) | Must be the same or **covariant** (a subtype) |
| Access modifier | Any | Cannot be **more restrictive** than the parent's |
| Exceptions | Any | Cannot throw **new checked exceptions**; unchecked are always allowed |
| Resolution | By the **compiler**, using the static types of the arguments | By the **JVM**, using the runtime class of the receiver |
| `static` methods | Can be overloaded | **Cannot be overridden** — they are *hidden* instead |
| `final` methods | Can be overloaded | **Cannot be overridden** |
| `private` methods | Can be overloaded | **Cannot be overridden** (not visible to the subclass) |

### The 4 conditions for a method to be overridden

All four must hold, or it is *not* an override (it is a new method, an overload, or a hide):

1. **Same name.**
2. **Same parameter list** (same number, same types, same order). Return type is *not* part of the
   signature for this test.
3. **The parent's method is not `private`** — a private method is not inherited, so there is
   nothing to override.
4. **The parent's method is not `static` and not `final`.**

Plus two more restrictions on the override itself:
- Access modifier must be **same or wider** (`protected` → `public` is legal; `public` →
  `protected` is a compile error).
- It may throw the same checked exceptions or a **subset** of them.

### Overload resolution — the 3-phase algorithm (Java 8)

The compiler tries these phases **in order** and stops at the first phase that yields an applicable
method.

| Phase | Allows | Example |
|---|---|---|
| **1. Strict invocation** | Widening primitive conversion, widening reference conversion. **No boxing, no varargs** | `f(int)` wins for `f(5)` |
| **2. Loose invocation** | Boxing / unboxing on top of phase 1 | `f(Integer)` wins for `f(Integer.valueOf(5))` |
| **3. Varargs** | Variable arity as the last resort | `f(int...)` wins for `f(1,2)` |

Within a phase, the **most specific** applicable method wins (the one needing the fewest
conversions).

### Worked code — overload resolution, fully determined

```java
class Calc {
    void add(int a)               { System.out.println("int"); }
    void add(long a)              { System.out.println("long"); }
    void add(Integer a)           { System.out.println("Integer"); }
    void add(Object a)            { System.out.println("Object"); }
    void add(int... a)            { System.out.println("varargs"); }
}

public class Main {
    public static void main(String[] args) {
        Calc c = new Calc();
        c.add(5);                    // ?
        c.add(5L);                   // ?
        c.add(Integer.valueOf(5));   // ?
        c.add("x");                  // ?
        c.add(1, 2);                 // ?
    }
}
```

**This prints exactly:**

```
int
long
Integer
Object
varargs
```

Why, line by line:

| Call | Phase hit | Method chosen | Reason |
|---|---|---|---|
| `add(5)` | 1 (strict) | `add(int)` | Exact match, `int` literal needs no conversion |
| `add(5L)` | 1 (strict) | `add(long)` | `long` literal, exact match |
| `add(Integer)` | 2 (loose) | `add(Integer)` | Phase 1 forbids unboxing; phase 2 allows it, and `Integer` is the most specific |
| `add("x")` | 1 (strict) | `add(Object)` | Widening reference conversion `String` → `Object`; no other candidate applies in phase 1 or 2 |
| `add(1, 2)` | 3 (varargs) | `add(int...)` | Arity 2 matches only the varargs method |

### Overriding — the runtime dispatch rule

```java
class Parent {
    static void show()  { System.out.println("Parent.show"); }
    void display()      { System.out.println("Parent.display"); }
}

class Child extends Parent {
    static void show()  { System.out.println("Child.show"); }
    @Override void display() { System.out.println("Child.display"); }
}

public class Main {
    public static void main(String[] args) {
        Parent p = new Child();
        p.show();      // ?
        p.display();   // ?
    }
}
```

**This prints exactly:**

```
Parent.show
Child.display
```

| Call | Binding | Why |
|---|---|---|
| `p.show()` | **Compile time**, on `Parent` | `show` is `static`. Static methods are resolved by the compiler using the **static type** of the reference (`Parent`), then *hidden* by `Child.show`. |
| `p.display()` | **Run time**, on the object | `display` is an instance method and is overridden. The JVM looks at the **runtime class** of the object (`Child`) and calls `Child.display`. |

This one pair of lines is the most-asked output-prediction question in the Java section. Learn it
until it is automatic.

### Covariant return types

An override may return a **narrower** type (a subtype) than the parent's:

```java
class A { Object get() { return null; } }
class B extends A { @Override String get() { return "b"; } }   // legal: String is a subtype of Object
```

| Return relationship | Legal? |
|---|---|
| Same type | ✅ |
| Narrower (covariant) — `String` overriding `Object` | ✅ |
| Wider (`Object` overriding `String`) | ❌ compile error |
| Unrelated types (`Integer` overriding `String`) | ❌ compile error |

Covariant returns matter because they let a subclass narrow the contract without breaking LSP.

### Method hiding vs overriding — the one-line distinction

| | Overriding | Hiding |
|---|---|---|
| Applies to | **Instance** methods | **Static** methods |
| Resolved by | The **runtime class** of the object | The **compile-time type** of the reference |
| Extra restriction | Return type must be same or covariant | Return type must be **identical** |

## Quick rules

- Overloading: **same class, same name, different parameters**. Overriding: **parent + child,
  same signature**.
- Overloading is resolved by the **compiler**; overriding by the **JVM**.
- A method is overridden only if the parent's is **visible (not private), not static, not final**.
- An override may **widen** access but never narrow it.
- An override may throw **fewer or equal checked exceptions**, never new ones.
- Covariant return = **narrower** return type is allowed in an override.
- `static` + `final` + `private` methods are **not overridable** — they are the classic trap.
- In overload resolution: **strict → loose → varargs**, most specific first.
- `Parent p = new Child(); p.instanceMethod()` runs the **child**; `p.staticMethod()` runs the
  **parent**.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "Same method name = overriding" | Overriding when it is overloading | Check the parameter list and the class boundary |
| "Different return type = overriding" | ❌ A method differing only in return type is a **compile error**, not an override | Return type alone never distinguishes overloads |
| "Static methods are overridden" | Overriding | Static methods are **hidden**, resolved at compile time |
| "Final methods can be overridden" | Overriding | `final` blocks overriding, not overloading |
| "Private methods are inherited" | Overriding a private method | A private method is not inherited at all |
| "Overload resolution picks the biggest type" | `add(Object)` for `add(5)` | Phase 1 strictness: exact/widening match wins first |
| "Overriding is decided by the variable's type" | `Parent.display` for `p.display()` | Overriding uses the **runtime class** |
| Forgetting access-modifier rule | Accepting a narrowed override | Parent `public` → child `protected` is a compile error |

## Checklist

- [ ] I can state the 4 override conditions without looking.
- [ ] I can state the 2 override restrictions (access widening only, no new checked exceptions).
- [ ] I know the 3-phase overload resolution order: strict → loose → varargs.
- [ ] I can predict the output of the `Calc` example above from memory.
- [ ] I can predict the output of the `Parent p = new Child()` example from memory.
- [ ] I know that a `static` method is hidden, not overridden, and that a hidden static method must
      have an identical return type.

## Related

- [The four pillars](01-the-four-pillars.md)
- [`this`, `super` and the modifier matrix](03-this-super-and-modifiers.md)
- [Method resolution order](../03-inheritance-polymorphism/02-techniques/01-method-resolution-order.md)
- [8 solved OOP questions](../03-worked-examples/01-solved-oop-questions.md)
- [OOP principles traps](../04-pitfalls/01-oop-principles-traps.md)
- [OOP principles one-pager](../05-reference/01-oop-principles-one-pager.md)
- [Topic overview](../README.md)
