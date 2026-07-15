# React + TypeScript Interview Questions

## 30+ Questions with Detailed Answers

---

### 1. What is the difference between `JSX.Element`, `ReactElement`, and `ReactNode`?

**Answer:**

- `JSX.Element` — the return type of JSX expressions. It's essentially the same as `React.ReactElement`.
- `React.ReactElement` — a plain object describing a React element type (`$$typeof: Symbol(react.element)`).
- `React.ReactNode` — the most inclusive type. It can be `JSX.Element | string | number | boolean | null | undefined | ReactNode[]`.

```typescript
const a: JSX.Element = <div />;       // Only JSX elements
const b: React.ReactNode = 'hello';   // Strings, numbers, elements, arrays, null, undefined
const c: React.ReactNode = 42;        // Valid
// const d: JSX.Element = 42;         // Compile error!
```

**When to use each:**
- `ReactNode` — for `children` props (most flexible).
- `JSX.Element` — for function return types that always return JSX.
- `ReactElement` — when you need to access element properties like `type` or `props`.

---

### 2. Why did React 18 remove implicit `children` from `FC`?

**Answer:**

In React 17, `React.FC` automatically included `children` in its type definition:

```typescript
// React 17
const Comp: React.FC = ({ children }) => <div>{children}</div>; // OK
```

In React 18, `children` was removed from `FC` to:
1. Make component types more explicit.
2. Allow components to opt out of accepting children.
3. Align with TypeScript's stricter type-checking.

```typescript
// React 18+
interface CardProps {
  title: string;
  children: React.ReactNode; // Must explicitly declare
}

const Card: React.FC<CardProps> = ({ title, children }) => (
  <div><h2>{title}</h2>{children}</div>
);
```

---

### 3. How do you type a controlled form with multiple fields?

**Answer:**

```typescript
interface FormState {
  name: string;
  email: string;
  age: number;
}

const [form, setForm] = useState<FormState>({
  name: '',
  email: '',
  age: 0,
});

const handleChange = <K extends keyof FormState>(field: K, value: FormState[K]) => {
  setForm((prev) => ({ ...prev, [field]: value }));
};

// Usage
<input value={form.name} onChange={(e) => handleChange('name', e.target.value)} />
<input value={form.age} onChange={(e) => handleChange('age', Number(e.target.value))} type="number" />
```

---

### 4. Explain discriminated unions for React props with an example.

**Answer:**

Discriminated unions use a common literal property (the discriminant) to narrow the type:

```typescript
type NotificationProps =
  | { type: 'info'; message: string }
  | { type: 'success'; message: string; actionLabel: string }
  | { type: 'error'; message: string; error: Error; retryable: boolean };

function Notification(props: NotificationProps) {
  switch (props.type) {
    case 'info':
      return <div>{props.message}</div>;
    case 'success':
      return <div>{props.message} <button>{props.actionLabel}</button></div>;
    case 'error':
      return <div>{props.message} {props.retryable && <button>Retry</button>}</div>;
  }
}
```

TypeScript narrows `props` in each branch, so you only have access to the properties of the current variant.

---

### 5. How do you type a custom hook that returns a tuple?

**Answer:**

```typescript
function useToggle(initial: boolean = false): [boolean, () => void, (value: boolean) => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue((v) => !v), []);
  const set = useCallback((v: boolean) => setValue(v), []);
  return [value, toggle, set];
}

// Usage
const [isOpen, toggleOpen, setOpen] = useToggle(false);
```

The return type is explicitly typed as a tuple, not an array. This ensures destructuring works with the correct types at each position.

---

### 6. When should you use `useState` vs `useReducer`?

**Answer:**

- **`useState`** — for simple, independent state (strings, numbers, booleans, small objects).
- **`useReducer`** — for complex state with multiple related values, many possible transitions, or when the next state depends on the previous one.

```typescript
// useState — simple
const [count, setCount] = useState(0);

// useReducer — complex
const [state, dispatch] = useReducer(todoReducer, initialState);
```

**Rule of thumb:** If you have more than 2-3 pieces of related state, or if updating one piece depends on another, use `useReducer`.

---

### 7. How do you type `useReducer` with discriminated unions?

**Answer:**

```typescript
interface State {
  count: number;
  step: number;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'setStep'; step: number }
  | { type: 'reset' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + state.step };
    case 'decrement': return { ...state, count: state.count - state.step };
    case 'setStep': return { ...state, step: action.step };
    case 'reset': return { count: 0, step: 1 };
  }
}
```

The `never` exhaustiveness check ensures all cases are handled:

```typescript
default:
  const _exhaustive: never = action;
  return state;
```

---

### 8. How do you type `useRef` for DOM elements vs mutable values?

**Answer:**

```typescript
// DOM ref — initial value is null
const inputRef = useRef<HTMLInputElement>(null);
// Type: React.RefObject<HTMLInputElement>
// { readonly current: HTMLInputElement | null }

// Mutable ref — initial value provided
const countRef = useRef<number>(0);
// Type: React.MutableRefObject<number>
// { current: number }

// Timer ref
const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
```

Key difference: DOM refs have `readonly current` (can only be set via React), while mutable refs have writable `current`.

---

### 9. How do you create a generic React component?

**Answer:**

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>): JSX.Element {
  return (
    <ul>
      {items.map((item) => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage — T is inferred from items
<List
  items={[{ id: 1, name: 'Alice' }]}
  keyExtractor={(u) => String(u.id)}
  renderItem={(u) => <span>{u.name}</span>}
/>
```

TypeScript infers `T` from the `items` prop, so the `renderItem` callback receives the correct type automatically.

---

### 10. What is the polymorphic `as` prop pattern?

**Answer:**

The polymorphic pattern lets a component render as any HTML element while maintaining type safety:

```typescript
type AsProp<C extends React.ElementType> = { as?: C };

type PolymorphicProps<C extends React.ElementType, Props = {}> =
  Props & AsProp<C> & Omit<React.ComponentPropsWithoutRef<C>, keyof (AsProp<C> & Props)>;

function Text<C extends React.ElementType = 'span'>({
  as, children, ...props
}: PolymorphicProps<C, { color?: string }>) {
  const Component = as || 'span';
  return <Component {...props}>{children}</Component>;
}

// Usage
<Text as="h1" color="primary">Heading</Text>
<Text as="p" color="secondary">Paragraph</Text>
<Text as="a" href="/about">Link</Text>
```

---

### 11. How do you type event handlers in React?

**Answer:**

```typescript
// Input change
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

// Button click
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.currentTarget.textContent);
};

// Form submit
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

// Keyboard
const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  if (e.key === 'Enter') submit();
};
```

---

### 12. How do you type a context with a default value?

**Answer:**

Two strategies:

```typescript
// Strategy 1: undefined default + guard hook
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

function useTheme(): ThemeContextType {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be within ThemeProvider');
  return ctx;
}

// Strategy 2: no-op defaults
const ThemeContext = createContext<ThemeContextType>({
  theme: 'light',
  toggleTheme: () => {}, // Silent no-op
});
```

---

### 13. How do you type `forwardRef` with a custom imperative handle?

**Answer:**

```typescript
interface InputHandle {
  focus: () => void;
  clear: () => void;
}

const FancyInput = forwardRef<InputHandle, { placeholder?: string }>(
  ({ placeholder }, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      clear: () => { if (inputRef.current) inputRef.current.value = ''; },
    }), []);

    return <input ref={inputRef} placeholder={placeholder} />;
  }
);

// Usage
const ref = useRef<InputHandle>(null);
<FancyInput ref={ref} />
ref.current?.focus();
ref.current?.clear();
```

---

### 14. What are the changes to `forwardRef` in React 19?

**Answer:**

In React 19, `ref` is passed as a regular prop instead of a second argument:

```typescript
// React 18: forwardRef required
const Input = forwardRef<HTMLInputElement, Props>(({ placeholder }, ref) => {
  return <input ref={ref} placeholder={placeholder} />;
});

// React 19: ref is a regular prop
function Input({ placeholder, ref }: Props & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} placeholder={placeholder} />;
}
```

Benefits:
- `forwardRef` is no longer needed.
- Generic components become simpler.
- `displayName` can be set as a static property.

---

### 15. How do you type a HOC in React?

**Answer:**

```typescript
// HOC that adds logging
function withLogging<P extends object>(
  WrappedComponent: React.ComponentType<P>
) {
  const WithLogging: React.FC<P> = (props) => {
    useEffect(() => {
      console.log('Mounted:', WrappedComponent.displayName);
    }, []);
    return <WrappedComponent {...props} />;
  };

  WithLogging.displayName = `withLogging(${WrappedComponent.displayName || 'Component'})`;
  return WithLogging;
}

// HOC that adds extra props
interface WithAuthProps {
  isAuthenticated: boolean;
}

function withAuth<P extends object>(
  Wrapped: React.ComponentType<P & WithAuthProps>
) {
  return function AuthenticatedComponent(props: Omit<P, keyof WithAuthProps>) {
    const { isAuthenticated } = useAuth();
    return <Wrapped {...(props as P)} isAuthenticated={isAuthenticated} />;
  };
}
```

---

### 16. How do you type `useEffect` cleanup functions?

**Answer:**

```typescript
useEffect(() => {
  const controller = new AbortController();

  fetch('/api/data', { signal: controller.signal })
    .then((res) => res.json())
    .then(setData);

  // Cleanup return type: void | (() => void)
  return () => controller.abort();
}, []);
```

---

### 17. How do you type a component with optional `children`?

**Answer:**

```typescript
// Option 1: React.ReactNode (most flexible)
interface WrapperProps {
  title: string;
  children?: React.ReactNode;
}

// Option 2: PropsWithChildren utility
import { PropsWithChildren } from 'react';
type WrapperProps2 = PropsWithChildren<{ title: string }>;

// Option 3: Single child only
interface SingleChildProps {
  children: React.ReactElement;
}
```

---

### 18. How do you type a form with react-hook-form?

**Answer:**

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const Schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type FormData = z.infer<typeof Schema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(Schema),
  });

  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}
      <button type="submit">Login</button>
    </form>
  );
}
```

---

### 19. How do you type a component that accepts different prop combinations?

**Answer:**

Use discriminated unions or conditional types:

```typescript
// Discriminated union
type ButtonProps =
  | { variant: 'link'; href: string; children: React.ReactNode }
  | { variant: 'button'; type?: 'button' | 'submit'; children: React.ReactNode };

function Button(props: ButtonProps) {
  if (props.variant === 'link') {
    return <a href={props.href}>{props.children}</a>;
  }
  return <button type={props.type}>{props.children}</button>;
}
```

---

### 20. How do you type a render props pattern?

**Answer:**

```typescript
interface RenderProps<T> {
  data: T;
  children: (item: T) => React.ReactNode;
}

function RenderItem<T>({ data, children }: RenderProps<T>) {
  return <div>{children(data)}</div>;
}

// Usage
<RenderItem data={{ name: 'Alice', age: 30 }}>
  {(user) => <span>{user.name} is {user.age}</span>}
</RenderItem>
```

---

### 21. How do you prevent type errors when spreading props?

**Answer:**

```typescript
// When extending native HTML attributes
interface CustomInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

function CustomInput({ label, error, className, ...rest }: CustomInputProps) {
  return (
    <div>
      <label>{label}</label>
      <input className={`${className ?? ''} ${error ? 'error' : ''}`} {...rest} />
      {error && <span>{error}</span>}
    </div>
  );
}
```

The `...rest` spread contains all native `input` props except those explicitly destructured.

---

### 22. How do you type a higher-order component that wraps a component with context?

**Answer:**

```typescript
function withTheme<P extends object>(
  Component: React.ComponentType<P & { theme: Theme }>
) {
  return function ThemedComponent(props: Omit<P, 'theme'>) {
    const theme = useContext(ThemeContext);
    return <Component {...(props as P)} theme={theme} />;
  };
}
```

---

### 23. How do you type a component that uses `useImperativeHandle`?

**Answer:**

```typescript
interface VideoHandle {
  play: () => void;
  pause: () => void;
  getTime: () => number;
}

const Video = forwardRef<VideoHandle, { src: string }>(({ src }, ref) => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useImperativeHandle(ref, () => ({
    play: () => videoRef.current?.play(),
    pause: () => videoRef.current?.pause(),
    getTime: () => videoRef.current?.currentTime ?? 0,
  }), []);

  return <video ref={videoRef} src={src} />;
});
```

---

### 24. How do you type conditional rendering based on props?

**Answer:**

```typescript
interface StatusProps {
  status: 'loading' | 'error' | 'success';
  message?: string;
  error?: Error;
  data?: unknown;
}

function StatusDisplay({ status, message, error, data }: StatusProps) {
  switch (status) {
    case 'loading':
      return <Spinner />;
    case 'error':
      return <div>Error: {error?.message}</div>;
    case 'success':
      return <div>Data: {JSON.stringify(data)}</div>;
  }
}
```

---

### 25. How do you type a component that uses `useCallback` with a complex function?

**Answer:**

```typescript
interface SearchHandler {
  (query: string, filters: Filter[]): void;
}

function SearchBar({ onSearch }: { onSearch: SearchHandler }) {
  const handleSearch = useCallback<SearchHandler>((query, filters) => {
    onSearch(query, filters);
  }, [onSearch]);

  return <SearchInput onSearch={handleSearch} />;
}
```

---

### 26. How do you type a component that wraps third-party libraries?

**Answer:**

```typescript
// Wrapping a library component
import Select from 'react-select';

interface CustomSelectProps {
  options: { label: string; value: string }[];
  value?: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

function CustomSelect({ options, value, onChange, placeholder }: CustomSelectProps) {
  return (
    <Select
      options={options}
      value={options.find((o) => o.value === value)}
      onChange={(selected) => onChange(selected?.value ?? '')}
      placeholder={placeholder}
    />
  );
}
```

---

### 27. How do you type a component with compound pattern?

**Answer:**

```typescript
interface AccordionContextType {
  openItems: Set<string>;
  toggle: (id: string) => void;
}

const AccordionContext = createContext<AccordionContextType | undefined>(undefined);

function Accordion({ children }: { children: React.ReactNode }) {
  const [openItems, setOpenItems] = useState(new Set<string>());
  const toggle = useCallback((id: string) => {
    setOpenItems((prev) => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }, []);

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div>{children}</div>
    </AccordionContext.Provider>
  );
}

Accordion.Item = function AccordionItem({ id, title, children }: {
  id: string;
  title: string;
  children: React.ReactNode;
}) {
  const ctx = useContext(AccordionContext)!;
  const isOpen = ctx.openItems.has(id);

  return (
    <div>
      <button onClick={() => ctx.toggle(id)}>{title}</button>
      {isOpen && <div>{children}</div>}
    </div>
  );
};
```

---

### 28. How do you type a portal component?

**Answer:**

```typescript
import { createPortal } from 'react-dom';

interface ModalPortalProps {
  children: React.ReactNode;
  containerId?: string;
}

function ModalPortal({ children, containerId = 'modal-root' }: ModalPortalProps) {
  const [container, setContainer] = useState<HTMLElement | null>(null);

  useEffect(() => {
    setContainer(document.getElementById(containerId));
  }, [containerId]);

  if (!container) return null;

  return createPortal(children, container);
}
```

---

### 29. How do you type a component that accepts a ref from a parent?

**Answer:**

```typescript
interface InputProps {
  label: string;
}

// Using forwardRef
const Input = forwardRef<HTMLInputElement, InputProps>(({ label }, ref) => (
  <div>
    <label>{label}</label>
    <input ref={ref} />
  </div>
));

// React 19: ref as prop
function Input({ label, ref }: InputProps & { ref?: React.Ref<HTMLInputElement> }) {
  return (
    <div>
      <label>{label}</label>
      <input ref={ref} />
    </div>
  );
}
```

---

### 30. How do you type a component that uses context and generics?

**Answer:**

```typescript
function createFormContext<T extends Record<string, any>>() {
  const Context = createContext<{
    values: T;
    setValue: <K extends keyof T>(key: K, value: T[K]) => void;
  } | undefined>(undefined);

  function Provider({ children, initialValues }: {
    children: React.ReactNode;
    initialValues: T;
  }) {
    const [values, setValues] = useState(initialValues);

    const setValue = useCallback(<K extends keyof T>(key: K, value: T[K]) => {
      setValues((prev) => ({ ...prev, [key]: value }));
    }, []);

    return (
      <Context.Provider value={{ values, setValue }}>
        {children}
      </Context.Provider>
    );
  }

  function useForm() {
    const ctx = useContext(Context);
    if (!ctx) throw new Error('useForm must be within FormProvider');
    return ctx;
  }

  return { Provider, useForm };
}

// Usage
interface LoginForm {
  email: string;
  password: string;
}

const { Provider: LoginFormProvider, useForm: useLoginForm } = createFormContext<LoginForm>();
```

---

### 31. How do you type a lazy-loaded component?

**Answer:**

```typescript
import React, { lazy, Suspense } from 'react';

// Basic lazy loading — type is inferred
const Dashboard = lazy(() => import('./Dashboard'));

// Lazy with named export
const Settings = lazy(() =>
  import('./Settings').then((module) => ({ default: module.Settings }))
);

// Lazy with explicit type
const HeavyChart = lazy<React.ComponentType<{ data: ChartData[] }>>(
  () => import('./HeavyChart')
);

// Wrapper with Suspense
function LazyRoute({ component: Component }: {
  component: React.LazyExoticComponent<React.ComponentType<any>>;
}) {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Component />
    </Suspense>
  );
}
```

---

### 32. How do you type a component that uses `useMemo` for expensive computation?

**Answer:**

```typescript
interface Props {
  items: Item[];
  sortKey: keyof Item;
  filterFn?: (item: Item) => boolean;
}

function SortedList({ items, sortKey, filterFn }: Props) {
  // useMemo return type is inferred from the callback
  const processed = useMemo(() => {
    let result = filterFn ? items.filter(filterFn) : [...items];
    result.sort((a, b) => {
      if (a[sortKey] < b[sortKey]) return -1;
      if (a[sortKey] > b[sortKey]) return 1;
      return 0;
    });
    return result;
  }, [items, sortKey, filterFn]);

  return (
    <ul>
      {processed.map((item) => (
        <li key={item.id}>{String(item[sortKey])}</li>
      ))}
    </ul>
  );
}
```

---

### 33. How do you type a component that wraps Redux or Zustand?

**Answer:**

```typescript
// Zustand store
interface AppState {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

const useAppStore = create<AppState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));

// Typed component
function Counter() {
  const { count, increment, decrement, reset } = useAppStore();

  return (
    <div>
      <span>{count}</span>
      <button onClick={increment}>+</button>
      <button onClick={decrement}>-</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

---

### 34. How do you handle TypeScript errors when using `React.cloneElement`?

**Answer:**

```typescript
// cloneElement is notoriously hard to type
interface Props {
  children: React.ReactElement<{ onClick?: () => void }>;
  label: string;
}

function ClickWrapper({ children, label }: Props) {
  // Use type assertion for cloneElement
  return React.cloneElement(children, {
    onClick: () => {
      console.log(label);
      children.props.onClick?.();
    },
  });
}

// Better: use children as function
interface BetterProps {
  children: (handlers: { onClick: () => void }) => React.ReactNode;
  label: string;
}

function BetterClickWrapper({ children, label }: BetterProps) {
  return (
    <div>
      {children({ onClick: () => console.log(label) })}
    </div>
  );
}
```

---

### 35. How do you type a component with dynamic tag names?

**Answer:**

```typescript
// Component that renders as different HTML elements
type HeadingLevel = 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';

interface HeadingProps {
  level: HeadingLevel;
  children: React.ReactNode;
  className?: string;
}

// Method 1: Record of components
const headingComponents: Record<HeadingLevel, React.FC<React.HTMLAttributes<HTMLHeadingElement>>> = {
  h1: (props) => <h1 {...props} />,
  h2: (props) => <h2 {...props} />,
  h3: (props) => <h3 {...props} />,
  h4: (props) => <h4 {...props} />,
  h5: (props) => <h5 {...props} />,
  h6: (props) => <h6 {...props} />,
};

function Heading({ level, children, className }: HeadingProps) {
  const Component = headingComponents[level];
  return <Component className={className}>{children}</Component>;
}

// Method 2: Polymorphic component
function DynamicHeading<C extends HeadingLevel = 'h1'>({
  as,
  children,
  ...props
}: {
  as: C;
  children: React.ReactNode;
} & React.ComponentPropsWithoutRef<C>) {
  const Component = as;
  return <Component {...props}>{children}</Component>;
}
```
