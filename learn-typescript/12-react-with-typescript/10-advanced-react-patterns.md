# Advanced React Patterns with TypeScript

## Overview

This guide covers advanced typing patterns in React: generic components, compound components, render props, HOCs, polymorphic components, and type-safe routing/i18n.

---

## 1. Generic Components

```typescript
import React from 'react';

// Generic API response hook
interface ApiResponse<T> {
  data: T | null;
  error: Error | null;
  loading: boolean;
}

function useApi<T>(url: string): ApiResponse<T> {
  const [state, setState] = useState<ApiResponse<T>>({
    data: null,
    error: null,
    loading: true,
  });

  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then((data: T) => setState({ data, error: null, loading: false }))
      .catch((error) => setState({ data: null, error, loading: false }));
  }, [url]);

  return state;
}

// Generic modal component
interface ModalProps<T> {
  isOpen: boolean;
  onClose: () => void;
  data: T;
  render: (data: T) => React.ReactNode;
  footer?: (data: T) => React.ReactNode;
}

function Modal<T>({ isOpen, onClose, data, render, footer }: ModalProps<T>) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>×</button>
        <div className="modal-body">{render(data)}</div>
        {footer && <div className="modal-footer">{footer(data)}</div>}
      </div>
    </div>
  );
}

// Generic list with sorting
interface SortableListProps<T> {
  items: T[];
  sortKey: keyof T;
  sortDirection?: 'asc' | 'desc';
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function SortableList<T extends Record<string, any>>({
  items,
  sortKey,
  sortDirection = 'asc',
  renderItem,
  keyExtractor,
}: SortableListProps<T>) {
  const sorted = useMemo(() => {
    return [...items].sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      const cmp = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
      return sortDirection === 'asc' ? cmp : -cmp;
    });
  }, [items, sortKey, sortDirection]);

  return (
    <div>
      {sorted.map((item, index) => (
        <div key={keyExtractor(item)}>{renderItem(item, index)}</div>
      ))}
    </div>
  );
}
```

---

## 2. Compound Components

```typescript
import React, { createContext, useContext, useState, useMemo } from 'react';

// --- Tabs Compound Component ---

interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | undefined>(undefined);

function useTabsContext() {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab components must be used within Tabs');
  return context;
}

// Root component
interface TabsProps {
  defaultTab: string;
  children: React.ReactNode;
  onChange?: (tabId: string) => void;
}

function Tabs({ defaultTab, children, onChange }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  const value = useMemo(
    () => ({
      activeTab,
      setActiveTab: (id: string) => {
        setActiveTab(id);
        onChange?.(id);
      },
    }),
    [activeTab, onChange]
  );

  return <TabsContext.Provider value={value}>{children}</TabsContext.Provider>;
}

// Tab list component
interface TabListProps {
  children: React.ReactNode;
  ariaLabel: string;
}

function TabList({ children, ariaLabel }: TabListProps) {
  return (
    <div role="tablist" aria-label={ariaLabel}>
      {children}
    </div>
  );
}

// Individual tab
interface TabProps {
  id: string;
  children: React.ReactNode;
  disabled?: boolean;
}

function Tab({ id, children, disabled = false }: TabProps) {
  const { activeTab, setActiveTab } = useTabsContext();

  return (
    <button
      role="tab"
      id={`tab-${id}`}
      aria-selected={activeTab === id}
      aria-controls={`panel-${id}`}
      disabled={disabled}
      onClick={() => setActiveTab(id)}
      className={activeTab === id ? 'tab active' : 'tab'}
    >
      {children}
    </button>
  );
}

// Tab panel
interface TabPanelProps {
  id: string;
  children: React.ReactNode;
}

function TabPanel({ id, children }: TabPanelProps) {
  const { activeTab } = useTabsContext();

  if (activeTab !== id) return null;

  return (
    <div
      role="tabpanel"
      id={`panel-${id}`}
      aria-labelledby={`tab-${id}`}
    >
      {children}
    </div>
  );
}

// Attach compound properties
Tabs.TabList = TabList;
Tabs.Tab = Tab;
Tabs.TabPanel = TabPanel;

// Usage
function Settings() {
  return (
    <Tabs defaultTab="general" onChange={(tab) => console.log('Tab changed:', tab)}>
      <Tabs.TabList ariaLabel="Settings">
        <Tabs.Tab id="general">General</Tabs.Tab>
        <Tabs.Tab id="security">Security</Tabs.Tab>
        <Tabs.Tab id="notifications">Notifications</Tabs.Tab>
      </Tabs.TabList>

      <Tabs.TabPanel id="general">
        <GeneralSettings />
      </Tabs.TabPanel>
      <Tabs.TabPanel id="security">
        <SecuritySettings />
      </Tabs.TabPanel>
      <Tabs.TabPanel id="notifications">
        <NotificationSettings />
      </Tabs.TabPanel>
    </Tabs>
  );
}
```

---

## 3. Render Props with Types

```typescript
import React from 'react';

// Mouse position tracker
interface Position {
  x: number;
  y: number;
}

interface MouseTrackerProps {
  render: (position: Position) => React.ReactNode;
}

function MouseTracker({ render }: MouseTrackerProps) {
  const [position, setPosition] = useState<Position>({ x: 0, y: 0 });

  return (
    <div
      style={{ height: '100vh' }}
      onMouseMove={(e) => setPosition({ x: e.clientX, y: e.clientY })}
    >
      {render(position)}
    </div>
  );
}

// Usage
<MouseTracker
  render={({ x, y }) => (
    <div>Mouse is at ({x}, {y})</div>
  )}
/>;

// Generic data fetcher
interface DataFetcherProps<T> {
  url: string;
  children: (result: {
    data: T | null;
    loading: boolean;
    error: Error | null;
    refetch: () => void;
  }) => React.ReactNode;
}

function DataFetcher<T>({ url, children }: DataFetcherProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(url);
      setData(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => { fetchData(); }, [fetchData]);

  return <>{children({ data, loading, error, refetch: fetchData })}</>;
}

// Usage
<DataFetcher<User[]> url="/api/users">
  {({ data, loading, error }) => {
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} />;
    return <UserList users={data!} />;
  }}
</DataFetcher>;

// Window size render prop
interface WindowSize {
  width: number;
  height: number;
}

interface WithWindowSizeProps {
  children: (size: WindowSize) => React.ReactNode;
}

function WithWindowSize({ children }: WithWindowSizeProps) {
  const [size, setSize] = useState<WindowSize>({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setSize({ width: window.innerWidth, height: window.innerHeight });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return <>{children(size)}</>;
}
```

---

## 4. HOC Typing

```typescript
import React from 'react';

// Basic HOC with types
function withLogging<P extends object>(
  WrappedComponent: React.ComponentType<P>
) {
  const WithLogging: React.FC<P> = (props) => {
    useEffect(() => {
      console.log('Component mounted:', WrappedComponent.displayName || 'Unknown');
      return () => console.log('Component unmounted');
    }, []);

    return <WrappedComponent {...props} />;
  };

  WithLogging.displayName = `withLogging(${WrappedComponent.displayName || WrappedComponent.name || 'Component'})`;
  return WithLogging;
}

// HOC with additional props
interface WithAuthProps {
  isAuthenticated: boolean;
  user: User | null;
}

function withAuth<P extends object>(
  WrappedComponent: React.ComponentType<P & WithAuthProps>
) {
  return function WithAuthComponent(props: Omit<P, keyof WithAuthProps>) {
    const { user, isAuthenticated } = useAuth();

    if (!isAuthenticated) {
      return <Redirect to="/login" />;
    }

    return <WrappedComponent {...(props as P)} isAuthenticated={isAuthenticated} user={user} />;
  };
}

// HOC that adds theme props
interface ThemeProps {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

function withTheme<P extends object>(
  WrappedComponent: React.ComponentType<P & ThemeProps>
) {
  return function WithThemeComponent(props: Omit<P, keyof ThemeProps>) {
    const { theme, toggleTheme } = useTheme();
    return <WrappedComponent {...(props as P)} theme={theme} toggleTheme={toggleTheme} />;
  };
}

// Composing HOCs
interface DashboardProps {
  title: string;
}

function Dashboard({ title, isAuthenticated, user, theme }: DashboardProps & WithAuthProps & ThemeProps) {
  return (
    <div className={`dashboard theme-${theme}`}>
      <h1>{title}</h1>
      <p>Welcome, {user?.name}</p>
    </div>
  );
}

// Compose multiple HOCs
const EnhancedDashboard = withTheme(
  withAuth(
    withLogging(Dashboard)
  )
);

// Usage
<EnhancedDashboard title="My Dashboard" />;
```

---

## 5. Polymorphic Components (as prop)

```typescript
import React from 'react';

// Type definitions
type AsProp<C extends React.ElementType> = {
  as?: C;
};

type PropsToOmit<C extends React.ElementType, P> = keyof (AsProp<C> & P);

type PolymorphicComponentProps<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props & AsProp<C>> &
  Omit<React.ComponentPropsWithoutRef<C>, PropsToOmit<C, Props>>;

type PolymorphicRef<C extends React.ElementType> =
  React.ComponentPropsWithRef<C>['ref'];

// Text component
interface TextProps {
  color?: 'primary' | 'secondary' | 'muted';
  weight?: 'bold' | 'normal' | 'light';
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

function Text<C extends React.ElementType = 'span'>({
  as,
  color,
  weight,
  size,
  children,
  ...restProps
}: PolymorphicComponentProps<C, TextProps>) {
  const Component = as || 'span';

  return (
    <Component
      className={`text-${color} text-weight-${weight} text-size-${size}`}
      {...restProps}
    >
      {children}
    </Component>
  );
}

// Usage — works with any HTML element
<Text as="h1" color="primary" weight="bold" size="xl">
  Heading
</Text>
<Text as="p" color="secondary" size="md">
  Paragraph
</Text>
<Text as="span" color="muted" size="sm">
  Inline
</Text>

// Button component
interface ButtonStyleProps {
  variant?: 'filled' | 'outlined' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

function PolymorphicButton<C extends React.ElementType = 'button'>({
  as,
  variant = 'filled',
  size = 'md',
  children,
  ...restProps
}: PolymorphicComponentProps<C, ButtonStyleProps>) {
  const Component = as || 'button';

  return (
    <Component
      className={`btn btn-${variant} btn-${size}`}
      {...restProps}
    >
      {children}
    </Component>
  );
}

// Works as button, anchor, or any element
<PolymorphicButton variant="filled" size="md">Click</PolymorphicButton>
<PolymorphicButton as="a" href="/about" variant="outlined">Link</PolymorphicButton>
<PolymorphicButton as={RouterLink} to="/home" variant="ghost">Router Link</PolymorphicButton>
```

---

## 6. Type-Safe CSS-in-JS

```typescript
// Type-safe style props
type CSSPropertiesWithMedia = {
  base?: React.CSSProperties;
  sm?: React.CSSProperties;
  md?: React.CSSProperties;
  lg?: React.CSSProperties;
  xl?: React.CSSProperties;
};

// Type-safe style objects
interface CardStyles {
  container: React.CSSProperties;
  header: React.CSSProperties;
  body: React.CSSProperties;
  footer: React.CSSProperties;
}

const cardStyles: CardStyles = {
  container: {
    borderRadius: 8,
    overflow: 'hidden',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  header: {
    padding: '16px',
    borderBottom: '1px solid #eee',
  },
  body: {
    padding: '16px',
  },
  footer: {
    padding: '16px',
    borderTop: '1px solid #eee',
  },
};

// Variant-based styles with types
type ButtonVariant = 'primary' | 'secondary' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg';

const buttonStyles: Record<ButtonVariant, Record<ButtonSize, React.CSSProperties>> = {
  primary: {
    sm: { padding: '4px 8px', fontSize: '12px' },
    md: { padding: '8px 16px', fontSize: '14px' },
    lg: { padding: '12px 24px', fontSize: '16px' },
  },
  secondary: {
    sm: { padding: '4px 8px', fontSize: '12px', background: 'gray' },
    md: { padding: '8px 16px', fontSize: '14px', background: 'gray' },
    lg: { padding: '12px 24px', fontSize: '16px', background: 'gray' },
  },
  danger: {
    sm: { padding: '4px 8px', fontSize: '12px', background: 'red' },
    md: { padding: '8px 16px', fontSize: '14px', background: 'red' },
    lg: { padding: '12px 24px', fontSize: '16px', background: 'red' },
  },
};

// Type-safe theme
interface Theme {
  colors: {
    primary: string;
    secondary: string;
    background: string;
    text: string;
    error: string;
    success: string;
  };
  spacing: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
  };
  typography: {
    fontFamily: string;
    sizes: Record<'xs' | 'sm' | 'md' | 'lg' | 'xl', string>;
    weights: Record<'light' | 'normal' | 'bold', number>;
  };
  breakpoints: Record<'sm' | 'md' | 'lg' | 'xl', number>;
}

const theme: Theme = {
  colors: {
    primary: '#007bff',
    secondary: '#6c757d',
    background: '#ffffff',
    text: '#212529',
    error: '#dc3545',
    success: '#28a745',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  typography: {
    fontFamily: 'system-ui, sans-serif',
    sizes: { xs: '12px', sm: '14px', md: '16px', lg: '18px', xl: '20px' },
    weights: { light: 300, normal: 400, bold: 700 },
  },
  breakpoints: { sm: 576, md: 768, lg: 992, xl: 1200 },
};

// Styled component pattern
function styled<P>(
  Component: React.ComponentType<P>,
  styles: (props: P, theme: Theme) => React.CSSProperties
) {
  return function StyledComponent(props: P) {
    const theme = useTheme();
    const style = styles(props, theme);
    return <Component {...props} style={style} />;
  };
}

const StyledCard = styled('div', (props, theme) => ({
  background: theme.colors.background,
  borderRadius: theme.spacing.sm,
  padding: theme.spacing.md,
}));
```

---

## 7. Type-Safe Routing

```typescript
// Route configuration with types
interface RouteConfig {
  path: string;
  component: React.ComponentType<any>;
  requiresAuth?: boolean;
  roles?: string[];
  children?: RouteConfig[];
}

// Type-safe route params
interface AppRoutes {
  '/': {};
  '/users': {};
  '/users/:userId': { userId: string };
  '/users/:userId/posts': { userId: string };
  '/users/:userId/posts/:postId': { userId: string; postId: string };
  '/settings': {};
  '/settings/profile': {};
  '/settings/security': {};
}

// Type-safe navigation
function useNavigate() {
  return {
    push: <K extends keyof AppRoutes>(path: K, params: AppRoutes[K]) => {
      // Navigate with typed params
      console.log('Navigating to:', path, params);
    },
    replace: <K extends keyof AppRoutes>(path: K, params: AppRoutes[K]) => {
      console.log('Replacing with:', path, params);
    },
  };
}

// Type-safe Link component
interface LinkProps<K extends keyof AppRoutes> {
  to: K;
  params: AppRoutes[K];
  children: React.ReactNode;
}

function Link<K extends keyof AppRoutes>({ to, params, children }: LinkProps<K>) {
  return <a href={buildPath(to, params)}>{children}</a>;
}

// Usage — params are type-checked
<Link to="/users/:userId" params={{ userId: '123' }}>User</Link>
<Link to="/users/:userId/posts/:postId" params={{ userId: '123', postId: '456' }}>Post</Link>
// Compile error:
// <Link to="/users/:userId" params={{ postId: '456' }}>Invalid</Link>
```

---

## 8. Type-Safe i18n

```typescript
// Translation keys type
interface Translations {
  common: {
    save: string;
    cancel: string;
    delete: string;
    confirm: string;
    loading: string;
    error: string;
  };
  auth: {
    login: string;
    logout: string;
    signup: string;
    forgotPassword: string;
  };
  dashboard: {
    welcome: string;
    stats: string;
    recentActivity: string;
  };
}

type TranslationKey = keyof Translations;
type NestedKey<T> = {
  [K in keyof T]: T[K] extends object
    ? `${string & K}.${NestedKey<T[K]>}`
    : string & K;
}[keyof T];

type AllTranslationKeys = NestedKey<Translations>;
// 'common.save' | 'common.cancel' | 'auth.login' | ...

// Type-safe translation function
function createI18n(translations: Record<string, Translations>) {
  return {
    t: (key: AllTranslationKeys, locale: string = 'en'): string => {
      const keys = key.split('.');
      let value: any = translations[locale];
      for (const k of keys) {
        value = value?.[k];
      }
      return value ?? key;
    },
  };
}

const i18n = createI18n({ en: translations, es: spanishTranslations });

// Usage — type-checked keys
i18n.t('common.save', 'en');     // Works
i18n.t('auth.login', 'es');      // Works
// i18n.t('invalid.key');        // Compile error
```

---

## 9. Best Practices

1. **Use generics** for components that work with arbitrary data types.
2. **Prefer compound components** for complex UI with shared state.
3. **Use `as const`** for literal type inference in variants.
4. **Type HOCs** to preserve the wrapped component's props.
5. **Use polymorphic components** for element-agnostic wrappers.
6. **Create type-safe route configs** with parameter extraction.
7. **Use `NestedKey` utility types** for dot-notation keys in i18n.
8. **Prefer render props over HOCs** for simpler composition.

---

## Interview Questions

1. How do you create a generic React component that works with any data type?
2. Explain the compound component pattern with TypeScript.
3. What are the benefits of polymorphic components?
4. How do you type an HOC that adds additional props?
5. Create a type-safe routing system with TypeScript.
6. How do you type CSS-in-JS styles?
7. What is the render prop pattern and how do you type it?
8. How do you implement type-safe i18n?
9. How do you type a context with generics?
10. What are the trade-offs between HOCs, render props, and hooks?
