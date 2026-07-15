# Builder Pattern in TypeScript

## Table of Contents

- [Builder Pattern Basics](#builder-pattern-basics)
- [Fluent Interface](#fluent-interface)
- [Type-Safe Builder](#type-safe-builder)
- [Builder vs Factory](#builder-vs-factory)
- [Builder with Generics](#builder-with-generics)
- [Step Builder Pattern](#step-builder-pattern)
- [Director Class](#director-class)
- [Real-World Examples](#real-world-examples)
- [Interview Questions](#interview-questions)

---

## Builder Pattern Basics

The Builder pattern separates the construction of a complex object from its representation.

```typescript
// Product
class QueryBuilder {
  private _table: string = "";
  private _conditions: string[] = [];
  private _fields: string[] = ["*"];
  private _orderBy: string = "";
  private _limit: number | null = null;
  private _offset: number | null = null;

  table(name: string): this {
    this._table = name;
    return this;
  }

  select(...fields: string[]): this {
    this._fields = fields;
    return this;
  }

  where(condition: string): this {
    this._conditions.push(condition);
    return this;
  }

  orderBy(field: string, direction: "ASC" | "DESC" = "ASC"): this {
    this._orderBy = `${field} ${direction}`;
    return this;
  }

  limit(n: number): this {
    this._limit = n;
    return this;
  }

  offset(n: number): this {
    this._offset = n;
    return this;
  }

  build(): string {
    let query = `SELECT ${this._fields.join(", ")} FROM ${this._table}`;
    if (this._conditions.length > 0) {
      query += ` WHERE ${this._conditions.join(" AND ")}`;
    }
    if (this._orderBy) query += ` ORDER BY ${this._orderBy}`;
    if (this._limit !== null) query += ` LIMIT ${this._limit}`;
    if (this._offset !== null) query += ` OFFSET ${this._offset}`;
    return query;
  }
}

// Usage
const query = new QueryBuilder()
  .table("users")
  .select("id", "name", "email")
  .where("age > 18")
  .where("active = true")
  .orderBy("name", "ASC")
  .limit(10)
  .build();

console.log(query);
// SELECT id, name, email FROM users WHERE age > 18 AND active = true ORDER BY name ASC LIMIT 10
```

---

## Fluent Interface

```typescript
// Fluent builder with method chaining
class RequestBuilder {
  private _url: string = "";
  private _method: string = "GET";
  private _headers: Record<string, string> = {};
  private _body: unknown = null;
  private _timeout: number = 5000;
  private _retries: number = 0;

  url(url: string): this {
    this._url = url;
    return this;
  }

  method(method: string): this {
    this._method = method.toUpperCase();
    return this;
  }

  header(key: string, value: string): this {
    this._headers[key] = value;
    return this;
  }

  headers(headers: Record<string, string>): this {
    Object.assign(this._headers, headers);
    return this;
  }

  body(body: unknown): this {
    this._body = body;
    return this;
  }

  timeout(ms: number): this {
    this._timeout = ms;
    return this;
  }

  retries(count: number): this {
    this._retries = count;
    return this;
  }

  // Terminal methods
  async send(): Promise<Response> {
    const options: RequestInit = {
      method: this._method,
      headers: this._headers,
      body: this._body ? JSON.stringify(this._body) : undefined,
      signal: AbortSignal.timeout(this._timeout),
    };

    let lastError: Error | undefined;
    for (let i = 0; i <= this._retries; i++) {
      try {
        return await fetch(this._url, options);
      } catch (error) {
        lastError = error as Error;
        if (i < this._retries) {
          await new Promise((r) => setTimeout(r, 1000 * (i + 1)));
        }
      }
    }
    throw lastError;
  }

  build(): { url: string; options: RequestInit } {
    return {
      url: this._url,
      options: {
        method: this._method,
        headers: this._headers,
        body: this._body ? JSON.stringify(this._body) : undefined,
      },
    };
  }
}

// Usage
const response = await new RequestBuilder()
  .url("https://api.example.com/users")
  .method("POST")
  .header("Content-Type", "application/json")
  .body({ name: "Alice", email: "alice@example.com" })
  .timeout(10000)
  .retries(3)
  .send();
```

---

## Type-Safe Builder

```typescript
// Builder with compile-time safety
interface ServerConfig {
  host: string;
  port: number;
  ssl: boolean;
  certPath?: string;
  keyPath?: string;
  database: string;
  cache: boolean;
}

class ServerConfigBuilder {
  private config: Partial<ServerConfig> = {};

  host(host: string): this {
    this.config.host = host;
    return this;
  }

  port(port: number): this {
    this.config.port = port;
    return this;
  }

  ssl(enabled: boolean): this {
    this.config.ssl = enabled;
    return this;
  }

  certPath(path: string): this {
    this.config.certPath = path;
    return this;
  }

  keyPath(path: string): this {
    this.config.keyPath = path;
    return this;
  }

  database(url: string): this {
    this.config.database = url;
    return this;
  }

  cache(enabled: boolean): this {
    this.config.cache = enabled;
    return this;
  }

  // Validate required fields
  build(): ServerConfig {
    if (!this.config.host) throw new Error("host is required");
    if (!this.config.port) throw new Error("port is required");
    if (this.config.ssl && (!this.config.certPath || !this.config.keyPath)) {
      throw new Error("certPath and keyPath are required when SSL is enabled");
    }
    return this.config as ServerConfig;
  }
}

// Usage
const config = new ServerConfigBuilder()
  .host("localhost")
  .port(3000)
  .ssl(true)
  .certPath("/path/to/cert.pem")
  .keyPath("/path/to/key.pem")
  .database("postgresql://localhost/mydb")
  .cache(true)
  .build();
```

---

## Builder vs Factory

```typescript
// Factory: Single method creates object
class UserFactory {
  static create(type: "admin" | "user", data: UserData): User {
    return { ...data, type, createdAt: new Date() };
  }
}

// Builder: Step-by-step construction
class UserBuilder {
  private name = "";
  private email = "";
  private role: "admin" | "user" = "user";
  private permissions: string[] = [];

  setName(name: string): this { this.name = name; return this; }
  setEmail(email: string): this { this.email = email; return this; }
  setRole(role: "admin" | "user"): this { this.role = role; return this; }
  addPermission(perm: string): this { this.permissions.push(perm); return this; }

  build(): User {
    if (!this.name) throw new Error("Name is required");
    if (!this.email) throw new Error("Email is required");

    const user: User = {
      id: crypto.randomUUID(),
      name: this.name,
      email: this.email,
      role: this.role,
      permissions: this.permissions,
      createdAt: new Date(),
    };

    // Reset for reuse
    this.name = "";
    this.email = "";
    this.role = "user";
    this.permissions = [];

    return user;
  }
}

// When to use which:
// Factory: Simple creation, one or few parameters, choose implementation
// Builder: Complex object, many optional parameters, step-by-step construction
```

---

## Builder with Generics

```typescript
// Generic builder
class GenericBuilder<T> {
  private product: Partial<T> = {};
  private validators: Array<(product: Partial<T>) => void> = [];

  set<K extends keyof T>(key: K, value: T[K]): this {
    this.product[key] = value;
    return this;
  }

  validate(validator: (product: Partial<T>) => void): this {
    this.validators.push(validator);
    return this;
  }

  build(): T {
    for (const validator of this.validators) {
      validator(this.product);
    }
    return this.product as T;
  }
}

// Usage
interface Email {
  to: string;
  subject: string;
  body: string;
  cc?: string[];
  bcc?: string[];
  attachments?: Array<{ name: string; content: Buffer }>;
}

const email = new GenericBuilder<Email>()
  .set("to", "user@example.com")
  .set("subject", "Hello")
  .set("body", "World")
  .validate((e) => {
    if (!e.to?.includes("@")) throw new Error("Invalid email");
  })
  .build();

// Type-safe builder with required fields tracking
type BuilderState = {
  [K in keyof Email]?: boolean;
};

class TypedEmailBuilder<TRequired extends keyof Email = never> {
  private email: Partial<Email> = {};

  to(email: string): TypedEmailBuilder<TRequired | "to"> {
    this.email.to = email;
    return this as any;
  }

  subject(subject: string): TypedEmailBuilder<TRequired | "subject"> {
    this.email.subject = subject;
    return this as any;
  }

  body(body: string): TypedEmailBuilder<TRequired | "body"> {
    this.email.body = body;
    return this as any;
  }

  build(this: TypedEmailBuilder<"to" | "subject" | "body">): Email {
    return this.email as Email;
  }
}

// All required fields must be set
const typedEmail = new TypedEmailBuilder()
  .to("user@example.com")  // ✅
  .subject("Hello")        // ✅
  .body("World")           // ✅
  .build();                // ✅ Works!

// const incomplete = new TypedEmailBuilder().to("x@y.com").build(); // ❌ Error!
```

---

## Step Builder Pattern

```typescript
// Enforce build steps at compile time
interface Step1 {
  setHost(host: string): Step2;
}

interface Step2 {
  setPort(port: number): Step3;
}

interface Step3 {
  setDatabase(url: string): Step4;
}

interface Step4 {
  build(): Config;
}

class ConfigBuilder implements Step1, Step2, Step3, Step4 {
  private config: Partial<Config> = {};

  setHost(host: string): Step2 {
    this.config.host = host;
    return this;
  }

  setPort(port: number): Step3 {
    this.config.port = port;
    return this;
  }

  setDatabase(url: string): Step4 {
    this.config.database = url;
    return this;
  }

  build(): Config {
    return this.config as Config;
  }
}

// Usage - must follow the correct order
const config = new ConfigBuilder()
  .setHost("localhost")
  .setPort(3000)
  .setDatabase("postgresql://localhost/mydb")
  .build();

// new ConfigBuilder().setPort(3000); // ❌ Error: must call setHost first
```

---

## Director Class

```typescript
// Director orchestrates builder calls
interface BuildPlan<T> {
  build(builder: any): void;
}

class Director {
  static buildUser(builder: UserBuilder, plan: "admin" | "user" | "guest"): void {
    switch (plan) {
      case "admin":
        builder.setRole("admin").addPermission("read").addPermission("write").addPermission("delete");
        break;
      case "user":
        builder.setRole("user").addPermission("read");
        break;
      case "guest":
        builder.setRole("user");
        break;
    }
  }
}

// Preset configurations
class ConfigPresets {
  static development(builder: ServerConfigBuilder): void {
    builder
      .host("localhost")
      .port(3000)
      .ssl(false)
      .cache(false);
  }

  static production(builder: ServerConfigBuilder): void {
    builder
      .host("api.example.com")
      .port(443)
      .ssl(true)
      .cache(true);
  }
}

// Usage with Director
const devConfig = ConfigPresets.development(new ServerConfigBuilder())
  .database("postgresql://localhost/dev")
  .build();
```

---

## Real-World Examples

```typescript
// React element builder (JSX is essentially a builder)
// <Button variant="primary" size="large" onClick={handler}>Submit</Button>

// HTML builder
class HTMLBuilder {
  private elements: string[] = [];

  tag(name: string, attrs?: Record<string, string>): this {
    const attrStr = attrs
      ? " " + Object.entries(attrs).map(([k, v]) => `${k}="${v}"`).join(" ")
      : "";
    this.elements.push(`<${name}${attrStr}>`);
    return this;
  }

  text(content: string): this {
    this.elements.push(content);
    return this;
  }

  endTag(name: string): this {
    this.elements.push(`</${name}>`);
    return this;
  }

  build(): string {
    return this.elements.join("");
  }
}

// Usage
const html = new HTMLBuilder()
  .tag("div", { class: "container" })
    .tag("h1")
    .text("Hello World")
    .endTag("h1")
    .tag("p")
    .text("This is a paragraph")
    .endTag("p")
  .endTag("div")
  .build();

// API endpoint builder
class EndpointBuilder {
  private path = "";
  private method = "GET";
  private middlewares: Function[] = [];
  private schemas: Record<string, unknown> = {};

  path(p: string): this { this.path = p; return this; }
  method(m: string): this { this.method = m; return this; }
  middleware(fn: Function): this { this.middlewares.push(fn); return this; }
  schema(name: string, schema: unknown): this { this.schemas[name] = schema; return this; }

  register(app: Express): void {
    (app as any)[this.method.toLowerCase()](this.path, ...this.middlewares);
  }
}
```

---

## Interview Questions

1. **What is the Builder pattern?**
   A creational pattern that separates the construction of a complex object from its representation, allowing step-by-step construction.

2. **When should you use Builder over Constructor?**
   When an object has many optional parameters, when construction involves multiple steps, or when you want readable object creation.

3. **What is the fluent interface?**
   Method chaining where each method returns `this`, allowing readable step-by-step configuration.

4. **What is the difference between Builder and Factory?**
   Factory creates objects in one step. Builder constructs objects step by step. Factory is for simple creation, Builder for complex construction.

5. **How do you make a type-safe builder in TypeScript?**
   Use generics, conditional types, and the `this` return type to ensure required fields are set before building.

6. **What is the Step Builder pattern?**
   A pattern that enforces the order of builder steps at compile time using interfaces.

7. **What is a Director class?**
   A class that encapsulates reusable build configurations, working with builders to create different representations.

8. **What are the advantages of the Builder pattern?**
   Readable code, immutability, optional parameters, step-by-step construction, and reuse via Director.

9. **Can builders be reused?**
   Yes, but they need to be reset between builds. Some implementations create a new builder for each build.

10. **What are real-world examples of the Builder pattern?**
    SQL query builders, HTTP request builders, HTML builders, test data builders, configuration builders.
