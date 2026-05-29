# Section 03: API Design Conventions

## Overview

Our API follows RESTful conventions with consistent URL structure, standardized request/response formats, predictable error codes, and cursor-based pagination. These conventions ensure that any developer familiar with one endpoint can work with any other without consulting documentation. The API is designed for consumption by both the Next.js frontend and third-party integrations.

## URL Structure

```
GET    /api/v1/voice/calls                    # List calls
POST   /api/v1/voice/calls                    # Create call
GET    /api/v1/voice/calls/:id                 # Get call details
PATCH  /api/v1/voice/calls/:id                 # Update call
DELETE /api/v1/voice/calls/:id                 # Delete call
POST   /api/v1/voice/calls/:id/end            # Action: end call
POST   /api/v1/voice/calls/:id/transfer       # Action: transfer call
GET    /api/v1/voice/calls/:id/transcript     # Nested resource
GET    /api/v1/voice/calls/:id/analytics      # Nested resource
```

URL conventions follow these rules:
1. **Plural nouns** for collection resources (`/calls`, `/participants`)
2. **Lowercase kebab-case** for multi-word resources (`/call-logs`)
3. **API version prefix** (`/api/v1/`) to enable versioning without breaking existing clients
4. **Actions as verbs on specific resources** (`/calls/:id/end`) — not as query parameters
5. **Nested resources** for parent-child relationships (`/calls/:id/transcript`)

**Design decision: Actions over sub-resources**. Some API designs model call end as `PATCH /calls/:id` with `{ status: "ended" }`. We prefer explicit action endpoints because:
1. The database operation (triggering disconnect, billing stop) is semantic, not a simple field update
2. Documentation is clearer — "POST to end" is unambiguous
3. Webhook-style consumers benefit from the semantic URL

## HTTP Methods and Status Codes

```text
┌──────────────────────────────────────────────────────────────┐
│                  HTTP Method & Status Reference                │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Operation  │ Method   │ Success Code │ Error Codes           │
│  ───────────┼──────────┼──────────────┼──────────────────────│
│  List       │ GET      │ 200          │ 400, 401, 403          │
│  Create     │ POST     │ 201          │ 400, 401, 403, 409     │
│  Read       │ GET      │ 200          │ 401, 403, 404          │
│  Update     │ PATCH    │ 200          │ 400, 401, 403, 404     │
│  Delete     │ DELETE   │ 204          │ 401, 403, 404          │
│  Action     │ POST     │ 200/202      │ 400, 401, 403, 404     │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**PUT vs PATCH**: We use `PATCH` (partial update) exclusively and never `PUT` (full replacement). Partial updates are idempotent at the field level and avoid accidental data loss when a client omits a field.

**202 Accepted**: Action endpoints that trigger async background jobs return `202 Accepted` with a location header pointing to a status resource:

```http
POST /api/v1/voice/calls/abc123/transcribe
202 Accepted
Location: /api/v1/voice/calls/abc123/transcription-status
```

## Request/Response Format

All requests and responses use JSON with camelCase properties:

```typescript
// Request Body
{
  "participantIds": ["user_1", "user_2"],
  "recordingEnabled": true,
  "maxDurationSeconds": 3600,
  "metadata": {
    "campaignId": "camp_456",
    "source": "website"
  }
}
```

```typescript
// Response Body
{
  "id": "call_789",
  "status": "connecting",
  "participantIds": ["user_1", "user_2"],
  "recordingEnabled": true,
  "maxDurationSeconds": 3600,
  "metadata": {
    "campaignId": "camp_456",
    "source": "website"
  },
  "createdAt": "2024-06-15T10:30:00Z",
  "updatedAt": "2024-06-15T10:30:00Z"
}
```

**Timestamps** are always ISO 8601 in UTC (`2024-06-15T10:30:00Z`). Never use Unix timestamps, never use local time.

**IDs** are prefixed strings (`call_789`, `user_1`) for human readability in logs. The prefix identifies the resource type at a glance during debugging.

## Standardized Error Format

```typescript
// Error Response Body
{
  "error": {
    "code": "CALL_NOT_FOUND",
    "message": "The requested call was not found.",
    "details": {
      "callId": "call_invalid_123"
    },
    "requestId": "req_abc123",
    "docsUrl": "https://docs.voiceagent.example.com/errors#CALL_NOT_FOUND"
  }
}
```

Error conventions:
- **`code`**: Machine-readable UPPER_SNAKE_CASE string. Consumers use this for programmatic handling.
- **`message`**: Human-readable description. Must be user-safe (no stack traces, no internal details).
- **`details`**: Structured context for the error. Validation errors include the offending field and constraint.
- **`requestId`**: Correlates the error to server logs for debugging.
- **`docsUrl`**: Links to documentation explaining the error and resolution steps.

Common error codes:

```typescript
export enum ApiErrorCode {
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  NOT_FOUND = 'NOT_FOUND',
  CONFLICT = 'CONFLICT',
  RATE_LIMITED = 'RATE_LIMITED',
  UNAUTHORIZED = 'UNAUTHORIZED',
  FORBIDDEN = 'FORBIDDEN',
  INTERNAL_ERROR = 'INTERNAL_ERROR',
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  DEPENDENCY_FAILURE = 'DEPENDENCY_FAILURE', // e.g., external API downstream failure
}
```

## Pagination

All list endpoints use cursor-based pagination:

```http
GET /api/v1/voice/calls?cursor=call_500&limit=20
```

```typescript
// Response
{
  "data": [
    { /* call object */ },
    { /* call object */ }
  ],
  "pagination": {
    "nextCursor": "call_520",
    "hasMore": true,
    "totalCount": 1542,
    "limit": 20
  }
}
```

**Cursor-based over offset-based**: Offset pagination (`?page=3&limit=20`) is simpler but has two fatal flaws for a voice platform:
1. **Stale results**: Inserting a new item shifts all offsets, causing duplicates or missed items
2. **Performance**: `OFFSET 100000 LIMIT 20` requires scanning the first 100,020 rows

Cursor pagination uses a unique, sortable field (typically `id` or `createdAt`). Queries are always `WHERE cursor > ? ORDER BY cursor LIMIT ?` which can use a B-tree index efficiently.

The `totalCount` field is optional (it requires a count query, which can be expensive). We include it but cache it with a 30-second TTL.

## Validation

Request validation uses Zod schemas shared between client and server:

```typescript
// packages/shared/src/schemas/voice-call.ts
import { z } from 'zod';

export const CreateVoiceCallSchema = z.object({
  participantIds: z.array(z.string()).min(2).max(10),
  recordingEnabled: z.boolean().default(false),
  maxDurationSeconds: z.number().int().positive().max(86400).default(3600),
  metadata: z.record(z.string()).optional(),
});

export type CreateVoiceCallInput = z.infer<typeof CreateVoiceCallSchema>;
```

Server validation returns structured errors:

```typescript
// Error for: POST { "participantIds": ["user_1"] }
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": {
      "fields": [
        {
          "path": "participantIds",
          "message": "Array must contain at least 2 element(s)",
          "code": "too_small"
        }
      ]
    },
    "requestId": "req_def456"
  }
}
```

## Rate Limiting

Rate limit information is returned in response headers:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1718461800
Retry-After: 30
```

When exceeded:

```typescript
// 429 Too Many Requests
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Please retry after the specified period.",
    "details": {
      "retryAfterSeconds": 30,
      "currentLimit": 100,
      "windowSeconds": 60
    },
    "requestId": "req_ghi789"
  }
}
```

## Integration Points

- **Zod schemas**: Shared between API route handlers and frontend forms for consistent validation
- **OpenAPI/Swagger**: Generated from Zod schemas using `zod-to-openapi` for documentation
- **API client**: Generated TypeScript client from OpenAPI spec using `openapi-typescript`
- **Error tracking**: `requestId` is sent to Sentry for correlation between API errors and server-side traces

## Production Considerations

1. **API versioning strategy**: `v1` lives indefinitely. Breaking changes go in `v2` alongside `v1` for a deprecation period. Use the `Sunset` and `Deprecation` headers to communicate timelines.
2. **Request ID propagation**: Pass `requestId` from API gateway to all downstream services via headers. This enables end-to-end traceability across microservices.
3. **Response compression**: Enable Brotli compression for responses larger than 1 KB. Reduces bandwidth by 60-70% for JSON payloads.
4. **Idempotency keys**: POST endpoints accept an `Idempotency-Key` header to safely retry requests. Keys expire after 24 hours.
5. **Field selection**: Support `?fields=id,status,participantIds` for clients that want to reduce payload size.
6. **Content negotiation**: Return `application/json` by default. Accept `application/vnd.voiceagent.v2+json` for versioned content types in the future.
