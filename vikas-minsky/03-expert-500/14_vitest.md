## 52. Vitest Expert Topics (1391–1405)

1391. How do parallel workers isolate tests?

   **Answer:** Vitest spawns worker threads (via Tinypool) that each run test files in isolation. Workers have separate module caches and environments, preventing test pollution. The number of workers is configurable via `--threads` or `poolOptions.threads`.

1392. Explain browser simulation environments.

   **Answer:** Vitest supports `@vitest/browser` for running tests in real browsers (Chrome, Firefox, Safari) using Playwright or WebdriverIO. This enables testing real DOM behavior, layout, and browser-specific features that jsdom can't simulate.

1393. What are deterministic fixture patterns?

   **Answer:** Deterministic fixtures use factory functions with seeded random values (faker with fixed seed), snapshot-serialized JSON files, or builder patterns. This ensures tests produce consistent results across runs and environments.

1394. Explain dependency mocking boundaries.

   **Answer:** Mocking boundaries define what's mocked (external HTTP, database, filesystem) versus what's tested as integration (internal modules). Vitest's `vi.mock` auto-mocks modules at the module system level, with `vi.importActual` for selective unmocking.

1395. How do snapshot serializers work?

   **Answer:** Snapshot serializers transform complex objects into a deterministic string representation before comparison. Custom serializers handle specific types (React elements, Dates, Buffers) to produce readable, stable snapshots.

1396. Explain flaky network test mitigation.

   **Answer:** Flaky network test mitigation uses mock service workers (MSW), deterministic request/response fixtures, and controlled timeouts. Vitest's `vi.useFakeTimers` combined with mocked fetch ensures network-dependent tests run reliably.

1397. What are mutation coverage metrics?

   **Answer:** Mutation testing (with tools like Stryker) modifies source code (changing `>` to `<`, removing conditionals) and checks whether tests fail. High mutation coverage indicates tests actually validate behavior, not just line coverage.

1398. Explain test orchestration pipelines.

   **Answer:** Test orchestration pipelines order test execution by type: unit → integration → e2e, with early failure for fast feedback. CI parallelizes across multiple runners, shards test files by duration, and retries flaky tests.

1399. How do distributed tests coordinate state?

   **Answer:** Distributed tests coordinate state through shared databases, seeded test data, and idempotent setup/teardown. Each test worker gets an isolated data subset, and clean-up ensures no state leaks between parallel runs.

1400. Explain frontend integration test architecture.

   **Answer:** Frontend integration tests render components with real dependencies (MSW for API, test database for data), testing user flows through actual interactions. Vitest's component testing with `@testing-library/react` provides realistic DOM behavior.

1401. What are CI testing bottlenecks?

   **Answer:** CI bottlenecks include long-running e2e suites, flaky tests requiring retries, slow test database setup, and dependency installation. Mitigations include test splitting, parallel execution, caching node_modules, and optimizing fixture generation.

1402. Explain runtime mocking tradeoffs.

   **Answer:** Runtime mocking (vi.mock, jest.mock) is easier to set up but may produce false positives by oversimplifying module behavior. Integration mocks (MSW at the network layer) provide more realistic tests without hitting production services.

1403. How do contract tests prevent regressions?

   **Answer:** Contract tests validate that API interactions conform to a shared schema (Pact, OpenAPI). When either provider or consumer changes the contract, tests fail, catching breaking changes before deployment.

1404. Explain resilient test suite design.

   **Answer:** Resilient test suites avoid shared mutable state, use deterministic fixtures, set explicit timeouts, run in random order, and isolate tests per module. They include both happy-path and edge-case coverage with minimal flakiness.

1405. How do engineering teams scale automated testing?

   **Answer:** Teams scale testing by establishing a test pyramid (many unit, fewer integration, few e2e), enforcing code coverage thresholds in CI, running tests in parallel across shards, and investing in test infrastructure (fast runners, cached dependencies).
