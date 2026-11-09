# Phase 7 — Practical TypeScript Mastery Projects

> Build the language, not just read it. Each project is TypeScript-only: types, generics, classes, modules, and compiler behavior.

## Projects

| # | Project | Level | Core skills |
| --- | --- | --- | --- |
| 01 | [Strongly Typed Utility Library](./project-01-typed-utility-library/README.md) | Beginner → Intermediate | Strict signatures, generics, guards, exports |
| 02 | [Advanced Type Utility Library](./project-02-advanced-type-utility-library/README.md) | Intermediate → Advanced | Mapped/conditional/recursive types |
| 03 | [Type-Safe State Management Engine](./project-03-type-safe-state-management/README.md) | Advanced | Discriminated unions, reducers, selectors |
| 04 | [Type-Safe Event System](./project-04-type-safe-event-system/README.md) | Advanced | Event maps, typed payloads, emitter contracts |
| 05 | [Type-Safe Configuration Engine](./project-05-type-safe-configuration-engine/README.md) | Expert | Nested config types, overrides, inference |
| 06 | [Type-Safe Schema and Validation Library](./project-06-schema-and-validation-library/README.md) | Expert | Runtime validation + `Infer<S>` |
| 07 | [Production-Grade TypeScript Library](./project-07-production-grade-library/README.md) | Expert / Industrial | Declarations, type tests, perf, versioning |

## Rules for every project

1. `"strict": true` plus the extra-safety flags from Module 25.
2. No `any`. Use `unknown` at boundaries and narrow.
3. Public API is typed first; implementation follows.
4. Add compile-time tests (`expect-type` or `@ts-expect-error`).
5. Export only what consumers need.
6. Document each public type with a one-line comment.

## Suggested workflow

```bash
mkdir my-project && cd my-project
npm init -y
npm i -D typescript expect-type
npx tsc --init --strict --noUncheckedIndexedAccess --exactOptionalPropertyTypes
mkdir src test
```

Start with [Project 01](./project-01-typed-utility-library/README.md).
