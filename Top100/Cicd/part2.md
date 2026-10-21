# CI/CD Interview Questions and Answers - Part 2

## Q1: How do you implement a CI/CD pipeline for database schema changes using the expand-contract pattern?
**A:** The expand-contract pattern handles database migrations with zero-downtime. Phases: (1) Expand: deploy new schema additions (new columns, new tables) alongside old schema, (2) Migrate: background job migrates existing data from old to new schema, (3) Contract: deploy the update that reads only from new schema and removes old schema references. In CI/CD: each phase is a separate deployment. Rollback: if phase 2 fails, roll back to phase 1 (old schema still works). Use feature flags to toggle between old and new code paths during migration.

**Code:**
```yaml
jobs:
  expand:
    runs-on: ubuntu-latest
    steps:
      - run: flyway migrate -target=2     # add new columns/tables only
  migrate-data:
    needs: expand
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/backfill-new-columns.sh
  contract:
    needs: migrate-data
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh contract          # code reads new schema only
      - run: flyway migrate                # remove old schema references
```

## Q2: How do you handle CI/CD pipeline secrets rotation without manual intervention?
**A:** Automated secrets rotation in CI/CD: (1) Use a secrets manager (Vault, AWS Secrets Manager) as the single source of truth, (2) CI/CD tools reference secrets by key rather than storing values, (3) Set up automated rotation scripts that update the secrets manager, (4) CI/CD pipelines automatically pick up new secret versions, (5) For long-running pipeline agents, ensure they refresh secrets periodically (Vault token TTL, STS session tokens). Never hardcode secrets in pipeline config or pass them as plain env vars to build logs.

**Code:**
```yaml
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - run: |
          sa=$(vault read -field=value secret/db/creds)
          aws secretsmanager update-secret --secret-id db/creds \
            --secret-string "{\"username\":\"$sa\",\"password\":$(openssl rand -hex 16 | jq -R)}"
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
        env:
          DB_CREDS: ${{ secrets.DB_CREDS }}
```

## Q3: How do you design a CI/CD pipeline for a monorepo with 50+ microservices to avoid building everything on every change?
**A:** Monorepo CI/CD optimization: (1) File-change detection using git diff to determine which projects changed, (2) Dependency graph analysis (Nx, Turborepo, Bazel) to determine which services are affected, (3) Build only affected services and their dependents, (4) Cache build artifacts across CI runs, (5) Parallelize independent builds, (6) Use CI matrix builds with dynamic configuration, (7) Implement a build manifest that maps changed files to services, (8) For Docker images, use cache-from with latest images. Use path filters: paths: ['services/auth/**'] triggers specific workflows per service.

**Code:**
```yaml
name: Monorepo CI
on:
  push:
    branches: [main]
    paths:
      - 'services/auth/**'
      - 'services/payments/**'
      - 'packages/shared/**'
jobs:
  affected:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npx nx affected:test --base=origin/main
      - run: npx nx affected:build --base=origin/main --parallel=5
```

## Q4: How do you implement a CI/CD pipeline that respects semantic versioning (semver) automatically?
**A:** Automated semver in CI/CD: (1) Use Conventional Commits: fix: = patch, feat: = minor, feat!: or BREAKING CHANGE = major, (2) Tools like semantic-release, release-it parse commit history to generate next version, (3) CI pipeline: detect version bump type -> update version files -> create git tag -> create release, (4) For pre-release versions: 2.0.0-alpha.1 for feature branches, (5) Only increment version on main branch (not on PRs), (6) Use dry-run mode in PRs to preview next version, (7) Generate CHANGELOG.md from commit messages.

**Code:**
```yaml
name: Semantic Release
on:
  push:
    branches: [main]
permissions:
  contents: write
  id-token: write
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npx semantic-release --branches main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Q5: How do you handle CI/CD pipeline failures due to infrastructure flakiness (network timeouts, registry outages)?
**A:** Resilient CI/CD design: (1) Retry with exponential backoff for transient failures, (2) Cache dependencies and build artifacts to reduce reliance on external services, (3) Use artifact repositories (Artifactory, Nexus) as proxy cache for external dependencies, (4) Implement pipeline health checks before starting, (5) Use --cache-from for Docker builds to avoid registry dependency, (6) Separate critical path from non-critical — allow non-critical stages to fail without blocking, (7) For critical pipelines, use self-hosted runners with local caches.

**Code:**
```yaml
name: Resilient CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: ~/.npm
          key: npm-${{ hashFiles('package-lock.json') }}
      - name: npm ci with retry
        run: |
          for i in 1 2 3 4 5; do
            npm ci && break || sleep $((i * 10))
          done
      - name: docker build with cache-from
        run: docker build --cache-from registry.example.com/app:latest -t app:latest .
```

## Q6: How do you implement a CI/CD pipeline that requires different environments with different approval workflows?
**A:** Multi-environment approval pipeline: (1) Environment-specific jobs: deploy-dev (auto), deploy-staging (auto with smoke tests), deploy-prod (manual gate), (2) Use environment protection rules with required reviewers, (3) Deploy artifact is built once and promoted, (4) Use conditional stages based on branch, (5) Environment-specific variables stored as CI/CD environment variables, (6) Deploy jobs reference the artifact version from previous stage, (7) Implement rollback as a separate pipeline or manual job.

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm ci && npm run build
  deploy-dev:
    needs: build
    runs-on: ubuntu-latest
    environment: development
    steps:
      - run: ./deploy.sh dev
  deploy-staging:
    needs: deploy-dev
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: ./deploy.sh staging
  deploy-prod:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - run: ./deploy.sh production
```

## Q7: How do you implement a CI/CD pipeline for mobile apps with code signing and app store distribution?
**A:** Mobile CI/CD: (1) Build: compile code, run tests on emulators, (2) Code signing: store signing certificates securely in CI/CD secrets, (3) iOS: use Fastlane match to manage signing identities, (4) Android: use Gradle signing config with env vars, (5) Distribution: Fastlane supplies to TestFlight (iOS) or Google Play (Android), (6) Version bump: automate version/build number increment, (7) For iOS: macOS runners required, (8) CI-only features: conditionally enable debug mode only in CI builds.

**Code:**
```yaml
jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 17
      - run: ./gradlew assembleRelease
        env:
          STORE_FILE: ${{ secrets.ANDROID_KEYSTORE }}
          STORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
      - run: fastlane android supply
  ios:
    runs-on: macos-latest
    steps:
      - run: fastlane match appstore
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
      - run: fastlane ios beta
```

## Q8: How do you implement CI/CD pipelines with canary deployments and automatic rollback based on metrics?
**A:** Canary CI/CD pipeline: (1) Deploy canary (10% traffic) alongside stable (90%), (2) Monitor key metrics: error rate, latency, CPU/memory, (3) Automatic promotion: if metrics are healthy for N minutes, gradually shift traffic to 100%, (4) Automatic rollback: if error rate exceeds threshold, route all traffic back to stable, (5) Tools: Flagger, Argo Rollouts, Spinnaker, (6) Analysis: separate pipeline or process watches metrics and triggers promotion/rollback, (7) Canary duration: 5-30 minutes depending on traffic volume.

**Code:**
```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: web
  namespace: prod
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  service:
    port: 80
  analysis:
    interval: 30s
    threshold: 10
    maxWeight: 100
    stepWeight: 10
    metrics:
      - name: error-rate
        thresholdRange:
          max: 1
      - name: latency
        threshold: 500
```

## Q9: How do you implement a secure software supply chain in CI/CD pipelines with SLSA compliance?
**A:** SLSA compliance: (1) L1: build as code, provenance generation with docker buildx --provenance=true, (2) L2: signed provenance, hosted builder using GitHub Actions or GitLab CI, sign attestations with Sigstore/cosign, (3) L3: hermetic builds with isolated environments and SBOM generation, (4) L4: two-person review, reproducibility, pin builder versions. Implementation: generate SBOM with Syft, sign with cosign keyless, attest provenance with BuildKit, store attestations in OCI registry, verify before deployment.

**Code:**
```yaml
name: SLSA Build
on:
  push:
    branches: [main]
permissions:
  id-token: write
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build with provenance and SBOM
        run: |
          docker buildx build --provenance=true --sbom=true \
            -t ghcr.io/acme/app:${{ github.sha }} --push .
      - name: Generate SBOM
        run: syft ghcr.io/acme/app:${{ github.sha }} -o cyclonedx > sbom.json
      - name: Keyless sign
        run: cosign sign --yes ghcr.io/acme/app:${{ github.sha }}
```

## Q10: How do you handle flaky tests in CI/CD without blocking the pipeline?
**A:** Flaky test management: (1) Track test pass/fail history per test case to detect flakiness, (2) Quarantine: auto-move flaky tests to a separate non-blocking suite, (3) Auto-retry known flaky tests up to 3 times, (4) Maintain a database of known flaky tests, (5) Forbid adding flaky tests in PRs, (6) Run quarantined tests nightly and alert on failures, (7) Tools: Test Retry, Quarantine, flaky test detection plugins, (8) Treat flaky tests as P1 bugs.

**Code:**
```yaml
jobs:
  stable-tests:
    runs-on: ubuntu-latest
    steps:
      - run: npm ci && npm run test:stable
  quarantined:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - run: npm run test:quarantined
```

## Q11: How do you implement a CI/CD pipeline for Infrastructure as Code with Terraform?
**A:** Terraform CI/CD: (1) Validate: fmt -check, validate, (2) Plan: plan -out=tfplan, (3) Security scan: tfsec, checkov for policy compliance, (4) Apply: apply tfplan only on main with approval for production, (5) Remote state: S3 + DynamoDB locking, (6) Workspace isolation: dev, staging, prod, (7) Use Terraform Cloud or Atlantis for PR-driven workflow, (8) Never store state files in CI/CD.

**Code:**
```yaml
name: Terraform
on:
  pull_request:
  push:
    branches: [main]
jobs:
  validate-plan:
    runs-on: ubuntu-latest
    steps:
      - uses: hashicorp/setup-terraform@v3
      - run: terraform fmt -check
      - run: terraform validate
      - run: tfsec .
      - run: checkov -d .
      - run: terraform plan -out=tfplan
      - uses: actions/upload-artifact@v4
        with:
          name: tfplan
          path: tfplan
  apply:
    needs: validate-plan
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: hashicorp/setup-terraform@v3
      - uses: actions/download-artifact@v4
        with:
          name: tfplan
      - run: terraform apply tfplan
```

## Q12: How do you implement CI/CD for Kubernetes with GitOps (Argo CD / Flux)?
**A:** GitOps CI/CD: (1) CI pipeline builds and pushes image to registry, (2) CI pipeline updates Kubernetes manifest in GitOps repo (updates image tag), (3) GitOps operator detects change in Git repo, (4) Operator syncs desired state with cluster, (5) Advantages: auditable (Git history), auto drift detection, easy rollback (revert commit), (6) Use Image Updater or renovate for auto-tag update, (7) Promotion: promote image tags dev -> staging -> prod.

**Code:**
```yaml
name: GitOps Deploy
on:
  push:
    branches: [main]
jobs:
  build-and-update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t registry.example.com/web:${{ github.sha }} .
      - run: docker push registry.example.com/web:${{ github.sha }}
      - uses: actions/checkout@v4
        with:
          repository: acme/gitops
          token: ${{ secrets.GITOPS_TOKEN }}
          path: gitops
      - run: |
          cd gitops
          yq -i '.spec.template.spec.containers[0].image = "registry.example.com/web:${{ github.sha }}"' apps/web/deploy.yaml
          git commit -am "release web ${{ github.sha }}" && git push
```

## Q13: How do you implement a CI/CD pipeline for a library/package published to npm, PyPI, or Maven Central?
**A:** Package publishing pipeline: (1) Version detection from git tags or commit messages, (2) Build: compile, run tests, (3) Publish to private registry for testing, (4) Release: create git tag, generate changelog, publish to public registry, (5) Trigger on git tag push or main merge, (6) Sign packages: GPG for Maven, npm publish --provenance for npm, (7) Pre-release: publish with next tag, (8) Dry-run in PRs, (9) Store registry tokens as CI/CD secrets.

**Code:**
```yaml
name: Publish
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci && npm test && npm run build
      - run: npm publish --signatures
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Q14: How do you implement CI/CD for serverless applications (AWS Lambda, Cloud Functions)?
**A:** Serverless CI/CD: (1) Build: install dependencies, (2) Package: zip artifact or use SAM/Serverless Framework, (3) Deploy: sls deploy or sam deploy, (4) Test: unit + integration tests against deployed dev env, (5) Promote: staging -> production, (6) IaC versioned in Git, (7) Each PR deploys unique ephemeral stack, (8) Lambda versioning with aliases (dev, staging, prod), (9) Traffic shifting: weighted aliases for canary.

**Code:**
```yaml
name: Serverless
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/setup-sam@v2
      - run: sam build
      - run: sam deploy --stack-name myapp --no-confirm-changeset --capabilities CAPABILITY_IAM
      - run: aws lambda update-alias --function-name my-lambda --name prod \
          --function-version $VERSION --routing-configuration '{"AdditionalVersionWeights":{"1":0.1}}'
```

## Q15: How do you implement a CI/CD pipeline that automatically detects and blocks secrets from being committed?
**A:** Secrets detection: (1) Pre-commit hooks: gitleaks, truffleHog, (2) CI pipeline scan on every PR, (3) Fail pipeline if secrets detected, (4) Scan git history, file contents, commit messages, (5) Use .gitignore for config files, (6) Rotate secrets immediately if leaked, (7) GitHub push protection, GitLab secret detection, (8) Maintain allowlist for false positives.

**Code:**
```yaml
name: Secret Scan
on:
  pull_request:
jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - run: gitleaks git --pre-commit --redact --verbose
```

## Q16: How do you implement CI/CD for a microservices architecture with independent deployment cycles?
**A:** Microservices CI/CD: (1) Each service has its own pipeline, (2) API contract testing with Pact for compatibility, (3) Integration testing in shared environment, (4) Service registry for dynamic discovery, (5) Backward-compatible APIs only, (6) Feature flags to decouple deploy from release, (7) Pipeline per service: build, test, integrate, deploy, (8) Shared pipeline library for common logic.

**Code:**
```yaml
name: Payment Service
on:
  push:
    paths: ['services/payments/**']
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd services/payments && npm ci && npm test
      - run: npm run pact:publish
  deploy:
    needs: build-test
    runs-on: ubuntu-latest
    steps:
      - run: cd services/payments && ./deploy.sh
```

## Q17: How do you implement a CI/CD pipeline for machine learning models (MLOps)?
**A:** MLOps CI/CD: (1) Data validation with Great Expectations, (2) Model training triggered by new data or code, (3) Model evaluation comparing against baseline, (4) Model registry with MLflow or DVC, (5) Deploy model as API (Seldon, BentoML), (6) A/B testing with traffic routing, (7) Monitor prediction drift and performance, (8) Automated retraining on schedule or degradation.

**Code:**
```yaml
name: MLOps
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 1 * * *'
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: dvc repro
      - run: mlflow run . --env-manager=local -P model_name=recommender
  evaluate:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - run: python evaluate.py --baseline production-model
      - run: mlflow models serve --model-uri models:/recommender/latest
```

## Q18: How do you implement a CI/CD pipeline for a WordPress or CMS site with database content?
**A:** CMS CI/CD: (1) Code pipeline for theme/plugin updates, (2) Content pipeline via migration scripts or WP-CFM, (3) Cache-busting through versioned filenames, (4) Staging: sync production DB (sanitized), (5) Deploy with rsync or deployer, (6) Database: wp db import for migrations, (7) Review apps: temporary WordPress instances for each PR.

**Code:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          rsync -az --delete themes/ plugins/ user@server:/srv/www/wp-content/
          wp db import migrations/${{ github.sha }}.sql --ssh=server
          wp cache flush --ssh=server
```

## Q19: How do you implement CI/CD for a monorepo with different language runtimes (Node, Python, Go)?
**A:** Multi-language monorepo CI/CD: (1) Matrix for each project with its runtime, (2) Install all required runtimes (nvm, pyenv, goenv), (3) Cache per-language (node_modules, pip, go/pkg), (4) Skip unchanged projects, (5) Shared makefiles or Taskfile, (6) Per-language linters, (7) Build only changed services' Docker images, (8) Use Nx, Turborepo, or Bazel for dependency graph.

**Code:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        include:
          - service: api
            setup: actions/setup-node@v4
          - service: worker
            setup: actions/setup-python@v5
          - service: cli
            setup: actions/setup-go@v5
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ${{ matrix.setup }}
      - run: cd services/${{ matrix.service }} && make test
```

## Q20: How do you implement a CI/CD pipeline that supports multiple cloud providers (AWS, GCP, Azure)?
**A:** Multi-cloud CI/CD: (1) Provider-agnostic tools: Terraform, Helm, (2) Provider-specific credentials as secrets, (3) Pipeline matrix per cloud, (4) Conditional stages per provider, (5) Kubernetes as abstraction layer, (6) Separate variable files per provider, (7) Multi-cloud testing against each deployment, (8) DR: deploy to secondary cloud if primary fails.

**Code:**
```yaml
jobs:
  deploy:
    strategy:
      matrix:
        cloud: [aws, gcp, azure]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform plan -var-file=${{ matrix.cloud }}.tfvars -out=tfplan
      - env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          GOOGLE_CREDENTIALS: ${{ secrets.GCP_SA_KEY }}
          ARM_CLIENT_SECRET: ${{ secrets.AZURE_SP_SECRET }}
        run: terraform apply tfplan
```

## Q21: How do you implement a CI/CD pipeline that does not expose the CI/CD system's internal IP addresses?
**A:** Security hardening: (1) Self-hosted runners in private subnet, (2) Pull-based execution (runner polls CI server), (3) NAT gateway for outbound-only access, (4) Validate webhooks with secret tokens, (5) IP allowlisting for CI/CD API access, (6) CI/CD behind reverse proxy with auth, (7) Never expose Docker socket to internet, (8) Private networking for artifacts via VPC endpoints.

**Code:**
```yaml
jobs:
  build:
    runs-on: [self-hosted, private-subnet]   # runner in private VPC
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
        env:
          NPM_REGISTRY: https://internal-artifacts.local  # via VPC endpoint
```

## Q22: How do you implement a CI/CD pipeline that builds and tests against multiple versions of a dependency?
**A:** Multi-version testing: (1) Matrix strategy with version list, (2) Setup step installs each version, (3) All tests run in parallel across versions, (4) Allow failures on non-LTS versions, (5) Install dependencies per version (separate venvs), (6) Run coverage on one version only, (7) Build distributable on one version only.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        node: [18, 20, 22, 23]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - continue-on-error: ${{ matrix.node == '23' }}
        run: npm ci && npm test
  coverage:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci && npm run test:coverage
```

## Q23: How do you implement a CI/CD pipeline that supports both amd64 and arm64 architectures?
**A:** Multi-architecture CI/CD: (1) Docker buildx for multi-arch images with --platform linux/amd64,linux/arm64, (2) Use CI runners with both architectures, (3) Run tests on each architecture separately, (4) Push multi-arch manifest to registry, (5) QEMU emulation for cross-platform builds, (6) Performance: native builds are 2-5x faster than QEMU.

**Code:**
```yaml
jobs:
  build:
    strategy:
      matrix:
        arch: [amd64, arm64]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-qemu-action@v3
      - uses: docker/setup-buildx-action@v3
      - run: |
          docker buildx build --platform linux/${{ matrix.arch }} \
            -t registry.example.com/app:${{ github.sha }} --push .
```

## Q24: How do you implement a CI/CD pipeline for a Chrome Extension / VS Code Extension?
**A:** Extension CI/CD: (1) Build: npm run build, (2) Lint manifest compliance, (3) Test with headless browser, (4) Package: zip for Chrome, vsix for VSCode, (5) Sign with store credentials, (6) Publish via chrome-webstore-upload or vsce publish, (7) Version auto-bump in manifest.json, (8) Load unpacked extension from CI artifact for testing.

**Code:**
```yaml
name: Extension Release
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test && npm run build
      - run: npx vsce publish -p ${{ secrets.VSCE_TOKEN }}
      - runs-on: ubuntu-latest
        steps:
          - run: npx @google/chrome-webstore-upload-cli upload --source dist --extension-id ${{ secrets.EXT_ID }} --client-id ${{ secrets.CLIENT_ID }} --client-secret ${{ secrets.CLIENT_SECRET }} --refresh-token ${{ secrets.REFRESH_TOKEN }}
```

## Q25: How do you implement a CI/CD pipeline for a database migration tool (Flyway, Liquibase)?
**A:** Database migration CI/CD: (1) Version-controlled migration scripts, (2) CI validates: check for duplicate versions, run against test DB, (3) Apply in deployment step (pre-deploy), (4) Rollback: have reversible migrations, (5) Zero-downtime: expand-contract pattern, (6) Backup before migrations, (7) Test against copy of production schema, (8) Run integrity checks after migration, (9) Locking to prevent concurrent migrations.

**Code:**
```yaml
jobs:
  flyway-validate:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
    steps:
      - uses: actions/checkout@v4
      - run: |
          docker run --rm -v $PWD/migrations:/flyway/sql flyway/flyway \
            -url=jdbc:postgresql://postgres/test -user=postgres -password=test \
            validate migrate
  deploy:
    needs: flyway-validate
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/backup-db.sh
      - run: docker run --rm -v $PWD/migrations:/flyway/sql flyway/flyway \
          -url=$PROD_DB_URL -user=$USER -password=$D Pass migrate
```

## Q26: How do you implement dynamic CI/CD pipeline generation based on repository contents?
**A:** Dynamic pipeline generation: (1) Setup job analyzes changed files, generates JSON matrix, (2) Build matrix uses fromJSON() for dynamic config, (3) GitLab: trigger child pipeline with artifact, (4) Jenkins: Pipeline Script with Groovy for dynamic stages, (5) Use cases: build only changed services, select test suites, deploy based on branch, (6) Ensure generated pipelines cannot inject arbitrary code.

**Code:**
```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.list.outputs.services }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - id: list
        run: |
          changed=$(git diff --name-only origin/main | cut -d/ -f2 | sort -u | jq -R -s -c 'split("\n")[:-1]')
          echo "services=$changed" >> $GITHUB_OUTPUT
  build:
    needs: setup
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: ${{ fromJSON(needs.setup.outputs.services) }}
    steps:
      - run: ./build.sh ${{ matrix.service }}
```

## Q27: How do you implement a CI/CD pipeline for a Node.js library with semantic-release?
**A:** Semantic-release CI/CD: (1) npm ci, (2) lint, (3) test with coverage, (4) build, (5) npx semantic-release which: analyzes commits, determines next version, generates changelog, creates git tag, publishes to npm, creates GitHub Release, (6) Config for branches and plugins, (7) Dry-run on PRs for preview, (8) npm publish --provenance for supply chain security.

**Code:**
```yaml
name: npm Release
on:
  push:
    branches: [main, beta]
permissions:
  contents: write
  id-token: write
jobs:
  semantic-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm run lint && npm run test:coverage && npm run build
      - run: npx semantic-release --dry-run
        if: github.event_name == 'pull_request'
      - run: npx semantic-release
        if: github.event_name == 'push'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Q28: How do you implement CI/CD pipelines for a Helm chart repository?
**A:** Helm chart CI/CD: (1) helm lint, (2) helm unittest for template rendering, (3) helm package for .tgz, (4) Update index.yaml, (5) Push to OCI registry, (6) Sign chart with GPG or cosign, (7) Install test with --dry-run --debug, (8) Dependency update, (9) Chart version follows app version, (10) Publish to chart museum or OCI registry.

**Code:**
```yaml
jobs:
  helm-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: helm lint charts/my-app
      - run: helm unittest charts/my-app
      - run: helm package charts/my-app -d dist/
      - run: helm repo index dist/ --merge index.yaml
      - run: cosign sign --yes dist/my-app-1.2.0.tgz
      - run: helm push dist/my-app-1.2.0.tgz oci://registry.example.com/charts
```

## Q29: How do you implement a CI/CD pipeline with approval gates that respect change risk classification?
**A:** Risk-based approval: (1) Classify changes: low (docs, tests), medium (new features), high (infrastructure, DB), (2) Pipeline reads classification from commit message or PR label, (3) Low: auto-approve, (4) Medium: one senior dev approval, (5) High: two approvals + security review + deployment window, (6) GitHub Environments with required reviewers, (7) GitLab: when: manual jobs with rules.

**Code:**
```yaml
jobs:
  classify:
    runs-on: ubuntu-latest
    steps:
      - id: risk
        run: |
          if grep -q "BREAKING\|db:\|infra:" "${{ github.event.pull_request.body }}"; then
            echo "risk=high" >> $GITHUB_OUTPUT
          else
            echo "risk=low" >> $GITHUB_OUTPUT
          fi
  deploy:
    needs: classify
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - run: ./deploy.sh
```

## Q30: How do you implement a CI/CD pipeline that automatically creates and tears down ephemeral environments per PR?
**A:** Ephemeral environments: (1) On PR open: pipeline creates environment (K8s namespace, preview deployment), (2) Identified by PR number or branch slug, (3) Deploy full stack, (4) Run E2E tests against it, (5) Post URL as PR comment, (6) On close: teardown, (7) Tools: GitHub Actions review apps, GitLab Review Apps, (8) Enforce max 24h TTL, (9) Seed with test data.

**Code:**
```yaml
name: Review App
on:
  pull_request:
    types: [opened, synchronize, closed]
jobs:
  deploy:
    if: github.event.action != 'closed'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: kubectl create ns preview-${{ github.event.number }}
      - run: helm install web ./chart -n preview-${{ github.event.number }} --set image.tag=${{ github.sha }}
      - run: kubectl annotate ns preview-${{ github.event.number }} ttl=24h
      - uses: actions/github-script@v7
        with:
          script: github.rest.issues.createComment({ issue_number: context.issue.number, body: `Preview: https://pr-${{ github.event.number }}.dev.example.com` })
  teardown:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - run: kubectl delete ns preview-${{ github.event.number }}

```

## Q31: How do you implement a CI/CD pipeline for a mono-repo with multiple release trains?
**A:** Multi-release train CI/CD: (1) Separate release branches: release/v1, release/v2, (2) Pipeline detects affected trains, (3) Auto-cherry-pick from main to release branches, (4) Per-train versioning, (5) Build matrix per version, (6) Each train has its own environment, (7) Shared libraries versioned per train, (8) Hotfix flows through release train pipeline.

**Code:**
```yaml
name: Release Train
on:
  push:
    branches: ['release/*']
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        train: [v1, v2]
    steps:
      - uses: actions/checkout@v4
      - run: ./build-train.sh ${{ matrix.train }}
      - run: ./deploy-train.sh ${{ matrix.train }} staging
```

## Q32: How do you implement CI/CD for a Kotlin Multiplatform Mobile (KMM) project?
**A:** KMM CI/CD: (1) Build matrix: shared, Android, iOS, (2) Android: Gradle build, unit tests, (3) iOS: macOS runner, Xcode build, (4) Shared: gradlew :shared:check, (5) Lint: detekt, ktlint, (6) Coverage: Kover for Kotlin, Xcode for iOS, (7) Distribution: Play Store via Gradle, TestFlight via Fastlane, (8) Gradle build cache between runs.

**Code:**
```yaml
jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - run: ./gradlew :shared:check :androidApp:assembleDebug
      - run: ./gradlew detekt ktlintCheck
  ios:
    runs-on: macos-latest
    steps:
      - run: ./gradlew :shared:iosArm64MainKlibrary
      - run: xcodebuild -project iosApp.xcodeproj -scheme iosApp test
      - run: fastlane ios beta
```

## Q33: How do you implement a CI/CD pipeline for embedded systems / IoT firmware?
**A:** Embedded CI/CD: (1) Cross-compilation with target toolchain, (2) Build firmware, (3) Host-compiled unit tests, (4) Hardware-in-loop with emulator (QEMU), (5) Sign firmware binaries, (6) Generate OTA update packages, (7) Version: firmware + hardware revision, (8) Test matrix across hardware revisions, (9) Staged rollout via OTA server.

**Code:**
```yaml
jobs:
  firmware:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        board: [esp32, stm32, nrf52]
    steps:
      - uses: actions/checkout@v4
      - run: docker run -v $PWD:/src xtensa-toolchain make -C /src build BOARD=${{ matrix.board }}
      - run: ./scripts/sign-fw.sh firmware.${{ matrix.board }}.bin
      - uses: actions/upload-artifact@v4
        with:
          name: fw-${{ matrix.board }}
          path: build/firmware.${{ matrix.board }}.bin
```

## Q34: How do you implement cryptography signing in CI/CD pipelines (GPG, Sigstore, cosign)?
**A:** Signing in CI/CD: (1) GPG: store private key in secrets, import with gpg --import, (2) Sigstore keyless: uses OIDC identity from CI provider, (3) cosign: sign with key from secrets manager, (4) Maven: mvn-gpg-plugin, (5) npm: npm publish --provenance, (6) Docker: cosign sign, (7) Never store private keys as plain text.

**Code:**
```yaml
name: Sign Artifacts
permissions:
  id-token: write
jobs:
  sign:
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --batch --import
          gpg --armor --detach-sign dist/app.tar.gz
      - run: cosign sign --yes ghcr.io/acme/app:${{ github.sha }}
      - run: |
          export COSIGN_PASSWORD=${{ secrets.COSIGN_PASSWORD }}
          cosign sign --key env://COSIGN_PASSWORD --yes ghcr.io/acme/app:${{ github.sha }}
```

## Q35: How do you implement CI/CD for a multi-tenant SaaS application with customer-specific configurations?
**A:** Multi-tenant CI/CD: (1) Single codebase with per-tenant YAML config, (2) CI validates tenant config schema, (3) Deploy shared or per-tenant instances, (4) Tenant-specific integration tests, (5) Feature flags per tenant (LaunchDarkly, Flagsmith), (6) Canary deploy to subset of tenants, (7) Per-tenant monitoring, (8) Per-tenant rollback capability.

**Code:**
```yaml
jobs:
  validate-configs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          for f in tenants/*.yaml; do
            yq eval '. as $v | .tenant, .limits.cpu, .limits.memory' $f
          done
  deploy-tenant:
    needs: validate-configs
    strategy:
      matrix:
        tenant: [acme, globex, initech]
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh --tenant ${{ matrix.tenant }} --weight 10
```

## Q36: How do you implement a CI/CD pipeline that automatically generates and publishes API documentation?
**A:** API doc CI/CD: (1) OpenAPI spec in repo as source of truth, (2) Lint with spectral, (3) Generate HTML with redoc-cli or swagger-ui, (4) Version docs alongside API, (5) Publish to static hosting, (6) PR preview of docs, (7) Auto-generate changelog from spec diff, (8) Fail CI on breaking changes, (9) Auto-generate client SDKs.

**Code:**
```yaml
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx @stoplight/spectral-cli lint openapi.yaml
      - run: npx openapi-diff openapi.yaml --fail-on-breaking
      - run: npx redocly build-docs openapi.yaml -o public/
      - uses: actions/upload-pages-artifact@v3
        with:
          path: public/
      - uses: actions/deploy-pages@v4
```

## Q37: How do you implement a CI/CD pipeline for a web application with DB seed data and automated E2E tests?
**A:** E2E CI/CD: (1) Build app, (2) Deploy to ephemeral environment, (3) Run DB migrations, (4) Seed with test data, (5) Run E2E tests (Cypress, Playwright), (6) Screenshots on failure, (7) Generate test report with video, (8) Clean up ephemeral env, (9) Parallel E2E with sharding.

**Code:**
```yaml
jobs:
  e2e:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: app_test
    env:
      DATABASE_URL: postgresql://postgres@postgres/app_test
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - run: npx prisma migrate deploy
      - run: npx prisma db seed
      - uses: cypress-io/github-action@v6
        with:
          start: npm start
          record: true
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: cypress-screenshots
          path: cypress/screenshots
```

## Q38: How do you implement a CI/CD pipeline that scans for dependency vulnerabilities and auto-creates fix PRs?
**A:** Dependency security automation: (1) Dependabot or Renovate scans on schedule, (2) Auto-creates PRs for vulnerable deps, (3) Auto-merge minor/patch after CI passes, (4) Major updates for manual review, (5) Fail CI if CVSS > 7, (6) Generate SBOM (CycloneDX/SPDX), (7) Upload to Dependency-Track, (8) Continuous monitoring after deployment.

**Code:**
```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: daily
    open-pull-requests-limit: 10
    reviewers:
      - security-team
  - package-ecosystem: pip
    directory: /
    schedule:
      interval: weekly
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: monthly
```

## Q39: How do you implement a CI/CD pipeline for a PHP/Laravel application?
**A:** Laravel CI/CD: (1) composer install, (2) Generate APP_KEY, (3) Lint with Pint, (4) Static analysis with phpstan, (5) Unit tests: php artisan test --parallel, (6) Feature tests with SQLite or MySQL service, (7) Build frontend: npm ci && npm run build, (8) Deploy: maintenance mode -> migrate -> deploy -> up, (9) Cache: optimize:clear && optimize.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_DATABASE: app
          MYSQL_ROOT_PASSWORD: secret
    steps:
      - uses: actions/checkout@v4
      - run: composer install --no-interaction --prefer-dist
      - run: cp .env.ci .env && php artisan key:generate
      - run: vendor/bin/pint --test
      - run: vendor/bin/phpstan analyse --memory-limit=1G
      - run: php artisan test --parallel
      - run: npm ci && npm run build
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: php artisan down
      - run: php artisan migrate --force
      - run: rsync -az --exclude node_modules ./ user@prod:/srv/app
      - run: php artisan up
      - run: php artisan optimize
```

## Q40: How do you implement a CI/CD pipeline that handles database rollbacks automatically?
**A:** Automated DB rollback: (1) Use migration tool with undo support, (2) Backup DB before deploy, (3) Run migrations in deploy, (4) If smoke test fails: trigger rollback, (5) Flyway: flyway undo, (6) Liquibase: liquibase rollbackCount, (7) Helm hooks for pre/post migration, (8) Expansion-contract safest for rollback, (9) Test rollback in staging regularly.

**Code:**
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/backup-db.sh
      - run: docker run --rm -v $PWD/migrations:/flyway/sql flyway/flyway -url=$PROD_DB migrate
      - run: ./deploy.sh
  smoke:
    needs: deploy
    runs-on: ubuntu-latest
    steps:
      - run: curl --fail --retry 10 https://app.example.com/health
  rollback:
    needs: smoke
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: docker run --rm -v $PWD/migrations:/flyway/sql flyway/flyway -url=$PROD_DB undo
      - run: ./scripts/restore-db.sh backup.sql
      - run: ./deploy.sh --previous
```

## Q41: How do you implement a CI/CD pipeline that generates code from OpenAPI specs and ensures it's always in sync?
**A:** OpenAPI code gen CI/CD: (1) Validate OpenAPI spec on PR, (2) Auto-generate server stub and client SDK, (3) Verify generated code is committed (diff check), (4) Lint generated code, (5) Build to ensure compilation, (6) Run contract tests, (7) Publish client SDKs as versioned packages, (8) Breaking change detection: fail PR on breaking diff.

**Code:**
```yaml
jobs:
  sync-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx @stoplight/spectral-cli lint openapi.yaml
      - run: npx openapi-generator-cli generate -i openapi.yaml -g typescript-fetch -o sdk
      - run: npx openapi-diff derive openapi.yaml main.yaml --fail-on-beta
      - run: |
          git diff --exit-code sdk/ || { echo "generated SDK out of sync"; exit 1; }
      - run: cd sdk && npm ci && npm test
```

## Q42: How do you implement a CI/CD pipeline for a Hugo/Jekyll/Next.js static site?
**A:** Static site CI/CD: (1) Build: npm run build or hugo, (2) Optimize: minify, image optimization, (3) Lint: broken link checking, (4) Preview: deploy to staging URL, (5) Production: deploy to CDN, (6) Cache invalidation, (7) SEO validation, (8) Accessibility checks (axe-core), (9) Performance budget (Lighthouse CI).

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - run: npx lychee ./out
      - run: npx @lhci/cli@0.14.x autorun --config=lighthouserc.json
      - uses: actions/upload-pages-artifact@v3
        with:
          path: out/
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
      - run: aws cloudfront create-invalidation --distribution-id $DISTRO --paths '/*'
```

## Q43: How do you implement a CI/CD pipeline for a Spring Boot / Java microservice with Gradle?
**A:** Spring Boot CI/CD: (1) gradlew build, (2) gradlew test and integrationTest, (3) Code quality: check (PMD, SpotBugs), (4) Package: bootJar or jibDockerBuild, (5) Docker: Jib (no daemon needed), (6) Deploy: Helm chart with health checks, (7) Monitoring: Actuator endpoints, (8) Migration: Flyway, (9) Performance: Gatling or K6.

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 21
      - uses: gradle/actions/setup-gradle@v4
      - uses: actions/cache@v4
        with:
          path: ~/.gradle
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*') }}
      - run: ./gradlew build
      - run: ./gradlew test integrationTest check
      - run: ./gradlew jibDockerBuild
        env:
          GITHUB_SHA: ${{ github.sha }}
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: helm upgrade web ./chart --set image.tag=${{ github.sha }}
```

## Q44: How do you implement a CI/CD pipeline for an Elixir/Phoenix application?
**A:** Elixir/Phoenix CI/CD: (1) mix deps.get, (2) mix format --check-formatted, (3) mix credo, (4) mix test, (5) mix compile --warnings-as-errors, (6) mix release, (7) Docker with distroless image, (8) mix ecto.migrate pre-deploy, (9) mix dialyzer for types, (10) LiveDashboard for monitoring.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
    env:
      MIX_ENV: test
      DATABASE_URL: postgresql://postgres@localhost/hello_test
    steps:
      - uses: actions/checkout@v4
      - uses: erlef/setup-beam@v1
        with:
          elixir-version: 1.16.0
          otp-version: 26.0
      - run: mix local.hex --force && mix deps.get
      - run: mix format --check-formatted
      - run: mix credo --strict
      - run: mix dialyzer
      - run: mix compile --warnings-as-errors
      - run: mix ecto.create && mix ecto.migrate
      - run: mix test
  release:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: mix do deps.get, release --overwrite
      - run: docker build -t reg.example.com/hello:${{ github.sha }} .
```

## Q45: How do you implement a CI/CD pipeline that enforces Code Review / PR size limits?
**A:** Code review enforcement: (1) PR size check with git diff --stat vs threshold, (2) Fail if >500 lines, (3) File count limit (max 20), (4) Commit message format (Conventional Commits), (5) Branch naming enforcement, (6) Auto-assign reviewers from CODEOWNERS, (7) WIP detection, (8) Rebase check, (9) Require resolved conversations.

**Code:**
```yaml
jobs:
  size-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: |
          diff=$(git diff origin/main...HEAD --numstat)
          added=$(echo "$diff" | awk '{s+=$1} END {print s}')
          files=$(echo "$diff" | wc -l)
          echo "added=$added files=$files"
          [ "$added" -le 500 ] || { echo "PR exceeds 500 added lines"; exit 1; }
          [ "$files" -le 20 ]  || { echo "PR touches more than 20 files"; exit 1; }
  commit-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npx commitlint --from ${{ github.event.pull_request.base.sha }}
```

## Q46: How do you implement CI/CD pipelines with approval flows that span multiple days (release trains)?
**A:** Multi-day release: (1) RC builds on schedule, (2) Deploy to staging, (3) Automated tests, (4) QA adds manual test results, (5) Product owner approves/rejects, (6) Approved RC goes through validation, (7) Deploy in scheduled window, (8) CI artifacts track RC state, (9) Jenkins with input steps, GitLab multi-environment approvals.

**Code:**
```yaml
stages:
  - build
  - staging
  - qa
  - approve
  - release

rc:
  stage: build
  script:
    - ./build-rc.sh
  artifacts:
    paths: [rc]
deploy-staging:
  stage: staging
  script:
    - ./deploy.sh staging
qa-signoff:
  stage: qa
  when: manual
  script:
    - ./run-qa-checklist.sh
product-approval:
  stage: approve
  when: manual
  allow_failure: false
  script:
    - ./gate.sh product-owner
release:
  stage: release
  when: manual
  environment: production
  script:
    - ./deploy.sh production
```

## Q47: How do you implement a CI/CD pipeline for a Rust application?
**A:** Rust CI/CD: (1) rustup for toolchain, (2) cargo fmt --check, (3) cargo clippy -- -D warnings, (4) cargo build --release, (5) cargo test --all-features, (6) cargo doc --no-deps, (7) cargo deny check, (8) cargo audit for vulnerabilities, (9) Cross-compile with cross, (10) Publish to crates.io, (11) Upload binary to GitHub Releases.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      - uses: actions/cache@v4
        with:
          path: target
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
      - run: cargo fmt --check
      - run: cargo clippy --all-targets -- -D warnings
      - run: cargo test --all-features
      - run: cargo build --release
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cargo audit
      - run: cargo deny check advisories licenses sources
```

## Q48: How do you implement a CI/CD pipeline for a GraphQL API with schema validation?
**A:** GraphQL CI/CD: (1) Schema validation with graphql-inspector, (2) Breaking change detection, (3) Schema linting, (4) Test queries against mocked schema, (5) Deploy to staging and test persisted queries, (6) Query complexity analysis, (7) Depth limiting for security, (8) Schema registry (Apollo Studio), (9) Client query validation.

**Code:**
```yaml
jobs:
  schema:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npm ci
      - run: npx graphql-inspector diff schema.graphql origin/main:schema.graphql
      - run: npx graphql-inspector lint schema.graphql
      - run: npm run test:queries
  publish:
    needs: schema
    runs-on: ubuntu-latest
    steps:
      - run: npx rover subgraph publish my-graph@current \
          --schema schema.graphql \
          --name checkout \
          --routing-url https://checkout.example.com/graphql
```

## Q49: How do you implement a CI/CD pipeline for a self-hosted CI runner fleet with auto-scaling?
**A:** Auto-scaling runners: (1) Ephemeral VMs or containers, (2) Scale up based on queue depth, (3) Scale down idle runners after grace period, (4) Use spot instances for cost, (5) Runners register on startup, (6) Unregister on shutdown, (7) Tools: actions-runner-controller, gitlab-runner-autoscaler, (8) Pre-baked AMI for fast startup, (9) Use --ephemeral for one-job-per-runner.

**Code:**
```yaml
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  name: autoscaled-runner
spec:
  replicas: 5
  template:
    spec:
      ephemeral: true            # one job per runner, auto-unregister
      repository: acme/app
      labels: [self-hosted, linux]
      resources:
        requests:
          cpu: 1000m
apiVersion: actions.summerwind.dev/v1alpha1
kind: HorizontalRunnerAutoscaler
metadata:
  name: autoscaler
spec:
  scaleTargetRef:
    name: autoscaled-runner
  minReplicas: 1
  maxReplicas: 20
  metrics:
    - type: TotalNumberOfQueuedAndInFlightWorkflowRuns
      repositoryNames: [acme/app]
```

## Q50: How do you implement CI/CD for a database migration that takes hours?
**A:** Long-running migration CI/CD: (1) Break into small batches, (2) Run as background job, (3) Deploy code that reads both old/new schemas, (4) Separate pipeline triggers migration, (5) Track progress via metrics, (6) Resumable: checkpoint and resume, (7) Pipeline continues while migration runs, (8) Compare old vs new data, (9) Migration has pause/resume/rollback API, (10) Second deploy removes old schema support.

**Code:**
```yaml
jobs:
  start-migration:
    runs-on: ubuntu-latest
    steps:
      - run: ./migrate.sh --batch 10000 --resume --checkpoint ckpt/
  monitor:
    needs: start-migration
    runs-on: ubuntu-latest
    steps:
      - run: |
          until ./migrate-status.sh --done; do
            ./migrate-status.sh --progress | tee progress.log
            sleep 300
          done
  verify:
    needs: monitor
    runs-on: ubuntu-latest
    steps:
      - run: ./compare-data.sh old_schema new_schema
  contract:
    needs: verify
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh --contract         # drop old schema support
```

## Q51: How do you implement a CI/CD pipeline for a video game (Unity/Unreal Engine)?
**A:** Game CI/CD: (1) Headless build with Unity -batchmode or Unreal RunUAT, (2) Tests in headless mode, (3) Asset validation (missing textures, broken prefabs), (4) Build matrix for multiple platforms, (5) Asset bundles for streaming, (6) Platform-specific signing, (7) SteamPipe for PC, App Store for iOS, (8) Automated performance benchmarking.

**Code:**
```yaml
jobs:
  build:
    strategy:
      matrix:
        target: [StandaloneWindows64, iOS, Android]
    runs-on: ubuntu-latest
    container: unityci/editor:2021.3.18f1-linux
    steps:
      - uses: actions/checkout@v4
      - run: |
          /opt/unity/Editor/Unity -batchmode -quit \
            -projectPath /src -buildTarget ${{ matrix.target }} -executeMethod BuildScript.Build
      - run: unity-editor -batchmode -quit -runTests -testPlatform EditMode
      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.target }}
          path: Build/${{ matrix.target }}/**
      - run: ./steampipe.sh upload "$GAME_ID"
```

## Q52: How do you implement a CI/CD pipeline that handles feature branch preview environments for Kubernetes?
**A:** K8s preview envs: (1) PR open: create namespace (pr-123), (2) Deploy from PR's image tag, (3) Create ingress with hostname from PR number, (4) Deploy dependent services, (5) Seed DB with test data, (6) Run integration tests, (7) Post URL to PR, (8) Close: delete namespace, (9) Resource limits to avoid cost, (10) Auto-delete after 24h.

**Code:**
```yaml
name: Preview on K8s
on:
  pull_request:
    types: [opened, synchronize, closed]
jobs:
  preview:
    if: github.event.action != 'closed'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: kubectl create namespace pr-${{ github.event.number }} --dry-run=client -o yaml | kubectl apply -f -
      - run: helm upgrade preview ./chart \
          --namespace pr-${{ github.event.number }} \
          --set image.tag=${{ github.sha }} \
          --set ingress.host=pr-${{ github.event.number }}.preview.example.com
      - run: kubectl apply -f seed-db.yaml -n pr-${{ github.event.number }}
      - run: curl --retry 20 --fail https://pr-${{ github.event.number }}.preview.example.com
  teardown:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - run: kubectl delete namespace pr-${{ github.event.number }}
```

## Q53: How do you implement a CI/CD pipeline that uses BuildKit's inline cache for Docker builds?
**A:** BuildKit inline cache: (1) docker buildx build --cache-to type=inline --cache-from type=registry,ref=myimage:latest, (2) Cache embedded in image as separate manifest, (3) Next build pulls image and uses layers as cache, (4) No separate cache storage needed, (5) Increases image size slightly, (6) Best for small-to-medium repos.

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - run: |
          docker buildx build \
            --cache-from=type=registry,ref=registry.example.com/app:cache  \
            --cache-to=type=registry,mode=max,ref=registry.example.com/app:cache \
            --push -t registry.example.com/app:latest -t registry.example.com/app:${{ github.sha }} .
```

## Q54: How do you implement a CI/CD pipeline for a Python package with multi-version testing and publishing?
**A:** Python package CI/CD: (1) pip install -e .[dev], (2) ruff lint and format check, (3) mypy type checking, (4) Test matrix: 3.9, 3.10, 3.11, 3.12, (5) Coverage: pytest --cov, (6) Build: python -m build, (7) Publish: twine upload to PyPI on tag, (8) Docs: deploy to Read the Docs.

**Code:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        python: ['3.9', '3.10', '3.11', '3.12']
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
          cache: pip
      - run: pip install -e ".[dev]"
      - run: ruff check . && ruff format --check .
      - run: mypy src
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
  publish:
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/my-package/${{ github.ref_name }}
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

## Q55: How do you implement a CI/CD pipeline with full observability of the pipeline itself?
**A:** Pipeline observability: (1) Track pipeline duration, stage duration, pass/fail rate as Prometheus metrics, (2) OpenTelemetry tracing from commit to deployment, (3) Structured JSON logs with correlation IDs, (4) Webhook to Slack/PagerDuty on failure, (5) Grafana dashboard for trends, (6) DORA metrics: deployment frequency, lead time, change failure rate, MTTR, (7) Flakiness monitoring, (8) Cost tracking.

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "{\"ci\":\"github\",\"ref\":\"$GITHUB_REF\",\"sha\":\"$GITHUB_SHA\"}" > ci-meta.json
      - id: timing
        run: echo "start=$(date +%s%3N)" >> $GITHUB_OUTPUT
      - run: npm ci && npm test
      - id: done
        run: echo "end=$(date +%s%3N)" >> $GITHUB_OUTPUT
      - run: |
          curl -X POST -H "Content-Type: text/plain" \
            --data-binary "ci_build_duration_ms ${{ steps.done.outputs.end }} - ${{ steps.timing.outputs.start }}" \
            http://prometheus-gateway:9091/metrics/job/ci/instance/github
      - if: failure()
        run: curl -X POST -H "Content-Type: application/json" -d '{"text":"CI failed"}' ${{ secrets.SLACK_WEBHOOK }}
```

## Q56: How do you implement a CI/CD pipeline for a Go application with cross-compilation and minimal Docker images?
**A:** Go CI/CD: (1) golangci-lint run, (2) go test -race -coverprofile=coverage.out, (3) Build: GOOS=linux GOARCH=amd64 go build -ldflags="-s -w", (4) Cross-compile matrix, (5) Docker: multi-stage FROM scratch, (6) Image size: ~5-15MB, (7) Security scan with Trivy, (8) Helm deploy as non-root, (9) Go's /healthz endpoint.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
      - run: golangci-lint run ./...
      - run: go test -race -coverprofile=coverage.out ./...
      - run: go vet ./...
  cross-compile:
    needs: test
    strategy:
      matrix:
        os: [linux, darwin, windows]
        arch: [amd64, arm64]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
      - run: |
          CGO_ENABLED=0 GOOS=${{ matrix.os }} GOARCH=${{ matrix.arch }} \
            go build -trimpath -ldflags="-s -w" -o bin/app-${{ matrix.os }}-${{ matrix.arch }} ./cmd/app
      - uses: actions/upload-artifact@v4
        with:
          name: app-${{ matrix.os }}-${{ matrix.arch }}
          path: bin/
```

## Q57: How do you implement a CI/CD pipeline that automatically rolls back if error rates increase after deployment?
**A:** Automated rollback: (1) Deploy to subset of instances, (2) Monitor error rate, latency p99 vs baseline, (3) Threshold: >1% error rate increase or >20% latency increase triggers rollback, (4) Rollback: revert to previous version, (5) Analysis window: 5-15 minutes, (6) Tools: Flagger, Argo Rollouts, (7) Integrate with APM tools, (8) Never auto-rollback outside business hours.

**Code:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: web
spec:
  replicas: 4
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: registry.example.com/web:2.0.0
  strategy:
    canary:
      steps:
        - setWeight: 25
        - pause: { duration: 5m }
        - setWeight: 50
        - pause: { duration: 5m }
        - setWeight: 100
      analysis:
        templates:
          - templateName: error-rate
        args:
          - name: service-name
            value: web-prod
```

## Q58: How do you implement a CI/CD pipeline for a data pipeline (Airflow DAGs, dbt models)?
**A:** Data pipeline CI/CD: (1) Lint DAGs, (2) Test DAGs with mocked Airflow, (3) dbt: compile, test, (4) dbt build --select state:modified+, (5) Schema tests on staging, (6) Data quality: Great Expectations, (7) Deploy: sync DAGs to Airflow, (8) Trigger DAG runs with config, (9) dbt docs generation, (10) Rollback: revert DAG files.

**Code:**
```yaml
jobs:
  dbt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: pip
      - run: pip install dbt-bigquery apache-airflow
      - run: python -m compileall dags//
      - run: ruff check dags/
      - run: dbt deps
      - run: dbt debug --target staging
      - run: dbt run --target staging --select state:modified+
      - run: dbt test --target staging
      - run: dbt docs generate --target staging
      - run: airflow dags list
```

## Q59: How do you implement a CI/CD pipeline for a Cross-Platform Desktop App (Electron, Tauri)?
**A:** Desktop app CI/CD: (1) Build matrix per OS, (2) Build with npm run build or cargo tauri build, (3) Code sign: macOS codesign, Windows Authenticode, (4) Notarize for macOS, (5) Package: dmg, exe/msi, AppImage/deb, (6) Auto-update server, (7) Tests with Spectron, (8) Security scan with Snyk.

**Code:**
```yaml
jobs:
  build:
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci && npm run test:unit
      - if: runner.os == 'macOS'
        run: |
          cargo build --release --target aarch64-apple-darwin
          npx electron-builder --mac dmg --publish never
      - run: npm run build && npx electron-builder --publish never
      - uses: actions/upload-artifact@v4
        with:
          name: dist-${{ matrix.os }}
          path: dist/
```

## Q60: How do you implement a CI/CD pipeline that automatically generates and publishes a changelog?
**A:** Automated changelog: (1) Parse git log between last tag and HEAD, (2) Conventional Commits: feat, fix, BREAKING CHANGE sections, (3) Tools: git-cliff, semantic-release, conventional-changelog, (4) Format: Markdown with links to commits/PRs, (5) Generate on merge to main or tag creation, (6) Commit CHANGELOG.md to repo, (7) Attach to Release on GitHub.

**Code:**
```yaml
name: Changelog
on:
  push:
    tags: ['v*']
jobs:
  changelog:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: orhun/git-cliff-action@v4
        with:
          config: cliff.toml
          args: -vv --latest --strip header
      - run: git add CHANGELOG.md && git commit -m "docs: update changelog" && git push
      - uses: softprops/action-gh-release@v2
        with:
          body_path: CHANGELOG.md
          generate_release_notes: true
```

## Q61: How do you implement a CI/CD pipeline that handles A/B testing infrastructure?
**A:** A/B testing CI/CD: (1) Feature flags as code in version control, (2) Validate flags have descriptions, owners, expiry dates, (3) Deploy variant code behind flag, (4) Register experiment in analytics tools, (5) Traffic split via flag tool, (6) Create dashboards for experiment metrics, (7) Cleanup: remove flag code, roll out winner, (8) Rollback: disable flag.

**Code:**
```yaml
jobs:
  validate-flags:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          for f in flags/*.yaml; do
            yq eval '. | required_fields(.name) | required(.owner) | required(.expiry) | required(.split)' $f
          done
  deploy-experiment:
    needs: validate-flags
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh --flag checkout-redesign --split 50:50
      - run: ./register-experiment.sh checkout-redesign metrics=conversion,revenue
  analyze:
    needs: deploy-experiment
    runs-on: ubuntu-latest
    steps:
      - run: ./analyze-experiment.sh checkout-redesign --window 14d
      - run: ./finalize-experiment.sh checkout-redesign --winner variant_b
```

## Q62: How do you implement a CI/CD pipeline for a WebSocket-heavy application?
**A:** WebSocket CI/CD: (1) Unit tests with mock WS server, (2) Integration tests connecting to deployed service, (3) Load tests with artillery, (4) Test max concurrent connections, (5) E2E tests in browser (Cypress), (6) Graceful shutdown: drain connections on SIGTERM, (7) Track connected clients and message throughput.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run test:unit
      - run: npm run test:ws-integration
  load:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: |
          npm run start:ws & SERVER=$!
          sleep 5
          npx artillery run ws-load.yml --output ws-report.json
          kill $SERVER
      - run: npx artillery report ws-report.json --output ws-report.html
      - uses: actions/upload-artifact@v4
        with:
          name: ws-report
          path: ws-report.*
```

## Q63: How do you implement a CI/CD pipeline for a DBaaS or managed database offering?
**A:** DBaaS CI/CD: (1) Test against multiple DB versions, (2) Snapshot testing of query results, (3) Test backup creation/restoration, (4) Performance regression detection, (5) Test migrations against production-scale data, (6) Chaos testing: kill DB process and verify recovery, (7) Test failover and consistency, (8) Penetration testing, (9) Audit log verification.

**Code:**
```yaml
jobs:
  compatibility:
    strategy:
      matrix:
        postgres: [14, 15, 16]
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:${{ matrix.postgres }}
        env:
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v4
      - run: export PGPASSWORD=test && createdb -h localhost -U postgres app_test
      - run: psql -h localhost -U postgres -d app_test -f schema.sql
      - run: go test ./... -run TestQueries
  backup-restore:
    runs-on: ubuntu-latest
    steps:
      - run: pg_dump -h localhost -Fc db > backup.dump
      - run: pg_restore -h localhost -d restored_backup backup.dump
      - run: ./chaos-test.sh kill --expect-recovery
```

## Q64: How do you implement CI/CD for HSM or cryptographic services?
**A:** HSM CI/CD: (1) Never store keys in CI/CD, use KMS key IDs, (2) Test with SoftHSM in CI, (3) Integration tests with real HSM in staging, (4) Key rotation triggers and validation, (5) FIPS 140-2 validation step, (6) Audit logging, (7) PKI: test cert generation and signing, (8) Benchmark crypto operations.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          apt-get update && apt-get install -y softhsm2
          softhsm2-util --init-token --free --label test-hsm --so-pin 1234 --pin 1234
          mkdir -p /tmp/tokens && printf "directories.tokendir = /tmp/tokens" > softhsm2.conf
          SOFTHSM2_CONF=softhsm2.conf go test ./crypto/... -tags=softhsm
  integration:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: ./rotate-keys.sh --hsm $KMS_KEY_ID
      - run: ./verify-fips.sh --config fips.conf
      - run: ./sign-test.sh --hsm $KMS_KEY_ID
```

## Q65: How do you implement CI/CD pipelines using reusable workflows to reduce duplication?
**A:** Reusable CI/CD: (1) GitHub Actions: reusable workflow with workflow_call, (2) Callers: uses: ./.github/workflows/reusable.yml, (3) GitLab: include: local: template, (4) Jenkins: shared library, (5) Parameterization: language, build command, test command, (6) Pin reusable workflow versions, (7) Common steps: checkout, setup, cache.

**Code:**
```yaml
# .github/workflows/reusable-ci.yml
name: Reusable CI
on:
  workflow_call:
    inputs:
      service:
        type: string
        required: true
    secrets:
      token:
        required: true
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd ${{ inputs.service }} && npm ci && npm test
```
```yaml
# Caller workflow
name: Payments CI
on: push
jobs:
  ci:
    uses: ./.github/workflows/reusable-ci.yml
    with:
      service: services/payments
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

## Q66: How do you implement a CI/CD pipeline for a documentation site with versioned docs?
**A:** Versioned docs CI/CD: (1) Source in /docs alongside code, (2) Docusaurus, VuePress, or MkDocs, (3) Each git tag creates new docs version, (4) Version dropdown for users, (5) Markdown linting and broken link checking, (6) PR preview of doc site, (7) Algolia DocSearch reindex on deploy, (8) Publish to S3/CloudFront, (9) /latest redirect.

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: npx markdownlint-cli2 docs/
      - run: npx broken-link-checker mmarkdown docs
      - run: npm ci && npm run docusaurus docs:version ${{ github.ref_name }}
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: build/
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
      - run: aws cloudfront create-invalidation --distribution-id $DISTRO --paths '/*'
```

## Q67: How do you implement a CI/CD pipeline for a gRPC service with protobuf compilation?
**A:** gRPC CI/CD: (1) buf lint, (2) buf breaking --against .git, (3) buf generate for stubs, (4) Build generated code, (5) Unit + integration tests, (6) Contract tests: verify all RPCs implemented, (7) Load test with ghz, (8) Publish generated clients to registry, (9) BSR for proto management.

**Code:**
```yaml
jobs:
  proto:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: bufbuild/buf-action@v1
        with:
          lint: true
          breaking: '{"against": ".git}", "buf_token": "${{ secrets.BUF_TOKEN }}"}'
      - run: buf generate
      - run: go build ./... && go test ./...
      - run: ghz --insecure --proto api/checkout.proto --call checkout.v1.CheckoutService/Pay \
          --total 10000 --concurrency 200 localhost:9090
```

## Q68: How do you implement a CI/CD pipeline for a Firebase/Firestore application?
**A:** Firebase CI/CD: (1) Tests against Firebase Emulator Suite, (2) Security rules testing, (3) firebase deploy --only functions,firestore,hosting, (4) Multiple projects: staging vs prod, (5) TypeScript compile, lint, test, deploy, (6) CI service account with restricted permissions.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx tsc --noEmit
      - run: npm run lint
      - run: firebase emulators:exec --only firestore,functions "npm test"
      - run: npx @firebase/rules-unit-testing
  deploy:
    needs: test
    environment:
      name: firebase-${{ github.ref_name == 'main' && 'prod' || 'staging' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: firebase deploy --only firestore:rules,functions,hosting
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_TOKEN }}
```

## Q69: How do you implement a CI/CD pipeline for CDK (AWS CDK) or Pulumi infrastructure?
**A:** CDK/Pulumi CI/CD: (1) cdk synth generates CloudFormation, (2) cdk diff as PR comment, (3) cdk-nag for compliance, (4) eslint for CDK code, (5) cdk deploy to dev on merge, (6) Manual approval for prod, (7) Snapshots for CDK testing, (8) pulumi preview and up, (9) State stored with locking.

**Code:**
```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: cdk synth
      - run: cdk-nag --severity ERROR --cdk-app cdk synth
      - run: npm test -- --snapshots
  deploy:
    needs: check
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: cdk diff
      - run: cdk deploy --all --require-approval never
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      - run: pulumi stack select prod && pulumi update -y
```

## Q70: How do you implement a CI/CD pipeline for an NPM workspace monorepo with inter-package dependencies?
**A:** NPM workspace CI/CD: (1) npm ci --workspaces, (2) npm run build --workspaces (dependency order), (3) npm test --workspaces --if-present, (4) npm pack per package, (5) npm publish --workspace=@scope/module for changed packages, (6) Use lerna changed or nx affected, (7) Cache .npm for npm ci, (8) Build/test only affected packages.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci --workspaces
      - run: npm run build --workspaces --if-present
      - run: npm test --workspaces --if-present
      - run: npx nx affected --base=origin/main --targets=build,test
  publish:
    needs: test
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci --workspaces
      - run: npx lerna publish from-package --yes --no-verify-access
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Q71: How do you implement a CI/CD pipeline for a WebAssembly (Wasm) application?
**A:** Wasm CI/CD: (1) Compile to Wasm target, (2) Optimize with wasm-opt, (3) Test in Wasmtime runtime, (4) Size budget: fail if .wasm exceeds limit, (5) Integration test from JavaScript, (6) Test shared memory for threading, (7) Publish to npm or CDN, (8) Benchmark vs native baseline.

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          target: wasm32-unknown-unknown
      - run: cargo build --release --target wasm32-unknown-unknown
      - run: wasm-opt -Oz -o app.opt.wasm target/wasm32-unknown-unknown/release/app.wasm
      - run: wasmtime app.opt.wasm --invoke main
      - run: |
          SIZE=$(stat -c%s app.opt.wasm)
          echo "wasm size: $SIZE bytes"
          [ "$SIZE" -le $((1 * 1024 * 1024)) ] || { echo "size budget exceeded"; exit 1; }
      - run: node test/integration.mjs
      - uses: actions/upload-artifact@v4
        with:
          name: wasm-module
          path: app.opt.wasm
```

## Q72: How do you implement a CI/CD pipeline that handles database-per-developer for testing?
**A:** Database-per-dev: (1) PR creates new DB container with migration, (2) Seed with sanitized prod data, (3) Run integration tests, (4) Destroy on completion, (5) Use ephemeral PostgreSQL containers, (6) Each test run gets isolated DB, (7) Parallel test execution with unique DB names, (8) Snapshot seeding for faster setup.

**Code:**
```yaml
jobs:
  integration:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
    steps:
      - uses: actions/checkout@v4
      - run: |
          export PGPASSWORD=test
          DB="app_dev_${GITHUB_SHA::7}_shard${{ matrix.shard }}"
          createdb -h localhost -U postgres "$DB"
          psql -h localhost -U postgres -d "$DB" -f schema.sql
          ./seed-db.sh "$DB"
          DATABASE_URL="postgresql://postgres:test@localhost/$DB" make test-integration
```

## Q73: How do you implement a CI/CD pipeline that performs chaos engineering tests before deployment?
**A:** Chaos engineering CI/CD: (1) Deploy to staging, (2) Run chaos experiments: kill pods, network latency, CPU stress, (3) Verify system recovers within SLO, (4) Tools: Chaos Mesh, Litmus, Gremlin, (5) Experiments defined as code in repo, (6) Pass/fail criteria: p99 latency, error rate, (7) Block production deployment if chaos tests fail, (8) Run in canary environment first.

**Code:**
```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - run: kubectl create ns chaos || true
      - run: helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos
      - run: kubectl apply -f experiments/node-chaos.yaml -n chaos
  chaos-run:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - run: litmus create experiment -f experiments/pod-delete.yaml
      - run: litmus check experiment --name pod-delete
      - run: ./assert-slo.sh --p99 500 --error-rate 0.01
  gater:
    needs: chaos-run
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: echo '::error::Chaos test failed, blocking production deploy' && exit 1
```

## Q74: How do you implement a CI/CD pipeline for a multi-module Maven project?
**A:** Maven multi-module CI/CD: (1) mvn validate, (2) mvn compile, (3) mvn test (unit), (4) mvn verify (integration), (5) mvn site (reports), (6) Dependency graph: changed modules only with mvn -pl, (7) mvn deploy to artifact repository, (8) Versioning: maven-release-plugin, (9) Cache .m2/repository between runs.

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 21
          cache: maven
      - run: mvn -B validate
      - run: mvn -B compile
      - run: mvn -B test
      - run: |
          CHANGED=$(git diff --name-only origin/main | cut -d/ -f1 | sort -u | tr '\n' ',' | sed 's/,$//')
          mvn -pl "$CHANGED" -am verify -DskipTests=false
      - run: mvn -B deploy
        env:
          MAVEN_USERNAME: ${{ secrets.MAVEN_USERNAME }}
          MAVEN_PASSWORD: ${{ secrets.MAVEN_PASSWORD }}
```

## Q75: How do you implement a CI/CD pipeline that handles zero-downtime deployments for stateful services?
**A:** Stateful service CI/CD: (1) Blue-green: deploy new version alongside old, switch traffic, (2) Database: backward-compatible migrations only, (3) Session draining: wait for active sessions to complete, (4) Health checks: readiness probe before routing traffic, (5) Graceful shutdown: SIGTERM handling, (6) Auto-rollback on health check failure, (7) Data migration as separate job.

**Code:**
```yaml
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - run: ./backward-compatible-migrate.sh
  blue-green:
    needs: migrate
    runs-on: ubuntu-latest
    steps:
      - run: kubectl apply -f deploy-green.yaml
      - run: kubectl rollout status deployment/app-green
      - run: kubectl wait --for=condition=Ready pod -l version=green --timeout=120s
      - run: kubectl drain connections --graceful-timeout=60
      - run: kubectl patch service/app -p '{"spec":{"selector":{"version":"green"}}}'
      - run: kubectl delete deployment/app-blue
```

## Q76: How do you implement a CI/CD pipeline for a Ruby on Rails application?
**A:** Rails CI/CD: (1) bundle install --jobs 4, (2) rubocop lint, (3) rails db:create db:migrate, (4) rails test (unit + integration), (5) rspec for spec tests, (6) brakeman for security, (7) bundler-audit for gem vulnerabilities, (8) Precompile assets: rails assets:precompile, (9) Deploy: capistrano or kamal.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
    env:
      RAILS_ENV: test
      DATABASE_URL: postgresql://postgres:test@localhost/app_test
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true
      - run: bundle exec rubocop --parallel
      - run: bundle exec rails db:create && bundle exec rails db:migrate
      - run: bundle exec rspec
      - run: bundle exec brakeman -q -w2
      - run: bundle exec bundler-audit check --update
      - run: bin/rails assets:precompile
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: bundle exec cap production deploy
```

## Q77: How do you implement a CI/CD pipeline that performs contract testing between microservices?
**A:** Contract testing CI/CD: (1) Provider publishes contract (Pact file), (2) Consumer tests use pact file to mock provider, (3) CI runs consumer tests with pact file, (4) CI runs provider verification against pact file, (5) Pact Broker stores contract versions, (6) Can-i-deploy: check if consumer and provider versions are compatible, (7) Matrix testing across versions.

**Code:**
```yaml
jobs:
  consumer:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
      - run: npm run pact:pactum -- --pact-broker ${{ secrets.PACT_BROKER_URL }}
  provider:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          ./start-api.sh & API_PID=$!
          npm run pact:verify -- --pact-broker ${{ secrets.PACT_BROKER_URL }} --provider checkout-api
      - run: pact-broker can-i-deploy \
          --pacticipant checkout-api --version $GITHUB_SHA --to production
```

## Q78: How do you implement a CI/CD pipeline for a Kubernetes operator?
**A:** K8s operator CI/CD: (1) Lint: golangci-lint, (2) Unit tests with envtest (controller-runtime), (3) Integration tests with kind (K8s in Docker), (4) Build operator image, (5) Deploy to test cluster, (6) Run E2E tests: create CR, verify controller response, (7) Scorecard tests (operator-sdk scorecard), (8) Publish to OperatorHub or OLM registry.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
      - run: make lint
      - run: KUBEBUILDER_ASSETS=$(setup-envtest use -p path) make test
      - run: make generate && git diff --exit-code
      - uses: helm/kind-action@v1
      - run: make deploy
      - run: kubectl apply -f test/cr.yaml && kubectl wait --for=condition=Ready app -n operators
      - run: operator-sdk scorecard bundle/ --kubeconfig $HOME/.kube/kind-config-kind
```

## Q79: How do you implement CI/CD for a Peloton/indoor cycling or fitness app with device-specific firmware?
**A:** Fitness app CI/CD: (1) Mobile app pipeline (iOS + Android), (2) Firmware pipeline: cross-compile for MCU, (3) Hardware testing with test rigs in CI, (4) BLE/ANT+ connectivity tests, (5) Firmware OTA update packaging, (6) Integration tests: mobile <-> device communication, (7) Performance: sensor data latency.

**Code:**
```yaml
jobs:
  firmware:
    strategy:
      matrix:
        board: [bike, treadmill, rower]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker run --rm -v $PWD:/src mcu-toolchain make BOARD=${{ matrix.board }} firmware
      - run: pytest tests/hardware/ -m BLE
      - run: ./pack-ota.sh ${{ matrix.board }} --version $GITHUB_SHA
      - uses: actions/upload-artifact@v4
        with:
          name: ota-${{ matrix.board }}
          path: ota/
  mobile:
    runs-on: macos-latest
    steps:
      - run: fastlane ios beta
      - run: fastlane android beta
```

## Q80: How do you implement a CI/CD pipeline that validates Dockerfile best practices and security?
**A:** Dockerfile validation: (1) hadolint for Dockerfile linting, (2) dockle for image best practices, (3) Trivy for vulnerability scanning, (4) Check: no hardcoded secrets, no root user, (5) Label validation: maintainer, version, (6) Multi-stage build verification, (7) Size check: fail if image exceeds threshold, (8) SBOM generation and verification.

**Code:**
```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: hadolint Dockerfile
      - run: docker build -t app:${{ github.sha }} .
      - run: dockle --exit-code 1 app:${{ github.sha }}
      - run: trivy image --exit-code 1 --severity HIGH,CRITICAL app:${{ github.sha }}
      - run: |
          SIZE=$(docker image inspect app:${{ github.sha }} --format '{{.Size}}')
          SIZE_MB=$((SIZE / 1000000))
          echo "image size: ${SIZE_MB}MB"
          [ "$SIZE_MB" -le 500 ] || { echo "image exceeds 500MB budget"; exit 1; }
      - run: syft app:${{ github.sha }} -o cyclonedx > sbom.json
      - run: grep -rE "AKIA|password=|secret=" Dockerfile && exit 1 || true
```

## Q81: How do you implement a CI/CD pipeline for a Django application?
**A:** Django CI/CD: (1) pip install -r requirements.txt, (2) ruff or flake8 lint, (3) pytest with coverage, (4) python manage.py check --deploy, (5) python manage.py collectstatic --noinput, (6) python manage.py migrate (pre-deploy), (7) Build: Docker image, (8) Deploy with gunicorn + nginx, (9) Security: django-check-seo, django-security-check.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
    env:
      DATABASE_URL: postgresql://postgres:test@localhost/db
      DJANGO_SETTINGS_MODULE: core.settings.ci
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest --cov=. --cov-report=xml
      - run: python manage.py check --deploy
      - run: python manage.py migrate && python manage.py collectstatic --noinput
      - run: python manage.py check --deploy --fail-level WARNING
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t registry.example.com/web:${{ github.sha }} .
      - run: docker push registry.example.com/web:${{ github.sha }}
      - run: ansible-playbook deploy.yml --extra-vars "image_tag=${{ github.sha }}"
```

## Q82: How do you implement a CI/CD pipeline for a chatbot/AI assistant application?
**A:** Chatbot CI/CD: (1) NLP pipeline: train/test NLU model, (2) Intent classification accuracy check, (3) Conversation flow tests (Rasa, Dialogflow), (4) API integration tests, (5) Performance: response time budget, (6) Deploy model + bot server, (7) A/B test conversations, (8) Monitor: user satisfaction, fallback rate.

**Code:**
```yaml
jobs:
  train-and-eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install rasa
      - run: rasa train
      - run: rasa test
      - run: |
          ACCURACY=$(rasa test nlu --cross-validation --fold 5 2>&1 | grep -oP 'accuracy:\s+\K[0-9.]+')
          python -c "import sys; sys.exit(0 if float('$ACCURACY') >= 0.85 else 1)"
      - run: rasa test core --evaluate missing
  perf:
    needs: train-and-eval
    runs-on: ubuntu-latest
    steps:
      - run: python scripts/load_test.py --rps 50 --max-latency 300ms
```

## Q83: How do you implement a CI/CD pipeline that uses artifact promotion across environments?
**A:** Artifact promotion: (1) Build once, promote across environments, (2) Each environment gets the same artifact digest, (3) Promotion: dev -> (test passed) -> staging -> (approval) -> prod, (4) Use immutable tags (sha256 digest), (5) Promotion metadata: who, when, which tests passed, (6) Promotion gate: automated checks, manual approval.

**Code:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm ci && npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: app-${{ github.sha }}
          path: dist/
      - run: echo "${{ github.sha }}" > image.digest.txt
      - uses: actions/upload-artifact@v4
        with:
          name: digest
          path: image.digest.txt
  promote-dev:
    needs: build
    runs-on: ubuntu-latest
    environment: development
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app-${{ github.sha }}
      - run: ./deploy.sh dev --digest ${{ github.sha }}
  promote-staging:
    needs: promote-dev
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: ./deploy.sh staging --digest ${{ github.sha }}
  promote-prod:
    needs: promote-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - run: ./deploy.sh production --digest ${{ github.sha }}
```

## Q84: How do you implement a CI/CD pipeline for a financial trading application?
**A:** Trading app CI/CD: (1) Low-latency performance tests, (2) Market data feed simulation, (3) Order matching engine tests, (4) FIX protocol conformance testing, (5) Risk checks: position limits, circuit breakers, (6) Audit logging verification, (7) Multi-region deployment, (8) Canary with synthetic orders, (9) Rollback to previous binary instantly.

**Code:**
```yaml
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
      - run: go build ./...
      - run: go test ./matching/... ./risk/... -race
      - run: go test ./fix/... -run TestFIXConformance -tags=fix
      - run: ./simulate-market-feed.sh --streams 4 --ticks 1e6
      - run: ./latency-benchmark.sh --p99-budget 50us
  deploy:
    needs: build-test
    runs-on: ubuntu-latest
    steps:
      - run: ./canary-deploy.sh --region us-east-1 --synthetic-orders on
      - run: ./verify-audit-logs.sh
```

## Q85: How do you implement a CI/CD pipeline that generates release notes from issue tracker data?
**A:** Release notes from issues: (1) Link commits to issues via conventional commits, (2) Fetch issue titles/labels from Jira/GitHub API, (3) Categorize: features, bugs, improvements, (4) Include issue links and commit SHAs, (5) Auto-generate release notes template, (6) Allow manual edits before publishing, (7) Attach to GitHub/GitLab Release.

**Code:**
```yaml
jobs:
  release-notes:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: |
          echo "# Release ${{ github.ref_name }}" > notes.md
          git log --pretty=format:'- %s (fixes #%s)' ${{ github.event.before }}..HEAD \
            | sort | uniq >> notes.md
          gh api graphql -f query='
            query($owner:String!, $name:String!) {
              repository(owner:$owner,name:$name) {
                issues(last:50, states:CLOSED) { edges { node { number title labels(first:5){nodes{name}} } } }
              }
            }' -F owner=acme -F name=app >> issues.json
      - run: ./render-notes.sh notes.md issues.json > FINAL_NOTES.md
      - uses: softprops/action-gh-release@v2
        with:
          body_path: FINAL_NOTES.md
```

## Q86: How do you implement CI/CD for a machine learning pipeline with feature store and model registry?
**A:** ML pipeline CI/CD: (1) Feature engineering tests, (2) Feature store validation (Tecton, Feast), (3) Model training with experiment tracking (MLflow), (4) Model evaluation: accuracy, precision, recall vs baseline, (5) Model registry: promote if passes, (6) Batch prediction pipeline tests, (7) Online serving: deploy model to endpoint, (8) Monitor: prediction drift, data drift.

**Code:**
```yaml
jobs:
  validate-features:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          feast plan --apply
          pytest tests/features/ -m "not slow"
  train:
    needs: validate-features
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: mlflow run . --experiment-name recsys --entry-point train
  evaluate:
    needs: train
    runs-on: ubuntu-latest
    steps:
      - run: |
          python evaluate_model.py \
            --candidate-model "${{ needs.train.outputs.model_uri }}" \
            --baseline production
          mlflow models stage "${{ needs.train.outputs.model_uri }}" --stage Staging
  deploy:
    needs: evaluate
    runs-on: ubuntu-latest
    steps:
      - run: mlflow models deploy -m models:/recsys/Staging --target kubernetes --name recsys
      - run: ./monitor-drift.sh --alerts-on
```

## Q87: How do you implement a CI/CD pipeline for a WebRTC application?
**A:** WebRTC CI/CD: (1) Build signaling server, (2) Build TURN/STUN server config, (3) Unit tests for signaling logic, (4) Integration tests with browser WebRTC API, (5) Connection quality tests: latency, jitter, packet loss, (6) Load test: concurrent calls, (7) Deploy signaling + media servers, (8) Monitor: call success rate, quality metrics.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run test:unit
      - run: npm run test:signaling
      - run: npx playwright test --test-dir e2e --grep webrtc
      - run: npm run test:turn -- --config turnserver.conf
  load:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: |
          ./start-media-server.sh &
          npx artillery run webrtc-load.yml --output report.json
          kill %1
      - run: ./quality-check.sh --max-jitter 30 --max-latency 150 --max-loss 0.02
```

## Q88: How do you implement a CI/CD pipeline that performs canary analysis with Prometheus metrics?
**A:** Canary analysis with Prom: (1) Deploy canary with label canary=true, (2) Prometheus queries compare canary vs baseline metrics, (3) Metrics: request rate, error rate, latency p50/p95/p99, (4) Statistical test: Mann-Whitney U test or mean comparison, (5) Pass: promote canary, (6) Fail: rollback, (7) Tools: Kayenta, Flagger, (8) Configurable thresholds per metric.

**Code:**
```yaml
apiVersion: flagger.app/v1beta1
kind: MetricTemplate
metadata:
  name: kube-metrics
spec:
  provider:
    type: prometheus
    address: http://prometheus:9090
  query: |
    histogram_quantile(0.99,
      sum(irate({{- index .Labels "job" }}{{ if .Metric }}[{{ .Metric }}]{{ end }}[1m])) by (le)
    )
---
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: web
spec:
  analysis:
    metrics:
      - name: error-rate
        templateRef: { name: kube-metrics }
        thresholdRange: { max: 1 }
      - name: latency
        templateRef: { name: kube-metrics }
        threshold: 500
      - name: request-success-rate
        thresholdRange: { min: 99 }
        interval: 1m
```

## Q89: How do you implement a CI/CD pipeline for a SaaS product with free, pro, and enterprise tiers?
**A:** Multi-tier CI/CD: (1) Feature flags per tier, (2) Tier-specific configuration in repo, (3) CI validates tier configs, (4) Tests run per tier (free tests faster, enterprise tests comprehensive), (5) Deploy per tier: shared cluster with tier isolation or separate clusters, (6) Enterprise: customer-specific branches/tags.

**Code:**
```yaml
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          for tier in free pro enterprise; do
            python validate_tier_config.py configs/$tier.yaml
          done
  test:
    needs: validate
    strategy:
      matrix:
        tier: [free, pro, enterprise]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest --tier=${{ matrix.tier }} --exitfirst
  deploy:
    needs: test
    strategy:
      matrix:
        tier: [free, pro, enterprise]
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh --tier ${{ matrix.tier }} --feature-flags configs/${{ matrix.tier }}/flags.yaml
```

## Q90: How do you implement a CI/CD pipeline that automatically rolls back database migrations on deployment failure?
**A:** Migration rollback: (1) Before deploy: backup database, (2) Run migrations as pre-deploy hook, (3) If deploy fails: automatically run rollback migration, (4) If rollback migration fails: manual intervention needed, (5) Rollback verification: compare schema and data counts, (6) Only auto-rollback for additive changes, (7) Destructive changes require manual rollback.

**Code:**
```yaml
jobs:
  pre-deploy:
    runs-on: ubuntu-latest
    steps:
      - run: ./backup-db.sh --out backup-${{ github.sha }}.dump
      - run: flyway migrate
  verify:
    needs: pre-deploy
    runs-on: ubuntu-latest
    steps:
      - run: ./smoke-test.sh --min-replicas 3
  rollback-db:
    needs: verify
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: flyway undo --target ${{ vars.LAST_GOOD_VERSION }}
      - run: ./verify-schema.sh --expect $LAST_GOOD_SCHEMA
      - run: pg_restore backup-${{ github.sha }}.dump
  notify:
    needs: [verify, rollback-db]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - if: failure()
        run: curl -X POST -H "Content-Type: application/json" -d '{"text":"Migration rollback needed manual review"}' ${{ secrets.SLACK_WEBHOOK }}
```

## Q91: How do you implement a CI/CD pipeline for an e-commerce platform with complex business logic?
**A:** E-commerce CI/CD: (1) Build: frontend + backend + services, (2) Pricing engine tests, (3) Inventory management tests, (4) Payment gateway integration tests (sandbox), (5) Cart/checkout flow E2E tests, (6) Performance: Black Friday load simulation, (7) Order processing pipeline tests, (8) Deploy with feature flags for promotions, (9) Rollback: revert pricing changes instantly.

**Code:**
```yaml
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:pricing-engine
      - run: npm run test:inventory
      - run: npm run test:order-processing
  integration:
    needs: unit
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
    steps:
      - run: npm run test:payment-gateway -- --sandbox stripe
  e2e:
    needs: integration
    runs-on: ubuntu-latest
    steps:
      - uses: cypress-io/github-action@v6
        with:
          start: npm start
          spec: cypress/e2e/checkout.cy.js
  perf:
    needs: e2e
    runs-on: ubuntu-latest
    steps:
      - run: k6 run --vus 1000 --duration 5m black-friday.js
  deploy:
    needs: perf
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh --flags promo-black-friday --weight 10
```

## Q92: How do you implement CI/CD with trunk-based development and short-lived feature branches?
**A:** Trunk-based CI/CD: (1) Feature branches last <1 day, (2) Small commits directly to main, (3) Feature flags for incomplete features, (4) CI runs on every push to main, (5) Automatic deployment to staging after merge, (6) No release branches, (7) Continuous deployment to prod after tests pass, (8) Rollback via feature flag disable.

**Code:**
```yaml
name: Trunk
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test && npm run lint
  deploy-staging:
    needs: ci
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: ./deploy.sh staging
  deploy-prod:
    needs: deploy-staging
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./deploy.sh production --flags rollout-controlled
```

## Q93: How do you implement a CI/CD pipeline for an SDK/library that needs to support multiple API versions?
**A:** Multi-version SDK CI/CD: (1) Matrix: API versions [v1, v2, v3], (2) Test SDK against each API version, (3) Deprecation tests: verify deprecation warnings for old versions, (4) Breaking change: new major version as separate package, (5) Compatibility tests: SDK compiled with old API works with new backend, (6) Version-specific docs.

**Code:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        api: [v1, v2, v3]
        sdk: ['3.x', '4.x']
    runs-on: ubuntu-latest
    services:
      api:
        image: myapi:${{ matrix.api }}
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build -- --version ${{ matrix.sdk }}
      - run: npm run test:compat -- --api ${{ matrix.api }}
      - run: npm run test:deprecation -- --api ${{ matrix.api }}
  publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: ./publish.sh --publish-version ${{ github.ref_name }}
```

## Q94: How do you implement a CI/CD pipeline for a healthcare application with HIPAA compliance?
**A:** HIPAA CI/CD: (1) PHI detection in logs and artifacts, (2) Encryption verification: data encrypted at rest and in transit, (3) Audit logging pipeline events, (4) Access control: role-based access to CI/CD, (5) Static analysis for security flaws, (6) Dependency vulnerability scanning, (7) Signed artifacts for integrity, (8) BA agreement with CI/CD provider.

**Code:**
```yaml
jobs:
  compliance-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: gitleaks detect --redact
      - run: ./scan-for-phi.sh --paths logs/ artifacts/
      - run: pip-audit && npm audit
      - run: ./verify-encryption.sh --at-rest --in-transit
      - run: semgrep scan --config p/security
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./emit-audit-event.sh action=gherkin-deploy who=githuak actor=$GITHUB_SHA
      - run: cosign sign --yes artifact.tar.gz
```

## Q95: How do you implement CI/CD for a monorepo with shared internal packages using Yarn PnP or pnpm?
**A:** PnP/pnpm CI/CD: (1) pnpm install --frozen-lockfile, (2) pnpm build (respects dependency graph), (3) pnpm test -r, (4) pnpm lint -r, (5) pnpm deploy --filter=@scope/package for publishing, (6) Changeset for version management, (7) CI validates changeset files on PRs, (8) Cache .pnpm-store, (9) Parallel test execution.

**Code:**
```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm build -r
      - run: pnpm test -r --workspace-concurrency=4
      - run: pnpm lint -r
      - run: npx changeset status
  publish:
    needs: ci
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - run: pnpm install --frozen-lockfile
      - run: npx changeset publish --tag latest
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Q96: How do you implement a CI/CD pipeline that supports database change management with schema drift detection?
**A:** Schema drift detection: (1) Store expected schema as SQL file in repo, (2) CI compares actual DB schema vs expected, (3) Drift detection: run on schedule and on deploy, (4) Alert on unexpected schema changes, (5) Auto-remediation: apply missing changes or flag for manual review, (6) Tools: schemachange, sqldef, (7) CI blocks deployment if schema drift is detected.

**Code:**
```yaml
jobs:
  drift-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          sqldef --file desired_schema.sql \
            --host prod-db --user deploy --password ${{ secrets.DB_PASSWORD }} \
            --diff-only || DRIFT=$?
          if [ -n "$DRIFT" ]; then
            echo '::error::Schema drift detected against production'
            exit 1
          fi
  deploy:
    needs: drift-check
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

## Q97: How do you implement a CI/CD pipeline for a system that uses event sourcing and CQRS?
**A:** Event sourcing CI/CD: (1) Event schema validation, (2) Event store migration tests, (3) Projection rebuild tests, (4) CQRS: test command side and query side independently, (5) Event replay: verify projections produce same state, (6) Backward compatibility: events cannot be deleted, only superseded, (7) Integration: verify command produces expected events.

**Code:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:event-schema
      - run: npm run test:command-side
      - run: npm run test:query-side
      - run: npm run test:event-store-migration
      - run: |
          ./replay-events.sh --from backup.events \
            --expect-state snapshot.golden.json
      - run: npm run test:projection-rebuild
```

## Q98: How do you implement a CI/CD pipeline for a blockchain or smart contract application?
**A:** Blockchain CI/CD: (1) Compile smart contracts (Solidity, Rust), (2) Unit tests with local testnet (Ganache, Hardhat), (3) Security analysis: Slither, Mythril, (4) Gas estimation and optimization, (5) Integration tests on testnet, (6) Contract verification (Etherscan), (7) Multi-sig deployment, (8) Upgradeability tests for proxy contracts.

**Code:**
```yaml
jobs:
  test-and-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npx hardhat compile
      - run: npx hardhat test
      - run: npx hardhat coverage
      - run: slither . --fail-high
      - run: myth analyze contracts/ --fail-on high
      - run: npx hardhat gas-estimation
  integrate-testnet:
    needs: test-and-audit
    runs-on: ubuntu-latest
    env:
      SEPOLIA_RPC: ${{ secrets.SEPOLIA_RPC }}
      ETHERSCAN_API_KEY: ${{ secrets.ETHERSCAN_API_KEY }}
    steps:
      - run: npx hardhat run scripts/deploy.js --network sepolia
      - run: npx hardhat verify --network sepolia $DEPLOYED_CONTRACT
```

## Q99: How do you implement a CI/CD pipeline for a platform engineering team's internal developer platform (IDP)?
**A:** IDP CI/CD: (1) Backstage/TechDocs template validation, (2) Scaffolder action tests, (3) Plugin compatibility matrix, (4) Self-service portal tests, (5) Golden path template CI (ensure templates produce working projects), (6) Performance: catalog indexing, search, (7) Deploy: rolling update of portal, (8) Backward compatibility of API.

**Code:**
```yaml
jobs:
  validate-templates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx @backstage/cli repo build
      - run: node scripts/validate-templates.js --glob templates/**/*.yaml
      - run: npx backstage-cli scaffolder test --coverage 80
  golden-path:
    needs: validate-templates
    runs-on: ubuntu-latest
    steps:
      - run: node scripts/smoke-golden-path.js template-node-service
      - run: cd out/golden && npm ci && npm test && npm run build
  portal:
    needs: golden-path
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy-portal.sh --rolling --grace 30
```

## Q100: How do you measure and improve CI/CD pipeline performance (reduce build time)?
**A:** Pipeline performance optimization: (1) Measure: total time, stage-level breakdown, queue time, (2) Parallelize independent stages, (3) Cache dependencies and build artifacts, (4) Use incremental builds (Nx, Turborepo), (5) Optimize Docker layer caching, (6) Use faster CI runners (more CPU, SSD), (7) Fail fast: run quick checks first, (8) Dependency pre-warming, (9) Remove redundant test runs, (10) Distribute tests across multiple runners.

**Code:**
```yaml
name: Optimized CI
on: push
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: git diff --name-only HEAD~1 | grep -E '\.(ts|tsx)$' || exit 0
      - run: npx eslint --cache --cache-location .eslintcache .
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: ~/.npm
          key: npm-${{ hashFiles('package-lock.json') }}
      - run: npm ci
      - run: npm run test:unit -- --shard=${{ matrix.shard }}/4
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - uses: actions/cache@v4
        with:
          path: .next/cache
          key: next-${{ github.sha }}-${{ runner.os }}
      - run: npm run build
```