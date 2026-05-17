## 28. Zustand + React Hooks Advanced (761–790)

761. How do Zustand subscriptions work internally?

   **Answer:** Zustand stores use a publish-subscribe pattern. `setState` notifies all subscribers via an internal listener array; `useStore` hooks subscribe by pushing a listener, and React re-renders when the selected state changes.

762. Explain selector memoization.

   **Answer:** Selector functions extract specific state slices. Without memoization (using `useShallow` or `useRef`), new object references on every render cause unnecessary re-renders. Zustand's `useStore` with equality comparers optimizes this.

763. What are derived states?

   **Answer:** Derived states are computed from existing store state without redundant storage. Zustand computes them in selectors or with custom hooks (e.g., `useMemo`), avoiding synchronization bugs.

764. Explain store slicing strategies.

   **Answer:** Store slicing splits Zustand stores into logical domains (auth, cart, UI) using separate `create` calls or a single store with nested slices. Slices communicate via the shared store or custom events.

765. How does Zustand compare to Jotai?

   **Answer:** Zustand uses a single store with selectors; Jotai uses atomic atoms with dependency tracking. Zustand is simpler for global state; Jotai excels at fine-grained reactivity and code-splittable state.

766. Explain Zustand with SSR.

   **Answer:** Zustand in SSR requires creating a fresh store per request to prevent cross-request state leakage. Use `createStore` on the server, then hydrate the client store with `useStore.setState()`.

767. What are hydration synchronization issues?

   **Answer:** Hydration issues occur when server-rendered HTML doesn't match client state. Zustand's `persist` middleware can cause mismatches if async hydration hasn't completed during first render.

768. Explain state normalization.

   **Answer:** State normalization structures nested data as flat dictionaries with IDs (like Redux). Normalization in Zustand simplifies updates, avoids deep nesting, and improves selector performance.

769. What are stale renders?

   **Answer:** Stale renders occur when a component displays outdated state because it hasn't re-rendered after a store change. Zustand avoids this by triggering subscriptions only when selected values actually change.

770. Explain useSyncExternalStore.

   **Answer:** `useSyncExternalStore` is a React hook for external stores. Zustand uses it internally to subscribe and get consistent state snapshots, preventing tearing in concurrent React rendering.

771. How does React scheduling work?

   **Answer:** React's scheduler prioritizes work: user input (highest), animations, then data fetching. It uses requestIdleCallback and message channels to yield to the browser, splitting rendering into chunks.

772. Explain render phases.

   **Answer:** The render phase calls components and produces fiber updates (pure, side-effect-free). React may pause, resume, or discard render work. The commit phase applies DOM mutations synchronously.

773. What are commit phases?

   **Answer:** The commit phase applies render results to the DOM. In the "before mutation" phase, React reads DOM state; the "mutation" phase mutates the DOM; the "layout" phase runs `useLayoutEffect` and reads layout.

774. Explain React fiber architecture.

   **Answer:** Fiber is React's core reconciliation engine. Each fiber node represents a component instance with state, effects, and child/sibling pointers. The work loop processes fibers incrementally, enabling interruption and prioritization.

775. How does reconciliation prioritize updates?

   **Answer:** React assigns lanes (priority bitmasks) to updates. Sync lanes (user input) are processed immediately, default lanes (data fetching) yield to the browser, and idle lanes (prefetching) run when the thread is free.

776. Explain tearing in concurrent rendering.

   **Answer:** Tearing occurs when concurrent renders see inconsistent external store values. `useSyncExternalStore` prevents tearing by forcing consistent snapshots during rendering using React's subscription model.

777. What are render blocking updates?

   **Answer:** Render blocking updates are high-priority state changes that suspend concurrent rendering. They include synchronous updates (`flushSync`) and transitions not wrapped in `startTransition`.

778. Explain transitions scheduling.

   **Answer:** `startTransition` marks updates as low priority, allowing React to interrupt them for urgent updates. Transitions show stale UI briefly until the transitioned state is ready.

779. How do refs persist values?

   **Answer:** `useRef` holds mutable values across renders without causing re-renders. The ref object is created once per component mount and persists via the fiber node's memoized state.

780. Explain state batching internals.

   **Answer:** React batches state updates within event handlers, effects, and async contexts (React 18+). Instead of re-rendering per `setState`, React collects updates and flushes in a single render pass.

781. What are render props?

   **Answer:** Render props are functions passed as component props to control rendering: `<DataProvider render={data => <View data={data} />} />`. They enable code reuse and inversion of control.

782. Explain hook composition patterns.

   **Answer:** Custom hooks compose primitive hooks (`useState`, `useEffect`) into reusable logic. Patterns include `useAuth()` (combines state + effect + context), `useDebounce()`, and `useMediaQuery()`.

783. What are controlled vs uncontrolled components?

   **Answer:** Controlled components have state managed by React (`value` + `onChange`). Uncontrolled components manage their own DOM state via refs. Controlled gives React full control; uncontrolled is simpler for forms.

784. Explain imperative handles.

   **Answer:** `useImperativeHandle` with `forwardRef` exposes custom methods to parent refs. It restricts access to only the specified API, keeping internal implementation private.

785. How do portals work?

   **Answer:** Portals (`createPortal`) render children into a different DOM node outside the parent hierarchy. They're useful for modals, tooltips, and dropdowns where CSS overflow or z-index is problematic.

786. Explain React synthetic events.

   **Answer:** Synthetic events wrap native browser events for cross-browser consistency. React pools synthetic events for performance (pre-React 17) and attaches event listeners at the root via delegation.

787. What are event delegation benefits?

   **Answer:** Event delegation attaches a single event listener on a common ancestor instead of per-element listeners. It reduces memory usage and simplifies dynamic children, as React does with its root-level delegation.

788. Explain optimistic UI patterns.

   **Answer:** Optimistic UI immediately reflects user actions in the UI before server confirmation. On success, no update needed; on failure, roll back. Zustand + TanStack Query manage optimistic states with cache rollbacks.

789. What are React anti-patterns?

   **Answer:** Anti-patterns include mutating state directly, infinite useEffect loops, excessive re-renders, giant components, mixing server/client logic, using state when a ref is sufficient, and ignoring cleanup functions.

790. How do you debug rendering bottlenecks?

   **Answer:** Debug with React DevTools profiler, `why-did-you-render` library, `console.log` in render bodies, Chrome Performance tab, React's `<Profiler>` component, and checking selector memoization in Zustand.
