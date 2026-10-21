# Jest Interview Questions and Answers (Top 100)

## Q1: What is Jest?
**A:** Jest is a JavaScript testing framework maintained by Meta, designed for simplicity and works out-of-the-box with zero config for most projects. It supports unit, integration, and snapshot testing for JavaScript and TypeScript (including React, Node, and Vue).

## Q2: What are the main features of Jest?
**A:** Zero-config setup, a built-in assertion library (`expect`), mocking, code coverage (Istanbul), snapshot testing, parallel test execution, and fake timers. It also has a watch mode and strong TypeScript support via ts-jest.

## Q3: How do you install Jest?
**A:** Run `npm install --save-dev jest` (or `yarn add -D jest`). For TypeScript add `ts-jest` and `npm install --save-dev ts-jest`.

## Q4: How do you run tests with Jest?
**A:** Use `npx jest` to run all tests, or `npx jest path/to/test` to run a specific file. Add a `test` script in package.json: `"test": "jest"`.

## Q5: What is the default test file naming convention in Jest?
**A:** Jest looks for files matching `__tests__` folders, `.test.js`, `.spec.js`, or `.test.ts`/`.spec.ts`. You can override with the `testMatch` config option.

## Q6: How do you create a basic jest.config.js?
**A:** Create `jest.config.js` exporting an object: `module.exports = { testEnvironment: 'node' };`. Run `npx jest --init` to generate one interactively.

## Q7: How do you configure Jest for a Babel project?
**A:** Install `babel-jest` (ships with Jest) and add `@babel/preset-env`. Create `babel.config.js` with `module.exports = { presets: ['@babel/preset-env'] };`.

## Q8: How do you configure Jest for TypeScript?
**A:** Install `ts-jest` and add to config: `module.exports = { preset: 'ts-jest', testEnvironment: 'node' };`. Alternatively use Babel with `@babel/preset-typescript`.

## Q9: What is the difference between ts-jest and Babel for TypeScript?
**A:** `ts-jest` type-checks your code and gives better error messages, while Babel strips types faster without type checking. Use ts-jest when you want type-aware transforms.

## Q10: What is testEnvironment and what options exist?
**A:** `testEnvironment` sets the global environment: `'node'` for backend code or `'jsdom'` for browser/DOM code (used for React). Default is `'node'` (older) / `'jsdom'` in newer setups via create-react-app.

## Q11: How do you run only failing tests in watch mode?
**A:** In watch mode press `f` to run only failed tests, or use `jest --onlyFailures`. Press `o` to run tests related to changed files (needs git).

## Q12: What does `jest --watch` do?
**A:** It runs tests and re-runs them automatically on file changes. It enables interactive modes like filtering by name (`t`), failed tests (`f`), or changed files (`o`).

## Q13: What does `jest --coverage` do?
**A:** It runs tests and produces a code coverage report (lines, statements, branches, functions) using Istanbul. Configure thresholds via `coverageThreshold`.

## Q14: What does `jest --runInBand` do?
**A:** Runs all tests serially in the same process instead of parallel workers. Useful for debugging, or when tests use a shared resource like a database.

## Q15: How do you run a single test file?
**A:** Run `npx jest path/to/file.test.js` or `npx jest -t "test name"` to filter by test name pattern. You can also use the `.only` modifier.

## Q16: What is the purpose of `testMatch` and `testPathIgnorePatterns`?
**A:** `testMatch` defines which files are tests (glob patterns); `testPathIgnorePatterns` excludes paths (e.g., `node_modules`). They control test discovery.

## Q17: How do you limit which tests run using `testNamePattern`?
**A:** Use `jest -t "pattern"` or the `testNamePattern` config to run only `describe`/`it` blocks whose names match the regex.

## Q18: What is the structure of a Jest test?
**A:** Tests use `describe` to group and `it`/`test` for individual cases, with `expect(...).matcher()` assertions inside. Example: `test('adds', () => { expect(1+1).toBe(2); });`.

## Q19: What is the difference between `it` and `test`?
**A:** They are aliases; `it` reads like BDD ("it should do X") and `test` is more generic. They behave identically.

## Q20: How do `describe`, `it`, and `expect` relate?
**A:** `describe` groups related tests (can nest), `it`/`test` defines a test case, and `expect` asserts values. Assertions must be inside `it`/`test` callbacks.

## Q21: What are the lifecycle hooks in Jest?
**A:** `beforeEach`, `afterEach`, `beforeAll`, and `afterAll`. They run setup/teardown code before/after each test or all tests in a `describe` block.

## Q22: When would you use beforeAll vs beforeEach?
**A:** Use `beforeAll` for expensive one-time setup (e.g., opening a DB connection) and `beforeEach` for per-test resets (e.g., clearing a mock) to keep tests isolated.

## Q23: Can hooks be nested? How do they run?
**A:** Yes. Hooks run in order: outer `beforeAll`, then per test outer `beforeEach`, inner `beforeEach`, the test, inner `afterEach`, outer `afterEach`. `afterAll` runs last.

## Q24: What is the `expect` function?
**A:** `expect(value)` wraps a value to be tested and returns an object with matcher methods like `toBe` or `toEqual`. It is Jest's built-in assertion API.

## Q25: What is the difference between `toBe` and `toEqual`?
**A:** `toBe` uses `Object.is` (strict equality, no deep object comparison), while `toEqual` recursively checks deep equality of objects/arrays. Use `toEqual` for objects.

## Q26: What does `toStrictEqual` do that `toEqual` does not?
**A:** `toStrictEqual` also fails on undefined properties and type mismatches (e.g., `undefined` vs missing key, or class instances vs plain objects). `toEqual` ignores undefined props.

## Q27: How do you check that two objects match partially?
**A:** Use `toMatchObject({ a: 1 })` to assert a subset of properties, or `objectContaining({ a: 1 })` inside `toEqual`/`toStrictEqual`.

## Q28: How do you assert an array contains an item?
**A:** Use `expect(arr).toContain(item)` for primitives, or `expect(arr).toContainEqual(obj)` for objects by value.

## Q29: How do you assert a function throws?
**A:** Wrap in a function: `expect(() => fn()).toThrow()` or `expect(() => fn()).toThrow('error message')` / `toThrow(ErrorType)`.

## Q30: How do you assert a value is null, undefined, or defined?
**A:** Use `toBeNull()`, `toBeUndefined()`, `toBeDefined()`, plus `toBeTruthy()` and `toBeFalsy()` for boolean coercion checks.

## Q31: What number matchers are available?
**A:** `toBeGreaterThan`, `toBeGreaterThanOrEqual`, `toBeLessThan`, `toBeLessThanOrEqual`, `toBeCloseTo` (for floats), and `toBeNaN`.

## Q32: What string matchers exist?
**A:** `toMatch(/regex/)` or `toMatch('substring')`, plus `toBe`/`toEqual` for exact strings and `stringContaining`.

## Q33: How do you check something is an instance of a class?
**A:** Use `expect(obj).toBeInstanceOf(MyClass)` or `expect(obj).toEqual(expect.any(MyClass))`.

## Q34: How do you match "any" value in matchers?
**A:** Use `expect.any(Number)` or `expect.any(String)` to assert a type regardless of value, e.g. `expect(fn).toHaveBeenCalledWith(expect.any(Number))`.

## Q35: What does `expect.not` do?
**A:** It inverts a matcher: `expect(x).not.toBe(y)` or `expect(fn).not.toHaveBeenCalled()`.

## Q36: How do you test promises with async/await?
**A:** Mark the test callback `async` and `await` the promise, then assert: `test('x', async () => { const r = await fetchData(); expect(r).toBe(1); });`.

## Q37: How do you use `.resolves` and `.rejects`?
**A:** `await expect(promise).resolves.toBe(1);` and `await expect(promise).rejects.toThrow();`. They return promises that must be awaited or returned.

## Q38: How do you test async code with the `done` callback?
**A:** Pass `done` to the test and call it when finished: `test('x', done => { fn(() => { expect(1).toBe(1); done(); }); });`. Call `done(err)` to fail.

## Q39: Why must you return or await promises in Jest?
**A:** If you don't return/await the promise, Jest finishes the test before the async work resolves and assertions may not run or may fail silently.

## Q40: What is `jest.fn()`?
**A:** Creates a mock function that records calls, arguments, and return values. `const mock = jest.fn();` then inspect with `mock.calls` or matchers.

## Q41: How do you set a return value on a mock?
**A:** Use `mock.mockReturnValue(value)` or `mock.mockReturnValueOnce(value)` for a single call. Example: `mock.mockReturnValue(42);`.

## Q42: How do you implement a mock dynamically?
**A:** Use `mock.mockImplementation(fn)` to run custom logic, e.g. `jest.fn(x => x + 1)`. Use `mockImplementationOnce` for one-off behavior.

## Q43: How do you mock a resolved/rejected promise?
**A:** `mock.mockResolvedValue(value)` or `mock.mockResolvedValueOnce(value)`, and `mock.mockRejectedValue(new Error())` for rejections.

## Q44: How do you assert a mock was called?
**A:** `expect(mock).toHaveBeenCalled()`, `toHaveBeenCalledTimes(n)`, and `toHaveBeenCalledWith(...args)`. Also `toHaveBeenLastCalledWith`.

## Q45: What is `jest.spyOn`?
**A:** `jest.spyOn(obj, 'method')` creates a mock that wraps an existing method, recording calls while optionally calling the real implementation. Restore with `mockRestore()`.

## Q46: How do you restore a spy or mock?
**A:** Call `spy.mockRestore()` or wrap in `jest.restoreAllMocks()` in `afterEach`. `mockReset()`/`mockClear()` clear data but `mockRestore` reverts implementation.

## Q47: What is the difference between `mockClear`, `mockReset`, and `mockRestore`?
**A:** `mockClear` resets call data; `mockReset` also removes implementations and return values; `mockRestore` reverts to the original (for spies) and removes mock.

## Q48: How do you mock an entire module with `jest.mock`?
**A:** `jest.mock('module-name');` auto-mocks all exports as jest.fn(). Place it at top level. Then override specific exports with `mockReturnValue`.

## Q49: How do you use a factory function with `jest.mock`?
**A:** `jest.mock('axios', () => ({ get: jest.fn(() => Promise.resolve({ data: {} })) }));`. The factory returns the mocked module shape.

## Q50: What is `jest.requireActual`?
**A:** Returns the real, unmocked module: `const actual = jest.requireActual('lodash');`. Useful inside a mock factory to wrap the real implementation.

## Q51: How do you use the `__mocks__` folder?
**A:** Place a mock at `__mocks__/moduleName.js` adjacent to node_modules (or colocated for user modules) and call `jest.mock('moduleName')` to use it automatically without a factory.

## Q52: What is automock?
**A:** With `automock: true` in config or `jest.autoMockOn()`, Jest auto-mocks every imported module. Generally discouraged; explicit `jest.mock` is clearer.

## Q53: How do you prevent a module from being automocked?
**A:** Call `jest.unmock('module-name')` after enabling automock, so that module's real implementation is used.

## Q54: How do you mock `fetch`?
**A:** `global.fetch = jest.fn(() => Promise.resolve({ json: () => Promise.resolve({ ok: true }) }));`. Or use libraries like `jest-fetch-mock`.

## Q55: How do you mock axios?
**A:** `jest.mock('axios');` then `axios.get.mockResolvedValue({ data: 'x' });`. For a single call use `mockResolvedValueOnce`.

## Q56: How do you test a module that imports lodash?
**A:** `jest.mock('lodash');` then `const _ = require('lodash'); _.debounce.mockImplementation(fn => fn);` to neutralize debounce/throttle.

## Q57: How do you mock moment or date-fns?
**A:** Mock the module and stub methods: `jest.mock('moment'); moment.mockImplementation(() => ({ format: () => '2020-01-01' }));`. Or use fake timers.

## Q58: What are fake timers and why use them?
**A:** `jest.useFakeTimers()` replaces setTimeout/setInterval with mock timers so you control time without waiting. Use for debounce, polling, schedules.

## Q59: How do you advance fake timers?
**A:** `jest.advanceTimersByTime(1000)` (ms) or `jest.advanceTimersToNextTimer()`. Then assert effects that should have happened after the delay.

## Q60: How do you mock the system clock / Date?
**A:** `jest.setSystemTime(new Date('2020-01-01'))` after `useFakeTimers()` to fix `Date.now()` and `new Date()`. Reset with `jest.useRealTimers()`.

## Q61: What is a common fake timers gotcha with async?
**A:** Fake timers don't advance real microtasks; promises resolve on the real microtask queue. Use `jest.advanceTimersByTime` plus `await Promise.resolve()` or `modern` fake timers with `await`.

## Q62: How do you test code that uses setInterval?
**A:** `jest.useFakeTimers(); fn(); jest.advanceTimersByTime(5000); expect(cb).toHaveBeenCalledTimes(5);` then `jest.useRealTimers()`.

## Q63: What is snapshot testing?
**A:** `expect(value).toMatchSnapshot()` serializes a value and saves it to a `.snap` file on first run; subsequent runs compare. Detects unintended UI/data changes.

## Q64: How do you update snapshots?
**A:** Run `jest -u` or `jest --updateSnapshot`. Use `--ci` to fail on new snapshots instead of writing them in CI.

## Q65: What are inline snapshots?
**A:** `expect(value).toMatchInlineSnapshot()` writes the snapshot directly into the test file instead of a separate `.snap` file, keeping tests self-contained.

## Q66: How do you handle dynamic values in snapshots?
**A:** Use `expect.any`, `expect.stringMatching`, or asymmetric matchers like `expect.objectContaining` so volatile fields (ids, dates) don't break snapshots.

## Q67: How do you mock CSS modules / SCSS imports?
**A:** Add a moduleNameMapper: `'\\.(css|scss)$': 'identity-obj-proxy'` (with `identity-obj-proxy` installed) or map to a stub file returning an empty object.

## Q68: How do you mock image/asset imports?
**A:** Use `moduleNameMapper`: `'\\.(png|jpg|svg)$': '<rootDir>/__mocks__/fileMock.js'` where the mock exports a string filename.

## Q69: What is setupFiles vs setupFilesAfterEach?
**A:** `setupFiles` runs before the test framework is installed (good for polyfills); `setupFilesAfterEach` (actually `setupFilesAfterEnv`) runs after, for global config like `jest-dom`.

## Q70: How do you add custom matchers like jest-dom?
**A:** Install `@testing-library/jest-dom` and add to `setupFilesAfterEnv`: `['<rootDir>/jest.setup.js']` which imports `'@testing-library/jest-dom'`.

## Q71: What is the correct config key for setup files that need the DOM?
**A:** `setupFilesAfterEnv` (not `setupFilesAfterEach`). It runs after the test environment is set up, enabling `expect.extend` and jest-dom matchers.

## Q72: How do you define Jest globals?
**A:** In config: `globals: { API_URL: 'http://test' }` or set `global` in a setup file. Accessible in tests as `global.API_URL`.

## Q73: How is code coverage collected and reported?
**A:** Jest uses Istanbul/Babel to instrument code. Reports (text, html, lcov) appear with `--coverage`; configure via `coverageReporters` and `collectCoverageFrom`.

## Q74: How do you enforce coverage thresholds?
**A:** Set `coverageThreshold` in config: `{ global: { branches: 80, functions: 80, lines: 80, statements: 80 } }`. CI fails if unmet.

## Q75: How do you collect coverage only from source files?
**A:** Use `collectCoverageFrom: ['src/**/*.{js,ts}', '!src/**/*.d.ts']` to include/exclude files even if untested.

## Q76: How does Jest run tests in parallel?
**A:** Jest spawns worker processes (based on CPU cores) and distributes test files across them. Each file runs in isolation; `maxWorkers` controls concurrency.

## Q77: What is test isolation and how does Jest provide it?
**A:** Each test file gets a fresh module registry and environment, so mocks/state don't leak between files. Within a file, use `beforeEach` to reset state.

## Q78: How do you reset modules between tests?
**A:** Call `jest.resetModules()` in `beforeEach` then re-`require` the module, useful when testing modules with mutable singletons or env-dependent init.

## Q79: How do you test React components with Jest?
**A:** Use `@testing-library/react` (or Enzyme) with `testEnvironment: 'jsdom'`. Render with `render(<Comp />)` and assert with `screen.getByText` and jest-dom matchers.

## Q80: How do you test a click handler in React with Testing Library?
**A:** `const onClick = jest.fn(); render(<Btn onClick={onClick}/>); fireEvent.click(screen.getByRole('button')); expect(onClick).toHaveBeenCalled();`.

## Q81: How do you mock a hook or child component in React tests?
**A:** Mock the module: `jest.mock('./useApi', () => ({ useApi: () => ({ data: 'x' }) }));`. Or use `jest.spyOn` on the hook's module.

## Q82: What is the difference between `@testing-library/react` and Enzyme?
**A:** Testing Library encourages testing behavior from the user's perspective (queries by role/text), while Enzyme offers shallow/deep rendering and component internals inspection.

## Q83: How do you test React state updates / async UI?
**A:** Use `findBy*` queries which return promises, and `await screen.findByText('loaded')`; wrap in `waitFor(() => expect(...))` for other async effects.

## Q84: How do you use `waitFor`?
**A:** `await waitFor(() => expect(screen.getByText('done')).toBeInTheDocument());` retries the callback until it passes or times out, handling async UI updates.

## Q85: How do you test a custom hook?
**A:** Use `renderHook` from `@testing-library/react`: `const { result } = renderHook(() => useCounter()); act(() => result.current.inc());`.

## Q86: What matchers does jest-dom add?
**A:** `toBeInTheDocument()`, `toBeVisible()`, `toHaveClass()`, `toHaveValue()`, `toHaveAttribute()`, `toBeDisabled()`, etc., for DOM assertions.

## Q87: How do you mock a module only for one test?
**A:** Use `jest.mock` at top (hoisted) then `mock.mockImplementation` inside the specific test, or use `jest.doMock` (not hoisted) with a local require inside the test.

## Q88: What is `jest.isolateModules`?
**A:** `jest.isolateModules(() => { const mod = require('./mod'); })` runs the callback with a fresh module registry so you can test module side-effects repeatedly.

## Q89: How do you mock a Node.js built-in like fs?
**A:** `jest.mock('fs');` then `const fs = require('fs'); fs.readFileSync.mockReturnValue('data');`. Or use `jest.requireActual` to keep some methods real.

## Q90: How do you test code that writes to console?
**A:** `jest.spyOn(console, 'log').mockImplementation(() => {});` then assert `expect(console.log).toHaveBeenCalledWith('x')`, and restore in `afterEach`.

## Q91: How do you skip or focus tests?
**A:** `test.skip('x', () => {})` / `describe.skip` to skip, and `test.only('x', () => {})` / `it.only` (or `fdescribe`) to run only those.

## Q92: What is the difference between Jest, Mocha, and Vitest?
**A:** Jest is an all-in-one framework with built-in mocking/coverage; Mocha is a lean runner needing separate assertion/mock libs; Vitest is Vite-native, faster, API-compatible with Jest for modern ESM/Vite projects.

## Q93: Why might you choose Vitest over Jest?
**A:** Vitest uses Vite's transform pipeline (instant ESM/TS, no extra babel/ts-jest config), shares config with Vite, and is faster for Vite-based projects. Jest remains better for legacy/CRA setups.

## Q94: How do you mock ESM / ES modules in Jest?
**A:** ESM mocking is limited; prefer `jest.unstable_mockModule` with dynamic `import()`, or transpile to CJS via ts-jest/babel. Static `jest.mock` works reliably with CommonJS.

## Q95: How do you test error boundaries or thrown errors in React?
**A:** Wrap with an error boundary component and assert fallback UI, or spy on `console.error` and expect it was called with the error. Testing Library doesn't catch errors directly.

## Q96: What is a common pitfall with `toBe` on objects?
**A:** `expect({a:1}).toBe({a:1})` fails because `toBe` checks reference equality. Use `toEqual` for structural comparison of objects/arrays.

## Q97: What is a common pitfall with fake timers and `Date.now`?
**A:** After `useFakeTimers`, you must `setSystemTime` or advance timers; otherwise `Date.now()` stays at the mocked start. Always `useRealTimers()` in `afterEach` to avoid leaking.

## Q98: How do you avoid leaking mock state between tests?
**A:** In `afterEach`, call `jest.clearAllMocks()`, `jest.resetAllMocks()`, or `jest.restoreAllMocks()`; use `jest.resetModules()` if modules cache mutable state.

## Q99: What are Jest best practices?
**A:** Keep tests isolated and fast, prefer `toEqual` for objects, use `beforeEach` to reset, mock at module boundaries, avoid testing implementation details, and use snapshots sparingly.

## Q100: How do you debug Jest tests?
**A:** Run `node --inspect-brk node_modules/.bin/jest --runInBand` and attach a debugger, or use `console.log`, `jest --verbose`, and `it.only` to isolate a failing test.
