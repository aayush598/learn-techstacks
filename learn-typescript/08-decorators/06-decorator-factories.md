# Decorator Factories in TypeScript

## Table of Contents

- [Overview](#overview)
- [What Are Decorator Factories](#what-are-decorator-factories)
- [Factory Pattern for Decorators](#factory-pattern-for-decorators)
- [Configurable Decorators](#configurable-decorators)
- [Decorator Composition](#decorator-composition)
- [Decorator Helper Libraries](#decorator-helper-libraries)
- [Real-World Factory Examples](#real-world-factory-examples)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Decorator factories are functions that return decorators. They allow you to configure decorator behavior before applying it. Instead of `@Decorator`, you use `@Decorator(options)` — the outer function is the factory, and it returns the actual decorator function.

---

## What Are Decorator Factories

### Bare Decorator (No Configuration)

```typescript
// This is a decorator — no configuration possible
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  console.log(`Method called: ${propertyKey}`);
}

class UserService {
  @Log  // Simple application — no options
  getUser() {}
}
```

### Decorator Factory (Configurable)

```typescript
// This is a factory — returns a decorator with configuration
function Log(level: string = 'info') {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = function (...args: any[]) {
      console.log(`[${level.toUpperCase()}] ${propertyKey} called`);
      return originalMethod.apply(this, args);
    };
  };
}

class UserService {
  @Log('debug')   // Factory called with 'debug', returns decorator
  getUser() {}

  @Log('error')   // Factory called with 'error', returns decorator
  deleteUser() {}
}
```

---

## Factory Pattern for Decorators

### Single Decorator Factory

```typescript
function Throttle(limitMs: number) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    let lastCall = 0;

    descriptor.value = function (...args: any[]) {
      const now = Date.now();
      if (now - lastCall < limitMs) {
        console.warn(`${propertyKey} throttled — wait ${limitMs}ms`);
        return;
      }
      lastCall = now;
      return originalMethod.apply(this, args);
    };
  };
}

class SearchService {
  @Throttle(300)
  search(query: string) {
    console.log(`Searching: ${query}`);
  }
}
```

### Multi-Option Factory

```typescript
interface LogOptions {
  level?: string;
  includeArgs?: boolean;
  includeResult?: boolean;
  prefix?: string;
}

function Log(options: LogOptions = {}) {
  const {
    level = 'info',
    includeArgs = true,
    includeResult = false,
    prefix = '',
  } = options;

  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const className = target.constructor.name;

    descriptor.value = function (...args: any[]) {
      const tag = prefix ? `${prefix}:` : '';
      console.log(
        `[${level.toUpperCase()}] ${tag}${className}.${propertyKey}`,
        includeArgs ? args : ''
      );

      const result = originalMethod.apply(this, args);

      if (includeResult) {
        console.log(
          `[${level.toUpperCase()}] ${tag}${className}.${propertyKey} result:`,
          result
        );
      }

      return result;
    };
  };
}

class ApiService {
  @Log({ level: 'debug', includeArgs: true, includeResult: true })
  fetchUsers(page: number) {
    return [{ id: 1, name: 'Alice' }];
  }

  @Log({ level: 'warn', prefix: 'API' })
  deprecatedMethod() {
    // ...
  }
}
```

### Class Decorator Factory

```typescript
function Component(name: string, version: string = '1.0.0') {
  return function <T extends new (...args: any[]) => any>(constructor: T) {
    return class extends constructor {
      static readonly componentName = name;
      static readonly componentVersion = version;

      getComponentInfo() {
        return `${name}@${version}`;
      }
    };
  };
}

@Component('UserService', '2.1.0')
class UserService {
  getUser() {}
}

const service = new UserService() as UserService & { getComponentInfo: () => string };
console.log(service.getComponentInfo()); // 'UserService@2.1.0'
```

---

## Configurable Decorators

### Class Configuration Factory

```typescript
interface ClassConfig {
  seal?: boolean;
  freeze?: boolean;
  timestamp?: boolean;
  singleton?: boolean;
}

function Configure(config: ClassConfig) {
  return function <T extends new (...args: any[]) => any>(constructor: T) {
    let instance: any;

    const modified = class extends constructor {
      constructor(...args: any[]) {
        super(...args);

        if (config.timestamp) {
          (this as any)._createdAt = new Date();
          (this as any)._updatedAt = new Date();
        }

        if (config.singleton) {
          if (instance) return instance;
          instance = this;
        }
      }
    };

    if (config.seal) {
      Object.seal(modified);
      Object.seal(modified.prototype);
    }

    if (config.freeze) {
      Object.freeze(modified);
      Object.freeze(modified.prototype);
    }

    return modified;
  };
}

@Configure({ timestamp: true, singleton: true })
class Database {
  query(sql: string) { return []; }
}

const db1 = new Database();
const db2 = new Database();
console.log(db1 === db2); // true (singleton)
```

### Method-Level Configuration

```typescript
interface CacheConfig {
  ttlMs?: number;
  maxSize?: number;
  keyPrefix?: string;
}

function Cached(config: CacheConfig = {}) {
  const { ttlMs = 60_000, maxSize = 100, keyPrefix = '' } = config;

  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const cache = new Map<string, { value: any; expiry: number }>();

    descriptor.value = function (...args: any[]) {
      const key = `${keyPrefix}${propertyKey}:${JSON.stringify(args)}`;
      const now = Date.now();
      const cached = cache.get(key);

      if (cached && cached.expiry > now) {
        return cached.value;
      }

      const result = originalMethod.apply(this, args);

      // Evict oldest if cache is full
      if (cache.size >= maxSize) {
        const oldest = cache.keys().next().value;
        cache.delete(oldest);
      }

      cache.set(key, { value: result, expiry: now + ttlMs });
      return result;
    };
  };
}

class ProductService {
  @Cached({ ttlMs: 30_000, maxSize: 50, keyPrefix: 'product:' })
  getProduct(id: string) {
    return { id, name: `Product ${id}` };
  }
}
```

---

## Decorator Composition

### Composing Multiple Decorators

```typescript
function Composed(...decorators: Function[]) {
  return function (
    target: any,
    propertyKey?: string,
    descriptor?: PropertyDescriptor
  ) {
    for (const decorator of decorators) {
      if (propertyKey && descriptor) {
        decorator(target, propertyKey, descriptor);
      } else if (propertyKey) {
        decorator(target, propertyKey);
      } else {
        decorator(target);
      }
    }
  };
}

// Create a "validated and logged" decorator
function ValidatedAndLogged(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  // Compose validation + logging in a specific order
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    // Validation first
    console.log('Validating...');
    // Then logging
    console.log(`Calling ${propertyKey}`);
    return originalMethod.apply(this, args);
  };
}
```

### Decorator Pipeline

```typescript
type MethodDecoratorFactory = (
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) => void;

function Pipeline(...factories: Array<(...args: any[]) => MethodDecoratorFactory>) {
  return function (decoratorArgs: Record<string, any>) {
    return function (
      target: any,
      propertyKey: string,
      descriptor: PropertyDescriptor
    ) {
      for (const factory of factories) {
        const decorator = factory(decoratorArgs);
        decorator(target, propertyKey, descriptor);
      }
    };
  };
}

// Usage:
// @Pipeline(LogFactory, CacheFactory, RetryFactory)({ level: 'debug', ttl: 60 })
```

---

## Decorator Helper Libraries

### reflect-metadata

```typescript
import 'reflect-metadata';

// Store and retrieve metadata in decorators
function Meta(key: string, value: any) {
  return function (target: any, propertyKey?: string) {
    Reflect.defineMetadata(key, value, target, propertyKey ?? 'constructor');
  };
}

function getMeta(target: any, key: string, propertyKey?: string) {
  return Reflect.getMetadata(key, target, propertyKey ?? 'constructor');
}

class UserService {
  @Meta('route', '/users')
  @Meta('method', 'GET')
  getUsers() {}
}

const route = getMeta(UserService.prototype, 'route', 'getUsers');
console.log(route); // '/users'
```

### Creating a Simple Decorator Utility Library

```typescript
// decorators/utils.ts
export function debounce(ms: number) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const original = descriptor.value;
    let timer: ReturnType<typeof setTimeout>;
    descriptor.value = function (...args: any[]) {
      clearTimeout(timer);
      timer = setTimeout(() => original.apply(this, args), ms);
    };
  };
}

export function memoize(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const original = descriptor.value;
  const cache = new Map();
  descriptor.value = function (...args: any[]) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = original.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

export function sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

// Re-export all decorators
export { debounce, memoize, sealed };
```

---

## Real-World Factory Examples

### Role-Based Access Control

```typescript
type Role = 'admin' | 'editor' | 'viewer';

function RequireRole(...roles: Role[]) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = function (...args: any[]) {
      const userRole: Role = (this as any).userRole;

      if (!roles.includes(userRole)) {
        throw new Error(
          `Access denied: requires one of [${roles.join(', ')}], has '${userRole}'`
        );
      }

      return originalMethod.apply(this, args);
    };
  };
}

class AdminController {
  @RequireRole('admin')
  deleteUser(id: string) { return { deleted: id }; }

  @RequireRole('admin', 'editor')
  editPost(id: string, data: any) { return { updated: id }; }

  @RequireRole('admin', 'editor', 'viewer')
  viewDashboard() { return { dash: 'data' }; }
}
```

### Rate Limiting by Method

```typescript
function RateLimit(maxCalls: number, windowMs: number) {
  const counters = new Map<string, number[]>();

  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = function (...args: any[]) {
      const key = `${target.constructor.name}.${propertyKey}`;
      const now = Date.now();
      const windowStart = now - windowMs;

      const calls = counters.get(key) || [];
      const validCalls = calls.filter((t) => t > windowStart);

      if (validCalls.length >= maxCalls) {
        throw new Error(`Rate limit exceeded for ${key}`);
      }

      validCalls.push(now);
      counters.set(key, validCalls);

      return originalMethod.apply(this, args);
    };
  };
}

class ApiClient {
  @RateLimit(10, 1_000) // 10 calls per second
  fetchData(url: string) {
    return fetch(url);
  }
}
```

---

## Best Practices

1. **Always use factories when you need options** — bare decorators should be for zero-config cases.

2. **Return the correct decorator type** from the factory — class, method, property, or parameter.

3. **Type your factory options** with interfaces for documentation and autocomplete.

4. **Provide sensible defaults** in factory options so they're usable with no arguments.

5. **Keep factories composable** — each factory should return a standard decorator.

6. **Document factory behavior** — decorators modify code implicitly.

---

## Interview Questions

### Q1: What is a decorator factory and why use it?

**Answer**: A decorator factory is a function that returns a decorator. It allows you to pass configuration options before the decorator is applied: `@Decorator(options)` vs `@Decorator`. The factory is called with your options and returns the actual decorator function that TypeScript applies to the target.

### Q2: How do you create a configurable logging decorator?

**Answer**: Create a factory that accepts options (level, includeArgs, prefix, etc.) and returns a method decorator. The returned decorator wraps the original method with logging logic that uses the captured options. The factory closes over the options, making them available to the decorator logic.

### Q3: Can you compose multiple decorators in a single factory?

**Answer**: Yes. A factory can internally call multiple decorator functions in sequence, or a decorator can be written to compose several concerns (validation + logging + caching). Libraries like `ts-middleware` provide decorator composition utilities. You can also write a `Pipeline` factory that chains multiple decorators.

### Q4: What is the difference between a decorator and a decorator factory?

**Answer**: A decorator is a function applied directly: `@Decorator`. A decorator factory is a function that returns a decorator: `@Decorator(options)`. The factory allows parameterization; the decorator itself is the final function that TypeScript calls with the target/key/descriptor.

### Q5: How does reflect-metadata work with decorator factories?

**Answer**: Inside the decorator (returned by the factory), you call `Reflect.defineMetadata(key, value, target, propertyKey)` to store the factory's configuration. Later, other code can retrieve this metadata with `Reflect.getMetadata()` to act on the decoration. This bridges compile-time decoration with runtime introspection.
