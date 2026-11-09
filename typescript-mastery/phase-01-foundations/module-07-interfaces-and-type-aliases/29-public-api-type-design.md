# Public API Type Design

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Design exported types as a small, stable contract: readonly inputs, explicit result unions, and no leaked implementation details.

## Syntax
```ts
export interface ClientOptions {
  readonly baseUrl: string;
}

export type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: string };

export interface Client {
  get<T>(path: string): Promise<ApiResult<T>>;
}
```

## Examples
### Basic
```ts
export interface ClientOptions {
  readonly baseUrl: string;
  readonly timeoutMs?: number;
  readonly headers?: Readonly<Record<string, string>>;
}

export type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: ApiError };

export interface ApiError {
  readonly code: string;
  readonly message: string;
  readonly retryable: boolean;
}
```

### Practical
```ts
export interface ClientOptions {
  readonly baseUrl: string;
  readonly timeoutMs?: number;
  readonly headers?: Readonly<Record<string, string>>;
}

export interface ApiError {
  readonly code: string;
  readonly message: string;
  readonly retryable: boolean;
}

export type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: ApiError };

export interface Client {
  get<T>(path: string): Promise<ApiResult<T>>;
  post<T>(path: string, body: unknown): Promise<ApiResult<T>>;
}

// Internal state is not exported.
interface InternalState {
  token: string;
  requestCount: number;
}

export function createClient(options: ClientOptions): Client {
  const state: InternalState = { token: "", requestCount: 0 };

  async function request<T>(path: string): Promise<ApiResult<T>> {
    state.requestCount += 1;
    try {
      const response = await fetch(`${options.baseUrl}${path}`, {
        headers: options.headers,
      });
      return { ok: true, data: (await response.json()) as T };
    } catch (error) {
      return {
        ok: false,
        error: {
          code: "NETWORK",
          message: error instanceof Error ? error.message : "unknown",
          retryable: true,
        },
      };
    }
  }

  return {
    get: <T>(path: string) => request<T>(path),
    post: <T>(path: string, body: unknown) => request<T>(path),
  };
}
```

### Advanced / edge cases
```ts
// Export types only, so consumers never import runtime values by accident.
interface Client {
  get(path: string): Promise<string>;
}

interface ClientOptions {
  readonly baseUrl: string;
}

type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: ApiError };

interface ApiError {
  readonly code: string;
}

export type { Client, ClientOptions, ApiResult, ApiError };

// Use a brand for identifiers that must not be mixed.
export type AccountId = string & { readonly __brand: "AccountId" };

// Additive options keep the public contract backward compatible.
export interface RequestOptions {
  readonly signal?: AbortSignal;
  readonly retries?: number;
}

// Never expose a mutable internal collection.
export interface Snapshot {
  readonly items: readonly string[];
}
```

## Key points
- Export the smallest surface that consumers actually need.
- Mark configuration and identifiers `readonly`.
- Return discriminated unions instead of throwing for expected failures.
- Keep internal state and helper types unexported.
- Add optional fields for backward-compatible evolution.

## Gotchas
- Exporting an internal implementation type couples consumers to refactors.
- Widening an input type is safe; narrowing it is usually breaking.
- `// ❌ Error:` exposing `any` in a public signature leaks unsafety to every caller.

## Best practice
- Document every exported type with a short JSDoc comment.
- Review public types like API endpoints: name, shape, and compatibility matter.
