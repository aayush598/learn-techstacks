# Adapter Pattern in TypeScript

## Table of Contents

- [Adapter Pattern Overview](#adapter-pattern-overview)
- [Class Adapter](#class-adapter)
- [Object Adapter](#object-adapter)
- [Typed Adapters](#typed-adapters)
- [Interface Adaptation](#interface-adaptation)
- [Third-Party Library Adapters](#third-party-library-adapters)
- [Adapter vs Wrapper](#adapter-vs-wrapper)
- [Real-World Examples](#real-world-examples)
- [Interview Questions](#interview-questions)

---

## Adapter Pattern Overview

The Adapter pattern allows incompatible interfaces to work together by wrapping one interface with another.

```typescript
// Problem: Different logging libraries with different interfaces
interface OldLogger {
  logMessage(level: string, message: string): void;
  logError(error: string, stackTrace: string): void;
}

interface NewLogger {
  info(message: string): void;
  error(message: string, error?: Error): void;
  warn(message: string): void;
}

// Adapter: Makes old logger work with new interface
class OldToNewLoggerAdapter implements NewLogger {
  constructor(private oldLogger: OldLogger) {}

  info(message: string): void {
    this.oldLogger.logMessage("INFO", message);
  }

  error(message: string, error?: Error): void {
    const stackTrace = error?.stack ?? "No stack trace";
    this.oldLogger.logError(message, stackTrace);
  }

  warn(message: string): void {
    this.oldLogger.logMessage("WARN", message);
  }
}

// Usage
const oldLogger: OldLogger = {
  logMessage: (level, msg) => console.log(`[${level}] ${msg}`),
  logError: (err, stack) => console.error(`[ERROR] ${err}\n${stack}`),
};

const adaptedLogger = new OldToNewLoggerAdapter(oldLogger);
adaptedLogger.info("Application started"); // Uses old logger under the hood
```

---

## Class Adapter

```typescript
// Class adapter uses inheritance
interface ModernStorage {
  save(key: string, value: unknown): Promise<void>;
  load(key: string): Promise<unknown>;
  delete(key: string): Promise<void>;
}

// Legacy storage with different interface
class LegacyLocalStorage {
  setItem(key: string, value: string): void {
    // Implementation
  }

  getItem(key: string): string | null {
    return null;
  }

  removeItem(key: string): void {
    // Implementation
  }
}

// Class adapter (extends the adaptee)
class LocalStorageAdapter extends LegacyLocalStorage implements ModernStorage {
  async save(key: string, value: unknown): Promise<void> {
    this.setItem(key, JSON.stringify(value));
  }

  async load(key: string): Promise<unknown> {
    const data = this.getItem(key);
    return data ? JSON.parse(data) : null;
  }

  async delete(key: string): Promise<void> {
    this.removeItem(key);
  }
}

// Another class adapter example
interface PaymentProcessor {
  charge(amount: number, currency: string): Promise<PaymentResult>;
  refund(transactionId: string): Promise<RefundResult>;
}

// Stripe's interface (different from ours)
class StripeAPI {
  createCharge(params: {
    amount: number;
    currency: string;
    source: string;
  }): Promise<{ id: string; status: string }> {
    return Promise.resolve({ id: "ch_123", status: "succeeded" });
  }

  createRefund(params: {
    charge: string;
    amount?: number;
  }): Promise<{ id: string; status: string }> {
    return Promise.resolve({ id: "rf_123", status: "succeeded" });
  }
}

// Adapter
class StripeAdapter extends StripeAPI implements PaymentProcessor {
  async charge(amount: number, currency: string): Promise<PaymentResult> {
    const result = await this.createCharge({
      amount: Math.round(amount * 100), // Convert to cents
      currency: currency.toLowerCase(),
      source: "tok_visa", // Would come from frontend
    });

    return {
      success: result.status === "succeeded",
      transactionId: result.id,
    };
  }

  async refund(transactionId: string): Promise<RefundResult> {
    const result = await this.createRefund({ charge: transactionId });
    return {
      success: result.status === "succeeded",
      refundId: result.id,
    };
  }
}
```

---

## Object Adapter

```typescript
// Object adapter uses composition
interface HttpClient {
  request(url: string, options: RequestOptions): Promise<HttpResponse>;
}

// Axios has different interface
import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

class AxiosAdapter implements HttpClient {
  private client: AxiosInstance;

  constructor(config?: AxiosRequestConfig) {
    this.client = axios.create(config);
  }

  async request(url: string, options: RequestOptions): Promise<HttpResponse> {
    const axiosConfig: AxiosRequestConfig = {
      url,
      method: options.method as any,
      headers: options.headers,
      data: options.body,
      timeout: options.timeout,
    };

    try {
      const response = await this.client.request(axiosConfig);
      return {
        status: response.status,
        headers: response.headers as Record<string, string>,
        body: response.data,
      };
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        return {
          status: error.response.status,
          headers: error.response.headers as Record<string, string>,
          body: error.response.data,
        };
      }
      throw error;
    }
  }
}

// Fetch adapter
class FetchAdapter implements HttpClient {
  async request(url: string, options: RequestOptions): Promise<HttpResponse> {
    const response = await fetch(url, {
      method: options.method,
      headers: options.headers as HeadersInit,
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: options.timeout ? AbortSignal.timeout(options.timeout) : undefined,
    });

    return {
      status: response.status,
      headers: Object.fromEntries(response.headers.entries()),
      body: await response.json(),
    };
  }
}

// Types
interface RequestOptions {
  method: string;
  headers?: Record<string, string>;
  body?: unknown;
  timeout?: number;
}

interface HttpResponse {
  status: number;
  headers: Record<string, string>;
  body: unknown;
}
```

---

## Typed Adapters

```typescript
// Generic adapter pattern
interface Adapter<TInput, TOutput> {
  adapt(input: TInput): TOutput;
}

// Compound adapter
class CompoundAdapter<T1, T2, TOutput>
  implements Adapter<[T1, T2], TOutput>
{
  constructor(
    private adapter1: Adapter<T1, any>,
    private adapter2: Adapter<T2, any>,
    private combiner: (a: any, b: any) => TOutput
  ) {}

  adapt(input: [T1, T2]): TOutput {
    return this.combiner(
      this.adapter1.adapt(input[0]),
      this.adapter2.adapt(input[1])
    );
  }
}

// Data format adapters
interface UserRecord {
  firstName: string;
  lastName: string;
  emailAddress: string;
}

interface UserEntity {
  name: string;
  email: string;
}

class UserRecordAdapter implements Adapter<UserRecord, UserEntity> {
  adapt(input: UserRecord): UserEntity {
    return {
      name: `${input.firstName} ${input.lastName}`,
      email: input.emailAddress,
    };
  }
}

class UserEntityAdapter implements Adapter<UserEntity, UserRecord> {
  adapt(input: UserEntity): UserRecord {
    const [firstName, ...rest] = input.name.split(" ");
    return {
      firstName,
      lastName: rest.join(" "),
      emailAddress: input.email,
    };
  }
}

// Chain of adapters
class AdapterChain<T> {
  private adapters: Adapter<any, any>[] = [];

  addAdapter<A, B>(adapter: Adapter<A, B>): AdapterChain<T> {
    this.adapters.push(adapter);
    return this;
  }

  adapt(input: T): T {
    return this.adapters.reduce(
      (result, adapter) => adapter.adapt(result),
      input as any
    ) as T;
  }
}
```

---

## Interface Adaptation

```typescript
// Adapting incompatible interfaces
interface EventEmitter {
  on(event: string, callback: Function): void;
  emit(event: string, ...args: unknown[]): void;
}

interface TypedEmitter<T extends Record<string, unknown>> {
  on<K extends keyof T>(event: K, callback: (data: T[K]) => void): void;
  emit<K extends keyof T>(event: K, data: T[K]): void;
}

// Adaptor
class EventEmitterAdapter<T extends Record<string, unknown>>
  implements TypedEmitter<T>
{
  constructor(private emitter: EventEmitter) {}

  on<K extends keyof T>(event: K, callback: (data: T[K]) => void): void {
    this.emitter.on(event as string, callback);
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    this.emitter.emit(event as string, data);
  }
}

// Adapting callbacks to promises
function promisify<T>(fn: (...args: any[]) => void): (...args: any[]) => Promise<T> {
  return (...args: any[]) =>
    new Promise((resolve, reject) => {
      fn(...args, (err: Error | null, result?: T) => {
        if (err) reject(err);
        else resolve(result!);
      });
    });
}

// Adapting sync to async
function asyncAdapter<T>(fn: () => T): () => Promise<T> {
  return () => Promise.resolve(fn());
}

// Adapting different date formats
interface DateAdapter<TInput> {
  toISO(input: TInput): string;
  fromISO(iso: string): TInput;
}

class UnixTimestampAdapter implements DateAdapter<number> {
  toISO(timestamp: number): string {
    return new Date(timestamp * 1000).toISOString();
  }

  fromISO(iso: string): number {
    return Math.floor(new Date(iso).getTime() / 1000);
  }
}

class DateObjectAdapter implements DateAdapter<Date> {
  toISO(date: Date): string {
    return date.toISOString();
  }

  fromISO(iso: string): Date {
    return new Date(iso);
  }
}
```

---

## Third-Party Library Adapters

```typescript
// Adapting different database ORMs
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findAll(): Promise<User[]>;
  create(data: CreateUserDTO): Promise<User>;
  update(id: string, data: Partial<User>): Promise<User>;
  delete(id: string): Promise<void>;
}

// Prisma adapter
class PrismaUserAdapter implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    const result = await this.prisma.user.findUnique({ where: { id } });
    return result ? this.toDomain(result) : null;
  }

  async findAll(): Promise<User[]> {
    const results = await this.prisma.user.findMany();
    return results.map(this.toDomain);
  }

  async create(data: CreateUserDTO): Promise<User> {
    const result = await this.prisma.user.create({ data });
    return this.toDomain(result);
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    const result = await this.prisma.user.update({ where: { id }, data });
    return this.toDomain(result);
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }

  private toDomain(prismaUser: any): User {
    return {
      id: prismaUser.id,
      name: prismaUser.name,
      email: prismaUser.email,
    };
  }
}

// TypeORM adapter
class TypeORMUserAdapter implements UserRepository {
  constructor(private repository: Repository<User>) {}

  async findById(id: string): Promise<User | null> {
    return this.repository.findOneBy({ id } as any);
  }

  async findAll(): Promise<User[]> {
    return this.repository.find();
  }

  async create(data: CreateUserDTO): Promise<User> {
    const entity = this.repository.create(data);
    return this.repository.save(entity);
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    await this.repository.update(id, data);
    return this.findById(id) as Promise<User>;
  }

  async delete(id: string): Promise<void> {
    await this.repository.delete(id);
  }
}

// Email service adapters
interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

class SendGridAdapter implements EmailService {
  constructor(private apiKey: string) {}

  async send(to: string, subject: string, body: string): Promise<void> {
    // Adapt to SendGrid's API
    await fetch("https://api.sendgrid.com/v3/mail/send", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: to }] }],
        from: { email: "noreply@example.com" },
        subject,
        content: [{ type: "text/plain", value: body }],
      }),
    });
  }
}

class AWSSESAdapter implements EmailService {
  constructor(private ses: AWS.SES) {}

  async send(to: string, subject: string, body: string): Promise<void> {
    await this.ses.sendEmail({
      Source: "noreply@example.com",
      Destination: { ToAddresses: [to] },
      Message: {
        Subject: { Data: subject },
        Body: { Text: { Data: body } },
      },
    }).promise();
  }
}
```

---

## Adapter vs Wrapper

```typescript
// Adapter: Changes interface to match expected API
// Wrapper: Adds behavior while keeping the same interface

// Adapter: Changes interface
interface OldAPI { getData(): string; }
interface NewAPI { fetchData(): Promise<string>; }

class APIAdapter implements NewAPI {
  constructor(private old: OldAPI) {}
  async fetchData(): Promise<string> {
    return this.old.getData();
  }
}

// Wrapper: Adds behavior
interface Logger {
  log(message: string): void;
}

class TimestampLogger implements Logger {
  constructor(private inner: Logger) {}
  log(message: string): void {
    this.inner.log(`[${new Date().toISOString()}] ${message}`);
  }
}

class LevelLogger implements Logger {
  constructor(private inner: Logger, private level: string) {}
  log(message: string): void {
    this.inner.log(`[${this.level}] ${message}`);
  }
}
```

---

## Real-World Examples

```typescript
// Payment gateway adapter
interface PaymentGateway {
  charge(amount: number, currency: string): Promise<PaymentResult>;
  refund(id: string): Promise<RefundResult>;
}

// Stripe adapter
class StripeAdapter implements PaymentGateway {
  async charge(amount: number, currency: string): Promise<PaymentResult> {
    // Adapt to Stripe API
    return { success: true, transactionId: "stripe_123" };
  }
  async refund(id: string): Promise<RefundResult> {
    return { success: true, refundId: "rf_123" };
  }
}

// PayPal adapter
class PayPalAdapter implements PaymentGateway {
  async charge(amount: number, currency: string): Promise<PaymentResult> {
    // Adapt to PayPal API
    return { success: true, transactionId: "paypal_123" };
  }
  async refund(id: string): Promise<RefundResult> {
    return { success: true, refundId: "pp_rf_123" };
  }
}

// Third-party API adapter
interface WeatherService {
  getTemperature(city: string): Promise<number>;
  getForecast(city: string): Promise<Forecast>;
}

class OpenWeatherAdapter implements WeatherService {
  constructor(private apiKey: string) {}

  async getTemperature(city: string): Promise<number> {
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${this.apiKey}`
    );
    const data = await response.json();
    return data.main.temp - 273.15; // Convert Kelvin to Celsius
  }

  async getForecast(city: string): Promise<Forecast> {
    // Adapt forecast data
    return { city, days: [] };
  }
}
```

---

## Interview Questions

1. **What is the Adapter pattern?**
   A structural pattern that allows incompatible interfaces to work together by wrapping one interface with another.

2. **When would you use the Adapter pattern?**
   When integrating third-party libraries, when working with legacy systems, or when different parts of a system use different interfaces.

3. **What is the difference between Class Adapter and Object Adapter?**
   Class adapter uses inheritance (extends the adaptee). Object adapter uses composition (wraps the adaptee).

4. **What is the difference between Adapter and Decorator?**
   Adapter changes the interface. Decorator adds behavior while maintaining the same interface.

5. **How do you implement a type-safe adapter in TypeScript?**
   Use generics to define input and output types, ensuring the adapter correctly transforms data.

6. **What is an example of the Adapter pattern in JavaScript?**
   Array.from() adapts iterables to arrays. Promise.resolve() adapts values to promises.

7. **Can an adapter work in both directions?**
   Yes, you can create adapters for both directions (A to B and B to A).

8. **What are the disadvantages of the Adapter pattern?**
   Added complexity, indirection, and potential performance overhead from the adaptation layer.

9. **How does the Adapter pattern relate to the Interface Segregation Principle?**
   Adapters help conform to ISP by adapting fat interfaces to specific client needs.

10. **What are real-world examples of the Adapter pattern?**
    Database drivers, payment gateways, API clients, logging frameworks, and legacy system integration.
