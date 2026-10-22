# Lambdas and Functional Interfaces

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 8 min_
> **Prerequisite:** [Interface anatomy](01-interface-anatomy.md)

## In one sentence

A **lambda expression** is a compact implementation of the **single abstract method** of a
functional interface, and the interface's method signature supplies the lambda's parameter types.

## Why the pre-test tests this

- "Which of the following can be replaced by a lambda expression?" is a standard 1-mark question
  with exactly one correct option.
- "What is the output of this lambda?" appears in the output-prediction archetype.
- Method references (`String::length`) look exotic but are a one-line answer: *"a shorthand for a
  lambda that calls that method."*

## Core concept

### Lambda syntax

```java
// Single parameter, expression body
name -> name.length()

// Parentheses optional for a single parameter
(String name) -> name.length()

// Multiple parameters
(a, b) -> a + b

// Block body — needs an explicit return
(a, b) -> {
    int sum = a + b;
    return sum;
}
```

| Rule | Detail |
|---|---|
| Parameter types | Usually **omitted** — they come from the target type |
| Return value | The expression's value is returned implicitly; a block body needs `return` |
| `new` keyword | Not used with a lambda |
| Target type | Must be a **functional interface** — a lambda has no type of its own |
| Scope | The lambda body can use the enclosing method's **effectively final** locals and `this` |
| No `this` inside | A lambda has no `this` of its own; `this` refers to the enclosing instance |

### Target typing — how the compiler knows the parameter types

A lambda is **not** a value on its own. It is a value **for a target type**. The compiler uses the
context to work out the parameter types and the return type.

```java
interface Calc { int apply(int a, int b); }

Calc add = (a, b) -> a + b;              // a and b are ints
Calc mul = (a, b) -> a * b;              // same shape, different body
```

If the target type has **two or more** abstract methods, the lambda **does not compile** —
"target type must be a functional interface".

### Method references

A **method reference** is a shorthand for a lambda that immediately calls an existing method.

| Form | Means | Example |
|---|---|---|
| `Type::staticMethod` | A static method of `Type` | `Integer::parseInt` |
| `Type::instanceMethod` | An instance method of the **first argument** | `String::length` |
| `instance::instanceMethod` | An instance method of a **bound** object | `System.out::println` |
| `Type::new` | A constructor of `Type` | `ArrayList::new` |

```java
import java.util.function.Function;
import java.util.function.Supplier;

Function<String, Integer> len = String::length;   // equivalent to s -> s.length()
Supplier<ArrayList<String>> list = ArrayList::new; // equivalent to () -> new ArrayList<>()
```

**The exam framing:** *"A method reference is shorthand for what?"* → **a lambda expression that
calls that method**.

### The common functional interfaces and their lambdas

| Interface | Method | Lambda |
|---|---|---|
| `Runnable` | `void run()` | `() -> { ... }` |
| `Callable<T>` | `T call() throws Exception` | `() -> value` |
| `Comparator<T>` | `int compare(T a, T b)` | `(a, b) -> a.compareTo(b)` |
| `Function<T, R>` | `R apply(T t)` | `t -> transform(t)` |
| `BiFunction<T, U, R>` | `R apply(T t, U u)` | `(t, u) -> combine(t, u)` |
| `Supplier<T>` | `T get()` | `() -> produce()` |
| `Consumer<T>` | `void accept(T t)` | `t -> consume(t)` |
| `Predicate<T>` | `boolean test(T t)` | `t -> check(t)` |

### Worked code — lambda, method reference and `Comparator`

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

public class Main {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>();
        names.add("Rahul");
        names.add("Ananya");
        names.add("Karthik");

        Collections.sort(names, (a, b) -> a.length() - b.length());
        System.out.println(names);

        Function<String, Integer> f = String::length;
        System.out.println(f.apply("Meera"));
    }
}
```

**This prints exactly:**

```
[Rahul, Ananya, Karthik]
5
```

| Line | Why |
|---|---|
| `Collections.sort(...)` | The lambda is the `Comparator` — `a.length() - b.length()` sorts by name length: `Rahul` (5), `Ananya` (6), `Karthik` (7) |
| `f.apply("Meera")` | `String::length` is a method reference to the instance method `length()` of the argument → `5` |

Note the lambda is **target-typed** by `Comparator<String>` — `a` and `b` are `String`s because of
the parameter type, not because you wrote it.

### Anonymous class vs lambda

| | **Anonymous class** | **Lambda** |
|---|---|---|
| Forms | `new Iface() { ... }` | `(a, b) -> ...` |
| Needs a functional interface? | ❌ no — can implement **many** methods | ✅ yes — exactly **one** abstract method |
| Can extend a class? | ✅ yes | ❌ no — only interfaces |
| Can hold state? | ✅ yes — it can declare fields | ❌ no — it can only capture effectively final locals |
| Its own type | Yes — it is an anonymous `class` | No — it is the functional interface type |
| `this` inside | Refers to the anonymous instance | Refers to the **enclosing** instance |
| Java version | All versions | Java 8+ |
| Can override `Object` methods? | ✅ yes (`equals`, `hashCode`) | ❌ no — only the interface's abstract method |

**The exam question:** *"Which of the following CAN be replaced by a lambda expression?"* → the
one whose interface has exactly **one** abstract method. An anonymous class implementing an
interface with two abstract methods **cannot** be replaced.

### Where lambdas beat anonymous classes — the practical rule

| Situation | Use |
|---|---|
| One method, no state, short body | **Lambda** |
| Multiple methods to implement | **Anonymous class** |
| Need to extend a class | **Anonymous class** |
| Need instance state or instance initialisers | **Anonymous class** |
| Need to override `equals`/`hashCode` on the object | **Anonymous class** |
| Passed to a library API (`Comparator`, `Runnable`) | **Lambda** |

## Quick rules

- A lambda needs a **functional interface** target — exactly **one** abstract method.
- Parameter types come from the **target type**; you usually omit them.
- Lambda bodies capture only **effectively final** locals.
- `this` inside a lambda means the **enclosing** instance.
- Method references: `Type::static`, `Type::instance` (first arg), `instance::instance` (bound),
  `Type::new` (constructor).
- A lambda **cannot** implement an interface with two abstract methods, and **cannot** extend a
  class.
- An anonymous class **can** do both.
- `Runnable` and `Comparator` are the two functional interfaces the pre-test names most.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "Any interface can be implemented with a lambda" | Yes | Only **functional** interfaces |
| "A lambda needs its parameter types written out" | Yes | They are inferred from the target type |
| "A lambda can extend a class" | Yes | Lambdas implement **interfaces** only |
| "A lambda can hold mutable state" | Yes | It can only capture effectively final locals |
| "`this` inside a lambda is the lambda's own object" | Yes | It is the **enclosing** instance |
| "A method reference is a new kind of lambda" | A separate feature | It is **shorthand for a lambda** |
| "An anonymous class can be replaced by a lambda always" | Yes | Only if the interface is functional |

## Checklist

- [ ] I can write a lambda for `Runnable`, `Comparator` and `Function` without checking.
- [ ] I know the four method-reference forms and one example of each.
- [ ] I know that lambda parameter types come from the target type.
- [ ] I can name the four things a lambda cannot do.
- [ ] I can explain why an anonymous class may need to stay an anonymous class.
- [ ] I know that a lambda body can only use effectively final locals.

## Related

- [Interface anatomy](01-interface-anatomy.md)
- [Nested and inner classes](03-nested-and-inner-classes.md)
- [Anonymous class, lambda, or named class?](../02-techniques/02-choosing-anonymous-lambda-or-named-class.md)
- [8 solved interfaces and inner-class questions](../03-worked-examples/01-solved-interfaces-inner-questions.md)
- [Interfaces and inner-class traps](../04-pitfalls/01-interfaces-inner-traps.md)
- [Interfaces and inner-class one-pager](../05-reference/01-interfaces-inner-one-pager.md)
- [Topic overview](../README.md)
