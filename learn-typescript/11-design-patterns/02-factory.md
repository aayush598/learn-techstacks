# Factory Pattern in TypeScript

## Table of Contents

- [Simple Factory](#simple-factory)
- [Factory Method](#factory-method)
- [Abstract Factory](#abstract-factory)
- [Typed Factory Functions](#typed-factory-functions)
- [Generic Factories](#generic-factories)
- [Factory with Configuration](#factory-with-configuration)
- [Factory vs Builder](#factory-vs-builder)
- [Factory in Dependency Injection](#factory-in-dependency-injection)
- [Interview Questions](#interview-questions)

---

## Simple Factory

A factory function or class method that creates objects without exposing the creation logic.

```typescript
// Basic factory
interface Notification {
  send(message: string): void;
}

class EmailNotification implements Notification {
  send(message: string): void {
    console.log(`Email: ${message}`);
  }
}

class SMSNotification implements Notification {
  send(message: string): void {
    console.log(`SMS: ${message}`);
  }
}

class PushNotification implements Notification {
  send(message: string): void {
    console.log(`Push: ${message}`);
  }
}

// Simple factory function
function createNotification(type: "email" | "sms" | "push"): Notification {
  switch (type) {
    case "email": return new EmailNotification();
    case "sms": return new SMSNotification();
    case "push": return new PushNotification();
    default: throw new Error(`Unknown notification type: ${type}`);
  }
}

// Usage
const notifier = createNotification("email");
notifier.send("Hello!");

// Factory class
class NotificationFactory {
  static create(type: "email" | "sms" | "push"): Notification {
    switch (type) {
      case "email": return new EmailNotification();
      case "sms": return new SMSNotification();
      case "push": return new PushNotification();
      default: throw new Error(`Unknown type: ${type}`);
    }
  }
}

const notifier2 = NotificationFactory.create("sms");
```

---

## Factory Method

Defines an interface for creating objects but lets subclasses decide which class to instantiate.

```typescript
// Abstract creator
abstract class LoggerFactory {
  abstract createLogger(): Logger;

  writeLog(message: string): void {
    const logger = this.createLogger();
    logger.log(message);
  }
}

// Concrete creators
class ConsoleLoggerFactory extends LoggerFactory {
  createLogger(): Logger {
    return new ConsoleLogger();
  }
}

class FileLoggerFactory extends LoggerFactory {
  createLogger(): Logger {
    return new FileLogger("/var/log/app.log");
  }
}

class DatabaseLoggerFactory extends LoggerFactory {
  createLogger(): Logger {
    return new DatabaseLogger("postgresql://localhost/logs");
  }
}

// Products
interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string): void {
    console.log(`[Console] ${message}`);
  }
}

class FileLogger implements Logger {
  constructor(private filePath: string) {}
  log(message: string): void {
    console.log(`[File:${this.filePath}] ${message}`);
  }
}

class DatabaseLogger implements Logger {
  constructor(private connectionString: string) {}
  log(message: string): void {
    console.log(`[DB:${this.connectionString}] ${message}`);
  }
}

// Usage
function configureLogger(env: string): LoggerFactory {
  switch (env) {
    case "development": return new ConsoleLoggerFactory();
    case "production": return new FileLoggerFactory();
    case "test": return new DatabaseLoggerFactory();
    default: return new ConsoleLoggerFactory();
  }
}

const factory = configureLogger(process.env.NODE_ENV ?? "development");
factory.writeLog("Application started");
```

---

## Abstract Factory

Creates families of related objects without specifying their concrete classes.

```typescript
// Abstract products
interface Button {
  render(): string;
  onClick(handler: () => void): void;
}

interface Input {
  render(): string;
  getValue(): string;
}

interface Modal {
  render(): string;
  open(): void;
  close(): void;
}

// Concrete products - Material Design
class MaterialButton implements Button {
  render(): string {
    return '<button class="material-btn">';
  }
  onClick(handler: () => void): void {
    console.log("Material button clicked");
  }
}

class MaterialInput implements Input {
  render(): string {
    return '<input class="material-input">';
  }
  getValue(): string {
    return "";
  }
}

class MaterialModal implements Modal {
  render(): string {
    return '<div class="material-modal">';
  }
  open(): void {
    console.log("Material modal opened");
  }
  close(): void {
    console.log("Material modal closed");
  }
}

// Concrete products - Bootstrap
class BootstrapButton implements Button {
  render(): string {
    return '<button class="btn btn-primary">';
  }
  onClick(handler: () => void): void {
    console.log("Bootstrap button clicked");
  }
}

class BootstrapInput implements Input {
  render(): string {
    return '<input class="form-control">';
  }
  getValue(): string {
    return "";
  }
}

class BootstrapModal implements Modal {
  render(): string {
    return '<div class="modal">';
  }
  open(): void {
    console.log("Bootstrap modal opened");
  }
  close(): void {
    console.log("Bootstrap modal closed");
  }
}

// Abstract factory
interface UIFactory {
  createButton(): Button;
  createInput(): Input;
  createModal(): Modal;
}

// Concrete factories
class MaterialUIFactory implements UIFactory {
  createButton(): Button {
    return new MaterialButton();
  }
  createInput(): Input {
    return new MaterialInput();
  }
  createModal(): Modal {
    return new MaterialModal();
  }
}

class BootstrapUIFactory implements UIFactory {
  createButton(): Button {
    return new BootstrapButton();
  }
  createInput(): Input {
    return new BootstrapInput();
  }
  createModal(): Modal {
    return new BootstrapModal();
  }
}

// Client code
function buildForm(factory: UIFactory): string {
  const button = factory.createButton();
  const input = factory.createInput();
  return `${input.render()}\n${button.render()}`;
}

// Usage
const materialUI = new MaterialUIFactory();
const bootstrapUI = new BootstrapUIFactory();

console.log(buildForm(materialUI));
console.log(buildForm(bootstrapUI));
```

---

## Typed Factory Functions

```typescript
// Factory with discriminated union input
interface ShapeConfig {
  type: "circle";
  radius: number;
} | {
  type: "rectangle";
  width: number;
  height: number;
} | {
  type: "triangle";
  base: number;
  height: number;
};

interface Shape {
  type: string;
  area(): number;
  perimeter(): number;
}

class Circle implements Shape {
  type = "circle" as const;
  constructor(private radius: number) {}
  area(): number { return Math.PI * this.radius ** 2; }
  perimeter(): number { return 2 * Math.PI * this.radius; }
}

class Rectangle implements Shape {
  type = "rectangle" as const;
  constructor(private width: number, private height: number) {}
  area(): number { return this.width * this.height; }
  perimeter(): number { return 2 * (this.width + this.height); }
}

class Triangle implements Shape {
  type = "triangle" as const;
  constructor(private base: number, private height: number) {}
  area(): number { return 0.5 * this.base * this.height; }
  perimeter(): number { return this.base + this.height * 2; } // Simplified
}

// Type-safe factory
function createShape(config: ShapeConfig): Shape {
  switch (config.type) {
    case "circle":
      return new Circle(config.radius); // config is narrowed
    case "rectangle":
      return new Rectangle(config.width, config.height);
    case "triangle":
      return new Triangle(config.base, config.height);
    default:
      const _exhaustive: never = config;
      return _exhaustive;
  }
}

// Factory with conditional types
type InstanceOf<T> = T extends new (...args: any[]) => infer R ? R : never;

class Registry<T extends Record<string, new (...args: any[]) => any>> {
  private creators = new Map<string, new (...args: any[]) => any>();

  register<K extends keyof T>(name: K, creator: T[K]): void {
    this.creators.set(name as string, creator);
  }

  create<K extends keyof T>(
    name: K,
    ...args: ConstructorParameters<T[K]>
  ): InstanceOf<T[K]> {
    const creator = this.creators.get(name as string);
    if (!creator) throw new Error(`Unknown type: ${String(name)}`);
    return new creator(...args) as InstanceOf<T[K]>;
  }
}

// Usage
const shapeRegistry = new Registry<{
  circle: typeof Circle;
  rectangle: typeof Rectangle;
}>();

shapeRegistry.register("circle", Circle);
shapeRegistry.register("rectangle", Rectangle);

const circle = shapeRegistry.create("circle", 5); // Circle
const rect = shapeRegistry.create("rectangle", 10, 20); // Rectangle
```

---

## Generic Factories

```typescript
// Generic factory with type inference
interface Factory<T, TConfig> {
  create(config: TConfig): T;
}

// Product interface
interface Product {
  id: string;
  name: string;
}

// Generic factory implementation
class GenericFactory<T extends Product, TConfig> implements Factory<T, TConfig> {
  private creators = new Map<string, (config: TConfig) => T>();

  register(type: string, creator: (config: TConfig) => T): void {
    this.creators.set(type, creator);
  }

  create(type: string, config: TConfig): T {
    const creator = this.creators.get(type);
    if (!creator) throw new Error(`Unknown type: ${type}`);
    return creator(config);
  }
}

// Usage
interface UserConfig {
  name: string;
  email: string;
}

interface User extends Product {
  name: string;
  email: string;
}

const userFactory = new GenericFactory<User, UserConfig>();
userFactory.register("admin", (config) => ({
  id: crypto.randomUUID(),
  ...config,
  role: "admin",
}));
userFactory.register("user", (config) => ({
  id: crypto.randomUUID(),
  ...config,
  role: "user",
}));

const admin = userFactory.create("admin", { name: "Alice", email: "alice@example.com" });

// Async factory
interface AsyncFactory<T> {
  create(): Promise<T>;
}

class AsyncDatabaseFactory implements AsyncFactory<Database> {
  async create(): Promise<Database> {
    const db = new Database();
    await db.connect();
    return db;
  }
}
```

---

## Factory with Configuration

```typescript
// Configuration-driven factory
interface ServiceConfig {
  type: string;
  options: Record<string, unknown>;
}

class ServiceFactory {
  private static registry = new Map<string, new (options: Record<string, unknown>) => unknown>();

  static register(type: string, creator: new (options: Record<string, unknown>) => unknown): void {
    ServiceFactory.registry.set(type, creator);
  }

  static create<T>(config: ServiceConfig): T {
    const Creator = ServiceFactory.registry.get(config.type);
    if (!Creator) throw new Error(`Unknown service type: ${config.type}`);
    return new Creator(config.options) as T;
  }
}

// Register services
ServiceFactory.register("cache", RedisCache);
ServiceFactory.register("queue", RabbitMQQueue);
ServiceFactory.register("storage", S3Storage);

// Create from config
const config: ServiceConfig[] = [
  { type: "cache", options: { host: "localhost", port: 6379 } },
  { type: "queue", options: { url: "amqp://localhost" } },
  { type: "storage", options: { bucket: "my-bucket" } },
];

const services = config.map((c) => ServiceFactory.create(c));

// Factory with preset configurations
interface Preset {
  name: string;
  config: Record<string, unknown>;
}

class ConfigurableFactory<T> {
  private presets = new Map<string, Record<string, unknown>>();
  private creator: (config: Record<string, unknown>) => T;

  constructor(creator: (config: Record<string, unknown>) => T) {
    this.creator = creator;
  }

  registerPreset(name: string, config: Record<string, unknown>): void {
    this.presets.set(name, config);
  }

  create(presetName: string, overrides?: Partial<Record<string, unknown>>): T {
    const preset = this.presets.get(presetName);
    if (!preset) throw new Error(`Unknown preset: ${presetName}`);
    return this.creator({ ...preset, ...overrides });
  }
}
```

---

## Factory vs Builder

```typescript
// Factory: Creates objects, often choosing the implementation
// Builder: Constructs complex objects step by step

// Factory
class ButtonFactory {
  static create(variant: "primary" | "danger"): Button {
    return variant === "primary"
      ? new PrimaryButton()
      : new DangerButton();
  }
}

// Builder
class ButtonBuilder {
  private text = "";
  private variant: "primary" | "danger" = "primary";
  private size: "sm" | "md" | "lg" = "md";
  private disabled = false;

  setText(text: string): this {
    this.text = text;
    return this;
  }

  setVariant(variant: "primary" | "danger"): this {
    this.variant = variant;
    return this;
  }

  setSize(size: "sm" | "md" | "lg"): this {
    this.size = size;
    return this;
  }

  setDisabled(disabled: boolean): this {
    this.disabled = disabled;
    return this;
  }

  build(): Button {
    return new Button(this.text, this.variant, this.size, this.disabled);
  }
}

// Usage
// Factory: Quick creation
const btn1 = ButtonFactory.create("primary");

// Builder: Complex creation with options
const btn2 = new ButtonBuilder()
  .setText("Submit")
  .setVariant("primary")
  .setSize("lg")
  .setDisabled(false)
  .build();
```

---

## Factory in Dependency Injection

```typescript
// Factory pattern in DI containers
interface ServiceFactory<T> {
  create(): T;
}

class DIContainer {
  private factories = new Map<string, ServiceFactory<any>>();
  private singletons = new Map<string, any>();

  register<T>(name: string, factory: ServiceFactory<T>): void {
    this.factories.set(name, factory);
  }

  registerSingleton<T>(name: string, factory: ServiceFactory<T>): void {
    this.factories.set(name, {
      create: () => {
        if (!this.singletons.has(name)) {
          this.singletons.set(name, factory.create());
        }
        return this.singletons.get(name);
      },
    });
  }

  resolve<T>(name: string): T {
    const factory = this.factories.get(name);
    if (!factory) throw new Error(`Service ${name} not registered`);
    return factory.create();
  }
}

// Usage
const container = new DIContainer();

container.register("logger", {
  create: () => new ConsoleLogger(),
});

container.registerSingleton("database", {
  create: () => new Database("connection-string"),
});

const logger = container.resolve<Logger>("logger");
const db = container.resolve<Database>("database");
```

---

## Interview Questions

1. **What is the Factory pattern?**
   A creational pattern that provides an interface for creating objects without specifying their concrete class.

2. **What is the difference between Simple Factory, Factory Method, and Abstract Factory?**
   Simple Factory uses a single method/class. Factory Method defines an interface for creation in subclasses. Abstract Factory creates families of related objects.

3. **When would you use a Factory over a Constructor?**
   When object creation is complex, when you need to return different types, or when you want to encapsulate creation logic.

4. **What is the advantage of using factories with TypeScript?**
   Better type safety through generics, discriminated unions, and conditional types.

5. **How does the Factory pattern relate to Dependency Injection?**
   Factories are often used in DI containers to create and manage object lifecycles.

6. **What is the Abstract Factory pattern?**
   A pattern that provides an interface for creating families of related objects without specifying their concrete classes.

7. **When should you prefer Factory Method over Abstract Factory?**
   When you only need one product type, or when the creation logic is simple enough for a single method.

8. **What is a factory function in TypeScript?**
   A function that returns a new object, often used as an alternative to classes for simpler object creation.

9. **How do you make a factory type-safe?**
   Use discriminated unions for input types, generics for return types, and exhaustive switch statements.

10. **What is the difference between Factory and Builder patterns?**
    Factory creates objects (often choosing the implementation). Builder constructs complex objects step by step.
