# Ref Typing in React + TypeScript

## Overview

Refs provide a way to access DOM nodes or React elements created in the render method. Proper typing of refs is critical for type safety when interacting with the DOM or exposing imperative APIs.

---

## 1. useRef for DOM Elements

```typescript
import { useRef, useEffect } from 'react';

// DOM ref — initial value is always null
const inputRef = useRef<HTMLInputElement>(null);
// Type: React.RefObject<HTMLInputElement>
// { readonly current: HTMLInputElement | null }

const divRef = useRef<HTMLDivElement>(null);
const canvasRef = useRef<HTMLCanvasElement>(null);
const videoRef = useRef<HTMLVideoElement>(null);

// Accessing the DOM element
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    // Optional chaining because current can be null
    inputRef.current?.focus();
  };

  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus Input</button>
    </>
  );
}

// Canvas example
function DrawingCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.fillStyle = 'blue';
    ctx.fillRect(0, 0, 100, 100);
  }, []);

  return <canvas ref={canvasRef} width={200} height={200} />;
}

// Multiple DOM refs
function MediaControl() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);
  const volumeRef = useRef<HTMLInputElement>(null);

  const play = () => videoRef.current?.play();
  const pause = () => videoRef.current?.pause();

  return (
    <div>
      <video ref={videoRef} src="/video.mp4" />
      <div ref={progressRef} className="progress-bar" />
      <input ref={volumeRef} type="range" min={0} max={100} />
    </div>
  );
}
```

---

## 2. useRef for Mutable Values

```typescript
import { useRef, useEffect } from 'react';

// Mutable ref — not for DOM, for storing mutable values
const countRef = useRef<number>(0);
// Type: React.MutableRefObject<number>
// { current: number }  (writable, initial value required)

// Timer reference
function Timer() {
  const [seconds, setSeconds] = useState(0);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const start = () => {
    intervalRef.current = setInterval(() => {
      setSeconds((s) => s + 1);
    }, 1000);
  };

  const stop = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

  return (
    <div>
      <p>{seconds}s</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  );
}

// Storing previous values
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}

// Storing callback references (latest callback pattern)
function useLatest<T extends (...args: any[]) => any>(callback: T): React.MutableRefObject<T> {
  const ref = useRef<T>(callback);
  ref.current = callback;
  return ref;
}

// Storing mounted state
function useIsMounted(): React.MutableRefObject<boolean> {
  const isMounted = useRef(false);

  useEffect(() => {
    isMounted.current = true;
    return () => { isMounted.current = false; };
  }, []);

  return isMounted;
}

// Usage in async operation
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const isMounted = useIsMounted();

  useEffect(() => {
    fetchUser(userId).then((data) => {
      if (isMounted.current) {
        setUser(data);
      }
    });
  }, [userId, isMounted]);

  return user ? <div>{user.name}</div> : <div>Loading...</div>;
}
```

---

## 3. Ref Callback Typing

```typescript
import { useCallback, useRef } from 'react';

// Ref callback — receives the element or null
function MeasuredDiv() {
  const measureRef = useCallback((node: HTMLDivElement | null) => {
    if (node) {
      const rect = node.getBoundingClientRect();
      console.log('Size:', rect.width, rect.height);
    }
  }, []);

  return <div ref={measuredDiv}>Measured content</div>;
}

// Ref callback for dynamic element type
function DynamicElement({ as: Component }: { as: React.ElementType }) {
  const ref = useCallback(
    (node: HTMLElement | null) => {
      if (node) {
        // node is HTMLElement — the common base
        console.log('Element mounted:', node.tagName);
      }
    },
    []
  );

  return <Component ref={ref} />;
}

// Ref callback with cleanup
function ResizeObserverExample() {
  const ref = useCallback((node: HTMLDivElement | null) => {
    if (!node) return;

    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        console.log('Size changed:', entry.contentRect);
      }
    });

    observer.observe(node);

    // Cleanup function
    return () => observer.disconnect();
  }, []);

  return <div ref={ref}>Resizable content</div>;
}

// Merging ref callback with existing ref
function useMergedRef<T>(
  ...refs: (React.Ref<T> | undefined)[]
): React.RefCallback<T> {
  return useCallback(
    (node: T | null) => {
      refs.forEach((ref) => {
        if (!ref) return;
        if (typeof ref === 'function') {
          ref(node);
        } else {
          (ref as React.MutableRefObject<T | null>).current = node;
        }
      });
    },
    refs
  );
}

// Usage
function CombinedRefInput() {
  const internalRef = useRef<HTMLInputElement>(null);
  const externalRef = useRef<HTMLInputElement>(null);
  const mergedRef = useMergedRef<HTMLInputElement>(internalRef, externalRef);

  return <input ref={mergedRef} />;
}
```

---

## 4. Ref Forwarding

```typescript
import { forwardRef, useRef, useImperativeHandle } from 'react';

// Basic ref forwarding to native element
const FancyInput = forwardRef<HTMLInputElement, { label: string }>(
  ({ label }, ref) => {
    return (
      <div>
        <label>{label}</label>
        <input ref={ref} />
      </div>
    );
  }
);

// Usage
function Parent() {
  const inputRef = useRef<HTMLInputElement>(null);
  return (
    <>
      <FancyInput ref={inputRef} label="Email" />
      <button onClick={() => inputRef.current?.focus()}>Focus</button>
    </>
  );
}

// Forwarding to custom imperative handle
interface TimerHandle {
  start: () => void;
  stop: () => void;
  reset: () => void;
  getTime: () => number;
}

const Stopwatch = forwardRef<TimerHandle, {}>((props, ref) => {
  const [time, setTime] = useState(0);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useImperativeHandle(ref, () => ({
    start: () => {
      if (!intervalRef.current) {
        intervalRef.current = setInterval(() => {
          setTime((t) => t + 1);
        }, 1000);
      }
    },
    stop: () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    },
    reset: () => {
      setTime(0);
    },
    getTime: () => time,
  }), [time]);

  return <div>{time}s</div>;
});

// Usage
function App() {
  const timerRef = useRef<TimerHandle>(null);

  return (
    <div>
      <Stopwatch ref={timerRef} />
      <button onClick={() => timerRef.current?.start()}>Start</button>
      <button onClick={() => timerRef.current?.stop()}>Stop</button>
      <button onClick={() => timerRef.current?.reset()}>Reset</button>
    </div>
  );
}
```

---

## 5. Controlled vs Uncontrolled with Types

```typescript
import { useState, useRef, forwardRef, useImperativeHandle } from 'react';

// Uncontrolled component — value managed by DOM
interface UncontrolledInputProps {
  defaultValue?: string;
  placeholder?: string;
  name: string;
}

const UncontrolledInput = forwardRef<HTMLInputElement, UncontrolledInputProps>(
  ({ defaultValue, placeholder, name }, ref) => {
    return (
      <input
        ref={ref}
        name={name}
        defaultValue={defaultValue}
        placeholder={placeholder}
      />
    );
  }
);

// Controlled component — value managed by React state
interface ControlledInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  name: string;
}

function ControlledInput({ value, onChange, placeholder, name }: ControlledInputProps) {
  return (
    <input
      name={name}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
    />
  );
}

// Hybrid: Controlled / Uncontrolled
interface InputProps {
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
  name: string;
  placeholder?: string;
}

function HybridInput({ value, defaultValue, onChange, name, placeholder }: InputProps) {
  const [internalValue, setInternalValue] = useState(defaultValue ?? '');

  // Determine if controlled
  const isControlled = value !== undefined;
  const currentValue = isControlled ? value : internalValue;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    if (!isControlled) {
      setInternalValue(newValue);
    }
    onChange?.(newValue);
  };

  return (
    <input
      name={name}
      value={currentValue}
      onChange={handleChange}
      placeholder={placeholder}
    />
  );
}
```

---

## 6. Best Practices

1. **Use `useRef<T>(null)`** for DOM refs — the type includes `| null`.
2. **Use `useRef<T>(initialValue)`** for mutable values — no `null` in type.
3. **Use optional chaining** when accessing `ref.current` for DOM refs.
4. **Prefer ref callbacks** for cleanup logic or measuring elements.
5. **Use `useImperativeHandle`** to expose only the API you need.
6. **Avoid reading/writing ref during rendering** — only in effects, callbacks, or imperative handlers.
7. **Use `forwardRef`** when a parent needs direct access to a child's DOM.
8. **Merge refs** when you need both internal and external ref access.

---

## Interview Questions

1. What is the type difference between `useRef<T>(null)` and `useRef<T>(initialValue)`?
2. When would you use a ref callback vs a ref object?
3. How do you merge multiple refs into one?
4. What is `useImperativeHandle` and when should you use it?
5. Explain the controlled vs uncontrolled component pattern with types.
6. How do you type a forwarded ref for a custom component?
7. What are the rules for when you can access `ref.current`?
8. How do you type a ref that stores a timer ID?
9. What is the "latest callback" pattern with refs?
10. How do you forward a ref and also use it internally?
