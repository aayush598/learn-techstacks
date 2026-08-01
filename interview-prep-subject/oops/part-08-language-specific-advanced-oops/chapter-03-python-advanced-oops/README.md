# Chapter: Python Advanced OOPs

## What you'll learn
How Python does OOP without interfaces and type hierarchies: **multiple inheritance resolved by the C3 linearization (MRO)**, `super()` in *cooperative* multiple inheritance, and the **dunder-method contract** (`__init__`, `__eq__`, `__hash__`, `__getattr__`, `__iter__`, etc.) that implements operator overloading, protocols, and duck typing — plus how dataclasses and abstract base classes formalize the patterns.

## Prerequisites (linked)
- [Part 01 — Classes & Objects](../../part-01-oops-fundamentals/README.md): you need the class/object vocabulary before Python's dynamic class model.
- [Part 03 — Inheritance](../../part-03-inheritance/README.md): the diamond problem is the reason MRO exists — this chapter resolves it in Python.
- [Part 04 — Polymorphism](../../part-04-polymorphism/README.md): duck typing vs interface-based polymorphism is the core tension here.
- [Part 02 — Encapsulation & Abstraction](../../part-02-encapsulation-and-abstraction/README.md): Python's name mangling and ABCs are its encapsulation/abstraction tools.
- [Part 06 — SOLID](../../part-06-solid-and-design-principles/README.md): LSP is enforced differently in a duck-typed, runtime-checked language.

## Sections (linked table)

| Section | Topic | Key skill |
|---|---|---|
| [01 — Python MRO, `super()` and Dunder Methods](section-01-python-oops-mro-super-and-dunder-methods.md) | C3 linearization, cooperative `super()`, `__init__` chains, operator/dunder protocols, dataclasses, ABCs | Trace the method resolution order for any class and design cooperative hierarchies |

## One-paragraph narrative connecting all sections
Python has no access modifiers, no interfaces in the Java sense, and no static type checker in the core — instead it leans on **conventions and protocols**. Section 01 opens with the C3 MRO, the deterministic algorithm that turns a (possibly diamond-shaped) inheritance graph into a single linear list of classes, so method lookup always has one unambiguous answer. It then shows `super()` as the *cooperative* call that threads `__init__` through every class in the MRO, not just the parent. Finally it covers the dunder methods — the "operator protocol" through which `+`, `==`, `in`, `len()` and iteration are implemented — plus dataclasses (immutable-ish value objects) and ABCs (Python's interface substitute). Understanding MRO + dunders answers the two questions Python OOP interviews always ask: "which method gets called, and in what order?" and "how does the language implement this operator or protocol?"

## Common interview trap in this chapter
Beginners write `super().__init__()` thinking it calls "the parent's" `__init__`. In multiple inheritance, `super()` follows the **full MRO**, so it can call an *uncle* class's `__init__` — and if every class uses `super()`, *every* `__init__` in the chain runs once. If any class in the diamond calls `Base.__init__` directly (non-cooperative), you get double-initialization and a confusing `__init__() got multiple values` error. Second trap: forgetting `__hash__` when defining `__eq__` — Python sets `__hash__` to `None`, making instances unhashable (usable as dict keys → `TypeError: unhashable type`). Third: assuming `__getattr__` catches everything — it only fires for *missing* attributes; `__getattribute__` fires for every access.

## Checklist before moving on
- [ ] I can compute the C3 linearization of a diamond `class D(A, B)` by hand and predict method lookup.
- [ ] I can explain why the order is D → A → B → Base (not D → B → A) given `class D(A, B)`.
- [ ] I can write a cooperative `super()` chain where every class in a diamond initializes exactly once.
- [ ] I can list the dunders behind `+`, `==`, `len()`, `in`, indexing, iteration, and truthiness.
- [ ] I know that defining `__eq__` kills `__hash__`, and how to restore it.
- [ ] I can contrast `__getattr__` vs `__getattribute__` vs `__setattr__`.
- [ ] I can use `@dataclass` and `@abstractmethod` correctly, and explain when an ABC is warranted.
- [ ] I can explain duck typing vs `isinstance` checks and when protocols/ABCs are the right tool.
