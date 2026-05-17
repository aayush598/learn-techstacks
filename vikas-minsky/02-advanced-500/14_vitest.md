## 33. Vitest Advanced (891–905)

891. Explain parallel test execution.

   **Answer:** Vitest runs tests in parallel using worker threads (default) or child processes. Each file gets its own worker, providing isolation and faster execution at the cost of CPU and memory.

892. How do module mocks work?

   **Answer:** `vi.mock()` intercepts module imports globally before tests run, replacing exports with mock implementations. Vitest hoists mocks to the top of the file via a transformer.

893. Explain browser mode in Vitest.

   **Answer:** Browser mode runs tests in a real browser (Chrome, Firefox) using Playwright or WebdriverIO. It enables testing DOM APIs, CSS, and browser-specific behavior in a realistic environment.

894. What are test doubles?

   **Answer:** Test doubles replace real dependencies: dummies (placeholder), fakes (working simplified impl), stubs (controlled responses), spies (call tracking), and mocks (expectations-based).

895. Explain deterministic testing.

   **Answer:** Deterministic tests produce the same result every run regardless of order or environment. Achieve by seeding random values, freezing time (`vi.useFakeTimers`), isolating I/O, and avoiding shared mutable state.

896. How do flaky async tests happen?

   **Answer:** Flaky async tests fail intermittently due to timing assumptions (`setTimeout`), unresolved race conditions, uncaught promise rejections, or shared state between tests. Use fake timers and proper `await` to fix.

897. Explain contract testing principles.

   **Answer:** Contract testing (via Pact) verifies that an API consumer's expectations match the provider's actual responses. Tests run against mock providers/consumers, ensuring compatibility without full end-to-end setup.

898. What are end-to-end test tradeoffs?

   **Answer:** E2E tests provide high confidence but are slow, flaky, expensive to maintain, and hard to debug. Balance with more unit/integration tests (testing pyramid) and use E2E sparingly for critical paths.

899. Explain fixture management.

   **Answer:** Fixtures set up test data before tests and clean up afterward. Vitest's `beforeEach`/`afterEach` hooks with factory functions (e.g., `buildUser()`) create isolated, repeatable test data.

900. How do isolated modules improve testing?

   **Answer:** Module isolation prevents test order dependencies and state leakage. Resetting modules between tests with `vi.resetModules()` ensures each test starts fresh with clean imports.

901. Explain mutation testing.

   **Answer:** Mutation testing introduces small code changes (mutations) and runs tests to see if they fail. Surviving mutations indicate untested paths. Tools like Stryker identify weak spots in test coverage.

902. What are testing anti-patterns?

   **Answer:** Anti-patterns include testing implementation details, brittle assertions, over-mocking, shared mutable fixtures, conditional logic in tests, and ignoring async edge cases.

903. Explain code coverage limitations.

   **Answer:** Coverage measures which lines are executed, not whether behavior is correct. High coverage can miss edge cases, integration failures, or incorrect logic. Combine coverage with mutation testing and code review.

904. How do you test distributed systems?

   **Answer:** Test distributed systems with in-memory simulators (e.g., in-memory message broker), containerized integration tests (Testcontainers), chaos experiments (network latency, crashes), and deterministic replays.

905. Explain scalable testing architecture.

   **Answer:** A scalable architecture groups tests by isolation needs: unit (fast, parallel), integration (database/resource per worker), and E2E (dedicated environment). Use test splitting, remote caching, and failure-only retries.
