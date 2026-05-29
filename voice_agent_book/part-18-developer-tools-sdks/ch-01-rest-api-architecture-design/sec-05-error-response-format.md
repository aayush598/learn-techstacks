# Section 05: Error Response Format

## Overview

The Voice Agent API uses a standardized error envelope for all error responses. Every error includes a machine-readable error code, a human-readable message, a request ID for debugging, and optional details for validation errors. This consistent format allows clients to handle errors programmatically without parsing response bodies.

## Architecture

```
Error Response Envelope
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HTTP 400 Bad Request:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "requestId": "req_abc_123",
    "details": [
      {
        "field": "voice.provider",
        "code": "INVALID_ENUM",
        "message": "Must be one of: elevenlabs, azure, google"
      },
      {
        "field": "model.temperature",
        "code": "RANGE_EXCEEDED",
        "message": "Must be between 0.0 and 2.0"
      }
    ]
  }
}

Error Code Taxonomy:
  4xx Client Errors:
    VALIDATION_ERROR    → Invalid request body
    NOT_FOUND          → Resource doesn't exist
    RATE_LIMITED       → Too many requests
    UNAUTHORIZED       → Missing/invalid auth
    FORBIDDEN          → Insufficient permissions
    CONFLICT           → Resource state conflict
    IDEMPOTENCY_ERROR  → Idempotency key replayed with different body

  5xx Server Errors:
    INTERNAL_ERROR     → Unexpected server error
    SERVICE_UNAVAILABLE → Downstream service failure
    TIMEOUT            → Request exceeded processing time
```

## Design Decisions

- **Single Error Envelope**: All errors, regardless of type, follow the same structure — clients write one error handler
- **Machine-Readable Codes**: Error codes are stable strings (not numbers) suitable for switch-case handling
- **Validation Details**: Field-level errors include the failing field path and a specific sub-code for precise handling
- **Request ID**: Every error includes a request ID that maps to server logs for debugging

## Implementation Approach

```typescript
// Error type definitions
interface ApiError {
  code: ErrorCode;
  message: string;
  requestId: string;
  details?: ErrorDetail[];
  documentation_url?: string;
}

interface ErrorDetail {
  field: string;
  code: string;
  message: string;
  constraints?: Record<string, string>;
}

type ErrorCode =
  | 'VALIDATION_ERROR'
  | 'NOT_FOUND'
  | 'RATE_LIMITED'
  | 'UNAUTHORIZED'
  | 'FORBIDDEN'
  | 'CONFLICT'
  | 'IDEMPOTENCY_ERROR'
  | 'INTERNAL_ERROR'
  | 'SERVICE_UNAVAILABLE'
  | 'TIMEOUT';

// Error class hierarchy
class ApiErrorResponse extends Error {
  constructor(
    public readonly statusCode: number,
    public readonly code: ErrorCode,
    message: string,
    public readonly details?: ErrorDetail[],
  ) {
    super(message);
    this.name = 'ApiErrorResponse';
  }

  toJson(requestId: string): { error: ApiError } {
    return {
      error: {
        code: this.code,
        message: this.message,
        requestId,
        details: this.details,
      },
    };
  }
}

class ValidationError extends ApiErrorResponse {
  constructor(details: ErrorDetail[]) {
    super(400, 'VALIDATION_ERROR', 'Request validation failed', details);
  }
}

class NotFoundError extends ApiErrorResponse {
  constructor(resourceType: string, id: string) {
    super(404, 'NOT_FOUND', `${resourceType} '${id}' not found`);
  }
}

// Global error handler middleware
function errorHandler(error: Error, c: Context): Response {
  const requestId = c.get('requestId');

  if (error instanceof ApiErrorResponse) {
    return c.json(error.toJson(requestId), error.statusCode);
  }

  // Unexpected errors — log and return generic 500
  console.error('Unhandled error:', error, { requestId });
  return c.json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId,
    },
  }, 500);
}
```

## Integration Points

- **SDK Error Mapping**: SDK translates API error responses into typed error classes
- **Logging Pipeline**: Request ID links error responses to server-side log entries
- **Analytics**: Error codes are tracked as metrics for API health monitoring

## Production Considerations

- **Error Code Stability**: Never remove or repurpose error codes — clients depend on them
- **Sensitive Data**: Never include stack traces, internal hostnames, or database details in error responses
- **Rate Limit Errors**: Include Retry-After header with rate limit errors for automatic client backoff
- **Documentation URL**: Error responses can include a documentation URL linking to troubleshooting guides

## Open-Source Tools

- **Zod**: Validation error parsing and transformation into ErrorDetail format
- **Hono**: Global error handler middleware for consistent error responses
