## 49. TanStack Query Expert Topics (1306–1330)

1306. How does stale data reconciliation work?
   TanStack Query marks cached data as stale after the `staleTime` expires. On stale reads, it returns the cached data immediately (for instant UI) while triggering a background refetch to refresh the cache when the response arrives.

1307. Explain background synchronization strategies.
   Background sync strategies include `refetchInterval` (polling), `refetchOnWindowFocus` (refetch on tab focus), `refetchOnReconnect` (after network recovery), and `refetchOnMount` (on component remount). Each balances freshness with network usage.

1308. What are query consistency guarantees?
   Queries guarantee that all observers of a query key see the same data object (by reference) during the same render pass. Updates are atomic—observers switch from stale to fresh data synchronously when the refetch completes.

1309. Explain query observer internals.
   Query observers subscribe to a query instance and receive notifications when that query's state changes (loading, error, success). Each observer maintains its own render lifecycle, batching updates via `setState` to avoid cascading re-renders.

1310. How do queries deduplicate network requests?
   Multiple components using the same query key share a single query instance. Only one network request fires, and the response is broadcast to all subscribers. Deduplication works across the component tree, not just within a page.

1311. Explain optimistic rollback flows.
   Optimistic updates execute the mutation on the client immediately, then on server confirmation either keep the optimistic value or roll back to the server's actual response. On failure, the cache restores the pre-mutation snapshot.

1312. What are mutation queue architectures?
   Mutation queues serialize mutations that must execute in order (e.g., banking transactions). TanStack Query's `useMutation` can be composed with a custom queue that enforces FIFO order and blocks until the prior mutation settles.

1313. Explain query synchronization across tabs.
   Cross-tab synchronization uses `focusManager` events and `broadcastChannel` or `localStorage` events. When one tab refetches data, other tabs detect the cache change via storage events and update their observers.

1314. How do persistent caches survive reloads?
   `persistQueryClient` middleware serializes the query cache to `localStorage`, IndexedDB, or an async storage provider. On reload, the cache is hydrated before the first render, showing previous data instantly.

1315. Explain cache eviction heuristics.
   Cache eviction removes entries based on `gcTime` (formerly `cacheTime`) after all observers unsubscribe. The default 5-minute window keeps data available for re-mounts but prevents unbounded memory growth.

1316. What are query hydration race conditions?
   Hydration race conditions occur when dehydrated server data conflicts with client-side refetches. TanStack Query resolves this by comparing timestamps: dehydrated data is applied only if it's newer than the current cache.

1317. Explain stale closure problems in mutations.
   Stale closures in `onMutate`, `onSuccess`, and `onError` capture outdated state from the render scope. Using refs or `queryClient.getQueryData` inside callbacks ensures access to the latest state.

1318. How does React Query reduce server load?
   React Query reduces server load through caching (avoiding redundant requests), deduplication (single request per key), stale-while-revalidate (serving cached data), and window focus refetch throttling.

1319. Explain cache persistence encryption.
   Cache persistence encryption encodes sensitive query data before writing to storage using the Web Crypto API. On hydration, the encrypted data is decrypted, ensuring sensitive data doesn't persist in plaintext.

1320. What are offline-first synchronization strategies?
   Offline-first strategies queue mutations while offline, replay them in order when connectivity returns, and reconcile any server conflicts using version vectors or last-write-wins semantics.

1321. Explain realtime cache updates.
   Realtime updates use `queryClient.setQueryData` to push data from websocket messages into the cache, triggering reactive UI updates without refetching. This enables instant UIs for collaborative features.

1322. How do websocket-driven queries work?
   Websocket-driven queries subscribe to a server-side channel that pushes updates for a specific query key. TanStack Query's `queryClient.invalidateQueries` or the subscription callback caches the pushed data, re-rendering observers.

1323. Explain cache fragmentation.
   Cache fragmentation happens when similar data is stored under many unique query keys with overlapping information, increasing memory usage and reducing cache efficiency. Normalizing query keys and using `select` prevents fragmentation.

1324. What are query retry storms?
   Retry storms occur when many queries fail simultaneously and retry on the same schedule, amplifying server load. TanStack Query mitigates this with exponential backoff, jitter, configurable retry counts, and circuit breaker patterns.

1325. Explain distributed frontend state synchronization.
   Distributed frontend state sync uses a central coordination layer (like a websocket server) that broadcasts state mutations to all connected clients. TanStack Query's cache updates serve as the state reconciliation mechanism.

1326. How do large applications organize query keys?
   Large applications organize query keys hierarchically as tuples: `['entities', 'users', userId, 'posts']`. Organizations prefix keys with a domain name to avoid collisions and use factory functions to generate consistent key structures.

1327. Explain query invalidation anti-patterns.
   Invalidation anti-patterns include invalidating everything on any mutation (causing cascading refetches), not invalidating related queries (stale data), and calling `invalidateQueries` without `refetchType: 'active'` (over-refetching).

1328. What are polling scalability concerns?
   Polling creates constant server load proportional to open browser tabs × polling interval. Excessive polling wastes bandwidth and server resources; websocket-based pushes scale better for realtime data.

1329. Explain frontend data consistency models.
   Frontend data consistency models range from stale-while-revalidate (TanStack Query default) to strongly consistent (waiting for fresh data before rendering). The choice depends on data criticality and user experience requirements.

1330. How do enterprise apps manage server state?
   Enterprise apps manage server state with TanStack Query as the central orchestration layer, combining it with optimistic updates for mutations, websocket subscriptions for realtime data, and persistent caches for offline resilience.
