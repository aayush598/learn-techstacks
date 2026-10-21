# React Interview Questions and Answers

## Q1: What is React?
**A:** React is an open-source JavaScript library for building user interfaces, primarily for single-page applications. It was developed by Facebook (Meta) and focuses on component-based architecture, declarative UI, and efficient rendering through a virtual DOM.

## Q2: What is JSX?
**A:** JSX (JavaScript XML) is a syntax extension for JavaScript that looks similar to HTML. It allows writing HTML-like code in JavaScript files. JSX gets transpiled to `React.createElement()` calls by tools like Babel, enabling declarative UI descriptions.

## Q3: What is the Virtual DOM?
**A:** The Virtual DOM is a lightweight JavaScript representation of the real DOM. When state changes, React creates a new virtual DOM tree, diffs it against the previous one (reconciliation), and applies minimal, efficient updates to the real DOM.

## Q4: What are components in React?
**A:** Components are reusable, independent pieces of UI. They can be function components (using plain functions) or class components (using ES6 classes). Components accept inputs called props and return React elements describing what should appear on screen.

## Q5: What is the difference between functional and class components?
**A:** Functional components are plain JavaScript functions that accept props and return JSX. Class components extend `React.Component` and have a `render()` method. Functional components use hooks for state/lifecycle; class components use `this.state` and lifecycle methods. Functional components are now preferred.

## Q6: What are props in React?
**A:** Props (short for properties) are read-only inputs passed to components. They allow data to flow from parent to child components. Props are immutable — a component cannot modify its own props. They can be any JavaScript value.

## Q7: What is state in React?
**A:** State is a built-in object that stores data that may change over time. Unlike props, state is managed within the component and can be mutated (using `setState` in class components or `useState` hook in functional components). State changes trigger re-renders.

## Q8: What is the `useState` hook?
**A:** `useState` is a React hook that adds state to functional components. It returns an array with two elements: the current state value and a setter function. Example: `const [count, setCount] = useState(0)`. The setter triggers a re-render.

## Q9: What is the `useEffect` hook?
**A:** `useEffect` is a hook that lets you perform side effects in functional components. It runs after render and can handle data fetching, subscriptions, DOM manipulation, and timers. The dependency array controls when the effect re-runs.

## Q10: What is the dependency array in useEffect?
**A:** The dependency array is the second argument to `useEffect`. It specifies values that the effect depends on. When any dependency changes, the effect re-runs. An empty array `[]` runs the effect only once (on mount). Omitting it runs on every render.

## Q11: What is the difference between `useEffect` and lifecycle methods?
**A:** `useEffect` combines `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount` from class components. The dependency array controls which lifecycle behavior is mimicked. Effects can have cleanup functions returned from them.

## Q12: What is the `useRef` hook?
**A:** `useRef` returns a mutable ref object whose `.current` property persists across renders without causing re-renders when changed. It's commonly used for accessing DOM elements directly or storing mutable values that shouldn't trigger re-renders.

## Q13: What is the `useContext` hook?
**A:** `useContext` lets you subscribe to React context without nesting. It accepts a context object (created by `React.createContext`) and returns the current context value. It re-renders the component when the context value changes.

## Q14: What is the `useReducer` hook?
**A:** `useReducer` is an alternative to `useState` for complex state logic. It accepts a reducer function (state, action) and an initial state, returning the current state and a dispatch function. It's preferable for state objects with multiple sub-values.

## Q15: What is the `useMemo` hook?
**A:** `useMemo` memoizes the result of a computation, recomputing only when dependencies change. It optimizes expensive calculations by returning the cached value on re-renders if dependencies haven't changed. `const memoizedValue = useMemo(() => compute(a, b), [a, b])`.

## Q16: What is the `useCallback` hook?
**A:** `useCallback` returns a memoized version of a callback function that only changes if dependencies change. It prevents unnecessary re-renders of child components that receive callbacks as props. `const memoizedCallback = useCallback(() => doSomething(a, b), [a, b])`.

## Q17: What is the difference between `useMemo` and `useCallback`?
**A:** `useMemo` memoizes the return value of a function (used for expensive computations). `useCallback` memoizes the function reference itself (used for preventing unnecessary re-renders). `useCallback(fn, deps)` is equivalent to `useMemo(() => fn, deps)`.

## Q18: What is the `useTransition` hook?
**A:** `useTransition` (React 18+) allows marking certain state updates as non-urgent (transitions). It returns a `isPending` flag and `startTransition` function. UI remains responsive during transitions by deferring less critical updates.

## Q19: What is the `useDeferredValue` hook?
**A:** `useDeferredValue` (React 18+) accepts a value and returns a deferred (laggy) version that may trail behind. It's useful for keeping the UI responsive when rendering large lists with frequent input changes — the deferred value updates less urgently.

## Q20: What is the `useId` hook?
**A:** `useId` (React 18+) generates unique IDs for accessibility attributes, stable across server and client rendering. It prevents hydration mismatches for IDs used in forms or ARIA attributes.

## Q21: What are custom hooks?
**A:** Custom hooks are JavaScript functions that start with `use` and can call other hooks. They enable extracting component logic into reusable functions. Example: `useWindowSize`, `useFetch`, `useLocalStorage`.

## Q22: What is the Context API in React?
**A:** The Context API provides a way to share values (like themes, user preferences) across the component tree without manually passing props through every level (prop drilling). It consists of `React.createContext`, `Context.Provider`, and `useContext` hook.

## Q23: What is prop drilling and how do you avoid it?
**A:** Prop drilling is passing data through multiple intermediate components that don't need the data themselves but only pass it down. Avoid it using Context API, state management libraries (Redux, Zustand), or component composition.

## Q24: What are React Portals?
**A:** Portals let you render a component's children into a different part of the DOM tree (outside the parent component's DOM hierarchy). Created with `ReactDOM.createPortal(child, container)`. Useful for modals, tooltips, dropdowns.

## Q25: What are React Fragments?
**A:** Fragments let you group a list of children without adding extra DOM nodes. `<React.Fragment>` or `<>...</>` syntax. They solve the problem of returning multiple elements from a component without a wrapper div.

## Q26: What are Higher-Order Components (HOCs)?
**A:** An HOC is a function that takes a component and returns a new component with additional props or behavior. Pattern: `const EnhancedComponent = higherOrderComponent(WrappedComponent)`. Examples: `connect()` in Redux, `withRouter()`.

## Q27: What is the difference between HOCs and hooks?
**A:** HOCs wrap components to inject behavior/logic, while hooks directly add functionality to components. Hooks are simpler, don't cause wrapper hell, and avoid naming collisions. Hooks are the modern, preferred approach over HOCs.

## Q28: What are Render Props?
**A:** Render props is a pattern where a component receives a function as a prop that returns a React element. The component calls this function to render its content, sharing logic while letting the parent control rendering.

## Q29: What is the `key` prop and why is it important?
**A:** The `key` prop helps React identify which items have changed, been added, or removed in a list. Stable, unique keys enable efficient reconciliation. Using array indices as keys can cause bugs when the list order changes.

## Q30: What is React reconciliation?
**A:** Reconciliation is the algorithm React uses to diff two trees (virtual DOM) and determine the minimal set of DOM mutations. It compares element types, keys, and props. It uses heuristics to achieve O(n) complexity.

## Q31: What is the `ref` prop and how is it used?
**A:** The `ref` prop provides access to DOM nodes or React elements. In functional components, use `useRef` and attach via `ref` prop on DOM elements or `React.forwardRef` for custom components.

## Q32: What is `forwardRef`?
**A:** `React.forwardRef` creates a component that can forward a ref to a child component. It receives `props` and `ref` as arguments. Used when parent components need direct access to a child's DOM node or a third-party component's instance.

## Q33: What is `useImperativeHandle`?
**A:** `useImperativeHandle` customizes the instance value exposed to parent components when using `ref` with `forwardRef`. It limits what the parent can access, typically exposing specific methods instead of the full DOM node.

## Q34: How does React handle events?
**A:** React uses synthetic events — a cross-browser wrapper around native events. Events are named in camelCase (`onClick`, `onChange`). React pools synthetic events for performance (pre-React 17). Event handlers receive a `SyntheticEvent` object.

## Q35: What is event pooling in React?
**A:** Event pooling (pre-React 17) reuses synthetic event objects for performance. After the event callback completes, the event properties are nullified. To access event properties asynchronously, call `event.persist()`. React 17+ removed pooling.

## Q36: What is controlled vs uncontrolled components?
**A:** Controlled components have their state managed by React — form data is handled by the component's state via `value` and `onChange`. Uncontrolled components store their own state in the DOM — accessed via `ref`. Controlled is the recommended approach.

## Q37: What are controlled components in forms?
**A:** In controlled components, form elements (`<input>`, `<select>`, `<textarea>`) are controlled by React state. The input's `value` is set by state, and changes are handled via `onChange`. This gives React single source of truth for form data.

## Q38: What is form validation in React?
**A:** Form validation can be done manually (tracking errors in state), using libraries like `react-hook-form`, `Formik`, or `react-final-form`. Validation can be synchronous or async, on change, on blur, or on submit.

## Q39: What is the difference between Shadow DOM and Virtual DOM?
**A:** Virtual DOM is a JavaScript object representation of the real DOM used by React for efficient rendering. Shadow DOM is a browser API for encapsulating DOM and styles within web components. They serve different purposes.

## Q40: What are React Strict Mode?
**A:** `React.StrictMode` is a tool that wraps an application or component tree to highlight potential problems. In development, it double-invokes renders, effects, and constructors to detect side effects. It also warns about deprecated APIs.

## Q41: What is React Suspense?
**A:** Suspense lets components "wait" for something before rendering. It's used with `React.lazy` for code splitting and (in React 18+) for data fetching. `Suspense` has a `fallback` prop that shows content while waiting.

## Q42: What is `React.lazy`?
**A:** `React.lazy` enables dynamic import of components — code splitting at the component level. `const MyComponent = React.lazy(() => import('./MyComponent'))`. It must be wrapped in `<Suspense>` with a fallback UI.

## Q43: What is code splitting in React?
**A:** Code splitting is splitting the bundle into smaller chunks loaded on demand. React supports it via `React.lazy` with dynamic imports. Combined with Suspense, it reduces initial bundle size and improves load performance.

## Q44: What is React.memo?
**A:** `React.memo` is a higher-order component that memoizes a component's render output. It only re-renders if props change (shallow comparison). Useful for optimizing expensive renders where props rarely change.

## Q45: What is the `useMemo` hook vs `React.memo`?
**A:** `useMemo` memoizes a value (computation result). `React.memo` memoizes an entire component (prevents re-render). Use `useMemo` for expensive calculations; use `React.memo` for components that receive stable props.

## Q46: What are React error boundaries?
**A:** Error boundaries are class components that catch JavaScript errors in their child component tree, log errors, and display a fallback UI. They use `componentDidCatch(error, info)` lifecycle method. There is no hook equivalent yet.

## Q47: How do you handle errors in functional components?
**A:** Functional components cannot directly implement error boundaries (no `componentDidCatch` equivalent). Use a class component wrapper as an error boundary, or use libraries like `react-error-boundary` which provide hooks and reusable boundaries.

## Q48: What is React hydration?
**A:** Hydration is the process where React attaches event listeners and state to server-rendered HTML. It converts a static HTML page (from SSR) into an interactive React application without re-rendering the entire DOM.

## Q49: What is SSR (Server-Side Rendering) in React?
**A:** SSR renders React components to HTML on the server, sending fully rendered HTML to the client. This improves SEO, perceived performance, and accessibility. Tools: Next.js, Remix, or manual setup with `ReactDOMServer.renderToString()`.

## Q50: What is the `renderToString` function?
**A:** `ReactDOMServer.renderToString(reactElement)` renders a React element to its initial HTML string on the server. It's used for server-side rendering, allowing search engines to crawl content and users to see content faster.

## Q51: What is the difference between `renderToString` and `renderToPipeableStream`?
**A:** `renderToString` generates HTML synchronously, blocking until complete. `renderToPipeableStream` (React 18+) streams HTML in chunks, allowing the browser to start rendering content earlier. The latter is preferred for SSR.

## Q52: What is `createRoot` vs `ReactDOM.render`?
**A:** `createRoot` (React 18+) is the new API for rendering, replacing `ReactDOM.render`. It enables concurrent features and automatic batching. Usage: `createRoot(container).render(<App />)`. `ReactDOM.render` is deprecated.

## Q53: What is concurrent React?
**A:** Concurrent React (React 18+) allows React to interrupt long-running rendering work to handle higher-priority updates. It enables features like `Suspense`, `useTransition`, `useDeferredValue`, and automatic batching, making apps more responsive.

## Q54: What is automatic batching in React 18?
**A:** Automatic batching groups multiple state updates within event handlers, effects, timeouts, and promises into a single re-render. In React 17, batching only happened inside React event handlers. React 18 batches all updates by default.

## Q55: What are React Server Components (RSC)?
**A:** React Server Components are components that run exclusively on the server. They reduce client bundle size by keeping heavy dependencies (databases, filesystems) on the server. They can be async and directly access backend resources.

## Q56: What is the difference between server and client components?
**A:** Server Components render on the server, have no interactivity (no hooks, no event handlers), and reduce JS bundle size. Client Components render on both server (for SSR) and client, support hooks and interactivity, and ship JavaScript to the browser.

## Q57: What is `renderToPipeableStream`?
**A:** `renderToPipeableStream` is a React 18+ API for streaming SSR. It renders React components to a Node.js Readable stream, allowing the server to send HTML in chunks as it's rendered. Supports Suspense for selective hydration.

## Q58: What is selective hydration?
**A:** Selective hydration (React 18+) allows React to hydrate different parts of the page independently as their JavaScript loads. Content wrapped in `<Suspense>` can be hydrated selectively, prioritizing visible or interactive content.

## Q59: What is the `startTransition` API?
**A:** `startTransition` marks state updates as transitions (non-urgent). React defers these updates, keeping the UI responsive for urgent updates (like typing). Available via `useTransition` hook or directly as `startTransition`.

## Q60: How do you optimize React performance?
**A:** Techniques include: `React.memo` for components, `useMemo`/`useCallback` for values/functions, virtualization (`react-window`, `react-virtualized`) for large lists, lazy loading with `React.lazy`, avoiding unnecessary re-renders, and using production builds.

## Q61: What is React DevTools?
**A:** React DevTools is a browser extension (Chrome, Firefox) for debugging React applications. It shows component trees, props, state, hooks, and performance profiling. It includes a Profiler tab for identifying rendering bottlenecks.

## Q62: What is the Profiler component?
**A:** `<React.Profiler id="..." onRender={callback}>` measures how often a component renders and the cost of rendering. The callback receives timing information (mount time, render time, commit time). Useful for performance analysis.

## Q63: What are synthetic events in React?
**A:** Synthetic events are React's cross-browser wrapper around the browser's native events. They provide a consistent API across browsers. In React 17+, synthetic events are no longer pooled. Access native events via `event.nativeEvent`.

## Q64: How does React handle two-way binding?
**A:** React doesn't have built-in two-way binding like Angular. Instead, controlled components combine `value` prop (bound to state) and `onChange` handler (updates state). This is one-way data flow with explicit update handling.

## Q65: What is the `children` prop?
**A:** `children` is a special prop that represents the content between opening and closing tags of a component. It can be a string, element, array, or function. Used for component composition — creating flexible, reusable wrapper components.

## Q66: What are React patterns for composition?
**A:** Common patterns: Children passthrough (using `children` prop), Render Props (function as children), Compound Components (like `<Select>` with `<Select.Option>`), Higher-Order Components, Custom Hooks, and Slot-based composition.

## Q67: What is Flux architecture?
**A:** Flux is an application architecture pattern with unidirectional data flow. It consists of: Actions (user events), Dispatcher (central hub), Stores (state containers), and Views (React components). Redux popularized this pattern.

## Q68: What is Redux?
**A:** Redux is a predictable state management library for JavaScript apps. It uses a single immutable state tree, actions to describe state changes, and pure reducer functions to handle actions. Works well with React via `react-redux`.

## Q69: What are Redux slices?
**A:** A slice (Redux Toolkit) is a collection of reducer logic and actions for a single feature. `createSlice` generates action creators and reducers automatically. Example: `createSlice({ name: 'todos', initialState: [], reducers: {} })`.

## Q70: What is Redux Toolkit (RTK)?
**A:** Redux Toolkit is the official, opinionated Redux package for efficient Redux development. It includes `configureStore`, `createSlice`, `createAsyncThunk`, `createEntityAdapter`, and RTK Query for data fetching/caching.

## Q71: What is Zustand?
**A:** Zustand is a minimal state management library for React. It provides a simple API with hooks-based stores, no boilerplate, no providers needed. Example: `const useStore = create((set) => ({ count: 0, increment: () => set(s => ({ count: s.count + 1 })) }))`.

## Q72: What is React Query (TanStack Query)?
**A:** React Query is a data-fetching and caching library for React. It manages server state (async data) with features like caching, background refetching, pagination, infinite queries, and optimistic updates using hooks like `useQuery` and `useMutation`.

## Q73: What is the difference between React Query and Redux?
**A:** React Query handles server state (async data from APIs) with automatic caching and synchronization. Redux manages client state (UI state, cached data) with predictable reducers. They can be used together — React Query for API data, Redux for UI state.

## Q74: What is `useQuery` hook?
**A:** `useQuery` (from TanStack Query) fetches, caches, and manages server data. It accepts a query key and async function. Returns `{ data, isLoading, error, isFetching, refetch }`. Automatically caches and deduplicates requests.

## Q75: What is `useMutation` hook?
**A:** `useMutation` handles create/update/delete operations (side effects). It provides `mutate`/`mutateAsync` functions and tracks mutation state (`isLoading`, `isError`, `onSuccess`, `onError` callbacks).

## Q76: What are React fibers?
**A:** React Fiber is the reimplementation of React's reconciliation engine (React 16+). It enables incremental rendering, the ability to pause/resume work, prioritize updates, and reuse previously completed work. It's the foundation for concurrent features.

## Q77: What is the React component lifecycle in functional components?
**A:** Functional components use hooks to mimic lifecycle phases: Mounting (`useEffect(() => {}, [])`), Updating (`useEffect(() => {}, [deps])`), Unmounting (`useEffect(() => { return cleanup }, [])`), and Error Handling (via error boundaries).

## Q78: What is the `ComponentDidCatch` lifecycle method?
**A:** `componentDidCatch(error, info)` is a class component lifecycle method that catches JavaScript errors in child components. It receives the error and an info object with `componentStack`. Used to implement error boundaries.

## Q79: What are pure components in React?
**A:** `React.PureComponent` is a base class that implements `shouldComponentUpdate` with a shallow prop/state comparison. It prevents unnecessary re-renders. For functional components, `React.memo` provides equivalent behavior.

## Q80: What is `shouldComponentUpdate`?
**A:** `shouldComponentUpdate(nextProps, nextState)` is a lifecycle method in class components that returns a boolean. It lets React skip rendering if the component doesn't need to update, based on custom comparison logic.

## Q81: What is `createRef` vs `useRef`?
**A:** `React.createRef()` creates a ref object in class components. `useRef()` is the hook equivalent for functional components. `useRef` persists across renders, while `createRef` creates a new ref each render (for class components, it's stored as instance property).

## Q82: How do you test React components?
**A:** Using React Testing Library (preferred) or Enzyme. React Testing Library focuses on testing behavior (not implementation), rendering components and asserting on rendered output, events, and accessibility.

## Q83: What is React Testing Library?
**A:** React Testing Library is a testing utility that encourages testing components from the user's perspective. It provides `render`, `screen` (queries like `getByText`, `getByRole`), `fireEvent`, and `waitFor`. Built on top of DOM Testing Library.

## Q84: What is the `act()` function in testing?
**A:** `act()` is a test utility that ensures all pending state updates and effects are processed before assertions. React Testing Library wraps its APIs in `act()` automatically. Manual `act()` is rarely needed with RTL.

## Q85: What is Storybook?
**A:** Storybook is a tool for developing, documenting, and testing UI components in isolation. It provides a sandbox environment where each component can be rendered with different props and states without running the full application.

## Q86: What are compound components in React?
**A:** Compound components are a pattern where multiple components share implicit state. Example: `<Menu>` with `<Menu.Item>`. State is shared via Context API or `React.Children.map` with `cloneElement`. Provides flexible, declarative APIs.

## Q87: What is `React.cloneElement`?
**A:** `React.cloneElement(element, props, ...children)` clones a React element and merges new props. Used in compound components and higher-order components to pass additional props to children. Should be used sparingly.

## Q88: What is `React.Children` utilities?
**A:** `React.Children` provides utilities for handling `this.props.children`: `React.Children.map`, `React.Children.forEach`, `React.Children.count`, `React.Children.only`, `React.Children.toArray`. Useful for manipulation and validation of children.

## Q89: What is hydration mismatch?
**A:** A hydration mismatch occurs when the HTML generated on the server differs from what React renders on the client during hydration. Causes include differences in data, browser-specific rendering, or non-deterministic values. React warns about these in development.

## Q90: What is the `dangerouslySetInnerHTML` prop?
**A:** `dangerouslySetInnerHTML` is React's replacement for `innerHTML`. It accepts an object with `__html` property. It's dangerous because it bypasses React's XSS protection. Use only with sanitized content.

## Q91: How do you handle accessibility (a11y) in React?
**A:** Use semantic HTML elements, ARIA attributes (`aria-label`, `role`), manage focus, use `useId` for unique IDs, ensure keyboard navigation, provide alt text for images, and use testing tools like `jest-axe` for automated checks.

## Q92: What are the rules of hooks?
**A:** Three rules: 1) Only call hooks at the top level (not inside loops, conditions, or nested functions). 2) Only call hooks from React function components or custom hooks (not regular JS functions). 3) Hook names must start with `use`.

## Q93: Why can't hooks be called conditionally?
**A:** React relies on the order of hook calls to correctly associate state between renders. Conditional hook calls would change this order, causing bugs where state gets misaligned. This is enforced by the ESLint plugin `eslint-plugin-react-hooks`.

## Q94: What is server-side rendering with React and hydration?
**A:** SSR generates HTML on the server using `renderToString` or `renderToPipeableStream`. The client receives pre-rendered HTML (faster initial paint) and React hydrates it by attaching event listeners. Hydration should match the server HTML exactly.

## Q95: What are React's upcoming features?
**A:** Upcoming/experimental features include: React Forget (automatic memoization compiler), Server Components (stable in frameworks), Asset Loading improvements, Offscreen rendering, and continued enhancements to concurrent features.

## Q96: What is React Forget?
**A:** React Forget is an experimental compiler that automatically memoizes React components and hooks. It aims to eliminate the need for manual `useMemo`, `useCallback`, and `React.memo` by automatically detecting and optimizing reactive dependencies.

## Q97: What is the difference between `useEffect` and `useLayoutEffect`?
**A:** `useEffect` runs asynchronously after the browser paints (non-blocking). `useLayoutEffect` runs synchronously after DOM mutations but before the browser paints (blocking). Use `useLayoutEffect` for DOM measurements and mutations that must be visible immediately.

## Q98: How do you handle concurrent updates in React?
**A:** React 18+ handles concurrency via `startTransition` and `useDeferredValue`. Mark non-urgent state updates as transitions so React can prioritize urgent updates (like typing) over less critical ones (like rendering search results).

## Q99: What is the React reconciliation key algorithm?
**A:** React uses `key` props to match children in the old and new virtual DOM. With stable keys, React moves/inserts/removes items accordingly. Without keys (or with index keys), React may unnecessarily unmount and remount siblings.

## Q100: What are the most common React performance pitfalls?
**A:** Common pitfalls include: unnecessary re-renders (no memoization on expensive components), missing dependency arrays in hooks (causing infinite loops or stale closures), large lists without virtualization, inline functions/objects in props (causing child re-renders), and excessive state updates.
