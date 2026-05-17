## 47. Zustand + React Expert Topics (1261–1290)

1261. How do React fibers schedule rendering work?

   **Answer:** React fibers represent units of work in a linked-list tree structure that the reconciler processes incrementally. Each fiber carries priority metadata (lane), pending work, and alternate pointers, enabling interruptible rendering.

1262. Explain lane priorities in React.

   **Answer:** Lanes are 32-bit bitmasks that encode rendering priority, with lower-numbered bits representing higher priority (transitions vs urgent updates). The reconciler processes lanes in order, starving lower-priority work until high-priority lanes drain.

1263. What are interruptible renders?

   **Answer:** Interruptible renders let React pause mid-reconciliation to process higher-priority updates or user input. The current incomplete work is discarded, and the reconciler restarts from the root with the new update's priority.

1264. Explain concurrent rendering starvation.

   **Answer:** Starvation occurs when continuous high-priority updates (like typing) prevent lower-priority work (like data fetching transitions) from ever completing. React's scheduling heuristics eventually boost starved lanes to ensure fairness.

1265. How do transitions defer updates?

   **Answer:** Transitions (`startTransition`) mark state updates as non-urgent, allowing React to delay their rendering in favor of more critical updates. The deferred update can be interrupted by new urgent updates and may never render if superseded.

1266. Explain hydration interruption.

   **Answer:** Hydration interruption occurs when the user interacts with partially hydrated content, forcing React to abort the current hydrate pass and prioritize the interaction. Remaining server HTML is discarded and rendered client-side.

1267. What are suspense boundary fallback strategies?

   **Answer:** Fallback strategies include showing spinners, skeleton screens, or partial content while suspended data loads. Nested boundaries can show multiple fallbacks, and the `useDeferredValue` hook prevents flash-of-fallback on fast networks.

1268. Explain React cache internals.

   **Answer:** React's internal cache stores the results of async operations per component rendering, purging entries when all referencing components unmount. The `cache` function deduplicates calls within a render pass but doesn't persist across renders.

1269. How does Zustand minimize subscriptions?

   **Answer:** Zustand minimizes subscriptions using atomic selector comparisons—components subscribe to specific state slices, and Zustand only notifies when the selected slice changes (defaulting to `Object.is` comparison). This prevents unnecessary re-renders.

1270. Explain optimistic state reconciliation.

   **Answer:** Optimistic reconciliation updates the UI immediately with the expected result of an async mutation, then confirms or rolls back when the server responds. Zustand's `setState` with a getter enables this pattern without separate state management.

1271. What are state rollback mechanisms?

   **Answer:** State rollback saves a snapshot before optimistic updates and restores it on failure. Zustand implements this through middleware or manual snapshot/restore patterns, preserving undo history for failed operations.

1272. Explain fine-grained reactivity.

   **Answer:** Fine-grained reactivity tracks individual property accesses rather than full state tree comparisons. Zustand achieves this via `useStore` with selectors and shallow equality, while libraries like Valtio use Proxy-based tracking.

1273. How do external stores integrate with React?

   **Answer:** External stores integrate via `useSyncExternalStore` (or `subscribe`/`getSnapshot` in Zustand's case), which ensures React reads consistent state and subscribes to changes without tearing during concurrent rendering.

1274. Explain rendering consistency guarantees.

   **Answer:** React's concurrent mode guarantees that a component sees the same state snapshot throughout a single render, even if the store updates concurrently. `useSyncExternalStore` enforces this by failing if the snapshot changes during rendering.

1275. What are stale snapshot issues?

   **Answer:** Stale snapshots occur when a closure captures state at render time but reads it later in an async callback or effect, missing intermediate updates. Using refs or Zustand's `getState()` inside callbacks resolves this.

1276. Explain React scheduler priorities.

   **Answer:** React's scheduler assigns each unit of work a priority level (Immediate, UserBlocking, Normal, Low, Idle) that determines its position in the work queue. The scheduler yields to the main thread every ~5ms to keep the UI responsive.

1277. How does React batch updates across async boundaries?

   **Answer:** React automatically batches state updates inside event handlers and effects. Updates in `setTimeout`, Promises, or native event handlers are also batched in React 18+ via automatic batching, reducing re-renders.

1278. Explain render tearing prevention.

   **Answer:** Render tearing happens when concurrent renders see different state values for the same component. `useSyncExternalStore` prevents this by requiring external stores to return consistent snapshots during a single render and throwing on inconsistency.

1279. What are advanced custom hook architectures?

   **Answer:** Advanced hook architectures include state machines with `useReducer`, parameterized hooks for derived state, hook factories for dynamic behavior, and composed hooks that split concerns without prop drilling.

1280. Explain hook dependency graph design.

   **Answer:** Hook dependency graphs model how data flows between hooks, identifying unnecessary re-computations and stale closures. Tools like `useMemo`, `useCallback`, and `useMemoizedFn` stabilize references to minimize cascading updates.

1281. How do reducers compare to external stores?

   **Answer:** Reducers (useReducer) are local to a component tree and reset on unmount, while external stores (Zustand) persist across navigations and share state between unrelated components. Reducers suit form state; stores suit global or server state.

1282. Explain derived selectors.

   **Answer:** Derived selectors compute new values from base state using memoized selectors (Zustand's `create` with middleware or `reselect`). They recompute only when source values change, providing efficient access to computed data.

1283. What are React synchronization pitfalls?

   **Answer:** Pitfalls include missing dependencies in `useEffect` (causing stale closures), infinite loops from setting state in effects, and race conditions where an effect completes after the component unmounts.

1284. Explain render memoization tradeoffs.

   **Answer:** Memoization with `React.memo`, `useMemo`, and `useCallback` trades memory and comparison overhead for skip-rendering benefits. Over-memoizing without profiling wastes memory, while under-memoizing causes unnecessary re-renders in large trees.

1285. How do portals preserve context?

   **Answer:** Portals render children into a different DOM subtree but preserve React context because portal children remain in the parent component's React tree. This allows modals and tooltips to access theme, auth, and other contexts.

1286. Explain React event replay.

   **Answer:** Event replay is a React 19 feature that replays user interactions that occurred before hydration completes, queuing them and applying them after hydration to prevent lost interactions.

1287. What are hydration consistency problems?

   **Answer:** Hydration consistency issues arise when the server-rendered HTML doesn't match the first client render due to browser-only APIs, random values, or time-dependent data. React logs warnings and discards mismatched DOM to avoid corruption.

1288. Explain frontend resilience patterns.

   **Answer:** Frontend resilience patterns include error boundaries per feature, graceful degradation when APIs fail, retry logic with exponential backoff, and fallback UI that keeps the app functional despite partial failures.

1289. What are frontend observability strategies?

   **Answer:** Frontend observability strategies capture Web Vitals (LCP, FID, CLS), error tracking with source maps, custom performance markers, and user interaction analytics. Tools like Sentry, Datadog RUM, and OpenTelemetry provide visibility.

1290. How do large teams scale React state management?

   **Answer:** Large teams scale state management by separating concerns: server state in TanStack Query, global UI state in Zustand, form state in React Hook Form, and URL state in Next.js searchParams. Clear ownership per concern prevents conflict.
