# Observables Pattern in TypeScript

## Table of Contents

- [Observable Concept](#observable-concept)
- [Simple Observable Implementation](#simple-observable-implementation)
- [Subscribe/Unsubscribe](#subscribeunsubscribe)
- [Subject](#subject)
- [BehaviorSubject](#behaviorsubject)
- [ReplaySubject](#replaysubject)
- [Comparison with Promises](#comparison-with-promises)
- [RxJS Introduction](#rxjs-introduction)
- [When to Use Observables](#when-to-use-observables)
- [Interview Questions](#interview-questions)

---

## Observable Concept

An Observable represents a stream of values that can be observed over time. Unlike promises which resolve once, observables can emit multiple values.

```typescript
// Conceptual difference:
// Promise: one value, one time
// Observable: zero to many values, over time

// Promise
const promise = new Promise<number>((resolve) => {
  resolve(42); // Single value
});

// Observable
const observable = new Observable<number>((subscriber) => {
  subscriber.next(1);  // Multiple values
  subscriber.next(2);
  subscriber.next(3);
  subscriber.complete();
});

// Real-world examples of observable-like patterns:
// - Mouse movements (many values over time)
// - WebSocket messages (continuous stream)
// - Database change streams (event-driven)
// - File system watchers (continuous monitoring)
```

---

## Simple Observable Implementation

```typescript
// Core types
interface Observer<T> {
  next: (value: T) => void;
  error: (error: unknown) => void;
  complete: () => void;
}

type TeardownFunction = () => void;

class SimpleObservable<T> {
  constructor(
    private subscriberFn: (observer: Observer<T>) => TeardownFunction | void
  ) {}

  subscribe(observer: Observer<T>): Subscription {
    let isUnsubscribed = false;
    let teardown: TeardownFunction | undefined;

    const wrappedObserver: Observer<T> = {
      next: (value: T) => {
        if (!isUnsubscribed) observer.next(value);
      },
      error: (error: unknown) => {
        if (!isUnsubscribed) {
          observer.error(error);
          isUnsubscribed = true;
        }
      },
      complete: () => {
        if (!isUnsubscribed) {
          observer.complete();
          isUnsubscribed = true;
        }
      },
    };

    try {
      teardown = this.subscriberFn(wrappedObserver) ?? undefined;
    } catch (error) {
      wrappedObserver.error(error);
    }

    return {
      unsubscribe: () => {
        if (!isUnsubscribed) {
          isUnsubscribed = true;
          teardown?.();
        }
      },
      closed: isUnsubscribed,
    };
  }

  pipe<R>(...operators: Array<(obs: SimpleObservable<T>) => SimpleObservable<any>>): SimpleObservable<any> {
    return operators.reduce((obs, operator) => operator(obs), this as SimpleObservable<any>);
  }
}

interface Subscription {
  unsubscribe: () => void;
  closed: boolean;
}

// Usage
const interval$ = new SimpleObservable<number>((observer) => {
  let count = 0;
  const id = setInterval(() => {
    observer.next(count++);
    if (count > 5) {
      observer.complete();
    }
  }, 1000);

  return () => clearInterval(id);
});

const subscription = interval$.subscribe({
  next: (value) => console.log(value),
  error: (err) => console.error(err),
  complete: () => console.log("done"),
});

// Unsubscribe later
setTimeout(() => subscription.unsubscribe(), 3000);
```

---

## Subscribe/Unsubscribe

```typescript
// Subscription management
class SubscriptionManager<T> {
  private subscriptions = new Map<string, Subscription>();

  add(key: string, observable: SimpleObservable<T>, observer: Observer<T>): void {
    // Unsubscribe existing subscription with same key
    this.subscriptions.get(key)?.unsubscribe();

    const subscription = observable.subscribe(observer);
    this.subscriptions.set(key, subscription);
  }

  remove(key: string): void {
    this.subscriptions.get(key)?.unsubscribe();
    this.subscriptions.delete(key);
  }

  removeAll(): void {
    for (const [key, sub] of this.subscriptions) {
      sub.unsubscribe();
    }
    this.subscriptions.clear();
  }
}

// Unsubscribing from multiple observables
function mergeUnsubscribable<T>(
  ...observables: Array<SimpleObservable<T>>
): { observable: SimpleObservable<T>; unsubscribeAll: () => void } {
  const subscriptions: Subscription[] = [];

  const merged = new SimpleObservable<T>((observer) => {
    observables.forEach((obs) => {
      subscriptions.push(obs.subscribe(observer));
    });

    return () => {
      subscriptions.forEach((sub) => sub.unsubscribe());
    };
  });

  return {
    observable: merged,
    unsubscribeAll: () => subscriptions.forEach((sub) => sub.unsubscribe()),
  };
}

// Cleanup patterns
class EventEmitter<T> {
  private listeners = new Map<string, Set<(value: T) => void>>();

  on(event: string, listener: (value: T) => void): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);

    // Return unsubscribe function
    return () => {
      this.listeners.get(event)?.delete(listener);
    };
  }

  emit(event: string, value: T): void {
    this.listeners.get(event)?.forEach((listener) => listener(value));
  }
}

// Usage with automatic cleanup
const emitter = new EventEmitter<string>();

// In React/Vue useEffect or component mount
const unsubscribe = emitter.on("data", (value) => {
  console.log(value);
});

// Cleanup on unmount
// return () => unsubscribe();
```

---

## Subject

A Subject is both an Observable and an Observer. It multicasts values to multiple subscribers.

```typescript
class Subject<T> implements Observer<T> {
  private observers = new Set<Observer<T>>();
  private isComplete = false;

  next(value: T): void {
    if (this.isComplete) return;
    this.observers.forEach((observer) => observer.next(value));
  }

  error(error: unknown): void {
    if (this.isComplete) return;
    this.observers.forEach((observer) => observer.error(error));
    this.isComplete = true;
  }

  complete(): void {
    if (this.isComplete) return;
    this.observers.forEach((observer) => observer.complete());
    this.isComplete = true;
  }

  subscribe(observer: Observer<T>): Subscription {
    this.observers.add(observer);

    return {
      unsubscribe: () => {
        this.observers.delete(observer);
      },
      closed: false,
    };
  }

  asObservable(): SimpleObservable<T> {
    return new SimpleObservable<T>((observer) => {
      const subscription = this.subscribe(observer);
      return () => subscription.unsubscribe();
    });
  }
}

// Usage
const subject = new Subject<number>();

const sub1 = subject.subscribe({
  next: (v) => console.log("Observer 1:", v),
  error: (e) => console.error(e),
  complete: () => console.log("Observer 1: complete"),
});

const sub2 = subject.subscribe({
  next: (v) => console.log("Observer 2:", v),
  error: (e) => console.error(e),
  complete: () => console.log("Observer 2: complete"),
});

subject.next(1); // Both observers receive 1
subject.next(2); // Both observers receive 2
subject.complete(); // Both observers get complete

// Practical: Event bus
class EventBus {
  private subjects = new Map<string, Subject<any>>();

  on<T>(event: string): SimpleObservable<T> {
    if (!this.subjects.has(event)) {
      this.subjects.set(event, new Subject<T>());
    }
    return this.subjects.get(event)!.asObservable();
  }

  emit<T>(event: string, value: T): void {
    this.subjects.get(event)?.next(value);
  }
}
```

---

## BehaviorSubject

A BehaviorSubject holds a current value and emits it to new subscribers.

```typescript
class BehaviorSubject<T> extends Subject<T> {
  constructor(private currentValue: T) {
    super();
  }

  get value(): T {
    return this.currentValue;
  }

  next(value: T): void {
    this.currentValue = value;
    super.next(value);
  }

  subscribe(observer: Partial<Observer<T>>): Subscription {
    // Emit current value immediately to new subscriber
    const wrappedObserver: Observer<T> = {
      next: (v) => observer.next?.(v),
      error: (e) => observer.error?.(e),
      complete: () => observer.complete?.(),
    };

    wrappedObserver.next(this.currentValue);

    return super.subscribe(wrappedObserver);
  }
}

// Usage: State management
interface AppState {
  user: User | null;
  theme: "light" | "dark";
  loading: boolean;
}

const state$ = new BehaviorSubject<AppState>({
  user: null,
  theme: "light",
  loading: false,
});

// Get current value synchronously
console.log(state$.value);

// Subscribe to changes
state$.subscribe((state) => {
  console.log("State changed:", state);
});

// Update state
state$.next({ ...state$.value, user: currentUser });
state$.next({ ...state$.value, theme: "dark" });

// Derived observable
function select<K>(selector: (state: AppState) => K): SimpleObservable<K> {
  return new SimpleObservable<K>((observer) => {
    let lastValue: K;

    const subscription = state$.subscribe({
      next: (state) => {
        const newValue = selector(state);
        if (newValue !== lastValue) {
          lastValue = newValue;
          observer.next(newValue);
        }
      },
      error: (e) => observer.error(e),
      complete: () => observer.complete(),
    });

    return () => subscription.unsubscribe();
  });
}

// Usage
select((s) => s.user).subscribe((user) => {
  console.log("User changed:", user);
});

select((s) => s.theme).subscribe((theme) => {
  document.body.className = theme;
});
```

---

## ReplaySubject

A ReplaySubject replays previous values to new subscribers.

```typescript
class ReplaySubject<T> extends Subject<T> {
  private buffer: T[] = [];
  private readonly bufferSize: number;

  constructor(bufferSize: number = Infinity) {
    super();
    this.bufferSize = bufferSize;
  }

  next(value: T): void {
    this.buffer.push(value);
    if (this.buffer.length > this.bufferSize) {
      this.buffer.shift();
    }
    super.next(value);
  }

  subscribe(observer: Partial<Observer<T>>): Subscription {
    // Replay buffered values to new subscriber
    const wrappedObserver: Observer<T> = {
      next: (v) => observer.next?.(v),
      error: (e) => observer.error?.(e),
      complete: () => observer.complete?.(),
    };

    for (const value of this.buffer) {
      wrappedObserver.next(value);
    }

    return super.subscribe(wrappedObserver);
  }
}

// Usage: Chat messages
const messages$ = new ReplaySubject<{ user: string; text: string }>(50);

// New subscribers get last 50 messages
messages$.subscribe((msg) => {
  console.log(`${msg.user}: ${msg.text}`);
});

// Emitting messages
messages$.next({ user: "Alice", text: "Hello!" });
messages$.next({ user: "Bob", text: "Hi!" });
```

---

## Comparison with Promises

```typescript
// Feature comparison

// Promise: single value
const promise = Promise.resolve(42);
promise.then((v) => console.log(v)); // 42

// Observable: multiple values
const observable = new SimpleObservable<number>((subscriber) => {
  subscriber.next(1);
  subscriber.next(2);
  subscriber.next(3);
  subscriber.complete();
});
observable.subscribe({ next: (v) => console.log(v) }); // 1, 2, 3

// Promise: eager execution
const eagerPromise = new SimpleObservable<number>((subscriber) => {
  console.log("This runs immediately!");
  subscriber.next(42);
}); // "This runs immediately!" logged

// Observable: lazy execution (unless using BehaviorSubject)
const lazyObservable = new SimpleObservable<number>((subscriber) => {
  console.log("This runs when subscribed!");
  subscriber.next(42);
}); // Nothing logged yet
lazyObservable.subscribe({ next: (v) => console.log(v) }); // Now "This runs when subscribed!" logged

// Promise: cannot cancel
const longPromise = fetch("https://api.example.com"); // Cannot cancel

// Observable: can unsubscribe
const longObservable = new SimpleObservable<number>((subscriber) => {
  const interval = setInterval(() => subscriber.next(Date.now()), 1000);
  return () => clearInterval(interval); // Cleanup on unsubscribe
});
const sub = longObservable.subscribe({ next: (v) => console.log(v) });
sub.unsubscribe(); // Stops the interval

// Promise: single error handler
fetch("bad-url")
  .then((r) => r.json())
  .catch((err) => console.log(err)); // Single catch

// Observable: multiple error opportunities
const errorObservable = new SimpleObservable<number>((subscriber) => {
  try {
    subscriber.next(1);
    throw new Error("Error during emission");
  } catch (e) {
    subscriber.error(e);
  }
});
```

---

## RxJS Introduction

RxJS is the most popular Observable library for TypeScript.

```typescript
import { Observable, Subject, BehaviorSubject, ReplaySubject } from "rxjs";
import { map, filter, debounceTime, switchMap, takeUntil } from "rxjs/operators";

// Creating observables
const interval$ = new Observable<number>((subscriber) => {
  let count = 0;
  const id = setInterval(() => {
    subscriber.next(count++);
    if (count > 5) subscriber.complete();
  }, 1000);
  return () => clearInterval(id);
});

// Operators
const processed$ = interval$.pipe(
  filter((n) => n % 2 === 0),    // Only even numbers
  map((n) => n * 10),            // Multiply by 10
  debounceTime(300),             // Wait 300ms after last emission
);

// Subscription
const subscription = processed$.subscribe({
  next: (v) => console.log(v),
  error: (e) => console.error(e),
  complete: () => console.log("done"),
});

// Cleanup
subscription.unsubscribe();

// Subject
const searchSubject = new Subject<string>();

const results$ = searchSubject.pipe(
  debounceTime(300),
  switchMap(async (query) => {
    const response = await fetch(`/api/search?q=${query}`);
    return response.json();
  })
);

results$.subscribe((results) => {
  console.log("Search results:", results);
});

searchSubject.next("typescript"); // Debounced search
```

---

## When to Use Observables

```typescript
// Use Observables when:
// 1. You need multiple values over time
// 2. You need cancellation
// 3. You need complex transformation chains
// 4. You're working with real-time data

// Use Promises when:
// 1. You need a single value
// 2. You're doing simple async operations
// 3. You're working with APIs that return promises
// 4. You need broader browser/runtime support

// Hybrid approach
function fetchWithObservable(url: string): Observable<Response> {
  return new Observable((subscriber) => {
    const controller = new AbortController();

    fetch(url, { signal: controller.signal })
      .then((response) => {
        subscriber.next(response);
        subscriber.complete();
      })
      .catch((error) => {
        if (!subscriber.closed) {
          subscriber.error(error);
        }
      });

    return () => controller.abort();
  });
}

// Converting promises to observables
function fromPromise<T>(promise: Promise<T>): Observable<T> {
  return new Observable((subscriber) => {
    promise
      .then((value) => {
        subscriber.next(value);
        subscriber.complete();
      })
      .catch((error) => {
        subscriber.error(error);
      });
  });
}

// Converting observables to promises
function toPromise<T>(observable: Observable<T>): Promise<T> {
  return new Promise((resolve, reject) => {
    let lastValue: T;
    observable.subscribe({
      next: (v) => { lastValue = v; },
      error: reject,
      complete: () => resolve(lastValue),
    });
  });
}
```

---

## Interview Questions

1. **What is an Observable?**
   A representation of a stream of values that can be observed over time, supporting multiple emissions, error handling, and cleanup.

2. **What is the difference between Observable and Promise?**
   Observables can emit multiple values, support cancellation, are lazy (don't execute until subscribed), and support complex transformation operators.

3. **What is a Subject in RxJS?**
   Both an Observable and an Observer. It multicasts values to multiple subscribers.

4. **What is a BehaviorSubject?**
   A Subject that holds a current value and emits it immediately to new subscribers. Useful for state management.

5. **What is a ReplaySubject?**
   A Subject that replays a specified number of previous values to new subscribers.

6. **When would you use a Subject over a BehaviorSubject?**
   When you don't need to provide an initial value or the current state to new subscribers.

7. **How do you handle unsubscription/cleanup?**
   Return a cleanup function from the subscribe callback, or use the `takeUntil` operator with a destroy subject.

8. **What are RxJS operators?**
   Functions that transform, filter, or combine observables. They take an observable and return a new observable.

9. **What is the `pipe` method?**
   Chains multiple operators together to transform the observable stream.

10. **When should you NOT use Observables?**
    For simple request-response patterns, when you only need a single value, or when working with APIs that natively return promises.

11. **What is hot vs cold observables?**
    Cold observables create a new execution for each subscriber. Hot observables share execution and are independent of subscribers.

12. **How do you convert between Observables and Promises?**
    Use `toPromise()` (Observable to Promise) and `from()` or `new Observable()` (Promise to Observable).

13. **What is multicasting?**
    Sharing a single subscription among multiple subscribers. Subjects and operators like `shareReplay` enable multicasting.

14. **What is backpressure in observables?**
    When a producer emits faster than a consumer can process. Use operators like `buffer`, `throttle`, or `debounceTime` to manage it.

15. **How do observables handle errors?**
    The `error` callback stops the stream. Use `catchError` operator to handle and potentially recover from errors.
