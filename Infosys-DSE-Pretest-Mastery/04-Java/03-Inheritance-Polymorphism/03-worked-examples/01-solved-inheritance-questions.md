# Inheritance & Polymorphism — 8 Solved Questions

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 14 min_
> **Prerequisite:** [The method resolution procedure](../02-techniques/01-method-resolution-order.md)

## In one sentence

Inheritance questions reduce to **three moves**: find the declared type, decide static or
instance, then walk up the hierarchy from the runtime class.

## Why the pre-test tests this

- Inheritance is the single biggest source of output-prediction questions in the Java section.
- The distractor tables below are the study material. An answer letter alone teaches nothing.
- Cap each question at 90 seconds.

## Core concept

- **Q1:** override needs a visible, non-`static`, non-`final` parent **instance** method with the
  same signature.
- **Q2, Q3:** instance methods dispatch on the **runtime class**; static methods bind to the
  **declared type**.
- **Q4:** a wrong downcast throws `ClassCastException` at **run time** — it is not a compile error.
- **Q5:** `null instanceof X` is **`false`** and never throws.
- **Q6:** an abstract class **cannot be instantiated**, but it may have **zero** abstract methods
  and it **may** have constructors.
- **Q7:** the constructor chain runs **top-down** — the topmost ancestor first.
- **Q8:** a covariant (narrower) return type **is** legal in an override.

## Worked example

### Q1 — Answer **D** (what can be overridden)

**Which of the following methods CAN be overridden by a subclass?**

A. A `static` method
B. A `final` method
C. A `private` method
D. A `public` instance method

**Solution**

| Option | Overridable? | Reason |
|---|---|---|
| A | ❌ | Static methods are **hidden**, not overridden — they are resolved at compile time |
| B | ❌ | `final` exists precisely to forbid overriding |
| C | ❌ | A private method is **not inherited**, so the child's method has nothing to override |
| D | ✅ | The normal case |

**Answer: D.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Static = hiding. The rules are different, and the exam will test that difference |
| B | `final` = "do not override" in one word |
| C | Private = invisible to the child, so it is a *new* method, not an override |

---

### Q2 — Answer **C** (dynamic dispatch walks up)

**What does the following program print?**

```java
class Animal {
    void speak() { System.out.println("Animal"); }
}
class Dog extends Animal {
    @Override void speak() { System.out.println("Dog"); }
}
class Puppy extends Dog {
    @Override void speak() { System.out.println("Puppy"); }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Puppy();
        a.speak();
    }
}
```

A. `Animal`
B. `Dog`
C. `Puppy`
D. Compile error — `Puppy` cannot be assigned to `Animal`

**Solution**

| Step | Finding |
|---|---|
| 1 | Declared type = `Animal`; `Animal` declares `speak()` → OK |
| 3 | `speak()` is an **instance** method |
| 4 | Runtime class = `Puppy` |
| 5 | `Puppy` declares `speak()` → the most derived implementation wins |

**Answer: C.** Output is:

```
Puppy
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Resolved on the declared type — that is the static/instance confusion |
| B | Forgot the third level of the hierarchy |
| D | `Puppy` **is** an `Animal` — upcasting is implicit and always safe |

---

### Q3 — Answer **B** (static binds to the declared type)

**What does the following program print?**

```java
class Parent {
    static void show() { System.out.println("Parent.show"); }
    void display() { System.out.println("Parent.display"); }
}
class Child extends Parent {
    static void show() { System.out.println("Child.show"); }
    @Override void display() { System.out.println("Child.display"); }
}

public class Main {
    public static void main(String[] args) {
        Parent p = new Child();
        p.show();
        p.display();
    }
}
```

A. `Child.show` then `Child.display`
B. `Parent.show` then `Child.display`
C. `Parent.show` then `Parent.display`
D. `Child.show` then `Parent.display`

**Solution**

| Call | Method | Binding |
|---|---|---|
| `p.show()` | `Parent.show` | **Static** → bound at compile time from the reference's declared type `Parent` |
| `p.display()` | `Child.display` | **Instance** → dispatched at run time on the runtime class `Child` |

**Answer: B.** Output is:

```
Parent.show
Child.display
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Applies runtime dispatch to a static call |
| C | Applies compile-time binding to an instance call |
| D | Both reversed |

---

### Q4 — Answer **B** (`ClassCastException` is a run-time failure)

**What does the following program print?**

```java
class Animal { }
class Dog extends Animal { }

public class Main {
    public static void main(String[] args) {
        Animal a = new Animal();
        try {
            Dog d = (Dog) a;
            System.out.println("ok");
        } catch (ClassCastException e) {
            System.out.println("caught");
        }
    }
}
```

A. `ok`
B. `caught`
C. `ClassCastException` — the program terminates
D. A compile error — the cast is not allowed

**Solution**

The compiler permits `(Dog) a` because `Dog` and `Animal` are related types. At run time the
object is an `Animal`, not a `Dog`, so the cast throws `ClassCastException`, which the `catch`
block handles.

**Answer: B.** Output is:

```
caught
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The object's runtime type is `Animal`, not `Dog` |
| C | The `catch` block catches the exception, so the program does not terminate |
| D | The cast is *related*, so it compiles — the failure is at run time |

---

### Q5 — Answer **B** (`instanceof` and `null`)

**What is the value of `result`?**

```java
Object o = null;
boolean result = (o instanceof String);
```

A. `true`
B. `false`
C. It throws a `NullPointerException`
D. It does not compile

**Solution**

`instanceof` returns `false` for a `null` reference — it never throws. The `null` check is
implicit.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Confuses "the reference is of the declared type" with a runtime check |
| C | `instanceof` is null-safe by design — that is one of its main uses |
| D | `o` is declared `Object`, so the cast check compiles fine |

---

### Q6 — Answer **C** (facts about abstract classes)

**Which of the following statements about abstract classes is TRUE?**

A. An abstract class must contain at least one abstract method.
B. An abstract class cannot have a constructor.
C. An abstract class cannot be instantiated.
D. An abstract class cannot extend another class.

**Solution**

| Option | Verdict | Reason |
|---|---|---|
| A | ❌ | An abstract class may have **zero** abstract methods — this is the classic trap |
| B | ❌ | It **can** have constructors, and they run when a subclass is created |
| C | ✅ | `new AbstractClass()` is a compile error — that is the defining restriction |
| D | ❌ | An abstract class **can** extend another class, and can even extend a concrete class |

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | The most common false belief about abstract classes |
| B | Confuses "cannot be instantiated" with "cannot be constructed" |
| D | Nothing stops an abstract class from having a superclass |

---

### Q7 — Answer **D** (the constructor chain is top-down)

**What does the following program print?**

```java
class A { A() { System.out.println("A"); } }
class B extends A { B() { super(); System.out.println("B"); } }
class C extends B { C() { super(); System.out.println("C"); } }

public class Main {
    public static void main(String[] args) {
        new C();
    }
}
```

A. `C`, `B`, `A`
B. `A`, `C`, `B`
C. `B`, `A`, `C`
D. `A`, `B`, `C`

**Solution**

`new C()` → `C()`'s first statement is `super()` → `B()` → `B()`'s first statement is `super()` →
`A()` → prints `A` → back to `B()` → prints `B` → back to `C()` → prints `C`.

**Answer: D.** Output is:

```
A
B
C
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Thinks the subclass body runs first — the chain always goes **up** first |
| B | Middle class out of order |
| C | Middle class out of order |

---

### Q8 — Answer **B** (covariant return types)

**Does the following code compile?**

```java
class A {
    Object get() { return null; }
}

class B extends A {
    @Override
    String get() { return "b"; }
}
```

A. No — an override must have the identical return type.
B. Yes — `String` is a subtype of `Object`, so this is a legal covariant return.
C. No — `B` is not allowed to change the return type of `A.get()`.
D. Yes, but only if `A` is declared `abstract`.

**Solution**

An override may return a **covariant** type — any subtype of the parent's return type.
`String` is a subtype of `Object`, so the code compiles and `B.get()` is a valid override of
`A.get()`.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Confuses "the return type must be compatible" with "must be identical". Identical is required for *overloading on return type* — which is illegal anyway |
| C | Covariant returns are explicitly allowed by the Java Language Specification |
| D | Nothing about `abstract` changes the rule |

## Quick rules

- Overridable = visible, non-`static`, non-`final` **instance** method with the same signature.
- Instance methods dispatch on the **runtime class**; static methods bind to the **declared
  type**.
- A wrong downcast throws at **run time** — guard it with `instanceof`.
- `null instanceof X` → **`false`**.
- Abstract class: **cannot be instantiated**; **may** have constructors; **may** have zero
  abstract methods.
- The constructor chain runs **top-down**, starting at `Object()`.
- Covariant (narrower) return types **are** legal in an override.

## Common traps

| Trap | Seen in | Fix |
|---|---|---|
| Static treated as overridable | Q1 | Static methods are hidden |
| `private` treated as overridable | Q1 | Not inherited |
| Dispatch on the declared type | Q2 | Runtime class for instance methods |
| Downcast failure treated as a compile error | Q4 | It is a run-time failure |
| `instanceof` assumed to throw on `null` | Q5 | It returns `false` |
| Abstract class assumed to need an abstract method | Q6 | Zero is allowed |
| Constructor chain assumed to run bottom-up | Q7 | Top-down |
| Covariant return assumed illegal | Q8 | Narrowing is legal |

## Checklist

- [ ] I can predict the output of Q2, Q3, Q4 and Q7 without hesitating.
- [ ] I can fill in the overridability triage table from memory.
- [ ] I know the abstract-class facts, especially "zero abstract methods is legal".
- [ ] I know `instanceof` is null-safe.
- [ ] I finished all 8 inside 14 minutes.

## Related

- [Inheritance basics and dynamic dispatch](../01-concepts/01-inheritance-basics-and-dispatch.md)
- [Casts, type checks and ClassCastException](../01-concepts/02-casts-type-checks-and-errors.md)
- [Abstract, final and the constructor chain](../01-concepts/03-abstract-final-and-the-constructor-chain.md)
- [The method resolution procedure](../02-techniques/01-method-resolution-order.md)
- [Override vs hide triage](../02-techniques/02-override-vs-hide-triage.md)
- [Inheritance traps](../04-pitfalls/01-inheritance-traps.md)
- [Inheritance one-pager](../05-reference/01-inheritance-one-pager.md)
- [Topic overview](../README.md)
