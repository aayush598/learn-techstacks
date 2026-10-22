# Abstract, Final, and the Constructor Chain

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 8 min_
> **Prerequisite:** [Inheritance basics and dynamic dispatch](01-inheritance-basics-and-dispatch.md)

## In one sentence

`abstract` forces a subclass to provide behaviour, `final` forbids changing it, and the two are
**mutually exclusive** on a method.

## Why the pre-test tests this

- "Which of the following is TRUE about abstract classes?" is a 1-mark question with one
  surprisingly non-obvious trap: an abstract class is **not required** to have an abstract method.
- "Which modifier combination is a compile error?" is decided in one table row.
- The abstract-class-vs-interface comparison is the most-repeated design question in the Java
  pre-test.

## Core concept

### Abstract classes

| Rule | Statement |
|---|---|
| Instantiation | ❌ **cannot** be instantiated with `new` |
| Abstract methods | May declare abstract methods with **no body** |
| Concrete methods | May also have fully implemented methods |
| Constructors | ✅ **may** have constructors — they run when a subclass is instantiated |
| Fields | ✅ any — instance, static, final |
| Static methods | ✅ yes |
| `final` methods | ✅ yes (a final concrete method in an abstract class is fine) |
| `private` methods | ✅ yes (not inherited, so nothing to implement) |
| Modifiers on the class | `public`, `protected`, package-private, `final`? — **no**: `abstract` and `final` cannot be combined on a class |
| Must have an abstract method? | ❌ **NO** — an abstract class with zero abstract methods is perfectly legal |
| Subclass rule | Every **concrete** subclass must implement every inherited abstract method, or declare itself abstract |

```java
abstract class Shape {
    Shape(String name) { this.name = name; }     // a constructor is fine
    String name;
    double area() { return 0; }                 // a concrete method is fine
    abstract double perimeter();                 // an abstract method is fine
}
```

`Shape` is abstract. It has a constructor, a concrete method and an abstract method, and it still
cannot be instantiated.

### Abstract methods

| Rule | Statement |
|---|---|
| Body | **None** — `abstract void f();` |
| Visibility | `public`, `protected`, or package-private. **Never `private`** — a private method is not inherited, so it could never be implemented |
| `static` | ❌ illegal — a static method is not overridden, so it could never be "implemented" |
| `final` | ❌ illegal — the whole point is that it *must* be implemented |
| `synchronized` | ❌ illegal |
| `native` | ❌ illegal with `abstract` |
| Return type | Any, including `void` |
| Where allowed | Abstract classes and interfaces only |

### `final`

| Target | Meaning | Exam phrasing |
|---|---|---|
| `final` class | Cannot be **extended** | "Which class cannot be inherited?" |
| `final` instance method | Cannot be **overridden** | "Which method cannot be overridden?" |
| `final` static method | Cannot be overridden **or hidden** | — |
| `final` field | Assigned **exactly once** | "Which field can be assigned only once?" |
| `final` parameter | Assigned exactly once inside the method | — |
| `final` local variable | Assigned exactly once before use | — |

**`final` and `abstract` are opposites.** A member is either:

| | `abstract` | `final` |
|---|---|---|
| Body | None | Has one |
| Must be changed by subclasses? | **Yes** — must be overridden | **No** — must not be overridden |

So `abstract final` is a contradiction, and the compiler rejects it.

### The illegal modifier combinations — the complete list

| Declaration | Verdict |
|---|---|
| `abstract final void f();` | ❌ illegal combination |
| `abstract static void f();` | ❌ illegal combination |
| `abstract private void f();` | ❌ illegal combination |
| `abstract synchronized void f();` | ❌ illegal combination |
| `abstract native void f();` | ❌ illegal combination |
| `abstract int x;` (a field) | ❌ illegal combination |
| `final abstract class A { }` | ❌ illegal combination |
| `abstract void f();` in an abstract class | ✅ legal |
| `static void f() { }` in an abstract class | ✅ legal |
| `private void f() { }` in an abstract class | ✅ legal |
| `final void f() { }` in an abstract class | ✅ legal |
| `abstract class A { }` with no abstract methods | ✅ legal |

### The constructor chain in a hierarchy

```java
class A {
    A() { System.out.println("A"); }
}
class B extends A {
    B() { super(); System.out.println("B"); }
}
class C extends B {
    C() { super(); System.out.println("C"); }
}
new C();
```

**Output:**

```
A
B
C
```

| Rule | Detail |
|---|---|
| Direction | **Top-down**: `A()` runs first, `C()` last |
| The implicit call | `super()` is inserted as the first statement unless you write `super(...)` or `this(...)` explicitly |
| Field initialisers | Each class's instance field initialisers run **after** its superclass constructor and **before** its own constructor body |
| Access needed | The parent's constructor must be `protected` or `public` for a subclass in another package. `private` is **not** accessible |
| `super(...)` placement | Must be the **first** statement |
| Constructors are not inherited | A subclass never "inherits" a parent constructor; it always calls one |

### Abstract class vs interface — the comparison table

| Dimension | **Abstract class** | **Interface** |
|---|---|---|
| Keyword | `abstract class` | `interface` |
| Extends / implements | Extends **one** class | Implements **any number** of interfaces |
| Constructors | ✅ yes | ❌ none |
| Instance fields | ✅ yes | ❌ only `public static final` |
| Method bodies | Mix of abstract and concrete | Java 8+: `default` and `static` methods have bodies |
| State | ✅ shared state is the point | ❌ stateless contract |
| `super` | ✅ available | ❌ no parent class |
| Constructor chaining | ✅ `super(...)` chain | ❌ impossible |
| Multiple inheritance of behaviour | ❌ only one class | ✅ many interfaces — this is the workaround for single inheritance |
| Best for | Shared code + shared state in a hierarchy | Capability contracts across unrelated hierarchies |

**The "multiple inheritance of type" fact:** a Java class cannot inherit from two classes, but it
can implement two interfaces that declare the same method — and then it must implement that
method **once** (unless a `default` exists). This is the practical reason interfaces exist.

### Worked code — an abstract class and an interface together

```java
interface Shape {
    double area();
    default String describe() { return "shape with area " + area(); }
}

abstract class Polygon implements Shape {
    protected final List<String> vertices = new ArrayList<>();

    Polygon() { }

    abstract int sides();

    @Override
    public String toString() { return describe() + " and " + sides() + " sides"; }
}
```

| Fact demonstrated | Where |
|---|---|
| An abstract class **can** implement an interface | `Polygon implements Shape` |
| An abstract class **can** have a constructor | `Polygon()` |
| An abstract class **can** have a concrete method | `toString()` |
| An interface `default` method **can** call an abstract method | `describe()` calls `area()` |
| An abstract class **can** have state | `vertices` |

## Quick rules

- Abstract class → **cannot be instantiated**. Abstract method → **no body**.
- An abstract class **may have zero** abstract methods. This is the classic trap.
- An abstract method may not be `private`, `static`, `final`, `synchronized` or `native`.
- `abstract` + `final` = compile error. `abstract` + `static` = compile error.
- `final` class → cannot be extended. `final` method → cannot be overridden. `final` field →
  assigned once.
- The constructor chain runs **top-down**, `Object()` first.
- Abstract class → **constructor** ✅, state ✅, concrete methods ✅, instantiation ❌.
- Interface → constructor ❌, instance state ❌, multiple implementation ✅.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| An abstract class must have an abstract method | True | It may have **none** |
| An abstract class cannot have a constructor | True | It can — and it runs for subclasses |
| `abstract static` is fine | Legal | Illegal combination |
| `abstract private` is fine | Legal | A private method is not inherited |
| `final` blocks overloading | "Cannot overload" | `final` blocks **overriding** only |
| The subclass constructor runs first | Wrong output order | The **superclass** constructor runs first |
| An interface can hold instance state | Yes | Only `public static final` fields |
| A class can extend two classes | Yes | Single class inheritance only |

## Checklist

- [ ] I can state the 5 illegal modifier combinations without looking.
- [ ] I know that an abstract class may have zero abstract methods.
- [ ] I can list what an abstract class may and may not have.
- [ ] I know the constructor chain runs top-down and starts at `Object()`.
- [ ] I can write the abstract class vs interface table from memory.
- [ ] I know `private` parent constructors are not accessible to subclasses.

## Related

- [Inheritance basics and dynamic dispatch](01-inheritance-basics-and-dispatch.md)
- [Casts, type checks and ClassCastException](02-casts-type-checks-and-errors.md)
- [The method resolution procedure](../02-techniques/01-method-resolution-order.md)
- [8 solved inheritance questions](../03-worked-examples/01-solved-inheritance-questions.md)
- [Inheritance traps](../04-pitfalls/01-inheritance-traps.md)
- [Inheritance one-pager](../05-reference/01-inheritance-one-pager.md)
- [Topic overview](../README.md)
