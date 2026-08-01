# Chapter: C++ Advanced OOPs

## What you'll learn
How C++ actually implements the OOP concepts you know from Java: the **v-table** (virtual dispatch) that makes `virtual` methods polymorphic at runtime, **RTTI** (`typeid`, `dynamic_cast`) that lets you identify and safely downcast objects, and the **copy/move semantics** governed by constructors, the Rule of Three/Five, and `std::move`. You'll be able to predict which constructor runs for any expression, explain the runtime cost of `virtual` and `dynamic_cast`, and write classes that are safe to copy, move, and destroy.

## Prerequisites (linked)
- [Part 01 — Classes & Objects](../../part-01-oops-fundamentals/README.md): constructors, member functions, and object lifecycle are the vocabulary of this chapter.
- [Part 03 — Inheritance](../../part-03-inheritance/README.md): the diamond problem and virtual inheritance appear when discussing C++ multiple inheritance.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md): `virtual` functions and `dynamic_cast` are exactly "polymorphism made real" in C++.
- [Part 05 — Object Relationships](../../part-05-association-aggregation-composition/README.md): ownership semantics (who deletes the pointer?) shape copy/move design.
- [Part 06 — SOLID](../../part-06-solid-and-design-principles/README.md): LSP drives `virtual` interface design and `dynamic_cast` usage.

## Sections (linked table)

| Section | Topic | Key skill |
|---|---|---|
| [01 — v-Tables, RTTI and `typeid`](section-01-cpp-vtables-rtti-and-typeid.md) | `virtual` dispatch, vptr/v-table, `typeid`, `dynamic_cast`, cost model | Explain how overriding works under the hood and predict cast/typeid behavior |
| [02 — Copy Constructors and Move Semantics](section-02-copy-constructors-and-move-semantics.md) | Rule of Three/Five, copy vs move, `std::move`, `unique_ptr`/`shared_ptr` | Write safe resource-owning classes and predict copy/move calls |

## One-paragraph narrative connecting all sections
C++ OOP is a story about **two kinds of information**: what the compiler knows statically (types, sizes — decided at compile time) and what the program must learn at runtime (which object a pointer really points to). Section 01 shows how the compiler encodes *runtime polymorphism* through v-tables and RTTI — the mechanisms behind `virtual` methods and safe downcasting. Section 02 shows how ownership is a *type-level contract*: copy constructors clone resources, move constructors transfer them, and the Rule of Five keeps them consistent so classes are safe under the strict lifetime rules (stack/heap/RAII) that make manual memory management survivable. Together they explain why C++ interviews focus on "what does the compiler generate?" and "who owns this memory?" — the two questions every C++ OOP answer must answer precisely.

## Common interview trap in this chapter
Candidates confuse **static and dynamic type**. With `Base* p = new Derived();`, `p` has static type `Base*` but dynamic type `Derived`. `p->f()` dispatches dynamically *only if `f` is `virtual`* — a non-virtual `Base::f` would run even though the object is a `Derived`. Second trap: calling `delete` through a base pointer without a `virtual` destructor is **undefined behavior** — the derived destructor never runs. Third: `dynamic_cast` works only on polymorphic types (types with at least one `virtual` method); it returns `nullptr` (pointer form) or throws `std::bad_cast` (reference form) on failure.

## Checklist before moving on
- [ ] I can draw a v-table diagram and trace `p->f()` dispatch for `Base*` pointing to `Derived`.
- [ ] I know exactly when a class gets a vptr and what `sizeof` costs it.
- [ ] I can explain `typeid(x).name()`, `typeid(*p) == typeid(*q)`, and when `dynamic_cast` returns `nullptr` vs throws.
- [ ] I know the Rule of Three and Rule of Five by heart and can state why the destructor is part of them.
- [ ] I can predict copy vs move for `A a2 = a1;`, `A a3 = std::move(a1);`, `return a;` (RVO), and `emplace_back`.
- [ ] I can write a move constructor that leaves the source in a valid-but-empty state and a move-assignment that self-assigns safely.
- [ ] I understand why `unique_ptr` is non-copyable, `shared_ptr` uses atomic refcounts, and what a virtual destructor is for.
- [ ] I can explain the cost model: virtual call ≈ extra indirect load; `dynamic_cast` may walk the inheritance graph.
