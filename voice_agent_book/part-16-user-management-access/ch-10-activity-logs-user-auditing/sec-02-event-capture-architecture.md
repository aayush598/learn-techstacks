# Event Capture Architecture

## Overview

Event capture architecture instruments the application to automatically record user actions. It uses middleware for automatic capture, provides an API for manual logging, and processes events asynchronously to minimize latency impact.

## Capture Layers

```
[User Action] → [Instrumentation Layer] → [Event Queue]
                    │                           │
            ┌───────┴───────┐            [Async Processor]
            ▼               ▼                   │
    Auto-Capture     Manual API            [Storage Layer]
    (Middleware)     (logEvent)               │
                                       [Elasticsearch/S3]
```

## Implementation

```typescript
class ActivityCaptureService {
  async autoCapture(req: Request, res: Response, duration: number): Promise<void> {
    const user = req.user;
    if (!user) return;

    const event: ActivityEvent = {
      id: generateId('act'),
      timestamp: new Date(),
      actor: {
        id: user.id,
        type: 'user',
        email: user.email,
        ipAddress: req.ip,
        userAgent: req.headers['user-agent'],
      },
      action: this.mapRouteToAction(req.method, req.path),
      target: this.extractTarget(req),
      context: {
        tenantId: user.tenantId,
        sessionId: req.session?.id,
        requestId: req.id,
        source: req.headers['x-source'] as string || 'app',
      },
      severity: res.statusCode >= 400 ? 'error' : 'info',
      metadata: { duration, statusCode: res.statusCode },
    };

    await this.queue.add(event);
  }

  async logEvent(event: Omit<ActivityEvent, 'id' | 'timestamp'>): Promise<void> {
    const fullEvent: ActivityEvent = {
      ...event,
      id: generateId('act'),
      timestamp: new Date(),
    };
    await this.queue.add(fullEvent);
  }

  private mapRouteToAction(method: string, path: string): string {
    const routeMap: Record<string, string> = {
      'GET': 'read',
      'POST': 'create',
      'PATCH': 'update',
      'PUT': 'update',
      'DELETE': 'delete',
    };
    const action = routeMap[method] || method.toLowerCase();
    const resource = path.split('/').filter(Boolean)[1] || 'unknown';
    return `${resource}.${action}`;
  }

  private extractTarget(req: Request): ActivityEvent['target'] {
    const pathParts = req.path.split('/').filter(Boolean);
    return {
      id: pathParts[2] || req.body?.id,
      type: pathParts[1] || 'unknown',
      name: req.body?.name,
    };
  }
}

// Express middleware for auto-capture
function activityCaptureMiddleware(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();
  res.on('finish', () => {
    captureService.autoCapture(req, res, Date.now() - start);
  });
  next();
}
```

## Open-Source Tools

- **BullMQ** (MIT) — Async event queue
- **Pino** (MIT) — Structured logging

## Production Considerations

- Process events asynchronously to avoid adding latency to API responses
- Batch write to storage (bulk every 5 seconds or 1000 events)
- Drop events if queue exceeds capacity (protect API performance)
- Sample high-volume events (e.g., token validation) at 1%
- Include request ID in all log events for correlation
- Never block API response on logging completion
- Monitor event queue depth and processing latency
