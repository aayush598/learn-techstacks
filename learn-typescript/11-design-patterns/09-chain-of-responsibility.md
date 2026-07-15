# Chain of Responsibility Pattern in TypeScript

## Table of Contents

- [Chain of Responsibility Overview](#chain-of-responsibility-overview)
- [Handler Chain](#handler-chain)
- [Middleware Pattern](#middleware-pattern)
- [Express-Style Middleware](#express-style-middleware)
- [Logging Pipeline](#logging-pipeline)
- [Validation Chain](#validation-chain)
- [Typed Handlers](#typed-handlers)
- [Real-World Examples](#real-world-examples)
- [Interview Questions](#interview-questions)

---

## Chain of Responsibility Overview

The Chain of Responsibility pattern passes a request along a chain of handlers until one handles it.

```typescript
// Basic concept
abstract class Handler {
  private nextHandler: Handler | null = null;

  setNext(handler: Handler): Handler {
    this.nextHandler = handler;
    return handler;
  }

  handle(request: unknown): unknown {
    if (this.nextHandler) {
      return this.nextHandler.handle(request);
    }
    return null;
  }
}

// Concrete handlers
class AuthHandler extends Handler {
  handle(request: Request): Response | null {
    if (!request.headers.authorization) {
      return { status: 401, body: "Unauthorized" };
    }
    return super.handle(request);
  }
}

class ValidationHandler extends Handler {
  handle(request: Request): Response | null {
    if (!request.body || Object.keys(request.body).length === 0) {
      return { status: 400, body: "Bad Request" };
    }
    return super.handle(request);
  }
}

class RateLimitHandler extends Handler {
  private requests = new Map<string, number[]>();

  handle(request: Request): Response | null {
    const ip = request.headers["x-forwarded-for"] ?? "unknown";
    const now = Date.now();
    const times = this.requests.get(ip as string) ?? [];
    const recent = times.filter((t) => now - t < 60000);

    if (recent.length >= 100) {
      return { status: 429, body: "Too Many Requests" };
    }

    recent.push(now);
    this.requests.set(ip as string, recent);
    return super.handle(request);
  }
}

// Chain setup
const auth = new AuthHandler();
const validation = new ValidationHandler();
const rateLimit = new RateLimitHandler();

auth.setNext(validation).setNext(rateLimit);

// Usage
const response = auth.handle(request);
```

---

## Handler Chain

```typescript
// Generic chain of responsibility
interface Handler<TInput, TOutput> {
  handle(input: TInput): TOutput | null;
  setNext(handler: Handler<TInput, TOutput>): Handler<TInput, TOutput>;
}

abstract class BaseHandler<TInput, TOutput> implements Handler<TInput, TOutput> {
  private next: Handler<TInput, TOutput> | null = null;

  setNext(handler: Handler<TInput, TOutput>): Handler<TInput, TOutput> {
    this.next = handler;
    return handler;
  }

  handle(input: TInput): TOutput | null {
    if (this.canHandle(input)) {
      return this.process(input);
    }
    if (this.next) {
      return this.next.handle(input);
    }
    return null;
  }

  protected abstract canHandle(input: TInput): boolean;
  protected abstract process(input: TInput): TOutput;
}

// Usage
class StringHandler extends BaseHandler<string, string> {
  protected canHandle(input: string): boolean {
    return typeof input === "string";
  }

  protected process(input: string): string {
    return input.toUpperCase();
  }
}

class NumberHandler extends BaseHandler<string, string> {
  protected canHandle(input: string): boolean {
    return !isNaN(Number(input));
  }

  protected process(input: string): string {
    return `Number: ${input}`;
  }
}

class DefaultHandler extends BaseHandler<string, string> {
  protected canHandle(): boolean {
    return true;
  }

  protected process(input: string): string {
    return `Default: ${input}`;
  }
}

// Chain
const chain = new StringHandler();
chain.setNext(new NumberHandler()).setNext(new DefaultHandler());

console.log(chain.handle("hello")); // "HELLO"
console.log(chain.handle("42"));    // "Number: 42"
console.log(chain.handle("xyz"));   // "Default: xyz"
```

---

## Middleware Pattern

```typescript
// Middleware is a specific form of chain of responsibility
type Next = () => Promise<void>;
type Middleware<TContext> = (context: TContext, next: Next) => Promise<void>;

class Application<TContext> {
  private middlewares: Middleware<TContext>[] = [];

  use(...middlewares: Middleware<TContext>[]): void {
    this.middlewares.push(...middlewares);
  }

  async execute(context: TContext): Promise<void> {
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
  response?: { status: number; body: unknown };
}

const app = new Application<RequestContext>();

app.use(async (ctx, next) => {
  console.log(`[LOG] ${ctx.method} ${ctx.path}`);
  const start = Date.now();
  await next();
  console.log(`[LOG] Completed in ${Date.now() - start}ms`);
});

app.use(async (ctx, next) => {
  const token = ctx.headers.authorization;
  if (!token) {
    ctx.response = { status: 401, body: "Unauthorized" };
    return;
  }
  ctx.user = { id: "123", role: "admin" };
  await next();
});

app.use(async (ctx, next) => {
  if (ctx.method === "POST" && !ctx.body) {
    ctx.response = { status: 400, body: "Body required" };
    return;
  }
  await next();
});

app.use(async (ctx, next) => {
  ctx.response = { status: 200, body: "OK" };
  await next();
});

await app.execute({
  method: "POST",
  path: "/api/users",
  headers: { authorization: "Bearer token" },
  body: { name: "Alice" },
});
```

---

## Express-Style Middleware

```typescript
// Express-like middleware
interface ExpressRequest {
  method: string;
  path: string;
  headers: Record<string, string>;
  body?: unknown;
  params?: Record<string, string>;
  query?: Record<string, string>;
  user?: unknown;
}

interface ExpressResponse {
  status: number;
  body: unknown;
  headers: Record<string, string>;
}

type ExpressMiddleware = (
  req: ExpressRequest,
  res: ExpressResponse,
  next: () => void
) => void;

class Router {
  private routes: Map<string, ExpressMiddleware[]> = new Map();

  get(path: string, ...middlewares: ExpressMiddleware[]): void {
    this.routes.set(`GET:${path}`, middlewares);
  }

  post(path: string, ...middlewares: ExpressMiddleware[]): void {
    this.routes.set(`POST:${path}`, middlewares);
  }

  async handle(req: ExpressRequest, res: ExpressResponse): Promise<void> {
    const key = `${req.method}:${req.path}`;
    const middlewares = this.routes.get(key) ?? [];

    let index = 0;

    const next = async (): Promise<void> => {
      if (index < middlewares.length) {
        const middleware = middlewares[index++];
        middleware(req, res, next);
      }
    };

    await next();
  }
}

// Built-in middleware
const corsMiddleware: ExpressMiddleware = (req, res, next) => {
  res.headers["Access-Control-Allow-Origin"] = "*";
  res.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE";
  next();
};

const bodyParserMiddleware: ExpressMiddleware = (req, res, next) => {
  if (req.method === "POST" || req.method === "PUT") {
    // Parse body
    req.body = req.body; // Simplified
  }
  next();
};

const helmetMiddleware: ExpressMiddleware = (req, res, next) => {
  res.headers["X-Content-Type-Options"] = "nosniff";
  res.headers["X-Frame-Options"] = "DENY";
  res.headers["Strict-Transport-Security"] = "max-age=31536000";
  next();
};
```

---

## Logging Pipeline

```typescript
// Composable logging pipeline
interface LogEntry {
  level: string;
  message: string;
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

type LogProcessor = (entry: LogEntry) => LogEntry | null;

class LoggingPipeline {
  private processors: LogProcessor[] = [];

  addProcessor(processor: LogProcessor): void {
    this.processors.push(processor);
  }

  process(entry: LogEntry): LogEntry | null {
    let current: LogEntry | null = entry;

    for (const processor of this.processors) {
      if (current === null) return null;
      current = processor(current);
    }

    return current;
  }
}

// Processors
const timestampProcessor: LogProcessor = (entry) => ({
  ...entry,
  timestamp: new Date(),
});

const sensitiveDataProcessor: LogProcessor = (entry) => {
  const sanitized = { ...entry };
  if (typeof sanitized.message === "string") {
    sanitized.message = sanitized.message
      .replace(/\b\d{3}-\d{2}-\d{4}\b/g, "XXX-XX-XXXX") // SSN
      .replace(/\b\d{16}\b/g, "XXXX-XXXX-XXXX-XXXX"); // Credit card
  }
  return sanitized;
};

const minimumLevelProcessor: LogProcessor = (entry) => {
  const levels = ["debug", "info", "warn", "error"];
  const minLevel = levels.indexOf("info");
  if (levels.indexOf(entry.level) < minLevel) return null;
  return entry;
};

const metadataProcessor: LogProcessor = (entry) => ({
  ...entry,
  metadata: {
    ...entry.metadata,
    hostname: "server-1",
    pid: process.pid,
  },
});

// Pipeline setup
const pipeline = new LoggingPipeline();
pipeline.addProcessor(timestampProcessor);
pipeline.addProcessor(sensitiveDataProcessor);
pipeline.addProcessor(minimumLevelProcessor);
pipeline.addProcessor(metadataProcessor);

// Usage
const entry = pipeline.process({
  level: "info",
  message: "User logged in with SSN 123-45-6789",
  timestamp: new Date(),
});
```

---

## Validation Chain

```typescript
// Composable validation
type Validator<T> = (value: T) => string | null;

class ValidationChain<T> {
  private validators: Validator<T>[] = [];

  add(validator: Validator<T>): this {
    this.validators.push(validator);
    return this;
  }

  validate(value: T): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    for (const validator of this.validators) {
      const error = validator(value);
      if (error) errors.push(error);
    }

    return { valid: errors.length === 0, errors };
  }
}

// Reusable validators
function required<T>(message?: string): Validator<T> {
  return (value) => {
    if (value === null || value === undefined || value === "") {
      return message ?? "This field is required";
    }
    return null;
  };
}

function minLength(min: number, message?: string): Validator<string> {
  return (value) => {
    if (value.length < min) {
      return message ?? `Must be at least ${min} characters`;
    }
    return null;
  };
}

function maxLength(max: number, message?: string): Validator<string> {
  return (value) => {
    if (value.length > max) {
      return message ?? `Must be at most ${max} characters`;
    }
    return null;
  };
}

function pattern(regex: RegExp, message?: string): Validator<string> {
  return (value) => {
    if (!regex.test(value)) {
      return message ?? "Invalid format";
    }
    return null;
  };
}

function custom<T>(fn: (value: T) => boolean, message: string): Validator<T> {
  return (value) => (fn(value) ? null : message);
}

// Usage
const emailValidation = new ValidationChain<string>()
  .add(required("Email is required"))
  .add(pattern(/^[^\s@]+@[^\s@]+\.[^\s@]+$/, "Invalid email format"))
  .add(maxLength(255, "Email too long"));

const result = emailValidation.validate("test@example.com");
console.log(result); // { valid: true, errors: [] }

// Complex validation chain
interface UserRegistration {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

const registrationValidation = new ValidationChain<UserRegistration>()
  .add((data) => {
    const usernameResult = new ValidationChain<string>()
      .add(required())
      .add(minLength(3))
      .add(maxLength(20))
      .add(pattern(/^[a-zA-Z0-9_]+$/, "Only letters, numbers, and underscores"));
    return usernameResult.validate(data.username).errors[0] ?? null;
  })
  .add((data) => {
    const emailResult = emailValidation;
    return emailResult.validate(data.email).errors[0] ?? null;
  })
  .add((data) => {
    if (data.password !== data.confirmPassword) {
      return "Passwords do not match";
    }
    return null;
  });
```

---

## Typed Handlers

```typescript
// Strongly typed handler chain
interface TypedHandler<TRequest, TResponse> {
  handle(
    request: TRequest,
    next: () => Promise<TResponse | null>
  ): Promise<TResponse | null>;
}

class TypedHandlerChain<TRequest, TResponse> {
  private handlers: TypedHandler<TRequest, TResponse>[] = [];

  use(handler: TypedHandler<TRequest, TResponse>): this {
    this.handlers.push(handler);
    return this;
  }

  async execute(request: TRequest): Promise<TResponse | null> {
    let index = 0;

    const next = async (): Promise<TResponse | null> => {
      if (index < this.handlers.length) {
        const handler = this.handlers[index++];
        return handler.handle(request, next);
      }
      return null;
    };

    return next();
  }
}

// Usage
interface APIRequest {
  method: string;
  path: string;
  headers: Record<string, string>;
  body?: unknown;
}

interface APIResponse {
  status: number;
  body: unknown;
}

const chain = new TypedHandlerChain<APIRequest, APIResponse>();

chain.use({
  async handle(req, next) {
    console.log(`[Auth] ${req.method} ${req.path}`);
    if (!req.headers.authorization) {
      return { status: 401, body: "Unauthorized" };
    }
    return next();
  },
});

chain.use({
  async handle(req, next) {
    console.log(`[RateLimit] Checking rate limit`);
    return next();
  },
});

chain.use({
  async handle(req, next) {
    console.log(`[Handler] Processing request`);
    return { status: 200, body: "OK" };
  },
});
```

---

## Real-World Examples

```typescript
// Authentication chain
interface AuthRequest {
  token?: string;
  ip: string;
  userAgent: string;
}

interface AuthResult {
  authenticated: boolean;
  user?: { id: string; role: string };
  error?: string;
}

class AuthChain {
  private handlers: Array<(req: AuthRequest) => Promise<AuthResult | null>> = [];

  use(handler: (req: AuthRequest) => Promise<AuthResult | null>): this {
    this.handlers.push(handler);
    return this;
  }

  async authenticate(req: AuthRequest): Promise<AuthResult> {
    for (const handler of this.handlers) {
      const result = await handler(req);
      if (result) return result;
    }
    return { authenticated: false, error: "No handler could authenticate" };
  }
}

// Build chain
const authChain = new AuthChain()
  .use(async (req) => {
    if (!req.token) return null;
    // Validate JWT
    return { authenticated: true, user: { id: "1", role: "admin" } };
  })
  .use(async (req) => {
    // Check API key
    if (req.userAgent.includes("Bot")) {
      return { authenticated: true, user: { id: "bot", role: "bot" } };
    }
    return null;
  });

// Error handling chain
class ErrorChain {
  private handlers: Array<(error: Error) => string | null> = [];

  use(handler: (error: Error) => string | null): this {
    this.handlers.push(handler);
    return this;
  }

  handle(error: Error): string {
    for (const handler of this.handlers) {
      const result = handler(error);
      if (result) return result;
    }
    return "Internal Server Error";
  }
}

const errorChain = new ErrorChain()
  .use((err) => {
    if (err instanceof ValidationError) return `Validation: ${err.message}`;
    return null;
  })
  .use((err) => {
    if (err instanceof NotFoundError) return `Not Found: ${err.message}`;
    return null;
  })
  .use(() => "Something went wrong");
```

---

## Interview Questions

1. **What is the Chain of Responsibility pattern?**
   A behavioral pattern that passes requests along a chain of handlers until one handles it.

2. **How does the middleware pattern relate to Chain of Responsibility?**
   Middleware is a specific form where each handler processes the request and calls `next()` to pass it along.

3. **What is the difference between middleware and Chain of Responsibility?**
   Middleware typically calls `next()` to continue the chain. Chain of Responsibility stops when a handler processes the request.

4. **How do you implement error handling in a middleware chain?**
   Use try/catch in each middleware, or implement error-specific middleware that catches thrown errors.

5. **What is the performance impact of long handler chains?**
   Each handler adds overhead. Keep chains short and optimize hot paths.

6. **How do you stop the chain from continuing?**
   Don't call `next()`, or return a response directly.

7. **What is the difference between Chain of Responsibility and Decorator?**
   Chain of Responsibility chooses one handler to process. Decorator wraps all handlers to add behavior.

8. **How do you handle asynchronous handlers in a chain?**
   Use async/await and ensure each handler awaits `next()`.

9. **What are real-world examples of this pattern?**
   Express middleware, logging pipelines, validation chains, authentication flows, and event bubbling.

10. **How do you test handler chains?**
    Test each handler independently, then test the chain with mock handlers.
