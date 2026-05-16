# GuardrailZ — Interview Preparation Guide

---

## 1. Architecture Decisions & Trade-offs

### Why Next.js 14 App Router for a Guardrail Platform?

**Decision**: Full-stack Next.js with API routes + dashboard + docs in one monolith.

**Trade-offs**:
- ✅ **Pro**: Single deployment, shared types between frontend/backend, no CORS, fast iteration
- ❌ **Con**: API and dashboard share resources; a traffic spike on validation could impact dashboard performance
- ❌ **Con**: Edge runtime limitations — forced `nodejs` runtime for `postgres.js`, can't use Edge Functions for validate endpoint

**Interview angle**: "We chose monolith for speed-to-market. For production scale, we'd extract the validation API into a standalone Node.js service with horizontal auto-scaling, keeping the dashboard on Next.js."

---

### Why Sequential Guardrail Execution?

**Decision**: Guardrails run one-by-one, short-circuit on BLOCK.

**Trade-offs**:
- ✅ **Pro**: Deterministic ordering, predictable latency for blocked requests, easy debugging
- ✅ **Pro**: Short-circuit saves compute on obviously malicious requests
- ❌ **Con**: ALLOW path pays full latency cost of every guardrail (O(n) always)
- ❌ **Con**: Independent guardrails (e.g., InputSize + LanguageRestriction) could run in parallel

**Interview angle**: "The sequential model prioritizes correctness and debuggability over throughput. For latency-sensitive use cases, we'd group independent guardrails for parallel execution with a configurable DAG."

---

### Why Singleton Registry + Factory Pattern?

**Decision**: `GuardrailRegistry` is a global singleton mapping names to factory functions.

**Trade-offs**:
- ✅ **Pro**: Simple, well-understood, no DI framework needed
- ✅ **Pro**: Deterministic registration order preserves execution ordering
- ❌ **Con**: Global state complicates testing (must reset between test cases)
- ❌ **Con**: Can't have multiple registry instances (e.g., tenant-specific subsets)

**Interview angle**: "The registry uses side-effect imports for registration, which is a pragmatic trade-off. For test isolation, we expose `__clearStore()`-style methods. At scale, we'd inject registries per-tenant."

---

### Why In-Memory + DB Dual Rate Limiting?

**Decision**: Both DB-backed sliding window (`lib/rate-limit.ts`) and in-memory (`RateLimitGuardrail`).

**Rationale**: DB rate limiter is the hard enforcement (survives restarts, works across instances). In-memory guardrail is optional per-profile for fine-grained tool-level control.

**Interview angle**: "Two-layer defense. The DB layer is mandatory at the API gateway. The in-memory guardrail is part of the profile system — you can configure tool-specific limits without adding DB round-trips."

---

### Why JSONB for Analytics Events?

**Decision**: Raw events stored as `jsonb` in `analytics_events` table.

**Trade-offs**:
- ✅ **Pro**: Schema flexibility, no migrations for new event types
- ✅ **Pro**: PostgreSQL can query JSONB with GIN indexes
- ❌ **Con**: No type safety at the DB level
- ❌ **Con**: Query performance degrades at scale without careful indexing
- ❌ **Con**: Can't use foreign keys inside JSONB payloads

**Interview angle**: "JSONB gives us fast iteration on event schemas. For production at scale, we'd migrate to a dedicated time-series database like TimescaleDB with strongly-typed columns."

---

### Why Clerk Auth Wrapped in Strategy Pattern?

**Decision**: `AuthProvider` interface with `ClerkAuthProvider` implementation.

**Trade-offs**:
- ✅ **Pro**: Swap Clerk for Auth0, Firebase, or custom auth by implementing one interface
- ✅ **Pro**: Business logic never depends on Clerk directly
- ❌ **Con**: Extra abstraction layer — adds indirection for simple cases
- ❌ **Con**: The interface is minimal (`getSession()`) and may need extension for features like MFA

**Interview angle**: "The strategy pattern future-proofs authentication. We started with Clerk for speed, but enterprise customers might require SAML/SSO — the abstraction means a single provider swap."

---

### Why Profiles Use Raw Descriptors in JSONB?

**Decision**: Profiles store `unknown[]` arrays of guardrail descriptors, compiled at runtime.

**Trade-offs**:
- ✅ **Pro**: Flexible — users can add any guardrail with any config without schema changes
- ✅ **Pro**: Compiler pattern separates storage format from runtime format
- ❌ **Con**: No referential integrity — a guardrail name could be renamed or removed, leaving orphaned descriptors
- ❌ **Con**: Must validate at runtime (compile step filters invalid entries)

**Interview angle**: "The compiler pattern follows the 'parse, don't validate' philosophy. Raw descriptors are parsed into validated `RuntimeProfile` at the boundary. Profile creation should validate names against the registry, but the current implementation doesn't — that's a documented enhancement."

---

## 2. Design Patterns Used

| Pattern | Where | Why |
|---------|-------|-----|
| **Strategy** | Auth providers | Swap auth mechanisms without changing business logic |
| **Factory** | GuardrailRegistry | Create guardrail instances with config, deferring construction |
| **Singleton** | GuardrailRegistry | Global access point for all guardrail factories |
| **Template Method** | BaseGuardrail.run() | `shouldSkip → preExecutionConfig → execute → postProcess` lifecycle with overridable hooks |
| **Abstract Class** | BaseGuardrail | Provide `result()` helper while forcing subclasses to implement `execute()` |
| **Dependency Injection** (manual) | ProfileService ← Repository | Service receives repository via constructor (no DI framework) |
| **Domain-Driven Design** | All modules | Separate domain, service, repository layers per module |
| **CQRS** (light) | Analytics module | Separate event ingestion (write) from query handlers (read) |
| **Event Sourcing** (light) | Analytics module | Events stored immutably, queries aggregate from events |
| **Normalizer** | Guardrail descriptors | Converts multiple input formats to canonical form |
| **Compiler** | Profile compiler | Transforms storage format → runtime execution format |
| **Resolver** | Profile resolver | Multi-source resolution (DB → builtins → error) |
| **Ensemble** | NSFWAdvanced, LLMClassifierInjection | Multiple signals weighted and combined for decision |
| **Sliding Window** | Rate limiting | Window-based request counting with bucket truncation |
| **Bootstrap/Registration** | Registry index | Side-effect imports at startup to populate registry |

---

## 3. Key Talking Points by Module

### Core Engine (Types, Registry, Executor, BaseGuardrail)

- **4 actions**: ALLOW, WARN, BLOCK, MODIFY — `BLOCK` is the only short-circuit action
- **Error handling**: Guardrail exceptions are caught and converted to BLOCK with `error` severity — the executor never throws
- **Registry singleton**: Side-effect import pattern — `import './registry'` at module level triggers all guardrail registrations
- **`result()` helper**: Automatically fills `guardrailName` so subclasses don't repeat themselves
- **Synchronous guardrails**: Some guardrails (regex-only) return `GuardrailResult` directly without `Promise` — the executor handles both
- **`execute()` is the contract**: Takes `(text: string, context: GuardrailContext)` — everything else is optional lifecycle hooks

### Input Guardrails

- **23 input guardrails** across prompt injection, content safety, data leakage, compliance, abuse prevention
- **NSFWAdvanced** is the most complex (424 lines): multi-tier severity, obfuscation detection, medical exemption, ensemble decision engine
- **Prompt injection cascade**: 6 guardrails (PromptInjectionSignature → SystemPromptLeak → JailbreakPattern → CrossContextManipulation → OverrideInstruction → RoleplayInjection) — layered defense
- **GDPR compliance**: 4 guardrails — RightToErasure, UserConsentValidation, GDPRDataMinimization, RightToErasure
- **LLMClassifierInjection**: Uses cumulative probability formula `score += weight * (1 - score)` — mathematical ensemble

### Output Guardrails

- **10 output guardrails** for data leakage, hallucination, quality, schema enforcement
- **MODIFY vs BLOCK**: PII redaction uses MODIFY (redacts in place), SecretLeak can be configured to BLOCK or MODIFY
- **HallucinationRisk**: Signal-based risk scoring with configurable thresholds (warn at 0.4, block at 0.75)
- **OutputSchemaValidation**: Uses AJV for JSON Schema validation — the only guardrail with an external dependency
- **CitationRequired**: Heuristic claim detection (verb + number pattern) — not NLP-based

### Profiles

- **6 built-in profiles**: default, enterprise_security, child_safety, healthcare, financial, minimal
- **Resolution order**: User-defined DB profile → built-in constant → error
- **Compiler pattern**: Transforms `unknown[]` DB data → typed `GuardrailDescriptor[]` → filters invalid entries
- **Built-in IDs**: Synthetic `builtin:default` format — distinguishes from DB-stored profiles
- **Financial profile** is the only one with tool guardrails (IAMPermission, ApiRateLimit)

### Analytics

- **CQRS-lite**: Separate write (ingestion) and read (queries) paths but same database
- **JSONB storage**: Raw events stored, queried with PostgreSQL window functions
- **percentile_cont**: Used for latency percentiles (P50, P95, P99)
- **date_trunc with COALESCE**: Time-series bucketing fills gaps with zeros
- **Only overview implemented**: The `AnalyticsReadModel` has stub arrays for hourly, guardrail, and profile stats
- **Event types**: guardrail.executed, profile.used, rate_limit.hit — extensible via type unions

### API Design

- **15 endpoints** total, 1 primary (`POST /api/validate`)
- **x-api-key header**: API key auth for the validate endpoint
- **Bearer token**: Clerk session for dashboard API
- **validateRequest flow**: Auth → Rate limit → Profile resolve → Execute guardrails → DB log → Response
- **Key generation**: `grd_live_${nanoid(32)}` — validates with regex `/^grd_live_[a-zA-Z0-9_-]{32}$/`
- **Rate limits returned** in validate response: `perMinute` and `perDay` limits with current counts

### Authentication

- **Strategy pattern**: `AuthProvider` interface → `ClerkAuthProvider` implementation
- **User Sync**: `UserSyncService.getOrCreate()` — Clerk is auth source of truth, DB users are synced on first access
- **requireAuth() guard**: Used in dashboard API routes, wraps AuthService with error handling
- **Public routes**: `/api/validate` is publicly accessible (uses API key, not session)

### Database

- **8 tables**: users, profiles, api_keys, guardrail_executions, rate_limit_tracking, user_rate_limits, analytics_events, orders
- **prepare: false**: Required for serverless/transaction poolers (PgBouncer compatibility)
- **JSONB columns**: profiles use JSONB for guardrail descriptors, analytics_events use JSONB for payload
- **Indexes on guardrail_executions**: (userId, createdAt), (userId, passed), (userId, profileId)

### SDK

- **Standalone package**: Separate `package.json` with tsup build for ESM + CJS
- **GuardrailsClient**: Wraps HTTP transport with configurable timeout (10s default) and retries (0 default)
- **Response type**: mirrors the API response shape
- **No auth logic**: Client expects pre-generated API key — the key is passed as a config parameter

### Rate Limiting

- **Two layers**: DB-backed mandatory (lib/rate-limit.ts) + in-memory optional (RateLimitGuardrail)
- **4-tier check**: API key per-minute (100) → per-day (10K) → user per-minute (500) → per-day (50K)
- **Sliding window**: Window bucket truncation via `utcMinuteBucket` and `utcDayBucket`
- **Upsert pattern**: SELECT then UPDATE/INSERT to avoid race conditions

---

## 4. Common Interview Questions

### Q: "How would you scale this to 10,000 requests/second?"

**Talk about**:
1. Extract validate API into standalone service (not Next.js)
2. Add Redis for rate limiting (removes DB bottleneck)
3. Horizonatal auto-scaling with stateless guardrail instances
4. Connection pooling with PgBouncer
5. Parallel guardrail execution for independent guardrails
6. CDN/gateway caching for identical inputs
7. Consider gRPC for internal service-to-service communication (SDK already has a client)

### Q: "How do you add a new guardrail?"

**Walk through**:
1. Create file in `modules/guardrails/guards/<stage>/<name>.guardrail.ts`
2. Extend `BaseGuardrail<Config>` with your config interface
3. Implement `execute(text, context)`: returns `GuardrailResult` via `this.result()`
4. Register in `<stage>.registry.ts`: `guardrailRegistry.register('MyGuardrail', (config) => new MyGuardrail(config))`
5. The registry bootstrap (side-effect import) picks it up automatically
6. Optionally add to profile descriptors and hub catalog

### Q: "How does short-circuiting work?"

**Answer**: The executor iterates guardrails in registration order. If any guardrail returns `action: 'BLOCK'`, the loop breaks immediately — remaining guardrails are not executed. The response still includes results up to the blocking guardrail. This saves compute on obviously malicious requests but means blocked requests get partial results.

### Q: "How do you handle errors in guardrail execution?"

**Answer**: The executor wraps each `guardrail.execute()` in try-catch. If a guardrail throws, the error is caught and converted to a `GuardrailResult` with `passed: false`, `action: 'BLOCK'`, `severity: 'error'`, and the error message in `metadata`. The executor itself never throws — errors are always surfaced as results. This ensures one failing guardrail doesn't crash the entire pipeline.

### Q: "How are profiles resolved?"

**Answer**: Two-tier resolution:
1. Query the `profiles` table for a user-defined profile matching `userId + profileName`
2. If not found, search the `BUILTIN_PROFILES` constant array
3. If neither found, throw "Profile not found"
Built-in profiles get synthetic IDs like `builtin:default`. The `ProfileService.ensureBuiltIns()` copies built-ins to the user's DB on first access.

### Q: "Why not just use an ML-based moderation API like OpenAI's?"

**Answer**: Several reasons:
1. **Determinism**: Regex-based guardrails are deterministic and auditable — ML models change over time
2. **Configurability**: Each guardrail has adjustable thresholds, allowlists, and modes
3. **Cost**: ML API calls cost money per request; regex is essentially free
4. **Latency**: ML APIs add 200-500ms per check; regex is <5ms
5. **Privacy**: Data never leaves your infrastructure
6. **Transparency**: Every guardrail result explains exactly why it fired

The trade-off is that regex-based detection has higher false positive/negative rates than well-tuned ML models. The ideal system uses both: regex for fast, deterministic blocking and ML as a secondary scoring layer.

### Q: "What would you improve first?"

**Answer**: 
1. **Redis caching** for rate limiting and registry lookups (P0 — removes DB bottleneck)
2. **Per-guardrail timeout** (P0 — prevents slow/frozen guardrails from blocking the pipeline)
3. **Structured logging** with correlation IDs (P0 — needed for debugging in production)
4. **Parallel execution** for independent guardrails (P1 — cuts latency by ~40% on ALLOW paths)
5. **Profile validation at creation** (P1 — catches typos in guardrail names early)

### Q: "How would you test a guardrail?"

**Walk through**:
1. Unit test: Create guardrail instance with known config
2. Execute with known input text
3. Assert the expected result (passed/action/message/metadata)
4. Test edge cases: empty text, very long text, Unicode, boundary values
5. Test config variations: strict mode, warn-only, custom blocklists
6. Test security signals: verify metadata includes appropriate signals
7. Integration test: Run through the full pipeline with profile resolution

### Q: "Explain the analytics architecture"

**Answer**: Lightweight CQRS with event sourcing. Three event types (guardrail.executed, profile.used, rate_limit.hit) are ingested via `AnalyticsIngestionService` and stored as JSONB in `analytics_events`. Queries use PostgreSQL aggregate functions (percentile_cont for latency, date_trunc for bucketing, COUNT with FILTER for pass/fail). The query service returns typed domain models. Currently only the overview stats are implemented (hourly/guardrail/profile stats are stub arrays).

### Q: "How does the platform handle GDPR compliance?"

**Answer**: There are 4 GDPR-specific guardrails:
1. **RightToErasure**: Detects erasure requests and routes them (always WARN, never blocks)
2. **UserConsentValidation**: Checks consent was given before processing personal data
3. **GDPRDataMinimization**: Ensures only necessary personal data is collected
4. **RetentionCheck**: Validates data hasn't exceeded retention periods
Plus PII detection/redaction in both input and output stages, and the `DataErasure` guardrail in the hub catalog.

---

## 5. System Design Discussion Topics

### Design a Multi-Tenant Guardrail Service

- **Isolation**: Row-level security in PostgreSQL vs schema-per-tenant
- **Registry per tenant**: Could customize which guardrails are available per tenant
- **Rate limiting**: Per-tenant quotas with burst allowances
- **Profile sharing**: Cross-tenant profile templates with overrides
- **Pricing tiers**: Free tier gets 5 guardrails, Pro gets unlimited, Enterprise gets custom guardrails
- **Audit logging**: Immutable per-tenant audit trail with data retention

### Design a Real-Time Analytics Pipeline

- **Ingestion**: Kafka/RabbitMQ for buffering guardrail execution events
- **Stream processing**: Flink/Kafka Streams for real-time aggregation
- **Storage**: ClickHouse/TimescaleDB for time-series, S3 for cold storage
- **Serving**: Materialized views with sub-second query times
- **Alerting**: Threshold-based alerts on BLOCK rate spikes
- **Dashboards**: WebSocket push to Grafana/custom dashboard

### Design for 99.99% Uptime

- **Multi-region deployment**: Active-active with DNS-based routing
- **PostgreSQL replication**: Streaming replication with automatic failover
- **Read replicas**: Route analytics queries to replicas
- **Guardrail execution**: Stateless — any instance can handle any request
- **Rate limiter state**: Redis cluster (not DB) so rate limit state is shared and fast
- **Graceful degradation**: If analytics DB is down, validation API still works (write to local buffer)
- **Canary deployments**: Roll out new guardrails to 1% of traffic first

### Design a Custom Guardrail DSL

- **YAML-based**: Users define guardrails in YAML config files
- **Example**:
  ```yaml
  name: my-company-policy
  stage: input
  rules:
    - pattern: "competitor-\\w+"
      action: BLOCK
      message: "References to competitors not allowed"
    - condition: "text.length > 1000"
      action: WARN
  ```
- **Compile step**: Parse YAML → compiled regex → BaseGuardrail instance
- **Runtime loading**: Hot-reload guardrails without server restart
- **Sandboxing**: Run user-defined guardrails in isolated VM to prevent ReDoS attacks
