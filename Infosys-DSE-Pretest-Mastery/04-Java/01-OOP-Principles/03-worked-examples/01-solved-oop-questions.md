# OOP Principles — 8 Solved Questions

> Section 4 · Java · OOP Principles · _Estimated reading time: 14 min_
> **Prerequisite:** [Identifying the pillar behind a code snippet](../02-techniques/01-identifying-a-pillar-procedure.md)

## In one sentence

Every OOP-principles answer is either a **one-word principle** or a **one-line output**, and the
8 questions below cover the shapes those answers take.

## Why the pre-test tests this

- Concept questions like these are the fast 1-markers that make a 25-question section survivable
  if the output-prediction ones go badly.
- Time each question at 90 seconds. If you exceed it, flag and move.

## Core concept

Each answer below comes from exactly one of five facts:

| # | Fact | Used in |
|---|---|---|
| 1 | The four pillars are Encapsulation, Abstraction, Inheritance, Polymorphism — nothing else | Q1 |
| 2 | Static methods bind at compile time; instance methods dispatch at run time | Q2, Q8 |
| 3 | Overload resolution runs strict → loose → varargs | Q4 |
| 4 | `abstract` cannot combine with `static`, `final` or `private` on a method | Q5 |
| 5 | An interface has no constructors and only `public static final` fields; a class extends one class but implements many interfaces | Q6, Q9 |

## Worked example

### Q1 — Answer **C** (which is NOT an OOP principle)

**Which of the following is NOT a principle of object-oriented programming?**

A. Encapsulation
B. Inheritance
C. Compilation
D. Polymorphism

**Solution**

The four pillars are encapsulation, abstraction, inheritance, polymorphism. Compilation is the
`javac` step that turns source into bytecode — a build activity, not a design principle.

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Encapsulation is pillar #1 |
| B | Inheritance is pillar #3 |
| D | Polymorphism is pillar #4 |

### Q2 — Answer **B** (static binds at compile time)

**What does the following program print?**

```java
class Parent {
    static void show()  { System.out.println("Parent.show"); }
    void display()      { System.out.println("Parent.display"); }
}

class Child extends Parent {
    static void show()  { System.out.println("Child.show"); }
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

| Call | Compile-time view of `p` | Runtime class of the object | Method that runs |
|---|---|---|---|
| `p.show()` | `Parent` — `show` is `static`, so it is resolved by the compiler from the **reference's type** | `Child` (irrelevant for a static call) | `Parent.show` |
| `p.display()` | `Parent` (only tells us it is overridable) | `Child` | `Child.display` |

`Child.show` **hides** `Parent.show`; hiding is a compile-time mechanism.

**Answer: B.** Output is:

```
Parent.show
Child.display
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Thinks both calls dispatch on the runtime type — true for instance methods, false for static ones |
| C | Thinks `display()` also binds statically — instance methods always dispatch on the runtime class |
| D | Backwards: the static call binds to the parent, the instance call binds to the child |

### Q3 — Answer **A** (`this` vs `super` field resolution)

**What does the following program print?**

```java
class Base {
    String name = "Base";
    Base() { System.out.println("Base ctor"); }
}

class Derived extends Base {
    String name = "Derived";
    Derived() {
        super();
        System.out.println(name);
    }
}

public class Main {
    public static void main(String[] args) {
        new Derived();
    }
}
```

A. `Base ctor` then `Derived`
B. `Derived` then `Base ctor`
C. `Base ctor` then `Base`
D. `Base` then `Base ctor`

**Solution**

1. `new Derived()` → `Derived`'s constructor begins, and its first statement is `super()`.
2. `super()` runs `Base()` → prints `Base ctor`.
3. `Base`'s field initialiser runs → `Base.name = "Base"`.
4. `Derived`'s field initialiser runs → `Derived.name = "Derived"` — it **hides** `Base.name`.
5. `System.out.println(name)` → unqualified `name` resolves to the **nearest** declaration →
   `Derived.name` → prints `Derived`.

**Answer: A.** Output is:

```
Base ctor
Derived
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Field initialisers run **after** the superclass constructor, so `Base ctor` comes first |
| C | Thinks `name` resolves to the parent — only `super.name` does that |
| D | Two field values and the wrong order; `Base ctor` always precedes the subclass initialiser |

### Q4 — Answer **D** (overload resolution phases)

**What does the following program print?**

```java
class Calc {
    void add(int a)     { System.out.println("int"); }
    void add(long a)    { System.out.println("long"); }
    void add(Integer a) { System.out.println("Integer"); }
    void add(Object a)  { System.out.println("Object"); }
    void add(int... a)  { System.out.println("varargs"); }
}

public class Main {
    public static void main(String[] args) {
        Calc c = new Calc();
        c.add(5);
        c.add(5L);
        c.add(Integer.valueOf(5));
        c.add("x");
        c.add(1, 2);
    }
}
```

A. `int`, `long`, `int`, `Object`, `varargs`
B. `int`, `long`, `Integer`, `Object`, `Object`
C. `long`, `long`, `Integer`, `Object`, `varargs`
D. `int`, `long`, `Integer`, `Object`, `varargs`
E. `int`, `long`, `Integer`, `Object`, `int`

**Solution**

| Call | Phase | Chosen | Reason |
|---|---|---|---|
| `add(5)` | 1 strict | `add(int)` | Exact match, no conversion needed |
| `add(5L)` | 1 strict | `add(long)` | Exact match |
| `add(Integer)` | 2 loose | `add(Integer)` | Phase 1 forbids unboxing; phase 2 allows it and `Integer` is most specific |
| `add("x")` | 1 strict | `add(Object)` | Widening reference conversion; no boxing needed |
| `add(1, 2)` | 3 varargs | `add(int...)` | Arity 2 fits only the varargs method |

**Answer: D.** Output is:

```
int
long
Integer
Object
varargs
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Unboxes the `Integer` argument to `int` — unboxing is not allowed in phase 1, and in phase 2 `add(Integer)` is more specific |
| B | Thinks `add(1,2)` matches `add(Object)` — two arguments cannot be passed to a single-parameter method; only the varargs method has arity 2 |
| C | Picks `add(long)` for the literal `5` — phase 1 allows the exact `int` match, which is more specific than widening to `long` |
| E | Thinks `add(1,2)` matches `add(int)` — that method takes exactly one argument |

### Q5 — Answer **B** (illegal modifier combination)

**Which of the following method declarations is a compile error inside an abstract class?**

A. `abstract void f();`
B. `static abstract void f();`
C. `final void f() { }`
D. `private void f() { }`

**Solution**

| Option | Legal? | Reason |
|---|---|---|
| A | ✅ | An abstract class may declare abstract methods — that is the whole point of it |
| B | ❌ | `abstract` + `static` is an illegal combination: a static method is not inherited-and-overridden, and an abstract method must have a body implemented by a subclass |
| C | ✅ | A `final` concrete method in an abstract class is fine |
| D | ✅ | A `private` concrete method is fine (it is simply not inherited) |

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Perfectly legal inside an abstract class |
| C | `final` and `abstract` are not required together; `final void f() {}` is concrete and legal |
| D | `private` is legal on a method; only `private` + `abstract` is illegal |

### Q6 — Answer **B** (interface facts)

**Which of the following statements about interfaces in Java is TRUE?**

A. A class can extend at most one class and implement at most one interface.
B. A class can extend at most one class and implement any number of interfaces.
C. An interface can contain constructors and instance variables.
D. All methods of an interface must be abstract.

**Solution**

| Option | Verdict | Reason |
|---|---|---|
| A | ❌ | The "one class" limit is real; the "one interface" limit is not |
| B | ✅ | **Single class inheritance + multiple interface implementation** — the single most-tested fact about interfaces |
| C | ❌ | An interface has **no constructors** and no instance fields (its fields are `public static final`) |
| D | ❌ | Since Java 8 an interface may have `default` and `static` methods with bodies |

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Half-right — it is the most common partial-knowledge trap |
| C | Confuses interface with abstract class; interfaces have no constructor and no instance state |
| D | Ignores Java 8 `default` and `static` interface methods |

### Q7 — Answer **C** (what blocks overriding)

**Which of the following methods CANNOT be overridden by a subclass?**

A. A `public` instance method
B. A `protected` instance method
C. A `final` instance method
D. A `public` instance method declared in an interface as abstract

**Solution**

| Option | Overridable? | Reason |
|---|---|---|
| A | ✅ yes | The normal case |
| B | ✅ yes | `protected` is visible to subclasses, so it can be overridden |
| C | ❌ **no** | `final` is exactly the "cannot be overridden" keyword |
| D | ✅ yes | An interface's abstract method **must** be implemented by the implementing class |

**Answer: C.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | `public` methods are the most overridable of all |
| B | `protected` is package + subclass access — visible enough to override |
| D | An abstract interface method is *required* to be overridden (implemented) |

### Q8 — Answer **A** (the "class wins" rule)

**What does the following program print?**

```java
class Parent {
    public void greet() { System.out.println("Parent.greet"); }
}

interface Greeter {
    default void greet() { System.out.println("Greeter.greet"); }
}

class Child extends Parent implements Greeter {
}

public class Main {
    public static void main(String[] args) {
        new Child().greet();
    }
}
```

A. `Parent.greet`
B. `Greeter.greet`
C. `Greeter.greet` then `Parent.greet`
D. Compile error — ambiguous method

**Solution**

`Child` inherits `Parent.greet()` (a concrete method from the superclass) **and** the default
`Greeter.greet()` (from the interface). Java's rule: **a method inherited from a class wins over
a default method inherited from an interface.** There is no ambiguity and no compile error — the
class method is simply used.

**Answer: A.** Output is:

```
Parent.greet
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Thinks the interface default wins — it does not |
| C | Thinks both run — only one method is invoked |
| D | Thinks the conflict is an error — the "class wins" rule resolves it silently |

## Quick rules

- The pillars are E, A, I, P. Compilation and optimization are never pillars.
- `static` call → the **reference's** type runs it. Instance call → the **object's** type runs it.
- Superclass constructor and its field initialisers run **before** the subclass's.
- Overload resolution: strict → loose → varargs. Never jump straight to varargs.
- `abstract` cannot be combined with `static`, `final` or `private`.
- One class per `extends`; unlimited `implements`.
- `final` method = no overriding (overloading is still fine).
- A superclass method beats an interface default method. No error.

## Common traps

| Trap | Seen in | Fix |
|---|---|---|
| Treating a static call as polymorphic | Q2 | Static binds to the reference's declared type |
| Unqualified field resolving to the parent | Q3 | Nearest declaration wins; use `super.name` for the parent |
| Unboxing too early in overload resolution | Q4 | Phase 1 forbids boxing; `Integer` beats `int` in phase 2 |
| Assuming abstract and static coexist | Q5 | Illegal combination |
| Believing interfaces allow one implementation only | Q6 | Many interfaces, one class |
| Expecting a compile error on the default-method conflict | Q8 | Class wins |

## Checklist

- [ ] I answered Q2 without running the code in my head — the output is `Parent.show` then `Child.display`.
- [ ] I got Q4 right, especially `add(Integer.valueOf(5))` → `Integer`.
- [ ] I can name all three illegal `abstract` combinations.
- [ ] I can state the "class wins" rule and its output.
- [ ] I finished all 8 inside 14 minutes (≈ 100 s each including reading).

## Related

- [The four pillars](../01-concepts/01-the-four-pillars.md)
- [Overloading vs overriding](../01-concepts/02-overloading-vs-overriding.md)
- [`this`, `super` and the modifier matrix](../01-concepts/03-this-super-and-modifiers.md)
- [Identifying the pillar behind a code snippet](../02-techniques/01-identifying-a-pillar-procedure.md)
- [Abstract class vs interface](../02-techniques/02-abstract-class-vs-interface.md)
- [OOP principles traps](../04-pitfalls/01-oop-principles-traps.md)
- [OOP principles one-pager](../05-reference/01-oop-principles-one-pager.md)
- [Topic overview](../README.md)
