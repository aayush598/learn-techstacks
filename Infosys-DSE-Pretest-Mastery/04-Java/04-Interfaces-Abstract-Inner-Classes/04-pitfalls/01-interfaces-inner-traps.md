# Interfaces and Inner Classes — The Traps

> Section 4 · Java · Interfaces, Abstract & Inner Classes · _Estimated reading time: 8 min_
> **Prerequisite:** [Interface anatomy](../01-concepts/01-interface-anatomy.md)

## In one sentence

Every trap here comes from carrying a **Java 1.4 belief** into a **Java 8** question.

## Why the pre-test tests this

- The distractors in an interface question are almost always one of these beliefs.
- Traps 1, 5 and 6 exist **only** because Java 8 changed the rules — the pre-test knows this.
- Traps 9, 10 and 12 catch nearly every candidate on inner-class questions.

## Core concept

### Trap 1 — "All interface methods are abstract"

**The wrong belief:** an interface can only declare method signatures.

**The truth since Java 8:** an interface may have `default` and `static` methods with a body.
Only `private` interface methods need Java 9.

```java
interface I {
    void run();                          // abstract
    default void stop() { }              // Java 8 — with a body
    static void create() { }             // Java 8 — with a body
}
```

**Exam form:** *"Which of the following can an interface contain in Java 8?"* → a `default` method.

### Trap 2 — "Interface methods are package-private"

**The wrong belief:** an interface method has default (package) access, like a class method.

**The truth:** every interface method is implicitly **`public`**. An interface exists to be used
from other packages, so its contract must be visible everywhere.

**Proof:** a package-private method could not be implemented by a class in another package.

### Trap 3 — "An interface can have instance variables"

**The wrong belief:** interfaces are "half-built classes", so they can have fields.

**The truth:** every interface field is implicitly **`public static final`** — a constant shared by
all implementors. You cannot write `private int x;` in an interface (illegal combination of
modifiers: `private` and `static`).

**Why the design forces it:** an interface has no instance state to attach a field to.

### Trap 4 — "An interface can have constructors"

**The wrong belief:** interfaces are classes, so they can be initialised.

**The truth:** an interface has **no constructors** and **no instance initialiser blocks** — it
cannot be instantiated, so there is nothing to initialise. The compiler forbids both.

### Trap 5 — "Private interface methods are available in Java 8"

**The wrong belief:** `private` works inside an interface, like it does in a class.

**The truth:** private interface methods arrived in **Java 9**. Under Java 8:

```
error: private interface methods are not supported in -source 8
```

**Why the exam cares:** Java 8 is the pre-test's baseline, so "an interface can have a private
method" is **false** there. Java 9 added them so `default` methods could share a helper.

### Trap 6 — "A class can implement only one interface"

**The wrong belief:** Java has single inheritance, so one "parent" only.

**The truth:** a class extends **one** superclass but implements **any number** of interfaces. The
restriction is on **class** inheritance only.

```java
class Impl implements A, B, C { }   // fine
```

### Trap 7 — "A static interface method is inherited by implementing classes"

**The wrong belief:** everything in an interface is inherited.

**The truth:** a `static` interface method is **not** inherited. It must be called through the
interface name: `I.create()`. Calling `impl.create()` is a **compile error**.

```java
interface S { static void make() { } }
class Impl implements S { }
new Impl().make();   // error: cannot find symbol: method make()
S.make();            // correct
```

### Trap 8 — "The interface default wins over the class method"

**The wrong belief:** the interface is "more specific" than the class.

**The truth:** the **class wins**. A concrete method in the class (or its superclass) beats any
interface `default`.

```java
interface P { default void print() { System.out.println("interface"); } }
class Base { public void print() { System.out.println("base"); } }
class Doc extends Base implements P { }
new Doc().print();   // → base
```

**Corollary trap:** two **unrelated** interfaces with the same `default` is a **compile error**
(`inherits unrelated defaults for run() from types A and B`) — the compiler does **not** pick one.

### Trap 9 — "An inner class can have static members"

**The wrong belief:** static members are allowed in any nested class.

**The truth:** under **Java 8**, an inner (non-static nested) class **cannot** declare static
members:

```
error: Illegal static declaration in inner class O.In
```

Only **constant variables** (`static final` with a compile-time constant initialiser) are allowed.
From **Java 16**, inner, local and anonymous classes may declare static members.

### Trap 10 — "The outer field shadows the inner field"

**The wrong belief:** the outer scope wins for a shared name.

**The truth:** the **innermost** scope wins. The outer field needs `Outer.this.field`.

```java
class Outer {
    int x = 10;
    class Inner {
        int x = 20;
        void show() { System.out.println(x); }            // 20
        void showOuter() { System.out.println(Outer.this.x); }  // 10
    }
}
```

### Trap 11 — "A lambda can implement any interface"

**The wrong belief:** a lambda is just a short class body, so it works everywhere.

**The truth:** a lambda target must be a **functional interface** — **exactly one abstract
method**. Two abstract methods, or zero, both fail:

```
error: incompatible types: R is not a functional interface
no abstract method found in interface R
```

Note that `default` methods do **not** count toward the limit.

### Trap 12 — "You can write `new Inner()` on its own"

**The wrong belief:** an inner class is created like any other object.

**The truth:** an inner class needs its outer instance, so the syntax is `outer.new Inner()`. A
**static nested** class is created with `new Outer.Nested()`.

**Why it matters on the exam:** the two syntaxes tell you whether the class has an outer instance —
which decides whether it can reach the outer's fields.

## Worked example — one program, four traps

```java
interface Speaker {
    default void speak() { System.out.println("speak"); }
    static int COUNT = 0;
}
class Radio implements Speaker {
    private String name = "Radio";
    class Tuner {
        void show() {
            System.out.println(name);   // the inner reaches the outer's private field
            System.out.println(COUNT);  // interface fields are static — one shared copy
            speak();                     // the default method is inherited
        }
    }
}
public class Main {
    public static void main(String[] args) {
        Radio r = new Radio();
        r.new Tuner().show();
    }
}
```

**This prints exactly:**

```
Radio
0
speak
```

| Line | Why |
|---|---|
| `System.out.println(name)` | `Tuner` is an inner class of `Radio`, so it holds an implicit `Radio` reference and can read its **`private`** field |
| `System.out.println(COUNT)` | `COUNT` is implicitly `public static final` — a **single shared** value, not a per-object copy. Nothing increments it, so it is `0` |
| `speak()` | `Radio` inherits `Speaker`'s **`default`** method, so it is callable with no qualifier |

## Quick rules

- Interface members: `public` methods, `public static final` fields, **no constructors**.
- `default` and `static` methods → **Java 8**. `private` methods → **Java 9**.
- A class may implement **many** interfaces; it may extend only **one** class.
- `static` interface methods are **not inherited** — call them via the interface name.
- The **class** beats the interface `default`; unrelated defaults are a **compile error**.
- An inner class may **not** declare static members under Java 8, and the **inner** field shadows
  the outer one — use `Outer.this.field`.
- A lambda needs a target with **exactly one abstract method**.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| All interface methods are abstract | "Yes" | `default` and `static` exist (Java 8) |
| Interfaces can have instance fields | "Yes" | Only `public static final` |
| Static interface methods are inherited | "Yes" | They are **not** |
| The interface default beats the class method | "interface" | The **class** wins |
| Unrelated defaults → pick one | "A" | **Compile error** |
| Inner classes can have static members | "Yes" | Not in Java 8 |
| The outer field shadows the inner | "10" | The **inner** wins |

## Checklist

- [ ] I can list the implicit modifiers of every interface member.
- [ ] I know which Java version added `default`, `static` and `private` interface methods.
- [ ] I know an interface has no constructor and no instance fields.
- [ ] I can state the conflict rules in order.
- [ ] I know the two creation syntaxes, the shadowing rule and the `Outer.this` escape.
- [ ] I know what counts toward the "one abstract method" limit.

## Related

- [Interface anatomy](../01-concepts/01-interface-anatomy.md)
- [Lambdas and functional interfaces](../01-concepts/02-lambdas-and-functional-interfaces.md)
- [Nested and inner classes](../01-concepts/03-nested-and-inner-classes.md)
- [Default method conflict resolution](../02-techniques/01-default-method-conflict-resolution.md)
- [8 solved interfaces and inner-class questions](../03-worked-examples/01-solved-interfaces-inner-questions.md)
- [Interfaces and inner-class one-pager](../05-reference/01-interfaces-inner-one-pager.md)
- [Topic overview](../README.md)
