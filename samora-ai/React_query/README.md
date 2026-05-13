# React Query Interview Questions and Answers

## Q1: What is React Query?
**A:** React Query (now TanStack Query) is a powerful data synchronization library for React applications. It handles fetching, caching, updating, and managing server state with minimal boilerplate. It provides hooks like useQuery and useMutation for declarative data management.

## Q2: What problem does React Query solve?
**A:** React Query solves the problem of managing server state in React applications. It eliminates the need for manual state management (Redux, Context) for API data, handles caching, background refetching, pagination, optimistic updates, error handling, and loading states automatically.

## Q3: What is the difference between server state and client state?
**A:** Server state is data stored on a remote server (e.g., database records, API responses) that is asynchronous and can become stale. Client state is UI-specific data (e.g., form inputs, modal open/close) that exists only in the browser. React Query is designed for server state management.

## Q4: What is the useQuery hook?
**A:** useQuery is a React hook that fetches, caches, and synchronizes data from a server. It accepts a unique query key and an async function that returns data. It returns status, data, error, and utility flags like isLoading, isError, isFetching, and refetch.

## Q5: What is the useMutation hook?
**A:** useMutation is a React hook for creating, updating, or deleting data (mutations). Unlike useQuery, it is not automatically retried. It exposes mutate/mutateAsync functions and callbacks like onSuccess, onError, onSettled for handling side effects after mutations.

## Q6: What are query keys and why are they important?
**A:** Query keys are unique identifiers (strings or arrays) that React Query uses to cache and track queries. When a key changes, the query is automatically refetched. Keys are also used for manual cache invalidation (invalidateQueries) and cache updates. They enable automatic deduplication.

## Q7: What is query deduplication?
**A:** Query deduplication means that if multiple components use the same query key simultaneously, React Query makes only one network request and shares the result across all subscribers. This prevents redundant API calls and improves performance.

## Q8: What is stale time (staleTime)?
**A:** staleTime is the duration (in milliseconds) that data is considered fresh. Within this period, React Query returns cached data without refetching. After staleTime expires, data becomes stale and will be refetched on next access or when specified triggers occur.

## Q9: What is cache time (gcTime or cacheTime)?
**A:** cacheTime (gcTime in v5) determines how long inactive query data is kept in memory before garbage collection. Even after all observers unmount, the data remains cached for this duration, allowing instant display if the user navigates back. Default is 5 minutes.

## Q10: What is the difference between staleTime and cacheTime?
**A:** staleTime controls when data is considered outdated and needs refetching. cacheTime controls how long unused cached data remains in memory before being garbage collected. staleTime is about freshness; cacheTime is about memory retention.

## Q11: What is background refetching?
**A:** Background refetching automatically triggers a new fetch when stale data is accessed, showing cached data immediately while updating in the background. This provides instant UI response while keeping data fresh. It is managed by refetchOnMount, refetchOnWindowFocus, and refetchInterval.

## Q12: What is refetchOnWindowFocus?
**A:** refetchOnWindowFocus is a React Query feature that automatically refetches stale queries when the browser tab regains focus. This ensures the UI shows fresh data when users return to the tab. It can be configured globally or per-query and defaults to true.

## Q13: What is the QueryClient and what does it do?
**A:** QueryClient is the central hub of React Query. It manages the query cache, provides methods for invalidating queries (invalidateQueries), pre-fetching, setting default options, clearing cache (clear), and configuring the global behavior of queries and mutations.

## Q14: What is QueryClientProvider?
**A:** QueryClientProvider is a React context provider that makes the QueryClient available to all components in the tree. It wraps the application and receives a client prop. Without it, useQuery and useMutation hooks will throw an error.

## Q15: What is the purpose of queryClient.invalidateQueries?
**A:** invalidateQueries marks queries as stale, triggering them to be refetched when next accessed. It accepts a query key or predicate function to selectively invalidate specific queries. It is commonly called after successful mutations to refresh related data.

## Q16: What is optimistic update?
**A:** Optimistic update is a pattern where the UI immediately reflects the expected mutation result before the server confirms it. If the server request fails, the UI is rolled back. This provides a snappy user experience. React Query's onMutate callback handles this with cache manipulation.

## Q17: How do you implement optimistic updates with useMutation?
**A:** In useMutation, the onMutate callback: (1) cancels outgoing queries to prevent stale data overwrite, (2) saves current cache snapshot for rollback, (3) updates the cache optimistically. onError reverts using the snapshot, and onSettled invalidates queries to ensure server consistency.

## Q18: What is the difference between isLoading and isFetching?
**A:** isLoading is true when the query has no data yet and is currently fetching (initial load). isFetching is true whenever any fetch is in progress, including background refetches when cached data exists. isLoading implies isFetching, but the reverse is not true.

## Q19: What is the enabled option in useQuery?
**A:** The enabled option controls whether a query automatically executes. When set to false, the query does not fetch until manually triggered via refetch() or the enabled condition becomes true. It is useful for dependent queries or conditional fetching.

## Q20: What are dependent queries?
**A:** Dependent queries are queries that only execute after another query completes. They use the enabled option set to a boolean that depends on the previous query's data. This creates a chain where data from one query is needed as input for another.

## Q21: What is parallel query execution?
**A:** Parallel queries execute multiple independent queries simultaneously. React Query supports this natively — simply call multiple useQuery hooks or use useQueries hook for dynamic parallel queries. Parallel queries minimize total loading time by fetching concurrently.

## Q22: What is the useQueries hook?
**A:** useQueries is a React Query hook for executing multiple parallel queries dynamically. It accepts an array of query option objects and returns an array of query results. It is ideal for rendering lists where each item requires its own data fetch.

## Q23: What is query cancellation?
**A:** Query cancellation aborts an in-flight request when the component unmounts or a new query replaces it. React Query supports this via AbortController and the AbortSignal passed to the query function. It prevents race conditions and saves bandwidth.

## Q24: How does React Query handle error boundaries?
**A:** React Query integrates with React Error Boundaries by exposing the useQuery error through a thrown promise. When using suspense mode, errors are thrown and caught by an Error Boundary. The useErrorBoundary option (useErrorBoundary or throwOnError in v5) controls this behavior.

## Q25: What is suspense mode in React Query?
**A:** Suspense mode uses React's Suspense component with React Query. When enabled, useQuery throws a promise during loading, which Suspense catches and shows a fallback UI. This simplifies loading state management by using a declarative approach.

## Q26: What are selectors in useQuery?
**A:** The select option in useQuery transforms or selects a portion of the query data. It runs after data is fetched and only triggers re-renders if the selected value changes (referential equality). Selectors optimize performance by preventing unnecessary renders.

## Q27: What is the keepPreviousData option?
**A:** keepPreviousData (placeholderData: keepPreviousData in v5) preserves the previous query's data while a new query is loading. This provides a smooth transition for paginated or filtered data, showing the old data as a placeholder until new data arrives.

## Q28: What is pagination with React Query?
**A:** Pagination with React Query typically uses query keys that include the page number. The keepPreviousData option prevents flash of loading state between pages. Cursor-based pagination prepends/updates the cache with new pages while maintaining previous data.

## Q29: How does infinite scrolling work with useInfiniteQuery?
**A:** useInfiniteQuery handles infinite scrolling by: (1) using getNextPageParam to extract the next cursor/offset from the response, (2) fetchNextPage to load more data, (3) flattening all pages into a single list via data.pages. It auto-fetches the next page when configured.

## Q30: What is useInfiniteQuery?
**A:** useInfiniteQuery is a React Query hook for paginated or infinite-scroll data. It extends useQuery with page-based fetching, providing getNextPageParam, fetchNextPage, hasNextPage, and isFetchingNextPage. It accumulates pages as the user scrolls.

## Q31: How does getNextPageParam work?
**A:** getNextPageParam is a function that receives the last page's data and all pages. It extracts the next cursor, offset, or page number. Returning undefined signals that there are no more pages. It determines whether hasNextPage is true or false.

## Q32: What is the difference between fetchNextPage and refetch?
**A:** fetchNextPage loads the next page of paginated data without invalidating existing data. refetch re-fetches all pages from scratch, starting from page 1. Use fetchNextPage for scrolling, refetch for full data refresh.

## Q33: How do you handle mutation side effects?
**A:** Mutation side effects are handled via callbacks: onMutate (before mutation), onSuccess (after success), onError (after error), onSettled (regardless of outcome). Common side effects include invalidating queries, showing toast notifications, and updating local state.

## Q34: What is the mutation key used for?
**A:** Mutation keys identify mutations for devtools and cache management. Unlike query keys, mutation keys do not trigger automatic behavior. They are used for organization, debugging with React Query Devtools, and manual mutation manipulation.

## Q35: How do you handle file uploads with useMutation?
**A:** File uploads use mutationFn with FormData. The mutation receives the File/Blob as a variable. Progress tracking requires integrating with axios (onUploadProgress) or XMLHttpRequest. React Query does not natively track upload progress — use external helpers or subscribe to progress events.

## Q36: What is the QueryObserver?
**A:** QueryObserver is an internal class that observes a query and notifies subscribers (components) of changes. Each useQuery call creates a QueryObserver. It handles deduplication, batching updates, and provides the reactive state the component renders.

## Q37: How does React Query handle caching strategies?
**A:** React Query uses an LRU (Least Recently Used) cache. Queries are stored in memory keyed by queryKey. staleTime determines freshness, cacheTime determines retention. The cache can be persisted via persisters (e.g., react-query-persist-client) for offline support.

## Q38: What is the default staleTime in React Query?
**A:** The default staleTime is 0 milliseconds, meaning data is considered stale immediately after fetching. This causes background refetches on mount, window focus, and network reconnection. Override staleTime globally or per-query for less aggressive refetching.

## Q39: What is the default cacheTime (gcTime) in React Query v5?
**A:** The default cacheTime (gcTime in v5) is 5 minutes (300,000 ms). Inactive query data is removed from memory after this duration. Adjust this for frequently revisited data (increase) or memory-constrained environments (decrease).

## Q40: How does React Query handle retries on failure?
**A:** React Query automatically retries failed queries up to 3 times by default with exponential backoff (1s, 2s, 4s, etc.). Retry count and delay can be customized via retry (number, boolean, or function) and retryDelay options globally or per-query.

## Q41: What is exponential backoff and how does React Query implement it?
**A:** Exponential backoff increases the delay between retries exponentially (e.g., attempt 1: 1s, attempt 2: 2s, attempt 3: 4s). React Query implements this by default with retryDelay: attemptIndex => Math.min(1000 * 2 ** (attemptIndex - 1), 30000). Jitter can be added for distributed systems.

## Q42: What is the networkMode option?
**A:** networkMode controls how React Query behaves with network connectivity. Options: online (default — pauses queries when offline), always (never pauses), and offlineFirst (pauses but attempts when online). It affects refetchOnReconnect and query retry behavior.

## Q43: How do you prefetch data in React Query?
**A:** Prefetching uses queryClient.prefetchQuery which fetches data and stores it in the cache without rendering. This is ideal for anticipating user navigation (e.g., hovering over a link). Prefetched data is instantly available when the component mounts.

## Q44: What is queryClient.setQueryData?
**A:** setQueryData synchronously sets query data in the cache without fetching. It is used for: optimistic updates, seeding the cache with initial data, or updating cached data from outside a query component. It accepts a query key and updater function/value.

## Q45: What is queryClient.getQueryData?
**A:** getQueryData synchronously reads cached data for a given query key. It returns undefined if the query does not exist in cache. It is used for reading cache outside of React components (e.g., in event handlers, thunks) without triggering re-renders.

## Q46: How do you reset a query to its initial state?
**A:** Query reset uses queryClient.resetQueries which clears the query's cached data and resets error/loading states. The query will refetch on next access. It is different from invalidateQueries which only marks as stale.

## Q47: What is the difference between removeQueries and resetQueries?
**A:** removeQueries completely deletes query data from cache, removing the query entry entirely. resetQueries clears the data but keeps the query entry, resetting it to its initial state (empty data, no error). removeQueries is more aggressive.

## Q48: How do you handle offline support with React Query?
**A:** Offline support uses: (1) networkMode: 'offlineFirst' to queue mutations, (2) QueryClient's defaultOptions to set staleTime, (3) persisters (e.g., react-query-persist-client with IndexedDB) to persist cache to localStorage/IndexedDB, and (4) refetchOnReconnect to auto-refresh when back online.

## Q49: What is the persistQueryClient plugin?
**A:** persistQueryClient persists the React Query cache to a storage provider (localStorage, IndexedDB, AsyncStorage). On app restart, cached data is restored, providing a seamless offline experience. It works with a persister (createSyncStoragePersister or createAsyncStoragePersister).

## Q50: How do you cancel a query manually?
**A:** Manual cancellation uses the AbortSignal passed to the query function. Calling queryClient.cancelQueries with the query key aborts the associated fetch via AbortController. The query function must support AbortSignal (pass it to fetch/axios).

## Q51: What is structural sharing?
**A:** Structural sharing is an optimization that preserves referential equality for unchanged portions of query data. React Query deep-comparison caches and reuses existing object references for unchanged sub-trees. This prevents unnecessary re-renders when data is refetched but unchanged.

## Q52: How does React Query compare to Redux Toolkit Query (RTK Query)?
**A:** Both solve server state management. React Query is framework-agnostic (works with React, Vue, Svelte), has richer caching features, better devtools, and more flexible configuration. RTK Query is tightly integrated with Redux Toolkit, making it natural for Redux-heavy projects.

## Q53: How does React Query compare to SWR?
**A:** SWR (stale-while-revalidate) by Vercel is simpler with fewer features. React Query offers more: mutation management, infinite queries, parallel queries, retry customization, cache persistence, window focus refetching, and developer tools. React Query is generally more feature-rich.

## Q54: What is the React Query Devtools?
**A:** React Query Devtools is a visual debugging panel that shows all queries and mutations in real-time. It displays: query status, data preview, stale time, cache time, last updated timestamp, refetch history, and allows manual cache manipulation (invalidate, refetch, remove).

## Q55: How do you configure default options globally?
**A:** Global defaults are set when creating the QueryClient:
```
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30000, retry: 2 },
    mutations: { retry: 1 }
  }
})
```
These apply to all queries/mutations unless overridden per-hook.

## Q56: What is the QueryCache?
**A:** QueryCache is the underlying cache storage for all queries. QueryClient contains a QueryCache instance. It manages query entries, handles garbage collection, and emits events for the devtools and subscribers. It is accessible via queryClient.getQueryCache().

## Q57: What is the MutationCache?
**A:** MutationCache stores mutation state and provides event listeners for devtools. Similar to QueryCache, it manages active, done, and failed mutations. Custom MutationCache instances can be passed to QueryClient for advanced use cases.

## Q58: How do you handle authentication tokens with React Query?
**A:** Authentication tokens are typically handled with: (1) an interceptor in the query function that attaches tokens to requests, (2) queryClient.setDefaultOptions for base configurations, (3) automatic refetch on 401 errors by invalidating queries, or (4) using axios interceptors with token refresh logic.

## Q59: What is the onError callback and how is it used?
**A:** onError is a callback that fires when a query or mutation fails. It receives the error object. It is used for: showing error toasts, logging, analytics, and triggering fallback actions. In queries, it can be set globally or per-hook.

## Q60: What is the onSuccess callback?
**A:** onSuccess fires when a query or mutation succeeds. For queries, it is useful for caching derived state or analytics. For mutations, it typically invalidates related queries or shows success notifications. Multiple callbacks can be chained.

## Q61: What is the onSettled callback?
**A:** onSettled fires after both success and failure outcomes. It receives data or error as arguments. It is commonly used for: stopping loading spinners, analytics tracking, or cleanup regardless of mutation/query outcome.

## Q62: How do you type React Query with TypeScript?
**A:** React Query is fully typed. Use generics: useQuery<TData, TError>(key, fn). TData is the data type, TError is the error type. QueryClient and hooks infer types from the query function return type. Use @tanstack/react-query types package.

## Q63: What are typed query keys?
**A:** Typed query keys create a type-safe mapping between query key structures and their data types. Libraries like @tanstack/query-key-factory provide factory functions that generate typed keys, ensuring consistent key usage and type inference across the application.

## Q64: How do you handle race conditions with React Query?
**A:** React Query handles race conditions by: (1) query deduplication — only one request per key, (2) query cancellation via AbortController, (3) automatic stale data overwrite prevention with structural sharing, (4) request deduplication during rapid key changes.

## Q65: What is the useIsFetching hook?
**A:** useIsFetching returns the number of queries currently fetching (including background refetches). It can accept an optional query key filter. It is useful for showing a global loading indicator (e.g., top progress bar) across all active fetches.

## Q66: What is the useIsMutating hook?
**A:** useIsMutating returns the number of active mutations. It can filter by mutation key. It is useful for global loading states during mutations (e.g., disabling form submit buttons, showing overlay spinners).

## Q67: How do you test React Query components?
**A:** Testing uses: (1) QueryClientProvider with a fresh QueryClient in test setup, (2) queryClient.clear() between tests, (3) mocking query functions, (4) using react-query testing utilities (@testing-library/react), (5) awaiting waitFor() for async assertions, (6) testing error/loading states.

## Q68: What is the QueryClientProvider's context system?
**A:** QueryClientProvider uses React Context to pass the QueryClient down. Multiple providers can be nested, each with its own QueryClient and cache. This enables micro-frontend patterns or isolated sections with independent caching.

## Q69: What are placeholderData and initialData in useQuery?
**A:** placeholderData is data shown while the query is loading (e.g., a skeleton). It is not cached. initialData is data used to initialize the cache immediately, avoiding a loading state. InitialData is cached; placeholderData is not.

## Q70: How does React Query handle SSR (Server-Side Rendering)?
**A:** SSR support includes: (1) prefetchQuery on the server within the queryClient, (2) dehydrate to serialize the cache as HTML, (3) Hydrate component on the client to rehydrate the cache, (4) prevent refetching on client mount using staleTime: Infinity.

## Q71: What is hydration in React Query?
**A:** Hydration is the process of transferring server-prefetched query data to the client. dehydrate serializes the query cache to a JSON object. The Hydrate component (or queryClient.mount) restores this cache on the client, preventing redundant initial fetches.

## Q72: How do you use React Query with Next.js?
**A:** Next.js integration uses: (1) getStaticProps/getServerSideProps to prefetch data with queryClient, (2) dehydrate the cache, (3) pass dehydratedState as props, (4) wrap the app with HydrationBoundary (in v5) or Hydrate (v4), (5) optionally use staleTime to control revalidation.

## Q73: What is the HydrationBoundary component?
**A:** HydrationBoundary (v5) wraps the application to rehydrate the query cache from server-dehydrated state. It accepts a state prop from dehydrate(). It ensures the client cache matches server state without making initial network requests.

## Q74: How do you implement optimistic updates with list data?
**A:** For list data: (1) in onMutate, cancel list queries, snapshot the cache, update the list optimistically, (2) in onError, rollback to snapshot, (3) in onSettled, invalidate the list query to refetch from server. Ensure query keys match for cache manipulation.

## Q75: What is serialization of query keys?
**A:** Query keys are serialized using deterministic JSON.stringify. Arrays are hashed into stable strings. Object property order is normalized. This ensures the same key always maps to the same cache entry regardless of creation context.

## Q76: How do you handle optimistic deletion?
**A:** Optimistic deletion: (1) onMutate removes the item from the cached list using setQueryData with a filter, (2) onError restores the item in the correct position using the cache snapshot, (3) onSettled invalidates the list. Account for pagination by checking page boundaries.

## Q77: What is the behavior of refetchInterval?
**A:** refetchInterval automatically refetches the query at a fixed interval (in milliseconds), like polling. Set to false or undefined to disable. Combined with refetchIntervalInBackground, polling continues even when the tab is unfocused.

## Q78: How do you stop refetchInterval when a condition is met?
**A:** Pass a function to refetchInterval returning the interval or false. For example: refetchInterval: (query) => query.state.data?.isComplete ? false : 3000. This stops polling when the condition (e.g., job completion) is satisfied.

## Q79: What is refetchIntervalInBackground?
**A:** refetchIntervalInBackground (default: false) controls whether refetchInterval continues polling when the browser tab is not focused. When false, polling pauses when the tab is backgrounded, reducing unnecessary network usage.

## Q80: How do you handle WebSocket updates with React Query?
**A:** WebSocket integration: (1) connect WebSocket in a useEffect, (2) on receiving updates, call queryClient.setQueryData or queryClient.invalidateQueries, (3) optionally use queryClient.cancelQueries to abort stale fetches, (4) clean up the WebSocket connection on unmount.

## Q81: What is the QueryFilters API?
**A:** QueryFilters allows selecting queries by criteria: type ('active', 'inactive', 'all'), exact (exact key match), predicate (custom filter function), and stale status. Used with invalidateQueries, resetQueries, cancelQueries, and removeQueries for targeted cache operations.

## Q82: How do you use the notifyOnChangeProps option?
**A:** notifyOnChangeProps specifies which properties of the query result trigger re-renders. Set to ['data', 'error'] to only re-render when data or error changes, ignoring status transitions. This optimizes performance for components that only need specific properties.

## Q83: What is the difference between queryClient.invalidateQueries and queryClient.refetchQueries?
**A:** invalidateQueries marks queries as stale, causing them to refetch when next observed (if mounted, they refetch immediately). refetchQueries immediately forces a refetch regardless of staleness. invalidateQueries is more efficient as it batches refetches.

## Q84: How do you implement a search-as-you-type feature with React Query?
**A:** Use useQuery with the search term as part of the query key. Debounce the input (300ms) before updating the search state to avoid excessive requests. The enabled option prevents fetching until the search term reaches minimum length. useQuery naturally handles race conditions.

## Q85: What is the behavior when a query key changes?
**A:** When a query key changes, React Query: (1) checks if cached data exists for the new key, (2) if cached and fresh, returns cached data, (3) if cached but stale, returns cached data and refetches in background, (4) if not cached, fetches from scratch and shows loading state.

## Q86: How do you handle dependent mutations?
**A:** Dependent mutations chain mutations using mutateAsync with await. The second mutation runs in onSuccess of the first. Alternatively, use Promise.all for parallel independent mutations. For complex workflows, callbacks or custom hooks orchestrate the sequence.

## Q87: What is the difference between mutate and mutateAsync?
**A:** mutate is fire-and-forget — it returns void and uses callbacks for side effects. mutateAsync returns a Promise that resolves with the mutation result or rejects with an error. Use mutateAsync when you need to await the result (e.g., in form handlers with try/catch).

## Q88: How do you update query data from a mutation response?
**A:** Use queryClient.setQueryData in onSuccess with the mutation response data. For example, after creating an item, update the list cache with the new item. This avoids a full list refetch. Match the query key of the cached data you want to update.

## Q89: What is stale-while-revalidate caching strategy?
**A:** The stale-while-revalidate strategy serves cached (stale) data immediately while triggering a background refetch. React Query implements this: on mount, if stale, show cached data and refetch. This provides instant responses while keeping data current.

## Q90: How do you handle pagination with cursor-based pagination?
**A:** useInfiniteQuery handles cursor-based pagination. getNextPageParam extracts the cursor from the response. The cursor becomes part of the query function's pageParam argument. Each page is stored separately in data.pages. hasNextPage controls the "load more" visibility.

## Q91: How does React Query handle query garbage collection?
**A:** When all observers of a query unmount, a timer (cacheTime/gcTime) starts. If the timer expires before a new observer subscribes, the query data is garbage collected from the cache. This prevents memory leaks from unused cached data.

## Q92: What is the QueryClient's default query options merging strategy?
**A:** Options are merged from: (1) global defaults (via QueryClient defaultOptions), (2) query-specific defaults (via defaults object), (3) hook-level options. More specific options override less specific ones using a shallow merge for most properties.

## Q93: How do you handle race conditions with rapid query key changes?
**A:** React Query handles rapid key changes by: (1) aborting the previous in-flight request via AbortController, (2) starting a new fetch for the new key, (3) only processing the response for the latest key. This ensures UI consistency and prevents stale data display.

## Q94: What is the difference between useQuery and useSuspenseQuery?
**A:** useSuspenseQuery (v5) integrates with React Suspense, throwing a promise during loading instead of returning isLoading state. It simplifies component code by removing manual loading checks. However, it requires a Suspense boundary and ErrorBoundary.

## Q95: How do you handle form submissions with useMutation?
**A:** Form submissions with useMutation: (1) call mutate with form data, (2) disable submit button while mutation is pending (isPending), (3) onSuccess: reset form, show success, invalidate list, (4) onError: show error message, keep form data for correction, (5) optionally use optimistic updates for instant feedback.

## Q96: What is the global cache event system?
**A:** React Query emits events on the QueryCache and MutationCache for queries and mutations (onAdded, onRemoved, onUpdated, onSuccess, onError, etc.). These can be used for persisting cache, analytics, logging, or custom cache behaviors.

## Q97: How do you implement a retry with exponential backoff and jitter?
**A:** Custom retryDelay function: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000) + Math.random() * 1000. Jitter prevents thundering herd problems where many clients retry simultaneously. Set via query options: retry: 3, retryDelay: customFunction.

## Q98: What are the migration considerations from React Query v3 to v5?
**A:** Key changes: (1) package renamed from react-query to @tanstack/react-query, (2) cacheTime renamed to gcTime, (3) keepPreviousData deprecated in favor of placeholderData: keepPreviousData, (4) useErrorBoundary renamed to throwOnError, (5) QueryCache and MutationCache restructured.

## Q99: How do you optimize React Query for performance?
**A:** Optimizations: (1) set staleTime > 0 to reduce refetches, (2) use select to extract only needed data, (3) set notifyOnChangeProps to limit re-renders, (4) use structural sharing (enabled by default), (5) deduplicate queries, (6) prefetch anticipated data, (7) use larger gcTime for frequently revisited views.

## Q100: Design a real-time dashboard with React Query for a stock trading application. What considerations would you have?
**A:** Design considerations: (1) use refetchInterval (1-5s) for price polling with staleTime: 0 for fresh data, (2) WebSocket integration for critical price updates via setQueryData, (3) useInfiniteQuery for historical data with pagination, (4) optimistic updates for trade submissions with rollback, (5) cache invalidation on successful trades to refresh portfolio, (6) useIsFetching for a global connection status indicator, (7) separate QueryClient instances for public (stocks) and authenticated (portfolio) data, (8) retry with exponential backoff for network failures, (9) persist cache for offline access to latest prices, (10) suspense mode for skeleton loading of dashboard sections.
