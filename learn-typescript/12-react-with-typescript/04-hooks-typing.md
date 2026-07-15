# Hooks Typing in React + TypeScript

## Overview

Every React hook has specific typing patterns. This guide covers all built-in hooks with complete type annotations, plus patterns for creating custom typed hooks.

---

## 1. useState

```typescript
import { useState } from 'react';

// Inferred from initial value
const [count, setCount] = useState(0); // number
const [name, setName] = useState('');  // string
const [flag, setFlag] = useState(false); // boolean

// Explicit generic type
const [items, setItems] = useState<string[]>([]);
const [selected, setSelected] = useState<string | null>(null);

// Complex state
interface User {
  id: string;
  name: string;
  email: string;
  roles: string[];
}

const [user, setUser] = useState<User | null>(null);

// Function updater type
setCount((prev) => prev + 1);            // prev is number
setItems((prev) => [...prev, 'new']);     // prev is string[]
setUser((prev) => (prev ? { ...prev, name: 'new' } : null)); // prev is User | null
```

---

## 2. useEffect

```typescript
import { useEffect } from 'react';

// No cleanup
useEffect(() => {
  document.title = `Count: ${count}`;
});

// With cleanup — return type is void | (() => void)
useEffect(() => {
  const handler = () => console.log('resize');
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler);
}, []);

// With dependency array
useEffect(() => {
  fetchData(url).then(setData);
}, [url]); // url is the dependency

// Async effect pattern
useEffect(() => {
  let cancelled = false;

  const load = async () => {
    setLoading(true);
    try {
      const result = await fetchUser(id);
      if (!cancelled) {
        setUser(result);
      }
    } catch (err) {
      if (!cancelled) {
        setError(err as Error);
      }
    } finally {
      if (!cancelled) {
        setLoading(false);
      }
    }
  };

  load();
  return () => { cancelled = true; };
}, [id]);
```

---

## 3. useContext

```typescript
import { createContext, useContext } from 'react';

interface AuthContextType {
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Typed context consumer
function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Usage
function Profile() {
  const { user, isAuthenticated, logout } = useAuth();

  if (!isAuthenticated) return <Redirect to="/login" />;
  return (
    <div>
      <h1>{user?.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

---

## 4. useRef

```typescript
import { useRef, useEffect } from 'react';

// DOM ref — initial value is null
const inputRef = useRef<HTMLInputElement>(null);
// RefObject<HTMLInputElement> — { current: HTMLInputElement | null }

// Mutable ref — initial value is provided
const countRef = useRef<number>(0);
// MutableRefObject<number> — { current: number }

// Timer ref
const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

useEffect(() => {
  intervalRef.current = setInterval(() => {
    console.log('tick');
  }, 1000);

  return () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };
}, []);

// Accessing DOM ref
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus</button>
    </>
  );
}

// Ref for storing previous value
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Usage
const [count, setCount] = useState(0);
const prevCount = usePrevious(count);
```

---

## 5. useMemo

```typescript
import { useMemo } from 'react';

// Typed return value
interface SortedListProps {
  items: { name: string; score: number }[];
  sortKey: 'name' | 'score';
}

function SortedList({ items, sortKey }: SortedListProps) {
  const sortedItems = useMemo(() => {
    return [...items].sort((a, b) => {
      if (sortKey === 'name') return a.name.localeCompare(b.name);
      return b.score - a.score;
    });
  }, [items, sortKey]);

  return (
    <ul>
      {sortedItems.map((item) => (
        <li key={item.name}>{item.name}: {item.score}</li>
      ))}
    </ul>
  );
}

// Expensive computation
const fibonacci = useMemo(() => {
  return computeFibonacci(n);
}, [n]); // n: number, return: number

// Memoized object
const style = useMemo(() => ({
  color: isActive ? 'blue' : 'gray',
  fontSize: size === 'large' ? '20px' : '14px',
}), [isActive, size]);
```

---

## 6. useCallback

```typescript
import { useCallback, useState } from 'react';

// Typed callback
interface SearchProps {
  onSearch: (query: string) => void;
}

function SearchBar({ onSearch }: SearchProps) {
  const [query, setQuery] = useState('');

  // useCallback preserves referential identity
  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      setQuery(value);
      onSearch(value);
    },
    [onSearch] // onSearch is the dependency
  );

  return <input value={query} onChange={handleChange} />;
}

// Callback with generic
function useCallbackWithAsync<TArgs extends any[], TResult>(
  callback: (...args: TArgs) => Promise<TResult>,
  deps: React.DependencyList
): (...args: TArgs) => Promise<TResult> {
  return useCallback(callback, deps);
}
```

---

## 7. useReducer

```typescript
import { useReducer } from 'react';

// Full type specification
interface State {
  count: number;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { count: state.count + 1 };
    case 'decrement': return { count: state.count - 1 };
    case 'reset': return { count: 0 };
  }
}

// With lazy initialization
function init(initialCount: number): State {
  return { count: initialCount };
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, 10, init);

  return (
    <div>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

---

## 8. useLayoutEffect

```typescript
import { useLayoutEffect, useRef, useState } from 'react';

// Same type signature as useEffect
function useElementSize() {
  const ref = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ width: 0, height: 0 });

  useLayoutEffect(() => {
    if (ref.current) {
      const { width, height } = ref.current.getBoundingClientRect();
      setSize({ width, height });
    }
  }, []); // Runs synchronously after DOM mutations

  return { ref, ...size };
}

// Tooltip positioning
function useTooltipPosition(triggerRef: React.RefObject<HTMLElement>) {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useLayoutEffect(() => {
    if (triggerRef.current) {
      const rect = triggerRef.current.getBoundingClientRect();
      setPosition({
        x: rect.left + rect.width / 2,
        y: rect.top - 8,
      });
    }
  }, [triggerRef]);

  return position;
}
```

---

## 9. useImperativeHandle

```typescript
import { useImperativeHandle, useRef, forwardRef } from 'react';

// Define the imperative API
interface InputHandle {
  focus: () => void;
  blur: () => void;
  clear: () => void;
  getValue: () => string;
}

interface FancyInputProps {
  placeholder?: string;
}

const FancyInput = forwardRef<InputHandle, FancyInputProps>(
  ({ placeholder }, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      blur: () => inputRef.current?.blur(),
      clear: () => {
        if (inputRef.current) inputRef.current.value = '';
      },
      getValue: () => inputRef.current?.value ?? '',
    }), []);

    return <input ref={inputRef} placeholder={placeholder} />;
  }
);

// Usage
function Form() {
  const inputRef = useRef<InputHandle>(null);

  return (
    <>
      <FancyInput ref={inputRef} placeholder="Type here..." />
      <button onClick={() => inputRef.current?.focus()}>Focus</button>
      <button onClick={() => inputRef.current?.clear()}>Clear</button>
    </>
  );
}
```

---

## 10. Custom Hook Patterns

```typescript
// Pattern 1: Typed state hook
function useToggle(initialValue: boolean = false): [boolean, () => void, (value: boolean) => void] {
  const [value, setValue] = useState(initialValue);
  const toggle = useCallback(() => setValue((v) => !v), []);
  const set = useCallback((v: boolean) => setValue(v), []);
  return [value, toggle, set];
}

// Pattern 2: Generic fetch hook
interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const json: T = await response.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => { fetchData(); }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Pattern 3: Typed localStorage hook
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T | ((prev: T) => T)) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      setStoredValue((prev) => {
        const valueToStore = value instanceof Function ? value(prev) : value;
        window.localStorage.setItem(key, JSON.stringify(valueToStore));
        return valueToStore;
      });
    },
    [key]
  );

  return [storedValue, setValue];
}

// Pattern 4: Generic debounce hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// Pattern 5: Typed event listener hook
function useEventListener<K extends keyof WindowEventMap>(
  eventName: K,
  handler: (event: WindowEventMap[K]) => void,
  element?: undefined,
  options?: boolean | AddEventListenerOptions
): void {
  const savedHandler = useRef(handler);

  useEffect(() => {
    savedHandler.current = handler;
  }, [handler]);

  useEffect(() => {
    const eventListener = (event: WindowEventMap[K]) => savedHandler.current(event);
    window.addEventListener(eventName, eventListener, options);
    return () => window.removeEventListener(eventName, eventListener, options);
  }, [eventName, options]);
}
```

---

## 11. Best Practices

1. **Always type useState** when the initial value doesn't convey the full type.
2. **Type useRef correctly** — `null` for DOM refs, initial value for mutable refs.
3. **Type useImperativeHandle** with an interface for the exposed API.
4. **Use generic return types** for custom hooks that work with arbitrary data.
5. **Type useCallback** parameters explicitly when the callback is complex.
6. **Use `React.ChangeEvent<HTMLInputElement>`** for input change handlers.
7. **Avoid `useEffect` for derived state** — use `useMemo` instead.
8. **Type custom hook returns** with explicit interfaces for clarity.

---

## Interview Questions

1. What is the type difference between `useRef<T>(null)` and `useRef<T>(initialValue)`?
2. How do you type a custom hook that returns a tuple?
3. Explain the difference between `useEffect` and `useLayoutEffect` types.
4. How do you type `useImperativeHandle` to expose a custom API?
5. Create a typed generic `useFetch` hook — what types are needed?
6. How do you type event listeners in custom hooks?
7. What is the return type of `useCallback`?
8. How do you type `useReducer` with lazy initialization?
9. How would you create a type-safe `useLocalStorage` hook?
10. What are the typing challenges with `useContext`?
