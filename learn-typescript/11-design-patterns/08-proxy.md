# Proxy Pattern in TypeScript

## Table of Contents

- [Proxy Pattern Overview](#proxy-pattern-overview)
- [Typed Proxy](#typed-proxy)
- [Proxy Object in JavaScript](#proxy-object-in-javascript)
- [Handler Traps](#handler-traps)
- [Validation Proxy](#validation-proxy)
- [Logging Proxy](#logging-proxy)
- [Caching Proxy](#caching-proxy)
- [Reactive Proxy (Vue 3)](#reactive-proxy-vue-3)
- [Proxy vs Decorator](#proxy-vs-decorator)
- [Interview Questions](#interview-questions)

---

## Proxy Pattern Overview

The Proxy pattern provides a surrogate or placeholder for another object to control access to it.

```typescript
// Basic proxy concept
interface Image {
  display(): void;
}

class RealImage implements Image {
  private filename: string;

  constructor(filename: string) {
    this.filename = filename;
    this.loadFromDisk();
  }

  private loadFromDisk(): void {
    console.log(`Loading ${this.filename} from disk...`);
  }

  display(): void {
    console.log(`Displaying ${this.filename}`);
  }
}

class ProxyImage implements Image {
  private realImage: RealImage | null = null;
  private filename: string;

  constructor(filename: string) {
    this.filename = filename;
  }

  display(): void {
    if (!this.realImage) {
      this.realImage = new RealImage(this.filename); // Lazy loading
    }
    this.realImage.display();
  }
}

// Usage
const image = new ProxyImage("photo.jpg");
// Image is NOT loaded yet
image.display(); // Loads and displays
image.display(); // Only displays (already loaded)
```

---

## Typed Proxy

```typescript
// Generic proxy with type safety
interface ProxiedObject<T> {
  get<K extends keyof T>(key: K): T[K];
  set<K extends keyof T>(key: K, value: T[K]): void;
  getAll(): Readonly<T>;
}

class ValidatingProxy<T> implements ProxiedObject<T> {
  private data: T;
  private validators: Partial<Record<keyof T, (value: any) => boolean>>;

  constructor(
    initial: T,
    validators: Partial<Record<keyof T, (value: any) => boolean>> = {}
  ) {
    this.data = { ...initial };
    this.validators = validators;
  }

  get<K extends keyof T>(key: K): T[K] {
    return this.data[key];
  }

  set<K extends keyof T>(key: K, value: T[K]): void {
    const validator = this.validators[key];
    if (validator && !validator(value)) {
      throw new Error(`Validation failed for key '${String(key)}'`);
    }
    this.data[key] = value;
  }

  getAll(): Readonly<T> {
    return Object.freeze({ ...this.data });
  }
}

// Usage
interface User {
  name: string;
  age: number;
  email: string;
}

const userProxy = new ValidatingProxy<User>(
  { name: "Alice", age: 30, email: "alice@example.com" },
  {
    name: (v) => typeof v === "string" && v.length > 0,
    age: (v) => typeof v === "number" && v > 0 && v < 150,
    email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
  }
);

userProxy.set("name", "Bob"); // ✅
// userProxy.set("age", -5); // ❌ Error: Validation failed
```

---

## Proxy Object in JavaScript

```typescript
// JavaScript Proxy API
interface Target {
  [key: string]: unknown;
}

const handler: ProxyHandler<Target> = {
  get(target, prop) {
    console.log(`Getting ${String(prop)}`);
    return Reflect.get(target, prop);
  },
  set(target, prop, value) {
    console.log(`Setting ${String(prop)} to ${value}`);
    return Reflect.set(target, prop, value);
  },
};

const proxy = new Proxy({ name: "Alice", age: 30 }, handler);

console.log(proxy.name); // Logs "Getting name", then "Alice"
proxy.age = 31;          // Logs "Setting age to 31"

// Revocable proxy
const { proxy: revocableProxy, revoke } = Proxy.revocable(
  { name: "Alice" },
  {
    get(target, prop) {
      return Reflect.get(target, prop);
    },
  }
);

console.log(revocableProxy.name); // "Alice"
revoke();
// console.log(revocableProxy.name); // TypeError: Cannot perform 'get' on a proxy that has been revoked
```

---

## Handler Traps

```typescript
// Complete list of traps
const comprehensiveHandler: ProxyHandler<object> = {
  // Property access
  get(target, prop, receiver) {
    console.log(`get ${String(prop)}`);
    return Reflect.get(target, prop, receiver);
  },

  // Property assignment
  set(target, prop, value, receiver) {
    console.log(`set ${String(prop)} = ${value}`);
    return Reflect.set(target, prop, value, receiver);
  },

  // Property existence check
  has(target, prop) {
    console.log(`has ${String(prop)}`);
    return Reflect.has(target, prop);
  },

  // Property deletion
  deleteProperty(target, prop) {
    console.log(`delete ${String(prop)}`);
    return Reflect.deleteProperty(target, prop);
  },

  // Property enumeration
  ownKeys(target) {
    console.log("ownKeys");
    return Reflect.ownKeys(target);
  },

  // Property descriptor
  getOwnPropertyDescriptor(target, prop) {
    console.log(`getOwnPropertyDescriptor ${String(prop)}`);
    return Reflect.getOwnPropertyDescriptor(target, prop);
  },

  // Object creation
  construct(target, args) {
    console.log(`construct with ${args}`);
    return Reflect.construct(target, args as any);
  },

  // Function call
  apply(target, thisArg, args) {
    console.log(`apply with ${args}`);
    return Reflect.apply(target as any, thisArg, args);
  },

  // Property definition
  defineProperty(target, prop, descriptor) {
    console.log(`defineProperty ${String(prop)}`);
    return Reflect.defineProperty(target, prop, descriptor);
  },

  // Prevent extensions
  preventExtensions(target) {
    console.log("preventExtensions");
    return Reflect.preventExtensions(target);
  },

  // Set prototype
  setPrototypeOf(target, prototype) {
    console.log("setPrototypeOf");
    return Reflect.setPrototypeOf(target, prototype);
  },

  // Get prototype
  getPrototypeOf(target) {
    console.log("getPrototypeOf");
    return Reflect.getPrototypeOf(target);
  },
};
```

---

## Validation Proxy

```typescript
// Type validation proxy
function createValidatedProxy<T extends object>(
  target: T,
  schema: Record<string, (value: unknown) => boolean>
): T {
  return new Proxy(target, {
    set(obj, prop, value) {
      const key = prop as string;
      if (key in schema && !schema[key](value)) {
        throw new TypeError(
          `Invalid value for ${key}: ${JSON.stringify(value)}`
        );
      }
      return Reflect.set(obj, prop, value);
    },
  });
}

// Usage
interface Config {
  port: number;
  host: string;
  debug: boolean;
}

const config = createValidatedProxy<Config>(
  { port: 3000, host: "localhost", debug: false },
  {
    port: (v) => typeof v === "number" && v > 0 && v < 65536,
    host: (v) => typeof v === "string" && v.length > 0,
    debug: (v) => typeof v === "boolean",
  }
);

config.port = 8080; // ✅
// config.port = -1; // ❌ TypeError
// config.port = "abc"; // ❌ TypeScript error (type checking)
// config.port = 99999; // ❌ Runtime TypeError

// Nested validation proxy
function createDeepProxy<T extends object>(
  target: T,
  schema: Record<string, any>
): T {
  return new Proxy(target, {
    set(obj, prop, value) {
      if (typeof value === "object" && value !== null && prop in schema) {
        value = createDeepProxy(value, schema[prop as string]);
      }
      return Reflect.set(obj, prop, value);
    },
    get(obj, prop) {
      const value = Reflect.get(obj, prop);
      if (typeof value === "object" && value !== null && prop in schema) {
        return createDeepProxy(value, schema[prop as string]);
      }
      return value;
    },
  });
}
```

---

## Logging Proxy

```typescript
// Comprehensive logging proxy
function createLoggingProxy<T extends object>(
  target: T,
  options: {
    logGets?: boolean;
    logSets?: boolean;
    logCalls?: boolean;
    logger?: (message: string) => void;
  } = {}
): T {
  const log = options.logger ?? console.log;

  return new Proxy(target, {
    get(obj, prop, receiver) {
      const value = Reflect.get(obj, prop, receiver);

      if (options.logGets && typeof prop === "string") {
        log(`[GET] ${String(prop)}`);
      }

      // Wrap methods
      if (typeof value === "function") {
        return function (this: any, ...args: any[]) {
          if (options.logCalls) {
            log(`[CALL] ${String(prop)}(${args.map(JSON.stringify).join(", ")})`);
          }
          const result = value.apply(this, args);
          if (result instanceof Promise) {
            return result.then((r) => {
              log(`[CALL RESULT] ${String(prop)} => ${JSON.stringify(r)}`);
              return r;
            });
          }
          log(`[CALL RESULT] ${String(prop)} => ${JSON.stringify(result)}`);
          return result;
        };
      }

      return value;
    },

    set(obj, prop, value) {
      if (options.logSets) {
        log(`[SET] ${String(prop)} = ${JSON.stringify(value)}`);
      }
      return Reflect.set(obj, prop, value);
    },
  });
}

// Usage
const user = createLoggingProxy(
  { name: "Alice", greet(name: string) { return `Hello, ${name}!`; } },
  { logGets: true, logSets: true, logCalls: true }
);

user.name; // [GET] name
user.name = "Bob"; // [SET] name = "Bob"
user.greet("Charlie"); // [CALL] greet("Charlie") => "Hello, Charlie!"
```

---

## Caching Proxy

```typescript
// Memoization proxy
function createCachingProxy<T extends object>(
  target: T,
  options: {
    ttl?: number;
    maxSize?: number;
  } = {}
): T {
  const cache = new Map<string, { value: unknown; expiry: number }>();
  const maxSize = options.maxSize ?? 100;
  const ttl = options.ttl ?? Infinity;

  return new Proxy(target, {
    get(obj, prop, receiver) {
      const value = Reflect.get(obj, prop, receiver);

      if (typeof value !== "function") return value;

      return function (this: any, ...args: any[]) {
        const key = `${String(prop)}:${JSON.stringify(args)}`;
        const now = Date.now();

        // Check cache
        const cached = cache.get(key);
        if (cached && now < cached.expiry) {
          return cached.value;
        }

        // Execute and cache
        const result = value.apply(this, args);

        if (result instanceof Promise) {
          return result.then((r) => {
            cache.set(key, { value: r, expiry: now + ttl });
            if (cache.size > maxSize) {
              const firstKey = cache.keys().next().value!;
              cache.delete(firstKey);
            }
            return r;
          });
        }

        cache.set(key, { value: result, expiry: now + ttl });
        if (cache.size > maxSize) {
          const firstKey = cache.keys().next().value!;
          cache.delete(firstKey);
        }
        return result;
      };
    },
  });
}

// Usage
const apiClient = createCachingProxy(
  {
    async getUser(id: string) {
      console.log(`Fetching user ${id}...`);
      return { id, name: "Alice" };
    },
  },
  { ttl: 60000, maxSize: 50 }
);

await apiClient.getUser("1"); // Fetches from API
await apiClient.getUser("1"); // Returns cached result
```

---

## Reactive Proxy (Vue 3)

```typescript
// Vue 3's reactivity system is built on Proxy
// Simplified version of Vue 3's reactive()

type Effect = () => void;
let currentEffect: Effect | null = null;

const targetMap = new WeakMap<object, Map<string | symbol, Set<Effect>>>();

function track(target: object, key: string | symbol): void {
  if (!currentEffect) return;

  let depsMap = targetMap.get(target);
  if (!depsMap) {
    depsMap = new Map();
    targetMap.set(target, depsMap);
  }

  let deps = depsMap.get(key);
  if (!deps) {
    deps = new Set();
    depsMap.set(key, deps);
  }

  deps.add(currentEffect);
}

function trigger(target: object, key: string | symbol): void {
  const depsMap = targetMap.get(target);
  if (!depsMap) return;

  const deps = depsMap.get(key);
  if (!deps) return;

  deps.forEach((effect) => effect());
}

function reactive<T extends object>(target: T): T {
  return new Proxy(target, {
    get(obj, key, receiver) {
      track(obj, key);
      const result = Reflect.get(obj, key, receiver);

      // Deep reactivity
      if (typeof result === "object" && result !== null) {
        return reactive(result);
      }

      return result;
    },
    set(obj, key, value, receiver) {
      const oldValue = Reflect.get(obj, key, receiver);
      const result = Reflect.set(obj, key, value, receiver);

      if (oldValue !== value) {
        trigger(obj, key);
      }

      return result;
    },
  });
}

function effect(fn: Effect): void {
  currentEffect = fn;
  fn();
  currentEffect = null;
}

// Usage
const state = reactive({ count: 0, user: { name: "Alice" } });

effect(() => {
  console.log(`Count: ${state.count}`);
});

state.count++; // Logs "Count: 1"

effect(() => {
  console.log(`Name: ${state.user.name}`);
});

state.user.name = "Bob"; // Logs "Name: Bob"
```

---

## Proxy vs Decorator

```typescript
// Proxy: Controls access, may modify behavior significantly
// Decorator: Adds behavior transparently

// Proxy: Can add access control, caching, lazy loading
class AccessProxy {
  constructor(
    private real: object,
    private allowedMethods: string[]
  ) {}

  get(target: object, prop: string) {
    if (!this.allowedMethods.includes(prop)) {
      throw new Error(`Access denied to ${prop}`);
    }
    return Reflect.get(target, prop);
  }
}

// Decorator: Adds logging, validation, etc.
class LoggingDecorator {
  constructor(private inner: object) {}

  get(target: object, prop: string) {
    console.log(`Accessing ${prop}`);
    return Reflect.get(target, prop);
  }
}

// Key differences:
// 1. Proxy can intercept operations completely (return different objects)
// 2. Decorator always delegates to wrapped object
// 3. Proxy can prevent operations (delete, set)
// 4. Decorator typically adds behavior around existing behavior
```

---

## Interview Questions

1. **What is the Proxy pattern?**
   A structural pattern that provides a surrogate or placeholder for another object to control access to it.

2. **What is the JavaScript Proxy object?**
   A built-in object that defines custom behavior for fundamental operations (get, set, delete, etc.).

3. **What are handler traps?**
   Methods that intercept fundamental object operations like get, set, has, deleteProperty, etc.

4. **What is the difference between Proxy and Decorator?**
   Proxy controls access and can prevent operations. Decorator adds behavior while maintaining the same interface.

5. **What is reactive programming with Proxy?**
   Vue 3 uses Proxy to track property access and trigger re-renders when data changes.

6. **What is a revocable proxy?**
   A proxy that can be disabled by calling a revoke function, making it unusable afterward.

7. **How do you implement a caching proxy?**
   Intercept method calls, check cache, return cached result or execute and cache the result.

8. **What are the performance implications of using Proxy?**
   Proxies add indirection which can slow down property access. They're not suitable for hot paths.

9. **Can Proxy intercept symbol properties?**
   Yes, the `get` and `set` traps receive Symbol keys.

10. **What are real-world uses of the Proxy pattern?**
    Vue 3 reactivity, logging, validation, access control, lazy loading, caching, and ORM lazy loading.
