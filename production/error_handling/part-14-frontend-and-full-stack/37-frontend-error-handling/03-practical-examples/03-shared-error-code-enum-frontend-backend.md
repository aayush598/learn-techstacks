# Shared Error-Code Enum Across Frontend/Backend

> Part XIV · Chapter 37 (cross-ref 38.2) · _Estimated reading time: 16 min_
> **Prerequisite:** [API Error → Form Field Mapping](./02-api-error-to-form-field-mapping.md), [Full-Stack Contracts — Shared Codes](../../38-full-stack-error-contracts/01-concepts/01-aligning-taxonomies-shared-codes.md)

## In one sentence

**Share a single source of truth for error codes (enum + types) across frontend and backend** so mapping is type-safe, unknown codes are detected, and contracts don't drift.

## Real-world use case

**Acme SaaS** needs consistent codes across services: `SLUG_TAKEN`, `EMAIL_TAKEN`, `SEAT_LIMIT_EXCEEDED`, `RATE_LIMITED`. Frontend maps codes to fields/UI actions; backend returns them in Problem Details. Shared types prevent typos.

## Key data / numbers

| Item | Guidance |
| --- | -------- |
| **Stability** | Codes are part of public contract; never rename without versioning/deprecation |
| **Namespacing** | Use uppercase snake_case, domain-scoped when large |
| **Extensibility** | Allow `UNKNOWN` fallback + `error_id` for unrecognized |
| **Sharing** | Monorepo package (`packages/errors`) or published internal package |

## Shared types (TypeScript)

```ts
// packages/errors/src/codes.ts
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
  RATE_LIMITED = 'RATE_LIMITED',
  // System
  INTERNAL_ERROR = 'INTERNAL_ERROR',
  SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE',
  UNKNOWN = 'UNKNOWN',
}

export const ErrorCodeValues = Object.values(ErrorCode) as string[];

export function isErrorCode(x: unknown): x is ErrorCode {
  return typeof x === 'string' && (ErrorCodeValues as string[]).includes(x);
}
```

```ts
// packages/errors/src/types.ts
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
  [key: string]: unknown;
}
```

## Backend usage (example)

```ts
// services/api/src/errors.ts
import { ErrorCode } from '@acme/errors';

export class AppError extends Error {
  constructor(
    public code: ErrorCode,
    public status: number,
    public detail?: string,
    public invalidParams?: Array<{field?:string; code: ErrorCode; message?:string}>
  ) {
    super(detail || code);
  }
}

// handler
if (slugTaken) {
  throw new AppError(ErrorCode.SLUG_TAKEN, 422, 'Slug already taken', [
    { field: 'slug', code: ErrorCode.SLUG_TAKEN, message: 'This slug is already taken.' }
  ]);
}
```

## Frontend usage

```ts
import { ErrorCode, isErrorCode } from '@acme/errors';

function mapCodeToAction(code?: string) {
  if (!isErrorCode(code)) return { type: 'fallback', message: 'Something went wrong.' };
  switch (code) {
    case ErrorCode.SLUG_TAKEN: return { type: 'field', field: 'slug' };
    case ErrorCode.SEAT_LIMIT_EXCEEDED: return { type: 'cta', cta: 'upgrade' };
    case ErrorCode.RATE_LIMITED: return { type: 'retry-after' };
    case ErrorCode.SESSION_EXPIRED: return { type: 'auth-refresh' };
    default: return { type: 'fallback' };
  }
}
```

## Governance notes

| Practice | Guidance |
| -------- | -------- |
| **Ownership** | Errors working group owns enum; changes reviewed |
| **Versioning** | Additive only in minor; breaking changes need new API version or deprecation window |
| **Documentation** | Each code documented with meaning, status, UI action, retryable? |
| **Tests** | Contract tests ensure backend doesn't emit unknown codes |
| **Deprecation** | Mark deprecated, keep for N releases, log usage |

## Real-world use case recap

**Checkout + Acme SaaS:** shared codes let the same mapping layer handle org creation and checkout validation; unknown codes go to safe fallback with `error_id` for support.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Ad-hoc strings | Fast | Typos, drift, no type safety | Never long-term |
| Shared enum | Type-safe, discoverable | Coupling across repos/packages | **Recommended default** |
| String union per service | Decentralized | Duplication/drift | Only if truly isolated |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Share via internal package/monorepo | Duplicate enum definitions |
| Use `isErrorCode` guard for unknown | Assume API always sends known codes |
| Treat codes as contract (version on break) | Rename codes arbitrarily |
| Log unknown codes with `error_id` | Crash on unknown code |

## Common mistakes

- **Frontend-only codes.** Backend must use same source.
- **Leaking internal codes.** Only expose stable contract codes.
- **No fallback.** Old clients hit unknown codes.

## Checklist

- [ ] Single source of truth for ErrorCode enum.
- [ ] Shared types exported for FE/BE.
- [ ] Type guards for unknown codes.
- [ ] Governance: review process for new codes.
- [ ] Contract tests prevent drift.

## Related

- [Full-Stack — Aligning Taxonomies and Shared Codes](../../38-full-stack-error-contracts/01-concepts/01-aligning-taxonomies-shared-codes.md)
- [API Error → Form Field Mapping](./02-api-error-to-form-field-mapping.md)
- [End-to-End Error Contract (Reference)](../../38-full-stack-error-contracts/05-reference/README.md)
