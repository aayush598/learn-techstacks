# Part: Polymorphism

## What this part covers
Polymorphism ("many forms") is the pillar that makes inheritance *useful*: it lets one method name or one interface drive many implementations, decided either at compile time (overloading, generics) or at runtime (overriding via virtual dispatch). This part covers the full spectrum: what polymorphism is and its four categories (ad-hoc, parametric, subtype); compile-time polymorphism through method overloading (with its resolution rules and traps); runtime polymorphism through overriding and virtual functions (C++ `virtual`, Java's default); the **vtable and dynamic dispatch internals** (how a call finds the right implementation in O(1), virtual tables, inline caches, devirtualization); and the subtler forms — covariant return types and the ad-hoc/subtype/parametric distinction. After this part you'll be able to explain "what happens when you call an overridden method" at the bytecode/assembly level and defend when each flavor of polymorphism is the right tool.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Polymorphism | polymorphism in depth, overloading (compile-time), overriding/virtual functions (runtime), vtable & dispatch internals, covariant returns & ad-hoc/subtype/parametric | Define polymorphism + 4 categories, apply overload resolution rules, use `virtual`/`@Override` correctly, explain vtable dispatch + devirtualization, use covariant returns and pick the right polymorphism kind |

## Study order
1. **ch-01** is the whole part — read its five sections in order: concept → compile-time → runtime → internals → advanced forms.
2. Section 04 (vtable internals) is the "depth" section — FAANG interviewers love it.
3. Section 05 ties the categories together and is the perfect capstone before Part 05.
4. Assumes **Part 03 (Inheritance)** — overriding and `super` are prerequisites.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — polymorphism is the pillar that powers design patterns, DI, and framework extension; vtable questions are a C++/Java system-design classic.
- **Emphasized by**: every SDE loop (Meta, Google, Amazon, Microsoft); C++ systems teams (Bloomberg, NVIDIA, Apple, trading firms) probe vtable/overloading in depth; Java teams ask override-resolution and `Object`-polymorphism questions.
- Typical asked: "What is polymorphism?", "Overloading vs overriding?", "How does dynamic dispatch work?", "What is a vtable?", "Can you overload on return type?", "What does `virtual` do in C++?", "What are covariant return types?".

## How the parts connect (roadmap)
- Polymorphism is the runtime payoff of **Part 03's** inheritance (overriding) and **Part 02's** abstraction (interfaces).
- **Part 05** relationships and **Part 06 SOLID** (OCP, LSP, DIP) are *built on* polymorphism — LSP is literally "subtypes must be polymorphically safe."
- After this part you have the complete four-pillar picture; design-pattern rounds assume you can say "Strategy uses interface polymorphism; Template Method uses overriding; Visitor uses double dispatch."
