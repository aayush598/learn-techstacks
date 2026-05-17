## 9. Zustand + React Hooks (261–290)

261. What is Zustand?
     Z**Answer:** Zustand is a lightweight state management library for React with a minimal API. It uses hooks-based store creation outside the component tree, supports middleware, and requires minimal boilerplate compared to Redux.

262. Difference between Zustand and Redux?
     Z**Answer:** Zustand has a simpler API (no actions/reducers/dispatch), smaller bundle size (~1KB vs ~12KB), and doesn't require context providers. Redux has a more opinionated structure with middleware ecosystem and DevTools, better suited for very large applications.

263. Explain Zustand store creation.
     S**Answer:** Stores are created with `create()` which takes a callback function receiving `set`, `get`, and `store` API. The callback returns the state object and actions. The returned hook provides access to state via selectors and actions directly.

264. What are selectors in Zustand?
     S**Answer:** Selectors extract specific state slices to optimize re-renders. `useStore(state => state.count)` subscribes only to `count` changes. Zustand uses referential equality by default — memoization with `useShallow` prevents unnecessary renders for object selectors.

265. Explain middleware in Zustand.
     M**Answer:** Middleware wraps store creation to add functionality: `persist` (localStorage/sessionStorage), `immer` (immutable state with mutable syntax), `devtools` (Redux DevTools integration), `subscribeWithSelector` (granular subscriptions), and `redux` (Redux-like reducer pattern).

266. How does persistence work?
     T**Answer:** The `persist` middleware saves state to storage (localStorage, sessionStorage, or custom) and rehydrates on app load. It handles partial persistence via `partialize`, versioning for migrations, and merge strategies for schema changes.

267. Explain immer middleware.
     T**Answer:** The `immer` middleware lets you write state updates with mutable syntax while maintaining immutability. Instead of spreading objects, you directly mutate a draft: `set(state => { state.count += 1 })`. Immer produces immutable state under the hood.

268. What are shallow comparisons?
     S**Answer:** Shallow comparisons check if object references changed rather than deep equality. Zustand uses shallow comparison by default — if a selector returns a new object each render, it triggers re-renders. `useShallow` provides shallow equality for object selectors.

269. Explain global vs local state.
     G**Answer:** Global state is shared across components (user auth, theme) managed by Zustand or Context. Local state is component-specific (form inputs, toggles) managed by `useState` or `useReducer`. Rule of thumb: lift state only as high as needed.

270. What are React hooks?
     H**Answer:** Hooks are functions that let you use React features (state, lifecycle, context) in function components. They replace class component patterns with `useState`, `useEffect`, `useContext`, `useRef`, `useMemo`, `useCallback`, and custom hooks for reusable logic.

271. Explain useState.
     `**Answer:** `useState(initialValue)` returns a tuple `[value, setValue]` where `value` is the current state and `setValue` triggers re-render with the new value. The setter can accept a value or updater function `prev => prev + 1` for computed updates.

272. Explain useEffect lifecycle.
     `**Answer:** `useEffect(callback, deps)` runs side effects after render. It runs on mount, when deps change, and cleanup runs on unmount or before re-execution. With empty deps `[]` it runs once on mount. With no deps it runs after every render.

273. What are dependency arrays?
     D**Answer:** Dependency arrays list values that `useEffect`, `useMemo`, and `useCallback` watch for changes. When a dependency changes, the hook re-executes. Omitting required deps causes stale closures; including unnecessary deps causes excessive re-execution.

274. Explain stale closures.
     S**Answer:** Stale closures occur when a hook captures a variable value from a previous render. When the callback executes later, it uses the old value. This happens with missing dependencies in `useEffect`, `useCallback`, or `setTimeout` — fixed by including proper deps.

275. What is useMemo?
     `**Answer:** `useMemo(() => expensiveComputation(a, b), [a, b])` memoizes the result of an expensive computation, recomputing only when dependencies change. It optimizes performance by avoiding recalculations on every render.

276. Explain useCallback.
     `**Answer:** `useCallback(fn, deps)` returns a memoized function reference that only changes when deps change. It prevents child components from re-rendering unnecessarily when the callback is passed as a prop, especially with `React.memo`.

277. Difference between useRef and useState?
     `**Answer:** `useRef` persists a mutable value across renders without causing re-renders when changed. `useState` triggers re-rendering on updates. Use `useRef` for DOM references and values that shouldn't trigger UI updates (intervals, previous values).

278. Explain custom hooks.
     C**Answer:** Custom hooks extract reusable stateful logic from components into functions prefixed with `use`. They can use other hooks internally and return state and actions. Examples: `useLocalStorage`, `useDebounce`, `useFetch`, `useIntersectionObserver`.

279. What are hook rules?
     T**Answer:** Two rules: (1) Only call hooks at the top level — not inside loops, conditions, or nested functions. (2) Only call hooks from React functions (components or custom hooks). These ensure consistent hook order across renders.

280. Explain hook re-render optimization.
     O**Answer:** Optimize by using `useMemo`/`useCallback` to stabilize references, `React.memo` to skip child re-renders, selectors in Zustand to subscribe to minimal state, `useShallow` for objects, and `useRef` for values that don't need re-renders.

281. What is context API?
     C**Answer:** Context API provides a way to pass data through the component tree without prop drilling. `createContext` creates a context, `Provider` wraps the tree with a value, and `useContext` consumes it. It's simpler than prop drilling but causes re-renders for all consumers.

282. Explain React reconciliation.
     R**Answer:** Reconciliation is React's diffing algorithm that updates the DOM efficiently. It compares virtual DOM trees, uses keys for list reconciliation, and applies minimal DOM mutations. The process determines which parts of the UI need updating.

283. What causes unnecessary re-renders?
     C**Answer:** Causes include: parent re-render propagating to children, creating new objects/arrays in render (breaking memoization), inline functions breaking `React.memo`, incorrect dependency arrays in hooks, and context changes affecting all consumers.

284. Explain batching in React.
     B**Answer:** Batching groups multiple state updates into a single re-render for performance. In React 18, all state updates (including promises, timeouts, and native events) are automatically batched, preventing intermediate renders between sequential `setState` calls.

285. What is concurrent rendering?
     C**Answer:** Concurrent rendering (React 18+) allows React to interrupt long renders to handle higher-priority updates. It enables features like `startTransition` for marking non-urgent updates, `useDeferredValue` for debouncing state, and Suspense for streaming.

286. Explain Suspense.
     S**Answer:** Suspense lets components "wait" for something before rendering, showing a fallback (spinner) while data loads. It works with React.lazy for code splitting and React 18's streaming SSR for progressively rendering server-rendered content.

287. What are transitions in React?
     T**Answer:** Transitions (via `startTransition`) mark state updates as non-urgent, allowing React to keep showing the current UI while processing the update. During transitions, the UI remains responsive, and urgent updates like input typing take priority.

288. Explain server state vs client state.
     S**Answer:** Server state (data from API) persists on the server and is managed by libraries like TanStack Query or SWR with caching and refetching. Client state (UI state, form inputs) exists only in the browser and uses Zustand/Context/useState.

289. How do hooks work internally?
     H**Answer:** Hooks use a linked list stored on the fiber node. Each call appends a node to the list — order must be consistent across renders. The current pointer advances through the list, matching hook calls to their persisted state.

290. Explain React performance optimization.
     O**Answer:** Optimizations include: `React.memo` for pure components, `useMemo`/`useCallback` to memoize values/functions, virtualization for long lists (react-window), lazy loading with `React.lazy`, code splitting, bundle analysis, and profiling with React DevTools Profiler.
