# Section 04: Generic & Utility Types

## Overview

Generic utility types form the backbone of type-safe, reusable code patterns in the voice agent platform. By defining a standard set of utilities — `AsyncReturnType`, `DeepPartial`, `PaginatedResponse`, `Result<T, E>` — we create consistent patterns for error handling, pagination, and async operations across the entire codebase.

## Core Utility Types

```typescript
// packages/types/src/utils/generics.ts

// ── Async Return Type ───────────────────────────────────────
export type AsyncReturnType<T extends (...args: unknown[]) => unknown> =
  T extends (...args: unknown[]) => Promise<infer R> ? R : never;

// Usage:
// type Result = AsyncReturnType<typeof getAgent>;
// Result is inferred as Agent | null

// ── Deep Partial ────────────────────────────────────────────
export type DeepPartial<T> = T extends object
  ? {
      [P in keyof T]?: T[P] extends (infer U)[]
        ? DeepPartial<U>[]
        : T[P] extends object
          ? DeepPartial<T[P]>
          : T[P];
    }
  : T;

// Usage:
// type UpdatePayload = DeepPartial<Agent>;
// Allows partial updates with nested optionality

// ── Deep Required ───────────────────────────────────────────
export type DeepRequired<T> = T extends object
  ? {
      [P in keyof T]-?: T[P] extends (infer U)[]
        ? DeepRequired<U>[]
        : T[P] extends object
          ? DeepRequired<T[P]>
          : NonNullable<T[P]>;
    }
  : NonNullable<T>;
```

## Result Type (Railway-Oriented Programming)

The `Result<T, E>` type provides a type-safe way to handle errors without exceptions:

```typescript
// packages/types/src/utils/result.ts
export type Result<T, E = Error> = Ok<T, E> | Err<T, E>;

export class Ok<T, E> {
  readonly _tag = "ok" as const;
  constructor(public readonly value: T) {}

  isOk(): this is Ok<T, E> {
    return true;
  }

  isErr(): this is Err<T, E> {
    return false;
  }

  map<U>(fn: (value: T) => U): Result<U, E> {
    return new Ok(fn(this.value));
  }

  mapErr<F>(_fn: (error: E) => F): Result<T, F> {
    return this as unknown as Result<T, F>;
  }

  unwrap(): T {
    return this.value;
  }

  unwrapOr(defaultValue: T): T {
    return this.value;
  }
}

export class Err<T, E> {
  readonly _tag = "err" as const;
  constructor(public readonly error: E) {}

  isOk(): this is Ok<T, E> {
    return false;
  }

  isErr(): this is Err<T, E> {
    return true;
  }

  map<U>(_fn: (value: T) => U): Result<U, E> {
    return this as unknown as Result<U, E>;
  }

  mapErr<F>(fn: (error: E) => F): Result<T, F> {
    return new Err(fn(this.error));
  }

  unwrap(): T {
    throw this.error;
  }

  unwrapOr(defaultValue: T): T {
    return defaultValue;
  }
}

// ── Helper Functions ───────────────────────────────────────
export function ok<T, E = never>(value: T): Result<T, E> {
  return new Ok(value);
}

export function err<T, E>(error: E): Result<T, E> {
  return new Err(error);
}

export function isOk<T, E>(result: Result<T, E>): result is Ok<T, E> {
  return result._tag === "ok";
}

export function isErr<T, E>(result: Result<T, E>): result is Err<T, E> {
  return result._tag === "err";
}
```

### Usage Example

```typescript
import { ok, err, type Result } from "@voice-agent/types/utils";

type AgentError =
  | { type: "not_found"; id: string }
  | { type: "validation"; message: string }
  | { type: "database"; cause: Error };

async function getAgent(id: string): Promise<Result<Agent, AgentError>> {
  try {
    const agent = await prisma.agent.findUnique({ where: { id } });
    if (!agent) {
      return err({ type: "not_found", id });
    }
    return ok(agent);
  } catch (cause) {
    return err({ type: "database", cause: cause as Error });
  }
}

// Consumer
const result = await getAgent(agentId);
if (isOk(result)) {
  processAgent(result.value);
} else {
  handleError(result.error);
}
```

## Pagination Types

```typescript
// packages/types/src/api/pagination.ts

// ── Offset-based pagination ────────────────────────────────
export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
  };
}

export function createPaginatedResponse<T>(
  data: T[],
  total: number,
  page: number,
  pageSize: number,
): PaginatedResponse<T> {
  return {
    data,
    meta: {
      total,
      page,
      pageSize,
      totalPages: Math.ceil(total / pageSize),
      hasNext: page * pageSize < total,
      hasPrevious: page > 1,
    },
  };
}

// ── Cursor-based pagination ────────────────────────────────
export interface CursorPaginatedResponse<T> {
  data: T[];
  meta: {
    nextCursor: string | null;
    hasMore: boolean;
  };
}

// ── Pagination Parameters ──────────────────────────────────
export interface PaginationParams {
  page?: number;
  pageSize?: number;
  cursor?: string;
}

export const DEFAULT_PAGE_SIZE = 20;
export const MAX_PAGE_SIZE = 100;
```

## API Response Wrapper

```typescript
// packages/types/src/api/response.ts
export interface ApiSuccessResponse<T> {
  success: true;
  data: T;
  meta?: {
    requestId: string;
    timestamp: string;
  };
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, string[]>;
  };
  meta?: {
    requestId: string;
    timestamp: string;
  };
}

export type ApiResponse<T> = ApiSuccessResponse<T> | ApiErrorResponse;

export function success<T>(data: T): ApiSuccessResponse<T> {
  return {
    success: true,
    data,
    meta: {
      requestId: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
    },
  };
}

export function failure(
  code: string,
  message: string,
  details?: Record<string, string[]>,
): ApiErrorResponse {
  return {
    success: false,
    error: { code, message, details },
    meta: {
      requestId: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
    },
  };
}
```

## Type Guards

```typescript
// packages/types/src/utils/guards.ts
export function isError(error: unknown): error is Error {
  return error instanceof Error;
}

export function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function isString(value: unknown): value is string {
  return typeof value === "string";
}

export function isNonEmptyString(value: unknown): value is string {
  return isString(value) && value.length > 0;
}

export function isPositiveInteger(value: unknown): value is number {
  return typeof value === "number" && Number.isInteger(value) && value > 0;
}
```

## Promise Utilities

```typescript
// packages/types/src/utils/promise.ts
export type PromiseResult<T> = [T, null] | [null, Error];

export async function to<T>(
  promise: Promise<T>,
): Promise<PromiseResult<T>> {
  try {
    const data = await promise;
    return [data, null];
  } catch (error) {
    return [null, error instanceof Error ? error : new Error(String(error))];
  }
}

// Usage:
// const [agent, error] = await to(getAgent(id));
// if (error) handle(error);
// else process(agent);

export async function waitAll<T extends readonly unknown[]>(
  ...promises: { [K in keyof T]: Promise<T[K]> }
): Promise<{ [K in keyof T]: T[K] }> {
  return Promise.all(promises);
}
```

## Discriminated Union Patterns

```typescript
// packages/types/src/utils/unions.ts

// ── State Machine with Data ────────────────────────────────
export type CallState =
  | { status: "initiating"; startedAt: Date }
  | { status: "ringing"; ringStartedAt: Date }
  | { status: "in_progress"; connectedAt: Date; agentId: string }
  | { status: "transferring"; toAgentId: string; initiatedAt: Date }
  | { status: "completed"; endedAt: Date; duration: number }
  | { status: "failed"; error: string; endedAt: Date };

// TypeScript narrows based on the `status` discriminant
function handleCallState(state: CallState): void {
  switch (state.status) {
    case "in_progress": {
      console.log(state.connectedAt); // TypeScript knows this exists
      break;
    }
    case "completed": {
      console.log(state.duration); // Type-safe access
      break;
    }
  }
}

// ── Async Operation State ──────────────────────────────────
export type AsyncState<T, E = Error> =
  | { type: "idle" }
  | { type: "loading" }
  | { type: "success"; data: T }
  | { type: "error"; error: E };
```

## Function Type Utilities

```typescript
// packages/types/src/utils/functions.ts
export type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

export type FirstArgument<T> = T extends (arg: infer A, ...rest: unknown[]) => unknown
  ? A
  : never;

export type SecondArgument<T> = T extends (
  arg: unknown,
  arg2: infer A,
  ...rest: unknown[]
) => unknown
  ? A
  : never;

export type ReturnTypeOf<T> = T extends (...args: unknown[]) => infer R ? R : never;

// Utility to make a function type's return type nullable
export type NullableReturn<T extends (...args: unknown[]) => unknown> = (
  ...args: Parameters<T>
) => ReturnType<T> | null;
```

## Design Decisions

### Result Type vs. Throwing Exceptions

| Approach | Pros | Cons |
|----------|------|------|
| **Result<T, E>** | Type-safe, explicit, composable | Verbose, TypeScript overhead |
| **Throwing exceptions** | Familiar, implicit | Not type-safe, easy to forget try/catch |

**Decision**: Use `Result<T, E>` for expected errors (validation, not found, rate limits) and throw for unexpected errors (programming bugs, infrastructure failures). This gives us the best of both worlds — the type safety of Result for domain errors and the simplicity of exceptions for unexpected situations.

### DeepPartial vs. Partial

The built-in `Partial<T>` only makes top-level properties optional. `DeepPartial<T>` recursively makes all nested properties optional, which is essential for partial updates and patch operations on deeply nested configuration objects.

## Integration Points

- **API layer**: `ApiResponse<T>` wraps all API responses
- **Repository layer**: `Result<T, E>` for database operations
- **React state**: `AsyncState<T, E>` for data fetching components
- **Generic components**: `DeepPartial<T>` for form state management

## Production Considerations

1. **Type recursion depth**: `DeepPartial` uses recursive conditional types which have a depth limit (typically ~50). For deeply nested objects, consider limiting the recursion or using a simpler utility
2. **Compile-time cost**: Complex generic types increase type-checking time. On large projects, benchmark with `tsc --generateTrace` to identify slow generic types
3. **Documentation**: Generic types are harder to understand than concrete types. Add clear JSDoc comments with usage examples
4. **Serialization**: The `Result<T, E>` type does not serialize naturally to JSON for API responses. Use `ApiResponse<T>` for API boundaries instead
