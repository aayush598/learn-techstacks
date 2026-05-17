## 14. Vitest (391–405)

391. What is Vitest?
     V**Answer:** Vitest is a blazing-fast unit test framework for Vite projects. It's compatible with Jest's API and assertions but runs natively on Vite, enabling instant hot-reload testing, native TypeScript/ESM support, and reuse of Vite config.

392. Difference between Jest and Vitest?
     V**Answer:** Vitest is faster due to Vite's HMR and native ESM, requires less configuration, and natively supports TypeScript, JSX, and ESM without additional setup. Jest is more mature with a larger ecosystem but slower and requires more configuration for TypeScript.

393. Explain unit testing.
     U**Answer:** Unit testing validates the smallest testable parts of code (functions, classes, components) in isolation. Tests mock dependencies and focus on single behavior, ensuring each unit works correctly before integration.

394. What are mocks and spies?
     M**Answer:** Mocks replace real implementations with fake ones for testing in isolation. Spies track function calls, arguments, and return values. Vitest provides `vi.mock()` for module mocking, `vi.fn()` for function mocks, and `vi.spyOn()` for spying on existing methods.

395. Explain test isolation.
     T**Answer:** Test isolation ensures each test runs independently without sharing state. Vitest automatically resets mocks and modules between tests via `vi.clearAllMocks()` or `vi.resetModules()`. Isolation prevents test ordering dependencies.

396. What is snapshot testing?
     S**Answer:** Snapshot testing captures the rendered output of a component and compares it against a stored snapshot on subsequent runs. It detects unexpected UI changes — developers review and update snapshots when changes are intentional.

397. Explain integration testing.
     I**Answer:** Integration testing verifies that multiple units work together correctly. It tests component interactions, API integrations, database queries, and service compositions without mocking all dependencies.

398. How do async tests work?
     A**Answer:** Async tests use `async/await` with `expect().resolves`/`expect().rejects` for promises. Vitest supports async callback completion, timeout configuration, and fake timers for testing time-dependent async code.

399. Explain coverage reports.
     C**Answer:** Coverage reports show what percentage of code is executed during tests, broken down by statements, branches, functions, and lines. Vitest uses `c8` or `istanbul` for coverage, configured via `coverage` option, and generates HTML/LCOL reports.

400. What are setup files?
     S**Answer:** Setup files run before all tests, configuring global mocks, environment variables, and test utilities. Defined via `setupFiles` in vitest config, they run once per test file or globally for all suites.

401. Explain mocking APIs.
     A**Answer:** API mocking intercepts HTTP requests during tests, returning controlled responses without hitting real servers. Vitest works with `MSW` (Mock Service Worker) for request interception, `vi.fn()` mocking fetch/axios, or `nock` for HTTP-level mocking.

402. How do you test React hooks?
     R**Answer:** React hooks are tested using `renderHook` from `@testing-library/react`, which renders a hook in a test component. The result provides `current` (hook return value) and `rerender` to test state changes and side effects.

403. Explain fake timers.
     F**Answer:** Fake timers (`vi.useFakeTimers()`) replace `setTimeout`, `setInterval`, `Date.now`, and `requestAnimationFrame` with controllable implementations. Tests advance time manually with `vi.advanceTimersByTime()` to test time-dependent code deterministically.

404. What are flaky tests?
     F**Answer:** Flaky tests pass or fail inconsistently without code changes, caused by timing issues, async race conditions, test ordering dependencies, external API flakiness, or non-deterministic data. Fix by improving test isolation and deterministic behavior.

405. How do you structure test suites?
     S**Answer:** Structure suites with `describe` for grouping related tests, `it`/`test` for individual cases, and `beforeEach`/`afterEach` for setup/teardown. Follow the AAA pattern (Arrange, Act, Assert), keep tests focused on one behavior, and use descriptive names.
