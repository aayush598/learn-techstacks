# forwardRef in React + TypeScript

## Overview

`React.forwardRef` lets a child component expose its DOM node (or an imperative handle) to a parent component. This guide covers the complete typing of `forwardRef`, generic patterns, and the React 19 changes.

---

## 1. Basic forwardRef Syntax

```typescript
import React, { forwardRef } from 'react';

// forwardRef<RefType, PropsType>
const TextInput = forwardRef<HTMLInputElement, { placeholder?: string }>(
  ({ placeholder }, ref) => {
    return <input ref={ref} placeholder={placeholder} />;
  }
);

// Usage
function Form() {
  const inputRef = React.useRef<HTMLInputElement>(null);

  return (
    <>
      <TextInput ref={inputRef} placeholder="Enter text" />
      <button onClick={() => inputRef.current?.focus()}>Focus</button>
    </>
  );
}
```

---

## 2. forwardRef with Custom Imperative Handle

```typescript
import React, { forwardRef, useImperativeHandle, useRef, useState } from 'react';

// Define the imperative API
interface VideoPlayerHandle {
  play: () => void;
  pause: () => void;
  seekTo: (time: number) => void;
  getCurrentTime: () => number;
  getDuration: () => number;
  setVolume: (volume: number) => void;
}

interface VideoPlayerProps {
  src: string;
  autoPlay?: boolean;
  onReady?: () => void;
}

const VideoPlayer = forwardRef<VideoPlayerHandle, VideoPlayerProps>(
  ({ src, autoPlay = false, onReady }, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const [isReady, setIsReady] = useState(false);

    useImperativeHandle(ref, () => ({
      play: () => videoRef.current?.play(),
      pause: () => videoRef.current?.pause(),
      seekTo: (time: number) => {
        if (videoRef.current) videoRef.current.currentTime = time;
      },
      getCurrentTime: () => videoRef.current?.currentTime ?? 0,
      getDuration: () => videoRef.current?.duration ?? 0,
      setVolume: (volume: number) => {
        if (videoRef.current) videoRef.current.volume = volume;
      },
    }), []);

    const handleLoadedData = () => {
      setIsReady(true);
      onReady?.();
    };

    return (
      <video
        ref={videoRef}
        src={src}
        autoPlay={autoPlay}
        onLoadedData={handleLoadedData}
        controls
      />
    );
  }
);

VideoPlayer.displayName = 'VideoPlayer';

// Usage
function VideoPage() {
  const playerRef = useRef<VideoPlayerHandle>(null);

  return (
    <div>
      <VideoPlayer
        ref={playerRef}
        src="/video.mp4"
        onReady={() => console.log('Ready!')}
      />
      <div className="controls">
        <button onClick={() => playerRef.current?.play()}>Play</button>
        <button onClick={() => playerRef.current?.pause()}>Pause</button>
        <button onClick={() => playerRef.current?.seekTo(30)}>Jump to 30s</button>
        <button onClick={() => {
          const time = playerRef.current?.getCurrentTime();
          console.log('Current time:', time);
        }}>Get Time</button>
      </div>
    </div>
  );
}
```

---

## 3. Generic forwardRef

```typescript
import React, { forwardRef, useImperativeHandle } from 'react';

// Generic forwardRef component
interface GenericListHandle<T> {
  scrollToItem: (item: T) => void;
  getItems: () => T[];
}

interface GenericListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

// TypeScript doesn't support generic forwardRef directly.
// Solution 1: Generic wrapper function
function createGenericList<T>() {
  const GenericList = forwardRef<GenericListHandle<T>, GenericListProps<T>>(
    ({ items, renderItem, keyExtractor }, ref) => {
      useImperativeHandle(ref, () => ({
        scrollToItem: (item: T) => {
          const element = document.getElementById(keyExtractor(item));
          element?.scrollIntoView({ behavior: 'smooth' });
        },
        getItems: () => items,
      }), [items, keyExtractor]);

      return (
        <div>
          {items.map((item) => (
            <div key={keyExtractor(item)} id={keyExtractor(item)}>
              {renderItem(item)}
            </div>
          ))}
        </div>
      );
    }
  );

  return GenericList;
}

// Usage
interface User {
  id: string;
  name: string;
}

const UserList = createGenericList<User>();

function App() {
  const listRef = useRef<GenericListHandle<User>>(null);

  return (
    <UserList
      ref={listRef}
      items={users}
      keyExtractor={(u) => u.id}
      renderItem={(u) => <span>{u.name}</span>}
    />
  );
}

// Solution 2: Cast the generic component
function GenericSelect<T extends string | number>(props: {
  ref?: React.Ref<{ getValue: () => T | null }>;
} & {
  options: { label: string; value: T }[];
  value?: T;
  onChange?: (value: T) => void;
}) {
  const { options, value, onChange, ref } = props;

  useImperativeHandle(ref, () => ({
    getValue: () => value ?? null,
  }), [value]);

  return (
    <select
      value={value}
      onChange={(e) => onChange?.(e.target.value as unknown as T)}
    >
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

## 4. forwardRef with Memo

```typescript
import React, { forwardRef, memo, useImperativeHandle, useRef } from 'react';

// Combining memo and forwardRef
interface SearchInputHandle {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

interface SearchInputProps {
  placeholder?: string;
  onSearch?: (query: string) => void;
  autoFocus?: boolean;
}

const SearchInput = memo(
  forwardRef<SearchInputHandle, SearchInputProps>(
    ({ placeholder = 'Search...', onSearch, autoFocus }, ref) => {
      const inputRef = useRef<HTMLInputElement>(null);

      useImperativeHandle(ref, () => ({
        focus: () => inputRef.current?.focus(),
        clear: () => {
          if (inputRef.current) inputRef.current.value = '';
        },
        getValue: () => inputRef.current?.value ?? '',
      }), []);

      return (
        <div className="search-input">
          <span className="search-icon">🔍</span>
          <input
            ref={inputRef}
            type="search"
            placeholder={placeholder}
            autoFocus={autoFocus}
            onChange={(e) => onSearch?.(e.target.value)}
          />
        </div>
      );
    }
  )
);

SearchInput.displayName = 'SearchInput';
```

---

## 5. forwardRef Patterns

```typescript
import React, { forwardRef, useImperativeHandle } from 'react';

// Pattern 1: Polymorphic forwarded component
type PolymorphicRef<C extends React.ElementType> =
  React.ComponentPropsWithRef<C>['ref'];

interface PolymorphicTextProps<C extends React.ElementType> {
  as?: C;
  children: React.ReactNode;
  color?: string;
}

const PolymorphicText = forwardRef<
  HTMLDivElement,
  PolymorphicTextProps<React.ElementType>
>(({ as: Component = 'div', children, color, ...restProps }, ref) => {
  return (
    <Component ref={ref} style={{ color }} {...restProps}>
      {children}
    </Component>
  );
});

// Pattern 2: Compound component with forwarded ref
interface DialogHandle {
  open: () => void;
  close: () => void;
}

interface DialogProps {
  title: string;
  children: React.ReactNode;
}

const Dialog = forwardRef<DialogHandle, DialogProps>(({ title, children }, ref) => {
  const [isOpen, setIsOpen] = useState(false);

  useImperativeHandle(ref, () => ({
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
  }), []);

  if (!isOpen) return null;

  return (
    <div className="dialog-overlay" onClick={() => setIsOpen(false)}>
      <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
        <h2>{title}</h2>
        {children}
        <button onClick={() => setIsOpen(false)}>Close</button>
      </div>
    </div>
  );
});

// Pattern 3: Accessible forwarded ref
interface AccessibleButtonHandle {
  focus: () => void;
  click: () => void;
}

interface AccessibleButtonProps {
  label: string;
  onClick?: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

const AccessibleButton = forwardRef<AccessibleButtonHandle, AccessibleButtonProps>(
  ({ label, onClick, disabled, variant = 'primary' }, ref) => {
    const buttonRef = useRef<HTMLButtonElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => buttonRef.current?.focus(),
      click: () => buttonRef.current?.click(),
    }), []);

    return (
      <button
        ref={buttonRef}
        className={`btn btn-${variant}`}
        onClick={onClick}
        disabled={disabled}
        aria-label={label}
        type="button"
      >
        {label}
      </button>
    );
  }
);
```

---

## 6. React 19 — forwardRef Deprecation

```typescript
// React 19: ref is passed as a regular prop
// forwardRef is no longer needed

// React 18:
const Input = forwardRef<HTMLInputElement, { placeholder?: string }>(
  ({ placeholder }, ref) => {
    return <input ref={ref} placeholder={placeholder} />;
  }
);

// React 19: ref is a regular prop
function Input({ placeholder, ref }: {
  placeholder?: string;
  ref?: React.Ref<HTMLInputElement>;
}) {
  return <input ref={ref} placeholder={placeholder} />;
}

// React 19: useImperativeHandle still works
function VideoPlayer({ src, ref }: {
  src: string;
  ref?: React.Ref<{
    play: () => void;
    pause: () => void;
  }>;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);

  useImperativeHandle(ref, () => ({
    play: () => videoRef.current?.play(),
    pause: () => videoRef.current?.pause(),
  }), []);

  return <video ref={videoRef} src={src} />;
}

// Generic component in React 19
function List<T extends { id: string }>({
  items,
  renderItem,
  ref,
}: {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  ref?: React.Ref<{ scrollToItem: (id: string) => void }>;
}) {
  useImperativeHandle(ref, () => ({
    scrollToItem: (id: string) => {
      document.getElementById(id)?.scrollIntoView();
    },
  }), []);

  return (
    <div>
      {items.map((item) => (
        <div key={item.id} id={item.id}>{renderItem(item)}</div>
      ))}
    </div>
  );
}
```

---

## 7. Best Practices

1. **Always set `displayName`** on forwarded components for DevTools.
2. **Use `useImperativeHandle`** to expose a minimal API, not the entire DOM node.
3. **Type the ref handle** with an interface for clarity.
4. **Prefer forwarding only what's needed** — avoid leaking internal DOM.
5. **Use `memo` with `forwardRef`** when the component is expensive.
6. **Consider React 19 patterns** — `ref` as a regular prop.
7. **Use generic `forwardRef` wrappers** when components need to work with arbitrary types.
8. **Test forwarded refs** by verifying the exposed API works correctly.

---

## Interview Questions

1. What is the signature of `React.forwardRef`?
2. How do you type a custom imperative handle with `useImperativeHandle`?
3. What is the difference between forwarding a DOM ref and a custom handle?
4. How do you create a generic component with `forwardRef`?
5. What changes did React 19 make to `forwardRef`?
6. How do you combine `memo` and `forwardRef`?
7. Why should you set `displayName` on forwarded components?
8. How do you expose only specific methods through `useImperativeHandle`?
9. When should you use `forwardRef` vs passing ref as a regular prop?
10. How do you forward a ref to a third-party component?
