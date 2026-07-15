# Component Typing in React + TypeScript

## Overview

Typing React components correctly is the foundation of a type-safe React application. This guide covers every aspect of component typing from basic FC usage to advanced patterns like `forwardRef`, `lazy`, and `memo`.

---

## 1. The `FC` Type (FunctionComponent)

`React.FC` is a generic type that provides type checking for function components.

```typescript
import React, { FC } from 'react';

// Basic FC usage
const Greeting: FC = () => {
  return <h1>Hello, World!</h1>;
};

// FC with props — Props is automatically inferred
interface GreetingProps {
  name: string;
  age?: number;
}

const Greeting: FC<GreetingProps> = ({ name, age }) => {
  return (
    <h1>
      Hello, {name}! {age && `You are ${age} years old.`}
    </h1>
  );
};

// Usage
<Greeting name="Alice" age={30} />
<Greeting name="Bob" />
```

### FC Implicit `children`

Before React 18, `React.FC` implicitly included `children` in its type definition. After React 18, `children` must be explicitly declared.

```typescript
// React 17 and earlier — children is implicit
const Card: FC<{ title: string }> = ({ title, children }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
};

// React 18+ — children must be explicit
interface CardProps {
  title: string;
  children: React.ReactNode;
}

const Card: FC<CardProps> = ({ title, children }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
};
```

### FC with Default Props

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

const Button: FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  onClick,
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

---

## 2. Function Components Without FC

Many teams prefer plain function signatures over `FC` for clarity and to avoid implicit `children` issues.

```typescript
// Plain function component with explicit return type
interface AvatarProps {
  src: string;
  alt: string;
  size?: number;
}

function Avatar({ src, alt, size = 48 }: AvatarProps): JSX.Element {
  return (
    <img
      src={src}
      alt={alt}
      width={size}
      height={size}
      style={{ borderRadius: '50%' }}
    />
  );
}

// Arrow function without FC
const Badge = ({ count }: { count: number }): JSX.Element => {
  return <span className="badge">{count > 99 ? '99+' : count}</span>;
};
```

---

## 3. Return Types

```typescript
// JSX.Element — most common
const Header = (): JSX.Element => {
  return <header>Site Header</header>;
};

// React.ReactElement — more precise
const Footer = (): React.ReactElement => {
  return <footer>Site Footer</footer>;
};

// ReactNode — can return strings, numbers, null, fragments
const MaybeGreeting = ({ show }: { show: boolean }): React.ReactNode => {
  if (!show) return null;
  return <span>Hello!</span>;
};

// void — for components that render nothing (side effects only)
const Logger = ({ message }: { message: string }): void => {
  console.log(message);
  // Component returns nothing
};
```

### JSX.Element vs ReactNode vs ReactElement

```typescript
import React from 'react';

// JSX.Element — a React element (what JSX produces)
const element: JSX.Element = <div>Hello</div>;

// React.ReactElement — same as JSX.Element in most cases
const reactElement: React.ReactElement = <div>Hello</div>;

// ReactNode — any renderable thing (most permissive)
const node: React.ReactNode = 'Hello';           // string
const node2: React.ReactNode = 42;               // number
const node3: React.ReactNode = null;             // null
const node4: React.ReactNode = <div>Hello</div>; // element
const node5: React.ReactNode = ['a', 'b'];       // array
const node6: React.ReactNode = undefined;        // undefined
```

---

## 4. Children Typing

```typescript
import React from 'react';

// React.ReactNode — the most flexible children type
interface WrapperProps {
  children: React.ReactNode;
}

const Wrapper: React.FC<WrapperProps> = ({ children }) => {
  return <div className="wrapper">{children}</div>;
};

// React.ReactElement — only React elements (no strings, numbers)
interface StrictWrapperProps {
  children: React.ReactElement;
}

// Single child only
interface SingleChildProps {
  children: React.ReactElement;
}

const SingleChild: React.FC<SingleChildProps> = ({ children }) => {
  return <div className="single">{children}</div>;
};

// Render function children
interface RenderProps {
  children: (data: { count: number }) => React.ReactNode;
}

const Counter: React.FC<RenderProps> = ({ children }) => {
  const [count, setCount] = React.useState(0);
  return <div>{children({ count })}</div>;
};

// Usage
<Counter>
  {({ count }) => <span>Count: {count}</span>}
</Counter>;

// PropsWithChildren utility type
import { PropsWithChildren } from 'react';

interface LayoutProps {
  title: string;
}

// PropsWithChildren<LayoutProps> = LayoutProps & { children?: ReactNode }
const Layout: React.FC<PropsWithChildren<LayoutProps>> = ({ title, children }) => {
  return (
    <div>
      <h1>{title}</h1>
      {children}
    </div>
  );
};
```

---

## 5. ComponentProps and ComponentPropsWithoutRef

Extract the props type of any component:

```typescript
import React from 'react';
import { ComponentProps, ComponentPropsWithoutRef } from 'react';

// Get props of a native element
type InputProps = ComponentProps<'input'>;
// Equivalent to React.InputHTMLAttributes<HTMLInputElement>

// Get props of a custom component
interface MyButtonProps {
  label: string;
  onClick: () => void;
  variant: 'primary' | 'secondary';
}

const MyButton: React.FC<MyButtonProps> = ({ label, onClick, variant }) => {
  return <button className={variant}>{label}</button>;
};

type MyButtonPropsExtracted = ComponentProps<typeof MyButton>;
// { label: string; onClick: () => void; variant: 'primary' | 'secondary' }

// ComponentPropsWithoutRef excludes ref
type ButtonWithoutRef = ComponentPropsWithoutRef<typeof MyButton>;

// ComponentPropsWithRef includes ref
type ButtonWithRef = ComponentPropsWithRef<typeof MyButton>;
```

---

## 6. displayName

`displayName` helps with debugging in React DevTools, especially for wrapped components.

```typescript
import React from 'react';

// Simple component with displayName
const UserCard: React.FC<{ name: string }> = ({ name }) => {
  return <div>{name}</div>;
};

UserCard.displayName = 'UserCard';

// displayName is critical for memo, forwardRef, and HOC
const MemoizedUserCard = React.memo(UserCard);
MemoizedUserCard.displayName = 'MemoizedUserCard';

// HOC with displayName
function withLoading<P extends object>(
  WrappedComponent: React.ComponentType<P>
) {
  const WithLoading: React.FC<P & { isLoading: boolean }> = ({
    isLoading,
    ...props
  }) => {
    if (isLoading) return <div>Loading...</div>;
    return <WrappedComponent {...(props as P)} />;
  };

  WithLoading.displayName = `WithLoading(${WrappedComponent.displayName || WrappedComponent.name || 'Component'})`;

  return WithLoading;
}
```

---

## 7. memo Typing

`React.memo` wraps a component to prevent unnecessary re-renders.

```typescript
import React from 'react';

interface TodoItemProps {
  id: number;
  title: string;
  completed: boolean;
  onToggle: (id: number) => void;
}

// Basic memo — type is automatically inferred
const TodoItem: React.FC<TodoItemProps> = React.memo(({ id, title, completed, onToggle }) => {
  return (
    <li onClick={() => onToggle(id)}>
      <span style={{ textDecoration: completed ? 'line-through' : 'none' }}>
        {title}
      </span>
    </li>
  );
});

// Memo with custom comparator
const ExpensiveList: React.FC<{ items: string[]; onSelect: (item: string) => void }> =
  React.memo(
    ({ items, onSelect }) => {
      return (
        <ul>
          {items.map((item) => (
            <li key={item} onClick={() => onSelect(item)}>
              {item}
            </li>
          ))}
        </ul>
      );
    },
    (prevProps, nextProps) => {
      // Return true if props are equal (skip re-render)
      return prevProps.items.length === nextProps.items.length &&
        prevProps.items.every((item, i) => item === nextProps.items[i]);
    }
  );

// Generic memo component
function MemoizedGeneric<T extends { id: string }>({
  items,
  renderItem,
}: {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}) {
  return <div>{items.map(renderItem)}</div>;
}

const MemoizedGenericComponent = React.memo(MemoizedGeneric);
```

---

## 8. lazy Typing

`React.lazy` enables code-splitting with full type safety.

```typescript
import React, { lazy, Suspense } from 'react';

// Basic lazy loading
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Lazy with named export
const Dashboard = lazy(() =>
  import('./Dashboard').then((module) => ({ default: module.Dashboard }))
);

// Lazy with type assertion
const Settings = lazy<React.ComponentType<{ userId: string }>>(() =>
  import('./Settings')
);

// Lazy with Suspense wrapper
function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}

// Lazy route wrapper pattern
interface LazyRouteProps {
  component: React.LazyExoticComponent<React.ComponentType<any>>;
}

const LazyRoute: React.FC<LazyRouteProps> = ({ component: Component }) => {
  return (
    <Suspense fallback={<div>Loading page...</div>}>
      <Component />
    </Suspense>
  );
};
```

---

## 9. forwardRef Typing

```typescript
import React, { forwardRef, useImperativeHandle, useRef } from 'react';

// Basic forwardRef with native element
const TextInput = forwardRef<HTMLInputElement, { placeholder?: string }>(
  ({ placeholder }, ref) => {
    return <input ref={ref} placeholder={placeholder} />;
  }
);

// forwardRef with custom component
interface FancyInputProps {
  label: string;
  error?: string;
}

interface FancyInputRef {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

const FancyInput = forwardRef<FancyInputRef, FancyInputProps>(
  ({ label, error }, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      clear: () => {
        if (inputRef.current) inputRef.current.value = '';
      },
      getValue: () => inputRef.current?.value ?? '',
    }));

    return (
      <div>
        <label>{label}</label>
        <input ref={inputRef} />
        {error && <span className="error">{error}</span>}
      </div>
    );
  }
);

FancyInput.displayName = 'FancyInput';

// Usage
function Form() {
  const fancyRef = useRef<FancyInputRef>(null);

  return (
    <div>
      <FancyInput ref={fancyRef} label="Email" />
      <button onClick={() => fancyRef.current?.focus()}>Focus</button>
      <button onClick={() => fancyRef.current?.clear()}>Clear</button>
    </div>
  );
}
```

---

## 10. Generic Components

```typescript
import React from 'react';

// Generic list component
interface ListProps<T> {
  items: T[];
  keyExtractor: (item: T) => string;
  renderItem: (item: T, index: number) => React.ReactNode;
}

function List<T>({ items, keyExtractor, renderItem }: ListProps<T>): JSX.Element {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={[{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]}
  keyExtractor={(user) => String(user.id)}
  renderItem={(user) => <span>{user.name}</span>}
/>;

// Generic select component
interface SelectProps<T extends string | number> {
  options: { label: string; value: T }[];
  value: T;
  onChange: (value: T) => void;
  placeholder?: string;
}

function Select<T extends string | number>({
  options,
  value,
  onChange,
  placeholder,
}: SelectProps<T>): JSX.Element {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value as unknown as T)}
    >
      {placeholder && <option value="">{placeholder}</option>}
      {options.map((opt) => (
        <option key={String(opt.value)} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
}
```

---

## 11. ComponentType and ComponentProps

```typescript
import React from 'react';

// ComponentType — union of FC and ClassComponent
type AnyComponent = React.ComponentType<{ name: string }>;

// Function that accepts any component
function renderComponent(Component: AnyComponent) {
  return <Component name="test" />;
}

// Polymorphic "as" prop component
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

// Usage
interface TextProps {
  color?: 'primary' | 'secondary' | 'muted';
  weight?: 'bold' | 'normal';
}

type TextComponentProps<C extends React.ElementType> =
  PolymorphicComponentProps<C, TextProps>;

function Text<C extends React.ElementType = 'span'>({
  as,
  color,
  weight,
  children,
  ...restProps
}: TextComponentProps<C>) {
  const Component = as || 'span';
  return (
    <Component
      className={`text-${color} text-weight-${weight}`}
      {...restProps}
    >
      {children}
    </Component>
  );
}

// Works with different elements
<Text as="h1" color="primary" weight="bold">Heading</Text>
<Text as="p" color="secondary">Paragraph</Text>
<Text as="span" color="muted">Inline text</Text>
```

---

## 12. Best Practices

1. **Prefer explicit prop interfaces** over inline types for reusability.
2. **Use `React.ReactNode`** for children unless you need to restrict the type.
3. **Avoid `any`** — use `unknown` and narrow with type guards.
4. **Name prop interfaces** with the component name + `Props` suffix.
5. **Use `ComponentProps`** to extract and extend native element props.
6. **Set `displayName`** on memoized and HOC-wrapped components.
7. **Prefer `forwardRef` with `useImperativeHandle`** over ref forwarding alone.
8. **Use generic components** when the component works with arbitrary data types.
9. **Prefer `React.FC`** or plain functions consistently — pick one convention.
10. **Always type event handlers** — don't rely on implicit `any` from React events.

---

## Interview Questions

1. What is the difference between `JSX.Element`, `ReactElement`, and `ReactNode`?
2. Why did React 18 remove implicit `children` from `FC`?
3. How do you extract the props type of a component?
4. What is the difference between `ComponentProps` and `ComponentPropsWithoutRef`?
5. When would you use `React.memo` vs `useMemo`?
6. How does `React.lazy` work with TypeScript?
7. What is `useImperativeHandle` and why is it needed with `forwardRef`?
8. How do you type a generic component in React?
9. What is the polymorphic `as` prop pattern?
10. Why should you set `displayName` on wrapped components?
