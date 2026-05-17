## 37. Prisma ORM Advanced (956–975)

956. Explain Prisma query engine internals.
   Prisma's query engine is a Rust binary embedded in the Node.js client. It receives query JSON over TypeScript, generates optimal SQL, and returns typed results. The engine handles relation loading, transactions, and connection pooling.

957. How does Prisma generate clients?
   `prisma generate` reads the schema, builds an AST, and generates TypeScript types and a JavaScript client with fully typed models, enums, and operations using Prisma's internal generator.

958. Explain relation batching.
   Prisma batches relation queries by collecting foreign keys and issuing `WHERE id IN (...)` queries. This avoids N+1 patterns for nested reads when using `include` or `select` with relations.

959. What are N+1 query problems?
   N+1 occurs when Prisma issues one query for the parent and one per child. Prisma's built-in batching mitigates this for `include` queries, but raw queries or custom resolvers may still exhibit it.

960. Explain dataloader strategies.
   Dataloader batches and caches database requests per request cycle. Prisma's query engine does similar batching internally; for GraphQL, use dataloader + Prisma to coalesce nested resolver calls.

961. How do Prisma transactions retry?
   `prisma.$transaction` with the interactive API automatically retries on serialization failures (deadlock, write conflict). Configure `maxRetries` and `timeout` to balance reliability and latency.

962. Explain Prisma middleware chains.
   Middleware (now called "client extensions") run on query lifecycle events. `$use` hooks (deprecated) are replaced by `$extends` with `query` methods that intercept and modify queries or results.

963. What are schema drift problems?
   Schema drift occurs when the database schema differs from the Prisma schema (manual SQL changes, migration conflicts). `prisma db pull` syncs schema from the database; `prisma migrate diff` detects drift.

964. Explain shadow databases.
   Shadow databases are temporary databases used during `prisma migrate dev` to detect schema changes. Prisma applies migrations to the shadow DB and compares it with the schema to generate new migrations.

965. How do Prisma migrations lock tables?
   Prisma's `migrate deploy` acquires a lock on the `_prisma_migrations` table. Long-running migrations block other migration attempts, but the lock is per-environment and doesn't affect application tables.

966. Explain relation mode configurations.
   Relation mode (`foreignKeys` or `prisma`) controls how relations are enforced. `foreignKeys` uses DB foreign keys; `prisma` manages relations in the application layer (useful for MongoDB or PlanetScale).

967. What are interactive transactions?
   Interactive transactions (`prisma.$transaction(async (tx) => { ... })`) give explicit control over transaction boundaries. Multiple queries execute atomically, with manual commit/rollback.

968. Explain Prisma in serverless environments.
   Prisma in serverless faces cold-start latency from query engine binary loading. Mitigate with data proxy (Prisma Accelerate), connection pooling (PgBouncer in transaction mode), and optimal binary targets.

969. How does Prisma handle pooling limitations?
   Prisma's query engine manages connections via `connectionLimit` in the datasource URL. In serverless, high concurrency may exhaust connections; use external poolers like PgBouncer or Prisma Accelerate.

970. Explain query optimization techniques.
   Optimize by selecting only needed fields (not `select *`), using `raw` for complex queries, adding indexes based on query patterns, enabling `previewFeatures = ["referentialIntegrity"]` for performance, and analyzing with `explain`.

971. What are ORM overfetching issues?
   Overfetching loads unnecessary columns or rows. Prisma's `select` solves column overfetching; `take`, `skip`, and `where` solve row overfetching. Always query only the data needed for the specific view.

972. Explain soft migration strategies.
   Soft migrations sequence schema changes to avoid downtime: add nullable columns first, backfill data, make columns required, then drop old columns in separate deploys.

973. What are Prisma deployment pitfalls?
   Pitfalls include using `migrate dev` in production (use `migrate deploy`), forgetting to run `generate` after schema changes, version mismatch between client and engine, and unhandled connection pool exhaustion.

974. Explain observability for ORM queries.
   Enable query logging via Prisma's `log: ['query', 'info']` in the datasource, use APM tools (Datadog, OpenTelemetry) to trace query performance, and monitor `prisma:query` events for slow queries.

975. How do you scale Prisma in enterprise apps?
   Scale with read replicas (configure separate datasource URLs), query caching (Redis for read-heavy data), proper connection pooling, efficient relation loading, and moving aggregated/queries to raw SQL for reporting.
