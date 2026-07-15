# Observer Pattern in TypeScript

## Table of Contents

- [Observer Pattern Basics](#observer-pattern-basics)
- [Subject/Observer Interfaces](#subjectobserver-interfaces)
- [Typed Event Emitter](#typed-event-emitter)
- [Generic Event System](#generic-event-system)
- [Observer vs Pub/Sub](#observer-vs-pubsub)
- [RxJS Observers](#rxjs-observers)
- [Typed Callbacks](#typed-callbacks)
- [RemoveEventListener Patterns](#removeeventlistener-patterns)
- [Interview Questions](#interview-questions)

---

## Observer Pattern Basics

The Observer pattern defines a one-to-many dependency between objects. When one object changes state, all its dependents are notified.

```typescript
// Simple observer pattern
interface Observer<T> {
  update(data: T): void;
}

interface Subject<T> {
  subscribe(observer: Observer<T>): () => void;
  unsubscribe(observer: Observer<T>): void;
  notify(data: T): void;
}

class ConcreteSubject<T> implements Subject<T> {
  private observers = new Set<Observer<T>>();

  subscribe(observer: Observer<T>): () => void {
    this.observers.add(observer);
    return () => this.observers.delete(observer);
  }

  unsubscribe(observer: Observer<T>): void {
    this.observers.delete(observer);
  }

  notify(data: T): void {
    this.observers.forEach((observer) => observer.update(data));
  }
}

// Usage
class PriceDisplay implements Observer<number> {
  update(price: number): void {
    console.log(`Price updated: $${price}`);
  }
}

const priceTracker = new ConcreteSubject<number>();
const display1 = new PriceDisplay();
const display2 = new PriceDisplay();

priceTracker.subscribe(display1);
priceTracker.subscribe(display2);

priceTracker.notify(99.99); // Both observers notified
```

---

## Subject/Observer Interfaces

```typescript
// Flexible observer with typed events
interface TypedObserver<Events extends Record<string, unknown>> {
  on<K extends keyof Events>(event: K, handler: (data: Events[K]) => void): void;
  off<K extends keyof Events>(event: K, handler: (data: Events[K]) => void): void;
}

interface TypedSubject<Events extends Record<string, unknown>> {
  emit<K extends keyof Events>(event: K, data: Events[K]): void;
}

// Implementation
class EventEmitter<Events extends Record<string, unknown>>
  implements TypedObserver<Events>, TypedSubject<Events>
{
  private handlers = new Map<keyof Events, Set<(data: any) => void>>();

  on<K extends keyof Events>(event: K, handler: (data: Events[K]) => void): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);
    return () => this.handlers.get(event)?.delete(handler);
  }

  off<K extends keyof Events>(event: K, handler: (data: Events[K]) => void): void {
    this.handlers.get(event)?.delete(handler);
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.handlers.get(event)?.forEach((handler) => handler(data));
  }
}

// Usage with event map
interface AppEvents {
  "user:login": { userId: string; timestamp: number };
  "user:logout": { userId: string };
  "data:changed": { key: string; value: unknown };
}

const emitter = new EventEmitter<AppEvents>();

emitter.on("user:login", (data) => {
  console.log(`User ${data.userId} logged in at ${data.timestamp}`);
});

emitter.emit("user:login", { userId: "123", timestamp: Date.now() });
// ✅ Type-safe: TypeScript knows data has userId and timestamp
```

---

## Typed Event Emitter

```typescript
// Full typed event emitter
type EventHandler<T> = (data: T) => void;

class TypedEventEmitter<TEvents extends Record<string, unknown>> {
  private listeners = new Map<keyof TEvents, Set<EventHandler<any>>>();

  on<K extends keyof TEvents>(
    event: K,
    handler: EventHandler<TEvents[K]>
  ): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(handler);
    return () => this.off(event, handler);
  }

  off<K extends keyof TEvents>(event: K, handler: EventHandler<TEvents[K]>): void {
    this.listeners.get(event)?.delete(handler);
  }

  once<K extends keyof TEvents>(
    event: K,
    handler: EventHandler<TEvents[K]>
  ): () => void {
    const wrapper: EventHandler<TEvents[K]> = (data) => {
      handler(data);
      this.off(event, wrapper);
    };
    return this.on(event, wrapper);
  }

  emit<K extends keyof TEvents>(event: K, data: TEvents[K]): void {
    this.listeners.get(event)?.forEach((handler) => handler(data));
  }

  removeAllListeners(event?: keyof TEvents): void {
    if (event) {
      this.listeners.delete(event);
    } else {
      this.listeners.clear();
    }
  }

  listenerCount(event: keyof TEvents): number {
    return this.listeners.get(event)?.size ?? 0;
  }
}

// Usage
interface ChatEvents {
  message: { user: string; text: string; timestamp: number };
  join: { user: string };
  leave: { user: string };
  typing: { user: string };
}

const chat = new TypedEventEmitter<ChatEvents>();

chat.on("message", (data) => {
  console.log(`${data.user}: ${data.text}`);
});

chat.on("join", (data) => {
  console.log(`${data.user} joined`);
});

chat.emit("message", { user: "Alice", text: "Hello!", timestamp: Date.now() });
```

---

## Generic Event System

```typescript
// Hierarchical event system
class EventBus<TEvents extends Record<string, unknown>> {
  private static instance: EventBus<any>;
  private handlers = new Map<string, Set<(data: any) => void>>();

  static getInstance<T extends Record<string, unknown>>(): EventBus<T> {
    if (!EventBus.instance) {
      EventBus.instance = new EventBus<T>();
    }
    return EventBus.instance as EventBus<T>;
  }

  on<K extends keyof TEvents & string>(
    event: K,
    handler: (data: TEvents[K]) => void
  ): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);
    return () => this.handlers.get(event)?.delete(handler);
  }

  emit<K extends keyof TEvents & string>(event: K, data: TEvents[K]): void {
    this.handlers.get(event)?.forEach((handler) => handler(data));
  }

  // Wildcard support
  onAny(handler: (event: string, data: unknown) => void): () => void {
    const wrappedHandler = (event: string) => (data: unknown) =>
      handler(event, data);

    const unsubscribes = Array.from(this.handlers.keys()).map((event) => {
      this.handlers.get(event)!.add(wrappedHandler(event));
      return () => this.handlers.get(event)?.delete(wrappedHandler(event));
    });

    return () => unsubscribes.forEach((unsub) => unsub());
  }
}

// Namespace-based events
interface DomainEvents {
  "user.created": { id: string; name: string };
  "user.updated": { id: string; changes: Partial<User> };
  "order.placed": { orderId: string; items: string[] };
}

const bus = new EventBus<DomainEvents>();

bus.on("user.created", (data) => {
  console.log(`New user: ${data.name}`);
});
```

---

## Observer vs Pub/Sub

```typescript
// Observer: Subject directly notifies observers
// Pub/Sub: Publishers and subscribers are decoupled via a message broker

// Observer pattern
class StockPrice {
  private observers: Array<(price: number) => void> = [];

  subscribe(observer: (price: number) => void): () => void {
    this.observers.push(observer);
    return () => {
      this.observers = this.observers.filter((o) => o !== observer);
    };
  }

  updatePrice(price: number): void {
    this.observers.forEach((observer) => observer(price));
  }
}

// Pub/Sub pattern
class PubSub<TEvents extends Record<string, unknown>> {
  private topics = new Map<string, Set<(data: any) => void>>();

  publish<K extends keyof TEvents & string>(topic: K, data: TEvents[K]): void {
    this.topics.get(topic)?.forEach((handler) => handler(data));
  }

  subscribe<K extends keyof TEvents & string>(
    topic: K,
    handler: (data: TEvents[K]) => void
  ): () => void {
    if (!this.topics.has(topic)) {
      this.topics.set(topic, new Set());
    }
    this.topics.get(topic)!.add(handler);
    return () => this.topics.get(topic)?.delete(handler);
  }
}

// Usage
interface StockEvents {
  "AAPL.price": number;
  "GOOGL.price": number;
  "market.closing": void;
}

const market = new PubSub<StockEvents>();

// Publisher (stock exchange)
setInterval(() => {
  market.publish("AAPL.price", 150 + Math.random() * 10);
}, 1000);

// Subscriber (trading bot)
market.subscribe("AAPL.price", (price) => {
  if (price < 150) console.log("Buy signal!");
});
```

---

## RxJS Observers

```typescript
import { Subject, BehaviorSubject, Observable, Observer } from "rxjs";
import { filter, map, tap, switchMap } from "rxjs/operators";

// RxJS observer interface
interface RxObserver<T> {
  next(value: T): void;
  error(error: unknown): void;
  complete(): void;
}

// Using RxJS for complex event handling
class FormModel {
  private valueChanges = new BehaviorSubject<Record<string, unknown>>({});
  private submit$ = new Subject<void>();

  value$ = this.valueChanges.asObservable();

  valid$ = this.value$.pipe(
    map((values) => {
      return Object.keys(values).every(
        (key) => values[key] !== null && values[key] !== ""
      );
    })
  );

  submitHandler$ = this.submit$.pipe(
    switchMap(() => this.value$),
    filter(() => this.valid$.getValue()),
    tap((values) => console.log("Submitting:", values))
  );

  constructor() {
    this.submitHandler$.subscribe();
  }

  setValue(key: string, value: unknown): void {
    this.valueChanges.next({
      ...this.valueChanges.getValue(),
      [key]: value,
    });
  }

  submit(): void {
    this.submit$.next();
  }
}

// Usage
const form = new FormModel();
form.value$.subscribe((values) => console.log("Form values:", values));
form.valid$.subscribe((valid) => console.log("Is valid:", valid));

form.setValue("email", "test@example.com");
form.setValue("name", "Alice");
form.submit();
```

---

## Typed Callbacks

```typescript
// Callback type definitions
type Callback<T> = (data: T) => void;
type ErrorCallback = (error: Error) => void;
type SuccessCallback<T> = (data: T) => void;

// Event emitter with typed callbacks
class TypedEmitter<TEvents> {
  private callbacks = new Map<string, Set<Function>>();

  on<K extends keyof TEvents>(
    event: K,
    callback: (data: TEvents[K]) => void
  ): () => void {
    const key = event as string;
    if (!this.callbacks.has(key)) {
      this.callbacks.set(key, new Set());
    }
    this.callbacks.get(key)!.add(callback);
    return () => this.callbacks.get(key)?.delete(callback);
  }

  emit<K extends keyof TEvents>(event: K, data: TEvents[K]): void {
    const key = event as string;
    this.callbacks.get(key)?.forEach((cb) => (cb as (data: TEvents[K]) => void)(data));
  }
}

// Strongly typed API client callbacks
interface APIEvents {
  request: { url: string; method: string };
  response: { url: string; status: number; data: unknown };
  error: { url: string; error: Error };
}

const apiEmitter = new TypedEmitter<APIEvents>();

apiEmitter.on("response", (data) => {
  console.log(`Response from ${data.url}: ${data.status}`);
});
```

---

## RemoveEventListener Patterns

```typescript
// Browser event listener cleanup
class Component {
  private cleanupFns: Array<() => void> = [];

  mount(): void {
    // Add listener and store cleanup function
    const onResize = () => console.log("resized");
    window.addEventListener("resize", onResize);
    this.cleanupFns.push(() => window.removeEventListener("resize", onResize));

    const onClick = () => console.log("clicked");
    document.addEventListener("click", onClick);
    this.cleanupFns.push(() => document.removeEventListener("click", onClick));
  }

  unmount(): void {
    this.cleanupFns.forEach((fn) => fn());
    this.cleanupFns = [];
  }
}

// React-style cleanup
function useEffect cleanup pattern

// Using AbortController for cleanup
class EventManager {
  private controller = new AbortController();

  addEventListener<K extends keyof WindowEventMap>(
    type: K,
    handler: (this: Window, ev: WindowEventMap[K]) => any
  ): void {
    window.addEventListener(type, handler, {
      signal: this.controller.signal,
    });
  }

  destroy(): void {
    this.controller.abort(); // Removes all listeners
  }
}

// Usage
const manager = new EventManager();
manager.addEventListener("resize", () => console.log("resize"));
manager.addEventListener("click", () => console.log("click"));
manager.destroy(); // All listeners removed
```

---

## Interview Questions

1. **What is the Observer pattern?**
   A behavioral pattern where an object (subject) maintains a list of dependents (observers) and notifies them of state changes.

2. **What is the difference between Observer and Pub/Sub?**
   In Observer, the subject directly notifies observers. In Pub/Sub, publishers and subscribers are decoupled via a message broker/topic.

3. **How do you implement type-safe event emitters in TypeScript?**
   Use generic type parameters with a record type mapping event names to their data types.

4. **What are the memory leak concerns with the Observer pattern?**
   Forgetting to unsubscribe observers can cause memory leaks. Always provide cleanup functions.

5. **What is the difference between `on` and `once` in event emitters?**
   `on` registers a persistent listener. `once` registers a listener that auto-removes after the first invocation.

6. **How do you handle errors in event handlers?**
   Wrap handler calls in try/catch, or use error events to propagate errors.

7. **What is the advantage of using RxJS over custom event emitters?**
   RxJS provides powerful operators for transforming, combining, and filtering streams of events.

8. **How do you implement wildcard event handling?**
   Use pattern matching or a proxy that intercepts property access to listen to all events.

9. **What is the "removeEventListener" problem?**
   When adding event listeners, you need to keep a reference to the handler function to remove it later. Arrow functions in `addEventListener` make this difficult.

10. **How does the Observer pattern relate to React's state management?**
    React's setState, Redux's store.subscribe, and Context all use observer-like patterns for state updates.
