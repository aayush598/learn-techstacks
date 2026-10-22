# Inheritance & Polymorphism — Traps the Exam Sets for You

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 8 min_
> **Prerequisite:** [The method resolution procedure](../02-techniques/01-method-resolution-order.md)

## In one sentence

Inheritance traps come in exactly two flavours: **the wrong binding** (static vs instance) and
**the wrong verdict** (override vs hide vs new method).

## Why the pre-test tests this

- Output-prediction questions on a class hierarchy are a staple of the 25-question Java section.
- The two flavours above account for the overwhelming majority of wrong answers.
- Naming the trap is what stops you making it — a candidate who knows "static binds to the
  declared type" does not need to think during the question.

## Core concept

### The 8 canonical inheritance traps

| # | Trap | The wrong answer it produces | The truth |
|---|---|---|---|
| 1 | **Static dispatch** | `Child.show` for a static call | Static binds to the **declared type** |
| 2 | **Instance dispatch** | `Parent.i` for an instance call | Instance dispatches on the **runtime class** |
| 3 | **Static is overridable** | "Yes, static methods can be overridden" | They are **hidden** |
| 4 | **Private is overridable** | "Yes" | Not inherited → a **new** method |
| 5 | **Final is overridable** | "Yes" | **Compile error** |
| 6 | **Abstract class needs an abstract method** | "True" | **Zero** abstract methods is legal |
| 7 | **Constructor chain is bottom-up** | Wrong output order | **Top-down**: `Object()` first |
| 8 | **Covariant return is illegal** | "Compile error" | Narrowing the return type is **legal** |

### Trap 3 and 5 in detail — the "can it be overridden?" trio

The exam option is usually one of four candidates, and **three** of them cannot be overridden:

| Candidate | Overridable? | Exact reason to give |
|---|---|---|
| `public` instance method | ✅ yes | — |
| `private` method | ❌ no | Not inherited — the child's method is brand new |
| `static` method | ❌ no | Static methods are **hidden**, not overridden |
| `final` method | ❌ no | `final` forbids overriding |

### Trap 4 in detail — the private method that is not inherited

```java
class Parent {
    private void hidden() { System.out.println("Parent.hidden"); }
}
class Child extends Parent {
    void hidden() { System.out.println("Child.hidden"); }   // a NEW method, not an override
}
```

`Child.hidden` has nothing to do with `Parent.hidden` — the parent's method is not inherited, so
the child simply declares a method with the same name. Calling `parentRef.hidden()` from outside
`Parent` is a **compile error**, because the resolved method is the private `Parent.hidden`.

### Trap 6 in detail — abstract classes

```java
abstract class Marker { }                    // legal — zero abstract methods
abstract class Shape { abstract double area(); }
```

An abstract class exists to say *"you cannot instantiate me"*. It does **not** have to declare
anything abstract. A class with a `default` method only — an abstract class with a concrete
implementation of everything — is perfectly legal.

### Trap 7 in detail — the constructor chain direction

```
new C()  →  C()  →  super()  →  B()  →  super()  →  A()  →  super()  →  Object()
```

The **calls** go down the chain (C → B → A), but the **bodies** execute bottom-up in that
sequence: `A()`'s body runs first, then `B()`'s, then `C()`'s. The print order is
`A, B, C`.

### Trap 8 in detail — covariant returns

```java
class A { Object get() { return null; } }
class B extends A { @Override String get() { return "b"; } }   // legal
```

`String` is a subtype of `Object`, so the override **narrows** the return type — this is allowed
and is called a **covariant return**. The opposite — widening — is a compile error.

## Worked example

**Q. Consider:**

```java
class Parent {
    private void hidden() { System.out.println("Parent.hidden"); }
    static void stat() { System.out.println("Parent.stat"); }
    void inst() { System.out.println("Parent.inst"); }
}

class Child extends Parent {
    void hidden() { System.out.println("Child.hidden"); }
    static void stat() { System.out.println("Child.stat"); }
    @Override void inst() { System.out.println("Child.inst"); }
}

public class Main {
    public static void main(String[] args) {
        Parent p = new Child();
        p.inst();
        p.stat();
        p.hidden();     // ← what does this do?
    }
}
```

**A.** `Child.inst`, `Parent.stat`, `Child.hidden`
**B.** `Child.inst`, `Child.stat`, `Parent.hidden`
**C.** `Child.inst`, `Parent.stat`, `Parent.hidden`
**D.** The program does not compile — `p.hidden()` is not accessible from `Main`

**The trap:** the `hidden()` method. It has the same name and signature as a parent method, so
candidates assume it is an override and that `Child.hidden()` runs.

**What a candidate who fell for it does:** picks **A** and assumes `p.hidden()` calls
`Child.hidden()`.

**The right reasoning:**

| Call | Method | Why |
|---|---|---|
| `p.inst()` | `Child.inst` | Instance method → runtime class `Child` overrides it |
| `p.stat()` | `Parent.stat` | Static → bound to the declared type `Parent`; `Child.stat` hides it |
| `p.hidden()` | ❌ compile error | The compile-time declaration is `Parent.hidden`, which is **`private`**. A private member is accessible only inside the body of the top-level class that declares it — `Parent`. `Main` is a different top-level class, so the call is **not accessible** |

**Answer: D.** The program does not compile, so **nothing prints at all**.

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Thinks `hidden()` is overridden — a private method is not inherited, so there is nothing to override; and the call is not even accessible |
| B | Thinks the static call dispatches on the runtime class |
| C | Thinks the call is legal and resolves to `Parent.hidden` — but a private member is reachable only from inside `Parent` |

> **Why not C?** `Parent.hidden` is private, so it cannot be called from `Main` even though
> `Main` sits in the same **file**. Private access is scoped to the **top-level class body** that
> declares it, not to the file.

**The related fact that the exam also tests:** if the call were written as
`Child c = new Child(); c.hidden();`, it would still fail — `Child.hidden` is not inherited from
`Parent`, so `c.hidden()` inside `Main` resolves to `Child.hidden` only if `Child.hidden` is
accessible (it is package-private here, and `Main` is in the same package, so it compiles and
prints `Child.hidden`). The visibility question is asked **per candidate method**, and the
candidate list is seeded from the **declared type** of the reference.

## Quick rules

- Instance → runtime class. Static → declared type. Never mix them up.
- Not overridable: `private`, `static`, `final`, constructors.
- `static` = hidden; `private` = not inherited; `final` = compile error.
- An abstract class may have **zero** abstract methods and **may** have constructors.
- Constructor bodies execute **top-down**: `A`, `B`, `C`.
- A covariant (narrower) return type is **legal**; a wider one is not.
- An override may widen access, never narrow it.
- A package-private parent method is overridable only from the **same package**.

## Common traps

| Trap | The wrong answer you would give | The right answer | Signal that you fell for it |
|---|---|---|---|
| Static dispatch | `Child.stat` | `Parent.stat` | You applied "runtime polymorphism" to a static call |
| Private is overridable | `Child.hidden` | Compile error — not accessible from `Main` | You matched signatures without checking visibility |
| Abstract needs an abstract method | "Must have one" | May have zero | You assumed the name implies the content |
| Chain is bottom-up | `C, B, A` | `A, B, C` | You followed the `new` call downward, not the body order |
| Covariant illegal | "Compile error" | Legal | You over-remembered the rule |

## Checklist

- [ ] I can state the three kinds of method that cannot be overridden.
- [ ] I can explain in one sentence why a private parent method is "not an override".
- [ ] I know the abstract-class facts, including zero abstract methods.
- [ ] I can write the constructor chain order from memory.
- [ ] I know covariant returns are legal.
- [ ] I know that a package-private parent method is overridable only within its package.

## Related

- [Inheritance basics and dynamic dispatch](../01-concepts/01-inheritance-basics-and-dispatch.md)
- [Casts, type checks and ClassCastException](../01-concepts/02-casts-type-checks-and-errors.md)
- [Abstract, final and the constructor chain](../01-concepts/03-abstract-final-and-the-constructor-chain.md)
- [The method resolution procedure](../02-techniques/01-method-resolution-order.md)
- [Override vs hide triage](../02-techniques/02-override-vs-hide-triage.md)
- [8 solved inheritance questions](../03-worked-examples/01-solved-inheritance-questions.md)
- [Inheritance one-pager](../05-reference/01-inheritance-one-pager.md)
- [Topic overview](../README.md)
