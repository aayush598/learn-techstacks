# E2E Testing Essentials for Solo Founders

## What E2E Testing Gets You

End-to-end (E2E) tests simulate real user behavior: clicking buttons, filling forms, navigating pages. They catch issues that unit and integration tests miss — the kind where individual components work perfectly but the system as a whole doesn't.

For solo founders, E2E testing is especially valuable because:
- **You don't have QA** — E2E tests catch what manual testing misses
- **You ship fast** — E2E tests prevent regressions
- **You sleep better** — E2E tests verify critical paths work

---

## 1. The E2E Testing Philosophy for Solo

### What to Test with E2E

Only test the most critical user paths. These are the flows that, if broken, would:
- Prevent users from using your product
- Lose you money
- Cause data loss
- Make users angry

### The Critical Paths for a SaaS

1. **Signup → Onboarding → First Core Action** (activation)
2. **Login → Dashboard** (retention)
3. **Upgrade to paid plan** (revenue)
4. **Create → Edit → Delete** (data integrity)
5. **Settings → Update profile** (account management)
6. **Password reset** (recovery)

### The 10 E2E Test Rule

For most solo SaaS products, 10 well-designed E2E tests are enough:
- 5 tests for the core activation flow
- 3 tests for payment/billing
- 2 tests for critical data operations

More than 20 E2E tests for a solo product is almost certainly overkill.

---

## 2. Playwright Setup

### Why Playwright

Playwright is the best E2E testing tool for solo founders:
- Fast (runs tests in parallel)
- Reliable (auto-waits, resilient selectors)
- Multi-browser (Chrome, Firefox, Safari)
- Cross-platform (Mac, Windows, Linux)
- Excellent debugging (trace viewer, video recording)
- Free and open source

### Installation

```bash
npm init playwright@latest
```

This creates:
- `playwright.config.ts` — Configuration
- `tests/` — Test directory
- `playwright-report/` — Test reports

### Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
  retries: 2,             // Retry flaky tests
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',  // Trace on failure
    video: 'on-first-retry',  // Video on failure
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
    // Optionally add Firefox and Safari
  ],
})
```

---

## 3. Writing Your First E2E Tests

### Test Structure

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test('user can sign up and complete onboarding', async ({ page }) => {
  // 1. Visit landing page
  await page.goto('/')
  
  // 2. Click sign up
  await page.click('text=Get Started')
  
  // 3. Fill signup form
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'Password123!')
  await page.click('button:has-text("Create Account")')
  
  // 4. Verify redirect to onboarding
  await expect(page).toHaveURL(/.*onboarding/)
  
  // 5. Complete onboarding
  await page.fill('[name="name"]', 'Test User')
  await page.click('button:has-text("Continue")')
  
  // 6. Verify redirect to dashboard
  await expect(page).toHaveURL(/.*dashboard/)
  await expect(page.locator('text=Welcome, Test User')).toBeVisible()
})
```

### The Page Object Pattern

For maintainable tests, extract page interactions:

```typescript
// e2e/pages/signup.page.ts
export class SignupPage {
  constructor(private page: Page) {}
  
  async goto() {
    await this.page.goto('/signup')
  }
  
  async signup(email: string, password: string) {
    await this.page.fill('[name="email"]', email)
    await this.page.fill('[name="password"]', password)
    await this.page.click('button:has-text("Create Account")')
  }
  
  async expectError(message: string) {
    await expect(this.page.locator(`text=${message}`)).toBeVisible()
  }
}

// e2e/auth.spec.ts
test('user can sign up', async ({ page }) => {
  const signupPage = new SignupPage(page)
  await signupPage.goto()
  await signupPage.signup('test@example.com', 'Password123!')
  await expect(page).toHaveURL(/.*onboarding/)
})
```

---

## 4. Testing Authentication

### Login Tests

```typescript
test('user can log in', async ({ page }) => {
  await page.goto('/sign-in')
  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'CorrectPassword123!')
  await page.click('button:has-text("Sign In")')
  
  await expect(page).toHaveURL('/dashboard')
})

test('shows error for wrong password', async ({ page }) => {
  await page.goto('/sign-in')
  await page.fill('[name="email"]', 'user@example.com')
  await page.fill('[name="password"]', 'WrongPassword')
  await page.click('button:has-text("Sign In")')
  
  await expect(page.locator('text=Invalid credentials')).toBeVisible()
})
```

### Session Testing

```typescript
test('redirects to login when not authenticated', async ({ page }) => {
  await page.goto('/dashboard')
  await expect(page).toHaveURL(/.*sign-in/)
})

test('user stays logged in after page reload', async ({ page }) => {
  // Login first
  await login(page, 'user@example.com', 'Password123!')
  
  // Reload
  await page.reload()
  
  // Should still be on dashboard
  await expect(page).toHaveURL('/dashboard')
})
```

---

## 5. Testing Core User Flows

### Testing the Core Loop

Every SaaS has a core loop. For a project management tool:

```typescript
test('user creates and completes a task', async ({ page }) => {
  // Login
  await loginAsTestUser(page)
  
  // Create project
  await page.click('text=New Project')
  await page.fill('[name="projectName"]', 'My Project')
  await page.click('button:has-text("Create")')
  
  // Create task
  await page.click('text=Add Task')
  await page.fill('[name="taskTitle"]', 'Design homepage')
  await page.click('button:has-text("Save")')
  
  // Verify task appears
  await expect(page.locator('text=Design homepage')).toBeVisible()
  
  // Complete task
  await page.click('[aria-label="Complete task"]')
  await expect(page.locator('[aria-label="Complete task"]')).toBeChecked()
})
```

### Testing the Empty State

```typescript
test('shows empty state for new user', async ({ page }) => {
  await loginAsNewUser(page)
  await page.goto('/projects')
  
  await expect(page.locator('text=No projects yet')).toBeVisible()
  await expect(page.locator('text=Create your first project')).toBeVisible()
})
```

---

## 6. Testing Payment Flows

### Stripe Checkout Testing

```typescript
test('user can upgrade to pro plan', async ({ page }) => {
  await loginAsTestUser(page)
  
  // Go to pricing page
  await page.goto('/pricing')
  
  // Click upgrade on Pro plan
  await page.click('button:has-text("Upgrade to Pro")')
  
  // Fill in Stripe test card
  const frame = page.frameLocator('iframe[name^="stripe-"]')
  await frame.fill('[name="cardNumber"]', '4242424242424242')
  await frame.fill('[name="cardExpiry"]', '12/28')
  await frame.fill('[name="cardCvc"]', '123')
  await page.click('button:has-text("Pay")')
  
  // Verify success
  await expect(page.locator('text=Welcome to Pro!')).toBeVisible()
})
```

### Testing Subscription Management

```typescript
test('user can cancel subscription', async ({ page }) => {
  await loginAsProUser(page)
  
  await page.goto('/settings/billing')
  await page.click('text=Cancel Subscription')
  await page.click('button:has-text("Confirm Cancellation")')
  
  await expect(page.locator('text=Subscription cancelled')).toBeVisible()
  await expect(page.locator('text=Plan: Free')).toBeVisible()
})
```

---

## 7. Testing Data Operations

### CRUD Testing

```typescript
test('user can create, edit, and delete an item', async ({ page }) => {
  await loginAsTestUser(page)
  await page.goto('/items')
  
  // Create
  await page.click('text=Add Item')
  await page.fill('[name="title"]', 'Test Item')
  await page.click('button:has-text("Save")')
  await expect(page.locator('text=Test Item')).toBeVisible()
  
  // Edit
  await page.click('text=Test Item')
  await page.fill('[name="title"]', 'Updated Item')
  await page.click('button:has-text("Save")')
  await expect(page.locator('text=Updated Item')).toBeVisible()
  
  // Delete
  await page.click('[aria-label="Delete"]')
  await page.click('button:has-text("Confirm")')
  await expect(page.locator('text=Updated Item')).not.toBeVisible()
})
```

---

## 8. Running Tests in CI

### GitHub Actions Setup

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on:
  push:
    branches: [main]

jobs:
  test:
    timeout-minutes: 10
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium
      
      - name: Run database migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
      
      - name: Run E2E tests
        run: npx playwright test
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
```

---

## 9. Debugging E2E Tests

### Using Playwright Trace Viewer

Playwright traces capture everything that happened during a test:

```typescript
// In playwright.config.ts
use: {
  trace: 'on-first-retry', // Capture trace on failure
}
```

View traces:
```bash
npx playwright show-trace trace.zip
```

### Debugging Locally

```bash
# Run tests in UI mode (visual debugger)
npx playwright test --ui

# Run a single test
npx playwright test auth.spec.ts

# Run with visible browser
npx playwright test --headed

# Debug mode (step through)
npx playwright test --debug
```

### Common Debugging Steps

When an E2E test fails:
1. Check the screenshot (automatically captured on failure)
2. Check the trace (shows every action and network request)
3. Check the video (records the browser)
4. Run in headed mode to see what's happening
5. Add `page.pause()` to inspect mid-test

---

## 10. The E2E Testing Checklist

### Test Design
- [ ] Tests only critical user paths
- [ ] No more than 10-20 tests total
- [ ] Each test covers one complete flow
- [ ] Tests are independent (can run in any order)
- [ ] Tests clean up after themselves

### Test Quality
- [ ] No hardcoded waits (use auto-waiting)
- [ ] No flaky tests (each test passes 95%+ of the time)
- [ ] Tests are readable (descriptive test names, page objects)
- [ ] Tests are fast (under 30 seconds each)

### CI Integration
- [ ] E2E tests run on every push to main
- [ ] Test results are visible in CI
- [ ] Screenshots/videos saved on failure
- [ ] Tests don't block CI (can run in parallel with deploy)

### Maintenance
- [ ] Tests are reviewed monthly (are they still relevant?)
- [ ] Flaky tests are fixed immediately
- [ ] New critical paths get E2E tests
- [ ] Removed features get their tests removed

---

## 11. Common E2E Testing Mistakes

### Mistake 1: Testing Too Much

50 E2E tests for a simple SaaS. Tests take 30 minutes to run. They're constantly flaky.

**Fix**: 10 tests max. Only test critical paths. Remove tests that have never found a bug.

### Mistake 2: Flaky Tests

Tests that pass locally but fail in CI. Tests that fail randomly.

**Fix**: Add retries (2 max). Fix the root cause of flakiness. If a test is consistently flaky, remove it.

### Mistake 3: Hardcoded Waits

```typescript
// Bad: fragile, slow
await page.waitForTimeout(3000)

// Good: resilient, fast
await page.waitForSelector('text=Welcome')
```

### Mistake 4: Test Pollution

Tests that depend on each other (creating data that another test relies on).

**Fix**: Each test should set up and clean up its own data. Tests should run in any order.

### Mistake 5: Not Using Page Objects

Repeating the same selectors across multiple tests. When the UI changes, you update 10 files.

**Fix**: Use page objects to encapsulate selectors and actions.

### Mistake 6: Testing in Production

Running E2E tests against production data. Creates test accounts, test data, test payments.

**Fix**: Run against a test database or use test API keys. Clean up test data after each run.

---

## 12. The E2E Testing Workflow

### Adding E2E Tests for a New Feature

1. **Build the feature**
2. **Identify the critical path** (what must work?)
3. **Write 1-2 E2E tests** for that path
4. **Run locally** until passing
5. **Add to CI**
6. **Monitor for flakiness**

### Weekly E2E Routine

1. **Run the full E2E suite** (should take < 5 minutes)
2. **Review failures** (if any)
3. **Fix flaky tests** (delete if unfixable)
4. **Add tests for any bugs found** (regression prevention)

### Monthly E2E Review

1. **Review test coverage** (are we testing the right things?)
2. **Remove outdated tests** (for removed/redesigned features)
3. **Consolidate similar tests** (keep test count manageable)
4. **Optimize slow tests** (keep suite under 5 minutes)

---

## 13. The E2E Testing Manifesto

1. **10 tests max** — More is worse, not better
2. **Test critical paths only** — Signup, payment, core loop
3. **Use Playwright** — It's the best tool for the job
4. **Page objects** — Keep tests maintainable
5. **No flaky tests** — Fix or delete immediately
6. **CI integration** — Every push runs E2E against critical paths
7. **Trace on failure** — Debugging without traces is painful
8. **Fast tests** — Suite under 5 minutes
9. **Independent tests** — Clean up after yourself
10. **E2E is your safety net** — Not your primary testing strategy

E2E tests are not a replacement for unit and integration tests. They're the final safety net that catches the bugs that fall through everything else. Used sparingly and strategically, they give you confidence to ship fast without breaking your users' most important flows.
