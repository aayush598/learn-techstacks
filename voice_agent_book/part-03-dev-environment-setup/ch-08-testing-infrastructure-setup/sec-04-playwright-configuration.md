# Section 04: Playwright Configuration

## Overview

Playwright provides end-to-end testing across Chromium, Firefox, and WebKit browsers. For the voice agent platform, Playwright tests the complete user journey — from login through agent configuration to call simulation — ensuring that all components work together correctly.

## Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  // Test configuration
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [
    ["html"],
    ["list"],
    ["json", { outputFile: "test-results/playwright-report.json" }],
    ["junit", { outputFile: "test-results/playwright-junit.xml" }],
  ],

  // Timeouts
  timeout: 30000,
  expect: {
    timeout: 10000,
    toHaveScreenshot: {
      maxDiffPixels: 100,
    },
  },

  // Web server (start before tests)
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
    env: {
      NODE_ENV: "test",
    },
  },

  // Browser projects
  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1280, height: 720 },
      },
    },
    {
      name: "firefox",
      use: {
        ...devices["Desktop Firefox"],
        viewport: { width: 1280, height: 720 },
      },
    },
    {
      name: "webkit",
      use: {
        ...devices["Desktop Safari"],
        viewport: { width: 1280, height: 720 },
      },
    },
    {
      name: "mobile-chrome",
      use: {
        ...devices["Pixel 5"],
      },
    },
    {
      name: "mobile-safari",
      use: {
        ...devices["iPhone 13"],
      },
    },
  ],
});
```

## Environment Configuration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on:
  schedule:
    - cron: '0 6 * * 1-5'  # Weekdays
  workflow_dispatch:

jobs:
  e2e:
    timeout-minutes: 30
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
      fail-fast: false

    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: voice_agent_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Install Playwright browsers
        run: pnpm exec playwright install --with-deps ${{ matrix.browser }}

      - name: Run E2E tests
        run: pnpm test:e2e -- --project=${{ matrix.browser }}
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/voice_agent_test
          NODE_ENV: test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-${{ matrix.browser }}
          path: playwright-report/
          retention-days: 30
```

## Test File Structure

```text
apps/web/e2e/
├── auth.setup.ts              # Authentication setup
├── fixtures.ts                # Custom fixtures
├── pages/                     # Page Object Model
│   ├── login.page.ts
│   ├── dashboard.page.ts
│   ├── agents.page.ts
│   ├── calls.page.ts
│   └── settings.page.ts
├── specs/
│   ├── auth.spec.ts           # Login/logout flows
│   ├── agents.spec.ts         # CRUD agent flows
│   ├── calls.spec.ts          # Call history/list
│   ├── dashboard.spec.ts      # Dashboard widgets
│   ├── campaigns.spec.ts      # Campaign management
│   └── settings.spec.ts       # Organization settings
└── utils/
    ├── test-data.ts           # Test data generation
    └── helpers.ts             # Shared utilities
```

## Page Object Model

```typescript
// apps/web/e2e/pages/login.page.ts
import type { Page, Locator } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel("Email");
    this.passwordInput = page.getByLabel("Password");
    this.submitButton = page.getByRole("button", { name: "Sign in" });
    this.errorMessage = page.getByTestId("login-error");
  }

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toHaveText(message);
  }

  async expectLoggedIn() {
    await expect(this.page).toHaveURL(/dashboard/);
  }
}
```

## Authentication Setup

```typescript
// apps/web/e2e/auth.setup.ts
import { test as setup } from "@playwright/test";
import { LoginPage } from "./pages/login.page";

const authFile = "playwright/.auth/user.json";

setup("authenticate", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login("admin@demo.voiceagent.dev", "test-password");
  await loginPage.expectLoggedIn();

  // Save authentication state
  await page.context().storageState({ path: authFile });
});
```

## Test Fixtures

```typescript
// apps/web/e2e/fixtures.ts
import { test as base, type Page } from "@playwright/test";
import { LoginPage } from "./pages/login.page";
import { DashboardPage } from "./pages/dashboard.page";
import { AgentsPage } from "./pages/agents.page";

// Extend base test with page objects
export const test = base.extend<{
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  agentsPage: AgentsPage;
}>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
  agentsPage: async ({ page }, use) => {
    await use(new AgentsPage(page));
  },
});

export { expect } from "@playwright/test";
```

## Test Implementation

```typescript
// apps/web/e2e/specs/agents.spec.ts
import { test, expect } from "../fixtures";
import { faker } from "@faker-js/faker";

test.describe("Agent Management", () => {
  test.beforeEach(async ({ dashboardPage }) => {
    await dashboardPage.goto();
    await dashboardPage.navigateToAgents();
  });

  test("should create a new agent", async ({ agentsPage }) => {
    const agentName = faker.company.catchPhrase();

    await agentsPage.clickCreateAgent();
    await agentsPage.fillAgentName(agentName);
    await agentsPage.selectVoiceProvider("elevenlabs");
    await agentsPage.selectVoice("Rachel");
    await agentsPage.fillGreeting("Hello! How can I help you?");
    await agentsPage.selectLLMProvider("openai");
    await agentsPage.clickSave();

    // Verify agent appears in the list
    await expect(agentsPage.agentListItem(agentName)).toBeVisible();
    await expect(agentsPage.agentStatus(agentName)).toHaveText("Draft");
  });

  test("should display validation errors", async ({ agentsPage }) => {
    await agentsPage.clickCreateAgent();
    await agentsPage.clickSave();

    await expect(agentsPage.nameError).toBeVisible();
    await expect(agentsPage.nameError).toHaveText("Name is required");
  });

  test("should delete an agent", async ({ agentsPage }) => {
    // Assuming there's at least one agent
    const firstAgent = await agentsPage.getFirstAgentName();
    await agentsPage.deleteAgent(firstAgent);

    await expect(agentsPage.agentListItem(firstAgent)).not.toBeVisible();
  });

  test("should toggle agent status", async ({ agentsPage }) => {
    const firstAgent = await agentsPage.getFirstAgentName();
    await agentsPage.toggleStatus(firstAgent);

    await expect(agentsPage.agentStatus(firstAgent)).toHaveText(/active|paused/);
  });
});
```

## Visual Testing

```typescript
// apps/web/e2e/specs/visual.spec.ts
import { test, expect } from "../fixtures";

test.describe("Visual Regression", () => {
  test("dashboard should match snapshot", async ({ page }) => {
    await page.goto("/dashboard");
    await page.waitForLoadState("networkidle");
    await expect(page).toHaveScreenshot("dashboard.png", {
      maxDiffPixels: 500,
      fullPage: true,
    });
  });

  test("agent list should match snapshot", async ({ page }) => {
    await page.goto("/agents");
    await page.waitForLoadState("networkidle");
    await expect(page).toHaveScreenshot("agents-list.png", {
      maxDiffPixels: 500,
    });
  });
});
```

## Test Data Generation for E2E

```typescript
// apps/web/e2e/utils/test-data.ts
import { faker } from "@faker-js/faker";

export function createTestAgent() {
  return {
    name: faker.company.catchPhrase(),
    description: faker.lorem.sentence(),
    voiceProvider: "elevenlabs" as const,
    voiceId: faker.string.alphanumeric(20),
    greetingMessage: faker.helpers.arrayElement([
      "Hello! How can I help you today?",
      "Welcome! I'm your virtual assistant.",
    ]),
    llmProvider: "openai" as const,
    llmModel: "gpt-4",
    temperature: 0.7,
  };
}

export function createTestContact() {
  return {
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    email: faker.internet.email(),
    phone: faker.phone.number({ style: "international" }),
  };
}
```

## Design Decisions

### Page Object Model vs. direct interactions

**Decision**: Use the Page Object Model pattern.

**Rationale**: Page objects encapsulate page structure and interactions, making tests more readable and maintainable. When the UI changes, only the page object needs updating — tests remain unchanged.

### Test isolation

Each test gets a fresh browser context. For tests that require logged-in state, use `storageState` to load pre-authenticated state rather than logging in before each test.

## Integration Points

- **Vitest**: Unit tests run alongside Playwright E2E tests
- **MSW**: API mocking can be integrated with Playwright for deterministic E2E tests
- **Storybook**: Visual regression tests can use Storybook's screenshots as baselines
- **CI**: Playwright runs on every PR with results uploaded as artifacts

## Production Considerations

1. **Flaky test management**: Use `retries: 2` in CI to handle transient failures. Track flaky tests and prioritize fixing them
2. **Test data**: E2E tests should create their own data and clean up afterward. Shared test state leads to flaky, order-dependent tests
3. **Browser coverage**: Run Chromium on every PR. Run Firefox and WebKit on main branch and nightly. Mobile browsers can be weekly
4. **Performance**: Keep E2E test suites under 15 minutes. Split into parallel jobs by spec file or feature area
5. **CI integration**: Upload Playwright report and test recordings as CI artifacts. Use Playwright's trace viewer for debugging failures
