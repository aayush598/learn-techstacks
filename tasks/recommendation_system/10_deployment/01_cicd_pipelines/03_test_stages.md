# Test Stages

Test stages in a recommendation system CI pipeline must validate more than code correctness — they must verify data integrity, model quality, performance under load, and security posture. A recommendation system that passes unit tests but serves degraded recommendations under production traffic is a failed test stage. This document covers integration testing, performance testing, security scanning, model validation, contract testing, and ephemeral environment management.

---

## 1. Integration Testing

Integration tests verify that components work together correctly — feature store reads, model inference, result ranking, and API responses.

### 1.1 Testcontainers

Testcontainers provides disposable Docker containers for integration tests, eliminating environment-dependent test flakiness.

**Containers for recommendation system testing:**

| Service | Image | Purpose | Startup Timeout |
|---|---|---|---|
| PostgreSQL | `postgres:16` | User metadata, interaction history | 30s |
| Redis | `redis:7-alpine` | Feature cache, session store | 10s |
| Kafka | `confluentinc/cp-kafka` | Event streaming, real-time features | 60s |
| MinIO | `minio/minio` | S3-compatible object store for model artifacts | 15s |
| Elasticsearch | `elasticsearch:8.x` | Catalog search, feature indexing | 45s |

**Test pattern:**

1. Start containers in `@pytest.fixture(scope="session")` — share across test module
2. Apply database migrations and seed test data in `session`-scoped fixture
3. Run integration tests against real containers (not mocks)
4. Tear down containers after all tests complete
5. Use `wait_for_logs()` or health check endpoints instead of fixed sleep timers

### 1.2 Integration Test Categories

| Category | What It Validates | Example |
|---|---|---|
| Data pipeline integration | ETL jobs write correctly to feature store | Feature pipeline writes 1000 feature vectors to Redis with correct TTL |
| Model serving integration | Model loads, accepts requests, returns valid responses | POST to `/predict` returns ranking with correct item IDs and scores |
| API integration | Full request/response cycle through all middleware | Authenticated request → feature retrieval → inference → response with proper latency |
| Cross-service integration | Services communicate correctly via message queue | Kafka event triggers feature refresh within SLA |
| Configuration integration | Environment-specific config loads correctly | Staging config connects to staging feature store |

### 1.3 Database Migration Testing

For recommendation systems with evolving schemas:

- Run migrations forward **and backward** in tests
- Verify data integrity after migration (no orphaned records)
- Test migration with production-scale data volume (subset)
- Validate that migrations are backward-compatible (zero-downtime deploys)

---

## 2. Performance Testing

### 2.1 Locust in CI

Run Locust load tests in CI with controlled, bounded load to catch performance regressions.

**CI-specific configuration:**

| Parameter | CI Value | Production Value | Rationale |
|---|---|---|---|
| Concurrent users | 50–200 | 10,000+ | Enough to surface issues, not enough to overload CI runner |
| Duration | 2–5 minutes | 30+ minutes | Detect regressions without excessive CI time |
| Ramp-up | 30 seconds | 5 minutes | Fast ramp to reach steady state quickly |
| Target RPS | 50% of production | Full production | Relative comparison baseline |

**Performance regression detection:**

- Store baseline metrics from `main` branch builds
- Compare P95 latency, P99 latency, throughput, and error rate
- Fail build if any metric regresses by > 10% from baseline
- Track performance trends over time in Grafana dashboard

### 2.2 Latency Budgets for Recommendation Systems

| Component | Target P95 | Target P99 | Maximum |
|---|---|---|---|
| API gateway | 5ms | 10ms | 20ms |
| Feature retrieval | 10ms | 25ms | 50ms |
| Model inference | 15ms | 30ms | 100ms |
| Result ranking | 5ms | 10ms | 20ms |
| Response assembly | 3ms | 5ms | 10ms |
| **Total end-to-end** | **38ms** | **80ms** | **200ms** |

### 2.3 Throughput Testing

- Measure maximum sustainable RPS before error rate exceeds 0.1%
- Test auto-scaling behavior: does the system scale gracefully under increasing load?
- Validate circuit breaker behavior when downstream services degrade

---

## 3. Security Scanning

### 3.1 SAST (Static Application Security Testing)

Analyze source code for security vulnerabilities without executing it.

**Tools and targets:**

| Tool | Target | What It Catches |
|---|---|---|
| Bandit | Python source | SQL injection, hardcoded secrets, insecure deserialization |
| Semgrep | All source files | Custom rules, CWE patterns, OWASP Top 10 |
| CodeQL | Python, Java, Go | Deep semantic analysis, data flow vulnerabilities |
| Checkov | IaC files | Misconfigurations in Terraform, Kubernetes manifests |

**Critical patterns to scan for in recommendation systems:**

- User input not sanitized before feature store queries
- Model artifact loading from untrusted sources
- API keys or tokens in source code
- Insecure deserialization of model artifacts (pickle files)
- Path traversal in file-based feature loading

### 3.2 DAST (Dynamic Application Security Testing)

Test the running application for vulnerabilities.

**Tools:**

- **OWASP ZAP**: Automated scanning against API endpoints
- **Nuclei**: Template-based vulnerability scanning
- **API-specific scanners**: For REST/gRPC endpoint discovery and testing

**DAST scope for recommendation APIs:**

- Authentication bypass attempts
- Rate limiting validation
- Input fuzzing on prediction endpoints
- IDOR (Insecure Direct Object Reference) on user-specific recommendations
- SSRF via feature store URL parameters

### 3.3 Security Scanning Schedule

| Scan Type | Frequency | Blocking? |
|---|---|---|
| SAST (Semgrep/Bandit) | Every commit | Yes (CRITICAL/HIGH) |
| Dependency scan (Trivy) | Every build | Yes (CRITICAL) |
| DAST (ZAP) | Nightly on staging | No (advisory, track in backlog) |
| Container scan | Every image build | Yes (CRITICAL) |
| Secret scanning | Every commit | Yes (any severity) |
| License compliance | Every build | Yes (GPL/AGPL in proprietary code) |

---

## 4. Model Quality Validation

### 4.1 Offline Metrics Validation

Validate model metrics against minimum thresholds before deployment.

| Metric | Minimum Threshold | Measurement Method |
|---|---|---|
| AUC-ROC | ≥ 0.75 | Holdout test set evaluation |
| NDCG@10 | ≥ 0.40 | Evaluation against ground truth rankings |
| Precision@5 | ≥ 0.30 | Top-5 recommendation accuracy |
| Coverage | ≥ 60% | Percentage of catalog items recommended |
| Diversity | ≥ 0.30 | Intra-list diversity (average dissimilarity) |
| Cold-start accuracy | ≥ 0.50 (AUC) | Performance on users with < 5 interactions |

### 4.2 Model Comparison Against Baseline

Before deploying a new model version, compare against the currently deployed model:

- Run both models on the same evaluation dataset
- New model must **not degrade** on any primary metric by more than 1%
- New model must **improve** on at least one primary metric
- Log comparison results as build artifacts for audit trail

### 4.3 Data Quality Validation

Validate input data before model inference:

- **Schema validation**: All required features present with correct types
- **Distribution validation**: Feature distributions match training data (KS test, PSI)
- **Freshness validation**: Features are not stale (TTL exceeded)
- **Completeness validation**: No more than 10% missing values in critical features
- **Anomaly detection**: Statistical tests for unusual input patterns

### 4.4 Model Artifact Validation

Verify model artifacts before serving:

- Check file integrity (checksum validation)
- Verify model format compatibility with serving framework
- Test prediction on sample input to verify output format
- Validate model metadata (training date, feature list, hyperparameters)
- Check model size against memory budget

---

## 5. Contract Testing

### 5.1 Purpose

Contract tests define the expected interface between services — request shapes, response shapes, error formats, and SLA guarantees. For a recommendation system with multiple consumers (mobile app, web frontend, internal services), contracts prevent integration breakage.

### 5.2 Pact Contract Testing

Pact uses consumer-driven contracts:

1. **Consumer writes contract**: "I expect POST /recommendations to accept `user_id` and return `items: [{item_id, score, reason}]`"
2. **Provider verifies contract**: Recommendation service runs provider tests against the contract
3. **Pact Broker**: Stores and versions contracts, fails provider build if contract breaks

**Contract areas for recommendation systems:**

| Contract | Consumer | Provider | Key Assertions |
|---|---|---|---|
| Recommendation response | Mobile app | Rec API | Response schema, max latency, item count |
| Feature request | Rec API | Feature store | Feature types, null handling, TTL |
| Model prediction | Rec API | Model server | Input schema, output scores, confidence |
| Event ingestion | Web frontend | Event service | Event schema, required fields |

### 5.3 gRPC/Protobuf Contracts

For gRPC-based services, `.proto` files serve as both interface definition and contract:

- Breaking changes to proto files fail the build
- Backward compatibility enforced via field numbering rules
- Proto compatibility checker tools validate evolution safety

---

## 6. Ephemeral Test Environments

### 6.1 Purpose

Ephemeral environments are short-lived, fully isolated environments created per pull request or branch, enabling integration testing against real infrastructure.

### 6.2 Architecture

| Component | Provisioning | Lifetime |
|---|---|---|
| Kubernetes namespace | Created by CI job | Duration of PR review |
| Database | Testcontainers or namespace-scoped instance | Duration of PR review |
| Feature store | In-memory or ephemeral container | Duration of PR review |
| Model serving | Lightweight model subset | Duration of PR review |
| Monitoring | Shared Grafana with environment prefix | Duration of PR review |

### 6.3 Environment Lifecycle

1. **PR opened**: CI creates ephemeral environment with unique identifier
2. **PR updated**: Environment is rebuilt (not patched) for consistency
3. **Tests run**: Integration tests, API tests, smoke tests against ephemeral env
4. **PR merged/closed**: Environment is automatically destroyed (TTL: 30 minutes)
5. **Cost tracking**: Tag all resources with PR number for cost attribution

### 6.4 Resource Management

- Limit concurrent ephemeral environments to 10 per cluster
- Set CPU/memory quotas per namespace to prevent runaway consumption
- Use spot/preemptible instances for ephemeral environments
- Automatically scale down idle environments after 1 hour
- Total monthly budget for ephemeral environments: track and alert at 80%

### 6.5 Data Seeding

Each ephemeral environment needs realistic but anonymized data:

- Load a subset of production catalog (10% sample)
- Generate synthetic user interaction data
- Pre-deploy a model checkpoint (not the latest production model)
- Seed feature store with representative feature vectors
