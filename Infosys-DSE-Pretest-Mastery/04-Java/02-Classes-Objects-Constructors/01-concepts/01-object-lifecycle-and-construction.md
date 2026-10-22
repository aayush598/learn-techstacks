# Object Lifecycle and Construction

> Section 4 · Java · Classes, Objects & Constructors · _Estimated reading time: 10 min_
> **Prerequisite:** none

## In one sentence

A Java object comes into existence in a **fixed order** — superclass constructor, then instance
field initialisers and instance initialiser blocks, then the constructor body — and every stage of
that order is examinable.

## Why the pre-test tests this

- "What is the output of this program?" with a class that has static blocks, instance blocks and
  initialisers is a recurring archetype. Get the order wrong and the answer is wrong.
- "What happens if a class does not declare a constructor?" — the **default constructor** rule is
  a 1-mark question that most candidates get wrong by assuming it always exists.
- "Can a constructor call another constructor?" — the `this()` / `super()` **must be first
  statement** rule decides several compile-or-not questions.

## Core concept

### The default constructor rule

| Situation | What happens |
|---|---|
| A class declares **no** constructor | The compiler generates a **default constructor**: no parameters, body empty except an implicit `super()` |
| A class declares **at least one** constructor | **No default constructor is generated** — `new Foo()` becomes a compile error |
| The default constructor's access | **Same as the class's access modifier**. A `public` class gets a `public` default constructor |

```java
class WithCtor {
    WithCtor(int x) { }
}
new WithCtor();     // ❌ compile error: constructor WithCtor in class WithCtor cannot be applied
                    //    to given types; required: int
```

### Constructor rules

| Rule | Statement |
|---|---|
| Return type | A constructor has **no return type** — not even `void`. `void Foo()` is a *method*, not a constructor |
| Name | Exactly the class name, case-sensitive |
| Body | May be empty, may throw, may call `super()` or `this()` |
| Modifier | Can be `public`, `protected`, `private` or package-private. `static`/`final`/`abstract` are illegal |
| Overloading | ✅ Constructors can be overloaded like methods |
| Inheritance | Constructors are **not inherited**. A subclass constructor always calls some parent constructor |

### Constructor chaining — the `this()` / `super()` rule

| Call | Meaning | Rule |
|---|---|---|
| `super(args)` | Call a constructor of the **immediate parent** | Must be the **first statement** of the constructor |
| `this(args)` | Call **another constructor of the same class** | Must be the **first statement** of the constructor |
| Neither | The compiler inserts `super()` as the first statement | Automatic, always legal if the parent has a no-arg constructor |

**Hard rules:**

1. `this(...)` and `super(...)` cannot both appear in the same constructor. ❌ compile error.
2. `super(...)` must be the **first** statement. Any statement before it → ❌ compile error.
3. `this(...)` must be the **first** statement. Same.
4. If the parent class has **no** no-arg constructor, every subclass constructor must explicitly
   call a parent constructor. ❌ compile error otherwise.

```java
class Parent {
    Parent() { System.out.println("Parent()"); }
}

class Child extends Parent {
    Child() {
        System.out.println("before");   // ❌ error: call to super must be first statement
        super();
    }
}
```

### The full object-creation order

When you write `new Derived()`, the JVM does exactly this, in this order:

| # | Step | Notes |
|---|---|---|
| 1 | **Initialise the class** (if not already) | Static fields + static initialiser blocks, in **textual** order. The **superclass is initialised first** |
| 2 | Allocate memory for the object | Fields get default values (`0`, `null`, `false`) |
| 3 | Run the **superclass constructor chain** | Parent instance field initialisers → parent instance blocks → parent constructor body |
| 4 | Run **this class's** instance field initialisers | In textual order, interleaved with instance blocks |
| 5 | Run this class's **instance initialiser blocks** | In textual order |
| 6 | Run **this constructor's body** | Last |

Key consequences:

- The **superclass constructor runs before the subclass's**.
- **Instance** field initialisers run **before the constructor body** of the same class.
- `static` and instance initialisers are completely independent: statics run once at class load,
  instance ones run once per object.

### Worked code — the complete order

```java
class Base {
    static { System.out.println("Base static block"); }
    { System.out.println("Base instance block"); }
    Base() { System.out.println("Base ctor"); }
}

class Derived extends Base {
    static int counter = 10;
    static { System.out.println("Derived static block"); }
    int value = 20;
    { System.out.println("Derived instance block"); }
    Derived() { super(); System.out.println("Derived ctor"); }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("main start");
        new Derived();
    }
}
```

**This prints exactly:**

```
main start
Base static block
Derived static block
Base instance block
Base ctor
Derived instance block
Derived ctor
```

| Step | Line printed | Why |
|---|---|---|
| 1 | `main start` | `main` runs; `Derived` has not been initialised yet |
| 2 | `Base static block` | Initialising `Derived` first initialises its superclass `Base` |
| 3 | `Derived static block` | Then `Derived`'s own static initialiser (`counter = 10` prints nothing) |
| 4 | `Base instance block` | `Base`'s instance initialisers run, before `Base()`'s body |
| 5 | `Base ctor` | `Base()`'s body — still before any `Derived` instance state |
| 6 | `Derived instance block` | `Derived`'s instance initialisers (`value = 20` prints nothing) |
| 7 | `Derived ctor` | `Derived()`'s body, last |

### Initializer blocks — instance vs static

| | **Instance initialiser block** | **Static initialiser block** |
|---|---|---|
| Syntax | `{ ... }` | `static { ... }` |
| Runs | Once per **object** creation | Once per **class** initialisation |
| When | After the superclass constructor, before this constructor's body | At class load, in textual order with static fields |
| Can use `this` | ✅ yes | ❌ no — "non-static variable this cannot be referenced from a static context" |
| Can use `super` | ✅ yes | ❌ no |
| Can declare `static` members | ❌ no | n/a |

### `final` fields and blank finals

| Declaration | Assignment rule |
|---|---|
| `final int x = 5;` | Assigned at declaration. **Cannot** be reassigned anywhere |
| `final int x;` (**blank final**) | Must be assigned **exactly once**, in **every** constructor, or in an instance initialiser block |
| `static final int X;` | Must be assigned in a `static` initialiser block or at the declaration |

```java
class Config {
    final int retries;      // blank final — instance
    static final String NAME;   // blank final — static

    Config(int retries) {
        this.retries = retries;   // definite assignment: OK
    }

    static {
        NAME = "prod";             // static blank final assigned here
    }
}
```

If a class has **two** constructors and a blank final instance field, **each** constructor must
assign it (or one must delegate to the other with `this(...)`).

### `this` escape — why `this` in a constructor is dangerous

Passing `this` out of a constructor publishes a **partially constructed** object: its superclass
state is set, but its own field initialisers have not all run yet. Another thread that receives
that reference can observe a half-built object.

| Escape form | Risk |
|---|---|
| `registry.add(this)` in the constructor | The registry can see an object with uninitialised fields |
| Starting a thread from the constructor | The thread can race on fields not yet assigned |
| `this` as a parameter to a helper that stores it | Same publication risk |

The fix is the **static factory method** pattern: construct privately, return a fully built
object. Java's own `Integer.valueOf`, `Boolean.valueOf` and `List.of` all do this.

## Quick rules

- Default constructor exists **only if you declare no constructor**.
- A constructor has **no return type**; `void ClassName()` is a method.
- `this(...)` / `super(...)` must be the **first statement**, and you may use **one or the other**,
  never both.
- Order: static (superclass first) → superclass instance state → subclass instance state →
  subclass constructor body.
- Instance blocks run **once per object**; static blocks run **once per class**.
- A blank `final` field must be assigned in **every** constructor.
- `this` must not escape the constructor — use a static factory instead.
- Constructors are **not inherited**; `super()` is always called, explicitly or implicitly.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "Every class gets a default constructor" | Compiles fine | Only if no constructor is declared |
| The default constructor is `public` | Yes | It takes the **class's** access modifier |
| `super()` can appear after other statements | Compiles fine | It must be the **first** statement |
| `this()` and `super()` can both be used | Compiles fine | Never both |
| Instance field initialisers run after the constructor body | Wrong output order | They run **before** the body |
| Static block of the subclass runs before the superclass's | Wrong output order | The **superclass** initialises first |
| A `final` field can be changed once already | Legal | `final` = exactly one assignment |
| A blank `final` needs assigning in only one constructor | Compiles fine | **Every** constructor |

## Checklist

- [ ] I can state the default-constructor rule in one sentence.
- [ ] I can write the 7-step object-creation order from memory.
- [ ] I can predict the output of the static/instance-block example above.
- [ ] I know `this(...)` and `super(...)` are mutually exclusive and must be first.
- [ ] I know a blank final must be assigned in every constructor.
- [ ] I can explain what "this escape" means in one sentence.

## Related

- [Object creation, copying and identity](02-object-creation-copying-and-identity.md)
- [Constructor rules and compile errors](../02-techniques/01-constructor-rules-and-compile-errors.md)
- [Creation patterns: singleton, immutable, factory, builder](../02-techniques/02-creation-patterns.md)
- [8 solved construction questions](../03-worked-examples/01-solved-construction-questions.md)
- [Construction traps](../04-pitfalls/01-construction-and-object-traps.md)
- [Construction one-pager](../05-reference/01-construction-one-pager.md)
- [Topic overview](../README.md)
