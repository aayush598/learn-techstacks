# Nested and Inner Classes

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 9 min_
> **Prerequisite:** [Interface anatomy](01-interface-anatomy.md)

## In one sentence

A **nested** class lives inside another class; a **static** nested class has no link to an outer
instance, while a **non-static inner** class carries one automatically and reaches it with
`Outer.this`.

## Why the pre-test tests this

- "Which of the following is TRUE about inner classes?" appears regularly.
- "What does this program print?" is a favourite for inner-class questions, because the answers
  hinge on **which outer instance** is attached.
- The shadowing rule — inner field wins, `Outer.this.field` reaches the outer — is a 2-mark
  question that most candidates get wrong.

## Core concept

### The four kinds

| Kind | Where it is declared | Has an outer instance? | Can be `static` (Java 8)? | How you create it |
|---|---|---|---|---|
| **Static nested class** | Inside a class, with `static` | ❌ no | ✅ yes | `new Outer.Nested()` |
| **Inner class** (non-static nested) | Inside a class, no `static` | ✅ yes, implicit | ❌ **no** | `outer.new Inner()` |
| **Local class** | Inside a **method or block body** | ✅ yes, if declared in an instance context | ❌ **no** | `new Local()` inside that scope |
| **Anonymous class** | At the point of instantiation | ✅ yes, if in an instance context | ❌ **no** | `new Iface() { ... }` |

**Java 8 rules above.** From **Java 16**, inner, local and anonymous classes may declare static
members. The pre-test runs Java 8, so "an inner class cannot have static members" is **correct**.

### Static nested class

```java
class Outer {
    static class Nested {
        void show() { System.out.println("Nested.show"); }
    }
}

public class Main {
    public static void main(String[] args) {
        Outer.Nested n = new Outer.Nested();
        n.show();
    }
}
```

**Prints exactly:** `Nested.show`

- It has **no** `this` for an outer instance, so it cannot touch the outer's instance fields.
- It **can** declare static members.
- You can also write `new Outer.Nested()` from anywhere the type is visible — no outer object is
  needed.

### Inner class

```java
class Outer {
    private int value = 42;

    class Inner {
        void show() {
            System.out.println(value);            // 42 — reached through the implicit outer instance
            System.out.println(Outer.this.value);  // 42 — explicit form
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Outer o = new Outer();
        Outer.Inner i = o.new Inner();             // ← note: outer.new Inner()
        i.show();
    }
}
```

**Prints exactly:**

```
42
42
```

- `o.new Inner()` is the required syntax — you cannot write `new Inner()` on its own, because the
  compiler needs to know **which** outer instance to bind.
- Inside an inner class, the outer's instance members are reachable **without a prefix**.
- `Outer.this` names the enclosing instance explicitly.

### Local class

```java
class Outer {
    int base = 7;

    void method() {
        int bonus = 3;                 // effectively final — never reassigned
        class Local {
            int total() { return base + bonus; }
        }
        System.out.println(new Local().total());
    }
}

public class Main {
    public static void main(String[] args) { new Outer().method(); }
}
```

**Prints exactly:** `10`

- A local class can read the enclosing method's **effectively final** locals. Reassign `bonus` and
  it stops compiling.
- A local class **must be declared before it is used** in the block.
- A local class may declare `static final` constants (compile-time constants) in Java 8.

### Anonymous class

```java
interface Greeter {
    String greet(String name);
}

public class Main {
    public static void main(String[] args) {
        Greeter g = new Greeter() {
            @Override
            public String greet(String name) {
                return "Hello " + name;
            }
        };
        System.out.println(g.greet("Ananya"));
    }
}
```

**Prints exactly:** `Hello Ananya`

- It has **no name** and no constructor of its own — the compiler supplies one.
- It can implement **multiple** abstract methods, which is why it cannot always become a lambda.
- It can also **extend an abstract class** or implement several interfaces at once.
- It can declare **fields and instance initialisers**, which a lambda cannot.

### Shadowing — the field-name collision

```java
class Outer {
    int x = 10;

    class Inner {
        int x = 20;

        void print() {
            System.out.println(x);            // 20 — the inner field wins
            System.out.println(this.x);       // 20 — same thing
            System.out.println(Outer.this.x); // 10 — the outer field
        }
    }
}

public class Main {
    public static void main(String[] args) {
        new Outer().new Inner().print();
    }
}
```

**Prints exactly:**

```
20
20
10
```

**The rule:** the **innermost** scope wins for a simple name. `Outer.this.x` is the escape hatch to
the outer field. The same applies to **method** names — an inner method hides an outer method with
the same signature unless the outer one is `super`-style reachable.

### Access from outside — the visibility rules

| Outer member | Inner class can reach it? | Same-package class outside the outer can reach it? |
|---|---|---|
| `private` | ✅ yes | ❌ no — only via the outer's own code |
| `protected` | ✅ yes | ✅ if the outside class is a subclass or in the same package |
| package-private | ✅ yes | ✅ yes |
| `public` | ✅ yes | ✅ yes |

An inner class can read the outer's **`private`** fields. That is the single biggest practical
difference between a nested class and a separate top-level class.

## Quick rules

- **Static nested** = no outer instance, may have static members, `new Outer.Nested()`.
- **Inner** (non-static) = has an outer instance, may **not** have static members (Java 8),
  `outer.new Inner()`.
- A local class may use the enclosing method's **effectively final** locals; it must be declared
  before use.
- An anonymous class can implement **many** methods; a lambda can implement **one**.
- Inner fields **shadow** outer fields; use `Outer.this.field` to reach the outer one.
- An inner class can access the outer's `private` members.
- Java 16 relaxed the static-member rule for inner/local/anonymous classes — Java 8 did not.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "Inner classes can have static methods" | Yes | **No** in Java 8 |
| "You can write `new Inner()` directly" | Yes | You need `outer.new Inner()` |
| "A static nested class needs an outer instance" | Yes | It does **not** |
| "The outer field wins when both have the same name" | Yes | The **inner** one wins |
| "Anonymous classes are always lambdas" | Yes | An anonymous class may implement several methods |
| "A local class can use any local variable" | Yes | Only **effectively final** ones |
| "Anonymous classes can declare constructors" | Yes | They cannot |
| "An inner class cannot access the outer's private fields" | True | It **can** |

## Checklist

- [ ] I can state which of the four kinds may hold static members under Java 8.
- [ ] I know the two creation syntaxes: `new Outer.Nested()` and `outer.new Inner()`.
- [ ] I can explain shadowing and write `Outer.this.x`.
- [ ] I know that a local class needs effectively final locals.
- [ ] I know that an anonymous class can implement several methods.
- [ ] I know an inner class can read the outer's private fields.

## Related

- [Interface anatomy](01-interface-anatomy.md)
- [Lambdas and functional interfaces](02-lambdas-and-functional-interfaces.md)
- [Anonymous class, lambda, or named class?](../02-techniques/02-choosing-anonymous-lambda-or-named-class.md)
- [8 solved interfaces and inner-class questions](../03-worked-examples/01-solved-interfaces-inner-questions.md)
- [Interfaces and inner-class traps](../04-pitfalls/01-interfaces-inner-traps.md)
- [Interfaces and inner-class one-pager](../05-reference/01-interfaces-inner-one-pager.md)
- [Topic overview](../README.md)
