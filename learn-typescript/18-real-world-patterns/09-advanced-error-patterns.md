# Advanced Error Handling Patterns

## Table of Contents

1. [Typed Errors in Large Applications](#typed-errors-in-large-applications)
2. [Error Catalog Pattern](#error-catalog-pattern)
3. [Never-Throwing Pattern](#never-throwing-pattern)
4. [Result Type Deep Dive](#result-type-deep-dive)
5. [neverthrow Library Patterns](#neverthrow-library-patterns)
6. [fp-ts Either Pattern](#fp-ts-either-pattern)
7. [Error Handling in Async/Await](#error-handling-in-asyncawait)
8. [Typed Error Boundaries (React)](#typed-error-boundaries-react)
9. [Server-Side Error Middleware](#server-side-error-middleware)
10. [Error Serialization for APIs](#error-serialization-for-apis)
11. [Error Recovery Patterns](#error-recovery-patterns)
12. [Typed Try-Catch with Discriminated Unions](#typed-try-catch-with-discriminated-unions)
13. [Interview Questions](#interview-questions)

---

## Typed Errors in Large Applications

```typescript
// In large applications, using `throw new Error('something went wrong')`
// loses all type information. Typed errors fix this.

// ============= The Problem =============
async function fetchUser(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
      // This error has no structure - calling code can't
      // distinguish between 404, 500, or network errors
    }
    return await response.json();
  } catch (error) {
    // error is `unknown` - you can't safely access properties
    if (error instanceof Error) {
      console.log(error.message); // only string message available
    }
    throw error;
  }
}

// ============= The Solution: Discriminated Error Types =============
interface AppError {
  code: string;
  message: string;
  timestamp: Date;
  context?: Record<string, unknown>;
}

interface NotFoundError extends AppError {
  code: 'NOT_FOUND';
  resource: string;
  resourceId: string;
}

interface ValidationError extends AppError {
  code: 'VALIDATION_ERROR';
  field: string;
  constraint: string;
}

interface NetworkError extends AppError {
  code: 'NETWORK_ERROR';
  url: string;
  status?: number;
}

interface AuthError extends AppError {
  code: 'AUTH_ERROR';
  reason: 'token_expired' | 'invalid_token' | 'insufficient_permissions';
}

type TypedError = NotFoundError | ValidationError | NetworkError | AuthError;

// Now error handling is exhaustive and type-safe:
function handleError(error: TypedError): string {
  switch (error.code) {
    case 'NOT_FOUND':
      // error is NotFoundError - resource and resourceId are available
      return `Resource ${error.resource} with id ${error.resourceId} not found`;

    case 'VALIDATION_ERROR':
      // error is ValidationError - field and constraint are available
      return `Validation failed on ${error.field}: ${error.constraint}`;

    case 'NETWORK_ERROR':
      // error is NetworkError - url and status are available
      return `Network error fetching ${error.url}`;

    case 'AUTH_ERROR':
      // error is AuthError - reason is available
      switch (error.reason) {
        case 'token_expired': return 'Session expired, please log in again';
        case 'invalid_token': return 'Invalid authentication token';
        case 'insufficient_permissions': return 'You lack required permissions';
      }
      break;

    default:
      // TypeScript ensures exhaustiveness
      const _exhaustive: never = error;
      return 'Unknown error';
  }
}

// Factory functions for creating typed errors
function createNotFoundError(resource: string, id: string): NotFoundError {
  return {
    code: 'NOT_FOUND',
    message: `${resource} with id ${id} not found`,
    timestamp: new Date(),
    resource,
    resourceId: id,
  };
}

function createValidationError(field: string, constraint: string): ValidationError {
  return {
    code: 'VALIDATION_ERROR',
    message: `Validation failed on ${field}: ${constraint}`,
    timestamp: new Date(),
    field,
    constraint,
  };
}

function createNetworkError(url: string, status?: number): NetworkError {
  return {
    code: 'NETWORK_ERROR',
    message: `Network error fetching ${url}`,
    timestamp: new Date(),
    url,
    status,
  };
}
```

---

## Error Catalog Pattern

```typescript
// A centralized catalog of all possible application errors
// with codes, messages, and metadata:

interface ErrorDefinition {
  code: string;
  message: string;
  httpStatus: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  retryable: boolean;
  category: 'auth' | 'validation' | 'not_found' | 'network' | 'internal';
}

const ERROR_CATALOG = {
  AUTH_001: {
    code: 'AUTH_001',
    message: 'Authentication token has expired',
    httpStatus: 401,
    severity: 'medium',
    retryable: false,
    category: 'auth',
  },
  AUTH_002: {
    code: 'AUTH_002',
    message: 'Invalid authentication token',
    httpStatus: 401,
    severity: 'high',
    retryable: false,
    category: 'auth',
  },
  AUTH_003: {
    code: 'AUTH_003',
    message: 'Insufficient permissions for this action',
    httpStatus: 403,
    severity: 'medium',
    retryable: false,
    category: 'auth',
  },
  VAL_001: {
    code: 'VAL_001',
    message: 'Required field is missing',
    httpStatus: 400,
    severity: 'low',
    retryable: false,
    category: 'validation',
  },
  VAL_002: {
    code: 'VAL_002',
    message: 'Field value is out of allowed range',
    httpStatus: 400,
    severity: 'low',
    retryable: false,
    category: 'validation',
  },
  NF_001: {
    code: 'NF_001',
    message: 'Requested resource was not found',
    httpStatus: 404,
    severity: 'low',
    retryable: false,
    category: 'not_found',
  },
  NET_001: {
    code: 'NET_001',
    message: 'Connection to external service failed',
    httpStatus: 502,
    severity: 'high',
    retryable: true,
    category: 'network',
  },
  NET_002: {
    code: 'NET_002',
    message: 'External service timed out',
    httpStatus: 504,
    severity: 'high',
    retryable: true,
    category: 'network',
  },
  INT_001: {
    code: 'INT_001',
    message: 'Internal server error',
    httpStatus: 500,
    severity: 'critical',
    retryable: false,
    category: 'internal',
  },
} as const satisfies Record<string, ErrorDefinition>;

type ErrorCode = keyof typeof ERROR_CATALOG;
type ErrorInfo = (typeof ERROR_CATALOG)[ErrorCode];

// Type-safe error creation from catalog
class ApplicationError extends Error {
  readonly code: ErrorCode;
  readonly httpStatus: number;
  readonly severity: ErrorInfo['severity'];
  readonly retryable: ErrorInfo['retryable'];
  readonly category: ErrorInfo['category'];
  readonly details: Record<string, unknown>;
  readonly timestamp: Date;

  constructor(code: ErrorCode, details: Record<string, unknown> = {}) {
    const errorDef = ERROR_CATALOG[code];
    super(errorDef.message);
    this.name = 'ApplicationError';
    this.code = code;
    this.httpStatus = errorDef.httpStatus;
    this.severity = errorDef.severity;
    this.retryable = errorDef.retryable;
    this.category = errorDef.category;
    this.details = details;
    this.timestamp = new Date();
  }
}

// Usage:
throw new ApplicationError('AUTH_001', { userId: '123', tokenExpiry: '2024-01-01' });

// Error handler in Express/Hono middleware
function errorMiddleware(error: unknown, req: Request, res: Response, next: Function) {
  if (error instanceof ApplicationError) {
    // All properties are fully typed
    console.error(`[${error.severity}] ${error.code}: ${error.message}`);

    if (error.severity === 'critical') {
      // Alert on-call team
      alertOnCall(error);
    }

    res.status(error.httpStatus).json({
      error: {
        code: error.code,
        message: error.message,
        details: error.details,
        retryable: error.retryable,
      },
    });
  } else {
    res.status(500).json({
      error: {
        code: 'INT_001',
        message: 'Internal server error',
        retryable: false,
      },
    });
  }
}
```

---

## Never-Throwing Pattern

```typescript
// Instead of throwing errors, return typed results.
// This forces callers to handle errors at compile time.

// The never-throwing wrapper
async function tryCatch<T>(
  fn: () => Promise<T>
): Promise<{ ok: true; value: T } | { ok: false; error: Error }> {
  try {
    const value = await fn();
    return { ok: true, value };
  } catch (error) {
    return {
      ok: false,
      error: error instanceof Error ? error : new Error(String(error)),
    };
  }
}

// Usage - caller MUST check the result
async function loadUserProfile(id: string) {
  const result = await tryCatch(() => fetchUser(id));

  if (!result.ok) {
    // result.error is Error - handle it
    console.error('Failed to load user:', result.error.message);
    return null;
  }

  // result.value is the user data
  return result.value;
}

// More specific never-throwing with typed errors
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function fetchUserTyped(
  id: string
): Promise<Result<User, NotFoundError | NetworkError>> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (response.status === 404) {
      return {
        ok: false,
        error: createNotFoundError('User', id),
      };
    }
    if (!response.ok) {
      return {
        ok: false,
        error: createNetworkError(`/api/users/${id}`, response.status),
      };
    }
    const user = await response.json();
    return { ok: true, value: user };
  } catch (error) {
    return {
      ok: false,
      error: createNetworkError(`/api/users/${id}`),
    };
  }
}

// Caller handles both success and error paths type-safely
async function displayUser(id: string) {
  const result = await fetchUserTyped(id);

  if (!result.ok) {
    switch (result.error.code) {
      case 'NOT_FOUND':
        showNotFound(result.error.resource, result.error.resourceId);
        break;
      case 'NETWORK_ERROR':
        showRetryPrompt(result.error.url);
        break;
    }
    return;
  }

  // result.value is User
  showUser(result.value);
}
```

---

## Result Type Deep Dive

```typescript
// A complete Result type implementation (Railway-Oriented Programming):

type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// Construction helpers
function Ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// Type guard
function isOk<T, E>(result: Result<T, E>): result is { ok: true; value: T } {
  return result.ok;
}

function isErr<T, E>(result: Result<T, E>): result is { ok: false; error: E } {
  return !result.ok;
}

// Monadic operations (chainable)
function map<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  return result.ok ? Ok(fn(result.value)) : result;
}

function mapError<T, E, F>(
  result: Result<T, E>,
  fn: (error: E) => F
): Result<T, F> {
  return result.ok ? result : Err(fn(result.error));
}

function flatMap<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  return result.ok ? fn(result.value) : result;
}

// Unwrap (unsafe - throws if Err)
function unwrap<T, E>(result: Result<T, E>): T {
  if (result.ok) return result.value;
  throw result.error;
}

// Unwrap with default
function unwrapOr<T, E>(result: Result<T, E>, defaultValue: T): T {
  return result.ok ? result.value : defaultValue;
}

// Unwrap with factory
function unwrapOrElse<T, E>(result: Result<T, E>, fn: (error: E) => T): T {
  return result.ok ? result.value : fn(result.error);
}

// Combine multiple Results
function all<T, E>(results: Result<T, E>[]): Result<T[], E> {
  const values: T[] = [];
  for (const result of results) {
    if (!result.ok) return result;
    values.push(result.value);
  }
  return Ok(values);
}

// Async versions
async function mapAsync<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Promise<U>
): Promise<Result<U, E>> {
  return result.ok ? Ok(await fn(result.value)) : result;
}

async function flatMapAsync<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Promise<Result<U, E>>
): Promise<Result<U, E>> {
  return result.ok ? fn(result.value) : result;
}

// ============= Railway-Oriented Programming =============
// Chain operations where errors short-circuit:

interface User {
  id: string;
  name: string;
  email: string;
}

interface Post {
  id: string;
  authorId: string;
  title: string;
}

function validateUserId(id: string): Result<string, ValidationError> {
  if (!id || id.length === 0) {
    return Err(createValidationError('userId', 'cannot be empty'));
  }
  return Ok(id);
}

function validateEmail(email: string): Result<string, ValidationError> {
  if (!email.includes('@')) {
    return Err(createValidationError('email', 'invalid format'));
  }
  return Ok(email);
}

async function findUser(id: string): Promise<Result<User, NotFoundError | NetworkError>> {
  // implementation...
  return Ok({ id, name: 'Alice', email: 'alice@test.com' });
}

async function findPostsByAuthor(authorId: string): Promise<Result<Post[], NetworkError>> {
  // implementation...
  return Ok([{ id: 'p1', authorId, title: 'Hello' }]);
}

// Chain operations - error short-circuits
async function getUserPosts(
  userId: string,
  email: string
): Promise<Result<Post[], ValidationError | NotFoundError | NetworkError>> {
  return flatMap(
    flatMap(
      validateUserId(userId),
      (validId) => validateEmail(email).map(() => validId)
    ),
    (validId) => ({ ok: true as const, value: validId })
  ) satisfies Result<string, ValidationError>;
}

// More readable version with helper
function pipe2<T, U, V>(
  result: Result<T, any>,
  fn1: (v: T) => Result<U, any>,
  fn2: (v: U) => Result<V, any>
): Result<V, any> {
  return flatMap(map(result, fn1), fn2);
}

// ============= Pattern matching =============
function match<T, E, U>(
  result: Result<T, E>,
  patterns: {
    ok: (value: T) => U;
    err: (error: E) => U;
  }
): U {
  return result.ok ? patterns.ok(result.value) : patterns.err(result.error);
}

// Usage
const result = validateUserId('123');
const message = match(result, {
  ok: (id) => `Valid user: ${id}`,
  err: (error) => `Validation failed: ${error.constraint}`,
});
```

---

## neverthrow Library Patterns

```typescript
// neverthrow provides Result<T, E> with rich combinators:

import { Result, Ok, Err, ResultAsync } from 'neverthrow';

// Basic usage
function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return Err('Cannot divide by zero');
  return Ok(a / b);
}

// Async operations
function fetchUserData(id: string): ResultAsync<User, ApplicationError> {
  return ResultAsync.fromPromise(
    fetch(`/api/users/${id}`).then(async (res) => {
      if (!res.ok) throw new ApplicationError('NF_001');
      return res.json() as Promise<User>;
    }),
    (error) => new ApplicationError('NET_001')
  );
}

// Chaining with map and andThen
function processUser(id: string): ResultAsync<string, ApplicationError> {
  return fetchUserData(id)
    .map((user) => user.name.toUpperCase())
    .andThen((name) => {
      if (name.length < 2) {
        return Err(new ApplicationError('VAL_001'));
      }
      return Ok(name);
    });
}

// Combining multiple async results
function loadDashboard(
  userId: string
): ResultAsync<{ user: User; posts: Post[] }, ApplicationError> {
  return ResultAsync.combine([
    fetchUserData(userId),
    fetchPostsByUser(userId),
  ]).map(([user, posts]) => ({ user, posts }));
}

// Error recovery
function loadUserWithFallback(
  id: string
): ResultAsync<User, ApplicationError> {
  return fetchUserData(id)
    .orElse((error) => {
      // Recover from specific errors
      if (error.code === 'NF_001') {
        return OkAsync(createDefaultUser(id));
      }
      return Err(error); // re-throw other errors
    });
}

// Match pattern for exhaustive handling
async function displayResult(id: string) {
  const result = await fetchUserData(id);

  result.match(
    (user) => console.log(`User: ${user.name}`),
    (error) => console.error(`Error: ${error.message}`)
  );
}
```

---

## fp-ts Either Pattern

```typescript
// fp-ts provides a functional approach with the Either type:

import { Either, left, right, isLeft, isRight, chain, map, fold } from 'fp-ts/Either';
import { pipe } from 'fp-ts/function';

// Either<L, R> - Left is error, Right is success
type AppEither<R> = Either<ApplicationError, R>;

function validateName(name: string): AppEither<string> {
  if (name.length < 2) {
    return left(createValidationError('name', 'too short'));
  }
  return right(name);
}

function validateAge(age: number): AppEither<number> {
  if (age < 0 || age > 150) {
    return left(createValidationError('age', 'out of range'));
  }
  return right(age);
}

// Compose validations using pipe
function createUser(
  name: string,
  age: number
): AppEither<{ name: string; age: number }> {
  return pipe(
    validateName(name),
    chain((validName) =>
      pipe(
        validateAge(age),
        map((validAge) => ({ name: validName, age: validAge }))
      )
    )
  );
}

// Fold to handle both cases
const result = createUser('Alice', 25);
const message = pipe(
  result,
  fold(
    (error) => `Error: ${error.message}`,
    (user) => `Created user: ${user.name}, age ${user.age}`
  )
);

// Async Either
import { TaskEither, tryCatch, chain as chainTE } from 'fp-ts/TaskEither';

function fetchUserEither(id: string): TaskEither<ApplicationError, User> {
  return tryCatch(
    async () => {
      const res = await fetch(`/api/users/${id}`);
      if (!res.ok) throw new Error(`${res.status}`);
      return res.json() as Promise<User>;
    },
    () => new ApplicationError('NET_001')
  );
}

// Chain async operations
function getUserEmail(id: string): TaskEither<ApplicationError, string> {
  return pipe(
    fetchUserEither(id),
    chainTE((user) => {
      if (!user.email) {
        return left(new ApplicationError('VAL_001'));
      }
      return right(user.email);
    })
  );
}
```

---

## Error Handling in Async/Await

```typescript
// Patterns for handling errors in async/await chains:

// Pattern 1: Typed try-catch wrapper
async function safeAsync<T, E extends Error = Error>(
  fn: () => Promise<T>
): Promise<[T, null] | [null, E]> {
  try {
    const result = await fn();
    return [result, null];
  } catch (error) {
    return [null, error as E];
  }
}

// Usage
const [user, error] = await safeAsync(() => fetchUser('123'));
if (error) {
  console.error('Failed:', error.message);
} else {
  console.log('User:', user.name);
}

// Pattern 2: Promise.allSettled with typed results
interface TypedSettledResult<T> {
  status: 'fulfilled';
  value: T;
} | {
  status: 'rejected';
  reason: ApplicationError;
}

async function loadAllUserData(
  ids: string[]
): Promise<TypedSettledResult<User>[]> {
  return Promise.allSettled(
    ids.map((id) => fetchUser(id))
  ) as Promise<TypedSettledResult<User>[]>;
}

// Process results
const results = await loadAllUserData(['1', '2', '3']);
const users = results
  .filter((r): r is TypedSettledResult<User> & { status: 'fulfilled' } =>
    r.status === 'fulfilled'
  )
  .map((r) => r.value);

const failures = results
  .filter((r): r is TypedSettledResult<User> & { status: 'rejected' } =>
    r.status === 'rejected'
  )
  .map((r) => r.reason);

// Pattern 3: Sequential error handling with reduce
async function processSequentially<TInput, TOutput, TError>(
  items: TInput[],
  processor: (item: TInput) => Promise<Result<TOutput, TError>>,
  onError: (error: TError, item: TInput) => void
): Promise<TOutput[]> {
  const outputs: TOutput[] = [];

  for (const item of items) {
    const result = await processor(item);
    if (result.ok) {
      outputs.push(result.value);
    } else {
      onError(result.error, item);
    }
  }

  return outputs;
}

// Pattern 4: Error boundary for async generators
async function* processWithRetry<TInput, TOutput>(
  items: AsyncIterable<TInput>,
  processor: (item: TInput) => Promise<TOutput>,
  maxRetries: number = 3
): AsyncGenerator<{ item: TInput; result: TOutput; attempts: number } | { item: TInput; error: Error; attempts: number }> {
  for await (const item of items) {
    let lastError: Error | undefined;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        const result = await processor(item);
        yield { item, result, attempts: attempt };
        lastError = undefined;
        break;
      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));
        if (attempt === maxRetries) {
          yield { item, error: lastError, attempts: attempt };
        }
      }
    }
  }
}
```

---

## Typed Error Boundaries (React)

```typescript
// React Error Boundaries with typed error handling:

import React, { Component, ErrorInfo, ReactNode } from 'react';

// Typed error for React components
interface ComponentError {
  code: 'RENDER_ERROR' | 'ASYNC_ERROR' | 'DATA_ERROR';
  message: string;
  componentStack?: string;
  cause?: Error;
  context?: Record<string, unknown>;
}

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback: (error: ComponentError) => ReactNode;
  onError?: (error: ComponentError, errorInfo: ErrorInfo) => void;
  onRetry?: () => void;
}

interface ErrorBoundaryState {
  error: ComponentError | null;
}

class TypedErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      error: {
        code: 'RENDER_ERROR',
        message: error.message,
        cause: error,
      },
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    const componentError: ComponentError = {
      code: 'RENDER_ERROR',
      message: error.message,
      componentStack: errorInfo.componentStack ?? undefined,
      cause: error,
    };

    this.props.onError?.(componentError, errorInfo);

    // Report to error tracking service
    errorTracker.report(componentError);
  }

  render() {
    if (this.state.error) {
      return this.props.fallback(this.state.error);
    }
    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <TypedErrorBoundary
      fallback={(error) => (
        <div className="error-container">
          <h2>Something went wrong</h2>
          <p>{error.message}</p>
          {error.code === 'RENDER_ERROR' && (
            <button onClick={() => window.location.reload()}>
              Reload page
            </button>
          )}
        </div>
      )}
      onError={(error, info) => {
        console.error('Error caught:', error);
        reportToSentry(error, info);
      }}
    >
      <Dashboard />
    </TypedErrorBoundary>
  );
}

// Async error hook with typed errors
function useAsyncOperation<T, E = Error>() {
  const [state, setState] = React.useState<{
    data: T | null;
    error: E | null;
    loading: boolean;
  }>({ data: null, error: null, loading: false });

  const execute = React.useCallback(async (fn: () => Promise<T>) => {
    setState({ data: null, error: null, loading: true });
    try {
      const data = await fn();
      setState({ data, error: null, loading: false });
      return { ok: true as const, data };
    } catch (error) {
      const err = error as E;
      setState({ data: null, error: err, loading: false });
      return { ok: false as const, error: err };
    }
  }, []);

  return { ...state, execute };
}

// Usage of the hook
function UserProfile({ userId }: { userId: string }) {
  const { data: user, error, loading, execute } = useAsyncOperation<User, ApplicationError>();

  React.useEffect(() => {
    execute(() => fetchUser(userId));
  }, [userId, execute]);

  if (loading) return <Spinner />;
  if (error) return <ErrorDisplay error={error} />;
  if (!user) return null;

  return <div>{user.name}</div>;
}
```

---

## Server-Side Error Middleware

```typescript
// Type-safe error middleware for Express/Hono:

import { Request, Response, NextFunction } from 'express';

// Base error class
abstract class HttpError extends Error {
  abstract readonly statusCode: number;
  abstract readonly errorCode: string;
  readonly isOperational = true;

  constructor(message: string, readonly details?: Record<string, unknown>) {
    super(message);
    this.name = this.constructor.name;
  }
}

class BadRequestError extends HttpError {
  readonly statusCode = 400;
  readonly errorCode = 'BAD_REQUEST';

  constructor(message: string, details?: Record<string, unknown>) {
    super(message, details);
  }
}

class NotFoundError extends HttpError {
  readonly statusCode = 404;
  readonly errorCode = 'NOT_FOUND';

  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, { resource, id });
  }
}

class UnauthorizedError extends HttpError {
  readonly statusCode = 401;
  readonly errorCode = 'UNAUTHORIZED';

  constructor(reason: string) {
    super(reason, { reason });
  }
}

class ConflictError extends HttpError {
  readonly statusCode = 409;
  readonly errorCode = 'CONFLICT';

  constructor(message: string, details?: Record<string, unknown>) {
    super(message, details);
  }
}

class InternalError extends HttpError {
  readonly statusCode = 500;
  readonly errorCode = 'INTERNAL_ERROR';
  readonly isOperational = false;

  constructor(message: string, cause?: Error) {
    super(message);
    if (cause) this.stack = cause.stack;
  }
}

// Error response type
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    timestamp: string;
    requestId?: string;
  };
}

// Type-safe error handler middleware
function errorHandler(
  err: Error,
  req: Request,
  res: Response<ErrorResponse>,
  next: NextFunction
): void {
  if (err instanceof HttpError) {
    // Known operational error
    res.status(err.statusCode).json({
      error: {
        code: err.errorCode,
        message: err.message,
        details: err.details,
        timestamp: new Date().toISOString(),
        requestId: req.headers['x-request-id'] as string,
      },
    });
  } else {
    // Unexpected error - don't leak details
    console.error('Unexpected error:', err);
    res.status(500).json({
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred',
        timestamp: new Date().toISOString(),
        requestId: req.headers['x-request-id'] as string,
      },
    });
  }
}

// Type-safe async route handler
type AsyncHandler = (
  req: Request,
  res: Response,
  next: NextFunction
) => Promise<void>;

function asyncHandler(fn: AsyncHandler): AsyncHandler {
  return (req, res, next) => {
    fn(req, res, next).catch(next);
  };
}

// Usage in routes
app.get('/users/:id', asyncHandler(async (req, res) => {
  const user = await findUser(req.params.id);
  if (!user) {
    throw new NotFoundError('User', req.params.id);
  }
  res.json(user);
}));

app.post('/users', asyncHandler(async (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);
  if (!result.success) {
    throw new BadRequestError('Invalid input', {
      errors: result.error.flatten(),
    });
  }
  const user = await createUser(result.data);
  res.status(201).json(user);
}));
```

---

## Error Serialization for APIs

```typescript
// Safe error serialization for API responses:

interface SerializedError {
  name: string;
  message: string;
  code?: string;
  stack?: string;
  cause?: SerializedError;
  timestamp: string;
}

function serializeError(error: unknown): SerializedError {
  const base: SerializedError = {
    name: 'UnknownError',
    message: 'An unknown error occurred',
    timestamp: new Date().toISOString(),
  };

  if (error instanceof Error) {
    const serialized: SerializedError = {
      name: error.name,
      message: error.message,
      timestamp: new Date().toISOString(),
    };

    // Include stack in development only
    if (process.env.NODE_ENV === 'development') {
      serialized.stack = error.stack;
    }

    // Serialize cause chain
    if (error.cause instanceof Error) {
      serialized.cause = serializeError(error.cause);
    }

    // Include custom properties
    if ('code' in error) {
      serialized.code = (error as { code: string }).code;
    }

    return serialized;
  }

  if (typeof error === 'string') {
    return { ...base, message: error };
  }

  return base;
}

// Safe JSON serialization (handles circular references)
function safeStringify(obj: unknown, indent?: number): string {
  const seen = new WeakSet();

  return JSON.stringify(
    obj,
    (key, value) => {
      if (typeof value === 'object' && value !== null) {
        if (seen.has(value)) {
          return '[Circular]';
        }
        seen.add(value);
      }
      if (value instanceof Error) {
        return serializeError(value);
      }
      return value;
    },
    indent
  );
}

// Client-side error deserialization
function deserializeError(data: SerializedError): Error {
  const error = new Error(data.message);
  error.name = data.name;
  if (data.stack) error.stack = data.stack;
  if (data.cause) error.cause = deserializeError(data.cause);
  return error;
}
```

---

## Error Recovery Patterns

```typescript
// Patterns for recovering from errors gracefully:

// Pattern 1: Retry with exponential backoff
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    baseDelay?: number;
    maxDelay?: number;
    retryIf?: (error: Error) => boolean;
  } = {}
): Promise<T> {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 30000,
    retryIf = () => true,
  } = options;

  let lastError: Error | undefined;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (attempt === maxRetries || !retryIf(lastError)) {
        throw lastError;
      }

      const delay = Math.min(
        baseDelay * Math.pow(2, attempt) + Math.random() * 1000,
        maxDelay
      );

      console.log(`Retry ${attempt + 1}/${maxRetries} after ${delay}ms`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}

// Pattern 2: Circuit breaker
class CircuitBreaker<T> {
  private state: 'closed' | 'open' | 'half-open' = 'closed';
  private failureCount = 0;
  private lastFailureTime?: Date;

  constructor(
    private fn: () => Promise<T>,
    private options: {
      failureThreshold?: number;
      resetTimeout?: number;
    } = {}
  ) {}

  async execute(): Promise<T> {
    if (this.state === 'open') {
      const timeSinceFailure = Date.now() - (this.lastFailureTime?.getTime() ?? 0);
      if (timeSinceFailure < (this.options.resetTimeout ?? 60000)) {
        throw new Error('Circuit breaker is open');
      }
      this.state = 'half-open';
    }

    try {
      const result = await this.fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    this.state = 'closed';
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = new Date();
    if (this.failureCount >= (this.options.failureThreshold ?? 5)) {
      this.state = 'open';
    }
  }
}

// Pattern 3: Fallback chain
async function withFallback<T>(
  ...strategies: Array<() => Promise<T>>
): Promise<T> {
  let lastError: Error | undefined;

  for (const strategy of strategies) {
    try {
      return await strategy();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
    }
  }

  throw lastError;
}

// Usage: try cache, then DB, then API
const data = await withFallback(
  () => getCachedData('users'),        // Try cache first
  () => db.query('SELECT * FROM users'), // Then database
  () => fetchFromAPI('/users'),         // Then external API
);
```

---

## Typed Try-Catch with Discriminated Unions

```typescript
// Making try-catch type-safe using discriminated unions:

type TryResult<T, E = Error> =
  | { success: true; value: T; thrown: false }
  | { success: false; error: E; thrown: true };

function trySync<T>(fn: () => T): TryResult<T> {
  try {
    return { success: true, value: fn(), thrown: false };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error : new Error(String(error)),
      thrown: true,
    };
  }
}

async function tryAsync<T>(fn: () => Promise<T>): Promise<TryResult<T>> {
  try {
    return { success: true, value: await fn(), thrown: false };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error : new Error(String(error)),
      thrown: true,
    };
  }
}

// Usage with exhaustive handling
const result = trySync(() => JSON.parse('{"valid": true}'));

if (result.thrown) {
  // result.error is Error
  console.error('Parse failed:', result.error.message);
} else {
  // result.value is the parsed object
  console.log(result.value.valid);
}

// With typed errors
type ParseError = { type: 'parse'; position: number; message: string };
type ValidationError = { type: 'validation'; field: string; reason: string };

function parseAndValidate(
  input: string
): TryResult<{ name: string; age: number }, ParseError | ValidationError> {
  const parseResult = trySync(() => JSON.parse(input));

  if (parseResult.thrown) {
    return {
      success: false,
      error: { type: 'parse', position: 0, message: parseResult.error.message },
      thrown: true,
    };
  }

  const data = parseResult.value as any;

  if (!data.name || typeof data.name !== 'string') {
    return {
      success: false,
      error: { type: 'validation', field: 'name', reason: 'required string' },
      thrown: true,
    };
  }

  if (typeof data.age !== 'number') {
    return {
      success: false,
      error: { type: 'validation', field: 'age', reason: 'required number' },
      thrown: true,
    };
  }

  return { success: true, value: { name: data.name, age: data.age }, thrown: false };
}

// Handle all error types
const parsed = parseAndValidate('{"name": "Alice", "age": 25}');
if (parsed.thrown) {
  switch (parsed.error.type) {
    case 'parse':
      console.error(`Parse error at position ${parsed.error.position}`);
      break;
    case 'validation':
      console.error(`Validation error on ${parsed.error.field}: ${parsed.error.reason}`);
      break;
  }
}
```

---

## Interview Questions

### Q1: What is the Result type and why use it over throw?

**Answer:** The Result type (Ok/Err pattern) encodes success and failure as data rather than control flow. Unlike throw/catch, Result is explicit - callers must handle both cases at compile time. This eliminates unhandled exceptions, makes error handling part of the type system, and enables composition through map/flatMap. It's borrowed from functional programming (Railway-Oriented Programming).

### Q2: How do discriminated unions improve error handling?

**Answer:** Discriminated unions use a common literal property (like `code`) to narrow error types in switch statements. Each error variant has different properties. TypeScript's control flow analysis narrows the type within each switch case, giving you access to error-specific properties without type assertions. The `never` exhaustiveness check ensures all error types are handled.

### Q3: What is the Error Catalog pattern?

**Answer:** A centralized registry of all possible application errors with pre-defined codes, messages, HTTP status codes, severity levels, and retry policies. Instead of scattering `new Error(...)` calls, you reference catalog entries. This ensures consistent error responses, enables centralized logging/monitoring, and makes error codes a first-class part of your API contract.

### Q4: How do you handle errors in async/await chains without losing type information?

**Answer:** Use typed try-catch wrappers that return Result types, Promise.allSettled for parallel operations, or neverthrow/fp-ts for functional composition. The key is avoiding bare `catch (e)` blocks that lose type info. Always type-narrow caught errors (`error instanceof Error`) or use libraries that preserve error types through the chain.

### Q5: Explain the never-throwing pattern and its benefits.

**Answer:** Instead of throwing errors, functions return `Result<T, E>` types. This forces callers to explicitly handle both success and error paths. Benefits: no unhandled exceptions, compiler-enforced error handling, composable error chains, and clearer function signatures that document all possible failure modes.

### Q6: How do you implement typed error boundaries in React?

**Answer:** Create a class component implementing `getDerivedStateFromError` and `componentDidCatch`. The error boundary catches render errors and stores them in typed state. The fallback render function receives a typed error object. Combine with typed hooks (useAsyncOperation) for async error handling. Use discriminated unions for different error types.

### Q7: What is the Circuit Breaker pattern and when should you use it?

**Answer:** A circuit breaker tracks failure counts and temporarily stops calling a failing service. States: closed (normal), open (failing, return cached/fallback), half-open (testing recovery). Use it when calling external services that might fail repeatedly - it prevents cascading failures, reduces load on struggling services, and allows recovery time.

### Q8: How do you serialize errors safely for API responses?

**Answer:** Create a serializer that extracts name, message, code, and cause chain from Error objects. Strip stack traces in production. Handle circular references with a WeakSet. Use a standard error response format (code, message, details, timestamp, requestId). On the client, deserialize back to Error instances for consistent handling.

### Q9: Compare fp-ts Either with neverthrow Result.

**Answer:** fp-ts Either is a full functional programming library with rich type-level composition (pipe, chain, fold). neverthrow is simpler, with a more imperative API (match, map, andThen). fp-ts has a steeper learning curve but more power. neverthrow is more approachable for teams new to FP. Both solve the same problem: encoding success/failure as data.

### Q10: How do you handle retry logic with exponential backoff?

**Answer:** Implement a retry loop with configurable max retries and base delay. On each failure, calculate delay as `baseDelay * 2^attempt + jitter`. Only retry if the error is retryable (network errors, 5xx) not for client errors (4xx). Use a circuit breaker to stop retrying after sustained failures. Track retry attempts for observability.

### Q11: What is the difference between operational and programmer errors?

**Answer:** Operational errors are expected failures (network timeouts, validation failures, not found) that should be handled gracefully. Programmer errors are bugs (null references, type mismatches) that indicate code defects. Operational errors use typed Result values or ApplicationError classes. Programmer errors should crash and be fixed. The `isOperational` flag on error classes helps distinguish them.
