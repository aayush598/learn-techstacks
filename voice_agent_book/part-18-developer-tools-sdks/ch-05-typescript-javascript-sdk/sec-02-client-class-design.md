# Section 02: Client Class Design

## Overview

The SDK client class provides a fluent, intuitive interface for all API operations. Resources are accessed as properties of the client instance, supporting method chaining and typed responses. The client handles authentication, request serialization, error mapping, and response parsing transparently.

## Architecture

```
Fluent Client Interface
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Client Access Patterns:
  // Resource access
  client.agents.list()              → ListResponse<Agent>
  client.agents.get(id)             → Agent
  client.agents.create(data)        → Agent
  client.calls.list()               → ListResponse<Call>
  client.campaigns.create(data)     → Campaign

  // Method chaining
  client.agents
    .list({ status: 'active' })
    .then(agents => agents.data[0])
    .then(agent => client.agents.get(agent.id))
    .then(agent => console.log(agent.name))

  // Streaming
  client.events.subscribe('call:*', (event) => {
    console.log(event.data);
  })

Request Builder Pattern:
  client.agents
    .query({ status: 'active' })
    .sort('createdAt', 'desc')
    .limit(20)
    .fetch()

Error Handling:
  try {
    await client.agents.get('nonexistent');
  } catch (error) {
    if (error instanceof NotFoundError) {
      // Handle 404
    } else if (error instanceof RateLimitError) {
      // Handle 429
    } else if (error instanceof ValidationError) {
      // Handle 400
    }
  }
```

## Design Decisions

- **Resource Properties Over Methods**: `client.agents` not `client.agents()` — cleaner syntax
- **Typed Errors**: API errors map to typed error classes for instanceof checks
- **Automatic Pagination**: List responses include pagination helpers for iteration
- **Request Interceptors**: Plugins can modify requests (add headers, log, retry) without changing client code

## Implementation Approach

```typescript
// HTTP client with typed responses
class HttpClient {
  constructor(private config: Required<VoiceAgentConfig>) {}

  private async request<T>(method: string, path: string, options?: RequestOptions): Promise<T> {
    const url = new URL(path, this.config.baseUrl);

    // Query parameters
    if (options?.params) {
      for (const [key, value] of Object.entries(options.params)) {
        if (value !== undefined) {
          url.searchParams.set(key, String(value));
        }
      }
    }

    const headers: Record<string, string> = {
      'Authorization': `Bearer ${this.config.apiKey}`,
      'Content-Type': 'application/json',
      'User-Agent': `@voiceagent/sdk v${VERSION}`,
      ...options?.headers,
    };

    // Idempotency key for mutating requests
    if (['POST', 'PATCH', 'DELETE'].includes(method) && !options?.skipIdempotency) {
      headers['Idempotency-Key'] = crypto.randomUUID();
    }

    let response = await fetch(url.toString(), {
      method,
      headers,
      body: options?.body ? JSON.stringify(options.body) : undefined,
      signal: options?.signal,
    });

    // Apply plugin response hooks
    for (const plugin of this.config.plugins) {
      if (plugin.response) {
        response = await plugin.response(response, { method, headers, body: options?.body });
      }
    }

    // Handle errors
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      throw this.mapError(response.status, errorBody);
    }

    // Parse response
    if (response.status === 204) {
      return undefined as T;
    }

    return response.json();
  }

  async get<T>(path: string, options?: RequestOptions): Promise<T> {
    return this.request<T>('GET', path, options);
  }

  async post<T>(path: string, options?: RequestOptions): Promise<T> {
    return this.request<T>('POST', path, options);
  }

  async patch<T>(path: string, options?: RequestOptions): Promise<T> {
    return this.request<T>('PATCH', path, options);
  }

  async delete<T>(path: string, options?: RequestOptions): Promise<T> {
    return this.request<T>('DELETE', path, options);
  }

  private mapError(status: number, body: { error?: { code?: string; message?: string } }): Error {
    const code = body?.error?.code || 'UNKNOWN';
    const message = body?.error?.message || 'An unknown error occurred';

    switch (status) {
      case 400: return new ValidationError(message, code);
      case 401: return new AuthenticationError(message, code);
      case 403: return new AuthorizationError(message, code);
      case 404: return new NotFoundError(message, code);
      case 409: return new ConflictError(message, code);
      case 422: return new ValidationError(message, code);
      case 429: return new RateLimitError(message, code);
      case 500:
      case 502:
      case 503:
        return new ServerError(message, code);
      default: return new ApiError(message, status, code);
    }
  }
}

// Fluent resource client
class AgentsResource {
  constructor(private http: HttpClient) {}

  list(params?: AgentListParams): Promise<ListResponse<Agent>> {
    return this.http.get('/v1/agents', { params });
  }

  get(id: string): Promise<Agent> {
    return this.http.get(`/v1/agents/${id}`);
  }

  create(data: CreateAgentRequest): Promise<Agent> {
    return this.http.post('/v1/agents', { body: data });
  }

  update(id: string, data: Partial<UpdateAgentRequest>): Promise<Agent> {
    return this.http.patch(`/v1/agents/${id}`, { body: data });
  }

  delete(id: string): Promise<void> {
    return this.http.delete(`/v1/agents/${id}`);
  }

  deploy(id: string): Promise<DeployResult> {
    return this.http.post(`/v1/agents/${id}/deploy`);
  }

  // Async iterator for auto-pagination
  async *listAll(params?: Omit<AgentListParams, 'cursor'>): AsyncGenerator<Agent> {
    let cursor: string | undefined;

    do {
      const response = await this.list({ ...params, cursor });
      for (const item of response.data) {
        yield item;
      }
      cursor = response.pagination.cursor || undefined;
    } while (cursor);
  }
}

// Usage with auto-pagination
async function main() {
  const client = new VoiceAgent({ apiKey: 'va_live_abc' });

  for await (const agent of client.agents.listAll({ status: 'active' })) {
    console.log(agent.name);
  }
}
```

## Integration Points

- **OpenAPI Types**: All request/response types generated from OpenAPI spec
- **Plugin System**: Extend client with custom behavior via plugins
- **WebSocket Events**: Event subscription methods integrated into client

## Production Considerations

- **Connection Pooling**: HTTP/2 multiplexing for Node.js; keep-alive for browsers
- **Request Timeout**: Configurable per-request timeout with AbortController
- **Error Recovery**: Retry logic with exponential backoff for transient failures
- **Bundle Size**: Client core ~5KB gzipped; individual resources tree-shakable

## Open-Source Tools

- **openapi-typescript**: Auto-generated TypeScript types from OpenAPI spec
