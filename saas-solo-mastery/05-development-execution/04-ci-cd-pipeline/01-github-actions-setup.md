# GitHub Actions CI/CD Setup for Solo

## Why CI/CD Matters for Solo Founders

Continuous Integration and Continuous Deployment (CI/CD) automates the boring parts of shipping software. For solo founders, CI/CD is not optional — it's essential:

- **No manual steps**: Push code → Everything happens automatically
- **Catch issues early**: Tests run on every push, not when you remember to run them
- **Ship faster**: No more "run tests, build, deploy" rituals
- **Reduce errors**: Automated processes don't forget steps
- **Sleep better**: CI/CD creates a safety net that lets you ship with confidence

---

## 1. The Solo CI/CD Philosophy

### Keep It Simple

As a solo founder, your CI/CD pipeline should have exactly ONE goal: get your code from your machine to production with minimal friction and maximum safety.

**Simple pipeline**:
```
Code → Lint → Type-check → Test → Build → Deploy
(10 seconds) (30 seconds) (1 min) (2 min) (2 min)
Total: ~5 minutes from push to production
```

### What NOT to Do

- **Don't build a complex multi-stage pipeline** — You don't need dev, staging, QA, and production
- **Don't run 50 different checks** — Your time is better spent building than waiting for CI
- **Don't gate on code coverage** — Coverage is a vanity metric
- **Don't run E2E tests in CI** — Run them locally before pushing (or skip them for solo)

### The Solo Pipeline Priority

1. **TypeScript check** (30s) — Catches most errors
2. **Lint** (10s) — Enforces code quality
3. **Unit + Integration tests** (1 min) — Verifies business logic
4. **Build** (1-2 min) — Ensures production build succeeds
5. **Deploy** (1-2 min) — Ships to production

---

## 2. Repository Setup

### Repository Structure

```
my-saas/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Main CI pipeline
│       ├── deploy.yml      # Deployment
│       └── security.yml    # Security scanning (optional)
├── src/
├── tests/
├── e2e/
├── package.json
└── playwright.config.ts
```

### Branch Strategy

For solo founders, the simplest strategy:

```
main → Production
  ↑
  (push directly)
```

No feature branches. No PRs. No code review (you're the only developer).

**When to branch**:
- Major feature that takes > 1 day
- Risky refactor
- Experimental work you might discard

### Protection Rules

Even for solo, set up branch protection on main:
- Require CI to pass before merging (but you can override if needed)
- This prevents merging broken code (even by accident)

---

## 3. The CI Pipeline

### Basic CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s

    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: TypeScript check
        run: npx tsc --noEmit
        env:
          CI: true
      
      - name: Lint
        run: npm run lint
      
      - name: Run tests
        run: npm run test:ci
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
      
      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${{ secrets.CLERK_PUBLISHABLE_KEY }}
```

### Step-by-Step Explanation

**Checkout**: Gets your code
**Setup Node**: Installs Node.js with caching (faster subsequent runs)
**Install dependencies**: `npm ci` (clean install, faster than `npm install`)
**TypeScript check**: Catches type errors
**Lint**: Enforces code style
**Test**: Runs unit and integration tests with database
**Build**: Ensures production build succeeds

### Parallel Jobs

If your pipeline has independent parts, run them in parallel:

```yaml
jobs:
  lint-and-type:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx tsc --noEmit
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx prisma migrate deploy
      - run: npm run test:ci
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test

  build:
    needs: [lint-and-type, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
```

---

## 4. The Deployment Pipeline

### Vercel Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${{ secrets.CLERK_PUBLISHABLE_KEY }}
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Alternative: Direct Deploy (Vercel GitHub Integration)

If you use Vercel's GitHub integration, you don't need a deploy workflow:

1. Connect your GitHub repo to Vercel
2. Vercel automatically deploys every push to main
3. No deploy workflow needed

**This is the recommended approach** for solo founders using Vercel.

### Alternative: Docker Deployment

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: ghcr.io/yourname/app:latest

- name: Deploy to server
  uses: appleboy/ssh-action@v1.0.0
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SSH_KEY }}
    script: |
      docker pull ghcr.io/yourname/app:latest
      docker-compose up -d
```

---

## 5. Environment Variables and Secrets

### Managing Secrets

Store secrets in GitHub Secrets (Settings → Secrets and variables → Actions):

```
DATABASE_URL
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
CLERK_SECRET_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
SENTRY_DSN
POSTHOG_API_KEY
VERCEL_TOKEN
```

### Using Secrets in Workflows

```yaml
steps:
  - name: Run tests
    run: npm run test:ci
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      CLERK_SECRET_KEY: ${{ secrets.CLERK_SECRET_KEY }}

  - name: Build
    run: npm run build
    env:
      NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${{ secrets.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY }}
      STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
```

### Environment Files in CI

For builds that need environment variables:

```yaml
- name: Create env file
  run: |
    echo "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=${{ secrets.CLERK_PUBLISHABLE_KEY }}" >> .env.production
    echo "DATABASE_URL=${{ secrets.DATABASE_URL }}" >> .env.production
```

---

## 6. Test Database Setup

### Using Service Containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
      - run: npm run test:ci
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
```

### Using SQLite for Tests

For simpler setup, use SQLite in tests:

```typescript
// vitest.config.ts
export default defineConfig({
  env: {
    DATABASE_URL: 'file:./test.db',
  },
})
```

---

## 7. Caching for Speed

### Node Modules Caching

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'
```

This caches `~/.npm` and speeds up installs from ~2 minutes to ~15 seconds.

### Build Caching

For Next.js:

```yaml
- name: Cache Next.js build
  uses: actions/cache@v4
  with:
    path: |
      .next/cache
    key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}
```

---

## 8. Notifications

### Slack/Discord Notifications

```yaml
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "CI failed on ${{ github.repository }}: ${{ github.workflow }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Email Notifications

GitHub sends email notifications by default for failed actions. For solo, this is usually sufficient.

### Deployment Success Notifications

```yaml
- name: Notify deploy success
  if: success()
  run: |
    curl -X POST ${{ secrets.DISCORD_WEBHOOK }} \
      -H "Content-Type: application/json" \
      -d '{"content": "✅ Deployed to production: ${{ github.sha }}"}'
```

---

## 9. The Complete Pipeline

### What Your Final Pipeline Should Look Like

```yaml
# .github/workflows/ci.yml — Main CI/CD (runs on every push)
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  # 1. Quick checks
  lint-and-type:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npx tsc --noEmit
      - run: npm run lint

  # 2. Tests
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
      - run: npm run test:ci
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test

  # 3. Build and deploy (only on main)
  deploy:
    needs: [lint-and-type, test]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
        env:
          NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${{ secrets.CLERK_PUBLISHABLE_KEY }}
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

---

## 10. Optimizing CI/CD

### Speeding Up Your Pipeline

| Optimization | Time Saved | Complexity |
|-------------|------------|------------|
| Cache npm | ~2 min | Low |
| Cache Next.js build | ~30s | Low |
| Run lint and type in parallel | ~1 min | Low |
| Use SQLite instead of Postgres for tests | ~30s | Medium |
| Skip platform-specific tests | Varies | Low |
| Use larger GitHub runner | ~1 min | Medium |

### The 5-Minute Pipeline Target

Your pipeline should complete in under 5 minutes. If it's longer:
- Check if you're running tests that don't need to run
- Check if your build step is slow
- Consider running some checks in parallel
- Consider removing checks that never fail

---

## 11. Security Scanning

### Dependency Scanning

```yaml
- name: Scan dependencies for vulnerabilities
  run: npm audit --audit-level=high
```

### Secret Scanning

Enable GitHub's built-in secret scanning. It's free and catches accidental secret commits.

### Code Quality

```yaml
- name: Run linter
  run: npm run lint
```

For solo founders, these three checks are sufficient. Skip SAST, DAST, and other enterprise-level tools.

---

## 12. Common CI/CD Mistakes

### Mistake 1: No CI at All

"I test locally, that's enough."

**Reality**: You forget to test edge cases. You forget to run lint. You ship code that doesn't build in production.

**Fix**: Set up a basic CI pipeline. It takes 30 minutes and catches 90% of common issues.

### Mistake 2: Over-Engineering the Pipeline

10 jobs, 30 checks, multi-stage deploys with manual gates.

**Reality**: You're a solo founder. You don't need a production pipeline that rivals Netflix.

**Fix**: 3 checks (type, lint, test) + deploy. That's it.

### Mistake 3: Skipping the Test Database

Running tests in CI without a database. Tests pass locally (with DB) but fail in CI.

**Fix**: Use service containers or SQLite. Your CI should match your local environment.

### Mistake 4: Not Caching

Every CI run installs dependencies from scratch. Takes 3 minutes.

**Fix**: Enable npm caching. Takes 5 seconds to configure, saves 2 minutes per run.

### Mistake 5: Deploying on Every Push Without Safety

Every push to main deploys to production. A broken commit goes live immediately.

**Fix**: Add CI checks before deploy stage. The build must pass before deployment.

---

## 13. CI/CD for Solo: Quick Start

### Day 1 Setup (30 minutes)

1. Create `.github/workflows/ci.yml` with the basic pipeline
2. Add secrets to GitHub
3. Connect to Vercel (or your host)
4. Push a commit to test

### Optional Additions

- **Day 2**: Add security scanning (5 minutes)
- **Day 3**: Add caching (5 minutes)
- **Week 2**: Add CD to Docker/other host if not using Vercel
- **Month 1**: Review and optimize pipeline speed

---

## 14. The CI/CD Manifesto

1. **Automate everything** — Manual steps are bugs waiting to happen
2. **5-minute max** — Your pipeline should complete in under 5 minutes
3. **TypeScript check first** — It catches the most errors for the least time
4. **Test with a real database** — SQLite or Postgres in a container
5. **Cache aggressively** — Every second saved compounds over a hundred deploys
6. **Deploy on green** — If CI passes, deploy automatically
7. **Rollback is one click** — Know how to undo a bad deploy
8. **Notifications on failure** — So you can fix it before users notice
9. **Don't over-engineer** — 3 checks + deploy. That's all you need.
10. **Set it and forget it** — CI/CD should run without your attention

Your CI/CD pipeline is the automatic pilot for your SaaS. Set it up once, and it will catch mistakes, deploy your work, and let you sleep peacefully, every single day.
