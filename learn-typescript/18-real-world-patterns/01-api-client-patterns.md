# API Client Patterns in TypeScript

## Table of Contents

- [Typed API Clients](#typed-api-clients)
- [Fetch Wrapper with Generics](#fetch-wrapper-with-generics)
- [API Response Types](#api-response-types)
- [Request/Response Interceptors](#requestresponse-interceptors)
- [Retry Logic with Types](#retry-logic-with-types)
- [API Client Builder Pattern](#api-client-builder-pattern)
- [Error Handling in API Clients](#error-handling-in-api-clients)
- [Interview Questions](#interview-questions)

---

## Typed API Clients

```typescript
// Base types for API clients
interface ApiClientConfig {
  baseUrl: string;
  headers?: Record<string, string>;
  timeout?: number;
  retries?: number;
}

interface RequestOptions {
  method?: string;
  headers?: Record<string, string>;
  body?: unknown;
  query?: Record<string, string | number | boolean>;
  timeout?: number;
  signal?: AbortSignal;
}

interface ApiResponse<T> {
  data: T;
  status: number;
  headers: Record<string, string>;
}

interface ApiError {
  status: number;
  message: string;
  code?: string;
  details?: Record<string, unknown>;
}

// Type-safe API client
class TypedApiClient {
  constructor(private config: ApiClientConfig) {}

  async get<T>(path: string, options?: RequestOptions): Promise<ApiResponse<T>> {
    return this.request<T>("GET", path, options);
  }

  async post<T>(path: string, body?: unknown, options?: RequestOptions): Promise<ApiResponse<T>> {
    return this.request<T>("POST", path, { ...options, body });
  }

  async put<T>(path: string, body?: unknown, options?: RequestOptions): Promise<ApiResponse<T>> {
    return this.request<T>("PUT", path, { ...options, body });
  }

  async delete<T>(path: string, options?: RequestOptions): Promise<ApiResponse<T>> {
    return this.request<T>("DELETE", path, options);
  }

  private async request<T>(
    method: string,
    path: string,
    options?: RequestOptions
  ): Promise<ApiResponse<T>> {
    const url = new URL(path, this.config.baseUrl);

    if (options?.query) {
      Object.entries(options.query).forEach(([key, value]) => {
        url.searchParams.set(key, String(value));
      });
    }

    const response = await fetch(url.toString(), {
      method,
      headers: {
        ...this.config.headers,
        ...options?.headers,
        "Content-Type": "application/json",
      },
      body: options?.body ? JSON.stringify(options.body) : undefined,
      signal: options?.signal,
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      throw {
        status: response.status,
        message: response.statusText,
        code: errorBody.code,
        details: errorBody,
      } as ApiError;
    }

    const data = await response.json() as T;
    const headers = Object.fromEntries(response.headers.entries());

    return { data, status: response.status, headers };
  }
}
```

---

## Fetch Wrapper with Generics

```typescript
// Strongly typed fetch wrapper
type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

interface EndpointConfig<TRequest, TResponse> {
  method: HttpMethod;
  path: string;
  response?: TRequest extends undefined ? never : TRequest;
  response?: TResponse;
}

// Type mapping for endpoints
interface ApiEndpoints {
  "/users": {
    GET: { response: User[]; query: { page?: number; limit?: number } };
    POST: { body: CreateUserDTO; response: User };
  };
  "/users/:id": {
    GET: { response: User };
    PUT: { body: Partial<User>; response: User };
    DELETE: { response: void };
  };
  "/posts": {
    GET: { response: Post[]; query: { userId?: string } };
    POST: { body: CreatePostDTO; response: Post };
  };
}

// Typed fetch function
async function apiFetch<
  TPath extends keyof ApiEndpoints,
  TMethod extends keyof ApiEndpoints[TPath]
>(
  path: TPath,
  method: TMethod,
  options?: {
    body?: ApiEndpoints[TPath][TMethod] extends { body: infer B } ? B : never;
    query?: ApiEndpoints[TPath][TMethod] extends { query: infer Q } ? Q : never;
  }
): Promise<
  ApiEndpoints[TPath][TMethod] extends { response: infer R } ? R : never
> {
  const url = new URL(path as string, "https://api.example.com");

  if (options?.query) {
    Object.entries(options.query as Record<string, unknown>).forEach(
      ([key, value]) => url.searchParams.set(key, String(value))
    );
  }

  const response = await fetch(url.toString(), {
    method: method as string,
    headers: { "Content-Type": "application/json" },
    body: options?.body ? JSON.stringify(options.body) : undefined,
  });

  return response.json();
}

// Usage - fully typed
const users = await apiFetch("/users", "GET", { query: { page: 1 } });
const user = await apiFetch("/users/:id", "GET");
const newUser = await apiFetch("/posts", "POST", {
  body: { title: "Hello", content: "World", authorId: "1" },
});
```

---

## API Response Types

```typescript
// Standardized API response types
interface SuccessResponse<T> {
  success: true;
  data: T;
  meta?: {
    page?: number;
    limit?: number;
    total?: number;
    hasMore?: boolean;
  };
}

interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
    validationErrors?: Array<{
      field: string;
      message: string;
    }>;
  };
}

type ApiResponse2<T> = SuccessResponse<T> | ErrorResponse;

// Discriminated union for error handling
function handleResponse<T>(response: ApiResponse2<T>): T {
  if (response.success) {
    return response.data;
  }
  throw new Error(response.error.message);
}

// Paginated response
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    currentPage: number;
    totalPages: number;
    totalItems: number;
    itemsPerPage: number;
    hasNextPage: boolean;
    hasPreviousPage: boolean;
  };
}

// Streaming response types
interface StreamResponse<T> {
  stream: ReadableStream<T>;
  cancel: () => void;
}

// Webhook response types
interface WebhookPayload<T> {
  event: string;
  timestamp: string;
  data: T;
  signature: string;
}
```

---

## Request/Response Interceptors

```typescript
// Interceptor pattern for API clients
interface RequestInterceptor {
  onRequest(config: RequestConfig): RequestConfig | Promise<RequestConfig>;
  onRequestError?(error: Error): Promise<never>;
}

interface ResponseInterceptor {
  onResponse<T>(response: ApiResponse<T>): ApiResponse<T> | Promise<ApiResponse<T>>;
  onResponseError?(error: ApiError): Promise<never>;
}

interface RequestConfig {
  url: string;
  method: string;
  headers: Record<string, string>;
  body?: unknown;
  timeout?: number;
}

// Interceptor manager
class InterceptorManager {
  private requestInterceptors: RequestInterceptor[] = [];
  private responseInterceptors: ResponseInterceptor[] = [];

  addRequestInterceptor(interceptor: RequestInterceptor): () => void {
    this.requestInterceptors.push(interceptor);
    return () => {
      this.requestInterceptors = this.requestInterceptors.filter(
        (i) => i !== interceptor
      );
    };
  }

  addResponseInterceptor(interceptor: ResponseInterceptor): () => void {
    this.responseInterceptors.push(interceptor);
    return () => {
      this.responseInterceptors = this.responseInterceptors.filter(
        (i) => i !== interceptor
      );
    };
  }

  async processRequest(config: RequestConfig): Promise<RequestConfig> {
    let result = config;
    for (const interceptor of this.requestInterceptors) {
      result = await interceptor.onRequest(result);
    }
    return result;
  }

  async processResponse<T>(response: ApiResponse<T>): Promise<ApiResponse<T>> {
    let result = response;
    for (const interceptor of this.responseInterceptors) {
      result = await interceptor.onResponse(result);
    }
    return result;
  }
}

// Built-in interceptors
const authInterceptor: RequestInterceptor = {
  onRequest(config) {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;
  },
};

const loggingInterceptor: RequestInterceptor = {
  onRequest(config) {
    console.log(`[API] ${config.method} ${config.url}`);
    return config;
  },
};

const cacheInterceptor: ResponseInterceptor = {
  onResponse(response) {
    if (response.status === 200) {
      const key = `cache:${response.headers["x-cache-key"]}`;
      localStorage.setItem(key, JSON.stringify(response.data));
    }
    return response;
  },
};

const retryInterceptor: ResponseInterceptor = {
  async onResponseError(error) {
    if (error.status === 429) {
      const retryAfter = error.details?.["retry-after"] ?? 5;
      await new Promise((r) => setTimeout(r, Number(retryAfter) * 1000));
      throw error; // Re-throw to trigger retry
    }
    throw error;
  },
};
```

---

## Retry Logic with Types

```typescript
// Typed retry with exponential backoff
interface RetryConfig {
  maxRetries: number;
  baseDelay: number;
  maxDelay: number;
  retryableStatuses: number[];
  retryableErrors: string[];
}

const defaultRetryConfig: RetryConfig = {
  maxRetries: 3,
  baseDelay: 1000,
  maxDelay: 30000,
  retryableStatuses: [408, 429, 500, 502, 503, 504],
  retryableErrors: ["NETWORK_ERROR", "TIMEOUT"],
};

async function withRetry<T>(
  fn: () => Promise<T>,
  config: Partial<RetryConfig> = {}
): Promise<T> {
  const mergedConfig = { ...defaultRetryConfig, ...config };
  let lastError: Error | undefined;

  for (let attempt = 0; attempt <= mergedConfig.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (attempt >= mergedConfig.maxRetries) break;

      const isRetryable =
        (error as ApiError).status &&
        mergedConfig.retryableStatuses.includes((error as ApiError).status) ||
        (error as ApiError).code &&
        mergedConfig.retryableErrors.includes((error as ApiError).code);

      if (!isRetryable) break;

      const delay = Math.min(
        mergedConfig.baseDelay * Math.pow(2, attempt) + Math.random() * 1000,
        mergedConfig.maxDelay
      );

      console.log(`Retry ${attempt + 1}/${mergedConfig.maxRetries} in ${delay}ms`);
      await new Promise((r) => setTimeout(r, delay));
    }
  }

  throw lastError;
}

// Usage
const data = await withRetry(
  () => apiClient.get<User[]>("/users"),
  { maxRetries: 5, retryableStatuses: [429, 500] }
);
```

---

## API Client Builder Pattern

```typescript
// Fluent API client builder
class APIClientBuilder {
  private baseUrl = "";
  private headers: Record<string, string> = {};
  private timeout = 5000;
  private retries = 3;
  private interceptors: RequestInterceptor[] = [];

  static create(): APIClientBuilder {
    return new APIClientBuilder();
  }

  baseUrl(url: string): this {
    this.baseUrl = url;
    return this;
  }

  header(key: string, value: string): this {
    this.headers[key] = value;
    return this;
  }

  headers(headers: Record<string, string>): this {
    Object.assign(this.headers, headers);
    return this;
  }

  timeout(ms: number): this {
    this.timeout = ms;
    return this;
  }

  retries(count: number): this {
    this.retries = count;
    return this;
  }

  withAuth(token: string): this {
    this.headers["Authorization"] = `Bearer ${token}`;
    return this;
  }

  withCors(): this {
    this.headers["Access-Control-Allow-Origin"] = "*";
    return this;
  }

  build(): TypedApiClient {
    return new TypedApiClient({
      baseUrl: this.baseUrl,
      headers: this.headers,
      timeout: this.timeout,
      retries: this.retries,
    });
  }
}

// Usage
const client = APIClientBuilder.create()
  .baseUrl("https://api.example.com")
  .withAuth("my-token")
  .timeout(10000)
  .retries(5)
  .build();

const users = await client.get<User[]>("/users");
```

---

## Error Handling in API Clients

```typescript
// Comprehensive error handling
class ApiClientError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string,
    public details?: Record<string, unknown>,
    public validationErrors?: Array<{ field: string; message: string }>
  ) {
    super(message);
    this.name = "ApiClientError";
  }

  static fromResponse(response: Response, body: unknown): ApiClientError {
    const error = body as any;
    return new ApiClientError(
      error?.message ?? response.statusText,
      response.status,
      error?.code,
      error?.details,
      error?.validationErrors
    );
  }

  isValidationError(): boolean {
    return this.status === 400 && !!this.validationErrors;
  }

  isUnauthorized(): boolean {
    return this.status === 401;
  }

  isForbidden(): boolean {
    return this.status === 403;
  }

  isNotFound(): boolean {
    return this.status === 404;
  }

  isRateLimited(): boolean {
    return this.status === 429;
  }

  isServerError(): boolean {
    return this.status >= 500;
  }
}

// Result pattern for API calls
type ApiResult<T> =
  | { ok: true; data: T; status: number }
  | { ok: false; error: ApiClientError };

async function safeApiCall<T>(
  fn: () => Promise<ApiResponse<T>>
): Promise<ApiResult<T>> {
  try {
    const response = await fn();
    return { ok: true, data: response.data, status: response.status };
  } catch (error) {
    if (error instanceof ApiClientError) {
      return { ok: false, error };
    }
    return {
      ok: false,
      error: new ApiClientError(
        error instanceof Error ? error.message : "Unknown error",
        0
      ),
    };
  }
}

// Usage with exhaustive error handling
const result = await safeApiCall(() => client.get<User[]>("/users"));

if (result.ok) {
  console.log(result.data); // TypeScript knows data is User[]
} else {
  if (result.error.isRateLimited()) {
    console.log("Rate limited, retry later");
  } else if (result.error.isUnauthorized()) {
    console.log("Please log in");
  } else {
    console.log(result.error.message);
  }
}
```

---

## Interview Questions

1. **How do you type API responses in TypeScript?**
   Use generics, discriminated unions for success/error, and mapped types for endpoint-specific responses.

2. **What is the advantage of typed API clients?**
   Compile-time type checking for requests and responses, better IDE support, and fewer runtime errors.

3. **How do you handle API errors in TypeScript?**
   Use discriminated unions, custom error classes, or Result types for type-safe error handling.

4. **What are interceptors and when would you use them?**
   Functions that run before requests or after responses. Used for auth, logging, caching, and retry logic.

5. **How do you implement retry logic with types?**
   Use generics to preserve return types and discriminated unions to determine retryable errors.

6. **What is the Builder pattern in API clients?**
   A fluent interface for configuring API clients with type-safe method chaining.

7. **How do you handle pagination in typed API clients?**
   Define paginated response types and use generics for the item type.

8. **What is the difference between a typed fetch wrapper and Axios?**
   A typed wrapper adds compile-time type safety. Axios has built-in types but less endpoint-specific typing.

9. **How do you handle streaming responses in TypeScript?**
   Use `ReadableStream<T>`, `AsyncGenerator`, or `for await...of` with appropriate types.

10. **What are the best practices for API client error handling?**
    Use discriminated unions, provide meaningful error messages, implement retry logic, and handle network errors gracefully.
