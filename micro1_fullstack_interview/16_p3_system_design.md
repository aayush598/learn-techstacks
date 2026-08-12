# Priority 3 — System Design (Q421–Q447)

**Why these matter for micro1:** the AI recruiter interview almost always asks you to design (or improve) a system — likely the Zara AI recruiter itself: resume parsing → candidate matching → AI screening → recruiter notifications. Expect a whiteboard-style flow: requirements → capacity → components → data → scale → tradeoffs.

---

## Q421: How do you approach a system design question?

**Always follow the same skeleton — it buys you structure and covers the scoring rubric:**

1. **Clarify requirements (2 min)** — scope, users, scale, read/write ratio, what's in/out.
2. **Non-functional requirements** — latency (chat should feel instant), availability, durability, consistency, cost.
3. **High-level architecture** — draw boxes: clients, API layer, services, workers, DB, cache, queue, storage.
4. **Data model** — core entities + storage choices.
5. **Key API + flows** — 2–3 main flows (e.g., submit application, screening, notification).
6. **Scaling + bottlenecks** — where it breaks, how you fix (queue, cache, replicas, partitioning).
7. **Tradeoffs + deep dives** — one or two you can defend (CAP, eventual consistency, stream vs poll).
8. **Wrap-up** — monitoring, failure modes, what you'd do next.

**Golden rule:** talk ~70%, write/diagram ~30%. The interviewer grades your *reasoning*, not a perfect diagram.

---

## Q422: Design the Zara AI recruiter — high-level architecture

**Problem:** candidates submit resumes; the AI recruiter parses them, screens/matches them against jobs, runs AI interviews, and hands qualified candidates to human recruiters.

**High-level components:**

```text
┌────────────┐  ┌──────────────────────────────┐  ┌───────────────┐
│ Candidate  │  │          Next.js/React        │  │   Recruiter   │
│   (web)    │──│   candidate + recruiter UI    │──│    (web)      │
└────────────┘  └──────────────┬───────────────┘  └───────────────┘
                              │ HTTPS (FastAPI)
                     ┌────────▼─────────┐
                     │  API Gateway     │  auth, rate limit, routing
                     └────────┬─────────┘
              ┌───────────────┼───────────────┐
        ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼──────┐
        │ Screening │   │ Matching  │   │  Parsing   │   ← stateless FastAPI services
        │  Service  │   │  Service  │   │  Service   │
        └─────┬─────┘   └─────┬─────┘   └─────┬──────┘
              │               │               │ consume from SQS/Redis Streams
              │        ┌──────▼──────┐   ┌────▼─────┐
              │        │ Vector/ES   │   │ LLM      │  (GPT, embeddings)
              │        │ search      │   │ provider │
              │        └─────────────┘   └──────────┘
              └───────────────────────────────────
     ┌───────────────┬───────────────┬───────────────┐
     │ PostgreSQL    │     Redis     │     S3        │
     │ primary data  │  cache/queues │ resumes/raw   │
     │               │  sessions     │ docs          │
     └───────────────┴───────────────┴───────────────┘
```

**Key design decisions:**
- **Async pipeline for expensive work:** resume upload → S3 + message to queue → parser worker → extracted JSON → matching → AI screen → notifications. The API responds in ms; heavy work is decoupled.
- **Separation of services:** parsing, matching, screening scale independently (different resource profiles: parsing is I/O-heavy, screening is LLM-call-bound).
- **PostgreSQL as source of truth**, S3 for raw docs, Redis for cache + queues + chat sessions, vector store for similarity matching.
- **Streaming for AI chat** (Q399) so interviews feel real-time.

---

## Q423: What are the core components/boxes, and why those boundaries?

1. **API Gateway / API layer** — auth (JWT), rate limiting, routing, request validation. Stateless → easy to scale.
2. **Parsing service** — converts PDF/DOCX resumes to structured JSON (text extraction + LLM). Heavy, async via queue.
3. **Matching service** — candidate ↔ job score. Uses embeddings/vector search + a rules/weighting layer.
4. **Screening service** — orchestrates the AI interview: builds prompt, streams Q&A, scores responses, stores transcript.
5. **Notification service** — emails/pushes to recruiters and candidates (job matches, interview scheduled, results).
6. **Datastores** — PostgreSQL (authoritative), Redis (cache, sessions, queues, rate limits), S3 (documents), vector DB (embeddings).
7. **Search** — Elasticsearch/OpenSearch or Postgres FTS for job/candidate search with facets and filters.

**Why separate:** independent scaling, independent failure (parser dies ≠ chat dies), team ownership, resource isolation. Don't over-split a small system — but for the interview, justify each boundary by scale or rate of change.

---

## Q424: What functional and non-functional requirements would you gather?

**Functional:**
- Candidate: upload resume, create profile, browse/search jobs, apply, chat with AI, view application status.
- Recruiter: post jobs, review candidates, get AI scores + reasoning, shortlist/archive, schedule human interviews, get notified.
- Admin: manage jobs/candidates, view audit logs, monitor model usage/cost.

**Non-functional:**
- **Latency:** chat < 1–2s time-to-first-token; page loads < 200ms; screening result within minutes (async).
- **Availability:** 99.9%+ for the web app; graceful degradation if the LLM provider is down (fallback messages).
- **Scalability:** thousands of concurrent candidates during hiring peaks; bursts of resume uploads.
- **Consistency:** strong for application status; eventual for scores/search.
- **Durability:** never lose a submitted application or chat transcript.
- **Security/privacy:** resume PII, GDPR/CCPA, role-based access, audit.
- **Cost:** LLM calls dominate — batch/stream, cache, budget caps per tenant.

---

## Q425: How would you estimate capacity?

**Worked example (the AI recruiter):**
- **Users:** 100k registered candidates, 5k recruiters. Hiring season peak: 10x daily active users.
- **DAU (candidates):** ~20% → 20k/day. Peak QPS: 20k/86400 × ~5x diurnal burst ≈ **2–5 QPS** overall; page-load bursts at 10–20 QPS. (Small numbers — the *workers* are the real load.)
- **Uploads:** 20k/day resumes, avg 1 MB → **20 GB/day** → ~7 TB/year. Cheap in S3.
- **Parsing:** 20k/day → ~0.23/s. Each parse ~5–10s of LLM work → need **~20–50 concurrent worker slots** or a queue that absorbs spikes.
- **Screening chat:** 20k candidates × avg 20 turns × ~500 tokens = 400M tokens/day ≈ $1–2k/day in LLM cost → **cost, not QPS, is the constraint.** Mitigate: shorter prompts, caches, cheaper models for simple turns, per-tenant quotas.
- **Database:** applications ~1M/yr, transcripts ~5M messages/yr, resumes parsed ~1M → tens of GB → single Postgres fine, add replicas for reads.
- **Redis:** session/queue data small; cache hit ratio target > 90% for profile/job reads.

**Answer format:** "rough math on users → QPS → storage → worker/LLM cost, then say the bottleneck is LLM cost + worker throughput, not API QPS."

---

## Q426: What's the data model for the AI recruiter?

**Core tables (PostgreSQL):**

```sql
users            (id, email, role, password_hash, created_at)
candidates       (user_id FK, name, resume_s3_key, parsed_json JSONB, embedding_id)
jobs             (id, company_id, title, description, requirements JSONB, status, created_at)
applications     (id, candidate_id, job_id, status, ai_score, stage, created_at,
                  UNIQUE(candidate_id, job_id))
interviews       (id, application_id, transcript JSONB, status, started_at)
messages         (id, interview_id, role, content, tokens, created_at)
matches          (id, candidate_id, job_id, score, reasons JSONB, viewed)
notifications    (id, user_id, type, payload JSONB, read, created_at)
audit_logs       (id, actor_id, action, target JSONB, created_at)
```

**Design notes:**
- JSONB for flexible parsed resumes/scores (Q327); indexed columns only for what you filter/sort.
- `UNIQUE(candidate_id, job_id)` = idempotency for applications (Q396).
- Partition `messages`/`audit_logs` by month at scale (Q552).
- Indexes: `applications(status)`, `applications(candidate_id)`, `jobs(status, created_at)`, FTS/vector columns for search.

---

## Q427: How would you design the resume parsing pipeline?

**Flow:** upload → store → extract → structure → enrich → index.

1. **Upload:** candidate uploads PDF/DOCX. API streams to **S3** (`resumes/{candidate_id}/{uuid}.pdf`), returns quickly.
2. **Queue job:** push `parse_resume` message with the S3 key to the queue (Redis Streams/SQS). Idempotency key = upload id.
3. **Worker picks it up:** downloads from S3, extracts raw text (pdfplumber/pypdf; DOCX via python-docx; OCR fallback for scanned PDFs).
4. **LLM structuring:** send extracted text to the LLM → structured JSON (name, email, skills, experience, education, projects) with Pydantic output validation (Q16/Q17).
5. **Validate + fallback:** if parsing fails or is low-confidence → retry with backoff (Q398), then queue for **manual review** (never silently drop).
6. **Enrich + index:** extract skill embeddings (Q267), write to vector store for matching, update `candidates.parsed_json`.
7. **Notify:** status update so the UI shows "resume processing".

**Reliability:** at-least-once delivery + idempotent upsert (`ON CONFLICT (candidate_id) DO UPDATE`); dead-letter queue for poisoned messages (Q561).

---

## Q428: How would you design candidate–job matching?

**Hybrid approach — rules + embeddings:**

1. **Candidate side (at apply/update):** embed the parsed resume (skills, title, summary) → store vector.
2. **Job side:** embed job description at post time → store vector.
3. **Retrieval (candidate or job side):** vector similarity (cosine) to get a shortlist (Q659) + Postgres FTS/keyword match as a recall booster.
4. **Ranking/rerank:** score = weighted blend:
   - `0.45` skill overlap (from parsed skills vs requirements),
   - `0.30` vector similarity,
   - `0.15` years of experience fit,
   - `0.10` location/seniority/availability.
   - Optionally a **reranker model** on the top-50 for quality (Q681).
5. **Explainability:** store the score *and reasons* (`reasons JSONB`: matched/missing skills) — recruiters must see why a score is high.
6. **Trigger points:** new job posted → match against top candidates; new candidate → match against open jobs; background nightly re-scan.

**Watch-outs:** avoid LLM in the hot path (slow/costly) — embeddings are precomputed; keep the LLM for generation, embeddings for retrieval.

---

## Q429: How would you design the AI screening interview?

1. **Trigger:** application accepted → screening starts (async).
2. **Context build:** pull job requirements + candidate parsed resume + any prior interview → build a focused prompt (keep it tight for cost/latency).
3. **Session state:** an `interviews` row + chat messages; store transcript as messages stream in (durable, Q441).
4. **Interaction loop:** one turn at a time —
   - user message → append to context → stream LLM reply (Q399) → save message → check termination conditions.
   - Stop when: questions asked enough, candidate says stop, budget of turns reached.
5. **Scoring:** at the end, a **separate scoring call** (don't let the conversational LLM also grade its own conversation — use a rubric prompt) → structured JSON score per rubric dimension + summary + recommendation.
6. **Human-in-the-loop:** AI recommendation ≠ decision — recruiters review scores/reasons before advancing (Q419).

**Failure handling:** provider timeout → retry once, then graceful "please retry" to the candidate; disconnect → resume from last saved message (durable session, Q441).

---

## Q430: Horizontal vs vertical scaling?

- **Vertical:** bigger machine (more CPU/RAM). Easy, but has a ceiling and a single point of failure. Fine for a small service, DB at moderate load.
- **Horizontal:** more instances behind a load balancer (Q431). Scales past the box limit, gives HA/failover, but adds complexity: shared state must move to Redis/DB, and any **in-memory session must be externalized** (Q82/Q441).

**For the recruiter:** scale the stateless API + worker fleet horizontally; keep state (sessions, scores, queues) in Redis/Postgres. The DB eventually needs replicas or partitioning (Q433/Q552).

---

## Q431: How does load balancing work, and what strategies exist?

**Load balancer (LB)** distributes traffic across instances and health-checks them (marks dead instances out, retries on others).

**Layers:**
- **L4 (transport):** TCP/IP-based, fast, no content awareness (NLB).
- **L7 (application):** HTTP-aware — path/host routing, header manipulation, TLS termination, sticky sessions (ALB/nginx).

**Algorithms:**
- **Round robin** — even distribution, ignores load.
- **Least connections / least outstanding requests** — better for mixed request durations (your LLM streaming requests are long → least-connections beats round robin).
- **IP hash / sticky sessions** — route the same client to the same instance (needed only if state isn't externalized).

**For chat/streaming:** L7 LB with **connection draining** (let in-flight streams finish before draining an instance during deploy — critical, or users get cut mid-interview).

---

## Q432: What's the caching strategy for this system?

**Cache the reads that hurt; never cache writes that must be durable.**

- **API responses:** job listings, candidate profiles, job details — cache 30–300s in Redis; invalidate on write.
- **Database:** read replicas for hot reads (Q433); Postgres shared_buffers for disk hits.
- **LLM outputs (biggest win for cost):**
  - **Prompt/cache layer:** cached identical system prompts across turns (Anthropic-style prompt caching) — saves 90% of input cost.
  - **Deterministic results cache:** same resume+job scoring → cached score with a key like `score:{job}:{cand}:{version}` (invalidate when resume/job changes).
  - **Embeddings cache:** same text → same embedding (dedupe on parse).
- **CDN:** static assets only (JS/CSS); don't CDN user data.
- **Session/chat state:** Redis for hot session lookups.

**Consistency:** cache-aside (Q251); version keys (`jobs:v2`) for cheap invalidation; short TTLs bound staleness.

---

## Q433: How would you use queues/async processing here?

**What queues:**
- `parse_resume` — upload → parser workers (SQS/Redis Streams).
- `match_candidate` — parsed candidate → matching pipeline.
- `run_screening` — accepted application → AI interview.
- `score_interview` — transcript done → scoring + notification.
- `notify` — recruiter/candidate emails & pushes.
- `audit` — async audit log writes.

**Why queue (not direct call):**
- **Decoupling:** API stays snappy; parser/screening can lag.
- **Burst absorption:** 1k resumes land at once → queue holds them, workers drain at their pace.
- **Retry + DLQ:** failed jobs retry with backoff, then go to a dead-letter queue for manual inspection (Q561).
- **Backpressure:** queues grow, don't drop; alarm on queue depth (Q439).

**Pattern:** producer → queue → worker; at-least-once delivery; consumers **idempotent** (Q387, Q396). Redis Streams with consumer groups (Q97) are a great single-store choice for you; SQS for AWS-native.

---

## Q434: How would you handle large file uploads (resumes)?

1. **Direct-to-S3 (presigned URL):** client gets a short-lived `PUT` URL from the API, uploads straight to S3 — the API never touches the bytes (offloads bandwidth, Q610).
2. **Size/type validation:** reject > 10 MB, allowlist PDF/DOCX/DOC; scan for malware if untrusted.
3. **Post-upload:** client confirms → API enqueues `parse_resume` with the S3 key → async pipeline (Q427).
4. **Multi-part/retryable uploads** for flaky networks; resume-able via S3 multipart.
5. **Cleanup:** delete raw file after parse (or retain per retention policy) to control S3 cost + PII exposure.

**Streaming vs loading:** never `read()` the whole file into memory server-side; stream to S3 or use presigned uploads.

---

## Q435: How do you design background jobs and workers?

**Worker anatomy:** a process that consumes from a queue and does the work (FastAPI app is the API; a `python -m app.worker` process is the consumer).

```python
# worker: consume parse_resume
async def main():
    async with redis_client.pubsub() as ps:   # or SQS poll loop
        while True:
            msg = await ps.get_message(...)
            if msg: await handle_parse(msg)
            await asyncio.sleep(0.05)
```

**Best practices:**
- **Idempotent handlers** — a job may run twice (at-least-once) → upsert, not insert (Q396).
- **Explicit timeouts + retries** with exponential backoff (Q398); per-task budget.
- **Concurrency control:** bounded workers per type; DB connections/LLM rate limits shared carefully (Q104).
- **Health/monitoring:** heartbeat + queue depth + per-task latency/failure metrics (Q631).
- **Graceful shutdown:** finish current task, stop polling, let LB drain (Q431).
- **DLQ** for poison messages; alert + replay tool.
- **Priorities:** two queues (high: screening/interview; low: parsing) or class-based Redis Streams.

---

## Q436: How do you achieve high availability (HA)?

**Definition:** the system keeps serving even when components fail — measured as uptime % (99.9% ≈ 8.7 h downtime/yr).

**Layers:**
- **Stateless app tier:** ≥2 instances across ≥2 AZs behind an LB; loss of one instance/AZ = traffic goes to the others. (AWS ALB + ASG, Q604.)
- **Database:** primary + **standby in another AZ** with automated failover (RDS Multi-AZ); read replicas for reads. RPO ~0 (sync standby), RTO minutes.
- **Queue/cache:** Redis with replicas (or managed Redis cluster) + persistence (AOF/RDB); queues in SQS (SQS is regionally redundant by default).
- **Storage:** S3 (11 nines durability).
- **DNS:** Route 53 health checks + failover.

**The gap to call out:** if the **LLM provider** is down, you can't fully serve interviews → graceful degradation: show a friendly message, cache common responses, queue screening for later, don't fail the whole app (Q437).

---

## Q437: How would you design fault tolerance and graceful degradation?

- **Fail small:** if screening service is down, candidates can still browse jobs and apply; only "AI chat" shows a degraded banner.
- **Fallbacks:** LLM down → reuse cached/generic responses for simple intros, or requeue with backoff; search backend down → fall back to Postgres FTS; vector store down → keyword-only matching.
- **Timeouts + circuit breakers** (Q438) so a slow dependency doesn't cascade into the whole app.
- **Retries with backoff** for transient failures (Q398).
- **Bulkheads:** separate worker pools/queues per workload so parser floods don't starve interview turns.
- **Dead-letter queues + alerting** so failures are *visible*, not silent (Q631).

**Answer:** "Every external dependency gets a timeout, a fallback, and a circuit breaker; the API always returns something useful even when a sub-system is degraded."

---

## Q438: What is a circuit breaker, and when would you use one?

**Circuit breaker:** stops calls to a failing dependency for a cooldown window after N consecutive failures, so you don't hammer a dead service (Q363, Q614).

```python
# states: CLOSED (normal) → OPEN (failing, fail fast) → HALF-OPEN (probe) → CLOSED
if breaker.state == "open":
    return fallback_result()            # fail fast, don't call LLM
try:
    result = await call_llm(...)
    breaker.record_success()            # reset count
    return result
except TimeoutError:
    breaker.record_failure()            # increment; open after threshold
    if breaker.should_open(): breaker.state = "open"
    raise
```

**Use for:** LLM provider calls, vector search, S3, email/SMS — anything external with variable latency. **Config:** failure threshold (e.g., 5), timeout window (e.g., 30s), probe interval. Combine with timeouts and a fallback (cached answer / friendly message).

---

## Q439: What is backpressure, and how do you handle it?

**Backpressure:** the system can't consume as fast as producers supply → you must slow/absorb producers instead of buffering unboundedly and OOMing.

**Where it hits you:**
- **Uploads:** 1k resumes burst → queue grows. Absorb in the queue (bounded), workers drain at their rate, **alarm on queue depth**.
- **LLM concurrency:** provider rate limit (429) → workers must **respect backoff** (Q270) or they flood retries; use a semaphore to cap concurrent LLM calls (Q104).
- **Streaming:** if the client is slower than the producer, buffer with a bounded queue and drop/signal; don't let `yield` pile up unbounded frames (Q399).
- **DB connections:** pool exhaustion → requests wait; cap worker concurrency to the pool size (Q111).

**Answer:** "Queues absorb bursts, workers impose concurrency limits, and I alarm on depth. If queues fill, I either scale workers horizontally or shed load (reject with 503 + Retry-After)."

---

## Q440: How would you scale the database for this system?

**Progression (do in order):**
1. **Indexes + query tuning** — fix the slow queries first (Q162, Q328).
2. **Read replicas** — route reads (job listings, profiles, search) to replicas; writes to primary (Q567). Good until replica lag matters.
3. **Cache (Redis)** — hot reads off the DB entirely (Q432).
4. **Partitioning** — `messages`, `audit_logs`, `notifications` by month (Q552); partitions let you drop old data cheaply.
5. **Vertical bump** — bigger instance (often buys years at your scale).
6. **Sharding** — split by tenant or candidate id (Q566) — last resort, adds big complexity.
7. **Move read-heavy workloads out:** search → Elasticsearch; analytics → data warehouse.

**Honest answer:** for the recruiter's actual scale (thousands–millions of records), replicas + cache + partitioning carry you a very long way; sharding is a "if I really needed it" answer.

---

## Q441: How do you persist chat/session state for the AI interview?

- **Store every message durably:** `messages(interview_id, role, content, tokens, created_at)` — the transcript is the source of truth, not Redis.
- **Redis = hot working set:** current turn context, lock per interview (prevent two concurrent replies in one session), rate-limit tokens per session.
- **Reconstruct context from the transcript** if a worker dies — the interview resumes where it stopped (candidate can refresh and continue).
- **Concurrency guard:** one in-flight turn per interview (distributed lock via Redis `SET NX` or optimistic version on the interview row) (Q553–555).
- **Idempotent turns:** client sends `turn_id`; `UNIQUE(interview_id, turn_id)` prevents duplicate LLM calls on retry (Q396) — critical because LLM calls cost money.
- **Expiry/retention:** transcripts retained per policy; PII in chat handled like resume PII (Q419).

---

## Q442: How would you implement real-time notifications?

**Notification types:** interview invite, screening started/finished, new match, recruiter: candidate shortlisted, system alerts.

- **Delivery channels:** in-app (poll/SSE), email (transactional), push.
- **In-app real-time:** **SSE** for one-way pushes (Q347, Q399) or **WebSocket** if the page must also send (chat) (Q348); a `notifications` table as the durable source + an unread badge query.
- **Email:** queue → worker → provider (Postmark/SES); async, retry with backoff, never block the API.
- **Fan-out:** new job posted → matched candidates get notified: query matches in batches, enqueue `notify` messages (don't loop 10k synchronous emails).
- **Dedupe/batching:** digest emails for low-priority match notifications (batch candidates into one daily email) to protect inboxes + cost.

---

## Q443: Where does idempotency matter in this system?

1. **Applications:** `UNIQUE(candidate_id, job_id)` + idempotency key on `POST /applications` (Q396).
2. **Resume parse:** one parse per upload id; upsert `parsed_json` (Q427).
3. **Interview turns:** `UNIQUE(interview_id, turn_id)` so a retried client message doesn't double-call the LLM (Q441).
4. **Notifications/emails:** dedupe by notification id so a retried worker doesn't send two "you're shortlisted" emails.
5. **Webhooks/events:** `UNIQUE(event_id)` + `ON CONFLICT DO NOTHING` (Q420, Q561).

**Golden rule:** any code path with a retry (queues, network) and a side effect (money, emails, LLM calls, DB writes) needs idempotency.

---

## Q444: How would you monitor and observe this system?

**Three pillars (Q631–635):**
- **Metrics (Prometheus/Grafana, CloudWatch):** request rate/latency/error rate per endpoint; **queue depth** (backlog alarm); worker task latency/success; LLM cost per user/feature; DB connections, replication lag; p99 streaming time-to-first-token.
- **Logs (structured, centralized):** every API request with `request_id`; worker jobs with job id; LLM calls (model, tokens, latency, truncated); audit events. Searchable, with sensible retention.
- **Traces (OpenTelemetry + Jaeger):** end-to-end per request — `POST /screen` → queue → worker → LLM → DB. Distributed tracing is how you find which hop is slow.

**Alerting:** alert on *symptoms* (p99 > 2s, queue depth > 10k, error rate > 1%, 5xx) not just metrics; on-call runbooks for LLM outage and DB failover.

---

## Q445: How would you optimize cost in this system?

**LLM is the dominant cost** — attack it first:
1. **Prompt caching** for system/context prefixes (Q432) — biggest win on input tokens.
2. **Cheaper model routing:** small/fast model for short chat turns, extraction, classification; big model only for scoring/hard reasoning (Q657, Q684).
3. **Shorten prompts:** trim resume + job text to relevant sections; cap candidate context.
4. **Cache deterministic outputs** (same resume+job → same score) (Q432).
5. **Retry/idempotency discipline** — each duplicate LLM call is pure waste (Q443).
6. **Batching** where latency allows (nightly re-scoring batches).
7. **Usage caps per tenant/user + quotas + alerts** (Q272, Q393).
8. **Not-LLM:** reserve DB with reserved instances, S3 lifecycle rules (archive old resumes/transcripts → Glacier), right-size workers (they're idle at night — autoscale down).

---

## Q446: What security considerations does this design need?

- **AuthN/AuthZ:** JWT access + rotating refresh (Q406–411); RBAC for recruiter/admin/candidate; ownership checks on every resource (Q407).
- **Data protection:** TLS in transit; encryption at rest; **encrypt resume PII/transcripts at the field level**; redact PII before sending to the LLM (Q419); retention/deletion policies (GDPR).
- **Prompt injection:** resume/job text is untrusted input to the LLM — sanitize, isolate, treat outputs as untrusted (Q419).
- **SSRF:** LLM/resume pipelines fetching URLs — allowlist + block private IPs (Q418).
- **Webhooks/email integrations:** verify signatures, replay protection (Q420).
- **Audit:** every score change, status change, and data access is logged (Q631).
- **Rate limiting:** on auth, on LLM endpoints (cost), on search (Q393).

---

## Q447: What's the biggest bottleneck, and how do you defend your design?

**Answer with a prioritized list — this is the classic "defend your architecture" question:**

1. **LLM provider (throughput + cost + latency):** the bottleneck. Mitigations: async queue absorbs bursts, streaming hides latency, prompt caching + cheaper-model routing cut cost, circuit breakers + fallbacks handle outages (Q429, Q438, Q445).
2. **Parser worker throughput:** bounded by LLM/CPU. Mitigate: horizontal auto-scaling of workers, queue depth alarm, concurrency caps (Q435).
3. **Database:** grows with transcripts/messages. Mitigate: replicas, Redis cache, partitioning (Q440).
4. **Single points of failure:** Postgres primary, Redis. Mitigate: Multi-AZ standby, Redis replicas, SQS (managed) (Q436).

**If asked "what would you add next":** traffic replay/stress testing, feature flags for model changes, per-tenant isolation for enterprise clients, an LLM eval harness that gates every model prompt change (Q682).
