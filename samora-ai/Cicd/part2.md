# CI/CD Interview Questions and Answers - Part 2

## Q1: How do you implement a CI/CD pipeline for database schema changes using the expand-contract pattern?
**A:** The expand-contract pattern handles database migrations with zero-downtime. Phases: (1) Expand: deploy new schema additions (new columns, new tables) alongside old schema, (2) Migrate: background job migrates existing data from old to new schema, (3) Contract: deploy the update that reads only from new schema and removes old schema references. In CI/CD: each phase is a separate deployment. Rollback: if phase 2 fails, roll back to phase 1 (old schema still works). Use feature flags to toggle between old and new code paths during migration.

## Q2: How do you handle CI/CD pipeline secrets rotation without manual intervention?
**A:** Automated secrets rotation in CI/CD: (1) Use a secrets manager (Vault, AWS Secrets Manager) as the single source of truth, (2) CI/CD tools reference secrets by key rather than storing values, (3) Set up automated rotation scripts that update the secrets manager, (4) CI/CD pipelines automatically pick up new secret versions, (5) For long-running pipeline agents, ensure they refresh secrets periodically (Vault token TTL, STS session tokens). Never hardcode secrets in pipeline config or pass them as plain env vars to build logs.

## Q3: How do you design a CI/CD pipeline for a monorepo with 50+ microservices to avoid building everything on every change?
**A:** Monorepo CI/CD optimization: (1) File-change detection using git diff to determine which projects changed, (2) Dependency graph analysis (Nx, Turborepo, Bazel) to determine which services are affected, (3) Build only affected services and their dependents, (4) Cache build artifacts across CI runs, (5) Parallelize independent builds, (6) Use CI matrix builds with dynamic configuration, (7) Implement a build manifest that maps changed files to services, (8) For Docker images, use cache-from with latest images. Use path filters: paths: ['services/auth/**'] triggers specific workflows per service.

## Q4: How do you implement a CI/CD pipeline that respects semantic versioning (semver) automatically?
**A:** Automated semver in CI/CD: (1) Use Conventional Commits: fix: = patch, feat: = minor, feat!: or BREAKING CHANGE = major, (2) Tools like semantic-release, release-it parse commit history to generate next version, (3) CI pipeline: detect version bump type -> update version files -> create git tag -> create release, (4) For pre-release versions: 2.0.0-alpha.1 for feature branches, (5) Only increment version on main branch (not on PRs), (6) Use dry-run mode in PRs to preview next version, (7) Generate CHANGELOG.md from commit messages.

## Q5: How do you handle CI/CD pipeline failures due to infrastructure flakiness (network timeouts, registry outages)?
**A:** Resilient CI/CD design: (1) Retry with exponential backoff for transient failures, (2) Cache dependencies and build artifacts to reduce reliance on external services, (3) Use artifact repositories (Artifactory, Nexus) as proxy cache for external dependencies, (4) Implement pipeline health checks before starting, (5) Use --cache-from for Docker builds to avoid registry dependency, (6) Separate critical path from non-critical — allow non-critical stages to fail without blocking, (7) For critical pipelines, use self-hosted runners with local caches.

## Q6: How do you implement a CI/CD pipeline that requires different environments with different approval workflows?
**A:** Multi-environment approval pipeline: (1) Environment-specific jobs: deploy-dev (auto), deploy-staging (auto with smoke tests), deploy-prod (manual gate), (2) Use environment protection rules with required reviewers, (3) Deploy artifact is built once and promoted, (4) Use conditional stages based on branch, (5) Environment-specific variables stored as CI/CD environment variables, (6) Deploy jobs reference the artifact version from previous stage, (7) Implement rollback as a separate pipeline or manual job.

## Q7: How do you implement a CI/CD pipeline for mobile apps with code signing and app store distribution?
**A:** Mobile CI/CD: (1) Build: compile code, run tests on emulators, (2) Code signing: store signing certificates securely in CI/CD secrets, (3) iOS: use Fastlane match to manage signing identities, (4) Android: use Gradle signing config with env vars, (5) Distribution: Fastlane supplies to TestFlight (iOS) or Google Play (Android), (6) Version bump: automate version/build number increment, (7) For iOS: macOS runners required, (8) CI-only features: conditionally enable debug mode only in CI builds.

## Q8: How do you implement CI/CD pipelines with canary deployments and automatic rollback based on metrics?
**A:** Canary CI/CD pipeline: (1) Deploy canary (10% traffic) alongside stable (90%), (2) Monitor key metrics: error rate, latency, CPU/memory, (3) Automatic promotion: if metrics are healthy for N minutes, gradually shift traffic to 100%, (4) Automatic rollback: if error rate exceeds threshold, route all traffic back to stable, (5) Tools: Flagger, Argo Rollouts, Spinnaker, (6) Analysis: separate pipeline or process watches metrics and triggers promotion/rollback, (7) Canary duration: 5-30 minutes depending on traffic volume.

## Q9: How do you implement a secure software supply chain in CI/CD pipelines with SLSA compliance?
**A:** SLSA compliance: (1) L1: build as code, provenance generation with docker buildx --provenance=true, (2) L2: signed provenance, hosted builder using GitHub Actions or GitLab CI, sign attestations with Sigstore/cosign, (3) L3: hermetic builds with isolated environments and SBOM generation, (4) L4: two-person review, reproducibility, pin builder versions. Implementation: generate SBOM with Syft, sign with cosign keyless, attest provenance with BuildKit, store attestations in OCI registry, verify before deployment.

## Q10: How do you handle flaky tests in CI/CD without blocking the pipeline?
**A:** Flaky test management: (1) Track test pass/fail history per test case to detect flakiness, (2) Quarantine: auto-move flaky tests to a separate non-blocking suite, (3) Auto-retry known flaky tests up to 3 times, (4) Maintain a database of known flaky tests, (5) Forbid adding flaky tests in PRs, (6) Run quarantined tests nightly and alert on failures, (7) Tools: Test Retry, Quarantine, flaky test detection plugins, (8) Treat flaky tests as P1 bugs.

## Q11: How do you implement a CI/CD pipeline for Infrastructure as Code with Terraform?
**A:** Terraform CI/CD: (1) Validate: fmt -check, validate, (2) Plan: plan -out=tfplan, (3) Security scan: tfsec, checkov for policy compliance, (4) Apply: apply tfplan only on main with approval for production, (5) Remote state: S3 + DynamoDB locking, (6) Workspace isolation: dev, staging, prod, (7) Use Terraform Cloud or Atlantis for PR-driven workflow, (8) Never store state files in CI/CD.

## Q12: How do you implement CI/CD for Kubernetes with GitOps (Argo CD / Flux)?
**A:** GitOps CI/CD: (1) CI pipeline builds and pushes image to registry, (2) CI pipeline updates Kubernetes manifest in GitOps repo (updates image tag), (3) GitOps operator detects change in Git repo, (4) Operator syncs desired state with cluster, (5) Advantages: auditable (Git history), auto drift detection, easy rollback (revert commit), (6) Use Image Updater or renovate for auto-tag update, (7) Promotion: promote image tags dev -> staging -> prod.

## Q13: How do you implement a CI/CD pipeline for a library/package published to npm, PyPI, or Maven Central?
**A:** Package publishing pipeline: (1) Version detection from git tags or commit messages, (2) Build: compile, run tests, (3) Publish to private registry for testing, (4) Release: create git tag, generate changelog, publish to public registry, (5) Trigger on git tag push or main merge, (6) Sign packages: GPG for Maven, npm publish --provenance for npm, (7) Pre-release: publish with next tag, (8) Dry-run in PRs, (9) Store registry tokens as CI/CD secrets.

## Q14: How do you implement CI/CD for serverless applications (AWS Lambda, Cloud Functions)?
**A:** Serverless CI/CD: (1) Build: install dependencies, (2) Package: zip artifact or use SAM/Serverless Framework, (3) Deploy: sls deploy or sam deploy, (4) Test: unit + integration tests against deployed dev env, (5) Promote: staging -> production, (6) IaC versioned in Git, (7) Each PR deploys unique ephemeral stack, (8) Lambda versioning with aliases (dev, staging, prod), (9) Traffic shifting: weighted aliases for canary.

## Q15: How do you implement a CI/CD pipeline that automatically detects and blocks secrets from being committed?
**A:** Secrets detection: (1) Pre-commit hooks: gitleaks, truffleHog, (2) CI pipeline scan on every PR, (3) Fail pipeline if secrets detected, (4) Scan git history, file contents, commit messages, (5) Use .gitignore for config files, (6) Rotate secrets immediately if leaked, (7) GitHub push protection, GitLab secret detection, (8) Maintain allowlist for false positives.

## Q16: How do you implement CI/CD for a microservices architecture with independent deployment cycles?
**A:** Microservices CI/CD: (1) Each service has its own pipeline, (2) API contract testing with Pact for compatibility, (3) Integration testing in shared environment, (4) Service registry for dynamic discovery, (5) Backward-compatible APIs only, (6) Feature flags to decouple deploy from release, (7) Pipeline per service: build, test, integrate, deploy, (8) Shared pipeline library for common logic.

## Q17: How do you implement a CI/CD pipeline for machine learning models (MLOps)?
**A:** MLOps CI/CD: (1) Data validation with Great Expectations, (2) Model training triggered by new data or code, (3) Model evaluation comparing against baseline, (4) Model registry with MLflow or DVC, (5) Deploy model as API (Seldon, BentoML), (6) A/B testing with traffic routing, (7) Monitor prediction drift and performance, (8) Automated retraining on schedule or degradation.

## Q18: How do you implement a CI/CD pipeline for a WordPress or CMS site with database content?
**A:** CMS CI/CD: (1) Code pipeline for theme/plugin updates, (2) Content pipeline via migration scripts or WP-CFM, (3) Cache-busting through versioned filenames, (4) Staging: sync production DB (sanitized), (5) Deploy with rsync or deployer, (6) Database: wp db import for migrations, (7) Review apps: temporary WordPress instances for each PR.

## Q19: How do you implement CI/CD for a monorepo with different language runtimes (Node, Python, Go)?
**A:** Multi-language monorepo CI/CD: (1) Matrix for each project with its runtime, (2) Install all required runtimes (nvm, pyenv, goenv), (3) Cache per-language (node_modules, pip, go/pkg), (4) Skip unchanged projects, (5) Shared makefiles or Taskfile, (6) Per-language linters, (7) Build only changed services' Docker images, (8) Use Nx, Turborepo, or Bazel for dependency graph.

## Q20: How do you implement a CI/CD pipeline that supports multiple cloud providers (AWS, GCP, Azure)?
**A:** Multi-cloud CI/CD: (1) Provider-agnostic tools: Terraform, Helm, (2) Provider-specific credentials as secrets, (3) Pipeline matrix per cloud, (4) Conditional stages per provider, (5) Kubernetes as abstraction layer, (6) Separate variable files per provider, (7) Multi-cloud testing against each deployment, (8) DR: deploy to secondary cloud if primary fails.

## Q21: How do you implement a CI/CD pipeline that does not expose the CI/CD system's internal IP addresses?
**A:** Security hardening: (1) Self-hosted runners in private subnet, (2) Pull-based execution (runner polls CI server), (3) NAT gateway for outbound-only access, (4) Validate webhooks with secret tokens, (5) IP allowlisting for CI/CD API access, (6) CI/CD behind reverse proxy with auth, (7) Never expose Docker socket to internet, (8) Private networking for artifacts via VPC endpoints.

## Q22: How do you implement a CI/CD pipeline that builds and tests against multiple versions of a dependency?
**A:** Multi-version testing: (1) Matrix strategy with version list, (2) Setup step installs each version, (3) All tests run in parallel across versions, (4) Allow failures on non-LTS versions, (5) Install dependencies per version (separate venvs), (6) Run coverage on one version only, (7) Build distributable on one version only.

## Q23: How do you implement a CI/CD pipeline that supports both amd64 and arm64 architectures?
**A:** Multi-architecture CI/CD: (1) Docker buildx for multi-arch images with --platform linux/amd64,linux/arm64, (2) Use CI runners with both architectures, (3) Run tests on each architecture separately, (4) Push multi-arch manifest to registry, (5) QEMU emulation for cross-platform builds, (6) Performance: native builds are 2-5x faster than QEMU.

## Q24: How do you implement a CI/CD pipeline for a Chrome Extension / VS Code Extension?
**A:** Extension CI/CD: (1) Build: npm run build, (2) Lint manifest compliance, (3) Test with headless browser, (4) Package: zip for Chrome, vsix for VSCode, (5) Sign with store credentials, (6) Publish via chrome-webstore-upload or vsce publish, (7) Version auto-bump in manifest.json, (8) Load unpacked extension from CI artifact for testing.

## Q25: How do you implement a CI/CD pipeline for a database migration tool (Flyway, Liquibase)?
**A:** Database migration CI/CD: (1) Version-controlled migration scripts, (2) CI validates: check for duplicate versions, run against test DB, (3) Apply in deployment step (pre-deploy), (4) Rollback: have reversible migrations, (5) Zero-downtime: expand-contract pattern, (6) Backup before migrations, (7) Test against copy of production schema, (8) Run integrity checks after migration, (9) Locking to prevent concurrent migrations.

## Q26: How do you implement dynamic CI/CD pipeline generation based on repository contents?
**A:** Dynamic pipeline generation: (1) Setup job analyzes changed files, generates JSON matrix, (2) Build matrix uses fromJSON() for dynamic config, (3) GitLab: trigger child pipeline with artifact, (4) Jenkins: Pipeline Script with Groovy for dynamic stages, (5) Use cases: build only changed services, select test suites, deploy based on branch, (6) Ensure generated pipelines cannot inject arbitrary code.

## Q27: How do you implement a CI/CD pipeline for a Node.js library with semantic-release?
**A:** Semantic-release CI/CD: (1) npm ci, (2) lint, (3) test with coverage, (4) build, (5) npx semantic-release which: analyzes commits, determines next version, generates changelog, creates git tag, publishes to npm, creates GitHub Release, (6) Config for branches and plugins, (7) Dry-run on PRs for preview, (8) npm publish --provenance for supply chain security.

## Q28: How do you implement CI/CD pipelines for a Helm chart repository?
**A:** Helm chart CI/CD: (1) helm lint, (2) helm unittest for template rendering, (3) helm package for .tgz, (4) Update index.yaml, (5) Push to OCI registry, (6) Sign chart with GPG or cosign, (7) Install test with --dry-run --debug, (8) Dependency update, (9) Chart version follows app version, (10) Publish to chart museum or OCI registry.

## Q29: How do you implement a CI/CD pipeline with approval gates that respect change risk classification?
**A:** Risk-based approval: (1) Classify changes: low (docs, tests), medium (new features), high (infrastructure, DB), (2) Pipeline reads classification from commit message or PR label, (3) Low: auto-approve, (4) Medium: one senior dev approval, (5) High: two approvals + security review + deployment window, (6) GitHub Environments with required reviewers, (7) GitLab: when: manual jobs with rules.

## Q30: How do you implement a CI/CD pipeline that automatically creates and tears down ephemeral environments per PR?
**A:** Ephemeral environments: (1) On PR open: pipeline creates environment (K8s namespace, preview deployment), (2) Identified by PR number or branch slug, (3) Deploy full stack, (4) Run E2E tests against it, (5) Post URL as PR comment, (6) On close: teardown, (7) Tools: GitHub Actions review apps, GitLab Review Apps, (8) Enforce max 24h TTL, (9) Seed with test data.

## Q31: How do you implement a CI/CD pipeline for a mono-repo with multiple release trains?
**A:** Multi-release train CI/CD: (1) Separate release branches: release/v1, release/v2, (2) Pipeline detects affected trains, (3) Auto-cherry-pick from main to release branches, (4) Per-train versioning, (5) Build matrix per version, (6) Each train has its own environment, (7) Shared libraries versioned per train, (8) Hotfix flows through release train pipeline.

## Q32: How do you implement CI/CD for a Kotlin Multiplatform Mobile (KMM) project?
**A:** KMM CI/CD: (1) Build matrix: shared, Android, iOS, (2) Android: Gradle build, unit tests, (3) iOS: macOS runner, Xcode build, (4) Shared: gradlew :shared:check, (5) Lint: detekt, ktlint, (6) Coverage: Kover for Kotlin, Xcode for iOS, (7) Distribution: Play Store via Gradle, TestFlight via Fastlane, (8) Gradle build cache between runs.

## Q33: How do you implement a CI/CD pipeline for embedded systems / IoT firmware?
**A:** Embedded CI/CD: (1) Cross-compilation with target toolchain, (2) Build firmware, (3) Host-compiled unit tests, (4) Hardware-in-loop with emulator (QEMU), (5) Sign firmware binaries, (6) Generate OTA update packages, (7) Version: firmware + hardware revision, (8) Test matrix across hardware revisions, (9) Staged rollout via OTA server.

## Q34: How do you implement cryptography signing in CI/CD pipelines (GPG, Sigstore, cosign)?
**A:** Signing in CI/CD: (1) GPG: store private key in secrets, import with gpg --import, (2) Sigstore keyless: uses OIDC identity from CI provider, (3) cosign: sign with key from secrets manager, (4) Maven: mvn-gpg-plugin, (5) npm: npm publish --provenance, (6) Docker: cosign sign, (7) Never store private keys as plain text.

## Q35: How do you implement CI/CD for a multi-tenant SaaS application with customer-specific configurations?
**A:** Multi-tenant CI/CD: (1) Single codebase with per-tenant YAML config, (2) CI validates tenant config schema, (3) Deploy shared or per-tenant instances, (4) Tenant-specific integration tests, (5) Feature flags per tenant (LaunchDarkly, Flagsmith), (6) Canary deploy to subset of tenants, (7) Per-tenant monitoring, (8) Per-tenant rollback capability.

## Q36: How do you implement a CI/CD pipeline that automatically generates and publishes API documentation?
**A:** API doc CI/CD: (1) OpenAPI spec in repo as source of truth, (2) Lint with spectral, (3) Generate HTML with redoc-cli or swagger-ui, (4) Version docs alongside API, (5) Publish to static hosting, (6) PR preview of docs, (7) Auto-generate changelog from spec diff, (8) Fail CI on breaking changes, (9) Auto-generate client SDKs.

## Q37: How do you implement a CI/CD pipeline for a web application with DB seed data and automated E2E tests?
**A:** E2E CI/CD: (1) Build app, (2) Deploy to ephemeral environment, (3) Run DB migrations, (4) Seed with test data, (5) Run E2E tests (Cypress, Playwright), (6) Screenshots on failure, (7) Generate test report with video, (8) Clean up ephemeral env, (9) Parallel E2E with sharding.

## Q38: How do you implement a CI/CD pipeline that scans for dependency vulnerabilities and auto-creates fix PRs?
**A:** Dependency security automation: (1) Dependabot or Renovate scans on schedule, (2) Auto-creates PRs for vulnerable deps, (3) Auto-merge minor/patch after CI passes, (4) Major updates for manual review, (5) Fail CI if CVSS > 7, (6) Generate SBOM (CycloneDX/SPDX), (7) Upload to Dependency-Track, (8) Continuous monitoring after deployment.

## Q39: How do you implement a CI/CD pipeline for a PHP/Laravel application?
**A:** Laravel CI/CD: (1) composer install, (2) Generate APP_KEY, (3) Lint with Pint, (4) Static analysis with phpstan, (5) Unit tests: php artisan test --parallel, (6) Feature tests with SQLite or MySQL service, (7) Build frontend: npm ci && npm run build, (8) Deploy: maintenance mode -> migrate -> deploy -> up, (9) Cache: optimize:clear && optimize.

## Q40: How do you implement a CI/CD pipeline that handles database rollbacks automatically?
**A:** Automated DB rollback: (1) Use migration tool with undo support, (2) Backup DB before deploy, (3) Run migrations in deploy, (4) If smoke test fails: trigger rollback, (5) Flyway: flyway undo, (6) Liquibase: liquibase rollbackCount, (7) Helm hooks for pre/post migration, (8) Expansion-contract safest for rollback, (9) Test rollback in staging regularly.

## Q41: How do you implement a CI/CD pipeline that generates code from OpenAPI specs and ensures it's always in sync?
**A:** OpenAPI code gen CI/CD: (1) Validate OpenAPI spec on PR, (2) Auto-generate server stub and client SDK, (3) Verify generated code is committed (diff check), (4) Lint generated code, (5) Build to ensure compilation, (6) Run contract tests, (7) Publish client SDKs as versioned packages, (8) Breaking change detection: fail PR on breaking diff.

## Q42: How do you implement a CI/CD pipeline for a Hugo/Jekyll/Next.js static site?
**A:** Static site CI/CD: (1) Build: npm run build or hugo, (2) Optimize: minify, image optimization, (3) Lint: broken link checking, (4) Preview: deploy to staging URL, (5) Production: deploy to CDN, (6) Cache invalidation, (7) SEO validation, (8) Accessibility checks (axe-core), (9) Performance budget (Lighthouse CI).

## Q43: How do you implement a CI/CD pipeline for a Spring Boot / Java microservice with Gradle?
**A:** Spring Boot CI/CD: (1) gradlew build, (2) gradlew test and integrationTest, (3) Code quality: check (PMD, SpotBugs), (4) Package: bootJar or jibDockerBuild, (5) Docker: Jib (no daemon needed), (6) Deploy: Helm chart with health checks, (7) Monitoring: Actuator endpoints, (8) Migration: Flyway, (9) Performance: Gatling or K6.

## Q44: How do you implement a CI/CD pipeline for an Elixir/Phoenix application?
**A:** Elixir/Phoenix CI/CD: (1) mix deps.get, (2) mix format --check-formatted, (3) mix credo, (4) mix test, (5) mix compile --warnings-as-errors, (6) mix release, (7) Docker with distroless image, (8) mix ecto.migrate pre-deploy, (9) mix dialyzer for types, (10) LiveDashboard for monitoring.

## Q45: How do you implement a CI/CD pipeline that enforces Code Review / PR size limits?
**A:** Code review enforcement: (1) PR size check with git diff --stat vs threshold, (2) Fail if >500 lines, (3) File count limit (max 20), (4) Commit message format (Conventional Commits), (5) Branch naming enforcement, (6) Auto-assign reviewers from CODEOWNERS, (7) WIP detection, (8) Rebase check, (9) Require resolved conversations.

## Q46: How do you implement CI/CD pipelines with approval flows that span multiple days (release trains)?
**A:** Multi-day release: (1) RC builds on schedule, (2) Deploy to staging, (3) Automated tests, (4) QA adds manual test results, (5) Product owner approves/rejects, (6) Approved RC goes through validation, (7) Deploy in scheduled window, (8) CI artifacts track RC state, (9) Jenkins with input steps, GitLab multi-environment approvals.

## Q47: How do you implement a CI/CD pipeline for a Rust application?
**A:** Rust CI/CD: (1) rustup for toolchain, (2) cargo fmt --check, (3) cargo clippy -- -D warnings, (4) cargo build --release, (5) cargo test --all-features, (6) cargo doc --no-deps, (7) cargo deny check, (8) cargo audit for vulnerabilities, (9) Cross-compile with cross, (10) Publish to crates.io, (11) Upload binary to GitHub Releases.

## Q48: How do you implement a CI/CD pipeline for a GraphQL API with schema validation?
**A:** GraphQL CI/CD: (1) Schema validation with graphql-inspector, (2) Breaking change detection, (3) Schema linting, (4) Test queries against mocked schema, (5) Deploy to staging and test persisted queries, (6) Query complexity analysis, (7) Depth limiting for security, (8) Schema registry (Apollo Studio), (9) Client query validation.

## Q49: How do you implement a CI/CD pipeline for a self-hosted CI runner fleet with auto-scaling?
**A:** Auto-scaling runners: (1) Ephemeral VMs or containers, (2) Scale up based on queue depth, (3) Scale down idle runners after grace period, (4) Use spot instances for cost, (5) Runners register on startup, (6) Unregister on shutdown, (7) Tools: actions-runner-controller, gitlab-runner-autoscaler, (8) Pre-baked AMI for fast startup, (9) Use --ephemeral for one-job-per-runner.

## Q50: How do you implement CI/CD for a database migration that takes hours?
**A:** Long-running migration CI/CD: (1) Break into small batches, (2) Run as background job, (3) Deploy code that reads both old/new schemas, (4) Separate pipeline triggers migration, (5) Track progress via metrics, (6) Resumable: checkpoint and resume, (7) Pipeline continues while migration runs, (8) Compare old vs new data, (9) Migration has pause/resume/rollback API, (10) Second deploy removes old schema support.

## Q51: How do you implement a CI/CD pipeline for a video game (Unity/Unreal Engine)?
**A:** Game CI/CD: (1) Headless build with Unity -batchmode or Unreal RunUAT, (2) Tests in headless mode, (3) Asset validation (missing textures, broken prefabs), (4) Build matrix for multiple platforms, (5) Asset bundles for streaming, (6) Platform-specific signing, (7) SteamPipe for PC, App Store for iOS, (8) Automated performance benchmarking.

## Q52: How do you implement a CI/CD pipeline that handles feature branch preview environments for Kubernetes?
**A:** K8s preview envs: (1) PR open: create namespace (pr-123), (2) Deploy from PR's image tag, (3) Create ingress with hostname from PR number, (4) Deploy dependent services, (5) Seed DB with test data, (6) Run integration tests, (7) Post URL to PR, (8) Close: delete namespace, (9) Resource limits to avoid cost, (10) Auto-delete after 24h.

## Q53: How do you implement a CI/CD pipeline that uses BuildKit's inline cache for Docker builds?
**A:** BuildKit inline cache: (1) docker buildx build --cache-to type=inline --cache-from type=registry,ref=myimage:latest, (2) Cache embedded in image as separate manifest, (3) Next build pulls image and uses layers as cache, (4) No separate cache storage needed, (5) Increases image size slightly, (6) Best for small-to-medium repos.

## Q54: How do you implement a CI/CD pipeline for a Python package with multi-version testing and publishing?
**A:** Python package CI/CD: (1) pip install -e .[dev], (2) ruff lint and format check, (3) mypy type checking, (4) Test matrix: 3.9, 3.10, 3.11, 3.12, (5) Coverage: pytest --cov, (6) Build: python -m build, (7) Publish: twine upload to PyPI on tag, (8) Docs: deploy to Read the Docs.

## Q55: How do you implement a CI/CD pipeline with full observability of the pipeline itself?
**A:** Pipeline observability: (1) Track pipeline duration, stage duration, pass/fail rate as Prometheus metrics, (2) OpenTelemetry tracing from commit to deployment, (3) Structured JSON logs with correlation IDs, (4) Webhook to Slack/PagerDuty on failure, (5) Grafana dashboard for trends, (6) DORA metrics: deployment frequency, lead time, change failure rate, MTTR, (7) Flakiness monitoring, (8) Cost tracking.

## Q56: How do you implement a CI/CD pipeline for a Go application with cross-compilation and minimal Docker images?
**A:** Go CI/CD: (1) golangci-lint run, (2) go test -race -coverprofile=coverage.out, (3) Build: GOOS=linux GOARCH=amd64 go build -ldflags="-s -w", (4) Cross-compile matrix, (5) Docker: multi-stage FROM scratch, (6) Image size: ~5-15MB, (7) Security scan with Trivy, (8) Helm deploy as non-root, (9) Go's /healthz endpoint.

## Q57: How do you implement a CI/CD pipeline that automatically rolls back if error rates increase after deployment?
**A:** Automated rollback: (1) Deploy to subset of instances, (2) Monitor error rate, latency p99 vs baseline, (3) Threshold: >1% error rate increase or >20% latency increase triggers rollback, (4) Rollback: revert to previous version, (5) Analysis window: 5-15 minutes, (6) Tools: Flagger, Argo Rollouts, (7) Integrate with APM tools, (8) Never auto-rollback outside business hours.

## Q58: How do you implement a CI/CD pipeline for a data pipeline (Airflow DAGs, dbt models)?
**A:** Data pipeline CI/CD: (1) Lint DAGs, (2) Test DAGs with mocked Airflow, (3) dbt: compile, test, (4) dbt build --select state:modified+, (5) Schema tests on staging, (6) Data quality: Great Expectations, (7) Deploy: sync DAGs to Airflow, (8) Trigger DAG runs with config, (9) dbt docs generation, (10) Rollback: revert DAG files.

## Q59: How do you implement a CI/CD pipeline for a Cross-Platform Desktop App (Electron, Tauri)?
**A:** Desktop app CI/CD: (1) Build matrix per OS, (2) Build with npm run build or cargo tauri build, (3) Code sign: macOS codesign, Windows Authenticode, (4) Notarize for macOS, (5) Package: dmg, exe/msi, AppImage/deb, (6) Auto-update server, (7) Tests with Spectron, (8) Security scan with Snyk.

## Q60: How do you implement a CI/CD pipeline that automatically generates and publishes a changelog?
**A:** Automated changelog: (1) Parse git log between last tag and HEAD, (2) Conventional Commits: feat, fix, BREAKING CHANGE sections, (3) Tools: git-cliff, semantic-release, conventional-changelog, (4) Format: Markdown with links to commits/PRs, (5) Generate on merge to main or tag creation, (6) Commit CHANGELOG.md to repo, (7) Attach to Release on GitHub.

## Q61: How do you implement a CI/CD pipeline that handles A/B testing infrastructure?
**A:** A/B testing CI/CD: (1) Feature flags as code in version control, (2) Validate flags have descriptions, owners, expiry dates, (3) Deploy variant code behind flag, (4) Register experiment in analytics tools, (5) Traffic split via flag tool, (6) Create dashboards for experiment metrics, (7) Cleanup: remove flag code, roll out winner, (8) Rollback: disable flag.

## Q62: How do you implement a CI/CD pipeline for a WebSocket-heavy application?
**A:** WebSocket CI/CD: (1) Unit tests with mock WS server, (2) Integration tests connecting to deployed service, (3) Load tests with artillery, (4) Test max concurrent connections, (5) E2E tests in browser (Cypress), (6) Graceful shutdown: drain connections on SIGTERM, (7) Track connected clients and message throughput.

## Q63: How do you implement a CI/CD pipeline for a DBaaS or managed database offering?
**A:** DBaaS CI/CD: (1) Test against multiple DB versions, (2) Snapshot testing of query results, (3) Test backup creation/restoration, (4) Performance regression detection, (5) Test migrations against production-scale data, (6) Chaos testing: kill DB process and verify recovery, (7) Test failover and consistency, (8) Penetration testing, (9) Audit log verification.

## Q64: How do you implement CI/CD for HSM or cryptographic services?
**A:** HSM CI/CD: (1) Never store keys in CI/CD, use KMS key IDs, (2) Test with SoftHSM in CI, (3) Integration tests with real HSM in staging, (4) Key rotation triggers and validation, (5) FIPS 140-2 validation step, (6) Audit logging, (7) PKI: test cert generation and signing, (8) Benchmark crypto operations.

## Q65: How do you implement CI/CD pipelines using reusable workflows to reduce duplication?
**A:** Reusable CI/CD: (1) GitHub Actions: reusable workflow with workflow_call, (2) Callers: uses: ./.github/workflows/reusable.yml, (3) GitLab: include: local: template, (4) Jenkins: shared library, (5) Parameterization: language, build command, test command, (6) Pin reusable workflow versions, (7) Common steps: checkout, setup, cache.

## Q66: How do you implement a CI/CD pipeline for a documentation site with versioned docs?
**A:** Versioned docs CI/CD: (1) Source in /docs alongside code, (2) Docusaurus, VuePress, or MkDocs, (3) Each git tag creates new docs version, (4) Version dropdown for users, (5) Markdown linting and broken link checking, (6) PR preview of doc site, (7) Algolia DocSearch reindex on deploy, (8) Publish to S3/CloudFront, (9) /latest redirect.

## Q67: How do you implement a CI/CD pipeline for a gRPC service with protobuf compilation?
**A:** gRPC CI/CD: (1) buf lint, (2) buf breaking --against .git, (3) buf generate for stubs, (4) Build generated code, (5) Unit + integration tests, (6) Contract tests: verify all RPCs implemented, (7) Load test with ghz, (8) Publish generated clients to registry, (9) BSR for proto management.

## Q68: How do you implement a CI/CD pipeline for a Firebase/Firestore application?
**A:** Firebase CI/CD: (1) Tests against Firebase Emulator Suite, (2) Security rules testing, (3) firebase deploy --only functions,firestore,hosting, (4) Multiple projects: staging vs prod, (5) TypeScript compile, lint, test, deploy, (6) CI service account with restricted permissions.

## Q69: How do you implement a CI/CD pipeline for CDK (AWS CDK) or Pulumi infrastructure?
**A:** CDK/Pulumi CI/CD: (1) cdk synth generates CloudFormation, (2) cdk diff as PR comment, (3) cdk-nag for compliance, (4) eslint for CDK code, (5) cdk deploy to dev on merge, (6) Manual approval for prod, (7) Snapshots for CDK testing, (8) pulumi preview and up, (9) State stored with locking.

## Q70: How do you implement a CI/CD pipeline for an NPM workspace monorepo with inter-package dependencies?
**A:** NPM workspace CI/CD: (1) npm ci --workspaces, (2) npm run build --workspaces (dependency order), (3) npm test --workspaces --if-present, (4) npm pack per package, (5) npm publish --workspace=@scope/module for changed packages, (6) Use lerna changed or nx affected, (7) Cache .npm for npm ci, (8) Build/test only affected packages.

## Q71: How do you implement a CI/CD pipeline for a WebAssembly (Wasm) application?
**A:** Wasm CI/CD: (1) Compile to Wasm target, (2) Optimize with wasm-opt, (3) Test in Wasmtime runtime, (4) Size budget: fail if .wasm exceeds limit, (5) Integration test from JavaScript, (6) Test shared memory for threading, (7) Publish to npm or CDN, (8) Benchmark vs native baseline.

## Q72: How do you implement a CI/CD pipeline that handles database-per-developer for testing?
**A:** Database-per-dev: (1) PR creates new DB container with migration, (2) Seed with sanitized prod data, (3) Run integration tests, (4) Destroy on completion, (5) Use ephemeral PostgreSQL containers, (6) Each test run gets isolated DB, (7) Parallel test execution with unique DB names, (8) Snapshot seeding for faster setup.

## Q73: How do you implement a CI/CD pipeline that performs chaos engineering tests before deployment?
**A:** Chaos engineering CI/CD: (1) Deploy to staging, (2) Run chaos experiments: kill pods, network latency, CPU stress, (3) Verify system recovers within SLO, (4) Tools: Chaos Mesh, Litmus, Gremlin, (5) Experiments defined as code in repo, (6) Pass/fail criteria: p99 latency, error rate, (7) Block production deployment if chaos tests fail, (8) Run in canary environment first.

## Q74: How do you implement a CI/CD pipeline for a multi-module Maven project?
**A:** Maven multi-module CI/CD: (1) mvn validate, (2) mvn compile, (3) mvn test (unit), (4) mvn verify (integration), (5) mvn site (reports), (6) Dependency graph: changed modules only with mvn -pl, (7) mvn deploy to artifact repository, (8) Versioning: maven-release-plugin, (9) Cache .m2/repository between runs.

## Q75: How do you implement a CI/CD pipeline that handles zero-downtime deployments for stateful services?
**A:** Stateful service CI/CD: (1) Blue-green: deploy new version alongside old, switch traffic, (2) Database: backward-compatible migrations only, (3) Session draining: wait for active sessions to complete, (4) Health checks: readiness probe before routing traffic, (5) Graceful shutdown: SIGTERM handling, (6) Auto-rollback on health check failure, (7) Data migration as separate job.

## Q76: How do you implement a CI/CD pipeline for a Ruby on Rails application?
**A:** Rails CI/CD: (1) bundle install --jobs 4, (2) rubocop lint, (3) rails db:create db:migrate, (4) rails test (unit + integration), (5) rspec for spec tests, (6) brakeman for security, (7) bundler-audit for gem vulnerabilities, (8) Precompile assets: rails assets:precompile, (9) Deploy: capistrano or kamal.

## Q77: How do you implement a CI/CD pipeline that performs contract testing between microservices?
**A:** Contract testing CI/CD: (1) Provider publishes contract (Pact file), (2) Consumer tests use pact file to mock provider, (3) CI runs consumer tests with pact file, (4) CI runs provider verification against pact file, (5) Pact Broker stores contract versions, (6) Can-i-deploy: check if consumer and provider versions are compatible, (7) Matrix testing across versions.

## Q78: How do you implement a CI/CD pipeline for a Kubernetes operator?
**A:** K8s operator CI/CD: (1) Lint: golangci-lint, (2) Unit tests with envtest (controller-runtime), (3) Integration tests with kind (K8s in Docker), (4) Build operator image, (5) Deploy to test cluster, (6) Run E2E tests: create CR, verify controller response, (7) Scorecard tests (operator-sdk scorecard), (8) Publish to OperatorHub or OLM registry.

## Q79: How do you implement CI/CD for a Peloton/indoor cycling or fitness app with device-specific firmware?
**A:** Fitness app CI/CD: (1) Mobile app pipeline (iOS + Android), (2) Firmware pipeline: cross-compile for MCU, (3) Hardware testing with test rigs in CI, (4) BLE/ANT+ connectivity tests, (5) Firmware OTA update packaging, (6) Integration tests: mobile <-> device communication, (7) Performance: sensor data latency.

## Q80: How do you implement a CI/CD pipeline that validates Dockerfile best practices and security?
**A:** Dockerfile validation: (1) hadolint for Dockerfile linting, (2) dockle for image best practices, (3) Trivy for vulnerability scanning, (4) Check: no hardcoded secrets, no root user, (5) Label validation: maintainer, version, (6) Multi-stage build verification, (7) Size check: fail if image exceeds threshold, (8) SBOM generation and verification.

## Q81: How do you implement a CI/CD pipeline for a Django application?
**A:** Django CI/CD: (1) pip install -r requirements.txt, (2) ruff or flake8 lint, (3) pytest with coverage, (4) python manage.py check --deploy, (5) python manage.py collectstatic --noinput, (6) python manage.py migrate (pre-deploy), (7) Build: Docker image, (8) Deploy with gunicorn + nginx, (9) Security: django-check-seo, django-security-check.

## Q82: How do you implement a CI/CD pipeline for a chatbot/AI assistant application?
**A:** Chatbot CI/CD: (1) NLP pipeline: train/test NLU model, (2) Intent classification accuracy check, (3) Conversation flow tests (Rasa, Dialogflow), (4) API integration tests, (5) Performance: response time budget, (6) Deploy model + bot server, (7) A/B test conversations, (8) Monitor: user satisfaction, fallback rate.

## Q83: How do you implement a CI/CD pipeline that uses artifact promotion across environments?
**A:** Artifact promotion: (1) Build once, promote across environments, (2) Each environment gets the same artifact digest, (3) Promotion: dev -> (test passed) -> staging -> (approval) -> prod, (4) Use immutable tags (sha256 digest), (5) Promotion metadata: who, when, which tests passed, (6) Promotion gate: automated checks, manual approval.

## Q84: How do you implement a CI/CD pipeline for a financial trading application?
**A:** Trading app CI/CD: (1) Low-latency performance tests, (2) Market data feed simulation, (3) Order matching engine tests, (4) FIX protocol conformance testing, (5) Risk checks: position limits, circuit breakers, (6) Audit logging verification, (7) Multi-region deployment, (8) Canary with synthetic orders, (9) Rollback to previous binary instantly.

## Q85: How do you implement a CI/CD pipeline that generates release notes from issue tracker data?
**A:** Release notes from issues: (1) Link commits to issues via conventional commits, (2) Fetch issue titles/labels from Jira/GitHub API, (3) Categorize: features, bugs, improvements, (4) Include issue links and commit SHAs, (5) Auto-generate release notes template, (6) Allow manual edits before publishing, (7) Attach to GitHub/GitLab Release.

## Q86: How do you implement CI/CD for a machine learning pipeline with feature store and model registry?
**A:** ML pipeline CI/CD: (1) Feature engineering tests, (2) Feature store validation (Tecton, Feast), (3) Model training with experiment tracking (MLflow), (4) Model evaluation: accuracy, precision, recall vs baseline, (5) Model registry: promote if passes, (6) Batch prediction pipeline tests, (7) Online serving: deploy model to endpoint, (8) Monitor: prediction drift, data drift.

## Q87: How do you implement a CI/CD pipeline for a WebRTC application?
**A:** WebRTC CI/CD: (1) Build signaling server, (2) Build TURN/STUN server config, (3) Unit tests for signaling logic, (4) Integration tests with browser WebRTC API, (5) Connection quality tests: latency, jitter, packet loss, (6) Load test: concurrent calls, (7) Deploy signaling + media servers, (8) Monitor: call success rate, quality metrics.

## Q88: How do you implement a CI/CD pipeline that performs canary analysis with Prometheus metrics?
**A:** Canary analysis with Prom: (1) Deploy canary with label canary=true, (2) Prometheus queries compare canary vs baseline metrics, (3) Metrics: request rate, error rate, latency p50/p95/p99, (4) Statistical test: Mann-Whitney U test or mean comparison, (5) Pass: promote canary, (6) Fail: rollback, (7) Tools: Kayenta, Flagger, (8) Configurable thresholds per metric.

## Q89: How do you implement a CI/CD pipeline for a SaaS product with free, pro, and enterprise tiers?
**A:** Multi-tier CI/CD: (1) Feature flags per tier, (2) Tier-specific configuration in repo, (3) CI validates tier configs, (4) Tests run per tier (free tests faster, enterprise tests comprehensive), (5) Deploy per tier: shared cluster with tier isolation or separate clusters, (6) Enterprise: customer-specific branches/tags.

## Q90: How do you implement a CI/CD pipeline that automatically rolls back database migrations on deployment failure?
**A:** Migration rollback: (1) Before deploy: backup database, (2) Run migrations as pre-deploy hook, (3) If deploy fails: automatically run rollback migration, (4) If rollback migration fails: manual intervention needed, (5) Rollback verification: compare schema and data counts, (6) Only auto-rollback for additive changes, (7) Destructive changes require manual rollback.

## Q91: How do you implement a CI/CD pipeline for an e-commerce platform with complex business logic?
**A:** E-commerce CI/CD: (1) Build: frontend + backend + services, (2) Pricing engine tests, (3) Inventory management tests, (4) Payment gateway integration tests (sandbox), (5) Cart/checkout flow E2E tests, (6) Performance: Black Friday load simulation, (7) Order processing pipeline tests, (8) Deploy with feature flags for promotions, (9) Rollback: revert pricing changes instantly.

## Q92: How do you implement CI/CD with trunk-based development and short-lived feature branches?
**A:** Trunk-based CI/CD: (1) Feature branches last <1 day, (2) Small commits directly to main, (3) Feature flags for incomplete features, (4) CI runs on every push to main, (5) Automatic deployment to staging after merge, (6) No release branches, (7) Continuous deployment to prod after tests pass, (8) Rollback via feature flag disable.

## Q93: How do you implement a CI/CD pipeline for an SDK/library that needs to support multiple API versions?
**A:** Multi-version SDK CI/CD: (1) Matrix: API versions [v1, v2, v3], (2) Test SDK against each API version, (3) Deprecation tests: verify deprecation warnings for old versions, (4) Breaking change: new major version as separate package, (5) Compatibility tests: SDK compiled with old API works with new backend, (6) Version-specific docs.

## Q94: How do you implement a CI/CD pipeline for a healthcare application with HIPAA compliance?
**A:** HIPAA CI/CD: (1) PHI detection in logs and artifacts, (2) Encryption verification: data encrypted at rest and in transit, (3) Audit logging pipeline events, (4) Access control: role-based access to CI/CD, (5) Static analysis for security flaws, (6) Dependency vulnerability scanning, (7) Signed artifacts for integrity, (8) BA agreement with CI/CD provider.

## Q95: How do you implement CI/CD for a monorepo with shared internal packages using Yarn PnP or pnpm?
**A:** PnP/pnpm CI/CD: (1) pnpm install --frozen-lockfile, (2) pnpm build (respects dependency graph), (3) pnpm test -r, (4) pnpm lint -r, (5) pnpm deploy --filter=@scope/package for publishing, (6) Changeset for version management, (7) CI validates changeset files on PRs, (8) Cache .pnpm-store, (9) Parallel test execution.

## Q96: How do you implement a CI/CD pipeline that supports database change management with schema drift detection?
**A:** Schema drift detection: (1) Store expected schema as SQL file in repo, (2) CI compares actual DB schema vs expected, (3) Drift detection: run on schedule and on deploy, (4) Alert on unexpected schema changes, (5) Auto-remediation: apply missing changes or flag for manual review, (6) Tools: schemachange, sqldef, (7) CI blocks deployment if schema drift is detected.

## Q97: How do you implement a CI/CD pipeline for a system that uses event sourcing and CQRS?
**A:** Event sourcing CI/CD: (1) Event schema validation, (2) Event store migration tests, (3) Projection rebuild tests, (4) CQRS: test command side and query side independently, (5) Event replay: verify projections produce same state, (6) Backward compatibility: events cannot be deleted, only superseded, (7) Integration: verify command produces expected events.

## Q98: How do you implement a CI/CD pipeline for a blockchain or smart contract application?
**A:** Blockchain CI/CD: (1) Compile smart contracts (Solidity, Rust), (2) Unit tests with local testnet (Ganache, Hardhat), (3) Security analysis: Slither, Mythril, (4) Gas estimation and optimization, (5) Integration tests on testnet, (6) Contract verification (Etherscan), (7) Multi-sig deployment, (8) Upgradeability tests for proxy contracts.

## Q99: How do you implement a CI/CD pipeline for a platform engineering team's internal developer platform (IDP)?
**A:** IDP CI/CD: (1) Backstage/TechDocs template validation, (2) Scaffolder action tests, (3) Plugin compatibility matrix, (4) Self-service portal tests, (5) Golden path template CI (ensure templates produce working projects), (6) Performance: catalog indexing, search, (7) Deploy: rolling update of portal, (8) Backward compatibility of API.

## Q100: How do you measure and improve CI/CD pipeline performance (reduce build time)?
**A:** Pipeline performance optimization: (1) Measure: total time, stage-level breakdown, queue time, (2) Parallelize independent stages, (3) Cache dependencies and build artifacts, (4) Use incremental builds (Nx, Turborepo), (5) Optimize Docker layer caching, (6) Use faster CI runners (more CPU, SSD), (7) Fail fast: run quick checks first, (8) Dependency pre-warming, (9) Remove redundant test runs, (10) Distribute tests across multiple runners.
