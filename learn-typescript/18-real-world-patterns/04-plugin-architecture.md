# Plugin Architecture in TypeScript

## Table of Contents

- [Plugin System with Types](#plugin-system-with-types)
- [Plugin Interface](#plugin-interface)
- [Plugin Registry](#plugin-registry)
- [Plugin Hooks](#plugin-hooks)
- [Typed Plugin API](#typed-plugin-api)
- [Extension Points](#extension-points)
- [Plugin Lifecycle](#plugin-lifecycle)
- [Real-World Plugin Examples](#real-world-plugin-examples)
- [Interview Questions](#interview-questions)

---

## Plugin System with Types

```typescript
// Core plugin interfaces
interface PluginMetadata {
  name: string;
  version: string;
  description: string;
  author: string;
  dependencies?: string[];
}

interface Plugin<TConfig = Record<string, unknown>> {
  metadata: PluginMetadata;
  initialize(context: PluginContext, config: TConfig): Promise<void>;
  destroy(): Promise<void>;
}

interface PluginContext {
  logger: Logger;
  config: AppConfig;
  services: ServiceRegistry;
  events: EventEmitter;
}

// Application that hosts plugins
class PluginHost {
  private plugins = new Map<string, Plugin>();
  private context: PluginContext;

  constructor(context: PluginContext) {
    this.context = context;
  }

  async loadPlugin<TConfig>(plugin: Plugin<TConfig>, config: TConfig): Promise<void> {
    // Check dependencies
    if (plugin.metadata.dependencies) {
      for (const dep of plugin.metadata.dependencies) {
        if (!this.plugins.has(dep)) {
          throw new Error(`Missing dependency: ${dep}`);
        }
      }
    }

    await plugin.initialize(this.context, config);
    this.plugins.set(plugin.metadata.name, plugin);
    this.context.logger.log(`Plugin loaded: ${plugin.metadata.name}`);
  }

  async unloadPlugin(name: string): Promise<void> {
    const plugin = this.plugins.get(name);
    if (plugin) {
      await plugin.destroy();
      this.plugins.delete(name);
      this.context.logger.log(`Plugin unloaded: ${name}`);
    }
  }

  getPlugin<T extends Plugin>(name: string): T | undefined {
    return this.plugins.get(name) as T | undefined;
  }

  async loadAll(): Promise<void> {
    for (const [, plugin] of this.plugins) {
      await plugin.destroy();
    }
    this.plugins.clear();
  }
}
```

---

## Plugin Interface

```typescript
// Extensible plugin interface with hooks
interface HookablePlugin<TConfig = Record<string, unknown>> extends Plugin<TConfig> {
  hooks?: PluginHooks;
}

interface PluginHooks {
  onInit?: () => Promise<void>;
  onStart?: () => Promise<void>;
  onStop?: () => Promise<void>;
  onConfigChange?: (config: Record<string, unknown>) => Promise<void>;
}

// Middleware-style plugin interface
interface MiddlewarePlugin<TContext = unknown> {
  metadata: PluginMetadata;
  middleware: (context: TContext, next: () => Promise<void>) => Promise<void>;
}

// Transformation plugin interface
interface TransformPlugin<TInput, TOutput> {
  metadata: PluginMetadata;
  transform(input: TInput): TOutput | Promise<TOutput>;
  canTransform(input: unknown): input is TInput;
}

// Validation plugin interface
interface ValidationPlugin<T> {
  metadata: PluginMetadata;
  validate(data: T): ValidationResult;
}

interface ValidationResult {
  valid: boolean;
  errors: Array<{
    field: string;
    message: string;
    code: string;
  }>;
}

// Storage plugin interface
interface StoragePlugin<T = unknown> {
  metadata: PluginMetadata;
  get(key: string): Promise<T | null>;
  set(key: string, value: T): Promise<void>;
  delete(key: string): Promise<void>;
  has(key: string): Promise<boolean>;
}
```

---

## Plugin Registry

```typescript
// Type-safe plugin registry
class PluginRegistry<TPluginMap extends Record<string, Plugin>> {
  private plugins = new Map<string, Plugin>();
  private categories = new Map<string, Set<string>>();

  register<K extends keyof TPluginMap & string>(
    category: K,
    plugin: TPluginMap[K]
  ): void {
    this.plugins.set(plugin.metadata.name, plugin);

    if (!this.categories.has(category)) {
      this.categories.set(category, new Set());
    }
    this.categories.get(category)!.add(plugin.metadata.name);
  }

  get<K extends keyof TPluginMap & string>(
    name: K
  ): TPluginMap[K] | undefined {
    return this.plugins.get(name) as TPluginMap[K] | undefined;
  }

  getByCategory<K extends keyof TPluginMap & string>(
    category: K
  ): Array<TPluginMap[K]> {
    const names = this.categories.get(category) ?? new Set();
    return Array.from(names)
      .map((name) => this.plugins.get(name) as TPluginMap[K])
      .filter(Boolean);
  }

  has(name: string): boolean {
    return this.plugins.has(name);
  }

  listAll(): PluginMetadata[] {
    return Array.from(this.plugins.values()).map((p) => p.metadata);
  }
}

// Usage
interface MyPluginMap {
  auth: AuthPlugin;
  storage: StoragePlugin;
  analytics: AnalyticsPlugin;
}

const registry = new PluginRegistry<MyPluginMap>();
registry.register("auth", new JWTAuthPlugin());
registry.register("storage", new RedisStoragePlugin());

const authPlugin = registry.get("auth"); // AuthPlugin type
const storagePlugins = registry.getByCategory("storage"); // StoragePlugin[]
```

---

## Plugin Hooks

```typescript
// Event-based plugin hooks
class HookManager {
  private hooks = new Map<string, Set<Function>>();

  registerHook<T>(name: string, handler: (data: T) => Promise<T | void>): () => void {
    if (!this.hooks.has(name)) {
      this.hooks.set(name, new Set());
    }
    this.hooks.get(name)!.add(handler);

    return () => {
      this.hooks.get(name)?.delete(handler);
    };
  }

  async executeHook<T>(name: string, data: T): Promise<T> {
    const handlers = this.hooks.get(name);
    if (!handlers) return data;

    let result = data;
    for (const handler of handlers) {
      const handlerResult = await (handler as (data: T) => Promise<T | void>)(result);
      if (handlerResult !== undefined) {
        result = handlerResult;
      }
    }

    return result;
  }
}

// Plugin with hooks
class AnalyticsPlugin implements Plugin {
  metadata: PluginMetadata = {
    name: "analytics",
    version: "1.0.0",
    description: "Analytics tracking",
    author: "Me",
  };

  async initialize(context: PluginContext): Promise<void> {
    // Register hooks
    context.events.onHook("user:created", async (user) => {
      await this.trackEvent("user_created", { userId: user.id });
      return user;
    });

    context.events.onHook("page:loaded", async (page) => {
      await this.trackEvent("page_view", { path: page.path });
      return page;
    });
  }

  async destroy(): Promise<void> {
    // Cleanup
  }

  private async trackEvent(event: string, data: Record<string, unknown>): Promise<void> {
    console.log(`[Analytics] ${event}:`, data);
  }
}

// Usage
const hooks = new HookManager();

hooks.registerHook("request:before", async (req) => {
  req.headers["x-request-id"] = crypto.randomUUID();
  return req;
});

hooks.registerHook("response:after", async (res) => {
  console.log(`Response: ${res.status}`);
  return res;
});
```

---

## Typed Plugin API

```typescript
// Type-safe plugin API
interface PluginAPI<TContext, TEvents extends Record<string, unknown>> {
  context: TContext;
  registerEvent<K extends keyof TEvents>(
    event: K,
    handler: (data: TEvents[K]) => Promise<TEvents[K] | void>
  ): () => void;
  emitEvent<K extends keyof TEvents>(event: K, data: TEvents[K]): Promise<TEvents[K]>;
  getConfig(): Record<string, unknown>;
}

// Plugin with typed API
class TypedPlugin<TConfig, TEvents extends Record<string, unknown>> {
  metadata: PluginMetadata;
  private api?: PluginAPI<any, TEvents>;

  constructor(metadata: PluginMetadata) {
    this.metadata = metadata;
  }

  async initialize(api: PluginAPI<unknown, TEvents>, config: TConfig): Promise<void> {
    this.api = api;

    // Register event handlers
    this.setupEvents(api, config);
  }

  protected abstract setupEvents(
    api: PluginAPI<unknown, TEvents>,
    config: TConfig
  ): Promise<void>;
}

// Usage with specific types
interface AppEvents {
  "user:created": { userId: string; email: string };
  "order:placed": { orderId: string; amount: number };
  "payment:received": { transactionId: string; amount: number };
}

class EmailNotificationPlugin extends TypedPlugin<
  { templates: Record<string, string> },
  AppEvents
> {
  metadata: PluginMetadata = {
    name: "email-notification",
    version: "1.0.0",
    description: "Send email notifications",
    author: "Me",
  };

  protected async setupEvents(
    api: PluginAPI<unknown, AppEvents>,
    config: { templates: Record<string, string> }
  ): Promise<void> {
    api.registerEvent("user:created", async (data) => {
      await this.sendEmail(data.email, "welcome", { userId: data.userId });
      return data;
    });

    api.registerEvent("order:placed", async (data) => {
      await this.sendEmail("admin@example.com", "order", { orderId: data.orderId });
      return data;
    });
  }

  private async sendEmail(
    to: string,
    template: string,
    data: Record<string, unknown>
  ): Promise<void> {
    console.log(`Sending ${template} email to ${to}`, data);
  }
}
```

---

## Extension Points

```typescript
// Define extension points for plugins
interface ExtensionPoint<T> {
  name: string;
  execute(data: T): Promise<T>;
  registerHandler(handler: (data: T) => Promise<T | void>): () => void;
}

function createExtensionPoint<T>(name: string): ExtensionPoint<T> {
  const handlers: Array<(data: T) => Promise<T | void>> = [];

  return {
    name,

    registerHandler(handler: (data: T) => Promise<T | void>): () => void {
      handlers.push(handler);
      return () => {
        const index = handlers.indexOf(handler);
        if (index > -1) handlers.splice(index, 1);
      };
    },

    async execute(data: T): Promise<T> {
      let result = data;
      for (const handler of handlers) {
        const handlerResult = await handler(result);
        if (handlerResult !== undefined) {
          result = handlerResult;
        }
      }
      return result;
    },
  };
}

// Application with extension points
class Application {
  extensionPoints = {
    "transform:user": createExtensionPoint<User>("transform:user"),
    "validate:order": createExtensionPoint<Order>("validate:order"),
    "render:page": createExtensionPoint<PageContext>("render:page"),
  };

  async processUser(user: User): Promise<User> {
    return this.extensionPoints["transform:user"].execute(user);
  }

  async validateOrder(order: Order): Promise<Order> {
    return this.extensionPoints["validate:order"].execute(order);
  }

  async renderPage(context: PageContext): Promise<string> {
    return this.extensionPoints["render:page"].execute(context) as Promise<string>;
  }
}

// Plugin registering at extension points
class ValidationPlugin implements Plugin {
  metadata: PluginMetadata = {
    name: "order-validation",
    version: "1.0.0",
    description: "Validates orders",
    author: "Me",
  };

  async initialize(context: PluginContext): Promise<void> {
    const app = context.services.get<Application>("app");

    app.extensionPoints["validate:order"].registerHandler(async (order) => {
      if (order.items.length === 0) {
        throw new Error("Order must have at least one item");
      }
      if (order.total < 0) {
        throw new Error("Order total cannot be negative");
      }
      return order;
    });
  }

  async destroy(): Promise<void> {}
}
```

---

## Plugin Lifecycle

```typescript
// Plugin lifecycle management
enum PluginState {
  UNLOADED = "unloaded",
  LOADING = "loading",
  LOADED = "loaded",
  ACTIVE = "active",
  ERROR = "error",
  DISABLED = "disabled",
}

class PluginLifecycleManager {
  private states = new Map<string, PluginState>();
  private lifecycle = new Map<string, {
    onInit?: () => Promise<void>;
    onStart?: () => Promise<void>;
    onStop?: () => Promise<void>;
    onUnload?: () => Promise<void>;
  }>();

  register(name: string, hooks: PluginLifecycleManager["lifecycle"] extends Map<string, infer V> ? V : never): void {
    this.lifecycle.set(name, hooks);
    this.states.set(name, PluginState.UNLOADED);
  }

  async load(name: string): Promise<void> {
    this.states.set(name, PluginState.LOADING);
    try {
      await this.lifecycle.get(name)?.onInit?.();
      this.states.set(name, PluginState.LOADED);
    } catch (error) {
      this.states.set(name, PluginState.ERROR);
      throw error;
    }
  }

  async start(name: string): Promise<void> {
    if (this.states.get(name) !== PluginState.LOADED) {
      throw new Error(`Plugin ${name} must be loaded first`);
    }
    await this.lifecycle.get(name)?.onStart?.();
    this.states.set(name, PluginState.ACTIVE);
  }

  async stop(name: string): Promise<void> {
    if (this.states.get(name) !== PluginState.ACTIVE) {
      throw new Error(`Plugin ${name} must be active to stop`);
    }
    await this.lifecycle.get(name)?.onStop?.();
    this.states.set(name, PluginState.LOADED);
  }

  async unload(name: string): Promise<void> {
    await this.lifecycle.get(name)?.onUnload?.();
    this.states.set(name, PluginState.UNLOADED);
    this.lifecycle.delete(name);
    this.states.delete(name);
  }

  getState(name: string): PluginState {
    return this.states.get(name) ?? PluginState.UNLOADED;
  }

  async loadAll(): Promise<void> {
    for (const [name] of this.lifecycle) {
      await this.load(name);
      await this.start(name);
    }
  }

  async stopAll(): Promise<void> {
    for (const [name, state] of this.states) {
      if (state === PluginState.ACTIVE) {
        await this.stop(name);
      }
    }
  }
}
```

---

## Real-World Plugin Examples

```typescript
// ESLint-style plugin system
interface LintRule {
  name: string;
  description: string;
  severity: "error" | "warning" | "info";
  check(node: ASTNode): LintResult[];
}

interface LintPlugin {
  metadata: PluginMetadata;
  rules: LintRule[];
  configs?: Record<string, { rules: Record<string, unknown> }>;
}

class LintEngine {
  private plugins = new Map<string, LintPlugin>();

  registerPlugin(plugin: LintPlugin): void {
    this.plugins.set(plugin.metadata.name, plugin);
  }

  lint(code: string): LintResult[] {
    const ast = parse(code);
    const results: LintResult[] = [];

    for (const [, plugin] of this.plugins) {
      for (const rule of plugin.rules) {
        for (const node of ast.nodes) {
          results.push(...rule.check(node));
        }
      }
    }

    return results;
  }
}

// Webpack-style plugin system
interface CompilerPlugin {
  name: string;
  apply(compiler: Compiler): void;
}

interface Compiler {
  hooks: {
    beforeCompile: AsyncSeriesHook<CompilationParams>;
    compile: AsyncSeriesHook<Compilation>;
    emit: AsyncSeriesHook<EmittedAsset>;
    done: AsyncSeriesHook<Stats>;
  };
}

class AsyncSeriesHook<T> {
  private taps: Array<(data: T) => Promise<T | void>> = [];

  tap(name: string, handler: (data: T) => Promise<T | void>): void {
    this.taps.push(handler);
  }

  async promise(data: T): Promise<T> {
    let result = data;
    for (const tap of this.taps) {
      const tapResult = await tap(result);
      if (tapResult !== undefined) result = tapResult;
    }
    return result;
  }
}

// VSCode extension-style plugin
interface Extension<TAPI> {
  activate(context: ExtensionContext): TAPI;
  deactivate(): void | Promise<void>;
}

interface ExtensionContext {
  subscriptions: { dispose(): void }[];
  workspaceState: Memento;
  globalState: Memento;
}
```

---

## Interview Questions

1. **What is a plugin architecture?**
   A system design pattern that allows extending functionality through independently developed modules (plugins) without modifying the core application.

2. **What is the difference between plugins and middleware?**
   Middleware processes requests in a pipeline. Plugins extend the entire application with hooks, events, and new functionality.

3. **How do you define plugin interfaces in TypeScript?**
   Use interfaces for plugin contracts, generics for configuration types, and event maps for typed hooks.

4. **What is a plugin registry?**
   A centralized system for registering, discovering, and managing plugins.

5. **How do you handle plugin dependencies?**
   Check dependency versions during plugin loading and load plugins in dependency order.

6. **What are plugin hooks?**
   Extension points where plugins can inject behavior before, after, or around core application operations.

7. **How do you ensure plugin isolation?**
   Use separate contexts, sandboxing, or process isolation to prevent plugins from affecting each other.

8. **What is the plugin lifecycle?**
   The sequence of states a plugin goes through: loading, initialization, activation, deactivation, and unloading.

9. **How do you handle plugin configuration?**
   Use typed configuration interfaces, validation, and provide default values.

10. **What are real-world examples of plugin architectures?**
    ESLint, Webpack, VSCode extensions, WordPress plugins, browser extensions, and CMS systems.
