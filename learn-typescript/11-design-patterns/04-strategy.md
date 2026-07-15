# Strategy Pattern in TypeScript

## Table of Contents

- [Strategy Pattern Basics](#strategy-pattern-basics)
- [Strategy Interface](#strategy-interface)
- [Concrete Strategies](#concrete-strategies)
- [Context Class](#context-class)
- [Strategy with Generics](#strategy-with-generics)
- [Strategy vs Polymorphism](#strategy-vs-polymorphism)
- [Runtime Strategy Selection](#runtime-strategy-selection)
- [Real-World Examples](#real-world-examples)
- [Interview Questions](#interview-questions)

---

## Strategy Pattern Basics

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

```typescript
// Basic concept
interface SortStrategy<T> {
  sort(data: T[]): T[];
}

class BubbleSort<T> implements SortStrategy<T> {
  sort(data: T[]): T[] {
    const arr = [...data];
    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr.length - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
          [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        }
      }
    }
    return arr;
  }
}

class QuickSort<T> implements SortStrategy<T> {
  sort(data: T[]): T[] {
    if (data.length <= 1) return data;
    const pivot = data[0];
    const rest = data.slice(1);
    const left = rest.filter((x) => x <= pivot);
    const right = rest.filter((x) => x > pivot);
    return [...this.sort(left), pivot, ...this.sort(right)];
  }
}

// Context
class Sorter<T> {
  constructor(private strategy: SortStrategy<T>) {}

  setStrategy(strategy: SortStrategy<T>): void {
    this.strategy = strategy;
  }

  sort(data: T[]): T[] {
    return this.strategy.sort(data);
  }
}

// Usage
const sorter = new Sorter(new BubbleSort<number>());
console.log(sorter.sort([3, 1, 4, 1, 5])); // [1, 1, 3, 4, 5]

sorter.setStrategy(new QuickSort<number>());
console.log(sorter.sort([3, 1, 4, 1, 5])); // [1, 1, 3, 4, 5]
```

---

## Strategy Interface

```typescript
// Strongly typed strategy interface
interface CompressionStrategy {
  readonly name: string;
  compress(data: Buffer): Promise<Buffer>;
  decompress(data: Buffer): Promise<Buffer>;
}

// Validation strategy
interface ValidationStrategy<T> {
  validate(value: T): ValidationResult;
}

interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

// Pricing strategy
interface PricingStrategy {
  calculate(items: CartItem[]): number;
  readonly name: string;
}

// Authentication strategy
interface AuthStrategy {
  authenticate(credentials: Credentials): Promise<AuthResult>;
  readonly provider: string;
}
```

---

## Concrete Strategies

```typescript
// Compression strategies
class GzipCompression implements CompressionStrategy {
  readonly name = "gzip";

  async compress(data: Buffer): Promise<Buffer> {
    const { gzip } = await import("zlib");
    return new Promise((resolve, reject) => {
      gzip(data, (err, result) => (err ? reject(err) : resolve(result)));
    });
  }

  async decompress(data: Buffer): Promise<Buffer> {
    const { gunzip } = await import("zlib");
    return new Promise((resolve, reject) => {
      gunzip(data, (err, result) => (err ? reject(err) : resolve(result)));
    });
  }
}

class BrotliCompression implements CompressionStrategy {
  readonly name = "brotli";

  async compress(data: Buffer): Promise<Buffer> {
    const { brotliCompress } = await import("zlib");
    return new Promise((resolve, reject) => {
      brotliCompress(data, (err, result) => (err ? reject(err) : resolve(result)));
    });
  }

  async decompress(data: Buffer): Promise<Buffer> {
    const { brotliDecompress } = await import("zlib");
    return new Promise((resolve, reject) => {
      brotliDecompress(data, (err, result) => (err ? reject(err) : resolve(result)));
    });
  }
}

// Pricing strategies
class StandardPricing implements PricingStrategy {
  readonly name = "standard";

  calculate(items: CartItem[]): number {
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }
}

class DiscountPricing implements PricingStrategy {
  readonly name = "discount";

  constructor(private discountPercent: number) {}

  calculate(items: CartItem[]): number {
    const subtotal = items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );
    return subtotal * (1 - this.discountPercent / 100);
  }
}

class BulkPricing implements PricingStrategy {
  readonly name = "bulk";

  calculate(items: CartItem[]): number {
    return items.reduce((sum, item) => {
      const price = item.quantity >= 10
        ? item.price * 0.8
        : item.price;
      return sum + price * item.quantity;
    }, 0);
  }
}

// Validation strategies
class EmailValidation implements ValidationStrategy<string> {
  validate(value: string): ValidationResult {
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
    return {
      isValid,
      errors: isValid ? [] : ["Invalid email format"],
    };
  }
}

class PasswordValidation implements ValidationStrategy<string> {
  validate(value: string): ValidationResult {
    const errors: string[] = [];
    if (value.length < 8) errors.push("Must be at least 8 characters");
    if (!/[A-Z]/.test(value)) errors.push("Must contain uppercase letter");
    if (!/[a-z]/.test(value)) errors.push("Must contain lowercase letter");
    if (!/[0-9]/.test(value)) errors.push("Must contain number");
    return { isValid: errors.length === 0, errors };
  }
}
```

---

## Context Class

```typescript
// Context with strategy
class ShoppingCart {
  private items: CartItem[] = [];
  private pricingStrategy: PricingStrategy;

  constructor(strategy: PricingStrategy = new StandardPricing()) {
    this.pricingStrategy = strategy;
  }

  setPricingStrategy(strategy: PricingStrategy): void {
    this.pricingStrategy = strategy;
  }

  addItem(item: CartItem): void {
    this.items.push(item);
  }

  getTotal(): number {
    return this.pricingStrategy.calculate(this.items);
  }

  getPricingInfo(): string {
    return `Using ${this.pricingStrategy.name} pricing: $${this.getTotal().toFixed(2)}`;
  }
}

// Context with multiple strategies
class FileProcessor {
  private compressionStrategy: CompressionStrategy;
  private validationStrategy: ValidationStrategy<Buffer>;

  constructor(
    compression: CompressionStrategy,
    validation: ValidationStrategy<Buffer>
  ) {
    this.compressionStrategy = compression;
    this.validationStrategy = validation;
  }

  setCompression(strategy: CompressionStrategy): void {
    this.compressionStrategy = strategy;
  }

  setValidation(strategy: ValidationStrategy<Buffer>): void {
    this.validationStrategy = strategy;
  }

  async process(data: Buffer): Promise<Buffer> {
    const validation = this.validationStrategy.validate(data);
    if (!validation.isValid) {
      throw new Error(`Validation failed: ${validation.errors.join(", ")}`);
    }
    return this.compressionStrategy.compress(data);
  }
}

// Usage
const cart = new ShoppingCart(new StandardPricing());
cart.addItem({ name: "Widget", price: 10, quantity: 5 });
console.log(cart.getTotal()); // 50

cart.setPricingStrategy(new DiscountPricing(20));
console.log(cart.getTotal()); // 40 (20% off)

cart.setPricingStrategy(new BulkPricing());
console.log(cart.getTotal()); // 40 (no bulk discount for qty < 10)
```

---

## Strategy with Generics

```typescript
// Generic strategy pattern
interface Strategy<TInput, TOutput> {
  execute(input: TInput): TOutput;
  readonly name: string;
}

class Pipeline<TInput, TOutput> {
  private strategies: Array<Strategy<any, any>> = [];

  addStrategy<TNext>(strategy: Strategy<any, TNext>): Pipeline<TInput, TNext> {
    this.strategies.push(strategy);
    return this as unknown as Pipeline<TInput, TNext>;
  }

  execute(input: TInput): TOutput {
    let result: any = input;
    for (const strategy of this.strategies) {
      result = strategy.execute(result);
    }
    return result as TOutput;
  }
}

// Usage
const pipeline = new Pipeline<string, string>();
pipeline
  .addStrategy({ name: "trim", execute: (s: string) => s.trim() })
  .addStrategy({ name: "lower", execute: (s: string) => s.toLowerCase() })
  .addStrategy({ name: "slug", execute: (s: string) => s.replace(/\s+/g, "-") });

const result = pipeline.execute("  Hello World  ");
console.log(result); // "hello-world"

// Strategy with constraint
interface Comparable<T> {
  compareTo(other: T): number;
}

class ComparableSort<T extends Comparable<T>> implements SortStrategy<T> {
  sort(data: T[]): T[] {
    return [...data].sort((a, b) => a.compareTo(b));
  }
}

// Strategy with default implementation
abstract class BaseStrategy<TInput, TOutput> implements Strategy<TInput, TOutput> {
  abstract readonly name: string;
  abstract execute(input: TInput): TOutput;

  // Default behavior that can be overridden
  canHandle(input: TInput): boolean {
    return true;
  }
}
```

---

## Strategy vs Polymorphism

```typescript
// Strategy: Composition over inheritance
// Select algorithm at runtime

class PaymentProcessor {
  private strategy: PaymentStrategy;

  constructor(strategy: PaymentStrategy) {
    this.strategy = strategy;
  }

  async process(amount: number): Promise<PaymentResult> {
    return this.strategy.pay(amount);
  }

  // Change strategy at runtime!
  changeStrategy(strategy: PaymentStrategy): void {
    this.strategy = strategy;
  }
}

// Polymorphism: Inheritance
// Select behavior at compile time
abstract class PaymentMethod {
  abstract process(amount: number): Promise<PaymentResult>;
}

class CreditCard extends PaymentMethod {
  async process(amount: number): Promise<PaymentResult> {
    return { success: true };
  }
}

class PayPal extends PaymentMethod {
  async process(amount: number): Promise<PaymentResult> {
    return { success: true };
  }
}

// Strategy allows runtime switching, polymorphism is static
const processor = new PaymentProcessor(new CreditCardPayment());
processor.changeStrategy(new PayPalPayment()); // Runtime change!

// Polymorphism requires creating new instance
let method: PaymentMethod = new CreditCard();
method = new PayPal(); // Different variable assignment
```

---

## Runtime Strategy Selection

```typescript
// Dynamic strategy registry
class StrategyRegistry<TInput, TOutput> {
  private strategies = new Map<string, Strategy<TInput, TOutput>>();

  register(strategy: Strategy<TInput, TOutput>): void {
    this.strategies.set(strategy.name, strategy);
  }

  get(name: string): Strategy<TInput, TOutput> {
    const strategy = this.strategies.get(name);
    if (!strategy) throw new Error(`Unknown strategy: ${name}`);
    return strategy;
  }

  getAvailable(): string[] {
    return Array.from(this.strategies.keys());
  }
}

// Usage
const sortRegistry = new StrategyRegistry<number[], number[]>();
sortRegistry.register(new BubbleSort());
sortRegistry.register(new QuickSort());
sortRegistry.register(new MergeSort());

// Select strategy based on input
function selectSortStrategy(data: number[]): Strategy<number[], number[]> {
  if (data.length < 10) return sortRegistry.get("bubble");
  if (data.length < 1000) return sortRegistry.get("quick");
  return sortRegistry.get("merge");
}

// Strategy with configuration
interface StrategyConfig {
  type: string;
  options: Record<string, unknown>;
}

function createStrategyFromConfig<TInput, TOutput>(
  config: StrategyConfig
): Strategy<TInput, TOutput> {
  const strategies: Record<string, new (options: Record<string, unknown>) => Strategy<TInput, TOutput>> = {
    gzip: GzipCompression,
    brotli: BrotliCompression,
  };

  const StrategyClass = strategies[config.type];
  if (!StrategyClass) throw new Error(`Unknown strategy: ${config.type}`);
  return new StrategyClass(config.options);
}
```

---

## Real-World Examples

```typescript
// Logger with different transport strategies
interface LogTransport {
  readonly name: string;
  send(level: string, message: string): Promise<void>;
}

class ConsoleTransport implements LogTransport {
  readonly name = "console";
  async send(level: string, message: string): Promise<void> {
    console.log(`[${level}] ${message}`);
  }
}

class FileTransport implements LogTransport {
  readonly name = "file";
  constructor(private filePath: string) {}
  async send(level: string, message: string): Promise<void> {
    // Write to file
  }
}

class HTTPTransport implements LogTransport {
  readonly name = "http";
  constructor(private endpoint: string) {}
  async send(level: string, message: string): Promise<void> {
    await fetch(this.endpoint, {
      method: "POST",
      body: JSON.stringify({ level, message }),
    });
  }
}

class Logger {
  private transports: LogTransport[] = [];

  addTransport(transport: LogTransport): void {
    this.transports.push(transport);
  }

  async log(level: string, message: string): Promise<void> {
    await Promise.all(
      this.transports.map((t) => t.send(level, message))
    );
  }
}

// Cache with different eviction strategies
interface EvictionStrategy<T> {
  evict(cache: Map<string, T>): void;
  readonly name: string;
}

class LRUEviction<T> implements EvictionStrategy<T> {
  readonly name = "lru";
  private accessOrder: string[] = [];

  access(key: string): void {
    this.accessOrder = this.accessOrder.filter((k) => k !== key);
    this.accessOrder.push(key);
  }

  evict(cache: Map<string, T>): void {
    if (this.accessOrder.length > 0) {
      cache.delete(this.accessOrder.shift()!);
    }
  }
}

class TTL_eviction<T> implements EvictionStrategy<T> {
  readonly name = "ttl";
  private timestamps = new Map<string, number>();

  access(key: string): void {
    this.timestamps.set(key, Date.now());
  }

  evict(cache: Map<string, T>): void {
    const now = Date.now();
    for (const [key, time] of this.timestamps) {
      if (now - time > 60000) {
        cache.delete(key);
        this.timestamps.delete(key);
      }
    }
  }
}
```

---

## Interview Questions

1. **What is the Strategy pattern?**
   A behavioral pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime.

2. **When would you use Strategy over Polymorphism?**
   When you need to change algorithms at runtime, when you have many possible algorithms, or when you want to compose behaviors.

3. **What is the advantage of Strategy over conditional logic?**
   Avoids large switch statements, follows Open/Closed Principle, and makes adding new strategies easier.

4. **How do you make Strategy patterns type-safe in TypeScript?**
   Use interfaces for strategy contracts and generics for input/output types.

5. **What are real-world examples of the Strategy pattern?**
   Sorting algorithms, compression methods, payment processors, validation rules, caching eviction policies.

6. **What is the difference between Strategy and State patterns?**
   Strategy changes the algorithm used. State changes behavior based on internal state. Strategy is selected externally, State transitions internally.

7. **How do you handle strategy selection in TypeScript?**
   Use factory functions, registries, or configuration objects to select strategies at runtime.

8. **Can strategies have state?**
   Yes. Strategies can be stateful, maintaining configuration or context between invocations.

9. **What is the relationship between Strategy and Factory patterns?**
   Factory creates the appropriate strategy. Strategy defines the algorithm interface. They're often used together.

10. **How does the Strategy pattern relate to functional programming?**
    In FP, strategies are often just functions passed as arguments. TypeScript's function types make this natural.
