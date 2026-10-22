# Inheritance Basics and Dynamic Dispatch

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 9 min_
> **Prerequisite:** [OOP Principles](../01-OOP-Principles/README.md)

## In one sentence

Inheritance gives you a **parent-child type relation**, and Java decides which method runs by
asking a single question: **is the method static (bind now) or instance (bind later)?**

## Why the pre-test tests this

- The 25-question Java section is full of "predict the output" questions built on a
  superclass/subclass pair. Every one of them is decided by the binding rule.
- "Can a static method be overridden?" / "Can a final method be overridden?" / "Can a private
  method be overridden?" are three of the highest-frequency 1-markers in the Java pre-test.
- The output-prediction questions are where candidates who read only the concept lose marks.

## Core concept

### The vocabulary

| Term | Meaning |
|---|---|
| **Superclass / parent / base class** | The class being extended |
| **Subclass / child / derived class** | The class doing the extending |
| **Direct superclass** | The class immediately above in the hierarchy — this is what `super` refers to |
| **`extends`** | Keyword for class inheritance |
| **`implements`** | Keyword for interface implementation |
| **Overriding** | Redefining an inherited **instance** method in the subclass |
| **Hiding** | Redefining an inherited **static** method in the subclass |
| **Dynamic dispatch** | Choosing the overriding implementation at **run time** based on the object's runtime class |

### Java's single inheritance rule

| Rule | Statement |
|---|---|
| Class inheritance | A class can extend **at most one** superclass |
| Interface implementation | A class can implement **any number** of interfaces |
| Interface inheritance | An interface can extend **any number** of interfaces — but never a class |
| Multiple levels | A hierarchy can be arbitrarily deep: `Object → A → B → C` |
| The root | Every class extends `Object` implicitly |

### The `super` keyword

| Usage | Meaning |
|---|---|
| `super.method()` | Call the **immediate parent's** implementation, skipping the child's override |
| `super.field` | Read the **immediate parent's** field (when the child shadows it) |
| `super(args)` | Call the parent's constructor — must be the **first** statement |
| `super` in a static method | ❌ compile error — "non-static variable super cannot be referenced from a static context" |

```java
class Parent {
    void show() { System.out.println("Parent.show"); }
}

class Child extends Parent {
    @Override
    void show() {
        super.show();                  // prints Parent.show
        System.out.println("Child.show");
    }
}

new Child().show();   // prints exactly:
                     // Parent.show
                     // Child.show
```

`super` reaches **one level only**. To reach a grandparent you must go through it explicitly
(`super.super` does not exist).

### The binding rule — the whole topic in one table

| | **Static method** | **Instance method** |
|---|---|---|
| Binding time | **Compile time** | **Run time** |
| Chosen by | The **declared type** of the reference | The **runtime class** of the object |
| Inherited? | Yes, but it can only be **hidden** | Yes, and it can be **overridden** |
| `final` | Cannot be overridden **or hidden** | Cannot be overridden |
| `private` | Not inherited | Not inherited |
| `this` allowed | ❌ | ✅ |

```java
class Parent {
    static void s() { System.out.println("Parent.s"); }
    void i()      { System.out.println("Parent.i"); }
}
class Child extends Parent {
    static void s() { System.out.println("Child.s"); }
    @Override void i() { System.out.println("Child.i"); }
}

Parent p = new Child();
p.s();   // Parent.s   <- compile-time binding, static HIDING
p.i();   // Child.i    <- run-time binding, dynamic dispatch
```

### Method resolution order — how the JVM picks the method

For a call `ref.m(args)`:

| Step | Action |
|---|---|
| 1 | Take the **declared (static) type** of `ref`. Find a method `m` that is applicable to the arguments and **accessible**. If none exists → ❌ compile error |
| 2 | If the selected method is **`static`** → **bind now** to the class that declared it. The subclass's version *hides* it. Done |
| 3 | If the selected method is an **instance** method → the call is **virtual**. Take the **runtime class** `R` of the object |
| 4 | Search `R` and then **up** its superclass chain for the **most derived** implementation of `m` |
| 5 | If no superclass provides one, look for a **`default`** method in an implemented interface |
| 6 | If nothing is found anywhere → the class must be abstract; a concrete class cannot be instantiated |

Worked example — each step visible:

```java
class Animal {
    void speak() { System.out.println("Animal"); }
}
class Dog extends Animal { }                 // does NOT override speak()

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        a.speak();
    }
}
```

Step 1: `Animal` declares `speak()` — applicable and accessible. Step 3: runtime class is `Dog`.
Step 4: `Dog` does not declare `speak()`, so the search moves up to `Animal`, which provides it.

**Output:**

```
Animal
```

### Overriding vs hiding — the one-line distinction

| | **Overriding** | **Hiding** |
|---|---|---|
| Applies to | Instance methods | Static methods |
| Resolved by | The **runtime class** of the object | The **declared type** of the reference |
| Return type | Same or **covariant** | Same or **covariant** |
| Access modifier | Same or **wider** only | Same or **wider** only |
| `final` | Blocks it | Blocks it |
| `super.method()` | Calls the parent's version | Calls the parent's version |

### Covariant return types in an override

```java
class A { Object get() { return null; } }
class B extends A { @Override String get() { return "b"; } }   // legal
```

| Return relationship | Legal in an override? |
|---|---|
| Same type | ✅ |
| Narrower / covariant (`String` for `Object`) | ✅ |
| Wider (`Object` for `String`) | ❌ compile error |
| Unrelated (`Integer` for `String`) | ❌ compile error |

Covariant returns let a subclass narrow a contract without breaking substitutability — this is
exactly what Liskov Substitution asks for.

### What can and cannot be overridden

| Parent member | Can it be overridden? | Why |
|---|---|---|
| `public` instance method | ✅ yes | The normal case |
| `protected` instance method | ✅ yes | Visible to subclasses |
| package-private instance method | ✅ yes, **only within the same package** | Otherwise it is not inherited |
| `private` instance method | ❌ **no** | Not inherited at all — the subclass method is a brand-new method |
| `static` method | ❌ **no** — it is **hidden** | Static methods are not polymorphic |
| `final` instance method | ❌ **no** | `final` is exactly the block |
| `final` static method | ❌ **no** — cannot be overridden or hidden | — |
| Constructor | ❌ **no** | Constructors are not inherited |
| Abstract method | ✅ **must** be | The whole point of an abstract method |

**The three classic answers:** *you cannot override a `private`, `static` or `final` method.*
Nothing else is on the list. A `private` method in the parent is not merely un-overridable — it is
invisible to the child, so the child's same-named method is an unrelated method.

### The constructor chain in a hierarchy

```
new C()  →  C()  →  super()  →  B()  →  super()  →  A()  →  super()  →  Object()
```

| Fact | Detail |
|---|---|
| Order | Always **top-down**: the topmost ancestor's constructor body runs first |
| The implicit `super()` | Inserted as the first statement of every constructor unless an explicit `super(...)` or `this(...)` exists |
| `this(...)` | Chaining inside the same class — it must be the first statement, and it eventually reaches a `super(...)` |
| Parent constructor access | `protected` is enough for a subclass in another package; `private` is **not** enough |

## Quick rules

- Java = **single class inheritance**, **multiple interface implementation**.
- `super` = the **immediate** parent only. Illegal in a static method.
- Static → compile-time binding, resolved by the **declared type**. Instance → run-time binding,
  resolved by the **runtime class**.
- Static methods are **hidden**, never overridden. `final` methods cannot be overridden.
- Overriding needs: same name, same parameters, parent method visible and non-`static`,
  non-`final`.
- An override may **widen** access and **narrow** the return type (covariant), but may not add
  new checked exceptions.
- A concrete subclass **must** implement every inherited abstract method, or be declared abstract.
- The constructor chain runs **top-down** — `Object()` first.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "Static methods are overridden" | Yes | They are **hidden** |
| "A private method can be overridden" | Yes | It is not inherited — the child's method is new |
| "A final method can be overridden" | Yes | `final` blocks it |
| "Overriding uses the variable's type" | `Parent.i` for `p.i()` | Overriding uses the **runtime class** |
| "Hiding uses the runtime class" | `Child.s` for `p.s()` | Hiding uses the **declared type** |
| "An abstract class must have an abstract method" | True | It may have **zero** abstract methods |
| "`super` can reach the grandparent" | Yes | Only **one** level |
| "A covariant return type is illegal in an override" | Compile error | Narrowing the return type is **legal** |

## Checklist

- [ ] I can state the single-inheritance rule in one line.
- [ ] I can predict the output of `Parent p = new Child(); p.s(); p.i();`.
- [ ] I can name the three method types that cannot be overridden.
- [ ] I can write the 6-step method resolution order.
- [ ] I know a `default` interface method is the **last** resort in that order.
- [ ] I know the constructor chain runs top-down.

## Related

- [Casts, type checks and ClassCastException](02-casts-type-checks-and-errors.md)
- [Abstract, final and the constructor chain](03-abstract-final-and-the-constructor-chain.md)
- [The method resolution procedure](../02-techniques/01-method-resolution-order.md)
- [Override vs hide triage](../02-techniques/02-override-vs-hide-triage.md)
- [8 solved inheritance questions](../03-worked-examples/01-solved-inheritance-questions.md)
- [Inheritance traps](../04-pitfalls/01-inheritance-traps.md)
- [Inheritance one-pager](../05-reference/01-inheritance-one-pager.md)
- [Topic overview](../README.md)
