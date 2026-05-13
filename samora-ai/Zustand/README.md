# Zustand Interview Questions and Answers

## Q1: What is Zustand?
**A:** Zustand is a small, fast, and scalable barebones state management library for React. It provides a simple API to create global state stores using hooks, without the boilerplate of Redux or the context provider nesting of React Context.

## Q2: How do you install Zustand?
**A:** Zustand is installed via npm or yarn: `npm install zustand` or `yarn add zustand`. It has zero dependencies and is tree-shakeable.

## Q3: How do you create a basic store in Zustand?
**A:** You use the `create` function from `zustand` with a callback that receives `set` and `get` and returns an object defining the state and actions:
```js
import { create } from 'zustand';
const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```

## Q4: How do you access state from a component?
**A:** You call the store hook and select the needed state. Zustand hooks are reactive – components re-render only when the selected slice changes:
```js
function Counter() {
  const count = useStore((state) => state.count);
  return <div>{count}</div>;
}
```

## Q5: What is the difference between Zustand and React Context?
**A:** Zustand creates stores outside the React tree without providers, avoids unnecessary re-renders via fine-grained subscriptions, requires no nesting, and has a simpler API. React Context re-renders all consumers when any context value changes unless memoization is used.

## Q6: How do you update state in Zustand?
**A:** Using the `set` function provided in the store creator. `set` merges the returned object shallowly with the current state. It can take either an object or a function receiving the current state: `set({ count: 5 })` or `set((state) => ({ count: state.count + 1 }))`.

## Q7: How do you access current state outside of React components?
**A:** Each store hook has a `.getState()` method and a `.setState()` method for imperative access. You can also subscribe to changes with `.subscribe(listener)` outside React.

## Q8: Can Zustand be used without React?
**A:** Yes. The core `zustand` package can be used standalone. There is also `zustand/vanilla` which exports `createStore` that works without any React dependency. The `create` from `zustand` wraps the vanilla store with React hooks.

## Q9: How does Zustand handle immutability?
**A:** Zustand expects immutable state updates. The `set` function performs a shallow merge, but nested objects must be updated immutably (create new objects). Zustand uses `Object.assign` under the hood for merging.

## Q10: What are selectors in Zustand?
**A:** Selectors are functions passed to the store hook to extract a specific slice of state. They control which parts of the state a component subscribes to, enabling fine-grained re-rendering:
```js
const userName = useStore((state) => state.user.name);
```

## Q11: Does Zustand support middleware?
**A:** Yes. Zustand supports middleware via a composable API. Built-in middleware includes `persist`, `immer`, `devtools`, `subscribeWithSelector`, `combine`, and `redux`. Custom middleware can also be written.

## Q12: How do you use the persist middleware?
**A:** You wrap the store creator with `persist` from `zustand/middleware`. It automatically saves state to localStorage (or a custom storage engine):
```js
import { persist } from 'zustand/middleware';
const useStore = create(persist((set) => ({
  theme: 'dark',
  setTheme: (theme) => set({ theme }),
}), { name: 'theme-storage' }));
```

## Q13: How do you use the devtools middleware?
**A:** Wrap your store with `devtools` from `zustand/middleware` to enable Redux DevTools integration:
```js
import { devtools } from 'zustand/middleware';
const useStore = create(devtools((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 }), false, 'increment'),
})));
```

## Q14: What is the subscribeWithSelector middleware?
**A:** It enhances the `.subscribe()` method to accept a selector and options for equality/compare, fireImmediately, etc. Useful for watching specific state changes outside React:
```js
useStore.subscribe((state) => state.count, (count) => console.log(count));
```

## Q15: How do you use Immer with Zustand?
**A:** The `immer` middleware allows mutable-style updates inside `set`:
```js
import { immer } from 'zustand/middleware/immer';
const useStore = create(immer((set) => ({
  todos: [],
  addTodo: (text) => set((state) => { state.todos.push({ text, done: false }); }),
})));
```

## Q16: How do you create multiple stores in Zustand?
**A:** Each call to `create` creates an independent store. You can have as many stores as needed, each managing a different domain:
```js
const useUserStore = create(...);
const useCartStore = create(...);
```

## Q17: How do you handle derived state in Zustand?
**A:** Derived state can be computed using selectors or by using external libraries like `immer`. You can also use the `subscribe` method or create helper functions that compute derived values from `getState()`.

## Q18: Can Zustand stores be typed with TypeScript?
**A:** Yes. Zustand has excellent TypeScript support. You define a type for the store and pass it as a generic:
```typescript
interface BearState { bears: number; increase: () => void; }
const useBearStore = create<BearState>()((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
}));
```

## Q19: How do you combine multiple slices/state in one store?
**A:** You can use the `combine` middleware or compose slices manually using the `set` function:
```js
const useStore = create((set) => ({
  ...userSlice(set),
  ...cartSlice(set),
}));
```

## Q20: What is the `set` function's second parameter?
**A:** The second parameter of `set` is a boolean (`replace`) that, when `true`, causes the entire state to be replaced rather than shallow-merged. The third parameter is a string used as an action name for Redux DevTools.

## Q21: How do you subscribe to store changes outside React?
**A:** Using `.subscribe(listener)` which returns an unsubscribe function:
```js
const unsub = useBearStore.subscribe((state) => console.log(state));
unsub(); // later
```

## Q22: How does Zustand handle equality checks?
**A:** Zustand uses `Object.is` for equality by default. You can provide a custom equality function via `useStore(selector, equalityFn)` or via the `subscribeWithSelector` middleware.

## Q23: What is `useShallow` in Zustand?
**A:** `useShallow` is a utility from `zustand/react/shallow` that provides shallow equality comparison for selectors returning objects. It prevents re-renders when the selected object's properties haven't changed:
```js
import { useShallow } from 'zustand/react/shallow';
const { name, age } = useStore(useShallow((state) => ({ name: state.name, age: state.age })));
```

## Q24: How do you test Zustand stores?
**A:** You can call `setState()` directly to set up test state and use `getState()` to assert values. You can also create fresh stores for each test. Vitest and Jest work well with Zustand.

## Q25: Can Zustand handle async actions?
**A:** Yes. Zustand has no opinion on async; you can use async functions directly in the store:
```js
const useStore = create((set) => ({
  data: null,
  fetchData: async (id) => {
    const res = await fetch(`/api/${id}`);
    set({ data: await res.json() });
  },
}));
```

## Q26: How do you reset a Zustand store to its initial state?
**A:** You can define a `reset` action that calls `set` with the initial state. A common pattern is to store the initial state:
```js
const initialState = { count: 0 };
const useStore = create((set) => ({
  ...initialState,
  reset: () => set(initialState),
}));
```

## Q27: What is the `transientUpdates` option in Zustand?
**A:** `transientUpdates` (from `zustand/middleware`) allows batching multiple synchronous updates into a single re-render. It's useful for performance optimization when many state changes happen rapidly.

## Q28: How do you use Zustand with Next.js?
**A:** Zustand works out of the box with Next.js. For server components, note that hooks cannot be used, so state management should be client-side. For SSR, ensure stores are not shared across requests by creating instances per request.

## Q29: Can you use Zustand with class components?
**A:** Yes. You can use the store hook inside a class component wrapper or use the `.subscribe()` and `.getState()` methods directly:
```js
class Counter extends React.Component {
  componentDidMount() { this.unsub = useStore.subscribe(() => this.forceUpdate()); }
  componentWillUnmount() { this.unsub(); }
  render() { return <div>{useStore.getState().count}</div>; }
}
```

## Q30: How does Zustand compare to Redux?
**A:** Zustand is simpler (no providers, reducers, action types, or dispatch), has zero boilerplate, is smaller (~1KB vs ~12KB), and provides fine-grained subscriptions out of the box. Redux has a larger ecosystem, middleware culture, and better DevTools. Zustand can be a drop-in for many Redux use cases.

## Q31: What is the `redux` middleware in Zustand?
**A:** It allows using Zustand with a Redux-like reducer pattern:
```js
import { redux } from 'zustand/middleware';
const useStore = create(redux((state, action) => {
  switch (action.type) { case 'INC': return { count: state.count + 1 }; }
}, { count: 0 }));
```

## Q32: How do you handle errors in Zustand stores?
**A:** Error handling is application-level. You can store error state, use try/catch in async actions, and set error fields in the store. There's no built-in error boundary support.

## Q33: What is `StateCreator` in Zustand?
**A:** `StateCreator` is a TypeScript utility type representing a store creation function. It's used internally and for typing custom middleware.

## Q34: How do you compose middleware in Zustand?
**A:** Middleware are composed by wrapping the store creator. The order matters – inner middleware wraps the state mutation, outer middleware wraps the whole thing:
```js
create(persist(devtools(myStore), { name: 'store' }))
```

## Q35: How does Zustand prevent stale closures?
**A:** Zustand's `get()` parameter in the store creator provides access to the latest state without closure issues. Inside React components, selectors get fresh state on each render.

## Q36: What is the `patch` method in Zustand?
**A:** Zustand doesn't have a specific `patch` method. Partial updates are done via `set({ ... })` which shallow-merges the provided object into the state.

## Q37: Can you use Zustand with React Native?
**A:** Yes. Zustand works with React Native out of the box. The persist middleware can be configured with `AsyncStorage` or any custom storage engine for React Native.

## Q38: How do you create computed properties in Zustand?
**A:** Computed properties can be created using selectors that derive values, or by using helper functions. Zustand does not have built-in computed/derived state, but you can use libraries like `valtio`-style proxies with the `immer` middleware.

## Q39: What is the difference between `set` and `setState`?
**A:** `set` is the internal updater available in the store creator callback. `setState` is the external method on the store that allows updating state from outside the store. They behave identically.

## Q40: How do you handle deeply nested state updates?
**A:** Use the `immer` middleware for mutable-style deep updates, or manually spread nested objects:
```js
set((state) => ({
  user: { ...state.user, address: { ...state.user.address, city: 'NYC' } },
}));
```

## Q41: Can Zustand stores be extended?
**A:** Yes, stores can be composed from multiple slices, and you can create higher-order stores that wrap other stores. The `create` function returns a hook that can be extended.

## Q42: How does Zustand handle server-side rendering?
**A:** On the server, each request should create a fresh store instance to avoid cross-request state leakage. You can use `createStore` from `zustand/vanilla` and then wrap it per request.

## Q43: What is the `StoreApi` type in Zustand?
**A:** `StoreApi` is a TypeScript interface representing the store's API including `setState`, `getState`, `subscribe`, and `destroy`. It's used for typing store references.

## Q44: How do you subscribe to specific state changes only?
**A:** Using `subscribeWithSelector` middleware, you can pass a selector and an equality function:
```js
useStore.subscribe((s) => s.count, (count) => console.log(count), { equalityFn: Object.is });
```

## Q45: How do you destroy a Zustand store?
**A:** Each store has a `.destroy()` method that removes all subscribers. This is useful for cleanup in testing or when a store is no longer needed.

## Q46: What is the `useSyncExternalStore` connection?
**A:** Zustand uses `useSyncExternalStore` internally (React 18+) to safely handle concurrent rendering. This prevents tearing and ensures consistent state across React's concurrent features.

## Q47: How do you create a store with initial state from props?
**A:** You can create a custom hook that accepts props and creates a store instance:
```js
function useMyStore(initialCount) {
  return useMemo(() => create((set) => ({ count: initialCount })), [initialCount]);
}
```

## Q48: Can you use Zustand without hooks?
**A:** Yes. The vanilla `createStore` from `zustand/vanilla` provides `getState`, `setState`, `subscribe`, and `destroy` without any React dependency.

## Q49: How do you handle race conditions in Zustand?
**A:** Race conditions are handled at the application level. Use patterns like abort controllers, cancellation tokens, or check if the component is still mounted before setting state.

## Q50: What is `useStore(selector, shallowEqual)`?
**A:** The second argument to `useStore` is an optional equality function. If provided, it compares the previous and current selected values to determine if a re-render is needed.

## Q51: How do you access a store inside another store?
**A:** You can import the store hook and use `getState()` to access another store. Cross-store communication is done imperatively:
```js
const useAuthStore = create(...);
const useCartStore = create((set) => ({
  checkout: () => {
    const user = useAuthStore.getState().user;
    // ...
  },
}));
```

## Q52: What is the `persist` middleware's partialize option?
**A:** `partialize` allows selecting which parts of the state to persist. This is useful for excluding transient state or sensitive data:
```js
persist(store, { partialize: (state) => ({ theme: state.theme }) })
```

## Q53: How does Zustand compare to Jotai?
**A:** Zustand uses a single store (or multiple stores) with selectors, while Jotai uses atomic atoms that can be composed. Zustand is simpler for global state; Jotai excels at fine-grained, composable state. Both are lightweight alternatives to Redux.

## Q54: Can Zustand work with SolidJS or Vue?
**A:** The vanilla core (`zustand/vanilla`) works anywhere JavaScript runs. Community adapters exist for SolidJS and Vue, but the main `zustand` package is React-focused.

## Q55: How do you debug Zustand stores?
**A:** Use the `devtools` middleware for Redux DevTools integration, or simply log state changes via `.subscribe()`. You can also use React DevTools to inspect component state relying on Zustand.

## Q56: What is the `temporal` middleware?
**A:** The `temporal` middleware (from `zundo`) adds undo/redo capability to Zustand stores. It tracks state history and provides `undo`, `redo`, `clear`, and other temporal actions.

## Q57: How do you batch multiple updates in Zustand?
**A:** Zustand batches updates automatically within React event handlers (React 18+). For external updates, use `unstable_batchedUpdates` from `react-dom` or wrap in `setTimeout`/`requestAnimationFrame`.

## Q58: How do you share stores across micro-frontends?
**A:** You can expose the vanilla store (`createStore`) on a shared global object or use a pub/sub pattern. Zustand stores can be shared across module boundaries as long as they access the same store instance.

## Q59: What is the `context` API in Zustand?
**A:** Zustand provides a `createContext` utility that creates a React Context for a store, allowing different parts of the tree to have different store instances (useful for SSR or testing):
```js
import { createContext } from 'zustand/context';
const { Provider, useStore } = createContext();
```

## Q60: Can you use Zustand selectors with React.memo?
**A:** Yes. Combining `React.memo` with Zustand selectors provides optimal performance by preventing re-renders when selected state hasn't changed.

## Q61: How do you handle form state with Zustand?
**A:** Zustand works well for form state. You can store form values, touched state, errors, and validation functions in the store. Libraries like `react-hook-form` can also be used alongside Zustand.

## Q62: How do you create a store with dynamic keys?
**A:** You can use computed property names or maintain a map/record in the store:
```js
const useStore = create((set) => ({
  items: {},
  setItem: (key, value) => set((state) => ({ items: { ...state.items, [key]: value } })),
}));
```

## Q63: What is the `shallow` utility in Zustand?
**A:** The `shallow` utility performs a shallow comparison of two objects/arrays. It's commonly used with selectors to prevent re-renders when returning objects:
```js
import { shallow } from 'zustand/shallow';
const { a, b } = useStore((s) => ({ a: s.a, b: s.b }), shallow);
```

## Q64: How do you migrate persist middleware data?
**A:** The `persist` middleware supports a `migrate` function for versioned migrations:
```js
persist(store, {
  version: 2,
  migrate: (persistedState, version) => ({ ...persistedState, newField: '' }),
})
```

## Q65: Can Zustand trigger side effects on state change?
**A:** Yes, use `.subscribe()` for side effects outside React, or use `useEffect` in components. The `subscribeWithSelector` middleware is particularly useful for reacting to specific changes.

## Q66: How do you create an undo/redo system in Zustand?
**A:** You can manually implement undo/redo by storing a history array in the store, or use the `zundo` library's `temporal` middleware which provides this out of the box.

## Q67: What is the `get` parameter in Zustand stores?
**A:** The second parameter in the store creator callback, `get`, is a function that returns the current state. It's useful in actions to access state without closure issues:
```js
create((set, get) => ({
  count: 0,
  doubleCount: () => set({ count: get().count * 2 }),
}));
```

## Q68: How does Zustand handle transaction-like updates?
**A:** Zustand doesn't have built-in transactions, but you can batch updates using `set` with a function that applies multiple changes atomically:
```js
set((state) => ({ a: state.a + 1, b: state.b - 1 }));
```

## Q69: Can Zustand be used with Electron?
**A:** Yes. Zustand's vanilla core works in Electron's main process, and the React integration works in renderer processes. The persist middleware can use Electron's `electron-store` as a custom storage engine.

## Q70: How do you handle query parameters/URL state with Zustand?
**A:** You can sync Zustand state with URL parameters via the persist middleware with a custom storage that reads/writes URL search params, or manually sync using event listeners.

## Q71: What is the difference between `create` and `createStore`?
**A:** `create` (from `zustand`) returns a React hook. `createStore` (from `zustand/vanilla`) returns a vanilla store object with `getState`, `setState`, `subscribe`, and `destroy`. `create` uses `createStore` internally and wraps it.

## Q72: How do you optimize Zustand stores for performance?
**A:** Use fine-grained selectors, avoid returning new objects in selectors without `shallow`, use `React.memo`, split large stores into smaller domain stores, and use `useShallow` for object selectors.

## Q73: Can Zustand stores be serialized?
**A:** Yes, `getState()` returns a plain JavaScript object that can be JSON-stringified. The `persist` middleware handles serialization automatically. For non-serializable state (e.g., class instances, functions), use `partialize` to exclude them.

## Q74: How do you create a Zustand store with middleware in TypeScript?
**A:** Use the pipe/factory pattern:
```typescript
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
interface Store { count: number; inc: () => void; }
const useStore = create<Store>()(devtools(persist((set) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
}), { name: 'count' })));
```

## Q75: How do you handle loading states in Zustand?
**A:** Include loading flags in the store state and update them during async actions:
```js
const useStore = create((set) => ({
  data: null,
  loading: false,
  fetchData: async () => {
    set({ loading: true });
    const data = await api.get();
    set({ data, loading: false });
  },
}));
```

## Q76: What are some common anti-patterns with Zustand?
**A:** Common anti-patterns include: creating stores inside components (unless intentionally scoped), putting everything in one store, not using selectors (causing full re-renders), mutating state directly instead of immutably, and mixing concerns in a single store.

## Q77: How do you test Zustand stores synchronously?
**A:** Create the store, call actions, and assert with `getState()`:
```js
const useStore = create((set) => ({ count: 0, inc: () => set((s) => ({ count: s.count + 1 })) }));
useStore.getState().inc();
expect(useStore.getState().count).toBe(1);
```

## Q78: Can Zustand work with Redux DevTools in production?
**A:** Yes, the `devtools` middleware works in both development and production. You can conditionally enable it based on `process.env.NODE_ENV` to disable in production for performance.

## Q79: How do you create a store with both private and public state?
**A:** Zustand stores expose all state by default. To have "private" state, you can use closures in the store creator:
```js
const useStore = create((set) => {
  const privateVar = 0;
  return {
    publicVar: 0,
    publicAction: () => set({ publicVar: privateVar + 1 }),
  };
});
```

## Q80: What is the Zustand `mutate` helper?
**A:** Zustand doesn't have a built-in `mutate` helper. The `immer` middleware provides `mutate`-like capabilities by allowing direct mutation inside `set` callbacks.

## Q81: How do you debug which component is causing re-renders?
**A:** Use React DevTools Profiler, add console logs in selectors, or use the `why-did-you-render` library. Zustand's fine-grained subscriptions make this easier than with Context.

## Q82: Can Zustand stores listen to each other?
**A:** Yes, via `subscribe` cross-store, or by calling `getState()` on one store inside another's actions. For complex inter-store communication, consider merging stores or using an event bus.

## Q83: How do you handle optimistic updates with Zustand?
**A:** Apply the update optimistically in the store, then revert if the API call fails:
```js
const useStore = create((set, get) => ({
  updateUser: async (id, data) => {
    const previous = get().users;
    set((state) => ({ users: state.users.map(u => u.id === id ? { ...u, ...data } : u) }));
    try { await api.patch(`/users/${id}`, data); }
    catch { set({ users: previous }); }
  },
}));
```

## Q84: What is the `subscribe` function's return value?
**A:** `.subscribe()` returns an unsubscribe function. Call it to stop listening to state changes:
```js
const unsub = store.subscribe(console.log);
unsub(); // cleanup
```

## Q85: How do you create a selector that returns multiple values?
**A:** Return an object or array from the selector. Use `shallow` or `useShallow` to compare structurally:
```js
const { name, email } = useStore(useShallow((s) => ({ name: s.name, email: s.email })));
```

## Q86: How do you handle WebSocket events with Zustand?
**A:** Subscribe to WebSocket events and call `setState` on the store:
```js
const ws = new WebSocket(url);
ws.onmessage = (event) => useStore.setState({ messages: [...useStore.getState().messages, event.data] });
```

## Q87: Can Zustand be used with Suspense?
**A:** Zustand stores don't directly integrate with Suspense, but you can use React's `use` hook (React 19) with promises stored in Zustand, or combine with libraries like `@tanstack/react-query`.

## Q88: How do you create a store factory (multiple instances)?
**A:** Create a function that returns `createStore` or `create`:
```js
const createCounterStore = () =>
  create((set) => ({ count: 0, inc: () => set((s) => ({ count: s.count + 1 })) }));
```

## Q89: What is the `api` parameter in Zustand stores?
**A:** The `set`, `get`, and `api` are the parameters. `api` provides the full store API including `setState`, `getState`, `subscribe`, and `destroy`, exposed as the third parameter.

## Q90: How does Zustand compare to Valtio?
**A:** Zustand uses immutable state with selector-based subscriptions. Valtio uses mutable proxy-based state where mutations automatically trigger updates. Zustand is more explicit; Valtio is more magical. Both are similar in bundle size.

## Q91: How do you use Zustand with Next.js App Router?
**A:** Create stores in client components (or use vanilla stores in server actions). Avoid sharing stores between server components. Use the `persist` middleware carefully to avoid hydration mismatches.

## Q92: What is the best way to structure large Zustand stores?
**A:** Split into multiple domain stores, use slices pattern, or use the `combine` middleware. Keep stores focused on a single concern. Consider using a directory structure with store files per domain.

## Q93: How do you handle dependencies between stores?
**A:** Use `getState()` to read from other stores. For reactive dependencies, subscribe to changes. For tightly coupled stores, consider merging them.

## Q94: Can you use Zustand with class-based state management patterns?
**A:** Yes, the vanilla store API (`createStore`) provides an imperative interface that works well with class-based patterns, MVC-like architectures, or any non-React code.

## Q95: How does Zustand handle concurrent rendering (React 18)?
**A:** Zustand uses `useSyncExternalStore` to safely read and subscribe to external stores during concurrent rendering, preventing "tearing" where different components see different state values.

## Q96: What is the Zustand middleware ordering convention?
**A:** Inner middleware (closest to the store) affects state mutation. Outer middleware (farthest) affects the store API. Common order: `immer -> persist -> devtools`.

## Q97: How do you add TypeScript generics to middleware?
**A:** Use the `StateCreator` type to type middleware:
```typescript
import { StateCreator } from 'zustand';
const myMiddleware = (config: StateCreator<MyStore>) => (set, get, api) => config((args) => {
  console.log('before', get());
  return set(args);
}, get, api);
```

## Q98: What is the `omit` utility in Zustand?
**A:** Zustand does not have a built-in `omit` utility. You can use JavaScript destructuring or libraries like `lodash.omit` to exclude fields from persisted state.

## Q99: How do you migrate from Redux to Zustand?
**A:** Create Zustand stores alongside existing Redux stores, gradually move slices over, use the `redux` middleware if you want a reducer pattern, and leverage Zustand's simpler API to eliminate boilerplate.

## Q100: What is the future of Zustand?
**A:** Zustand continues to evolve with React's concurrent features, improved TypeScript support, and ecosystem growth. It's maintained by the Poimandres team and has become one of the most popular React state management libraries due to its simplicity, performance, and small bundle size.
