# Section 08: Authentication Error Handling

## Overview

Authentication errors follow clear HTTP semantics with the WWW-Authenticate header guiding clients on how to authenticate. The system distinguishes between missing credentials (401), invalid credentials (401), and insufficient permissions (403). Rate limiting on auth failures prevents brute force attacks, and error responses include enough information for debugging without exposing security-sensitive details.

## Architecture

```
Authentication Error Matrix
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario                    Status   Code                WWW-Authenticate
─────────────────────────────────────────────────────────────────────────
No Authorization header     401      UNAUTHORIZED        Bearer realm="api.voiceagent.com"
Malformed header            401      UNAUTHORIZED        Bearer error="invalid_request"
Expired token               401      UNAUTHORIZED        Bearer error="invalid_token"
Invalid API key             401      UNAUTHORIZED        Bearer error="invalid_token"
Insufficient scopes         403      FORBIDDEN           (no header)
Resource belongs to other   403      FORBIDDEN           (no header)
tenants

Error Response Body (401):
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired API key",
    "requestId": "req_abc_123",
    "documentation_url": "https://docs.voiceagent.com/api/authentication"
  }
}

Error Response Body (403):
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions. Required scope: calls:write",
    "requestId": "req_def_456"
  }
}
```

## Design Decisions

- **401 vs 403**: 401 when credentials are missing or invalid; 403 when credentials are valid but insufficient
- **WWW-Authenticate Header**: Tells clients which auth scheme to use — supports API key and Bearer token
- **Avoid Information Leakage**: Never distinguish between "user not found" and "wrong password" in error messages
- **Rate Limit on Auth Failures**: Aggressive rate limiting on auth failures — 5 attempts per second per IP

## Implementation Approach

```typescript
// Authentication error classes
class AuthenticationError extends ApiErrorResponse {
  constructor(message: string, wwwAuthenticate?: string) {
    super(401, 'UNAUTHORIZED', message);
    this.wwwAuthenticate = wwwAuthenticate;
  }

  wwwAuthenticate?: string;
}

class AuthorizationError extends ApiErrorResponse {
  constructor(message: string) {
    super(403, 'FORBIDDEN', message);
  }
}

// Error response builder
class AuthErrorHandler {
  handleMissingCredentials(): AuthenticationError {
    return new AuthenticationError(
      'Missing Authorization header. Provide a Bearer token or API key.',
      `Bearer realm="api.voiceagent.com", error="invalid_request"`,
    );
  }

  handleInvalidToken(): AuthenticationError {
    return new AuthenticationError(
      'Invalid or expired authentication credentials.',
      `Bearer realm="api.voiceagent.com", error="invalid_token"`,
    );
  }

  handleInsufficientScopes(requiredScopes: string[]): AuthorizationError {
    return new AuthorizationError(
      `Insufficient permissions. Required scope(s): ${requiredScopes.join(', ')}`,
    );
  }

  handleRateLimitedOnAuth(): AuthenticationError {
    return new AuthenticationError(
      'Too many authentication attempts. Please wait before retrying.',
      `Bearer realm="api.voiceagent.com", error="slow_down"`,
    );
  }
}

// Auth failure rate limiter
class AuthRateLimiter {
  private attempts: Map<string, { count: number; resetAt: number }> = new Map();

  constructor(
    private maxAttempts = 5,
    private windowSeconds = 1,
  ) {}

  check(key: string): void {
    const now = Date.now();
    const record = this.attempts.get(key);

    if (record && now < record.resetAt) {
      record.count++;

      if (record.count > this.maxAttempts) {
        throw new AuthErrorHandler().handleRateLimitedOnAuth();
      }
    } else {
      this.attempts.set(key, {
        count: 1,
        resetAt: now + this.windowSeconds * 1000,
      });
    }
  }

  // Periodic cleanup
  cleanup(): void {
    const now = Date.now();
    for (const [key, record] of this.attempts) {
      if (now >= record.resetAt) {
        this.attempts.delete(key);
      }
    }
  }
}

// Enhanced auth middleware with error handling
function authMiddleware(options: {
  authStrategies: AuthStrategy[];
  rateLimiter: AuthRateLimiter;
  errorHandler: AuthErrorHandler;
}) {
  return async (c: Context, next: Next) => {
    // Check auth rate limit by IP
    const clientIp = c.req.header('X-Forwarded-For') || 'unknown';
    options.rateLimiter.check(clientIp);

    const authHeader = c.req.header('Authorization');

    if (!authHeader) {
      throw options.errorHandler.handleMissingCredentials();
    }

    let authContext: AuthContext;
    let authSuccessful = false;

    for (const strategy of options.authStrategies) {
      try {
        authContext = await strategy.authenticate(c.req);
        authSuccessful = true;
        break;
      } catch (error) {
        // Try next strategy
        continue;
      }
    }

    if (!authSuccessful) {
      // Reset rate limit for valid attempts
      throw options.errorHandler.handleInvalidToken();
    }

    // Check required scopes
    const requiredScopes: string[] = c.get('requiredScopes') || [];
    const validator = new ScopeValidator();

    for (const scope of requiredScopes) {
      const result = validator.check(authContext!.scopes, scope);
      if (!result.allowed) {
        throw options.errorHandler.handleInsufficientScopes(requiredScopes);
      }
    }

    c.set('authContext', authContext);
    await next();
  };
}
```

## Integration Points

- **SDK Error Handling**: SDK maps 401 responses to `AuthenticationError` class, 403 to `AuthorizationError`
- **Logging**: Auth failures are logged with request ID for debugging; excessive failures trigger security alerts
- **Developer Portal**: Error documentation includes troubleshooting steps for common authentication errors

## Production Considerations

- **Rate Limit on Auth**: More aggressive than API rate limits — protects the auth service from brute force
- **Distributed Auth Rate Limiting**: Use Redis for auth failure rate limiting across multiple gateway instances
- **Breach Detection**: Alert on auth failure spikes that may indicate credential stuffing attacks
- **Audit Trail**: All authentication and authorization decisions are logged for compliance and incident response

## Open-Source Tools

- **Redis**: Distributed rate limiting for auth failures across instances
- **Hono**: Error handler middleware for consistent error responses
