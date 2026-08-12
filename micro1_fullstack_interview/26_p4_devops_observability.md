# Priority 4 — DevOps & Observability (Q621–Q635)

**Why these matter for micro1:** the role touches deployment and running AI features in production. Expect CI/CD, deploy strategies, and the three pillars (logs, metrics, traces) — plus how you'd monitor an LLM feature.

---

## Q621: What is CI/CD? How do you design a pipeline?

**CI (Continuous Integration):** every push → automated **build + test** — catch breakage *before* merge. **CD (Continuous Delivery/Deployment):** every passing build is deployable automatically (delivery = manual click to prod; deployment = fully automated).

**Pipeline stages (GitHub Actions example):**
1. **Trigger** — push/PR to `main`.
2. **Lint + typecheck** — ruff, mypy (fail fast).
3. **Unit tests** — fast, isolated.
4. **Integration tests** — real DB (Testcontainers), Redis, fake LLM.
5. **Build** — Docker images (FastAPI, worker, frontend) → push to ECR; static build for Next.js.
6. **Security scan** — dependency audit (pip-audit, npm audit), secret scan (gitleaks).
7. **Deploy** — to staging automatically; to prod via **gate** (approval) then **blue/green or canary** (Q622).
8. **Post-deploy** — health checks + smoke tests (login, apply flow).

**Design principles:** fast feedback (< 10 min core suite), the pipeline is the *only* way to prod (no manual deploy exceptions), secrets injected from the store (Q617), every stage produces a verifiable artifact, and deploy is reversible (Q623).

---

## Q622: Deploy strategies — rolling, blue/green, canary?

- **Rolling:** instances updated one-by-one behind the LB (always serving). Simple, but old+new coexist during deploy; no instant rollback.
- **Blue/green:** two full environments — new ("green") deployed fully, tested, then traffic **switched** (Route 53/ALB) all at once; instant rollback = flip back. Cost: 2x infra during switch.
- **Canary:** route **1% → 5% → 50%** of traffic to the new version while monitoring error rate/latency; auto-rollback if metrics degrade; then full rollout. Best for **risky changes** (LLM prompt updates, schema-affecting features).

**Your app's choice:** blue/green for routine deploys (FastAPI is stateless, DB is the only shared state → keep migrations compatible, Q558); **canary for AI/model changes** (evaluation of real prompts/scores with the golden-test harness, Q682) and for anything touching the streaming path (watch time-to-first-token + error rate).

**Stateful caveats:** WebSocket/SSE sessions must survive: connection draining on the LB (Q602) and externalized session state (Redis, Q441) — else users get cut mid-interview on every deploy.

---

## Q623: How do you roll back a bad deployment?

**Fast + safe rollback (ordered):**
1. **Detect first:** health checks, error-rate/latency alarms, synthetic smoke tests (Q631). If an alarm fires within minutes, act *now* — don't debug under load.
2. **Instant revert:** point the LB/Route 53 back to the previous known-good version (blue/green flip, Q622) — **seconds**, no image rebuild. `git revert` the config/code separately, then re-deploy properly.
3. **DB rollback is the hard part:** *never* roll back schema migrations forward-in-time (Q558) — the fix is a **forward migration** that undoes the bad change, because data written by the bad version already exists. Application data (applications, scores) is rarely rolled back; you *recover* state via idempotent replays/backfills (Q443).
4. **Post-incident:** blameless post-mortem (Q527) — why did CI not catch it? add a regression test + a check in the pipeline.

**Answer:** "The best rollback is the one that's a flip, not a rebuild — blue/green or canary with automatic rollback on alarm; DB changes are forward-migrated, never reverted."

---

## Q624: What is the three pillars of observability?

**Logs, Metrics, Traces — the trio that answers: what happened, how healthy, where did it go.**

- **Logs** — discrete events (requests, errors, worker jobs): *what exactly happened*. Structured (JSON), centralised, searchable, with `request_id`.
- **Metrics** — aggregated numeric values over time (QPS, p99 latency, error rate, queue depth): *is the system healthy now / trending*. Stored time-series, alerts.
- **Traces** — end-to-end request flow across services (API → queue → worker → LLM → DB): *where the time went*. Span IDs + `trace_id` correlation.

**The three form a hierarchy:** a trace tells you *which* hop is slow; metrics tell you it's slow *now*; logs tell you *why* (the actual error). All three share the **correlation IDs** (Q65). Without correlation, you have three unlinked clues.

---

## Q625: What is structured logging? Why does it matter?

**Structured logging** = log **machine-parseable fields** (JSON), not free-form text:

```python
logger.info("application_created",
            extra={"application_id": app.id, "candidate_id": cand.id,
                   "job_id": job.id, "latency_ms": 42})
# or with a JSON formatter:
{"level":"INFO","logger":"app.services","event":"application_created",
 "application_id":"app_9","candidate_id":"cand_2","latency_ms":42}
```

**Why:**
- **Filterable/searchable** — "all application_created events for candidate X" is one query.
- **Alertable** — metrics/aggregations from logs (CloudWatch Logs Insights).
- **Correlation** — every entry carries `request_id`/`trace_id` so logs join with traces (Q624).
- **Privacy-safe** — fields you *choose*; never log passwords, tokens, resume content, or PII (Q417, Q419). Redact by default.

**Your app:** a middleware that logs method, path, status, latency, user_id, request_id per request (Q65) + structured worker job logs (`job_id`, `attempt`, `error`). Every log line is JSON — grep-able, joinable, alertable.

---

## Q626: What metrics would you track for a web service?

**The RED/USE mnemonic (Google SRE):**
- **RED (request-level):** **R**ate (QPS), **E**rrors (count/rate, with 5xx vs 4xx split), **D**uration (latency distribution — p50/p95/p99; track **time-to-first-token** separately for streaming).
- **USE (resource-level):** **U**tilization, **S**aturation, **E**rrors for CPU, memory, connections, threads, disk.

**For the recruiter, add domain metrics:**
- **LLM:** cost per hour, tokens per request, per-tenant spend, time-to-first-token (Q445, Q631).
- **Queue/workers:** queue depth, task latency, success/retry/DLQ rate, worker concurrency (Q433, Q439).
- **DB:** connection pool utilization, query p95, replication lag (Q562, Q567).
- **Business:** resume parse success rate, screening completion rate, match precision (human review agrees with AI), application funnel.

**Alarm on symptoms:** p99 > target, error rate > threshold, queue depth > limit — with runbooks for each (Q631).

---

## Q627: What is distributed tracing? How does it work?

**Distributed tracing** follows a single request **across services** (Q624): a **trace** = tree of **spans**; each span = one unit of work (HTTP call, DB query, LLM call) with start/duration/attributes.

**How it works:**
- **Instrumentation** injects a **trace/span ID header** (e.g., `W3C traceparent`, or your own `X-Request-Id`) at entry (LB/API).
- Each service creates child spans, tagging service/operation/attributes, and forwards the ID downstream (FastAPI → queue message → worker → LLM call).
- **Collectors** (OpenTelemetry) ship spans to Jaeger/Tempo/CloudWatch X-Ray; the UI renders the waterfall with per-hop timing.

```python
# FastAPI + OpenTelemetry: automatic for http/db; manual for LLM
with tracer.start_as_current_span("llm.screen") as span:
    span.set_attribute("model", "gpt-4o")
    span.set_attribute("input_tokens", n)
    result = await llm.complete(...)
```

**Why you need it:** your request crosses API → queue → worker → LLM → DB. When a screening takes 12s, tracing shows it's 9s in the LLM call, 2s queue wait, 1s DB — so you optimize the right hop (Q444).

---

## Q628: What is OpenTelemetry? Why is it the standard?

**OpenTelemetry (OTel)** = the open standard for **generating, emitting, and collecting telemetry** (traces, metrics, logs) in a vendor-neutral way.

- **One SDK/API per language** — instrument once (Python: `opentelemetry-python` + auto-instrumentors for FastAPI/httpx/DB), export to any backend (Jaeger, Prometheus, Tempo, X-Ray) via **OTLP** or vendor exporters.
- **Auto-instrumentation** covers the common cases (HTTP, DB, queues) with zero/minimal code; manual spans for LLM calls.
- **Semantic conventions** — standardized span/log names → consistent dashboards.
- **Why standard:** avoids vendor lock-in (no per-vendor agents), community-driven, the de-facto answer to "how do I instrument?"

**Interview answer:** "OTel is the CNCF standard for telemetry — one instrumentation layer that exports traces, metrics, and logs to any backend. I'd use its Python SDK with auto-instrumentation for FastAPI/DB and manual spans for LLM calls."

---

## Q629: What is a Service Level Objective (SLO)? SLI vs SLO vs SLA?

- **SLI (Indicator)** — the measured number: request **availability** (99.5% of requests succeed), **latency** (p95 < 300ms), parse success rate.
- **SLO (Objective)** — the target you commit to *internally*: "99.5% availability over 30 days." An SLO = SLI + target + window.
- **SLA (Agreement)** — the *contractual* commitment to customers (usually looser than your SLO so you have margin).

**Example:**
- SLI: "fraction of `POST /api/v1/screen` requests returning 2xx within 10s."
- SLO: "≥ 99.9% over 28 days."
- SLA: "≥ 99.5%" (customer contract).

**SLO practice (why it matters in interviews):** **error budgets** — if you burn 100% of the 0.1% error budget, you *stop shipping risky changes* until it recovers. SLOs make reliability a *decision* (what to prioritize), not an accident. Start with 3–5 SLOs on the critical user journeys (apply, screen, chat) (Q631).

---

## Q630: What is an incident response process?

**A runbook'd process (borrow the classic order):**
1. **Detect** — alerts/synthetic checks fire (Q626); anyone can declare an incident (low friction).
2. **Declare + communicate** — a channel (#incident), an incident commander (one decision-maker), a scribe (timeline log), status to stakeholders. **Severity triage** (SEV-1 = down, SEV-2 = degraded).
3. **Mitigate before root-cause** — the goal is to *restore service*: rollback (Q623), scale out, disable a feature flag, redirect traffic. You can debug later.
4. **Stabilize + monitor** — confirm metrics recover, keep watching.
5. **Post-incident (blameless post-mortem)** — timeline, what happened, **contributing factors** (not "who"), action items (fixes + tests + runbook improvements) with owners and dates. No one gets punished for the incident.
6. **Track** — action items in a backlog; review in a monthly reliability meeting.

**Answer structure:** "Detect → declare/communicate → mitigate first → stabilize → blameless post-mortem with tracked action items. The discipline is: fix service first, understand later."

---

## Q631: How would you monitor an AI/LLM feature specifically?

**LLM features need their own observability (they're slow, costly, non-deterministic):**

1. **Cost & usage:** tokens in/out per request, per user, per feature; cost per screening; quota/budget alarms (Q445, Q393).
2. **Latency:** **time-to-first-token** (streaming UX), total generation time, per-model; p95/p99. Alert on regressions.
3. **Reliability:** LLM call error rate, retry rate, timeout rate, circuit-breaker open time, fallback usage (Q438).
4. **Quality (the hard one):**
   - **Golden tests** — fixed inputs, expected outputs; run on every prompt/model change (Q456, Q682).
   - **Determinism tracking** — score variance for the same input (temperature/seed drift).
   - **Human-feedback loop** — store recruiter accept/reject of AI scores → measure AI-precision over time.
5. **Safety:** PII detected in prompts/outputs (redaction alerts), prompt-injection incidents, content-safety rejections (Q419).
6. **Trace each LLM call:** model, prompt size, tokens, duration, response, truncation flag — correlated with the application request (Q627).

**Answer:** "I instrument every LLM call as a span with model/tokens/latency, track cost and time-to-first-token as metrics, run golden-test evals in CI, log human feedback on AI decisions, and alarm on error rate + cost spikes."

---

## Q632: How do you handle logs retention and privacy?

**Retention tiers (match cost to need):**
- Hot (searchable, 7–30 days): request logs, errors, traces.
- Warm (1–3 months): aggregated/debug logs, quieter but searchable.
- Cold (up to regulatory limit): audit logs, compliance (CloudTrail/audit_logs) — often months-years, in S3/Glacier.
- **GDPR/CCPA:** define a retention *max* and enforce deletion — resumes/transcripts get a lifecycle policy (Q607), not indefinite storage.

**Privacy in logs (this is the interview core):**
- **Never log:** passwords, tokens, full resumes, emails/phone (PII), LLM prompt content with PII, secrets.
- **Structure the log schema** so sensitive fields are excluded by default; add an explicit `redact()` utility; **sanitize** exception messages (stack traces can embed user data).
- **Access control:** logs are sensitive too — restrict read access, audit who queries them.
- **Alert on PII leaks:** grep patterns in CI/test + periodic scans.

**Answer:** "Hot-warm-cold retention with enforcement, and a deny-by-default log schema: no PII, no secrets; sanitized exceptions; access-controlled, audited log store."

---

## Q633: What are feature flags? How do you use them?

**Feature flags** — runtime toggles that switch behavior without a deploy (kill-switches, gradual rollouts, testing in prod).

```python
if await feature_flag("ai_screening_v2", user_id=user.id):
    return await screen_v2(job, candidate)
return await screen_v1(job, candidate)   # old path still there
```

**Uses:**
- **Gradual rollout:** % of users → AI-v2 prompt while measuring (Q622).
- **Kill switch:** instantly disable a broken feature (esp. costly LLM features).
- **Decouple deploy from release:** merge code dark, enable later.
- **Canary/per-user targeting** (enterprise tenants first).
- **Experiment A/B** (Q622 + evals).

**Best practices:** flags should be **short-lived** (delete once the feature is stable — dead flags accumulate), values from a config service (not hardcoded in code), **audited**, and default to **off** for new features. A kill-switch flag on the LLM path is a *requirement* for an AI feature (Q419).

---

## Q634: How do you build a deployment pipeline for the recruiter project?

**Concrete, tied to the stack (compose Q621–623, Q604):**

1. **PR → CI (GitHub Actions):** ruff + mypy + unit tests + integration tests (Testcontainers Postgres/Redis, fake LLM) + **golden eval suite** for scoring prompts (Q456). Gate on coverage floor.
2. **Merge → build:** Docker images for `api`, `worker`, `frontend` → push to ECR (tagged by commit SHA); static Next.js assets.
3. **Staging deploy:** full stack to staging (ECS Fargate + RDS + Redis + S3) → smoke tests (apply → parse → screen with a stub LLM).
4. **Prod deploy:** **blue/green** (or canary for AI changes) behind ALB; **DB migrations run first** (forward-only Alembic, Q558).
5. **Post-deploy:** health checks + synthetic smoke test; watch **time-to-first-token, error rate, queue depth** (Q631); auto-rollback on alarm (Q623).
6. **Feature release:** behind a flag (Q633); AI prompt/model changes gated by the eval harness.
7. **Infra as code:** Terraform/CloudFormation for VPC, RDS, ECS, buckets — PR-reviewed, reproducible, no click-ops.

**Interview value:** naming the eval harness, migration-first ordering, and rollback strategy shows you've thought about *production* AI, not just code.

---

## Q635: What is infrastructure as code (IaC)? Why does it matter?

**IaC** = describing infrastructure in **version-controlled, reviewable code** (Terraform, CloudFormation, Pulumi) instead of clicking in the console.

**Why:**
- **Reproducible** — staging and prod are identical by construction; a new region is a config change, not a rebuild.
- **Versioned + reviewable** — every infra change is a PR with history; rollback is `git revert` + apply.
- **Drift detection** — `terraform plan` shows what's changed vs reality; auto-enforced where possible.
- **Automation** — infra is part of CI/CD (Q634); no snowflake servers.
- **Least-privilege friendly** — review gates on IAM changes catch dangerous policies (Q608).

**Good practices:** state management (remote state with locking — Terraform), environments as separate workspaces/dirs, modules for reusable pieces (VPC, ECS service), **never hand-edit infra** (that's how drift happens), secret values from a store, not state files (secrets in tfstate are a classic leak, Q617).

**Answer:** "IaC turns the environment into code: reproducible, reviewable, versioned, and deployable through the same pipeline as the app — I'd use Terraform with remote state and modules for VPC/ECS/RDS/S3."
