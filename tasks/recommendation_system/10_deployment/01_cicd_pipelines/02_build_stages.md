# Build Stages

Build stages form the first line of defense in a production CI/CD pipeline for a recommendation system. A poorly structured build stage silently accumulates technical debt, lets type errors slip through, and produces bloated container images that increase attack surface and slow deployments. This document covers every phase of a rigorous, FAANG-grade build pipeline — from linting to artifact publishing — with specific tooling, configuration strategies, and anti-patterns.

---

## 1. Linting

Linting enforces code style and catches syntactic issues before they reach review or runtime.

### 1.1 Ruff (Python Linting & Formatting)

Ruff replaces Flake8, isort, pyupgrade, and dozens of other linters in a single Rust-based tool. It runs 10–100× faster than Python-native linters.

**Configuration strategy:**

| Setting | Recommendation | Rationale |
|---|---|---|
| `line-length` | 100 (or 88 for Black compatibility) | Balances readability with line count |
| `select` | `E`, `F`, `W`, `I`, `N`, `UP`, `B`, `A`, `C4`, `SIM`, `TCH` | Covers pyflakes, pycodestyle, isort, naming, upgrade, bugbear, annotations, comprehensions, simplification, type-checking imports |
| `ignore` | Per-project exceptions only | Avoid blanket ignores that defeat the purpose |
| `target-version` | `py311` or `py312` | Enables syntax upgrades for the target Python version |

**Integration pattern:** Run `ruff check` and `ruff format --check` as separate pipeline steps. Format check failing should block merge; lint warnings can be advisory with a transition period.

### 1.2 Mypy (Static Type Checking)

Mypy validates type annotations at build time. For a recommendation system with complex data models (feature vectors, model outputs, request/response schemas), type safety prevents runtime serialization failures.

**Strict mode configuration:**

- `strict = true` — Enables all optional strictness flags
- `disallow_untyped_defs = true` — Every function must have type annotations
- `disallow_any_generics = true` — Prevents unparameterized generics like `list` instead of `list[float]`
- `warn_return_any = true` — Flags functions returning `Any`
- `warn_unused_ignores = true` — Catches stale `# type: ignore` comments
- `no_implicit_optional = true` — Requires explicit `Optional[X]` instead of `X = None` without annotation

**Incremental adoption:** For existing codebases, use `--follow-imports=skip` initially, then progressively enable strictness per module using `# mypy: strict` file-level directives.

### 1.3 Additional Linting Tools

- **Bandit**: Security-focused linter for Python. Catches `eval()`, SQL injection patterns, hardcoded passwords, insecure random number generation.
- **ShellCheck**: Validates shell scripts in Docker entrypoints and deployment scripts.
- **yamllint**: Validates Kubernetes manifests, Helm values, and CI configuration files.
- **hadolint**: Lints Dockerfiles for best practices (pinning versions, avoiding `latest` tag, layer ordering).

---

## 2. Type Checking

Type checking extends beyond linting into semantic analysis.

### 2.1 Pyright / Pylance

Pyright performs fast, broad type checking with better inference than Mypy in some cases. Use it as a complementary checker or as the primary checker in TypeScript-heavy stacks.

### 2.2 Protocol and Structural Subtyping

For recommendation system interfaces (feature stores, model serving endpoints), use `Protocol` classes to define structural contracts:

- Feature store read interface
- Model prediction interface
- Cache client interface
- Event ingestion interface

This allows mock implementations for testing without coupling to concrete classes.

### 2.3 Type Checking in CI

Run type checking as a **blocking gate** — not advisory. A single untyped function in a critical path (feature computation, scoring) can mask bugs that surface only in production under load.

---

## 3. Unit Testing

Unit tests validate individual components in isolation.

### 3.1 Test Framework Configuration

Use **pytest** with these plugins:

- `pytest-xdist` — Parallel test execution (`-n auto`)
- `pytest-cov` — Coverage with `--cov-fail-under=80` minimum threshold
- `pytest-mock` — Fixture-based mocking
- `pytest-asyncio` — For async feature store and model serving code
- `pytest-randomly` — Randomized test ordering to catch order-dependent bugs
- `pytest-timeout` — Prevent hanging tests (recommendation: 30s default)

### 3.2 Test Categories for Recommendation Systems

| Category | Examples | Coverage Target |
|---|---|---|
| Feature engineering | Feature transformations, normalization, missing value handling | 95% |
| Model inference | Prediction pipeline, post-processing, ranking logic | 90% |
| Data validation | Schema checks, distribution validation, outlier detection | 85% |
| API handlers | Request parsing, response serialization, error handling | 90% |
| Configuration | Model loading, feature store connection, fallback behavior | 80% |

### 3.3 Mutation Testing

Use **mutmut** or **cosmic-ray** to verify test quality. Mutation testing introduces deliberate bugs and checks whether tests catch them. A mutation score below 70% indicates weak tests despite high line coverage.

---

## 4. Dependency Scanning

Dependency scanning catches known vulnerabilities and license compliance issues before they reach production.

### 4.1 Trivy (Container & Filesystem Scanning)

Trivy scans container images, filesystems, and Git repositories for:

- **OS packages**: Vulnerabilities in Alpine, Debian, Ubuntu base images
- **Language packages**: CVEs in pip, npm, Go modules
- **Configuration issues**: Misconfigured Kubernetes manifests, Dockerfiles
- **Secrets**: Hardcoded API keys, credentials, tokens

**Severity thresholds:**

| Severity | Action |
|---|---|
| CRITICAL | Block build immediately |
| HIGH | Block build, require security team review |
| MEDIUM | Log warning, require fix within sprint |
| LOW | Informational, track in backlog |

### 4.2 Safety (Python Dependency Scanning)

Safety checks the Python dependency tree against the PyUp vulnerability database. Key practices:

- Pin all direct and transitive dependencies (`pip freeze` output)
- Run `safety check --full-report` in CI
- Use `safety json-report` for machine-readable output in automated pipelines
- Integrate with Dependabot or Renovate for automated update PRs

### 4.3 Software Bill of Materials (SBOM)

Generate SBOMs using **Syft** or **cyclonedx-bom** for every build. Store SBOMs as build artifacts. This is increasingly required for compliance (SOC 2, FedRAMP) and enables rapid response to new CVEs — you can query all builds affected by a newly disclosed vulnerability.

---

## 5. Container Image Building

### 5.1 Multi-Stage Docker Builds

Multi-stage builds separate build-time dependencies from runtime, producing minimal images.

**Architecture pattern for ML services:**

| Stage | Purpose | Base Image | Size Impact |
|---|---|---|---|
| `builder` | Install build tools, compile dependencies | `python:3.12-slim` | Discarded |
| `deps` | Install Python packages with compiled extensions | `python:3.12-slim` | Shared layer |
| `runtime` | Copy only installed packages and application code | `python:3.12-slim` or distroless | ~80% smaller |
| `scout` | Security scanning stage (optional) | Any | Discarded |

**Key optimizations:**

- Order Dockerfile instructions from least to most frequently changing (maximize layer caching)
- Use `COPY --from=builder` to copy only artifacts, not build tools
- Combine `RUN` commands with `&&` to reduce layer count
- Use `.dockerignore` to exclude `.git`, `__pycache__`, test fixtures, documentation

### 5.2 Base Image Selection

| Base Image | Use Case | Attack Surface | Size |
|---|---|---|---|
| `python:3.12-slim` | General ML services | Low | ~120MB |
| `gcr.io/distroless/python3-debian12` | Production-only | Minimal | ~50MB |
| `cgr.dev/chainguard/python` | Security-hardened | Minimal | ~45MB |
| Custom Alpine-based | Size-critical edge deployment | Very low | ~30MB |

### 5.3 Image Tagging Strategy

Use a combination of tags for every image:

- **Git SHA** (`abc1234`): Immutable, traceable to exact commit
- **SemVer** (`v1.2.3`): Human-readable release identifier
- **Branch** (`main`, `develop`): Latest from branch (never use in production)
- **Never use `latest`** in any environment specification

---

## 6. Image Scanning

### 6.1 Pre-Publish Scanning

Scan images before pushing to the registry:

- Run Trivy scan as a CI step
- Fail the pipeline on CRITICAL/HIGH vulnerabilities
- Cache scan results to avoid re-scanning unchanged layers

### 6.2 Post-Publish Continuous Scanning

Push to registry, then scan in a separate job:

- Use registry webhooks to trigger scans on push
- Scan on a schedule (daily) for newly disclosed CVEs
- Tools: Trivy Operator (in-cluster), Snyk Container, Grype

### 6.3 Image Signing

Sign images using **Cosign** (Sigstore) to ensure supply chain integrity:

- Sign every image pushed to production registries
- Verify signatures in admission controllers (Kyverno, Gatekeeper)
- Store signing keys in hardware security modules (HSMs) or cloud KMS

---

## 7. Artifact Publishing

### 7.1 Container Registry Strategy

| Registry | Use Case | Features |
|---|---|---|
| Amazon ECR | AWS-native workloads | IAM integration, lifecycle policies, cross-account sharing |
| GitHub Container Registry | Open-source, GitHub Actions native | GITHUB_TOKEN auth, package linking |
| Artifact Registry (GCP) | GCP-native workloads | IAM, vulnerability scanning, remote repositories |
| Harbor | Self-hosted, air-gapped | RBAC, replication, CVE scanning built-in |

### 7.2 Publishing Pipeline

1. Build image with semver + git SHA tags
2. Run Trivy scan — block on critical findings
3. Sign image with Cosign
4. Push to staging registry (auto on every merge to `main`)
5. Push to production registry (only on release tag)
6. Update Helm chart values with new image tag (automated PR)
7. Generate and store SBOM as build artifact

### 7.3 Retention Policies

- Keep last 10 images per branch
- Keep all semver-tagged release images
- Delete untagged images after 7 days
- Archive images older than 90 days to cold storage

---

## 8. Build Caching

Effective caching reduces build times from minutes to seconds.

### 8.1 BuildKit Caching

BuildKit is the default Docker build engine. Enable advanced caching:

- **Inline cache**: Embeds cache metadata in the image itself (`--cache-to type=inline`)
- **Registry cache**: Stores cache layers in the registry (`--cache-to type=registry`)
- **Local cache**: Fast local caching for dev machines (`--cache-to type=local`)
- **S3/GCS cache**: Shared remote cache for CI runners (`--cache-to type=s3`)

**Recommended pattern for CI:** Use registry-based cache with `mode=max` to cache all layers, not just the final image layers.

### 8.2 GitHub Actions Cache

- **Action cache**: `actions/cache@v4` for pip, npm, Poetry caches
- **Docker layer cache**: `docker/build-push-action` with `cache-from/cache-to` using GitHub Actions cache backend
- **Dependency lock file**: Key cache on `poetry.lock` or `requirements.txt` hash — invalidate on dependency changes only

### 8.3 Build Time Optimization Targets

| Build Type | Target Time | Strategy |
|---|---|---|
| Full rebuild (cold) | < 10 minutes | Multi-stage, parallel stages |
| Incremental (cache hit) | < 2 minutes | Layer caching, dependency caching |
| Lint + type check | < 3 minutes | Incremental checking, parallel execution |
| Unit tests | < 5 minutes | Parallel execution, test splitting |

### 8.4 Cache Invalidation Strategy

- **Automatic**: When dependency lock files change
- **Automatic**: When base image version changes (weekly rebuild schedule)
- **Manual**: Security incidents requiring full rebuild
- **Scheduled**: Weekly full rebuilds to pick up base image security patches

---

## 9. Pipeline Composition

### 9.1 Stage Ordering

```
Lint → Type Check → Unit Test → Dependency Scan → Build → Image Scan → Publish
```

Each stage gates the next. A failure in any stage blocks progression.

### 9.2 Parallelization Opportunities

Run these stages concurrently:

- Lint + Type Check + Unit Test (parallel after dependency installation)
- Dependency Scan + Unit Test (independent)
- Image Scan + SBOM Generation (after publish, parallel)

### 9.3 Build Stage Monitoring

Track these metrics per build:

- **P50/P95/P99 build time**: Detect regressions in build infrastructure
- **Cache hit rate**: Target > 80% for incremental builds
- **Flaky test rate**: Target < 1% — quarantine flaky tests immediately
- **Vulnerability discovery rate**: Track new vulnerabilities per build

### 9.4 Build Artifact Lineage

Maintain traceability from artifact to source:

- Image digest → Git commit SHA
- Git commit SHA → CI run ID
- CI run ID → Build logs, test results, scan reports
- Store this mapping in a build metadata database or artifact registry annotations
