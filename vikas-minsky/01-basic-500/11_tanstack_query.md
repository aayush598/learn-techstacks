## 11. React Query / TanStack Query (306–330)

306. What is TanStack Query?
     TanStack Query (formerly React Query) is a library for managing server state in React applications. It handles caching, background refetching, pagination, optimistic updates, and synchronization between server and client state with minimal configuration.

307. Difference between server state and client state?
     Server state is data stored on the server (database) that requires async fetching and can become stale. Client state is UI-specific data (form inputs, modals, theme) that exists only in the browser. TanStack Query specializes in server state management.

308. Explain query keys.
     Query keys are unique identifiers for cached data, typically arrays of strings and objects: `['users', userId]`. Keys enable caching, deduplication, invalidation, and refetching — changing a key creates a new cache entry.

309. What is query invalidation?
     Query invalidation (`queryClient.invalidateQueries(['users'])`) marks cached data as stale, triggering automatic refetching when components using that query render. It's used after mutations to refresh related data without manual reload.

310. Explain stale time vs cache time.
     Stale time (`staleTime`) determines how long data is considered fresh before refetching is needed. Cache time (`gcTime` or `cacheTime`) determines how long inactive data remains in memory before garbage collection. Stale data can still be shown from cache.

311. How do mutations work?
     Mutations (`useMutation`) handle create, update, and delete operations. They trigger side effects on success/error via `onMutate`, `onSuccess`, `onError`, and `onSettled` callbacks, and typically invalidate related queries on success.

312. Explain optimistic updates.
     Optimistic updates update the UI immediately before the server confirms, assuming success. On mutation error, the UI rolls back to the previous state. Implemented via `onMutate` (update cache) and `onError` (rollback) callbacks.

313. What are infinite queries?
     `useInfiniteQuery` handles paginated or cursor-based data loading with `getNextPageParam` and `getPreviousPageParam`. It accumulates pages and provides `fetchNextPage`/`fetchPreviousPage` for manual or intersection-observer-driven loading.

314. Explain retries in React Query.
     Retries automatically re-fetch failed queries with exponential backoff. Configured via `retry` (number of retries or boolean) and `retryDelay` (fixed or function). Default is 3 retries with doubling delay.

315. How does background refetching work?
     Background refetching automatically re-fetches stale data when components mount, the window regains focus, or the network reconnects. It provides updated data without user interaction, controlled by `refetchOnMount`, `refetchOnWindowFocus`, `refetchOnReconnect` options.

316. Explain query deduplication.
     Query deduplication ensures that identical queries (same key) only make one network request regardless of how many components use them. Other components reuse the in-flight promise, preventing redundant API calls.

317. What are dependent queries?
     Dependent queries wait for prerequisite data before executing. Achieved by passing `enabled: !!userId` — the query only runs when the dependency is truthy, enabling sequential data fetching with type safety.

318. Explain prefetching.
     Prefetching (`queryClient.prefetchQuery`) fetches data before it's needed and stores it in the cache. Used for anticipated user actions like hovering over a link, resulting in instant data display when the component mounts.

319. How do you persist query caches?
     Query caches persist via `@tanstack/query-persist-client-core` with adapters for localStorage, IndexedDB, or custom storage. Persistence enables offline support and preserves cache across page reloads.

320. Explain pagination handling.
     Pagination is handled with `keepPreviousData: true` which preserves the previous page's data while loading the next page, preventing layout shifts. Queries use page numbers or cursors in the key: `['users', { page }]`.

321. What are hydration and dehydration?
     Dehydration serializes the query cache into a string, and hydration restores it on the client. Used with SSR/SSG to pass server-fetched data to the client, preventing re-fetching on initial render.

322. Explain SSR integration.
     SSR integration prefetches queries on the server using `queryClient.prefetchQuery`, dehydrates the cache, and hydrates it client-side. This ensures pages are fully rendered on the server with data, improving SEO and initial load time.

323. How does error handling work?
     Errors are exposed via `isError`, `error`, and `failureCount` from query hooks. Global error handling uses `QueryClient`'s `defaultOptions.queries.onError`. Mutations have separate `onError` callbacks for fine-grained handling.

324. Explain devtools usage.
     `@tanstack/react-query-devtools` provides a floating panel showing query cache state, active queries, mutation history, and the ability to refetch, invalidate, or remove cached data manually for debugging.

325. What are mutation side effects?
     Mutation side effects are callbacks that run during the mutation lifecycle: `onMutate` (before mutation, for optimistic updates), `onSuccess` (after success), `onError` (after failure), and `onSettled` (after either success or failure).

326. Explain cache synchronization.
     Cache synchronization keeps client state consistent with server state through background refetching, query invalidation after mutations, WebSocket subscriptions for real-time updates, and manual refetch triggers when data is known to change.

327. How does garbage collection work?
     Garbage collection (controlled by `gcTime`/`cacheTime`) removes inactive query data from memory after the specified duration. Inactive queries become eligible after all observers unmount, freeing resources for new data.

328. Explain offline support.
     Offline support allows queries to serve cached data when the network is unavailable. `networkMode: 'offlineFirst'` returns cached data during offline and refetches when online. Mutations can be paused and retried on reconnection.

329. What are query observers?
     Query observers are internal objects that subscribe to query state changes. Each `useQuery` call creates an observer — when multiple observers exist for the same key, they share the same query and deduplicate requests.

330. How do you optimize API-heavy apps?
     Optimize by: using proper `staleTime` to reduce refetches, prefetching anticipated data, deduplicating queries with shared keys, paginating large lists, implementing optimistic updates, and enabling `keepPreviousData` for smooth pagination.
