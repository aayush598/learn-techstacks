# Priority 5 — Fullstack Scenarios (Q721–Q740)

**Why these matter for micro1:** the interviewer will pick one feature and ask you to design it *end-to-end* — backend, frontend, DB, and the tricky bits. Each scenario below is a complete walkthrough you can adapt. **Pattern: requirements → data model → API → frontend → reliability → security → scale.**

---

## Q721: Design user registration (candidate + recruiter).

**Requirements:** sign up with email+password (and social via OAuth), role selection, verify email, welcome flow.

**Flow:**
1. `POST /auth/register {email, password, role}` → validate (Pydantic), check email uniqueness (`UNIQUE(email)`), **hash password** (argon2id/bcrypt, Q414), create user in one transaction.
2. **Email verification:** create a short-lived signed token (JWT with `type=verify_email`, 24h) → send email via queue → user clicks → `POST /auth/verify` marks `email_verified=True`.
3. Auto-login (issue access + refresh, Q408) or redirect to sign-in.
4. **Role guard:** recruiter flag only set by admin (or verified domain), never by self-service alone (Q395).

**Security:** rate-limit registration (Q393), password strength policy, lockout on repeated failures, no logging of passwords/PII (Q632), CSRF-safe cookie handling (Q404), duplicate email → 409 with a *generic* message (don't leak which emails are registered).

**Frontend:** form (react-hook-form + zod, Q581) → loading state → success screen → "check your email"; error mapping for 409/422.

**Data model:**
```sql
users(id, email UNIQUE, password_hash, role, email_verified, created_at)
```

---

## Q722: Design login + session management.

**Flow:** `POST /auth/login {email, password}` → verify hash → issue **access token (JWT, 15 min)** + **refresh token (opaque, 30 days, stored hashed in DB)** → refresh token in `HttpOnly; Secure; SameSite=Lax` cookie. Frontend stores access token in memory; sends `Authorization: Bearer` (Q406–411).

**Refresh:** `POST /auth/refresh` (cookie) → verify + **rotate** (Q409) → new pair; **reuse detection** → revoke session family on replay (Q409). Logout → revoke refresh token server-side.

**Extras:** MFA (TOTP) for recruiters; device list (per-device session rows); **sign out everywhere**; password change → revoke all sessions; email change → re-verify.

**Threats to name:** token in localStorage = XSS-exposed (Q410); missing SameSite = CSRF (Q404); no rate limit = credential stuffing (Q393); long-lived access = bigger blast radius (Q408).

**Frontend:** axios/fetch interceptor → on 401, call refresh once, retry original request; redirect to login on refresh failure; "remember me" = long-lived refresh vs session-only.

---

## Q723: Design a candidate's job application flow.

**Flow:** browse/search jobs → view job → apply (upload resume) → confirmation → track status.

1. **Browse:** GET `/jobs?filters=...` (Redis-cached listings, cursor pagination, Q389) — public/read-mostly.
2. **Apply:** `POST /applications` with **idempotency key** (Q397) + `UNIQUE(candidate_id, job_id)` (Q396) → creates application `submitted`.
3. **Resume upload:** presigned S3 PUT (Q434, Q610) → enqueue `parse_resume` (Q427).
4. **Async pipeline:** parse → embed → match → screening (Q427–429) — status transitions `submitted → parsed → screening → scored → shortlisted/archived` with a status history table.
5. **Candidate sees status** in the dashboard; **recruiter gets notified** (Q442).

**Reliability/consistency:** the application row is the source of truth; the pipeline is idempotent; **no lost submissions** (each stage writes its state + DLQ on failure, Q561). **Edge cases:** applying twice (409/conflict), job closed mid-apply (atomic status check + update), resume parse failure (manual review fallback, Q427).

**Frontend:** upload progress (S3 multipart), optimistic UI for the submission, a status stepper component, and a re-try affordance.

---

## Q724: Design the AI chat / screening interview feature (full).

**Backend:**
- **Session:** `POST /interviews` (application_id) → creates interview row; conversation state = `messages` table (durable, Q441).
- **Transport:** **WebSocket** per session (bidirectional chat, Q492) — with the **LLM streamed as SSE frames over it** (Q399).
- **Turn handling:** client sends message with `turn_id` → idempotent guard `UNIQUE(interview_id, turn_id)` (Q441, Q443) → context = system prompt + trimmed resume/job context + history (Q663, Q678) → stream reply → save assistant message + token counts.
- **Termination:** interview ends after N questions / candidate says stop / score computed → **separate scoring call** (rubric, Q429).
- **Concurrency:** distributed lock per interview (one in-flight turn), Q441.

**Frontend:**
- Chat UI: messages list, streaming render (append tokens incrementally — a `useStreamingChat` hook, Q587), typing indicator, retry button, reconnect (WebSocket auto-reconnect with last-message id).
- **Stale closure/race safety** (Q573–574): only apply stream chunks from the *current* turn.

**Reliability:** reconnect without losing turns (durable messages + turn_id), provider timeouts → retry once → graceful fallback message (Q437–438), token/cost caps per session (Q272).

**Scale:** sessions are long-lived → Redis pub/sub for cross-instance fan-out (Q349); horizontal workers for the LLM calls; monitor time-to-first-token (Q631).

---

## Q725: Design streaming of AI responses (end-to-end).

**Backend (FastAPI):** `POST /screen/stream` → `StreamingResponse` with `media_type="text/event-stream"`, `Cache-Control: no-cache`, `X-Accel-Buffering: no` (disable nginx buffering). Stream LLM chunks as SSE `data:` frames; heartbeat comments every ~15s; handle client disconnect (`request.is_disconnected()`) to stop token billing (Q399).

**Frontend:** `fetch` + `ReadableStream` reader (parse `data:` lines incrementally), or EventSource for one-way; render tokens as they arrive (Q587); "thinking…" placeholder; abort on unmount (Q574).

**Operational details to name:**
- **Proxy/ALB:** tune keepalive + request/response timeouts; disable response buffering (Q602); connection draining on deploys so streams finish (Q431).
- **Backpressure:** bounded internal buffer; don't accumulate unbounded frames (Q439).
- **Cost:** cancel on disconnect; token caps; prompt caching on the static system prompt (Q432, Q445).
- **Testing:** fake-LLM golden stream in integration tests (Q456); E2E with a canned SSE fixture (Q462).

**Interview answer:** "Streaming needs three aligned layers: the API streams SSE and disables proxy buffering; the frontend reads the stream incrementally and aborts on unmount; ops keeps timeouts/keepalives tuned and drains connections on deploy."

---

## Q726: Design resume parsing (PDF/DOCX → structured data).

1. **Upload:** S3 presigned (Q434) → validate type/size (< 10 MB, PDF/DOCX allowlist).
2. **Extract text:** pdfplumber/pypdf for PDFs, python-docx for DOCX; **OCR fallback** for scanned PDFs (Tesseract) — detect textless pages and route.
3. **Structure (LLM):** prompt → structured JSON via tool-calling + **Pydantic validation** (Q665): name, contact, skills, experience[], education[], projects[].
4. **Validate + repair:** Pydantic parse; on failure retry once, then **manual review queue** (never silently drop, Q427).
5. **Index:** embed skills/summary (Q656), write to pgvector, upsert `candidates.parsed_json` (`ON CONFLICT`, idempotent, Q443).
6. **Post-parse:** update status, trigger matching (Q428), notify.

**Edge cases:** multi-page, tables, images, non-English, corrupted files, duplicate uploads (per-upload id idempotency, Q443). **Privacy:** raw + parsed resume PII handled per retention policy; redact before any third-party embedding call (Q419). **Scale:** workers + queue (Q433), DLQ + replay (Q561).

---

## Q727: Design candidate matching/scoring (hybrid).

1. **Features:** parsed skills, title, years, location, seniority, embedding of resume/job (Q428).
2. **Retrieval:** vector (pgvector cosine) + FTS/BM25 keyword + metadata filters (`status='open'`) → merge top-50 via RRF/weights (Q659).
3. **Rerank:** cross-encoder scores the top-50 (Q681) → top-10.
4. **Score:** weighted blend — skill overlap 0.45, vector 0.30, experience-fit 0.15, seniority/location 0.10; **store `score` + `reasons`** (matched/missing skills, Q428).
5. **Triggers:** new job → match candidates; new candidate → match open jobs; nightly full re-scan.
6. **Evaluation:** golden set with human-verified scores (Q682); measure precision vs recruiter decisions in production (Q631).

**Ties to your project:** candidates see *why* they're matched (reasons), recruiters see explainable scores — explainability is a product feature, not just a nice-to-have (Q428). **Watch-outs:** no LLM in the hot path (Q428), score drift pinned by model version (Q683), cold-start for new jobs (use the job description + category defaults).

---

## Q728: Design a recruiter dashboard (list, filters, real-time updates).

**Backend:** `GET /recruiter/candidates?status&score&job&cursor&sort` → paginated (Q389) + filters (Q75) — **indexed** (`applications(status)`, `(job_id, status)` covering index, Q560), cached listings (Q432), read replicas (Q567).

**Real-time:** **SSE** for one-way updates (new match, screening done, status change) — subscribe to a Redis pub/sub channel per recruiter (Q442, Q492). WebSocket only if recruiters also *interact* live.

**Frontend:**
- Table/cards with sorting, filtering (client-side for loaded page, server-side for big sets), virtualization for large lists (Q588).
- **Live updates:** SSE handler updates rows in place (merge by id), a badge for new matches.
- Skeleton loading + error states; debounced search (Q572).
- Status stepper (submitted → screening → scored → shortlisted) and a detail drawer with the AI score + reasons + transcript link.

**Interview answer:** "The dashboard is read-heavy: index + cache + replicas for the queries, cursor pagination, and SSE with Redis pub/sub for live updates — merging by id on the client so in-place rows update without re-fetching."

---

## Q729: Design email/notification delivery.

**Channels:** in-app (SSE, Q442), email (transactional), push (optional).

**Pipeline:** an event happens (application submitted, screening scored) → `notifications` row (durable) + **queue** → worker renders + sends via a provider (SES/Postmark) with retries/backoff (Q398), DLQ on hard failures (Q561), **dedupe by notification id** (Q443).

**Email specifics:**
- **Templates** per type; **no raw HTML from AI** — sanitize AI-generated content before templating (Q403, Q419).
- **Batching/digests** for low-priority match suggestions (one daily email, not 10) — inbox + cost.
- **Deliverability:** SPF/DKIM/DMARC (Q486), complaint/bounce handling, unsubscribe (legally required).
- **Personalization** with candidate/job names; **privacy**: PII only to the intended recipient.

**Frontend:** in-app bell with unread badge; SSE marks new; mark-as-read API (idempotent).

**Observability:** send success/failure rates, bounce/complaint alerts, per-type counts (Q631).

---

## Q730: Design search for jobs (or candidates).

**Requirements:** keyword + filters (location, remote, seniority, skills) + sort + pagination.

**Tier 1 (small scale — start here):** **Postgres FTS** (`tsvector` + GIN, Q559): `to_tsvector(title || ' ' || description) @@ plainto_tsquery('query')` + indexes on filter columns. Good to ~100k jobs.

**Tier 2 (grow):** **hybrid search** — FTS for exact terms + **vector** for semantic ("growth marketing" ≈ "performance marketing") (Q659) + filters. Rerank top-50 (Q681).

**Tier 3 (scale out):** **Elasticsearch/OpenSearch** (or Meilisearch/Typesense): inverted index, facets, typo-tolerance, relevance tuning (BM25), pagination (`search_after` for deep pages, Q390). Sync via **logical replication/CDC** from Postgres (Q557) or event-driven reindexing (Q433).

**Frontend:** debounced search box (Q572), facet filters, instant results with `useDeferredValue` (Q588), loading skeletons.

**Answer:** "Postgres FTS + GIN with hybrid vector search serves us for a long time; I'd move to Elasticsearch only when query volume or relevance tuning demands it — and I'd keep Postgres as source of truth with CDC sync."

---

## Q731: Design the audit trail (who did what, when).

**What to record:** auth events (login/refresh/logout/role changes), application status changes, AI score generation + model version + prompt hash, resume uploads/parse, data exports, admin actions, permission changes.

**Storage options:**
1. **`audit_logs` table** (partitioned by month, Q552) with `actor_id, action, target_type, target_id, payload JSONB, created_at` — good for a single-writer app; indexed on `(actor_id, created_at)` and `(target_type, target_id)`.
2. **Append-only log + cold store** (S3/Glacier) for long retention (Q632).

**Design principles:**
- **Immutability:** no UPDATE/DELETE on audit rows (append-only); the API has no update route.
- **Idempotent writes:** async audit writes via queue (don't block the request, Q433), dedupe by event id (Q443).
- **Who/what/when:** capture actor (user_id or system), IP/device, action, target, and the **result** (success/failure) + request_id (links to logs/traces, Q65).
- **Include system actors:** LLM pipeline writes ("score_generated", model=gpt-4o, prompt_version=v3).
- **Access:** only admin/audit roles read audit logs; never log secrets/PII payloads wholesale (Q632).
- **Retention:** keep hot ~1–3 months, archive to S3 for regulatory needs (Q632).

**Why interviewers ask:** it shows production maturity — "I record every consequential action append-only, idempotently, with actor/target/result, and archive to cold storage."

---

## Q732: Design a feature flag system (kill-switch for AI).

**Backend:**
- `feature_flags` table or a config service: `(name, enabled, rollout_percent, targeting JSONB, owner, updated_at)`.
- **Middleware/dependency:** `get_flag(name, user)` — deterministic per-user bucketing (hash user_id → bucket < rollout_percent); override by tenant/email (for enterprise/QA).
- **Cache flags** in Redis (short TTL) so checks are cheap; admin API + audit on changes (Q731).
- **Serving:** flags read at request time (fast path) — for the LLM path, the **kill-switch is checked before every screening call** (Q633).

**Frontend:** flags exposed via a `/flags` endpoint (only non-sensitive ones); the chat UI reads `chat_v2` before choosing the streaming implementation.

**Ops value:** roll back a bad prompt/model **without a deploy** (Q633) — for AI, this is mandatory: a prompt change that degrades scoring should be behind `screen_v3` and reversibly disabled (Q634).

**Interview answer:** "Flags are runtime switches with per-user bucketing and a fast Redis lookup; the killer use-case is the AI kill-switch — I can disable a bad model or prompt in seconds without deploying."

---

## Q733: Design the resume upload with progress and resumability.

1. **S3 presigned PUT** (Q434, Q610) — client uploads directly; the API never handles the bytes.
2. **Multipart upload** (S3 CreateMultipartUpload → upload parts → Complete) — **resumable** across network drops; client tracks completed parts, retries failed ones (Q398).
3. **Progress UI:** upload progress bar from the part-completion callbacks; **pause/cancel**; on completion → `POST /uploads/confirm {key, upload_id}` → API validates size/type → enqueues `parse_resume` (Q427).
4. **Security:** presigned URL scoped to the object + expiry; file-type sniffing (magic bytes, not just extension); size cap; malware scan for untrusted uploads (Q434).
5. **Failure paths:** part retry with backoff; resume on reload (persist upload state in localStorage/DB with the upload id); cleanup orphaned multipart uploads (S3 lifecycle).

**Frontend detail:** `fetch`/XHR with progress events, or the S3 SDK's managed upload; disable double-submit (Q396).

**Interview answer:** "Presigned URL + multipart upload → resumable with progress, and the API stays out of the data path; confirm step enqueues parsing; everything idempotent by upload id."

---

## Q734: Design a WebSocket chat that survives reconnects.

**The hard parts:** the connection is ephemeral; the conversation must be durable (Q441).

**Design:**
1. **Messages are the source of truth** (Postgres `messages`); the socket is *transport*.
2. **Client tracks `last_message_id`**; on (re)connect, sends it; server replays everything after it (Q349).
3. **Turn idempotency:** every client message has `turn_id`; server dedupes (`UNIQUE(interview_id, turn_id)`) so retries don't double-LLM-call (Q441, Q443).
4. **Cross-instance fan-out:** with N app instances, a message to user X's socket may be on a different instance than the one that produced the reply → **Redis pub/sub**: worker publishes `interview:xyz` events; all instances subscribe; the one holding the user's socket forwards (Q349).
5. **Heartbeats:** server ping/pong (or SSE comment frames, Q399) to keep idle connections alive through proxies (Q491).
6. **Graceful deploys:** connection draining (Q431) + client auto-reconnect with backoff.

**Test story:** kill the server mid-stream, reconnect, assert no lost turns (Q462-style integration test with a real Redis).

---

## Q735: How would you paginate the candidate list in the dashboard?

(Compose Q389–390 + Q560 into one concrete answer.)

- **Default:** **cursor pagination** on `(id)` or `(score, id)` keyset — `WHERE (score, id) < (?, ?) ORDER BY score DESC, id DESC LIMIT 50` → stable under churn, constant cost deep pages (Q390).
- **Index:** `applications(job_id, status, score)` supporting the filtered, sorted query (covering `id` too → index-only scan, Q560).
- **Envelope:** `{items, next_cursor, has_more}` (Q389).
- **When offset is OK:** admin screens with "jump to page 5" on small, static data (Q390).
- **Edge cases:** score ties (add `id` to the tiebreak), status changes mid-paging (cursor is still stable), very deep pages (no offset cost).

**Interview answer:** "Keyset/cursor pagination with a composite index on the sort+filter columns — stable, O(page) even deep, and I only fall back to offset for small admin datasets."

---

## Q736: How would you handle high load on the AI screening endpoint?

**The screening endpoint is the bottleneck (LLM-bound, cost-bound, slow):**

1. **Async queue the *work*, stream the *experience*:** the heavy compute (LLM scoring) runs on **workers**, not the request path (Q433). Chat turns are inherently interactive → stream them (Q725) with a **circuit breaker + fallback** (Q438).
2. **Protect the provider:** per-user rate limits + concurrency caps (semaphore, Q104, Q393) so a burst doesn't trip the provider 429s and cascade retries (Q270).
3. **Cache what you can:** prompt caching for the static system prompt (Q432), deterministic-result cache for repeated (resume, job) scoring (Q671).
4. **Scale the workers horizontally** (autoscaling on queue depth, Q435, Q603) — the API tier scales independently of the LLM-call tier.
5. **Graceful degradation:** when the provider is down/overloaded → cached/fallback answers + requeue (Q437); recruiters still see candidate data and can shortlist manually.
6. **Cost guardrails:** per-tenant budget caps → route over-quota tenants to a cheaper model (Q445, Q669).

**Answer:** "Queue the LLM work, stream the interactive parts, bound concurrency, cache aggressively, and autoscale the worker pool — with a kill-switch and fallbacks so load degrades gracefully instead of failing."

---

## Q737: How would you ensure data consistency between Redis cache and Postgres?

**Consistency strategies (choose per data type):**

1. **Cache-aside (lazy load):** read: cache miss → DB → set cache (TTL). Write: **invalidate the cache key on write** (delete, don't update — avoids stale dual-writes). Simplest and most robust (Q432, Q251).
2. **Write-through:** update DB + cache in the same request — *doesn't solve atomicity* across stores; risk of partial failure. Only for low-stakes, low-volume data.
3. **TTL as the safety net:** even with perfect invalidation, a short TTL (30–300s) bounds staleness if a bug skips invalidation (Q432).
4. **Versioned keys:** `jobs:v3:123` — bump the version on schema/logic change; old keys just expire.
5. **Do DB-first, then invalidate (never update cache from the app):** if the app crashes between the two, the DB is correct and the stale cache expires on TTL — never the reverse (a stale *write* to cache with no DB update is the dangerous case).
6. **For derived/hot data** (counts, scores): compute off an event stream (Q433) with eventual consistency, tolerate seconds of lag (Q567).

**Answer:** "Cache-aside with write-through invalidation (delete key on write), short TTLs as a bound on staleness, versioned keys for cheap invalidation — and I never write cache from the app path without the DB write first."

---

## Q738: How would you test the whole stack end-to-end?

**Compose the strategy (Q465 + Q462) into a concrete plan:**

1. **Unit (fast, many):** scoring/prompt-building/idempotency/PII-redaction — mocked LLM + DB.
2. **Integration (the valuable middle):** FastAPI `TestClient` + **real Postgres (Testcontainers)** + Redis → apply → parse → screen flows; workers against a real queue; **fake LLM client** with golden outputs (Q456).
3. **Contract:** zod schema ↔ Pydantic model equivalence check (both sides validate the same shape — Q582/Q665).
4. **E2E (few, critical):** **Playwright** — register → upload resume → apply → chat with the AI (stubbed SSE fixture) → recruiter shortlists → candidate sees status. Run on staging against the full stack (Q462).
5. **AI evals (the AI-specific layer):** golden set + regression cases run in CI on every prompt/model change (Q682, Q456).
6. **Reliability tests:** circuit-breaker drill (provider down → fallback works, Q456), reconnect mid-stream (Q734), duplicate-turn idempotency.
7. **Perf smoke:** streaming time-to-first-token budget, queue drain rate (Q626).

**Answer:** "Pyramid — fast unit tests, integration against real Postgres/Redis with a fake LLM, a few Playwright journeys, plus an AI eval harness in CI and failure-mode drills; coverage floor + flaky-test quarantine."

---

## Q739: How would you monitor the health of the whole system?

**Health endpoints + layered checks + alerts (compose Q444, Q626, Q631):**

1. **`/healthz`** — liveness: process up (LB uses it).
2. **`/readyz`** — readiness: dependencies reachable — Postgres (`SELECT 1`), Redis (PING), queue writable. Used by LB/rollout to take the instance out of rotation when a dependency is down (Q431, Q623).
3. **Synthetic checks:** an external monitor (and a scheduled Lambda) hitting the real flow: healthz, login, one read endpoint, one write (Q626).
4. **RED metrics** per endpoint: QPS, errors (4xx/5xx split), p50/p95/p99 + **time-to-first-token** for streaming (Q626).
5. **Domain metrics:** queue depths, worker task success/retry/DLQ, LLM cost + error rate, parse success rate, screening completion, DB connections + replica lag (Q631).
6. **Distributed traces:** every request → `trace_id` → API → queue → worker → LLM → DB (Q627); logs structured + correlated (Q625).
7. **Alarms on symptoms** with runbooks: p99 breach, 5xx > 1%, queue depth > 5k, LLM error rate spike, cost budget breach (Q631). **SLOs + error budgets** on the critical journeys (Q629).

**Answer:** "Readiness checks gate the LB, RED + domain metrics give the dashboard, traces find the hop, and symptom-based alerts with runbooks wake someone — with SLOs on apply/screen/chat."

---

## Q740: If you could redesign the whole system, what would you change?

**An honest, senior answer — name real weaknesses and priorities:**

1. **Bottleneck now:** the LLM dependency (cost + latency + availability). I'd put **prompt caching, model routing (Q669), and a semantic cache (Q671)** at the very top — and make every provider call go through a circuit-breaker with a fallback *from day one* (Q438, Q684).
2. **Data/state:** I'd centralize event-driven sync between Postgres and the vector/search index (logical replication/CDC, Q557) instead of ad-hoc triggers — one source of truth, no drift (Q659, Q730).
3. **Observability for AI:** a production eval + human-feedback loop from the start (Q631, Q682) — every prompt change gated by evals (Q634).
4. **Deploy discipline:** blue/green + canary for AI changes with automatic rollback (Q622–623) and **feature flags as the default** for every release (Q633).
5. **Security by default:** PII redaction enforced at the prompt boundary (Q419), SSRF-safe URL fetching (Q418), audit logs for every AI decision (Q731).
6. **Testing the risky layer:** golden eval sets + failure drills (Q456, Q738) — the LLM is the least deterministic part, so it gets the most rigorous testing.

**Interview framing:** "I'd rebalance toward the things that most determine whether an AI product survives contact with production: cost-aware routing, evals gating every model change, a kill-switch, and fail-soft behavior when the provider blinks."
