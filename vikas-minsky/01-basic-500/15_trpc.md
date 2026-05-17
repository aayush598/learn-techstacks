## 15. tRPC (406–420)

406. What is tRPC?
     t**Answer:** tRPC is a TypeScript RPC framework that enables end-to-end type-safe API calls without code generation or schema definitions. It infers types from your backend procedures and provides fully typed client calls with autocompletion.

407. Why use tRPC over REST?
     t**Answer:** tRPC eliminates manual API client code, provides automatic type inference from server to client, catches API contract violations at compile time, and reduces boilerplate. REST requires manual client types, documentation, and validation.

408. Explain end-to-end type safety.
     E**Answer:** End-to-end type safety means type errors are caught at compile time across the entire stack — from database schema (via ORM) through server procedures to client calls. Changes in backend types immediately show as type errors in frontend code.

409. What are routers in tRPC?
     R**Answer:** Routers organize related procedures using `t.router({ ... })`. They can be nested for hierarchical APIs and merged with `mergeRouters`. The router defines the public API surface and is exported for client consumption.

410. Explain procedures.
     P**Answer:** Procedures are the building blocks of tRPC APIs, defined with `t.procedure` and chained methods. Each procedure receives input (validated), context, and returns typed output. Procedures can be queries (GET) or mutations (POST).

411. Difference between query and mutation?
     Q**Answer:** Queries fetch data without side effects (GET semantics), support caching via `@tanstack/react-query`, and are idempotent. Mutations modify data (POST/PUT/DELETE semantics), trigger cache invalidation, and handle optimistic updates.

412. Explain middleware in tRPC.
     M**Answer:** Middleware wraps procedure execution, running before and after the handler. It's used for authentication, logging, rate limiting, or request transformation. Middleware has access to context and can modify it for downstream procedures.

413. How does context work?
     C**Answer:** Context is created per-request and passed to all procedures. The `createContext` function (runs on each request) provides request-specific data like user session, database connection, and request headers to procedures.

414. Explain Zod integration.
     Z**Answer:** Zod schemas define input validation for procedures via `.input(z.object({...}))`. tRPC automatically validates inputs, infers types for both client and server, and provides type-safe error messages. Complex validation with refinements and transformations is supported.

415. How does authentication work?
     A**Answer:** Authentication uses middleware that extracts tokens from headers/cookies, verifies them, and injects user info into context. Unauthenticated requests return errors or redirect. Authentication logic is centralized in middleware rather than per-procedure.

416. Explain subscriptions.
     S**Answer:** Subscriptions enable real-time bidirectional communication via WebSockets. Clients subscribe to events using `useSubscription`, and servers push updates through iterator/yield patterns. Built on top of WebSockets with reconnection handling.

417. How does batching work?
     t**Answer:** tRPC automatically batch-fetches multiple queries made in the same microtask into a single HTTP request using its `httpBatchLink`. This reduces network round trips and is particularly beneficial during initial page loads.

418. Explain error formatting.
     E**Answer:** Error formatting transforms thrown errors into structured responses extended via the `mapError` option. It provides consistent error shapes across procedures, with support for custom error types, validation errors, and error codes.

419. What are tRPC limitations?
     L**Answer:** Limitations include: requires TypeScript on both client and server, less suitable for public APIs consumed by non-TypeScript clients, no built-in REST compatibility, and larger bundle size compared to bare REST calls.

420. How do you scale tRPC applications?
     S**Answer:** Scale by splitting into multiple routers by domain, using `mergeRouters` for composition, implementing caching layers, adding rate limiting middleware, using server-side rendering for initial data, and distributing procedures across microservices.
