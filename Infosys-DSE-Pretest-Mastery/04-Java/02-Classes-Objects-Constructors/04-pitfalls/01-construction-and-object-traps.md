# Classes & Objects — Traps the Exam Sets for You

> Section 4 · Java · Classes, Objects & Constructors · _Estimated reading time: 8 min_
> **Prerequisite:** [Object lifecycle and construction](../01-concepts/01-object-lifecycle-and-construction.md)

## In one sentence

The object-lifecycle traps all share one root: **Java does more than you think, automatically, at
a moment you did not specify.**

## Why the pre-test tests this

- The Java section's compile-or-not questions are cheap marks if you know the automatic rules, and
  pure losses if you do not.
- The traps below are the specific automatic behaviours: the implicit default constructor, the
  implicit `super()` call, the implicit `this` reference.
- Each trap below names the wrong answer it produces, so you can catch yourself in the test.

## Core concept

### The 8 canonical traps

| # | Trap | The option that sells it | The truth |
|---|---|---|---|
| 1 | **Default constructor always exists** | "Compiles fine" | Only if the class declares **no** constructor |
| 2 | **`super()` after a statement** | "Compiles fine" | An explicit `super(...)` must be the **first** statement |
| 3 | **Instance initialisers run after the constructor** | Wrong output order | They run **before** the body |
| 4 | **Subclass static block before the superclass's** | Wrong output order | The superclass initialises **first** |
| 5 | **`clone()` is a deep copy** | "The nested list is copied too" | `clone()` is **shallow** — references are shared |
| 6 | **Overriding `equals` overrides `hashCode`** | "Yes" | They are **independent** methods |
| 7 | **`finalize()` will run** | "The GC calls it before collecting" | It is **deprecated** and **never guaranteed** |
| 8 | **Naive lazy singleton is thread-safe** | "Thread-safe" | Two threads can create **two** instances |

### Trap 3 and 4 in detail — the two ordering traps

**Trap 3 — instance state vs constructor body.** A subclass field initialiser runs *before* the
subclass constructor body, not after. This matters whenever a field and a constructor write to
the same place:

```java
class C {
    int x = 5;             // runs before the constructor body
    C() { x = 10; }        // overwrites it
}
new C().x   // 10, not 5
```

**Trap 4 — superclass static initialisation.** When the JVM initialises a subclass, it initialises
the superclass **first**. So a static block in `Base` always prints before a static block in
`Derived`, no matter which file order you imagine.

### Trap 5 in detail — shallow vs deep copy, the numbers

```java
class Node implements Cloneable {
    int v = 1;
    List<String> tags = new ArrayList<>();
    public Node clone() { try { return (Node) super.clone(); } catch (CloneNotSupportedException e) { return null; } }
}
```

| After `n2 = n1.clone(); n2.tags.add("x");` | Value | Why |
|---|---|---|
| `n1.tags.size()` | `1` | The **same** list object is referenced by both copies |
| `n1.v` | `1` | `int` copied by value; assigning `n2.v` does not touch `n1.v` |

A deep copy would give `n1.tags.size() == 0`.

### Trap 6 in detail — the equals/hashCode pairing

Overriding `equals` without `hashCode` is the most common real-world bug in this area, and the
exam asks "what happens if you override only `equals`?" The answer:

> Two objects that `equals` reports as equal can end up in **different buckets** of a `HashSet`,
> so the set can contain "duplicates".

Rule 4 of the contract is the one to memorise: **equal objects ⇒ equal hash codes.**

### Trap 8 in detail — the singleton race

```java
class Bad {
    private static Bad instance;
    private Bad() { }
    static Bad getInstance() {
        if (instance == null) {       // thread A and thread B can both be here
            instance = new Bad();     // two instances created
        }
        return instance;
    }
}
```

The fix is either the **holder idiom** (no `synchronized` needed) or **double-checked locking
with a `volatile` field**.

## Worked example

**Q. Consider the following class. What is the value of `x` after `new C()`?**

```java
class C {
    int x = 5;
    static int s = 100;

    static {
        s = s + 1;
    }

    {
        x = x * 2;
    }

    C() {
        x = x + 1;
    }
}
```

A. `5`
B. `10`
C. `11`
D. `6`

**The trap:** candidates treat the initialiser block as if it ran after the constructor, or assume
the field initialiser overwrites the block.

**What a candidate who fell for it does:** picks **A** — they reason "the field initialiser sets
`x = 5` last, after everything".

**The right reasoning:**

| Step | Statement | `x` after the step |
|---|---|---|
| 1 | Field initialiser: `x = 5` | `5` |
| 2 | Instance initialiser block: `x = x * 2` | `10` |
| 3 | Constructor body: `x = x + 1` | `11` |

The three statements run in **textual order**, and the constructor body runs **last**.

**Answer: C.** `x` is `11`.

**Note on `s`:** the static field and the static block run at **class initialisation** — the first
time `C` is actively used, which here is at `new C()`. `s` becomes `100`, then the static block
makes it `101`. The static block does **not** affect `x` at all.

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Assumes the field initialiser runs last — it runs first |
| B | Stops after the instance block and ignores the constructor body |
| D | Thinks the block and constructor body conflict somehow and one wins |

## Quick rules

- Default constructor: **only** if no constructor is declared; it takes the class's visibility.
- An explicit `super(...)` must be the **first** statement; there is no way to have both
  `this(...)` and `super(...)`.
- Textual order for fields and blocks; the constructor body is **last**.
- Superclass static initialisation precedes subclass static initialisation.
- `clone()` is shallow; without `Cloneable` it throws `CloneNotSupportedException`.
- `equals` and `hashCode` are independent — override both or neither.
- `finalize()` is deprecated and **not guaranteed**; `transient` fields are skipped by
  serialization.
- Thread-safe lazy singleton without `synchronized` = **holder idiom**.

## Common traps

| Trap | The wrong answer you would give | The right answer | Signal that you fell for it |
|---|---|---|---|
| Default constructor exists | "Compiles fine" | Compile error | You did not check whether a constructor was declared |
| `super()` placement | "Compiles fine" | Compile error | You did not look at the first statement |
| Initialiser vs constructor order | `5` or `10` | `11` | You put the field initialiser last |
| Subclass static before superclass | Wrong output | Superclass first | You imagined file order, not class-init order |
| `clone()` depth | "The list is copied" | Same list | You assumed deep copy |
| `equals` auto-updates `hashCode` | "Yes" | No — override both | You assumed the compiler helps |
| `finalize()` guaranteed | "Runs before GC" | No guarantee | You trusted the old documentation |
| Naive singleton | "Thread-safe" | Race condition | You did not check for two threads |

## Checklist

- [ ] I can state the default-constructor rule and its visibility rule.
- [ ] I can list the three automatic actions of Java: default constructor, implicit `super()`,
      implicit `this`.
- [ ] I can write the textual-order execution template for fields, blocks and constructor body.
- [ ] I can explain the shallow-copy numbers in one sentence.
- [ ] I know the equals/hashCode contract rule 4.
- [ ] I can say why the holder-idiom singleton needs no `synchronized`.

## Related

- [Object lifecycle and construction](../01-concepts/01-object-lifecycle-and-construction.md)
- [Object creation, copying and identity](../01-concepts/02-object-creation-copying-and-identity.md)
- [Constructor rules and compile errors](../02-techniques/01-constructor-rules-and-compile-errors.md)
- [Creation patterns: singleton, immutable, factory, builder](../02-techniques/02-creation-patterns.md)
- [8 solved construction questions](../03-worked-examples/01-solved-construction-questions.md)
- [Construction one-pager](../05-reference/01-construction-one-pager.md)
- [Topic overview](../README.md)
