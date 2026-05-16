# API Routes

GuardrailZ uses Next.js App Router API routes (`/app/api/`) for its REST API. Each route is a server-side endpoint.

---

## 1. POST `/api/validate`

**Main endpoint** — validates text against a guardrail profile.

### Request
```http
POST /api/validate
Content-Type: application/json
x-api-key: grd_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

```json
{
  "text": "User input or model output to validate",
  "profileName": "default",
  "validationType": "input"
}
```

### Response (200)
```json
{
  "passed": true,
  "profile": { "id": "builtin:default", "name": "default" },
  "validationType": "input",
  "results": [
    {
      "passed": true,
      "guardrailName": "InputSize",
      "action": "ALLOW",
      "severity": "info",
      "message": "Input size within acceptable limits",
      "metadata": { "charCount": 42, "byteCount": 42, "maxChars": 50000, "maxBytes": 200000 }
    }
  ],
  "summary": { "total": 1, "passed": 1, "failed": 0 },
  "executionTimeMs": 5,
  "rateLimits": {
    "perMinute": { "current": 1, "max": 100 },
    "perDay": { "current": 1, "max": 10000 }
  }
}
```

### Error Responses
- `401`: Missing API key
- `400`: Validation error (invalid input, invalid API key, rate limited, profile not found)

### Flow
1. Extract `x-api-key` header
2. Zod-validate request body (text required, profileName required, validationType defaults to 'input')
3. `validateRequest()` performs: API key auth → rate limit check → profile resolution → guardrail execution → DB logging
4. Return results

### File: `app/api/validate/route.ts`
```typescript
export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';
```

---

## 2. GET `/api/profiles`

**List all profiles** for the authenticated user.

### Request
```http
GET /api/profiles
Authorization: Bearer <clerk_session>
```

### Response (200)
```json
{
  "profiles": [
    { "id": "...", "name": "default", "input": [...], "output": [...], "tool": [...], "all": [...] }
  ]
}
```

### Flow
1. `requireAuth()` → Clerk auth
2. `ensureBuiltIns()` — creates built-in profiles on first access
3. `getRuntimeProfiles()` — returns compiled RuntimeProfile array

---

## 3. POST `/api/profiles`

**Create a custom profile**.

### Request
```json
{
  "name": "my-custom-profile",
  "description": "My custom guardrails",
  "inputGuardrails": [{ "name": "InputSize", "config": { "maxChars": 10000 } }],
  "outputGuardrails": [],
  "toolGuardrails": []
}
```

### Response (200)
```json
{ "profile": { ... } }
```

---

## 4. GET `/api/keys`

**List all API keys** for the authenticated user.

### Response
```json
{
  "apiKeys": [
    {
      "id": "uuid",
      "key": "grd_live_...",
      "name": "Production Key",
      "isActive": true,
      "requestsPerMinute": 100,
      "requestsPerDay": 10000,
      "createdAt": "...",
      "lastUsedAt": null,
      "expiresAt": null
    }
  ]
}
```

---

## 5. POST `/api/keys`

**Create a new API key**.

### Request
```json
{
  "name": "Production Key",
  "requestsPerMinute": 100,
  "requestsPerDay": 10000
}
```

### Key Generation
```typescript
// Format: grd_live_ + 32-char nanoid
export function generateApiKey(): string {
  return `grd_live_${nanoid(32)}`;
}

export function validateApiKeyFormat(key: string): boolean {
  return /^grd_live_[a-zA-Z0-9_-]{32}$/.test(key);
}
```

---

## 6. DELETE `/api/keys/[id]`

**Delete an API key** by ID. Ensures ownership.

---

## 7. PATCH `/api/keys/[id]`

**Update an API key** (name and/or isActive).

---

## 8. GET `/api/usage`

**Get overall usage stats** for the authenticated user.

### Response
```json
{
  "totalExecutions": 150,
  "last24Hours": 23,
  "passedExecutions": 145,
  "failedExecutions": 5
}
```

---

## 9. GET `/api/usage/keys`

**Get per-key usage** (minute and day rate limit tracking).

### Response
```json
{
  "perDay": { "uuid-1": 42 },
  "perMinute": { "uuid-1": 3 }
}
```

---

## 10. GET `/api/usage/keys/[id]`

**Detailed per-key analytics** — the most complex analytics endpoint.

### Returns
- `perMinute`: Request count per minute (last 60 min)
- `perHour`: Aggregated per hour (last 24h)
- `perDay`: Per day (last 7 days)
- `successFailure`: Pass/fail counts
- `latency`: P50, P95, P99 latency via PostgreSQL `percentile_cont`

### Uses PostgreSQL window functions
```sql
percentile_cont(0.5) within group (order by execution_time_ms)
```

---

## 11. GET `/api/analytics`

**Dashboard analytics** with time range filtering.

### Query Params
- `range`: `24h` | `7d` (default) | `30d` | `90d`

### Response
```json
{
  "overview": {
    "totalExecutions": 150,
    "totalPassed": 145,
    "totalFailed": 5,
    "avgExecutionTime": 12,
    "successRate": 96.67,
    "changeFromLastPeriod": null
  },
  "guardrailStats": [...]
}
```

---

## 12. GET `/api/dashboard/stats`

**Dashboard overview stats** (simplified).

### Response
```json
{
  "totalExecutions": 150,
  "last24Hours": 23,
  "last7Days": 89,
  "passedExecutions": 145,
  "failedExecutions": 5,
  "avgExecutionTime": 12
}
```

---

## 13. GET `/api/guardrails/catalog`

**List all registered guardrail names**.

### Response
```json
{
  "guardrails": [
    { "name": "InputSize" },
    { "name": "SecretsInInput" },
    ...
  ]
}
```

Used by the frontend to show available guardrails when creating profiles.

---

## 14. POST `/api/payments/create-order`

**Create a Razorpay payment order** for plan upgrades.

### Request
```json
{ "plan": "pro", "amount": 999 }
```

---

## 15. POST `/api/payments/verify`

**Verify Razorpay payment signature** and upgrade user plan.

---

## Middleware (`middleware.ts`)

Protects routes using Clerk:

```typescript
const isPublicRoute = createRouteMatcher([
  '/', '/docs(.*)', '/hub(.*)', '/pricing(.*)', '/blogs(.*)',
  '/profiles(.*)', '/guardrails(.*)', '/sign-in(.*)', '/sign-up(.*)',
  '/api/validate(.*)', '/sitemap.xml', '/robots.txt',
]);
```

- Public routes → pass through
- All other routes → `auth.protect()` required
- Dashboard, analytics, profiles, keys, settings are all protected
