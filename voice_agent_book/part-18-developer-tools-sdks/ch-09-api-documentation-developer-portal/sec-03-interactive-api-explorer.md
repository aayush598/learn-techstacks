# Section 03: Interactive API Explorer

## Overview

The interactive API explorer lets developers make real API calls directly from the documentation. Scalar API Reference provides a try-it-out interface with request builder, authentication integration, and response viewer. Developers can explore endpoints without leaving the documentation or writing code.

## Architecture

```
Interactive Explorer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Scalar API Reference UI]
    │
    ├── Endpoint List
    │   ├── GET /v2/agents         [▶ Try it]
    │   ├── POST /v2/agents        [▶ Try it]
    │   ├── GET /v2/agents/{id}    [▶ Try it]
    │   └── PATCH /v2/agents/{id}  [▶ Try it]
    │
    ├── Request Builder
    │   ├── Base URL: https://api.sandbox.voiceagent.com/v2
    │   ├── Auth:    ● Bearer Token  [••••••••••]
    │   ├── Headers: Content-Type: application/json
    │   ├── Path Parameters
    │   │   └── id: [ag_123]
    │   ├── Query Parameters
    │   │   ├── limit: [20]
    │   │   └── status: [active]
    │   └── Request Body (JSON Editor)
    │       └── {"name": "Test Agent", ...}
    │
    ├── [Send Request]
    │
    └── Response Viewer
        ├── Status: 201 Created
        ├── Headers: x-request-id: req_abc
        ├── Body:
        │   {
        │     "id": "ag_456",
        │     "name": "Test Agent",
        │     "status": "draft"
        │   }
        └── [Copy cURL] [Copy Response]
```

## Design Decisions

- **Scalar Over Swagger UI**: Better UI, built-in authentication management, code example generation
- **Sandbox URL Default**: API explorer defaults to sandbox endpoint for safe experimentation
- **Persistent Auth**: Authentication state persisted in localStorage; no need to re-enter
- **cURL Export**: Every request can be exported as a cURL command

## Implementation Approach

```typescript
// Scalar API Reference integration
// docusaurus.config.js — Scalar plugin
plugins: [
  [
    'docusaurus-plugin-scalar-api-reference',
    {
      id: 'api-explorer',
      specPath: 'specs/openapi.yaml',
      // Scalar configuration
      config: {
        // Default to sandbox
        servers: [
          { url: 'https://api.sandbox.voiceagent.com/v2', description: 'Sandbox (default)' },
          { url: 'https://api.voiceagent.com/v2', description: 'Production' },
        ],
        // Authentication
        authentication: {
          preferredSecurityScheme: 'bearerAuth',
          apiKey: {
            token: '',
          },
        },
        // UI customization
        showSidebar: true,
        theme: 'purple',
      },
    },
  ],
];

// Custom API explorer component (for embedded use)
function ApiExplorer({ endpoint, method }: { endpoint: string; method: string }) {
  const [authToken, setAuthToken] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const [requestBody, setRequestBody] = useState('{\n  \n}');
  const [queryParams, setQueryParams] = useState<Record<string, string>>({});

  async function executeRequest() {
    setLoading(true);

    try {
      const url = new URL(`https://api.sandbox.voiceagent.com/v2${endpoint}`);
      for (const [key, value] of Object.entries(queryParams)) {
        if (value) url.searchParams.set(key, value);
      }

      const res = await fetch(url.toString(), {
        method,
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json',
        },
        body: method !== 'GET' ? requestBody : undefined,
      });

      const responseBody = await res.json();

      setResponse({
        status: res.status,
        statusText: res.statusText,
        headers: Object.fromEntries(res.headers),
        body: responseBody,
        time: Date.now(),
      });
    } catch (error) {
      setResponse({
        status: 0,
        statusText: 'Network Error',
        error: (error as Error).message,
      });
    } finally {
      setLoading(false);
    }
  }

  function generateCurl(): string {
    const parts = [`curl -X ${method}`];
    parts.push(`'https://api.sandbox.voiceagent.com/v2${endpoint}'`);
    parts.push(`-H 'Authorization: Bearer ${authToken}'`);
    parts.push("-H 'Content-Type: application/json'");

    if (requestBody && method !== 'GET') {
      parts.push(`-d '${requestBody}'`);
    }

    return parts.join(' \\\n  ');
  }

  return (
    <div className="api-explorer">
      <div className="auth-section">
        <label>Bearer Token:</label>
        <input
          type="password"
          value={authToken}
          onChange={(e) => setAuthToken(e.target.value)}
          placeholder="va_test_... or your JWT token"
        />
      </div>

      <div className="request-section">
        <div className="method-badge">{method}</div>
        <code className="endpoint">{`/v2${endpoint}`}</code>
        <button onClick={executeRequest} disabled={loading}>
          {loading ? 'Sending...' : 'Send Request'}
        </button>
        <button onClick={() => navigator.clipboard.writeText(generateCurl())}>
          Copy cURL
        </button>
      </div>

      {response && (
        <div className="response-section">
          <div className={`status-badge ${response.status < 400 ? 'success' : 'error'}`}>
            {response.status} {response.statusText}
          </div>

          <details>
            <summary>Response Headers</summary>
            <pre>{JSON.stringify(response.headers, null, 2)}</pre>
          </details>

          <div>
            <h4>Response Body:</h4>
            <pre>{JSON.stringify(response.body, null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
```

## Integration Points

- **Developer Portal**: Embedded API explorer on each endpoint documentation page
- **Authentication**: Uses sandbox API keys automatically for try-it-out
- **Code Examples**: Automatically generated from request configuration

## Production Considerations

- **CORS Configuration**: API Explorer requires CORS headers on sandbox API
- **Rate Limits**: Explorer calls count toward sandbox rate limits
- **Sensitive Data**: Warn users not to use production API keys in the explorer
- **Request Timeout**: Explorer requests timeout after 30 seconds

## Open-Source Tools

- **Scalar API Reference**: Interactive API documentation with try-it-out
- **Swagger UI**: Alternative interactive API explorer
