# React & Next.js Interview Q&A — 400+ Questions

> **Level:** YC Startup / Top Company
> **Format:** Each answer is detailed with code examples
> **Topics:** React Core, State Management, Performance, Next.js, React Router, General

---

## Table of Contents

1. [React Core (Q1–Q120)](#react-core-q1-q120)
2. [State Management (Q121–Q180)](#state-management-q121-q180)
3. [Performance Optimization (Q181–Q230)](#performance-optimization-q181-q230)
4. [Next.js (Q231–Q350)](#next-js-q231-q350)
5. [React Router & Navigation (Q351–Q380)](#react-router--navigation-q351-q380)
6. [General React Interview (Q381–Q400)](#general-react-interview-q381-q400)

---

## React Core (Q1–Q120)

### Q1: What is React?

**React** is a JavaScript library for building user interfaces, developed by Meta. It is declarative, component-based, and driven by a virtual DOM.

```tsx
function Greeting({ name }: { name: string }) {
  return <h1>Hello, {name}!</h1>;
}
```

**Key characteristics:**
- **Declarative** — you describe what the UI should look like.
- **Component-based** — UI is composed of encapsulated, reusable components.
- **Virtual DOM** — lightweight representation of the real DOM in memory.

---

### Q2: What is the Virtual DOM? Explain diffing and reconciliation.

The **Virtual DOM** is a lightweight JS object mirroring the real DOM. When state changes:

1. Creates a new Virtual DOM tree.
2. **Diffs** it against the previous tree (**reconciliation**).
3. Computes minimal changes (patches).
4. Applies patches to the real DOM.

```tsx
function diff(oldVNode, newVNode) {
  if (oldVNode.type !== newVNode.type)
    return { type: 'REPLACE', newVNode };
  if (oldVNode.props !== newVNode.props)
    return { type: 'UPDATE_PROPS', props: newVNode.props };
  return null;
}
```

**Fiber** (React 16+) enables:
- Incremental rendering (splitting work into chunks).
- Prioritization (user input > data fetches).
- Pausing and resuming work.

---

### Q3: How does JSX compile?

JSX is syntactic sugar for `React.createElement`. Babel/TypeScript compiles it:

```tsx
// JSX
const el = <div className="container">Hello</div>;
// Compiled
const el = React.createElement('div', { className: 'container' }, 'Hello');

// React 17+ JSX transform (automatic runtime)
import { jsx as _jsx } from 'react/jsx-runtime';
function App() {
  return _jsx('h1', { children: 'Hello' });
}
```

`React.createElement` signature: `React.createElement(type, props, ...children)`

---

### Q4: Functional vs Class components

| Aspect | Functional | Class |
|--------|-----------|-------|
| State | `useState` hook | `this.state` + `this.setState` |
| Lifecycle | `useEffect` | `componentDidMount`, `componentDidUpdate` |
| `this` | No binding issues | Must bind handlers |
| Performance | Lighter | Slightly heavier |
| Current standard | Preferred | Legacy |

```tsx
// Functional
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c+1)}>{count}</button>;
}

// Class
class Counter extends React.Component {
  state = { count: 0 };
  render() {
    return <button onClick={() => this.setState(s => ({ count: s.count+1 }))}>
      {this.state.count}
    </button>;
  }
}
```

---

### Q5: Props vs State

| | Props | State |
|---|---|---|
| Source | Parent component | Component itself |
| Mutability | Immutable | Mutable via setter |
| Purpose | Configuration | Internal dynamic data |
| Triggers re-render? | Yes | Yes |

```tsx
function Parent() {
  const [mode, setMode] = useState('dark');
  return <Child theme={mode} />;
}
function Child({ theme }: { theme: string }) {
  return <div className={theme}>Content</div>;
}
```

---

### Q6: How does `useState` work? Batch updates and stale closures

`useState` returns `[value, setValue]`. State is stored in the fiber node.

**Batch updates:** React groups multiple `setState` calls into a single re-render.

```tsx
function BatchExample() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(c => c + 1); // 1
    setCount(c => c + 1); // 2
    setCount(c => c + 1); // 3 — batched into one render
  }

  // Without functional updater — stale closure bug:
  function badClick() {
    setCount(count + 1); // all three see same stale count
    setCount(count + 1);
    setCount(count + 1); // result: 1, not 3
  }

  return <button onClick={handleClick}>{count}</button>;
}
```

**Stale closure fix:**
```tsx
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1); // always reads latest
  }, 1000);
  return () => clearInterval(id);
}, []);
```

---

### Q7: `useEffect` -- dependencies, cleanup, behaviors

| Dependency array | Runs on |
|---|---|
| `undefined` | Every render |
| `[]` (empty) | Mount only |
| `[a, b]` | When `a` or `b` change |

```tsx
function LifecycleDemo({ userId }: { userId: string }) {
  // Every render
  useEffect(() => { console.log('Rendered'); });

  // Mount only
  useEffect(() => {
    console.log('Mounted');
    return () => console.log('Unmounted'); // cleanup on unmount
  }, []);

  // When userId changes + cleanup
  useEffect(() => {
    const controller = new AbortController();
    fetch(`/api/users/${userId}`, { signal: controller.signal })
      .then(r => r.json()).then(setUser);
    return () => controller.abort(); // cancel on re-run or unmount
  }, [userId]);
}
```

**Cleanup runs:** (1) on unmount, (2) before re-running the effect.

---

### Q8: `useRef` -- use cases

`useRef` provides a mutable object persisting across renders without causing re-render.

```tsx
// DOM ref
function AutoFocus() {
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => { inputRef.current?.focus(); }, []);
  return <input ref={inputRef} />;
}

// Mutable value (no re-render)
function Timer() {
  const countRef = useRef(0);
  function increment() {
    countRef.current += 1; // persists, no re-render
  }
  return <button onClick={increment}>{countRef.current}</button>;
}

// Previous value
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => { ref.current = value; }, [value]);
  return ref.current;
}
```

---

### Q9: `useMemo` and `useCallback` -- when to use, when NOT to

```tsx
// useMemo: memoize expensive computation
function ExpensiveList({ items, filter }: { items: Item[]; filter: string }) {
  const filteredItems = useMemo(
    () => items.filter(i => i.name.includes(filter)).sort(sortItems),
    [items, filter]
  );
  return filteredItems.map(item => <ListItem key={item.id} item={item} />);
}

// useCallback: stable function reference
function Parent() {
  const [other, setOther] = useState(0);
  const handleClick = useCallback(() => {
    doSomething();
  }, []); // stable reference

  return <ExpensiveChild onAction={handleClick} />;
}
```

**When NOT to use:**
- Cheap computation (basic math, simple conditions).
- Child doesn't use `React.memo` / `PureComponent`.
- Premature optimization -- measure with Profiler first.
- Deps change every render anyway.

---

### Q10: `useContext` -- how it works, performance implications

```tsx
const ThemeContext = createContext('light');

function App() {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function ThemedButton() {
  const { theme, setTheme } = useContext(ThemeContext);
  return <button className={theme} onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>
    Toggle
  </button>;
}
```

**Performance:**
- **All consumers re-render** when context value changes.
- Fix: split contexts, use `useMemo` on the value.

```tsx
// BAD: monolithic -- any change re-renders all consumers
// GOOD: split contexts
function App() {
  return (
    <ThemeProvider>
      <UserProvider>
        <Main />
      </UserProvider>
    </ThemeProvider>
  );
}
```

---

### Q11: `useReducer` vs `useState`

```tsx
type Action =
  | { type: 'ADD_TODO'; text: string }
  | { type: 'TOGGLE_TODO'; id: number };

function todoReducer(state: Todo[], action: Action): Todo[] {
  switch (action.type) {
    case 'ADD_TODO':
      return [...state, { id: Date.now(), text: action.text, done: false }];
    case 'TOGGLE_TODO':
      return state.map(t => t.id === action.id ? { ...t, done: !t.done } : t);
  }
}

function TodoApp() {
  const [todos, dispatch] = useReducer(todoReducer, []);
  return (
    <>
      <AddTodo onAdd={text => dispatch({ type: 'ADD_TODO', text })} />
      {todos.map(t => <TodoItem key={t.id} todo={t} onToggle={() => dispatch({ type: 'TOGGLE_TODO', id: t.id })} />)}
    </>
  );
}
```

**When `useReducer` wins:** Complex state logic, interdependent fields, next state depends on previous, deep updates, testable pure reducer.

---

### Q12: Custom hooks and rules of hooks

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debouncedValue;
}

function Search() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);
  useEffect(() => { if (debouncedQuery) fetchSearch(debouncedQuery); }, [debouncedQuery]);
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

**Rules of Hooks:**
1. **Only call hooks at the top level** -- not in loops, conditions, or nested functions.
2. **Only call hooks from React function components or custom hooks.**
3. Custom hooks must start with `use`.

```tsx
// BAD
function Bad({ flag }: { flag: boolean }) {
  if (flag) const [value, setValue] = useState(0); // violation!
}
// GOOD
function Good({ flag }: { flag: boolean }) {
  const [value, setValue] = useState(0);
  useEffect(() => { if (flag) { /* ... */ } }, [flag]);
}
```

---

### Q13: Component lifecycle equivalents in hooks era

| Phase | Class | Hooks |
|-------|-------|-------|
| Mount | `constructor` | `useState` initializer |
| Mount | `componentDidMount` | `useEffect(fn, [])` |
| Update | `componentDidUpdate` | `useEffect(fn, [deps])` |
| Unmount | `componentWillUnmount` | `useEffect` cleanup |
| Before paint | `componentWillMount` (legacy) | `useLayoutEffect` |
| Skip re-render | `shouldComponentUpdate` | `React.memo` |

```tsx
function LifecycleExample({ id }: { id: string }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(`/api/${id}`).then(r => r.json()).then(d => {
      if (!cancelled) { setData(d); setLoading(false); }
    });
    return () => { cancelled = true; };
  }, [id]);

  useEffect(() => { console.log('Rendered'); });

  useLayoutEffect(() => { /* DOM measurement */ }, []);

  if (loading) return <Spinner />;
  return <div>{data?.name}</div>;
}
```

---

### Q14: `React.memo` and `PureComponent` -- when do they help?

```tsx
const ExpensiveChild = React.memo(function ExpensiveChild({ data }: { data: Item }) {
  console.log('Re-rendered');
  return <div>{data.name}</div>;
});

function Parent() {
  const [count, setCount] = useState(0);
  const data = useMemo(() => ({ id: 1, name: 'test' }), []);
  return (
    <>
      <button onClick={() => setCount(c => c+1)}>{count}</button>
      <ExpensiveChild data={data} />
    </>
  );
}
```

**When memo helps:** Props rarely change, component is expensive, child is "pure".
**When memo hurts:** Props change every render, cheap to re-render.
**Custom comparison:** `React.memo(Comp, (prev, next) => prev.id === next.id)`

---

### Q15: Why is the `key` prop important?

Without keys, React uses position-based reconciliation -- causes bugs.

```tsx
// BAD -- index key (causes state corruption on reorder/delete)
{todos.map((todo, index) => <li key={index}><TodoItem todo={todo} /></li>)}

// GOOD -- stable, unique key
{todos.map(todo => <li key={todo.id}><TodoItem todo={todo} /></li>)}
```

**What goes wrong:**
- **State mapping corruption** -- component instances are reused based on position.
- **Input state scrambling** -- text in inputs jumps between items.
- **Performance** -- React re-renders all siblings instead of moving them.

**When index key is acceptable:** Static list, never filtered/sorted/mutated, no component state.

---

### Q16: Lifting state up and component composition

**Lifting state up:** Moving shared state to closest common ancestor.

```tsx
function TemperatureConverter() {
  const [celsius, setCelsius] = useState(0);
  const fahrenheit = (celsius * 9/5) + 32;
  return (
    <div>
      <CelsiusInput value={celsius} onChange={setCelsius} />
      <FahrenheitDisplay value={fahrenheit} />
    </div>
  );
}
```

**Component composition:** Using `children` instead of inheritance.

```tsx
function Card({ title, children, footer }: {
  title: string; children: React.ReactNode; footer?: React.ReactNode;
}) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
      {footer && <div className="footer">{footer}</div>}
    </div>
  );
}
```

---

### Q17: Controlled vs uncontrolled components

```tsx
// Controlled -- React manages state
function ControlledInput() {
  const [value, setValue] = useState('');
  return <input value={value} onChange={e => setValue(e.target.value)} />;
}

// Uncontrolled -- DOM manages state
function UncontrolledInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  return <input ref={inputRef} defaultValue="initial" />;
}
```

| Aspect | Controlled | Uncontrolled |
|--------|-----------|-------------|
| State location | React | DOM |
| Value | `value` prop + `onChange` | `ref` + `defaultValue` |
| Use cases | Validation, dynamic forms | File inputs, simple forms, 3rd-party integration |

---

### Q18: Forms and form handling (react-hook-form, Formik)

```tsx
// react-hook-form + Zod (modern, performant)
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});
type FormData = z.infer<typeof schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(data => fetch('/api/login', { method: 'POST', body: JSON.stringify(data) }))}>
      <input {...register('email')} placeholder="Email" />
      {errors.email && <span>{errors.email.message}</span>}
      <input type="password" {...register('password')} placeholder="Password" />
      <button disabled={isSubmitting} type="submit">Submit</button>
    </form>
  );
}

// Formik (battle-tested)
import { Formik, Form, Field, ErrorMessage } from 'formik';

function LoginFormik() {
  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      validate={values => { const e: Record<string, string> = {}; if (!values.email) e.email = 'Required'; return e; }}
      onSubmit={async (values, { setSubmitting }) => { await fetch('/api/login', ...); setSubmitting(false); }}
    >
      {({ isSubmitting }) => (
        <Form>
          <Field name="email" type="email" />
          <ErrorMessage name="email" component="span" />
          <button disabled={isSubmitting} type="submit">Submit</button>
        </Form>
      )}
    </Formik>
  );
}
```

---

### Q19: Event handling -- SyntheticEvent

React uses **SyntheticEvent**, a cross-browser wrapper around native DOM events.

```tsx
function EventDemo() {
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    console.log('Type:', e.type, 'Target:', e.target);
    console.log('Native:', e.nativeEvent);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log('Value:', e.target.value);
  };

  return (
    <form onSubmit={e => { e.preventDefault(); }}>
      <input onChange={handleChange} />
      <button onClick={handleClick}>Click</button>
    </form>
  );
}
```

Event pooling was removed in React 17. In React 16, SyntheticEvent properties were nullified after callback.

---

### Q20: Conditional rendering patterns

```tsx
function UserDashboard({ user, loading, error }: Props) {
  // 1. Ternary
  return <div>{user ? <Profile user={user} /> : <LoginButton />}</div>;

  // 2. && short-circuit
  return <div>
    {loading && <Spinner />}
    {error && <ErrorBanner message={error} />}
  </div>;

  // 3. Early return
  if (loading) return <Spinner />;
  if (error) return <ErrorPage error={error} />;
  if (!user) return <LoginPrompt />;
  return <Profile user={user} />;

  // 4. Object lookup
  const stepComponents = {
    info: <InfoStep />, payment: <PaymentStep />, done: <DoneStep />,
  } as const;
  return stepComponents[currentStep] || <p>Unknown step</p>;
}
```

---

### Q21: List rendering and keys

```tsx
function ListExamples() {
  const items = [{ id: 1, text: 'Learn React' }, { id: 2, text: 'Build' }];
  return <ul>{items.map(item => <li key={item.id}>{item.text}</li>)}</ul>;
}

// Keyed fragments
function Glossary({ items }: { items: { term: string; def: string }[] }) {
  return <dl>{items.map(item => (
    <React.Fragment key={item.term}>
      <dt>{item.term}</dt>
      <dd>{item.def}</dd>
    </React.Fragment>
  ))}</dl>;
}
```

---

### Q22: Error boundaries

Error boundaries catch JS errors in child component tree. Must be class components.

```tsx
class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  state = { hasError: false };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    logErrorToService(error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <h1>Something went wrong</h1>;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<p>Section crashed</p>}>
  <UserProfile userId={123} />
</ErrorBoundary>
```

**What error boundaries DON'T catch:** Event handlers (use try/catch), async code, SSR errors, errors in the boundary itself.

**With react-error-boundary library:**
```tsx
import { ErrorBoundary } from 'react-error-boundary';

function Fallback({ error, resetErrorBoundary }: { error: Error; resetErrorBoundary: () => void }) {
  return <div role="alert"><p>{error.message}</p><button onClick={resetErrorBoundary}>Try again</button></div>;
}

<ErrorBoundary FallbackComponent={Fallback}>
  <UserProfile />
</ErrorBoundary>
```

---

### Q23: React Portals -- use cases

Portals render children into a different DOM node outside the parent hierarchy.

```tsx
import { createPortal } from 'react-dom';

function Modal({ open, onClose, children }: { open: boolean; onClose: () => void; children: React.ReactNode }) {
  if (!open) return null;
  return createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>{children}</div>
    </div>,
    document.getElementById('modal-root')!
  );
}
```

**Use cases:** Modals (avoids z-index/overflow issues), tooltips, dropdowns, notifications, context menus.

---

### Q24: Render props pattern

```tsx
interface DataProviderProps<T> {
  url: string;
  children: (state: { data: T | null; loading: boolean; error: Error | null }) => React.ReactNode;
}

function DataProvider<T>({ url, children }: DataProviderProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData).catch(setError).finally(() => setLoading(false));
  }, [url]);

  return <>{children({ data, loading, error })}</>;
}

// Usage
<DataProvider<User> url="/api/user">
  {({ data, loading, error }) => {
    if (loading) return <Spinner />;
    if (error) return <Error message={error.message} />;
    return <div>{data?.name}</div>;
  }}
</DataProvider>
```

---

### Q25: Higher-Order Components (HOCs)

HOC: a function that takes a component and returns an enhanced component.

```tsx
function withAuth<P extends object>(Component: React.ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const { user, loading } = useAuth();
    if (loading) return <Spinner />;
    if (!user) return <Redirect to="/login" />;
    return <Component {...props} user={user} />;
  };
}

const DashboardPage = withAuth(Dashboard);

// Compose HOCs
const EnhancedDashboard = withLogging(withAuth(Dashboard));
```

HOCs have been largely replaced by hooks for logic sharing, but still used in some libraries (Redux `connect`, React Router v5 `withRouter`).

---

### Q26: React Fragment

```tsx
// Without Fragment -- unnecessary wrapper div (bad for <table>)
function Table() {
  return <div><td>Name</td><td>Age</td></div>; // invalid HTML
}

// With Fragment
function Table() {
  return <><td>Name</td><td>Age</td></>; // correct
}

// Keyed fragments (for lists)
{items.map(item => <React.Fragment key={item.id}>
  <dt>{item.term}</dt>
  <dd>{item.def}</dd>
</React.Fragment>)}
```

**Why fragments:** Avoid invalid HTML, reduce DOM nodes. `<>` can't take keys or attributes.

---

### Q27: `createRef` vs `useRef` vs `forwardRef`

```tsx
// useRef -- functional component
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);
  return <input ref={inputRef} />;
}

// createRef -- class component
class MyInput extends React.Component {
  inputRef = React.createRef<HTMLInputElement>();
  componentDidMount() { this.inputRef.current?.focus(); }
  render() { return <input ref={this.inputRef} />; }
}

// forwardRef -- pass ref to child
const FancyInput = React.forwardRef<HTMLInputElement, { label: string }>(
  (props, ref) => <div><label>{props.label}</label><input ref={ref} /></div>
);

function Parent() {
  const ref = useRef<HTMLInputElement>(null);
  useEffect(() => { ref.current?.focus(); }, []);
  return <FancyInput ref={ref} label="Name" />;
}
```

---

### Q28: React DevTools

Browser extension for inspecting React component trees.

**Components tab:** View tree, props, state, hooks.
**Profiler tab:** Record render performance (flamegraph, ranked chart).

```tsx
import { Profiler } from 'react';

function onRender(id: string, phase: string, actualDuration: number) {
  console.log(`${id} took ${actualDuration}ms`);
}

<Profiler id="App" onRender={onRender}>
  <Main />
</Profiler>
```

---

### Q29: Testing React components (React Testing Library + Jest)

```tsx
// Component
function Counter({ initial = 0 }: { initial?: number }) {
  const [count, setCount] = useState(initial);
  return (
    <div>
      <p data-testid="count">Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}

// Test
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('Counter', () => {
  it('renders and increments', async () => {
    render(<Counter initial={0} />);
    expect(screen.getByTestId('count')).toHaveTextContent('Count: 0');

    await userEvent.click(screen.getByRole('button', { name: /increment/i }));
    expect(screen.getByTestId('count')).toHaveTextContent('Count: 1');
  });
});

// Testing hooks
import { renderHook, act } from '@testing-library/react';

it('increments', () => {
  const { result } = renderHook(() => useCounter(0));
  act(() => result.current.increment());
  expect(result.current.count).toBe(1);
});
```

---

### Q30: React 18 features

```tsx
// 1. Automatic batching (even in timeouts/promises)
function AutoBatching() {
  const [count, setCount] = useState(0);
  const [flag, setFlag] = useState(false);
  function handleClick() {
    setTimeout(() => {
      setCount(c => c + 1); // batched with below (React 18)
      setFlag(f => !f);     // single re-render
    }, 100);
  }
  return <button onClick={handleClick}>Count: {count}</button>;
}

// 2. Transitions (mark non-urgent updates)
const [isPending, startTransition] = useTransition();
startTransition(() => setSearchResults(filterExpensive(query)));

// 3. Suspense (declarative loading states)
<Suspense fallback={<Spinner />}>
  <UserProfile userId={123} />
</Suspense>

// 4. useDeferredValue -- defer updating a value
const deferredQuery = useDeferredValue(query);

// 5. useId -- unique IDs for SSR accessibility
const id = useId();
<input id={id} /> <label htmlFor={id}>Name</label>

// 6. useSyncExternalStore -- for external stores
const state = useSyncExternalStore(store.subscribe, store.getSnapshot);

// 7. createRoot
const root = createRoot(document.getElementById('root')!);
root.render(<App />);
```

---

### Q31: React Server Components (RSC)

Server Components run on the server, never on the client. They reduce bundle size.

```tsx
// ServerComponent (default in Next.js App Router)
async function Note({ id }: { id: string }) {
  const note = await db.notes.findUnique({ where: { id } });
  return <article><h1>{note.title}</h1><div>{note.content}</div></article>;
}

// Client component -- "use client" directive
'use client';
function LikeButton({ noteId }: { noteId: string }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>{liked ? 'Heart' : 'HeartOutline'}</button>;
}
```

**Benefits:** Zero client JS for server components, direct DB access, auto code-splitting, smaller bundle.

---

### Q32: What does StrictMode do?

Development-only wrapper that:
1. **Double-invokes effects** (mount -> unmount -> mount) to detect missing cleanup.
2. **Double-invokes state updaters/reducers** to detect impure logic.
3. **Checks for deprecated APIs** (`componentWillMount`, `findDOMNode`).
4. **Warns about legacy string refs** and `contextTypes`.

```tsx
<StrictMode><Main /></StrictMode>
```

**No impact on production builds.**

---

### Q33: Reconciliation / diffing algorithm

1. **Different element types** -> tear down old tree, build new one.
2. **Same element type** -> update existing instance, keep DOM node.
3. **Keys** -> match children by key, not position.
4. **Depth-first traversal** -- React walks tree recursively.

```tsx
// Different types -> full rebuild
// <div><Counter /></div> -> <span><Counter /></span> (Counter destroyed!)

// Same type -> update in place
// <div className="old" /> -> <div className="new" /> (just update className)

// Keys -- match by key, reorder vs destroy+recreate
```

**Complexity:** O(n). Without heuristics, optimal diffing is O(n^3).

---

### Q34: Fiber architecture

Fiber is React 16's reconciliation engine. Each fiber is a unit of work.

```tsx
// Simplified fiber structure
interface Fiber {
  tag: WorkTag;         // FunctionComponent, ClassComponent, HostComponent
  type: any;            // Component type
  key: string | null;
  stateNode: any;       // DOM node or instance
  child: Fiber | null;  // First child
  sibling: Fiber | null;// Next sibling
  return: Fiber | null; // Parent
  memoizedState: any;   // Hook state queue
  alternate: Fiber | null; // Work-in-progress link
}
```

**Fiber enables:** Incremental rendering, prioritization (user input > data fetch), pausing/resuming, concurrent features.

**Render phase** (reconcile, interruptible) -> **Commit phase** (DOM mutation, synchronous).

---

### Q35: Error handling patterns in React

```tsx
// 1. Error Boundaries (class components)
// 2. Try/catch in event handlers
async function handleDelete() {
  try { await deleteItem(id); } catch (e) { toast.error('Failed'); }
}

// 3. useErrorHandler (react-error-boundary)
import { useErrorHandler } from 'react-error-boundary';
function DataFetcher({ url }: { url: string }) {
  const handleError = useErrorHandler();
  useEffect(() => { fetch(url).then(r => r.json()).then(setData).catch(handleError); }, [url]);
}

// 4. Global error handling
window.addEventListener('error', (event) => logError(event.error));
window.addEventListener('unhandledrejection', (event) => logError(event.reason));
```

---

### Q36: `useLayoutEffect` vs `useEffect`

| | `useEffect` | `useLayoutEffect` |
|---|---|---|
| Timing | After paint (async) | Before paint (sync) |
| Use case | Side effects, API calls | DOM measurements, mutations |
| Default | Use this | Only when needed |

```tsx
useLayoutEffect(() => {
  // Measure DOM before paint -- no flicker
  setHeight(divRef.current.getBoundingClientRect().height);
}, []);
```

---

### Q37: How does React handle events across browsers?

React's `SyntheticEvent` wraps the native event and normalizes behavior cross-browser.

**Event delegation:** React attaches event listeners to the root DOM node (React 17+) or document (React 16-). One listener per event type.

**Benefits:** Cross-browser consistency, performance (one listener vs many), memory efficient.

---

### Q38: The `children` prop

```tsx
function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return <div className="card"><h2>{title}</h2><div>{children}</div></div>;
}

// Children can be: string, JSX, array, function, expression, undefined/null
<Card title="Welcome"><p>Content</p><button>Click</button></Card>
```

---

### Q39: Side effects in React

```tsx
function SideEffects({ userId }: { userId: string }) {
  // 1. Data fetching
  useEffect(() => {
    const controller = new AbortController();
    fetch(`/api/user/${userId}`, { signal: controller.signal }).then(...);
    return () => controller.abort();
  }, [userId]);

  // 2. Subscriptions
  useEffect(() => {
    const sub = eventSource.subscribe(userId, setData);
    return () => sub.unsubscribe();
  }, [userId]);

  // 3. DOM
  useEffect(() => { document.title = `User ${userId}`; return () => { document.title = 'App'; }; }, [userId]);

  // 4. Timers
  useEffect(() => { const id = setInterval(refresh, 30000); return () => clearInterval(id); }, []);

  // 5. Analytics
  useEffect(() => { analytics.track('Viewed', { userId }); }, [userId]);
}
```

---

### Q40: Controlled vs uncontrolled -- recap

| Aspect | Controlled | Uncontrolled |
|--------|-----------|-------------|
| State | React state | DOM (ref) |
| Value source | `value` prop | `defaultValue` + `ref` |
| Validation | Easy | Difficult |
| Dynamic fields | Yes | No |
| File input | Always uncontrolled | Yes |

---

### Q41: `createPortal` detailed

```tsx
function Dropdown({ trigger, children }: { trigger: React.ReactNode; children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLDivElement>(null);
  const [pos, setPos] = useState({ top: 0, left: 0 });

  useEffect(() => {
    if (open && triggerRef.current) {
      const rect = triggerRef.current.getBoundingClientRect();
      setPos({ top: rect.bottom, left: rect.left });
    }
  }, [open]);

  return (
    <>
      <div ref={triggerRef} onClick={() => setOpen(!open)}>{trigger}</div>
      {open && createPortal(
        <div style={{ position: 'fixed', top: pos.top, left: pos.left }} className="dropdown">
          {children}
        </div>,
        document.body
      )}
    </>
  );
}
```

Events bubble through React tree, not DOM tree.

---

### Q42: `dangerouslySetInnerHTML`

```tsx
function RichContent({ html }: { html: string }) {
  return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(html) }} />;
}
```

Always sanitize HTML before rendering. Prefer markdown renderers or rich text libraries instead.

---

### Q43: Prop drilling and solutions

```tsx
// Prop drilling
function App() { const [user, setUser] = useState(null); return <Layout user={user} setUser={setUser} />; }
function Layout({ user, setUser }) { return <Sidebar user={user} setUser={setUser} />; }
function Sidebar({ user, setUser }) { return <UserAvatar user={user} setUser={setUser} />; }

// Solutions:
// 1. Context API
// 2. Component composition
function App() {
  const [user, setUser] = useState(null);
  return <Layout><Sidebar><UserAvatar user={user} setUser={setUser} /></Sidebar></Layout>;
}
// 3. State management library
```

---

### Q44: Synthetic events

Covered in Q19/Q37. Cross-browser wrapper. Event pooling removed in React 17.

---

### Q45: `useImperativeHandle`

```tsx
interface FancyInputHandle { focus: () => void; clear: () => void; shake: () => void; }

const FancyInput = forwardRef<FancyInputHandle, { label: string }>((props, ref) => {
  const inputRef = useRef<HTMLInputElement>(null);
  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    clear: () => { if (inputRef.current) inputRef.current.value = ''; },
    shake: () => { inputRef.current?.classList.add('shake'); setTimeout(() => inputRef.current?.classList.remove('shake'), 500); },
  }), []);
  return <div><label>{props.label}</label><input ref={inputRef} /></div>;
});

// Parent: inputRef.current?.focus()
```

---

### Q46: `useDebugValue`

```tsx
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  useEffect(() => {
    const handle = () => setIsOnline(navigator.onLine);
    window.addEventListener('online', handle);
    window.addEventListener('offline', handle);
    return () => { window.removeEventListener('online', handle); window.removeEventListener('offline', handle); };
  }, []);
  useDebugValue(isOnline ? 'Online' : 'Offline');
  return isOnline;
}
// Shows label in React DevTools
```

---

### Q47: Optimizing context to avoid re-renders

```tsx
// BAD -- monolithic context: any change re-renders all consumers

// Solution 1: Split contexts
const ThemeContext = createContext<ThemeType>(null!);
const UserContext = createContext<UserType>(null!);

// Solution 2: Memoize value
const value = useMemo(() => ({ state, dispatch }), [state]);

// Solution 3: Split read/write contexts
const CountContext = createContext(0);
const DispatchContext = createContext<React.Dispatch<Action>>(() => {});
// Components that only dispatch won't re-render on count change
```

---

### Q48: `useSyncExternalStore`

```tsx
// React 18 hook for subscribing to external stores
function useWindowWidth() {
  return useSyncExternalStore(
    (callback) => { window.addEventListener('resize', callback); return () => window.removeEventListener('resize', callback); },
    () => window.innerWidth,
    () => 1024 // server snapshot (SSR)
  );
}

// For stores that can change between renders (iframes)
```

---

### Q49: `useEffect(fn, [])` vs `useEffect(fn)`

| | `useEffect(fn, [])` | `useEffect(fn)` |
|---|---|---|
| Runs on mount | Yes | Yes |
| Runs on update | No | Yes |
| Class equivalent | `componentDidMount` + `componentWillUnmount` | `componentDidMount` + `componentDidUpdate` |

---

### Q50: Creating refs: class vs functional

```tsx
// Class: createRef
inputRef = React.createRef<HTMLInputElement>();
<input ref={this.inputRef} />

// Functional: useRef
const inputRef = useRef<HTMLInputElement>(null);
<input ref={inputRef} />

// Callback ref (both)
const measureRef = useCallback((node: HTMLDivElement | null) => {
  if (node) setHeight(node.getBoundingClientRect().height);
}, []);
<div ref={measureRef} />
```

---

### Q51: `useReducer` with complex state

```tsx
interface UserState {
  profile: Profile | null;
  posts: Post[];
  loading: boolean;
  error: string | null;
}

type UserAction =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; profile: Profile; posts: Post[] }
  | { type: 'FETCH_ERROR'; error: string }
  | { type: 'ADD_POST'; post: Post };

function userReducer(state: UserState, action: UserAction): UserState {
  switch (action.type) {
    case 'FETCH_START': return { ...state, loading: true, error: null };
    case 'FETCH_SUCCESS': return { ...state, loading: false, profile: action.profile, posts: action.posts };
    case 'FETCH_ERROR': return { ...state, loading: false, error: action.error };
    case 'ADD_POST': return { ...state, posts: [action.post, ...state.posts] };
    default: return state;
  }
}

function UserDashboard() {
  const [state, dispatch] = useReducer(userReducer, initialState);
  // dispatch({ type: 'FETCH_START' }) etc.
}
```

---

### Q52: `React.cloneElement`

```tsx
function RadioGroup({ children, name }: { children: React.ReactElement[]; name: string }) {
  const [selected, setSelected] = useState('');
  return <div>{React.Children.map(children, child => React.cloneElement(child, {
    name, checked: child.props.value === selected,
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => setSelected(e.target.value),
  }))}</div>;
}
```

---

### Q53: `React.Children` utilities

```tsx
React.Children.map(children, fn)       // Map over children
React.Children.forEach(children, fn)   // Iterate
React.Children.count(children)         // Count
React.Children.only(children)          // Assert single child
React.Children.toArray(children)       // Flatten with keys

// React.Children.map handles fragments and nested arrays correctly vs Array.map
```

---

### Q54: Element vs Component vs Instance

```tsx
// Component: function/class that returns JSX
function Button({ label }: { label: string }) { return <button>{label}</button>; }

// Element: output of component/JSX -- plain object { type: Button, props: { label: 'Click' } }
const buttonElement = <Button label="Click" />;

// Instance: rendered instance in tree (fiber node for function components)
```

---

### Q55: React 18 automatic batching

```tsx
function BatchDemo() {
  const [count, setCount] = useState(0);
  const [flag, setFlag] = useState(false);

  // All batched into single re-render in React 18 (even in promises, timeouts, native events)
  const handleAsync = () => {
    fetch('/api/data').then(() => {
      setCount(c => c + 1);
      setFlag(f => !f); // single re-render (was 2 in React 17)
    });
  };
}

// Opt out of batching: ReactDOM.flushSync(() => { setCount(c => c+1); });
```

---

### Q56: `useEvent` (React 19)

```tsx
// Stable function reference that always reads latest props/state
// Coming in React 19
const onMessage = useEvent((msg: string) => {
  console.log(`Message from ${selectedUser}:`, msg); // always latest selectedUser
  setMessages(prev => [...prev, msg]);
});

useEffect(() => {
  const sub = chatAPI.subscribe(selectedUser, onMessage);
  return () => sub.unsubscribe();
}, [selectedUser]);
```

---

### Q57: `useOptimistic` (React 19)

```tsx
function MessageForm() {
  const [messages, setMessages] = useState<string[]>([]);
  const [optimisticMessages, addOptimistic] = useOptimistic(
    messages,
    (state, newMessage: string) => [...state, newMessage]
  );

  async function sendMessage(formData: FormData) {
    const message = formData.get('message') as string;
    addOptimistic(message); // show immediately
    const res = await fetch('/api/messages', { method: 'POST', body: formData });
    if (res.ok) setMessages(prev => [...prev, message]);
    // else optimistic update auto-rolls back
  }

  return <form action={sendMessage}>...</form>;
}
```

---

### Q58: Testing custom hooks

```tsx
import { renderHook, act } from '@testing-library/react';

it('increments and resets', () => {
  const { result } = renderHook(() => useCounter(0));

  act(() => { result.current.increment(); result.current.increment(); });
  expect(result.current.count).toBe(2);

  act(() => { result.current.reset(); });
  expect(result.current.count).toBe(0);
});
```

---

### Q59: Side effects on unmount

```tsx
function SubscriptionManager({ userId }: { userId: string }) {
  useEffect(() => {
    const socket = new WebSocket(`ws://example.com/user/${userId}`);
    socket.onmessage = handleMessage;
    return () => socket.close(); // cleanup on unmount
  }, [userId]);

  // Global cleanup (runs only on unmount)
  useEffect(() => { return () => analytics.flush(); }, []);
}
```

---

### Q60: `displayName`

```tsx
const Button = React.forwardRef<HTMLButtonElement, { label: string }>((props, ref) => (
  <button ref={ref}>{props.label}</button>
));
Button.displayName = 'Button'; // Shows "Button" in DevTools

// HOC displayName
function withAuth<P>(Component: React.ComponentType<P>) {
  function WithAuth(props: P) { return <Component {...props} />; }
  WithAuth.displayName = `WithAuth(${Component.displayName || Component.name || 'Component'})`;
  return WithAuth;
}
```

---

### Q61: Controlled vs uncontrolled inputs

Covered in Q17/Q40.

---

### Q62: `useTransition`

```tsx
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<string[]>([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value); // URGENT
    startTransition(() => setResults(expensiveFilter(allItems, e.target.value))); // NON-URGENT
  };

  return (
    <div>
      <input value={query} onChange={handleChange} />
      {isPending ? <Spinner /> : <Results list={results} />}
    </div>
  );
}
```

Transitions are interruptible. Old results remain visible during transition (no flicker).

---

### Q63: `useDeferredValue` vs `useTransition`

```tsx
// useTransition: wraps state updates in startTransition
startTransition(() => setSearchResults(results));

// useDeferredValue: wraps a value (same effect, different approach)
const deferredQuery = useDeferredValue(query);
const results = expensiveFilter(items, deferredQuery);

// useDeferredValue is useful when you can't control the update source
```

---

### Q64: Forms with multiple fields

```tsx
function RegistrationForm() {
  const [form, setForm] = useState({
    username: '', email: '', password: '', confirmPassword: '',
  });
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };
  return (
    <form onSubmit={e => { e.preventDefault(); /* validate & submit */ }}>
      <input name="username" value={form.username} onChange={handleChange} />
      <input name="email" type="email" value={form.email} onChange={handleChange} />
      <input name="password" type="password" value={form.password} onChange={handleChange} />
      <button type="submit">Register</button>
    </form>
  );
}
```

---

### Q65: React 18 concurrent features

`useTransition`, `useDeferredValue`, Suspense, automatic batching, `useSyncExternalStore`, `useId`, `createRoot`.

---

### Q66: Server-side rendering with React

```tsx
// Server
import { renderToString } from 'react-dom/server';
const app = renderToString(<StaticRouter location={req.url}><App /></StaticRouter>);

// Client
import { hydrateRoot } from 'react-dom/client';
hydrateRoot(document.getElementById('root')!, <BrowserRouter><App /></BrowserRouter>);
```

---

### Q67: Hydration

**Hydration:** Attaching event handlers to server-rendered HTML.

**Mismatch example:**
```tsx
function TimeDisplay() {
  // Server time != client time
  return <div>{new Date().toISOString()}</div>;
}
```

**Fix:** Use `useEffect` for client-only content.

---

### Q68: `renderToString` vs `renderToPipeableStream`

| | `renderToString` | `renderToPipeableStream` |
|---|---|---|
| Output | Single string (blocks response) | Stream (progressive HTML) |
| TTFB | Slower | Faster |
| SEO | Full HTML at once | Yes (with `onAllReady`) |
| Suspense | Doesn't support | Supports streaming |

---

### Q69: Keys reconciliation

Covered in Q15, Q21, Q33. Stable + unique + predictable. Never `Math.random()`.

---

### Q70: `useInsertionEffect`

```tsx
// For CSS-in-JS library authors
// Fires synchronously BEFORE any DOM mutations
// Don't read DOM or set state here

useInsertionEffect(() => {
  const style = document.createElement('style');
  style.textContent = `.dynamic-class { color: red; }`;
  document.head.appendChild(style);
  return () => style.remove();
}, []);
```

Order: `useInsertionEffect` -> `useLayoutEffect` -> `useEffect`

---

### Q71: Shallow vs deep comparison

```tsx
// Shallow: reference equality (=== for each prop) -- React default
// Deep: value equality (expensive)

React.memo(Comp); // shallow comparison by default
React.memo(Comp, (prev, next) => deepEqual(prev, next)); // custom deep (rare)
```

---

### Q72: Global state without Redux (medium app)

```tsx
// 1. Context + useReducer
// 2. Zustand (minimal)
// 3. React Query for server state

// Zustand example
import { create } from 'zustand';
const useStore = create<Store>(set => ({
  user: null, setUser: (user) => set({ user }),
  theme: 'light', toggleTheme: () => set(s => ({ theme: s.theme === 'light' ? 'dark' : 'light' })),
}));

function Navbar() {
  const user = useStore(s => s.user);
  const theme = useStore(s => s.theme);
  return <div className={theme}>{user?.name}</div>;
}
```

---

### Q73: Custom hook for data fetching

```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();
    setLoading(true);
    fetch(url, { signal: controller.signal })
      .then(r => r.json())
      .then(d => { if (!cancelled) { setData(d); setLoading(false); } })
      .catch(e => { if (!cancelled && e.name !== 'AbortError') { setError(e); setLoading(false); } });
    return () => { cancelled = true; controller.abort(); };
  }, [url]);

  return { data, loading, error };
}
```

---

### Q74: `useRef` with TypeScript

```tsx
const inputRef = useRef<HTMLInputElement>(null!);
const countRef = useRef<number>(0);

// forwardRef with TypeScript
const FancyInput = forwardRef<HTMLInputElement, { label: string }>(
  ({ label, error }, ref) => (
    <div><label>{label}</label><input ref={ref} aria-invalid={!!error} /></div>
  )
);
```

---

### Q75: Component lifecycle phases

1. **Mount:** constructor/useState -> render -> componentDidMount/useEffect(fn, [])
2. **Update:** shouldComponentUpdate/React.memo -> render -> componentDidUpdate/useEffect(fn, [deps])
3. **Unmount:** componentWillUnmount/useEffect cleanup
4. **Error:** getDerivedStateFromError + componentDidCatch

---

### Q76: setState inside useEffect

```tsx
// Infinite loop (no deps -> re-render -> useEffect -> setState -> re-render)
useEffect(() => { setCount(count + 1); });

// Fix: empty deps or functional update + condition
useEffect(() => { setCount(prev => prev + 1); }, []);
useEffect(() => { if (count < 10) setCount(prev => prev + 1); }, [count]);
```

---

### Q77: Testing useEffect with async

```tsx
it('renders data after fetch', async () => {
  (global.fetch as Mock).mockResolvedValueOnce({
    ok: true, json: () => Promise.resolve({ name: 'John' }),
  });

  render(<DataFetcher url="/api/user" />);
  expect(screen.getByTestId('loading')).toBeInTheDocument();
  await waitFor(() => expect(screen.getByTestId('data')).toHaveTextContent('John'));
});
```

---

### Q78: `isPending` flag in `useTransition`

Indicates a transition is in progress. Shows spinner or disables UI without blocking urgent updates.

---

### Q79: Force re-render

```tsx
// 1. useReducer trick
const [, forceUpdate] = useReducer(x => x + 1, 0);

// 2. useState dummy
const [, setTick] = useState(0);
const forceUpdate = () => setTick(t => t + 1);

// 3. Class: this.forceUpdate()

// 4. Key trick (remount)
<ExpensiveComponent key={key} />
```

---

### Q80: How React renders different types in JSX

```tsx
// Renders nothing: {undefined} {null} {false} {true}
// Renders: {0} renders "0" -- trap with &&
// Renders: {[<span>a</span>, <span>b</span>]} -- array
// Renders: {42} 'hello' -- numbers/strings
// Error: {{ key: 'value' }} -- objects not valid as React child
```

---

### Q81: Rules for keys

Unique among siblings, stable, predictable. Not `Math.random()`. Not index for dynamic lists.

---

### Q82: Callback ref pattern

```tsx
function MeasuredBox() {
  const [height, setHeight] = useState(0);
  const measureRef = useCallback((node: HTMLDivElement | null) => {
    if (node) setHeight(node.getBoundingClientRect().height);
  }, []);
  return <div ref={measureRef}>Height: {height}px</div>;
}
```

Called on mount (DOM element), unmount (null), and ref change.

---

### Q83: Child to parent communication

```tsx
function Parent() {
  const [data, setData] = useState('');
  return <Child onSend={setData} />;
}
function Child({ onSend }: { onSend: (d: string) => void }) {
  return <button onClick={() => onSend('hello')}>Send</button>;
}
```

---

### Q84: `componentDidMount` vs `useEffect(fn, [])`

`useEffect` runs after paint (async). `componentDidMount` runs before paint during commit. `useLayoutEffect` is closer to `componentDidMount`.

---

### Q85: Animations in React

```tsx
// CSS transitions
// Framer Motion
import { motion, AnimatePresence } from 'framer-motion';
<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} />

// react-spring
const springs = useSpring({ from: { opacity: 0 }, to: { opacity: 1 } });
<animated.div style={springs} />
```

---

### Q86: Key prop in conditional rendering

```tsx
// Without keys: React reuses component -- input state preserved
// With keys: React destroys and recreates -- input state reset

{isAdmin ? <AdminForm key="admin" /> : <UserForm key="user" />}
```

---

### Q87: `useRef` vs regular variable

```tsx
// Regular variable resets every render
let regular = 0; regular += 1; // Always 1

// Ref persists across renders
const refCount = useRef(0); refCount.current += 1; // 1, 2, 3...
```

---

### Q88: `useMemo` vs `useCallback` equivalence

```tsx
// These are equivalent:
const fn = useCallback(() => doSomething(a, b), [a, b]);
const fn = useMemo(() => () => doSomething(a, b), [a, b]);
```

---

### Q89: Scroll-based animations

```tsx
function ScrollAnimation() {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.unobserve(entry.target); } },
      { threshold: 0.1 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return <div ref={ref} className={`fade-in ${visible ? 'visible' : ''}`}>Content</div>;
}
```

---

### Q90: `useEffect` best practices

1. Provide proper dependencies.
2. Use cleanup functions.
3. Don't use `useEffect` for computations (use `useMemo`).
4. Don't use `useEffect` for event handlers.
5. Extract complex logic into custom hooks.
6. Use functional state updates when new state depends on old.
7. Use `useLayoutEffect` for DOM measurements.

---

### Q91: Sharing logic with custom hooks

```tsx
function useWindowSize() {
  const [size, setSize] = useState({ width: window.innerWidth, height: window.innerHeight });
  useEffect(() => {
    const handle = () => setSize({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener('resize', handle);
    return () => window.removeEventListener('resize', handle);
  }, []);
  return size;
}

// Reused across components
function ResponsiveSidebar() {
  const { width } = useWindowSize();
  return width < 768 ? <MobileSidebar /> : <DesktopSidebar />;
}
```

---

### Q92: `useRef` DOM relationships

Covered in Q8. React sets `ref.current` to DOM node on mount, `null` on unmount.

---

### Q93: Implementing a modal

```tsx
function Modal({ open, onClose, children }: { open: boolean; onClose: () => void; children: React.ReactNode }) {
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    document.addEventListener('keydown', handler);
    document.body.style.overflow = 'hidden';
    return () => { document.removeEventListener('keydown', handler); document.body.style.overflow = ''; };
  }, [open, onClose]);

  if (!open) return null;
  return createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button onClick={onClose}>x</button>
        {children}
      </div>
    </div>,
    document.getElementById('modal-root')!
  );
}
```

---

### Q94: Compound components

```tsx
const TabsContext = createContext<{ activeTab: string; setActiveTab: (tab: string) => void }>(null!);

function Tabs({ defaultTab, children }: { defaultTab: string; children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return <TabsContext.Provider value={{ activeTab, setActiveTab }}>{children}</TabsContext.Provider>;
}

function Tab({ value, children }: { value: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  return <button role="tab" aria-selected={activeTab === value} onClick={() => setActiveTab(value)}>{children}</button>;
}

function TabPanel({ value, children }: { value: string; children: React.ReactNode }) {
  const { activeTab } = useContext(TabsContext);
  if (activeTab !== value) return null;
  return <div role="tabpanel">{children}</div>;
}

<Tabs defaultTab="profile">
  <Tab value="profile">Profile</Tab>
  <Tab value="settings">Settings</Tab>
  <TabPanel value="profile">Profile content</TabPanel>
  <TabPanel value="settings">Settings content</TabPanel>
</Tabs>
```

---

### Q95: State vs Ref

| | `useState` | `useRef` |
|---|---|---|
| Re-render | Yes | No |
| Mutability | Via setter | `current` directly |
| Use cases | UI state | DOM refs, mutable values |

---

### Q96: Measuring DOM elements

```tsx
// useLayoutEffect (sync, before paint)
useLayoutEffect(() => {
  if (ref.current) setDimensions({
    width: ref.current.offsetWidth, height: ref.current.offsetHeight,
  });
}, []);

// ResizeObserver (reacts to size changes)
useEffect(() => {
  const observer = new ResizeObserver(entries => {
    setSize(entries[0].contentRect);
  });
  if (ref.current) observer.observe(ref.current);
  return () => observer.disconnect();
}, []);
```

---

### Q97: Focus management

```tsx
// Auto-focus
const emailRef = useRef<HTMLInputElement>(null);
useEffect(() => emailRef.current?.focus(), []);

// Focus trap in modal -- cycle Tab between first/last focusable elements
```

---

### Q98: Accordion component

```tsx
function Accordion({ items }: { items: { title: string; content: string }[] }) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);
  return <div>{items.map((item, i) => (
    <div key={i}>
      <button onClick={() => setOpenIndex(openIndex === i ? null : i)} aria-expanded={openIndex === i}>
        {item.title}
      </button>
      {openIndex === i && <div>{item.content}</div>}
    </div>
  ))}</div>;
}
```

---

### Q99: Debounce in React

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debouncedValue;
}

function SearchBox() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);
  useEffect(() => { if (debouncedQuery) fetchResults(debouncedQuery); }, [debouncedQuery]);
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

---

### Q100: Keyboard events

```tsx
function handleKeyDown(e: React.KeyboardEvent) {
  if (e.key === 'Enter') submit();
  if (e.key === 'Escape') cancel();
  if (e.key === ' ' || e.key === 'Space') toggle();
  if (e.key === 'ArrowDown') moveDown();
  if (e.ctrlKey && e.key === 's') { e.preventDefault(); save(); }
}

// Global keyboard listener
useEffect(() => {
  const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') closeModal(); };
  window.addEventListener('keydown', handler);
  return () => window.removeEventListener('keydown', handler);
}, []);
```

---

### Q101: Browser back/forward in SPA

```tsx
import { useNavigate } from 'react-router-dom';

function NavigationHandler() {
  const navigate = useNavigate();

  const goBack = () => {
    if (hasUnsavedChanges && !window.confirm('Leave without saving?')) return;
    navigate(-1);
  };

  return <button onClick={goBack}>Back</button>;
}
```

---

### Q102: Infinite scrolling

```tsx
function InfiniteScroll() {
  const [items, setItems] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const loaderRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting && hasMore && !loading) setPage(p => p + 1); },
      { threshold: 0.1 }
    );
    if (loaderRef.current) observer.observe(loaderRef.current);
    return () => observer.disconnect();
  }, [hasMore, loading]);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/items?page=${page}`).then(r => r.json()).then(data => {
      setItems(prev => [...prev, ...data.items]);
      setHasMore(data.hasMore);
      setLoading(false);
    });
  }, [page]);

  return <div>
    {items.map((item, i) => <div key={i}>{item}</div>)}
    {loading && <Spinner />}
    {hasMore && <div ref={loaderRef} style={{ height: 1 }} />}
  </div>;
}
```

---

### Q103: Drag and drop

```tsx
// Native HTML5 drag and drop
function DragNDrop() {
  const [items, setItems] = useState(['A', 'B', 'C']);
  const dragItem = useRef<number | null>(null);

  const handleDragStart = (index: number) => { dragItem.current = index; };
  const handleDragOver = (e: React.DragEvent, index: number) => {
    e.preventDefault();
    if (dragItem.current === null || dragItem.current === index) return;
    const newItems = [...items];
    const [dragged] = newItems.splice(dragItem.current, 1);
    newItems.splice(index, 0, dragged);
    dragItem.current = index;
    setItems(newItems);
  };

  return <div>{items.map((item, i) => (
    <div key={item} draggable onDragStart={() => handleDragStart(i)} onDragOver={e => handleDragOver(e, i)}>
      {item}
    </div>
  ))}</div>;
}
```

---

### Q104: Custom dropdown component

Covered in full implementation. Key features: close on outside click, close on Escape, keyboard navigation, ARIA attributes.

---

### Q105: Toast/notification system

```tsx
const ToastContext = createContext<{ addToast: (msg: string, type: 'success' | 'error') => void }>(null!);

function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const addToast = useCallback((message: string, type: Toast['type']) => {
    const id = crypto.randomUUID();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 5000);
  }, []);
  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      <div className="toast-container">
        {toasts.map(t => <div key={t.id} className={`toast toast-${t.type}`}>{t.message}<button onClick={() => setToasts(p => p.filter(x => x.id !== t.id))}>x</button></div>)}
      </div>
    </ToastContext.Provider>
  );
}
```

---

### Q106: Media queries in React

```tsx
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => window.matchMedia(query).matches);
  useEffect(() => {
    const mql = window.matchMedia(query);
    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mql.addEventListener('change', handler);
    return () => mql.removeEventListener('change', handler);
  }, [query]);
  return matches;
}

// Usage
const isMobile = useMediaQuery('(max-width: 768px)');
```

---

### Q107: `useRef` vs `createRef`

`useRef` for functional components (persists across renders). `createRef` for class components.

---

### Q108: Async data with Suspense

```tsx
// React.lazy for code splitting
const LazyComponent = React.lazy(() => import('./HeavyComponent'));

<Suspense fallback={<Spinner />}>
  <LazyComponent />
</Suspense>

// With SWR/React Query (suspense mode)
function Profile({ userId }: { userId: string }) {
  const { data } = useSWR(`/api/users/${userId}`, fetcher, { suspense: true });
  return <div>{data.name}</div>;
}
```

---

### Q109: `React.lazy` with named exports

```tsx
// React.lazy expects default export
// For named exports, create an intermediary module:
export { MyComponent as default } from './MyComponent';
// Or inline:
const LazyComponent = React.lazy(() => import('./MyComponent').then(m => ({ default: m.MyComponent })));
```

---

### Q110: `React.memo` with TypeScript

```tsx
const MyComponent = React.memo(function MyComponent({ items }: { items: Item[] }) {
  return <div>{items.length}</div>;
});

// With custom comparator
const MyComponent = React.memo(
  ({ items }: { items: Item[] }) => <div>{items.length}</div>,
  (prev, next) => prev.items.length === next.items.length
);
```

---

### Q111: `useRef` for interval/timer cleanup

```tsx
function Timer() {
  const [count, setCount] = useState(0);
  const savedCallback = useRef<() => void>();

  useEffect(() => { savedCallback.current = () => setCount(c => c + 1); });

  useEffect(() => {
    const id = setInterval(() => savedCallback.current?.(), 1000);
    return () => clearInterval(id);
  }, []);
}
```

---

### Q112: What is `flushSync`?

```tsx
// React 18: force synchronous (unbatched) update
import { flushSync } from 'react-dom';

flushSync(() => setCount(c => c + 1)); // committed immediately
```

---

### Q113: How React handles whitespace and newlines in JSX

```tsx
// Newlines are collapsed into single spaces
// Leading/trailing whitespace trimmed
// Adjacent text nodes concatenated
```

---

### Q114: What is the `style` prop?

```tsx
// Inline styles use camelCase properties
<div style={{ backgroundColor: 'red', fontSize: '16px', marginTop: 10 }}>
  Styled content
</div>
```

---

### Q115: `className` vs `class` in JSX

Use `className` in JSX (the `class` attribute is reserved in JS).

```tsx
<div className="container">Content</div>
```

---

### Q116: How do you handle boolean HTML attributes?

```tsx
// React ignores boolean attribute values of `true`/`false`
// Use truthy/falsy expressions:
<button disabled={isSubmitting}>Submit</button>
<input type="checkbox" checked={isChecked} />
```

---

### Q117: What is `React.PureComponent`?

Class component equivalent of `React.memo`. Implements `shouldComponentUpdate` with shallow prop/state comparison.

```tsx
class MyComponent extends React.PureComponent<{ data: Item }> {
  render() { return <div>{this.props.data.name}</div>; }
}
```

---

### Q118: What are controlled form components?

Form elements whose value is controlled by React state. Every state mutation has an associated handler.

```tsx
<input value={val} onChange={e => setVal(e.target.value)} />
```

---

### Q119: What are uncontrolled form components?

Form elements that maintain their own state in the DOM. You read values via refs when needed.

```tsx
<input ref={inputRef} defaultValue="initial" />
```

---

### Q120: How do you implement a theme switcher?

```tsx
const ThemeContext = createContext<{ theme: string; toggleTheme: () => void }>(null!);

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState('light');
  const toggleTheme = useCallback(() => setTheme(t => t === 'light' ? 'dark' : 'light'), []);
  const value = useMemo(() => ({ theme, toggleTheme }), [theme]);

  useEffect(() => { document.documentElement.setAttribute('data-theme', theme); }, [theme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

function ThemeToggle() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  return <button onClick={toggleTheme}>Switch to {theme === 'light' ? 'dark' : 'light'}</button>;
}
```

---

## State Management (Q121–Q180)

### Q121: What is the props drilling problem?

When you pass props through multiple intermediate components that don't need them.

```tsx
// Props drilling: Layout and Sidebar don't use `user` -- just pass it through
<App> -> <Layout user={user}> -> <Sidebar user={user}> -> <UserAvatar user={user} />
```

---

### Q122: Solutions to props drilling

1. **Context API** -- provide/consume pattern.
2. **Component composition** -- lift children to avoid passing through intermediaries.
3. **State management library** -- Zustand, Redux, Jotai.
4. **Props collection** -- pass fewer props by restructuring.

---

### Q123: Context API -- pros and cons

**Pros:** Built-in, simple, no extra deps, good for low-frequency updates (theme, locale, auth).

**Cons:** All consumers re-render on any value change, not optimized for high-frequency updates, harder to test, doesn't support middleware.

---

### Q124: When to use Context API

- Theme, locale, auth (infrequent updates).
- Small to medium apps.
- Simple state without complex logic.

---

### Q125: Redux principles

1. **Single source of truth** -- store is a single object tree.
2. **State is read-only** -- changes via actions (objects with `type`).
3. **Pure reducers** -- `(state, action) => newState`, no side effects.

```tsx
// Action
{ type: 'INCREMENT', payload: 1 }

// Reducer (pure function)
function counterReducer(state = 0, action) {
  switch (action.type) {
    case 'INCREMENT': return state + action.payload;
    case 'DECREMENT': return state - action.payload;
    default: return state;
  }
}

// Store
const store = createStore(counterReducer);
store.dispatch({ type: 'INCREMENT', payload: 1 });
```

---

### Q126: Redux Toolkit vs classic Redux

| Aspect | Classic Redux | Redux Toolkit |
|--------|-------------|---------------|
| Boilerplate | High | Minimal |
| Setup | `createStore`, combineReducers | `configureStore` |
| Immutable updates | Manual spread/assign | `createSlice` with Immer |
| Middleware | Manual | `getDefaultMiddleware` included |
| Async | `redux-thunk` / `redux-saga` | `createAsyncThunk` |
| DevTools | Manual setup | Auto-enabled |

```tsx
// Redux Toolkit
import { createSlice, configureStore } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; }, // Immer handles immutability
    decrement: (state) => { state.value -= 1; },
    incrementByAmount: (state, action) => { state.value += action.payload; },
  },
});

export const { increment, decrement, incrementByAmount } = counterSlice.actions;

const store = configureStore({
  reducer: { counter: counterSlice.reducer },
});
```

---

### Q127: Zustand -- deep dive

```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface BearStore {
  bears: number;
  increase: (by?: number) => void;
  reset: () => void;
}

const useBearStore = create<BearStore>()(
  persist(
    (set) => ({
      bears: 0,
      increase: (by = 1) => set((state) => ({ bears: state.bears + by })),
      reset: () => set({ bears: 0 }),
    }),
    { name: 'bear-storage' }
  )
);

// In component
function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  const increase = useBearStore((state) => state.increase);
  return <div><span>{bears}</span><button onClick={() => increase()}>+</button></div>;
}
```

**Key features:** Minimal boilerplate, no provider needed, selector-based subscriptions (auto-optimized), middleware support, TypeScript first.

---

### Q128: Zustand vs Redux vs Context

| Aspect | Zustand | Redux | Context |
|--------|---------|-------|---------|
| Boilerplate | Minimal | Medium (RTK less) | Minimal |
| Provider needed | No | Yes | Yes |
| Selector optimization | Auto | Manual (Reselect) | None (all re-render) |
| Middleware | Yes (persist, immer, devtools) | Yes (thunk, saga, logger) | No |
| Bundle size | ~1KB | ~12KB | 0 (built-in) |
| DevTools | Yes | Yes | No |
| TypeScript | Excellent | Good | Good |

---

### Q129: Zustand stores, slices, middleware

```tsx
// Store with slices pattern
import { create } from 'zustand';
import { devtools, persist, immer } from 'zustand/middleware';

interface UserSlice { user: User | null; setUser: (user: User | null) => void; }
interface CartSlice { items: Item[]; addItem: (item: Item) => void; }

const useStore = create<UserSlice & CartSlice>()(
  devtools(
    persist(
      immer((set) => ({
        // User slice
        user: null,
        setUser: (user) => set({ user }),
        // Cart slice
        items: [],
        addItem: (item) => set((state) => { state.items.push(item); }), // immer allows mutation
      })),
      { name: 'app-storage' }
    )
  )
);
```

---

### Q130: Zustand with TypeScript

```tsx
import { create } from 'zustand';

interface CounterState {
  count: number;
  increment: () => void;
  decrement: () => void;
}

const useCounterStore = create<CounterState>()((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
}));

// Typed selector
const count = useCounterStore((s) => s.count);

// Typed actions
const { increment, decrement } = useCounterStore.getState();

// Subscribe with selector
useCounterStore.subscribe((state) => console.log('count:', state.count));
```

---

### Q131: Jotai and Recoil (atomic state management)

```tsx
// Jotai -- atomic state
import { atom, useAtom } from 'jotai';

const countAtom = atom(0);
const doubledAtom = atom((get) => get(countAtom) * 2); // derived atom

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const [doubled] = useAtom(doubledAtom);
  return <div>{count} x2 = {doubled}</div>;
}

// Recoil (Meta)
import { atom, useRecoilState, selector } from 'recoil';

const textState = atom({ key: 'textState', default: '' });
const charCountState = selector({
  key: 'charCountState',
  get: ({ get }) => get(textState).length,
});
```

---

### Q132: React Query / TanStack Query

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Fetch data
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetch(`/api/users/${userId}`).then(r => r.json()),
    staleTime: 5 * 60 * 1000, // 5 min
    gcTime: 30 * 60 * 1000, // cache persists (was cacheTime)
  });

  if (isLoading) return <Spinner />;
  return <div>{data.name}</div>;
}

// Mutate data
function AddTodo() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (newTodo) => fetch('/api/todos', { method: 'POST', body: JSON.stringify(newTodo) }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
  });

  return <button onClick={() => mutation.mutate({ text: 'New todo' })}>Add</button>;
}
```

**Key features:** Caching, background refetching, pagination, infinite queries, optimistic updates, SSR support.

---

### Q133: SWR

```tsx
import useSWR from 'swr';
import useSWRMutation from 'swr/mutation';

const fetcher = (url: string) => fetch(url).then(r => r.json());

function Profile({ userId }: { userId: string }) {
  const { data, error, isLoading, mutate } = useSWR(`/api/users/${userId}`, fetcher);

  const { trigger } = useSWRMutation(
    `/api/users/${userId}`,
    (url, { arg }: { arg: Partial<User> }) => fetch(url, { method: 'PATCH', body: JSON.stringify(arg) })
  );

  return (
    <div>
      {data?.name}
      <button onClick={() => trigger({ name: 'New Name' })}>Update</button>
    </div>
  );
}
```

---

### Q134: State normalization

Normalized state avoids duplication and makes updates easier.

```tsx
// Denormalized (nested) -- hard to update
{
  posts: [{ id: 1, comments: [{ id: 1, author: { id: 1 } }] }]
}

// Normalized (flat) -- easy to update
{
  posts: { 1: { id: 1, title: 'Post', commentIds: [1] } },
  comments: { 1: { id: 1, text: 'Comment', authorId: 1 } },
  users: { 1: { id: 1, name: 'John' } },
}
```

**Tools:** Redux Toolkit's `createEntityAdapter`, Zustand with manual normalization, or libraries like normalizr.

---

### Q135: Optimistic updates

```tsx
// Zustand optimistic update
const useStore = create<Store>((set, get) => ({
  todos: [],
  addTodoOptimistic: (text: string) => {
    const tempId = Date.now();
    // Optimistically add
    set((state) => ({ todos: [...state.todos, { id: tempId, text, status: 'saving' }] }));

    fetch('/api/todos', { method: 'POST', body: JSON.stringify({ text }) })
      .then(r => r.json())
      .then(serverTodo => {
        // Replace temp with server version
        set((state) => ({
          todos: state.todos.map(t => t.id === tempId ? { ...serverTodo, status: 'saved' } : t),
        }));
      })
      .catch(() => {
        // Rollback on error
        set((state) => ({ todos: state.todos.filter(t => t.id !== tempId) }));
        toast.error('Failed to save todo');
      });
  },
}));

// React Query optimistic update
const mutation = useMutation({
  mutationFn: (newTodo) => fetch('/api/todos', { method: 'POST', body: JSON.stringify(newTodo) }),
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previousTodos = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old: Todo[]) => [...old, { ...newTodo, id: 'temp', status: 'optimistic' }]);
    return { previousTodos };
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context?.previousTodos);
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
});
```

---

### Q136: Selectors and memoization (Reselect)

```tsx
import { createSelector } from '@reduxjs/toolkit';
// or from 'reselect'

interface RootState {
  todos: Todo[];
  filter: string;
}

const selectTodos = (state: RootState) => state.todos;
const selectFilter = (state: RootState) => state.filter;

// Memoized selector -- only recomputes when inputs change
const selectFilteredTodos = createSelector(
  [selectTodos, selectFilter],
  (todos, filter) => {
    console.log('Computing filtered todos'); // only runs when todos or filter change
    return todos.filter(t => t.text.includes(filter));
  }
);

// Usage in component
const filteredTodos = useSelector(selectFilteredTodos);
```

**Why memoization:** Prevents expensive recomputation when unrelated state changes.

---

### Q137: Middleware in state management

```tsx
// Redux middleware (logger example)
const loggerMiddleware = (store) => (next) => (action) => {
  console.log('dispatching', action);
  const result = next(action);
  console.log('next state', store.getState());
  return result;
};

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(loggerMiddleware),
});

// Zustand middleware
const logMiddleware = (config: StateCreator<Store>) => (set, get, api) =>
  config(
    (args) => {
      console.log('prev state:', get());
      set(args);
      console.log('next state:', get());
    },
    get,
    api
  );

const useStore = create<Store>()(logMiddleware(persist(immer((set) => ({
  // ...
})), { name: 'store' })));
```

---

### Q138: Redux Toolkit `createAsyncThunk`

```tsx
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUsers = createAsyncThunk('users/fetchUsers', async (_, { rejectWithValue }) => {
  try {
    const response = await fetch('/api/users');
    return await response.json();
  } catch (err) {
    return rejectWithValue(err.message);
  }
});

const usersSlice = createSlice({
  name: 'users',
  initialState: { items: [], loading: false, error: null },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchUsers.fulfilled, (state, action) => { state.loading = false; state.items = action.payload; })
      .addCase(fetchUsers.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});
```

---

### Q139: Redux `createEntityAdapter`

```tsx
import { createEntityAdapter, createSlice } from '@reduxjs/toolkit';

interface Todo { id: string; text: string; completed: boolean; }

const todosAdapter = createEntityAdapter<Todo>({
  selectId: (todo) => todo.id,
  sortComparer: (a, b) => a.text.localeCompare(b.text),
});

const todosSlice = createSlice({
  name: 'todos',
  initialState: todosAdapter.getInitialState({ loading: false }),
  reducers: {
    addTodo: todosAdapter.addOne,
    updateTodo: todosAdapter.updateOne,
    removeTodo: todosAdapter.removeOne,
    setAll: todosAdapter.setAll,
  },
});

// Generated selectors
export const { selectAll: selectAllTodos, selectById: selectTodoById } = todosAdapter.getSelectors(
  (state: RootState) => state.todos
);
```

---

### Q140: Zustand slices pattern

```tsx
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

// Define slices
interface UserSlice { user: null | User; setUser: (user: User | null) => void; }
interface CartSlice { items: Item[]; addItem: (item: Item) => void; removeItem: (id: string) => void; }

const createUserSlice: StateCreator<UserSlice & CartSlice, [], [], UserSlice> = (set) => ({
  user: null,
  setUser: (user) => set({ user }),
});

const createCartSlice: StateCreator<UserSlice & CartSlice, [], [], CartSlice> = (set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.id !== id) })),
});

const useStore = create<UserSlice & CartSlice>()(devtools((...a) => ({
  ...createUserSlice(...a),
  ...createCartSlice(...a),
})));
```

---

### Q141: Atomic state vs global state

**Atomic (Jotai/Recoil):** State as atoms (independent units) + derived selectors. Granular subscriptions.

**Global (Redux/Zustand):** Single store with selectors. Simpler mental model.

---

### Q142: When to use which state management?

- **Local state:** `useState` / `useReducer` -- component-specific.
- **Server state:** React Query / SWR -- data from API.
- **Global UI state:** Zustand / Context -- theme, auth, modals.
- **Complex global state:** Redux Toolkit -- large apps, complex logic, middleware needs.
- **Atomic state:** Jotai/Recoil -- fine-grained subscriptions, medium complexity.

---

### Q143: How does `useSyncExternalStore` work with Zustand?

```tsx
// Zustand already uses useSyncExternalStore internally (React 18)
// When using older React, Zustand falls back to useReducer + useEffect
// You don't need to do anything special -- Zustand handles it
```

---

### Q144: What is the problem with Context + useState for high-frequency updates?

Every context consumer re-renders on every value change. For high-frequency updates (animations, socket data), this causes performance issues. Use Zustand or atomic state instead.

---

### Q145: Redux middleware order

Middleware is applied in array order. Each middleware passes actions to the next in chain.

```tsx
const store = configureStore({
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .prepend(logger)      // runs first
      .concat(analytics),   // runs last
});
```

---

### Q146: What is `createListenerMiddleware` (RTK)?

```tsx
import { createListenerMiddleware } from '@reduxjs/toolkit';

const listenerMiddleware = createListenerMiddleware();

listenerMiddleware.startListening({
  actionCreator: todoAdded,
  effect: async (action, listenerApi) => {
    localStorage.setItem('todos', JSON.stringify(listenerApi.getState().todos));
  },
});

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().prepend(listenerMiddleware),
});
```

---

### Q147: Immer in state management

```tsx
// Immer allows writing mutable code that produces immutable state

// Without Immer:
setState(prev => ({ ...prev, users: prev.users.map(u => u.id === id ? { ...u, name } : u) }));

// With Immer:
setState(produce(draft => {
  const user = draft.users.find(u => u.id === id);
  if (user) user.name = newName;
}));

// RTK uses Immer automatically in createSlice reducers
// Zustand with immer middleware
```

---

### Q148: Zustand `subscribe` with selector

```tsx
const useStore = create<Store>()((set) => ({ count: 0, name: 'foo' }));

// Subscribe with selector (no re-render)
useStore.subscribe(
  (state) => state.count,
  (count, prevCount) => console.log('count changed', count, prevCount)
);

// Subscribe to whole state
const unsub = useStore.subscribe(console.log);
unsub(); // unsubscribe
```

---

### Q149: Redux `useSelector` equality functions

```tsx
import { useSelector, shallowEqual } from 'react-redux';

// Default: strict reference equality (===)
const count = useSelector(state => state.counter.value);

// Shallow equality for returning objects
const { count, name } = useSelector(state => ({
  count: state.counter.value,
  name: state.user.name,
}), shallowEqual);

// Custom equality
const items = useSelector(state => state.todos, (a, b) => a.length === b.length);
```

---

### Q150: What is Redux DevTools?

Browser extension for debugging Redux state changes. Shows action history, state diffs, time-travel debugging.

RTK automatically enables it:
```tsx
const store = configureStore({
  reducer: rootReducer,
  devTools: process.env.NODE_ENV !== 'production',
});
```

---

### Q151: Zustand with `get()` for outside React

```tsx
const useStore = create<Store>()((set, get) => ({
  count: 0,
  increment: () => set({ count: get().count + 1 }),
}));

// Outside React
const { count } = useStore.getState();
useStore.setState({ count: 10 });
```

---

### Q152: RTK Query

```tsx
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    getUser: builder.query<User, string>({
      query: (id) => `users/${id}`,
    }),
    updateUser: builder.mutation<User, Partial<User> & { id: string }>({
      query: ({ id, ...patch }) => ({ url: `users/${id}`, method: 'PATCH', body: patch }),
    }),
  }),
});

export const { useGetUserQuery, useUpdateUserMutation } = api;
```

RTK Query handles caching, loading states, refetching, optimistic updates -- replaces React Query + Redux.

---

### Q153: Jotai with TypeScript

```tsx
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';

const countAtom = atom(0);
const doubleAtom = atom((get) => get(countAtom) * 2);

const Counter = () => {
  const setCount = useSetAtom(countAtom);
  const count = useAtomValue(countAtom);
  const double = useAtomValue(doubleAtom);

  return <div>
    <span>{count} (double: {double})</span>
    <button onClick={() => setCount(c => c + 1)}>+</button>
  </div>;
};

// Async atom
const userAtom = atom(async (get) => {
  const response = await fetch('/api/user');
  return response.json();
});
```

---

### Q154: State persistence patterns

```tsx
// Zustand persist middleware
const useStore = create(
  persist(
    (set) => ({ count: 0, increment: () => set(s => ({ count: s.count + 1 })) }),
    { name: 'my-store', storage: createJSONStorage(() => localStorage) }
  )
);

// Redux persist
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

const persistConfig = { key: 'root', storage };
const persistedReducer = persistReducer(persistConfig, rootReducer);
const store = configureStore({ reducer: persistedReducer });
const persistor = persistStore(store);
```

---

### Q155: What is re-render caused by context? How to avoid?

Context re-renders all consumers on any value change. Avoid by:
1. Splitting contexts (separate for theme, auth, data).
2. Using `useMemo` for context value.
3. Separating read/dispatch contexts.
4. Using Zustand/Jotai instead.

---

### Q156: Valtio -- proxy-based state management

```tsx
import { proxy, useSnapshot } from 'valtio';

const state = proxy({ count: 0, text: 'hello' });

function Counter() {
  const snap = useSnapshot(state); // reactive, only re-renders on accessed properties
  return <div onClick={() => ++state.count}>{snap.count}</div>;
}
```

---

### Q157: When is `useReducer` better than global state?

When state is local to a component tree and has complex update logic. Don't reach for Redux/Zustand for every bit of state.

---

### Q158: Redux saga vs thunk

| | Redux Thunk | Redux Saga |
|---|---|---|
| Type | Functions | Generator functions |
| Complexity | Low | High |
| Testing | Easy | Medium |
| Side effects | Manual | Declarative (effects) |
| Best for | Simple async | Complex workflows, debouncing, race conditions |

---

### Q159: Persisting Zustand with partial storage

```tsx
const useStore = create(
  persist(
    (set, get) => ({
      count: 0,
      sensitiveData: null, // not persisted
      increment: () => set(s => ({ count: s.count + 1 })),
    }),
    {
      name: 'my-store',
      partialize: (state) => ({ count: state.count }), // only persist count
    }
  )
);
```

---

### Q160: Redux combineReducers with RTK

```tsx
import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userSlice';
import todosReducer from './todosSlice';

const store = configureStore({
  reducer: {
    user: userReducer,
    todos: todosReducer,
  },
});

type RootState = ReturnType<typeof store.getState>;
type AppDispatch = typeof store.dispatch;
```

---

### Q161: Zustand middleware -- persist with custom storage

```tsx
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

const useStore = create(
  persist(
    (set) => ({ bears: 0, addBear: () => set(s => ({ bears: s.bears + 1 })) }),
    {
      name: 'bear-storage',
      storage: createJSONStorage(() => sessionStorage),
    }
  )
);

// Async storage (React Native)
import AsyncStorage from '@react-native-async-storage/async-storage';
const storage = createJSONStorage(() => AsyncStorage);
```

---

### Q162: What is `devtools` middleware in Zustand?

```tsx
import { devtools } from 'zustand/middleware';

const useStore = create(
  devtools(
    (set) => ({ count: 0, increment: () => set(s => ({ count: s.count + 1 }), false, 'increment') }),
    { name: 'CounterStore' }
  )
);
// Enables Redux DevTools to inspect Zustand state changes
```

---

### Q163: RTK `createSlice` with TypeScript generics

```tsx
interface CounterState { value: number; }

const initialState: CounterState = { value: 0 };

const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    increment: (state) => { state.value += 1; },
    decrement: (state) => { state.value -= 1; },
    incrementByAmount: (state, action: PayloadAction<number>) => { state.value += action.payload; },
  },
});
```

---

### Q164: How does Zustand prevent unnecessary re-renders?

Zustand uses `useSyncExternalStore` with **selector equality check**. If the selected value doesn't change (by reference), the component doesn't re-render.

```tsx
// Only re-renders when count changes
const count = useStore((state) => state.count);

// For objects, provide equality function
const user = useStore((state) => state.user, shallow);
```

---

### Q165: What are `signal` and `store` in Zustand?

```tsx
// `store` = create returns a store object
const useStore = create(() => ({ count: 0 }));
// useStore is both a hook and has .getState(), .setState(), .subscribe()

// `api` = third argument in the creator function
const useStore = create((set, get, api) => ({
  count: 0,
  increment: () => set({ count: get().count + 1 }),
  reset: () => api.setState({ count: 0 }),
  subscribe: api.subscribe,
}));
```

---

### Q166: What is the `combine` middleware in Zustand?

```tsx
import { create } from 'zustand';
import { combine } from 'zustand/middleware';

const useStore = create(
  combine(
    { count: 0, name: 'Zustand' }, // initial state
    (set) => ({
      increment: () => set((state) => ({ count: state.count + 1 })),
      setName: (name: string) => set({ name }),
    })
  )
);
```

---

### Q167: Zustand computed/derived values

```tsx
// Approach 1: Compute in selector
const total = useStore((state) => state.items.reduce((sum, i) => sum + i.price, 0));

// Approach 2: Subscribe with selector outside component
const useTotal = () => useStore((state) => state.items.reduce((sum, i) => sum + i.price, 0));

// Approach 3: State in store with set on dependency change
const useStore = create((set, get) => ({
  items: [],
  total: 0,
  addItem: (item) => set((state) => ({
    items: [...state.items, item],
    total: state.total + item.price,
  })),
}));
```

---

### Q168: Zustand with immer middleware

```tsx
import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

const useStore = create(
  immer((set) => ({
    items: [{ id: 1, name: 'Item', quantity: 1 }],
    updateQuantity: (id: number, quantity: number) =>
      set((state) => {
        const item = state.items.find(i => i.id === id);
        if (item) item.quantity = quantity; // mutable syntax
      }),
    addItem: (item) => set((state) => { state.items.push(item); }),
  }))
);
```

---

### Q169: React Query `useInfiniteQuery`

```tsx
import { useInfiniteQuery } from '@tanstack/react-query';

function Projects() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['projects'],
    queryFn: ({ pageParam = 0 }) => fetch(`/api/projects?offset=${pageParam}`).then(r => r.json()),
    getNextPageParam: (lastPage) => lastPage.nextOffset ?? undefined,
    initialPageParam: 0,
  });

  return <div>
    {data?.pages.map((page, i) => <div key={i}>{page.items.map(item => <Project key={item.id} {...item} />)}</div>)}
    <button onClick={() => fetchNextPage()} disabled={!hasNextPage}>
      {isFetchingNextPage ? 'Loading...' : 'Load more'}
    </button>
  </div>;
}
```

---

### Q170: React Query mutation with optimistic update

```tsx
const mutation = useMutation({
  mutationFn: (updatedTodo) => fetch(`/api/todos/${updatedTodo.id}`, {
    method: 'PATCH', body: JSON.stringify(updatedTodo),
  }),
  onMutate: async (updatedTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previous = queryClient.getQueryData(['todos']);
    queryClient.setQueryData(['todos'], (old: Todo[]) =>
      old.map(t => t.id === updatedTodo.id ? { ...t, ...updatedTodo } : t)
    );
    return { previous };
  },
  onError: (err, todo, context) => {
    queryClient.setQueryData(['todos'], context?.previous);
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
});
```

---

### Q171: Recoil atoms and selectors

```tsx
import { atom, selector, useRecoilState, useRecoilValue } from 'recoil';

const todoListState = atom({
  key: 'todoListState',
  default: [],
});

const todoListFilterState = atom({
  key: 'todoListFilterState',
  default: 'Show All',
});

const filteredTodoListState = selector({
  key: 'filteredTodoListState',
  get: ({ get }) => {
    const filter = get(todoListFilterState);
    const list = get(todoListState);
    switch (filter) {
      case 'Show Completed': return list.filter(item => item.isComplete);
      case 'Show Uncompleted': return list.filter(item => !item.isComplete);
      default: return list;
    }
  },
});
```

---

### Q172: Zustand `subscribeWithSelector`

```tsx
import { subscribeWithSelector } from 'zustand/middleware';

const useStore = create(
  subscribeWithSelector((set) => ({
    count: 0,
    increment: () => set(s => ({ count: s.count + 1 })),
  }))
);

// Subscribe to specific changes
useStore.subscribe(
  (state) => state.count,
  (count, prevCount) => console.log(`count: ${prevCount} -> ${count}`)
);
```

---

### Q173: What is the difference between `staleTime` and `gcTime` in React Query?

| | `staleTime` | `gcTime` (was `cacheTime`) |
|---|---|---|
| Purpose | How long data is considered "fresh" | How long inactive data stays in cache |
| Refetch on mount | No (if fresh) | N/A |
| Default | 0 (always stale) | 5 minutes |
| Effect | Controls background refetching | Controls cache garbage collection |

---

### Q174: React Query `useQueries`

```tsx
// Dynamic parallel queries
const userIds = [1, 2, 3, 4, 5];

const userQueries = useQueries({
  queries: userIds.map(id => ({
    queryKey: ['user', id],
    queryFn: () => fetch(`/api/users/${id}`).then(r => r.json()),
  })),
});
```

---

### Q175: What is "pessimistic" vs "optimistic" update?

**Optimistic:** Update UI immediately, rollback on error.
**Pessimistic:** Wait for server response, then update.

Optimistic is better for UX (instant). Pessimistic is safer (always correct).

---

### Q176: Jotai `atomFamily`

```tsx
import { atomFamily, useAtomValue } from 'jotai/utils';

const todoAtomFamily = atomFamily((id: number) => atom(async (get) => {
  const response = await fetch(`/api/todos/${id}`);
  return response.json();
}));

function TodoItem({ id }: { id: number }) {
  const todo = useAtomValue(todoAtomFamily(id));
  return <div>{todo.title}</div>;
}
```

---

### Q177: When to use Zustand vs React Query?

**Zustand:** Client state (auth, theme, UI state, cart). **React Query:** Server state (API data, caching, background sync). They complement each other.

---

### Q178: How to structure a large Zustand store?

```tsx
// Split into slices, compose in create
// Use TypeScript for type safety
// Use middleware: devtools for debugging, persist for persistence
// Keep actions colocated with state
// Prefer small selectors over full state reads
```

---

### Q179: What is the Flux pattern?

**Flux:** Unidirectional data flow pattern with:
- **Action** -- payload describing the change.
- **Dispatcher** -- distributes actions to stores.
- **Store** -- contains state and logic.
- **View** -- React components that re-render on store changes.

Redux simplified Flux to a single store + pure reducers.

---

### Q180: What is the "single source of truth" principle?

All application state lives in a single store object tree. This makes debugging, serialization, and time-travel easier. Redux, Zustand, and Recoil all follow this (though Recoil atoms are multiple sources, the composition is predictable).

---

## Performance Optimization (Q181–Q230)

### Q181: `React.memo` usage and pitfalls

```tsx
// Good: Expensive component that renders same output for same props
const ExpensiveList = React.memo(function ExpensiveList({ items }: { items: Item[] }) {
  return <div>{items.map(i => <Item key={i.id} item={i} />)}</div>;
});

// Pitfall: Inline props break memoization
<ExpensiveList items={items} style={{ color: 'red' }} /> // style is new object every render

// Fix: useMemo for object props
const style = useMemo(() => ({ color: 'red' }), []);
<ExpensiveList items={items} style={style} />

// Pitfall: Inline function as prop
<ExpensiveList onAction={() => doSomething()} /> // new function every render

// Fix: useCallback
const onAction = useCallback(() => doSomething(), []);
```

---

### Q182: `useMemo` and `useCallback` -- actual performance impact

```tsx
// Actually helps: expensive computation
const sortedList = useMemo(() => {
  return [...items].sort((a, b) => complexSort(a, b)); // O(n log n)
}, [items]);

// Overkill: cheap computation
const total = useMemo(() => items.length, [items]); // just items.length!

// Helps: maintaining referential equality for child dependencies
const config = useMemo(() => ({ theme, size }), [theme, size]);
<Child config={config} /> // Child won't re-render if config reference is stable

// Hurts: unnecessary useMemo adds memory and comparison overhead
```

**Rule of thumb:** Profile first. Don't optimize prematurely.

---

### Q183: Code splitting (React.lazy, Suspense)

```tsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));
const Analytics = lazy(() => import('./Analytics'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Suspense fallback={<Spinner />}><Settings /></Suspense>} />
      </Routes>
    </Suspense>
  );
}
```

---

### Q184: Bundle size optimization

1. **Code splitting** (React.lazy, dynamic imports).
2. **Tree shaking** -- use ES modules, avoid side effects.
3. **Remove dead code** -- check bundle analyzer.
4. **Minimize dependencies** -- prefer smaller libraries.
5. **Image optimization** -- WebP, lazy loading.
6. **Use production builds** -- `NODE_ENV=production`.
7. **Compression** -- gzip/brotli on server.

---

### Q185: Lazy loading images and components

```tsx
// Lazy loading images
function LazyImage({ src, alt }: { src: string; alt: string }) {
  const imgRef = useRef<HTMLImageElement>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && imgRef.current) {
          imgRef.current.src = src;
          setLoaded(true);
          observer.unobserve(imgRef.current);
        }
      },
      { rootMargin: '200px' }
    );
    if (imgRef.current) observer.observe(imgRef.current);
    return () => observer.disconnect();
  }, [src]);

  return <img ref={imgRef} alt={alt} className={loaded ? 'loaded' : 'placeholder'} />;
}

// Or using native loading
<img src={src} loading="lazy" alt={alt} />
```

---

### Q186: Virtualization (react-window, react-virtuoso)

```tsx
// react-window
import { FixedSizeList as List } from 'react-window';

function VirtualList({ items }: { items: string[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>Row {items[index]}</div>
  );

  return (
    <List height={400} itemCount={items.length} itemSize={35} width={300}>
      {Row}
    </List>
  );
}

// react-virtuoso (auto-sizing, more features)
import { Virtuoso } from 'react-virtuoso';

function VirtualScroll({ items }: { items: string[] }) {
  return (
    <Virtuoso
      style={{ height: '400px' }}
      totalCount={items.length}
      itemContent={(index) => <div>Item {items[index]}</div>}
    />
  );
}
```

---

### Q187: Windowing for large lists

Virtualization only renders visible items + overscan. Prevents rendering thousands of DOM nodes.

```tsx
// Variable size items
import { VariableSizeList } from 'react-window';

function VariableList({ items }: { items: string[] }) {
  const getItemSize = (index: number) => items[index].length > 50 ? 80 : 35;

  return (
    <VariableSizeList
      height={400}
      itemCount={items.length}
      itemSize={getItemSize}
      width={300}
    >
      {Row}
    </VariableSizeList>
  );
}
```

---

### Q188: Debouncing and throttling in React

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debouncedValue;
}

function useThrottle<T>(value: T, limit: number): T {
  const [throttledValue, setThrottledValue] = useState(value);
  const lastRun = useRef(Date.now());

  useEffect(() => {
    const handler = setTimeout(() => {
      if (Date.now() - lastRun.current >= limit) {
        setThrottledValue(value);
        lastRun.current = Date.now();
      }
    }, limit - (Date.now() - lastRun.current));
    return () => clearTimeout(handler);
  }, [value, limit]);

  return throttledValue;
}
```

**Debounce vs Throttle:** Debounce waits for pause. Throttle limits rate.

---

### Q189: Avoiding unnecessary re-renders

```tsx
// 1. React.memo for pure components
// 2. useMemo for stable object references
// 3. useCallback for stable function references
// 4. Keys for list reconciliation
// 5. Lift state down (keep state close to where it's used)
// 6. Split contexts
// 7. Use selectors (Zustand, Redux) -- not full state reads
// 8. Avoid inline objects/functions in JSX
// 9. useRef for values that don't need re-render
// 10. Virtualize large lists

// Bad: inline object
<Child config={{ theme, size }} />

// Good: memoized object
const config = useMemo(() => ({ theme, size }), [theme, size]);
<Child config={config} />
```

---

### Q190: React Profiler

```tsx
import { Profiler } from 'react';

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number,
) {
  console.log(`${id} (${phase}) took ${actualDuration.toFixed(2)}ms`);
}

<Profiler id="Navigation" onRender={onRenderCallback}>
  <Navigation />
</Profiler>

// Better: use React DevTools Profiler tab for visual analysis
```

---

### Q191: Chrome DevTools performance tab for React

1. Record performance while interacting.
2. Look for **long tasks** (>50ms) in the flamegraph.
3. Check **FPS** -- should be 60fps for smooth UI.
4. **Layout shifts** -- caused by DOM mutations without dimensions.
5. **Forced reflow** -- reading layout properties after mutations.
6. Use React DevTools Profiler for component-level analysis.

---

### Q192: Image optimization (next/image)

```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // above-the-fold
  quality={85}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

**Benefits:** Automatic WebP/AVIF conversion, responsive images, lazy loading by default, CLS prevention.

---

### Q193: Font optimization

```tsx
// next/font (Next.js)
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], display: 'swap' });
const robotoMono = Roboto_Mono({ subsets: ['latin'] });

<html className={inter.className}>
  <body className={robotoMono.className}></body>
</html>

// CSS font-display
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* show fallback text, swap when loaded */
}
```

---

### Q194: Tree shaking

Tree shaking eliminates dead exports during bundling.

```tsx
// Good -- tree-shakable
import { useQuery } from '@tanstack/react-query';

// Bad -- imports entire library
import lodash from 'lodash';

// Good -- tree-shakable import
import debounce from 'lodash/debounce';
```

**Requirements:** ES modules (`import`/`export`), production mode, side-effect-free packages.

---

### Q195: Suspense for data fetching

```tsx
// Traditional: isLoading state
function Profile({ userId }: { userId: string }) {
  const { data, isLoading } = useFetch(`/api/users/${userId}`);
  if (isLoading) return <Spinner />;
  return <ProfileCard user={data} />;
}

// Suspense: no loading state in component
function Profile({ userId }: { userId: string }) {
  const data = useFetchSuspense(`/api/users/${userId}`);
  return <ProfileCard user={data} />;
}

// Parent handles fallback
<Suspense fallback={<ProfileSkeleton />}>
  <Profile userId={123} />
</Suspense>
```

---

### Q196: When NOT to use React.memo

- Component re-renders rarely.
- Component is cheap to render.
- Props change every render anyway.
- Preview overhead > render cost.

---

### Q197: Performance impact of React Fragments

Fragments are free -- they don't create DOM nodes. Using `<div>` wrappers unnecessarily increases DOM size.

---

### Q198: How does React handle keyed elements in lists?

Using stable keys allows React to reuse DOM nodes instead of destroying and recreating them. Without keys, React uses index-based matching which can cause unnecessary DOM operations.

---

### Q199: What is the `key` prop's effect on input state?

Without keys, input state (controlled or uncontrolled) persists in the component instance. Keys let you control when a component is destroyed and re-created.

---

### Q200: Concurrent mode performance benefits

Concurrent features (transitions, useDeferredValue) allow React to:
- Interrupt low-priority renders for high-priority input.
- Keep showing old UI while new UI is being computed.
- Prevent jank by yielding to the browser.

---

### Q201: What is the "commit phase" vs "render phase"?

**Render phase:** Virtual DOM diffing, can be interrupted. **Commit phase:** DOM mutations, synchronous, cannot be interrupted.

---

### Q202: How to profile a React app in production?

- React DevTools Profiler (development).
- `React.Profiler` component (development/production with conditional).
- Chrome DevTools Performance tab.
- Web Vitals (LCP, FID, CLS) with `next/web-vitals` or `web-vitals` library.

---

### Q203: What causes layout thrashing in React?

Reading layout properties (offsetHeight, getBoundingClientRect) after writing to DOM (setting styles, adding classes) forces synchronous reflow. Avoid mixing reads and writes.

---

### Q204: How to measure component render time?

```tsx
function useRenderTime(label: string) {
  const startTime = useRef(performance.now());

  useEffect(() => {
    const elapsed = performance.now() - startTime.current;
    console.log(`${label} rendered in ${elapsed.toFixed(2)}ms`);
  });
}
```

---

### Q205: Dynamic imports with React.lazy

```tsx
// Standard
const MarkdownEditor = lazy(() => import('./MarkdownEditor'));

// With named export
const MarkdownEditor = lazy(() => import('./MarkdownEditor').then(m => ({ default: m.MarkdownEditor })));

// With webpack chunk naming
const MarkdownEditor = lazy(() => import(/* webpackChunkName: "editor" */ './MarkdownEditor'));
```

---

### Q206: What is the impact of inline arrow functions in JSX?

```tsx
// Each render creates a new function -- breaks React.memo
<ExpensiveItem onClick={() => handleItem(item.id)} />

// useCallback is stable
const handleClick = useCallback(() => handleItem(item.id), [item.id]);
<ExpensiveItem onClick={handleClick} />
```

---

### Q207: How to optimize context to reduce re-renders?

- Split contexts (separate for unrelated state).
- Use `useMemo` for context value.
- Use dispatch-only context for actions (separate read and write contexts).
- For frequent updates, use Zustand/Redux instead.

---

### Q208: What is the performance cost of using spread operator in setState?

```tsx
// Spread creates a new object each time
setState(prev => ({ ...prev, count: prev.count + 1 }));

// For large state objects, consider useReducer or Immer
// The cost is usually negligible for small objects
```

---

### Q209: Should you always add `useCallback` to event handlers?

No. Only add when:
- Passed to a child wrapped in `React.memo`.
- Used in a `useEffect` dependency array.
- The function is expensive to create (rare).

---

### Q210: How does SSR affect performance perception?

SSR improves **LCP** (Largest Contentful Paint) and **FCP** (First Contentful Paint) because the server sends HTML that the browser can render immediately. Hydration then adds interactivity.

---

### Q211: What is the "perceived performance" trick with Suspense?

Show skeleton screens immediately, stream content progressively. Users perceive the app as faster even if total load time is the same.

---

### Q212: How to implement skeleton loading in React?

```tsx
function Skeleton({ width, height }: { width: string; height: string }) {
  return <div className="skeleton" style={{ width, height, background: 'linear-gradient(90deg, #eee 25%, #f5f5f5 50%, #eee 75%)', backgroundSize: '200% 100%', animation: 'shimmer 1.5s infinite' }} />;
}

function ProfileSkeleton() {
  return <div>
    <Skeleton width="100px" height="100px" />
    <Skeleton width="200px" height="20px" />
    <Skeleton width="150px" height="20px" />
  </div>;
}
```

---

### Q213: How to prevent layout shift (CLS)?

- Set explicit dimensions on images (`width`, `height` attributes).
- Reserve space for dynamic content.
- Use `next/image` which auto-sets dimensions.
- Avoid injecting content above existing content without reserve space.

---

### Q214: What is the cost of creating too many React contexts?

Each context provider adds a wrapper in the tree. Nit: negligible for <10 contexts. For >10, consider consolidating related state.

---

### Q215: `React.memo` with children prop

```tsx
// React.memo is useless if children change every render
<ExpensiveMemoizedChild>
  <OtherChild /> {/* new reference every Parent render */}
</ExpensiveMemoizedChild>

// Memoize children if possible
const children = useMemo(() => <OtherChild />, []);
<ExpensiveMemoizedChild>{children}</ExpensiveMemoizedChild>
```

---

### Q216: How to optimize images for performance?

1. Use `next/image` (auto WebP, lazy loading, responsive sizes).
2. Specify `width` and `height` to prevent CLS.
3. Use `loading="lazy"` for below-fold images.
4. Compress images (quality 80-85).
5. Use CDN for image delivery.
6. Provide responsive sizes with `sizes` attribute.

---

### Q217: What is the difference between `visibility: hidden` and `display: none` for React performance?

`visibility: hidden` keeps the DOM node (React still renders it). `display: none` keeps the node but doesn't paint. Conditional rendering (`&&`) removes the node entirely (React unmounts component).

---

### Q218: How does React handle server-side rendering performance?

SSR is CPU-intensive on the server. React 18's streaming SSR improves TTFB by sending HTML progressively. Use caching (Full Route Cache in Next.js) to reduce server load.

---

### Q219: What is `useDeferredValue` for performance?

Defers updating a computed value. The old value stays visible while the new value is being computed, preventing jank.

---

### Q220: Virtual DOM vs direct DOM manipulation performance

Virtual DOM avoids unnecessary DOM operations by batching updates and computing minimal changes. Direct DOM manipulation can be faster for isolated changes but scales poorly.

---

### Q221: How to avoid "hydration mismatch" performance issues?

Use `useEffect` for browser-specific code, suppress hydration for dynamic content, ensure server and client generate the same initial HTML.

---

### Q222: What is the performance impact of `useLayoutEffect`?

`useLayoutEffect` runs synchronously before paint, blocking the browser's paint cycle. Use `useEffect` instead unless you need to read/measure DOM before paint.

---

### Q223: What is `next/dynamic`?

```tsx
import dynamic from 'next/dynamic';

const DynamicHeader = dynamic(() => import('../components/Header'), {
  loading: () => <HeaderSkeleton />,
  ssr: false, // disable SSR for this component
});

// For named exports
const DynamicComponent = dynamic(() => import('../components/Chart').then(m => m.Chart), {
  ssr: false,
});
```

---

### Q224: What is the bundle size of React itself?

React 18 + ReactDOM is ~42KB gzipped (~130KB minified). This is baseline -- your app code adds on top.

---

### Q225: How does React's event delegation impact performance?

React uses one event listener per event type (attached to root node) instead of one per element. This reduces memory usage compared to vanilla JS with many listeners.

---

### Q226: When does React re-render a component?

1. State changes (`useState`, `useReducer`).
2. Context value changes (for consumers).
3. Parent re-render (by default, children re-render).
4. `forceUpdate` / dispatch.
5. Props reference changes.

---

### Q227: How to prevent child re-render on parent state change?

- `React.memo` for the child.
- `useMemo`/`useCallback` for props passed to child.
- Move state-consuming components to where the state is (lift state down).
- Use context selectors with appropriate comparison.

---

### Q228: What is the performance impact of React DevTools?

React DevTools adds overhead in development. It can slow down renders by up to 20%. Disable in production (which is the default).

---

### Q229: How to optimize Redux selectors?

```tsx
// Unoptimized -- new object every time
const data = useSelector(state => ({
  user: state.user,
  posts: state.posts,
}));

// Optimized -- only re-renders when values change
import { createSelector } from '@reduxjs/toolkit';
const selectUserAndPosts = createSelector(
  [state => state.user, state => state.posts],
  (user, posts) => ({ user, posts })
);
const data = useSelector(selectUserAndPosts);

// Or use shallowEqual
const data = useSelector(state => ({
  user: state.user,
  posts: state.posts,
}), shallowEqual);
```

---

### Q230: How to identify performance bottlenecks?

1. **React DevTools Profiler** -- flamegraph shows which components render.
2. **Why did you render** -- npm package that logs unnecessary renders.
3. **Chrome DevTools Performance** -- record interactions, check long tasks.
4. **`console.log` in render** -- count renders.
5. **Lighthouse** -- automated performance audits.
6. **Web Vitals** -- real user metrics (LCP, FID, CLS).

---

## Next.js (Q231–Q350)

### Q231: What is Next.js? Key features?

**Next.js** is a React framework for production-grade applications. Key features:

- **Routing** -- file-based (Pages Router and App Router).
- **Rendering** -- SSR, SSG, ISR, CSR.
- **Data fetching** -- `getServerSideProps`, `getStaticProps`, Server Components.
- **Optimization** -- Image, Font, Script, Bundle.
- **API routes** -- backend endpoints in the same app.
- **Middleware** -- run code before request completes.
- **Built-in CSS support** -- CSS Modules, Tailwind, Sass.
- **TypeScript support** -- first-class.
- **Edge runtime** -- run at the network edge.

---

### Q232: App Router vs Pages Router

| Aspect | Pages Router | App Router |
|--------|-------------|------------|
| Introduced | Next.js 9+ | Next.js 13.4+ (stable) |
| Component model | React (class + functional) | React Server Components |
| File convention | `pages/about.tsx` | `app/about/page.tsx` |
| Layouts | Manual | `layout.tsx` (nested) |
| Data fetching | `getServerSideProps`, `getStaticProps` | Server Components (async), fetch |
| Loading UI | Custom | `loading.tsx` (Suspense) |
| Error handling | Custom | `error.tsx` |
| Partial rendering | Manual | Automatic via Suspense |
| Streaming | Limited | Built-in |

---

### Q233: Server Components vs Client Components

```tsx
// Server Component (default in App Router)
// - Runs on server only
// - Can be async (fetch data directly)
// - No hooks, no event handlers
// - Reduces client bundle
async function Note({ id }: { id: string }) {
  const note = await db.note.findUnique({ where: { id } });
  return <article><h1>{note.title}</h1><p>{note.content}</p></article>;
}

// Client Component ("use client")
// - Runs on client (hydrated)
// - Has hooks, event handlers, state
// - Can use browser APIs
'use client';
function LikeButton({ noteId }: { noteId: string }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>{liked ? 'Heart' : 'HeartOutline'}</button>;
}
```

---

### Q234: When to use "use client" directive?

Use `'use client'` when the component needs:
- `useState`, `useReducer`, `useEffect`, `useRef`, `useContext`.
- Event handlers (`onClick`, `onChange`, etc.).
- Browser-only APIs (`localStorage`, `window`, `document`).
- Custom hooks that use any of the above.

**Do NOT use** `'use client'` for components that only render static data fetched on the server.

---

### Q235: Data fetching methods -- SSR, SSG, ISR, CSR

| Method | When | Data freshness | Use case |
|--------|------|---------------|----------|
| **SSR** (Server-Side Rendering) | Every request | Always fresh | Personalized content, dashboards |
| **SSG** (Static Site Generation) | Build time | Stale until next build | Blog, marketing pages |
| **ISR** (Incremental Static Regeneration) | Build + revalidate | Configurable staleness | E-commerce products, docs |
| **CSR** (Client-Side Rendering) | In browser after load | Fresh on client | User-specific data (orders, settings) |

```tsx
// Pages Router:
// SSR: export async function getServerSideProps() {}
// SSG: export async function getStaticProps() {}
// ISR: export async function getStaticProps() { return { revalidate: 60 } }

// App Router:
// SSR: dynamic fetch (no cache option)
// SSG: fetch with { cache: 'force-cache' }
// ISR: fetch with { next: { revalidate: 60 } }
// CSR: use useEffect / React Query / SWR in client component
```

---

### Q236: `getServerSideProps` (Pages Router)

```tsx
export async function getServerSideProps(context: GetServerSidePropsContext) {
  const { params, req, res, query } = context;
  const data = await fetch(`https://api.example.com/posts/${params.id}`, {
    headers: { cookie: req.headers.cookie || '' },
  });
  const post = await data.json();

  if (!post) {
    return { notFound: true };
  }

  return {
    props: { post }, // passed to the page component
  };
}

export default function PostPage({ post }: { post: Post }) {
  return <article><h1>{post.title}</h1><div>{post.content}</div></article>;
}
```

Runs on every request. Use for authenticated/personalized data.

---

### Q237: `getStaticProps` (Pages Router)

```tsx
export async function getStaticProps(context: GetStaticPropsContext) {
  const data = await fetch('https://api.example.com/posts');
  const posts = await data.json();

  return {
    props: { posts },
    revalidate: 60, // ISR: revalidate every 60 seconds
  };
}

export async function getStaticPaths() {
  const data = await fetch('https://api.example.com/posts');
  const posts = await data.json();

  return {
    paths: posts.map(post => ({ params: { id: post.id } })),
    fallback: 'blocking', // 'true' | 'false' | 'blocking'
  };
}
```

Runs at build time. Use for static content. `revalidate` enables ISR.

---

### Q238: `getStaticPaths` (Pages Router)

```tsx
// Generates paths for dynamic routes at build time
export async function getStaticPaths() {
  const res = await fetch('https://.../posts');
  const posts = await res.json();

  const paths = posts.map(post => ({
    params: { id: post.id.toString() },
  }));

  return { paths, fallback: 'blocking' };
}

// fallback options:
// - false: 404 for non-generated paths
// - true: show fallback UI, generate on first request
// - 'blocking': wait for generation (SSR-like)
```

---

### Q239: Server Components data fetching (async components)

```tsx
// app/page.tsx (App Router)
async function Page() {
  // Directly await fetch -- no useEffect needed
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 }, // ISR
  }).then(r => r.json());

  return (
    <div>
      {posts.map(post => (
        <div key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.body}</p>
        </div>
      ))}
    </div>
  );
}
```

**No `useEffect`, no `useState`, no loading state needed.** The component directly awaits the data.

---

### Q240: Next.js App Router: layout.tsx, page.tsx, loading.tsx, error.tsx, not-found.tsx

```tsx
// app/layout.tsx -- wraps all pages in a route segment (nested)
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav>Global Nav</nav>
        <main>{children}</main>
        <footer>Footer</footer>
      </body>
    </html>
  );
}

// app/dashboard/layout.tsx -- nested layout for /dashboard/*
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <div className="dashboard"><aside>Sidebar</aside><section>{children}</section></div>;
}

// app/dashboard/page.tsx -- the page content
export default function DashboardPage() {
  return <h1>Dashboard</h1>;
}

// app/dashboard/loading.tsx -- shown while page is loading (Suspense boundary)
export default function Loading() {
  return <DashboardSkeleton />;
}

// app/dashboard/error.tsx -- error boundary for this segment
'use client';
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return <div><h2>Something went wrong!</h2><button onClick={reset}>Try again</button></div>;
}

// app/not-found.tsx -- 404 page
export default function NotFound() {
  return <div><h2>Page not found</h2><p>Could not find requested resource</p></div>;
}
```

---

### Q241: Route handlers (API routes in App Router)

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}

// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({ where: { id: params.id } });
  if (!user) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(user);
}
```

---

### Q242: Middleware in Next.js

```tsx
// middleware.ts (at root of project)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Redirect if not authenticated
  const token = request.cookies.get('token');
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Rewrite based on user agent
  if (request.nextUrl.pathname === '/' && request.headers.get('user-agent')?.includes('Mobile')) {
    return NextResponse.rewrite(new URL('/mobile', request.url));
  }

  // Add custom header
  const response = NextResponse.next();
  response.headers.set('x-custom-header', 'hello');
  return response;
}

export const config = {
  matcher: ['/dashboard/:path*', '/'], // which paths trigger middleware
};
```

---

### Q243: Next.js 13/14/15 features

**Next.js 13:** App Router (stable), React Server Components, Turbopack, `next/font`, `next/image` improvements.
**Next.js 14:** Server Actions (stable), Partial Prerendering (PPR preview), Turbopack 50% faster.
**Next.js 15:** React 19 support, `@next/codemod`, improved form handling, `next/after` for post-response work.

---

### Q244: Image optimization with next/image

```tsx
import Image from 'next/image';

// Local image (auto-optimized)
import profilePic from './profile.jpg';
<Image src={profilePic} alt="Profile" placeholder="blur" />

// Remote image (need domain in config)
<Image
  src="https://example.com/image.jpg"
  alt="Remote"
  width={800}
  height={600}
  priority
/>

// Responsive with sizes
<Image
  src="/hero.jpg"
  alt="Hero"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  style={{ objectFit: 'cover' }}
/>
```

**next.config.js:**
```js
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'example.com' },
    ],
  },
};
```

---

### Q245: Font optimization with next/font

```tsx
import { Inter, Lusitana } from 'next/font/google';
import localFont from 'next/font/local';

// Google Fonts (self-hosted, no external requests)
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

// Local fonts
const myFont = localFont({
  src: './my-font.woff2',
  display: 'swap',
  weight: '400 700',
});

// Load multiple weights
const lusitana = Lusitana({
  weight: ['400', '700'],
  subsets: ['latin'],
});

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${myFont.className}`}>
      <body>{children}</body>
    </html>
  );
}
```

---

### Q246: next/link vs next/navigation

```tsx
// Pages Router: next/link
import Link from 'next/link';
<Link href="/about">About</Link>
<Link href={`/posts/${post.id}`}>Post</Link>
<Link href={{ pathname: '/posts', query: { id: 1 } }}>Query</Link>

// App Router: next/link (still used for links)
import Link from 'next/link';
<Link href="/dashboard" prefetch={false}>Dashboard</Link>

// App Router: programmatic navigation
import { useRouter } from 'next/navigation'; // NOT next/router
const router = useRouter();
router.push('/dashboard');
router.replace('/login');
router.back();
router.refresh(); // refresh current route (re-fetch data)
router.prefetch('/dashboard'); // prefetch for performance
```

---

### Q247: Dynamic routes, catch-all routes

```tsx
// app/blog/[slug]/page.tsx -- dynamic route
export default function BlogPost({ params }: { params: { slug: string } }) {
  return <article>Post: {params.slug}</article>;
}

// app/blog/[...slug]/page.tsx -- catch-all route
// matches /blog/a, /blog/a/b, /blog/a/b/c
export default function CatchAll({ params }: { params: { slug: string[] } }) {
  return <div>Slugs: {params.slug.join(', ')}</div>;
}

// app/blog/[[...slug]]/page.tsx -- optional catch-all (also matches /blog)
// matches /blog, /blog/a, /blog/a/b
export default function OptionalCatchAll({ params }: { params: { slug?: string[] } }) {
  return <div>{params.slug?.join(', ') || 'All posts'}</div>;
}

// Generate static params for SSG
export async function generateStaticParams() {
  const posts = await fetch('https://.../posts').then(r => r.json());
  return posts.map(post => ({ slug: post.slug }));
}
```

---

### Q248: Parallel routes, intercepting routes

```tsx
// Parallel routes -- render multiple pages simultaneously in the same layout
// app/dashboard/@analytics/page.tsx
// app/dashboard/@team/page.tsx
export default function DashboardLayout({ analytics, team }: {
  analytics: React.ReactNode;
  team: React.ReactNode;
}) {
  return (
    <div className="flex">
      <div className="flex-1">{analytics}</div>
      <div className="flex-1">{team}</div>
    </div>
  );
}

// Intercepting routes -- show a route in context while changing the URL
// app/feed/(..)photo/[id]/page.tsx
// (..) goes up one segment (intercepts from feed to photo)
// Useful for modals that open from a feed

// Default slot for parallel routes (when slot has no matching page)
// app/dashboard/@analytics/default.tsx
```

---

### Q249: Server Actions -- what are they? When to use?

```tsx
// Server Actions are async functions that run on the server
// Used for form mutations, data modifications

// app/todos/page.tsx
async function addTodo(formData: FormData) {
  'use server'; // marks as Server Action

  const text = formData.get('text') as string;
  if (!text.trim()) throw new Error('Text required');

  await db.todo.create({ data: { text } });
  revalidatePath('/todos'); // revalidate the page
}

export default function TodoPage() {
  return (
    <form action={addTodo}>
      <input name="text" required />
      <button type="submit">Add</button>
    </form>
  );
}

// With useActionState (Next.js 15 / React 19)
'use client';
import { useActionState } from 'react';

function TodoForm() {
  const [state, formAction, isPending] = useActionState(addTodo, null);

  return (
    <form action={formAction}>
      <input name="text" />
      <button disabled={isPending}>{isPending ? 'Adding...' : 'Add'}</button>
      {state?.error && <p className="error">{state.error}</p>}
    </form>
  );
}
```

**When to use:** Form mutations, data mutations that revalidate pages, server-side logic without building an API route.

---

### Q250: Next.js caching (Data Cache, Full Route Cache, Router Cache)

```tsx
// 1. Full Route Cache (static) -- HTML is cached at build time
// Static routes are cached by default

// 2. Data Cache (fetch results) -- fetch responses are cached
fetch('https://api.example.com/data', {
  cache: 'force-cache', // default, cache on server
  // cache: 'no-store', // don't cache (dynamic)
  next: { revalidate: 3600 }, // ISR-like revalidation
});

// 3. Router Cache (client-side) -- prefetched page segments
// Next.js caches route segments in the browser for instant back/forward navigation
// router.refresh() invalidates the Router Cache

// 4. Full Route Cache invalidation:
// - revalidatePath('/blog')
// - revalidateTag('posts') // with fetch tags
// - On-demand revalidation via API route

fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }, // tag for revalidation
});

// revalidateTag('posts'); // in Server Action or API route
```

---

### Q251: Next.js revalidation strategies (time-based, on-demand)

```tsx
// Time-based revalidation (ISR)
export const revalidate = 3600; // seconds (page-level)

// Or per fetch:
fetch(url, { next: { revalidate: 60 } });

// On-demand revalidation (API route)
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';

export async function POST(request: Request) {
  const { path, tag } = await request.json();

  if (path) revalidatePath(path);
  if (tag) revalidateTag(tag);

  return NextResponse.json({ revalidated: true });
}

// Trigger from your CMS webhook
// POST /api/revalidate { path: '/blog/my-post' }
```

---

### Q252: Incremental Static Regeneration (ISR)

```tsx
// ISR: Combine static generation with periodic revalidation

export async function getStaticProps() {
  const data = await fetch('https://api.example.com/products');
  const products = await data.json();

  return {
    props: { products },
    revalidate: 60, // regenerate at most once every 60 seconds
  };
}

// App Router equivalent:
async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 60 },
  }).then(r => r.json());

  return <ProductList products={products} />;
}

// On-demand ISR (preferred)
// Trigger from webhook:
await revalidateTag('products');
```

**Benefits:** Stale-while-revalidate pattern. Users get cached page, server regenerates in background.

---

### Q253: Static vs Dynamic rendering

```tsx
// Static rendering (default if no dynamic APIs used)
// - Rendered at build time
// - Cached and reused
// - Fastest TTFB

// Dynamic rendering (when any dynamic API is used)
// - Rendered per request
// - Uses: cookies(), headers(), searchParams, no-store fetch
// - Fresh data

// Force dynamic:
export const dynamic = 'force-dynamic';

// Force static:
export const dynamic = 'force-static';

// App Router decides automatically:
// static: fetch with { cache: 'force-cache' }
// dynamic: fetch with { cache: 'no-store' } or { next: { revalidate: 0 } }

// Partial Prerendering (PPR) -- mix static + dynamic in same page
// Static shell + dynamic holes (Suspense boundaries)
```

---

### Q254: next.config.js configuration

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Image optimization
  images: {
    remotePatterns: [{ protocol: 'https', hostname: 'images.unsplash.com' }],
    formats: ['image/avif', 'image/webp'],
  },

  // Experimental features
  experimental: {
    ppr: 'incremental', // Partial Prerendering
  },

  // Redirects
  async redirects() {
    return [
      { source: '/old', destination: '/new', permanent: true },
    ];
  },

  // Rewrites (proxy)
  async rewrites() {
    return [
      { source: '/api/:path*', destination: 'https://api.example.com/:path*' },
    ];
  },

  // Headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'Content-Security-Policy', value: "default-src 'self'" },
        ],
      },
    ];
  },

  // Bundle analyzer
  // withBundleAnalyzer = require('@next/bundle-analyzer')({ enabled: true });

  // Compiler options
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Standalone output (for Docker)
  output: 'standalone',
};

module.exports = nextConfig;
```

---

### Q255: Environment variables in Next.js

```bash
# .env.local (local only, not in git)
DATABASE_URL=postgres://...
NEXT_PUBLIC_API_URL=https://api.example.com
SECRET_KEY=super-secret

# .env.production
NEXT_PUBLIC_API_URL=https://api.prod.com

# .env.development
NEXT_PUBLIC_API_URL=http://localhost:3000
```

**Accessing env vars:**
- Server-side: `process.env.DATABASE_URL` (any env file)
- Client-side: only `NEXT_PUBLIC_*` prefix variables

**TypeScript:**
```tsx
// env.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXT_PUBLIC_API_URL: z.string().url(),
});

export const env = envSchema.parse(process.env);
```

---

### Q256: Next.js with TypeScript

```tsx
// Typed route parameters
// app/users/[id]/page.tsx
interface PageProps {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default function UserPage({ params, searchParams }: PageProps) {
  return <div>User {params.id} - View: {searchParams.view}</div>;
}

// Typed API routes
// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
): Promise<NextResponse<User>> {
  const user = await getUser(params.id);
  return NextResponse.json(user);
}

// Strict mode
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

---

### Q257: Next.js with authentication (Clerk, NextAuth, Auth.js)

```tsx
// NextAuth.js / Auth.js v5
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';

const handler = NextAuth({
  providers: [
    GitHub({ clientId: process.env.GITHUB_ID!, clientSecret: process.env.GITHUB_SECRET! }),
  ],
  callbacks: {
    session({ session, token }) {
      session.user.id = token.sub!;
      return session;
    },
  },
});

export { handler as GET, handler as POST };

// Protecting pages (App Router)
// app/dashboard/page.tsx
import { auth } from '@/auth';

export default async function Dashboard() {
  const session = await auth();
  if (!session) return <div>Not authenticated</div>;
  return <div>Welcome {session.user?.name}</div>;
}

// Client-side protection with Clerk
'use client';
import { useAuth, SignInButton } from '@clerk/nextjs';

function Profile() {
  const { userId, isLoaded } = useAuth();
  if (!isLoaded) return <Spinner />;
  if (!userId) return <SignInButton />;
  return <div>Logged in as {userId}</div>;
}

// Middleware protection
// middleware.ts
export { auth as middleware } from '@/auth';
export const config = { matcher: ['/dashboard/:path*'] };
```

---

### Q258: Next.js deployment (Vercel, Docker, self-hosted)

```tsx
// Vercel (easiest)
// 1. Push to GitHub
// 2. Import in Vercel
// 3. Auto-deploys on push
// Features: Edge Functions, ISR, Analytics, Instant Rollbacks

// Docker
// Dockerfile
FROM node:18-alpine AS base
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]

// Self-hosted
// npm run build && npm run start
// Or with PM2: pm2 start npm --name "next-app" -- start

// next.config.js for self-hosting
module.exports = {
  output: 'standalone', // reduces deployment size
};
```

---

### Q259: Next.js middleware for redirects, rewrites, headers

```tsx
// middleware.ts (runs at edge, before request)

// Authentication redirect
export function middleware(request: NextRequest) {
  if (!request.cookies.has('token') && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}

// A/B testing rewrite
export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname === '/') {
    const variant = Math.random() > 0.5 ? 'a' : 'b';
    return NextResponse.rewrite(new URL(`/home-${variant}`, request.url));
  }
}

// Geo-based redirect (Vercel Edge)
export function middleware(request: NextRequest) {
  const country = request.geo?.country || 'US';
  if (country === 'DE') {
    return NextResponse.redirect(new URL('/de', request.url));
  }
}

// Add security headers
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  return response;
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

---

### Q260: Next.js internationalization (i18n)

```tsx
// App Router approach (no built-in i18n, use middleware)

// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

const locales = ['en', 'es', 'fr', 'de'];
const defaultLocale = 'en';

function getLocale(request: NextRequest) {
  const acceptLang = request.headers.get('accept-language') || '';
  const preferred = acceptLang.split(',')[0]?.split('-')[0];
  return locales.includes(preferred) ? preferred : defaultLocale;
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const pathnameHasLocale = locales.some(locale =>
    pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );

  if (pathnameHasLocale) return;

  const locale = getLocale(request);
  request.nextUrl.pathname = `/${locale}${pathname}`;
  return NextResponse.redirect(request.nextUrl);
}

export const config = {
  matcher: ['/((?!_next|api|favicon.ico).*)'],
};

// app/[lang]/layout.tsx (dictionary provider)
// app/[lang]/page.tsx

// Pages Router had built-in i18n:
// next.config.js
module.exports = {
  i18n: {
    locales: ['en', 'es', 'fr'],
    defaultLocale: 'en',
    localeDetection: true,
  },
};
```

---

### Q261: Next.js SEO (metadata API, sitemap, robots.txt)

```tsx
// Metadata API (App Router)
// app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: { default: 'My App', template: '%s | My App' },
  description: 'My awesome app',
  openGraph: {
    title: 'My App',
    description: 'My awesome app',
    images: '/og-image.png',
  },
  twitter: {
    card: 'summary_large_image',
    site: '@handle',
  },
  robots: { index: true, follow: true },
};

// Per-page metadata
export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn about our company',
  alternates: { canonical: '/about' },
};

// Dynamic metadata
export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const post = await getPost(params.id);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: { images: [post.image] },
  };
}

// Sitemap (app/sitemap.ts)
import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: 'https://example.com', lastModified: new Date(), changeFrequency: 'yearly', priority: 1 },
    { url: 'https://example.com/about', lastModified: new Date(), changeFrequency: 'monthly', priority: 0.8 },
  ];
}

// Robots (app/robots.ts)
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/', disallow: '/private/' },
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

---

### Q262: Streaming and Suspense boundaries in Next.js

```tsx
// Next.js App Router supports streaming by default

// app/dashboard/page.tsx
import { Suspense } from 'react';
import { SlowComponent, SlowerComponent } from './components';

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      {/* Each Suspense boundary streams independently */}
      <Suspense fallback={<SlowSkeleton />}>
        <SlowComponent /> {/* takes 2 seconds */}
      </Suspense>
      <Suspense fallback={<SlowerSkeleton />}>
        <SlowerComponent /> {/* takes 4 seconds */}
      </Suspense>
    </div>
  );
}

// The static shell (h1 + layout) renders immediately
// Each Suspense boundary streams as data arrives
// loading.tsx provides a Suspense boundary for the entire page

// Disable streaming:
export const dynamic = 'force-dynamic';
// Or use loading.tsx without nested Suspense
```

---

### Q263: next/dynamic for dynamic imports

```tsx
import dynamic from 'next/dynamic';

// Same as React.lazy but with SSR options
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Spinner />,
  ssr: false, // don't render on server (client-only)
});

// For named exports
const Chart = dynamic(() => import('./Chart').then(m => m.Chart), {
  ssr: false,
});

// With suspense
const DynamicComponent = dynamic(() => import('./Dynamic'), {
  suspense: true, // wrap in Suspense boundary
});

// Usage
<Suspense fallback={<Loading />}>
  <DynamicComponent />
</Suspense>
```

---

### Q264: Next.js bundle analyzer

```bash
npm install @next/bundle-analyzer
```

```js
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // your config
});
```

```bash
ANALYZE=true npm run build
```

Opens visual reports showing bundle composition, helping identify large dependencies.

---

### Q265: Custom server in Next.js

```tsx
// server.ts (rare -- usually deploy on Vercel)
import { createServer } from 'http';
import { parse } from 'url';
import next from 'next';

const dev = process.env.NODE_ENV !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  createServer((req, res) => {
    const parsedUrl = parse(req.url!, true);
    // Custom routing
    if (parsedUrl.pathname === '/custom') {
      app.render(req, res, '/custom-page', parsedUrl.query);
    } else {
      handle(req, res, parsedUrl);
    }
  }).listen(3000, () => {
    console.log('> Ready on http://localhost:3000');
  });
});
```

**Note:** Custom server disables some optimizations (ISR, automatic static optimization). Prefer Vercel or middleware for routing needs.

---

### Q266: React Server Components (RSC) protocol

RSC uses a wire format to serialize component trees from server to client:

```tsx
// Server Component renders to a special format (not HTML)
// The RSC payload contains serialized component output + references to client components
// Client receives the RSC payload and renders it

// Simplified flow:
// 1. Server renders Server Components -> RSC payload (JSON-like)
// 2. RSC payload includes placeholders for Client Components
// 3. Client merges RSC payload with Client Component bundles
// 4. Client hydrates interactive parts

// This enables:
// - Server-only data access (DB, filesystem)
// - Zero client JS for Server Components
// - Automatic code splitting for Client Components
// - Streaming RSC payloads
```

---

### Q267: Server Components vs Client Components -- performance implications

| Aspect | Server Components | Client Components |
|--------|------------------|-------------------|
| Bundle size contribution | 0 bytes | Full component code |
| Data fetching | Direct (async) | useEffect / React Query |
| Hydration | None | Required (blocking) |
| Interactivity | No | Yes (hooks, events) |
| Server load | More (rendering) | Less |
| Best for | Static content, data fetching | Interactive UI, forms |

**Optimization strategy:** Push components to the server as much as possible. Only add `'use client'` when absolutely needed.

---

### Q268: Next.js edge runtime vs node runtime

```tsx
// Edge Runtime -- lightweight, runs at CDN edge
// Limited Node.js APIs
// app/api/edge/route.ts
export const runtime = 'edge'; // or 'nodejs' (default)

export async function GET() {
  return new Response(JSON.stringify({ hello: 'edge' }), {
    headers: { 'content-type': 'application/json' },
  });
}

// Node.js Runtime -- full Node.js support
export const runtime = 'nodejs';

// Difference:
// Edge: faster cold starts, limited APIs (no fs, no full crypto)
// Node: full API access, slightly slower cold starts
```

---

### Q269: next/script for third-party scripts

```tsx
import Script from 'next/script';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      {/* Strategy options: */}
      <Script
        src="https://www.google-analytics.com/analytics.js"
        strategy="afterInteractive" // default: load after page is interactive
      />
      <Script
        src="https://cdn.example.com/widget.js"
        strategy="lazyOnload" // load when browser is idle
      />
      <Script
        src="https://cdn.example.com/chat.js"
        strategy="beforeInteractive" // load before page is interactive (risky)
      />
      <Script
        src="https://cdn.example.com/worker.js"
        strategy="worker" // offload to web worker (experimental)
      />
    </>
  );
}

// Inline scripts
<Script id="show-banner" strategy="afterInteractive">
  {`document.getElementById('banner').classList.remove('hidden')`}
</Script>

// Event handlers
<Script
  src="/analytics.js"
  onLoad={() => console.log('Script loaded')}
  onError={() => console.log('Script failed')}
/>
```

---

### Q270: next/headers, next/cookies

```tsx
// next/headers (App Router -- server-only)
import { cookies } from 'next/headers';
import { headers } from 'next/headers';

export default async function Page() {
  // Read cookies
  const cookieStore = await cookies();
  const token = cookieStore.get('token')?.value;
  const allCookies = cookieStore.getAll();

  // Set cookies (in Server Action or Route Handler)
  // cookieStore.set('theme', 'dark');

  // Read headers
  const headersList = await headers();
  const userAgent = headersList.get('user-agent');
  const referer = headersList.get('referer');

  return <div>UA: {userAgent}</div>;
}

// In Route Handlers:
export async function GET(request: NextRequest) {
  const token = request.cookies.get('token');
  const referer = request.headers.get('referer');

  // Set cookie in response
  const response = NextResponse.json({ success: true });
  response.cookies.set('session', 'abc123', { httpOnly: true, secure: true });
  return response;
}
```

---

### Q271: Route groups in App Router

```tsx
// Route groups: organize routes without affecting URL path
// Create folders with (name) -- parentheses

// app/(marketing)/page.tsx -> /
// app/(marketing)/about/page.tsx -> /about
// app/(marketing)/layout.tsx -> layout for marketing pages

// app/(dashboard)/dashboard/page.tsx -> /dashboard
// app/(dashboard)/dashboard/settings/page.tsx -> /dashboard/settings
// app/(dashboard)/layout.tsx -> separate layout for dashboard

// app/(auth)/login/page.tsx -> /login
// app/(auth)/register/page.tsx -> /register

// Benefits:
// - Share layouts within a group
// - Different layouts for different sections
// - Keep files organized without URL impact
// - Multiple root layouts possible

// app/(marketing)/layout.tsx
export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return <div className="marketing">{children}</div>;
}

// app/(dashboard)/layout.tsx
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <div className="dashboard"><Sidebar />{children}</div>;
}
```

---

### Q272: Layout nesting and hierarchy

```tsx
// Layouts nest hierarchically in App Router

// app/layout.tsx (root layout) -- wraps everything
// app/blog/layout.tsx -- wraps all /blog/* pages
// app/blog/[slug]/page.tsx -- leaf page

// Nested layout example:
// app/layout.tsx
//   <Header />
//   {children}

// app/blog/layout.tsx
//   <BlogSidebar />
//   {children}          // <-- both Header and BlogSidebar visible

// app/blog/[slug]/page.tsx
//   <Article />         // <-- wrapped in both layouts

// Render order:
// Root Layout -> Blog Layout -> Page
// All three remain mounted when navigating between blog posts

// Partial rendering: when navigating from /blog/post-1 to /blog/post-2
// Root Layout and Blog Layout are preserved (not re-rendered!)
// Only the page component updates

// Layout gets: { children: React.ReactNode }
// Template gets: { children: React.ReactNode } (re-renders on every navigation)
// Use template.tsx if you need to re-mount children on each navigation
```

---

### Q273: `generateStaticParams` in App Router

```tsx
// app/products/[id]/page.tsx

export async function generateStaticParams() {
  const products = await fetch('https://api.example.com/products')
    .then(r => r.json());

  return products.map(product => ({
    id: product.id.toString(),
  }));
  // Returns: [{ id: '1' }, { id: '2' }, { id: '3' }]
}

// This generates static pages for these paths at build time
// Combined with revalidate for ISR
```

---

### Q274: `generateMetadata` for dynamic SEO

Covered in Q261.

---

### Q275: What is Partial Prerendering (PPR)?

```tsx
// PPR: Combine static and dynamic rendering in the same page
// Preview in Next.js 14, stable in Next.js 15

// next.config.js
module.exports = {
  experimental: {
    ppr: 'incremental', // enable PPR
  },
};

// app/page.tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      {/* Static shell -- prerendered at build time */}
      <header>
        <nav>Links</nav>
        <h1>My App</h1>
        <Suspense fallback={<Skeleton />}>
          {/* Dynamic content -- streamed on request */}
          <UserSpecificContent />
        </Suspense>
      </header>
    </div>
  );
}
```

**How it works:** The static shell is prerendered and cached. Dynamic Suspense boundaries are streamed on request. Best of SSG + SSR.

---

### Q276: How to implement search in Next.js?

```tsx
// Client-side search with URL params
'use client';
import { useRouter, useSearchParams } from 'next/navigation';

function SearchInput() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const handleSearch = (term: string) => {
    const params = new URLSearchParams(searchParams);
    if (term) params.set('q', term);
    else params.delete('q');
    router.push(`/products?${params.toString()}`);
  };

  return <input onChange={e => handleSearch(e.target.value)} placeholder="Search..." />;
}

// Server-side filtering
// app/products/page.tsx
export default async function ProductsPage({
  searchParams,
}: {
  searchParams: { q?: string };
}) {
  const products = await db.product.findMany({
    where: searchParams.q ? {
      name: { contains: searchParams.q },
    } : undefined,
  });

  return <ProductList products={products} />;
}
```

---

### Q277: Next.js and SSR performance optimization

1. Enable streaming (App Router default).
2. Use `loading.tsx` for Suspense boundaries.
3. Prefer static rendering where possible.
4. Use ISR for content that changes infrequently.
5. Optimize images with `next/image`.
6. Self-host fonts with `next/font`.
7. Lazily load heavy components with `next/dynamic`.
8. Use Edge Runtime for high-traffic API routes.

---

### Q278: What is `next/after` (Next.js 15)?

```tsx
// next/after -- run code after response is sent
// Useful for logging, analytics, cleanup

import { after } from 'next/server';

export async function GET() {
  after(() => {
    // This runs after the response is sent to the client
    analytics.track('api-call', { path: '/api/data' });
    logToDatabase({ timestamp: Date.now() });
  });

  return NextResponse.json({ data: 'ok' });
}

// Don't block the response -- great for non-critical work
```

---

### Q279: What is Turbopack?

Turbopack is Next.js's Rust-based bundler (replaces webpack in development). Up to 50x faster than webpack for hot module replacement.

```bash
# Next.js 14+ uses Turbopack by default in dev
next dev --turbo # or just next dev (with turbo as default)
```

**Benefits:** Instant HMR, faster builds, incremental computation.

---

### Q280: Next.js with Tailwind CSS

```tsx
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0070f3',
      },
    },
  },
  plugins: [],
};

export default config;

// Usage in components
function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-lg border bg-card p-6 shadow-sm">
      <h3 className="text-lg font-semibold">{title}</h3>
      <div className="mt-2 text-muted-foreground">{children}</div>
    </div>
  );
}
```

---

### Q281: How to handle 404 pages in App Router?

```tsx
// app/not-found.tsx (global 404)
export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-4xl font-bold">404</h2>
      <p className="text-muted-foreground">Page not found</p>
      <a href="/" className="mt-4 text-blue-500 hover:underline">Go home</a>
    </div>
  );
}

// app/blog/not-found.tsx (scoped to /blog/*)
export default function BlogNotFound() {
  return <div>This blog post doesn't exist</div>;
}

// Triggering not-found programmatically:
import { notFound } from 'next/navigation';

async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  if (!post) notFound(); // renders nearest not-found.tsx
  return <article>{post.title}</article>;
}
```

---

### Q282: What is `revalidatePath` and `revalidateTag`?

```tsx
import { revalidatePath, revalidateTag } from 'next/cache';

// Server Action or Route Handler
export async function updatePost(formData: FormData) {
  'use server';
  // Update data
  await db.post.update({ where: { id }, data });

  // Revalidate by path
  revalidatePath('/blog');
  revalidatePath(`/blog/${id}`);

  // Revalidate by fetch tag
  revalidateTag('posts');
}

// Fetch with tags
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'] },
  });
  return res.json();
}
```

---

### Q283: What is the difference between `loading.tsx` and Suspense?

```tsx
// loading.tsx = automatic Suspense boundary for the entire page segment
// app/dashboard/loading.tsx -> wraps the entire dashboard page

// Manual Suspense = granular control over which parts show loading
<Suspense fallback={<Spinner />}>
  <SlowComponent />
</Suspense>

// loading.tsx is equivalent to wrapping the page content in Suspense
// Use Suspense for: per-component loading states
// Use loading.tsx for: page-level loading states
```

---

### Q284: How to implement middleware-based authentication?

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const protectedPaths = ['/dashboard', '/profile', '/settings'];
const authPaths = ['/login', '/register'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get('session')?.value;

  // Redirect to login if accessing protected route without auth
  if (protectedPaths.some(p => pathname.startsWith(p)) && !token) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Redirect to dashboard if already authenticated
  if (authPaths.includes(pathname) && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*', '/login', '/register'],
};
```

---

### Q285: What is the `useSearchParams` hook?

```tsx
'use client';
import { useSearchParams } from 'next/navigation';

function SearchFilters() {
  const searchParams = useSearchParams();

  const category = searchParams.get('category') || 'all';
  const sort = searchParams.get('sort') || 'newest';
  const page = parseInt(searchParams.get('page') || '1');

  return (
    <div>
      <p>Category: {category}</p>
      <p>Sort: {sort}</p>
      <p>Page: {page}</p>
    </div>
  );
}
```

---

### Q286: What is `usePathname`?

```tsx
'use client';
import { usePathname } from 'next/navigation';

function ActiveLink({ href, children }: { href: string; children: React.ReactNode }) {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link href={href} className={isActive ? 'active' : ''}>
      {children}
    </Link>
  );
}
```

---

### Q287: How do you handle forms in Next.js App Router?

```tsx
// Server Actions approach (recommended)
// app/contact/page.tsx
async function submitForm(formData: FormData) {
  'use server';

  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  // Validate
  if (!name || !email) {
    return { error: 'All fields required' };
  }

  // Save to database
  await db.contact.create({ data: { name, email } });

  // Revalidate
  revalidatePath('/contact');
  return { success: true };
}

export default function ContactPage() {
  return (
    <form action={submitForm}>
      <input name="name" required placeholder="Name" />
      <input name="email" type="email" required placeholder="Email" />
      <button type="submit">Submit</button>
    </form>
  );
}

// With useActionState (Next.js 15)
'use client';
import { useActionState } from 'react';

function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitForm, null);

  return (
    <form action={formAction}>
      {state?.error && <p className="error">{state.error}</p>}
      <input name="name" required />
      <button disabled={isPending}>{isPending ? 'Submitting...' : 'Submit'}</button>
    </form>
  );
}
```

---

### Q288: What is the difference between `next/link` prefetch behavior?

```tsx
// next/link prefetches visible links by default (App Router)
<Link href="/dashboard">Dashboard</Link> // prefetched when visible

// Disable prefetch
<Link href="/dashboard" prefetch={false}>Dashboard</Link>

// Prefetch only in viewport (intersection observer)
// Links below the fold are not prefetched until scrolled to

// Programmatic prefetch
const router = useRouter();
router.prefetch('/dashboard');
```

---

### Q289: How does caching work in Next.js App Router?

**Three cache layers:**

1. **Full Route Cache (server):** HTML/RSC payload cached for static routes. Revalidated on demand or after revalidate time. Only for static render.

2. **Data Cache (server):** fetch results cached. `force-cache` (default) or `no-store` (dynamic). Revalidate with `next.revalidate` or `revalidateTag`.

3. **Router Cache (client):** RSC payload cached in browser for instant back/forward. Invalidated by `router.refresh()` or `revalidatePath`.

```tsx
// Cache behavior depends on rendering:
// Static: Full Route Cache + Data Cache (force-cache)
// Dynamic: No Full Route Cache + Data Cache (no-store default)
// ISR: Full Route Cache + Data Cache with revalidate
```

---

### Q290: What is the `next.config.js` `output` option?

```js
module.exports = {
  // 'standalone' -- minimal standalone server (for Docker, self-host)
  // 'export' -- static HTML export (no server)
  // undefined -- default (Next.js server with .next directory)
  output: 'standalone',
};

// With output: 'standalone', Next.js creates a .next/standalone folder
// containing only necessary files for production
// ~80% smaller than full .next directory
```

---

### Q291: How do you handle redirects in Next.js?

```tsx
// 1. next.config.js (permanent/static redirects)
module.exports = {
  async redirects() {
    return [
      { source: '/old-page', destination: '/new-page', permanent: true },
      { source: '/blog/:slug', destination: '/posts/:slug', permanent: true },
    ];
  },
};

// 2. Middleware redirects (dynamic)
export function middleware(request: NextRequest) {
  return NextResponse.redirect(new URL('/new', request.url));
}

// 3. Server component redirect
import { redirect } from 'next/navigation';
if (!session) redirect('/login');

// 4. Client-side redirect
const router = useRouter();
router.push('/dashboard');

// 5. Route handler redirect
export async function GET() {
  return NextResponse.redirect(new URL('/new', request.url));
}
```

---

### Q292: What is the `generateStaticParams` function?

Covered in Q273.

---

### Q293: What is the difference between `layout.tsx` and `template.tsx`?

```tsx
// layout.tsx -- preserved across navigations (doesn't re-mount)
// template.tsx -- re-mounted on every navigation

// app/blog/layout.tsx
export default function BlogLayout({ children }: { children: React.ReactNode }) {
  return <div className="blog-layout"><Sidebar />{children}</div>;
}

// app/blog/template.tsx
export default function BlogTemplate({ children }: { children: React.ReactNode }) {
  // Re-mounts on every navigation to /blog/*
  // Useful for: page view analytics, animations, state reset
  useEffect(() => {
    trackPageView();
  }, []);
  return <div className="blog-template">{children}</div>;
}
```

---

### Q294: How do you add custom fonts in Next.js?

Covered in Q245.

---

### Q295: Next.js with CSS Modules

```tsx
// components/Button.module.css
.button {
  padding: 8px 16px;
  background-color: #0070f3;
  color: white;
  border: none;
  border-radius: 4px;
}

// components/Button.tsx
import styles from './Button.module.css';

export function Button({ children }: { children: React.ReactNode }) {
  return <button className={styles.button}>{children}</button>;
}
```

---

### Q296: What is `next/og` for Open Graph images?

```tsx
// app/og/route.tsx -- Dynamic OG image generation (Edge)
import { ImageResponse } from 'next/og';

export const runtime = 'edge';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') || 'Default Title';

  return new ImageResponse(
    (
      <div style={{ fontSize: 60, color: 'white', background: 'linear-gradient(to right, #000, #333)', width: 1200, height: 630, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        {title}
      </div>
    ),
    { width: 1200, height: 630 }
  );
}

// Usage in metadata:
export const metadata = {
  openGraph: { images: ['/api/og?title=Hello'] },
};
```

---

### Q297: What is `next/cache`?

```tsx
import { unstable_cache } from 'next/cache';

// Cache expensive computations (not just fetch)
const getCachedData = unstable_cache(
  async (userId: string) => {
    return await db.user.findUnique({ where: { id: userId } });
  },
  ['user-cache'], // cache keys
  { revalidate: 60, tags: ['users'] }
);

export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await getCachedData(params.id);
  return <div>{user.name}</div>;
}
```

---

### Q298: How do you handle race conditions in Next.js data fetching?

```tsx
// Sequential requests (one after another)
const user = await fetch('/api/user').then(r => r.json());
const posts = await fetch(`/api/users/${user.id}/posts`).then(r => r.json());

// Parallel requests (faster)
const [user, posts] = await Promise.all([
  fetch('/api/user').then(r => r.json()),
  fetch('/api/posts').then(r => r.json()),
]);

// With React Query (client-side, handles deduplication)
const { data: user } = useQuery({
  queryKey: ['user'],
  queryFn: () => fetch('/api/user').then(r => r.json()),
});
```

---

### Q299: What is `next/compat/router`?

```tsx
// For gradual migration from Pages Router to App Router
// Allows importing useRouter from both:
import { useRouter } from 'next/router'; // Pages Router
import { useRouter } from 'next/navigation'; // App Router

// next/compat/router bridge (rarely used)
```

---

### Q300: How does Next.js handle concurrent requests for ISR?

ISR handles concurrent requests by:
1. First request triggers regeneration.
2. Subsequent requests receive the stale cached page.
3. When regeneration completes, cache is updated.
4. Next request gets the fresh page.

This prevents the "thundering herd" problem where concurrent requests would all trigger regeneration simultaneously.

---

### Q301: What is `next/script` strategy `worker`?

```tsx
// Offloads script to a web worker (experimental)
<Script
  src="/heavy-analytics.js"
  strategy="worker"
/>
// Runs in a background thread, doesn't block main thread
// Limited browser support (Chrome with Partitions)
```

---

### Q302: How to use Next.js with Prisma?

```tsx
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

// app/users/page.tsx
import { prisma } from '@/lib/prisma';

export default async function UsersPage() {
  const users = await prisma.user.findMany({
    include: { posts: { take: 3 } },
  });

  return <div>{users.map(u => <div key={u.id}>{u.name}</div>)}</div>;
}
```

---

### Q303: How to deploy Next.js with Docker?

Covered in Q258.

---

### Q304: What is the `useReportWebVitals` hook?

```tsx
'use client';
import { useReportWebVitals } from 'next/web-vitals';

export function WebVitals() {
  useReportWebVitals((metric) => {
    console.log(metric); // { id, name, value, delta }
    // Send to analytics
    analytics.track('web-vital', metric);
  });

  return null;
}

// In layout.tsx
<WebVitals />
```

---

### Q305: How does Next.js handle `no-cache` in fetch?

```tsx
// Dynamic rendering
fetch('https://api.example.com/data', {
  cache: 'no-store', // don't cache at all
});

// Fetch per request (SSR-like)
async function Page() {
  const data = await fetch('https://api.example.com/data', {
    cache: 'no-store',
  }).then(r => r.json());
  return <div>{data.value}</div>;
}

// Without the cache option, Next.js defaults to force-cache (static)
```

---

### Q306: What is the `next/constants` module?

```tsx
import { PHASE_PRODUCTION_SERVER } from 'next/constants';

// Used in next.config.js to detect build phase
module.exports = (phase) => {
  const isProdServer = phase === PHASE_PRODUCTION_SERVER;
  return {
    // config
  };
};
```

---

### Q307: How do you handle file uploads in Next.js?

```tsx
// Server Action for file upload
async function uploadFile(formData: FormData) {
  'use server';

  const file = formData.get('file') as File;
  const bytes = await file.arrayBuffer();
  const buffer = Buffer.from(bytes);

  // Save to storage (S3, local, etc.)
  const path = `uploads/${Date.now()}-${file.name}`;
  await fs.writeFile(path, buffer);

  revalidatePath('/upload');
  return { url: path };
}

// Client component
'use client';
function UploadForm() {
  return (
    <form action={uploadFile}>
      <input type="file" name="file" required />
      <button type="submit">Upload</button>
    </form>
  );
}

// API route handler for larger files
export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const file = formData.get('file') as File;

  // Stream to S3 for large files
  const buffer = Buffer.from(await file.arrayBuffer());
  await s3.putObject({ Bucket: 'my-bucket', Key: file.name, Body: buffer });

  return NextResponse.json({ url: `https://s3.amazonaws.com/my-bucket/${file.name}` });
}
```

---

### Q308: What is the `instrumentation.ts` file?

```tsx
// instrumentation.ts (Next.js 14+)
// Runs once on server startup -- for monitoring setup

export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation.node');
  }

  if (process.env.NEXT_RUNTIME === 'edge') {
    await import('./instrumentation.edge');
  }
}

// Use for: OpenTelemetry setup, Sentry config, Datadog init
```

---

### Q309: How do you handle pagination in Next.js?

```tsx
// Server component with searchParams
export default async function ProductsPage({
  searchParams,
}: {
  searchParams: { page?: string; limit?: string };
}) {
  const page = parseInt(searchParams.page || '1');
  const limit = parseInt(searchParams.limit || '12');
  const skip = (page - 1) * limit;

  const [products, total] = await Promise.all([
    db.product.findMany({ take: limit, skip }),
    db.product.count(),
  ]);

  const totalPages = Math.ceil(total / limit);

  return (
    <div>
      <ProductGrid products={products} />
      <Pagination current={page} total={totalPages} />
    </div>
  );
}

// Client component pagination
'use client';
import { useRouter, useSearchParams } from 'next/navigation';

function Pagination({ current, total }: { current: number; total: number }) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const goToPage = (page: number) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', page.toString());
    router.push(`/products?${params.toString()}`);
  };

  return (
    <div className="flex gap-2">
      {Array.from({ length: total }, (_, i) => i + 1).map(p => (
        <button key={p} onClick={() => goToPage(p)} className={p === current ? 'active' : ''}>
          {p}
        </button>
      ))}
    </div>
  );
}
```

---

### Q310: What is the `next` global object?

```tsx
// In development, `next` CLI commands:
next dev      // Start dev server (with Turbopack)
next build    // Build for production
next start    // Start production server
next lint     // Run ESLint
next info     // Print system info
```

---

### Q311: How does ISR interact with CDN caching?

ISR uses `stale-while-revalidate` pattern:

1. CDN serves cached page immediately.
2. If page is stale, CDN triggers Next.js to regenerate.
3. Next.js sends fresh HTML to CDN.
4. CDN replaces cached version.

**CDN headers:**
```
Cache-Control: s-maxage=60, stale-while-revalidate=300
```

This tells CDN to cache for 60s, and serve stale content for up to 300s while revalidating.

---

### Q312: What is `next build` and `next export`?

```bash
next build    # Build for production (requires server)
next export   # Static HTML export (no server needed, output: 'export')
```

`next export` creates a fully static site. No SSR, no ISR, no API routes. Deployable to any static host (S3, Netlify, GitHub Pages).

---

### Q313: How do you handle CORS in Next.js?

```tsx
// In middleware.ts
export function middleware(request: NextRequest) {
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    });
  }

  const response = NextResponse.next();
  response.headers.set('Access-Control-Allow-Origin', '*');
  return response;
}

// In route handler
export async function GET() {
  return NextResponse.json(data, {
    headers: { 'Access-Control-Allow-Origin': 'https://example.com' },
  });
}
```

---

### Q314: What is the `next/error` module?

```tsx
// Pages Router: custom error page
// pages/_error.tsx
function ErrorPage({ statusCode }: { statusCode: number }) {
  return <p>{statusCode ? `Server error: ${statusCode}` : 'Client error'}</p>;
}

// App Router: use error.tsx and not-found.tsx instead
```

---

### Q315: How do you configure ESLint in Next.js?

```json
// .eslintrc.json
{
  "extends": "next/core-web-vitals",
  "rules": {
    "react/no-unescaped-entities": "off",
    "@next/next/no-img-element": "error"
  }
}
```

```bash
npm run lint # or: next lint
```

---

### Q316: What is the `next/head` component?

```tsx
// Pages Router only (App Router uses Metadata API)
import Head from 'next/head';

function Page() {
  return (
    <>
      <Head>
        <title>My Page</title>
        <meta name="description" content="My page description" />
      </Head>
      <div>Content</div>
    </>
  );
}
```

---

### Q317: App Router equivalent of `_app.tsx` and `_document.tsx`

```tsx
// Pages Router:
// pages/_app.tsx -> wraps all pages (providers, layouts)
// pages/_document.tsx -> custom HTML/body structure

// App Router equivalent:
// app/layout.tsx -> replaces both _app and _document
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>{/* metadata handled by Metadata API */}</head>
      <body>
        {/* providers, nav, etc. */}
        {children}
      </body>
    </html>
  );
}
```

---

### Q318: How to disable SSR for a component in Next.js?

```tsx
import dynamic from 'next/dynamic';

const ClientOnlyComponent = dynamic(() => import('./ClientComponent'), {
  ssr: false, // only render on client
});

// Alternative: use useEffect to detect mount
'use client';
function ClientOnly({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return null; // or return placeholder
  return <>{children}</>;
}
```

---

### Q319: What is `server-only` package?

```tsx
// Install: npm install server-only

// lib/db.ts
import 'server-only'; // ensures this file is never imported from client

export const db = new PrismaClient();

// If a client component imports this, build fails
// Prevents accidental client-side exposure of server secrets
```

---

### Q320: What is `client-only` package?

```tsx
// Install: npm install client-only

// hooks/useLocalStorage.ts
import 'client-only'; // ensures this file is never imported on server

export function useLocalStorage(key: string) {
  // ...
}
```

---

### Q321: How do you implement dark mode in Next.js?

```tsx
// app/providers.tsx
'use client';
import { ThemeProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}

// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

// Usage in component
'use client';
import { useTheme } from 'next-themes';

function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  return (
    <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      {theme === 'dark' ? 'Light' : 'Dark'}
    </button>
  );
}
```

---

### Q322: What is the `next-auth` `unstable_getServerSession`?

```tsx
// NextAuth v4 (Pages Router)
import { unstable_getServerSession } from 'next-auth/next';
import { authOptions } from './api/auth/[...nextauth]';

export async function getServerSideProps(context) {
  const session = await unstable_getServerSession(context.req, context.res, authOptions);
  return { props: { session } };
}

// NextAuth v5 (App Router)
import { auth } from '@/auth';

export default async function Page() {
  const session = await auth();
  return <div>{session?.user?.name}</div>;
}
```

---

### Q323: What is `next-redirect`?

There is no `next-redirect` package. Use:
- `redirect()` from `next/navigation` (server)
- `NextResponse.redirect()` (middleware)
- `router.push()` (client)

---

### Q324: How does `next.config.js` `publicRuntimeConfig` work?

```js
// Pages Router only
module.exports = {
  publicRuntimeConfig: {
    API_URL: process.env.API_URL,
  },
};

// Usage
import getConfig from 'next/config';
const { publicRuntimeConfig } = getConfig();
// publicRuntimeConfig.API_URL
```

**App Router:** Use environment variables with `NEXT_PUBLIC_` prefix instead.

---

### Q325: What is `next/amp`?

```tsx
// Next.js supports AMP (Accelerated Mobile Pages)

// Page-level AMP
export const config = { amp: true }; // hybrid or true

// With AMP, Next.js automatically creates AMP version of pages
// Use amphtml tag in metadata
```

---

### Q326: How do you handle websockets in Next.js?

```tsx
// Custom server (Pages Router only)
const server = createServer((req, res) => {
  handle(req, res, parseUrl);
});

const wss = new WebSocketServer({ server });
wss.on('connection', (ws) => {
  ws.on('message', (msg) => {
    console.log('Received:', msg);
  });
});

// Client component (App Router)
'use client';
function LiveChat() {
  const [messages, setMessages] = useState<string[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket('wss://api.example.com/chat');

    ws.current.onmessage = (event) => {
      setMessages(prev => [...prev, event.data]);
    };

    return () => ws.current?.close();
  }, []);

  return <div>{messages.map((m, i) => <p key={i}>{m}</p>)}</div>;
}
```

---

### Q327: What is the `next/link` `scroll` prop?

```tsx
// By default, next/link scrolls to top on navigation
<Link href="/blog" scroll={false}>Blog</Link> // don't scroll to top

// Useful for:
// - Back/forward navigation preserving scroll position
// - Modal-like navigation
// - Tab switching
```

---

### Q328: How do you add custom error pages in Pages Router?

```tsx
// pages/404.tsx
export default function Custom404() {
  return <h1>404 - Page Not Found</h1>;
}

// pages/500.tsx
export default function Custom500() {
  return <h1>500 - Server Error</h1>;
}

// pages/_error.tsx (generic error)
function Error({ statusCode }: { statusCode: number }) {
  return <p>{statusCode ? `Server error: ${statusCode}` : 'Client error'}</p>;
}
```

---

### Q329: What is `fallback` in `getStaticPaths`?

Covered in Q238. Values: `true`, `false`, `'blocking'`.

---

### Q330: How do you use Next.js with Redis for caching?

```tsx
// lib/redis.ts
import { Redis } from '@upstash/redis';

export const redis = new Redis({
  url: process.env.REDIS_URL!,
  token: process.env.REDIS_TOKEN!,
});

// Usage in server component
export default async function Page() {
  // Try cache first
  const cached = await redis.get('products');
  if (cached) return <ProductList products={JSON.parse(cached)} />;

  // Fetch from DB
  const products = await db.product.findMany();
  await redis.set('products', JSON.stringify(products), { ex: 60 });

  return <ProductList products={products} />;
}
```

---

### Q331: What is the `locale` property in Next.js?

Covered in Q260.

---

### Q332: How do you handle environment-specific config in Next.js?

```bash
# .env.local (all environments, local)
# .env.development (development only)
# .env.production (production only)
# .env.test (test only)

# Override order: .env.local > .env.{environment} > .env
```

---

### Q333: What is `next/dynamic` `loading` prop?

Covered in Q263.

---

### Q334: How does Next.js handle CSS imports?

```tsx
// Global CSS -- only importable in _app.tsx (Pages) or layout.tsx (App)
import 'globals.css';

// CSS Modules -- component-scoped
import styles from './Button.module.css';

// Tailwind CSS -- utility classes
<div className="flex items-center p-4 bg-white shadow" />

// CSS-in-JS (styled-components, Emotion, styled-jsx)
// Needs configuration in next.config.js for styled-components

// styled-jsx (built-in)
<style jsx>{`
  .button { color: red; }
`}</style>
```

---

### Q335: What is the `next/head` alternative in App Router?

```tsx
// App Router uses Metadata API instead of next/head

// Static metadata
export const metadata: Metadata = {
  title: 'Page Title',
  description: 'Page description',
};

// Dynamic metadata
export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
  const data = await getData(params.id);
  return { title: data.title, openGraph: { images: [data.image] } };
}
```

---

### Q336: What is the `basePath` config in Next.js?

```js
// next.config.js
module.exports = {
  basePath: '/docs',
};

// Accessible at: https://example.com/docs/about
// All routes prefixed with /docs
// Useful for hosting under a sub-path
```

---

### Q337: How do you configure `trailingSlash` in Next.js?

```js
// next.config.js
module.exports = {
  trailingSlash: true,
};

// /about becomes /about/
// Useful for static file hosts that expect trailing slashes
```

---

### Q338: What is the `assetPrefix` config?

```js
// next.config.js
module.exports = {
  assetPrefix: 'https://cdn.example.com',
};

// JS/CSS assets are served from CDN instead of same origin
```

---

### Q339: How do you add Google Analytics to Next.js?

```tsx
// App Router (using next/script)
import Script from 'next/script';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'GA_MEASUREMENT_ID');
          `}
        </Script>
      </body>
    </html>
  );
}
```

---

### Q340: How do you handle preview mode in Next.js?

```tsx
// Preview mode (Pages Router) -- show draft content
// app/api/preview/route.ts
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const secret = searchParams.get('secret');

  if (secret !== process.env.PREVIEW_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  const response = NextResponse.redirect(new URL('/draft', request.url));
  response.cookies.set('__prerender_bypass', 'true', { httpOnly: true });
  response.cookies.set('__next_preview_data', 'true', { httpOnly: true });
  return response;
}
```

---

### Q341: What is the `useEvent` hook alternative in Next.js?

Not available yet (React 19). Use `useCallback` pattern for stable event handlers.

---

### Q342: How do you handle content security policy (CSP) in Next.js?

```tsx
// middleware.ts
export function middleware(request: NextRequest) {
  const nonce = crypto.randomUUID();

  const csp = [
    `default-src 'self'`,
    `script-src 'self' 'nonce-${nonce}'`,
    `style-src 'self' 'unsafe-inline'`,
    `img-src 'self' https: blob:`,
    `font-src 'self'`,
    `connect-src 'self' https://api.example.com`,
  ].join('; ');

  const response = NextResponse.next();
  response.headers.set('Content-Security-Policy', csp);
  response.headers.set('x-nonce', nonce);
  return response;
}

// In layout
<Script nonce={nonce} ... />
```

---

### Q343: What is `next/sitemap`?

Covered in Q261.

---

### Q344: How do you create an RSS feed in Next.js?

```tsx
// app/feed.xml/route.ts
export async function GET() {
  const posts = await db.post.findMany({ orderBy: { createdAt: 'desc' }, take: 20 });

  const feed = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>My Blog</title>
    <link>https://example.com</link>
    <description>Latest posts</description>
    ${posts.map(post => `
      <item>
        <title>${escapeXml(post.title)}</title>
        <link>https://example.com/posts/${post.slug}</link>
        <description>${escapeXml(post.excerpt)}</description>
        <pubDate>${post.createdAt.toUTCString()}</pubDate>
      </item>
    `).join('')}
  </channel>
</rss>`;

  return new Response(feed, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
```

---

### Q345: How does Next.js handle `async` in `getServerSideProps`?

```tsx
// getServerSideProps can be async (it already is)
export async function getServerSideProps(context) {
  const data = await fetchData();
  return { props: { data } };
}

// You can use Promise.all for parallel fetching
export async function getServerSideProps() {
  const [user, posts] = await Promise.all([
    fetchUser(),
    fetchPosts(),
  ]);
  return { props: { user, posts } };
}
```

---

### Q346: What is the `notFound` return in `getStaticProps`?

```tsx
export async function getStaticProps({ params }) {
  const post = await getPost(params.id);

  if (!post) {
    return { notFound: true }; // shows 404 page
  }

  return { props: { post } };
}
```

---

### Q347: How do you handle rate limiting in Next.js API routes?

```tsx
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

// app/api/route.ts
export async function GET(request: NextRequest) {
  const ip = request.headers.get('x-forwarded-for') || 'anonymous';
  const { success, limit, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json({ error: 'Too many requests' }, {
      status: 429,
      headers: { 'X-RateLimit-Limit': limit.toString(), 'X-RateLimit-Remaining': remaining.toString() },
    });
  }

  return NextResponse.json({ data: 'ok' });
}
```

---

### Q348: What is `next.config.js` `poweredByHeader`?

```js
module.exports = {
  poweredByHeader: false, // remove X-Powered-By: Next.js header
};
```

---

### Q349: How do you handle JWT authentication in Next.js?

```tsx
// lib/auth.ts
import jwt from 'jsonwebtoken';

export function signToken(payload: object) {
  return jwt.sign(payload, process.env.JWT_SECRET!, { expiresIn: '7d' });
}

export function verifyToken(token: string) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET!);
  } catch {
    return null;
  }
}

// middleware.ts
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  const payload = verifyToken(token);

  if (!payload && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}
```

---

### Q350: What are the best practices for Next.js project structure?

```
src/
  app/              # App Router pages
    (marketing)/    # Route group
    (dashboard)/
    api/            # API routes
  components/       # Shared components
    ui/             # Primitive UI components
    forms/          # Form components
    layout/         # Layout components
  lib/              # Utility functions, config
    db.ts           # Database client
    auth.ts         # Auth utilities
    api-client.ts   # API client
  hooks/            # Custom hooks
  stores/           # Zustand stores
  types/            # TypeScript types/interfaces
  utils/            # Helper functions
    cn.ts           # Classname utility
    format.ts       # Formatting helpers
public/             # Static assets
  images/
  fonts/
```

---

## React Router & Navigation (Q351–Q380)

### Q351: React Router v6 -- BrowserRouter, Routes, Route

```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users/:id" element={<UserProfile />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

// Nested routes with Outlet
<Route path="/dashboard" element={<DashboardLayout />}>
  <Route index element={<DashboardHome />} />
  <Route path="settings" element={<Settings />} />
  <Route path="users" element={<Users />} />
</Route>

function DashboardLayout() {
  return (
    <div className="dashboard">
      <Sidebar />
      <Outlet /> {/* nested routes render here */}
    </div>
  );
}
```

---

### Q352: useParams, useNavigate, useLocation, useSearchParams

```tsx
import { useParams, useNavigate, useLocation, useSearchParams } from 'react-router-dom';

function UserPage() {
  // Get route params
  const { id } = useParams<{ id: string }>();

  // Programmatic navigation
  const navigate = useNavigate();
  const goBack = () => navigate(-1);
  const goToUser = (id: string) => navigate(`/users/${id}`);
  const goWithState = () => navigate('/dashboard', { state: { from: 'user' } });

  // Current location
  const location = useLocation();
  const currentPath = location.pathname;
  const state = location.state; // passed via navigate { state }

  // Query params
  const [searchParams, setSearchParams] = useSearchParams();
  const page = searchParams.get('page') || '1';
  const sort = searchParams.get('sort');

  const updateFilter = (key: string, value: string) => {
    const next = new URLSearchParams(searchParams);
    next.set(key, value);
    setSearchParams(next);
  };

  return (
    <div>
      <p>User ID: {id}</p>
      <p>Current path: {currentPath}</p>
      <p>Page: {page}</p>
      <button onClick={() => updateFilter('sort', 'name')}>Sort by name</button>
      <button onClick={goBack}>Back</button>
    </div>
  );
}
```

---

### Q353: Nested routes and layout routes

```tsx
// react-router-dom v6 nested routing
<Routes>
  <Route element={<Layout />}>
    <Route path="/" element={<Home />} />
    <Route path="/products" element={<Products />} />
    <Route path="/products/:id" element={<ProductDetail />} />
    <Route path="*" element={<NotFound />} />
  </Route>
</Routes>

// Layout component
function Layout() {
  return (
    <div>
      <Header />
      <main>
        <Outlet /> {/* child routes render here */}
      </main>
      <Footer />
    </div>
  );
}

// Deeply nested layouts
<Route element={<RootLayout />}>
  <Route path="/" element={<Home />} />
  <Route path="/dashboard" element={<DashboardLayout />}>
    <Route index element={<DashboardHome />} />
    <Route path="analytics" element={<Analytics />} />
    <Route path="settings" element={<DashboardSettings />} />
  </Route>
</Route>
```

---

### Q354: Protected routes / auth guards

```tsx
import { Navigate, Outlet } from 'react-router-dom';

// Layout-based protection
function ProtectedRoute() {
  const { user, loading } = useAuth();

  if (loading) return <Spinner />;
  if (!user) return <Navigate to="/login" replace />;

  return <Outlet />; // render child routes
}

// Usage
<Routes>
  <Route path="/login" element={<Login />} />
  <Route element={<ProtectedRoute />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/profile" element={<Profile />} />
    <Route path="/settings" element={<Settings />} />
  </Route>
</Routes>

// Role-based protection
function RoleGuard({ roles }: { roles: string[] }) {
  const { user } = useAuth();
  if (!user || !roles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }
  return <Outlet />;
}

// Permission check in component
function AdminPage() {
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user?.role !== 'admin') navigate('/dashboard');
  }, [user, navigate]);

  return <AdminDashboard />;
}
```

---

### Q355: Lazy loading routes

```tsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}

// With nested routes
const DashboardLayout = lazy(() => import('./layouts/DashboardLayout'));
const Analytics = lazy(() => import('./pages/Analytics'));

<Route path="/dashboard" element={
  <Suspense fallback={<DashboardSkeleton />}>
    <DashboardLayout />
  </Suspense>
}>
  <Route path="analytics" element={<Analytics />} />
</Route>
```

---

### Q356: Route loaders and actions (Remix-inspired)

```tsx
// React Router v6.4+ (data loading with loaders)
// router.ts
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    loader: async () => {
      const user = await fetch('/api/user').then(r => r.json());
      return { user };
    },
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: 'users/:id',
        element: <UserDetail />,
        loader: async ({ params }) => {
          const user = await fetch(`/api/users/${params.id}`).then(r => r.json());
          if (!user) throw new Response('', { status: 404 });
          return { user };
        },
        errorElement: <UserError />,
      },
    ],
  },
]);

// Component uses useLoaderData
import { useLoaderData } from 'react-router-dom';

function UserDetail() {
  const { user } = useLoaderData<{ user: User }>();
  return <div>{user.name}</div>;
}

// Actions for form mutations
{
  path: '/new-user',
  element: <NewUser />,
  action: async ({ request }) => {
    const formData = await request.formData();
    const user = await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(Object.fromEntries(formData)),
    });
    return redirect('/users');
  },
}
```

---

### Q357: Navigation guards in React Router

```tsx
import { useBlocker } from 'react-router-dom';

function FormGuard() {
  const [hasChanges, setHasChanges] = useState(false);

  // Block navigation if form has unsaved changes
  const blocker = useBlocker(
    ({ currentLocation, nextLocation }) =>
      hasChanges && currentLocation.pathname !== nextLocation.pathname
  );

  return (
    <div>
      {blocker.state === 'blocked' && (
        <div>
          <p>You have unsaved changes. Leave anyway?</p>
          <button onClick={() => blocker.proceed()}>Leave</button>
          <button onClick={() => blocker.reset()}>Stay</button>
        </div>
      )}
      <Form onChange={() => setHasChanges(true)} />
    </div>
  );
}

// Custom navigation prompt (beforeunload)
useEffect(() => {
  const handler = (e: BeforeUnloadEvent) => {
    if (hasChanges) {
      e.preventDefault();
      e.returnValue = '';
    }
  };
  window.addEventListener('beforeunload', handler);
  return () => window.removeEventListener('beforeunload', handler);
}, [hasChanges]);
```

---

### Q358: React Router v6 `useRoutes` hook

```tsx
import { useRoutes } from 'react-router-dom';

function App() {
  const element = useRoutes([
    { path: '/', element: <Home /> },
    { path: '/about', element: <About /> },
    {
      path: '/dashboard',
      element: <DashboardLayout />,
      children: [
        { index: true, element: <DashboardHome /> },
        { path: 'settings', element: <Settings /> },
      ],
    },
    { path: '*', element: <NotFound /> },
  ]);

  return element;
}
```

---

### Q359: What is the difference between `Link` and `NavLink`?

```tsx
import { Link, NavLink } from 'react-router-dom';

// Link -- basic navigation
<Link to="/about">About</Link>
<Link to="/users/123" state={{ from: 'home' }}>User</Link>

// NavLink -- same as Link but with active class/styling
<NavLink
  to="/dashboard"
  className={({ isActive }) => isActive ? 'active-link' : ''}
  style={({ isActive }) => ({ fontWeight: isActive ? 'bold' : 'normal' })}
>
  Dashboard
</NavLink>

// NavLink with end prop (exact match for parent routes)
<NavLink to="/dashboard" end>Dashboard Home</NavLink>
// Only active on /dashboard, not /dashboard/settings
```

---

### Q360: React Router `Navigate` component

```tsx
import { Navigate } from 'react-router-dom';

// Declarative redirect
function LoginPage() {
  const { user } = useAuth();
  if (user) return <Navigate to="/dashboard" replace />;
  return <LoginForm />;
}

// Conditional redirect in JSX
{isLoggedIn && <Navigate to="/dashboard" />}

// With state
<Navigate to="/login" state={{ from: location }} replace />
```

---

### Q361: How does `createBrowserRouter` differ from `BrowserRouter`?

```tsx
// BrowserRouter (v6.0-v6.3) -- declarative
<BrowserRouter>
  <Routes>{/* ... */}</Routes>
</BrowserRouter>

// createBrowserRouter (v6.4+) -- data-aware, supports loaders/actions
const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    loader: rootLoader,
    children: [/* ... */],
  },
]);
<RouterProvider router={router} />

// Key differences:
// createBrowserRouter: loaders, actions, error boundaries, lazy routes
// BrowserRouter: simpler, no data loading built-in
```

---

### Q362: What is `ScrollRestoration` in React Router?

```tsx
// React Router v6.4+
import { ScrollRestoration, Outlet } from 'react-router-dom';

function RootLayout() {
  return (
    <div>
      <ScrollRestoration /> {/* restore scroll position on back/forward */}
      <Outlet />
    </div>
  );
}

// Custom behavior
<ScrollRestoration
  getKey={(location) => {
    // Return different keys for different scroll positions
    return location.pathname; // default
    // return location.key; // every navigation restores separately
  }}
/>
```

---

### Q363: How do you handle query parameters in React Router?

Covered in Q352.

---

### Q364: What is the `Outlet` context?

```tsx
// Pass context to child routes via Outlet
function Layout() {
  const [theme, setTheme] = useState('light');

  return (
    <div className={theme}>
      <button onClick={() => setTheme(t => t === 'light' ? 'dark' : 'light')}>Toggle</button>
      <Outlet context={{ theme, setTheme }} />
    </div>
  );
}

// Child component reads context
import { useOutletContext } from 'react-router-dom';

function Child() {
  const { theme, setTheme } = useOutletContext<{
    theme: string;
    setTheme: React.Dispatch<React.SetStateAction<string>>;
  }>();

  return <div className={theme}>Content</div>;
}
```

---

### Q365: How do you test React Router components?

```tsx
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';

// Test with MemoryRouter
it('renders home page', () => {
  render(
    <MemoryRouter initialEntries={['/']}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </MemoryRouter>
  );

  expect(screen.getByText('Welcome to Home')).toBeInTheDocument();
});

// Test navigation
it('navigates to about page', async () => {
  render(
    <MemoryRouter initialEntries={['/']}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </MemoryRouter>
  );

  await userEvent.click(screen.getByText('About'));
  expect(screen.getByText('About Us')).toBeInTheDocument();
});

// Test with loader data
it('renders with loader data', async () => {
  const route = {
    path: '/',
    element: <UserProfile />,
    loader: () => ({ user: { name: 'John' } }),
  };

  const router = createMemoryRouter([route], { initialEntries: ['/'] });
  render(<RouterProvider router={router} />);

  await waitFor(() => {
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});
```

---

### Q366: React Router v6 `useNavigation` hook

```tsx
import { useNavigation } from 'react-router-dom';

function LoadingIndicator() {
  const navigation = useNavigation();

  if (navigation.state === 'loading') {
    return <GlobalSpinner />;
  }

  return null;
}

// navigation.state: 'idle' | 'loading' | 'submitting'
// navigation.location: location being navigated to (during loading)
```

---

### Q367: What is `Form` in React Router (v6.4+)?

```tsx
import { Form, useNavigation } from 'react-router-dom';

function NewUserForm() {
  const navigation = useNavigation();
  const isSubmitting = navigation.state === 'submitting';

  return (
    <Form method="post" action="/users/new">
      <input name="name" required />
      <input name="email" type="email" required />
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create User'}
      </button>
    </Form>
  );
}

// Action handler
export async function action({ request }: { request: Request }) {
  const formData = await request.formData();
  const user = await createUser(Object.fromEntries(formData));
  return redirect(`/users/${user.id}`);
}
```

---

### Q368: How does React Router v6 handle 404s?

```tsx
// With Routes
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="*" element={<NotFound />} /> {/* catches all */}
</Routes>

// With createBrowserRouter
const router = createBrowserRouter([
  { path: '/', element: <Home /> },
  { path: '*', element: <NotFound /> },
]);

// With loader (throw Response)
const router = createBrowserRouter([
  {
    path: 'users/:id',
    loader: async ({ params }) => {
      const user = await fetchUser(params.id);
      if (!user) throw new Response('Not Found', { status: 404 });
      return { user };
    },
    element: <UserDetail />,
  },
]);
```

---

### Q369: React Router vs Next.js routing

| Feature | React Router v6 | Next.js App Router |
|---------|----------------|-------------------|
| Setup | Manual | File-based (automatic) |
| Nested layouts | `<Outlet />` | `layout.tsx` |
| Data loading | Loaders | Server Components + fetch |
| Dynamic routes | `:id` | `[id]` |
| Catch-all | `*` | `[...slug]` |
| Navigation | `Link`, `useNavigate` | `Link`, `useRouter` |
| Lazy loading | `React.lazy` | `next/dynamic` |
| Server support | Manual SSR setup | Built-in SSR/SSG/ISR |

---

### Q370: What is the `useBlocker` hook?

Covered in Q357.

---

### Q371: How do you implement route transitions/animations?

```tsx
import { useLocation, Routes, Route } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Home />
          </motion.div>
        } />
        <Route path="/about" element={
          <motion.div initial={{ x: 100 }} animate={{ x: 0 }} exit={{ x: -100 }}>
            <About />
          </motion.div>
        } />
      </Routes>
    </AnimatePresence>
  );
}
```

---

### Q372: What is `generatePath` in React Router?

```tsx
import { generatePath } from 'react-router-dom';

// Generate a URL from route pattern and params
const url = generatePath('/users/:id', { id: '123' });
// url: '/users/123'

const url2 = generatePath('/products/:category/:id', {
  category: 'electronics',
  id: '42',
});
// url2: '/products/electronics/42'
```

---

### Q373: What is `matchPath`?

```tsx
import { matchPath } from 'react-router-dom';

// Check if a path matches a pattern
const match = matchPath('/users/:id', '/users/42');
// match: { params: { id: '42' }, pathname: '/users/42', ... }

const noMatch = matchPath('/users/:id', '/about');
// noMatch: null

// Useful for custom route matching logic
```

---

### Q374: How do you handle hash fragments in React Router?

```tsx
// React Router v6 handles hash routes via hash router
import { HashRouter } from 'react-router-dom';

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </HashRouter>
  );
}

// Access hash
const location = useLocation();
const hash = location.hash; // '#section-2'

// Programmatic scroll to hash
useEffect(() => {
  if (location.hash) {
    const element = document.querySelector(location.hash);
    element?.scrollIntoView({ behavior: 'smooth' });
  }
}, [location.hash]);
```

---

### Q375: What is `useHref` in React Router?

```tsx
import { useHref } from 'react-router-dom';

function CustomLink({ to, children }: { to: string; children: React.ReactNode }) {
  const href = useHref(to); // resolves relative paths

  return <a href={href}>{children}</a>;
}
```

---

### Q376: React Router v6.4+ `defer` for parallel data loading

```tsx
import { defer, useLoaderData, Await } from 'react-router-dom';
import { Suspense } from 'react';

// Loader returns deferred data
function loader() {
  const userPromise = fetchUser();
  const postsPromise = fetchPosts();

  return defer({
    user: await userPromise, // wait for user
    posts: postsPromise, // defer posts (lazy)
  });
}

function Profile() {
  const { user, posts } = useLoaderData() as { user: User; posts: Promise<Post[]> };

  return (
    <div>
      <h1>{user.name}</h1>

      <Suspense fallback={<PostsSkeleton />}>
        <Await resolve={posts}>
          {(resolvedPosts: Post[]) => (
            <ul>{resolvedPosts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
          )}
        </Await>
      </Suspense>
    </div>
  );
}
```

---

### Q377: What is the `<Routes>` component's `location` prop?

```tsx
// Used with AnimatePresence to keep old route mounted during exit animation
function AnimatedApp() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </AnimatePresence>
  );
}
```

---

### Q378: How do you create a custom `Link` component?

```tsx
function ButtonLink({ to, children, variant = 'primary' }: {
  to: string;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}) {
  const navigate = useNavigate();

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    navigate(to);
  };

  return (
    <a
      href={to}
      onClick={handleClick}
      className={`btn btn-${variant}`}
    >
      {children}
    </a>
  );
}
```

---

### Q379: What is the `relative` prop in React Router?

```tsx
// In nested routes, determine how paths are resolved
import { Link, useNavigate } from 'react-router-dom';

// parent: /dashboard/settings
// child: /dashboard/settings/profile

// Relative to route (default)
<Link to="profile" relative="route">Profile</Link> // /dashboard/settings/profile

// Relative to path
<Link to="profile" relative="path">Profile</Link> // /dashboard/settings/profile

// Going up
<Link to=".." relative="route">Back</Link> // /dashboard
```

---

### Q380: What is the difference between React Router v5 and v6?

| Aspect | v5 | v6 |
|--------|----|----|
| Route syntax | `component={Home}` | `element={<Home />}` |
| Nested routes | Manual | `<Outlet />` |
| `Switch` | `<Switch>` | `<Routes>` (better matching) |
| `useHistory` | `useHistory()` | `useNavigate()` |
| `Redirect` | `<Redirect>` | `<Navigate>` |
| Params | `useParams()` | `useParams()` (same) |
| Location | `useLocation()` | `useLocation()` (same) |
| Data loading | Not built-in | Loaders + actions |
| Relative links | Complex | `relative="route"` |
| Route ordering | Exact first | Best match (automatic) |

---

## General React Interview (Q381–Q400)

### Q381: Virtual DOM vs Shadow DOM

| | Virtual DOM | Shadow DOM |
|---|---|---|
| Purpose | Performance optimization | CSS/style encapsulation |
| Type | JavaScript object tree | Browser DOM fragment |
| Scope | Entire component tree | Single custom element |
| React-specific | Yes (React) | No (Web Components) |
| Framework | React | Native browser feature |

**Virtual DOM:** React's lightweight representation of the real DOM for efficient diffing and patching.

**Shadow DOM:** Browser feature that encapsulates DOM and styles within a custom element. Used by Web Components.

```tsx
// Virtual DOM (React)
const vdom = <div className="container"><h1>Hello</h1></div>;
// Results in: { type: 'div', props: { className: 'container' }, children: [...] }

// Shadow DOM (native browser)
// <custom-element> has its own scoped DOM tree
```

---

### Q382: React vs Angular vs Vue

| Aspect | React | Angular | Vue |
|--------|-------|---------|-----|
| Type | Library | Full framework | Progressive framework |
| Learning curve | Moderate | Steep | Easy |
| State management | External (Zustand, Redux) | Built-in (RxJS, NgRx) | Built-in (Pinia) |
| Bundle size | ~42KB | ~500KB+ | ~30KB |
| Templating | JSX | HTML with directives | HTML with directives |
| Data binding | One-way | Two-way | Two-way (via v-model) |
| TypeScript | Optional | Required | Optional |
| SSR | Next.js | Angular Universal | Nuxt.js |
| Company | Meta | Google | Community |
| Best for | Flexible, large apps | Enterprise, strict structure | Small-medium, rapid dev |

---

### Q383: Unidirectional data flow in React

Data flows **down** from parent to child via props. Events flow **up** via callbacks.

```tsx
// Parent passes state down, child communicates up via callback
function Parent() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <Child onIncrement={() => setCount(c => c + 1)} />
    </div>
  );
}

function Child({ onIncrement }: { onIncrement: () => void }) {
  return <button onClick={onIncrement}>+</button>;
}
```

**Benefits:** Predictable, easier to debug, simpler mental model.

---

### Q384: Composition vs inheritance in React

React favors **composition** over inheritance.

```tsx
// Bad: inheritance
class AdminPanel extends BasePanel {
  // ...
}

// Good: composition
function Panel({ header, content, footer }: {
  header: React.ReactNode;
  content: React.ReactNode;
  footer?: React.ReactNode;
}) {
  return (
    <div className="panel">
      <div className="header">{header}</div>
      <div className="content">{content}</div>
      {footer && <div className="footer">{footer}</div>}
    </div>
  );
}

// Flexible composition
<Panel
  header={<h2>Title</h2>}
  content={<UserForm />}
  footer={<button>Save</button>}
/>

// Specialization via composition
function AdminPanel() {
  return (
    <Panel
      header={<h2>Admin Panel</h2>}
      content={<AdminControls />}
      footer={<AdminFooter />}
    />
  );
}
```

---

### Q385: React design patterns (compound components, render props, controlled props)

```tsx
// 1. Compound Components (state shared implicitly via context)
// Already covered in Q94

// 2. Render Props (function as children for logic sharing)
// Already covered in Q24

// 3. Controlled Props (component controlled externally, with default behavior)
function ExpandablePanel({
  children,
  expanded: externalExpanded,
  onToggle: externalOnToggle,
}: {
  children: React.ReactNode;
  expanded?: boolean;
  onToggle?: () => void;
}) {
  const [internalExpanded, setInternalExpanded] = useState(false);
  const isControlled = externalExpanded !== undefined;
  const expanded = isControlled ? externalExpanded : internalExpanded;
  const toggle = isControlled ? externalOnToggle! : () => setInternalExpanded(e => !e);

  return (
    <div>
      <button onClick={toggle}>{expanded ? 'Collapse' : 'Expand'}</button>
      {expanded && <div>{children}</div>}
    </div>
  );
}

// 4. State Reducer Pattern (invert control)
// Used by downshift, react-table
```

---

### Q386: Accessibility in React (ARIA, keyboard navigation)

```tsx
// Semantic HTML
function Nav() {
  return (
    <nav aria-label="Main navigation">
      <ul role="list">
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </nav>
  );
}

// ARIA attributes
function Modal({ open, onClose, title, children }: ModalProps) {
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      aria-hidden={!open}
    >
      <h2 id="modal-title">{title}</h2>
      <div>{children}</div>
      <button onClick={onClose} aria-label="Close modal">x</button>
    </div>
  );
}

// Keyboard navigation
function Menu({ items }: { items: string[] }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex(i => Math.min(i + 1, items.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex(i => Math.max(i - 1, 0));
        break;
      case 'Enter':
      case ' ':
        e.preventDefault();
        selectItem(activeIndex);
        break;
    }
  };

  return (
    <ul role="menu" onKeyDown={handleKeyDown}>
      {items.map((item, i) => (
        <li
          key={i}
          role="menuitem"
          tabIndex={i === activeIndex ? 0 : -1}
          aria-current={i === activeIndex ? 'true' : undefined}
        >
          {item}
        </li>
      ))}
    </ul>
  );
}

// Screen reader only content
function VisuallyHidden({ children }: { children: React.ReactNode }) {
  return (
    <span className="sr-only" style={{
      position: 'absolute',
      width: '1px', height: '1px', padding: 0, margin: '-1px',
      overflow: 'hidden', clip: 'rect(0,0,0,0)', border: 0,
    }}>
      {children}
    </span>
  );
}

// Focus management with useRef
function LoginForm() {
  const emailRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    emailRef.current?.focus();
  }, []);

  return <input ref={emailRef} type="email" aria-required="true" />;
}
```

---

### Q387: React best practices

1. **Component organization** -- one component per file, colocate styles/tests.
2. **Hooks rules** -- top-level, only in function components/custom hooks.
3. **State management** -- local state first, then context, then external library.
4. **Performance** -- memoize expensive computations, not everything.
5. **TypeScript** -- strict mode, typed props, avoid `any`.
6. **Testing** -- React Testing Library for behavior, not implementation.
7. **Accessibility** -- semantic HTML, ARIA, keyboard nav.
8. **Code splitting** -- `React.lazy` and `Suspense` for route-based splitting.
9. **Error handling** -- error boundaries, try/catch in effects.
10. **Bundle size** -- tree-shakeable imports, avoid large libraries for small tasks.

```tsx
// Example of a well-structured component
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export function Button({ label, onClick, variant = 'primary', disabled }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
      aria-disabled={disabled}
    >
      {label}
    </button>
  );
}
```

---

### Q388: Common React mistakes and anti-patterns

```tsx
// 1. Missing keys in lists
{items.map(item => <li>{item}</li>)} // missing key prop

// 2. Key as index (for dynamic lists)
{items.map((item, i) => <li key={i}>{item}</li>)} // index key bug

// 3. Mutating state directly
const [user, setUser] = useState({ name: 'John' });
user.name = 'Jane'; // mutation! use setUser({ ...user, name: 'Jane' })

// 4. Lying about dependencies
useEffect(() => {
  fetchUser(id);
}, []); // missing `id` dependency

// 5. Inline functions in JSX (breaking memo)
<ExpensiveChild onClick={() => doSomething()} /> // new function each render

// 6. Too many re-renders (setting state in render)
function Bad() {
  const [count, setCount] = useState(0);
  setCount(count + 1); // infinite loop!
  return <div>{count}</div>;
}

// 7. Using state where refs suffice (causing unnecessary re-renders)
const [intervalId, setIntervalId] = useState<NodeJS.Timeout>(); // should be useRef

// 8. Prop drilling without context
function A({ user }) { return <B user={user} />; }
function B({ user }) { return <C user={user} />; }
function C({ user }) { return <D user={user} />; } // use context instead

// 9. Loading state anti-pattern (multiple states)
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
const [data, setData] = useState(null);
// Consider useReducer or a state management library

// 10. God component (too many responsibilities in one component)
function ProfilePage() { /* renders profile, fetches data, handles form, manages complex state */ }
// Split into smaller components
```

---

### Q389: How do you handle side effects in tests?

```tsx
// Mock API calls
global.fetch = vi.fn().mockResolvedValue({
  ok: true,
  json: () => Promise.resolve({ data: 'test' }),
});

// Mock timers
beforeEach(() => {
  vi.useFakeTimers();
});
afterEach(() => {
  vi.useRealTimers();
});

// Test that useEffect runs correctly
it('calls fetch on mount', () => {
  render(<DataFetcher url="/api/data" />);
  expect(global.fetch).toHaveBeenCalledWith('/api/data');
});

// Test cleanup
it('cleans up on unmount', () => {
  const { unmount } = render(<Timer />);
  unmount();
  // expect timer to be cleared
});
```

---

### Q390: What is the `use` hook (React 19)?

```tsx
// React 19: use() -- read a promise or context directly in render
// Allows reading async data without useEffect

import { use } from 'react';

function Comments({ commentsPromise }: { commentsPromise: Promise<Comment[]> }) {
  // Suspends the component until promise resolves
  const comments = use(commentsPromise);
  return <ul>{comments.map(c => <li key={c.id}>{c.text}</li>)}</ul>;
}

// Usage with Suspense
function PostPage() {
  const commentsPromise = fetchComments(); // start fetch
  return (
    <Suspense fallback={<CommentsSkeleton />}>
      <Comments commentsPromise={commentsPromise} />
    </Suspense>
  );
}
```

---

### Q391: What is the `act` function in React testing?

```tsx
import { act } from 'react';
// or from '@testing-library/react'

// act() wraps code that causes state updates
// Ensures all state updates are processed before assertions

// With RTL, most things are wrapped automatically
// But for custom behavior:

it('updates after async', async () => {
  let resolve: (value: string) => void;
  const promise = new Promise<string>(r => { resolve = r; });

  function AsyncComponent() {
    const [value, setValue] = useState('');
    useEffect(() => { promise.then(setValue); }, []);
    return <div>{value}</div>;
  }

  const { container } = render(<AsyncComponent />);
  expect(container.textContent).toBe('');

  await act(async () => {
    resolve('done');
    await promise;
  });

  expect(container.textContent).toBe('done');
});
```

---

### Q392: What is the purpose of `inputProps` in React?

```tsx
// Spread remaining props onto an element
function Input({ label, error, ...inputProps }: {
  label: string;
  error?: string;
} & React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <div>
      <label>{label}</label>
      <input {...inputProps} aria-invalid={!!error} />
      {error && <span role="alert">{error}</span>}
    </div>
  );
}

// Usage -- any additional HTML input props work
<Input label="Email" type="email" placeholder="you@example.com" required />
```

---

### Q393: How do you handle concurrent rendering with `startTransition`?

Already covered in Q62.

---

### Q394: What is the difference between `export default` and `named export` in React?

```tsx
// Default export (imported without braces)
// component/Button.tsx
export default function Button() { return <button>Click</button>; }

// Import
import Button from './Button';

// Named export
export function Button() { return <button>Click</button>; }
export function IconButton() { return <button><Icon /></button>; }

// Import
import { Button, IconButton } from './Button';

// Best practice: use named exports for components (better tree-shaking, IDE support)
```

---

### Q395: How do you structure large React applications?

```
src/
  components/       # Shared UI components
    ui/             # Primitives (Button, Input, Card)
    layout/         # Layout components (Header, Sidebar)
    forms/          # Form components
  features/         # Feature modules
    auth/           # Auth feature (self-contained)
      components/
      hooks/
      api/
    dashboard/
    users/
  hooks/            # Shared custom hooks
  lib/              # Utilities, API clients
  stores/           # State management
  types/            # TypeScript types
  utils/            # Helper functions
  pages/            # Page components (or app/ in Next.js)
```

**Feature-based organization:** Each feature contains its own components, hooks, and API calls. Reduces coupling.

---

### Q396: What are Micro-Frontends in React?

```tsx
// Micro-frontends: independent apps composed into a single UI

// Module Federation (Webpack 5)
// Host app loads remote apps at runtime

// host/webpack.config.js
new ModuleFederationPlugin({
  name: 'host',
  remotes: {
    app1: 'app1@http://localhost:3001/remoteEntry.js',
    app2: 'app2@http://localhost:3002/remoteEntry.js',
  },
});

// Dynamically load remote component
const RemoteButton = React.lazy(() => import('app1/Button'));

function App() {
  return (
    <Suspense fallback="Loading...">
      <RemoteButton />
    </Suspense>
  );
}
```

---

### Q397: How do you handle time zones and dates in React?

```tsx
// Use libraries like date-fns, dayjs, or luxon
import { format, formatDistanceToNow } from 'date-fns';
import { es } from 'date-fns/locale';

function DateDisplay({ date }: { date: Date }) {
  // Format with timezone
  const formatted = format(date, 'PPP', { locale: es });

  // Relative time
  const relative = formatDistanceToNow(date, { addSuffix: true, locale: es });

  return (
    <div>
      <p>Date: {formatted}</p>
      <p>{relative}</p>
    </div>
  );
}

// Use Intl.DateTimeFormat for built-in i18n
function IntlDate({ date }: { date: Date }) {
  const formatted = new Intl.DateTimeFormat('en-US', {
    dateStyle: 'full', timeStyle: 'long', timeZone: 'America/New_York',
  }).format(date);

  return <time dateTime={date.toISOString()}>{formatted}</time>;
}
```

---

### Q398: How do you handle real-time updates in React?

```tsx
// 1. WebSocket
'use client';
function LivePrice({ symbol }: { symbol: string }) {
  const [price, setPrice] = useState<number | null>(null);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(`wss://ws.example.com/prices/${symbol}`);

    ws.current.onmessage = (event) => {
      setPrice(JSON.parse(event.data).price);
    };

    return () => ws.current?.close();
  }, [symbol]);

  return <div>${price?.toFixed(2) ?? 'Loading...'}</div>;
}

// 2. Server-Sent Events (SSE)
useEffect(() => {
  const eventSource = new EventSource('/api/events');

  eventSource.onmessage = (event) => {
    setData(JSON.parse(event.data));
  };

  eventSource.addEventListener('notification', (event) => {
    // Handle specific event type
  });

  return () => eventSource.close();
}, []);

// 3. Polling with React Query
const { data } = useQuery({
  queryKey: ['live-data'],
  queryFn: () => fetch('/api/live').then(r => r.json()),
  refetchInterval: 5000, // poll every 5 seconds
});

// 4. Firebase / Supabase real-time listeners
useEffect(() => {
  const unsubscribe = supabase
    .channel('realtime')
    .on('postgres_changes', { event: 'INSERT', schema: 'public' }, (payload) => {
      setItems(prev => [...prev, payload.new]);
    })
    .subscribe();

  return () => unsubscribe();
}, []);
```

---

### Q399: What are the common security concerns in React?

```tsx
// 1. XSS (Cross-Site Scripting) -- React escapes by default, but:
// Dangerous: dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userProvidedHTML }} /> // sanitize first!

// 2. Injection in URLs
<a href={userProvidedURL}>Click</a> // use URL validation
// const sanitized = new URL(userProvidedURL, window.location.origin);

// 3. Prototype pollution
const [state, setState] = useState({});
const update = (key: string, value: any) => {
  // Avoid: setState(prev => ({ ...prev, [key]: value }))
  // If key === '__proto__', this pollutes Object prototype
  if (key === '__proto__' || key === 'constructor') return;
  setState(prev => ({ ...prev, [key]: value }));
};

// 4. Sensitive data in client bundle
// Don't expose secrets in client components
// Use NEXT_PUBLIC_ prefix for public env vars in Next.js

// 5. CSRF -- use SameSite cookies, CSRF tokens
// React apps making API calls should include CSRF tokens in headers

// 6. Dependency vulnerabilities
// Regularly run npm audit and update dependencies

// 7. Server-side rendering data leaks
// Don't pass sensitive data from getServerSideProps to client unnecessarily
```

---

### Q400: What is the future of React? React 19 and beyond

```tsx
// React 19 features (upcoming):
// 1. `use()` hook -- read promises and context in render
// 2. `useActionState` -- simplified form handling with pending state
// 3. `useOptimistic` -- optimistic updates
// 4. `useEvent` -- stable event handler references
// 5. Server Components (stable)
// 6. React Compiler (React Forget) -- automatic memoization
// 7. Improved hydration error messages
// 8. Asset loading (styles, fonts) built into Suspense

// React Compiler (React Forget):
// Automatically memoizes values and functions
// No more useMemo/useCallback needed in most cases
// Currently experimental

// React Server Components:
// Growing ecosystem support
// Better integration with databases and backend frameworks

// The trend:
// - Less manual optimization (compiler handles it)
// - More server-side rendering (RSC)
// - Better concurrent features
// - Improved developer experience
```

---

## Conclusion

This comprehensive guide covers 400+ interview questions spanning React Core, State Management, Performance Optimization, Next.js, React Router, and General React topics. Each answer includes practical code examples to demonstrate deep understanding of the concepts.

**Key areas to focus for YC/top company interviews:**
- Deep understanding of React's rendering behavior (reconciliation, fiber, batching)
- Server Components and the App Router (Next.js)
- State management trade-offs (Zustand, Redux, Context)
- Performance optimization patterns
- Real-world problem-solving with code
- Accessibility and best practices

**Practice approach:**
1. Implement each code example yourself
2. Build a full-stack project using Next.js App Router + Zustand + React Query
3. Profile and optimize your app's performance
4. Write tests for your components and hooks
5. Contribute to open-source React projects
