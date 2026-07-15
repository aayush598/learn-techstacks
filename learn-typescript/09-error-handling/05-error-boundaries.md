# Error Boundaries in TypeScript

## Table of Contents

- [Overview](#overview)
- [Error Boundary Concept](#error-boundary-concept)
- [React Error Boundaries with TypeScript](#react-error-boundaries-with-typescript)
- [Server-Side Error Boundaries](#server-side-error-boundaries)
- [Global Error Handlers](#global-error-handlers)
- [Error Middleware](#error-middleware)
- [Structured Error Responses](#structured-error-responses)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Error boundaries catch errors during rendering, in event handlers, and in asynchronous code, preventing the entire application from crashing. They represent architectural boundaries where errors are caught, logged, and transformed into user-friendly responses.

---

## Error Boundary Concept

### What Error Boundaries Catch

```
Component Tree:
App
├── Header          ← renders fine
├── ErrorBoundary   ← catches errors from below
│   ├── Sidebar     ← throws error
│   └── Content     ← NOT rendered (parent failed)
└── Footer          ← renders fine (outside boundary)
```

### Error Boundary vs Try/Catch

```
Try/Catch:
  - Catches errors in imperative code
  - Limited to synchronous code (without async/await)
  - Doesn't catch errors in rendering or lifecycle methods
  - Doesn't prevent component tree from unmounting

Error Boundary:
  - Catches errors during rendering
  - Catches errors in lifecycle methods
  - Catches errors in child components
  - Replaces the failed tree with a fallback UI
```

### Where Errors Are NOT Caught by Error Boundaries

```typescript
// Error boundaries DO NOT catch:
// 1. Event handlers
function Button() {
  const handleClick = () => {
    try {
      riskyOperation(); // Must use try/catch here
    } catch (error) {
      handleError(error);
    }
  };
  return <button onClick={handleClick}>Click</button>;
}

// 2. Async code (setTimeout, Promise, async callbacks)
async function fetchData() {
  try {
    await fetch('/api'); // Must use try/catch
  } catch (error) {
    handleError(error);
  }
}

// 3. Server-side rendering
// 4. Errors thrown in the error boundary itself
```

---

## React Error Boundaries with TypeScript

### Basic Error Boundary Component

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('Error boundary caught:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  reset = (): void => {
    this.setState({ hasError: false, error: null });
  };

  render(): ReactNode {
    if (this.state.hasError && this.state.error) {
      if (typeof this.props.fallback === 'function') {
        return this.props.fallback(this.state.error, this.reset);
      }

      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div role="alert">
          <h2>Something went wrong</h2>
          <p>{this.state.error.message}</p>
          <button onClick={this.reset}>Try again</button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### Typed Error Boundary with Retry

```typescript
import React, { Component, ErrorInfo, ReactNode } from 'react';

interface ErrorBoundaryProps {
  children: ReactNode;
  maxRetries?: number;
  fallbackUI?: (props: {
    error: Error;
    retryCount: number;
    reset: () => void;
  }) => ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  retryCount: number;
}

class TypedErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  static defaultProps = {
    maxRetries: 3,
  };

  state: ErrorBoundaryState = {
    hasError: false,
    error: null,
    retryCount: 0,
  };

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.props.onError?.(error, errorInfo);
  }

  reset = (): void => {
    this.setState((prev) => ({
      hasError: false,
      error: null,
      retryCount: prev.retryCount + 1,
    }));
  };

  render(): ReactNode {
    if (this.state.hasError && this.state.error) {
      if (this.state.retryCount >= (this.props.maxRetries ?? 3)) {
        return (
          <div role="alert">
            <h2>Maximum retries exceeded</h2>
            <p>{this.state.error.message}</p>
          </div>
        );
      }

      if (this.props.fallbackUI) {
        return this.props.fallbackUI({
          error: this.state.error,
          retryCount: this.state.retryCount,
          reset: this.reset,
        });
      }

      return (
        <div role="alert">
          <h2>Error: {this.state.error.message}</h2>
          <p>Retry {this.state.retryCount} of {this.props.maxRetries}</p>
          <button onClick={this.reset}>Retry</button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### Using Error Boundaries

```typescript
// App.tsx
function App() {
  return (
    <ErrorBoundary
      maxRetries={3}
      onError={(error, info) => {
        logToService(error, info);
      }}
      fallbackUI={({ error, retryCount, reset }) => (
        <div className="error-fallback">
          <h2>Oops! Something went wrong</h2>
          <p>{error.message}</p>
          <p>Attempt {retryCount}/3</p>
          <button onClick={reset}>Try Again</button>
        </div>
      )}
    >
      <Dashboard />
    </ErrorBoundary>
  );
}

// Per-feature boundary
function Dashboard() {
  return (
    <div>
      <Header />
      <ErrorBoundary fallback={<SidebarError />}>
        <Sidebar />
      </ErrorBoundary>
      <ErrorBoundary fallback={<ContentError />}>
        <Content />
      </ErrorBoundary>
      <Footer />
    </div>
  );
}
```

---

## Server-Side Error Boundaries

### Express Error Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: Record<string, unknown>,
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// 404 handler
function notFoundHandler(req: Request, res: Response, next: NextFunction) {
  next(new AppError(404, 'NOT_FOUND', `Route ${req.method} ${req.url} not found`));
}

// Global error handler
function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  // Operational errors — expected failures
  if (err instanceof AppError && err.isOperational) {
    res.status(err.statusCode).json({
      status: 'error',
      code: err.code,
      message: err.message,
      details: err.details,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
    });
    return;
  }

  // Programming errors — bugs
  console.error('PROGRAMMING ERROR:', err);

  res.status(500).json({
    status: 'error',
    code: 'INTERNAL_ERROR',
    message: 'An unexpected error occurred',
    ...(process.env.NODE_ENV === 'development' && {
      stack: err.stack,
      message: err.message,
    }),
  });
}

// Usage
app.use(notFoundHandler);
app.use(errorHandler);
```

### NestJS Exception Filters

```typescript
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Internal server error';
    let code = 'INTERNAL_ERROR';

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const exResponse = exception.getResponse();
      message = typeof exResponse === 'string'
        ? exResponse
        : (exResponse as any).message;
      code = (exResponse as any).error || 'HTTP_ERROR';
    } else if (exception instanceof Error) {
      message = exception.message;
    }

    response.status(status).json({
      status: 'error',
      code,
      message,
      path: request.url,
      timestamp: new Date().toISOString(),
      ...(process.env.NODE_ENV === 'development' && {
        stack: exception instanceof Error ? exception.stack : undefined,
      }),
    });
  }
}
```

---

## Global Error Handlers

### Node.js Global Handlers

```typescript
// Process-level error handlers
process.on('uncaughtException', (error: Error) => {
  console.error('UNCAUGHT EXCEPTION:', error);
  // Log to error reporting service
  // Attempt graceful shutdown
  process.exit(1);
});

process.on('unhandledRejection', (reason: unknown, promise: Promise<any>) => {
  console.error('UNHANDLED REJECTION:', reason);
  // Log to error reporting service
  // Don't exit — this might be a recoverable situation
});

// For warnings about deprecations, etc.
process.on('warning', (warning: Error) => {
  console.warn('WARNING:', warning);
});
```

### Browser Global Error Handler

```typescript
// Capture unhandled errors
window.addEventListener('error', (event: ErrorEvent) => {
  console.error('Unhandled error:', event.error);
  // Report to error tracking service
  reportError({
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error,
  });
});

// Capture unhandled promise rejections
window.addEventListener('unhandledrejection', (event: PromiseRejectionEvent) => {
  console.error('Unhandled rejection:', event.reason);
  reportError({
    type: 'unhandled_rejection',
    reason: event.reason,
  });
  // Prevent the default console error
  event.preventDefault();
});

// React error handling
function reportError(error: {
  message?: string;
  filename?: string;
  lineno?: number;
  colno?: number;
  error?: Error;
  type?: string;
  reason?: unknown;
}) {
  // Send to Sentry, Datadog, etc.
  fetch('/api/errors', {
    method: 'POST',
    body: JSON.stringify({
      ...error,
      url: window.location.href,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
    }),
  }).catch(() => {
    // Silently fail if error reporting itself fails
  });
}
```

---

## Structured Error Responses

### API Error Response Format

```typescript
// Standard API error response
interface ApiErrorResponse {
  status: 'error';
  code: string;
  message: string;
  details?: Record<string, unknown>;
  stack?: string; // Only in development
  timestamp: string;
  path?: string;
}

// Validation error response
interface ValidationErrorResponse extends ApiErrorResponse {
  code: 'VALIDATION_ERROR';
  details: {
    fields: Array<{
      field: string;
      message: string;
      value?: unknown;
    }>;
  };
}

// Not found response
interface NotFoundResponse extends ApiErrorResponse {
  code: 'NOT_FOUND';
  details: {
    resource: string;
    identifier: string | number;
  };
}

// Paginated error response
interface PaginatedErrorResponse extends ApiErrorResponse {
  details: {
    totalErrors: number;
    errors: Array<{
      index: number;
      code: string;
      message: string;
    }>;
  };
}
```

### Error Response Builder

```typescript
class ErrorResponseBuilder {
  static validation(fields: Array<{ field: string; message: string }>): ValidationErrorResponse {
    return {
      status: 'error',
      code: 'VALIDATION_ERROR',
      message: `Validation failed for ${fields.length} field(s)`,
      details: { fields },
      timestamp: new Date().toISOString(),
    };
  }

  static notFound(resource: string, identifier: string | number): NotFoundResponse {
    return {
      status: 'error',
      code: 'NOT_FOUND',
      message: `${resource} with id "${identifier}" not found`,
      details: { resource, identifier },
      timestamp: new Date().toISOString(),
    };
  }

  static internal(message: string = 'Internal server error'): ApiErrorResponse {
    return {
      status: 'error',
      code: 'INTERNAL_ERROR',
      message,
      timestamp: new Date().toISOString(),
    };
  }
}
```

---

## Best Practices

1. **Place error boundaries at feature boundaries** — one per page, sidebar, widget.

2. **Always log errors** before showing fallback UI.

3. **Provide a "Try Again" button** in error boundary fallbacks.

4. **Use operational vs programming error distinction** to decide if error should be caught or crash.

5. **Centralize error handling middleware** in Express/NestJS applications.

6. **Never expose internal errors to clients** in production — return generic messages.

7. **Include error codes** in API responses for machine-readable error handling.

8. **Use structured error responses** with consistent format across your API.

---

## Interview Questions

### Q1: What is a React error boundary?

**Answer**: A React error boundary is a class component that catches JavaScript errors during rendering, lifecycle methods, and constructors of its child tree. It prevents the entire app from crashing by replacing the failed component tree with a fallback UI. Error boundaries don't catch errors in event handlers or async code.

### Q2: What errors do React error boundaries NOT catch?

**Answer**: They don't catch: (1) errors in event handlers (use try/catch there), (2) asynchronous code (setTimeout, Promise, async/await), (3) server-side rendering, (4) errors thrown in the error boundary itself. These are expected limitations of the boundary pattern.

### Q3: How do you implement a global error handler in Node.js?

**Answer**: Use `process.on('uncaughtException', handler)` for synchronous uncaught errors and `process.on('unhandledRejection', handler)` for rejected promises. Both should log the error and attempt graceful shutdown. In production, these handlers are the last line of defense.

### Q4: What is the difference between operational and programming errors?

**Answer**: Operational errors are expected failures (validation, not found, auth) — the system should handle them gracefully. Programming errors are bugs (null reference, type error) — they indicate code defects. Operational errors should be caught and returned as responses; programming errors should be allowed to crash so developers can fix them.

### Q5: What is a structured error response?

**Answer**: A consistent JSON format for API error responses with fields like `status`, `code`, `message`, `details`, and `timestamp`. Having a standardized format enables clients to handle errors programmatically and provides consistent debugging information across the API.
