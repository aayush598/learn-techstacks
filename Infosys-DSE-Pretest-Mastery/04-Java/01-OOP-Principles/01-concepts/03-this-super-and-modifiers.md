# `this`, `super`, and the Modifier Matrix

> Section 4 · Java · OOP Principles · _Estimated reading time: 8 min_
> **Prerequisite:** [Overloading vs overriding](02-overloading-vs-overriding.md)

## In one sentence

`this` refers to the **current object** and `super` refers to the **immediate parent**, and the
`final` / `abstract` / `static` modifiers form a **fixed compatibility matrix** where exactly one
combination per row is illegal.

## Why the pre-test tests this

- "What does `this` and `super` refer to?" is a standard 1-mark question.
- "Which modifier combination is a compile error?" appears as a "does this compile" question, where
  the answer is decided in one line of the modifier matrix.
- Output-prediction questions where a field is **shadowed** by a subclass field are frequent, and
  the `this.x` / `super.x` distinction is the whole answer.

## Core concept

### `this` vs `super`

| Keyword | Points to | Legal places | Typical uses |
|---|---|---|---|
| **`this`** | The **current object** | Instance methods, constructors, instance initializers | `this.field` to disambiguate a shadowed field; `this.method()`; `this(args)` constructor chaining |
| **`super`** | The **immediate superclass** | Instance methods, constructors, instance initializers | `super.field` to reach the parent's version; `super.method()`; `super(args)` constructor chaining |

Both are **implicit**: inside any instance method, `this` already means the current object, so
`this.toString()` is the same as `toString()`.

### Illegal uses of `this` and `super`

| Statement | Result |
|---|---|
| `this` inside a **static** method | ❌ compile error — "non-static variable this cannot be referenced from a static context" |
| `super` inside a **static** method | ❌ compile error — same reason |
| `this()` / `super()` anywhere other than the **first statement** of a constructor | ❌ compile error |
| `this()` and `super()` in the **same** constructor | ❌ compile error — you may call one or the other, never both |
| `super()` in a class with **no** superclass constructor declared | ❌ compile error — the no-arg superclass constructor does not exist |

### Field shadowing and how to reach each field

```java
class Base {
    String name = "Base";
}

class Derived extends Base {
    String name = "Derived";

    void print() {
        System.out.println(name);        // Derived  (own field wins)
        System.out.println(this.name);   // Derived  (explicitly own field)
        System.out.println(super.name);  // Base     (parent's field)
    }
}
```

The rule: **the subclass field hides the parent field**; unqualified `name` resolves to the
*nearest* declaration. Use `super.name` to reach the parent's.

### Worked code — construction order and shadowing

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

**This prints exactly:**

```
Base ctor
Derived
```

| Step | What happens |
|---|---|
| 1 | `new Derived()` → JVM allocates the object |
| 2 | `super()` runs → `Base` constructor runs → prints `Base ctor` |
| 3 | `Base`'s instance field initialiser runs → `name = "Base"` |
| 4 | `Derived`'s instance field initialiser runs → `name = "Derived"` (hides `Base.name`) |
| 5 | `Derived` constructor body continues → `name` resolves to `Derived.name` → prints `Derived` |

### The modifier matrix — where each modifier may sit

| Modifier | On a **class** | On a **method** | On a **field** |
|---|---|---|---|
| `public` | ✅ | ✅ | ✅ |
| `protected` | ❌ (top-level only; allowed on a *nested* class) | ✅ | ✅ |
| `private` | ❌ (top-level only; allowed on a *nested* class) | ✅ | ✅ |
| `static` | ❌ (a top-level class cannot be static; nested classes can) | ✅ | ✅ |
| `final` | ✅ — cannot be extended | ✅ — cannot be overridden | ✅ — assigned once |
| `abstract` | ✅ — cannot be instantiated | ✅ — no body, must be implemented | ❌ illegal on a field |

### The illegal combinations (each is a compile error)

| Illegal declaration | Reason |
|---|---|
| `abstract static void f();` | An abstract method has no body to make static; also a static method cannot be inherited-and-overridden |
| `abstract final void f();` | An abstract method must be implemented; a final method must not be |
| `abstract private void f();` | A private method is not inherited, so it can never be implemented |
| `final abstract class A {}` | Same as `abstract final` |

**Legal combinations worth memorising:**

| Declaration | Legal? | Note |
|---|---|---|
| `abstract void f();` inside `abstract class A` | ✅ | The rule of the abstract class is that it may *declare* abstract methods |
| `static void f() {}` inside an abstract class | ✅ | Concrete static method in an abstract class is fine |
| `private void f() {}` inside an abstract class | ✅ | Not inherited, not overridable |
| `final void f() {}` inside an abstract class | ✅ | Not overridable, but the class stays abstract |
| `synchronized void f() {}` | ✅ | `synchronized` is orthogonal to `abstract`/`final`/`static` |

### What `final` actually blocks, in one table

| Target | `final` means | Error message you'll see |
|---|---|---|
| Class | Cannot be **extended** | "cannot inherit from final class" |
| Instance method | Cannot be **overridden** | "overridden method is final" |
| Static method | Cannot be **overridden or hidden** | "cannot override final method" / "cannot hide" |
| Field | Assigned **exactly once** | "variable X might already have been assigned" |
| Local variable | Assigned exactly once | "variable X might already have been assigned" |
| Parameter | Assigned exactly once | same |

**`final` does not mean "immutable object".** A `final` field can hold a mutable object
(a `List`, a `Date`); the *reference* is fixed, the *contents* are not. Full immutability rules
are in [Classes, Objects & Constructors](../02-classes-objects-constructors/README.md).

## Quick rules

- `this` = current object. `super` = immediate parent. Both illegal in a `static` context.
- `this(...)` and `super(...)` must be the **first statement** of a constructor, and never both.
- A subclass field **hides** the parent's; `super.field` reaches the parent's.
- Unqualified `field` resolves to the **nearest** declaration.
- `abstract` + `static` / `final` / `private` on a method = **compile error**, all three.
- `abstract` on a **field** = compile error. `static` on a **top-level class** = compile error.
- `final` method → not overridable, but **still overloadable**.
- `final` field → assigned once (declaration, initializer block, or constructor).
- `final` ≠ immutable; it fixes the reference, not the object's contents.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| `this` inside a static method is legal | "Compiles fine" | Compile error: non-static context |
| `super()` need not be the first statement | Accepting the code | Compile error: "call to super must be first statement" |
| Both `this()` and `super()` in one constructor | Accepting the code | Compile error: "call to super must be first statement" |
| `super` refers to "some ancestor" | Choosing the grandparent's field | `super` = **immediate** parent only |
| `final` method cannot be overloaded | Rejecting a legal overload | `final` blocks **overriding**, not **overloading** |
| `final` field means the object is immutable | "The list inside can never change" | Only the reference is fixed |
| `abstract private` is fine | Accepting it | A private method cannot be inherited → can never be implemented |
| `static` and `abstract` together | Accepting it | Abstract methods exist to be overridden; static methods are not overridden |

## Checklist

- [ ] I can name the three compile errors involving `this`/`super` placement.
- [ ] I can name the four illegal modifier combinations without looking.
- [ ] I know `final` blocks overriding but not overloading.
- [ ] I know `final` fixes a reference, not the object's contents.
- [ ] I can predict the output of the shadowing example above.
- [ ] I can list which modifiers are legal on a top-level class: `public`, `final`, `abstract`
      (and the default/package-private), plus `strictfp`/`sealed` in newer versions.

## Related

- [The four pillars](01-the-four-pillars.md)
- [Overloading vs overriding](02-overloading-vs-overriding.md)
- [Object lifecycle and construction](../02-classes-objects-constructors/01-concepts/01-object-lifecycle-and-construction.md)
- [8 solved OOP questions](../03-worked-examples/01-solved-oop-questions.md)
- [OOP principles traps](../04-pitfalls/01-oop-principles-traps.md)
- [OOP principles one-pager](../05-reference/01-oop-principles-one-pager.md)
- [Topic overview](../README.md)
