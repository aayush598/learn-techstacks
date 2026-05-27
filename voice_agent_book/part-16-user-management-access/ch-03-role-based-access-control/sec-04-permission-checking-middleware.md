# Permission Checking Middleware

## Overview

Permission checking middleware intercepts API requests and verifies that the authenticated user has the required permissions before the request reaches the handler. This section covers middleware patterns for REST APIs, GraphQL, gRPC, and server-rendered pages.

## Express/Next.js Middleware Pattern

```
[Request] → [Auth Middleware] → [Permission Middleware] → [Route Handler]
                │                       │
                ▼                       ▼
         Authenticate User         Check Permissions
         Extract Token             Action + Resource
         Load User + Roles         Evaluate → Allow/Deny
                                               │
                                         ┌─────┴─────┐
                                         ▼           ▼
                                       Allow       Deny (403)
```

## Implementation

```typescript
import { NextRequest, NextResponse } from 'next/server';

type PermissionCheck = (
  req: NextRequest,
  context: { params: Record<string, string> }
) => Promise<boolean>;

interface PermissionMiddlewareOptions {
  action: string;
  resource: string | ((req: NextRequest, params: Record<string, string>) => string);
  getResourceId?: (req: NextRequest, params: Record<string, string>) => string | undefined;
}

function requirePermission(options: PermissionMiddlewareOptions): PermissionCheck {
  return async (req, context) => {
    const user = await getAuthUser(req);
    if (!user) return false;

    const resource = typeof options.resource === 'function'
      ? options.resource(req, context.params)
      : options.resource;

    const resourceId = options.getResourceId?.(req, context.params);

    return permissionEngine.check({
      userId: user.id,
      tenantId: user.tenantId,
      action: options.action,
      resource,
      resourceId,
    }).then(result => result.allowed);
  };
}

// Usage in API routes
export async function GET(req: NextRequest) {
  const hasPermission = await requirePermission({
    action: 'read',
    resource: 'agents',
    getResourceId: (req, params) => params.id,
  })(req, { params: { id: req.nextUrl.pathname.split('/').pop()! } });

  if (!hasPermission) {
    return NextResponse.json(
      { error: 'Forbidden', code: 'INSUFFICIENT_PERMISSIONS' },
      { status: 403 }
    );
  }

  // Continue with handler logic
  return NextResponse.json({ data: 'ok' });
}
```

## Express Middleware

```typescript
import { Request, Response, NextFunction } from 'express';

interface PermissionGuardOptions {
  action: string;
  resource: string;
  getResourceId?: (req: Request) => string | undefined;
}

function permissionGuard(options: PermissionGuardOptions) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = req.user; // Set by auth middleware
      if (!user) {
        return res.status(401).json({ error: 'Unauthorized' });
      }

      const resourceId = options.getResourceId?.(req);

      const result = await permissionEngine.check({
        userId: user.id,
        tenantId: user.tenantId,
        action: options.action,
        resource: options.resource,
        resourceId,
      });

      if (!result.allowed) {
        return res.status(403).json({
          error: 'Forbidden',
          code: 'INSUFFICIENT_PERMISSIONS',
          reason: result.reason,
        });
      }

      next();
    } catch (error) {
      next(error);
    }
  };
}

// Router-level usage
router.get('/agents',
  permissionGuard({ action: 'read', resource: 'agents' }),
  agentController.listAgents
);

router.post('/agents/:id/calls',
  permissionGuard({
    action: 'create',
    resource: 'calls',
    getResourceId: (req) => req.params.id,
  }),
  callController.createCall
);
```

## Decorator-Based Approach (TypeScript)

```typescript
function RequirePermission(action: string, resource: string) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const req = findRequestObject(args);
      const user = req?.user;

      if (!user) {
        throw new HttpException(401, 'Unauthorized');
      }

      const allowed = await permissionEngine.check({
        userId: user.id,
        tenantId: user.tenantId,
        action,
        resource,
      });

      if (!allowed) {
        throw new HttpException(403, 'Forbidden');
      }

      return originalMethod.apply(this, args);
    };

    return descriptor;
  };
}

// Usage
class AgentController {
  @RequirePermission('read', 'agents')
  async listAgents(req: Request, res: Response) {
    // Handler logic
  }
}
```

## GraphQL Directive Guards

```typescript
import { mapSchema, MapperKind, getDirectives } from '@graphql-tools/utils';
import { GraphQLSchema } from 'graphql';

function permissionDirectiveTransformer(schema: GraphQLSchema) {
  return mapSchema(schema, {
    [MapperKind.OBJECT_FIELD]: (fieldConfig) => {
      const directives = getDirectives(schema, fieldConfig);
      const permissionDirective = directives['permission'] as {
        action?: string;
        resource?: string;
      };

      if (!permissionDirective) return fieldConfig;

      const originalResolver = fieldConfig.resolve;

      fieldConfig.resolve = async (source, args, context, info) => {
        const user = context.user;
        if (!user) {
          throw new GraphQLError('Unauthorized', { extensions: { code: 401 } });
        }

        const allowed = await permissionEngine.check({
          userId: user.id,
          tenantId: user.tenantId,
          action: permissionDirective.action || 'read',
          resource: permissionDirective.resource || info.fieldName,
        });

        if (!allowed) {
          throw new GraphQLError('Forbidden', { extensions: { code: 403 } });
        }

        return originalResolver?.call(this, source, args, context, info);
      };

      return fieldConfig;
    },
  });
}
```

## Middleware Pipeline with Permission Context

```typescript
interface PermissionContext {
  action: string;
  resource: string;
  resourceId?: string;
  attributes?: Record<string, unknown>;
}

// Attach permission context to request for downstream use
function enrichRequestWithPermissions(action: string, resource: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    req.permissionContext = { action, resource };
    next();
  };
}

// Resource-level ownership check middleware
function requireResourceOwnership(resourceType: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    const resourceId = req.params.id;

    const resource = await resourceService.getResource(resourceType, resourceId);
    if (!resource) {
      return res.status(404).json({ error: 'Not found' });
    }

    // Check if user owns the resource or has tenant-level access
    const allowed = resource.ownerId === user.id ||
      resource.tenantId === user.tenantId;

    if (!allowed) {
      return res.status(403).json({ error: 'Forbidden' });
    }

    req.resource = resource;
    next();
  };
}
```

## Testing

```typescript
describe('Permission Middleware', () => {
  it('returns 403 when user lacks permission', async () => {
    const req = mockRequest({ user: { id: 'user1', tenantId: 'tenant1', roles: ['viewer'] } });
    const res = mockResponse();
    const next = jest.fn();

    await permissionGuard({ action: 'delete', resource: 'agents' })(req, res, next);

    expect(res.status).toHaveBeenCalledWith(403);
    expect(next).not.toHaveBeenCalled();
  });

  it('calls next when user has permission', async () => {
    const req = mockRequest({ user: { id: 'admin1', tenantId: 'tenant1', roles: ['admin'] } });
    const res = mockResponse();
    const next = jest.fn();

    await permissionGuard({ action: 'delete', resource: 'agents' })(req, res, next);

    expect(next).toHaveBeenCalled();
  });
});
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Middleware for Express, Koa, and other frameworks
- **express-jwt-permissions** (MIT) — Lightweight JWT permission middleware
- **graphql-shield** (MIT) — GraphQL permission layer

## Production Considerations

- Apply permission middleware at the router level (before route-specific middleware) to fail fast
- Cache permission decisions at the middleware level with short TTL (30s) for high-traffic routes
- Return consistent error format with permission denied reason for debugging
- Include permission check duration in response headers (X-Permission-Check-Ms) for monitoring
- Add per-route rate limiting that considers permission failures as potential attack indicators
- Test permission middleware in isolation with mocked permission engine
