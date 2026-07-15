# Context Typing in React + TypeScript

## Overview

React Context provides a way to pass data through the component tree without manually passing props. Proper typing ensures type safety and prevents runtime errors from undefined context values.

---

## 1. createContext Typing

```typescript
import { createContext } from 'react';

// Default value: undefined (use with a guard hook)
interface AuthContextType {
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
// Type: React.Context<AuthContextType | undefined>

// Default value: actual object (no guard needed)
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: 'light',
  toggleTheme: () => {},  // No-op default
});
// Type: React.Context<ThemeContextType>

// Default value: null
interface UserContextType {
  user: User | null;
  setUser: (user: User | null) => void;
}

const UserContext = createContext<UserContextType | null>(null);
```

---

## 2. Typed Context Provider

```typescript
import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';

// --- Complete Auth Context Example ---

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  updateProfile: (updates: Partial<User>) => void;
}

// Context with undefined default (requires guard)
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const login = useCallback(async (credentials: LoginCredentials) => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });
      if (!response.ok) throw new Error('Login failed');
      const data: User = await response.json();
      setUser(data);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    setUser(null);
  }, []);

  const updateProfile = useCallback((updates: Partial<User>) => {
    setUser((prev) => (prev ? { ...prev, ...updates } : null));
  }, []);

  const value = useMemo<AuthContextType>(
    () => ({
      user,
      isAuthenticated: user !== null,
      isLoading,
      login,
      logout,
      updateProfile,
    }),
    [user, isLoading, login, logout, updateProfile]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Typed consumer hook with guard
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

---

## 3. Context with Default Values

```typescript
import { createContext, useContext } from 'react';

// Strategy 1: No default + guard hook
interface NotificationContextType {
  notifications: Notification[];
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
}

const NotificationContext = createContext<NotificationContextType | null>(null);

export function useNotifications(): NotificationContextType {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be within NotificationProvider');
  }
  return context;
}

// Strategy 2: No-op defaults (no error, silent failure)
interface ModalContextType {
  openModal: (config: ModalConfig) => void;
  closeModal: () => void;
  isOpen: boolean;
}

const ModalContext = createContext<ModalContextType>({
  openModal: () => {},  // No-op
  closeModal: () => {}, // No-op
  isOpen: false,
});

// Strategy 3: Discriminated default
type DataContext<T> =
  | { status: 'loading' }
  | { status: 'loaded'; data: T }
  | { status: 'error'; error: Error };

function createContextWithDefault<T>() {
  return createContext<DataContext<T>>({ status: 'loading' });
}
```

---

## 4. Context with Generics

```typescript
import React, { createContext, useContext, useState, useMemo } from 'react';

// Generic context factory
interface StoreContextValue<T> {
  state: T;
  setState: React.Dispatch<React.SetStateAction<T>>;
  reset: () => void;
}

function createStoreContext<T>(defaultState: T) {
  const Context = createContext<StoreContextValue<T>>({
    state: defaultState,
    setState: () => {},
    reset: () => {},
  });

  function Provider({ children, initialState }: {
    children: React.ReactNode;
    initialState?: T;
  }) {
    const [state, setState] = useState<T>(initialState ?? defaultState);
    const reset = () => setState(defaultState);

    const value = useMemo(
      () => ({ state, setState, reset }),
      [state]
    );

    return <Context.Provider value={value}>{children}</Context.Provider>;
  }

  function useStore(): StoreContextValue<T> {
    return useContext(Context);
  }

  return { Provider, useStore, Context };
}

// Usage
interface CartState {
  items: { id: string; name: string; price: number; quantity: number }[];
  coupon: string | null;
}

const CartStore = createStoreContext<CartState>({
  items: [],
  coupon: null,
});

// In app
function App() {
  return (
    <CartStore.Provider initialState={{ items: [], coupon: 'SAVE20' }}>
      <CartPage />
    </CartStore.Provider>
  );
}

function CartPage() {
  const { state, setState, reset } = CartStore.useStore();
  // state is typed as CartState
  // setState accepts SetStateAction<CartState>
  return (
    <div>
      <p>{state.items.length} items</p>
      <button onClick={reset}>Clear Cart</button>
    </div>
  );
}
```

---

## 5. Multiple Contexts

```typescript
// Combining multiple contexts
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

interface LocaleContextType {
  locale: string;
  setLocale: (locale: string) => void;
  t: (key: string) => string;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);
const LocaleContext = createContext<LocaleContextType | undefined>(undefined);

// Combined provider
interface AppProviderProps {
  children: React.ReactNode;
}

function AppProvider({ children }: AppProviderProps) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [locale, setLocale] = useState('en');

  const themeValue = useMemo<ThemeContextType>(
    () => ({
      theme,
      toggleTheme: () => setTheme((t) => (t === 'light' ? 'dark' : 'light')),
    }),
    [theme]
  );

  const localeValue = useMemo<LocaleContextType>(
    () => ({
      locale,
      setLocale,
      t: (key: string) => translations[locale]?.[key] ?? key,
    }),
    [locale]
  );

  return (
    <ThemeContext.Provider value={themeValue}>
      <LocaleContext.Provider value={localeValue}>
        {children}
      </LocaleContext.Provider>
    </ThemeContext.Provider>
  );
}

// Typed hooks for each context
function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be within ThemeProvider');
  return context;
}

function useLocale(): LocaleContextType {
  const context = useContext(LocaleContext);
  if (!context) throw new Error('useLocale must be within LocaleProvider');
  return context;
}

// Combined hook
function useAppContext() {
  return { theme: useTheme(), locale: useLocale() };
}
```

---

## 6. Context Performance

```typescript
import React, { createContext, useContext, useMemo, useCallback, useState } from 'react';

// BAD: Creating new objects on every render
const BadContext = createContext({ count: 0, increment: () => {} });

function BadProvider({ children }: { children: React.ReactNode }) {
  const [count, setCount] = useState(0);

  // This creates a new object every render — all consumers re-render
  return (
    <BadContext.Provider value={{ count, increment: () => setCount(c => c + 1) }}>
      {children}
    </BadContext.Provider>
  );
}

// GOOD: Memoize the value
interface GoodContextType {
  count: number;
  increment: () => void;
}

const GoodContext = createContext<GoodContextType | undefined>(undefined);

function GoodProvider({ children }: { children: React.ReactNode }) {
  const [count, setCount] = useState(0);

  const increment = useCallback(() => {
    setCount((c) => c + 1);
  }, []);

  // useMemo ensures value object is stable across renders
  const value = useMemo<GoodContextType>(
    () => ({ count, increment }),
    [count, increment]
  );

  return (
    <GoodContext.Provider value={value}>{children}</GoodContext.Provider>
  );
}

// BEST: Split contexts for read/write separation
interface CountReadContextType {
  count: number;
}

interface CountWriteContextType {
  increment: () => void;
  decrement: () => void;
}

const CountReadContext = createContext<CountReadContextType>({ count: 0 });
const CountWriteContext = createContext<CountWriteContextType>({
  increment: () => {},
  decrement: () => {},
});

function CountProvider({ children }: { children: React.ReactNode }) {
  const [count, setCount] = useState(0);

  const readValue = useMemo(() => ({ count }), [count]);
  const writeValue = useMemo(
    () => ({
      increment: () => setCount((c) => c + 1),
      decrement: () => setCount((c) => c - 1),
    }),
    []
  );

  return (
    <CountWriteContext.Provider value={writeValue}>
      <CountReadContext.Provider value={readValue}>
        {children}
      </CountReadContext.Provider>
    </CountWriteContext.Provider>
  );
}

// Components that only read don't re-render when increment changes
function CountDisplay() {
  const { count } = useContext(CountReadContext);
  return <span>{count}</span>;
}

// Components that only write don't re-render when count changes
function IncrementButton() {
  const { increment } = useContext(CountWriteContext);
  return <button onClick={increment}>+</button>;
}
```

---

## 7. Context vs Dependency Injection

```typescript
// Pattern 1: Service injection via context
interface ApiService {
  get: <T>(url: string) => Promise<T>;
  post: <T>(url: string, data: unknown) => Promise<T>;
  put: <T>(url: string, data: unknown) => Promise<T>;
  delete: <T>(url: string) => Promise<T>;
}

const ApiContext = createContext<ApiService | null>(null);

function useApi(): ApiService {
  const api = useContext(ApiContext);
  if (!api) throw new Error('useApi requires ApiProvider');
  return api;
}

// Pattern 2: Configuration injection
interface AppConfig {
  apiUrl: string;
  features: {
    darkMode: boolean;
    notifications: boolean;
    analytics: boolean;
  };
  limits: {
    maxUploadSize: number;
    maxListItems: number;
  };
}

const ConfigContext = createContext<AppConfig | null>(null);

function useConfig(): AppConfig {
  const config = useContext(ConfigContext);
  if (!config) throw new Error('useConfig requires ConfigProvider');
  return config;
}

// Usage in component
function SettingsPage() {
  const config = useConfig();

  return (
    <div>
      {config.features.darkMode && <DarkModeToggle />}
      {config.features.notifications && <NotificationSettings />}
    </div>
  );
}
```

---

## 8. Best Practices

1. **Always type `createContext`** — never use `createContext({})` without a type.
2. **Use a guard hook** that throws if context is undefined.
3. **Memoize context values** with `useMemo` to prevent unnecessary re-renders.
4. **Split read/write contexts** for performance-critical scenarios.
5. **Use `useCallback`** for functions passed through context.
6. **Prefer multiple small contexts** over one large context.
7. **Use generic factories** for reusable context patterns.
8. **Set display names** on provider components for debugging.

---

## Interview Questions

1. How do you type `createContext` with a default value of `undefined`?
2. Why should you memoize context values?
3. What is the "split context" pattern and when should you use it?
4. How do you create a generic context factory in TypeScript?
5. Explain the difference between `useContext` returning `T` vs `T | undefined`.
6. How do you handle context performance in large applications?
7. What are the alternatives to React Context for state management?
8. How do you test components that consume typed context?
9. Create a type-safe context for a theme system.
10. When should you use context vs props drilling vs state management libraries?
