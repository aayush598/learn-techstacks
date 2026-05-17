## 53. tRPC Expert Topics (1406–1420)

1406. How does procedure inference flow across layers?

   **Answer:** tRPC infers TypeScript types from procedure definitions (input schemas, output validation) and propagates them through routers, middleware, and client proxies. The client's `useQuery` or `useMutation` automatically knows input/output types.

1407. Explain router composition patterns.

   **Answer:** Router composition merges sub-routers using `t.router({})` merging, allowing domain-split organizations (usersRouter, postsRouter) combined into an appRouter. Composed routers preserve full type inference across the hierarchy.

1408. What are transport serialization constraints?

   **Answer:** tRPC serializes data over HTTP/JSON by default, which limits payloads to JSON-serializable types (no Date, Map, Set, or BigInt without custom transformers). SuperJSON or custom serializers extend supported types.

1409. Explain input parser performance optimization.

   **Answer:** Input parsing runs Zod validation on every request. For hot paths, validating with `.parse()` versus `.safeParse()` (which avoids exceptions) and caching schemas per procedure improves throughput under load.

1410. How does batching reduce API overhead?

   **Answer:** tRPC's HTTP batch merges multiple procedure calls into a single HTTP request using the `httpBatchLink`. This reduces round trips and TLS negotiation overhead, especially beneficial for initial page loads needing multiple data sources.

1411. Explain type-safe API federation.

   **Answer:** Type-safe federation merges multiple tRPC routers from different microservices into a unified API gateway. Each service exposes its procedures via a router, and the gateway composes them while preserving full client-side type safety.

1412. What are hybrid client-server validation flows?

   **Answer:** Hybrid validation runs Zod schemas both server-side (for security) and client-side (for UX). The same schema is shared via a monorepo package, ensuring validation consistency without duplicating rules.

1413. Explain websocket transport upgrades.

   **Answer:** tRPC supports upgrading from HTTP long-polling to WebSocket connections for subscriptions. The `wsLink` establishes a persistent connection that pushes realtime updates to the client without polling.

1414. How do subscriptions synchronize state?

   **Answer:** Subscriptions emit typed events from the server that the client receives and merges into TanStack Query's cache using `queryClient.setQueryData`. This keeps server-side state synchronized across all connected clients.

1415. Explain edge runtime compatibility.

   **Answer:** tRPC runs on edge runtimes (Cloudflare Workers, Vercel Edge) by using the `@trpc/client` adapter with `fetch`-based links. Edge compatibility requires avoiding Node.js-specific APIs and using platform adapters.

1416. What are backend/frontend contract guarantees?

   **Answer:** tRPC guarantees that the frontend can only call procedures defined by the backend, with type-checked inputs and outputs. Compilation fails if the client uses a non-existent procedure or passes wrong types.

1417. Explain auth propagation through routers.

   **Answer:** Auth middleware at the router level extracts user context from headers (JWT, session) and attaches it to the request context. Middleware can deny unauthorized access by throwing a TRPCError.

1418. How does tRPC simplify monorepos?

   **Answer:** tRPC eliminates separate API client generation—the server types are directly importable by the frontend package in a monorepo. This removes schema stubs, SDK generation scripts, and manual type alignment.

1419. What are tRPC scalability bottlenecks?

   **Answer:** Bottlenecks include JSON serialization overhead for large payloads, unbatched per-request HTTP overhead, Zod validation CPU cost on complex schemas, and middleware chains on heavily hit procedures.

1420. How do startups architect large tRPC systems?

   **Answer:** Startups architect large tRPC systems by splitting routers by domain, using middleware for cross-cutting concerns (auth, logging, rate limiting), batching with `httpBatchLink`, and adopting subscriptions for realtime features.
