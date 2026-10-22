# Express, Fastify, and NestJS Adapters

> Part XVIII · Chapter 48 · Sections 48.1–48.8 · _Estimated reading time: 26 min_
> **Prerequisite:** [Framework Hierarchies and Handlers](../01-concepts/01-framework-hierarchies-and-handlers.md), [Dependency Injection, ORM, and Validation Mapping](../01-concepts/02-dependency-injection-orm-and-validation-mapping.md), [Framework-Independent Policy and Adapters](../01-concepts/03-framework-independent-policy-and-adapters.md)

## In one sentence

Three concrete adapters show the same core policy wired into **Express**, **Fastify**, and
**NestJS** — with validation normalization, ORM translation, DI-aware bootstrap, and RFC 9457
responses.

## Why this matters in production

Reading specs is not enough. These examples show the wiring details that break in practice:
Express 4-arg middleware, Fastify's `setErrorHandler`, NestJS filters and pipes, Prisma error
mapping, and zod/class-validator normalization. Copy the pattern, not the framework magic.

## Shared core (framework-free)

```ts
// core/errors.ts
export class AppError extends Error {
  constructor(
    public readonly code: string,
    public readonly safeContext: Record<string, unknown> = {},
    options?: { cause?: unknown }
  ) {
    super(code, options);
    this.name = 'AppError';
  }
}

// core/registry.ts
export const ERROR_REGISTRY = {
  VALIDATION_ERROR:        { status: 422, retryable: false, alert: false, title: 'Validation failed' },
  DUPLICATE_RESOURCE:      { status: 409, retryable: false, alert: false, title: 'Conflict' },
  REFERENCE_NOT_FOUND:     { status: 422, retryable: false, alert: false, title: 'Invalid reference' },
  PAYMENT_CARD_DECLINED:   { status: 402, retryable: false, alert: false, title: 'Card declined' },
  PAYMENT_PROVIDER_TIMEOUT:{ status: 504, retryable: true,  alert: false, title: 'Payment provider timeout' },
  DEPENDENCY_TIMEOUT:      { status: 504, retryable: true,  alert: false, title: 'Dependency timeout' },
  DEPENDENCY_UNAVAILABLE:  { status: 503, retryable: true,  alert: false, title: 'Service unavailable' },
  CONCURRENCY_CONFLICT:    { status: 409, retryable: true,  alert: false, title: 'Conflict' },
  NOT_FOUND:               { status: 404, retryable: false, alert: false, title: 'Not found' },
  INTERNAL_ERROR:          { status: 500, retryable: false, alert: true,  title: 'Internal error' },
} as const;

export function policyFor(code: string) {
  return (ERROR_REGISTRY as any)[code] ?? ERROR_REGISTRY.INTERNAL_ERROR;
}

// core/normalize.ts
export function normalize(err: unknown): AppError {
  if (err instanceof AppError) return err;
  // framework/validation/orm translations added by adapters via checks below
  if (isZodError(err)) return mapZod(err);
  if (isPrismaError(err)) return mapPrisma(err);
  // unknown
  return new AppError('INTERNAL_ERROR', {}, { cause: err });
}
```

## 1) Express adapter

### Validation with zod

```ts
// adapters/express/validate.ts
import { z } from 'zod';
import { AppError } from '../../core/errors';

export function validate<T>(schema: z.ZodSchema<T>) {
  return (req: any, res: any, next: any) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      // map to AppError at the boundary
      return next(mapZodError(result.error));
    }
    req.body = result.data;
    next();
  };
}

function mapZodError(e: z.ZodError) {
  const fields = e.issues.map(i => ({ path: i.path.join('.'), code: i.code, message: i.message }));
  return new AppError('VALIDATION_ERROR', { fields });
}
```

### ORM translation in repository

```ts
// repo/userRepo.ts
import { Prisma } from '@prisma/client';
import { AppError } from '../core/errors';

export async function createUser(data: any) {
  try {
    return await prisma.user.create({ data });
  } catch (e) {
    if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === 'P2002') {
      throw new AppError('DUPLICATE_RESOURCE', { target: e.meta?.target }, { cause: e });
    }
    if (e instanceof Prisma.PrismaClientKnownRequestError && e.code === 'P2034') {
      throw new AppError('CONCURRENCY_CONFLICT', {}, { cause: e });
    }
    throw e; // let normalize handle
  }
}
```

### Error middleware

```ts
// adapters/express/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { normalize } from '../../core/normalize';
import { policyFor } from '../../core/registry';
import { toProblem } from '../../core/problem';

export function errorHandler(err: unknown, req: Request, res: Response, next: NextFunction) {
  if (res.headersSent) {
    return next(err); // delegate
  }
  const appErr = normalize(err);
  const p = policyFor(appErr.code);
  const body = toProblem(appErr, p, req);
  // structured log + alert here
  res.status(p.status).type('application/problem+json').json(body);
}

// app.ts
app.use(express.json());
app.post('/checkout', validate(CheckoutSchema), checkoutHandler);
app.use(errorHandler); // last
```

## 2) Fastify adapter

Fastify uses `setErrorHandler` and has built-in schema validation. Normalize both.

```ts
// adapters/fastify/app.ts
import Fastify from 'fastify';
import { AppError } from '../../core/errors';
import { normalize } from '../../core/normalize';
import { policyFor } from '../../core/registry';
import { toProblem } from '../../core/problem';

const fastify = Fastify({ logger: true });

// JSON schema validation errors are thrown as FST_ERR_VALIDATION
fastify.setErrorHandler((err: any, req, reply) => {
  // Fastify validation error
  if (err.validation) {
    const fields = err.validation.map((v: any) => ({
      path: v.instancePath || v.dataPath || '',
      message: v.message,
      keyword: v.keyword
    }));
    const appErr = new AppError('VALIDATION_ERROR', { fields }, { cause: err });
    const p = policyFor(appErr.code);
    return reply.code(p.status).type('application/problem+json').send(toProblem(appErr, p, req));
  }

  const appErr = normalize(err);
  const p = policyFor(appErr.code);
  return reply.code(p.status).type('application/problem+json').send(toProblem(appErr, p, req));
});

fastify.post('/checkout', {
  schema: { body: CheckoutJsonSchema }
}, checkoutHandler);
```

**Note:** Fastify's schema validation errors are easier to normalize at the handler because
`err.validation` is present. Don't let them reach a generic string-based mapper.

## 3) NestJS adapter

NestJS uses pipes for validation, filters for exceptions, and modules for DI. Handle
startup failures separately.

### Validation pipe

```ts
// adapters/nestjs/validation.pipe.ts
import { PipeTransform, Injectable, ArgumentMetadata } from '@nestjs/common';
import { AppError } from '../../core/errors';

@Injectable()
export class AppValidationPipe implements PipeTransform {
  constructor(private schema: any) {}
  transform(value: any, metadata: ArgumentMetadata) {
    const result = this.schema.safeParse(value);
    if (!result.success) {
      const fields = result.error.issues.map((i: any) => ({ path: i.path.join('.'), code: i.code, message: i.message }));
      throw new AppError('VALIDATION_ERROR', { fields });
    }
    return result.data;
  }
}
```

### Exception filter

```ts
// adapters/nestjs/global-exception.filter.ts
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { normalize } from '../../core/normalize';
import { policyFor } from '../../core/registry';
import { toProblem } from '../../core/problem';

@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    // If NestJS HttpException and not an AppError, normalize if possible
    let appErr = normalize(exception);
    // If it's a plain HttpException with no mapping, normalize will make it INTERNAL_ERROR
    // but you can also map specific ones here

    const p = policyFor(appErr.code);
    const body = toProblem(appErr, p, request);
    response.status(p.status).type('application/problem+json').json(body);
  }
}

// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalFilters(new GlobalExceptionFilter());
  app.useGlobalPipes(new AppValidationPipe(CheckoutSchema)); // or per-route
  await app.init();
  await app.listen(3000);
}
bootstrap().catch(err => {
  console.error('startup_failed', err);
  process.exit(1);
});
```

### DI startup example

```ts
// modules/checkout/checkout.service.ts
@Injectable()
export class CheckoutService {
  constructor(private readonly repo: UserRepo, private readonly gateway: PaymentGateway) {}
  async charge() { /* ... */ }
}

// If PaymentGateway constructor throws (bad config), NestJS will fail during module init
// and bootstrap().catch() will log and exit — correct for critical deps
```

## Shared problem serializer

```ts
// core/problem.ts
export function toProblem(appErr: any, p: any, req: any) {
  return {
    type: `https://api.acme.com/errors/${appErr.code.toLowerCase().replace(/_/g, '-')}`,
    title: p.title,
    status: p.status,
    detail: appErr.message === appErr.code ? p.title : appErr.message,
    instance: req?.url,
    code: appErr.code,
    ...(appErr.safeContext?.fields ? { errors: appErr.safeContext.fields } : {}),
    requestId: req?.id
  };
}
```

**Key data:**

- Use `type` as a stable URI-like identifier (don't fabricate a public URL unless it exists).
- Put machine-readable `code` in the body; put status in the HTTP status line.
- Never put `stack` or `cause` in the client response.

## Testing the adapters

| Case | Input | Expected |
| ---- | ----- | -------- |
| Zod validation fails | `ZodError` with one issue | `422`, `code: VALIDATION_ERROR`, `errors[]` has path |
| Prisma duplicate | `P2002` | `409`, `code: DUPLICATE_RESOURCE` |
| Deadlock | `P2034` | `409`, `code: CONCURRENCY_CONFLICT`, `retryable: true` |
| Fastify schema error | `err.validation` present | Normalized to `VALIDATION_ERROR` |
| Unknown error | `new Error('db crashed')` | `500`, `code: INTERNAL_ERROR`, no stack |
| Headers sent (Express) | Error after `res.json()` | Delegated to `next(err)`, no double response |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate ORM errors in repositories | Let Prisma exceptions reach Express middleware unhandled |
| Normalize validation at the boundary (pipe/middleware/schema) | Return raw validation objects |
| Fail fast in `bootstrap().catch()` | Catch startup errors in request middleware |
| Guard against `headersSent` in Express | Write to the response after headers sent |
| Keep adapters thin and core framework-free | Duplicate the registry in each adapter |

## Checklist

- [ ] Does the Express adapter use a 4-arg error middleware last in the chain?
- [ ] Does Fastify normalize both `err.validation` and other errors?
- [ ] Does NestJS use a global filter and fail-fast bootstrap?
- [ ] Are Prisma errors translated in the repository to `AppError`?
- [ ] Is the RFC 9457 shape consistent across all three adapters?
- [ ] Does the core have zero framework imports?

## Related

- [Framework Hierarchies and Handlers](../01-concepts/01-framework-hierarchies-and-handlers.md)
- [Dependency Injection, ORM, and Validation Mapping](../01-concepts/02-dependency-injection-orm-and-validation-mapping.md)
- [Custom vs Built-in Handler Conflicts](../02-deep-dive/01-custom-vs-built-in-handler-conflicts.md)
- [Framework-Independent Policy and Adapters](../01-concepts/03-framework-independent-policy-and-adapters.md)
- [Chapter 47 — Type-Safe Handling and the Common Architecture](../../47-language-level-error-semantics/02-deep-dive/02-type-safe-handling-and-common-architecture.md)
