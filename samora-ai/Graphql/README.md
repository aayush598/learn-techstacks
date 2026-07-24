# GraphQL Interview Questions and Answers

## Q1: What is GraphQL?
**A:** GraphQL is a query language for APIs and a runtime for executing those queries against your data. Created by Facebook in 2012 and open-sourced in 2015, it allows clients to request exactly the data they need in a single request. It provides a strongly-typed schema that serves as a contract between client and server.

## Q2: What is the difference between GraphQL and REST?
**A:** REST uses multiple endpoints with fixed data structures, often leading to over-fetching or under-fetching. GraphQL uses a single endpoint where clients specify exactly what data they need. REST is simpler for basic CRUD, while GraphQL excels when clients have diverse data requirements or need related data from multiple resources in a single request.

## Q3: What is a GraphQL schema?
**A:** A GraphQL schema defines the types, fields, and relationships available in the API. It specifies what queries, mutations, and subscriptions clients can execute. The schema uses the Schema Definition Language (SDL) and acts as a contract between client and server. Every GraphQL API must have exactly one schema.

## Q4: What are the three root operation types in GraphQL?
**A:** Query (read operations, fetching data), Mutation (write operations, creating, updating, or deleting data), and Subscription (real-time data via WebSocket connections). Queries and mutations are the most common; subscriptions enable real-time features like live notifications or chat.

## Q5: What is a GraphQL query?
**A:** A GraphQL query is a read operation that fetches data from the server. The query specifies the exact fields and relationships to retrieve. The response mirrors the query's shape, returning only the requested data. Queries are always safe (no side effects) and can be cached.

## Q6: What is a GraphQL mutation?
**A:** A GraphQL mutation is a write operation that modifies server-side data. Mutations follow the same syntax as queries but are defined under the `mutation` type. They are executed sequentially (unlike queries which can be parallelized) to ensure predictable ordering of writes. Mutations typically return the modified object.

## Q7: What is a GraphQL subscription?
**A:** A GraphQL subscription establishes a long-lived connection (usually WebSocket) between client and server for real-time data. When data changes on the server, it pushes updates to subscribed clients. Subscriptions are useful for live feeds, notifications, chat applications, and collaborative features.

## Q8: What is a GraphQL resolver?
**A:** A resolver is a function that fetches data for a single field in the schema. Each field in the schema can have its own resolver that knows how to retrieve or compute its value. Resolvers receive four arguments: parent, args, context, and info. They can fetch from databases, APIs, or any data source.

## Q9: What are the arguments of a GraphQL resolver?
**A:** parent (result from the parent field resolver), args (object of arguments passed to the field), context (shared across all resolvers for request-scoped data like authentication), and info (AST representation of the query, field name, and schema information). These provide resolvers with everything needed to fulfill a field.

## Q10: What is the N+1 query problem in GraphQL?
**A:** The N+1 problem occurs when resolving a list of N items triggers an additional query for each item's related data, resulting in 1 query for the list + N individual queries. For example, fetching 100 posts and then each post's author separately creates 101 database queries. This is a common performance issue in GraphQL.

## Q11: How do you solve the N+1 problem in GraphQL?
**A:** The primary solution is DataLoader, a utility that batches and caches database queries within a single request. It collects individual load requests and dispatches them as a single batch query. Other solutions include JOIN Monster for SQL JOINs, writeBatchLoadFn for custom batching, and designing schemas that allow fetching related data in fewer queries.

## Q12: What is DataLoader?
**A:** DataLoader is a generic utility created by Facebook for batching and caching data loading. Within a single request, it collects multiple `.load()` calls and dispatches them as a single batch function call. It also provides per-request caching to prevent duplicate fetches. DataLoader is essential for preventing the N+1 problem in GraphQL resolvers.

## Q13: What is a GraphQL type system?
**A:** GraphQL's type system defines the shape of data in the API. Built-in scalar types include Int, Float, String, Boolean, and ID. Custom types can be defined using object types, enums, interfaces, unions, input types, and non-null modifiers. The type system enables validation, documentation, and tooling.

## Q14: What are scalar types in GraphQL?
**A:** Scalar types are leaf types that hold a single value. Built-in scalars are Int (32-bit integer), Float (double-precision floating point), String (UTF-8), Boolean (true/false), and ID (unique identifier). Custom scalars (DateTime, Email, URL) can be defined using libraries like graphql-scalars.

## Q15: What are object types in GraphQL?
**A:** Object types define the shape of data with named fields, each having a type. For example, `type User { id: ID!, name: String!, email: String! }`. Object types are the most common types in a schema and represent the entities in your data model. Fields can return other object types, creating relationships.

## Q16: What is the difference between `!` (non-null) and nullable types?
**A:** By default, all types in GraphQL are nullable (can return null). Adding `!` after a type makes it non-null, guaranteeing a value is always returned. Non-null fields provide stronger guarantees but can cause the parent type to become null if the non-null field errors. Use non-null for fields that should always have values.

## Q17: What are enums in GraphQL?
**A:** Enums (enumeration types) define a set of allowed values for a field. For example, `enum Role { ADMIN, USER, MODERATOR }`. Enums provide type safety, prevent invalid values, and improve API documentation. They can be used as field types, argument types, or in input types.

## Q18: What are interfaces in GraphQL?
**A:** Interfaces define a common set of fields that multiple types must implement. For example, `interface Node { id: ID! }` ensures all implementing types have an `id` field. Interfaces enable polymorphic queries — you can query an interface type and get results from any implementing type. They're useful for shared fields across types.

## Q19: What are unions in GraphQL?
**A:** Unions define a type that can be one of several object types but don't share fields. For example, `union SearchResult = User | Post | Comment`. When querying a union field, you must use inline fragments (`... on User { name }`) to specify which fields to fetch from each possible type. Unions differ from interfaces in that they have no shared fields.

## Q20: What are input types in GraphQL?
**A:** Input types are special object types used exclusively for mutation arguments. They define the structure of data sent from client to server. For example, `input CreateUserInput { name: String!, email: String! }`. Input types support default values and are validated by the GraphQL server before being passed to resolvers.

## Q21: What are fragments in GraphQL?
**A:** Fragments are reusable units of fields that can be included in queries. They avoid repetition when querying the same fields across multiple types or operations. Fragments are defined with `fragment FragmentName on TypeName { fields }` and included with `...FragmentName`. Inline fragments (`... on TypeName { fields }`) are used with unions and interfaces.

## Q22: What is a GraphQL introspection system?
**A:** Introspection allows clients to query the schema itself to discover its types, fields, arguments, and documentation. Using `{ __schema { types { name } } }`, clients can explore the entire API structure. Introspection powers tools like GraphiQL, Apollo Studio, and code generation. It can be disabled in production for security.

## Q23: What are introspection queries?
**A:** Introspection queries are special queries that retrieve metadata about the GraphQL schema. Key introspection fields include `__schema` (full schema info), `__type` (specific type details), and `__typename` (runtime type name). Tools use these to generate documentation, autocomplete, and type-safe client code.

## Q24: What is GraphQL SDL (Schema Definition Language)?
**A:** SDL is the syntax for defining GraphQL schemas. It uses type definitions, field declarations, and directives to describe the API. Example: `type Query { users: [User!]! }`. SDL is human-readable, serves as documentation, and is used by tools for code generation, validation, and visualization.

## Q25: What are directives in GraphQL?
**A:** Directives modify the execution or behavior of fields, types, or arguments. Built-in directives include `@include(if: Boolean!)` (include field if true), `@skip(if: Boolean!)` (skip field if true), and `@deprecated(reason: String)` (mark field as deprecated). Custom directives can be defined to implement authorization, validation, or logging.

## Q26: What is the `@deprecated` directive used for?
**A:** The `@deprecated` directive marks a field or enum value as deprecated, indicating it should no longer be used. It accepts an optional `reason` string explaining the deprecation. Deprecated fields appear in documentation as deprecated and can be filtered out by tools. It enables schema evolution without breaking existing clients.

## Q27: What is a custom scalar in GraphQL?
**A:** Custom scalars extend GraphQL's built-in scalar types to represent domain-specific values like DateTime, Email, URL, JSON, or PhoneNumber. They require definition in the schema and serialization/deserialization logic on the server. Libraries like `graphql-scalars` provide common custom scalars.

## Q28: What is the `__typename` field?
**A:** The `__typename` field is a meta-field available on every object type that returns the type's name as a string. It's useful for resolving union and interface types on the client, implementing Apollo Client's cache normalization, and determining the runtime type of polymorphic fields.

## Q29: What is GraphQL caching?
**A:** GraphQL caching can occur at multiple levels: HTTP caching (using GET requests with persisted queries), CDN caching (for cacheable queries), application-level caching (Apollo Client's normalized cache, Relay's store), and server-side caching (response caching, query batching). The single-endpoint nature of GraphQL complicates traditional HTTP caching.

## Q30: How does Apollo Client handle caching?
**A:** Apollo Client uses a normalized cache that stores objects by their `__typename` and `id` (or `_id`). When a query result is received, each object is stored individually, and references replace nested objects. Subsequent queries that include the same fields use cached values. Cache updates can be configured with `fetchPolicy` (cache-first, network-only, etc.).

## Q31: What are fetch policies in Apollo Client?
**A:** Fetch policies control how Apollo Client uses its cache: `cache-first` (use cache if available, fetch if not), `network-only` (always fetch from network, update cache), `cache-and-network` (return cache, also fetch network), `no-cache` (no cache interaction), and `cache-only` (never fetch, use cache only). `cache-first` is the default.

## Q32: What is a GraphQL fragment spread?
**A:** A fragment spread includes a named fragment's fields in a query. Syntax: `fragment UserFields on User { id name email }` then `query { users { ...UserFields } }`. This promotes reuse, keeps queries DRY, and ensures consistent field selection across different queries. Fragment spreads work with object types, interfaces, and unions.

## Q33: What is the difference between GraphQL and gRPC?
**A:** GraphQL is a query language for APIs using HTTP with JSON, designed for flexible client-driven data fetching. gRPC is a high-performance RPC framework using Protocol Buffers and HTTP/2, designed for efficient service-to-service communication. GraphQL is better for client-facing APIs; gRPC is better for internal microservice communication.

## Q34: What is query batching in GraphQL?
**A:** Query batching combines multiple GraphQL operations into a single HTTP request. Instead of sending separate requests for different data needs, clients send an array of operations. The server processes all operations and returns an array of results. This reduces HTTP overhead and can improve performance for multiple simultaneous data requirements.

## Q35: What is persisted queries?
**A:** Persisted queries map a query's hash to its full text, stored on the server. Clients send only the hash instead of the full query string, reducing bandwidth and improving security (no arbitrary queries). Automatic Persisted Queries (APQ) allow clients to register queries on-the-fly. This reduces payload size and enables query whitelisting.

## Q36: What is schema stitching?
**A:** Schema stitching combines multiple GraphQL schemas into a single unified schema. It allows clients to query multiple backend services through a single GraphQL endpoint. The gateway merges schemas, resolves types across services, and handles cross-service references. Tools like Apollo Gateway and GraphQL Tools provide schema stitching capabilities.

## Q37: What is the difference between schema stitching and federation?
**A:** Schema stitching merges schemas at runtime in a gateway, which may become a bottleneck. Federation (Apollo Federation) distributes the schema across multiple services, with each service owning part of the schema and resolving its own types. Federation is more scalable, allows independent team ownership, and is the preferred approach for large organizations.

## Q38: What is Apollo Federation?
**A:** Apollo Federation is an architecture for building a distributed GraphQL graph across multiple services. Each service defines and owns a portion of the schema using `@key`, `@extends`, and `@external` directives. The Apollo Gateway composes the subgraphs into a unified schema and routes queries to the appropriate services. It supports entity references across services.

## Q39: What are the `@key` and `@external` directives in Apollo Federation?
**A:** `@key` declares the entity's primary key for cross-service references: `type Product @key(fields: "id") { id: ID! name: String }`. `@external` marks a field as defined in another service: `extend type Product @key(fields: "id") { id: ID! @external price: Float }`. These directives enable services to reference and extend types owned by other services.

## Q40: What is a GraphQL gateway?
**A:** A GraphQL gateway is a server that sits between clients and multiple GraphQL services, providing a unified API. It handles query planning, request routing, response merging, and cross-service authentication. Examples include Apollo Gateway, graphql-mesh, and custom solutions. Gateways are essential for microservices architectures with multiple GraphQL services.

## Q41: What is GraphQL error handling?
**A:** GraphQL returns errors in a standard `errors` array alongside `data`. Each error includes a `message`, optional `locations` (line/column), `path` (field path), and custom `extensions` (like error codes). Unlike REST, GraphQL can return partial data alongside errors (200 status code). Error handling best practices include using error codes, structured error types, and not leaking internal details.

## Q42: What is partial data in GraphQL responses?
**A:** GraphQL can return partial data when some fields succeed and others fail. For example, if fetching a user succeeds but their posts fail, the response includes the user data and an error for the posts field. Non-null fields that error will propagate the null to their parent, potentially nullifying larger portions of the response.

## Q43: What is query complexity analysis?
**A:** Query complexity analysis assigns cost values to fields and calculates the total cost of a query before execution. This prevents expensive queries from overwhelming the server. Fields can have complexity scores (e.g., lists cost more), and queries exceeding a threshold are rejected. Libraries like `graphql-query-complexity` implement this.

## Q44: What is query depth limiting?
**A:** Query depth limiting restricts how deeply nested a query can be. For example, a depth limit of 5 prevents queries like `user { posts { comments { author { posts { ... } } } } }`. This protects against deeply nested queries that cause excessive database loads. However, depth alone doesn't capture all attack vectors (e.g., wide queries).

## Q45: What is a GraphQL subscription resolver?
**A:** A subscription resolver establishes the real-time connection and defines how to listen for events. Unlike query/mutation resolvers, the subscription's top-level resolver returns an AsyncIterator (using PubSub). When events are published to the subscription's topic, the iterator yields new data that is sent to connected clients.

## Q46: What is PubSub in GraphQL?
**A:** PubSub (Publish-Subscribe) is the in-memory event system used to power GraphQL subscriptions. When a mutation publishes an event to a topic, all active subscriptions listening on that topic receive the event. Implementations include in-memory PubSub (testing only), Redis PubSub (production), Kafka, and Google Cloud PubSub.

## Q47: What is the difference between HTTP and WebSocket transports for subscriptions?
**A:** HTTP transport uses Server-Sent Events (SSE) or long-polling for subscriptions — simpler but less efficient for high-frequency updates. WebSocket transport maintains a persistent bidirectional connection — more efficient for real-time updates but requires WebSocket infrastructure. WebSockets are the standard for GraphQL subscriptions.

## Q48: What is GraphQL middleware?
**A:** GraphQL middleware intercepts and modifies requests before or after resolvers execute. It's used for authentication, authorization, logging, validation, and error handling. In Apollo Server, middleware is implemented as plugins or as field-level directives. In graphql-yoga, built-in plugins provide middleware-like functionality.

## Q49: What is the difference between authentication and authorization in GraphQL?
**A:** Authentication verifies identity (who the user is) — typically handled by middleware checking JWT tokens, session cookies, or API keys before the request reaches resolvers. Authorization determines permissions (what the user can access) — typically handled in resolvers or directives checking user roles and permissions against the requested data.

## Q50: What are the most popular GraphQL server implementations?
**A:** JavaScript/TypeScript: Apollo Server, graphql-yoga, Mercurius. Python: Strawberry, Ariadne, graphene. Go: gqlgen, graphql-go. Java/Kotlin: Spring GraphQL, graphql-java. Ruby: graphql-ruby. Rust: async-graphql. PHP: webonyx/graphql-php, Siler. Each has different features, performance characteristics, and ecosystem integrations.

## Q51: What is the difference between Apollo Server and graphql-yoga?
**A:** Apollo Server is the most popular GraphQL server with extensive tooling (Apollo Studio, Federation, Client). graphql-yoga is a lightweight, batteries-included server built on standard Web APIs with built-in subscriptions, file uploads, and auto-caching. Yoga is simpler to set up; Apollo provides a more comprehensive ecosystem for enterprise needs.

## Q52: What are the most popular GraphQL client libraries?
**A:** Apollo Client (React, Angular, Vue, iOS, Android) with normalized cache. Relay (React only) with compiler-based optimization. urql (React, lightweight). graphql-request (minimal, framework-agnostic). SWR + GraphQL hooks. Apollo Client is most popular; Relay is preferred for large-scale applications requiring automatic optimization.

## Q53: What is the difference between Apollo Client and Relay?
**A:** Apollo Client is a full-featured client with normalized caching, developer tools, and framework support. Relay is Facebook's client with compiler-based query optimization, automatic pagination, and fragment-based data fetching. Apollo is easier to learn and more flexible; Relay provides stronger guarantees about performance at scale but has a steeper learning curve.

## Q54: What is persisted queries and how do they improve security?
**A:** Persisted queries store approved query hashes on the server, allowing only pre-registered queries to execute. This prevents arbitrary query execution, mitigating injection attacks and malicious queries. In production, disabling introspection and enabling persisted queries significantly reduces the attack surface of a GraphQL API.

## Q55: What is query whitelisting?
**A:** Query whitelisting (or allowlisting) is a security practice where only pre-approved queries are allowed to execute. The server maintains a list of valid query hashes or patterns and rejects any request containing a query not on the list. This prevents malicious or expensive queries but requires management of the whitelist as the API evolves.

## Q56: What is the difference between REST over-fetching and GraphQL?
**A:** REST endpoints return fixed data structures regardless of what the client needs, leading to over-fetching (receiving unused fields) and under-fetching (needing multiple requests for related data). GraphQL lets clients specify exactly which fields they need, receiving only that data. This reduces bandwidth usage and improves client performance.

## Q57: What is a GraphQL variable?
**A:** Variables are dynamic values passed to GraphQL operations, replacing hardcoded values in queries. Declared in the operation definition (`query GetUser($id: ID!)`) and passed as a JSON object. Variables provide type safety, prevent injection attacks (unlike string interpolation), and enable query reuse with different parameters.

## Q58: What are operation names in GraphQL?
**A:** Operation names are optional but recommended identifiers for GraphQL operations (e.g., `query GetUser { ... }`). They make debugging easier (identifying operations in logs and monitoring), enable persisted queries, and help with query complexity analysis. Best practice is to always name operations.

## Q59: What is the `node` interface pattern in GraphQL?
**A:** The Node interface provides a global object identification pattern where every entity implements `interface Node { id: ID! }`. Clients can fetch any object by its global ID using a `node(id: ID!)` query. This pattern enables client-side caching (Relay's `nodeInterface`), refetching, and store-based data management.

## Q60: What is cursor-based pagination in GraphQL?
**A:** Cursor-based pagination uses an opaque cursor (usually an encoded ID or timestamp) instead of page numbers to traverse data. The query passes a cursor to the server, which returns the next set of results. This is more efficient than offset-based pagination for large datasets and provides consistent results even when data changes between requests.

## Q61: What is the Relay Connection specification?
**A:** The Relay Connection spec is a standardized pagination format that uses edges, nodes, cursors, and page info. It defines `Connection`, `Edge`, and `PageInfo` types for consistent paginated responses. While created for Relay, it's widely adopted as a pagination best practice across the GraphQL ecosystem.

## Q62: What is offset vs. cursor-based pagination?
**A:** Offset-based pagination uses a numeric offset and limit (`skip: 20, limit: 10`) — simple but can skip items or show duplicates when data changes. Cursor-based pagination uses a reference point (cursor) to fetch the next batch — more reliable for real-time data but slightly more complex to implement. Cursor-based is preferred for GraphQL.

## Q63: What is GraphQL code generation?
**A:** GraphQL code generation uses tools like GraphQL Code Generator to automatically generate TypeScript types, React hooks, resolvers, and schema files from your GraphQL schema and operations. This eliminates manual type definitions, catches errors at compile time, and ensures type safety across the entire stack.

## Q64: What is GraphQL Code Generator?
**A:** GraphQL Code Generator (graphql-codegen) is a tool that generates typed code from GraphQL schemas and operations. It supports TypeScript types, React hooks, resolvers, schema files, and more. You configure it with your schema, operations, and desired plugins, and it generates code that keeps your types in sync with your API.

## Q65: What is a GraphQL playground?
**A:** A GraphQL playground is an interactive IDE for exploring and testing GraphQL APIs. It provides query editing, autocomplete, schema documentation, query history, and variable editing. Examples include GraphiQL (in-browser IDE), Apollo Sandbox, and GraphQL Playground. They use introspection to display the schema and provide real-time validation.

## Q66: What is the difference between GraphiQL and GraphQL Playground?
**A:** GraphiQL is the original GraphQL IDE maintained by the GraphQL Foundation, embedded in browsers for API exploration. GraphQL Playground is a fork by Prisma with additional features like tabs, query history, and HTTP header editing. Both provide similar functionality; GraphQL Playground has a more modern UI.

## Q67: What is GraphQL file upload?
**A:** GraphQL file upload typically uses the multipart request spec (GraphQL multipart request specification). Files are sent as multipart form data alongside the GraphQL operation. Libraries like `graphql-upload` (server) and `apollo-upload-client` (client) handle this. Alternatively, files can be uploaded to cloud storage and referenced by URL in GraphQL.

## Q68: What is a GraphQL directive?
**A:** Directives annotate schema elements or query operations to modify behavior. They use the `@` syntax: `@deprecated(reason: "Use newField")`, `@include(if: $showDetails)`. Custom directives can implement authorization (`@auth(role: ADMIN)`), validation (`@constraint(maxLength: 255)`), or caching (`@cacheControl(maxAge: 300)`).

## Q69: What is schema-first vs. code-first GraphQL development?
**A:** Schema-first writes the SDL schema definition first, then implements resolvers — the schema drives the development. Code-first generates the schema from code (decorators, builders) — the code drives the schema. Schema-first is simpler and more explicit; code-first provides type safety, reusability, and keeps schema in sync with implementation.

## Q70: What is a GraphQL plugin?
**A:** A GraphQL plugin extends the server's functionality by hooking into request lifecycle events. Plugins can handle request parsing, validation, execution, response formatting, error handling, and logging. Apollo Server uses a plugin architecture, and graphql-yoga uses built-in plugins. They're the preferred way to add cross-cutting concerns.

## Q71: What is request batching in GraphQL?
**A:** Request batching combines multiple GraphQL operations into a single HTTP request by sending them as a JSON array. The server processes all operations and returns an array of results. This reduces HTTP overhead and can be implemented with Apollo Client's `batchHttpLink`. Batch size should be limited to prevent timeout issues.

## Q72: What is GraphQL tooling ecosystem?
**A:** The GraphQL ecosystem includes: servers (Apollo Server, yoga), clients (Apollo Client, Relay), IDEs (GraphiQL, Apollo Sandbox), gateways (Apollo Gateway, graphql-mesh), code generation (graphql-codegen), monitoring (Apollo Studio), testing (graphql-tag, nock), and validation (ESLint plugins). Each tool addresses specific development needs.

## Q73: What is Apollo Studio?
**A:** Apollo Studio is a cloud-based platform for GraphQL development that provides schema registry, operation logging, performance metrics, schema change validation, and collaboration tools. It helps teams monitor their GraphQL API, detect performance issues, validate schema changes before deployment, and track usage patterns.

## Q74: What is schema change validation in GraphQL?
**A:** Schema change validation (schema registry) detects breaking changes when the schema is modified. Tools like Apollo Studio compare old and new schemas to identify removed fields, type changes, and other breaking modifications. This prevents deploying schema changes that would break existing clients and enables safe schema evolution.

## Q75: How do you version a GraphQL API?
**A:** GraphQL typically avoids explicit versioning (v1, v2) by evolving the schema. Strategies include: adding new fields (non-breaking), deprecating old fields with `@deprecated`, using schema directives, and creating new types when necessary. Breaking changes are rare with proper evolution. Tools like schema registries help manage this evolution safely.

## Q76: What is a GraphQL union type and how do you query it?
**A:** A union type represents a type that can be one of several object types without sharing fields. To query a union, you must use inline fragments: `search(query: "term") { ... on User { name } ... on Post { title } }`. The `__typename` field identifies which type was returned. Unions are useful for polymorphic search results.

## Q77: What is the difference between interfaces and unions?
**A:** Interfaces define shared fields that all implementing types must have — you can query common fields directly on the interface. Unions don't define shared fields — all field queries must use inline fragments for each possible type. Use interfaces when types share structure; use unions when types are unrelated but can appear in the same context.

## Q78: What is error handling best practice in GraphQL?
**A:** Best practices include: returning structured errors with codes in the `extensions` field, providing partial data alongside errors when possible, not leaking internal implementation details, using custom scalar types for error values, implementing field-level error handling, logging server errors for debugging, and using unions or custom error types for expected business errors.

## Q79: What is a GraphQL Error union type pattern?
**A:** Instead of relying on the `errors` array, return errors as part of the data using union types: `union CreateUserResult = User | ValidationError | ConflictError`. This makes errors explicit in the schema, enables type-safe error handling on the client, and distinguishes between expected business errors and unexpected system errors.

## Q80: What is the `data` field in GraphQL responses?
**A:** The `data` field contains the result of the executed operation, matching the shape of the query. It can be null if the root query or mutation errors entirely, or partially null if non-null fields error. The `data` field always exists in the response even if all fields are null due to errors (unless the operation itself is invalid).

## Q81: What is a GraphQL data loader pattern?
**A:** The data loader pattern uses DataLoader to batch and cache database requests within a single GraphQL operation. It prevents N+1 queries by collecting individual load requests dispatched across resolvers and batching them into a single database query. DataLoader is initialized per-request to ensure request-level caching.

## Q82: What is a query plan in GraphQL federation?
**A:** A query plan is the execution strategy the Apollo Gateway creates to resolve a federated query across multiple services. It determines which services to call, in what order, and how to merge results. The plan minimizes network requests by batching and parallelizing where possible, handling entity references across services.

## Q83: What is the difference between `require` and `requireAuth` in GraphQL?
**A:** `require` typically refers to server-side field-level resolvers that must fetch data, while `requireAuth` is a directive or middleware pattern that checks user authentication before resolving a field. `requireAuth` validates the user's identity and permissions; `require` loads data. Both are patterns for controlling access and data loading.

## Q84: What is query normalization in Apollo Client?
**A:** Query normalization decomposes query results into individual objects stored by `__typename` and `id`. Nested objects are replaced with references. This ensures that when one query updates an object, all queries referencing that object see the update automatically. Normalization eliminates data duplication and provides consistent views.

## Q85: What is optimistic updates in GraphQL?
**A:** Optimistic updates immediately update the UI with the expected result before the server confirms. Apollo Client's `optimisticResponse` option provides the expected mutation result, updating the cache instantly. If the server response differs, the cache is corrected. This provides instant feedback without waiting for network latency.

## Q86: What is the `@cacheControl` directive?
**A:** The `@cacheControl` directive sets caching parameters for fields, types, or operations. It defines `maxAge` (how long the response is fresh) and `scope` (PUBLIC or PRIVATE). This enables Apollo Server and CDNs to cache responses appropriately. It works with Apollo Server's response caching plugin.

## Q87: What is response caching in GraphQL?
**A:** Response caching stores entire query responses based on cache control headers. Apollo Server's `responseCachePlugin` caches responses with keys based on the query, variables, and context. Cache is invalidated when mutations modify related data. Response caching significantly reduces server load for frequently accessed, rarely changing data.

## Q88: What is a GraphQL schema registry?
**A:** A schema registry is a centralized service for storing, versioning, and managing GraphQL schemas. It tracks schema changes over time, validates breaking changes, and ensures schema consistency across services. Apollo Studio's schema registry is the most common implementation, providing change detection and deployment workflows.

## Q89: What is a query mask in Relay?
**A:** Relay's query mask ensures components only receive the data they explicitly request. Each component's fragment is independently fetched and the result is masked so a parent component can't access a child's data. This enforces encapsulation, prevents data dependencies from leaking, and enables efficient data fetching.

## Q90: What is the `@defer` and `@stream` directives?
**A:** `@defer` allows parts of a query to be returned later, enabling progressive rendering — the client receives critical data immediately and deferred data as it becomes available. `@stream` is similar for list fields, returning initial items immediately and streaming additional items. Both improve perceived performance for large responses.

## Q91: What is the difference between GraphQL and tRPC?
**A:** GraphQL is a query language and schema-based API specification that works across languages and platforms. tRPC is a TypeScript-first RPC framework that provides end-to-end type safety without schema definition — it infers types directly from server functions. tRPC is simpler for TypeScript-only stacks; GraphQL is better for polyglot environments and public APIs.

## Q92: What is a GraphQL mock server?
**A:** A GraphQL mock server returns simulated data for testing and development without a real backend. Tools like `graphql-tools` (mock function), Apollo Server's `mocks` option, and MSW (Mock Service Worker) can mock GraphQL APIs. Mock servers enable frontend development in parallel with backend implementation.

## Q93: What is the difference between mocking and stubbing in GraphQL?
**A:** Mocking generates random but schema-compliant data for all fields automatically — useful for development and testing without writing data. Stubbing provides specific, hand-crafted responses for known queries — useful for testing exact behaviors. Both are valuable; mocking for general development, stubbing for specific test cases.

## Q94: What is a GraphQL subscription resolver's return type?
**A:** A subscription resolver's top-level resolver must return an AsyncIterator (or an object with a `subscribe` method that returns one). The AsyncIterator yields events matching the subscription's type. Subsequent resolvers (for fields on the subscription type) process each yielded event to shape the response data.

## Q95: How do you handle authentication in GraphQL subscriptions?
**A:** Authentication for subscriptions happens during the connection initialization. The client passes auth tokens (JWT, session) in the connection parameters when establishing the WebSocket connection. The server validates the token during `connection_init` and rejects unauthorized connections. Some implementations also support per-message auth validation.

## Q96: What is the difference between GraphQL over HTTP and WebSocket?
**A:** GraphQL over HTTP uses standard HTTP requests (GET for persisted queries, POST for operations) — simple, stateless, cacheable, and works with existing infrastructure. WebSocket uses persistent connections for subscriptions — stateful, bidirectional, and efficient for real-time updates. Most applications use HTTP for queries/mutations and WebSocket for subscriptions.

## Q97: What is a GraphQL schema stitcher vs. a gateway?
**A:** A schema stitcher (like graphql-tools' `stitchSchemas`) merges multiple schemas at the application level, requiring manual type resolution configuration. A gateway (like Apollo Gateway) provides a managed, declarative approach with automatic type resolution and query planning. Gateways are better for production microservices; stitchers offer more control for simpler use cases.

## Q98: What is query cost analysis in production GraphQL?
**A:** Query cost analysis calculates the computational cost of a query before execution to prevent abuse. Each field is assigned a cost (with lists multiplied by their maximum size), and the total is checked against a threshold. Queries exceeding the limit are rejected. This complements query depth limiting for comprehensive protection.

## Q99: What is the `@specifiedBy` directive in GraphQL?
**A:** The `@specifiedBy` directive (introduced in GraphQL 18) associates a URL with a custom scalar type, pointing to its specification. This replaces the deprecated `@specifiedBy` pattern and provides machine-readable documentation about custom scalar behavior. It improves tooling support and schema documentation.

## Q100: What are the best practices for designing a GraphQL API?
**A:** Best practices include: design the schema around client needs (not database structure), use descriptive field and type names, leverage the type system for validation, implement pagination with cursors, use DataLoader for N+1 prevention, version through schema evolution (not API versions), secure with authentication and authorization layers, monitor query performance, use persisted queries in production, and provide comprehensive documentation through schema descriptions.
