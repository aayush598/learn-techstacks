# Section 06: Error Handling Strategy

## Overview

Error handling follows a layered strategy with custom error classes, React error boundaries, a centralized Express error middleware, and user-safe error messages. The goal is to never swallow errors silently, never leak internal details to users, and always provide enough context for debugging. Every error is logged, tracked, and assignable to a specific request.

## Error Hierarchy

```text
┌──────────────────────────────────────────────────────────────┐
│                      Error Class Hierarchy                     │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Error (built-in)                                              │
│    └── AppError (base)                                         │
│         ├── ValidationError      │ 400 Bad Request              │
│         ├── NotFoundError        │ 404 Not Found                │
│         ├── ConflictError        │ 409 Conflict                 │
│         ├── UnauthorizedError    │ 401 Unauthorized             │
│         ├── ForbiddenError       │ 403 Forbidden                │
│         ├── RateLimitError       │ 429 Too Many Requests        │
│         └── ExternalServiceError │ 502 Bad Gateway              │
│              ├── VoiceProviderError                              │
│              ├── STTProviderError                                │
│              └── LLMProviderError                                │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Custom Error Implementation

```typescript
// packages/shared/src/errors/app-error.ts
export abstract class AppError extends Error {
  public readonly requestId: string;
  public readonly timestamp: Date;
  public readonly isOperational: boolean;

  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly code: string,
    public readonly details?: Record<string, unknown>,
    isOperational = true
  ) {
    super(message);
    this.name = this.constructor.name;
    this.requestId = crypto.randomUUID();
    this.timestamp = new Date();
    this.isOperational = isOperational;
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
        details: this.details,
        requestId: this.requestId,
        docsUrl: `https://docs.voiceagent.example.com/errors#${this.code}`,
      },
    };
  }
}

export class ValidationError extends AppError {
  constructor(
    message: string,
    details?: Record<string, unknown>
  ) {
    super(message, 400, 'VALIDATION_ERROR', details);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(
      `${resource} not found.`,
      404,
      'NOT_FOUND',
      { resource, id }
    );
  }
}

export class ExternalServiceError extends AppError {
  constructor(
    service: string,
    originalError: Error
  ) {
    super(
      `External service ${service} returned an error.`,
      502,
      'DEPENDENCY_FAILURE',
      { service, originalMessage: originalError.message }
    );
  }
}
```

**Design decision: `isOperational` flag**. Operational errors (invalid input, missing resource, rate limit) are expected and handled gracefully. Programmer errors (null reference, type error) are unexpected and should crash the process for restart. The `isOperational` flag allows the error handler to distinguish between the two — operational errors return a clean response, programmer errors trigger restart logic.

## Global Error Handler (Express)

```typescript
// apps/api/src/middleware/error-handler.ts
import { type Request, type Response, type NextFunction } from 'express';
import { AppError } from '@voice-agent/shared';
import { logger } from '@voice-agent/shared';

export function globalErrorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
) {
  // Log everything
  logger.error({
    message: err.message,
    stack: err.stack,
    requestId: req.id,
    method: req.method,
    path: req.path,
    ip: req.ip,
    userId: req.user?.id,
  });

  // Known operational error → structured JSON response
  if (err instanceof AppError) {
    res.status(err.statusCode).json(err.toJSON());
    return;
  }

  // Zod validation error → transform to our format
  if (err.name === 'ZodError') {
    const zodError = err as ZodError;
    const validationError = new ValidationError(
      'Request validation failed.',
      {
        fields: zodError.errors.map((e) => ({
          path: e.path.join('.'),
          message: e.message,
          code: e.code,
        })),
      }
    );
    res.status(400).json(validationError.toJSON());
    return;
  }

  // Unexpected error → generic response (don't leak internals)
  logger.fatal({ err, requestId: req.id }, 'Unhandled error');
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred.',
      requestId: req.id,
      docsUrl: 'https://docs.voiceagent.example.com/errors#INTERNAL_ERROR',
    },
  });

  // If programmer error, restart the process
  if (!(err instanceof AppError) || !err.isOperational) {
    process.exit(1);
  }
}
```

## React Error Boundaries

```typescript
// packages/ui/src/error-boundary/error-boundary.tsx
import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to error tracking service
    logger.error({
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
    });
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div role="alert" className="error-boundary">
          <h2>Something went wrong</h2>
          <p>An unexpected error occurred. Please try again.</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

Error boundaries are placed at strategic levels:
1. **Root layout**: Catches any unhandled render error, prevents white screen
2. **Feature sections** (`/calls`, `/analytics`): Isolates errors to one feature
3. **Individual widgets** (voice call panel, analytics chart): Prevents one widget from crashing the whole page

## Service-Level Error Handling

Business logic uses a Result pattern to make error handling explicit:

```typescript
// packages/shared/src/result.ts
export type Result<T, E = AppError> =
  | { success: true; data: T }
  | { success: false; error: E };

export function ok<T>(data: T): Result<T> {
  return { success: true, data };
}

export function fail<E extends AppError>(error: E): Result<never, E> {
  return { success: false, error };
}
```

```typescript
// packages/voice/src/services/call-service.ts
export class CallService {
  async startCall(input: StartCallInput): Promise<Result<VoiceCall>> {
    // Validate
    const parsed = CreateVoiceCallSchema.safeParse(input);
    if (!parsed.success) {
      return fail(new ValidationError('Invalid input', {
        fields: parsed.error.errors,
      }));
    }

    // Check rate limit
    const canProceed = await this.rateLimiter.check(input.participantIds[0]);
    if (!canProceed) {
      return fail(new RateLimitError('Call limit reached'));
    }

    // Execute
    try {
      const call = await this.callRepo.create(parsed.data);
      return ok(call);
    } catch (err) {
      return fail(new ExternalServiceError('VoiceProvider', err as Error));
    }
  }
}
```

Consumers must handle both cases:

```typescript
const result = await callService.startCall(input);
if (!result.success) {
  // TypeScript narrows to { success: false, error: AppError }
  return res.status(result.error.statusCode).json(result.error.toJSON());
}
// TypeScript narrows to { success: true, data: VoiceCall }
return res.status(201).json(result.data);
```

## Logging and Monitoring

```typescript
// packages/shared/src/logger.ts
export const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  redact: ['req.headers.authorization', 'req.body.apiKey'],
  transport:
    process.env.NODE_ENV === 'development'
      ? { target: 'pino-pretty' }
      : undefined,
});
```

Errors are categorized by severity:
- **fatal**: Process will terminate (programmer errors)
- **error**: Request failed (validation, not found, downstream failures)
- **warn**: Recoverable issues (retry attempts, rate limit approaching)
- **info**: Normal operations

## Integration Points

- **Sentry**: `componentDidCatch` and global Express handler send errors to Sentry with full context (requestId, userId, session metadata)
- **Pino**: Structured JSON logging ships to stdout for containerized deployment
- **Datadog/Grafana**: Error rate metrics, p50/p95/p99 response times, and error distribution by endpoint
- **Slack alerts**: `fatal` errors trigger on-call notifications via webhook

## Production Considerations

1. **Error budget**: Track error budget (acceptable error rate × time window). 4xx errors are customer-facing issues, 5xx errors are SLO violations. Alert when error budget is 50% consumed.
2. **Sensitive data redaction**: Never log request bodies containing API keys, passwords, or PII. Use Pino's `redact` configuration and Zod's `z.string().transform()` to mask sensitive fields.
3. **Stack trace in production**: Source maps are uploaded to Sentry for stack trace deobfuscation. Raw stack traces are never exposed to clients.
4. **Graceful shutdown**: On `SIGTERM`, the process stops accepting new requests, drains existing connections, flushes pending logs, and exits cleanly.
5. **Correlation IDs**: Every incoming request gets a unique `requestId` (set at the API gateway or first middleware). This ID propagates to all downstream services, logs, and error responses for end-to-end tracing.
