# Default Method Conflict Resolution — The 3 Rules in Order

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 7 min_
> **Prerequisite:** [Interface anatomy](../01-concepts/01-interface-anatomy.md)

## In one sentence

When two `default` methods collide, **a class beats an interface**, a **more specific interface
beats a less specific one**, and if neither rule settles it you **must override and disambiguate**.

## Why the pre-test tests this

- "Which method is called when a class implements two interfaces with the same `default` method?"
  is a classic 2-mark output-prediction question.
- The diamond problem is the classic interview framing of the same rule.
- The `Interface.super.method()` syntax appears in the options and most candidates have never
  seen it.

## Core concept

### The 3 rules, in the order you apply them

| # | Rule | Statement |
|---|---|---|
| 1 | **Class wins** | A concrete method from the class or its superclass beats any interface `default` |
| 2 | **More specific interface wins** | If one interface extends another, the **sub**-interface's `default` wins |
| 3 | **You must override** | Two unrelated interfaces, no class method → the class **must** override and call `I.super.m()` explicitly |

### Rule 1 — class wins

```java
interface Greet { default void hi() { System.out.println("interface"); } }

class Base {
    public void hi() { System.out.println("class"); }
}

class Impl extends Base implements Greet { }

public class Main {
    public static void main(String[] args) { new Impl().hi(); }
}
```

**Prints exactly:** `class`

The superclass's concrete method wins over the interface `default`. Note this also holds when the
class itself supplies the method:

```java
class Impl2 implements Greet {
    @Override public void hi() { System.out.println("own"); }
}
// new Impl2().hi();  →  own
```

### Rule 2 — the more specific interface wins

```java
interface Parent { default void show() { System.out.println("Parent"); } }

interface Child extends Parent {
    @Override default void show() { System.out.println("Child"); }
}

class Impl implements Child { }

public class Main {
    public static void main(String[] args) { new Impl().show(); }
}
```

**Prints exactly:** `Child`

`Child` is a sub-interface of `Parent`, so its `default` is the more specific one.

### Rule 3 — you must override

```java
interface X { default void run() { System.out.println("X"); } }
interface Y { default void run() { System.out.println("Y"); } }

class Z implements X, Y {
    @Override
    public void run() {
        X.super.run();
        Y.super.run();
    }
}

public class Main {
    public static void main(String[] args) { new Z().run(); }
}
```

**Prints exactly:**

```
X
Y
```

Without the override, `class Z` **does not compile**:

```
error: class Z inherits unrelated defaults for run() from types X and Y
```

**The `I.super.m()` syntax:** valid **only** inside a class that **directly implements** `I`, and
only for a `default` method. `Z` directly implements both `X` and `Y`, so `X.super.run()` and
`Y.super.run()` are both legal. `SomeOther.super.run()` would not be.

### The decision procedure

```
1. Does the class (or a superclass) supply a concrete method with that signature?
   → YES: that method runs. DONE.
2. Does exactly one interface in the hierarchy supply a default, and is it the
   most specific (sub-interface of any other supplier)?
   → YES: that default runs. DONE.
3. Do two UNRELATED interfaces supply a default?
   → The class must override and call I.super.m() explicitly.
   → Without the override: COMPILE ERROR.
```

### The diamond in full

```java
interface Top {
    default void hi() { System.out.println("Top"); }
}
interface Left extends Top { }
interface Right extends Top { }
class Diamond implements Left, Right { }

public class Main {
    public static void main(String[] args) { new Diamond().hi(); }
}
```

**Prints exactly:** `Top`

`Left` and `Right` both inherit the *same* `Top` default — there is no conflict, because they do
not declare competing defaults.

### Two hard limits on `default` methods

| Rule | Consequence |
|---|---|
| A `default` method may **not** override a method of `java.lang.Object` | `default String toString() { ... }` inside an interface is a **compile-time error** |
| A `default` method may **not** override a `static` method from a superclass | Compile-time error: `s() in Base cannot implement s() in I` — `overriding method is static` |
| A `default` method sitting next to a **`final`** superclass method | **Legal** — the final class method wins, and the default is simply never inherited |

Verified against `javac --release 8`:

```
error: default method toString in interface I overrides a member of java.lang.Object
```

So `equals`, `hashCode` and `toString` must be implemented as **class** methods, never as
interface defaults.

## Worked example — a full exam-style trace

```java
interface A { default void run() { System.out.println("A"); } }
interface B { default void run() { System.out.println("B"); } }

class Parent {
    public void run() { System.out.println("Parent"); }
}

class Kid extends Parent implements A, B { }

public class Main {
    public static void main(String[] args) { new Kid().run(); }
}
```

**This prints exactly:** `Parent`

| Step | Result |
|---|---|
| Rule 1 — does the class chain supply a concrete `run()`? | ✅ `Parent.run()` → **rule 1 settles it** |
| Rules 2 and 3 | Not reached |

Now remove `Parent`:

```java
class Kid implements A, B { }   // ← compile error
```

**Compile error:** `inherits unrelated defaults for run() from types A and B`.

The correct fix:

```java
class Kid implements A, B {
    @Override public void run() { A.super.run(); B.super.run(); }
}
// prints: A then B
```

## Quick rules

- **Class wins** over interface, always checked first.
- **Sub-interface wins** over super-interface.
- **Unrelated interfaces → you must override**; `I.super.m()` disambiguates.
- `I.super.m()` works only in a class that **directly implements** `I`.
- Two interfaces that inherit the **same** default cause **no** conflict.
- An interface `default` may **not** override an `Object` method.
- An interface `default` may **not** override an `Object` method or a `static` superclass method.
- A `default` method **cannot** be `static`, `final` or `private` (in Java 8).

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "The most derived interface always wins" | Always | Only if it is a **sub**-interface of the other |
| "The compiler picks one automatically" | Yes | Two unrelated defaults = **compile error** |
| "`X.super.m()` can be called anywhere" | Yes | Only in a class that **directly implements** `X` |
| "A class cannot have a method with the same name as a default" | True | It can — the class method simply wins |
| "The diamond always needs an override" | Yes | Not when both branches inherit the **same** default |
| "`default String toString()` is legal" | Yes | It overrides an `Object` method → compile error |
| "A `default` method can be `final`" | Yes | It cannot be `final`, `static` or `private` in Java 8 |

## Checklist

- [ ] I can recite the 3 rules in order.
- [ ] I know the exact compile error for two unrelated defaults.
- [ ] I can write `I.super.m()` and state when it is legal.
- [ ] I know the diamond with a shared ancestor needs no override.
- [ ] I know a `default` cannot override an `Object` method.
- [ ] I can say whether a class method beats an interface default.

## Related

- [Interface anatomy](../01-concepts/01-interface-anatomy.md)
- [Nested and inner classes](../01-concepts/03-nested-and-inner-classes.md)
- [Anonymous class, lambda, or named class?](02-choosing-anonymous-lambda-or-named-class.md)
- [8 solved interfaces and inner-class questions](../03-worked-examples/01-solved-interfaces-inner-questions.md)
- [Interfaces and inner-class traps](../04-pitfalls/01-interfaces-inner-traps.md)
- [Interfaces and inner-class one-pager](../05-reference/01-interfaces-inner-one-pager.md)
- [Topic overview](../README.md)
