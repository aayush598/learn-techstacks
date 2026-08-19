# TailorTalk — 100 Backend Interview Q&A

> Based on TailorTalk — Backend Development Internship (AI sales/support agents, LLMs)  > Candidate: Aayush Gid (Python/FastAPI/REST/DB/LLM guardrails background)

---

## 1. Python & OOP Fundamentals (Q1–Q12)

**Q1: What are the key differences between a list and a tuple in Python?**  
A: Lists are mutable (can be changed after creation) and use `[]`; tuples are immutable and use `()`. Tuples are slightly faster and hashable, so they're good for fixed collections and dict keys. For backend code, use tuples for fixed config and lists for dynamic collections.

**Q2: Explain Object-Oriented Programming and its four pillars.**  
A: OOP models software as objects with data (attributes) and behavior (methods). The four pillars are encapsulation (hiding internals), abstraction (exposing only needed interface), inheritance (reusing base classes), and polymorphism (same interface, different behavior). At TailorTalk this helps build maintainable service layers for agents.

**Q3: What are decorators in Python and where have you used them?**  
A: A decorator wraps a function to add behavior without modifying it.
```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```
I've used `@app.get()` in FastAPI and `@router.post()` extensively, plus custom decorators for auth checks.

**Q4: What do *args and **kwargs do?**  
A: `*args` collects positional arguments into a tuple; `**kwargs` collects keyword arguments into a dict. They let functions accept variable input, useful for wrapper/utility functions and forwarding params in service layers.

**Q5: What is the GIL and how does it affect multithreading in Python?**  
A: The Global Interpreter Lock allows only one thread to execute Python bytecode at a time, so CPU-bound multithreading doesn't truly parallelize. I/O-bound work (network/DB calls, common in backends) still benefits via `asyncio` or threading. For true CPU parallelism use multiprocessing or offload to workers.

**Q6: What is the difference between `==` and `is`?**  
A: `==` compares values; `is` compares object identity (memory location). Use `==` for equality and `is` only for singletons like `None` (`x is None`).

**Q7: Explain mutable default arguments pitfall.**  
A: Default args are evaluated once at function definition, so a mutable default (like a list) is shared across calls.
```python
def add(x, items=[]):  # bug
    items.append(x); return items
```
Use `items=None` then initialize inside the function.

**Q8: How do you define an interface or abstract class in Python?**  
A: Use the `abc` module with `@abstractmethod`.
```python
from abc import ABC, abstractmethod
class Agent(ABC):
    @abstractmethod
    def respond(self, msg): ...
```
This enforces a contract for different agent implementations — useful for pluggable LLM backends.

**Q9: What are context managers and why are they useful?**  
A: Context managers (`with`) guarantee setup/teardown (e.g., closing DB connections).
```python
with open("x.txt") as f: data = f.read()
```
FastAPI uses them for lifespan events and DB sessions, preventing resource leaks.

**Q10: What is the difference between a generator and a list comprehension?**  
A: A list comprehension builds the whole list in memory; a generator yields items lazily, one at a time, via `yield`. Generators are memory-efficient for large/streamed data — e.g., streaming LLM token responses.

**Q11: When would you prefer composition over inheritance?**  
A: Prefer composition (holding another object) when you want flexibility and to avoid tight coupling; inheritance suits "is-a" relationships. For scalable backend services, composition (e.g., injecting a `Cache` or `LLMClient` dependency) is usually safer than deep inheritance trees.

**Q12: How would you structure a FastAPI project using OOP principles?**  
A: Separate concerns: `models/` (Pydantic + ORM), `schemas/`, `services/` (business logic as classes), `routers/` (HTTP layer), `repositories/` (DB access). Inject dependencies (DB session, cache, clients) rather than hardcoding, keeping the API layer thin and logic testable.

---

## 2. FastAPI & RESTful API Design (Q13–Q28)

**Q13: Why would you choose FastAPI over Flask for TailorTalk's backend?**  
A: FastAPI gives async support, automatic OpenAPI docs, Pydantic-based validation, and strong typing — ideal for high-throughput LLM agent endpoints. Flask is simpler but lacks built-in async and validation, which slows development of a typed, documented API.

**Q14: When should an endpoint be `async def` vs `def` in FastAPI?**  
A: Use `async def` for I/O-bound work (DB calls, HTTP to LLMs, Redis) so the event loop handles concurrency. Use plain `def` only for CPU-bound or blocking code, which FastAPI runs in a threadpool. Mixing correctly avoids blocking the event loop.

**Q15: What is the role of Pydantic in FastAPI?**  
A: Pydantic models validate and serialize request/response data with type hints, auto-generating docs and catching bad input early. They replace manual validation and make contracts explicit between the agent backend and clients.

**Q16: What is the difference between a path parameter and a query parameter?**  
A: Path params (`/agents/{id}`) identify a resource and are required; query params (`/agents?status=active`) are optional filters. FastAPI distinguishes them by declaration: `id: int` in the path vs `status: str = None` in the function signature.

**Q17: What HTTP status codes should a REST API return for common cases?**  
A: `200` OK, `201` created, `204` no content, `400` bad request, `401` unauthorized, `403` forbidden, `404` not found, `409` conflict, `422` validation error (FastAPI default), `429` too many requests, `500` server error.

**Q18: What does idempotency mean and why is it important for APIs?**  
A: An idempotent operation produces the same result no matter how many times it's repeated (e.g., `GET`, `PUT`). It matters for retries in unreliable networks — a retried payment or agent action shouldn't double-execute.

**Q19: What is the difference between PUT and PATCH?**  
A: `PUT` replaces the entire resource; `PATCH` partially updates it. For an agent config, `PATCH /agents/{id}` to change just the prompt is safer than resending the whole object.

**Q20: How does FastAPI's dependency injection work?**  
A: You declare dependencies as function params (e.g., `db: Session = Depends(get_db)`). FastAPI resolves and injects them, enabling reusable auth, DB sessions, and caching without global state — great for clean service composition.

**Q21: How do you handle errors and exceptions in FastAPI?**  
A: Use `HTTPException` for expected errors and register exception handlers via `@app.exception_handler`. Centralize validation/domain errors so clients get consistent JSON with proper status codes instead of stack traces.

**Q22: What are middlewares and a practical use case?**  
A: Middleware runs before/after every request. Use cases: CORS, request ID logging, auth checks, and timing. Example: a middleware that logs latency and injects correlation IDs for tracing agent calls.

**Q23: How would you version a REST API?**  
A: Common approaches: URL prefix (`/v1/agents`), header (`Accept: application/vnd.tailortalk.v1+json`), or subdomain. URL versioning is simplest and explicit; keep deprecated versions alive behind a redirect with a sunset header.

**Q24: How do you implement pagination for a list of conversations?**  
A: Use `limit`/`offset` or cursor-based keyset pagination.
```python
@app.get("/conversations")
def list_conv(limit: int = 20, cursor: str | None = None): ...
```
Cursor pagination scales better than offset for large, append-heavy chat tables.

**Q25: How would you design a REST endpoint for an LLM sales agent chat?**  
A: `POST /v1/conversations` to create, `POST /v1/conversations/{id}/messages` to send a message that triggers the agent, returning the reply (or a task id for async). Keep message history in the DB and stream tokens via SSE/WebSocket for UX.

**Q26: How would you implement rate limiting on a public API?**  
A: Use a token-bucket or sliding-window counter in Redis keyed by API key/IP, checking on each request and returning `429` with `Retry-After`. Libraries like `slowapi` integrate with FastAPI; this protects LLM cost and downstream services.

**Q27: How did you use FastAPI BackgroundTasks at Krip AI, and when are they appropriate?**  
A: BackgroundTasks run a function after the response is sent — good for sending emails or firing non-critical side effects. For heavier/long jobs (LLM batch runs), I'd use a real queue (Celery/RQ) instead, since BackgroundTasks share the process and aren't durable.

**Q28: How do you test a FastAPI app?**  
A: Use `TestClient` from `starlette`/`fastapi` with `pytest`.
```python
def test_create(client):
    r = client.post("/v1/agents", json={...})
    assert r.status_code == 201
```
Mock DB/cache/LLM dependencies via `monkeypatch` or DI overrides to keep tests fast and deterministic.

---

## 3. Databases: SQL vs NoSQL (Q29–Q42)

**Q29: When would you choose SQL over NoSQL and vice versa?**  
A: Choose SQL (PostgreSQL) when you need relational integrity, transactions, and complex queries (billing, users). Choose NoSQL (MongoDB) for flexible, schema-less, high-write workloads like raw event/chat logs. TailorTalk's core data is relational; chat logs can be document-based.

**Q30: What are the differences between PostgreSQL and MySQL?**  
A: PostgreSQL is more standards-compliant, supports richer types (JSONB, arrays), and advanced indexing; MySQL is historically faster for simple reads and widely used with PHP stacks. For an LLM backend, Postgres's JSONB and full-text/search features are a big plus.

**Q31: In what scenario is MongoDB a good fit for an agent backend?**  
A: Storing semi-structured conversation transcripts, tool-call logs, and experiment outputs where schema evolves rapidly. Embedding message arrays in one document avoids complex joins for a single conversation.

**Q32: How do database indexes work and why are they important?**  
A: Indexes (B-tree by default) let the DB find rows without a full scan, trading write/space cost for read speed. Index columns used in `WHERE`, `JOIN`, and `ORDER BY` (e.g., `conversations(user_id, created_at)`).

**Q33: What is the N+1 query problem and how do you avoid it?**  
A: Fetching a list then querying per-item (1 + N queries) instead of joining once. In SQLAlchemy use `joinedload`/`selectinload`; in raw SQL use a `JOIN`. It's a common performance killer when listing conversations with their messages.

**Q34: Explain ACID properties.**  
A: Atomicity (all-or-nothing), Consistency (valid state), Isolation (concurrent txns don't interfere), Durability (committed data survives crashes). Important for billing/usage records in a B2C product.

**Q35: What is normalization and when would you denormalize?**  
A: Normalization reduces redundancy/anomalies (1NF–3NF); denormalization duplicates data for read speed. Denormalize (e.g., cache last-message preview on a conversation row) when reads dominate and joins are costly.

**Q36: Explain different SQL JOIN types.**  
A: `INNER` (matching rows both sides), `LEFT` (all left + matched right, nulls otherwise), `RIGHT`, `FULL`, and `CROSS`. Most agent queries use `INNER`/`LEFT` to join users with conversations.

**Q37: What is connection pooling and why use it?**  
A: A pool reuses DB connections instead of opening/closing per request, cutting latency and preventing connection exhaustion. Configure `pool_size`/`max_overflow` in SQLAlchemy; critical under FastAPI's concurrency.

**Q38: What are the trade-offs between an ORM and raw SQL?**  
A: ORMs (SQLAlchemy) speed development and prevent injection but can generate inefficient queries and add abstraction overhead. Use ORM for CRUD and drop to optimized raw SQL/`text()` for analytics or hot paths.

**Q39: How would you model chat history in MongoDB?**  
A: One document per conversation with an embedded `messages` array, plus indexes on `userId` and `updatedAt`.
```json
{ "_id": "...", "userId": "u1", "messages": [ {"role":"user","text":"hi"} ] }
```
Cap message array growth or archive to a separate collection if very long.

**Q40: What are database migrations and how have you used them?**  
A: Migrations version-control schema changes so they're reproducible across environments. With FastAPI I use Alembic to generate/apply migrations; never alter prod schema manually. GuardrailZ and agent services rely on this for safe deploys.

**Q41: Why did you use SQLite at Clone Futura and when is it appropriate?**  
A: SQLite is serverless, zero-config, and fine for local dev, small single-user tools, or Google Drive automation scripts. Avoid it for concurrent production writes; switch to Postgres when multiple workers hit the DB.

**Q42: What is eventual consistency and where does it appear?**  
A: A system where replicas converge to the same state after some delay, common in distributed NoSQL and caches. You design for it by accepting slightly stale reads (e.g., analytics dashboards) while keeping critical paths strongly consistent.

---

## 4. Caching, Redis & Performance (Q43–Q54)

**Q43: What is Redis and what are its common use cases?**  
A: Redis is an in-memory key-value store used for caching, sessions, rate limiting, pub/sub, and queues. At Krip AI I used it to cache LLM responses and feature flags for low-latency agent serving.

**Q44: Explain the cache-aside (lazy loading) pattern.**  
A: App checks cache first; on miss, read DB, populate cache, then return.
```python
val = redis.get(key)
if not val:
    val = db.query(...); redis.set(key, val, ex=300)
```
Simple and resilient, but can serve stale data until TTL expires.

**Q45: What are common cache invalidation strategies?**  
A: Set a TTL (time-based), explicitly delete/update on writes, or use versioned keys. The hard part is consistency; I prefer write-through/delete plus TTL as a safety net to avoid stale agent configs.

**Q46: Name key Redis data structures and a use for each.**  
A: Strings (cache values, counters), Hashes (user/session objects), Lists (queues), Sets (unique tags), Sorted Sets (leaderboards, delayed jobs), Streams (event logs). Pick the structure matching access patterns.

**Q47: What is a TTL and why set one?**  
A: Time-to-live makes a key auto-expire, bounding memory and staleness. Essential so cached LLM outputs or auth tokens don't live forever.

**Q48: Why use Redis instead of an in-process dictionary for caching?**  
A: A dict is per-process and lost on restart; Redis is shared across workers/instances and persists optionally. For multi-worker FastAPI on ECS, a shared cache prevents duplicate LLM calls and inconsistent state.

**Q49: Describe how you used Redis caching at Krip AI.**  
A: I cached expensive LLM responses and intermediate agent state keyed by prompt/context hash with short TTLs, and used it for rate limiting and session lookups across ECS tasks — cutting p95 latency and LLM cost.

**Q50: What is the difference between write-through and write-back caching?**  
A: Write-through writes to cache and DB together (consistent, slower writes); write-back writes to cache first and flushes to DB later (fast, risk of loss). For correctness-critical data use write-through; for volatile metrics use write-back.

**Q51: What is a cache stampede / thundering herd and how do you prevent it?**  
A: Many requests miss the same key simultaneously and all hit the DB/LLM. Prevent with a single-flight lock, request coalescing, or serving slightly stale data while refreshing (lock-per-key via Redis `SET NX`).

**Q52: How can Redis Pub/Sub be used in an agent backend?**  
A: To broadcast events (new message, agent done) across workers, or coordinate real-time notifications to WebSocket clients. For durable queues prefer Redis Streams over Pub/Sub (no persistence).

**Q53: When should you NOT cache?**  
A: For highly personalized, never-repeated, or strongly consistency-critical data (e.g., a one-off payment confirmation). Caching there adds complexity and staleness risk with little benefit.

**Q54: How does Redis persist data (RDB vs AOF)?**  
A: RDB snapshots periodically (fast restart, some data loss); AOF logs every write (more durable, larger). You can combine both. For a cache, persistence is often optional; for session/state stores, enable AOF.

---

## 5. Authentication: JWT & OAuth (Q55–Q66)

**Q55: What is a JWT and what are its three parts?**  
A: A JSON Web Token has `header.payload.signature`, base64url-encoded. The payload holds claims (sub, exp, role); the signature (HMAC/RSA) proves integrity. It's stateless auth — no server session needed.

**Q56: How should a JWT be stored on the frontend?**  
A: Prefer HttpOnly, Secure, SameSite cookies to mitigate XSS token theft; avoid `localStorage` for tokens. In GuardrailZ with Clerk, auth is handled client-side with short-lived tokens and secure cookie/session flows.

**Q57: What are refresh tokens and why use them?**  
A: Short-lived access tokens plus longer-lived refresh tokens let you stay logged in securely. When the access token expires, the refresh token mints a new one; revoke the refresh token to log out everywhere.

**Q58: What is the difference between OAuth2 and JWT?**  
A: OAuth2 is an authorization framework (delegating access via tokens); JWT is a token format. OAuth2 often issues JWTs as access tokens. They solve different layers: delegation vs representation.

**Q59: What is the difference between authentication and authorization?**  
A: Authentication verifies who you are (login); authorization decides what you can do (roles/permissions). At Clone Futura I built API auth to identify callers and permission checks to restrict actions.

**Q60: Describe the OAuth2 authorization code flow.**  
A: User is redirected to the provider, logs in, gets a code, the backend exchanges it for tokens at the token endpoint, then calls APIs. With PKCE for public clients — this is how integrating Google Workspace (Drive) auth worked.

**Q61: How did you implement API authentication and permissions at Clone Futura?**  
A: FastAPI dependencies validated API keys/JWTs per request, with a permissions layer gating Google Drive operations by scope. Requests were scoped to the authenticated user so one tenant couldn't access another's files.

**Q62: How should passwords be stored?**  
A: Never plaintext — hash with a slow, salted function like bcrypt/argon2.
```python
from passlib.context import CryptContext
pwd = CryptContext(schemes=["bcrypt"]); hashed = pwd.hash("pw")
```
Verify with `pwd.verify` during login.

**Q63: What is the difference between XSS and CSRF, and how do you prevent each?**  
A: XSS injects scripts into pages (prevent by output encoding, CSP, HttpOnly cookies); CSRF forces authenticated requests from a victim (prevent with SameSite cookies, CSRF tokens, origin checks). Both matter for any user-facing agent dashboard.

**Q64: How do you manage secrets and API keys securely?**  
A: Keep them out of code/repo; use environment variables or a secrets manager (AWS Secrets Manager/Vault). In CI/CD, store as encrypted GitHub Actions secrets; never log them. Rotate on suspected leaks.

**Q65: What is Role-Based Access Control (RBAC)?**  
A: Users are assigned roles, roles have permissions, and the system enforces them. For TailorTalk: `admin` manages agents, `agent_user` only runs them. Implement via a middleware/dependency checking the token's role claim.

**Q66: Compare session-based vs token-based authentication.**  
A: Session auth stores state server-side (scales via shared store); token (JWT) is stateless and easy to scale across services but harder to revoke instantly. For a distributed microservice backend, JWT with short TTL + refresh is practical.

---

## 6. Docker, CI/CD & DevOps (Q67–Q78)

**Q67: What is Docker and the difference between an image and a container?**  
A: An image is an immutable blueprint (app + deps); a container is a running instance of that image. You build images and run many containers from one — core to packaging FastAPI services for ECS/Render.

**Q68: What are Dockerfile best practices you follow?**  
A: Use small base images (slim), multi-stage builds, pin versions, run as non-root, copy only needed files, and leverage layer caching.
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn","app:app","--host","0.0.0.0"]
```

**Q69: What is docker-compose used for?**  
A: It defines multi-container local environments (app + Postgres + Redis) in one file, so devs run the whole stack with `docker compose up`. Great for reproducing the agent backend locally.

**Q70: What is CI/CD and why does it matter?**  
A: Continuous Integration merges/tests code automatically; Continuous Deployment ships it to production. It catches bugs early and enables safe, frequent releases — exactly what I built with GitHub Actions at Krip AI.

**Q71: Describe a GitHub Actions workflow you built.**  
A: On push/PR: checkout, setup Python, install deps, run `pytest` + linter, build Docker image, push to registry, and deploy to ECS on main. Caching pip and image layers kept it fast; required checks blocked bad merges.

**Q72: How would you containerize a FastAPI app?**  
A: Write a Dockerfile (slim Python, install deps, copy code, run uvicorn), add a `healthcheck`, build/push the image, and run with env vars for DB/Redis/LLM keys. Expose the port and put it behind a load balancer on ECS/Render.

**Q73: What is the difference between COPY and ADD in a Dockerfile?**  
A: `COPY` copies local files only; `ADD` also supports URL fetches and auto-tar extraction. Prefer `COPY` for clarity; use `ADD` only when you need those extras.

**Q74: Why add a HEALTHCHECK to a container?**  
A: It lets the orchestrator detect and restart unhealthy containers. For FastAPI, point it at a `/health` endpoint that checks DB/Redis connectivity so bad deploys self-heal.

**Q75: How have you deployed with Render and Vercel?**  
A: Vercel for the Next.js frontends (GuardrailZ, video editor); Render for backend services/containers with automatic builds from Git. Both simplify CI/CD for small teams without managing full infra.

**Q76: How do you handle environment-specific configuration?**  
A: Use env vars loaded via `pydantic-settings` (e.g., `DATABASE_URL`, `REDIS_URL`, `OPENAI_API_KEY`) with `.env` for local and secrets for prod. Never hardcode config; keep a documented example `.env.example`.

**Q77: What logging and monitoring would you add to a backend?**  
A: Structured JSON logs with request IDs, plus metrics (latency, error rate, LLM cost) exported to a dashboard and alerts on anomalies. For a startup, lightweight options like basic CloudWatch + custom logs suffice early.

**Q78: How do you safely roll back a bad deployment?**  
A: Keep the previous image tagged and redeploy it, or use blue-green/canary releases. With ECS/Render, reverting to the last good image is quick; CI should gate deploys on tests to reduce rollback need.

---

## 7. System Design & Scalability (Q79–Q90)

**Q79: Design the backend for TailorTalk's LLM sales/support agent.**  
A: Components: API gateway/router (FastAPI), Auth service, Conversation/State store (Postgres + Redis cache), Agent orchestration service calling the LLM + tools, a message queue for async jobs, and a guardrails layer. Stateless API workers behind a load balancer; LLM calls wrapped with caching, retries, and timeouts.

**Q80: How would you scale a FastAPI service horizontally?**  
A: Run multiple stateless worker containers behind a load balancer, externalize state to Postgres/Redis, and make workers idempotent. Use Gunicorn+Uvicorn workers and autoscale on CPU/request metrics in ECS.

**Q81: Why and when would you introduce a message queue?**  
A: To decouple slow work (LLM generation, email, webhooks) from request handling, smooth spikes, and add durability/retries. Use Redis Streams, SQS, or RabbitMQ when agent tasks exceed acceptable request latency.

**Q82: How do you handle LLM rate limits, timeouts, and failures?**  
A: Wrap calls with exponential backoff + jitter, circuit breakers, request concurrency limits, and caching of repeated prompts. Fail gracefully with a fallback message and queue the job for retry instead of 500-ing the user.

**Q83: How would webhooks be used for a B2C support agent?**  
A: Inbound channels (e.g., a store's form or WhatsApp) POST events to `/webhooks`; verify signatures, enqueue, and let the agent respond asynchronously. Outbound webhooks notify the client's systems of resolved tickets.

**Q84: How do read replicas help and what are the trade-offs?**  
A: They offload read traffic (analytics, history listing) from the primary, improving scale. Trade-off: replication lag can serve stale data; keep writes and strongly-consistent reads on the primary.

**Q85: How do you design for concurrency safety in the backend?**  
A: Use DB transactions with appropriate isolation, optimistic locking (`version` columns) for updates, and atomic Redis operations for counters. Avoid shared mutable global state in async workers.

**Q86: What is load balancing and which strategies fit an API?**  
A: Distributing traffic across instances via round-robin, least-connections, or latency-based routing. Put it in front of FastAPI workers; combine with health checks so unhealthy nodes stop receiving traffic.

**Q87: How would you reduce LLM API costs?**  
A: Cache repeated prompts/responses, use smaller models for simple classification, compress/summarize conversation history, batch where possible, and set token/timeout budgets per request. Monitor cost per conversation.

**Q88: How would you design conversation memory/state for an agent?**  
A: Store full history in Postgres (durable) and keep recent context in Redis for fast access; trim/prompt-compress older turns before sending to the LLM. Support multi-session state keyed by conversation + user.

**Q89: Explain the CAP theorem.**  
A: A distributed system can't simultaneously guarantee Consistency, Availability, and Partition tolerance; under a network partition you trade C or A. For agent metadata pick CP (consistency); for ephemeral presence, AP is fine.

**Q90: How would you make the system observable?**  
A: Emit structured logs, metrics (RED: rate, errors, duration), and distributed traces across API→agent→LLM calls. Add alerting on error spikes and cost anomalies so a small team catches issues fast.

---

## 8. LLM Agents, Guardrails & Security (Q91–Q100)

**Q91: What are LLM guardrails and how did you build them in GuardrailZ?**  
A: Guardrails are checks that sit around model input/output to enforce safety and correctness. In GuardrailZ I implemented 50+ regex/rule-based guardrails: prompt-injection detection, PII/PHI detection, redaction, and output validation, as a modular TypeScript layer with Clerk auth.

**Q92: What is prompt injection and how would you defend against it?**  
A: An attacker manipulates the model via untrusted input (e.g., "ignore previous instructions"). Defenses: separate system instructions from user input, strict input validation, detect injection patterns (like GuardrailZ), constrain tool use, and validate outputs before acting.

**Q93: How do you detect and redact PII/PHI in agent traffic?**  
A: Use regex/ML detectors for emails, phones, SSNs, medical terms, then redact or tokenize before sending to logs/LLM. In GuardrailZ this runs as a preprocessing step; never log raw PII and prefer masking with reversible tokens when the system needs it.

**Q94: Explain the SSRF protection you contributed to Sim Studio.**  
A: SSRF lets an attacker make the server fetch internal/localhost URLs. My fix validated URLs, blocked loopback/link-local ranges (127.0.0.0/8, ::1, 169.254.0.0/16), resolved DNS and re-checked the IP, and added tests. This prevents agents from reaching cloud metadata or internal services.

**Q95: How would you validate LLM output before using it?**  
A: Enforce a schema (e.g., JSON via function-calling/Pydantic), run content guardrails (toxicity, injection, PII), and verify any tool calls against an allowlist. Reject and retry on validation failure rather than blindly executing actions.

**Q96: How would you build a sales agent that calls external tools?**  
A: Define a tool registry with typed schemas, let the LLM emit tool calls, validate them against an allowlist, execute via a sandboxed service, and feed results back. Guard each tool with auth, rate limits, and SSRF/input checks (per your Sim Studio work).

**Q97: How do you prevent data leakage between B2C customers?**  
A: Enforce tenant isolation: scope every query by `tenant_id`/user, validate ownership in auth dependencies, and ensure logs/vectors/cache keys are namespaced per tenant. GuardrailZ-style redaction stops PII leaking across accounts.

**Q98: How would you evaluate the reliability of an agent?**  
A: Track task success rate, hallucination/refusal rates, guardrail trigger counts, latency, and cost per conversation. Add eval datasets and replay tests; alert when metrics degrade after model/prompt changes.

**Q99: Why are you interested in the TailorTalk backend internship?**  
A: My FastAPI/Redis/LLM-guardrails experience (Krip AI, GuardrailZ, Sim Studio) directly maps to building reliable sales/support agents. I want to own core backend features at an early-stage AI startup and grow in system design for production LLM systems.

**Q100: What do you hope to learn and where do you see yourself contributing first?**  
A: I want to deepen distributed system design and production LLM observability/cost control. I'd contribute immediately on REST API design, caching/rate limiting, and the guardrails/security layer — areas where my resume overlaps with TailorTalk's needs.
