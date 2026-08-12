# micro1 Fullstack Developer (Python/React) — Interview Q&A Bank

Complete answer bank for the **micro1 Fullstack Developer** role (AI Recruiter / Zara, Python+FastAPI, React/Next.js/TypeScript, PostgreSQL, AWS).

**Last date to complete interview:** Aug 12, 2026 — format: AI Interview + Coding Exercise, up to 48 min.
**Focus areas:** Python & FastAPI, Concurrency & Optimization, React, SQL.

## How to use this bank

- Files are numbered in the **exact priority order** of the source question bank.
- **Status: COMPLETE — all 765 questions written (Q1–765), Tiers 1–5.**
- Study tiers 1 → 2 first; everything else is backup.
- For **every** Tier-1 question, also prepare the follow-ups the AI interviewer is likely to drill:
  - **"Why?"** — internal mechanism / tradeoffs.
  - **"How would you optimize it?"**
  - **"What happens internally?"**
  - **"What would you do if this failed at scale?"**

## Study order

| Tier | Priority | Files | Questions | Theme |
|---|---|---|---|---|
| 1 | Priority 1 | `01`–`07` | 1–265 | Python → FastAPI → Async → SQL → React → TypeScript → Performance |
| 2 | Priority 2 | `08`–`15` | 266–420 | AI/LLM → Next.js → PostgreSQL → SQLAlchemy → AWS → Docker → API → Security |
| 3 | Priority 3 | `16`–`20` | 421–528 | System design → Testing → Git → Networking → Behavioral |
| 4 | Priority 4 | `21`–`26` | 529–635 | Advanced Python/DB/React/TS → AWS/DevOps |
| 5 | Priority 5 | `27`–`31` | 636–765 | Deep internals → Advanced AI → Coding → Scenarios → Own projects |

## Directory map

| File | Questions | Topic |
|---|---|---|
| `01_p1_python_fundamentals.md` | 1–40 | Data structures, object model, functions, decorators, generators, context managers |
| `02_p1_fastapi.md` | 41–78 | Framework, Pydantic, dependencies, middleware, project structure, testing |
| `03_p1_async_concurrency.md` | 79–120 | asyncio, event loop, coroutines, locking, pooling, retries, timeouts |
| `04_p1_sql.md` | 121–175 | Joins, aggregations, subqueries, window functions, ACID, indexes, EXPLAIN |
| `05_p1_react.md` | 176–215 | Components, props/state, hooks, lists/keys, forms, context |
| `06_p1_typescript.md` | 216–242 | Types, interfaces, generics, narrowing, utility types, props typing |
| `07_p1_performance_optimization.md` | 243–265 | Backend/DB/frontend optimization, caching, pagination, batching |
| `08_p2_ai_llm_agents.md` | 266–305 | LLM APIs, prompts, tool calling, agents, context, evals, safety |
| `09_p2_nextjs.md` | 306–324 | App Router, server/client components, SSR, data fetching, FastAPI integration |
| `10_p2_postgresql.md` | 325–340 | JSONB, indexes, MVCC, VACUUM, optimization at scale |
| `11_p2_sqlalchemy_orm.md` | 341–354 | ORM, sessions, lazy/eager loading, N+1, async, session lifecycle |
| `12_p2_aws.md` | 355–373 | EC2, S3, RDS, Lambda, ECS, IAM, deployment, scaling |
| `13_p2_docker_deployment.md` | 374–385 | Images/containers, Dockerfile, Compose, volumes, multi-stage builds |
| `14_p2_api_design.md` | 386–399 | REST design, idempotency, pagination, versioning, streaming |
| `15_p2_security.md` | 400–420 | Injection, XSS, CSRF, CORS, JWT, OAuth, secrets, AI-agent risks |
| `16_p3_system_design.md` | 421–447 | AI recruiter, scaling, queues, caching, HA, circuit breakers |
| `17_p3_testing.md` | 448–465 | Unit/integration/E2E, pytest, mocking, async + LLM testing |
| `18_p3_git.md` | 466–480 | Branching, merge/rebase, stash, revert/reset, PR review |
| `19_p3_networking_http.md` | 481–497 | HTTP, HTTPS, DNS, TLS, cookies, CORS, WebSocket vs SSE |
| `20_p3_behavioral.md` | 498–528 | Experience, STAR stories, ownership, remote work |
| `21_p4_advanced_python.md` | 529–548 | GIL, GC, descriptors, metaclasses, ABCs, slots, pickling |
| `22_p4_advanced_database.md` | 549–568 | MVCC internals, locking, partitioning, sharding, migrations, replication |
| `23_p4_advanced_react.md` | 569–588 | Reconciliation, Fiber, stale closures, race conditions, state libs |
| `24_p4_advanced_typescript.md` | 589–599 | Conditional/mapped/template-literal types, variance, overloads |
| `25_p4_advanced_aws.md` | 600–620 | VPC, ALB, ASG, CloudFront, SQS/SNS, DR, IAM, cost |
| `26_p4_devops_observability.md` | 621–635 | CI/CD, deploys, logs/metrics/traces, metrics, tracing, rollback |
| `27_p5_deep_internals.md` | 636–655 | Bytecode, GC internals, ASGI/WSGI, Uvicorn, Gunicorn, workers |
| `28_p5_advanced_ai.md` | 656–684 | Embeddings, vector search, RAG, chunking, reranking, routing, fallbacks |
| `29_p5_coding_exercises.md` | 685–720 | Strings, arrays, hashing, linked lists, trees, concurrency, scheduler |
| `30_p5_fullstack_scenarios.md` | 721–740 | Registration, login, chat, streaming, resume parsing, scoring, audit |
| `31_p5_own_projects.md` | 741–765 | Deep-dive on your own projects, architecture, tradeoffs, scaling |

## Golden rules for the micro1 AI interview

1. **Answer with the "why" built in** — the AI recruiter probes every claim.
2. **Give structure** (3 bullets or a mini-outline) before detail.
3. **Lead with Python/FastAPI/concurrency/SQL/React** — that is what it scores on.
4. **For coding**: narrate the approach, complexity (time/space), edge cases, then code.
5. **Be honest + specific** — reference your own projects (see `31_p5_own_projects.md`).
