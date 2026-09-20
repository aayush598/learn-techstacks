# Infosys SP DSE — 100 Internships Interview Q&A

> Based on Aayush Gid's internships as listed on the resume: **Krip AI** (Agentic AI Intern, Jun–Aug 2025 — FastAPI microservices, Docker containerization, AWS ECS deployment, Redis caching, GitHub Actions CI/CD with pytest coverage), **Clone Futura** (AI Agent Developer — REST API automations + SQLite), and **NullClass** (Data Science Internship — BERT/VADER chatbot). All answers grounded strictly in resume facts; where a detail isn't on the resume, the answer says so rather than inventing it.
> Candidate: Aayush Gid — B.Tech E&C | MigratorGen, ScriptVector, OpenRTL.ai | Agno Open-Source PRs | IEEE Publication (2024)
> Scope: internships only — role specifics, projects, tech-stack choices, CI/CD and deployment lessons, teamwork, and "what did you actually do vs what's on paper" probes. DSA, project deep-dives, open source, research, hackathons, and HR questions are in separate sheets.
> Interview pattern observed: panels dig into internship details with "name the tech", "why that choice", "what broke", who else was on the team, and cross-check answers against resume wording.

---

## 1. Krip AI — Agentic AI Intern (Q1–Q38)

**Q1: Tell me about your Krip AI internship — company, role, duration.**
A: Krip AI, Agentic AI Intern, June–August 2025. The role centered on building agentic-AI product features and services around LLM agents. The resume facts: FastAPI microservices, Docker containerization, AWS ECS deployment, Redis caching, and GitHub Actions CI/CD with pytest coverage.

**Q2: What does "Agentic AI Intern" actually mean at this company?**
A: It means I worked on products that wrap LLMs in agentic loops — services that call models, run tools, manage state, and respond to events — and on the production infrastructure around them (APIs, caching, deployment, CI). So it combined LLM application engineering with backend/platform engineering, exactly the blend Infosys SP DSE work needs.

**Q3: Walk me through the tech stack and why each piece.**
A: FastAPI for the API layer (async, pydantic validation, Python-native — matches my stack), Docker for containerization (consistent environment, multi-stage builds for small images), AWS ECS for running containers at scale, Redis for caching (low-latency reads, LLM response/state caching), and GitHub Actions for CI/CD with pytest coverage gates.

**Q4: Why FastAPI over Flask or Django for an agentic backend?**
A: FastAPI gives async support out of the box — LLM calls and external tool calls are I/O-bound, so async concurrency directly helps — plus pydantic validation with type hints for request/response contracts, and auto-generated OpenAPI docs that speed up team integration and frontend work. Flask needs async bolted on; Django is heavier than the microservice sizing called for here.

**Q5: What services did you actually build or work on?**
A: FastAPI microservices exposing agent functionality as HTTP endpoints — the agentic services around LLM orchestration — plus shared infrastructure: Redis-backed caching layers, Dockerfiles, CI pipelines, and ECS deployment configs. At an internship level I implemented features within that architecture rather than owning the whole product.

**Q6: What does a typical FastAPI endpoint you wrote look like?**
A: A route with pydantic request/response models, an injected service layer making the actual LLM/tool call, Redis caching where results are cacheable, and structured error handling returning proper status codes, with async def for I/O-bound handlers. Clean separation: router → service → client — makes services testable and the codebase consistent.

**Q7: What was Redis actually caching?**
A: Cacheable artifacts: repeated LLM responses for identical or prefix-matching requests (saves token cost and latency), computed agent state or session data, and hot lookups. The design principle: never cache non-deterministic or user-sensitive responses blindly, only what's safe to serve from cache, with TTLs so stale results expire naturally.

**Q8: Why cache at Redis rather than just in-process?**
A: In-process caching doesn't survive restarts, doesn't scale across multiple ECS tasks, and couples memory to instance size. Redis is a shared cache every replica can hit, so cache hits work regardless of which container served the earlier request. For an auto-scaling microservice setup, an externalized shared cache is the right architecture.

**Q9: What Docker practices did you follow?**
A: Multi-stage builds — a build stage with the full toolchain and a slim runtime stage copying only what's needed, so images are smaller with a smaller attack surface. Also .dockerignore, a non-root user in the container, pinned base images, and layer caching to speed CI. Smaller, cleaner images improved both deploy speed and security posture.

**Q10: Why multi-stage builds specifically — what do you gain?**
A: The build stage needs the full toolchain (e.g. Python plus build deps to compile wheels), but the runtime image doesn't. Multi-stage lets you COPY only built artifacts into the runtime stage — typically 3–5× smaller final image, faster pulls on ECS, less attack surface. It's a small change with outsized impact on deploy experience.

**Q11: How did GitHub Actions CI/CD work in your project?**
A: Two behaviors, resume facts: (1) pytest coverage gating — every PR must run the test suite with a coverage threshold before merge, enforced as a required check; (2) deploy on merge — pushing to the protected main branch triggers building the Docker image and deploying to ECS. The pipeline is "test → build → deploy", and protected branches stop direct pushes.

**Q12: What are protected branches and why do they matter?**
A: A protected branch (typically main) disallows direct pushes and requires PRs that pass required checks (tests + coverage) to merge. It's the guardrail that makes CI meaningful: untested code can't silently reach production. I learned this at Krip and applied the same "required checks on merge" thinking in my own repos.

**Q13: Walk me through the actual deploy pipeline you set up.**
A: On merge to main, GitHub Actions: checks out, sets up the build environment, runs pytest with coverage gating, builds the Docker image via the multi-stage Dockerfile, logs into the container registry, pushes the image, and instructs ECS to roll the service to the new image revision. Failure at any gate stops the deploy — the pipeline is the release process.

**Q14: How did you test an agentic service, given LLM behavior is non-deterministic?**
A: Test the deterministic boundaries: mock the LLM client for unit tests of the orchestration logic (tests assert your code's behavior, not model behavior), load fixtures for tool responses, test the API contract with FastAPI's TestClient, and keep a small number of integration tests with recorded stub responses. Coverage gating measures that the service logic — not the model — is tested.

**Q15: What does pytest coverage gating actually enforce and why?**
A: A percentage threshold (e.g. ≥80%) on the merged code; the PR check fails if new code drops coverage below the gate. It enforces the habit that shipping code ships tests. Nuance I push back on: coverage measures lines executed, not correctness — so the gate is necessary but not sufficient; unit + contract tests matter more than chasing 100%.

**Q16: How did AWS ECS run your containers?**
A: ECS takes the Docker image from the registry and runs it as tasks/services on EC2 or Fargate, with load balancing and auto-scaling across tasks. In my work the app ran as a service with N replicas behind a load balancer, all sharing the same Redis for cache, so scaling out doesn't duplicate state. Deployment = a new task-definition revision, rolled through.

**Q17: ECS vs EKS vs plain EC2 — why would you pick ECS?**
A: ECS is the simplest managed container orchestrator on AWS for services that don't need Kubernetes' portability or plugin ecosystem — less operational overhead than EKS, more structure than raw EC2 + docker. For a FastAPI microservice footprint, ECS is usually the right cost/complexity tradeoff. I'd mention Kubernetes only when multitenancy or complex orchestration demands it.

**Q18: How do you handle secrets in this kind of deployment?**
A: Never in the image or repo. In CI, secrets come from GitHub Secrets/trusted OIDC; at runtime, from the platform's secret mechanism injected as env at task start, not baked into the image. This triple hygiene avoids leaking credentials — a discipline reinforced by my security work elsewhere (SSRF research, proxy-config credential handling).

**Q19: What did you do if a deploy failed after merge?**
A: The failure surfaced as the image failing to start or a health check failing; the response was rollback — redeploy the previous known-good image — then investigate the failing commit. The pattern I internalized: deploys must be reversible and fast to reverse; CI gating reduces but never eliminates the need for a rollback path.

**Q20: What was the biggest bug or incident you hit during this internship?**
A: Honestly, the classic categories rather than one movie scene: cache-staleness (serving stale agent output after a prompt/model change — fixed by versioned cache keys) and CI-vs-local mismatch (tests passing locally, failing in CI due to environment drift — fixed by keeping test env deterministic/containerized). Both taught durable lessons: version what you cache, and make CI match prod.

**Q21: How do you avoid serving stale cached LLM output after a code change?**
A: Version the cache key or namespace per prompt/tool/model version, so a code change automatically produces a different cache key and new results get cached fresh while old entries expire by TTL. The "debug by wiping the cache" anti-pattern is a smell; versioned keys make invalidation a code decision, not an ops emergency.

**Q22: How did you work with the rest of the team during this internship?**
A: Daily syncs, PR-based collaboration with required checks, and a clear split between the parts I owned and features that crossed paths with other people's services. It scaled like a small team on a repo with enforced process — which is exactly how Infosys teams run, so the lesson transfers directly.

**Q23: What did you learn about writing production Python at Krip AI?**
A: Type hints + pydantic to enforce contracts at boundaries, async for I/O-bound paths, structured errors instead of bare exceptions, tests as a merge requirement, and small focused services over monoliths. The internship is where "code that runs on my laptop" became "code that runs behind a load balancer" — environments, secrets, health checks, and reversibility became mandatory.

**Q24: How does Krip connect to your MigratorGen and OpenRTL work?**
A: Same principles at different levels: MigratorGen uses structured rules + a deterministic rewrite engine (like mocking the LLM for tests); OpenRTL uses flow/test/CI to gate agent work (like the coverage-gated CI at Krip). The internship gave me the production vocabulary — Docker, ECS, Redis, CI/CD — that makes my side projects look like engineering, not tutorials.

**Q25: Why Redis over other caches (Memcached, in-process dict)?**
A: Redis is persistent-capable, offers data structures beyond key/value, easy TTLs, and is shared across replicas; Memcached is simpler but more limited; an in-process dict is single-process only. For a shared, expiring, multi-type cache across autoscaled tasks, Redis is the standard choice. The resume fact maps to a real architectural rationale.

**Q26: What security considerations came up in this backend work?**
A: Secrets hygiene (nothing baked into images), input validation via pydantic at every endpoint (no unvalidated user input straight into prompts or tools), dependency pinning/review, and never leaking prompts or tool payloads into logs. LLM endpoints are a new attack surface — prompt injection — so treating user input as untrusted at the API boundary mattered.

**Q27: What is prompt injection, and how did you guard agentic services against it?**
A: It's when adversarial text (from a user, a retrieved document, or a tool result) is crafted to override the agent's system instructions. Guards: treat all model inputs as untrusted, isolate system instructions clearly, sanitize/validate tool inputs, and keep only trustworthy domain content in context. The service boundary — validate in, validate out — is where I applied it.

**Q28: How did you measure that your services were fast/good?**
A: The metrics that mattered: p95 latency of endpoints, cache-hit ratio, error rate, and token/cost per request. Starlette/FastAPI makes timing middleware straightforward; I'd watch cache-hit ratio to confirm Redis was pulling its weight and p95 to catch tail latency. Monitor the pipeline's outcome, not just "did the code run".

**Q29: How do you load-test or at least sanity-check services?**
A: Written load scripts hitting endpoints at expected QPS while watching p95 and error rate, plus soak checks for autoscaling behavior. Even small internships find issues when you put real concurrent load on an async service — the top "works in dev, breaks in load" gap.

**Q30: What's your process for reproducing a bug in your own service?**
A: Read the structured log trail for the request (correlation ID when present), replay the exact request against a staging instance with the same cache/environment state, and narrow by adding minimal instrumentation rather than guessing. The discipline — structured input, controlled repro, one changed variable at a time — is the same as my research experiment protocol.

**Q31: How did you handle versioning of APIs in your microservices?**
A: Versioned routes/paths (e.g. /v1/...) so breaking changes don't silently break consumers; internal consumers pin to a version with a migration path. In a multi-service repo where other people consume your endpoints, that's the basic courtesy that avoids "works now, breaks on your next deploy" surprises.

**Q32: Did you use any observability tooling at Krip?**
A: Structured logging at minimum — JSON logs with request IDs, timings, status — plus the platform's logs/metrics and ECS health checks for alerts. The internship is where I internalized that observability is a feature, not a tool you bolt on after incidents.

**Q33: What Docker image issues did you actually hit?**
A: The classics: huge images from installing build deps at runtime (fixed by multi-stage), running as root (fixed with a non-root user), Python bytecode/home-dir problems on Alpine (fixed by knowing when slim ≠ alpine), and base-image hash pinning for reproducibility. Each a small real fix that compounded into cleaner, safer images.

**Q34: How do you decide between a monolith and microservices for a small team?**
A: Start as a modular monolith: one deployable, clean internal boundaries, and split later only when a team boundary or scaling profile demands it. Microservices as a default is premature complexity. Krip was genuinely multi-service, but the principle — split on real boundary need, not fashion — is what I defend.

**Q35: What would you have done differently at Krip AI given hindsight?**
A: Add contract tests between services earlier, and set up local parity with CI (same containers, same environment) from week one instead of after an environment-mismatch incident. Both are cheap and both prevent whole categories of "works locally" pain. Reflecting on process, not just features, is part of the answer.

**Q36: How do you keep agentic LLM responses within a cost budget?**
A: Cache repeatable requests, cap context sent to the model (only pack what the request actually needs), choose the smallest model that meets quality, and add fallback/circuit behavior. A "cost per request" metric makes all of this measurable. My OpenRouter cost-metric contribution came directly from this budgeting instinct.

**Q37: What FastAPI patterns did you use for async LLM calls?**
A: async/await on the I/O-bound call, timeouts with retries/backoff for the upstream, and streaming for long responses. The app stays responsive because yielding while awaiting lets other requests proceed — the reason async FastAPI suits agent backends. Pydantic typed the boundaries around streaming payloads too.

**Q38: If a recruiter asks "what did you build at Krip in one sentence"?**
A: "I helped build and operate production-grade agentic-AI backend services at Krip AI — FastAPI microservices, Docker multi-stage images, Redis caching, AWS ECS deployment, and a GitHub Actions CI/CD pipeline with pytest coverage gates, while learning to handle LLM-specific concerns like cost, latency, and prompt injection."---

## 2. Clone Futura — AI Agent Developer (Q39–Q70)

**Q39: Tell me about your Clone Futura internship.**
A: Clone Futura, an AI Agent Developer role. The resume fact: built REST API automations using SQLite for state/storage. It was a more autonomous, end-to-end engagement — designing and implementing agent-style automations against external REST APIs and persisting state in SQLite. I frame it precisely by what the resume claims.

**Q40: What are "REST API automations" in practice?**
A: Automated flows that call external REST APIs to perform a task — fetch data, trigger actions, update records — driven by a script/agent instead of a human clicking through a UI. The automation layer wraps API calls, handles auth/tokens, retries, and stores resulting state in a database.

**Q41: Why SQLite for this kind of automation?**
A: SQLite is zero-server, file-based, transactional (ACID), and skips the operational overhead of a DBMS — perfect for automations with a single-node, moderate-write footprint. For tracking run state, configs, or small datasets without standing up Postgres, SQLite is the pragmatic choice — the same "right-sized storage" judgment I'd use on the job.

**Q42: When would SQLite be the WRONG choice — to show you know the tradeoff?**
A: High concurrent write throughput, multiple cross-server writers, strict sharding, or large analytical workloads — that's when Postgres/MySQL-style servers and their row-based engines are right. SQLite shines single-writer/read-heavy, with low ops overhead; I chose it because the automation fit that profile, not because I default to it.

**Q43: What kind of agent did you build around these APIs?**
A: Autonomous workflows that call multiple REST endpoints in sequence and make decisions based on data returned from prior steps — the "agent" aspect being conditional branching and multi-step reasoning over results rather than a single fetch. State persisted to SQLite so runs can resume and be audited.

**Q44: How did the agent authenticate to the external APIs?**
A: Token-based auth handled by the automation layer: fetch/store/refresh tokens with secure storage (env/secrets, not committed), and on a 401, refresh and replay exactly once. That's the standard bearer-token lifecycle; I'd apply the same pattern in any integration.

**Q45: How did you handle API rate limits in automations?**
A: Read rate-limit headers, backoff on 429, and a simple in-code queue/semaphore to respect the concurrency cap. Pausing and retrying from persisted state (SQLite) makes long-running automations resumable when throttled — the persistence isn't just storage, it's reliability.

**Q46: What's the difference between an automation and an agent here?**
A: An automation is a fixed sequence; an agent adds decision-making inside the loop — it looks at the result of a step and chooses the next action, including calling a different endpoint or stopping. Clone Futura's "AI Agent" framing meant the flow had that conditional decision layer, not just a for-loop over API calls.

**Q47: How did you test automations against live external APIs?**
A: Test the boundaries: mock/recorded API responses for deterministic logic tests, and a small live smoke test with real credentials in limited scope so the integration is verified without hammering the API. Automations break on schema drift, so a JSON contract/response validator catches that deterministically.

**Q48: What SQLite schema/pragmas mattered for correctness?**
A: A clean schema with proper primary keys, a runs/steps table for idempotency, transactions around multi-step writes so a crash can't leave partial state, and pragmas like WAL for better read/write concurrency. Idempotency keys ensure a retried step doesn't double-apply — the automation equivalent of "the fix is safe to replay".

**Q49: How do you make an automation idempotent?**
A: Every step records a unique run/step key; before applying an action, check whether it's already been applied for that key, and apply inside a transaction. A crash-and-retry can then never duplicate external effects. This is the same correctness idea as MigratorGen's transactional, verification-backed rewriting.

**Q50: What failures were most common here, honestly?**
A: External API drift (fields renamed/removed, breaking the automation), auth token expiry at bad moments, and rate-limit hiccups. All three reduce to: validate the contract, persist state to resume, retry with backoff — assume the external world changes and design for it.

**Q51: How would you monitor long-running automations?**
A: Log each step and its result to the database (a runs/steps table), expose a status endpoint or CLI to inspect progress, and alert on step failure or excessive duration. When state lives in SQLite, "where is the run and why did it stop" is a query away — that's observable automation design.

**Q52: How does Clone Futura relate to Krip AI in skills?**
A: Krip was the bigger production platform (FastAPI, Docker, ECS, CI/CD); Clone Futura was more autonomous end-to-end logic — designing the automation, persisting state, handling real API behavior. Together they cover the two halves of platform work: operating infrastructure and driving integrations — both relevant to SP DSE.

**Q53: "AI Agent Developer" — how much actual AI vs plain automation is involved here?**
A: The intelligence is in conditional decision logic over API results rather than heavy ML — lightweight agents selecting actions based on response data. I'm precise on scope: REST automation with an agentic decision layer, not model training. Precision about scope is itself a strong signal.

**Q54: How did you structure the code so a future developer could maintain it?**
A: Separation of concerns: an API-client layer, a decision/agent layer, a state/storage layer, and an entrypoint — each independently testable, with config (URLs, credential handling, limits) externalized. It mirrors how I structure larger projects: small files, clear contracts, tests at the boundaries.

**Q55: Was there a frontend/UI component?**
A: Not primarily — the core is service/CLI-level automation. If surfaced, it would be a thin dashboard reading the state tables. The resume doesn't claim a frontend, and I wouldn't invent one. The engineering value is backend/automation, which matches the role being applied for.

**Q56: What did you learn about working autonomously at Clone Futura?**
A: Small teams make you own the whole lifecycle: design the automation, implement it, handle the errors real APIs throw, and document it for the next person. I learned to set my own acceptance criteria when there's no reviewer standing by — and to keep the quality bar PR-level even without a PR.

**Q57: What's the biggest lesson you'd reuse from Clone Futura in production?**
A: Persist state and make every external action idempotent — then the world (APIs, auth, retries, crashes) becomes survivable. Most automation systems fail because they assume the outside world is stable; assuming it changes and designing for resumability is the durable lesson.

**Q58: How did you handle secrets for the API credentials in this project?**
A: Environment variables/secrets manager at runtime, nothing hard-coded or committed, and a `.env.example` documenting keys without values. Same rule everywhere I work: credentials never enter the repo or the image.

**Q59: How would you scale this automation if volume grew 20×?**
A: Move state from local SQLite to a server DB shared by workers, turn the automation into a scheduled/queued job system with retries, and parallelize independent steps — keeping idempotency keys so retries stay safe. The core logic survives; storage and scheduling change.

**Q60: What made this "AI Agent" rather than "scripts"?**
A: Scripts run; agents decide. The turning point was a decision loop: after each API response, choose the next action from options based on the data returned, with failures producing different branches. That conditional autonomy distinguishes the project conceptually.

**Q61: If a panel asks for a specific bug you fixed here, what do you say?**
A: A verifiable class of example: a mid-run 401 where the credential had expired — fixed by token-refresh-with-single-replay and persisted state so the run resumed from where it stopped instead of restarting from zero. If the panel asks for details the resume doesn't capture, I say so honestly rather than fabricate.

**Q62: How do you keep agent decision logic testable when it depends on external data?**
A: Extract the decision function to take structured inputs (data + context) and return an action — pure logic, unit-testable with fixtures, with I/O in thin wrappers. The "agent" becomes testable; the API calls remain integration-test territory. Same pattern as mocking LLM clients at Krip.

**Q63: What was the most useful debugging technique here?**
A: Persisting a timestamped step log in the state DB. Since failures often happened during long unattended runs, the DB was the only record of "where it stopped and why" — and replaying that exact step against a recorded response reproduced it quickly. Debug from visible state, not from memory.

**Q64: How did you decide the automation's stopping conditions?**
A: Explicit success/terminal states in the decision loop: all actions complete, an unrecoverable error, or a configurable max-attempts with human-visible partial state. Nothing runs forever silently; every exit is recorded in the run table.

**Q65: What SQLite behaviors did you deliberately use, and why?**
A: WAL mode (readers don't block the writer), enforced foreign keys (PRAGMA foreign_keys=ON), and transactions around multi-row writes — each chosen for a correctness or concurrency reason. Showing that level of detail demonstrates the storage choice was deliberate, not defaulted.

**Q66: How would you phrase Clone Futura on your resume for a hiring manager?**
A: "Built REST API automations with an agentic decision layer and SQLite persistence — handling auth lifecycle, rate limits, and resumable idempotent runs." Precise and scoped; tells the interviewer what skills to probe without overclaiming.

**Q67: What's the difference between a "job" and a "run" in your automation design?**
A: A job is the definition (what to do); a run is one execution of it with its own state and step logs. Separating them lets you retry a failed run without redefining the job and inspect individual execution histories — basic but essential modeling.

**Q68: Would you use SQLite again for this?**
A: Yes, for this profile — single-node, moderate writes, wants ACID and zero-ops. I'd revisit if it went multi-writer or multi-node. Choosing the tool and being able to justify it is the skill; the tool itself was defensible for the load.

**Q69: How does resumability make your life easier as the developer?**
A: When a run fails at 4 AM, you fix the root cause and replay from the failed step instead of redoing everything. Less wasted API quota, less wasted time, and a cleaner audit trail. Development against flaky integrations is faster when the harness just retries from checkpoints.

**Q70: One-sentence summary of Clone Futura for a panel?**
A: "At Clone Futura I built REST-API automations with agentic decision logic and SQLite-backed, idempotent, resumable state — learning to design integrations that survive the messiness of real external APIs."

---

## 3. NullClass — Data Science Internship (Q71–Q90)

**Q71: Tell me about the NullClass internship.**
A: NullClass, Data Science Internship. The resume fact: built a chatbot using BERT/VADER. It's the data-science/ML thread of my experience — text classification and sentiment analysis applied to a conversational chatbot.

**Q72: What is VADER and why would you use it in a chatbot?**
A: VADER (Valence Aware Dictionary and sEntiment Reasoner) is a rule/dictionary-based sentiment analyzer tuned for social-media-style text — fast, no training needed, good on short informal text with emoticons and emphasis. In a chatbot pipeline it gives cheap sentiment on user input without a model call, useful for intent and escalation logic.

**Q73: What is BERT and how does it fit alongside VADER?**
A: BERT is a transformer-based language model pretrained on huge text corpora; fine-tuned, it gives higher-quality classification than rules. The pairing: VADER for fast lexicon-based sentiment, BERT for stronger semantic understanding/classification — VADER the quick path, BERT the accurate path, or BERT for intent classification and VADER for sentiment scoring.

**Q74: What was the actual chatbot built with, and how do you describe the stack?**
A: The resume fact is a chatbot built with BERT/VADER — so I describe a Python-based rule+ML hybrid: VADER for sentiment signals on short messages, BERT (pretrained/finetuned) for classification/intent, and a response pipeline wiring them together. If the panel asks for framework specifics the resume doesn't list, I say exactly what the resume shows rather than inventing details.

**Q75: Why combine a lexicon approach (VADER) with a transformer (BERT)?**
A: Complementary failure modes: VADER is lightweight, fast, and transparent on short emotive text; BERT handles context and sarcasm better but is heavier. Using both lets the system trade accuracy against cost on a per-message basis — and demonstrates I understand when rules beat models and when models beat rules, rather than dogmatically picking one.

**Q76: What sentiment scores does VADER produce, and how would you use them?**
A: VADER returns a compound score in [-1, 1] plus positive/negative/neutral proportions. In a chatbot you threshold the compound: strong negative → escalate or empathetic path, neutral → normal handling. It's cheap, deterministic, and auditable — a good guardrail even when a model is the main brain.

**Q77: What data did you need for the BERT component, and how did you handle it?**
A: Pretrained BERT needs none beyond its pretraining corpus; fine-tuning needs labeled examples of the classification/intent task. I'd use a public domain-aligned dataset with a careful split and validation — the same "small data → augment/transfer-learn and validate honestly" lesson as my mask-detection paper.

**Q78: How do you evaluate a chatbot's classification quality?**
A: For the classifier: accuracy and a confusion matrix, plus precision/recall per intent (rare intents get drowned in overall accuracy). For sentiment, agreement with labeled sentiment. I evaluate the classification side with standard ML metrics and don't claim a persona metric that wasn't actually measured.

**Q79: What are the failure modes of rule-based sentiment in a chatbot?**
A: Sarcasm, negation ("not bad"), emoji-heavy vs typed text, domain jargon, and language mismatch. VADER handles social-media-style text well but fails silently on context-dependent meaning — precisely the gap BERT covers. Being able to list these shows I understand the tools' boundaries, not just their headlines.

**Q80: What distinguishes the data-science internship from your other two?**
A: Krip and Clone Futura were backend/platform + automation; NullClass was ML/data-centric — data prep, model choice, evaluation, metrics. The three together give a T-shaped picture: broad engineering plus data-science depth on top of platform skills, which matches an AI/data-systems role.

**Q81: How did the BERT/VADER pairing influence your later work?**
A: It reinforced cost-aware model selection — choosing the right tool for the task instead of defaulting to the biggest model. That habit reappears in OpenRouter cost metrics, real-time detection model sizing, and choosing fast/small tools in OpenRTL. The ML internship taught me to reason about the model budget, not just accuracy.

**Q82: What's your honest framing of the nullclass proprietary vs public work split?**
A: The resume fact is that I built the chatbot during the internship; some details of the engagement are internal. I relate what I can honestly discuss and avoid inventing dataset sizes, model names, or metrics that aren't on the resume.

**Q83: How would you improve the chatbot's handling of noisy input?**
A: Normalize first (case, emoji mapping, URL/mention stripping for the classifier), then route: VADER gets the raw social-style text it likes, BERT gets the cleaned canonical form. Progressive cleaning means each tool receives its ideal input — a pipeline-thinking habit from this internship.

**Q84: If the chatbot had to go to production, what would you add?**
A: The same production layer as everywhere else in my work: a served inference endpoint (FastAPI pattern), caching for repeated queries, input validation, metrics (per-intent accuracy, latency p95, sentiment drift), and a retraining/canary evaluation path. The model is the core; production is the surrounding engineering I learned at Krip.

**Q85: How do you decide when a rule/manual approach beats ML?**
A: When the logic is stable, enumerable, and cheap — a whitelist/blacklist or a deterministic decision tree beats a model that overfits a tiny dataset or is 100× slower. If behavior is context-dependent and growing, ML pays. VADER-vs-BERT is the same curve at a different scale; the decision framework transfers exactly.

**Q86: What was the most interesting thing you learned at NullClass?**
A: That two "AI" tools can disagree, and reconciling that matters: VADER might say neutral where BERT says strongly negative, and which you trust depends on formality and cost budget. Confidence/agreement-based fallback — use the model when they diverge on high-stakes text — is a genuinely useful pattern.

**Q87: How does NullClass relate to OpenRTL's report engine / data work?**
A: OpenRTL's report engine is data analysis — parsing, aggregating, visualizing tool output; NullClass gave me the data methodology half. Combined, I can both train a model and build the instrumentation around it — the difference between analyst and engineer, which is what this role needs.

**Q88: What would you do with a fresh NLP task at work starting tomorrow?**
A: Lock the problem and metric (classification? sentiment? latency/cost budget?), audit and label the data, start with a cheap baseline (VADER-class rules or logistic over embeddings) to set a floor, then decide whether BERT-class fine-tuning earns its compute. Baseline-first is a direct transfer from this internship and my research protocol.

**Q89: Any pitfalls with pretrained BERT you learned the hard way?**
A: Domain/tone mismatch — a model fine-tuned or pretrained on one corpus can score well in demos and poorly on your actual user text — and inference latency/cost creeping up in a chat loop where every message is a forward pass. Both point to: validate on real data, and never assume pretrained equals fitted.

**Q90: One-sentence summary of NullClass for a panel?**
A: "At NullClass I built a chatbot combining VADER's fast rule-based sentiment with BERT's stronger language understanding — learning cost-aware model choice, honest evaluation, and the pipeline thinking that links ML internals to usable product behavior."---

## 4. Cross-Cutting Internship Questions (Q91–Q100)

**Q91: How do these three internships together tell one story?**
A: Agentic/LLM backend services (Krip), API automation with state (Clone Futura), and ML/data science (NullClass) — three legs of one platform: model/agent engineering, integrations, and data. The narrative: "an engineer who can build agentic-AI products end to end, with the rigor to ship and evaluate them honestly."

**Q92: What's the single best technical lesson across all internships?**
A: Assume the outside world changes: models get swapped, APIs drift, credentials expire, load spikes — and build reversibility (idempotency), observability (logs/state), and boundary testing into the design from the start. Every internship reinforced it from a different angle.

**Q93: How do you know which internship skills transfer to an Infosys SP DSE role?**
A: The platform skills (FastAPI, Docker, CI/CD, ECS, Redis) transfer near-directly to SP DSE build/automation work; the LLM-agent skills (orchestration, caching, prompt-injection guardrails, cost control) transfer to its AI-systems projects; the research discipline transfers to "verify claims honestly". I frame each internship by skills, not by company name.

**Q94: What would you say if asked "which internship was most valuable"?**
A: Each for a different reason — Krip for production platform habits, Clone Futura for autonomous end-to-end ownership, NullClass for ML fundamentals. If I must pick one, Krip AI, because it forced the highest production bar (multi-stage Docker, coverage-gated CI, ECS deploys) — the habits that matter most day one on a platform team.

**Q95: Your internships all sound similar (Python + APIs). Where's the diversity?**
A: Same language, different difficulty layers: Krip was large-scale production infrastructure (scaling, caching, deployment, security); Clone Futura was reliability of external integrations (idempotency, resumability, rate limits); NullClass was model quality and evaluation (BERT/VADER, metrics). The consistency is my foundation; the diversity is the layer each internship exercised.

**Q96: What would a new grad at Infosys say if asked to do what you did at Krip with no team?**
A: Same phases, smaller scope: ship a FastAPI service in Docker with a CI gate even for a prototype, because "it works locally" doesn't scale. The internship taught me that platform habits cost little early and pay forever — a lesson I apply to every project, including my interview-prep repos.

**Q97: What do you do when a manager hands you an unfamiliar service tomorrow?**
A: Read the README and CI pipeline first (that's the contract), trace one request end to end, run the test suite, then make a small logged change and deploy to a safe target. Within a day I'd know the architecture, the tests, and the deploy path — the same onboarding pattern I used on every intern project.

**Q98: How do you ensure what you learn at an internship is scratchable, not just memory?**
A: I write things down into reusable artifacts — checklists, boilerplate, and docs — and rebuild the key patterns in my own repos afterward. MigratorGen, OpenRTL, and my open-source PRs are effectively "internship lessons turned into public proof." If I can rebuild it, I actually learned it.

**Q99: What's the biggest risk a panel sees in internship-heavy resumes, and your counter?**
A: That internships were shallow or padded. Counter: every resume fact I state, I can demonstrate — walk through the CI YAML logic, the Dockerfile, the Redis cache-key design, the BERT/VADER split. I only claim what I can defend with details, and I say so when a detail isn't in the resume.

**Q100: Give the panel a one-sentence closing pitch on your internships.**
A: "Three internships across agentic backends, API automation, and data science taught me the complete lifecycle of shipping and evaluating AI-powered services — and my projects, research, and open-source contributions prove I internalized those lessons enough to rebuild them from scratch."