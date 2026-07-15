# Method Decorators in TypeScript

## Table of Contents

- [Overview](#overview)
- [Method Decorator Signature](#method-decorator-signature)
- [Modifying Method Behavior](#modifying-method-behavior)
- [Logging Decorators](#logging-decorators)
- [Caching Decorators](#caching-decorators)
- [Timing Decorators](#timing-decorators)
- [Method Decorator with Descriptor](#method-decorator-with-descriptor)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Method decorators are applied to method declarations within a class. They can intercept method calls, modify arguments, change return values, log execution, cache results, and more. They're the most commonly used decorator type.

---

## Method Decorator Signature

### Legacy Signature

```typescript
function MyDecorator(
  target: any,                // The prototype of the class
  propertyKey: string,        // The name of the method
  descriptor: PropertyDescriptor // The method's property descriptor
) {
  // target[propertyKey] is the original method
  // descriptor.value is the original method function
}
```

### Stage 3 Signature

```typescript
function MyDecorator(
  value: Function,            // The original method function
  context: ClassMethodDecoratorContext
  // context.kind === 'method'
  // context.name === propertyKey
  // context.static === boolean
  // context.access === { get(), has() }
) {
  // Return a new function to replace the original
}
```

### Basic Example

```typescript
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    console.log(`Method ${propertyKey} called with:`, args);
    const result = originalMethod.apply(this, args);
    console.log(`Method ${propertyKey} returned:`, result);
    return result;
  };
}

class MathService {
  @Log
  add(a: number, b: number): number {
    return a + b;
  }

  @Log
  multiply(a: number, b: number): number {
    return a * b;
  }
}

const math = new MathService();
math.add(2, 3);
// "Method add called with: [2, 3]"
// "Method add returned: 5"
```

---

## Modifying Method Behavior

### Changing Arguments

```typescript
function SanitizeInput(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    // Trim all string arguments
    const sanitizedArgs = args.map((arg) =>
      typeof arg === 'string' ? arg.trim() : arg
    );
    return originalMethod.apply(this, sanitizedArgs);
  };
}

class UserService {
  @SanitizeInput
  createUser(name: string, email: string) {
    return { name, email };
  }
}

const service = new UserService();
service.createUser('  Alice  ', '  alice@example.com  ');
// { name: 'Alice', email: 'alice@example.com' }
```

### Changing Return Value

```typescript
function ToLowerCase(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    const result = originalMethod.apply(this, args);
    if (typeof result === 'string') {
      return result.toLowerCase();
    }
    return result;
  };
}

class TextService {
  @ToLowerCase
  format(text: string): string {
    return text;
  }
}
```

### Conditional Execution

```typescript
function OnlyInDevelopment(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    if (process.env.NODE_ENV !== 'development') {
      console.warn(`${propertyKey} is only available in development`);
      return undefined;
    }
    return originalMethod.apply(this, args);
  };
}

class DebugService {
  @OnlyInDevelopment
  inspectObject(obj: any) {
    console.log(JSON.stringify(obj, null, 2));
  }
}
```

---

## Logging Decorators

### Comprehensive Method Logger

```typescript
function LogMethod(options: { level?: string } = {}) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const className = target.constructor.name;

    descriptor.value = function (...args: any[]) {
      const start = performance.now();
      console.log(
        `[${options.level ?? 'INFO'}] ${className}.${propertyKey} — called`
      );
      console.log(`  args:`, JSON.stringify(args));

      try {
        const result = originalMethod.apply(this, args);
        const duration = performance.now() - start;
        console.log(
          `[${options.level ?? 'INFO'}] ${className}.${propertyKey} — completed in ${duration.toFixed(2)}ms`
        );
        return result;
      } catch (error) {
        const duration = performance.now() - start;
        console.error(
          `[ERROR] ${className}.${propertyKey} — failed after ${duration.toFixed(2)}ms`,
          error
        );
        throw error;
      }
    };
  };
}

class UserService {
  @LogMethod({ level: 'DEBUG' })
  async findUser(id: string) {
    // Simulate database call
    return { id, name: 'Alice' };
  }

  @LogMethod({ level: 'INFO' })
  async createUser(data: any) {
    return { id: '1', ...data };
  }
}
```

### Async Method Logger

```typescript
function LogAsync(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = async function (...args: any[]) {
    const label = `${target.constructor.name}.${propertyKey}`;
    console.time(label);

    try {
      const result = await originalMethod.apply(this, args);
      console.timeEnd(label);
      return result;
    } catch (error) {
      console.timeEnd(label);
      console.error(`${label} threw:`, error);
      throw error;
    }
  };
}
```

---

## Caching Decorators

### Memoization Decorator

```typescript
function Memoize(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;
  const cache = new Map<string, any>();

  descriptor.value = function (...args: any[]) {
    const key = JSON.stringify(args);

    if (cache.has(key)) {
      console.log(`Cache hit for ${propertyKey}(${key})`);
      return cache.get(key);
    }

    const result = originalMethod.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

class Fibonacci {
  @Memoize
  calculate(n: number): number {
    if (n <= 1) return n;
    return this.calculate(n - 1) + this.calculate(n - 2);
  }
}

const fib = new Fibonacci();
fib.calculate(40); // Fast — cached results
```

### TTL Cache Decorator

```typescript
function TTLCache(ttlMs: number) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const cache = new Map<string, { value: any; expiry: number }>();

    descriptor.value = function (...args: any[]) {
      const key = JSON.stringify(args);
      const now = Date.now();
      const cached = cache.get(key);

      if (cached && cached.expiry > now) {
        return cached.value;
      }

      const result = originalMethod.apply(this, args);
      cache.set(key, { value: result, expiry: now + ttlMs });
      return result;
    };
  };
}

class ApiService {
  @TTLCache(60_000) // Cache for 60 seconds
  async fetchData(endpoint: string) {
    const response = await fetch(endpoint);
    return response.json();
  }
}
```

---

## Timing Decorators

### Performance Timer

```typescript
function Measure(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    const start = performance.now();
    const result = originalMethod.apply(this, args);
    const duration = performance.now() - start;

    console.log(`${propertyKey} took ${duration.toFixed(3)}ms`);

    // Attach timing info to result if it's an object
    if (typeof result === 'object' && result !== null) {
      (result as any).__timing = { method: propertyKey, duration };
    }

    return result;
  };
}

class SortService {
  @Measure
  bubbleSort(arr: number[]): number[] {
    const sorted = [...arr];
    for (let i = 0; i < sorted.length; i++) {
      for (let j = 0; j < sorted.length - i - 1; j++) {
        if (sorted[j] > sorted[j + 1]) {
          [sorted[j], sorted[j + 1]] = [sorted[j + 1], sorted[j]];
        }
      }
    }
    return sorted;
  }
}
```

### Retry Decorator

```typescript
function Retry(maxRetries: number = 3, delayMs: number = 1000) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      let lastError: Error | undefined;

      for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
          return await originalMethod.apply(this, args);
        } catch (error) {
          lastError = error as Error;
          console.warn(
            `${propertyKey} attempt ${attempt}/${maxRetries} failed: ${lastError.message}`
          );

          if (attempt < maxRetries) {
            await new Promise((resolve) => setTimeout(resolve, delayMs));
          }
        }
      }

      throw lastError;
    };
  };
}

class ExternalApiService {
  @Retry(3, 2000)
  async callExternalApi(url: string) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }
}
```

---

## Method Decorator with Descriptor

### Making Methods Non-Enumerable

```typescript
function NonEnumerable(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  descriptor.enumerable = false;
}

class User {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  @NonEnumerable
  internalId(): string {
    return 'internal-id';
  }
}

const user = new User('Alice');
Object.keys(user); // ['name'] — internalId is not enumerable
```

### Making Methods Read-Only

```typescript
function ReadOnly(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  descriptor.writable = false;
  descriptor.configurable = false;
}

class Config {
  @ReadOnly
  getVersion(): string {
    return '1.0.0';
  }
}

// Cannot override the method
Config.prototype.getVersion = () => '2.0.0'; // Error in strict mode
```

---

## Real-World Examples

### Debounce Decorator

```typescript
function Debounce(delayMs: number) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    let timeoutId: ReturnType<typeof setTimeout>;

    descriptor.value = function (...args: any[]) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        originalMethod.apply(this, args);
      }, delayMs);
    };
  };
}

class SearchService {
  @Debounce(300)
  search(query: string) {
    console.log(`Searching for: ${query}`);
  }
}
```

### Rate Limiter Decorator

```typescript
function RateLimit(maxCalls: number, windowMs: number) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const calls: number[] = [];

    descriptor.value = function (...args: any[]) {
      const now = Date.now();
      const windowStart = now - windowMs;

      // Remove calls outside the window
      while (calls.length > 0 && calls[0] <= windowStart) {
        calls.shift();
      }

      if (calls.length >= maxCalls) {
        throw new Error(
          `Rate limit exceeded for ${propertyKey}. Max ${maxCalls} calls per ${windowMs}ms`
        );
      }

      calls.push(now);
      return originalMethod.apply(this, args);
    };
  };
}

class ApiClient {
  @RateLimit(100, 60_000) // 100 calls per minute
  async fetchData(url: string) {
    return fetch(url).then((r) => r.json());
  }
}
```

---

## Best Practices

1. **Always save and call the original method** — unless you intentionally want to replace it.

2. **Use `apply(this, args)`** to preserve the correct `this` context.

3. **Handle async methods** — use `async/await` in the wrapper if the original might be async.

4. **Keep decorators pure when possible** — avoid side effects that make testing difficult.

5. **Use decorator factories** for configurable behavior (retry count, TTL, etc.).

6. **Return the correct type** — TypeScript infers the type from the original descriptor.

---

## Interview Questions

### Q1: What arguments does a method decorator receive?

**Answer**: Legacy: `(target, propertyKey, descriptor)` where target is the class prototype, propertyKey is the method name, and descriptor is the PropertyDescriptor. Stage 3: `(value, context)` where value is the method function and context is a ClassMethodDecoratorContext with kind, name, static, and access properties.

### Q2: How do you preserve `this` context in a method decorator?

**Answer**: Use `descriptor.value = function(...args) { return originalMethod.apply(this, args); }`. Arrow functions capture `this` lexically, so they won't work correctly. The `function` keyword creates its own `this`, and `.apply(this, args)` forwards the calling context.

### Q3: Can a method decorator change the method's return type?

**Answer**: Yes. The decorator replaces `descriptor.value`, so the new function can return a different type. TypeScript will infer the return type from the replacement function. However, this can cause type mismatches — use type assertions or generic constraints to handle this.
