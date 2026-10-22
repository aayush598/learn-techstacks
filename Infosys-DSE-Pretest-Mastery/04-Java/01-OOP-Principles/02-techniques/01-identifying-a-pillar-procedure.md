# Identifying the Pillar Behind a Code Snippet

> Section 4 · Java · OOP Principles · _Estimated reading time: 8 min_
> **Prerequisite:** [The four pillars](../01-concepts/01-the-four-pillars.md)

## In one sentence

Every "which OOP principle does this code show?" question is answered by **four yes/no checks in a
fixed order**, and you can finish inside the 90-second rule.

## Why the pre-test tests this

- "Which OOP concept is demonstrated by the following code?" is a recurring 1-mark archetype in the
  Java section — the code is 6 lines, the answer is 1 word.
- The trap is that most snippets demonstrate **two** pillars, so you must pick the one the question
  is *pointing at*.
- The procedure below gives you a deterministic order of inspection instead of a feeling.

## Core concept

### The 4-check procedure

Run these checks **in order**. The first one that matches is almost always the intended answer.

| # | Check | If YES → the pillar is |
|---|---|---|
| 1 | Is the code **hiding state** behind `private` fields + getters/setters? | **Encapsulation** |
| 2 | Is the code **declaring** a contract with an `abstract`/`interface` and **not** providing the body? | **Abstraction** |
| 3 | Does one class **extend/implement** another to reuse or specialise? | **Inheritance** |
| 4 | Does one reference produce **different behaviours** at run time (an overridden method) or compile time (an overload)? | **Polymorphism** |

### Tie-break table — when two checks both match

| Snippet feature | The pillar the question wants | Why the other one is not the answer |
|---|---|---|
| `private int id;` + `getId()` | **Encapsulation** | The `private` keyword is the tell. Abstraction would need an unimplemented method |
| `interface Shape { double area(); }` | **Abstraction** | No data hiding is happening |
| `class Circle implements Shape` | **Inheritance** (implementation) | Unless the question asks "which mechanism lets `Circle` be used as a `Shape`" → then it is **polymorphism** |
| `abstract class Animal { abstract void sound(); }` | **Abstraction** | The keyword `abstract` is the tell |
| `void print(int x)` and `void print(String s)` | **Polymorphism** (compile-time / overloading) | No inheritance involved |
| `Parent p = new Child(); p.display();` | **Polymorphism** (run-time / overriding) | The `extends` is there, but the *observable* behaviour is polymorphic |
| `class Employee { private double salary; public void raise() {...} }` | **Encapsulation** | Nothing abstract, nothing inherited |

### A 20-second scan of a snippet

```
1. Do I see `private` + getters/setters?          → Encapsulation
2. Do I see an unimplemented method or interface? → Abstraction
3. Do I see `extends` / `implements`?             → Inheritance
4. Do I see the SAME method name twice?           → Overloading  → Polymorphism (compile-time)
5. Do I see a subclass redefining a parent's method? → Overriding → Polymorphism (run-time)
```

If two ticks fire, pick the **later** one only if the question says "demonstrated by"; pick the
**earlier** one if the question says "used to hide" or "primary purpose".

### The "NOT an OOP principle" quick-kill list

When the stem is negative, you do not need the positive analysis. Just scan the options for
anything in this list — it is nearly always the answer:

| Kill-list option | Why it is not a pillar |
|---|---|
| **Compilation / compiling** | A build step performed by `javac`, not a design principle |
| **Optimization** | A non-functional goal; OOP is about structure, not speed |
| **Parallelism / concurrency** | An execution model, orthogonal to OOP |
| **Serialization** | A library feature in `java.io` |
| **Modularity** | A genuine OOP *feature*, but not one of the four pillars — a weak option; prefer compilation/optimization if present |

**Trap:** some papers phrase it as *"Which of the following is NOT a feature of OOP?"* and offer
**Compilation**, **Abstraction**, **Encapsulation**, **Inheritance**. Compilation is the answer.
If the options offer **Polymorphism** instead of one of the pillars, the answer is whichever
non-pillar option is present.

### 60-second budget for a pillar question

| Phase | Seconds | Action |
|---|---|---|
| Read the stem | 10 | Decide: positive ("which principle") or negative ("which is NOT") |
| Scan the code | 20 | Apply checks 1–4 in order |
| Scan the options | 15 | If negative: look for a kill-list word. If positive: match the check that fired |
| Verify | 10 | Say the answer aloud as a sentence — if you cannot, guess |
| **Total** | **~55** | Comfortably inside 90 seconds |

## Worked example

**Q. Which OOP principle is primarily demonstrated by the following code?**

```java
abstract class Vehicle {
    protected String registrationNumber;

    Vehicle(String registrationNumber) {
        this.registrationNumber = registrationNumber;
    }

    abstract int getNumberOfWheels();

    public String getRegistrationNumber() {
        return registrationNumber;
    }
}

class Bike extends Vehicle {
    Bike(String reg) { super(reg); }

    @Override
    int getNumberOfWheels() { return 2; }
}
```

A. Encapsulation
B. Abstraction
C. Polymorphism
D. Inheritance

**Solution**

| Check | Result |
|---|---|
| 1. Hiding state behind `private` + getters? | No — the field is `protected`, and there is no data-hiding scheme. Not encapsulation |
| 2. An unimplemented method / contract? | **Yes** — `abstract int getNumberOfWheels();` has no body, and `Vehicle` cannot be instantiated |
| 3. `extends`? | Yes, but inheritance is the *mechanism* here, not the demonstrated principle |
| 4. Same method dispatched differently? | Only if the question asks about runtime behaviour |

The **first** check that fires is check 2 → **Abstraction**.

**Answer: B.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | No data is hidden behind `private`; there is no encapsulation scheme in the snippet |
| C | Nothing is dispatched at run time here — `getNumberOfWheels()` is called directly, not through a superclass reference |
| D | `Bike extends Vehicle` exists, but the *principle* the snippet is built to show is the unimplemented contract |

**Second trap in the same question:** if the stem had said *"which concept allows `Bike` to be
treated as a `Vehicle` and call `getNumberOfWheels()` through a `Vehicle` reference"*, the answer
would be **D (Inheritance)** as the mechanism and **C (Polymorphism)** as the principle. Read the
stem's verb: *"demonstrated by"* → the concept in the code; *"allows"* → the enabling relationship.

## Quick rules

- Run the checks in order 1→4: hide state → declare contract → extend → dispatch.
- The **first** matching check wins for "which principle is demonstrated".
- Negative stems ("NOT a principle") → hunt the kill list: compilation, optimization, parallelism.
- `private` + getters = encapsulation. Unimplemented method = abstraction.
- `extends`/`implements` present does **not** automatically make the answer "inheritance" — read
  the verb in the stem.
- Same method name twice in one class = **overloading** → compile-time polymorphism.
- Subclass redefining a parent method = **overriding** → run-time polymorphism.
- Budget 55 seconds. Move on.

## Common traps

| Trap | What you pick | Fix |
|---|---|---|
| Picking inheritance because you see `extends` | D | The stem asks for a *principle*; check whether a contract is being declared |
| Picking polymorphism for any `extends` | C | Polymorphism needs a **reference holding a different runtime type** |
| Ignoring the negative stem | Positive pick | Re-read: "NOT" flips the whole analysis |
| Choosing "Modularity" as the non-pillar | Modularity | Modularity is a real OOP feature; prefer compilation/optimization/parallelism |
| Overthinking a 1-mark question | — | 55 seconds, then move |

## Checklist

- [ ] I can state the 4 checks in order from memory.
- [ ] I know the kill list for negative stems: compilation, optimization, parallelism, serialization.
- [ ] I know that `private` + getters is the encapsulation tell.
- [ ] I know that an unimplemented method is the abstraction tell.
- [ ] I can pick the right answer in the worked example in under 60 seconds.

## Related

- [The four pillars](../01-concepts/01-the-four-pillars.md)
- [Overloading vs overriding](../01-concepts/02-overloading-vs-overriding.md)
- [Abstract class vs interface](02-abstract-class-vs-interface.md)
- [8 solved OOP questions](../03-worked-examples/01-solved-oop-questions.md)
- [OOP principles traps](../04-pitfalls/01-oop-principles-traps.md)
- [OOP principles one-pager](../05-reference/01-oop-principles-one-pager.md)
- [Topic overview](../README.md)
