# Classes, Objects & Constructors — 8 Solved Questions

> Section 4 · Java · Classes, Objects & Constructors · _Estimated reading time: 14 min_
> **Prerequisite:** [Constructor rules and compile errors](../02-techniques/01-constructor-rules-and-compile-errors.md)

## In one sentence

Most constructor questions reduce to **three facts**: the default-constructor rule, the creation
order, and the `this()` / `super()` first-statement rule.

## Why the pre-test tests this

- These questions cluster in the "compile or not" and "predict the output" archetypes — the two
  archetypes that carry the most weight in the 25-question Java section.
- Cap each question at 90 seconds. Flag and move if you exceed it.

## Core concept

- **Q1:** a default constructor exists **only** if the class declares none.
- **Q2, Q8:** creation order = static (superclass first) → superclass instance state → subclass
  instance state → subclass constructor body.
- **Q3:** `this(...)` / `super(...)` must be the **first** statement.
- **Q4, Q5:** `clone()` is a **shallow** copy needing `Cloneable`; default `equals` compares
  **identity**.
- **Q5:** overriding `equals` requires overriding `hashCode`; equal objects ⇒ equal hash codes.
- **Q6:** `finalize()` is **deprecated**; `transient` fields are skipped by serialization.
- **Q7:** a **holder-idiom** singleton is thread-safe with no `synchronized`.
## Worked example

### Q1 — Answer **C** (the default constructor rule)

```java
class Employee {
    Employee(String name) { }
}
```

**What happens when you write `new Employee();`?**

A. It compiles and creates an object with a `null` name.
B. It compiles and calls `Employee(String)` with a `null` argument.
C. It is a compile error — no constructor matching `Employee()` exists.
D. It compiles because the JVM generates a default constructor.

**Solution**

The compiler generates a default constructor **only when the class declares no constructor at
all**. `Employee` declares one, so no default constructor is generated, and there is no
no-argument constructor to call.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | There is no no-arg constructor to call, so there is no object to have a `null` name |
| B | Java does **not** auto-pass `null` to a single-argument constructor |
| D | The default constructor is generated only if **no** constructor is declared |

### Q2 — Answer **A** (the creation order)

**What does the following program print?**

```java
class A {
    static { System.out.println("A static"); }
    { System.out.println("A instance"); }
    A() { System.out.println("A ctor"); }
}

class B extends A {
    static { System.out.println("B static"); }
    { System.out.println("B instance"); }
    B() { super(); System.out.println("B ctor"); }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("main");
        new B();
    }
}
```

A. `main`, `A static`, `B static`, `A instance`, `A ctor`, `B instance`, `B ctor`
B. `A static`, `B static`, `main`, `A instance`, `A ctor`, `B instance`, `B ctor`
C. `main`, `A static`, `B static`, `A instance`, `B instance`, `A ctor`, `B ctor`
D. `main`, `B static`, `A static`, `A instance`, `A ctor`, `B instance`, `B ctor`

**Solution**

| Step | Printed | Why |
|---|---|---|
| 1 | `main` | `A` and `B` are not initialised yet |
| 2 | `A static` | Initialising `B` initialises its superclass `A` **first** |
| 3 | `B static` | Then `B`'s own static initialiser |
| 4 | `A instance`, `A ctor` | Object phase: `A`'s instance initialisers, then `A()`'s body |
| 5 | `B instance`, `B ctor` | Then `B`'s instance initialisers, then `B()`'s body |

**Answer: A.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Puts the static blocks before `main` — the classes are initialised only when first used, which is at `new B()` |
| C | Interleaves the instance blocks — the superclass's instance state and constructor complete **before** the subclass's instance block runs |
| D | Puts the subclass's static block first — the **superclass** initialises first |

### Q3 — Answer **B** (`super()` must be first)

**Does the following code compile?**

```java
class Parent {
    Parent() { System.out.println("Parent"); }
}

class Child extends Parent {
    Child() {
        System.out.println("start");
        super();
        System.out.println("end");
    }
}
```

A. Yes, it compiles and prints `start`, `Parent`, `end`.
B. No — `super()` must be the first statement in the constructor.
C. No — `Parent()` is `private` and therefore not accessible.
D. Yes, but it prints `Parent`, `start`, `end`.

**Solution**

An explicit `super(...)` call **replaces** the implicit one and **must be the first statement** of
the constructor. `System.out.println("start")` comes first, so the code does not compile.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The code does not compile at all |
| C | `Parent()` is package-private and `Child` is in the same package — it is accessible |
| D | Ignores the compile error; there is no runtime output at all |

**Fix:** move `super();` to the top. The corrected program prints `Parent`, `start`, `end`.

### Q4 — Answer **C** (shallow copy)

**What does the following program print?**

```java
import java.util.ArrayList;
import java.util.List;

class Bag implements Cloneable {
    List<String> items = new ArrayList<>();
    int count = 0;

    @Override
    public Bag clone() {
        try {
            return (Bag) super.clone();
        } catch (CloneNotSupportedException e) {
            return null;
        }
    }
}

public class Main {
    public static void main(String[] args) {
        Bag b1 = new Bag();
        b1.items.add("a");
        b1.count = 1;

        Bag b2 = b1.clone();
        b2.items.add("b");
        b2.count = 2;

        System.out.println(b1.items.size());
        System.out.println(b1.count);
    }
}
```

A. `1` then `2`
B. `2` then `2`
C. `2` then `1`
D. `1` then `1`

**Solution**

`super.clone()` copies the fields **shallowly**: primitives by value, object references by
reference.

| Field | Copied as | Effect |
|---|---|---|
| `count` (int) | value | `b2.count = 2` does **not** change `b1.count` → still `1` |
| `items` (List) | reference | Both copies point at the **same** list, so `b2.items.add("b")` makes `b1.items.size()` = `2` |

**Answer: C.** Output is:

```
2
1
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Assumes a deep copy — the list was shared, not copied |
| B | Assumes the primitive field is also shared — impossible for an `int` |
| D | Assumes neither field was affected |

### Q5 — Answer **D** (the equals/hashCode contract)

**Which of the following statements about `equals` and `hashCode` is TRUE?**

A. Overriding `equals` automatically overrides `hashCode`.
B. If two objects are not equal, their hash codes must be different.
C. Two equal objects may have different hash codes.
D. If two objects are equal, their hash codes must be equal.

**Solution**

| Option | Verdict | Reason |
|---|---|---|
| A | ❌ | They are independent methods. If you override `equals`, you **must** override `hashCode` yourself |
| B | ❌ | The converse is not required — different objects may collide in a hash bucket |
| C | ❌ | This directly violates the contract and breaks `HashSet` / `HashMap` |
| D | ✅ | **Equal objects must have equal hash codes** |

**Answer: D.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The classic misconception — the compiler does not generate a matching `hashCode` |
| B | Collisions are legal and normal |
| C | The exact failure the contract prevents |

### Q6 — Answer **B** (`finalize()` is deprecated)

**Which of the following statements is TRUE about object lifecycle methods in Java?**

A. `finalize()` is guaranteed to be called before an object is garbage collected.
B. `finalize()` has been deprecated since Java 9 and is never guaranteed to run.
C. `transient` fields are serialized with their default values.
D. `static` fields are serialized along with the instance fields of the same class.

**Solution**

| Option | Verdict | Reason |
|---|---|---|
| A | ❌ | The GC gives **no guarantee** that `finalize()` ever runs |
| B | ✅ | Deprecated since Java 9 and marked for removal. Use explicit `close()` (try-with-resources) instead |
| C | ❌ | `transient` fields are **skipped entirely** by serialization |
| D | ❌ | `static` fields belong to the class, not the instance — never serialized |

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The whole reason `finalize()` was deprecated |
| C | `transient` means "do not serialize this field" |
| D | Statics are restored from the class, not from the stream |

### Q7 — Answer **C** (the holder idiom)

**Which singleton implementation is thread-safe **without** using the `synchronized` keyword?**

A. `if (instance == null) { instance = new Singleton(); }` inside `getInstance()`
B. A `public static` field initialised with `new Singleton()`
C. A private static nested `Holder` class whose static final field holds the instance
D. `public static synchronized Singleton getInstance()`

**Solution**

| Option | Verdict | Reason |
|---|---|---|
| A | ❌ | The classic race — two threads can both create an instance |
| B | ❌ | Eager initialisation is thread-safe but not **lazy**; it creates the object whether you need it or not |
| C | ✅ | **Holder idiom.** The JVM guarantees class initialisation happens exactly once and is properly synchronised, so the holder's `static final` field is safely published |
| D | ❌ | Thread-safe, but it **does** use `synchronized` — it fails the question's condition |

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The textbook singleton bug — two instances are possible |
| B | Thread-safe but eager; the marker of the answer is the **nested holder class** |
| D | Uses `synchronized`, so it fails the stated condition |

### Q8 — Answer **A** (constructor chaining order)

**What does the following program print?**

```java
class Parent {
    Parent() { System.out.println("Parent()"); }
}

class Child extends Parent {
    Child() {
        this(5);
        System.out.println("Child()");
    }

    Child(int x) {
        super();
        System.out.println("Child(" + x + ")");
    }
}

public class Main {
    public static void main(String[] args) {
        new Child();
    }
}
```

A. `Parent()`, `Child(5)`, `Child()`
B. `Child(5)`, `Parent()`, `Child()`
C. `Parent()`, `Child()`, `Child(5)`
D. `Child(5)`, `Child()`, `Parent()`

**Solution**

1. `new Child()` → `Child()`'s first statement is `this(5)` → control transfers to `Child(int)`.
2. `Child(int)`'s first statement is `super()` → `Parent()` runs → prints `Parent()`.
3. `super()` returns → `Child(int)` body prints `Child(5)`.
4. `Child(int)` returns → `Child()` continues → prints `Child()`.

**Answer: A.** Output is:

```
Parent()
Child(5)
Child()
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | `Child(5)` cannot print before `Parent()` — `super()` is always the first thing that runs |
| C | `Child()`'s body runs **after** the delegated constructor completes |
| D | Same error as B, plus the parent always runs first |

## Quick rules

- Default constructor exists only if **no** constructor is declared.
- `this(...)` / `super(...)`: first statement, one of them, never both.
- Textual order for fields and blocks; the constructor body is **last**.
- Superclass static initialisation precedes subclass static initialisation.
- `clone()` is shallow; without `Cloneable` it throws `CloneNotSupportedException`.
- `equals` and `hashCode` are independent — override both or neither.
- `finalize()` is deprecated and **not guaranteed**; `transient` fields are skipped by
  serialization.

## Common traps

| Trap | Seen in | Fix |
|---|---|---|
| Default constructor always exists | Q1 | Only when no constructor is declared |
| Subclass static block before superclass's | Q2 | Superclass initialises first |
| Instance block after the constructor body | Q2 | Initialisers run before the body |
| `super()` after a statement | Q3 | Must be first |
| `clone()` is a deep copy | Q4 | Shallow — references are shared |
| `equals` implies `hashCode` is generated | Q5 | You must override both |
| `finalize()` always runs | Q6 | No guarantee |

## Checklist

- [ ] I can predict the Q2 output without pausing.
- [ ] I can list the three reasons a constructor fails to compile.
- [ ] I can explain in one sentence why `b1.count` stayed `1` in Q4 while `b1.items.size()` became `2`.
- [ ] I can state the equals/hashCode contract in one line.
- [ ] I can write the holder-idiom singleton from memory.
- [ ] I finished all 8 inside 14 minutes.

## Related

- [Object lifecycle and construction](../01-concepts/01-object-lifecycle-and-construction.md)
- [Object creation, copying and identity](../01-concepts/02-object-creation-copying-and-identity.md)
- [Constructor rules and compile errors](../02-techniques/01-constructor-rules-and-compile-errors.md)
- [Creation patterns: singleton, immutable, factory, builder](../02-techniques/02-creation-patterns.md)
- [Construction traps](../04-pitfalls/01-construction-and-object-traps.md)
- [Construction one-pager](../05-reference/01-construction-one-pager.md)
- [Topic overview](../README.md)
