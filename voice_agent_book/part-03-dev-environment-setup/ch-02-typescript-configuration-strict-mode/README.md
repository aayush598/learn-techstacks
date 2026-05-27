# Chapter 02: TypeScript Configuration & Strict Mode

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Strict Mode Configuration](sec-01-strict-mode-configuration.md) | strict: true, noUncheckedIndexedAccess, exactOptionalPropertyTypes, all strict flags |
| 02 | [Path Aliases & Module Resolution](sec-02-path-aliases-module-resolution.md) | @/ for source files, @voice-agent/ for packages, barrel exports, index files |
| 03 | [Shared Type Definitions](sec-03-shared-type-definitions.md) | Domain types in packages/types, API contracts, database types (Prisma-generated) |
| 04 | [Generic & Utility Types](sec-04-generic-utility-types.md) | AsyncReturnType, DeepPartial, PaginatedResponse, ApiResponse, Result<T,E> |
| 05 | [Type Safety Patterns](sec-05-type-safety-patterns.md) | Branded types for IDs, discriminated unions for states, template literals for routes |
| 06 | [Declaration Files & Ambient Types](sec-06-declaration-files-ambient-types.md) | Global types, process.env typing, module declarations, browser API types |
| 07 | [TypeScript & Prisma Integration](sec-07-typescript-prisma-integration.md) | Generated types, type overrides, input types, select/include type inference |

---

## Key Takeaways

- Full strict mode enabled for maximum type safety
- Path aliases (@) for clean imports within apps
- Shared types package for cross-service type contracts
- Branded types (type Brand<T, B> = T & { __brand: B }) for IDs
- Discriminated unions for state machine states
- Prisma-generated types used directly for database operations
- noUncheckedIndexedAccess prevents undefined array access
