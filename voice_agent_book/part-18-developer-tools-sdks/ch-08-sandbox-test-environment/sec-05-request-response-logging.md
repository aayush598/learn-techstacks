# Section 05: Request/Response Logging

## Overview

Every sandbox API request and its response are captured in full for debugging. Request logs include headers, body, query parameters, and timing. A replay capability allows developers to re-run requests with the same parameters. The logging UI provides search, filter, and detail inspection.

## Architecture

```
Request Logging Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[API Request] → [Sandbox Gateway]
                    │
              [Logging Middleware]
                    │
              ├── Capture Request:
              │   ├── Method, URL, Headers
              │   ├── Query parameters
              │   ├── Request body
              │   └── Timestamp
                    │
              [Process Request]
                    │
              [Logging Middleware]
                    │
              ├── Capture Response:
              │   ├── Status code
              │   ├── Response headers
              │   ├── Response body
              │   ├── Duration
              │   └── Error (if any)
                    │
              [Store in Log Database]
                    │
              [Replay Capability]
              ├── View in Dashboard
              ├── Download as cURL
              └── Replay with modifications

Log Entry:
  {
    "id": "log_abc_123",
    "requestId": "req_xyz_789",
    "tenantId": "tenant_demo",
    "method": "POST",
    "path": "/v1/agents",
    "query": {},
    "requestHeaders": {
      "authorization": "Bearer va_test_... (masked)",
      "content-type": "application/json"
    },
    "requestBody": {"name": "Test Agent", "voice": {...}},
    "responseStatus": 201,
    "responseHeaders": {"x-request-id": "req_xyz_789"},
    "responseBody": {"id": "ag_123", "name": "Test Agent", ...},
    "durationMs": 245,
    "createdAt": "2025-06-01T10:00:00.000Z"
  }
```

## Design Decisions

- **Full Body Capture**: Request and response bodies stored for complete debugging
- **Sensitive Data Masking**: Authorization headers, API keys, and tokens are masked in logs
- **Search & Filter**: Logs searchable by method, path, status code, and date range
- **cURL Export**: One-click export of any request as a cURL command

## Implementation Approach

```typescript
// Request/response log capture
interface RequestLog {
  id: string;
  requestId: string;
  tenantId: string;
  method: string;
  path: string;
  query: Record<string, string>;
  requestHeaders: Record<string, string>;
  requestBody: unknown;
  responseStatus: number;
  responseHeaders: Record<string, string>;
  responseBody: unknown;
  durationMs: number;
  error?: string;
  createdAt: Date;
}

class RequestLogger {
  async capture(
    requestId: string,
    tenantId: string,
    req: Request,
    res: Response,
    durationMs: number,
  ): Promise<void> {
    const log: RequestLog = {
      id: generateId('log'),
      requestId,
      tenantId,
      method: req.method,
      path: new URL(req.url).pathname,
      query: Object.fromEntries(new URL(req.url).searchParams),
      requestHeaders: this.sanitizeHeaders(req.headers),
      requestBody: await this.safeParseBody(req),
      responseStatus: res.status,
      responseHeaders: this.sanitizeHeaders(res.headers),
      responseBody: await this.safeParseBody(res),
      durationMs,
      createdAt: new Date(),
    };

    await this.store.logs.insert(log);
  }

  private sanitizeHeaders(headers: Headers): Record<string, string> {
    const sensitiveHeaders = ['authorization', 'x-api-key', 'cookie', 'set-cookie'];
    const result: Record<string, string> = {};

    for (const [key, value] of headers) {
      if (sensitiveHeaders.includes(key.toLowerCase())) {
        result[key] = value.slice(0, 10) + '... (masked)';
      } else {
        result[key] = value;
      }
    }

    return result;
  }

  private async safeParseBody(source: { body?: unknown; json?: () => Promise<unknown>; text?: () => Promise<string> }): Promise<unknown> {
    try {
      if (source.body) return source.body;
      if (source.json) return source.json();
      if (source.text) return source.text();
      return null;
    } catch {
      return '<unparseable>';
    }
  }
}

// Log search and replay
class LogInspector {
  async search(params: {
    tenantId: string;
    method?: string;
    path?: string;
    status?: number;
    from?: Date;
    to?: Date;
    cursor?: string;
    limit?: number;
  }): Promise<ListResponse<RequestLog>> {
    const query = this.buildQuery(params);
    return this.store.logs.find(query, { createdAt: -1 }, params.limit || 20);
  }

  async getById(logId: string): Promise<RequestLog | null> {
    return this.store.logs.findOne({ id: logId });
  }

  async replay(logId: string): Promise<ReplayResult> {
    const log = await this.getById(logId);
    if (!log) throw new Error('Log not found');

    // Reconstruct and send request
    const response = await fetch(`${log.path}${this.buildQueryString(log.query)}`, {
      method: log.method,
      headers: log.requestHeaders,
      body: log.method !== 'GET' ? JSON.stringify(log.requestBody) : undefined,
    });

    return {
      status: response.status,
      headers: Object.fromEntries(response.headers),
      body: await response.json(),
      durationMs: 0, // Measured by caller
    };
  }

  async exportAsCurl(logId: string): Promise<string> {
    const log = await this.getById(logId);
    if (!log) throw new Error('Log not found');

    const parts = [`curl -X ${log.method}`];
    parts.push(`'${log.path}'`);

    for (const [key, value] of Object.entries(log.requestHeaders)) {
      parts.push(`-H '${key}: ${value}'`);
    }

    if (log.requestBody && log.method !== 'GET') {
      parts.push(`-d '${JSON.stringify(log.requestBody)}'`);
    }

    return parts.join(' \\\n  ');
  }
}
```

## Integration Points

- **Developer Dashboard**: Log viewer with search, filter, and detail panels
- **cURL Export**: One-click cURL command generation for sharing requests
- **Webhook Debugging**: Webhook delivery logs show request/response for each attempt

## Production Considerations

- **Storage Volume**: Full logging generates significant data; 7-day retention for sandbox logs
- **Performance Impact**: Logging is async (fire-and-forget) — no latency added to request processing
- **Sensitive Data Auditing**: Regular audit of masked fields to ensure no credentials leak
- **Log Export**: Bulk export capability for compliance and analysis

## Open-Source Tools

- **Elasticsearch**: Log storage and full-text search
- **Kibana**: Log visualization and dashboard
