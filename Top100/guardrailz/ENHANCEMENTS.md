# Enhancement Suggestions

Consolidated cross-cutting and per-guardrail enhancement ideas for production readiness.

---

## 1. Input Guardrail Enhancements

| Guardrail | Enhancements |
|-----------|-------------|
| **InputSize** | Token counting via tiktoken for LLM-specific limits; streaming-aware size tracking; model-specific limits (GPT-4 8K vs Claude 100K) |
| **SecretsInInput** | Entropy-based detection for unknown token patterns; GitLeaks/TruffleHog integration; more cloud provider keys (GCP, Azure); context-aware detection to reduce false positives |
| **NSFWAdvanced** | Image-based NSFW detection via vision API; ML classifier as alternative to regex; more obfuscation patterns (emoji, zero-width chars, Unicode normalization); telemetry for dashboard analytics |
| **PHIAwareness** | HIPAA-specific identifiers (MRN, health plan IDs); NER-based detection; redaction capability for de-identified output; ICD-10 code dictionary |
| **UrlFileBlocker** | Domain allowlist/blocklist; URL reputation (Google Safe Browsing); IP geolocation; data URI detection enhancement |
| **BinaryAttachment** | Magic number/byte signature detection; compressibility check; antivirus/file scanning API integration |
| **EncodingObfuscation** | Unicode normalization (NFKC) for homoglyph attacks; URL encoding (%XX); quoted-printable/uuencode; base32/base58 detection |
| **LanguageRestriction** | CJK-specific handling (Japanese has 4 scripts mixed); language detection (not just scripts); locale-based restrictions |
| **PromptInjectionSignature** | ML-based injection classifier alongside regex; adversarial robustness testing; semantic similarity to known attack vectors |
| **SystemPromptLeak** | Cross-session context tracking; embedding similarity to known system prompts |
| **RightToErasure** | Automated workflow trigger (not just detection); integration with data deletion pipelines; legal case management |
| **UserConsentValidation** | Consent expiry tracking; granular consent revocation; audit trail for consent changes |
| **GDPRDataMinimization** | Field-level classification; automatic field stripping; data retention-based minimization |
| **PoliticalPersuasion** | Entity recognition for political figures; geographic targeting detection; temporal awareness around election periods |
| **SelfHarm** | Crisis resource integration (hotline numbers in WARN responses); escalation workflow to human moderators; severity reassessment model |
| **HateSpeech** | Contextual understanding of reclaimed language; dialect-aware detection; counter-speech generation suggestions |
| **RegexFilter** | Regex validation UI with live testing; regex timeout protection (ReDoS); pattern library for common use cases |
| **LLMClassifierInjection** | Additional ML-sourced signals; ensemble weighting based on model confidence; calibration curves per signal type; few-shot prompt-based classification |

---

## 2. Output Guardrail Enhancements

| Guardrail | Enhancements |
|-----------|-------------|
| **OutputPIIRedaction** | More PII types (passport, driver's license, MRN); NER-based detection; differential privacy noise for aggregates; custom replacement templates |
| **SecretLeakOutput** | Shannon entropy analysis; whitelist known safe tokens; log management system integration (DataDog, Splunk) |
| **InternalDataLeak** | DNS-based internal domain resolution; network-level validation; cloud metadata service detection |
| **HallucinationRisk** | Factual grounding via external knowledge base; contradiction detection against known facts; RAG pipeline integration; per-sentence confidence scoring |
| **Confidentiality** | Document classification (not just keyword); embedding similarity to confidential documents; data loss prevention (DLP) integration |
| **OutputSchemaValidation** | Multiple schema formats (YAML, XML); partial validation for streaming; OpenAPI/Swagger compatibility |
| **CitationRequired** | DOI/PubMed ID validation; link rot detection; knowledge base cross-reference |
| **QualityThreshold** | Readability score (Flesch-Kincaid); response coherence metrics; instruction-following assessment; BERTScore/semantic similarity |
| **EnvVarLeak** | Runtime env var scanning; config file pattern detection; CI/CD secret exposure detection |
| **InternalEndpointLeak** | Service mesh integration (Kubernetes DNS); cloud provider metadata API detection; port scan pattern detection |
| **CommandInjectionOutput** | AST-level command detection; sandboxed execution verification; shell syntax tree parsing |
| **SecretsInLogs** | Context-aware entropy with Shannon; known safe token allowlist; log shipper integrations |
| **SandboxedOutput** | gVisor/Firecracker sandbox verification; capability-based execution restriction; container escape detection |

---

## 3. Content, Operational, Tool, Security, General Enhancements

| Guardrail | Enhancements |
|-----------|-------------|
| **Defamation** | NLU-based defamation detection; entity resolution against public figures; legal jurisdiction awareness; statute-of-limitations check |
| **MedicalAdvice** | Medical taxonomy integration (SNOMED, ICD-11); practitioner credential verification; prescription validation against drug databases |
| **Violence** | Dynamic severity via NLP transformer; cultural context awareness; DRF (Digital Rights Framework) integration for hate speech intersection |
| **RateLimit** | Distributed rate limiting (Redis); dynamic throttling based on system load; per-endpoint granular limits |
| **CostThreshold** | Real-time pricing API integration; spot-instance cost awareness; budget alerts and forecasting |
| **ModelVersionPin** | Auto-update policy (pin with grace period); version change notifications; model registry integration |
| **TelemetryEnforcement** | OpenTelemetry integration; structured audit log format; real-time alerting pipeline |
| **ToolAccess** | OAuth 2.0 token exchange; JWK-based capability token verification; mTLS for tool communication; dynamic policy evaluation via OPA/Rego |
| **IAMPermission** | Real IAM policy engine (AWS IAM/Google CAI); role hierarchy resolution; permission boundary enforcement |
| **DestructiveToolCall** | Approval workflow integration (PagerDuty); runbook automation; blast radius calculation |
| **FileWriteRestriction** | Filesystem namespace isolation; overlay filesystem sandbox; inode-level tracking |
| **ApiRateLimit** | Token bucket with burst; queue-based rate limiting; priority queuing for premium tiers |
| **RetentionCheck** | S3 lifecycle policy integration; GDPR Article 17 auto-deletion workflow; legal hold management with eDiscovery integration |
| **ApiKeyRotationTrigger** | Automated rotation via provider APIs; webhook notifications; rotation audit trail |

---

## 4. Profile System Enhancements

1. **Profile versioning** — Track changes over time with diff views and rollback
2. **Profile inheritance** — "Extend" built-in profiles with custom additions (like OOP inheritance)
3. **Guardrail ordering** — Allow users to reorder execution sequence; drag-and-drop UI
4. **A/B testing** — Split traffic between profile configurations with statistical reporting
5. **Import/export** — Share profiles between accounts via JSON/YAML
6. **Profile analytics** — Per-profile pass/fail rates, latency, cost tracking
7. **Validation at creation** — Validate guardrail names against registry at profile creation time (catch typos early)
8. **Merge capability** — Combine multiple profiles with conflict resolution
9. **Scheduled switching** — Time-based or event-based profile activation
10. **Templates marketplace** — Community-shared profile templates in the hub
11. **Preview mode** — Dry-run a profile to see which guardrails would fire before saving

---

## 5. Analytics Enhancements

1. **Full CQRS** — Separate read/write databases for analytics vs operational data
2. **Real-time streaming** — WebSocket-based live analytics dashboard
3. **Time-series DB** — TimescaleDB or ClickHouse for time-based query performance
4. **Pre-aggregation** — Materialized views for common dashboard queries (hourly/daily totals)
5. **Alerting** — Threshold-based alerts on anomaly detection (sudden spike in BLOCKs)
6. **Export** — CSV/JSON export of raw and aggregated data
7. **Custom dashboards** — User-configurable dashboard widgets and saved views
8. **Cost analytics** — Per-guardrail, per-profile, and per-API-key cost breakdown
9. **Retention policies** — Automated data lifecycle management (delete events older than N days)
10. **Anomaly detection** — ML-based detection of unusual guardrail behavior (e.g., injection bypass attempts)
11. **Guardrail heatmap** — Which guardrails fire most, co-occurrence patterns
12. **Funnel analysis** — Track user paths through the validation pipeline

---

## 6. Cross-Cutting Architectural Improvements

### 6.1 Performance & Scalability

- **Caching layer**: Add Redis for rate limiting (replaces DB-backed), registry lookups, and profile resolution
- **Parallel guardrail execution**: Allow configurable parallelism for independent guardrails (currently all sequential)
- **Guardrail timeout**: Add per-guardrail timeout to prevent a single slow guardrail from blocking the pipeline
- **Batch processing**: Support batch validation of multiple texts in a single API call
- **CDN caching**: Cache validation results for identical inputs (with TTL)
- **Connection pooling**: Tune postgres.js pool size based on load testing

### 6.2 Security Hardening

- **HMAC request signing**: Sign API requests with a nonce + timestamp to prevent replay attacks
- **IP allowlisting**: Restrict API key usage to specific IP ranges
- **Audit log immutability**: Use append-only DB tables or blockchain-based logging for audit trails
- **Rate limit bypass prevention**: Add CAPTCHA or proof-of-work for repeated rate limit violators
- **Secrets in transit**: Enforce TLS 1.3 minimum
- **Dependency scanning**: Automated CVE scanning in CI pipeline

### 6.3 Observability

- **OpenTelemetry**: Distributed tracing across guardrail execution pipeline
- **Structured logging**: JSON-formatted logs with correlation IDs
- **Health check endpoint**: `/api/health` with DB connectivity, registry loaded, latency checks
- **Metrics endpoint**: Prometheus metrics for guardrail execution counts, durations, error rates
- **Sentry/Error tracking**: Error monitoring integration for production issues
- **Dashboards**: Grafana dashboards for system health and guardrail performance

### 6.4 Testing & CI/CD

- **Load testing**: k6 or Artillery scripts for throughput and latency benchmarking
- **Fuzz testing**: Random input generation to find corner cases in guardrail regex
- **Property-based testing**: Use fast-check to verify guardrail invariants
- **E2E tests**: Playwright/Cypress tests for dashboard workflows
- **Contract tests**: API contract testing with Pact or OpenAPI validator
- **Performance regression CI**: Guardrail against latency regressions in CI pipeline
- **Smoke tests**: Post-deployment smoke test suite

### 6.5 Developer Experience

- **Guardrail scaffolding CLI**: `npm run generate:guardrail -- --name MyGuardrail --stage input`
- **OpenAPI spec**: Auto-generated or maintained OpenAPI 3.0 spec for the REST API
- **Local dev environment**: One-command setup with Docker Compose including seed data
- **Guardrail hot-reload**: Watch guardrail files and re-register without server restart (for development)
- **API client libraries**: Python, Go, and Rust SDKs in addition to TypeScript

### 6.6 Architecture

- **Plugin system**: Allow third-party guardrails to be loaded dynamically without code changes
- **Event-driven architecture**: Use message queues (RabbitMQ, Kafka) for async guardrail execution
- **Multi-tenant isolation**: Schema-per-tenant or row-level security policies in PostgreSQL
- **Feature flags**: LaunchDarkly or custom flag system for gradual guardrail rollout
- **Webhook callbacks**: Async validation result delivery via webhooks
- **Guardrail composition**: AND/OR/NOT combinators for complex guardrail logic

---

## 7. Documentation Fixes (Current Docs)

The following inconsistencies were identified in the current documentation and should be fixed:

| Issue | Location | Current | Correct |
|-------|----------|---------|---------|
| Input guardrail count | `03A_INPUT_GUARDRAILS.md` line 1 | "17 Guards" | 23 guards |
| Output guardrail count | `03B_OUTPUT_GUARDRAILS.md` line 1 | "10 Guards" | 13 guards |
| Total guardrail count | `02_CORE_ENGINE.md` line 143 | "41 registered guardrails" | 50 (or update individual counts) |
| Summary table count | `03C_CONTENT_OPERATIONAL_TOOL_SECURITY_GENERAL.md` line 356 | "All 41 Guardrails" | All 50 Guardrails |
| Registry count reference | `02_CORE_ENGINE.md` registry bootstrap | "17 input" / "10 output" | Registry actually lists 17 input and 10 output; extra 6 input + 3 output guards exist as implementations but not registered |
| Hub catalog count | `07_HUB_MODULE.md` | "41 guardrail entries" | 50 entries (or verify actual catalog count) |
| Missing enhancement cross-references | Multiple | Per-guardrail enhancements scattered | Consolidated list in this document |

**Root cause**: There are 41 guardrails in the production registry, but the documentation also covers guardrails that exist in the codebase as implementations or in the hub catalog that are not registered in the engine registry. The total count across all doc files should be audited against the actual source code.

---

## 8. Prioritization Matrix

| Category | Impact | Effort | Priority |
|----------|--------|--------|----------|
| Redis caching for rate limiting | High | Medium | P0 |
| Guardrail timeout | High | Low | P0 |
| Per-guardrail structured logging | High | Low | P0 |
| Guardrail scaffolding CLI | Medium | Low | P1 |
| Profile validation at creation | Medium | Low | P1 |
| OpenAPI spec generation | Medium | Medium | P1 |
| Batch validation endpoint | High | Medium | P1 |
| Plugin system | High | High | P2 |
| Event-driven architecture | High | High | P2 |
| Real-time analytics streaming | Medium | High | P2 |
| ML-based anomaly detection | Medium | High | P3 |
| WebSocket analytics | Low | High | P3 |
| Multi-tenant isolation | High | High | P3 |
