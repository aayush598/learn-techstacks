# Section 05: Request/Response Transformation

## Transformation Pipeline

The gateway transforms incoming requests and outgoing responses to normalize data formats, enforce pagination, validate schemas, and wrap responses in a consistent envelope.

```
┌─────────────────────────────────────────────────────────────────────┐
│                 REQUEST/RESPONSE TRANSFORMATION                     │
│                                                                     │
│  ┌──────────┐    ┌────────────────────────────────────────────┐    │
│  │  Client  │───→│              INBOUND PIPELINE              │    │
│  └──────────┘    │                                            │    │
│                   │  1. Body normalization                    │    │
│                   │     - camelCase → snake_case (internal)   │    │
│                   │     - Trim whitespace                     │    │
│                   │     - Coerce types                        │    │
│                   │                                            │    │
│                   │  2. Validation (Zod)                      │    │
│                   │     - Schema check against route spec     │    │
│                   │     - Return 422 with field errors        │    │
│                   │                                            │    │
│                   │  3. Pagination enforcer                   │    │
│                   │     - Default page=1, pageSize=25         │    │
│                   │     - Clamp pageSize to max (100)         │    │
│                   │     - Reject negative values              │    │
│                   │                                            │    │
│                   │  4. Tenant injection                      │    │
│                   │     - Attach tenantId to body/params      │    │
│                   │     - Row-level security enforced later   │    │
│                   └────────────────────────────────────────────┘    │
│                                            │                        │
│                                            ▼                        │
│                   ┌────────────────────────────────────────────┐    │
│                   │      INTERNAL SERVICE HANDLER              │    │
│                   └────────────────────────────────────────────┘    │
│                                            │                        │
│                                            ▼                        │
│                   ┌────────────────────────────────────────────┐    │
│                   │              OUTBOUND PIPELINE             │    │
│                   │                                            │    │
│                   │  1. Response envelope wrapping             │    │
│                   │     - Wrap data in { success, data, meta } │    │
│                   │                                            │    │
│                   │  2. Field transformation                   │    │
│                   │     - snake_case → camelCase (client)      │    │
│                   │     - Remove null fields (optional)        │    │
│                   │     - Date formatting (ISO 8601)           │    │
│                   │                                            │    │
│                   │  3. Error formatting                       │    │
│                   │     - Consistent error shape               │    │
│                   │     - requestId attached                   │    │
│                   │     - Stack traces removed in production   │    │
│                   │                                            │    │
│                   │  4. CORS headers                           │    │
│                   └────────────────────────────────────────────┘    │
│                                            │                        │
│                                            ▼                        │
│                   ┌──────────────┐                                 │
│                   │   Client     │                                 │
│                   └──────────────┘                                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Request Validation

```typescript
// Route-specific validation schemas
const ROUTE_SCHEMAS: Record<string, z.ZodSchema> = {
  'POST /api/v1/agents': AgentCreateSchema,
  'PUT /api/v1/agents/:id': AgentUpdateSchema,
  'POST /api/v1/calls': CallInitiateSchema,
  'POST /api/v1/campaigns': CampaignCreateSchema,
};

// Validation middleware
async function validationMiddleware(request: NextRequest, route: string): Promise<NextResponse | null> {
  const schema = ROUTE_SCHEMAS[route];
  if (!schema) return null; // No validation needed

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return formatError('invalid_json', 'Request body is not valid JSON', 400);
  }

  const result = schema.safeParse(body);
  if (!result.success) {
    const fieldErrors: Record<string, string[]> = {};
    for (const issue of result.error.issues) {
      const path = issue.path.join('.');
      if (!fieldErrors[path]) fieldErrors[path] = [];
      fieldErrors[path].push(issue.message);
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'validation_error',
        message: 'Request validation failed',
        details: fieldErrors,
        requestId: crypto.randomUUID(),
      },
    }, { status: 422 });
  }

  // Replace body with parsed data
  const nextRequest = new NextRequest(request.url, {
    ...request,
    body: JSON.stringify(result.data),
  });

  return null; // Continue with transformed request
}
```

## Pagination Enforcer

```typescript
interface PaginationParams {
  page: number;
  pageSize: number;
  sort?: string;
  order?: 'asc' | 'desc';
  filter?: Record<string, string>;
}

const DEFAULT_PAGINATION: PaginationParams = { page: 1, pageSize: 25 };
const MAX_PAGE_SIZE = 100;

function normalizePagination(searchParams: URLSearchParams): PaginationParams {
  const page = Math.max(1, parseInt(searchParams.get('page') ?? '1', 10) || 1);
  const rawSize = parseInt(searchParams.get('pageSize') ?? '25', 10) || 25;
  const pageSize = Math.min(MAX_PAGE_SIZE, Math.max(1, rawSize));

  return {
    page,
    pageSize,
    sort: searchParams.get('sort') ?? undefined,
    order: (searchParams.get('order') ?? 'asc') as 'asc' | 'desc',
  };
}

// Response metadata
interface PaginationMeta {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
  hasMore: boolean;
}

function buildPaginationMeta(total: number, params: PaginationParams): PaginationMeta {
  return {
    page: params.page,
    pageSize: params.pageSize,
    total,
    totalPages: Math.ceil(total / params.pageSize),
    hasMore: params.page * params.pageSize < total,
  };
}
```

## Error Formatting

```typescript
// Standard error format
interface ApiError {
  code: string;              // Machine-readable: 'validation_error', 'not_found', 'rate_limit_exceeded'
  message: string;           // Human-readable description
  details?: Record<string, string[]>;  // Field-level errors
  requestId: string;         // Correlation ID for debugging
  docs?: string;             // Link to documentation
}

// Error code catalog
const ERROR_CODES = {
  validation_error: { status: 422, message: 'Request validation failed' },
  not_found: { status: 404, message: 'Resource not found' },
  unauthorized: { status: 401, message: 'Authentication required' },
  forbidden: { status: 403, message: 'Insufficient permissions' },
  rate_limit_exceeded: { status: 429, message: 'Rate limit exceeded' },
  conflict: { status: 409, message: 'Resource conflict' },
  internal_error: { status: 500, message: 'Internal server error' },
  service_unavailable: { status: 503, message: 'Service temporarily unavailable' },
} as const;
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Case convention | camelCase in API, snake_case internally | JavaScript convention externally, SQL convention internally |
| Validation library | Zod | TypeScript-first, composable, excellent error messages |
| Pagination strategy | Offset-based (page/pageSize) | Simple, stateless, cacheable |
| Null handling | Omit null fields by default | Smaller payload, cleaner client code |
| Error format | RFC 7807 (Problem Details) inspired | Industry standard, extensible |

## Integration Points

- **Ch 07 (API Gateway)** — Transformation middleware runs as part of gateway pipeline
- **Ch 02 (Next.js Architecture)** — API route handlers receive normalized data
- **Ch 06 (Frontend)** — Client SDK parses camelCase response envelope

## Production Considerations

- **Payload Size**: Maximum request body: 1MB; larger payloads rejected with 413
- **Streaming**: Large responses use streaming (NDJSON) instead of buffering
- **Compression**: All responses compressed with brotli (preferred) or gzip
- **Null Fields**: `removeNullFields` header controls whether null fields are stripped
- **Date Format**: All timestamps in ISO 8601 UTC (e.g., `2026-03-15T14:30:00Z`)
- **Idempotency**: POST endpoints support `Idempotency-Key` header for safe retries
