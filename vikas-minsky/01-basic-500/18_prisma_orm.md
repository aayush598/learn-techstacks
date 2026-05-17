## 18. Prisma ORM (456–475)

456. What is Prisma ORM?
     P**Answer:** Prisma is an ORM for Node.js and TypeScript that simplifies database access. It provides a declarative schema language, auto-generated type-safe client, migration system, and a visual editor (Prisma Studio) for database management.

457. Explain Prisma schema.
     T**Answer:** The Prisma schema (`schema.prisma`) defines data sources (database connection), generators (Prisma Client), and models (tables). Models use a declarative syntax with fields, types, relations, attributes (`@id`, `@unique`, `@default`), and indexes.

458. How do migrations work in Prisma?
     P**Answer:** Prisma Migrate generates SQL migration files from schema changes using `prisma migrate dev`. Each migration is versioned and can be applied (`prisma migrate deploy`) or rolled back. The migration history tracks all schema changes.

459. Explain Prisma Client.
     P**Answer:** Prisma Client is an auto-generated type-safe query builder created from the schema. It provides methods like `prisma.user.findMany()`, `prisma.user.create()`, and `prisma.user.update()` with full TypeScript autocompletion and validation.

460. What are relations in Prisma?
     R**Answer:** Relations connect models via foreign keys, defined with `@relation` attribute. Types include one-to-one (`User ↔ Profile`), one-to-many (`User → Posts`), and many-to-many (implicit or explicit join tables). Prisma generates type-safe nested queries.

461. Explain transactions.
     P**Answer:** Prisma supports `prisma.$transaction([...])` for batched operations, `prisma.$transaction(async (tx) => {...})` for interactive transactions with savepoints, and nested writes within `create`/`update` for atomic operations on related records.

462. Difference between Prisma and Drizzle?
     P**Answer:** Prisma uses a declarative schema language and high-level ORM API with auto-generated client, making it easier for simple queries. Drizzle uses SQL-like syntax with finer control, smaller bundle size, and direct access to SQL for complex queries.

463. Explain nested writes.
     N**Answer:** Nested writes create or update related records in a single query using `create: { user: { connect: { id: 1 } } }` syntax. They support `create`, `connect`, `disconnect`, `set`, `update`, `upsert`, and `delete` for relational operations.

464. What are Prisma middlewares?
     M**Answer:** Middlewares (now deprecated in favor of client extensions) intercept queries for cross-cutting concerns like logging, soft deletes, rate limiting, or field encryption. They run before/after query execution and can modify params or results.

465. Explain Prisma indexing.
     I**Answer:** Indexes are defined in the schema with `@@index([field1, field2])` on models. They speed up queries on indexed columns. Composite indexes follow leftmost prefix rules, and `@@unique` creates unique constraints with optional indexes.

466. What are Prisma generators?
     G**Answer:** Generators extend Prisma's capabilities. The default `prisma-client-js` generates the client. Other generators include `prisma-dbml-generator` (visual diagrams), `zod-prisma-types` (Zod schemas), and `prisma-json-types-generator`.

467. Explain connection pooling.
     P**Answer:** Prisma uses connection pooling to manage database connections efficiently. With PgBouncer or Supabase's pooler, Prisma's `connectionLimit` controls pool size. Serverless environments use Data Proxy or Accelerate for scalable connection management.

468. What are Prisma performance pitfalls?
     P**Answer:** Pitfalls include: N+1 queries (solve with `include` or `select`), fetching unnecessary fields (always specify `select`), large result sets (paginate), missing indexes, and heavy relations in nested writes causing slow queries.

469. Explain raw SQL support.
     `**Answer:** `prisma.$queryRaw` executes raw SQL queries when Prisma's API is insufficient for complex queries. Returns typed results matching template literal interpolations. `$executeRaw` runs raw commands with typed parameters.

470. How does Prisma handle type safety?
     P**Answer:** Prisma generates TypeScript types from the schema during `prisma generate`. All queries are type-checked at compile time — invalid field names, wrong types, and incorrect relation queries are caught during development.

471. Explain soft deletes.
     S**Answer:** Soft deletes mark records as deleted (e.g., `deletedAt` timestamp) instead of removing them. Implemented via Prisma middleware/client extensions that add `where: { deletedAt: null }` to queries and set timestamp on delete.

472. What are cascading relations?
     C**Answer:** Cascading relations define behavior on parent delete: `onDelete: Cascade` automatically deletes related records, `SetNull` sets foreign keys to NULL, `Restrict` prevents deletion if related records exist, and `NoAction` leaves handling to the database.

473. Explain optimistic concurrency.
     O**Answer:** Optimistic concurrency prevents lost updates by checking a version field before updating. Prisma supports this via `@@version` fields or explicit checks — if another process modified the record, the update fails and must be retried.

474. How do you debug Prisma queries?
     D**Answer:** Debug by enabling `log: ['query', 'info', 'warn', 'error']` in Prisma Client config to see generated SQL. Use `prisma studio` for visual inspection, query timing with `withAccelerateInfo()`, and Prisma's event system for monitoring.

475. Explain scaling Prisma applications.
     S**Answer:** Scale with connection pooling for high traffic, query caching via Prisma Accelerate, read replicas for read-heavy workloads, pagination for large datasets, selective field fetching to reduce payload size, and database sharding for write scaling.
