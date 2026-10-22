# Static, Final, and Class Initialisation

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 11 min_
> **Prerequisite:** none

## In one sentence

`static` belongs to the **class** and runs **once, in textual order, when the class is first used**;
`final` means "cannot be reassigned" — and only a `final` primitive/`String` with a constant
initialiser is a **compile-time constant**.

## Why the pre-test tests this

- "What is the output?" questions with a `static` block are a staple: the answer depends on
  *when* the class is initialised, not on where the block appears.
- "Which of these is a compile-time constant?" is a standard MCQ with one defensible answer.
- `final`, `static final`, and constant folding show up in the `==` and string-pool questions too.

## Core concept

### `static` — what it changes

| Aspect | `static` member | Instance member |
|---|---|---|
| Belongs to | the **class** | each **object** |
| Copies | exactly **one** per class | one per object |
| Access | `ClassName.member` | `object.member` |
| Can be called without an object | ✅ | ❌ |
| Can use `this` / `super` | ❌ | ✅ |
| Can be overridden | ❌ — only **hidden** | ✅ |
| Belongs to the instance lifecycle | ❌ | ✅ |

```java
class Counter {
    static int total = 0;      // one copy for the whole class
    int perObject = 0;
}
```

**What a `static` method may not do:** reference `this`, call `super()`, or touch an instance field
or instance method. Doing so is a compile error:

```
error: non-static variable this cannot be referenced from a static context
```

### Class initialisation order

When a class is **first actively used** (created, or a static member accessed), the JVM:

1. Initialises the **superclass** first (recursively).
2. Runs the class's static field initialisers and static blocks **in textual order**.
3. The class is then "initialised" and stays that way.

```java
class A {
    static int x = 10;
    static { x += 5; }        // 2nd
    static int y = x * 2;     // 3rd
}
```

| Step | Statement | `x` | `y` |
|---|---|---|---|
| 1 | `static int x = 10;` | 10 | — |
| 2 | `static { x += 5; }` | 15 | — |
| 3 | `static int y = x * 2;` | 15 | 30 |

So `x` is 15 and `y` is 30. The static block sees the value of `x` **at that point in the source
order**, not the final value.

**The instance side**, for contrast: instance field initialisers and instance blocks run **in
textual order**, at `new` time, immediately **before** the constructor body and **after** the
parent constructor.

### `final` — the four flavours

| Flavour | Rule | Compile error if broken |
|---|---|---|
| `final` local / field | the **reference or value** cannot be reassigned | `cannot assign a value to final variable x` |
| `final` parameter | the parameter cannot be reassigned | `cannot assign a value to final parameter x` |
| `final` method | cannot be overridden | `m() in B cannot override m() in A; overriding method is final` |
| `final` class | cannot be extended | `cannot subclass final class A` |

**Important:** `final` freezes the *reference*, not the *object*.

```java
final int[] a = {1, 2, 3};
a[0] = 99;        // legal — the array's contents changed
a = new int[5];   // compile error — the reference cannot change
```

### Compile-time constants

A variable is a **constant variable** when **all three** hold:

1. it is declared `final`,
2. its type is a primitive or `String`,
3. it is initialised with a **constant expression** (literals, other constant variables, and `+`
   between them).

```java
final int A = 10;              // constant variable
final int B = A * 2;           // constant variable (20)
final String S = "Hi";         // constant variable
final String T = S + "!";      // constant variable ("Hi!")
final int C = aMethod();       // NOT a constant — a method call is not a constant expression
final int D = 5;  final int E = D + 1;   // constant
```

Constant variables are **inlined at compile time**. So `final int A = 10;` does not create a
storage slot — the literal `10` is substituted at every use site. That is why `A` can be used in a
`case` label of a `switch` and why `"x" + A` is a compile-time constant expression (and therefore
pooled).

### Blank finals and effectively final

| Concept | Meaning |
|---|---|
| **Blank final** | `final int x;` with no initialiser. It must be assigned **exactly once**, in the constructor or an initialiser block. If the class defines no constructor, the compiler generates one and the field must be initialised inline or it is a compile error. |
| **Effectively final** | A **local** variable that is never reassigned. It may be captured by a lambda or an anonymous class even without the `final` keyword (Java 8+). |

```java
int count = 0;              // effectively final
Runnable r = () -> System.out.println(count);   // legal in Java 8
count = 5;                  // now it is NOT effectively final → the lambda no longer compiles
```

### `static final` — the constant

```java
class Config {
    static final int MAX = 100;
    static final String NAME = "prod";
}
```

- `static` → one copy for the class.
- `final` → cannot be reassigned.
- With a constant initialiser → a **compile-time constant**, inlined everywhere.

Without `static`, `final int MAX = 100;` is one constant per **object** — a common mistake.

### `static` imports

```java
import static java.lang.Math.max;      // call max(a, b) directly
import static java.lang.Math.*;         // discouraged
```

Legal, and it appears occasionally as "what does this import do?".

## Worked example

**Q. What is printed?**

```java
class A {
    static int x = 10;
    static { x += 5; }
    static int y = x * 2;
    int z = y;
}
public class Main {
    public static void main(String[] args) {
        System.out.println(A.y);
        A a = new A();
        System.out.println(a.z);
        System.out.println(A.x);
    }
}
```

**Solution**

| Step | Event | Value |
|---|---|---|
| 1 | `A` is initialised on first use: `static int x = 10;` | `x = 10` |
| 2 | `static { x += 5; }` | `x = 15` |
| 3 | `static int y = x * 2;` | `y = 30` |
| 4 | `println(A.y)` | prints `30` |
| 5 | `new A()` → instance initialiser `int z = y;` | `z = 30` |
| 6 | `println(a.z)` | prints `30` |
| 7 | `println(A.x)` | prints `15` |

**Output (exact):**

```
30
30
15
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `20` then `30` then `15` | `y` is initialised **after** the static block, so it sees `x = 15` |
| `30` then `30` then `20` | the static block ran before `y` was initialised, so `x` ends at 15, not 20 |
| `30` then `30` then `30` | `x` is 15 at the end; `y` is 30 |

## Quick rules

- `static` = one copy per class; instance = one per object.
- Static initialisation happens **at first use**, not at program start, and **superclass first**.
- Static field initialisers and static blocks run in **textual order**, interleaved.
- Instance initialisers and instance blocks run in **textual order**, at `new` time, after the parent
  constructor.
- A `static` method cannot use `this`, `super()`, or any instance member.
- `final` freezes the reference, not the object's contents.
- Constant variable = `final` + primitive/`String` + constant-expression initialiser.
- Constant variables are inlined at compile time.
- Effectively final local variables can be captured by lambdas (Java 8+).

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| "Static blocks run when the program starts" | statics first | They run at **first use** of the class |
| "Static block sees the final value of `x`" | 20 | It sees the value at that point in source order |
| "`final` makes the object immutable" | contents frozen | Only the reference is frozen |
| "A `final` field needs no initialiser" | compiles | Blank final must be assigned exactly once |
| "`static final int` is one per object" | per object | `static` makes it one per class |

## Checklist

- [ ] I can state the class-initialisation order in one sentence.
- [ ] I know the three conditions for a compile-time constant.
- [ ] I know that `final` freezes the reference, not the object.
- [ ] I know a `static` method cannot use `this` or instance members.
- [ ] I know what "effectively final" means and why it matters in Java 8.

## Related

- [Varargs and wrapper types](02-varargs-and-wrapper-types.md)
- [Operator precedence and arithmetic](03-operator-precedence-and-arithmetic.md)
- [Decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)
- [Solved static/final/varargs set](../03-worked-examples/01-solved-static-final-varargs-set.md)
- [Static/final/varargs traps](../04-pitfalls/01-static-final-varargs-traps.md)
- [Static/final/varargs one-pager](../05-reference/01-static-final-varargs-one-pager.md)
- [Topic overview](../README.md)
