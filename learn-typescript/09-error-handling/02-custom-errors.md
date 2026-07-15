# Custom Errors in TypeScript

## Table of Contents

- [Overview](#overview)
- [Creating Custom Error Classes](#creating-custom-error-classes)
- [Extending Error](#extending-error)
- [Error Hierarchy](#error-hierarchy)
- [Error Codes Enum](#error-codes-enum)
- [Typed Error Responses](#typed-error-responses)
- [Error Serialization](#error-serialization)
- [Custom Errors in APIs](#custom-errors-in-apis)
- [Error Factories](#error-factories)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Custom errors allow you to create domain-specific error types that carry structured information, enabling better error handling, debugging, and API responses. Instead of generic `Error('something went wrong')`, you create typed errors like `UserNotFoundError(userId)` or `ValidationError('email', 'invalid format')`.

---

## Creating Custom Error Classes

### Basic Custom Error

```typescript
class AppError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AppError';
    // Fix prototype chain for instanceof to work
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

throw new AppError('Application error');
```

### Custom Error with Additional Data

```typescript
class ValidationError extends Error {
  constructor(
    public field: string,
    public value: unknown,
    public constraint: string
  ) {
    super(`Validation failed for "${field}": ${constraint}`);
    this.name = 'ValidationError';
    Object.setPrototypeOf(this, ValidationError.prototype);
  }
}

class UserNotFoundError extends Error {
  constructor(public userId: string) {
    super(`User with ID "${userId}" not found`);
    this.name = 'UserNotFoundError';
    Object.setPrototypeOf(this, UserNotFoundError.prototype);
  }
}

// Usage
function findUser(id: string): User {
  const user = db.users.findById(id);
  if (!user) {
    throw new UserNotFoundError(id);
  }
  return user;
}

try {
  findUser('nonexistent');
} catch (error) {
  if (error instanceof UserNotFoundError) {
    console.error(`User ${error.userId} not found`);
    return { status: 404, error: error.message };
  }
  throw error;
}
```

---

## Extending Error

### Why Object.setPrototypeOf Is Needed

```typescript
// WITHOUT setPrototypeOf — breaks in TypeScript/Babel compiled code:
class MyError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'MyError';
  }
}

const err = new MyError('test');
console.log(err instanceof MyError); // false! (in some environments)
console.log(err instanceof Error);   // true

// WITH setPrototypeOf — instanceof works correctly:
class MyError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'MyError';
    Object.setPrototypeOf(this, MyError.prototype);
  }
}

const err = new MyError('test');
console.log(err instanceof MyError); // true
```

### Modern Alternative (ES2022+)

```typescript
// In modern environments (ES2022+), you can use Error.captureStackTrace
class AppError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AppError';

    // V8-specific: cleaner stack trace
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AppError);
    }
  }
}
```

---

## Error Hierarchy

### Domain-Specific Error Tree

```typescript
// Base application error
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = 'AppError';
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

// Validation errors (400)
class ValidationError extends AppError {
  constructor(
    public field: string,
    message: string
  ) {
    super(message, 'VALIDATION_ERROR', 400);
    this.name = 'ValidationError';
    Object.setPrototypeOf(this, ValidationError.prototype);
  }
}

class RequiredFieldError extends ValidationError {
  constructor(field: string) {
    super(field, `"${field}" is required`);
    this.name = 'RequiredFieldError';
    Object.setPrototypeOf(this, RequiredFieldError.prototype);
  }
}

class InvalidFormatError extends ValidationError {
  constructor(field: string, expectedFormat: string) {
    super(field, `"${field}" must match format: ${expectedFormat}`);
    this.name = 'InvalidFormatError';
    Object.setPrototypeOf(this, InvalidFormatError.prototype);
  }
}

// Authentication errors (401)
class AuthenticationError extends AppError {
  constructor(message: string = 'Authentication required') {
    super(message, 'AUTH_ERROR', 401);
    this.name = 'AuthenticationError';
    Object.setPrototypeOf(this, AuthenticationError.prototype);
  }
}

class TokenExpiredError extends AuthenticationError {
  constructor(public tokenExpiry: Date) {
    super('Token has expired');
    this.name = 'TokenExpiredError';
    Object.setPrototypeOf(this, TokenExpiredError.prototype);
  }
}

// Authorization errors (403)
class ForbiddenError extends AppError {
  constructor(resource: string, action: string) {
    super(
      `Not authorized to ${action} ${resource}`,
      'FORBIDDEN',
      403
    );
    this.name = 'ForbiddenError';
    Object.setPrototypeOf(this, ForbiddenError.prototype);
  }
}

// Not found errors (404)
class NotFoundError extends AppError {
  constructor(resource: string, identifier: string | number) {
    super(`${resource} with id "${identifier}" not found`, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
    Object.setPrototypeOf(this, NotFoundError.prototype);
  }
}

// Conflict errors (409)
class ConflictError extends AppError {
  constructor(message: string) {
    super(message, 'CONFLICT', 409);
    this.name = 'ConflictError';
    Object.setPrototypeOf(this, ConflictError.prototype);
  }
}
```

### Using the Hierarchy

```typescript
function handleRequest(handler: () => void) {
  try {
    handler();
  } catch (error) {
    if (error instanceof ValidationError) {
      return { status: 400, field: error.field, message: error.message };
    }
    if (error instanceof AuthenticationError) {
      return { status: 401, message: error.message };
    }
    if (error instanceof ForbiddenError) {
      return { status: 403, message: error.message };
    }
    if (error instanceof NotFoundError) {
      return { status: 404, message: error.message };
    }
    if (error instanceof AppError) {
      return { status: error.statusCode, message: error.message };
    }
    console.error('Unexpected error:', error);
    return { status: 500, message: 'Internal Server Error' };
  }
}
```

---

## Error Codes Enum

### Typed Error Codes

```typescript
enum ErrorCode {
  // Validation (1xxx)
  VALIDATION_FAILED = 'E1000',
  REQUIRED_FIELD = 'E1001',
  INVALID_FORMAT = 'E1002',
  INVALID_LENGTH = 'E1003',

  // Auth (2xxx)
  AUTH_REQUIRED = 'E2000',
  TOKEN_EXPIRED = 'E2001',
  INVALID_CREDENTIALS = 'E2002',
  ACCOUNT_LOCKED = 'E2003',

  // Not Found (3xxx)
  RESOURCE_NOT_FOUND = 'E3000',
  USER_NOT_FOUND = 'E3001',
  POST_NOT_FOUND = 'E3002',

  // Conflict (4xxx)
  DUPLICATE_RESOURCE = 'E4000',
  EMAIL_EXISTS = 'E4001',
  USERNAME_EXISTS = 'E4002',

  // Server (5xxx)
  INTERNAL_ERROR = 'E5000',
  DATABASE_ERROR = 'E5001',
  EXTERNAL_SERVICE_ERROR = 'E5002',
}

class AppError extends Error {
  constructor(
    public code: ErrorCode,
    message: string,
    public statusCode: number = 500,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'AppError';
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

// Usage
throw new AppError(
  ErrorCode.USER_NOT_FOUND,
  'User not found',
  404,
  { userId: '123' }
);
```

### Error Code to HTTP Status Mapping

```typescript
const ERROR_STATUS_MAP: Record<ErrorCode, number> = {
  [ErrorCode.VALIDATION_FAILED]: 400,
  [ErrorCode.REQUIRED_FIELD]: 400,
  [ErrorCode.INVALID_FORMAT]: 400,
  [ErrorCode.INVALID_LENGTH]: 400,
  [ErrorCode.AUTH_REQUIRED]: 401,
  [ErrorCode.TOKEN_EXPIRED]: 401,
  [ErrorCode.INVALID_CREDENTIALS]: 401,
  [ErrorCode.ACCOUNT_LOCKED]: 403,
  [ErrorCode.RESOURCE_NOT_FOUND]: 404,
  [ErrorCode.USER_NOT_FOUND]: 404,
  [ErrorCode.POST_NOT_FOUND]: 404,
  [ErrorCode.DUPLICATE_RESOURCE]: 409,
  [ErrorCode.EMAIL_EXISTS]: 409,
  [ErrorCode.USERNAME_EXISTS]: 409,
  [ErrorCode.INTERNAL_ERROR]: 500,
  [ErrorCode.DATABASE_ERROR]: 500,
  [ErrorCode.EXTERNAL_SERVICE_ERROR]: 502,
};
```

---

## Typed Error Responses

```typescript
// Discriminated union for error responses
type ApiError =
  | { type: 'validation'; field: string; message: string }
  | { type: 'not_found'; resource: string; id: string }
  | { type: 'authentication'; message: string }
  | { type: 'forbidden'; resource: string }
  | { type: 'conflict'; field: string; existingValue: unknown }
  | { type: 'internal'; message: string };

function handleError(error: unknown): ApiError {
  if (error instanceof ValidationError) {
    return {
      type: 'validation',
      field: error.field,
      message: error.message,
    };
  }
  if (error instanceof NotFoundError) {
    return {
      type: 'not_found',
      resource: 'User',
      id: '123',
    };
  }
  return {
    type: 'internal',
    message: error instanceof Error ? error.message : 'Unknown error',
  };
}
```

---

## Error Serialization

### Safe Error Serialization

```typescript
// JSON.stringify drops Error message, stack, and custom properties
// This is a common gotcha:

const error = new Error('test');
console.log(JSON.stringify(error)); // '{}' — all info lost!

// Solution: implement toJSON
class SerializableError extends Error {
  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: (this as any).code,
      stack: this.stack,
    };
  }
}

// Or serialize explicitly:
function serializeError(error: unknown): Record<string, unknown> {
  if (error instanceof Error) {
    return {
      name: error.name,
      message: error.message,
      stack: error.stack,
      ...(error as any).code ? { code: (error as any).code } : {},
    };
  }
  return { message: String(error) };
}
```

### Error Logging Format

```typescript
function formatErrorForLogging(error: unknown): string {
  if (error instanceof Error) {
    return [
      `[${error.name}] ${error.message}`,
      error.stack ? `Stack: ${error.stack}` : '',
      `Timestamp: ${new Date().toISOString()}`,
    ].filter(Boolean).join('\n');
  }
  return `Unknown error: ${String(error)}`;
}
```

---

## Custom Errors in APIs

### Express Error Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

class AppError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = 'AppError';
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
      },
    });
  }

  // Unknown error — don't leak details
  console.error('Unexpected error:', err);
  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  });
}

// Usage in routes
app.post('/users', async (req, res, next) => {
  try {
    const user = await createUser(req.body);
    res.status(201).json(user);
  } catch (error) {
    next(error); // Pass to error middleware
  }
});
```

### Fastify Error Handling

```typescript
import { FastifyError } from 'fastify';

class AppError extends Error implements FastifyError {
  code: string;
  statusCode: number;
  constructor(statusCode: number, code: string, message: string) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

// Register error handler
fastify.setErrorHandler((error, request, reply) => {
  if (error instanceof AppError) {
    reply.status(error.statusCode).send({
      error: error.code,
      message: error.message,
    });
  } else {
    reply.status(500).send({
      error: 'INTERNAL_ERROR',
      message: 'Something went wrong',
    });
  }
});
```

---

## Error Factories

### Factory Functions for Common Errors

```typescript
function notFound(resource: string, id: string | number): NotFoundError {
  return new NotFoundError(resource, id);
}

function validation(field: string, message: string): ValidationError {
  return new ValidationError(field, message);
}

function required(field: string): RequiredFieldError {
  return new RequiredFieldError(field);
}

function auth(message?: string): AuthenticationError {
  return new AuthenticationError(message);
}

function forbidden(resource: string, action: string): ForbiddenError {
  return new ForbiddenError(resource, action);
}

function conflict(message: string): ConflictError {
  return new ConflictError(message);
}

// Usage — concise and readable
function createUser(data: CreateUserDto) {
  if (!data.name) throw required('name');
  if (!data.email) throw required('email');
  if (!data.email.includes('@')) throw validation('email', 'must be valid');

  const existing = findByEmail(data.email);
  if (existing) throw conflict('Email already registered');

  const user = db.users.create(data);
  if (!user) throw new AppError('INTERNAL_ERROR', 'Failed to create user');

  return user;
}
```

### Generic Error Factory

```typescript
function createError<T extends AppError>(
  ErrorClass: new (...args: any[]) => T,
  ...args: ConstructorParameters<T>
): T {
  return new ErrorClass(...args);
}

// Usage
const err = createError(NotFoundError, 'User', '123');
```

---

## Best Practices

1. **Always call `Object.setPrototypeOf(this, ErrorClass.prototype)`** in custom error constructors for `instanceof` to work.

2. **Use error codes** — they're stable identifiers for error handling, unlike message strings.

3. **Mark operational vs programming errors** — operational errors are expected (404, 400); programming errors are bugs (null reference, type errors).

4. **Don't throw generic `Error`** in application code — use domain-specific custom errors.

5. **Serialize errors safely** for logging and API responses — `JSON.stringify` drops Error properties.

6. **Include error codes** in API responses — they're machine-readable and client-friendly.

7. **Use error cause chains** (`{ cause: error }`) to preserve context.

8. **Keep error hierarchy shallow** — 2-3 levels is usually enough.

---

## Interview Questions

### Q1: Why do you need `Object.setPrototypeOf` in custom error classes?

**Answer**: TypeScript compiles class syntax to ES5/ES6, which can break the prototype chain for classes extending built-ins like `Error`. Without `Object.setPrototypeOf`, `instanceof CustomError` returns `false` in some environments. `Object.setPrototypeOf(this, CustomError.prototype)` fixes the chain.

### Q2: What is the difference between operational and programming errors?

**Answer**: Operational errors are expected failures (user not found, validation failed) — the system should handle them gracefully. Programming errors are bugs (null reference, type error, index out of bounds) — they indicate code defects that should be fixed. Operational errors should be caught; programming errors should be allowed to crash.

### Q3: How do you serialize Error objects for JSON responses?

**Answer**: `JSON.stringify(error)` returns `{}` because Error properties (message, stack) are non-enumerable. Solutions: implement `toJSON()` on the error class, manually extract properties with `Object.getOwnPropertyNames()`, or create a plain object with the error details explicitly.

### Q4: What is an error code enum and why use it?

**Answer**: An error code enum defines machine-readable error identifiers (e.g., `USER_NOT_FOUND = 'E3001'`). Benefits: stable identifiers (not affected by message localization), easy to handle in clients (`if (error.code === 'E3001')`), and enables centralized error-to-status mapping.

### Q5: How do you handle errors in Express with TypeScript?

**Answer**: Use typed error middleware: `(err: Error, req: Request, res: Response, next: NextFunction)`. Check `instanceof` for custom errors, return appropriate status codes and JSON responses. For unexpected errors, return 500 without leaking details. Use `next(error)` in route handlers to delegate to the error middleware.
