# Chapter 10: Project Conventions & Coding Standards

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Naming Conventions](sec-01-naming-conventions.md) | Files (kebab-case), components (PascalCase), functions (camelCase), constants (UPPER_CASE), types (PascalCase) |
| 02 | [Folder Structure Standards](sec-02-folder-structure-standards.md) | Feature-based organization, colocation of tests, barrel exports, index files |
| 03 | [API Design Conventions](sec-03-api-design-conventions.md) | URL structure, HTTP methods, request/response format, error codes, pagination |
| 04 | [Component Development Standards](sec-04-component-development-standards.md) | One component per file, named exports, prop types, forwardRef, displayName |
| 05 | [Database Access Patterns](sec-05-database-access-patterns.md) | Repository pattern for Prisma, transaction usage, query optimization, N+1 prevention |
| 06 | [Error Handling Strategy](sec-06-error-handling-strategy.md) | Custom error classes, error boundaries, global error handler, user-facing messages |
| 07 | [Code Review Guidelines](sec-07-code-review-guidelines.md) | Review checklist, approval requirements, reviewer rotation, security review for sensitive changes |
| 08 | [Documentation Standards](sec-08-documentation-standards.md) | JSDoc for public APIs, README for packages, changelog maintenance, ADR for decisions |

---

## Key Takeaways

- Consistent naming: kebab-case for files, PascalCase for components/types, camelCase for functions
- Feature-based folder organization with colocated tests
- API design follows RESTful conventions with standardized error format
- Repository pattern for database access — never direct Prisma in controllers
- Custom error hierarchy with user-friendly messages
- Two-person review required for all PRs
- Architecture Decision Records (ADR) for significant design choices
