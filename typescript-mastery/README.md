# TypeScript Mastery — Beginner to Expert

A code-first, production-grade TypeScript curriculum. **35 modules**, **300+ topics**, **7 practical projects**.

> Rule of this repo: **read less, run more.** Every topic is taught with runnable examples, compiler-error annotations (`// ❌`), correct patterns (`// ✅`), and a short "why".

---

## How to use this repo

1. Follow the phases in order. Advanced type-system modules depend on earlier ones.
2. Open a topic file, read the `TL;DR`, then read the code top-to-bottom.
3. Copy examples into a scratch file and compile with `tsc --strict --noEmit`.
4. Break the examples on purpose. Read the real compiler error. Fix it.
5. Finish each phase with its projects under `phase-07-projects/`.

```bash
# one-time setup for experimenting with any example
mkdir ts-scratch && cd ts-scratch
npm init -y
npm i -D typescript
npx tsc --init --strict
npx tsc --noEmit
```

---

## The learning structure

| Phase | Modules | Focus | Directory |
| --- | --- | --- | --- |
| 1 | 01–07 | Foundations and core language | [`phase-01-foundations`](./phase-01-foundations/README.md) |
| 2 | 08–13 | Intermediate TypeScript | [`phase-02-intermediate`](./phase-02-intermediate/README.md) |
| 3 | 14–20 | Advanced type system | [`phase-03-advanced-type-system`](./phase-03-advanced-type-system/README.md) |
| 4 | 21–24 | Expert type engineering | [`phase-04-expert-engineering`](./phase-04-expert-engineering/README.md) |
| 5 | 25–30 | Production-grade practices | [`phase-05-production`](./phase-05-production/README.md) |
| 6 | 31–35 | Expert specialization | [`phase-06-expert-specialization`](./phase-06-expert-specialization/README.md) |
| 7 | Projects 1–7 | Practical mastery | [`phase-07-projects`](./phase-07-projects/README.md) |

---

## Module index

### Phase 1 — Foundations
- [Module 01 — Introduction to TypeScript](./phase-01-foundations/module-01-introduction-to-typescript/README.md)
- [Module 02 — Installation and Compiler Fundamentals](./phase-01-foundations/module-02-installation-and-compiler-fundamentals/README.md)
- [Module 03 — Basic Types](./phase-01-foundations/module-03-basic-types/README.md)
- [Module 04 — Variables, Constants, and Type Inference](./phase-01-foundations/module-04-variables-constants-and-inference/README.md)
- [Module 05 — Functions](./phase-01-foundations/module-05-functions/README.md)
- [Module 06 — Object Types and Object Properties](./phase-01-foundations/module-06-object-types/README.md)
- [Module 07 — Interfaces and Type Aliases](./phase-01-foundations/module-07-interfaces-and-type-aliases/README.md)

### Phase 2 — Intermediate
- [Module 08 — Union and Intersection Types](./phase-02-intermediate/module-08-union-and-intersection-types/README.md)
- [Module 09 — Type Narrowing and Type Guards](./phase-02-intermediate/module-09-narrowing-and-type-guards/README.md)
- [Module 10 — Type Assertions and Type Safety](./phase-02-intermediate/module-10-type-assertions-and-safety/README.md)
- [Module 11 — Generics](./phase-02-intermediate/module-11-generics/README.md)
- [Module 12 — Classes](./phase-02-intermediate/module-12-classes/README.md)
- [Module 13 — Enums and Literal-Based Alternatives](./phase-02-intermediate/module-13-enums-and-literal-alternatives/README.md)

### Phase 3 — Advanced type system
- [Module 14 — Type Operators and Type Manipulation](./phase-03-advanced-type-system/module-14-type-operators/README.md)
- [Module 15 — Mapped Types](./phase-03-advanced-type-system/module-15-mapped-types/README.md)
- [Module 16 — Conditional Types](./phase-03-advanced-type-system/module-16-conditional-types/README.md)
- [Module 17 — Template Literal Types](./phase-03-advanced-type-system/module-17-template-literal-types/README.md)
- [Module 18 — Tuple Types and Advanced Array Typing](./phase-03-advanced-type-system/module-18-tuples-and-arrays/README.md)
- [Module 19 — Utility Types (Built-in and Custom)](./phase-03-advanced-type-system/module-19-utility-types/README.md)
- [Module 20 — Advanced Type Modeling and Type-Level Programming](./phase-03-advanced-type-system/module-20-type-level-programming/README.md)

### Phase 4 — Expert engineering
- [Module 21 — Advanced Type Safety and Modeling Patterns](./phase-04-expert-engineering/module-21-advanced-type-safety/README.md)
- [Module 22 — Declarations and Declaration Files](./phase-04-expert-engineering/module-22-declarations-and-declaration-files/README.md)
- [Module 23 — Modules and Package API Design](./phase-04-expert-engineering/module-23-modules-and-package-api-design/README.md)
- [Module 24 — Compiler and Language Internals](./phase-04-expert-engineering/module-24-compiler-and-language-internals/README.md)

### Phase 5 — Production
- [Module 25 — Strict TypeScript and Maximum Type Safety](./phase-05-production/module-25-strict-typescript/README.md)
- [Module 26 — Maintainable TypeScript Coding Standards](./phase-05-production/module-26-coding-standards/README.md)
- [Module 27 — Scalable TypeScript Project Organization](./phase-05-production/module-27-project-organization/README.md)
- [Module 28 — TypeScript Testing and Type Verification](./phase-05-production/module-28-testing-and-type-verification/README.md)
- [Module 29 — TypeScript Performance and Compiler Optimization](./phase-05-production/module-29-performance/README.md)
- [Module 30 — Versioning, Migration, and Long-Term Maintenance](./phase-05-production/module-30-versioning-and-migration/README.md)

### Phase 6 — Expert specialization
- [Module 31 — Advanced TypeScript Design Patterns](./phase-06-expert-specialization/module-31-advanced-design-patterns/README.md)
- [Module 32 — Advanced Type System Edge Cases](./phase-06-expert-specialization/module-32-type-system-edge-cases/README.md)
- [Module 33 — TypeScript API and Library Design](./phase-06-expert-specialization/module-33-api-and-library-design/README.md)
- [Module 34 — Compiler API and Custom Tooling](./phase-06-expert-specialization/module-34-compiler-api-and-tooling/README.md)
- [Module 35 — Production Readiness and Engineering Standards](./phase-06-expert-specialization/module-35-production-readiness/README.md)

### Phase 7 — Projects
- [Project 01 — Strongly Typed Utility Library](./phase-07-projects/project-01-typed-utility-library/README.md)
- [Project 02 — Advanced Type Utility Library](./phase-07-projects/project-02-advanced-type-utility-library/README.md)
- [Project 03 — Type-Safe State Management Engine](./phase-07-projects/project-03-type-safe-state-management/README.md)
- [Project 04 — Type-Safe Event System](./phase-07-projects/project-04-type-safe-event-system/README.md)
- [Project 05 — Type-Safe Configuration Engine](./phase-07-projects/project-05-type-safe-configuration-engine/README.md)
- [Project 06 — Type-Safe Schema and Validation Library](./phase-07-projects/project-06-schema-and-validation-library/README.md)
- [Project 07 — Production-Grade TypeScript Library](./phase-07-projects/project-07-production-grade-library/README.md)

---

## The 7-level mastery standard

Use this for **every** topic:

1. **Understand** — what it is and why it exists.
2. **Syntax** — rules and variations.
3. **Examples** — simple → complex.
4. **Internals** — compiler behavior, inference, compatibility, limits.
5. **Practical application** — where it belongs in real code.
6. **Best practices** — readability, alternatives, trade-offs.
7. **Production implementation** — build, test, refactor, document.

---

## Learning rules

1. Never skip fundamentals to reach advanced generics.
2. Never memorize utility types without understanding their definitions.
3. Know the difference between compile-time and runtime guarantees.
4. Prefer simple types over clever types.
5. Use `strict` in every practice project.
6. Understand every compiler error instead of suppressing it.
7. Avoid `any` unless clearly justified.
8. Design types that make invalid states hard to represent.
9. Refactor types without breaking contracts.
10. Consider compiler performance when designing type-level abstractions.

---

## File conventions used in this repo

| Convention | Meaning |
| --- | --- |
| `// ✅` | Correct / recommended pattern |
| `// ❌` | Compiler error or unsafe pattern |
| `// Error:` | Exact-ish compiler diagnostic |
| `// =>` | Inferred type or runtime result |
| `type _ = ...` | Compile-time assertion trick |
| `@ts-expect-error` | Used only to *test* that an error occurs |

---

## Completion criteria

You are production-grade when you can independently:

- Design complex type systems and reusable generic abstractions.
- Read and write conditional, mapped, template-literal, and recursive types.
- Build custom utility-type libraries and strongly typed APIs.
- Write and maintain declaration files.
- Configure the compiler and organize large codebases.
- Diagnose inference problems and optimize compiler performance.
- Evolve public type contracts without breaking consumers.
- Set and enforce team-wide TypeScript standards.

> Mastering TypeScript is not writing the most complicated types. It is expressing the **necessary constraints** with the **simplest, clearest, most reliable types**.
