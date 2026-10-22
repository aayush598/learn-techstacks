# Casts, Type Checks and ClassCastException

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 7 min_
> **Prerequisite:** [Inheritance basics and dynamic dispatch](01-inheritance-basics-and-dispatch.md)

## In one sentence

**Upcasting is implicit and always safe; downcasting is explicit and can throw
`ClassCastException`; and `instanceof` is the guard that stops the exception before it happens.**

## Why the pre-test tests this

- "Which of the following is TRUE about casting?" is a common 1-mark question.
- `ClassCastException` appears in output-prediction questions where the exam wants you to see that
  the cast fails at run time.
- `instanceof` is the most-used type operator in production Java, so the pre-test asks what it
  returns for `null`.

## Core concept

### Upcasting vs downcasting

| | **Upcasting** | **Downcasting** |
|---|---|---|
| Direction | Child → Parent | Parent → Child |
| Syntax | Implicit — just assign | Explicit — `(Child) parentRef` |
| Always safe? | ✅ **yes** — a child *is* a parent | ❌ **no** — it may throw `ClassCastException` |
| Compile-time check | None needed | The compiler allows it if the types are *related*; the **runtime** check decides |
| Example | `Animal a = new Dog();` | `Dog d = (Dog) a;` |

```java
class Animal { }
class Dog extends Animal { }

Animal a = new Dog();     // upcast — implicit, always safe
Dog d = (Dog) a;          // downcast — explicit, safe HERE because a really is a Dog
Dog e = (Dog) new Cat();  // downcast — throws ClassCastException at run time
```

### The `ClassCastException` rule

| Situation | Result |
|---|---|
| The object's runtime type **is** the target type | Cast succeeds |
| The object's runtime type is a **subtype** of the target type | Cast succeeds |
| The object's runtime type is **unrelated** to the target type | ❌ **`ClassCastException`** at run time |
| The reference is `null` | Cast **succeeds** — the result is `null`. No exception |
| The compiler can see the cast is impossible (e.g. `final` unrelated types) | ❌ **compile error** — "inconvertible types" |

**Critical exam point:** `ClassCastException` is a **run-time** exception, not a compile-time
error. The compiler permits `(Dog) someAnimal` even when the object is a `Cat`. That is why
`instanceof` exists.

### `instanceof`

| Question | Answer |
|---|---|
| What does `x instanceof Dog` return? | `true` if `x`'s runtime type is `Dog` **or a subclass** of `Dog`; `false` otherwise |
| What if `x` is `null`? | **`false`** — never throws |
| Is `null instanceof X` legal? | ✅ legal, always `false` |
| What if `x`'s static type is unrelated to `Dog`? | ❌ **compile error** — "inconvertible types" |
| Does `instanceof` work with generics? | ❌ `list instanceof ArrayList<String>` is illegal — the type argument cannot be checked at run time |

```java
Object o = "hello";
if (o instanceof String) {          // true
    String s = (String) o;           // the cast is safe
}
```

### Pattern matching for `instanceof` (Java 16+, not Java 8)

Java 16 added a pattern that binds the casted value in one step:

```java
// Java 16+
if (o instanceof String s) {
    System.out.println(s.length());   // s is already a String — no cast needed
}
```

| Version | Pre-test relevance |
|---|---|
| **Java 8** (what the pre-test runs on) | Use `if (o instanceof String) { String s = (String) o; ... }` |
| Java 16+ | The combined pattern form above |

If a pre-test question shows the combined form, treat it as a **Java 16+** question and answer it
on those semantics. If it asks "is this valid in Java 8?", the answer is **no**.

### The safe-cast idiom

```java
if (obj instanceof Employee) {
    Employee e = (Employee) obj;   // no ClassCastException possible
    e.getName();
}
```

**Java 8 safe-cast with generics:**

```java
if (obj instanceof List<?>) {
    List<?> list = (List<?>) obj;   // the wildcard form compiles in Java 8
}
```

The plain `List` cast would give an unchecked warning; the wildcard form is the safe, warning-free
version.

### Upcasting and collections — the practical reason it matters

`ArrayList<Object>`, `ArrayList<Animal>` and `ArrayList<Dog>` are **different types**. Java's
generics are invariant — a `List<Dog>` is **not** a `List<Animal>`.

| Assignment | Legal? |
|---|---|
| `List<Animal> a = new ArrayList<Dog>();` | ❌ compile error — generics are invariant |
| `List<Object> a = new ArrayList<Dog>();` | ❌ compile error — same reason |
| `Animal a = new Dog();` | ✅ legal — **upcasting** of a *reference* is fine |
| `List<? extends Animal> a = new ArrayList<Dog>();` | ✅ legal — wildcards work around invariance |

The exam trap: *"Why can you assign a `Dog` to an `Animal` variable but not a `ArrayList<Dog>` to
an `ArrayList<Animal>`?"* → **generics are invariant**; use a wildcard (`? extends Animal`) if you
need it. See the [Collections Framework](../06-Collections-Framework/README.md).

### Casting and the `Object` class

Every class extends `Object`, so **every reference can be upcast to `Object`**. That is why
`Object.equals`, `Object.toString` and `Object.hashCode` are available on everything — and why
`Object` is the only method set every type shares.

## Quick rules

- **Upcast** = child to parent = implicit = **always safe**.
- **Downcast** = parent to child = explicit = **may throw** `ClassCastException`.
- `ClassCastException` is a **run-time** failure, not a compile error.
- `null instanceof X` → **`false`**, always, and never throws.
- `instanceof` checks the **runtime** type and includes subclasses.
- `instanceof` with a generic type argument → compile error.
- Casting a `null` reference succeeds and yields `null`.
- Generics are **invariant**: `List<Dog>` is not a `List<Animal>` — use `? extends Animal`.
- Every type can be upcast to `Object`.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "Downcasting is always safe" | Yes | It can throw `ClassCastException` |
| "A wrong downcast is a compile error" | Compile error | The compiler allows it; it fails at **run time** |
| "`null instanceof X` throws NPE" | Throws | It returns **`false`** |
| "`instanceof` includes subclasses" | No | It **does** — `new Puppy() instanceof Dog` is `true` |
| "You can check `instanceof ArrayList<String>`" | Yes | Type arguments are erased — compile error |
| "Generics are covariant, so `List<Dog>` fits `List<Animal>`" | Yes | Java generics are **invariant** |
| "Casting `null` throws" | Throws | It succeeds and gives `null` |

## Checklist

- [ ] I can define upcasting and downcasting in one line each.
- [ ] I know exactly when `ClassCastException` is thrown.
- [ ] I know `null instanceof X` is `false`.
- [ ] I know `instanceof` includes subclasses.
- [ ] I can explain why `List<Dog>` is not a `List<Animal>`.
- [ ] I know the Java 8 safe-cast idiom with a wildcard.

## Related

- [Inheritance basics and dynamic dispatch](01-inheritance-basics-and-dispatch.md)
- [Abstract, final and the constructor chain](03-abstract-final-and-the-constructor-chain.md)
- [The method resolution procedure](../02-techniques/01-method-resolution-order.md)
- [8 solved inheritance questions](../03-worked-examples/01-solved-inheritance-questions.md)
- [Inheritance traps](../04-pitfalls/01-inheritance-traps.md)
- [Inheritance one-pager](../05-reference/01-inheritance-one-pager.md)
- [Topic overview](../README.md)
