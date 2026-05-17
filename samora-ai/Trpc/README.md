# tRPC Interview Questions and Answers

## Q1: What is tRPC?
**A:** tRPC (TypeScript Remote Procedure Call) is a framework for building fully typesafe APIs without code generation or schema definitions. It allows you to define procedures on the server and call them directly from the client with full TypeScript inference.

## Q2: How does tRPC work?
**A:** tRPC uses TypeScript's type system to infer the types of your server procedures and expose them to the client. The server defines routers with procedures, and the client imports the type of the router to get end-to-end type safety.

## Q3: How does tRPC differ from REST?
**A:** In REST, you define resources and endpoints with specific HTTP verbs, and the client manually constructs URLs and parses responses. tRPC abstracts away HTTP details and lets you call server functions directly from the client with full type safety.

## Q4: How does tRPC differ from GraphQL?
**A:** GraphQL requires a schema definition language, resolvers, and a query language on the client. tRPC uses TypeScript types as the single source of truth, eliminating the need for code generation or separate schema files.

## Q5: What are procedures in tRPC?
**A:** Procedures are the building blocks of a tRPC API. They represent individual endpoints and come in three types: queries (for fetching data), mutations (for modifying data), and subscriptions (for real-time data streams).

## Q6: What is a query procedure?
**A:** A query procedure is used to fetch data without side effects. It maps to HTTP GET requests by default and can be cached on the client side using React Query.

## Q7: What is a mutation procedure?
**A:** A mutation procedure is used to create, update, or delete data. It maps to HTTP POST requests by default and is not cached by the client.

## Q8: What is a subscription procedure?
**A:** A subscription procedure establishes a persistent WebSocket connection between the client and server, allowing the server to push real-time updates to the client.

## Q9: What is a router in tRPC?
**A:** A router is an object that groups related procedures together. Routers can be nested and merged to create a hierarchical API structure, similar to Express routers or NestJS modules.

## Q10: How do you create a tRPC router?
**A:** You use the `t.router()` method from the tRPC server instance, passing an object where keys are procedure names and values are procedure definitions created with `t.procedure.query()` or `t.procedure.mutation()`.

## Q11: What is middleware in tRPC?
**A:** Middleware in tRPC are functions that run before or after a procedure executes. They can modify the context, check authentication, log requests, or enforce rate limits. Middleware can be applied globally or per-router.

## Q12: How do you create a middleware in tRPC?
**A:** You call `t.middleware()` with a function that receives an object with `ctx`, `input`, `type`, `path`, `rawInput`, and `next`. The `next()` function continues execution, and you can pass modified context to it.

## Q13: What is context in tRPC?
**A:** Context is an object created per request that is available to all procedures and middleware. It typically contains request-specific data like the authenticated user, database session, or request headers.

## Q14: How do you create context in tRPC?
**A:** You pass a `createContext` function when creating the tRPC server instance. This function receives the request and response objects and returns an object that becomes available to all procedures.

## Q15: What is input validation in tRPC?
**A:** Input validation ensures that the data received by a procedure matches the expected schema. tRPC integrates with Zod and other validation libraries to parse and validate inputs before the procedure runs.

## Q16: How do you use Zod with tRPC?
**A:** You use `.input()` on a procedure definition with a Zod schema. The input will be validated and typed automatically, and the client will infer the input type from the schema.

## Q17: How do you handle errors in tRPC?
**A:** tRPC provides a `TRPCError` class that allows you to throw typed errors with specific codes like `UNAUTHORIZED`, `NOT_FOUND`, `BAD_REQUEST`, and `INTERNAL_SERVER_ERROR`. These errors are serialized and sent to the client.

## Q18: What is error formatting in tRPC?
**A:** Error formatting allows you to customize how errors are serialized before being sent to the client. You can use `formatError` in the router configuration to transform `TRPCError` instances into custom shapes.

## Q19: What HTTP methods does tRPC use?
**A:** By default, query procedures use HTTP GET requests, mutation procedures use HTTP POST requests, and subscriptions use WebSocket connections. These can be customized with links on the client side.

## Q20: How does tRPC handle GET requests for queries?
**A:** Query procedures are sent as GET requests with input serialized as query parameters. This enables browser caching, request deduplication, and link prefetching out of the box.

## Q21: How does tRPC handle POST requests for mutations?
**A:** Mutations use HTTP POST requests with the input serialized in the request body. This prevents caching and ensures mutations always execute on the server.

## Q22: What is the tRPC client?
**A:** The tRPC client is a strongly typed client that connects to a tRPC server. You create it with `createTRPCClient` and pass the server URL and a links array. The client provides fully typed `query`, `mutation`, and `subscription` methods.

## Q23: How do you set up a tRPC client?
**A:** You call `createTRPCClient` with a `links` array containing at least an `httpBatchLink` or `httpLink` pointing to your server URL. The client type is inferred from the server's router type.

## Q24: What is the difference between httpLink and httpBatchLink?
**A:** `httpLink` sends one HTTP request per procedure call, while `httpBatchLink` batches multiple procedure calls into a single HTTP request, reducing network overhead and improving performance.

## Q25: How does request batching work in tRPC?
**A:** When using `httpBatchLink`, multiple procedure calls made within the same microtask are collected and sent as a single HTTP POST request. The server processes each procedure and returns an array of responses.

## Q26: What is the splitLink in tRPC?
**A:** `splitLink` is used to conditionally route requests to different links based on the procedure type or path. For example, you can use `httpBatchLink` for queries and `wsLink` for subscriptions.

## Q27: How do you integrate tRPC with React Query?
**A:** tRPC provides `@trpc/react-query` which wraps React Query hooks. You create a `trpc` client using `createTRPCReact` and use hooks like `trpc.someQuery.useQuery()` and `trpc.someMutation.useMutation()`.

## Q28: What is createTRPCReact?
**A:** `createTRPCReact` is a function from `@trpc/react-query` that creates a strongly typed tRPC client for React. It returns an object with React hooks that mirror your server procedures.

## Q29: How do you set up the tRPC provider in React?
**A:** You wrap your app with the `<TRPCProvider>` component generated by `createTRPCReact`, passing the tRPC client and a QueryClient for React Query.

## Q30: How do you use useQuery in tRPC?
**A:** Call `trpc.procedureName.useQuery(input)` where `procedureName` is a query procedure on your router and `input` is the validated input. The hook returns `{ data, isLoading, error }` like React Query.

## Q31: How do you use useMutation in tRPC?
**A:** Call `trpc.procedureName.useMutation()` which returns a mutation object with `mutate` and `mutateAsync` methods. Pass input to `mutate(input)` and handle the response or error.

## Q32: How do you use useSubscription in tRPC?
**A:** Call `trpc.procedureName.useSubscription(input, { onData, onError, onComplete })` to subscribe to real-time updates from the server. The subscription is automatically cleaned up on unmount.

## Q33: How do you invalidate queries in tRPC?
**A:** Use `trpc.useContext()` to access the tRPC context, then call `context.procedureName.invalidate()` to refetch specific queries, or `context.invalidate()` to invalidate all queries.

## Q34: How do you integrate tRPC with Next.js App Router?
**A:** You set up the tRPC server in a route handler file (e.g., `app/api/trpc/[trpc]/route.ts`) and create the client in a provider component. The server adapter handles requests and responses for the App Router.

## Q35: How do you integrate tRPC with Next.js Pages Router?
**A:** You create an API route at `pages/api/trpc/[trpc].ts` using `@trpc/next` adapter, which creates a Next.js API handler that delegates to your tRPC router.

## Q36: What is the @trpc/next adapter?
**A:** `@trpc/next` provides utilities for integrating tRPC with Next.js, including the API handler, SSR helpers, and a `withTRPC` HOC that wraps your app with the tRPC provider.

## Q37: How do you do SSR with tRPC in Next.js?
**A:** You use `trpcClient.dehydrate()` and pass the dehydrated state to the page's props. The client can prefetch queries during SSR using `serverHelpers.prefetchQuery()`.

## Q38: How do you do SSG with tRPC in Next.js?
**A:** You use `getStaticProps` to prefetch queries using the server-side tRPC helpers. The data is dehydrated and passed to the client, enabling static generation with dynamic data.

## Q39: What is a tRPC server instance?
**A:** A tRPC server instance is created with `initTRPC.create()` and provides methods to create routers, procedures, and middleware. It can be configured with a context type and optionally a meta type.

## Q40: How do you define a tRPC procedure with input?
**A:** Call `t.procedure.input(zodSchema).query(({ input }) => {...})` or `.mutation(...)`. The input is validated at runtime and the TypeScript type is inferred from the Zod schema.

## Q41: How do you define a tRPC procedure without input?
**A:** Call `t.procedure.query(() => {...})` or `t.procedure.mutation(() => {...})` without the `.input()` chain. The procedure receives no typed input but can still access context.

## Q42: What are procedure metadata in tRPC?
**A:** Procedure metadata is arbitrary data attached to a procedure definition using `.meta({...})`. It can be accessed in middleware via `opts.meta`, enabling patterns like permission flags or rate limit configs.

## Q43: How do you merge routers in tRPC?
**A:** Use `t.mergeRouters(router1, router2)` to combine multiple routers into one. Alternatively, you can nest routers by passing a router object as a property value when creating a parent router.

## Q44: How do you nest routers in tRPC?
**A:** When creating a router, set a property to another router instance. The nested router's procedures become accessible at a path like `parentRouter.nestedRouter.procedureName`.

## Q45: What is the recommended file structure for tRPC?
**A:** A common structure is `server/trpc.ts` (init), `server/context.ts` (context), `server/routers/` (individual routers), `server/routers/_app.ts` (root router), and `server/routers/post.ts`, `server/routers/user.ts`, etc.

## Q46: How do you handle authentication in tRPC middleware?
**A:** Create a middleware that checks for an authenticated user in the context. If the user is not found, throw a `TRPCError` with code `UNAUTHORIZED`. Apply this middleware to protected procedures.

## Q47: How do you implement authorization in tRPC?
**A:** Use middleware to check user roles or permissions against procedure metadata. For example, check if `ctx.user.role` matches the required role stored in `opts.meta.allowedRoles`.

## Q48: How do you implement rate limiting in tRPC?
**A:** Create a middleware that tracks request counts per user or IP using an in-memory store or Redis. If the limit is exceeded, throw a `TOO_MANY_REQUESTS` `TRPCError`.

## Q49: How do you set up a tRPC server with Express?
**A:** Use `@trpc/server/adapters/express` which exports `createExpressMiddleware`. Pass your router and context function to create middleware that you mount on an Express app.

## Q50: How do you set up a tRPC server with Fastify?
**A:** Use `@trpc/server/adapters/fastify` which exports `fastifyTRPCPlugin`. Register the plugin on your Fastify instance and pass your router and createContext function.

## Q51: How do you set up a tRPC server with Next.js?
**A:** Use `@trpc/next` adapter or create a route handler for the App Router. The API route imports your app router and creates a handler that processes incoming requests.

## Q52: How do you set up a tRPC server with AWS Lambda?
**A:** Use `@trpc/server/adapters/aws-lambda` which provides `createLambdaHandler`. Export the handler from your Lambda function entry point, passing your router and context function.

## Q53: What is superjson and why use it with tRPC?
**A:** superjson is a data serialization library that supports types like Date, Map, Set, and BigInt that JSON does not natively handle. tRPC uses it as a data transformer to preserve these types across the wire.

## Q54: How do you configure a data transformer in tRPC?
**A:** Pass a `transformer` option to `initTRPC.create()` with a transformer object (like superjson) that implements `serialize` and `deserialize` methods.

## Q55: How do you configure superjson on the tRPC client?
**A:** Pass the same transformer in the `TRPCLink` configuration. For `httpBatchLink`, set `transformer: superjson` in the link options. Both client and server must use the same transformer.

## Q56: What are tRPC adapter functions?
**A:** Adapter functions bridge tRPC with different HTTP frameworks. They take a router, context creator, and framework-specific request/response objects, and return framework-compatible handlers.

## Q57: What is the tRPC panel?
**A:** The tRPC Panel is a development tool that provides a visual interface for exploring and testing your tRPC API, similar to GraphQL's GraphiQL or REST's Swagger UI.

## Q58: How do you enable CORS in tRPC?
**A:** CORS is not handled by tRPC itself; you configure it on your HTTP framework. For Express, use the `cors` middleware. For Next.js, set CORS headers in the API route or middleware.

## Q59: What is the difference between tRPC v10 and v11?
**A:** tRPC v11 introduced a new links-based client architecture, improved subscription handling, better error formatting, and deprecated the legacy client. It also added support for the OpenAPI plugin.

## Q60: What is the @trpc/client package?
**A:** `@trpc/client` provides the client-side utilities for tRPC, including `createTRPCClient`, link implementations (`httpLink`, `httpBatchLink`, `wsLink`, `splitLink`), and the `TRPCClientError` class.

## Q61: What is the @trpc/server package?
**A:** `@trpc/server` provides the server-side utilities for tRPC, including `initTRPC`, `TRPCError`, router and procedure builders, middleware helpers, and HTTP framework adapters.

## Q62: What is the @trpc/react-query package?
**A:** `@trpc/react-query` integrates tRPC with React Query, providing React hooks (`useQuery`, `useMutation`, `useSubscription`) that are fully typed based on your router definition.

## Q63: What is the @trpc/next package?
**A:** `@trpc/next` provides Next.js-specific integrations including the API route handler, SSR/SSG helpers, and the `withTRPC` higher-order component for the Pages Router.

## Q64: What is the @trpc/next/app-router package?
**A:** `@trpc/next/app-router` provides utilities for using tRPC with Next.js 13+ App Router, including server component helpers and client provider components.

## Q65: What is tree-shaking in tRPC?
**A:** Tree-shaking in tRPC refers to the practice of only importing the procedures you use on the client. By importing specific router types, unused procedures are not included in the client bundle.

## Q66: How do you handle file uploads in tRPC?
**A:** File uploads are typically handled outside of tRPC using the HTTP framework directly, since tRPC procedures expect JSON-serializable input. You can return a signed upload URL or handle the upload in a separate endpoint.

## Q67: How do you handle pagination in tRPC?
**A:** Implement cursor-based or offset-based pagination by defining input schemas with `cursor` or `skip`/`take` fields. Return paginated results with a cursor for the next page.

## Q68: How do you handle caching in tRPC?
**A:** tRPC leverages React Query's caching mechanisms. Queries are cached by default with configurable `staleTime` and `cacheTime`. For HTTP-level caching, set cache headers in your procedure's response.

## Q69: How do you do optimistic updates in tRPC?
**A:** Use `useMutation` with `onMutate` to update the cache optimistically, and `onError` to roll back if the mutation fails. tRPC's React Query integration supports all standard React Query mutation callbacks.

## Q70: How do you test tRPC procedures?
**A:** Use `@trpc/server`'s `caller` factory to invoke procedures directly in unit tests without HTTP. For integration tests, use a test server like Supertest with your tRPC adapter.

## Q71: What is the caller in tRPC?
**A:** The `caller` is a server-side function that creates a callable version of your router. It allows you to invoke procedures directly in Node.js without making HTTP requests, useful for testing and SSR.

## Q72: How do you use the tRPC caller for SSR?
**A:** Create a caller with a server-side context, then call `caller.procedureName(input)` to prefetch data. The data is returned as a Promise and can be dehydrated for the client.

## Q73: How do you create a caller in tRPC?
**A:** Call `router.createCaller(ctx)` where `ctx` is the server-side context object. The returned caller object has typed `query` and `mutation` methods matching your router.

## Q74: What is a TRPCError?
**A:** `TRPCError` is tRPC's error class that extends the native `Error`. It accepts a `code` from a predefined set (like `UNAUTHORIZED`, `NOT_FOUND`, `BAD_REQUEST`) and optional `message` and `cause`.

## Q75: What error codes does TRPCError support?
**A:** `PARSE_ERROR`, `BAD_REQUEST`, `NOT_FOUND`, `INTERNAL_SERVER_ERROR`, `UNAUTHORIZED`, `FORBIDDEN`, `TIMEOUT`, `CONFLICT`, `PRECONDITION_FAILED`, `PAYLOAD_TOO_LARGE`, `METHOD_NOT_SUPPORTED`, `UNPROCESSABLE_CONTENT`, `TOO_MANY_REQUESTS`, and `CLIENT_CLOSED_REQUEST`.

## Q76: How do you handle Zod validation errors in tRPC?
**A:** tRPC automatically catches Zod validation errors and formats them as `TRPCError` with code `BAD_REQUEST`. The error contains detailed information about which fields failed validation.

## Q77: What is the difference between TRPCError and regular errors?
**A:** `TRPCError` includes a typed error code that the client can use for error handling, and it is serialized and sent to the client. Regular errors might result in generic `INTERNAL_SERVER_ERROR` unless caught and re-thrown.

## Q78: How do you handle errors on the client side?
**A:** Catch `TRPCClientError` in the error callbacks of your React Query hooks or in try-catch blocks for direct calls. Check the error's `data.code` property to determine the error type.

## Q79: What is TRPCClientError?
**A:** `TRPCClientError` is the client-side error class that matches `TRPCError` on the server. It provides typed access to the error code, message, and any custom data sent by the server's error formatter.

## Q80: How do you implement logging middleware in tRPC?
**A:** Create a middleware that logs `opts.path`, `opts.type`, and `opts.durationMs`. Apply it globally with `t.middleware()` and pass it to `t.procedure.use()` or use `t.middleware()` directly.

## Q81: How do you measure procedure execution time in tRPC?
**A:** In middleware, record the start time before calling `next()`, then compare it to the current time after `next()` resolves. The `opts.durationMs` property is also available in v11.

## Q82: How do you create a reusable middleware in tRPC?
**A:** Define middleware as a separate function and call it with `t.middleware()`. Apply it to specific procedures or routers using `.use()`, or to all procedures using the default middleware in `initTRPC`.

## Q83: What is the default middleware in tRPC?
**A:** The default middleware is set during `initTRPC.create()` and applies to all procedures. You can pass middleware functions in the `middleware` array option to run them globally.

## Q84: How do you handle WebSocket connections in tRPC?
**A:** Use `wsLink` on the client and set up a WebSocket server with `@trpc/server` adapter. Subscriptions use WebSocket for bidirectional communication, with automatic reconnection support.

## Q85: What is the wsLink in tRPC?
**A:** `wsLink` is a tRPC client link that uses WebSocket for transport. It is required for subscriptions and also supports queries and mutations over the WebSocket connection.

## Q86: How do you set up a WebSocket server for tRPC?
**A:** Use `applyWSSHandler` from `@trpc/server/adapters/ws` with your router and a WebSocket server instance (like `ws` library). The handler processes incoming WebSocket messages.

## Q87: How does tRPC handle connection resilience?
**A:** The WebSocket client link supports automatic reconnection. React Query handles query refetching on reconnection. Mutations that fail due to connection issues can be retried using React Query's retry mechanism.

## Q88: What is the OpenAPI plugin for tRPC?
**A:** The OpenAPI plugin (`@trpc/openapi`) generates OpenAPI-compliant REST endpoints from your tRPC router, enabling interoperability with non-tRPC clients like mobile apps or third-party integrations.

## Q89: How do you generate OpenAPI specs from tRPC?
**A:** Use the `@trpc/openapi` package's `generateOpenApiDocument` function, passing your router, title, version, and base URL. The output is an OpenAPI 3.0 compliant JSON schema.

## Q90: How do you protect against CSRF in tRPC?
**A:** tRPC uses GET for queries (no side effects) and POST for mutations. For additional CSRF protection, use framework-specific middleware like `csurf` for Express or SameSite cookies.

## Q91: How do you handle query input serialization in GET requests?
**A:** tRPC serializes query input as URL query parameters by default. Complex nested objects are encoded using a key-value structure. Use `httpBatchLink` to send inputs as POST bodies instead.

## Q92: How do you handle large inputs in tRPC queries?
**A:** For large inputs, use `httpLink` or `httpBatchLink` which send data in the request body rather than URL parameters. You can also increase the URL length limit on your server.

## Q93: How do you handle procedure deprecation in tRPC?
**A:** Use procedure metadata to mark procedures as deprecated, and handle this in middleware or client-side logging. There is no built-in deprecation mechanism; it is managed through convention.

## Q94: What are the performance considerations for tRPC?
**A:** Use `httpBatchLink` for batching, enable compression on your HTTP server, set appropriate `staleTime` in React Query, and avoid deeply nested routers that increase serialization overhead.

## Q95: How does tRPC compare to a REST API in terms of type safety?
**A:** REST APIs typically require separate client SDKs or manual type definitions. tRPC infers types directly from the server code, providing automatic end-to-end type safety without code generation.

## Q96: How does tRPC compare to GraphQL in terms of bundle size?
**A:** GraphQL clients like Apollo add significant bundle size. tRPC client is lightweight because it does not include a query parser, schema introspection, or normalization cache.

## Q97: How does tRPC compare to GraphQL in terms of flexibility?
**A:** GraphQL allows clients to request exactly the fields they need. tRPC returns fixed responses per procedure, which is simpler but less flexible for varying client data requirements.

## Q98: How does tRPC handle versioning?
**A:** tRPC does not have built-in versioning. Common strategies include creating separate routers (e.g., `postV1` and `postV2`), using URL prefixes, or evolving procedures with optional new fields.

## Q99: Can you use tRPC with non-TypeScript clients?
**A:** tRPC is designed for TypeScript end-to-end type safety. For non-TypeScript clients, use the OpenAPI plugin to generate REST endpoints or build a separate API layer.

## Q100: What are the limitations of tRPC?
**A:** tRPC requires TypeScript on both client and server, the client must bundle the router types, it does not support field selection like GraphQL, and it is less suitable for public APIs consumed by non-TypeScript clients.
