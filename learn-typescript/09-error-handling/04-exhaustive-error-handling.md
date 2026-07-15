# Exhaustive Error Handling in TypeScript

## Table of Contents

- [Overview](#overview)
- [Exhaustive Switch on Error Types](#exhaustive-switch-on-error-types)
- [never Type for Unhandled Errors](#never-type-for-unhandled-errors)
- [Error Boundary Pattern](#error-boundary-pattern)
- [Error Catalog Pattern](#error-catalog-pattern)
- [Typed Catch Blocks](#typed-catch-blocks)
- [Error Discrimination](#error-discrimination)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Exhaustive error handling ensures that every possible error type is explicitly handled. TypeScript's type system can enforce this — if you add a new error type and forget to handle it, the compiler will catch it. This is critical for building robust error handling in large codebases.

---

## Exhaustive Switch on Error Types

### Discriminated Union Errors

```typescript
// Define all possible errors as a discriminated union
type AppError =
  | { type: 'VALIDATION_ERROR'; field: string; message: string }
  | { type: 'NOT_FOUND'; resource: string; id: string }
  | { type: 'AUTH_ERROR'; reason: string }
  | { type: 'NETWORK_ERROR'; url: string; status: number }
  | { type: 'DATABASE_ERROR'; query: string };

function handleError(error: AppError): string {
  switch (error.type) {
    case 'VALIDATION_ERROR':
      return `Invalid ${error.field}: ${error.message}`;
    case 'NOT_FOUND':
      return `${error.resource} with id "${error.id}" not found`;
    case 'AUTH_ERROR':
      return `Authentication failed: ${error.reason}`;
    case 'NETWORK_ERROR':
      return `Network error calling ${error.url}: HTTP ${error.status}`;
    case 'DATABASE_ERROR':
      return `Database error executing: ${error.query}`;
    default:
      // If you remove a case above, this will cause a type error!
      const _exhaustive: never = error;
      return _exhaustive;
  }
}
```

### Adding a New Error Type

```typescript
// If you add a new error type:
type AppError =
  | { type: 'VALIDATION_ERROR'; field: string; message: string }
  | { type: 'NOT_FOUND'; resource: string; id: string }
  | { type: 'AUTH_ERROR'; reason: string }
  | { type: 'NETWORK_ERROR'; url: string; status: number }
  | { type: 'DATABASE_ERROR'; query: string }
  | { type: 'RATE_LIMIT_ERROR'; retryAfter: number }; // NEW!

// The switch statement will now have a TypeScript error:
// Type '{ type: "RATE_LIMIT_ERROR"; retryAfter: number; }' is not assignable to type 'never'
// because the 'RATE_LIMIT_ERROR' case is missing!
```

### Nested Exhaustive Handling

```typescript
type ApiError =
  | { type: 'CLIENT_ERROR'; clientError: { code: number; message: string } }
  | { type: 'SERVER_ERROR'; serverError: { code: number; trace: string } };

function handleApiError(error: ApiError): string {
  switch (error.type) {
    case 'CLIENT_ERROR': {
      switch (error.clientError.code) {
        case 400:
          return 'Bad Request';
        case 401:
          return 'Unauthorized';
        case 403:
          return 'Forbidden';
        case 404:
          return 'Not Found';
        case 429:
          return 'Too Many Requests';
        default: {
          const _exhaustive: never = error.clientError.code;
          return `Unknown client error: ${_exhaustive}`;
        }
      }
    }
    case 'SERVER_ERROR': {
      switch (error.serverError.code) {
        case 500:
          return 'Internal Server Error';
        case 502:
          return 'Bad Gateway';
        case 503:
          return 'Service Unavailable';
        default: {
          const _exhaustive: never = error.serverError.code;
          return `Unknown server error: ${_exhaustive}`;
        }
      }
    }
    default: {
      const _exhaustive: never = error;
      return _exhaustive;
    }
  }
}
```

---

## never Type for Unhandled Errors

### The never Type in Exhaustive Checks

```typescript
// never represents a value that never occurs
// Used in exhaustive switch: after handling all union members,
// the remaining type should be `never`

function processError(error: AppError): void {
  if (error.type === 'VALIDATION_ERROR') {
    console.log(error.field, error.message);
    return;
  }

  if (error.type === 'NOT_FOUND') {
    console.log(error.resource, error.id);
    return;
  }

  // If we reach here, error must be one of the remaining types
  // Using `never` ensures we've handled them all:
  const _unreachable: never = error;
  console.error('Unhandled error type:', _unreachable);
}

// This works because:
// 1. After removing VALIDATION_ERROR and NOT_FOUND from the union
// 2. The remaining type is the union of the other cases
// 3. If that union is NOT empty, assigning to `never` causes a type error
// 4. This catches missing cases at compile time
```

### never with Default Cases

```typescript
function getErrorMessage(error: AppError): string {
  switch (error.type) {
    case 'VALIDATION_ERROR':
      return error.message;
    case 'NOT_FOUND':
      return `Not found: ${error.resource}`;
    case 'AUTH_ERROR':
      return error.reason;
    case 'NETWORK_ERROR':
      return `HTTP ${error.status}`;
    case 'DATABASE_ERROR':
      return 'Database error';
    default:
      return exhaustiveSwitch(error);
  }
}

function exhaustiveSwitch(x: never): string {
  throw new Error(`Unhandled case: ${x}`);
}
```

---

## Error Boundary Pattern

### Class-Based Error Boundary

```typescript
// Error boundary catches errors at specific boundaries
class ErrorBoundary {
  private handlers = new Map<string, (error: Error) => void>();

  register(errorType: string, handler: (error: Error) => void): void {
    this.handlers.set(errorType, handler);
  }

  async execute<T>(operation: () => Promise<T>): Promise<T | null> {
    try {
      return await operation();
    } catch (error) {
      if (error instanceof Error) {
        const handler = this.handlers.get(error.name);
        if (handler) {
          handler(error);
          return null;
        }
      }
      throw error; // Re-throw if no handler registered
    }
  }
}

// Usage
const boundary = new ErrorBoundary();
boundary.register('ValidationError', (err) => {
  console.warn('Validation failed:', err.message);
});
boundary.register('NetworkError', (err) => {
  console.error('Network error:', err.message);
});

const result = await boundary.execute(async () => {
  return await fetchUserData('123');
});
```

### Typed Error Boundaries

```typescript
type ErrorBoundaryConfig<TError extends Error> = {
  errorType: new (...args: any[]) => TError;
  handler: (error: TError) => void;
};

class TypedErrorBoundary {
  private configs: ErrorBoundaryConfig<any>[] = [];

  register<T extends Error>(config: ErrorBoundaryConfig<T>): void {
    this.configs.push(config);
  }

  async execute<T>(operation: () => Promise<T>): Promise<T | null> {
    try {
      return await operation();
    } catch (error) {
      for (const config of this.configs) {
        if (error instanceof config.errorType) {
          config.handler(error);
          return null;
        }
      }
      throw error;
    }
  }
}

// Usage
const boundary = new TypedErrorBoundary();

boundary.register({
  errorType: ValidationError,
  handler: (err) => console.warn(`Validation: ${err.field} — ${err.message}`),
});

boundary.register({
  errorType: NotFoundError,
  handler: (err) => console.warn(`Not found: ${err.resource}`),
});
```

---

## Error Catalog Pattern

### Centralized Error Definitions

```typescript
// error-catalog.ts
interface ErrorDefinition {
  code: string;
  message: string;
  statusCode: number;
  category: 'client' | 'server' | 'network';
}

const ERROR_CATALOG = {
  VALIDATION_FAILED: {
    code: 'E1000',
    message: 'Validation failed',
    statusCode: 400,
    category: 'client',
  },
  REQUIRED_FIELD: {
    code: 'E1001',
    message: 'Required field missing',
    statusCode: 400,
    category: 'client',
  },
  NOT_FOUND: {
    code: 'E2000',
    message: 'Resource not found',
    statusCode: 404,
    category: 'client',
  },
  UNAUTHORIZED: {
    code: 'E3000',
    message: 'Authentication required',
    statusCode: 401,
    category: 'client',
  },
  RATE_LIMITED: {
    code: 'E4000',
    message: 'Rate limit exceeded',
    statusCode: 429,
    category: 'client',
  },
  DATABASE_ERROR: {
    code: 'E5000',
    message: 'Database error',
    statusCode: 500,
    category: 'server',
  },
  SERVICE_UNAVAILABLE: {
    code: 'E5001',
    message: 'Service unavailable',
    statusCode: 503,
    category: 'server',
  },
} as const;

type ErrorCode = keyof typeof ERROR_CATALOG;

class CatalogError extends Error {
  public readonly code: string;
  public readonly statusCode: number;
  public readonly category: string;

  constructor(code: ErrorCode, details?: Record<string, unknown>) {
    const definition = ERROR_CATALOG[code];
    super(definition.message);
    this.name = 'CatalogError';
    this.code = definition.code;
    this.statusCode = definition.statusCode;
    this.category = definition.category;
    this.details = details;
    Object.setPrototypeOf(this, CatalogError.prototype);
  }

  details?: Record<string, unknown>;
}

// Usage
function throwNotFound(resource: string, id: string): never {
  throw new CatalogError('NOT_FOUND', { resource, id });
}

function throwValidation(field: string, reason: string): never {
  throw new CatalogError('VALIDATION_FAILED', { field, reason });
}
```

---

## Typed Catch Blocks

### Narrowing Error Types in Catch

```typescript
async function apiCall(url: string): Promise<any> {
  try {
    const response = await fetch(url);

    if (response.status === 404) {
      throw new NotFoundError('Endpoint', url);
    }

    if (response.status === 401) {
      throw new AuthenticationError('Invalid credentials');
    }

    if (!response.ok) {
      throw new AppError('API_ERROR', `HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    // Typed catch blocks using narrowing
    if (error instanceof NotFoundError) {
      return { status: 404, message: error.message };
    }

    if (error instanceof AuthenticationError) {
      return { status: 401, message: error.message };
    }

    if (error instanceof AppError) {
      return { status: error.statusCode, message: error.message };
    }

    if (error instanceof TypeError) {
      // Network error (fetch throws TypeError on network failure)
      return { status: 0, message: 'Network error' };
    }

    // Unknown error
    console.error('Unexpected error:', error);
    return { status: 500, message: 'Internal Server Error' };
  }
}
```

---

## Error Discrimination

### Using `in` Operator

```typescript
type HttpError =
  | { status: number; message: string; response?: Response }
  | { status: number; message: string; cause: Error };

function handleHttpError(error: HttpError): string {
  if ('response' in error && error.response) {
    // Has response — server returned an error
    return `Server error ${error.status}: ${error.message}`;
  }

  if ('cause' in error) {
    // Has cause — network or client error
    return `Request failed: ${error.cause.message}`;
  }

  return `HTTP error ${error.status}`;
}
```

### Using Type Predicates

```typescript
function isValidationError(error: unknown): error is ValidationError {
  return (
    error instanceof Error &&
    error.name === 'ValidationError' &&
    'field' in error
  );
}

function isNotFoundError(error: unknown): error is NotFoundError {
  return (
    error instanceof Error &&
    error.name === 'NotFoundError' &&
    'resource' in error
  );
}

function handleError(error: unknown): string {
  if (isValidationError(error)) {
    return `Invalid ${error.field}: ${error.message}`;
  }
  if (isNotFoundError(error)) {
    return `${error.resource} not found`;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}
```

---

## Best Practices

1. **Use discriminated unions** for error types — enable exhaustive switch checking.

2. **Always include a `never` check** at the end of exhaustive switches.

3. **Add new error types** and let the compiler tell you where to handle them.

4. **Use type predicates** (`is` keyword) to narrow `unknown` errors.

5. **Centralize error definitions** in a catalog for consistency across the codebase.

6. **Layer error handling** — catch specific types, re-throw unknown.

---

## Interview Questions

### Q1: What is exhaustive error handling and why is it important?

**Answer**: Exhaustive error handling means every possible error type is explicitly handled. TypeScript enforces this using the `never` type — if a new error type is added and a case is missing, the assignment to `never` causes a compile error. This prevents accidentally unhandled error paths.

### Q2: How does the `never` type work in exhaustive checks?

**Answer**: `never` represents a value that can never exist. In an exhaustive switch, after handling all union members, the remaining type should be `never`. If it's not `never` (because a case is missing), TypeScript raises a compile error, catching the missing case.

### Q3: What is the error catalog pattern?

**Answer**: A centralized registry of all possible application errors with their codes, messages, HTTP status codes, and categories. Instead of scattering error definitions across the codebase, the catalog provides a single source of truth. Errors are thrown using the catalog keys, ensuring consistency.

### Q4: How do you handle errors with `unknown` type in catch blocks?

**Answer**: Use a series of `instanceof` checks or type predicates to narrow the type. Start with the most specific types (custom errors) and fall through to generic types (Error, then unknown). Always include a fallback for truly unknown values.

### Q5: What is an error boundary pattern?

**Answer**: An error boundary is a wrapper that catches errors at a specific point in the call stack, preventing them from propagating further. It's like a try/catch at an architectural boundary — it handles errors gracefully and allows the rest of the application to continue functioning.
