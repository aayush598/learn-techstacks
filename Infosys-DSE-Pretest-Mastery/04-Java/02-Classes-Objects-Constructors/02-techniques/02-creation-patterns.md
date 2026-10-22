# Creation Patterns — Singleton, Immutable, Factory, Builder

> Section 4 · Java · Classes, Objects & Constructors · _Estimated reading time: 9 min_
> **Prerequisite:** [Object creation, copying and identity](../01-concepts/02-object-creation-copying-and-identity.md)

## In one sentence

The four object-creation patterns the exam asks about are decided by **one question each** — how
many instances, can the state change after construction, how many parameters, and who owns the
construction logic.

## Why the pre-test tests this

- "Which is the correct way to implement a thread-safe singleton?" is a recurring 1-mark
  question, and the four variants (eager, lazy-unsafe, lazy-holder, DCL) map onto four options.
- "Which of the following makes a class immutable?" tests a checklist, not a keyword.
- "Factory method vs builder pattern" is a classic design-pattern MCQ.

## Core concept

### Singleton — the four variants

| Variant | Code | Thread-safe? | Note |
|---|---|---|---|
| **Eager** | `private static final S INSTANCE = new S();` | ✅ yes | The instance is created at class load, whether you need it or not |
| **Lazy (naive)** | `if (instance == null) instance = new S();` | ❌ **no** | Two threads can both create an instance — a race |
| **Lazy (holder idiom)** | `private static class Holder { static final S INSTANCE = new S(); }`<br>`static S getInstance() { return Holder.INSTANCE; }` | ✅ yes | The JVM guarantees class initialisation is synchronised — **no** `synchronized` keyword needed |
| **Double-checked locking** | `if (instance == null) { synchronized (lock) { if (instance == null) instance = new S(); } }` | ✅ yes, **only if** the field is `volatile` | `volatile` prevents a thread from seeing a partially constructed object |

**The exam fact:** the **holder idiom** is thread-safe without `synchronized`, because the JVM
serialises class initialisation. That is the answer to "which singleton is thread-safe with no
synchronization?".

### The singleton trap — construction cost vs correctness

| Decision | Answer |
|---|---|
| Singleton with expensive construction? | Use **lazy** (holder idiom), not eager |
| Singleton that must be available immediately at startup? | Eager is fine |
| Does a singleton break testability? | Yes — global state. The exam may ask "what is a drawback" → answer: **hard to test / cannot create fresh instances** |

### Immutable classes — the 5-point checklist

An immutable object's state **can never change after construction**. All 5 must hold:

| # | Rule | Why |
|---|---|---|
| 1 | All fields are `private final` | No reassignment, no outside access |
| 2 | No setters or any method that mutates state | Behaviour must not change state |
| 3 | The class is `final` (or all its fields are final and it has no subclass) | Otherwise a subclass could mutate inherited state |
| 4 | **Defensive copies** of mutable objects passed in (constructor) and returned (getters) | Otherwise the caller can mutate the object's internals |
| 5 | Fields are not `static` and not mutable containers | A shared static `List` breaks immutability |

**Worked example — an immutable class:**

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

final class ImmutableOrder {
    private final String id;
    private final List<String> lines;

    ImmutableOrder(String id, List<String> lines) {
        this.id = id;
        this.lines = Collections.unmodifiableList(new ArrayList<>(lines)); // defensive copy
    }

    public String getId() { return id; }

    public List<String> getLines() { return lines; }   // already unmodifiable
}
```

| Rule satisfied | How |
|---|---|
| 1 | `private final` fields |
| 2 | No setters |
| 3 | The class is `final` |
| 4 | The constructor copies the incoming list; the getter returns an unmodifiable view |
| 5 | No static mutable fields |

**Why `String` is immutable** — the same checklist applied: `final` fields, no setters, and
`char[]` is not exposed (Java 8 and earlier used a `char[]` copied in the constructor; Java 9+
uses a `byte[]`). `Integer`, `Long`, `Double`, `Boolean`, `BigDecimal` are immutable too.

**Trap:** a class with a `final` field of type `List` is **not** immutable unless the list is
defensively copied and unmodifiable. `final` alone does not make an object immutable.

### Factory method vs builder — the decision

| | **Factory method** | **Builder** |
|---|---|---|
| Construction | One step: `create(a, b, c)` | Multi-step: `new Builder().a().b().build()` |
| Parameter count | Few, fixed, known | Many, or many optional |
| Optional parameters | Awkward — needs overloads | Natural — just don't call the setter |
| Immutability | Easy — the factory controls the result | Easy — build() returns a fresh immutable object |
| Cost of a new optional field | Add an overload | Add a builder method |
| Typical use | Simple, stable value objects | Complex objects with 6+ fields, or configuration objects |

**Exam framing:** *"Which pattern is most suitable when an object has many optional
attributes?"* → **Builder**. *"Which pattern hides which concrete class is created?"* →
**Factory method**.

### Related creation idioms worth knowing

| Idiom | What it does | Exam hook |
|---|---|---|
| **Static factory method** | A `public static` method on the class that returns an instance | Lets you hide the constructor, return cached instances, and avoid `this` escape |
| **Private constructor + static factory** | The class controls every instantiation | "How do you prevent instantiation?" → private constructor |
| **Factory pattern** | A separate factory class decides which concrete type to return | Decouples callers from concrete classes |
| **Prototype / `clone()`** | Creates an object by copying an existing one | Shallow vs deep copy |
| **Singleton** | Exactly one instance | The four variants above |

## Quick rules

- Thread-safe singleton with no `synchronized`: the **holder idiom**.
- Double-checked locking needs a **`volatile`** field.
- Immutable class = `private final` fields + no setters + `final` class + **defensive copies** +
  no mutable static state.
- `final` on a `List` field does **not** make the class immutable.
- Many optional parameters → **Builder**. Few fixed parameters → **Factory method**.
- `String`, the wrapper classes and `BigDecimal` are immutable.
- A private constructor is the standard way to forbid direct `new`.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| The naive lazy singleton is thread-safe | "Thread-safe" | Two threads can both create one — that is the classic bug |
| DCL works without `volatile` | "Safe" | Without `volatile` a thread can see a half-built object |
| `final` fields ⇒ immutable class | "Immutable" | The **contents** can still change |
| A class with only getters is immutable | "Immutable" | Without `final` fields and a `final` class it is not |
| Returning the internal list from a getter is fine | "Immutable" | The caller can mutate it — return a copy |
| Builder is for objects with few fields | "Builder" | Builder is for **many** / optional fields |
| Factory method is a design pattern with a separate class | "Yes always" | It is also commonly a `static` method on the same class |

## Checklist

- [ ] I can write the holder-idiom singleton from memory.
- [ ] I know why double-checked locking needs `volatile`.
- [ ] I can list the 5 rules of immutability.
- [ ] I can explain why `final List<String> list = new ArrayList<>()` is not immutable.
- [ ] I know which pattern fits "many optional attributes".
- [ ] I can name 3 immutable JDK classes.

## Related

- [Object lifecycle and construction](../01-concepts/01-object-lifecycle-and-construction.md)
- [Object creation, copying and identity](../01-concepts/02-object-creation-copying-and-identity.md)
- [Constructor rules and compile errors](01-constructor-rules-and-compile-errors.md)
- [8 solved construction questions](../03-worked-examples/01-solved-construction-questions.md)
- [Construction traps](../04-pitfalls/01-construction-and-object-traps.md)
- [Construction one-pager](../05-reference/01-construction-one-pager.md)
- [Topic overview](../README.md)
