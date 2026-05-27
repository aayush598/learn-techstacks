# Section 05: Authentication & Auth Test Helpers

## Overview

Authentication testing for the voice AI platform involves validating JWT token handling, session management, role-based access control (RBAC), API key authentication, and OAuth integration. Auth test helpers provide utilities for generating test tokens, creating authenticated sessions, simulating different user roles, and testing authorization enforcement across API endpoints.

The auth testing strategy treats authentication and authorization as separate concerns. Authentication tests validate that the system correctly verifies who the user is. Authorization tests validate that authenticated users can only access resources they're permitted to access. Both are tested extensively at the integration level.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Simulator|--->| Utterance|--->| Flow     |--->| Debug    |--->| Report   |
| (in-     |    | Player   |    | Executor |    | Panel    |    | (pass/   |
|  browser)|    | (text/   |    | (step    |    | (log,    |    |  fail    |
|          |    |  audio)  |    |  thru)   |    |  state)  |    |  + trace)|
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **In-Browser Simulator**: Full conversation simulation with WASM runtime. No backend needed.
- **Utterance Testing**: Pre-defined test utterances with assertions on path and response.
- **Flow Validation**: Graph analysis for unreachable nodes, infinite loops, missing required fields.
## Implementation Approach

```typescript
// Auth test helpers
import jwt from 'jsonwebtoken';

interface AuthContext {
  token: string;
  user: { id: string; email: string; role: string };
  organization: { id: string; name: string };
}

function createAuthContext(overrides: Partial<AuthContext> = {}): AuthContext {
  const defaults: AuthContext = {
    token: '',
    user: { id: 'user-1', email: 'test@example.com', role: 'admin' },
    organization: { id: 'org-1', name: 'Test Org' },
  };
  const ctx = { ...defaults, ...overrides };

  ctx.token = jwt.sign(
    {
      sub: ctx.user.id,
      email: ctx.user.email,
      role: ctx.user.role,
      orgId: ctx.organization.id,
    },
    process.env.JWT_SECRET || 'test-secret',
    { expiresIn: '1h' }
  );

  return ctx;
}

// Permission matrix testing
const permissionMatrix = [
  { role: 'admin',   endpoint: 'POST /api/agents', expected: 201 },
  { role: 'admin',   endpoint: 'DELETE /api/agents/:id', expected: 200 },
  { role: 'member',  endpoint: 'POST /api/agents', expected: 201 },
  { role: 'member',  endpoint: 'DELETE /api/agents/:id', expected: 403 },
  { role: 'viewer',  endpoint: 'POST /api/agents', expected: 403 },
  { role: 'viewer',  endpoint: 'GET /api/agents', expected: 200 },
];

describe.each(permissionMatrix)(
  '$role can access $endpoint',
  ({ role, endpoint, expected }) => {
    it(`returns ${expected} for ${role}`, async () => {
      const ctx = createAuthContext({
        user: { ...defaultUser, role },
      });
      const [method, path] = endpoint.split(' ');
      
      const response = await apiRequest(app)
        .as(ctx.token)
        [method.toLowerCase()](path.replace(':id', 'agent-1'));

      expect(response.status).toBe(expected);
    });
  }
);
```

## Integration Points

- **JWT Secret**: Test JWT secret configured in test environment
- **Session Store**: Test session store (Redis) managed by Testcontainers
- **OAuth Provider**: OAuth flow tested with mock OAuth provider (MSW)
- **API Key Store**: API keys stored in test database alongside fixtures
- **Permission Cache**: Permission cache cleared between test suites

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Token Expiry**: Test token expiry handling; ensure tests don't use expired tokens
- **Secret Rotation**: Test secret rotation scenarios; system should handle multiple valid secrets
- **Rate Limiting**: Auth endpoints often have rate limits; ensure tests account for this
- **Audit Logging**: Test that auth events are properly logged in audit trail
- **Multi-Factor Auth**: If MFA is implemented, add MFA-specific test flows
