# Design Patterns in TypeScript - Interview Questions

## Table of Contents

- [Creational Patterns](#creational-patterns)
- [Structural Patterns](#structural-patterns)
- [Behavioral Patterns](#behavioral-patterns)
- [TypeScript-Specific Patterns](#typescript-specific-patterns)
- [Code Challenges](#code-challenges)
- [System Design](#system-design)

---

## Creational Patterns

### Q1: What is the Singleton pattern and what problems does it create?

**Answer:** Singleton ensures a class has only one instance. Problems include: hidden dependencies, tight coupling, difficulty testing (can't mock), global state, and lifecycle management. In TypeScript/JavaScript, modules are often better singletons.

```typescript
// ❌ Problematic singleton
class Database {
  private static instance: Database;
  private constructor() {}
  static getInstance() {
    if (!Database.instance) Database.instance = new Database();
    return Database.instance;
  }
}

// ✅ Better: Module or DI
export const db = new Database();
```

### Q2: When would you use a Factory over a Constructor?

**Answer:** When object creation is complex, when you need to return different types based on input, when you want to encapsulate creation logic, or when the class has many constructor overloads.

### Q3: What is the Abstract Factory pattern?

**Answer:** Provides an interface for creating families of related objects without specifying their concrete classes. Useful for theming (Material UI vs Bootstrap), cross-platform UI, or multiple database support.

### Q4: What is the Builder pattern's advantage over telescoping constructors?

**Answer:** Builder provides readable step-by-step construction, optional parameters without overloads, validation before building, and immutable configuration. Telescoping constructors become unreadable with many optional parameters.

```typescript
// ❌ Telescoping constructor
new User("Alice", "alice@example.com", true, true, false, null, undefined, "admin");

// ✅ Builder
new UserBuilder()
  .name("Alice")
  .email("alice@example.com")
  .verified(true)
  .role("admin")
  .build();
```

### Q5: What is the Prototype pattern in TypeScript?

**Answer:** Creating new objects by cloning existing instances. JavaScript's prototype chain is the foundation. Use `Object.create()`, spread operator, or structuredClone for deep cloning.

---

## Structural Patterns

### Q6: What is the Adapter pattern?

**Answer:** Allows incompatible interfaces to work together. Wraps one interface with another. Examples: database driver adapters, payment gateway adapters, API client adapters.

### Q7: What is the difference between Adapter and Decorator?

**Answer:** Adapter changes the interface. Decorator adds behavior while maintaining the same interface. Adapter is for compatibility, Decorator is for enhancement.

### Q8: What is the Proxy pattern?

**Answer:** Provides a surrogate for another object to control access. Can add caching, logging, validation, lazy loading, or access control. JavaScript's `Proxy` object enables this natively.

### Q9: What is the Facade pattern?

**Answer:** Provides a simplified interface to a complex subsystem. Hides complexity behind a simple API. Examples: jQuery is a facade over DOM APIs, ORMs are facades over SQL.

### Q10: What is the difference between Facade and Adapter?

**Answer:** Facade simplifies a complex interface. Adapter makes two incompatible interfaces work together. Facade hides complexity; Adapter bridges differences.

### Q11: What is the Composite pattern?

**Answer:** Composes objects into tree structures and treats individual objects and compositions uniformly. Examples: DOM tree, file system, UI component trees.

### Q12: What is the Bridge pattern?

**Answer:** Separates abstraction from implementation so both can vary independently. Useful when you have multiple dimensions of variation (e.g., shape × color).

---

## Behavioral Patterns

### Q13: What is the Observer pattern?

**Answer:** Defines a one-to-many dependency where when one object changes state, all dependents are notified. Examples: DOM events, RxJS, custom event emitters, pub/sub systems.

### Q14: What is the difference between Observer and Pub/Sub?

**Answer:** Observer: subject directly notifies observers. Pub/Sub: publishers and subscribers are decoupled via a message broker. Pub/Sub is more loosely coupled.

### Q15: What is the Strategy pattern?

**Answer:** Defines a family of algorithms, encapsulates each, and makes them interchangeable. Examples: sorting algorithms, payment methods, compression algorithms.

### Q16: What is the difference between Strategy and State patterns?

**Answer:** Strategy changes algorithm used (external selection). State changes behavior based on internal state (internal transitions). Strategy is selected by client; State transitions automatically.

### Q17: What is the Command pattern?

**Answer:** Encapsulates a request as an object. Enables undo/redo, command queuing, macro recording, and decoupling invocation from execution.

### Q18: What is the Chain of Responsibility pattern?

**Answer:** Passes requests along a chain of handlers until one handles it. Examples: middleware, event bubbling, logging pipelines.

### Q19: What is the Template Method pattern?

**Answer:** Defines the skeleton of an algorithm in a base class, letting subclasses override specific steps. Uses abstract methods and hook methods.

### Q20: What is the Iterator pattern?

**Answer:** Provides a way to access elements of a collection sequentially without exposing its underlying representation. JavaScript's iterator protocol is a built-in implementation.

---

## TypeScript-Specific Patterns

### Q21: What is the Result/Either pattern?

**Answer:** A functional error handling pattern using discriminated unions instead of exceptions.

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return { ok: false, error: "Division by zero" };
  return { ok: true, value: a / b };
}
```

### Q22: What are phantom types?

**Answer:** Type parameters that don't affect runtime behavior but provide compile-time type safety. Used to distinguish between values with the same runtime representation.

```typescript
type Validated = { readonly _brand: unique symbol };
type Unvalidated = { readonly _brand: unique symbol };

function validate(data: string): Result<Validated, string> {
  return data.length > 0
    ? { ok: true, value: data as any }
    : { ok: false, error: "Empty" };
}

function process(data: Validated): void { /* ... */ }

// process("raw"); // ❌ Error: string is not Validated
// process(validate("test").value); // ❌ Error: might be error case
```

### Q23: What is the Builder with Type-State pattern?

**Answer:** Uses TypeScript's type system to enforce build steps at compile time.

```typescript
class RequestBuilder {
  private hasUrl = false;

  url(u: string): this & { hasUrl: true } {
    this.hasUrl = true;
    return this as any;
  }

  build(this: this & { hasUrl: true }): Request {
    return {} as Request;
  }
}

new RequestBuilder().url("http://example.com").build(); // ✅
// new RequestBuilder().build(); // ❌ Error: hasUrl is missing
```

### Q24: What is the Typed Builder pattern?

**Answer:** Uses generics and conditional types to ensure required fields are set before building.

### Q25: How do you implement a type-safe event emitter?

**Answer:** Use generic type parameters mapping event names to their data types.

```typescript
class EventEmitter<Events extends Record<string, unknown>> {
  on<K extends keyof Events>(event: K, handler: (data: Events[K]) => void): () => void { /* ... */ }
  emit<K extends keyof Events>(event: K, data: Events[K]): void { /* ... */ }
}
```

---

## Code Challenges

### Q26: Implement a memoization decorator

```typescript
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map<string, ReturnType<T>>();

  return ((...args: Parameters<T>): ReturnType<T> => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key)!;
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

const expensive = memoize((n: number) => {
  console.log("Computing...");
  return n * n;
});
```

### Q27: Implement a typed middleware system

```typescript
type Middleware<T> = (context: T, next: () => Promise<void>) => Promise<void>;

class Pipeline<T> {
  private middlewares: Middleware<T>[] = [];

  use(...fns: Middleware<T>[]): this {
    this.middlewares.push(...fns);
    return this;
  }

  async execute(context: T): Promise<void> {
    let index = 0;
    const next = async (): Promise<void> => {
      if (index < this.middlewares.length) {
        await this.middlewares[index++](context, next);
      }
    };
    await next();
  }
}
```

### Q28: Implement a state machine

```typescript
type StateConfig = Record<string, Record<string, string>>;

class StateMachine<T extends StateConfig> {
  private state: keyof T;
  private transitions: T;

  constructor(transitions: T, initial: keyof T) {
    this.transitions = transitions;
    this.state = initial;
  }

  send(event: string): keyof T {
    const transition = this.transitions[this.state][event];
    if (!transition) throw new Error(`Invalid event ${event} in state ${this.state}`);
    this.state = transition as keyof T;
    return this.state;
  }

  getState(): keyof T {
    return this.state;
  }
}

// Usage
const light = new StateMachine({
  green: { next: "yellow" },
  yellow: { next: "red" },
  red: { next: "green" },
}, "green");

light.send("next"); // yellow
light.send("next"); // red
```

### Q29: What is the difference between Composition and Inheritance?

**Answer:** Composition creates objects that contain other objects (has-a). Inheritance creates specialized versions of existing classes (is-a). Prefer composition over inheritance for flexibility.

```typescript
// ❌ Inheritance
class SwimmingDog extends Dog { /* ... */ }

// ✅ Composition
class Dog {
  constructor(private swimmer: Swimmer) {}
  swim() { this.swimmer.swim(); }
}
```

### Q30: How do you implement dependency injection in TypeScript?

**Answer:** Use constructor injection, a DI container, or framework-specific DI (NestJS, InversifyJS).

```typescript
// Constructor injection
class UserService {
  constructor(private db: Database, private logger: Logger) {}
}

// DI Container
class Container {
  private services = new Map<string, () => any>();
  register<T>(name: string, factory: () => T): void { this.services.set(name, factory); }
  resolve<T>(name: string): T { return this.services.get(name)!() as T; }
}
```

---

## System Design

### Q31: How would you design a plugin architecture?

**Answer:** Define plugin interfaces, use a registry pattern, support lifecycle hooks, and enable dynamic loading.

```typescript
interface Plugin {
  name: string;
  version: string;
  initialize(app: App): Promise<void>;
  destroy(): Promise<void>;
}

class PluginRegistry {
  private plugins = new Map<string, Plugin>();

  register(plugin: Plugin): void {
    this.plugins.set(plugin.name, plugin);
  }

  async initializeAll(app: App): Promise<void> {
    for (const plugin of this.plugins.values()) {
      await plugin.initialize(app);
    }
  }
}
```

### Q32: How would you design a type-safe API client?

**Answer:** Use generics for request/response types, discriminated unions for errors, and branded types for IDs.

```typescript
interface APIResponse<T> {
  data: T;
  status: number;
}

interface APIError {
  code: string;
  message: string;
}

type Result<T> = { ok: true; data: T } | { ok: false; error: APIError };

class TypedAPIClient {
  async get<T>(url: string): Promise<Result<T>> {
    try {
      const response = await fetch(url);
      const data = await response.json() as T;
      return { ok: true, data };
    } catch (error) {
      return { ok: false, error: { code: "NETWORK_ERROR", message: String(error) } };
    }
  }
}
```

### Q33: What design patterns are used in React?

**Answer:**
- **Component Pattern**: Composite pattern
- **Hooks**: Observer pattern (useState, useEffect)
- **Context**: Observer/mediator pattern
- **Higher-Order Components**: Decorator pattern
- **Render Props**: Strategy pattern
- **Compound Components**: Composite pattern

### Q34: What design patterns are used in Redux?

**Answer:**
- **Store**: Singleton pattern
- **Reducers**: Strategy pattern
- **Middleware**: Chain of Responsibility pattern
- **Actions**: Command pattern
- **Selectors**: Decorator/Adapter pattern

### Q35: How would you implement a connection pool?

**Answer:** Use the Object Pool pattern with a factory for creating connections and a manager for tracking available/in-use connections.

```typescript
class ConnectionPool<T> {
  private available: T[] = [];
  private inUse = new Set<T>();

  constructor(
    private factory: () => T,
    private destroy: (conn: T) => void,
    private maxSize: number
  ) {}

  async acquire(): Promise<T> {
    if (this.available.length > 0) {
      const conn = this.available.pop()!;
      this.inUse.add(conn);
      return conn;
    }
    if (this.inUse.size < this.maxSize) {
      const conn = this.factory();
      this.inUse.add(conn);
      return conn;
    }
    // Wait for a connection to be released
    return new Promise((resolve) => {
      const check = setInterval(() => {
        if (this.available.length > 0) {
          clearInterval(check);
          resolve(this.acquire());
        }
      }, 100);
    });
  }

  release(conn: T): void {
    this.inUse.delete(conn);
    this.available.push(conn);
  }

  destroy(): void {
    [...this.available, ...this.inUse].forEach(this.destroy);
    this.available = [];
    this.inUse.clear();
  }
}
```
