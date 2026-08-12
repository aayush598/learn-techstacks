# Priority 5 — Own Projects Deep-Dive (Q741–Q765)

**Why these matter for micro1:** the AI interviewer will ask about *your* projects to verify experience and probe depth. These answers must be **personal** — the frameworks and the Zara-example answers below are templates; replace the specifics with your real projects and numbers.

**Before the interview, prepare one "flagship" project in full depth** (architecture, DB, tradeoffs, mistakes, scale) and 2 supporting projects (one backend-heavy, one frontend-heavy).

---

## Q741: Tell me about your most impressive project.

**Framework:** problem → what you built (3–5 boxes) → YOUR role → results (quantified) → hardest technical decision + why.

**Zara-example answer:**
"The most impressive project I've built is an AI recruiter that screens candidates automatically. The problem: recruiters manually review hundreds of resumes and schedule first interviews — slow and subjective. I built a FastAPI backend with an async resume-parsing pipeline (S3 upload → queue → LLM extraction → embeddings in pgvector), a hybrid candidate–job matching system, and a streaming AI chat interview over SSE/WebSocket. I personally designed and built the screening pipeline and made LLM calls production-safe: idempotent turns, retries with backoff, circuit breakers, and a fallback when the provider is down. It screens a candidate end-to-end in about a minute versus hours manually, and the scores come with reasons so recruiters can audit them. The hardest decision was choosing pgvector over a dedicated vector DB — I deliberately started simpler, and it was right."

---

## Q742: What was your specific contribution?

**Be precise about YOUR work (interviewers probe this hard):**
- "I designed the database schema and all migrations (Alembic)."
- "I built the resume parsing pipeline and its failure handling (DLQ, manual review fallback)."
- "I implemented the streaming chat protocol and the WebSocket reconnection logic."
- "I added the eval suite for LLM scoring — that's what made prompt changes safe."
- "I set up CI/CD: tests, images, blue/green deploys."

**Rules:** never say "we did X" for something you didn't personally do; claim your work with specifics (file/endpoint/algorithm-level detail), and be honest about what was *your* idea vs the team's.

---

## Q743: What was the hardest bug you fixed?

**Framework:** symptom → investigation method (traces/logs/repro) → root cause → fix → prevention.

**Zara-example:** "The screening chat would occasionally skip a user's turn and bill us for a duplicate LLM call. Root cause: the client retried a timed-out request, and nothing keyed the turn, so the worker called the LLM twice and lost the first response. I added a `turn_id` with a unique constraint (idempotency) and replay-on-reconnect; zero duplicates since. The lesson was that retries + side effects need idempotency by design — it became the rule for every queue consumer."

**Have 2–3 ready:** a concurrency bug, an async bug (stale closure / blocking the loop), a data bug (migration), a distributed bug (eventual consistency).

---

## Q744: What was the hardest technical decision and why?

**Framework:** the options → the tradeoffs → your choice → the outcome → would you change it.

**Zara-example:** "Postgres FTS + pgvector vs a dedicated search/vector stack (Elasticsearch + Qdrant). I chose Postgres-first: one transactional store, no sync pipelines, fast to ship, and our volume was small. The tradeoff was eventual relevance tuning and scale limits. It proved right — we scaled past the point I feared, and moving later is a contained migration. But I set it up behind an interface so the swap isn't a rewrite."

**The senior signal:** you made a *reasoned* tradeoff, understood the cost, and re-evaluated — not "we used the popular thing."

---

## Q745: How did you make tradeoffs around scope and time?

**Zara-example:** "When the demo deadline pulled in by two weeks, I defined must-haves (upload, parse, score, shortlist) vs cuttable (email digests, admin analytics) with the stakeholder, shipped the core path first behind a flag, and delivered on the new date. I learned that the *conversation* about scope is the deliverable — quietly cutting quality is how you lose trust; cutting scope explicitly is how you keep it."

---

## Q746: How did you handle scaling in your project?

**If your project scaled (or you designed for it):** name the real or designed bottlenecks and the fixes (Q440, Q735):
- DB reads → read replicas + Redis cache.
- List queries → cursor pagination + composite indexes (Q735).
- Heavy work → async queue + workers (Q433).
- LLM cost → prompt caching + model routing (Q445, Q669).

**If it didn't scale:** be honest — "I hit a real bottleneck at ~X concurrent users and solved it with Y; here's what I'd do at 10x (Z)." Interviewers respect honest "it broke and here's how I fixed it" more than fake scale.

---

## Q747: Why did you choose Python + FastAPI (or your stack)?

**Your answer:** "FastAPI because it's async-first, gives typed request/response validation via Pydantic for free, generates OpenAPI docs, and has first-class WebSocket/SSE support — all of which the AI chat needed. Python because the AI ecosystem (LLM SDKs, embeddings, data tooling) is best-in-class and the team stack matches." *(Substitute React/Next.js reasoning for the frontend: RSC/SSR for SEO + streaming, component model for the dashboard, TS for safety.)*

---

## Q748: What would you improve in your project if you had more time?

**Framework:** honest weaknesses → prioritized improvements → what you'd measure.

**Zara-example:** "Three things: (1) an eval harness with real recruiter-labeled scores gating every prompt change — I added a basic golden set but it should be the CI gate; (2) model routing — cheaper model for chat turns, flagship for scoring; (3) a proper incident post-mortem process and runbooks, which I only formalized late. I'd also want human-feedback data flowing into eval sets so quality is measured in production, not just offline."

---

## Q749: How do you structure your projects? (architecture philosophy)

**Framework:** what you prioritize and why:
- **Layers:** API (FastAPI) / domain logic (services) / data (repositories/ORM) — testable boundaries.
- **Async everywhere it matters:** queues for heavy work, streaming for chat (Q433, Q399).
- **Single source of truth:** Postgres; Redis only for cache/sessions/queues (Q737).
- **Contract-first:** Pydantic models at the API boundary, zod on the frontend mirroring them (Q582, Q665).
- **Simple by default:** choose the boring, well-understood option; add complexity only when a metric demands it (Q512).

---

## Q750: How do you decide between different technologies?

**Framework:** the decision criteria, in order:
1. **Fit for the actual problem** (not popularity) — e.g., "queue? Do I even have async work?"
2. **Operational cost I can carry** — managed vs self-hosted; "can a small team run this at 2am?"
3. **Ecosystem + docs + community** — hiring/maintenance angle.
4. **Testing story** — can I test it deterministically (fake LLM, Testcontainers)?
5. **Escape hatch** — is the choice behind an interface so I can swap it?
   Then: **a spike/prototype with the real workload, measured** — "I benchmarked X vs Y against our query pattern before committing."

---

## Q751: How do you ensure code quality in your projects?

- **CI gates:** lint (ruff), typecheck (mypy), tests, coverage floor (Q458).
- **Type safety both ends:** Pydantic backend, TS frontend, zod at boundaries (Q582).
- **Tests that test behavior** not implementation; golden evals for AI (Q456).
- **Code review** (even solo: self-review + PR discipline, Q472/Q477).
- **Small PRs**; docs where non-obvious (but code-first).
- **Runbooks + logging** for what you ship (Q625).
- **Refactor discipline:** leave code cleaner than found (boyscout rule); delete dead code/flags (Q633).

---

## Q752: What's your most complex frontend feature?

**Framework:** the feature → why it was hard → how you built it → perf/testing approach.

**Zara-example:** "The AI chat view: streaming tokens, WebSocket reconnect without losing turns, and race safety when a user sends a new message while the previous turn is still streaming. I built a `useStreamingChat` hook (Q587) with a per-turn guard so stale chunks can't render, an idempotent `turn_id` on every message, and replay-on-reconnect from the server. Testing was hard — I used a canned SSE fixture in Playwright plus hook tests with mocked streams (Q461, Q462)."

---

## Q753: How do you handle state in your frontend?

**Framework (Q582):** 
- **Server state** → TanStack Query (caching, invalidation, optimistic updates).
- **Client/UI state** → local + hooks, colocated (Q572).
- **Global cross-cutting** → Context for low-churn (auth/theme) or a minimal store (Zustand) for chat/connection state.
- **Forms** → react-hook-form + zod (Q581).
- **Why:** "most 'state' is really server data, so Query handles it; I keep client state small and near where it's used."

---

## Q754: How do you structure your backend code?

**Framework:** a clean FastAPI layout you can describe in one breath:
```
app/
  main.py            # app factory, routers, middleware, lifespan
  core/              # config, security, logging
  db/                # engine, session, models, migrations (Alembic)
  schemas/           # Pydantic request/response models
  api/routes/        # routers per resource
  services/          # business logic (parsing, scoring, matching)
  workers/           # queue consumers
  llm/               # provider client interface (routing, retries, fallback)
  tests/
```
**Principles:** routers are thin (parse → delegate → respond); logic lives in services (testable without HTTP); the LLM client is behind an interface (Q684); dependencies via FastAPI DI (Q60).

---

## Q755: How do you handle errors in your project?

**Backend (Q77, Q392):** one `AppError` + one exception handler → consistent envelope `{error: {code, message, details, request_id}}`; Pydantic 422 mapped; 4xx vs 5xx distinction; no stack traces leaked (Q402); `request_id` middleware linking errors to logs (Q65).
**Workers (Q561):** retry with backoff → DLQ → alert → replay.
**Frontend:** typed error handling per request (Q597), user-friendly messages for 4xx, "something went wrong" + retry for 5xx, error boundaries for crashes.

**Answer:** "Errors are a contract: consistent codes, correlation ids, and distinct handling for client bugs (4xx), server bugs (5xx), and retryable work (queue retries + DLQ)."

---

## Q756: How do you secure your projects? (applied, not theoretical)

**Your answer should include:** hashed passwords (Q414), JWT access + rotating refresh in HttpOnly cookies (Q408–411), RBAC + ownership checks on every route (Q395, Q407), parameterized SQL everywhere (Q401), input validation via Pydantic (Q46), PII redaction before LLM calls (Q419), SSRF guards on URL fetches (Q418), rate limiting on auth + LLM endpoints (Q393), secrets in a store never in code (Q417), and audit logging (Q731).

**Tie each to where it *actually* bit you** — "resumes contain PII, so redaction before third-party embedding was a hard requirement."

---

## Q757: How do you test AI/LLM features in your project?

**Your concrete answer (Q456, Q682):**
- **Fake LLM client** behind the provider interface → deterministic unit/integration tests.
- **Golden eval set:** ~50–100 (resume, job) pairs with human-verified rubric scores, run in CI on every prompt change — structure checks + score tolerance.
- **Prompt contract tests:** assert PII is redacted and required sections present (Q456).
- **Failure-mode tests:** provider 429/timeout → retry + fallback path fires (Q438).
- **E2E:** canned SSE fixture for the chat journey (Q462).
- **Production feedback:** recruiter accept/reject of AI scores → grows the eval set (Q631).

---

## Q758: What metrics do you track in your projects?

**Tie metrics to your app (Q626, Q631):**
- **API:** QPS, p50/p95/p99 latency, error rate by status, time-to-first-token for streaming.
- **Workers:** queue depth, task latency, retry rate, DLQ count.
- **LLM:** cost/hour, tokens by model/feature, per-tenant spend, provider error rate.
- **DB:** connections, query p95, replica lag.
- **Business:** parse success rate, screening completion, AI-score acceptance rate by recruiters (the ultimate quality metric).

**Answer:** "I track RED (rate/errors/duration) plus domain metrics, and I alert on symptoms — p99 breach, error-rate spikes, queue growth, cost overruns."

---

## Q759: How do you keep your skills current? What's next you want to learn?

**Your honest plan:** "I learn by building: my projects are my lab — that's how I picked up async streaming, vector search, and LLM reliability. I follow release notes for FastAPI/Next.js and the AI SDK ecosystem, read a couple of engineering blogs, and write up what I learn. Next I want to go deeper on: (1) production LLM operations — evals at scale, fine-tuning vs RAG tradeoffs; (2) observability — OpenTelemetry in anger; (3) distributed systems basics — event-driven architectures, since the recruiter's sync problems are the frontier."

---

## Q760: What's a project you'd build from scratch with no constraints?

**This is a passion + system-design signal. Show you think big but grounded:**
**Zara-example:** "A career copilot that I'd build properly this time: a system that learns a candidate's signals over time (not just one resume), continuously matches them against the live job market, and coaches them through interviews using their actual target roles — with privacy by design (local or contractual data handling). The interesting systems problem: a continuous ingestion + re-ranking pipeline over a moving corpus, plus an eval loop that measures coaching quality against real outcomes. I'd start with the sync between Postgres and the vector index and a feedback pipeline for model quality."

---

## Q761: Describe your development workflow (dev → prod).

**Framework (Q634):** "Local dev with Docker Compose (API + Postgres + Redis + worker) and hot-reload → feature branch + PR → CI (lint, typecheck, unit + integration tests with Testcontainers, AI golden evals) → staging deploy (full stack) with smoke tests → production blue/green behind ALB with migration-first deploy → post-deploy health + metrics + auto-rollback → feature flags for risky changes. Everything infra-as-code (Terraform), secrets from a store."

---

## Q762: How do you approach debugging a production issue?

**Framework (Q497, Q527):**
1. **Contain first:** check the alarm/runbook; if it's a deploy or config, **rollback immediately** (Q623) — don't debug under load.
2. **Correlate:** find the `request_id`/`trace_id` → trace (which hop is slow/failing, Q627) → logs (structured, the actual error, Q625) → metrics (was this a ramp-up? Q626).
3. **Reproduce:** curl the exact request; check if it's data-dependent (which candidate? which payload?).
4. **Fix at the root** + regression test + update the runbook; blameless post-mortem (Q630).
   **Mantra:** "restore service first, understand second, prevent third."

---

## Q763: What was your experience with remote/distributed collaboration?

**Framework (Q518) applied to your project:** "I worked async-first: written design notes + PR descriptions with the reasoning, clear owners on the board, recordings of decisions. I kept my overlap hours for unblocking and used Loom/text for context that didn't need a meeting. It worked because we over-communicated the *why* in writing — the async medium punishes context-hoarding."

---

## Q764: What's your biggest strength as an engineer? (tie to evidence)

**Framework:** one strength + one story + why it matters to THIS role.
**Zara-example:** "Taking ambiguous AI features and making them reliable systems. Evidence: I took 'an AI that screens candidates' and turned it into a pipeline with idempotency, retries, evals, and a fallback — the LLM is the most failure-prone dependency, so I designed it to fail soft. That's exactly the discipline a production AI product needs, and it's what the team's roadmap demands."

---

## Q765: What do you want to get out of this role?

**Framework:** the outcome you want + why it matters to you:
**Zara-example:** "I want to own a real production AI system — to take the patterns I built on my own and learn what they look like at real scale and real cost. Concretely: in a year, I want to be the person who owns screening or matching end-to-end, with eval-driven quality, a kill-switch, and cost-aware routing — and to have grown through strong code review and hard design conversations. I want to be measured by impact: faster, fairer, more accurate hiring decisions."
