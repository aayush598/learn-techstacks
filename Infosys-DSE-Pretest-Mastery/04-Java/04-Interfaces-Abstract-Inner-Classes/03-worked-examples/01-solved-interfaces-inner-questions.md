# 8 Solved Questions — Interfaces, Abstract & Inner Classes

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 16 min_
> **Prerequisite:** [Default method conflict resolution](../02-techniques/01-default-method-conflict-resolution.md)

## In one sentence

Answer each question on paper first with a 90-second cap, then read the **distractor table** — the
wrong option you picked is the only thing worth studying.

## Why the pre-test tests this

- Interface-member questions are a reliable 1–2 marks each, and there are usually 3–4 of them.
- The output-prediction questions here hinge on one of four decisions: implicit modifiers, the
  conflict rules, lambda eligibility, or the inner-class attachment.

## Core concept

Before you start, fix these in your head:

- Interface fields are `public static final` — there are **no** instance fields in an interface.
- Interface methods are `public` — `default`, `static` (Java 8), `private` (Java 9).
- A functional interface has exactly **one abstract** method; `default` methods do not count.
- A class method beats an interface `default` (conflict rule 1).
- Two unrelated interface defaults = **compile error** — you must override.
- An inner class carries an outer instance: `outer.new Inner()`, `Outer.this`.

## Question 1 — Which statement about an interface is TRUE?

```java
interface Shape {
    double area();
    default String label() { return "shape"; }
    static int SIDES = 0;
    int DIMENSIONS = 2;
}
```

**A.** `area()` is `private` by default, so only classes in the same package can call it.
**B.** `label()` is inherited by every class that implements `Shape`.
**C.** `SIDES` and `DIMENSIONS` are instance fields, so each implementing object has its own copy.
**D.** `Shape` can be instantiated directly with `new Shape()`.

### Solution

| Step | Fact |
|---|---|
| 1 | Every interface method is implicitly `public`. `private` is not allowed → **A is wrong** |
| 2 | A `default` method has a body and is inherited by implementing classes unless overridden → **B holds** |
| 3 | Interface fields are implicitly `public static final`, so they are **shared**, not per-object → **C is wrong** |
| 4 | An interface has no constructor and cannot be instantiated → **D is wrong** |

### Answer: **B**

### Why the distractors fail

| Option | The belief behind it | The fact |
|---|---|---|
| A | "Abstract means hidden" | Abstract means **no body**, not hidden. Interface methods are `public` |
| C | "Fields are per-object" | They are `static` — one copy shared by all implementors |
| D | "It looks like a class" | Interfaces have **no constructor**, so `new Shape()` cannot compile |

## Question 2 — What does this print?

```java
interface Printer { default void print() { System.out.println("interface"); } }

class Base {
    public void print() { System.out.println("base"); }
}

class Doc extends Base implements Printer { }

public class Main {
    public static void main(String[] args) { new Doc().print(); }
}
```

**A.** `interface`
**B.** `base`
**C.** `base` then `interface`
**D.** The program does not compile

### Solution

| Step | Check |
|---|---|
| 1 | Does the **class chain** supply a concrete `print()`? `Base.print()` — ✅ **yes** |
| 2 | Rule 1 fires: **a class method beats an interface `default`**. Stop here |
| 3 | `Printer.print()` is not inherited by `Doc` at all — it is shadowed, so it never runs |

### Answer: **B** — the output is exactly

```
base
```

### Why the distractors fail

| Option | The belief behind it | The fact |
|---|---|---|
| A | "The interface default is the implementation" | `Base` has a concrete `print()`, and the class wins |
| C | "Both run" | A `default` is either inherited or shadowed — never both |
| D | "Two methods with the same name conflict" | They do not have the same **signature path**; the class method simply wins |

## Question 3 — What does this print?

```java
interface A { default void run() { System.out.println("A"); } }
interface B { default void run() { System.out.println("B"); } }

class C implements A, B {
    @Override public void run() { A.super.run(); B.super.run(); }
}

public class Main {
    public static void main(String[] args) { new C().run(); }
}
```

**A.** `A`
**B.** `B`
**C.** `A` then `B`
**D.** The program does not compile

### Solution

| Step | Check |
|---|---|
| 1 | `A` and `B` are **unrelated** interfaces, so rule 2 cannot apply |
| 2 | The class `C` **does** provide `run()`, so rule 3 is satisfied — the conflict is resolved by hand |
| 3 | Inside `C.run()`, `A.super.run()` calls `A`'s default, then `B.super.run()` calls `B`'s |
| 4 | Order is the order of the statements in the method body |

### Answer: **C** — the output is exactly

```
A
B
```

### Why the distractors fail

| Option | The belief behind it | The fact |
|---|---|---|
| A | "The first interface wins" | There is **no** first-interface rule. `A.super.run()` and `B.super.run()` are **both** called |
| B | "The last interface wins" | Same — both run, in statement order |
| D | "`A.super` is invalid syntax" | `A.super.run()` is legal because `C` **directly implements** `A` |

> **Follow-up the exam loves:** if you delete the `run()` override from `C`, the program stops
> compiling with `error: class C inherits unrelated defaults for run() from types A and B`.

## Question 4 — Which of these interfaces can be the target of a lambda expression?

```java
interface P { void run(); }
interface Q { void run(); void stop(); }
interface R { default void run() { } }
```

**A.** `P` only
**B.** `P` and `Q`
**C.** `P` and `R`
**D.** `P`, `Q` and `R`

### Solution

| Step | Check |
|---|---|
| 1 | A lambda target must be a **functional interface** — **exactly one abstract method** |
| 2 | `P` has one abstract method → ✅ |
| 3 | `Q` has two abstract methods → ❌ |
| 4 | `R` has **zero** abstract methods — `run()` is a `default`. Zero is not exactly one → ❌ |

### Answer: **A**

### Why the distractors fail

| Option | The belief behind it | The fact |
|---|---|---|
| B | "`Q` has one method to implement" | `Q` has **two abstract** methods. A lambda implements exactly one |
| C | "`R` has only one method, so it qualifies" | A lambda counts **abstract** methods only. `R` has **none** |
| D | "Count all methods" | Count **abstract** methods only |

> **Verified error message** for `R`: `error: incompatible types: R is not a functional interface —
> no abstract method found in interface R`.

## Question 5 — What does this print?

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<String> names = new ArrayList<>(Arrays.asList("Karthik", "Ananya", "Rahul"));
        names.sort(Comparator.comparingInt(String::length));
        System.out.println(names);
    }
}
```

**A.** `[Karthik, Ananya, Rahul]`
**B.** `[Rahul, Ananya, Karthik]`
**C.** `[Ananya, Karthik, Rahul]`
**D.** The program does not compile

### Solution

| Step | Check |
|---|---|
| 1 | `Comparator.comparingInt(...)` takes a key extractor that returns an `int` |
| 2 | `String::length` is a **method reference** to the instance method `length()` of the argument — it is shorthand for `s -> s.length()` |
| 3 | The comparator sorts **ascending by length** |
| 4 | Lengths: `Karthik` = 7, `Ananya` = 6, `Rahul` = 5 |

### Answer: **B** — the output is exactly

```
[Rahul, Ananya, Karthik]
```

### Why the distractors fail

| Option | The belief behind it | The fact |
|---|---|---|
| A | "The list was already sorted" | It was in the order `Karthik, Ananya, Rahul` — descending length |
| C | "Alphabetical" | `Ananya`(6) before `Karthik`(7) is right, but `Rahul`(5) is shortest, so it comes first |
| D | "`String::length` needs a receiver" | `Type::instanceMethod` uses the **first argument** as the receiver |

## Question 6 — What does this print?

```java
class Outer {
    int x = 10;
    class Inner {
        int x = 20;
        void show() {
            System.out.println(x);
            System.out.println(Outer.this.x);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Outer o = new Outer();
        Outer.Inner i = o.new Inner();
        i.show();
    }
}
```

**A.** `10` then `20`
**B.** `20` then `20`
**C.** `20` then `10`
**D.** The program does not compile

### Solution

| Step | Check |
|---|---|
| 1 | Inside `Inner.show()`, the bare name `x` resolves to the **innermost** scope — `Inner.x` |
| 2 | `Outer.this.x` explicitly names the enclosing instance's field |
| 3 | `o.new Inner()` is the required syntax: the compiler needs to know **which** outer instance to bind |
| 4 | `Inner` is a non-static nested class, so it has an implicit `Outer` reference |

### Answer: **C** — the output is exactly

```
20
10
```

### Why the distractors fail

| Option | The belief behind it | The fact |
|---|---|---|
| A | "The outer field wins" | The **inner** scope wins for a simple name; the outer one needs `Outer.this` |
| B | "Both names point at the inner field" | `Outer.this.x` is explicitly the **outer** field |
| D | "`o.new Inner()` is invalid" | It is the **correct** syntax for an inner class |

## Question 7 — Which statement is TRUE?

**A.** An inner class can declare a `static` method.
**B.** A static nested class can be instantiated without creating an instance of the outer class.
**C.** To create an inner class instance you must first make the outer class `static`.
**D.** An anonymous class can be declared `static` inside a method.

### Solution

| Step | Check |
|---|---|
| 1 | **Java 8**: an inner (non-static nested) class may **not** declare static members → **A is wrong** |
| 2 | A static nested class holds **no** outer instance, so `new Outer.Nested()` needs no outer object → **B holds** |
| 3 | The outer class's own modifier is irrelevant to creating an inner instance → **C is wrong** |
| 4 | **Java 8**: an anonymous class may not be `static` → **D is wrong** |

### Answer: **B**

### Why the distractors fail

| Option | The belief behind it | The fact |
|---|---|---|
| A | "Static is allowed inside any nested class" | **Java 8** forbids it: `error: Illegal static declaration in inner class`. From **Java 16** it is allowed |
| C | "Inner classes need a static outer" | The outer class is usually a normal instance class — `outer.new Inner()` proves it |
| D | "Anonymous classes are just nested classes" | An anonymous class is created at an instantiation point and, in **Java 8**, cannot be `static` |

## Question 8 — What does this print?

```java
class Outer {
    void run() {
        int base = 5;

        class Local {
            int calc() { return base * 2; }
        }

        Runnable r = new Runnable() {
            @Override public void run() {
                System.out.println("anon " + new Local().calc());
            }
        };

        r.run();
    }
}

public class Main {
    public static void main(String[] args) { new Outer().run(); }
}
```

**A.** `anon 10`
**B.** `anon 5`
**C.** `anon 5` then `anon 5`
**D.** The program does not compile

### Solution

| Step | Check |
|---|---|
| 1 | `base` is a local of `run()` that is **never reassigned** → it is effectively final, so `Local` may capture it |
| 2 | `Local.calc()` returns `base * 2` = `5 * 2` = `10` |
| 3 | The anonymous `Runnable` captures the local variable `r`'s scope, so `new Local()` is visible inside it — a **local class** is in scope for the whole remaining block |
| 4 | `r.run()` prints `"anon "` followed by `10` |

### Answer: **A** — the output is exactly

```
anon 10
```

### Why the distractors fail

| Option | The belief behind it | The fact |
|---|---|---|
| B | "The anonymous class cannot see `Local`" | A local class is visible to everything in the same block, including an anonymous class declared there |
| C | "Both `run()` and the local initialiser print" | `run()` is called **once** |
| D | "A local class needs a `final` keyword" | Since **Java 8**, **effectively final** is enough — no `final` keyword required |

> **The variant the exam also asks:** if `base` were reassigned after the class declaration
> (`base = 6;`), the program would **not compile** — `error: local variables referenced from an
> inner class must be final or effectively final`.

## Quick rules

- Interface fields are `public static final`; interface methods are `public`.
- `default` and `static` interface methods are **Java 8**; `private` ones are **Java 9**.
- The conflict order: **class → sub-interface → must override**.
- A lambda target needs **exactly one abstract method**.
- Inner class → `outer.new Inner()`; static nested → `new Outer.Nested()`.
- The **inner** field shadows the outer one; `Outer.this.field` reaches the outer.

## Common traps

| Trap | Fix |
|---|---|
| "The interface default wins over the class method" | The class wins |
| "Two unrelated defaults → pick one" | Compile error; you must override |
| "`default` methods block a lambda" | Only **abstract** methods count |

## Checklist

- [ ] I answered all 8 under 90 seconds each, and can justify each in one sentence.
- [ ] I have read the distractor table for **every** question I got wrong.
- [ ] I can recite the 3 conflict rules in order.
- [ ] I can write `outer.new Inner()` and `new Outer.Nested()` without hesitating.
- [ ] I know the exact error message for unrelated defaults.

## Related

- [Interface anatomy](../01-concepts/01-interface-anatomy.md)
- [Lambdas and functional interfaces](../01-concepts/02-lambdas-and-functional-interfaces.md)
- [Nested and inner classes](../01-concepts/03-nested-and-inner-classes.md)
- [Default method conflict resolution](../02-techniques/01-default-method-conflict-resolution.md)
- [Anonymous class, lambda, or named class?](../02-techniques/02-choosing-anonymous-lambda-or-named-class.md)
- [Interfaces and inner-class traps](../04-pitfalls/01-interfaces-inner-traps.md)
- [Interfaces and inner-class one-pager](../05-reference/01-interfaces-inner-one-pager.md)
- [Topic overview](../README.md)
