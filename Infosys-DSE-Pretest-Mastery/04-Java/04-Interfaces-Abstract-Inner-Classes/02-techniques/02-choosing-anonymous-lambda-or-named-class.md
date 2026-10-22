# Anonymous Class, Lambda, or Named Class — Choosing the Right Form

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 7 min_
> **Prerequisite:** [Lambdas and functional interfaces](../01-concepts/02-lambdas-and-functional-interfaces.md)

## In one sentence

Use a **lambda** for a single-method contract with no state, an **anonymous class** when you need
several methods or extra fields, and a **named class** when the type is reused or needs a name.

## Why the pre-test tests this

- "Which of the following CAN be replaced by a lambda expression?" is a standard 1-mark question.
- "Which of the following is a valid way to create an instance of an interface?" has three plausible
  options and one exact.
- Candidates lose marks by assuming a lambda is always "the modern way", even when the interface has
  two abstract methods.

## Core concept

### The capability matrix — the whole decision in one table

| Capability | **Named class** | **Anonymous class** | **Lambda** |
|---|---|---|---|
| Implements **2 or more** abstract methods | ✅ | ✅ | ❌ |
| **Extends** a class | ✅ | ✅ | ❌ |
| Declares **fields** | ✅ | ✅ | ❌ |
| Instance initialiser blocks | ✅ | ✅ | ❌ |
| Declares a **constructor** | ✅ | ❌ | ❌ |
| Holds **mutable state** | ✅ | ✅ | ❌ (captures only effectively final locals) |
| Overrides `equals` / `hashCode` | ✅ | ✅ | ❌ |
| Has a **name** you can refer to | ✅ | ❌ | ❌ |
| Can be `instanceof`-tested against its own type | ✅ | ✅ | ❌ |
| Can be `Serializable` | ✅ | ✅ | ❌ (lambdas are not serializable) |
| Its own class file | ✅ | ✅ (named `Outer$1.class`) | ✅ (synthetic) |
| Available | Java 1.0 | Java 1.0 | **Java 8+** |

### The decision procedure

```
1. Does the target type have EXACTLY ONE abstract method?
   ├── NO  → named class or anonymous class. Go to 3.
   └── YES → do you need state, fields, a constructor, or more than one method?
             ├── NO  → LAMBDA.  (or a method reference)
             └── YES → ANONYMOUS CLASS. Go to 3.

2. (only if 1 was YES) — none of that, but you need a reusable, named type?
   → NAMED CLASS.

3. Do you need to EXTEND a class, or implement 2+ interfaces?
   → ANONYMOUS CLASS.

4. Do you need the object to be reusable, stored in a field, or passed around by name?
   → NAMED CLASS (top-level or nested).
```

### Worked example — the same interface, three forms

```java
interface Greeter {
    String greet(String name);
    default String prefix() { return "Hello"; }
}

class FormalGreeter implements Greeter {
    @Override public String greet(String name) { return "Good day, " + name; }
}

public class Main {
    public static void main(String[] args) {
        Greeter formal = new FormalGreeter();
        Greeter anon = new Greeter() {
            @Override public String greet(String name) { return "Hi " + name; }
        };
        Greeter lambda = name -> "Yo " + name;

        System.out.println(formal.greet("Ananya"));
        System.out.println(anon.greet("Rahul"));
        System.out.println(lambda.greet("Meera"));
    }
}
```

**This prints exactly:**

```
Good day, Ananya
Hi Rahul
Yo Meera
```

All three produce the same **type** (`Greeter`). The difference is what they can *do*, not what
they are.

### Why `FormalGreeter` cannot be a lambda

`Greeter` has **two** methods — `greet` (abstract) and `prefix` (default). It is still a
functional interface, because only **one** method is abstract. So a lambda **is** legal here — but
the lambda can only implement the abstract method, and `prefix()` comes from the interface's
default.

Now add a second abstract method:

```java
interface Greeter2 {
    String greet(String name);
    String farewell(String name);
}

Greeter2 g = (name) -> "Hi " + name;   // ← COMPILE ERROR
```

```
error: incompatible types: bad type in lambda expression
       bad return type in lambda expression
       missing target type for the abstract method farewell(String)
```

The rule is **one abstract method**, not "one method".

### The state test — the reason a lambda cannot win

```java
interface Counter { int next(); }

public class Main {
    public static void main(String[] args) {
        int[] count = {0};
        Counter c = () -> ++count[0];
        System.out.println(c.next());
        System.out.println(c.next());
    }
}
```

**This prints exactly:**

```
1
2
```

A lambda **can** mutate state if that state lives in an **array** or another object captured by
reference. What it cannot do is **declare** its own mutable fields. That is the precise limit:

| Lambda can | Lambda cannot |
|---|---|
| Read effectively final locals | Declare its own field |
| Mutate an object it captured (array, `List`) | Reassign a captured local |
| Call methods on captured objects | Have a constructor |
| Use `this` from the enclosing scope | Have its own `this` |

### Where the named class wins

| Need | Named class |
|---|---|
| Reuse the same implementation in several places | ✅ |
| Store it in a field and pass it around by name | ✅ |
| Implement `Serializable`, `Comparable`, `Comparator` in one place | ✅ |
| Override `equals`/`hashCode` correctly | ✅ |
| Give it a meaningful `toString()` | ✅ |
| Extend an abstract class with state | ✅ |

## Quick rules

- Lambda ⇔ exactly **one abstract method** and **no** declared state.
- Anonymous class ⇔ several methods, fields, a constructor is not allowed, state is allowed.
- Named class ⇔ reuse, naming, or serialization.
- A lambda can **mutate captured objects**; it just cannot **declare** mutable fields.
- A lambda is **not** `Serializable` and has **no** `toString()` of its own.
- All three forms have the same **static type**; only the capabilities differ.
- A **method reference** is another lambda form — use it when the body is a single call.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "A lambda works for any interface" | Yes | Only **functional** interfaces |
| "A lambda can have fields" | Yes | It cannot declare any |
| "An anonymous class can have a constructor" | Yes | It cannot |
| "A lambda has its own `this`" | Yes | `this` is the **enclosing** instance |
| "Lambdas are serializable" | Yes | They are not |
| "The interface's `default` methods count toward the lambda limit" | Yes | Only **abstract** methods count |
| "A method reference is a different feature from a lambda" | Yes | It is lambda shorthand |
| "An anonymous class is always replaceable by a lambda" | Yes | Only if the interface is functional |

## Checklist

- [ ] I can apply the decision procedure to any interface in the options.
- [ ] I know that `default` methods do **not** block a lambda.
- [ ] I know exactly what a lambda may and may not mutate.
- [ ] I know an anonymous class cannot declare a constructor.
- [ ] I can write a lambda for `Runnable` and `Comparator` from memory.
- [ ] I know lambdas are not serializable.

## Related

- [Interface anatomy](../01-concepts/01-interface-anatomy.md)
- [Lambdas and functional interfaces](../01-concepts/02-lambdas-and-functional-interfaces.md)
- [Nested and inner classes](../01-concepts/03-nested-and-inner-classes.md)
- [Default method conflict resolution](01-default-method-conflict-resolution.md)
- [8 solved interfaces and inner-class questions](../03-worked-examples/01-solved-interfaces-inner-questions.md)
- [Interfaces and inner-class traps](../04-pitfalls/01-interfaces-inner-traps.md)
- [Interfaces and inner-class one-pager](../05-reference/01-interfaces-inner-one-pager.md)
- [Topic overview](../README.md)
