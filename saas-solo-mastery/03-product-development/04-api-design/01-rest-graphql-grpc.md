# API Design: REST vs GraphQL vs gRPC for SaaS

## The API Decision

Your API is the contract between your frontend and backend, and potentially between your product and external developers. Choosing the right API paradigm affects development speed, performance, and developer experience for years to come.

This guide covers the three major API paradigms — REST, GraphQL, and gRPC — with specific guidance for solo SaaS founders building both internal and external APIs.

## API Paradigm Comparison

### At a Glance

```markdown
| Feature              | REST              | GraphQL           | gRPC               |
|----------------------|-------------------|-------------------|--------------------|
| Paradigm             | Resource-based    | Query language    | Service-based      |
| Data fetching        | Multiple endpoints | Single endpoint   | Single method call |
| Over-fetching        | Common            | None              | None               |
| Under-fetching       | Common            | None              | None               |
| Caching              | Excellent         | Complex           | Limited            |
| Tooling              | Excellent         | Good              | Good               |
| Learning curve       | Low               | Medium            | High               |
| Versioning           | URL/Header        | Schema evolution  | Proto versions     |
| Transport            | HTTP/1.1          | HTTP/2            | HTTP/2             |
| Data format          | JSON/XML          | JSON              | Protobuf (binary)  |
| Browser support      | Native            | Native            | Requires proxy     |
| Performance          | Good              | Good              | Excellent          |
| Complexity           | Low               | Medium            | High               |
| Best for             | Public APIs       | Complex UIs       | Internal services  |
```

## REST: The Workhorse

### When REST is the Right Choice

```markdown
1. Public APIs
   - REST is the industry standard for public APIs
   - Every developer knows REST
   - Best ecosystem for API documentation (OpenAPI/Swagger)
   - Most widely supported by API clients

2. Simple CRUD Applications
   - Create, Read, Update, Delete map naturally to HTTP methods
   - Resource-based thinking aligns with most databases
   - Simple to understand and implement

3. Caching-Heavy Workloads
   - HTTP caching is built into REST
   - GET requests are cacheable by default
   - CDN-friendly (cache API responses at the edge)
   - Browser caching works naturally

4. Mobile Applications
   - REST works well with mobile network conditions
   - Simple retry logic (idempotent GETs)
   - JSON parsing is efficient on mobile

5. Stateless Architectures
   - REST is stateless by design
   - Scales horizontally with no session stickiness
   - Simple load balancing
```

### REST Best Practices for SaaS

```typescript
// 1. Resource naming conventions
// Plural nouns for collections
GET    /api/v1/users           // List users
POST   /api/v1/users           // Create user
GET    /api/v1/users/:id       // Get user
PATCH  /api/v1/users/:id       // Update user
DELETE /api/v1/users/:id       // Delete user

// Nested resources for relationships
GET    /api/v1/users/:id/projects      // User's projects
POST   /api/v1/users/:id/projects      // Create project for user
GET    /api/v1/projects/:id/tasks      // Project's tasks

// Actions (when resource CRUD doesn't fit)
POST   /api/v1/users/:id/activate      // Action on a resource
POST   /api/v1/projects/:id/duplicate  // Custom action

// 2. Consistent response format
interface ApiResponse<T> {
  data: T;
  meta?: {
    page: number;
    limit: number;
    total: number;
    hasMore: boolean;
  };
  error?: {
    code: string;
    message: string;
    details?: Record<string, string[]>; // Field-level errors
  };
}

// 3. Error handling
HTTP Status Codes:
  200: Success (GET, PATCH)
  201: Created (POST)
  204: No Content (DELETE)
  400: Bad Request (validation errors)
  401: Unauthorized (not authenticated)
  403: Forbidden (authenticated but not allowed)
  404: Not Found
  409: Conflict (duplicate, state conflict)
  422: Unprocessable Entity (validation)
  429: Too Many Requests (rate limited)
  500: Internal Server Error
  503: Service Unavailable

// 4. Pagination
// Always paginate list endpoints
GET /api/v1/projects?page=1&limit=20&sort=-created_at

// Response with pagination metadata
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 85,
    "hasMore": true
  }
}

// 5. Sparse fieldsets (let clients choose fields)
GET /api/v1/users/123?fields=id,email,name

// 6. Conditional requests (caching)
GET /api/v1/users/123
If-None-Match: "abc123"  // ETag
If-Modified-Since: Wed, 21 Oct 2024 07:28:00 GMT

Response:
  200 + data (if modified)
  304 Not Modified (if not modified)
```

### Solo Founder REST Stack

```typescript
// lib/api/response.ts
// Standardized API response helpers

export function success<T>(data: T, meta?: ApiMeta) {
  return Response.json({ data, meta }, { status: 200 });
}

export function created<T>(data: T) {
  return Response.json({ data }, { status: 201 });
}

export function noContent() {
  return new Response(null, { status: 204 });
}

export function badRequest(message: string, details?: Record<string, string[]>) {
  return Response.json(
    { error: { code: 'BAD_REQUEST', message, details } },
    { status: 400 }
  );
}

export function notFound(message = 'Resource not found') {
  return Response.json(
    { error: { code: 'NOT_FOUND', message } },
    { status: 404 }
  );
}

export function conflict(message: string) {
  return Response.json(
    { error: { code: 'CONFLICT', message } },
    { status: 409 }
  );
}

export function serverError(error: Error) {
  console.error('Internal server error:', error);
  return Response.json(
    { error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } },
    { status: 500 }
  );
}

// lib/api/pagination.ts
export function paginated<T>(
  data: T[],
  total: number,
  page: number,
  limit: number
) {
  return {
    data,
    meta: {
      page,
      limit,
      total,
      hasMore: page * limit < total,
    },
  };
}
```

## GraphQL: When You Need Flexibility

### When GraphQL is the Right Choice

```markdown
1. Complex UI with Nested Data
   - Dashboard that shows user + projects + tasks + comments
   - GraphQL fetches everything in one request
   - Avoids REST's multiple round-trips

2. Multiple Client Types
   - Web app, mobile app, third-party integrations
   - Each client fetches different data
   - GraphQL lets each client specify exactly what it needs

3. Rapid Frontend Iteration
   - Frontend adds new features without backend changes
   - No need to add new REST endpoints
   - Schema is self-documenting

4. Real-time Subscriptions
   - GraphQL subscriptions for WebSocket-based real-time
   - Built into most GraphQL servers
   - Simpler than REST + WebSocket combination

5. Federated Architecture
   - Multiple backend services exposed through one GraphQL gateway
   - Clients see a unified API
   - Simplifies microservice API consumption
```

### GraphQL Best Practices for Solo SaaS

```graphql
# 1. Schema design
type Query {
  me: User
  user(id: ID!): User
  users(page: Int, limit: Int): UserConnection!
  project(id: ID!): Project
  projects(status: ProjectStatus): [Project!]!
  search(query: String!, type: SearchType): [SearchResult!]!
}

type Mutation {
  createProject(input: CreateProjectInput!): Project!
  updateProject(id: ID!, input: UpdateProjectInput!): Project!
  deleteProject(id: ID!): Boolean!
  inviteUser(email: String!, projectId: ID!): Invitation!
}

type User {
  id: ID!
  email: String!
  name: String!
  avatar: String
  projects: [Project!]!
  createdAt: DateTime!
}

type Project {
  id: ID!
  name: String!
  description: String
  status: ProjectStatus!
  owner: User!
  members: [User!]!
  tasks: [Task!]!
  createdAt: DateTime!
}

enum ProjectStatus {
  ACTIVE
  ARCHIVED
  COMPLETED
}

input CreateProjectInput {
  name: String!
  description: String
}

# 2. Pagination with Relay-style connections
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# 3. Error handling
type MutationResult {
  success: Boolean!
  errors: [Error!]
}

type Error {
  field: String
  message: String!
  code: String!
}

# 4. Rate limiting in extensions
extend type Query {
  _rateLimit: RateLimitInfo!
}

type RateLimitInfo {
  limit: Int!
  remaining: Int!
  resetAt: DateTime!
}
```

```typescript
// lib/graphql/resolvers.ts
// Solo-friendly GraphQL resolver pattern

export const resolvers: Resolvers = {
  Query: {
    me: async (_, __, { userId }) => {
      if (!userId) throw new AuthenticationError('Not authenticated');
      return userService.getUser(userId);
    },

    projects: async (_, { status }, { userId }) => {
      if (!userId) throw new AuthenticationError('Not authenticated');
      return projectService.listProjects(userId, status);
    },

    project: async (_, { id }, { userId }) => {
      if (!userId) throw new AuthenticationError('Not authenticated');
      const project = await projectService.getProject(id);
      if (!project) throw new NotFoundError('Project not found');
      return project;
    },
  },

  Mutation: {
    createProject: async (_, { input }, { userId }) => {
      if (!userId) throw new AuthenticationError('Not authenticated');
      return projectService.createProject(userId, input);
    },

    deleteProject: async (_, { id }, { userId }) => {
      if (!userId) throw new AuthenticationError('Not authenticated');
      await projectService.deleteProject(id, userId);
      return true;
    },
  },

  // Resolve relationships efficiently (DataLoader pattern)
  User: {
    projects: async (user, _, { loaders }) => {
      return loaders.projectsByUser.load(user.id);
    },
  },

  Project: {
    tasks: async (project, _, { loaders }) => {
      return loaders.tasksByProject.load(project.id);
    },
  },
};
```

### When NOT to Use GraphQL

```markdown
1. Simple CRUD APIs
   - REST is simpler and more natural
   - GraphQL adds unnecessary complexity

2. Performance-critical public APIs
   - REST caching (HTTP caching) is simpler
   - GraphQL responses are hard to cache at the CDN level
   - Each query is unique, making cache keys complex

3. File upload APIs
   - REST handles file uploads naturally
   - GraphQL needs additional spec (multipart request spec)

4. Solo founder building internal API only
   - If you control both frontend and backend
   - REST is simpler to implement
   - GraphQL's flexibility is wasted when you control all clients

5. HATEOAS/REST is sufficient
   - If your UI fits a standard CRUD pattern
   - Over-fetching is not a performance issue for most apps
```

## gRPC: For Internal Service Communication

### When gRPC is the Right Choice

```markdown
1. Microservice Communication
   - Low-latency internal service calls
   - Strongly-typed service contracts
   - Efficient binary serialization (Protobuf)
   - Built-in streaming support

2. High-Performance Requirements
   - gRPC is 5-10x faster than JSON-based APIs
   - Lower CPU usage (binary format)
   - HTTP/2 multiplexing (one connection, many requests)

3. Polyglot Environments
   - Multiple programming languages
   - gRPC generates client libraries automatically
   - Consistent API across languages

4. Streaming Use Cases
   - Server streaming (event feeds)
   - Client streaming (large uploads)
   - Bidirectional streaming (chat, real-time)
```

### gRPC for Solo Founders

For solo founders, gRPC is almost never the right choice for external APIs. But it can be useful for communication between internal services.

```protobuf
// proto/billing/v1/billing.proto

syntax = "proto3";

package billing.v1;

service BillingService {
  rpc CreateSubscription(CreateSubscriptionRequest) returns (Subscription);
  rpc CancelSubscription(CancelSubscriptionRequest) returns (CancelSubscriptionResponse);
  rpc GetSubscription(GetSubscriptionRequest) returns (Subscription);
  rpc ListInvoices(ListInvoicesRequest) returns (ListInvoicesResponse);
  rpc HandleWebhook(HandleWebhookRequest) returns (HandleWebhookResponse);
}

message CreateSubscriptionRequest {
  string user_id = 1;
  string plan_id = 2;
  string payment_method_id = 3;
}

message Subscription {
  string id = 1;
  string user_id = 2;
  string plan_id = 3;
  SubscriptionStatus status = 4;
  double current_period_start = 5;
  double current_period_end = 6;
  bool cancel_at_period_end = 7;
}

enum SubscriptionStatus {
  SUBSCRIPTION_STATUS_UNSPECIFIED = 0;
  SUBSCRIPTION_STATUS_ACTIVE = 1;
  SUBSCRIPTION_STATUS_CANCELED = 2;
  SUBSCRIPTION_STATUS_PAST_DUE = 3;
  SUBSCRIPTION_STATUS_TRIALING = 4;
}

message ListInvoicesRequest {
  string user_id = 1;
  int32 page = 2;
  int32 limit = 3;
}

message ListInvoicesResponse {
  repeated Invoice invoices = 1;
  int32 total = 2;
  bool has_more = 3;
}
```

## Hybrid Approach: REST + GraphQL

For many solo founders, the best approach is a hybrid:

```markdown
Internal API (between services): REST (simple) or gRPC (perf)
Public API: REST (industry standard)
Frontend → Backend: GraphQL (flexible) or REST (simple)

Solo founder default:
  - Start with REST for everything
  - Add GraphQL ONLY if you find REST painful for frontend
  - Never use gRPC until you have multiple services
```

## API Versioning Strategies

### REST Versioning

```typescript
// Strategy 1: URL versioning (simplest, most common)
GET /api/v1/users
GET /api/v2/users

// Implementation
import { Router } from 'express';

const v1Router = Router();
const v2Router = Router();

v1Router.get('/users', v1UserController.list);
v2Router.get('/users', v2UserController.list);

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// Strategy 2: Header versioning (cleaner URLs)
GET /api/users
Accept: application/vnd.myapp.v1+json

// Strategy 3: Query parameter versioning (simple but ugly)
GET /api/users?version=1
```

### GraphQL Versioning

```graphql
# Version through evolution, not explicit versions
# Add new fields, deprecate old ones

type User {
  id: ID!
  email: String!
  name: String!
  # Old field, use 'name' instead
  fullName: String @deprecated(reason: "Use 'name' instead")
  # New field added in schema evolution
  avatar: String
  createdAt: DateTime!
}
```

## API Documentation

### REST: OpenAPI/Swagger

```typescript
// lib/api/openapi.ts
// OpenAPI documentation via code annotations or Zod schemas

import { z } from 'zod';
import { extendApi } from '@anatine/zod-openapi';

// Define schemas with OpenAPI metadata
export const UserSchema = extendApi(
  z.object({
    id: z.string().uuid(),
    email: z.string().email(),
    name: z.string().min(1).max(100),
    role: z.enum(['user', 'admin']),
    createdAt: z.string().datetime(),
  }),
  {
    title: 'User',
    description: 'A user of the system',
  }
);

export const CreateUserSchema = extendApi(
  z.object({
    email: z.string().email(),
    name: z.string().min(1).max(100),
    password: z.string().min(8).max(100),
  }),
  {
    title: 'CreateUserInput',
    description: 'Input for creating a user',
  }
);

// Generate OpenAPI spec from Zod schemas
import { generateOpenAPI } from '@anatine/zod-openapi';
const openApiSpec = generateOpenAPI({
  openapi: '3.0.3',
  info: {
    title: 'My SaaS API',
    version: '1.0.0',
    description: 'API for My SaaS Product',
  },
  servers: [{ url: 'https://api.mysaas.com' }],
  paths: {
    '/users': {
      get: {
        operationId: 'listUsers',
        summary: 'List all users',
        responses: {
          '200': {
            description: 'List of users',
            content: {
              'application/json': {
                schema: {
                  type: 'array',
                  items: { $ref: '#/components/schemas/User' },
                },
              },
            },
          },
        },
      },
    },
  },
});
```

## API Security Patterns

```typescript
// lib/api/auth.ts
// API authentication middleware

// Pattern 1: API Key (for external developers)
export function requireApiKey() {
  return async (req: Request, res: Response, next: NextFunction) => {
    const apiKey = req.headers['x-api-key'];

    if (!apiKey) {
      return res.status(401).json({ error: 'API key required' });
    }

    const key = await apiKeyService.validateKey(apiKey as string);
    if (!key) {
      return res.status(401).json({ error: 'Invalid API key' });
    }

    req.apiKey = key;
    req.organizationId = key.organizationId;
    next();
  };
}

// Pattern 2: JWT Authentication (for browser clients)
export function requireAuth() {
  return async (req: Request, res: Response, next: NextFunction) => {
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    try {
      const payload = jwt.verify(token, process.env.JWT_SECRET!);
      req.userId = payload.sub;
      next();
    } catch {
      return res.status(401).json({ error: 'Invalid or expired token' });
    }
  };
}

// Pattern 3: Rate Limiting
export function rateLimit(config: { windowMs: number; max: number }) {
  const requests = new Map<string, { count: number; resetAt: number }>();

  return (req: Request, res: Response, next: NextFunction) => {
    const key = req.ip || req.headers['x-forwarded-for'] as string;
    const now = Date.now();
    const record = requests.get(key);

    if (!record || now > record.resetAt) {
      requests.set(key, { count: 1, resetAt: now + config.windowMs });
      return next();
    }

    if (record.count >= config.max) {
      return res.status(429).json({
        error: 'Too many requests',
        retryAfter: Math.ceil((record.resetAt - now) / 1000),
      });
    }

    record.count++;
    next();
  };
}
```

## API Error Patterns

```typescript
// lib/api/errors.ts
// Consistent error handling for all API paradigms

export class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: Record<string, string[]>
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(404, 'NOT_FOUND', `${resource} not found`);
  }
}

export class ValidationError extends AppError {
  constructor(details: Record<string, string[]>) {
    super(400, 'VALIDATION_ERROR', 'Validation failed', details);
  }
}

export class AuthenticationError extends AppError {
  constructor() {
    super(401, 'UNAUTHORIZED', 'Authentication required');
  }
}

export class ForbiddenError extends AppError {
  constructor() {
    super(403, 'FORBIDDEN', 'You do not have permission');
  }
}

// Global error handler
export function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
      },
    });
  }

  // Unexpected errors
  console.error('Unhandled error:', err);
  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  });
}
```

## API Testing Strategy

```typescript
// tests/api/users.test.ts
// Integration tests for API endpoints

import { describe, it, expect } from 'vitest';
import { app } from '@/app';

describe('Users API', () => {
  describe('POST /api/v1/users', () => {
    it('should create a user', async () => {
      const response = await app.request('/api/v1/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'test@example.com',
          name: 'Test User',
        }),
      });

      expect(response.status).toBe(201);
      const body = await response.json();
      expect(body.data.email).toBe('test@example.com');
      expect(body.data.id).toBeDefined();
    });

    it('should reject invalid email', async () => {
      const response = await app.request('/api/v1/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'not-an-email',
          name: 'Test User',
        }),
      });

      expect(response.status).toBe(422);
    });

    it('should reject duplicate email', async () => {
      // Create first user
      await app.request('/api/v1/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'dupe@example.com', name: 'First' }),
      });

      // Attempt duplicate
      const response = await app.request('/api/v1/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'dupe@example.com', name: 'Second' }),
      });

      expect(response.status).toBe(409);
    });
  });

  describe('GET /api/v1/users/:id', () => {
    it('should return user by id', async () => {
      const createRes = await app.request('/api/v1/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'get@example.com', name: 'Get Test' }),
      });
      const { data: user } = await createRes.json();

      const response = await app.request(`/api/v1/users/${user.id}`);
      expect(response.status).toBe(200);
      const body = await response.json();
      expect(body.data.id).toBe(user.id);
    });

    it('should return 404 for non-existent user', async () => {
      const response = await app.request('/api/v1/users/non-existent-id');
      expect(response.status).toBe(404);
    });
  });
});
```

## The Solo Founder's API Recommendation

```markdown
For 90% of solo founders building SaaS:

1. Start with REST (always)
   - Simplest to implement
   - Everyone understands it
   - Best for public APIs
   - Best tooling ecosystem

2. Add GraphQL only if:
   - Your frontend needs complex nested data
   - You have multiple clients with different data needs
   - REST endpoints become painful to manage

3. Never use gRPC until:
   - You have 2+ backend services
   - Performance between services matters
   - Streaming is core to your product

The "Just REST" advice:
  - REST handles everything you need for 1-100k users
  - Most successful SaaS companies use REST publicly
  - GraphQL adds complexity that solo founders don't need
  - You can always add GraphQL later (it can wrap REST APIs)
```

## API First Development Checklist

```markdown
When designing your API, check:

[ ] Consistent naming conventions (plural nouns, kebab-case)
[ ] Standard HTTP methods (GET, POST, PATCH, DELETE)
[ ] Proper HTTP status codes (not just 200 and 500)
[ ] Consistent response format (wrapped in { data, error })
[ ] Pagination on all list endpoints
[ ] Filtering, sorting, and field selection
[ ] Authentication (API key or JWT)
[ ] Rate limiting headers (X-RateLimit-Remaining)
[ ] Error responses with codes and messages
[ ] Request validation (Zod, Joi, or similar)
[ ] OpenAPI/Swagger documentation
[ ] CORS configuration
[ ] Idempotency keys for mutations
[ ] Conditional requests (ETags)
[ ] Versioning strategy
[ ] API health endpoint
```

## Summary

Choose your API paradigm based on your current needs, not theoretical future needs:

```
Current Need           | Best Choice
-----------------------|------------
Public API             | REST (OpenAPI documented)
Internal API (monolith)| REST (simple, fast to build)
Internal API (services)| REST or gRPC
Frontend → Backend     | REST (default) or GraphQL (if needed)
Mobile app → Backend   | REST (mobile-friendly)
Third-party integrations| REST (industry standard)
Real-time features     | WebSocket (with REST) or GraphQL subscriptions

Remember: You can always add GraphQL as a layer on top of REST.
You can always add gRPC for specific high-throughput internal services.
Start simple (REST), add complexity only when you need it.
```
