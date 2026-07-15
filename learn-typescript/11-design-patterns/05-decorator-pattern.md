# Decorator Pattern in TypeScript

## Table of Contents

- [Decorator Pattern Overview](#decorator-pattern-overview)
- [Interface-Based Decorators](#interface-based-decorators)
- [Stacking Decorators](#stacking-decorators)
- [Decorator vs Inheritance](#decorator-vs-inheritance)
- [Real-World Examples](#real-world-examples)
- [TypeScript Decorators vs GoF Decorator](#typescript-decorators-vs-gof-decorator)
- [Interview Questions](#interview-questions)

---

## Decorator Pattern Overview

The Decorator pattern attaches additional responsibilities to an object dynamically, providing a flexible alternative to subclassing.

```typescript
// Core concept: wrap an object to add behavior
interface Coffee {
  cost(): number;
  description(): string;
}

class SimpleCoffee implements Coffee {
  cost(): number { return 1.99; }
  description(): string { return "Simple coffee"; }
}

// Decorator base class
abstract class CoffeeDecorator implements Coffee {
  constructor(protected coffee: Coffee) {}

  abstract cost(): number;
  abstract description(): string;
}

// Concrete decorators
class MilkDecorator extends CoffeeDecorator {
  cost(): number { return this.coffee.cost() + 0.50; }
  description(): string { return `${this.coffee.description()}, milk`; }
}

class SugarDecorator extends CoffeeDecorator {
  cost(): number { return this.coffee.cost() + 0.25; }
  description(): string { return `${this.coffee.description()}, sugar`; }
}

// Usage
let coffee: Coffee = new SimpleCoffee();
coffee = new MilkDecorator(coffee);
coffee = new SugarDecorator(coffee);

console.log(coffee.description()); // "Simple coffee, milk, sugar"
console.log(coffee.cost()); // 2.74
```

---

## Interface-Based Decorators

```typescript
// Generic decorator interface
interface Decorator<T> {
  decorate(target: T): T;
}

// Logger decorator
interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string): void {
    console.log(`[LOG] ${message}`);
  }
}

class LoggerDecorator implements Decorator<Logger> {
  constructor(private prefix: string) {}

  decorate(logger: Logger): Logger {
    const originalLog = logger.log.bind(logger);
    return {
      log: (message: string) => {
        originalLog(`${this.prefix}: ${message}`);
      },
    };
  }
}

// HTTP client decorator
interface HttpClient {
  fetch(url: string, options?: RequestInit): Promise<Response>;
}

class BaseHttpClient implements HttpClient {
  async fetch(url: string, options?: RequestInit): Promise<Response> {
    return globalThis.fetch(url, options);
  }
}

class LoggingHttpClient implements HttpClient {
  constructor(private inner: HttpClient) {}

  async fetch(url: string, options?: RequestInit): Promise<Response> {
    console.log(`[HTTP] ${options?.method ?? "GET"} ${url}`);
    const start = Date.now();
    const response = await this.inner.fetch(url, options);
    console.log(`[HTTP] ${response.status} (${Date.now() - start}ms)`);
    return response;
  }
}

class AuthHttpClient implements HttpClient {
  constructor(
    private inner: HttpClient,
    private getToken: () => string
  ) {}

  async fetch(url: string, options?: RequestInit): Promise<Response> {
    return this.inner.fetch(url, {
      ...options,
      headers: {
        ...options?.headers,
        Authorization: `Bearer ${this.getToken()}`,
      },
    });
  }
}

class RetryHttpClient implements HttpClient {
  constructor(
    private inner: HttpClient,
    private maxRetries: number = 3
  ) {}

  async fetch(url: string, options?: RequestInit): Promise<Response> {
    let lastError: Error | undefined;
    for (let i = 0; i <= this.maxRetries; i++) {
      try {
        return await this.inner.fetch(url, options);
      } catch (error) {
        lastError = error as Error;
        if (i < this.maxRetries) {
          await new Promise((r) => setTimeout(r, 1000 * (i + 1)));
        }
      }
    }
    throw lastError;
  }
}

// Compose decorators
const client = new RetryHttpClient(
  new AuthHttpClient(
    new LoggingHttpClient(
      new BaseHttpClient()
    ),
    () => "my-token"
  ),
  3
);

await client.fetch("https://api.example.com/data");
```

---

## Stacking Decorators

```typescript
// Stream decorator pattern
interface ReadStream {
  read(): string;
}

class FileStream implements ReadStream {
  constructor(private path: string) {}
  read(): string {
    return `Contents of ${this.path}`;
  }
}

class DecoratedStream implements ReadStream {
  constructor(protected inner: ReadStream) {}
  read(): string { return this.inner.read(); }
}

class UpperCaseStream extends DecoratedStream {
  read(): string {
    return super.read().toUpperCase();
  }
}

class TrimStream extends DecoratedStream {
  read(): string {
    return super.read().trim();
  }
}

class PrefixStream extends DecoratedStream {
  constructor(
    inner: ReadStream,
    private prefix: string
  ) {
    super(inner);
  }

  read(): string {
    return `${this.prefix}${super.read()}`;
  }
}

// Stack decorators
let stream: ReadStream = new FileStream("/path/to/file.txt");
stream = new TrimStream(stream);
stream = new UpperCaseStream(stream);
stream = new PrefixStream(stream, ">>> ");

console.log(stream.read()); // ">>> CONTENTS OF /PATH/TO/FILE.TXT"

// Middleware pattern (decorators in disguise)
type Middleware<T> = (context: T, next: () => Promise<void>) => Promise<void>;

class Pipeline<T> {
  private middlewares: Middleware<T>[] = [];

  use(middleware: Middleware<T>): void {
    this.middlewares.push(middleware);
  }

  async execute(context: T): Promise<void> {
    let index = 0;

    const next = async (): Promise<void> => {
      if (index < this.middlewares.length) {
        const middleware = this.middlewares[index++];
        await middleware(context, next);
      }
    };

    await next();
  }
}

// Usage
interface RequestContext {
  method: string;
  path: string;
  headers: Record<string, string>;
  body?: unknown;
  user?: { id: string; role: string };
}

const pipeline = new Pipeline<RequestContext>();

pipeline.use(async (ctx, next) => {
  console.log(`[LOG] ${ctx.method} ${ctx.path}`);
  await next();
  console.log(`[LOG] Completed ${ctx.path}`);
});

pipeline.use(async (ctx, next) => {
  const token = ctx.headers["authorization"];
  if (!token) throw new Error("Unauthorized");
  ctx.user = { id: "123", role: "admin" };
  await next();
});

pipeline.use(async (ctx, next) => {
  console.log(`[CACHE] Checking cache for ${ctx.path}`);
  await next();
});

await pipeline.execute({
  method: "GET",
  path: "/api/users",
  headers: { authorization: "Bearer token" },
});
```

---

## Decorator vs Inheritance

```typescript
// ❌ Inheritance: rigid, compile-time only
class Animal {
  move(): string { return "moving"; }
}

class FlyingAnimal extends Animal {
  move(): string { return "flying"; }
}

class SwimmingAnimal extends Animal {
  move(): string { return "swimming"; }
}

// What about a FlyingSwimmingAnimal? Multiple inheritance not supported.

// ✅ Decorator: flexible, runtime
interface Movement {
  move(): string;
}

class BaseMovement implements Movement {
  move(): string { return "moving"; }
}

class FlyingDecorator implements Movement {
  constructor(private inner: Movement) {}
  move(): string { return `${this.inner.move()} + flying`; }
}

class SwimmingDecorator implements Movement {
  constructor(private inner: Movement) {}
  move(): string { return `${this.inner.move()} + swimming`; }
}

// Compose any combination
const duck = new SwimmingDecorator(new FlyingDecorator(new BaseMovement()));
console.log(duck.move()); // "moving + flying + swimming"

// Runtime flexibility
class DynamicMovement implements Movement {
  private behaviors: Array<(s: string) => string> = [];

  addBehavior(behavior: (s: string) => string): void {
    this.behaviors.push(behavior);
  }

  move(): string {
    return this.behaviors.reduce((result, b) => b(result), "moving");
  }
}

const custom = new DynamicMovement();
custom.addBehavior((s) => `${s} quickly`);
custom.addBehavior((s) => `${s} gracefully`);
console.log(custom.move()); // "moving quickly gracefully"
```

---

## Real-World Examples

```typescript
// Express-style middleware (decorator pattern)
type RequestHandler = (req: Request, res: Response) => Promise<void>;

class ExpressApp {
  private middlewares: RequestHandler[] = [];

  use(handler: RequestHandler): void {
    this.middlewares.push(handler);
  }

  async handle(req: Request, res: Response): Promise<void> {
    let index = 0;

    const next = async (): Promise<void> => {
      if (index < this.middlewares.length) {
        await this.middlewares[index++](req, res);
      }
    };

    await next();
  }
}

// Data transformer decorators
interface DataTransformer<T> {
  transform(data: T): T;
}

class DataPipeline<T> {
  private transformers: DataTransformer<T>[] = [];

  add(transformer: DataTransformer<T>): void {
    this.transformers.push(transformer);
  }

  execute(data: T): T {
    return this.transformers.reduce(
      (result, transformer) => transformer.transform(result),
      data
    );
  }
}

// Usage
const pipeline = new DataPipeline<UserData>();
pipeline.add({
  transform: (data) => ({
    ...data,
    name: data.name.trim(),
  }),
});
pipeline.add({
  transform: (data) => ({
    ...data,
    email: data.email.toLowerCase(),
  }),
});
pipeline.add({
  transform: (data) => ({
    ...data,
    createdAt: new Date(data.createdAt),
  }),
});

const cleanData = pipeline.execute({
  name: "  Alice  ",
  email: "ALICE@EXAMPLE.COM",
  createdAt: "2024-01-01",
});

// Component decorator pattern (UI)
interface UIComponent {
  render(): string;
}

class TextComponent implements UIComponent {
  constructor(private text: string) {}
  render(): string { return `<span>${this.text}</span>`; }
}

class BorderDecorator implements UIComponent {
  constructor(private inner: UIComponent, private color: string) {}
  render(): string {
    return `<div style="border: 1px solid ${this.color}">${this.inner.render()}</div>`;
  }
}

class ShadowDecorator implements UIComponent {
  constructor(private inner: UIComponent) {}
  render(): string {
    return `<div style="box-shadow: 2px 2px 5px rgba(0,0,0,0.3)">${this.inner.render()}</div>`;
  }
}

let component: UIComponent = new TextComponent("Hello");
component = new BorderDecorator(component, "blue");
component = new ShadowDecorator(component);
console.log(component.render());
```

---

## TypeScript Decorators vs GoF Decorator

```typescript
// GoF Decorator: Wraps objects at runtime
class GoFDecorator {
  constructor(private inner: SomeInterface) {}
  method() {
    // Add behavior before/after
    this.inner.method();
  }
}

// TypeScript Decorator: Modifies classes/methods at definition time
function Log(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with`, args);
    return original.apply(this, args);
  };
}

class Calculator {
  @Log
  add(a: number, b: number): number {
    return a + b;
  }
}

// TypeScript decorators are syntactic sugar for:
// - Class decorators: modify the class constructor
// - Method decorators: modify methods
// - Property decorators: modify properties
// - Parameter decorators: modify constructor/function parameters
```

---

## Interview Questions

1. **What is the Decorator pattern?**
   A structural pattern that dynamically adds responsibilities to objects by wrapping them in decorator objects.

2. **What is the difference between Decorator and inheritance?**
   Decorators add behavior at runtime and are composable. Inheritance is static and limited by single inheritance.

3. **How do TypeScript decorators differ from GoF decorators?**
   TypeScript decorators modify classes/methods at definition time (metadata). GoF decorators wrap objects at runtime (composition).

4. **What is the middleware pattern?**
   A chain of decorators where each one processes a request and passes it to the next. Used in Express, Koa, etc.

5. **When should you use Decorator over Inheritance?**
   When you need to add behavior dynamically, compose multiple behaviors, or avoid class explosion from combining features.

6. **What are the advantages of the Decorator pattern?**
   Single Responsibility, Open/Closed Principle, runtime flexibility, and avoiding class explosion.

7. **Can decorators be removed once applied?**
   GoF decorators can be unwrapped. TypeScript decorators modify metadata at definition time and cannot be easily removed.

8. **What is the difference between Decorator and Proxy patterns?**
   Decorator adds behavior transparently. Proxy controls access and can add behavior like lazy loading, caching, etc.

9. **How do you implement a generic decorator in TypeScript?**
   Use interfaces and composition: `class Decorator<T extends Interface> implements Interface { constructor(private inner: T) {} }`

10. **What are real-world examples of the Decorator pattern?**
    Java I/O streams, Express middleware, TypeScript decorators, React higher-order components, Redux middleware.
