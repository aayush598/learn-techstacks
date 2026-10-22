# Shared Error Code Enum (TypeScript) — Full Stack

> Part XIV · Chapter 38 · Section 38.2 · _Estimated reading time: 16 min_
> **Prerequisite:** [Shared Error-Code Enum (Ch37)](../../37-frontend-error-handling/03-practical-examples/03-shared-error-code-enum-frontend-backend.md), [Aligning Taxonomies](../01-concepts/01-aligning-taxonomies-shared-codes.md)

## In one sentence

**Create a versioned shared errors package** with `ErrorCode` enum, type guards, Problem Details types, and usage examples for backend and frontend.

## Package structure

```text
packages/errors/
├── src/
│   ├── codes.ts
│   ├── types.ts
│   ├── guards.ts
│   └── index.ts
├── package.json
└── tsconfig.json
```

## Implementation

```ts
// src/codes.ts
export enum ErrorCode {
  // Validation
  VALIDATION_FAILED = 'VALIDATION_FAILED',
  REQUIRED = 'REQUIRED',
  INVALID_FORMAT = 'INVALID_FORMAT',
  EMAIL_TAKEN = 'EMAIL_TAKEN',
  SLUG_TAKEN = 'SLUG_TAKEN',
  SLUG_INVALID = 'SLUG_INVALID',
  // Auth
  UNAUTHENTICATED = 'UNAUTHENTICATED',
  UNAUTHORIZED = 'UNAUTHORIZED',
  SESSION_EXPIRED = 'SESSION_EXPIRED',
  // Business
  CONFLICT = 'CONFLICT',
  SEAT_LIMIT_EXCEEDED = 'SEAT_LIMIT_EXCEEDED',
  DOMAIN_NOT_ALLOWED = 'DOMAIN_NOT_ALLOWED',
  PAYMENT_DECLINED = 'PAYMENT_DECLINED',
  RATE_LIMITED = 'RATE_LIMITED',
  // System
  INTERNAL_ERROR = 'INTERNAL_ERROR',
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  UNKNOWN = 'UNKNOWN',
}

export const ERROR_CODE_SET = new Set<string>(Object.values(ErrorCode));
```

```ts
// src/guards.ts
import { ErrorCode, ERROR_CODE_SET } from './codes';

export function isErrorCode(x: unknown): x is ErrorCode {
  return typeof x === 'string' && ERROR_CODE_SET.has(x);
}

export function asErrorCode(x: unknown, fallback: ErrorCode = ErrorCode.UNKNOWN): ErrorCode {
  return isErrorCode(x) ? x : fallback;
}
```

```ts
// src/types.ts
export interface InvalidParam {
  field?: string;
  code?: string | ErrorCode;
  message?: string;
  value?: unknown;
}

export interface ProblemDetails {
  type?: string;
  title?: string;
  status?: number;
  detail?: string;
  instance?: string;
  error_id?: string;
  code?: string | ErrorCode;
  invalid_params?: InvalidParam[];
  traceId?: string;
  [key: string]: unknown;
}
```

```ts
// src/index.ts
export * from './codes';
export * from './types';
export * from './guards';
```

## Backend usage

```ts
import { ErrorCode, ProblemDetails } from '@acme/errors';

function problem(status: number, code: ErrorCode, detail: string, extra: Partial<ProblemDetails> = {}): ProblemDetails {
  return { status, code, detail, error_id: genId(), ...extra };
}

// In controller
if (taken) {
  res.status(422).json(problem(422, ErrorCode.SLUG_TAKEN, 'Slug taken', {
    invalid_params: [{ field: 'slug', code: ErrorCode.SLUG_TAKEN }]
  }));
}
```

## Frontend usage

```ts
import { ErrorCode, isErrorCode, ProblemDetails } from '@acme/errors';

function map(p: ProblemDetails) {
  const code = isErrorCode(p.code) ? p.code : ErrorCode.UNKNOWN;
  if (code === ErrorCode.SLUG_TAKEN) return { kind: 'field', field: 'slug' };
  // ...
}
```

## Real-world use case

**Checkout + Acme SaaS:** same package used by Node API, BFF, React web, React Native — eliminates drift.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Shared package | Type-safe, versioned | Build/publish setup | **Recommended default** |
| Copy/paste | No deps | Drift guaranteed | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Export types + guards | Export only enum |
| Version package (semver) | Break silently |
| Use in both FE/BE | Duplicate definitions |

## Checklist

- [ ] Package builds and exports correctly
- [ ] FE and BE import from same package
- [ ] Guards used for unknowns
- [ ] Versioning policy defined

## Related

- [Chapter 37 — Shared Enum Practical](../../37-frontend-error-handling/03-practical-examples/03-shared-error-code-enum-frontend-backend.md)
- [Aligning Taxonomies](../01-concepts/01-aligning-taxonomies-shared-codes.md)
