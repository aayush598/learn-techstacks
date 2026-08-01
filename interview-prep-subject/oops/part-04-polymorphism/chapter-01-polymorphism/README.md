# Chapter: Polymorphism

## What you'll learn
- The precise definition of **polymorphism** ("many forms") and the **four categories**: ad-hoc (overloading), parametric (generics), subtype (inheritance/overriding), and coercion (implicit conversion).
- **Compile-time polymorphism** via method overloading: the resolution rules (most specific, phase matching), the "overload on return type?" trap, and overloading-vs-overriding.
- **Runtime polymorphism** via overriding and **virtual functions**: Java's default-virtual model vs C++'s explicit `virtual`, `final`/`@Override`, and the substitution principle.
- **Vtable and dynamic dispatch internals**: how a virtual call is compiled to O(1) table lookup, inline caches, megamorphic calls, and devirtualization.
- **Covariant return types** and how ad-hoc/subtype/parametric polymorphism differ in when they're chosen and what they cost.

## Prerequisites (linked)
- [Part 03 — Inheritance](../../part-03-inheritance/README.md): overriding, `super`, upcasting are required reading.
- [Part 02 — Abstraction](../../part-02-encapsulation-and-abstraction/README.md): interfaces give you interface polymorphism.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Polymorphism in Depth](section-01-polymorphism-in-depth.md) | The definition, four categories, "many forms, one interface" |
| [Section 02 — Compile-Time Polymorphism: Method Overloading](section-02-compile-time-polymorphism-method-overloading.md) | Same name, different signatures; resolution rules and traps |
| [Section 03 — Runtime Polymorphism: Overriding and Virtual Functions](section-03-runtime-polymorphism-overriding-and-virtual-functions.md) | Dynamic dispatch, Java vs C++ virtual, `final`/`@Override` |
| [Section 04 — Vtable and Dynamic Dispatch Internals](section-04-vtable-and-dynamic-dispatch-internals.md) | Object layout, vptr/vtable, inline caches, devirtualization |
| [Section 05 — Covariant Returns & Ad-hoc/Subtype/Parametric](section-05-covariant-return-types-and-ad-hoc-subtype-parametirc-polymorphism.md) | The finer flavors and when to use each |

## One-paragraph narrative connecting all sections
Polymorphism means "one interface, many implementations" — the property that lets a single call shape (`speak()`) produce different behavior per object (Section 01). Some of that variety is decided at compile time: **overloading** picks among same-named methods by their argument types (Section 02). The powerful variety is decided at runtime: **overriding** lets the actual object choose its implementation through **virtual functions** (Section 03), and the machinery that makes that fast is the **vtable** — a per-class method table, one O(1) indirection, refined by inline caches and devirtualization in real JVMs/compilers (Section 04). The remaining flavors — covariant return types, ad-hoc vs parametric vs subtype — are the precise vocabulary you use to say *which kind* of polymorphism a design employs (Section 05).

## Common interview trap in this chapter
Candidates conflate overloading and overriding ("both are polymorphism — same thing"). They are both polymorphism but opposite in timing: overloading resolves at **compile time by signature** (no vtable), overriding resolves at **runtime by object type** (vtable). Second trap: "you can overload on return type." You cannot in Java/C++ — return type alone never disambiguates. Third: "Java methods are not virtual unless you mark them." Wrong — Java instance methods are virtual by default (only `final`/`static`/`private` aren't); it's C++ that requires the explicit `virtual` keyword.

## Checklist before moving on
- [ ] I can define polymorphism and name all four categories with one example each.
- [ ] I can apply overload-resolution rules (exact → widening → boxing → varargs) and explain why return type doesn't matter.
- [ ] I can explain overriding rules and the Java-vs-C++ `virtual` difference.
- [ ] I can draw the vtable, trace a virtual call in 5 steps, and explain inline-cache devirtualization.
- [ ] I can explain covariant return types with an example.
- [ ] I can say which category (ad-hoc/parametric/subtype) a given design uses and why.
