# Override vs Hide — the 60-Second Triage

> Section 4 · Java · Inheritance & Polymorphism · _Estimated reading time: 7 min_
> **Prerequisite:** [The method resolution procedure](01-method-resolution-order.md)

## In one sentence

A same-named method in a subclass is an **override** if the parent's is an instance method, a
**hide** if it is static, and **neither** if the parent's is `private`, `final` or a constructor.

## Why the pre-test tests this

- "Which of these methods can be overridden?" is a pure recall 1-marker that candidates lose
  because they treat "same name in a subclass" as the answer.
- The pre-test loves options that are *almost* right: "a static method can be overridden" is
  wrong; "a static method can be hidden" is right; "an overloaded method can be overridden" is
  wrong.
- One table settles every version of this question.

## Core concept

### The triage table

| The parent's method is… | The child's same-named method is… | Is it an override? | Is it a hide? | Rule |
|---|---|---|---|---|
| `public` instance | `public` instance | ✅ yes | — | Normal override |
| `protected` instance | `public` instance | ✅ yes | — | Widening access is allowed |
| `public` instance | `protected` instance | ❌ | — | Narrowing access → **compile error** |
| package-private instance (same package) | same signature | ✅ yes | — | Visible, so overridable |
| package-private instance (different package) | same signature | ❌ | — | Not inherited → a **new** method |
| `private` instance | same signature | ❌ | — | Not inherited → a **new** method |
| `static` | `static` | ❌ | ✅ yes | **Hiding** |
| `static` | instance | ❌ | — | Not allowed — compile error |
| instance | `static` | ❌ | — | Not allowed — compile error |
| `final` instance | same signature | ❌ | — | **Compile error** ("cannot override final method") |
| `final` static | `static` | ❌ | ❌ | **Compile error** ("cannot hide") |
| a constructor | same name | ❌ | — | Constructors are **not inherited** |
| different parameter list | any | ❌ | — | That is **overloading**, not overriding |

### The three legal-override conditions

A method is overridden only when **all** of these hold:

| # | Condition | Fails when |
|---|---|---|
| 1 | Same **name** and same **parameter list** | The parameter list differs → it is an overload |
| 2 | The parent's method is **visible** to the child (not `private`, and package-private only within the same package) | The parent's method is `private` → a brand-new method |
| 3 | The parent's method is **not `static`** and **not `final`** | `static` → hiding; `final` → compile error |

Plus the two restrictions on the child version:

| Restriction | Rule | Error if broken |
|---|---|---|
| Access modifier | Same or **wider** | "attempting to assign weaker access privileges" |
| Checked exceptions | Same or a **subset** | "unreported exception" |

And one permission:

| Permission | Rule |
|---|---|
| Return type | Same or **covariant** (a subtype) |

### Covariant return types — the legality table

```java
class A { Object get() { return null; } }
class B extends A { @Override String get() { return "b"; } }    // legal
```

| Parent returns | Child returns | Legal? |
|---|---|---|
| `Object` | `Object` | ✅ |
| `Object` | `String` | ✅ covariant |
| `Object` | `Integer` | ✅ covariant |
| `String` | `Object` | ❌ wider |
| `String` | `Integer` | ❌ unrelated |
| `void` | anything | ❌ — `void` is not substitutable |

**The exam trap:** *"A method can differ in its return type and still override."* → **False**. The
return type is **not** part of the signature for the override test; a method that differs *only*
in return type is a **compile error** (not an overload, not an override).

### Worked example — four methods, four verdicts

```java
class Parent {
    public void a() { }
    protected void b() { }
    public static void c() { }
    private void d() { }
    final void e() { }
    Parent() { }
}

class Child extends Parent {
    @Override public void a() { }                  // 1
    @Override public void b() { }                  // 2
    static void c() { }                            // 3
    void d() { }                                   // 4
    // void e() { }                               // 5 — would not compile
    Child() { }                                    // 6
}
```

| # | Child's method | Verdict | Why |
|---|---|---|---|
| 1 | `public void a()` | ✅ **override** | Same signature, public instance method |
| 2 | `public void b()` | ✅ **override** | Widening `protected` → `public` is allowed |
| 3 | `static void c()` | **hide** | The parent's is static → hiding, not overriding |
| 4 | `void d()` | **not an override** | The parent's `d()` is `private` — not inherited. This is a brand-new method |
| 5 | `void e()` | ❌ **compile error** | The parent's `e()` is `final` |
| 6 | `Child()` | **not an override** | Constructors are not inherited; `Child()` implicitly calls `super()` |

**Method 4 is the trap.** The child has a method with the same name and signature as a private
parent method — but because the parent's method is **not inherited**, the child's method has
nothing to override. It is simply a new method. The exam loves this.

### Overriding vs overloading — the "two methods with the same name" triage

| Question | Overriding | Overloading |
|---|---|---|
| Same class or across classes? | Across (parent → child) | Within the **same** class |
| Same parameter list? | ✅ yes | ❌ no — must differ |
| Is the return type allowed to differ? | Yes, **covariant** only | Yes, freely |
| Can it be `static`? | No | Yes |
| Can it be `private`? | No | Yes |
| Can it be `final`? | No | Yes |
| When is it resolved? | Run time | Compile time |

**Two methods with the same name and the same parameters in the same class are a compile error** —
you cannot overload on return type alone.

## Quick rules

- Instance + same signature + visible parent + non-static + non-final = **override**.
- Static + same signature = **hide**.
- `private` parent method = **not inherited** → the child's method is new.
- `final` parent method = **compile error** if the child tries to override.
- Constructors are **not inherited** and **not overridable**.
- Overriding may **widen** access and **narrow** the return type — never the reverse.
- Overloading may **not** differ only in return type.
- A package-private parent method is overridable only from the **same package**.

## Common traps

| Trap | The wrong answer it produces | Fix |
|---|---|---|
| "Static methods can be overridden" | Yes | They are **hidden** |
| "Private methods can be overridden" | Yes | Not inherited → new method |
| "Final methods can be overridden" | Yes | Compile error |
| "Constructors can be overridden" | Yes | Constructors are not inherited |
| "A package-private method can be overridden from any package" | Yes | Only from the **same package** |
| "Overriding may narrow the access modifier" | Yes | Only **wider** is allowed |
| "An override may add a new checked exception" | Yes | Only the same or a **subset** |
| "Different return type = overloading" | Yes | It is a **compile error** |

## Checklist

- [ ] I can fill in the triage table from memory.
- [ ] I can state the three override conditions.
- [ ] I know the two restrictions and the one permission of an override.
- [ ] I can explain why the child's `void d()` is not an override.
- [ ] I know that `void` cannot be covariantly overridden.
- [ ] I know the rule about package-private methods and packages.

## Related

- [The method resolution procedure](01-method-resolution-order.md)
- [Inheritance basics and dynamic dispatch](../01-concepts/01-inheritance-basics-and-dispatch.md)
- [Abstract, final and the constructor chain](../01-concepts/03-abstract-final-and-the-constructor-chain.md)
- [8 solved inheritance questions](../03-worked-examples/01-solved-inheritance-questions.md)
- [Inheritance traps](../04-pitfalls/01-inheritance-traps.md)
- [Inheritance one-pager](../05-reference/01-inheritance-one-pager.md)
- [Topic overview](../README.md)
