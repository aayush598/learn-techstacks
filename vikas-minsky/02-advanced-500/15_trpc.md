## 34. tRPC Advanced (906–920)

906. Explain transport-agnostic APIs.
   tRPC APIs work over HTTP, WebSocket, or any transport that passes serialized data. The same procedure definition runs regardless of transport, with adapters handling protocol-specific concerns.

907. How do procedures compose?
   Procedures compose by chaining middleware and input schemas. A public procedure could be: `publicProcedure.input(z.string()).query(...)`, and middleware can wrap multiple procedures with shared auth/validation logic.

908. Explain input parser pipelines.
   Input parsers run as middleware before procedure execution. tRPC chains parsers with `pipe()` or nested middleware, transforming and validating input through multiple stages (sanitize → validate → transform).

909. What are context propagation patterns?
   Context in tRPC is created per-request in the `createContext` function, injected into all procedures. Propagate user identity, database connections, and logging metadata; downstream middleware and procedures access it via `opts.ctx`.

910. Explain server-side batching.
   tRPC's `httpBatchLink` batches multiple procedure calls into a single HTTP request. The server processes each procedure independently but client-side latency is reduced by eliminating multiple round trips.

911. How does tRPC handle serialization?
   tRPC serializes procedure inputs and outputs using JSON.stringify/parse. Custom `transformer` (e.g., superjson) adds support for Date, Map, Set, and BigInt by encoding type metadata alongside values.

912. Explain websocket adapters.
   WebSocket adapters maintain persistent connections for subscriptions and real-time updates. They use `ws` or `uWebSockets.js` and support reconnection, keep-alive pings, and link-level state management.

913. What are API boundary concerns?
   Boundaries include input validation (Zod schemas), error serialization (tRPC's TRPCError codes), rate limiting at the adapter level, and security headers. tRPC manages serialization but transport security is handled separately.

914. Explain type inference propagation.
   tRPC infers client types from the server router definition using `inferRouterOutputs` and `inferRouterInputs`. The client's `createTRPCReact` provides fully typed hooks without any `type` imports.

915. How do middleware chains execute?
   Middleware executes as nested wrappers around procedures. `t.middleware()` returns a function that receives `opts.next`, called to pass control to the next middleware or the procedure itself.

916. Explain auth propagation in tRPC.
   Auth flows through context: middleware extracts JWT from headers, verifies it, and attaches user info to `ctx`. Protected procedures check `ctx.user`; `rejectUnauthorized` middleware throws TRPCError on failure.

917. What are scaling challenges with tRPC?
   Challenges include serialization overhead for large payloads, no built-in caching (must integrate TanStack Query), WebSocket connection management at scale, and type regeneration on every server change.

918. Explain client-side cache integration.
   tRPC integrates with TanStack Query via `@trpc/tanstack-react-query`. Each tRPC procedure maps to a query/mutation with automatic cache keys based on input, enabling stale-while-revalidate patterns.

919. What are monorepo advantages for tRPC?
   Monorepos share TypeScript types between server and client without package publishing. The router is in a shared package, and both server and client import it directly, ensuring type sync.

920. Explain hybrid REST+tRPC architectures.
   Hybrid architectures expose tRPC for first-party app communication (typed, efficient) and REST endpoints for third-party APIs, webhooks, or integrations. NestJS or a gateway can route between both interfaces.
