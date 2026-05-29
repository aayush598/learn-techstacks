# Section 04: Error Handling Patterns

## Overview

The SDK provides typed error handling for every API interaction. Errors are mapped to specific classes based on HTTP status code and error code, enabling instanceof checks and granular error handling. The error system includes support for retryable errors, network errors, and timeout handling.

## Architecture

```
Error Class Hierarchy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ApiError (base)
├── AuthenticationError     → 401 — Invalid/expired credentials
├── AuthorizationError      → 403 — Insufficient permissions
├── NotFoundError           → 404 — Resource not found
├── ValidationError         → 400/422 — Invalid request data
├── ConflictError           → 409 — Resource state conflict
├── RateLimitError          → 429 — Rate limit exceeded
├── ServerError             → 500/502/503 — Server error
├── NetworkError            → Fetch failed — network issue
└── TimeoutError            → Request exceeded timeout

Error Handling Patterns:
  // Pattern 1: Specific error handling
  try {
    await client.agents.get('nonexistent');
  } catch (error) {
    if (error instanceof NotFoundError) {
      // Handle not found
    } else if (error instanceof RateLimitError) {
      // Wait and retry
    } else if (error instanceof ValidationError) {
      // Fix validation
    } else {
      throw error; // Re-throw unexpected errors
    }
  }

  // Pattern 2: Retry wrapper
  const result = await withRetry(
    () => client.agents.create(data),
    { maxRetries: 3, retryOn: [RateLimitError, NetworkError] }
  );

  // Pattern 3: Error code switch
  try {
    await client.agents.deploy(id);
  } catch (error) {
    if (error instanceof ApiError) {
      switch (error.code) {
        case 'AGENT_ALREADY_DEPLOYED':
          // Handle specific error code
          break;
        case 'AGENT_VALIDATION_FAILED':
          // Handle validation
          break;
      }
    }
  }
```

## Design Decisions

- **Typed Error Classes**: Instanceof checks work across module boundaries; each class has a distinct name
- **Error Code Preservation**: Server error codes are available on error objects for fine-grained handling
- **Retry Wrapper**: Built-in retry utility for transient errors (rate limits, network failures, 5xx)
- **Error Cause Chain**: Network errors preserve the original cause via Error.cause for debugging

## Implementation Approach

```typescript
// Error class definitions
class ApiError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly code: string,
    options?: ErrorOptions,
  ) {
    super(message, options);
    this.name = 'ApiError';
  }

  get isRetryable(): boolean {
    return [408, 429, 500, 502, 503].includes(this.statusCode);
  }
}

class AuthenticationError extends ApiError {
  constructor(message: string, code: string) {
    super(message, 401, code);
    this.name = 'AuthenticationError';
  }
}

class AuthorizationError extends ApiError {
  constructor(message: string, code: string) {
    super(message, 403, code);
    this.name = 'AuthorizationError';
  }
}

class NotFoundError extends ApiError {
  constructor(message: string, code: string) {
    super(message, 404, code);
    this.name = 'NotFoundError';
  }
}

class ValidationError extends ApiError {
  public readonly details?: Array<{ field: string; code: string; message: string }>;

  constructor(message: string, code: string, details?: Array<{ field: string; code: string; message: string }>) {
    super(message, 400, code);
    this.name = 'ValidationError';
    this.details = details;
  }
}

class ConflictError extends ApiError {
  constructor(message: string, code: string) {
    super(message, 409, code);
    this.name = 'ConflictError';
  }
}

class RateLimitError extends ApiError {
  public readonly retryAfter: number;

  constructor(message: string, code: string, retryAfter?: number) {
    super(message, 429, code);
    this.name = 'RateLimitError';
    this.retryAfter = retryAfter || 5;
  }
}

class ServerError extends ApiError {
  constructor(message: string, code: string) {
    super(message, 500, code);
    this.name = 'ServerError';
  }
}

class NetworkError extends ApiError {
  constructor(message: string, cause?: Error) {
    super(message, 0, 'NETWORK_ERROR', { cause });
    this.name = 'NetworkError';
  }

  override get isRetryable(): boolean {
    return true;
  }
}

class TimeoutError extends ApiError {
  constructor(timeoutMs: number) {
    super(`Request timed out after ${timeoutMs}ms`, 0, 'TIMEOUT');
    this.name = 'TimeoutError';
  }

  override get isRetryable(): boolean {
    return true;
  }
}

// Retry wrapper
interface RetryOptions {
  maxRetries: number;
  baseDelayMs: number;
  retryOn?: Array<new (...args: unknown[]) => ApiError>;
  onRetry?: (error: Error, attempt: number) => void;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = { maxRetries: 3, baseDelayMs: 1000 },
): Promise<T> {
  let lastError: Error;

  for (let attempt = 1; attempt <= options.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Check if this error type is retryable
      const isRetryable = options.retryOn
        ? options.retryOn.some(ErrorType => error instanceof ErrorType)
        : (error instanceof ApiError && error.isRetryable);

      if (!isRetryable || attempt === options.maxRetries) {
        throw error;
      }

      // Calculate delay with exponential backoff
      const delay = options.baseDelayMs * Math.pow(2, attempt - 1);
      options.onRetry?.(error as Error, attempt);

      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}

// Usage
const result = await withRetry(
  () => client.agents.create(data),
  {
    maxRetries: 3,
    baseDelayMs: 1000,
    retryOn: [RateLimitError, NetworkError, ServerError],
    onRetry: (error, attempt) => {
      console.warn(`Retry ${attempt}: ${error.message}`);
    },
  },
);
```

## Integration Points

- **Plugin System**: Error logging plugin captures all errors for telemetry
- **Retry Plugin**: Automatic retry plugin applies withRetry to all requests
- **Error Reporting**: Unhandled errors can be forwarded to error tracking services

## Production Considerations

- **Retry Budget**: Total retry time should not exceed 30 seconds to maintain UX
- **Error Telemetry**: SDK sends error metrics for monitoring SDK health
- **Sensitive Data**: Never include API keys or tokens in error messages
- **Backoff Strategy**: Exponential backoff with jitter for rate limit retries

## Open-Source Tools

- **p-retry**: Promise-based retry utility with backoff
