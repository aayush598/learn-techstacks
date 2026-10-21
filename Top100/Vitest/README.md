# Vitest Interview Questions and Answers (Top 100)

## Q1: What is Vitest?
**A:** Vitest is a Vite-native test runner that uses the same configuration and transform pipeline as your Vite app, giving instant startup and HMR-like test feedback. It is designed to be Jest-compatible while being faster for Vite projects.

## Q2: Why would you choose Vitest over Jest?
**A:** Vitest reuses Vite's config, plugins, and transform (esbuild/SWC), so there is no separate babel/ts-jest setup and tests start instantly. It also supports ESM, TypeScript, and JSX out of the box with better Vite ecosystem integration.

## Q3: How do you install Vitest?
**A:** Install it as a dev dependency: `npm i -D vitest`. For coverage add `@vitest/coverage-v8`.

## Q4: How do you configure Vitest?
**A:** Add a `test` field to `vite.config.ts`, or create `vitest.config.ts`. Example:
```ts
import { defineConfig } from 'vitest/config'
export default defineConfig({
  test: { globals: true, environment: 'node' }
})
```

## Q5: What is the difference between `vitest` and `vitest run`?
**A:** `vitest` starts watch mode by default and reruns tests on file changes. `vitest run` executes all tests once and exits, which is what you want in CI.

## Q6: How do you run a single test file?
**A:** Use `vitest run path/to/test.spec.ts` or `npx vitest path/to/test.spec.ts` in watch mode. You can also use the `--reporter` flag to change output.

## Q7: What does `vitest --ui` do?
**A:** It launches an interactive web UI (`@vitest/ui`) showing test results, allowing you to filter, inspect, and rerun tests visually. Install `@vitest/ui` to use it.

## Q8: What environments does Vitest support?
**A:** `node` (default), `jsdom`, `happy-dom`, and `edge-runtime`. Set via the `environment` option or per-file with a docblock comment.

## Q9: How do you use jsdom in Vitest?
**A:** Install `jsdom` and set `test: { environment: 'jsdom' }`. Vitest will then provide `window`, `document`, and DOM globals to your tests.

## Q10: What is happy-dom and when would you use it?
**A:** happy-dom is a lightweight, faster alternative to jsdom that implements the DOM API. Use it for component tests where speed matters and full DOM fidelity is not required.

## Q11: How do you set the test environment per file?
**A:** Add a docblock at the top of the test file:
```ts
// @vitest-environment jsdom
```

## Q12: What is the basic test syntax in Vitest?
**A:** Use `describe` to group and `it`/`test` for cases, with `expect` assertions:
```ts
import { describe, it, expect } from 'vitest'
describe('math', () => {
  it('adds', () => { expect(1 + 1).toBe(2) })
})
```

## Q13: What is the difference between `it` and `test`?
**A:** They are aliases; `it` is BDD-style and `test` is more traditional. Both register a test case and behave identically.

## Q14: How do you enable global APIs (describe/it/expect) without imports?
**A:** Set `test: { globals: true }` in config. Then `describe`, `it`, `expect`, and `vi` are available globally, but you lose type inference unless you add `vitest/globals` to tsconfig types.

## Q15: What is `test.each` used for?
**A:** It runs the same test body against multiple inputs, generating a case per row:
```ts
test.each([[1, 2, 3], [2, 3, 5]])('sum %i+%i=%i', (a, b, c) => {
  expect(a + b).toBe(c)
})
```

## Q16: How do you skip or focus tests?
**A:** Use `it.skip(...)`, `it.only(...)`, `describe.skip`, `describe.only`, or `.todo`. `only` restricts the run to marked tests, useful for debugging.

## Q17: What is the difference between `toBe` and `toEqual`?
**A:** `toBe` uses `Object.is` (strict equality, no deep compare) for primitives and reference checks; `toEqual` recursively compares object/array structure and values, ignoring `undefined` properties and key order.

## Q18: When should you use `toStrictEqual`?
**A:** Use `toStrictEqual` when you need stricter checks: it fails on `undefined` properties, `undefined` vs missing keys, and on type mismatches like `{}` vs `[]`.

## Q19: What does `toMatchObject` do?
**A:** It asserts that the received object contains the subset of properties described in the expected object; extra properties are ignored. Useful for partial matches.

## Q20: How do you assert an error is thrown?
**A:** Use `expect(fn).toThrow()` or with a message/regex/error class:
```ts
expect(() => badFn()).toThrow('boom')
expect(() => badFn()).toThrow(TypeError)
```

## Q21: How do you test async functions with `toThrow`?
**A:** Because `toThrow` expects a throwing function, wrap the await in a function:
```ts
await expect(async () => { await badFn() }).rejects.toThrow('boom')
```

## Q22: How do you test promises with `resolves`/`rejects`?
**A:** Use `expect(promise).resolves.toBe(x)` and `expect(promise).rejects.toThrow()`. You must `await` the `expect` call.

## Q23: What are snapshot tests and how do you write one?
**A:** Snapshots serialize a value and compare it to a stored file; use `expect(value).toMatchSnapshot()`. The first run creates the snapshot, later runs compare against it.

## Q24: How do you update snapshots?
**A:** Run with `-u` or `--update`, i.e. `vitest run -u`. Obsolete snapshots can be removed with `--update` after removing the code.

## Q25: What is `toMatchInlineSnapshot`?
**A:** It stores the snapshot inline inside the test file rather than a separate `.snap` file, keeping the expectation next to the code. Vitest fills it in on first run.

## Q26: How do you assert a function was called?
**A:** Use `expect(fn).toHaveBeenCalled()`, `toHaveBeenCalledTimes(n)`, and `toHaveBeenCalledWith(...args)` on a spy or mock created via `vi.fn`.

## Q27: What is `vi.fn`?
**A:** `vi.fn()` creates a mock function that records calls and can be given implementations/return values. It integrates with the `toHaveBeenCalled*` matchers.

## Q28: How do you set a return value on a mock?
**A:** Use `mockReturnValue` or `mockResolvedValue` for async:
```ts
const fn = vi.fn().mockReturnValue(42)
const asyncFn = vi.fn().mockResolvedValue('ok')
```

## Q29: What is `mockImplementation`?
**A:** It lets you define the function body of a mock so it computes results from arguments:
```ts
const fn = vi.fn((a, b) => a + b)
```

## Q30: What is `vi.spyOn`?
**A:** `vi.spyOn(obj, 'method')` wraps an existing method so you can assert calls and optionally change behavior, while still calling through by default. Call `.mockRestore()` to revert.

## Q31: How do you restore a spy?
**A:** Call `spy.mockRestore()` to remove the spy and restore the original method. Or rely on Vitest's automatic restoration if `mockReset`/`restoreMocks` is configured.

## Q32: What is the difference between `clearAllMocks`, `resetAllMocks`, and `restoreAllMocks`?
**A:** `clearAllMocks` clears call data; `resetAllMocks` also removes implementations and returns; `restoreAllMocks` restores original implementations for spies.

## Q33: How do you configure automatic mock cleanup?
**A:** In config set `test: { clearMocks: true, restoreMocks: true, mockReset: false }` as desired, or call cleanup in a setup file for predictable isolation.

## Q34: What is `vi.mock`?
**A:** `vi.mock('module')` mocks an entire module for the file; the factory runs before imports due to hoisting. It replaces the module's exports in that test file.

## Q35: Why is `vi.mock` hoisted and what is `vi.hoisted`?
**A:** Vitest hoists `vi.mock` above imports so the mock is active before the module under test loads. Use `vi.hoisted` to declare variables/factories that the hoisted mock needs:
```ts
const { mockFn } = vi.hoisted(() => ({ mockFn: vi.fn() }))
vi.mock('./db', () => ({ get: mockFn }))
```

## Q36: How do you use the real module with `vi.importActual`?
**A:** Inside a `vi.mock` factory, call `const actual = await vi.importActual('module')` to spread/reuse real exports while overriding specific ones.

## Q37: How do you mock a named export partially?
**A:** Combine `vi.importActual` with overrides:
```ts
vi.mock('./api', async () => {
  const actual = await vi.importActual('./api')
  return { ...actual, fetchUser: vi.fn() }
})
```

## Q38: What is `vi.doMock`?
**A:** Unlike `vi.mock`, `vi.doMock` is not hoisted and can be called dynamically inside a test, but you must import the module with `await import()` after calling it.

## Q39: How do you mock fetch?
**A:** Use `vi.stubGlobal('fetch', vi.fn())` or `vi.spyOn(globalThis, 'fetch')` and return a mocked Response:
```ts
vi.stubGlobal('fetch', vi.fn(async () => new Response('{}')))
```

## Q40: How do you mock a timer with fake timers?
**A:** Call `vi.useFakeTimers()` to replace `setTimeout`/`setInterval` etc., then control time with `vi.advanceTimersByTime(1000)` and reset with `vi.useRealTimers()`.

## Q41: What is `vi.advanceTimersByTime`?
**A:** It synchronously advances fake timers by the given milliseconds, firing any due callbacks. Use it to test debounces, intervals, and timeouts deterministically.

## Q42: How do you run only the timers that are pending once?
**A:** Use `vi.runOnlyPendingTimers()` to trigger currently scheduled timers without advancing real time, or `vi.runAllTimers()` to flush everything including nested timers.

## Q43: How do you test a debounced function?
**A:** Use fake timers: call the debounced fn, `vi.advanceTimersByTime(debounceMs)`, then assert. Always `vi.useRealTimers()` in `afterEach`.

## Q44: What is the difference between fake and real timers?
**A:** Real timers use the system clock and require waiting; fake timers are simulated by Vitest so you can advance time instantly and deterministically without delays.

## Q45: How do you mock `Date` with fake timers?
**A:** `vi.useFakeTimers()` also mocks `Date` by default; use `vi.setSystemTime(new Date('2020-01-01'))` to fix the current time for assertions.

## Q46: What are setup files in Vitest?
**A:** Files listed in `test.setupFiles` run before each test file, ideal for global mocks, extending matchers, or cleaning up (e.g., `cleanup` from Testing Library).

## Q47: How do you add jest-dom matchers?
**A:** Install `@testing-library/jest-dom` and import it in a setup file: `import '@testing-library/jest-dom/vitest'` (or `extendExpect` as needed). This adds `toBeInTheDocument` etc.

## Q48: How do you test Vue components with Vitest?
**A:** Use `@testing-library/vue` with `render` and `screen`, set `environment: 'jsdom'`, and assert on the DOM. Example: `const { getByText } = render(Comp); expect(getByText('Hi')).toBeInTheDocument()`.

## Q49: How do you test React components with Vitest?
**A:** Use `@testing-library/react` with `render`/`screen`, `environment: 'jsdom'`, and import jest-dom in setup. Same patterns as Jest but powered by Vitest.

## Q50: What is the difference between `render` in Testing Library and mounting directly?
**A:** Testing Library's `render` wraps components in a realistic DOM and provides queries; it encourages testing behavior over internals, unlike framework-specific mount APIs.

## Q51: What is test isolation in Vitest?
**A:** By default each test file runs in its own context (separate module registry), so module-level state doesn't leak between files. Within a file, reset mocks/state in `beforeEach`/`afterEach`.

## Q52: What is the difference between `globals: true` and importing APIs?
**A:** `globals: true` injects `describe/it/expect/vi` globally (less explicit, needs tsconfig types), while importing keeps code explicit and tree-shakeable and works without config.

## Q53: What test pools does Vitest support and what do they mean?
**A:** `threads` (default, isolates via worker threads), `forks` (child processes, stronger isolation, slower), and `vmThreads` (lighter isolates). Configured via `test.pool`.

## Q54: When would you use `pool: 'forks'`?
**A:** When you need true process isolation (e.g., to avoid shared native module state) at the cost of speed. Useful for tests that pollute the global environment heavily.

## Q55: What is `concurrent` testing?
**A:** Mark tests with `it.concurrent` (or `describe.concurrent`) so they run in parallel within a file, improving speed. Shared state must be avoided since order is not guaranteed.

## Q56: How do you run tests concurrently?
**A:** Use `it.concurrent('...', async () => {...})` or `describe.concurrent`. Vitest schedules them together but still isolates via the pool.

## Q57: What is a workspace config?
**A:** A `vitest.workspace.ts` (or `vitest.projects`) defines multiple project configs (e.g., unit + e2e + different environments) so Vitest runs them together with shared reporting.

## Q58: How do you define multiple projects/workspaces?
**A:** Create `vitest.workspace.ts` exporting an array of configs:
```ts
export default ['./pkg-a', './pkg-b', { test: { environment: 'jsdom' } }]
```

## Q59: How do you measure code coverage?
**A:** Install `@vitest/coverage-v8` (or `-istanbul`), set `test.coverage.enabled = true`, and run `vitest run --coverage`. Reports appear in `coverage/`.

## Q60: What is the difference between v8 and istanbul coverage?
**A:** v8 coverage uses V8's built-in coverage (fast, line/function/branch, no instrumented source) while istanbul instruments code (slower but more config options and better with transpiled edge cases).

## Q61: How do you set coverage thresholds?
**A:** Configure `test.coverage.lines`, `branches`, `functions`, `statements` thresholds; the run fails if not met:
```ts
coverage: { thresholds: { lines: 90, functions: 80 } }
```

## Q62: How do you exclude files from coverage?
**A:** Use `test.coverage.exclude` (globs) such as `['**/*.test.ts', '**/dist/**']`. Vitest has sensible defaults for test files and build output.

## Q63: What is `expectTypeOf`?
**A:** `expectTypeOf` performs type-level assertions at compile time without runtime cost:
```ts
expectTypeOf<number>().toEqualTypeOf<number>()
expectTypeOf(fn).parameter(0).toBeString()
```

## Q64: What is `assertType`?
**A:** `assertType<T>(value)` is a compile-time guard that fails to typecheck if `value` is not assignable to `T`, with no runtime effect.

## Q65: How is type testing different from runtime testing in Vitest?
**A:** Type tests run via `vitest typecheck` (enabled with `test.typecheck.enabled`) and verify TypeScript types, complementing runtime `expect` assertions.

## Q66: How do you run type tests?
**A:** Enable `test: { typecheck: { enabled: true } }` and run `vitest --typecheck` or `vitest typecheck`. It uses `tsc`/`vue-tsc` under the hood.

## Q67: What is `vitest bench`?
**A:** Vitest includes a benchmarking mode (`vitest bench`) to measure function performance using `bench()` definitions, similar to `it()` but for performance regressions.

## Q68: How do you write a benchmark?
**A:** Use `bench` from `vitest`:
```ts
import { bench } from 'vitest'
bench('map', () => [1,2,3].map(x => x*2))
```
Run with `vitest bench`.

## Q69: How do you mock a module that uses default export?
**A:** In `vi.mock`, return `{ default: vi.fn() }` (or your implementation). For `import x from 'm'`, the default key maps to the default export.

## Q70: How do you reset modules between tests?
**A:** Use `vi.resetModules()` (and `vi.doMock` re-evaluation) in `afterEach` to clear the module cache so re-imported modules get fresh state.

## Q71: What is `vi.resetModules` vs `vi.resetAllMocks`?
**A:** `vi.resetModules` clears the module registry so subsequent imports reload modules; `vi.resetAllMocks` resets mock functions' behavior and call data—different concerns.

## Q72: How do you test code that imports CSS?
**A:** Vite handles CSS imports natively; for tests you can set `css: false` in config or use `test.server.deps.inline`. Vitest ignores CSS side effects by default in test mode.

## Q73: How do you handle path aliases in tests?
**A:** Vitest reads `resolve.alias` from your Vite config automatically, so `@/` aliases work the same in tests as in the app without extra config.

## Q74: How do you use environment variables in tests?
**A:** Set them in a setup file or use `process.env`. For `.env`, Vite loads them; you can also use `vi.stubEnv('KEY', 'val')` and `vi.unstubAllEnvs()` for cleanup.

## Q75: What is `vi.stubEnv`?
**A:** `vi.stubEnv(name, value)` overrides an environment variable for the test and tracks it so `vi.unstubAllEnvs()` can restore originals, preventing cross-test leakage.

## Q76: How do you test functions that call `console`?
**A:** Spy on console: `vi.spyOn(console, 'log').mockImplementation(() => {})` and assert with `expect(console.log).toHaveBeenCalledWith(...)`. Restore after.

## Q77: How do you mock a class instance method?
**A:** Spy on the prototype or instance: `vi.spyOn(Service.prototype, 'method')` or `vi.spyOn(instance, 'method')`, then set return values/implementations as needed.

## Q78: How do you test event listeners / DOM events?
**A:** Render or create elements in jsdom, use `fireEvent` from Testing Library, and assert side effects. Fake timers help for debounced handlers.

## Q79: What is the difference between `fireEvent` and `userEvent`?
**A:** `fireEvent` dispatches a single DOM event synchronously; `userEvent` simulates realistic user interactions (typing, clicks) with async, more accurate behavior.

## Q80: How do you test a custom hook in React?
**A:** Use `renderHook` from `@testing-library/react`: `const { result } = renderHook(() => useCounter()); act(() => result.current.inc())`.

## Q81: How do you test a Vue composable?
**A:** Call it inside a `test` with `import { ref } from 'vue'` and assert on returned refs, or use `@vue/test-utils`'s `mount`/`composable` helpers with jsdom.

## Q82: How do you assert on console errors/warnings?
**A:** Spy on `console.error`/`console.warn` and assert calls; often combined with suppressing output. Useful to verify error handling without crashing tests.

## Q83: What is the difference between Vitest and pytest?
**A:** Vitest is JS/TS-focused, runs in Node with Vite transforms, uses `describe/it/expect`; pytest is Python, uses functions/classes with `assert` and fixtures. Different ecosystems and toolchains.

## Q84: How does Vitest handle ESM?
**A:** Because it runs on Vite, native ESM is first-class—no CommonJS interop hacks needed, and top-level `await`/dynamic `import()` work naturally.

## Q85: How do you mock a JSON import?
**A:** `vi.mock('data.json', () => ({ default: { foo: 'bar' } }))`. Vite supports JSON imports, and the mock replaces the resolved module.

## Q86: What is the `test.name` option for?
**A:** It names the current project/workspace so reports and dashboards can distinguish suites when running multiple projects.

## Q87: How do you run tests in a specific directory or with a pattern?
**A:** Pass a filter: `vitest run src/utils` or use filename patterns. Vitest matches by file path/glob and also supports `-t` to filter by test name.

## Q88: What does `-t` (`--testNamePattern`) do?
**A:** It filters which tests run by matching the test name against a regex, e.g. `vitest run -t "login"`. Great for re-running a subset quickly.

## Q89: How do you debug Vitest tests?
**A:** Run with a debugger: `node --inspect` via `vitest --inspect` or use VS Code's "Debug" config launching `vitest`. Add `console.log` or breakpoints in the test file.

## Q90: How do you test code using `import.meta.env`?
**A:** Vitest provides `import.meta.env.MODE` and `import.meta.env.TEST` is true during tests; you can stub env values with `vi.stubEnv` for mode-specific branches.

## Q91: What are common pitfalls with `vi.mock` hoisting?
**A:** Referencing variables inside the factory that aren't wrapped in `vi.hoisted` fails because the factory is hoisted above imports; always use `vi.hoisted` for external references.

## Q92: Why might mocks leak between tests and how to prevent it?
**A:** If you don't restore/reset mocks and modules, state carries over. Use `afterEach` with `vi.clearAllMocks()`, `vi.restoreAllMocks()`, `vi.resetModules()`, and `vi.unstubAllEnvs()`.

## Q93: How do you ensure deterministic tests with Math.random?
**A:** Spy/stub it: `vi.spyOn(Math, 'random').mockReturnValue(0.5)`. Restore afterward with `mockRestore()`.

## Q94: How do you test async code that uses callbacks?
**A:** Wrap the callback in a Promise and `await` it, or use `vi.waitFor` / `findBy*` queries from Testing Library which retry until assertions pass.

## Q95: What is `vi.waitFor`?
**A:** `vi.waitFor(() => expect(...).toBe(...))` retries the callback until it passes or times out, ideal for async UI updates without fixed sleeps.

## Q96: How do you set a test timeout?
**A:** Pass a third argument: `it('slow', async () => {}, 10000)` or set `test.testTimeout` globally. Default is 5000ms.

## Q97: How do you run Vitest in CI?
**A:** Use `vitest run --coverage` (non-watch) and set `CI=true`; many CI systems auto-detect. Add `--reporter=github` for annotations on GitHub Actions.

## Q98: What is the recommended project structure for tests?
**A:** Co-locate `*.test.ts`/`*.spec.ts` next to source, or use a `__tests__` folder. Configure `include`/`exclude` in `test` to match your convention.

## Q99: How do you extend Vitest with custom matchers?
**A:** Use `expect.extend({ toBeEven(received) { ...; return { pass, message } } })` in a setup file; then use `expect(x).toBeEven()`.

## Q100: What are best practices for mocking in Vitest?
**A:** Mock at the module boundary (use `vi.mock`), prefer spies when you still need real behavior, always restore/reset in `afterEach`, avoid over-mocking internals, and use fake timers for time-based logic to keep tests fast and deterministic.
