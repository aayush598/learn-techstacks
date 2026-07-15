# Company-Specific TypeScript Interview Questions

## 6 Company Styles with Representative Questions

---

## 1. Google/Meta Style: Algorithmic + Types

Focus: Algorithmic problem solving with TypeScript type system.

### Q1: Implement a Type-Safe Trie

**Problem**: Implement a Trie data structure with type-safe autocomplete.

```typescript
class TrieNode<T> {
  children = new Map<string, TrieNode<T>>();
  value?: T;
}

class Trie<T> {
  private root = new TrieNode<T>();

  insert(key: string, value: T): void {
    let node = this.root;
    for (const char of key) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char)!;
    }
    node.value = value;
  }

  search(key: string): T | undefined {
    let node = this.root;
    for (const char of key) {
      if (!node.children.has(char)) return undefined;
      node = node.children.get(char)!;
    }
    return node.value;
  }

  startsWith(prefix: string): string[] {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) return [];
      node = node.children.get(char)!;
    }

    const results: string[] = [];
    this.collect(node, prefix, results);
    return results;
  }

  private collect(node: TrieNode<T>, prefix: string, results: string[]): void {
    if (node.value !== undefined) {
      results.push(prefix);
    }
    for (const [char, child] of node.children) {
      this.collect(child, prefix + char, results);
    }
  }
}

// Usage
const trie = new Trie<{ id: number; name: string }>();
trie.insert('apple', { id: 1, name: 'Apple' });
trie.insert('app', { id: 2, name: 'App' });
trie.insert('application', { id: 3, name: 'Application' });

console.log(trie.startsWith('app')); // ['app', 'apple', 'application']
```

### Q2: Implement Type-Safe LRU Cache with TTL

**Problem**: Create an LRU cache with time-to-live expiration.

```typescript
class LRUCacheWithTTL<K, V> {
  private cache = new Map<K, { value: V; expiry: number }>();
  private maxSize: number;
  private defaultTTL: number;

  constructor(maxSize: number, defaultTTL: number = Infinity) {
    this.maxSize = maxSize;
    this.defaultTTL = defaultTTL;
  }

  get(key: K): V | undefined {
    const entry = this.cache.get(key);
    if (!entry) return undefined;

    if (Date.now() > entry.expiry) {
      this.cache.delete(key);
      return undefined;
    }

    // Move to end (most recently used)
    this.cache.delete(key);
    this.cache.set(key, entry);

    return entry.value;
  }

  set(key: K, value: V, ttl?: number): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.maxSize) {
      // Delete least recently used (first item)
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }

    this.cache.set(key, {
      value,
      expiry: Date.now() + (ttl ?? this.defaultTTL),
    });
  }

  has(key: K): boolean {
    return this.get(key) !== undefined;
  }

  delete(key: K): boolean {
    return this.cache.delete(key);
  }

  get size(): number {
    return this.cache.size;
  }
}

// Usage
const cache = new LRUCacheWithTTL<string, number>(100, 5000);
cache.set('a', 1, 1000); // Expires in 1 second
cache.get('a'); // 1
setTimeout(() => cache.get('a'), 1100); // undefined (expired)
```

### Q3: Type-Safe Graph Traversal

**Problem**: Implement BFS/DFS with type-safe node types.

```typescript
class Graph<T> {
  private adjacencyList = new Map<T, Set<T>>();

  addNode(node: T): void {
    if (!this.adjacencyList.has(node)) {
      this.adjacencyList.set(node, new Set());
    }
  }

  addEdge(from: T, to: T): void {
    this.addNode(from);
    this.addNode(to);
    this.adjacencyList.get(from)!.add(to);
    this.adjacencyList.get(to)!.add(from);
  }

  bfs(start: T, callback: (node: T, distance: number) => void): void {
    const visited = new Set<T>();
    const queue: Array<{ node: T; distance: number }> = [{ node: start, distance: 0 }];
    visited.add(start);

    while (queue.length > 0) {
      const { node, distance } = queue.shift()!;
      callback(node, distance);

      for (const neighbor of this.adjacencyList.get(node) || []) {
        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          queue.push({ node: neighbor, distance: distance + 1 });
        }
      }
    }
  }

  dfs(start: T, callback: (node: T, depth: number) => void): void {
    const visited = new Set<T>();

    const dfsHelper = (node: T, depth: number): void => {
      visited.add(node);
      callback(node, depth);

      for (const neighbor of this.adjacencyList.get(node) || []) {
        if (!visited.has(neighbor)) {
          dfsHelper(neighbor, depth + 1);
        }
      }
    };

    dfsHelper(start, 0);
  }
}

// Usage
const graph = new Graph<string>();
graph.addEdge('A', 'B');
graph.addEdge('A', 'C');
graph.addEdge('B', 'D');
graph.addEdge('C', 'E');

graph.bfs('A', (node, distance) => {
  console.log(`Node: ${node}, Distance: ${distance}`);
});
```

---

## 2. Amazon Style: System Design + Types

Focus: Scalable systems with type safety.

### Q4: Design a Type-Safe Rate Limiter

```typescript
interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
}

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: number;
}

class RateLimiter {
  private config: RateLimitConfig;
  private requests = new Map<string, number[]>();

  constructor(config: RateLimitConfig) {
    this.config = config;
  }

  check(key: string): RateLimitResult {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;

    // Get existing requests in window
    const existing = this.requests.get(key) || [];
    const validRequests = existing.filter(time => time > windowStart);

    if (validRequests.length >= this.config.maxRequests) {
      return {
        allowed: false,
        remaining: 0,
        resetAt: validRequests[0] + this.config.windowMs,
      };
    }

    // Add new request
    validRequests.push(now);
    this.requests.set(key, validRequests);

    return {
      allowed: true,
      remaining: this.config.maxRequests - validRequests.length,
      resetAt: windowStart + this.config.windowMs,
    };
  }

  reset(key: string): void {
    this.requests.delete(key);
  }
}

// Usage
const limiter = new RateLimiter({ maxRequests: 100, windowMs: 60000 });
const result = limiter.check('user:123');
console.log(result); // { allowed: true, remaining: 99, resetAt: ... }
```

### Q5: Design a Type-Safe Cache with Strategy Pattern

```typescript
interface CacheStrategy<K, V> {
  get(key: K): V | undefined;
  set(key: K, value: V): void;
  has(key: K): boolean;
  delete(key: K): boolean;
  clear(): void;
}

class LRUCacheStrategy<K, V> implements CacheStrategy<K, V> {
  private cache = new Map<K, V>();
  private maxSize: number;

  constructor(maxSize: number) {
    this.maxSize = maxSize;
  }

  get(key: K): V | undefined {
    const value = this.cache.get(key);
    if (value !== undefined) {
      this.cache.delete(key);
      this.cache.set(key, value);
    }
    return value;
  }

  set(key: K, value: V): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }

  has(key: K): boolean {
    return this.cache.has(key);
  }

  delete(key: K): boolean {
    return this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }
}

class TypedCache<K, V> {
  private strategy: CacheStrategy<K, V>;

  constructor(strategy: CacheStrategy<K, V>) {
    this.strategy = strategy;
  }

  get(key: K): V | undefined {
    return this.strategy.get(key);
  }

  set(key: K, value: V): void {
    this.strategy.set(key, value);
  }
}

// Usage
const userCache = new TypedCache<string, User>(
  new LRUCacheStrategy(1000)
);

userCache.set('user:1', { id: '1', name: 'Alice' });
const user = userCache.get('user:1');
```

### Q6: Design a Type-Safe Circuit Breaker

```typescript
type CircuitState = 'closed' | 'open' | 'half-open';

interface CircuitBreakerConfig {
  failureThreshold: number;
  successThreshold: number;
  timeout: number;
}

class CircuitBreaker<T extends (...args: any[]) => any> {
  private state: CircuitState = 'closed';
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime = 0;
  private config: CircuitBreakerConfig;

  constructor(
    private fn: T,
    config: Partial<CircuitBreakerConfig> = {}
  ) {
    this.config = {
      failureThreshold: 5,
      successThreshold: 3,
      timeout: 60000,
      ...config,
    };
  }

  async execute(...args: Parameters<T>): Promise<ReturnType<T>> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailureTime > this.config.timeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await this.fn(...args);
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;

    if (this.state === 'half-open') {
      this.successCount++;
      if (this.successCount >= this.config.successThreshold) {
        this.state = 'closed';
        this.successCount = 0;
      }
    }
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.config.failureThreshold) {
      this.state = 'open';
    }
  }

  getState(): CircuitState {
    return this.state;
  }
}

// Usage
const apiCall = new CircuitBreaker(
  async (url: string) => {
    const response = await fetch(url);
    return response.json();
  },
  { failureThreshold: 3, timeout: 30000 }
);

try {
  const data = await apiCall.execute('https://api.example.com/data');
} catch (error) {
  console.log('Circuit breaker is open:', apiCall.getState());
}
```

---

## 3. Apple Style: Low-Level + Types

Focus: Memory efficiency, systems programming, type-level computations.

### Q7: Implement Type-Safe Bit Flags

```typescript
type BitFlag<T extends string> = {
  [K in T]: 1 << number;
};

function createFlags<T extends string>(...flags: T[]): BitFlag<T> {
  const result = {} as BitFlag<T>;
  flags.forEach((flag, index) => {
    (result as any)[flag] = 1 << index;
  });
  return result;
}

function hasFlag(flags: number, flag: number): boolean {
  return (flags & flag) === flag;
}

function addFlag(flags: number, flag: number): number {
  return flags | flag;
}

function removeFlag(flags: number, flag: number): number {
  return flags & ~flag;
}

// Usage
const Permissions = createFlags('read', 'write', 'execute');
type Permissions = typeof Permissions;

let userPerms = 0;
userPerms = addFlag(userPerms, Permissions.read);
userPerms = addFlag(userPerms, Permissions.write);

console.log(hasFlag(userPerms, Permissions.read)); // true
console.log(hasFlag(userPerms, Permissions.execute)); // false
```

### Q8: Implement Type-Safe Ring Buffer

```typescript
class RingBuffer<T> {
  private buffer: (T | undefined)[];
  private head = 0;
  private tail = 0;
  private count = 0;
  private readonly capacity: number;

  constructor(capacity: number) {
    this.capacity = capacity;
    this.buffer = new Array(capacity);
  }

  push(item: T): boolean {
    if (this.isFull()) {
      return false;
    }

    this.buffer[this.tail] = item;
    this.tail = (this.tail + 1) % this.capacity;
    this.count++;
    return true;
  }

  pop(): T | undefined {
    if (this.isEmpty()) {
      return undefined;
    }

    const item = this.buffer[this.head];
    this.buffer[this.head] = undefined;
    this.head = (this.head + 1) % this.capacity;
    this.count--;
    return item;
  }

  peek(): T | undefined {
    if (this.isEmpty()) {
      return undefined;
    }
    return this.buffer[this.head];
  }

  isEmpty(): boolean {
    return this.count === 0;
  }

  isFull(): boolean {
    return this.count === this.capacity;
  }

  get size(): number {
    return this.count;
  }

  getCapacity(): number {
    return this.capacity;
  }

  toArray(): T[] {
    const result: T[] = [];
    let index = this.head;
    for (let i = 0; i < this.count; i++) {
      result.push(this.buffer[index] as T);
      index = (index + 1) % this.capacity;
    }
    return result;
  }
}

// Usage
const buffer = new RingBuffer<number>(3);
buffer.push(1);
buffer.push(2);
buffer.push(3);
console.log(buffer.pop()); // 1
buffer.push(4);
console.log(buffer.toArray()); // [2, 3, 4]
```

---

## 4. Netflix Style: Scaling

Focus: High-throughput systems, caching, performance.

### Q9: Implement Type-Safe Retry with Exponential Backoff

```typescript
interface RetryConfig {
  maxRetries: number;
  initialDelay: number;
  maxDelay: number;
  backoffFactor: number;
}

async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  config: Partial<RetryConfig> = {}
): Promise<T> {
  const {
    maxRetries = 3,
    initialDelay = 1000,
    maxDelay = 30000,
    backoffFactor = 2,
  } = config;

  let lastError: Error | undefined;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (attempt < maxRetries) {
        const delay = Math.min(
          initialDelay * Math.pow(backoffFactor, attempt),
          maxDelay
        );
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}

// Usage
const data = await retryWithBackoff(
  async () => {
    const response = await fetch('https://api.example.com/data');
    if (!response.ok) throw new Error('Failed');
    return response.json();
  },
  { maxRetries: 3, initialDelay: 1000 }
);
```

### Q10: Implement Type-Safe Connection Pool

```typescript
interface Connection {
  id: string;
  inUse: boolean;
  createdAt: number;
}

class ConnectionPool<T extends Connection> {
  private pool: T[] = [];
  private maxSize: number;
  private createConnection: () => T;
  private validateConnection: (conn: T) => boolean;

  constructor(config: {
    maxSize: number;
    createConnection: () => T;
    validateConnection?: (conn: T) => boolean;
  }) {
    this.maxSize = config.maxSize;
    this.createConnection = config.createConnection;
    this.validateConnection = config.validateConnection || (() => true);
  }

  async acquire(): Promise<T> {
    // Find available connection
    const available = this.pool.find(conn => !conn.inUse && this.validateConnection(conn));

    if (available) {
      available.inUse = true;
      return available;
    }

    // Create new connection if pool not full
    if (this.pool.length < this.maxSize) {
      const newConn = this.createConnection();
      newConn.inUse = true;
      this.pool.push(newConn);
      return newConn;
    }

    // Wait for available connection
    return new Promise((resolve) => {
      const check = setInterval(() => {
        const conn = this.pool.find(c => !c.inUse && this.validateConnection(c));
        if (conn) {
          clearInterval(check);
          conn.inUse = true;
          resolve(conn);
        }
      }, 100);
    });
  }

  release(conn: T): void {
    conn.inUse = false;
  }

  get size(): number {
    return this.pool.length;
  }

  get available(): number {
    return this.pool.filter(c => !c.inUse).length;
  }
}

// Usage
interface DBConnection extends Connection {
  query: (sql: string) => Promise<any>;
}

const pool = new ConnectionPool<DBConnection>({
  maxSize: 10,
  createConnection: () => ({
    id: Math.random().toString(36),
    inUse: false,
    createdAt: Date.now(),
    query: async (sql: string) => { /* ... */ },
  }),
});

const conn = await pool.acquire();
try {
  await conn.query('SELECT * FROM users');
} finally {
  pool.release(conn);
}
```

---

## 5. Startup Style: Full-Stack + Types

Focus: Rapid development, type safety across the stack.

### Q11: Design a Type-Safe API Layer

```typescript
// Shared types between frontend and backend
interface ApiTypes {
  'GET /api/users': {
    response: User[];
    query: { page?: number; limit?: number };
  };
  'POST /api/users': {
    response: User;
    body: CreateUserDTO;
  };
  'GET /api/users/:id': {
    response: User;
    params: { id: string };
  };
  'PUT /api/users/:id': {
    response: User;
    body: Partial<User>;
    params: { id: string };
  };
  'DELETE /api/users/:id': {
    response: void;
    params: { id: string };
  };
}

// Backend route handler
type RouteHandler<K extends keyof ApiTypes> = (
  req: {
    body: ApiTypes[K] extends { body: infer B } ? B : never;
    query: ApiTypes[K] extends { query: infer Q } ? Q : never;
    params: ApiTypes[K] extends { params: infer P } ? P : never;
  },
  res: {
    json: (data: ApiTypes[K]['response']) => void;
    status: (code: number) => { json: (data: any) => void };
  }
) => void;

// Frontend API client
class TypedApiClient {
  async request<K extends keyof ApiTypes>(
    endpoint: K,
    options?: {
      body?: ApiTypes[K] extends { body: infer B } ? B : never;
      query?: ApiTypes[K] extends { query: infer Q } ? Q : never;
    }
  ): Promise<ApiTypes[K]['response']> {
    const [method, ...pathParts] = (endpoint as string).split(' ');
    let path = pathParts.join(' ');

    // Replace params
    if (options?.query) {
      const params = new URLSearchParams(options.query as any);
      path += `?${params.toString()}`;
    }

    const response = await fetch(path, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: options?.body ? JSON.stringify(options.body) : undefined,
    });

    return response.json();
  }
}

// Usage
const api = new TypedApiClient();
const users = await api.request('GET /api/users', {
  query: { page: 1, limit: 10 },
});
// users: User[]
```

### Q12: Design a Type-Safe Form System

```typescript
type FormField<T> = {
  type: 'text' | 'number' | 'email' | 'select' | 'checkbox';
  label: string;
  defaultValue?: T;
  required?: boolean;
  validate?: (value: T) => string | null;
  options?: T extends string ? string[] : never;
};

type FormSchema<T> = {
  [K in keyof T]: FormField<T[K]>;
};

class TypedForm<T extends Record<string, any>> {
  private schema: FormSchema<T>;
  private values: T;
  private errors: Partial<Record<keyof T, string>> = {};

  constructor(schema: FormSchema<T>) {
    this.schema = schema;
    this.values = Object.fromEntries(
      Object.entries(schema).map(([key, field]) => [
        key,
        (field as FormField<any>).defaultValue,
      ])
    ) as T;
  }

  setValue<K extends keyof T>(key: K, value: T[K]): void {
    this.values[key] = value;
    this.validateField(key);
  }

  getValue<K extends keyof T>(key: K): T[K] {
    return this.values[key];
  }

  validateField<K extends keyof T>(key: K): string | null {
    const field = this.schema[key] as FormField<T[K]>;
    const value = this.values[key];

    if (field.required && (value === undefined || value === null)) {
      this.errors[key] = `${String(key)} is required`;
      return this.errors[key];
    }

    if (field.validate) {
      const error = field.validate(value);
      if (error) {
        this.errors[key] = error;
        return error;
      }
    }

    delete this.errors[key];
    return null;
  }

  validate(): boolean {
    let valid = true;
    for (const key of Object.keys(this.schema)) {
      if (this.validateField(key as keyof T)) {
        valid = false;
      }
    }
    return valid;
  }

  getErrors(): Partial<Record<keyof T, string>> {
    return { ...this.errors };
  }
}

// Usage
interface LoginForm {
  email: string;
  password: string;
}

const form = new TypedForm<LoginForm>({
  email: {
    type: 'email',
    label: 'Email',
    required: true,
    validate: (value) => {
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        return 'Invalid email';
      }
      return null;
    },
  },
  password: {
    type: 'text',
    label: 'Password',
    required: true,
    validate: (value) => {
      if (value.length < 8) return 'Password must be 8+ characters';
      return null;
    },
  },
});

form.setValue('email', 'bad');
form.validate(); // false
console.log(form.getErrors()); // { email: 'Invalid email' }
```

---

## 6. Tesla/NVIDIA Style: Embedded/Performance

Focus: Memory efficiency, low-level operations, performance-critical code.

### Q13: Implement Type-Safe Ring Buffer for IoT Data

```typescript
type SensorData = {
  timestamp: number;
  temperature: number;
  humidity: number;
  pressure: number;
};

class SensorBuffer {
  private buffer: Float64Array;
  private metadata: Array<{ timestamp: number; valid: boolean }>;
  private head = 0;
  private count = 0;
  private readonly capacity: number;

  constructor(capacity: number) {
    this.capacity = capacity;
    // Store 4 values per sample (timestamp, temp, humidity, pressure)
    this.buffer = new Float64Array(capacity * 4);
    this.metadata = new Array(capacity).fill(null).map(() => ({
      timestamp: 0,
      valid: false,
    }));
  }

  push(data: SensorData): boolean {
    if (this.count >= this.capacity) {
      return false;
    }

    const offset = this.head * 4;
    this.buffer[offset] = data.timestamp;
    this.buffer[offset + 1] = data.temperature;
    this.buffer[offset + 2] = data.humidity;
    this.buffer[offset + 3] = data.pressure;

    this.metadata[this.head] = {
      timestamp: data.timestamp,
      valid: true,
    };

    this.head = (this.head + 1) % this.capacity;
    this.count++;
    return true;
  }

  getLatest(): SensorData | null {
    if (this.count === 0) return null;

    const index = (this.head - 1 + this.capacity) % this.capacity;
    const offset = index * 4;

    return {
      timestamp: this.buffer[offset],
      temperature: this.buffer[offset + 1],
      humidity: this.buffer[offset + 2],
      pressure: this.buffer[offset + 3],
    };
  }

  getAverage(): Omit<SensorData, 'timestamp'> | null {
    if (this.count === 0) return null;

    let tempSum = 0;
    let humidSum = 0;
    let pressSum = 0;

    for (let i = 0; i < this.count; i++) {
      const offset = i * 4;
      tempSum += this.buffer[offset + 1];
      humidSum += this.buffer[offset + 2];
      pressSum += this.buffer[offset + 3];
    }

    return {
      temperature: tempSum / this.count,
      humidity: humidSum / this.count,
      pressure: pressSum / this.count,
    };
  }

  get count(): number {
    return this.count;
  }

  get size(): number {
    return this.capacity;
  }

  get memoryUsage(): number {
    return this.buffer.byteLength + this.metadata.length * 16;
  }
}

// Usage
const sensorBuffer = new SensorBuffer(1000);
sensorBuffer.push({
  timestamp: Date.now(),
  temperature: 22.5,
  humidity: 65,
  pressure: 1013.25,
});

const latest = sensorBuffer.getLatest();
const avg = sensorBuffer.getAverage();
console.log(`Memory: ${sensorBuffer.memoryUsage} bytes`);
```

### Q14: Implement Type-Safe State Machine for Hardware

```typescript
type HardwareState = 'idle' | 'initializing' | 'running' | 'error' | 'shutdown';
type HardwareEvent = 'init' | 'start' | 'stop' | 'error' | 'reset';

interface HardwareTransition {
  from: HardwareState;
  to: HardwareState;
  event: HardwareEvent;
  guard?: () => boolean;
  action?: () => void;
}

class HardwareStateMachine {
  private current: HardwareState = 'idle';
  private transitions: HardwareTransition[] = [];
  private listeners = new Map<HardwareState, Set<() => void>>();

  constructor(transitions: HardwareTransition[]) {
    this.transitions = transitions;
  }

  on(state: HardwareState, callback: () => void): () => void {
    if (!this.listeners.has(state)) {
      this.listeners.set(state, new Set());
    }
    this.listeners.get(state)!.add(callback);

    return () => {
      this.listeners.get(state)?.delete(callback);
    };
  }

  send(event: HardwareEvent): HardwareState {
    const transition = this.transitions.find(
      t => t.from === this.current && t.event === event
    );

    if (!transition) {
      throw new Error(
        `Invalid transition: ${this.current} + ${event}`
      );
    }

    if (transition.guard && !transition.guard()) {
      throw new Error(
        `Guard failed for transition: ${this.current} + ${event}`
      );
    }

    transition.action?.();
    this.current = transition.to;

    this.listeners.get(this.current)?.forEach(cb => cb());

    return this.current;
  }

  getState(): HardwareState {
    return this.current;
  }
}

// Usage
const hardware = new HardwareStateMachine([
  { from: 'idle', to: 'initializing', event: 'init' },
  { from: 'initializing', to: 'running', event: 'start' },
  { from: 'running', to: 'idle', event: 'stop' },
  { from: 'running', to: 'error', event: 'error' },
  { from: 'error', to: 'idle', event: 'reset' },
  { from: '*', to: 'shutdown', event: 'stop' },
]);

hardware.on('running', () => {
  console.log('Hardware started');
});

hardware.send('init');
hardware.send('start');
console.log(hardware.getState()); // 'running'
```

---

## Common Themes Across Companies

### Algorithm + Types (Google/Meta)

```typescript
// Always consider:
// 1. Time complexity of type operations
// 2. Type-level algorithms (recursion depth)
// 3. Edge cases in generic constraints
// 4. Performance of runtime operations
```

### System Design + Types (Amazon)

```typescript
// Always consider:
// 1. Scalability of typed systems
// 2. Type safety across service boundaries
// 3. Error handling patterns
// 4. Configuration and dependency injection
```

### Performance + Types (Apple/NVIDIA)

```typescript
// Always consider:
// 1. Memory layout of typed data
// 2. Zero-cost abstractions
// 3. Type erasure at runtime
// 4. Compile-time vs runtime overhead
```

### Full-Stack + Types (Startups)

```typescript
// Always consider:
// 1. Shared types between frontend/backend
// 2. Type-safe API contracts
// 3. Form validation and user input
// 4. Rapid iteration with type safety
```

---

## Interview Tips by Company

| Company | Focus | Key Skills |
|---------|-------|------------|
| Google | Algorithmic + Types | Data structures, type manipulation, problem solving |
| Meta | System Design + Types | Scalable architecture, type safety, performance |
| Amazon | System Design + Types | AWS services, distributed systems, typed APIs |
| Apple | Low-Level + Types | Memory management, performance, systems programming |
| Netflix | Scaling + Types | High throughput, caching, fault tolerance |
| Startups | Full-Stack + Types | Rapid development, end-to-end type safety |
| Tesla/NVIDIA | Performance + Types | Real-time systems, hardware interfaces, optimization |
