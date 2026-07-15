# Type-Safe API Design

## Table of Contents

1. [Generic API Client](#generic-api-client)
2. [Type-Safe Path Parameters](#type-safe-path-parameters)
3. [Query and Header Types](#query-and-header-types)
4. [Method Discrimination](#method-discrimination)
5. [Type-Safe Router Design](#type-safe-router-design)
6. [Type-Safe Validation](#type-safe-validation)
7. [Type-Safe ORM Patterns](#type-safe-orm-patterns)
8. [Type-Safe Configuration](#type-safe-configuration)
9. [Type-Safe Event Systems](#type-safe-event-systems)
10. [Type-Safe State Machines](#type-safe-state-machines)
11. [Library API Design Patterns](#library-api-design-patterns)
12. [Interview Questions](#interview-questions)

---

## Generic API Client

```typescript
// A fully type-safe API client where endpoints, methods,
// request bodies, and responses are all inferred from types.

// ============= Endpoint Definitions =============
interface ApiEndpoints {
  '/users': {
    GET: {
      response: User[];
      query: { page?: number; limit?: number; search?: string };
    };
    POST: {
      response: User;
      body: CreateUserInput;
    };
  };
  '/users/:id': {
    GET: {
      response: User;
      params: { id: string };
    };
    PUT: {
      response: User;
      params: { id: string };
      body: UpdateUserInput;
    };
    DELETE: {
      response: void;
      params: { id: string };
    };
  };
  '/users/:id/posts': {
    GET: {
      response: Post[];
      params: { id: string };
      query: { page?: number };
    };
    POST: {
      response: Post;
      params: { id: string };
      body: CreatePostInput;
    };
  };
  '/posts/:postId/comments': {
    GET: {
      response: Comment[];
      params: { postId: string };
    };
  };
}

// Supporting types
interface User {
  id: string;
  name: string;
  email: string;
}

interface Post {
  id: string;
  authorId: string;
  title: string;
  content: string;
}

interface Comment {
  id: string;
  postId: string;
  body: string;
}

interface CreateUserInput {
  name: string;
  email: string;
}

interface UpdateUserInput {
  name?: string;
  email?: string;
}

// ============= Type-Safe Client =============
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

type ExtractParams<T extends string> =
  T extends `${infer _}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ExtractParams<Rest>]: string }
    : T extends `${infer _}:${infer Param}`
    ? { [K in Param]: string }
    : {};

class ApiClient {
  constructor(private baseUrl: string) {}

  async request<
    Path extends keyof ApiEndpoints,
    Method extends keyof ApiEndpoints[Path] & HttpMethod
  >(
    method: Method,
    path: Path,
    options?: {
      params?: ExtractParams<Path & string>;
      query?: ApiEndpoints[Path][Method] extends { query: infer Q } ? Q : never;
      body?: ApiEndpoints[Path][Method] extends { body: infer B } ? B : never;
    }
  ): Promise<
    ApiEndpoints[Path][Method] extends { response: infer R } ? R : never
  > {
    // Resolve path parameters
    let resolvedPath = path as string;
    if (options?.params) {
      for (const [key, value] of Object.entries(options.params)) {
        resolvedPath = resolvedPath.replace(`:${key}`, value as string);
      }
    }

    // Build query string
    let url = `${this.baseUrl}${resolvedPath}`;
    if (options?.query) {
      const params = new URLSearchParams();
      for (const [key, value] of Object.entries(options.query as Record<string, string>)) {
        if (value !== undefined) {
          params.set(key, String(value));
        }
      }
      const qs = params.toString();
      if (qs) url += `?${qs}`;
    }

    // Make request
    const response = await fetch(url, {
      method: method as string,
      headers: {
        'Content-Type': 'application/json',
      },
      body: options?.body ? JSON.stringify(options.body) : undefined,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    // Return typed response
    return response.json() as Promise<any>;
  }
}

// ============= Usage =============
const api = new ApiClient('https://api.example.com');

// All fully typed — IDE autocompletion works for everything
async function demo() {
  // GET /users?page=1&limit=10
  const users = await api.request('GET', '/users', {
    query: { page: 1, limit: 10 },
  });
  // users: User[]

  // POST /users
  const newUser = await api.request('POST', '/users', {
    body: { name: 'Alice', email: 'alice@example.com' },
  });
  // newUser: User

  // GET /users/:id
  const user = await api.request('GET', '/users/:id', {
    params: { id: '123' },
  });
  // user: User

  // PUT /users/:id
  const updated = await api.request('PUT', '/users/:id', {
    params: { id: '123' },
    body: { name: 'Alice Updated' },
  });
  // updated: User

  // GET /users/:id/posts
  const posts = await api.request('GET', '/users/:id/posts', {
    params: { id: '123' },
    query: { page: 1 },
  });
  // posts: Post[]

  // TypeScript errors:
  // await api.request('GET', '/users', { body: {} });
  // Error: GET /users doesn't accept a body
  // await api.request('POST', '/users/:id');
  // Error: POST /users/:id requires params and body
}
```

---

## Type-Safe Path Parameters

```typescript
// Extract route parameters from path strings:

type ExtractRouteParams<T extends string> =
  T extends `${infer _Start}:${infer Param}/${infer Rest}`
    ? { [K in Param]: string } & ExtractRouteParams<Rest>
    : T extends `${infer _Start}:${infer Param}`
    ? { [K in Param]: string }
    : {};

// Usage
type UserPostParams = ExtractRouteParams<'/users/:userId/posts/:postId'>;
// { userId: string; postId: string }

type UserParams = ExtractRouteParams<'/users/:id'>;
// { id: string }

// Make params required (not optional)
type RequiredParams<T extends string> = {
  [K in keyof ExtractRouteParams<T>]-?: string;
};

// Validate that all params are provided
function buildUrl<Path extends string>(
  path: Path,
  params: RequiredParams<Path>
): string {
  let result = path as string;
  for (const [key, value] of Object.entries(params)) {
    result = result.replace(`:${key}`, value as string);
  }
  return result;
}

// Usage — TypeScript ensures all params are provided
const url1 = buildUrl('/users/:id/posts/:postId', {
  id: '123',
  postId: '456',
});
// url1 = "/users/123/posts/456"

// TypeScript error: missing 'postId'
// const url2 = buildUrl('/users/:id/posts/:postId', { id: '123' });

// Dynamic route matching
type MatchRoute<
  Path extends string,
  Input extends string
> = Path extends Input
  ? ExtractRouteParams<Path>
  : never;

type R1 = MatchRoute<'/users/:id', '/users/:id'>;
// { id: string }

// Advanced: path with optional segments
type ExtractOptionalParams<T extends string> =
  T extends `${infer _Start}:${infer Param}?/${infer Rest}`
    ? { [K in Param]?: string } & ExtractOptionalParams<Rest>
    : T extends `${infer _Start}:${infer Param}?`
    ? { [K in Param]?: string }
    : ExtractRouteParams<T>;

type OptionalParams = ExtractOptionalParams<'/users/:id?/posts/:postId'>;
// { id?: string; postId: string }
```

---

## Query and Header Types

```typescript
// Type-safe query parameters with validation:

type ParseQueryString<T extends string> =
  T extends `${infer Key}=${infer Value}&${infer Rest}`
    ? { [K in Key]: Value } & ParseQueryString<Rest>
    : T extends `${infer Key}=${infer Value}`
    ? { [K in Key]: Value }
    : {};

type Q = ParseQueryString<'page=1&limit=10&search=hello'>;
// { page: "1"; limit: "10"; search: "hello" }

// Primitives for query params
interface QueryConfig {
  page: number;
  limit: number;
  search: string;
  sort: 'asc' | 'desc';
  fields: string[];
  filter: Record<string, string>;
}

// Type-safe query builder
class QueryBuilder<T extends Record<string, unknown>> {
  private params: Partial<T> = {};

  set<K extends keyof T>(key: K, value: T[K]): this {
    this.params[key] = value;
    return this;
  }

  build(): Partial<T> {
    return { ...this.params };
  }

  toSearchString(): string {
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(this.params)) {
      if (value !== undefined) {
        if (Array.isArray(value)) {
          params.set(key, value.join(','));
        } else {
          params.set(key, String(value));
        }
      }
    }
    return params.toString();
  }
}

// Usage
const query = new QueryBuilder<QueryConfig>()
  .set('page', 1)
  .set('limit', 20)
  .set('sort', 'asc')
  .set('search', 'typescript');
// query.set('sort', 'invalid'); // Error: 'invalid' is not assignable to 'asc' | 'desc'

// Type-safe headers
interface RequestHeaders {
  'Content-Type': 'application/json' | 'application/xml' | 'text/plain';
  'Authorization': `Bearer ${string}`;
  'X-Request-Id': string;
  'X-Tenant-Id': string;
  'Accept-Language': 'en' | 'es' | 'fr' | 'de';
}

class TypedHeaders {
  private headers: Record<string, string> = {};

  set<K extends keyof RequestHeaders>(key: K, value: RequestHeaders[K]): this {
    this.headers[key] = value;
    return this;
  }

  build(): Headers {
    return new Headers(this.headers);
  }
}

const headers = new TypedHeaders()
  .set('Content-Type', 'application/json')
  .set('Authorization', 'Bearer token123')
  .set('X-Request-Id', 'req-001')
  .set('Accept-Language', 'en');
// headers.set('Content-Type', 'text/html'); // Error
// headers.set('Authorization', 'Basic abc'); // Error
```

---

## Method Discrimination

```typescript
// Different HTTP methods return different types:

interface ApiContract {
  'GET /users': {
    response: User[];
    query: { page?: number; limit?: number };
    error: ApiError;
  };
  'POST /users': {
    response: User;
    body: CreateUserInput;
    error: ApiError | ValidationError;
  };
  'GET /users/:id': {
    response: User;
    params: { id: string };
    error: ApiError | NotFoundError;
  };
  'PUT /users/:id': {
    response: User;
    params: { id: string };
    body: Partial<User>;
    error: ApiError | NotFoundError | ValidationError;
  };
  'DELETE /users/:id': {
    response: void;
    params: { id: string };
    error: ApiError | NotFoundError;
  };
}

type ExtractMethod<T extends string> =
  T extends `${infer Method} ${infer _Path}` ? Method : never;

type ExtractPath<T extends string> =
  T extends `${infer _Method} ${infer Path}` ? Path : never;

type GetEndpoint<K extends keyof ApiContract> =
  ApiContract[K];

// Type-safe fetch wrapper
async function typedFetch<
  Route extends keyof ApiContract
>(
  route: Route,
  options?: {
    params?: ApiContract[Route] extends { params: infer P } ? P : never;
    body?: ApiContract[Route] extends { body: infer B } ? B : never;
    query?: ApiContract[Route] extends { query: infer Q } ? Q : never;
  }
): Promise<ApiContract[Route] extends { response: infer R } ? R : never> {
  const [method, pathTemplate] = (route as string).split(' ');

  let path = pathTemplate;
  if (options?.params) {
    for (const [key, val] of Object.entries(options.params as Record<string, string>)) {
      path = path.replace(`:${key}`, val);
    }
  }

  const response = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: options?.body ? JSON.stringify(options.body) : undefined,
  });

  return response.json();
}

// Usage
const users = await typedFetch('GET /users', {
  query: { page: 1 },
});
// users: User[]

const user = await typedFetch('GET /users/:id', {
  params: { id: '123' },
});
// user: User

const newUser = await typedFetch('POST /users', {
  body: { name: 'Alice', email: 'alice@test.com' },
});
// newUser: User
```

---

## Type-Safe Router Design

```typescript
// A type-safe HTTP router that infers parameter types:

type RouteHandler<
  Params extends Record<string, string> = {},
  Query extends Record<string, string> = {},
  Body = unknown,
  Response = unknown
> = (context: {
  params: Params;
  query: Query;
  body: Body;
  headers: Record<string, string>;
}) => Promise<Response> | Response;

interface RouteDefinition {
  params: Record<string, string>;
  query: Record<string, string>;
  body: unknown;
  response: unknown;
}

class TypedRouter {
  private routes: Map<string, { method: string; handler: Function }> = new Map();

  route<
    Path extends string,
    Def extends RouteDefinition
  >(
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    path: Path,
    handler: RouteHandler<Def['params'], Def['query'], Def['body'], Def['response']>
  ): this {
    const key = `${method} ${path}`;
    this.routes.set(key, { method, handler });
    return this;
  }

  async handle(
    method: string,
    path: string,
    options: {
      params?: Record<string, string>;
      query?: Record<string, string>;
      body?: unknown;
      headers?: Record<string, string>;
    } = {}
  ): Promise<unknown> {
    const key = `${method} ${path}`;
    const route = this.routes.get(key);
    if (!route) throw new Error(`Route not found: ${key}`);

    return (route.handler as Function)({
      params: options.params ?? {},
      query: options.query ?? {},
      body: options.body,
      headers: options.headers ?? {},
    });
  }
}

// Usage
const router = new TypedRouter();

interface UserListDef {
  params: {};
  query: { page?: string; limit?: string };
  body: never;
  response: User[];
}

router.route<'GET /users', UserListDef>('GET', '/users', async ({ query }) => {
  const page = Number(query.page ?? 1);
  const limit = Number(query.limit ?? 10);
  // query.page and query.limit are string | undefined
  return [{ id: '1', name: 'Alice', email: 'alice@test.com' }];
});

interface UserCreateDef {
  params: {};
  query: {};
  body: CreateUserInput;
  response: User;
}

router.route<'POST /users', UserCreateDef>('POST', '/users', async ({ body }) => {
  // body is CreateUserInput
  return { id: '2', ...body };
});
```

---

## Type-Safe Validation

### Zod Schemas -> TypeScript Types

```typescript
import { z } from 'zod';

// Define schemas (single source of truth for both validation AND types)
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(2).max(100),
  email: z.string().email(),
  role: z.enum(['admin', 'editor', 'viewer']),
  createdAt: z.coerce.date(),
  metadata: z.record(z.unknown()).optional(),
});

// Extract TypeScript type from schema (no duplication!)
type User = z.infer<typeof UserSchema>;
// {
//   id: string;
//   name: string;
//   email: string;
//   role: "admin" | "editor" | "viewer";
//   createdAt: Date;
//   metadata?: Record<string, unknown>;
// }

// Validate at runtime
function createUser(input: unknown): User {
  return UserSchema.parse(input); // throws ZodError if invalid
}

// Safe validation (doesn't throw)
function safeCreateUser(input: unknown) {
  const result = UserSchema.safeParse(input);
  if (result.success) {
    return { ok: true, data: result.data };
  }
  return { ok: false, errors: result.error.errors };
}

// Complex schemas
const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(10),
  tags: z.array(z.string()).max(10).optional(),
  publishedAt: z.coerce.date().optional(),
});

type CreatePostInput = z.infer<typeof CreatePostSchema>;

// Schema composition
const PaginatedSchema = <T extends z.ZodType>(itemSchema: T) =>
  z.object({
    data: z.array(itemSchema),
    meta: z.object({
      page: z.number(),
      limit: z.number(),
      total: z.number(),
    }),
  });

const PaginatedUsersSchema = PaginatedSchema(UserSchema);
type PaginatedUsers = z.infer<typeof PaginatedUsersSchema>;

// API route with Zod validation
async function handleCreatePost(request: Request): Promise<Response> {
  const body = await request.json();
  const result = CreatePostSchema.safeParse(body);

  if (!result.success) {
    return Response.json(
      { errors: result.error.flatten() },
      { status: 400 }
    );
  }

  // result.data is fully typed as CreatePostInput
  const post = await createPost(result.data);
  return Response.json(post);
}
```

### io-ts Pattern

```typescript
import * as t from 'io-ts';
import { fold } from 'fp-ts/Either';

// io-ts: runtime type system for TypeScript
const UserCodec = t.type({
  id: t.string,
  name: t.string,
  email: t.string,
  role: t.union([t.literal('admin'), t.literal('editor'), t.literal('viewer')]),
});

// Extract the static type (compile-time)
type User = t.TypeOf<typeof UserCodec>;

// Extract the encoded type (runtime validation shape)
type UserOutput = t.OutputOf<typeof UserCodec>;

// Validate
const input: unknown = { id: '1', name: 'Alice', email: 'a@b.com', role: 'admin' };

const result = UserCodec.decode(input);
// result is Either<Errors, User>

fold(
  (errors) => console.error('Validation failed:', errors),
  (user) => console.log('Valid user:', user.name),
)(result);

// Middleware for Express-style APIs
function validate<T extends t.Type<any>>(codec: T) {
  return (req: any, res: any, next: any) => {
    const result = codec.decode(req.body);
    fold(
      (errors) => res.status(400).json({ errors }),
      (decoded) => {
        req.validatedBody = decoded;
        next();
      }
    )(result);
  };
}
```

### Valibot Pattern

```typescript
import * as v from 'valibot';

// Valibot: smaller bundle alternative to Zod
const UserSchema = v.object({
  id: v.pipe(v.string(), v.uuid()),
  name: v.pipe(v.string(), v.minLength(2), v.maxLength(100)),
  email: v.pipe(v.string(), v.email()),
  role: v.union([v.literal('admin'), v.literal('editor'), v.literal('viewer')]),
});

type User = v.InferOutput<typeof UserSchema>;

const result = v.safeParse(UserSchema, input);
if (result.success) {
  // result.output is User
}
```

---

## Type-Safe ORM Patterns

### Prisma

```typescript
// Prisma generates types from your schema.prisma file:

// schema.prisma
// model User {
//   id        String   @id @default(uuid())
//   name      String
//   email    String   @unique
//   posts    Post[]
//   role     Role     @default(VIEWER)
// }
//
// model Post {
//   id         String   @id @default(uuid()
//   title      String
//   content   String?
//   published Boolean  @default(false)
//   author    User     @relation(fields: [authorId], references: [id])
//   authorId  String
// }
//
// enum Role {
//   ADMIN
//   EDITOR
//   VIEWER
// }

import { PrismaClient, Prisma } from '@prisma/client';

const prisma = new PrismaClient();

// Fully type-safe queries
async function getUsersWithPosts() {
  // The return type is inferred from the select/include
  const users = await prisma.user.findMany({
    include: {
      posts: {
        where: { published: true },
        select: {
          id: true,
          title: true,
        },
      },
    },
  });

  // users: (User & { posts: { id: string; title: string }[] })[]
  type UserType = typeof users[number];
  // { id: string; name: string; email: string; role: Role; posts: { id: string; title: string }[] }
}

// Type-safe create
async function createUser(data: Prisma.UserCreateInput) {
  // Prisma.UserCreateInput is generated from schema:
  // { name: string; email: string; role?: Role; posts?: Prisma.PostCreateNestedManyWithoutAuthorInput }
  return prisma.user.create({ data });
}

// Type-safe where clauses
async function findUsers(where: Prisma.UserWhereInput) {
  // Prisma.UserWhereInput includes all filterable fields with operators
  return prisma.user.findMany({ where });
}

await findUsers({
  role: 'ADMIN',
  posts: {
    some: {
      published: true,
    },
  },
});

// Type-safe raw queries
const rawUsers = await prisma.$queryRaw`
  SELECT * FROM "User" WHERE email LIKE ${'%@example.com'}
`;
// rawUsers is typed based on the select
```

### Drizzle ORM

```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { pgTable, text, varchar, boolean, uuid } from 'drizzle-orm/pg-core';

// Define schema (also the source of truth for types)
const users = pgTable('users', {
  id: uuid('id').defaultRandom().primaryKey(),
  name: varchar('name', { length: 100 }).notNull(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  role: text('role', { enum: ['admin', 'editor', 'viewer'] }).default('viewer'),
});

const posts = pgTable('posts', {
  id: uuid('id').defaultRandom().primaryKey(),
  title: varchar('title', { length: 200 }).notNull(),
  content: text('content'),
  published: boolean('published').default(false),
  authorId: uuid('author_id').references(() => users.id),
});

// Drizzle generates TypeScript types from schema
type User = typeof users.$inferSelect; // { id: string; name: string; ... }
type NewUser = typeof users.$inferInsert; // { id?: string; name: string; ... }

// Type-safe queries
const db = drizzle(process.env.DATABASE_URL!);

async function getUsersWithPosts() {
  const result = await db
    .select({
      userId: users.id,
      userName: users.name,
      postTitle: posts.title,
    })
    .from(users)
    .leftJoin(posts, eq(posts.authorId, users.id))
    .where(eq(users.role, 'admin'));

  // Result type is fully inferred:
  // { userId: string; userName: string; postTitle: string | null }[]
}

// Type-safe insert
async function createUser(data: NewUser) {
  return db.insert(users).values(data).returning();
}
```

---

## Type-Safe Configuration

```typescript
// Ensure environment variables are properly typed and validated:

import { z } from 'zod';

const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  API_PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  CORS_ORIGINS: z.string().transform((s) => s.split(',')),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  // Optional with defaults
  ENABLE_METRICS: z.coerce.boolean().default(false),
  MAX_CONNECTIONS: z.coerce.number().default(10),
});

// Parse and validate at startup (fail fast)
const env = EnvSchema.parse(process.env);

// env is fully typed:
// {
//   NODE_ENV: "development" | "test" | "production";
//   DATABASE_URL: string;
//   REDIS_URL: string;
//   JWT_SECRET: string;
//   API_PORT: number;
//   CORS_ORIGINS: string[];
//   LOG_LEVEL: "debug" | "info" | "warn" | "error";
//   ENABLE_METRICS: boolean;
//   MAX_CONNECTIONS: number;
// }

// Use throughout the app — fully typed
console.log(env.DATABASE_URL); // string
console.log(env.CORS_ORIGINS); // string[]
console.log(env.ENABLE_METRICS); // boolean

// Type-safe config object
interface AppConfig {
  database: {
    url: string;
    maxConnections: number;
  };
  redis: {
    url: string;
  };
  auth: {
    jwtSecret: string;
    tokenExpiry: string;
  };
  server: {
    port: number;
    corsOrigins: string[];
    logLevel: 'debug' | 'info' | 'warn' | 'error';
  };
}

function createConfig(env: z.infer<typeof EnvSchema>): AppConfig {
  return {
    database: {
      url: env.DATABASE_URL,
      maxConnections: env.MAX_CONNECTIONS,
    },
    redis: { url: env.REDIS_URL },
    auth: {
      jwtSecret: env.JWT_SECRET,
      tokenExpiry: '24h',
    },
    server: {
      port: env.API_PORT,
      corsOrigins: env.CORS_ORIGINS,
      logLevel: env.LOG_LEVEL,
    },
  };
}

const config = createConfig(env);
// config.database.url: string
// config.server.port: number
```

---

## Type-Safe Event Systems

```typescript
// A fully typed event emitter where events, payloads, and
// listeners are all connected:

type EventMap = {
  'user:created': { userId: string; name: string };
  'user:updated': { userId: string; changes: Partial<{ name: string; email: string }> };
  'user:deleted': { userId: string };
  'post:published': { postId: string; authorId: string; title: string };
  'post:viewed': { postId: string; viewerId?: string };
  'system:error': { code: string; message: string; stack?: string };
};

class TypedEventEmitter<Events extends Record<string, unknown>> {
  private listeners = new Map<string, Set<Function>>();

  on<K extends keyof Events>(
    event: K,
    handler: (payload: Events[K]) => void
  ): () => void {
    const key = event as string;
    if (!this.listeners.has(key)) {
      this.listeners.set(key, new Set());
    }
    this.listeners.get(key)!.add(handler);

    // Return unsubscribe function
    return () => {
      this.listeners.get(key)?.delete(handler);
    };
  }

  once<K extends keyof Events>(
    event: K,
    handler: (payload: Events[K]) => void
  ): () => void {
    const wrappedHandler = (payload: Events[K]) => {
      unsubscribe();
      handler(payload);
    };
    const unsubscribe = this.on(event, wrappedHandler);
    return unsubscribe;
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    const handlers = this.listeners.get(event as string);
    handlers?.forEach((handler) => handler(payload));
  }

  // Type-safe event filtering
  onAny<K extends keyof Events>(
    ...events: K[]
  ): (handler: (event: K, payload: Events[K]) => void) => () => void {
    return (handler) => {
      const unsubs = events.map((event) =>
        this.on(event, (payload) => handler(event, payload))
      );
      return () => unsubs.forEach((unsub) => unsub());
    };
  }
}

// Usage
const emitter = new TypedEventEmitter<EventMap>();

// Fully typed listeners
emitter.on('user:created', (payload) => {
  console.log(payload.name); // string
  console.log(payload.userId); // string
});

emitter.on('post:published', (payload) => {
  console.log(payload.title); // string
  console.log(payload.authorId); // string
});

// TypeScript errors for wrong payloads:
// emitter.on('user:created', (payload) => {
//   console.log(payload.postId); // Error: 'postId' doesn't exist
// });

// emitter.emit('user:created', { postId: '123' }); // Error
// emitter.emit('user:created', { userId: '1', name: 'Alice' }); // OK

// Emit events
emitter.emit('user:created', { userId: '1', name: 'Alice' });
emitter.emit('post:published', {
  postId: 'p1',
  authorId: '1',
  title: 'Hello World',
});
```

---

## Type-Safe State Machines

```typescript
// Using XState patterns with TypeScript:

// Define the state machine contract
interface TodoMachine {
  states: {
    idle: {};
    loading: {};
    editing: { context: { draft: string } };
    saving: { context: { draft: string } };
    error: { context: { error: string } };
    saved: {};
  };
  events: {
    START_EDIT: { draft: string };
    UPDATE_DRAFT: { draft: string };
    SAVE: {};
    SUCCESS: {};
    FAILURE: { error: string };
    CANCEL: {};
    RETRY: {};
  };
}

// Type-safe state transitions
type State = keyof TodoMachine['states'];
type Event = keyof TodoMachine['events'];

// Valid transitions map
type ValidTransitions = {
  idle: 'START_EDIT';
  loading: 'START_EDIT' | 'FAILURE';
  editing: 'UPDATE_DRAFT' | 'SAVE' | 'CANCEL';
  saving: 'SUCCESS' | 'FAILURE';
  error: 'RETRY' | 'CANCEL';
  saved: 'START_EDIT';
};

class TypedStateMachine {
  private state: State = 'idle';
  private context: Record<string, unknown> = {};

  transition<E extends Event>(
    event: E
  ): void {
    // Validate transition is allowed
    const allowedEvents = ValidTransitions[this.state] as Event;
    if (!allowedEvents.includes(event)) {
      throw new Error(
        `Invalid transition: ${event} from state ${this.state}`
      );
    }

    // Handle state change
    switch (this.state) {
      case 'idle':
        if (event === 'START_EDIT') {
          this.state = 'editing';
        }
        break;
      case 'editing':
        if (event === 'SAVE') {
          this.state = 'saving';
        } else if (event === 'CANCEL') {
          this.state = 'idle';
        }
        break;
      // ... other transitions
    }
  }

  getState(): State {
    return this.state;
  }
}
```

---

## Library API Design Patterns

### Builder Pattern

```typescript
// Fluent builder for constructing complex objects type-safely:

class QueryBuilder<T extends Record<string, unknown>> {
  private filters: Partial<T> = {};
  private sortOrder: 'asc' | 'desc' = 'asc';
  private sortField?: keyof T;
  private limitValue?: number;
  private offsetValue?: number;

  where<K extends keyof T>(field: K, value: T[K]): this {
    this.filters[field] = value;
    return this;
  }

  orderBy(field: keyof T, order: 'asc' | 'desc' = 'asc'): this {
    this.sortField = field;
    this.sortOrder = order;
    return this;
  }

  limit(n: number): this {
    this.limitValue = n;
    return this;
  }

  offset(n: number): this {
    this.offsetValue = n;
    return this;
  }

  build(): string {
    const parts: string[] = [];
    for (const [key, value] of Object.entries(this.filters)) {
      parts.push(`${key}=${value}`);
    }
    if (this.sortField) {
      parts.push(`sort=${String(this.sortField)}:${this.sortOrder}`);
    }
    if (this.limitValue) parts.push(`limit=${this.limitValue}`);
    if (this.offsetValue) parts.push(`offset=${this.offsetValue}`);
    return parts.join('&');
  }
}

// Usage — all type-safe
const query = new QueryBuilder<{ name: string; age: number; role: string }>()
  .where('role', 'admin')
  .orderBy('age', 'desc')
  .limit(10)
  .build();
// query = "role=admin&sort=age:desc&limit=10"
// .where('name', 123) // Error: number is not assignable to string
```

### Pipe/Flow Pattern

```typescript
// Type-safe function composition:

function pipe<A>(value: A): A;
function pipe<A, B>(value: A, ab: (a: A) => B): B;
function pipe<A, B, C>(value: A, ab: (a: A) => B, bc: (b: B) => C): C;
function pipe<A, B, C, D>(
  value: A,
  ab: (a: A) => B,
  bc: (b: B) => C,
  cd: (c: C) => D
): D;
function pipe(value: unknown, ...fns: Function[]): unknown {
  return fns.reduce((acc, fn) => fn(acc), value);
}

// Usage — each step's return type flows to the next
const result = pipe(
  { name: '  Alice  ', age: '25', email: 'ALICE@TEST.COM' },
  (user) => ({ ...user, name: user.name.trim() }),
  (user) => ({ ...user, age: Number(user.age) }),
  (user) => ({ ...user, email: user.email.toLowerCase() }),
  (user) => ({
    ...user,
    displayName: `${user.name} (${user.age})`,
  })
);
// result: { name: string; age: number; email: string; displayName: string }
```

---

## Interview Questions

### Q1: How do you achieve end-to-end type safety from API routes to database?

**Answer:** Use a schema-first approach: define schemas (Prisma, Drizzle, Zod) as the single source of truth. Zod validates inputs, Prisma/Drizzle generates database types. Connect them in API handlers: `Zod.parse()` -> handler function -> Prisma query -> typed response. The entire chain from HTTP request to database query is type-checked.

### Q2: Explain the pattern of extracting TypeScript types from Zod schemas.

**Answer:** Use `z.infer<typeof Schema>` to extract the compile-time TypeScript type from a Zod runtime schema. This gives you one definition that serves as both a runtime validator and a compile-time type. No duplication. `z.infer` maps Zod types to TypeScript types (e.g., `z.string()` -> `string`, `z.object({...})` -> `{...}`).

### Q3: How do you type a generic API client?

**Answer:** Define an interface mapping endpoints to their HTTP methods, request/response types, params, query, and body. The client method takes the endpoint path and method as generic parameters, extracts the corresponding types from the mapping interface, and enforces correct usage through generics. Type inference ensures the return type matches the endpoint.

### Q4: How would you design a type-safe event emitter?

**Answer:** Define an event map type: `{ 'event:name': PayloadType; ... }`. The emitter's `on` method takes `K extends keyof Events` and a handler typed as `(payload: Events[K]) => void`. The `emit` method requires `event: K` and `payload: Events[K]`. This ensures listeners match event payloads at compile time.

### Q5: What is the builder pattern in TypeScript and when is it useful?

**Answer:** The builder pattern uses method chaining to construct complex objects step by step. Each method returns `this` for chaining. It's useful when constructing objects with many optional fields (database queries, HTTP requests, configuration objects). TypeScript ensures each step provides correct types and prevents invalid method sequences through the return type chain.

### Q6: How do you type path parameters in a route like `/users/:id/posts/:postId`?

**Answer:** Use template literal types with conditional type inference: `ExtractRouteParams<'/users/:id/posts/:postId'>` recursively extracts `:param` segments into `{ id: string; postId: string }`. The recursive type handles `:param/rest` patterns by building an intersection of `{ [Param]: string }` for each parameter found.

### Q7: Compare Zod, io-ts, and Valibot for runtime validation.

**Answer:** Zod is the most popular, with excellent TypeScript inference and error messages. io-ts is fp-ts-compatible, uses Either for error handling (functional style), but larger bundle. Valibot is Zod-compatible with 10x smaller bundle size (~2KB vs ~20KB), ideal for browser/bundle-size-sensitive apps. All three provide runtime validation with TypeScript type inference.

### Q8: How do you implement type-safe configuration from environment variables?

**Answer:** Define a Zod schema for all required env vars with types, defaults, and transforms. Parse `process.env` at startup with `EnvSchema.parse(process.env)`. If any required var is missing, the app fails immediately with a clear error. The parsed result is fully typed and used throughout the app. Use `z.coerce` for number/boolean conversion from string env vars.

### Q9: How do you type different HTTP methods with different return types?

**Answer:** Define a route contract interface where each route maps HTTP method to its response, body, params, and error types. The client's method parameter (`'GET /users'` | `'POST /users'`) is a string literal type. TypeScript infers the return type based on the matched route and method in the contract. Discriminated union on the method string enables method-specific behavior.

### Q10: Explain type-safe state machines in TypeScript.

**Answer:** Define a type map of states and events. A transitions map (`ValidTransitions`) associates each state with its allowed events as a union type. The `transition` method takes an event type and validates it against the current state's allowed events. Context types can carry state-specific data. XState provides a full implementation with guards, actions, and services.
