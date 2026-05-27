# Chapter 08: Testing Infrastructure Setup

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Vitest Configuration](sec-01-vitest-configuration.md) | Workspace config, test environment (jsdom/node), globals, coverage configuration |
| 02 | [Test Utilities & Helpers](sec-02-test-utilities-helpers.md) | Test factories, fixtures, mocking utilities, custom matchers, test data builders |
| 03 | [MSW (Mock Service Worker)](sec-03-msw-mock-service-worker.md) | API mocking, handler definition, browser + server integration, scenario mocking |
| 04 | [Playwright Configuration](sec-04-playwright-configuration.md) | Browser setup, project configuration, test isolation, visual testing, CI integration |
| 05 | [Test Database Setup](sec-05-test-database-setup.md) | Testcontainers for integration tests, database seeding per test, transaction rollback |
| 06 | [Coverage & Reporting](sec-06-coverage-reporting.md) | Istanbul coverage, threshold enforcement, HTML reports, CI annotations, uncovered code detection |

---

## Key Takeaways

- Vitest for unit/integration with workspace support for monorepo
- MSW for API mocking — no network calls in tests
- Playwright for E2E with Chromium, Firefox, WebKit
- Testcontainers for realistic integration tests with real databases
- Coverage threshold: 80%+ for packages, 60%+ for apps
- Test factories with faker.js for realistic data generation
