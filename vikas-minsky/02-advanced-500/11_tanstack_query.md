## 30. TanStack Query Advanced (806–830)

806. Explain cache hydration internals.

   **Answer:** Hydration serializes the query cache on the server and deserializes on the client using `dehydrate`/`hydrate`. The `QueryCache` stores serialized queries (key, data, state) which are restored before client-side queries execute.

807. How do observers trigger updates?

   **Answer:** Each `useQuery` call creates an observer subscribed to the query cache. When cache data changes, all observers are notified and trigger re-renders via React state updates.

808. Explain stale data synchronization.

   **Answer:** Stale data is determined by `staleTime`. When a query becomes stale, TanStack Query automatically refetches in the background on mount, window refocus, or network reconnection.

809. What are background refresh strategies?

   **Answer:** Strategies include refetchOnMount, refetchOnWindowFocus, refetchOnReconnect, and refetchInterval. Each triggers background refetches to keep data fresh without blocking the UI.

810. Explain query cancellation.

   **Answer:** TanStack Query supports query cancellation via `AbortController`. The `queryFn` receives an `AbortSignal`; aborting cancels in-flight requests, preventing race conditions and wasted bandwidth.

811. How does optimistic concurrency work?

   **Answer:** Optimistic updates immediately apply mutations to the cache before server confirmation. On error, the cache rolls back to the previous state, providing instant feedback with safe rollback.

812. Explain parallel query execution.

   **Answer:** Parallel queries run independent queries concurrently using `useQueries` hook or multiple `useQuery` calls. TanStack Query manages each query independently, deduplicating identical parallel requests.

813. What are race conditions in queries?

   **Answer:** Race conditions occur when a slower previous request overwrites a newer response. TanStack Query prevents this by tracking query hash and discarding stale responses from outdated keys.

814. Explain dedupe intervals.

   **Answer:** Deduplication merges concurrent requests with identical query keys into a single network call. Within the dedupe window, additional subscribers wait for the same promise rather than creating new requests.

815. How do mutations synchronize caches?

   **Answer:** After a mutation succeeds, `onSuccess` invalidates or updates related query caches via `queryClient.invalidateQueries()` or `queryClient.setQueryData()`, ensuring read data reflects the mutation.

816. Explain cache invalidation granularity.

   **Answer:** Granular invalidation targets specific queries by key patterns: exact keys, prefix matching (e.g., `['posts']` matches `['posts', '1']`), or predicate functions. Coarse invalidation refreshes entire cache segments.

817. What are persistence adapters?

   **Answer:** Persistence adapters (e.g., `@tanstack/query-persist-client-core`) save the query cache to `localStorage`, `AsyncStorage`, or IndexedDB. On reload, the cache hydrates from storage for offline resilience.

818. Explain React Query with websockets.

   **Answer:** Websockets push real-time updates. The handler calls `queryClient.setQueryData()` or `queryClient.invalidateQueries()` to synchronize the cache with server-pushed events.

819. How does offline mutation replay work?

   **Answer:** Offline mutations queue in the mutation cache (`networkMode: 'offlineFirst'`). When back online, they replay in order via the `onlineManager`, and the cache updates propagate accordingly.

820. Explain cache garbage collection tuning.

   **Answer:** `cacheTime` (default 5 minutes) controls how long inactive queries remain in cache. Tuning higher keeps data longer (useful for back-navigation), lower reduces memory. Set per query based on data volatility.

821. What are query waterfalls?

   **Answer:** Query waterfalls happen when dependent queries wait for parent data before fetching (e.g., fetch user, then fetch posts by user). Mitigate with parallel queries, prefetching, or suspense.

822. Explain request collapsing.

   **Answer:** Request collapsing combines multiple identical concurrent requests into one network call. All subscribers share the same promise, reducing server load and network bandwidth.

823. How do suspense queries work?

   **Answer:** Suspense queries (`useSuspenseQuery`) throw a promise during rendering, caught by React Suspense boundaries. This allows declarative loading states without manual `isLoading` checks.

824. Explain polling tradeoffs.

   **Answer:** Polling (`refetchInterval`) provides near-real-time updates but increases server load and network usage. Use low intervals (e.g., 30s) for non-critical data and prefer websockets for real-time needs.

825. What are query boundary patterns?

   **Answer:** Query boundaries define which component tree scope a query belongs to. Prefetching in route loaders, colocating queries in feature components, and shared queries in layout components are common patterns.

826. Explain infinite scrolling optimization.

   **Answer:** Infinite scrolling uses `useInfiniteQuery` with `getNextPageParam`. Optimizations include prefetching the next page, virtualized rendering, keeping only visible pages in cache, and debouncing scroll handlers.

827. How does pagination caching work?

   **Answer:** Pagination caching stores each page as separate data within the same query key (e.g., `['posts', { page: 1 }]`). Navigated pages remain cached, enabling instant back-navigation without refetching.

828. Explain enterprise server-state management.

   **Answer:** Enterprise patterns include centralized query factories, stale-while-revalidate defaults, prefetching in routers, optimistic updates with rollbacks, cache persistence for offline, and structured error handling.

829. What are anti-patterns in TanStack Query?

   **Answer:** Anti-patterns include disabling stale refetching entirely, treating it as a global state manager, storing non-server state in the cache, ignoring error handling, and excessive query invalidation.

830. How do you profile query-heavy apps?

   **Answer:** Profile with TanStack Query Devtools, React DevTools profiler, network tab analysis, `placeholderData` waterfall detection, custom `onSettled` logging, and monitoring query count, refetch frequency, and cache hit rates.
