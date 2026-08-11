# Priority 2 — API Design (Q386–Q399)

**Why these matter for micro1:** you'll build/improve the Zara AI recruiter APIs. Expect REST design principles, idempotency, pagination, versioning, consistent errors, rate limiting, auth, and **streaming LLM responses** (a very likely question).

---

## Q386: What makes a good REST API?

1. **Resources, not actions** — nouns + HTTP verbs (`POST /applications`, not `/apply`).
2. **Consistent naming** — plural resources, lowercase kebab-case paths.
3. **Correct status codes** — 200/201/204, 400/401/403/404/409/422, 500/503 (Q54).
4. **Consistent error format** — an envelope `{error, message, details, request_id}` everywhere (Q77, Q392).
5. **Idempotency** where it matters (POST with idempotency keys) (Q387–397).
6. **Pagination** on all list endpoints (Q389).
7. **Versioning** strategy (Q391).
8. **Filtering/sorting** via query params (Q75).
9. **Security** — auth (JWT/OAuth), rate limiting, input validation, no secrets (Q394–395, Q400+).
10. **Documentation** — OpenAPI (FastAPI gives this free).
11. **Backward compatibility** — additive changes by default.
12. **Performance** — response models, caching headers, streaming for large payloads (Q247, Q399).

---

## Q387: What is idempotency?

**Performing the same operation multiple times has the same effect as performing it once** — duplicate requests don't create duplicate side effects.

- `GET`, `PUT`, `DELETE` are naturally idempotent.
- `POST` is *not* — retrying can create duplicate resources → use an **idempotency key** (Q397).

Example: client sends `POST /payments` with `Idempotency-Key: k-123`; the server, on retry, returns the **original response** instead of charging twice.

**Why it matters:** retries are inevitable (timeouts, network). Idempotency makes retries safe.

---

## Q388: Which HTTP methods are idempotent?

- **Idempotent:** `GET`, `HEAD`, `PUT`, `DELETE`, `OPTIONS`, `TRACE`.
- **Not idempotent:** `POST`, `PATCH` (PATCH *can* be idempotent by design if it sets absolute values, but it isn't guaranteed).

```text
PUT /users/1  {name:"Ada"}      → same result each time (idempotent)
POST /applications {...}        → creates a new one each time (not idempotent)
DELETE /users/1                 → after first delete, 404 — but "no user" is the same end state (idempotent)
```

- **Safe** (no side effects): GET/HEAD/OPTIONS. Idempotent ≠ safe.

---

## Q389: How would you design pagination?

```json
GET /api/v1/applications?cursor=eyJpZCI6MTAwfQ&limit=50

{
  "items": [...],
  "next_cursor": "eyJpZCI6MTUwfQ",
  "has_more": true,
  "limit": 50
}
```

- **Cursor (keyset) pagination** (recommended, Q390): encode `WHERE (id) > last_id ORDER BY id` into an opaque cursor.
- Envelope: `items` + `next_cursor` + `has_more` (+ optional `total` for admin UIs).
- Cap `limit` (e.g., 1–100), default ~50.
- Offsets are fine for small/admin datasets (Q256–257).

---

## Q390: Offset vs cursor pagination?

(Also Q257.) Key tradeoffs:

| | **Offset** `?page=2&limit=50` | **Cursor** `?cursor=...` |
|---|---|---|
| Cost | O(offset) — slow deep pages | O(page) — constant |
| Stability | Skips/dupes if rows change mid-paging | Stable (forward-only) |
| Random jump to page N | Yes | No |
| Total count | Trivial | Extra query |
| Best for | Small/admin tables | Feeds, chat history, big lists |

**Recommendation:** cursor by default for production lists; offset when you need "page 5" UI on small datasets.

---

## Q391: How would you design API versioning?

(Also Q76.) Pick one primary strategy:

1. **URL versioning** — `/api/v1/applications`. Explicit, cache-friendly, simple. **Most common.**
2. **Header/content negotiation** — `Accept: application/vnd.zara.v2+json`. Cleaner URLs, more complex clients.
3. **Query param** — `?version=2`. Simplest but pollutes caches/URLs.

**Best practice:**
- Version the **path prefix** (`/api/v1`), keep multiple versions deployed.
- **Additive changes first** — adding fields/endpoints usually needs no new version.
- Deprecate with a timeline: `Deprecation` header + sunset date, then remove.
- Never break old versions without a migration plan; keep old ones alive during the deprecation window.

---

## Q392: How would you design consistent error responses?

**One envelope everywhere (Q77):**

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request body",
    "details": [{"field": "email", "reason": "must be a valid email"}],
    "request_id": "req_abc123"
  }
}
```

**Implementation (FastAPI):**
- A base `AppError(status, code, message)` raised anywhere; one `@app.exception_handler(AppError)` renders the envelope.
- Map Pydantic `RequestValidationError` → 422 with the same shape.
- Add `request_id` via middleware (Q65) so errors link to logs.
- Use stable **machine-readable codes** (`candidate_not_found`, `rate_limited`) so clients branch on codes, not messages.
- Document codes in OpenAPI (`responses={...}`).

---

## Q393: How would you handle API rate limiting?

1. **Where:** edge (nginx/API Gateway/WAF), app-level middleware, or both.
2. **Algorithm:** token bucket (burst + steady) or sliding window; per-user, per-IP, per-API-key.
3. **Redis-based** (distributed, works across instances):

```python
# fixed window via INCR + EXPIRE
key = f"rl:{user_id}:{window_start}"
count = await redis.incr(key)
if count == 1: await redis.expire(key, window_seconds)
if count > limit: raise HTTPException(429, "rate limit exceeded")
```

4. **Return headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`; 429 + `Retry-After`.
5. **Different tiers:** anonymous vs authenticated; read vs write; LLM endpoints stricter (they cost money) (Q272).
6. **Respect the 429** downstream (LLM providers) too (Q270).
7. **Monitor:** who's hitting limits, abuse patterns, quota per user (Q631).

---

## Q394: How would you design authentication?

(Details in Q408–413.) **High-level design:**

1. **Pick the scheme:**
   - First-party web app → **JWT access token (short TTL) + refresh token (HTTP-only cookie)** (Q408–411).
   - Third-party/social login → **OAuth2/OIDC** (Google, LinkedIn for candidates) (Q412).
   - Internal services → API keys or signed requests.
2. **Flow:** `POST /auth/login` (username/password or OAuth) → issue tokens → client sends `Authorization: Bearer <access>` → FastAPI dependency verifies + injects user (Q62).
3. **Storage:** password hashing (**argon2id/bcrypt** — never plaintext) (Q414); refresh tokens stored hashed server-side (revocable).
4. **Security:** short-lived access tokens, rotation for refresh, HTTP-only/Secure/SameSite cookies, CSRF protection for cookie-based auth (Q404–405), rate limited login, lockout on repeated failures, MFA option.
5. **Authorization (roles/permissions)** enforced separately per route (Q395).

---

## Q395: How would you design authorization?

**RBAC (role-based) + permission checks at the route level:**

```python
def require_permission(perm: str):
    def dep(user: User = Depends(get_current_user)):
        if not user.has_permission(perm):
            raise HTTPException(403, "Forbidden")
        return user
    return dep

@router.get("/candidates", dependencies=[Depends(require_permission("view_candidates"))])
def list_candidates(...): ...
```

- **RBAC** — roles → permissions (simple, most apps).
- **ABAC** — attribute/policy-based for fine-grained rules ("recruiter can view candidates in *their* team").
- **Ownership checks:** a candidate can only see their own applications: `WHERE application.candidate_id == current_user.id`.
- **Principle of least privilege**; deny by default; test every permission path.
- Centralize in a dependency (Q60) so it's consistent and auditable.

---

## Q396: How would you prevent duplicate requests?

1. **Idempotency keys** for non-idempotent endpoints (POST) (Q397).
2. **Database unique constraints** as the final guarantee: `UNIQUE(candidate_id, job_id)` prevents duplicate applications even if the app layer races (Q156).
3. **Optimistic/pessimistic locking** for read-modify-write (Q553–555).
4. **Single-flight / locks** for expensive one-shot ops (distributed lock via Redis).
5. **Debounce** frontend double-clicks (disable submit button on submit).
6. **De-dup webhooks/events** by event id (`UNIQUE(event_id)` + `ON CONFLICT DO NOTHING`).

**Answer:** "Idempotency keys at the API layer + unique constraints at the DB layer = duplicate requests can't create duplicate state, even under retries and concurrency."

---

## Q397: What is an idempotency key?

A **client-supplied unique token** sent with a request so the server can recognize retries and return the **original result** instead of re-executing.

```http
POST /api/v1/applications
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

```python
# store key → cached result with a short TTL (e.g., 24h)
key = f"idem:{idempotency_key}"
cached = await redis.get(key)
if cached:
    return json.loads(cached)          # return original response
resp = await create_application(...)   # do the real work once
await redis.set(key, resp.json(), ex=86400)
return resp
```

**Rules of thumb:**
- Generate a UUID **client-side**, one key per intent (don't reuse across different requests).
- Return the stored response on replay, including the same status code.
- Key expires after a day or so; after expiry a new request creates new state.
- Great for: payments, applications, job posts — anything with side effects behind retries.

---

## Q398: How do you handle API timeouts and retries?

**Timeouts (design them explicitly):**
- **Client:** connect timeout + read timeout (e.g., httpx: 10s connect, 30s read); longer for LLM/streaming calls.
- **Server:** per-endpoint time budgets; FastAPI routes for LLM work should be **streaming** (Q399) so a long generation doesn't tie up a worker or time out the proxy.
- Short timeouts on cheap endpoints → fast failure, users retry sooner.

**Retries (do them safely):**
1. **Only retry idempotent requests** or requests with idempotency keys (Q387, Q397).
2. **Exponential backoff + jitter** — 100ms → 200ms → 400ms… + random ±; cap at ~5–8s.
3. **Retry budget** — e.g., 3–5 attempts max; honor `Retry-After` on 429/503.
4. **Circuit breaker** — after N consecutive failures, fail fast for a cooldown window instead of hammering a dead service (Q363, Q614).
5. **Don't retry 4xx** (except 408/429) — retry 5xx, network errors, timeouts.

---

## Q399: How would you stream an LLM response from your API?

**Why:** full JSON responses from an LLM take seconds to minutes; a user staring at a spinner will leave. Streaming shows tokens as they arrive (like ChatGPT/Zara chat).

**Pattern (SSE, Server-Sent Events):**
```python
from fastapi.responses import StreamingResponse

async def stream_screening(job, candidate):
    async with httpx.AsyncClient(timeout=httpx.Timeout(120)) as client:
        async with client.stream("POST", openai_url,
                                 json={"model": "gpt-4o", "stream": True,
                                       "messages": [...], "max_tokens": 1024}) as r:
            async for line in r.aiter_lines():
                # SSE data: ...
                yield f"data: {line}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/api/v1/screen/stream")
async def screen(job: JobIn, user=Depends(get_current_user)):
    return StreamingResponse(stream_screening(job, user),
                             media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
```

**Best practices:**
1. **SSE** (`text/event-stream`) for one-way server→client text; **WebSocket** if the client must send messages mid-conversation (chat) (Q348).
2. Set `Cache-Control: no-cache`; disable nginx buffering (`X-Accel-Buffering: no`).
3. Client parses `data:` lines, appends incrementally, stops at `[DONE]`.
4. Keep connection alive with heartbeat comments (`: ping`) so proxies don't cut idle connections.
5. Handle mid-stream client disconnects (`await request.is_disconnected()`) to stop token billing.
6. Timeout/backpressure: the client must be able to consume; buffer and flush, don't accumulate unbounded chunks.
7. For UI copy: keep a persistent WebSocket per session (Q349) and multiplex SSE frames over it.

**Answer structure (if asked):** "I'd return a StreamingResponse with content-type text/event-stream, stream chunks from the LLM provider as SSE data frames, disable proxy buffering, handle client disconnect to stop billing, and send heartbeats to keep the connection alive."
