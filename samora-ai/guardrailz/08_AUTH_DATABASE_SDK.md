# Authentication, Database & SDK

---

## A. Authentication (`shared/auth/`)

### Architecture (Strategy Pattern)

```
shared/auth/
├── domain/
│   ├── auth-user.ts       # AuthUser interface
│   ├── auth-session.ts    # AuthSession interface
│   └── auth-errors.ts     # UnauthorizedError
├── guards/
│   └── require-auth.ts    # requireAuth() function
├── providers/
│   ├── auth.provider.ts   # AuthProvider interface
│   └── clerk.provider.ts  # ClerkAuthProvider implementation
├── service/
│   ├── auth.service.ts    # AuthService
│   └── user-sync.service.ts # UserSyncService
└── index.ts               # Re-exports
```

### AuthProvider Interface
```typescript
export interface AuthProvider {
  getSession(): Promise<AuthSession | null>;
}
```

### ClerkAuthProvider
```typescript
export class ClerkAuthProvider implements AuthProvider {
  async getSession(): Promise<AuthSession | null> {
    const user = await currentUser();  // @clerk/nextjs/server
    if (!user) return null;
    return {
      user: {
        id: user.id,
        email: user.emailAddresses[0]?.emailAddress ?? '',
        firstName: user.firstName,
        lastName: user.lastName,
        imageUrl: user.imageUrl,
      },
      issuedAt: new Date(),
    };
  }
}
```

### AuthService
```typescript
class AuthService {
  async requireUser(): Promise<{ authUser: AuthUser; dbUser: User }>
  async getOptionalUser(): Promise<{ authUser: AuthUser; dbUser: User } | null>
}
```

`requireUser()`: Gets session → throws `UnauthorizedError` if null → syncs user to DB → returns both auth user and DB user.

### requireAuth() Guard
```typescript
export async function requireAuth() {
  const auth = new AuthService();
  try {
    return await auth.requireUser();
  } catch (err) {
    if (err instanceof UnauthorizedError) throw err;
    throw new UnauthorizedError();
  }
}
```

### User Sync
`UserSyncService.getOrCreate()`: If user doesn't exist in DB, creates a new record. Returns existing or new user.

### Design Rationale
The `AuthProvider` interface abstracts the auth mechanism. Currently only Clerk is implemented, but you could add Auth0, Firebase Auth, or any other provider by implementing the interface.

---

## B. Database (`shared/db/`)

### Stack
- **ORM**: Drizzle ORM
- **Driver**: postgres.js (serverless-compatible)
- **Database**: PostgreSQL

### DB Client (`client.ts`)
```typescript
const client = postgres(DATABASE_URL, { prepare: false, max: 10 });
export const db = drizzle(client, { schema, logger: process.env.NODE_ENV === 'development' });
```

Key settings:
- `prepare: false` — required for serverless/transaction poolers (PgBouncer)
- `max: 10` — max pool connections
- Logger enabled in development for query debugging

### Schema (8 tables)

**1. `users`**
```typescript
{ id: text PK, email: text UNIQUE, firstName?, lastName?, plan: text default 'free', createdAt, updatedAt }
```
Clerk user ID serves as primary key.

**2. `profiles`**
```typescript
{ id: uuid PK, userId FK→users, name, description?, isBuiltIn: boolean,
  inputGuardrails: jsonb, outputGuardrails: jsonb, toolGuardrails: jsonb, createdAt, updatedAt }
```
Guardrails stored as JSONB arrays of descriptors.

**3. `api_keys`**
```typescript
{ id: uuid PK, userId FK→users, key: text UNIQUE, name, isActive: boolean,
  requestsPerMinute: int default 100, requestsPerDay: int default 10000,
  createdAt, lastUsedAt?, expiresAt? }
```

**4. `guardrail_executions`**
```typescript
{ id: uuid PK, userId FK→users, apiKeyId FK→api_keys, profileId FK→profiles,
  inputText?, outputText?, guardrailResults: jsonb, passed: boolean,
  executionTimeMs: int, createdAt }
**Indexes**: (userId, createdAt), (userId, passed), (userId, profileId)
```

**5. `rate_limit_tracking`**
```typescript
{ id: uuid PK, apiKeyId FK→api_keys, userId FK→users,
  requestCount: int, windowStart: timestamp, windowType: varchar(10) }
```

**6. `user_rate_limits`**
```typescript
{ id: uuid PK, userId FK→users,
  requestsPerMinute: int default 500, requestsPerDay: int default 50000, createdAt }
```

**7. `analytics_events`**
```typescript
{ eventId: uuid PK, eventType: text, userId, apiKeyId?, profileId?,
  payload: jsonb, createdAt: timestamp with tz }
```

**8. `orders`**
```typescript
{ id: text PK, userId FK→users, razorpayOrderId, razorpayPaymentId?,
  razorpaySignature?, plan, amount: int, status: text default 'created', createdAt, updatedAt }
```

### Relations
Defined via Drizzle relations:
- `users` → has many `profiles`, `apiKeys`, `executions`, `orders`
- `profiles` → belongs to `user`
- `apiKeys` → belongs to `user`
- `orders` → belongs to `user`

---

## C. SDK (`sdk/`)

A standalone TypeScript SDK for integrating GuardrailZ into external applications.

### Structure
```
sdk/
├── core/
│   ├── client.ts        # GuardrailsClient
│   ├── config.ts        # SDK config
│   ├── error.ts         # SDK errors
│   └── http.ts          # HTTP transport
├── guardrails/
│   ├── index.ts
│   ├── types.ts         # Request/response types
│   └── validate.ts      # Validate method
├── index.ts             # Exports
├── package.json         # Separate package
├── tsup.config.ts       # Build config
└── README.md
```

### Usage
```typescript
import { GuardrailsClient } from '@guardrailz/sdk';

const client = new GuardrailsClient({
  baseUrl: 'https://api.guardrailz.com',
  apiKey: 'grd_live_...',
});

const result = await client.validate({
  text: 'User input to validate',
  profileName: 'default',
  validationType: 'input',
});
```

### Config
```typescript
interface GuardrailsSDKConfig {
  baseUrl: string;
  apiKey: string;
  timeoutMs?: number;    // default: 10,000
  retries?: number;      // default: 0
}
```

### Response Type
```typescript
interface ValidateResponse {
  passed: boolean;
  profile: { id: string; name: string };
  validationType: 'input' | 'output';
  results: Array<{
    guardrailName: string;
    passed: boolean;
    severity: string;
    action: string;
    message?: string;
    redactedText?: string;
    metadata?: Record<string, unknown>;
  }>;
  summary: {
    total: number;
    passed: number;
    failed: number;
  };
  executionTimeMs: number;
}
```

### Build
Uses `tsup` to bundle into ESM and CJS formats for maximum compatibility.

---

## D. Rate Limiting (`lib/rate-limit.ts`)

The rate limiter uses a **sliding window** approach with DB-backed counters.

### `checkRateLimit(apiKeyId, userId): RateLimitResult`

**Checks in order:**
1. **API key per-minute** limit (default: 100)
2. **API key per-day** limit (default: 10,000)
3. **User account per-minute** limit (default: 500)
4. **User account per-day** limit (default: 50,000)

### `incrementRateLimit(apiKeyId, userId, now)`
- Upserts `rate_limit_tracking` for minute and day windows
- Updates `api_keys.lastUsedAt`

### Window Buckets
```typescript
function utcMinuteBucket(date: Date): Date  // Truncate to minute
function utcDayBucket(date: Date): Date     // Truncate to day
```

### Design Rationale
- DB-backed (not in-memory) → survives restarts, works across multiple instances
- Upsert pattern (select + update/insert) to avoid race conditions
- Auto-creates default user limits on first check
- Returns detailed limit info in response headers
