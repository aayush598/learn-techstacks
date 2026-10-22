# Interface Anatomy — What an Interface Can and Cannot Contain

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 9 min_
> **Prerequisite:** [OOP Principles](../01-OOP-Principles/README.md)

## In one sentence

An interface is a **contract**: every member is `public`, every field is implicitly
`public static final`, and since Java 8 it may also carry `default` and `static` **method
bodies**.

## Why the pre-test tests this

- "Which of the following is TRUE about interfaces?" is a 1-mark question with exactly one
  correct answer, and the distractors are all plausible.
- "Can an interface have a default method?" / "Can an interface have a static method?" /
  "Can an interface have a constructor?" — three versions of the same question.
- The `default` method conflict rules decide several "predict the output" questions.

## Core concept

### The interface rules by Java version

| Member kind | Java 8 | Java 9+ | Notes |
|---|---|---|---|
| Abstract methods | ✅ `public abstract` implicitly | ✅ | No body |
| `default` methods | ✅ **new in Java 8** — with a body | ✅ | Inherited by implementing classes |
| `static` methods | ✅ **new in Java 8** — with a body | ✅ | **Not** inherited by implementing classes |
| `private` methods | ❌ **not available in Java 8** | ✅ **new in Java 9** | Helper methods for `default` methods; not inherited |
| `public static final` fields | ✅ | ✅ | The only kind of field allowed |
| Non-final instance fields | ❌ | ❌ | Would need per-implementation state |
| Constructors | ❌ | ❌ | An interface is not instantiable, so it has none |
| Instance initialiser blocks | ❌ | ❌ | Same reason |
| Nested classes | ✅ | ✅ | Allowed — a nested class in an interface is implicitly `public static` |

**The pre-test runs on Java 8.** So treat private interface methods as **unavailable**, and treat
`default` and `static` interface methods as **available**.

### The implicit modifiers — the single most-tested fact

| Declaration in an interface | What the compiler makes it |
|---|---|
| `int count = 0;` | `public static final int count = 0;` |
| `void run();` | `public abstract void run();` |
| `default void run() { }` | `public default void run() { }` |
| `static void create() { }` | `public static void create() { }` |

There is **no way** to write a non-`public` abstract method or a non-`final` field in an
interface. Attempting `private int x;` is a compile error ("illegal combination of modifiers:
private and static").

### Interface vs abstract class — the full comparison

| Dimension | **Interface** | **Abstract class** |
|---|---|---|
| Keyword | `interface` | `abstract class` |
| What it is | A contract of behaviours | A partially implemented class |
| Multiple inheritance of type | ✅ implements many interfaces | ❌ extends one class |
| Constructors | ❌ none | ✅ yes |
| Instance fields | ❌ only `public static final` | ✅ any |
| Method bodies | `default` and `static` (Java 8+) | any mix of abstract and concrete |
| `super` keyword | ❌ no parent class | ✅ available |
| `this` in field initialisers | ❌ fields are static | ✅ available |
| State | ❌ stateless | ✅ shared state is the point |
| Constructor chaining | ❌ impossible | ✅ `super(...)` |
| Best for | Capability across unrelated hierarchies | Shared code + shared state |

### Marker interfaces

A **marker interface** has **no methods at all**. It exists purely to tag a type so that other
code can recognise it with `instanceof`.

| Marker interface | What it marks | Who checks it |
|---|---|---|
| `java.io.Serializable` | "This object can be serialized" | `ObjectOutputStream` |
| `java.lang.Cloneable` | "This object may be `clone()`d" | `Object.clone()` |
| `java.lang.Runnable` | "This object has a `run()` to execute" | `Thread`, executors |
| `java.util.RandomAccess` | "This `List` supports fast random access" | `Collections` algorithms |

**Exam question:** *"Which of the following is a marker interface?"* → `Serializable` (the others
on the list have methods).

### Functional interfaces — the one-abstract-method rule

A **functional interface** has **exactly one** abstract method. Everything else in it must be
`default`, `static` or (Java 9+) `private`.

| Interface | Single abstract method | Lambda example |
|---|---|---|
| `java.lang.Runnable` | `void run()` | `() -> System.out.println("go")` |
| `java.util.function.Supplier<T>` | `T get()` | `() -> "value"` |
| `java.util.function.Consumer<T>` | `void accept(T t)` | `t -> System.out.println(t)` |
| `java.util.function.Function<T, R>` | `R apply(T t)` | `s -> s.length()` |
| `java.util.function.Predicate<T>` | `boolean test(T t)` | `s -> s.isEmpty()` |
| `java.util.Comparator<T>` | `int compare(T a, T b)` | `(a, b) -> a.size() - b.size()` |
| `java.lang.Iterable<T>` | `Iterator<T> iterator()` | — |

The `@FunctionalInterface` annotation is **optional**, but adding it makes the compiler enforce
the rule — useful when you are writing your own.

### Sealed interfaces (Java 17 — mention, not test)

```java
public sealed interface Shape permits Circle, Square { }

final class Circle implements Shape { }
final class Square implements Shape { }
```

A **sealed** type restricts who may extend or implement it. It gives you exhaustive `switch`
pattern matching and says "this hierarchy is closed". It is **Java 17**, so the Java 8 pre-test
will not test it beyond recognising the word.

### Worked code — what an interface can hold

```java
interface Shape {
    double area();                                   // public abstract
    default String describe() { return "area " + area(); }   // public default
    static Shape unit() { return null; }             // public static — NOT inherited
    int SIDES = 0;                                   // public static final
}

class Circle implements Shape {
    private final double r;
    Circle(double r) { this.r = r; }
    @Override public double area() { return Math.PI * r * r; }
}

public class Main {
    public static void main(String[] args) {
        Circle c = new Circle(2);
        System.out.println(c.describe());
        System.out.println(Shape.SIDES);
        System.out.println(Shape.unit());
    }
}
```

**This prints exactly:**

```
area 12.566370614359172
0
null
```

| Line | Why |
|---|---|
| `c.describe()` | `Circle` inherits the `default` method from `Shape`; `area()` dispatches to `Circle.area()` |
| `Shape.SIDES` | The implicit `public static final` field, accessed via the interface name |
| `Shape.unit()` | A `static` interface method — it is **not** inherited, so it must be called via `Shape.` |

## Quick rules

- Every interface field is `public static final`. There is no exception.
- Every interface method is `public` — abstract, `default`, `static`, or (Java 9+) `private`.
- An interface has **no constructors** and **no instance fields**.
- Java 8 added `default` and `static` interface methods. Java 9 added `private` ones.
- `static` interface methods are **not inherited** by implementing classes.
- A **marker interface** has **no methods** — `Serializable` is the classic example.
- A **functional interface** has exactly **one** abstract method — `Runnable`, `Comparator`.
- An interface may be extended by another interface, but **never by a class**.
- `sealed` is Java 17 — know the word, do not expect a question on it.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "All interface methods are abstract" | True (Java 8 has `default` and `static`) | Java 8 changed this |
| "An interface can have instance variables" | True | Only `public static final` |
| "An interface can have constructors" | True | It has none |
| "Interface methods can be `private`" | True (Java 8) | Private interface methods are **Java 9** |
| "A class can implement only one interface" | True | Any number |
| "A static interface method is inherited by implementors" | True | It is **not** |
| "`Serializable` is a functional interface" | Yes | It has **zero** methods — it is a marker |
| "An interface can extend a class" | Yes | Interfaces extend **interfaces** only |

## Checklist

- [ ] I can list the implicit modifiers for every interface member kind.
- [ ] I know the Java version each interface feature arrived in (8 → default/static, 9 → private,
      17 → sealed).
- [ ] I know the four members an interface may **not** contain.
- [ ] I can name three marker interfaces and three functional interfaces.
- [ ] I know that static interface methods are not inherited.
- [ ] I can state the abstract-class-vs-interface rule in one line.

## Related

- [Lambdas and functional interfaces](02-lambdas-and-functional-interfaces.md)
- [Nested and inner classes](03-nested-and-inner-classes.md)
- [Default method conflict resolution](../02-techniques/01-default-method-conflict-resolution.md)
- [Abstract class vs interface](../01-OOP-Principles/02-techniques/02-abstract-class-vs-interface.md)
- [8 solved interfaces and inner-class questions](../03-worked-examples/01-solved-interfaces-inner-questions.md)
- [Interfaces and inner-class traps](../04-pitfalls/01-interfaces-inner-traps.md)
- [Interfaces and inner-class one-pager](../05-reference/01-interfaces-inner-one-pager.md)
- [Topic overview](../README.md)
