# Props Typing in React + TypeScript

## Overview

Props are the primary way to pass data into React components. Properly typed props catch bugs at compile time, serve as documentation, and improve the developer experience with autocompletion and type inference.

---

## 1. Props Interface Naming Conventions

```typescript
// Convention: ComponentName + Props
interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
}

const UserCard: React.FC<UserCardProps> = ({ name, email, avatar }) => {
  return (
    <div className="user-card">
      {avatar && <img src={avatar} alt={name} />}
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
};

// Alternative: using type alias (equivalent for most cases)
type ButtonProps = {
  label: string;
  onClick: () => void;
  disabled?: boolean;
};

// Interface allows declaration merging — useful for extending
interface BaseProps {
  className?: string;
  id?: string;
}

// Extend with interface
interface IconButtonProps extends BaseProps {
  icon: React.ReactNode;
  label: string;
  onClick: () => void;
}

// Extend with type intersection
type DangerButtonProps = BaseProps & {
  label: string;
  onClick: () => void;
};
```

---

## 2. Optional Props

```typescript
// Using ? for optional props
interface SearchInputProps {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  onSubmit?: (value: string) => void;
  autoFocus?: boolean;
  maxLength?: number;
}

const SearchInput: React.FC<SearchInputProps> = ({
  placeholder = 'Search...',
  value = '',
  onChange,
  onSubmit,
  autoFocus = false,
  maxLength = 100,
}) => {
  return (
    <input
      type="search"
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === 'Enter') onSubmit?.(value);
      }}
      autoFocus={autoFocus}
      maxLength={maxLength}
    />
  );
};

// Optional with union types
interface StatusBadgeProps {
  status: 'active' | 'inactive' | 'pending';
  label?: string;  // Optional — defaults based on status
  showIcon?: boolean; // Optional boolean
}

// Required props with union — all variants must be handled
type Size = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

interface AlertProps {
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  size: Size;  // Required — no default
  dismissible?: boolean;
  onDismiss?: () => void;
}
```

---

## 3. Default Props

```typescript
// Method 1: Destructuring defaults (most common)
interface CardProps {
  title: string;
  variant?: 'elevated' | 'outlined' | 'filled';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  borderRadius?: 'none' | 'sm' | 'md' | 'lg' | 'full';
}

const Card: React.FC<CardProps> = ({
  title,
  variant = 'elevated',
  padding = 'md',
  borderRadius = 'md',
}) => {
  return (
    <div className={`card card-${variant} p-${padding} rounded-${borderRadius}`}>
      <h3>{title}</h3>
    </div>
  );
};

// Method 2: defaultProps (legacy — still works but discouraged)
const CardLegacy: React.FC<CardProps> = ({ title, variant, padding, borderRadius }) => {
  return (
    <div className={`card card-${variant} p-${padding} rounded-${borderRadius}`}>
      <h3>{title}</h3>
    </div>
  );
};

CardLegacy.defaultProps = {
  variant: 'elevated',
  padding: 'md',
  borderRadius: 'md',
};

// Method 3: Factory function defaults
interface ApiConfigProps {
  baseUrl: string;
  timeout?: number;
  retries?: number;
  headers?: Record<string, string>;
}

function createDefaultConfig(overrides?: Partial<ApiConfigProps>): ApiConfigProps {
  return {
    baseUrl: 'https://api.example.com',
    timeout: 5000,
    retries: 3,
    headers: { 'Content-Type': 'application/json' },
    ...overrides,
  };
}
```

---

## 4. Render Props Pattern

```typescript
import React from 'react';

// Render prop with children as function
interface MouseTrackerProps {
  children: (position: { x: number; y: number }) => React.ReactNode;
}

const MouseTracker: React.FC<MouseTrackerProps> = ({ children }) => {
  const [position, setPosition] = React.useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    setPosition({ x: e.clientX, y: e.clientY });
  };

  return (
    <div onMouseMove={handleMouseMove} style={{ height: '100vh' }}>
      {children(position)}
    </div>
  );
};

// Usage
<MouseTracker>
  {({ x, y }) => (
    <div>
      Mouse position: ({x}, {y})
    </div>
  )}
</MouseTracker>;

// Typed render prop with generic
interface DataFetcherProps<T> {
  url: string;
  children: (data: T | null, loading: boolean, error: Error | null) => React.ReactNode;
}

function DataFetcher<T>({ url, children }: DataFetcherProps<T>) {
  const [data, setData] = React.useState<T | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<Error | null>(null);

  React.useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => setError(err))
      .finally(() => setLoading(false));
  }, [url]);

  return <>{children(data, loading, error)}</>;
}

// Usage
<DataFetcher<User[]> url="/api/users">
  {(users, loading, error) => {
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} />;
    return <UserList users={users!} />;
  }}
</DataFetcher>;
```

---

## 5. Props Spreading

```typescript
// Spreading native HTML attributes
interface CustomButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant: 'primary' | 'secondary';
}

const CustomButton: React.FC<CustomButtonProps> = ({
  variant,
  className,
  children,
  ...restProps  // All native button props are spread
}) => {
  return (
    <button
      className={`btn btn-${variant} ${className ?? ''}`}
      {...restProps}
    >
      {children}
    </button>
  );
};

// Usage — all native button props work
<CustomButton
  variant="primary"
  onClick={() => console.log('clicked')}
  disabled={false}
  type="submit"
  aria-label="Submit form"
  data-testid="submit-btn"
>
  Submit
</CustomButton>;

// Spreading with controlled overrides
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

const Input: React.FC<InputProps> = ({ label, error, id, ...rest }) => {
  const inputId = id || label.toLowerCase().replace(/\s/g, '-');

  return (
    <div className="input-group">
      <label htmlFor={inputId}>{label}</label>
      <input
        id={inputId}
        className={error ? 'input-error' : ''}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : undefined}
        {...rest}
      />
      {error && (
        <span id={`${inputId}-error`} className="error">
          {error}
        </span>
      )}
    </div>
  );
};
```

---

## 6. Generic Components

```typescript
import React from 'react';

// Generic table component
interface Column<T> {
  key: keyof T & string;
  header: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
  sortable?: boolean;
  width?: number;
}

interface TableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
  keyExtractor: (row: T) => string;
}

function Table<T extends Record<string, any>>({
  data,
  columns,
  onRowClick,
  keyExtractor,
}: TableProps<T>) {
  return (
    <table>
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key} style={{ width: col.width }}>
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row) => (
          <tr
            key={keyExtractor(row)}
            onClick={() => onRowClick?.(row)}
          >
            {columns.map((col) => (
              <td key={col.key}>
                {col.render
                  ? col.render(row[col.key], row)
                  : String(row[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Usage
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

<Table<User>
  data={users}
  keyExtractor={(user) => String(user.id)}
  onRowClick={(user) => navigate(`/users/${user.id}`)}
  columns={[
    { key: 'name', header: 'Name', sortable: true },
    { key: 'email', header: 'Email' },
    {
      key: 'role',
      header: 'Role',
      render: (value) => <Badge>{value as string}</Badge>,
    },
  ]}
/>;
```

---

## 7. Props with Events

```typescript
// Typed event handler props
interface FormProps {
  onSubmit: (data: FormData) => void;
  onReset: () => void;
  onChange?: (field: string, value: string) => void;
  onError?: (error: FormError) => void;
}

interface FormError {
  field: string;
  message: string;
  code: string;
}

// Typed callbacks with specific signatures
interface DataTableProps<T> {
  data: T[];
  onRowSelect: (selectedRows: T[], selectedIds: string[]) => void;
  onSort: (column: keyof T, direction: 'asc' | 'desc') => void;
  onFilter: (filters: Record<string, string>) => void;
  onPageChange: (page: number, pageSize: number) => void;
}

// Event handler types from DOM
interface InteractiveListProps {
  items: string[];
  onItemClick: (item: string, event: React.MouseEvent<HTMLLIElement>) => void;
  onItemDoubleClick: (item: string, event: React.MouseEvent<HTMLLIElement>) => void;
  onItemKeyDown: (item: string, event: React.KeyboardEvent<HTMLLIElement>) => void;
  onContextMenu: (item: string, event: React.MouseEvent<HTMLLIElement>) => void;
}

// Callback returning a value
interface SelectProps<T> {
  options: { label: string; value: T }[];
  value: T;
  onChange: (newValue: T) => void;
  onBeforeChange?: (oldValue: T, newValue: T) => boolean; // Can cancel
}
```

---

## 8. Discriminated Props (Tagged Unions)

```typescript
import React from 'react';

// Discriminated union for different notification types
interface BaseNotificationProps {
  id: string;
  timestamp: Date;
}

interface InfoNotification extends BaseNotificationProps {
  type: 'info';
  message: string;
}

interface SuccessNotification extends BaseNotificationProps {
  type: 'success';
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}

interface WarningNotification extends BaseNotificationProps {
  type: 'warning';
  message: string;
  details: string;
  onDismiss: () => void;
}

interface ErrorNotification extends BaseNotificationProps {
  type: 'error';
  message: string;
  error: Error;
  retryable: boolean;
  onRetry?: () => void;
  onDismiss: () => void;
}

type NotificationProps =
  | InfoNotification
  | SuccessNotification
  | WarningNotification
  | ErrorNotification;

const Notification: React.FC<NotificationProps> = (props) => {
  switch (props.type) {
    case 'info':
      return <div className="notification info">{props.message}</div>;

    case 'success':
      return (
        <div className="notification success">
          {props.message}
          {props.actionLabel && (
            <button onClick={props.onAction}>{props.actionLabel}</button>
          )}
        </div>
      );

    case 'warning':
      return (
        <div className="notification warning">
          {props.message}
          <details>{props.details}</details>
          <button onClick={props.onDismiss}>Dismiss</button>
        </div>
      );

    case 'error':
      return (
        <div className="notification error">
          {props.message}
          {props.retryable && (
            <button onClick={props.onRetry}>Retry</button>
          )}
          <button onClick={props.onDismiss}>Dismiss</button>
        </div>
      );
  }
};

// Another example: polymorphic Modal
interface ModalBaseProps {
  title: string;
  onClose: () => void;
}

interface AlertModalProps extends ModalBaseProps {
  variant: 'alert';
  message: string;
  confirmLabel?: string;
  onConfirm: () => void;
}

interface ConfirmModalProps extends ModalBaseProps {
  variant: 'confirm';
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}

interface FormModalProps extends ModalBaseProps {
  variant: 'form';
  children: React.ReactNode;
  onSubmit: () => void;
  submitLabel?: string;
  isSubmitting?: boolean;
}

type ModalProps = AlertModalProps | ConfirmModalProps | FormModalProps;

const Modal: React.FC<ModalProps> = (props) => {
  // TypeScript narrows `props` based on `variant`
  return (
    <div className="modal">
      <h2>{props.title}</h2>
      <p>{props.message}</p>
      {/* Switch on variant to access variant-specific props */}
    </div>
  );
};
```

---

## 9. Props Validation Patterns

```typescript
// Runtime validation with Zod
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  role: z.enum(['admin', 'user', 'guest']),
  avatar: z.string().url().optional(),
});

type ValidatedUserProps = z.infer<typeof UserSchema>;

// React component with validated props
const UserForm: React.FC = () => {
  const [errors, setErrors] = React.useState<Record<string, string>>({});

  const handleSubmit = (data: unknown) => {
    const result = UserSchema.safeParse(data);
    if (!result.success) {
      const fieldErrors: Record<string, string> = {};
      result.error.issues.forEach((issue) => {
        const field = issue.path.join('.');
        fieldErrors[field] = issue.message;
      });
      setErrors(fieldErrors);
      return;
    }
    // result.data is fully typed as ValidatedUserProps
    submitUser(result.data);
  };

  return <form>...</form>;
};

// Compile-time validation with branded types
type Email = string & { readonly __brand: 'Email' };
type UserId = number & { readonly __brand: 'UserId' };

function createEmail(value: string): Email {
  if (!value.includes('@')) {
    throw new Error('Invalid email');
  }
  return value as Email;
}

function createUserId(value: number): UserId {
  if (value <= 0) {
    throw new Error('Invalid user ID');
  }
  return value as UserId;
}

interface UserProfileProps {
  userId: UserId;   // Must be a branded UserId
  email: Email;     // Must be a branded Email
  name: string;
}

// This would be a compile error:
// <UserProfileProps userId={123} email="invalid" name="test" />

// This works:
<UserProfile userId={createUserId(123)} email={createEmail("test@example.com")} name="Test" />;
```

---

## 10. Best Practices

1. **Use interfaces for component props** — they support declaration merging and are easier to extend.
2. **Use discriminated unions** for components with multiple variants.
3. **Prefer destructuring with defaults** over `defaultProps`.
4. **Spread rest props** for wrapper components to maintain native element compatibility.
5. **Use `PropsWithChildren`** utility type when children are optional.
6. **Make props required by default** — only use `?` when the default value exists.
7. **Name callback props** with `on` prefix: `onClick`, `onChange`, `onSubmit`.
8. **Use generic components** for reusable data-driven components.
9. **Validate runtime data** with Zod/Joi when props come from external sources.
10. **Use branded types** for domain-specific strings/numbers to prevent mixing.

---

## Interview Questions

1. What is the difference between `interface` and `type` for defining props?
2. How do you handle props spreading with custom and native HTML props?
3. Explain discriminated unions for React props with an example.
4. How do you type a render props pattern?
5. What are branded types and when would you use them in props?
6. How do you create a generic React component that works with any data type?
7. How would you type a component that accepts different prop combinations?
8. What is `PropsWithChildren` and when should you use it?
9. How do you handle default props in TypeScript React components?
10. Explain the difference between `ComponentProps` and manually defining props.
