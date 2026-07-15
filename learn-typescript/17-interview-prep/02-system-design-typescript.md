# System Design with TypeScript Focus

## 6 System Design Questions with TypeScript Implementation

---

## 1. Design a Type-Safe API Client

### Requirements

- Type-safe HTTP methods (GET, POST, PUT, DELETE)
- Automatic request/response typing
- Interceptors for auth, logging, error handling
- Support for middleware
- Abort/cancel support

### Architecture

```
┌─────────────────────────────────────────────────┐
│                  ApiClient                       │
│  ┌───────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Intercept │  │ Request  │  │   Response   │  │
│  │   ors     │→ │ Builder  │→ │   Parser     │  │
│  └───────────┘  └──────────┘  └──────────────┘  │
│       ↑                              ↓           │
│  ┌───────────┐               ┌──────────────┐    │
│  │   Auth    │               │    Cache     │    │
│  │ Interceptor│               │   Interceptor│    │
│  └───────────┘               └──────────────┘    │
└─────────────────────────────────────────────────┘
```

### Implementation

```typescript
// types.ts
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

interface ApiResponse<T> {
  data: T;
  status: number;
  headers: Record<string, string>;
}

interface ApiError {
  message: string;
  status: number;
  code?: string;
}

interface RequestConfig {
  headers?: Record<string, string>;
  params?: Record<string, any>;
  body?: any;
  signal?: AbortSignal;
  timeout?: number;
}

interface Interceptor {
  request?: (config: RequestConfig) => RequestConfig | Promise<RequestConfig>;
  response?: (response: ApiResponse<any>) => ApiResponse<any> | Promise<ApiResponse<any>>;
  error?: (error: ApiError) => Promise<never>;
}

// api-client.ts
class ApiClient {
  private baseURL: string;
  private interceptors: Interceptor[] = [];

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  addInterceptor(interceptor: Interceptor): void {
    this.interceptors.push(interceptor);
  }

  async request<T>(
    method: HttpMethod,
    url: string,
    config: RequestConfig = {}
  ): Promise<ApiResponse<T>> {
    let requestConfig = { ...config, method };

    // Apply request interceptors
    for (const interceptor of this.interceptors) {
      if (interceptor.request) {
        requestConfig = await interceptor.request(requestConfig);
      }
    }

    const fullURL = new URL(`${this.baseURL}${url}`);
    if (requestConfig.params) {
      Object.entries(requestConfig.params).forEach(([key, value]) => {
        fullURL.searchParams.set(key, String(value));
      });
    }

    try {
      const response = await fetch(fullURL.toString(), {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...requestConfig.headers,
        },
        body: requestConfig.body ? JSON.stringify(requestConfig.body) : undefined,
        signal: requestConfig.signal,
      });

      const data = await response.json();
      let apiResponse: ApiResponse<T> = {
        data,
        status: response.status,
        headers: Object.fromEntries(response.headers.entries()),
      };

      // Apply response interceptors
      for (const interceptor of this.interceptors) {
        if (interceptor.response) {
          apiResponse = await interceptor.response(apiResponse);
        }
      }

      return apiResponse;
    } catch (error) {
      const apiError: ApiError = {
        message: (error as Error).message,
        status: 0,
      };

      for (const interceptor of this.interceptors) {
        if (interceptor.error) {
          await interceptor.error(apiError);
        }
      }

      throw apiError;
    }
  }

  get<T>(url: string, config?: RequestConfig): Promise<ApiResponse<T>> {
    return this.request('GET', url, config);
  }

  post<T>(url: string, body?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
    return this.request('POST', url, { ...config, body });
  }

  put<T>(url: string, body?: any, config?: RequestConfig): Promise<ApiResponse<T>> {
    return this.request('PUT', url, { ...config, body });
  }

  delete<T>(url: string, config?: RequestConfig): Promise<ApiResponse<T>> {
    return this.request('DELETE', url, config);
  }
}

// typed-client.ts
interface ApiSchema {
  'GET /users': { response: User[]; params: { page?: number } };
  'POST /users': { response: User; body: CreateUserDTO };
  'GET /users/:id': { response: User; params: { id: string } };
  'PUT /users/:id': { response: User; body: Partial<User> };
  'DELETE /users/:id': { response: void };
}

class TypedApiClient {
  private client: ApiClient;

  constructor(baseURL: string) {
    this.client = new ApiClient(baseURL);
  }

  async get<K extends keyof ApiSchema & `GET ${string}`>(
    endpoint: K,
    config?: Omit<ApiSchema[K], 'response'>
  ): Promise<ApiResponse<ApiSchema[K]['response']>> {
    const [method, path] = (endpoint as string).split(' ');
    return this.client.get(path, config);
  }

  async post<K extends keyof ApiSchema & `POST ${string}`>(
    endpoint: K,
    body?: ApiSchema[K] extends { body: infer B } ? B : never
  ): Promise<ApiResponse<ApiSchema[K]['response']>> {
    const [method, path] = (endpoint as string).split(' ');
    return this.client.post(path, body);
  }
}

// Usage
const api = new TypedApiClient('https://api.example.com');
const users = await api.get('GET /users', { params: { page: 1 } });
// users.data: User[]
```

---

## 2. Design a Type-Safe State Management System

### Requirements

- Type-safe state access and updates
- Middleware support
- Subscription system
- Immutable updates
- DevTools integration

### Implementation

```typescript
// store.ts
type State = Record<string, any>;
type Reducer<S, A> = (state: S, action: A) => S;
type Middleware<S> = (store: StoreApi<S>) => (next: (action: any) => any) => (action: any) => any;

interface StoreApi<S extends State> {
  getState: () => Readonly<S>;
  dispatch: (action: any) => void;
  subscribe: (listener: () => void) => () => void;
  getReducer: () => Reducer<S, any>;
}

class Store<S extends State> {
  private state: S;
  private listeners = new Set<() => void>();
  private reducer: Reducer<S, any>;
  private middlewares: Middleware<S>[] = [];

  constructor(reducer: Reducer<S, any>, initialState: S) {
    this.reducer = reducer;
    this.state = initialState;
  }

  use(middleware: Middleware<S>): void {
    this.middlewares.push(middleware);
  }

  getState(): Readonly<S> {
    return Object.freeze({ ...this.state });
  }

  dispatch(action: any): void {
    this.state = this.reducer(this.state, action);
    this.listeners.forEach(listener => listener());
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
}

// Example usage
interface AppState {
  user: User | null;
  todos: Todo[];
  loading: boolean;
}

type AppAction =
  | { type: 'SET_USER'; payload: User }
  | { type: 'ADD_TODO'; payload: Todo }
  | { type: 'SET_LOADING'; payload: boolean };

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'ADD_TODO':
      return { ...state, todos: [...state.todos, action.payload] };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    default:
      return state;
  }
}

const store = new Store(appReducer, {
  user: null,
  todos: [],
  loading: false,
});

store.subscribe(() => {
  console.log('State changed:', store.getState());
});

store.dispatch({ type: 'SET_USER', payload: { id: '1', name: 'Alice' } });
```

---

## 3. Design a Plugin Architecture

### Requirements

- Plugin registration and lifecycle
- Type-safe plugin API
- Plugin dependencies
- Plugin hooks
- Hot reloading support

### Implementation

```typescript
// plugin-system.ts
interface Plugin<T = any> {
  name: string;
  version: string;
  dependencies?: string[];
  setup: (api: PluginApi) => T | Promise<T>;
  destroy?: () => void | Promise<void>;
}

interface PluginApi {
  registerHook: <T>(name: string, handler: (data: T) => T | Promise<T>) => void;
  emitHook: <T>(name: string, data: T) => Promise<T>;
  getConfig: <T>(key: string) => T | undefined;
  setConfig: (key: string, value: any) => void;
}

class PluginManager {
  private plugins = new Map<string, Plugin>();
  private hooks = new Map<string, Set<Function>>();
  private configs = new Map<string, any>();
  private initialized = new Set<string>();

  register(plugin: Plugin): void {
    if (this.plugins.has(plugin.name)) {
      throw new Error(`Plugin '${plugin.name}' already registered`);
    }

    // Check dependencies
    if (plugin.dependencies) {
      for (const dep of plugin.dependencies) {
        if (!this.plugins.has(dep)) {
          throw new Error(`Plugin '${plugin.name}' requires '${dep}'`);
        }
      }
    }

    this.plugins.set(plugin.name, plugin);
  }

  async initialize(): Promise<void> {
    for (const [name, plugin] of this.plugins) {
      if (this.initialized.has(name)) continue;

      // Initialize dependencies first
      if (plugin.dependencies) {
        for (const dep of plugin.dependencies) {
          if (!this.initialized.has(dep)) {
            await this.initializePlugin(dep);
          }
        }
      }

      await this.initializePlugin(name);
    }
  }

  private async initializePlugin(name: string): Promise<void> {
    const plugin = this.plugins.get(name);
    if (!plugin || this.initialized.has(name)) return;

    const api: PluginApi = {
      registerHook: (hookName, handler) => {
        if (!this.hooks.has(hookName)) {
          this.hooks.set(hookName, new Set());
        }
        this.hooks.get(hookName)!.add(handler);
      },
      emitHook: async (hookName, data) => {
        const handlers = this.hooks.get(hookName);
        if (!handlers) return data;
        let result = data;
        for (const handler of handlers) {
          result = await handler(result);
        }
        return result;
      },
      getConfig: (key) => this.configs.get(key),
      setConfig: (key, value) => this.configs.set(key, value),
    };

    await plugin.setup(api);
    this.initialized.add(name);
  }

  async destroy(): Promise<void> {
    for (const [name, plugin] of this.plugins) {
      if (this.initialized.has(name) && plugin.destroy) {
        await plugin.destroy();
      }
    }
    this.initialized.clear();
  }
}

// Plugin example
const loggerPlugin: Plugin = {
  name: 'logger',
  version: '1.0.0',
  setup: (api) => {
    api.registerHook('request', (data: { url: string }) => {
      console.log(`Request: ${data.url}`);
      return data;
    });
    api.registerHook('response', (data: { status: number }) => {
      console.log(`Response: ${data.status}`);
      return data;
    });
  },
};
```

---

## 4. Design a Type-Safe Event System

### Requirements

- Type-safe event registration and emission
- Wildcard event matching
- Event history/replay
- Priority-based handlers
- Async event handling

### Implementation

```typescript
// event-system.ts
type EventMap = Record<string, any>;

class TypedEventSystem<Events extends EventMap> {
  private handlers = new Map<keyof Events, Set<Function>>();
  private history: Array<{ event: string; data: any; timestamp: number }> = [];

  on<K extends keyof Events>(
    event: K,
    handler: (data: Events[K]) => void | Promise<void>
  ): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);

    return () => {
      this.handlers.get(event)?.delete(handler);
    };
  }

  async emit<K extends keyof Events>(
    event: K,
    data: Events[K]
  ): Promise<void> {
    this.history.push({
      event: event as string,
      data,
      timestamp: Date.now(),
    });

    const handlers = this.handlers.get(event);
    if (!handlers) return;

    for (const handler of handlers) {
      await handler(data);
    }
  }

  getHistory(event?: keyof Events): typeof this.history {
    if (event) {
      return this.history.filter(h => h.event === event);
    }
    return [...this.history];
  }

  replay(event: keyof Events, from?: number): void {
    const events = this.getHistory(event)
      .filter(h => from ? h.timestamp >= from : true);
    
    events.forEach(async (h) => {
      await this.emit(event, h.data);
    });
  }
}

// Usage
interface AppEvents {
  userCreated: { id: string; name: string };
  userDeleted: { id: string };
  orderPlaced: { orderId: string; total: number };
}

const events = new TypedEventSystem<AppEvents>();

events.on('userCreated', async (data) => {
  console.log(`User created: ${data.name}`);
});

await events.emit('userCreated', { id: '1', name: 'Alice' });
```

---

## 5. Design a Type-Safe ORM

### Requirements

- Type-safe query building
- Schema definition with types
- Migration support
- Relation handling
- Transaction support

### Implementation

```typescript
// orm.ts
type ColumnType = 'string' | 'number' | 'boolean' | 'date';

interface ColumnDef {
  type: ColumnType;
  nullable?: boolean;
  default?: any;
  primary?: boolean;
}

type TableDef = Record<string, ColumnDef>;

class Table<T extends TableDef> {
  private name: string;
  private columns: T;

  constructor(name: string, columns: T) {
    this.name = name;
    this.columns = columns;
  }

  createSQL(): string {
    const columnDefs = Object.entries(this.columns)
      .map(([name, def]) => {
        const sqlType = this.getSQLType(def.type);
        const nullable = def.nullable ? '' : ' NOT NULL';
        const primary = def.primary ? ' PRIMARY KEY' : '';
        const defaultVal = def.default ? ` DEFAULT ${def.default}` : '';
        return `  ${name} ${sqlType}${nullable}${primary}${defaultVal}`;
      })
      .join(',\n');

    return `CREATE TABLE ${this.name} (\n${columnDefs}\n);`;
  }

  private getSQLType(type: ColumnType): string {
    switch (type) {
      case 'string': return 'VARCHAR(255)';
      case 'number': return 'INTEGER';
      case 'boolean': return 'BOOLEAN';
      case 'date': return 'TIMESTAMP';
    }
  }
}

// Usage
const usersTable = new Table('users', {
  id: { type: 'number', primary: true },
  name: { type: 'string', nullable: false },
  email: { type: 'string', nullable: false },
  createdAt: { type: 'date', default: 'NOW()' },
});

console.log(usersTable.createSQL());
```

---

## 6. Design a Validation Library

### Requirements

- Schema-based validation
- Type inference from schemas
- Custom validators
- Nested object validation
- Error reporting

### Implementation

```typescript
// validator.ts
type ValidationSchema<T> = {
  [K in keyof T]: Validator<T[K]>;
};

interface ValidationResult<T> {
  success: boolean;
  data?: T;
  errors?: ValidationError[];
}

interface ValidationError {
  field: string;
  message: string;
  code: string;
}

class Validator<T> {
  private rules: Array<(value: T) => true | string> = [];

  required(message?: string): this {
    this.rules.push((value) => {
      if (value === undefined || value === null || value === '') {
        return message || 'Field is required';
      }
      return true;
    });
    return this;
  }

  minLength(min: number, message?: string): this {
    this.rules.push((value) => {
      if (typeof value === 'string' && value.length < min) {
        return message || `Must be at least ${min} characters`;
      }
      return true;
    });
    return this;
  }

  pattern(regex: RegExp, message?: string): this {
    this.rules.push((value) => {
      if (typeof value === 'string' && !regex.test(value)) {
        return message || 'Invalid format';
      }
      return true;
    });
    return this;
  }

  custom(fn: (value: T) => boolean, message?: string): this {
    this.rules.push((value) => {
      if (!fn(value)) {
        return message || 'Validation failed';
      }
      return true;
    });
    return this;
  }

  validate(value: T): true | string {
    for (const rule of this.rules) {
      const result = rule(value);
      if (result !== true) {
        return result;
      }
    }
    return true;
  }
}

function createSchema<T extends Record<string, any>>(
  schema: { [K in keyof T]: Validator<T[K]> }
): { validate: (data: T) => ValidationResult<T> } {
  return {
    validate: (data: T) => {
      const errors: ValidationError[] = [];

      for (const [field, validator] of Object.entries(schema)) {
        const result = validator.validate(data[field as keyof T]);
        if (result !== true) {
          errors.push({
            field,
            message: result,
            code: 'VALIDATION_ERROR',
          });
        }
      }

      if (errors.length > 0) {
        return { success: false, errors };
      }

      return { success: true, data };
    },
  };
}

// Usage
interface CreateUserDTO {
  name: string;
  email: string;
  password: string;
}

const userSchema = createSchema<CreateUserDTO>({
  name: new Validator<string>().required().minLength(2),
  email: new Validator<string>().required().pattern(/^[^\s@]+@[^\s@]+\.[^\s@]+$/),
  password: new Validator<string>().required().minLength(8),
});

const result = userSchema.validate({
  name: 'A',
  email: 'bad',
  password: '123',
});

if (!result.success) {
  console.log(result.errors);
}
```

---

## Interview Discussion Points

**Q1**: How do you ensure type safety across the entire stack?
**A**: Use shared type definitions, code generation, and type-safe APIs. Ensure types flow from database schema to API to frontend.

**Q2**: What are the trade-offs of runtime validation vs compile-time types?
**A**: Compile-time types are zero-cost but erased at runtime. Runtime validation catches bad data but adds overhead. Use both: types for internal code, validation for external data.

**Q3**: How do you handle dynamic types in a type-safe way?
**A**: Use generic types, conditional types, and mapped types. For truly dynamic data, use type assertions with runtime validation.

**Q4**: What patterns help maintain type safety in large codebases?
**A**: Branded types, discriminated unions, strict null checks, and type-safe builders. Also use linting rules and CI type checking.

**Q5**: How do you design APIs for extensibility while maintaining type safety?
**A**: Use generic types, plugin architectures with typed hooks, and mapped types for extending existing interfaces.
