# Constructor Rules and Compile Errors

> Section 4 · Java · Classes, Objects & Constructors · _Estimated reading time: 8 min_
> **Prerequisite:** [Object lifecycle and construction](../01-concepts/01-object-lifecycle-and-construction.md)

## In one sentence

Every constructor compile-error question is answered by **three rules** — first-statement
placement, mutual exclusivity, and definite assignment of blank finals — and nothing else.

## Why the pre-test tests this

- The Java section asks "does this compile?" more than any other archetype. Roughly a third of
  those questions are decided by constructor rules.
- A compile-error question is binary: either the code is legal or it is not. There is no partial
  credit and no "probably compiles".
- Reading a snippet for these three rules takes 30 seconds once you know them.

## Core concept

### The three rules

| # | Rule | Violation → |
|---|---|---|
| **R1** | `this(...)` and `super(...)` must be the **first statement** of the constructor | ❌ "call to super must be first statement in constructor" |
| **R2** | You may use `this(...)` **or** `super(...)`, **never both** | ❌ "call to super must be first statement in constructor" |
| **R3** | A **blank final** field must be assigned exactly once in **every** constructor (or in an instance initialiser block) | ❌ "variable x might not have been initialized" / "might already have been assigned" |

### The 6-step constructor scan

Run these in order on any constructor snippet:

```
1. Does the constructor have a RETURN TYPE?
       yes → it is a METHOD, not a constructor (and it will not be
             invoked by `new`)      → keep reading, but note the trick

2. Does the constructor body contain `this(...)` or `super(...)`?
       no  → the compiler inserts `super()` automatically → legal
            → now check R3 (blank finals)

3. If it DOES contain one, is it the FIRST statement?
       no  → ❌ COMPILE ERROR (R1)

4. Does it contain BOTH `this(...)` and `super(...)`?
       yes → ❌ COMPILE ERROR (R2)

5. Does the parent class have a no-arg constructor (or is a super-call explicit)?
       no  → ❌ COMPILE ERROR: no suitable superclass constructor

6. Are all blank final fields assigned on every path through this constructor?
       no  → ❌ COMPILE ERROR (R3)
```

### Worked code — legal vs illegal

```java
class Parent {
    Parent() { }                 // no-arg parent constructor exists
}

class Child extends Parent {
    final int id;
    final String label;

    Child() {
        this(0, "default");      // ✅ legal: `this(...)` is the first statement
    }

    Child(int id, String label) {
        this.id = id;            // ✅ blank finals assigned here
        this.label = label;
    }
}
```

**Legal.** `Child()` delegates to `Child(int, String)` via `this(...)`, which is the first
statement. The blank finals are assigned in the delegating target, which satisfies definite
assignment for both constructors.

### The five illegal variants — and why each fails

| # | Illegal snippet | Fails because |
|---|---|---|
| 1 | `Child() { int x = 1; super(); }` | `super()` is not the first statement → **R1** |
| 2 | `Child() { this(1); super(); }` | Both `this(...)` and `super(...)` → **R2** |
| 3 | `Child() { super(); this(1); }` | `this(...)` is not the first statement → **R1** |
| 4 | `class Child extends Parent { final int id; Child() { } }` with `Parent` having **only** `Parent(int n)` | No no-arg parent constructor and no explicit `super(...)` → step 5 |
| 5 | `class C { final int a; final int b; C() { a = 1; } }` | `b` is never assigned → **R3** (and if assigned twice → "might already have been assigned") |

### Fixing each illegal variant

| Illegal | Fix |
|---|---|
| `super()` after a statement | Move `super()` to the top, or move the statement into a helper called after `super()` |
| Both `this()` and `super()` | Keep `this(...)` (it will chain to `super()` eventually), or keep `super()` and drop `this(...)` |
| Blank final not assigned | Assign it in the constructor, in an initialiser block, or give the field an initial value |
| Blank final assigned twice | Remove one assignment; a blank final takes exactly one |

### Initializer-block ordering — the printing recipe

When a question shows a class with static blocks, instance blocks and initialised fields, answer
it with this fixed template:

```
STATIC PHASE  (once, at class initialisation)
  superclass static fields + static blocks      ← superclass FIRST
  then this class's static fields + static blocks, in TEXTUAL order

OBJECT PHASE  (per `new`)
  1. superclass: instance fields + instance blocks (textual order)
  2. superclass constructor body
  3. this class: instance fields + instance blocks (textual order)
  4. this constructor body
```

Two rules candidates forget:

| Forgotten rule | Symptom |
|---|---|
| **Static and instance initialisers are independent** | Predicting the static block in the middle of object creation |
| **Textual order** among fields and blocks of the same kind | Predicting fields before blocks when the code has them the other way round |

### The 60-second budget

| Phase | Seconds | Action |
|---|---|---|
| Read the snippet | 15 | Find the constructors, the blocks and the field initialisers |
| Run the 6-step scan | 20 | Constructor legality |
| Run the ordering template | 15 | Output prediction |
| Match the option | 10 | Pick the answer |
| **Total** | **~60** | Inside the 90-second rule |

## Worked example

**Q. Does the following code compile?**

```java
class Base {
    Base(int x) { System.out.println(x); }
}

class Derived extends Base {
    final int value;

    Derived() {
        value = 10;
        super(value);
    }
}
```

A. Yes, it compiles and prints `10`.
B. No — `super()` must be the first statement in the constructor.
C. No — `value` is final and cannot be assigned.
D. No — `Base` has no no-arg constructor.

**Solution**

Apply the 6-step scan:

| Step | Finding |
|---|---|
| 1 | `Derived()` has no return type → it is a constructor ✅ |
| 2 | It contains `super(value)` → no implicit `super()` is inserted |
| 3 | `super(value)` is **not** the first statement — `value = 10;` comes first → **R1 violated** |

**Answer: B.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | The implicit `super()` insertion does **not** happen when an explicit `super(...)` is present, and that explicit call must be first. The code does not compile |
| C | Assigning a `final` field once in a constructor is exactly what a blank final requires — that part is fine |
| D | The problem is not the missing no-arg constructor; `super(value)` explicitly passes a value. The problem is the statement order |

**Fix:** swap the two lines.

```java
Derived() {
    super(10);
    value = 10;
}
```

**Note:** the fixed version prints `10`. `super(10)` runs `Base(10)`, which prints `10`, and then
`value = 10` assigns the field.

## Quick rules

- `this(...)` / `super(...)`: first statement, and one or the other.
- No explicit call → the compiler inserts `super()` at the top.
- A blank final must be assigned on **every** path of **every** constructor.
- `final` fields are assigned once — that is legal, not an error.
- Constructor has no return type; `void ClassName()` is a method.
- Static phase: superclass first, textual order. Object phase: superclass state, then subclass
  state, then the constructor body.
- Static and instance initialisers never interleave.
- If the parent has no no-arg constructor, every subclass constructor needs an explicit
  `super(...)`.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| Implicit `super()` inserted even when an explicit call exists | "Compiles fine" | The explicit call replaces the implicit one — and must be first |
| Assigning a `final` field is illegal | "Compile error" | One assignment is exactly right for a blank final |
| Both `this()` and `super()` is fine | "Compiles" | Mutually exclusive |
| Superclass static block runs after the subclass's | Wrong output order | Superclass initialises **first** |
| Instance blocks run after the constructor body | Wrong output order | Before the body |
| Static and instance blocks interleave | Wrong output order | Separate phases |
| A blank final assigned in only one of two constructors | "Compiles" | **Every** constructor |

## Checklist

- [ ] I can recite the 6-step constructor scan.
- [ ] I can name the exact error for each of the 5 illegal variants.
- [ ] I can write the static-phase and object-phase ordering templates from memory.
- [ ] I know that an explicit `super(...)` suppresses the implicit one.
- [ ] I know a blank final needs assignment in every constructor.
- [ ] I can fix the worked example by swapping two lines and say what it prints.

## Related

- [Object lifecycle and construction](../01-concepts/01-object-lifecycle-and-construction.md)
- [Object creation, copying and identity](../01-concepts/02-object-creation-copying-and-identity.md)
- [Creation patterns: singleton, immutable, factory, builder](02-creation-patterns.md)
- [8 solved construction questions](../03-worked-examples/01-solved-construction-questions.md)
- [Construction traps](../04-pitfalls/01-construction-and-object-traps.md)
- [Construction one-pager](../05-reference/01-construction-one-pager.md)
- [Topic overview](../README.md)
