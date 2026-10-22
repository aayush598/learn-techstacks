# The Method Resolution Procedure

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 8 min_
> **Prerequisite:** [Inheritance basics and dynamic dispatch](../01-concepts/01-inheritance-basics-and-dispatch.md)

## In one sentence

Every "what does this print?" question with inheritance in it is answered by **one 6-step
procedure**, and the whole procedure fits in 40 seconds.

## Why the pre-test tests this

- The output-prediction archetype is the highest-value archetype in the 25-question Java section.
- Inheritance is the most common source of output-prediction questions because it adds a second
  class to the snippet and therefore two chances to get the order wrong.
- Karthik's retrospective advice from the last attempt: *"I read the code twice. I should have read
  the hierarchy once."*

## Core concept

### The procedure

For a call `ref.m(args)`:

| Step | Question | If the answer is... |
|---|---|---|
| **1. Static type** | What is the **declared** type of `ref`? | Write it down. It decides *accessibility* and, for static methods, *which* method runs |
| **2. Existence** | Does that type (or a supertype) declare an applicable, accessible `m`? | If no → ❌ **compile error**. Stop here |
| **3. Static or instance?** | Is `m` declared `static`? | If yes → **bind now**. Go to the hiding rules |
| **4. Runtime class** | What is the **runtime class** of the object `ref` points to? | Write it down. This is the search start |
| **5. Walk up** | Does the runtime class declare `m`? If not, its superclass? Then up to `Object`? | The **first** (most derived) implementation found wins |
| **6. Interface default** | If no superclass implements `m`, does an implemented interface supply a `default` `m`? | If yes → the default runs. If no → the class would have to be abstract |

**Step 3 is the fork.** Everything after it depends on whether the method is static.

### Worked example 1 — an instance method (dynamic dispatch)

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

| Step | Finding |
|---|---|
| 1–2 | Declared type `Animal`; `Animal` declares `speak()` → accessible → OK |
| 3–4 | Instance method; runtime class = `Puppy` |
| 5 | `Puppy` declares `speak()` → **most derived wins** |

**Output:**

```
Puppy
```

### Worked example 2 — a static method (compile-time binding)

```java
class Animal {
    static void info() { System.out.println("Animal"); }
}
class Dog extends Animal {
    static void info() { System.out.println("Dog"); }
}

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        a.info();
    }
}
```

Step 3 fires: `info()` is **static** → bind now to the declaring class → `Animal.info`. The runtime
class `Dog` is irrelevant; `Dog.info()` **hides** `Animal.info()`.

**Output:**

```
Animal
```

### Worked example 3 — no override in the runtime class

```java
class Animal {
    void speak() { System.out.println("Animal"); }
}
class Dog extends Animal { }          // no override

public class Main {
    public static void main(String[] args) {
        Animal a = new Dog();
        a.speak();
    }
}
```

Step 4: runtime class is `Dog`. Step 5: `Dog` does **not** declare `speak()`, so the search moves
up to `Animal`, which provides it.

**Output:**

```
Animal
```

### Worked example 4 — the interface `default` as the last resort

```java
interface Greeter {
    default void greet() { System.out.println("Greeter.greet"); }
}
class Silent implements Greeter { }     // does not override

public class Main {
    public static void main(String[] args) {
        Greeter g = new Silent();
        g.greet();
    }
}
```

| Step | Finding |
|---|---|
| 4 | Runtime class = `Silent` |
| 5 | `Silent` → `Object`: no `greet()` anywhere in the class chain |
| 6 | `Greeter` supplies the `default` → it runs |

**Output:**

```
Greeter.greet
```

### Worked example 5 — "class wins" over a default method

```java
class Base {
    public void greet() { System.out.println("Base.greet"); }
}
interface Greeter {
    default void greet() { System.out.println("Greeter.greet"); }
}
class Child extends Base implements Greeter { }

public class Main {
    public static void main(String[] args) {
        Greeter g = new Child();
        g.greet();
    }
}
```

| Step | Finding |
|---|---|
| 4 | Runtime class = `Child` |
| 5 | `Child` → `Base` → `Base.greet()` found — a **class** implementation |

**Output:**

```
Base.greet
```

A concrete method inherited from a class always beats a `default` method inherited from an
interface. **No compile error, no ambiguity, no override required.**

### The decision table for "which method runs?"

| The method is... | The **declared** type declares it? | The runtime class overrides it? | The method that runs |
|---|---|---|---|
| Instance | Yes | Yes, in the runtime class | The runtime class's version |
| Instance | Yes | Yes, in an intermediate class | The most derived version found walking up |
| Instance | Yes | No, anywhere in the class chain | The superclass's version (or an interface default) |
| Static | Yes | n/a | The declaring class's version — **declared type wins** |
| Static | Yes, but the subclass declares a same-named static | n/a | The **declared** type's version — the subclass's version is only reached if the reference's type is the subclass |

### The 45-second budget

| Phase | Seconds | Action |
|---|---|---|
| Read the snippet | 15 | Find the reference's declared type and the object's construction |
| Step 1–2 | 5 | Static type, then existence |
| Step 3 | 2 | Static or instance? |
| Step 4–6 | 15 | Runtime class, walk up, interface default |
| Match the option | 8 | Pick |
| **Total** | **~45** | Comfortable inside the 90-second rule |

## Worked example

**Q. What does the following program print?**

```java
class Base {
    static void show() { System.out.println("Base static"); }
    void run() { System.out.println("Base run"); }
}

interface Runner {
    default void run() { System.out.println("Runner run"); }
}

class Child extends Base implements Runner {
    static void show() { System.out.println("Child static"); }
    @Override void run() { System.out.println("Child run"); }
}

public class Main {
    public static void main(String[] args) {
        Base b = new Child();
        b.show();
        b.run();

        Runner r = (Runner) b;
        r.run();
    }
}
```

A. `Base static`, `Child run`, `Child run`
B. `Child static`, `Child run`, `Child run`
C. `Base static`, `Base run`, `Runner run`
D. `Child static`, `Child run`, `Runner run`

**Solution**

| Call | Step 1 | Step 3 | Step 4–5 | Method that runs |
|---|---|---|---|---|
| `b.show()` | `Base` | **static** → bind now to `Base` | — | `Base.show` → `Base static` |
| `b.run()` | `Base` | instance | runtime class `Child` declares `run()` | `Child.run` → `Child run` |
| `r.run()` | `Runner` | instance | runtime class `Child` declares `run()` | `Child.run` → `Child run` |

Note that `Runner.run()`'s default never runs: the runtime class overrides `run()` with a
concrete method.

**Answer: A.** Output is:

```
Base static
Child run
Child run
```

**Distractors**

| Option | Why it is wrong |
|---|---|
| B | Thinks the static call dispatches on the runtime class — static methods never do |
| C | Thinks the default method wins over the class's concrete method — **class wins** |
| D | Same static mistake as B |

## Quick rules

- Step 1: **declared** type decides accessibility and static binding.
- Step 3 is the fork: `static` → bind now; instance → bind at run time.
- Walking up the hierarchy, the **most derived** implementation wins.
- A `default` interface method is the **last** resort, not the first.
- **Class wins** over interface default — silently.
- The runtime class is what matters for instance methods, and the declared type for static ones.
- If no implementation is found anywhere, the class must be abstract.

## Common traps

| Trap | Symptom | Fix |
|---|---|---|
| Starting the search at the declared type | Printing the parent's method | Start at the **runtime class** |
| Starting the search at the runtime class for a static call | Printing the child's method | Static binds to the **declared** type |
| Thinking a default method beats a superclass method | Printing `Runner run` | Class wins |
| Forgetting to check intermediate classes | Wrong answer | Walk **up** the chain, not just one level |
| Checking "does the runtime class have it?" and stopping | Wrong answer | Keep walking up |
| Applying the instance rules to a static call | Wrong answer | Step 3 first, always |

## Checklist

- [ ] I can state the 6 steps in order without looking.
- [ ] I can predict the output of all 5 worked examples above.
- [ ] I know which step is the fork between static and instance behaviour.
- [ ] I know the default method is the last resort.
- [ ] I can explain "class wins" in one sentence.
- [ ] I finished the worked example inside 45 seconds.

## Related

- [Inheritance basics and dynamic dispatch](../01-concepts/01-inheritance-basics-and-dispatch.md)
- [Abstract, final and the constructor chain](../01-concepts/03-abstract-final-and-the-constructor-chain.md)
- [Override vs hide triage](02-override-vs-hide-triage.md)
- [8 solved inheritance questions](../03-worked-examples/01-solved-inheritance-questions.md)
- [Inheritance traps](../04-pitfalls/01-inheritance-traps.md)
- [Inheritance one-pager](../05-reference/01-inheritance-one-pager.md)
- [Topic overview](../README.md)
