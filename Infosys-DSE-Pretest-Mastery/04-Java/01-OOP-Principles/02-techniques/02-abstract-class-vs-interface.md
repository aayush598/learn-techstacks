# Abstract Class vs Interface — the Decision Table

> Section 4 · Java · OOP Principles · _Estimated reading time: 8 min_
> **Prerequisite:** [The four pillars](../01-concepts/01-the-four-pillars.md)

## In one sentence

Use an **abstract class** when the subclasses share state and a constructor chain, and an
**interface** when you need a behaviour contract that unrelated classes can implement.

## Why the pre-test tests this

- "Which of the following is TRUE about an interface?" and "Can a class extend more than one
  class?" are recurring 1-mark questions with very specific answers.
- The "compile or not" archetype needs one fact: **a class extends at most one class, but
  implements any number of interfaces.**
- The abstract-class-vs-interface comparison is also the base of the whole Interfaces topic.

## Core concept

### The comparison table

| Dimension | **Abstract class** | **Interface** (Java 8) |
|---|---|---|
| Keyword | `abstract class` | `interface` |
| What it is | A **partially implemented** class | A **contract** of behaviours |
| Extends / implements | `extends` **one** abstract class | `implements` **any number** of interfaces |
| Can extend another class? | ✅ | ❌ (interfaces cannot extend classes) |
| Can extend/implement another interface? | ✅ (implements) | ✅ (extends) |
| Fields | Any — instance, static, final | **All fields are implicitly `public static final`** |
| Constructors | ✅ yes | ❌ **no constructors at all** |
| Instance initialiser blocks | ✅ | ❌ |
| Methods | Abstract, concrete, static, final, private, protected, public | Abstract, `default`, `static`, `private` (Java 9), `public` |
| Method body required | Only for non-abstract methods | Not for abstract / `default` methods (Java 8+ allows `default`) |
| Access on members | Any modifier | Interface methods are `public` by default |
| Instantiation | ❌ cannot `new` an abstract class | ❌ cannot `new` an interface |
| `this` / `super` | ✅ both available | ❌ no `super` (no parent class) |
| Best for | Shared state, constructor chaining, "is-a" hierarchy | Capability contracts across unrelated hierarchies |

### The three hard rules

| Rule | Statement | Why |
|---|---|---|
| 1 | A class can `extends` **at most one** class, and `implements` **any number** of interfaces | Java has single class inheritance but multiple interface implementation |
| 2 | A `default` method in an interface **cannot override** an inherited concrete method from a superclass | The class always wins — "class wins" rule |
| 3 | Interface fields are **implicitly `public static final`** | You cannot declare a non-final instance field in an interface |

### Worked code — what compiles and what does not

```java
interface Printable {
    void print();
}

interface Compressible {
    void compress();
}

abstract class Document implements Printable {
    protected String title;

    Document(String title) {
        this.title = title;
    }

    public String getTitle() {
        return title;
    }
}

class Pdf extends Document implements Compressible {
    Pdf(String title) { super(title); }

    @Override
    public void print() { System.out.println("Print " + getTitle()); }

    @Override
    public void compress() { System.out.println("Compress"); }
}

public class Main {
    public static void main(String[] args) {
        Pdf p = new Pdf("Q3-Report");
        Printable pr = p;
        pr.print();       // ?
        Compressible c = p;
        c.compress();     // ?
    }
}
```

**This prints exactly:**

```
Print Q3-Report
Compress
```

| Call | Resolution | Why |
|---|---|---|
| `pr.print()` | `Pdf.print()` | `print()` is abstract in `Printable` and implemented in `Pdf`; the runtime type is `Pdf` |
| `c.compress()` | `Pdf.compress()` | Same mechanism through a second interface reference |

**The illegal variants:**

| Illegal code | Error |
|---|---|
| `class C extends Document, Pdf {}` | ❌ "class can only extend one class" — `implements Compressible, Printable` is fine, `extends A, B` is not |
| `interface I extends Pdf {}` | ❌ "bad type in extends clause" — an interface cannot extend a class |
| `new Document("x")` | ❌ "Document is abstract; cannot be instantiated" |
| `interface I { int x; }` — legal (implicitly `public static final`). But `interface I { private int x; }` | ❌ "illegal combination of modifiers: private and static" |
| `interface I { private void helper() {} }` — legal in Java 9+, **error in Java 8** | The pre-test runs Java 8: treat private interface methods as unavailable |

### Choosing between them — a 5-question decision procedure

```
1. Do the implementers need to share STATE or a CONSTRUCTOR chain?
        YES → abstract class
        NO  → go to 2

2. Do the implementers come from UNRELATED hierarchies
   (e.g. Pdf, ExcelFile, NetworkPrinter all "can print")?
        YES → interface
        NO  → go to 3

3. Does the type need to be PASSED as a parameter / returned / stored
   in a collection (i.e. used as a contract)?
        YES → interface (you cannot pass an abstract class where
              unrelated implementations must vary)
        NO  → go to 4

4. Do you need inherited CODE (shared default behaviour) that all
   subclasses must run?
        YES → abstract class
        NO  → interface (keep it a pure contract)

5. Default answer in industry: interface first,
   extract an abstract class only when you actually need shared state.
```

### The "class wins" rule, in one snippet

```java
class Parent {
    public void greet() { System.out.println("Parent.greet"); }
}

interface Greeter {
    default void greet() { System.out.println("Greeter.greet"); }
}

class Child extends Parent implements Greeter {
    // inherits Parent.greet AND the default Greeter.greet -> conflict?
    // Java rule: the superclass method wins. No compile error, no @Override needed.
}

public class Main {
    public static void main(String[] args) {
        new Child().greet();   // ?
    }
}
```

**This prints exactly:**

```
Parent.greet
```

The **class wins** over the interface's default method. There is no ambiguity error and no
requirement to override. This is a favourite "predict the output" question.

## Quick rules

- A class extends **one** class and implements **many** interfaces. Both facts are examinable.
- An interface has **no constructors** and **no instance fields**.
- Interface fields are `public static final` — always.
- An abstract class **may** have constructors, concrete methods, and state.
- Interfaces cannot extend classes. Abstract classes can implement interfaces.
- You cannot instantiate an abstract class or an interface.
- **Class wins** over an interface default method — no error, no override needed.
- In Java 8: interface methods are `public abstract`, `default`, or `static`. No `private` interface
  methods (that is Java 9).

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "A class can extend multiple classes" | True/False → True | Single class inheritance only |
| "An interface can have instance variables" | True | Only `public static final` fields |
| "An abstract class cannot have constructors" | True | It can, and needs them for the constructor chain |
| "Interfaces cannot have any method body" | True (Java 8) | `default` and `static` methods have bodies |
| "A class implementing an interface must implement all its methods" | True | It must implement all **abstract** methods; `default` ones are inherited |
| "The default-method conflict is a compile error" | Compile error | The class's inherited method wins — no error |
| "An interface can extend a class" | True | Interfaces extend **interfaces** only |

## Checklist

- [ ] I can recite the "one class, many interfaces" rule.
- [ ] I know interface fields are implicitly `public static final`.
- [ ] I know an abstract class can have constructors, state and concrete methods.
- [ ] I know the "class wins" rule for default methods and can predict its output.
- [ ] I know that in Java 8 there are no private interface methods.
- [ ] I can answer "can an interface extend a class?" in one word: no.

## Related

- [The four pillars](../01-concepts/01-the-four-pillars.md)
- [`this`, `super` and the modifier matrix](../01-concepts/03-this-super-and-modifiers.md)
- [Identifying the pillar behind a code snippet](01-identifying-a-pillar-procedure.md)
- [Interface anatomy](../04-interfaces-abstract-inner-classes/01-concepts/01-interface-anatomy.md)
- [8 solved OOP questions](../03-worked-examples/01-solved-oop-questions.md)
- [OOP principles traps](../04-pitfalls/01-oop-principles-traps.md)
- [OOP principles one-pager](../05-reference/01-oop-principles-one-pager.md)
- [Topic overview](../README.md)
