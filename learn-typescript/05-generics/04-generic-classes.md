# 04 — Generic Classes

## Table of Contents

1. [Generic Class Syntax](#generic-class-syntax)
2. [Generic Class with Constraints](#generic-class-with-constraints)
3. [Generic Class Implementing Interface](#implementing-interface)
4. [Generic Class Extending Class](#extending-class)
5. [Generic Static Members](#generic-static-members)
6. [Generic Class with Multiple Parameters](#multiple-parameters)
7. [Real-World Generic Class Examples](#real-world-examples)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## Generic Class Syntax

Generic classes declare type parameters in the class name. The type parameter is then
available throughout the class body — properties, methods, and constructors.

```typescript
class Box<T> {
  private value: T;

  constructor(value: T) {
    this.value = value;
  }

  getValue(): T {
    return this.value;
  }

  setValue(value: T): void {
    this.value = value;
  }

  map<R>(fn: (value: T) => R): Box<R> {
    return new Box(fn(this.value));
  }
}

// Usage
const numberBox = new Box<number>(42);
console.log(numberBox.getValue()); // 42

const stringBox = new Box<string>("hello");
console.log(stringBox.getValue()); // "hello"

// Type inference
const inferred = new Box(true); // Box<boolean>

// Map transforms the inner type
const lengthBox = numberBox.map((n) => n.toString());
// lengthBox: Box<string>
```

### Generic with Method-Level Type Parameters

Classes can have class-level AND method-level type parameters:

```typescript
class Container<T> {
  private items: T[] = [];

  constructor(initialItems?: T[]) {
    if (initialItems) {
      this.items = [...initialItems];
    }
  }

  add(item: T): void {
    this.items.push(item);
  }

  // Method has its OWN type parameter U
  map<U>(fn: (item: T) => U): Container<U> {
    return new Container(this.items.map(fn));
  }

  // Method uses class-level T
  filter(predicate: (item: T) => boolean): Container<T> {
    return new Container(this.items.filter(predicate));
  }

  // Method introduces a NEW type parameter
  reduce<U>(fn: (acc: U, item: T) => U, initial: U): U {
    return this.items.reduce(fn, initial);
  }

  toArray(): T[] {
    return [...this.items];
  }
}

const numbers = new Container([1, 2, 3, 4, 5]);

const doubled = numbers.map((n) => n * 2);
// doubled: Container<number>, items: [2, 4, 6, 8, 10]

const evens = numbers.filter((n) => n % 2 === 0);
// evens: Container<number>, items: [2, 4]

const sum = numbers.reduce((acc, n) => acc + n, 0);
// sum: number (= 15)
```

---

## Generic Class with Constraints

The `extends` keyword restricts what types can be used as the generic parameter.

```typescript
class SortedList<T extends { compare(other: T): number }> {
  private items: T[] = [];

  add(item: T): void {
    const index = this.items.findIndex(
      (existing) => existing.compare(item) > 0
    );
    if (index === -1) {
      this.items.push(item);
    } else {
      this.items.splice(index, 0, item);
    }
  }

  get(index: number): T | undefined {
    return this.items[index];
  }

  size(): number {
    return this.items.length;
  }

  toArray(): T[] {
    return [...this.items];
  }
}

// Must have a compare method
class Priority implements Priority {
  constructor(public value: number, public label: string) {}

  compare(other: Priority): number {
    return this.value - other.value;
  }
}

const priorities = new SortedList<Priority>();
priorities.add(new Priority(3, "Low"));
priorities.add(new Priority(1, "High"));
priorities.add(new Priority(2, "Medium"));

console.log(priorities.toArray().map((p) => p.label));
// ["High", "Medium", "Low"]
```

### Constraining to Object Types

```typescript
class EventEmitter<TEvents extends Record<string, unknown>> {
  private listeners = new Map<keyof TEvents, Set<Function>>();

  on<K extends keyof TEvents>(
    event: K,
    listener: (payload: TEvents[K]) => void
  ): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);
  }

  emit<K extends keyof TEvents>(event: K, payload: TEvents[K]): void {
    this.listeners.get(event)?.forEach((fn) => fn(payload));
  }
}

interface AppEvents {
  userLogin: { userId: string; timestamp: number };
  userLogout: { userId: string };
  error: { code: string; message: string };
}

const emitter = new EventEmitter<AppEvents>();
emitter.on("userLogin", (data) => {
  console.log(data.userId, data.timestamp); // ✅ fully typed
});
```

---

## Implementing Interface

Generic classes can implement generic interfaces, binding the type parameter or
leaving it open.

```typescript
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(item: Omit<T, "id">): Promise<T>;
  update(id: string, item: Partial<T>): Promise<T>;
  delete(id: string): Promise<boolean>;
}

// Leave T open — callers provide the type
class InMemoryRepository<T extends { id: string }> implements Repository<T> {
  private items: Map<string, T> = new Map();

  async findById(id: string): Promise<T | null> {
    return this.items.get(id) ?? null;
  }

  async findAll(): Promise<T[]> {
    return Array.from(this.items.values());
  }

  async create(item: Omit<T, "id">): Promise<T> {
    const newItem = { ...item, id: crypto.randomUUID() } as T;
    this.items.set(newItem.id, newItem);
    return newItem;
  }

  async update(id: string, updates: Partial<T>): Promise<T> {
    const existing = this.items.get(id);
    if (!existing) throw new Error(`Not found: ${id}`);
    const updated = { ...existing, ...updates };
    this.items.set(id, updated);
    return updated;
  }

  async delete(id: string): Promise<boolean> {
    return this.items.delete(id);
  }
}

// Usage
interface User {
  id: string;
  name: string;
  email: string;
}

const userRepo = new InMemoryRepository<User>();
await userRepo.create({ name: "Alice", email: "alice@example.com" });
```

### Binding to a Concrete Type

```typescript
interface CacheItem {
  key: string;
  value: unknown;
  ttl: number;
}

// Bind the generic at the class level
class Cache implements Repository<CacheItem> {
  private store = new Map<string, CacheItem>();

  async findById(id: string): Promise<CacheItem | null> {
    return this.store.get(id) ?? null;
  }

  async findAll(): Promise<CacheItem[]> {
    return Array.from(this.store.values());
  }

  async create(item: Omit<CacheItem, "id">): Promise<CacheItem> {
    const newItem = { ...item, id: crypto.randomUUID() } as CacheItem;
    this.store.set(newItem.id, newItem);
    return newItem;
  }

  async update(id: string, updates: Partial<CacheItem>): Promise<CacheItem> {
    const existing = this.store.get(id);
    if (!existing) throw new Error(`Not found: ${id}`);
    const updated = { ...existing, ...updates };
    this.store.set(id, updated);
    return updated;
  }

  async delete(id: string): Promise<boolean> {
    return this.store.delete(id);
  }
}
```

---

## Extending Class

Generic classes can extend other generic classes, either binding or forwarding type
parameters.

### Forwarding Type Parameters

```typescript
class BaseRepository<T> {
  protected items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  getAll(): T[] {
    return [...this.items];
  }
}

// T is forwarded from BaseRepository
class SearchableRepository<T> extends BaseRepository<T> {
  search(predicate: (item: T) => boolean): T[] {
    return this.items.filter(predicate);
  }
}

// T is forwarded again
class PaginatedRepository<T> extends SearchableRepository<T> {
  getPage(page: number, pageSize: number): T[] {
    const start = (page - 1) * pageSize;
    return this.items.slice(start, start + pageSize);
  }

  totalPages(pageSize: number): number {
    return Math.ceil(this.items.length / pageSize);
  }
}

const repo = new PaginatedRepository<User>();
repo.add({ id: "1", name: "Alice", email: "alice@example.com", createdAt: new Date(), updatedAt: new Date() });
const results = repo.search((u) => u.name.startsWith("A"));
const page = repo.getPage(1, 10);
```

### Binding Type Parameters

```typescript
class StringSet extends BaseRepository<string> {
  has(value: string): boolean {
    return this.items.includes(value);
  }

  addUnique(value: string): void {
    if (!this.has(value)) {
      this.add(value);
    }
  }
}

const tags = new StringSet();
tags.addUnique("typescript");
tags.addUnique("typescript"); // ignored
console.log(tags.getAll());   // ["typescript"]
```

---

## Generic Static Members

Static members **cannot** use the class's type parameters. This is a common point of
confusion.

```typescript
class Factory<T> {
  private value: T;

  constructor(value: T) {
    this.value = value;
  }

  // ✅ Instance method — T is available
  getValue(): T {
    return this.value;
  }

  // ❌ Static methods CANNOT use T
  // static create(value: T): Factory<T> { ... }

  // ✅ Workaround: make the static method generic itself
  static create<T>(value: T): Factory<T> {
    return new Factory(value);
  }
}

const instance = Factory.create(42); // Factory<number>
const instance2 = Factory.create("hello"); // Factory<string>
```

### Static Utility on Generic Class

```typescript
class MathUtil {
  static sum<T extends number>(values: T[]): number {
    return values.reduce((acc, v) => acc + v, 0);
  }

  static average<T extends number>(values: T[]): number {
    return MathUtil.sum(values) / values.length;
  }

  static min<T extends number>(values: T[]): number {
    return Math.min(...values);
  }

  static max<T extends number>(values: T[]): number {
    return Math.max(...values);
  }
}

MathUtil.average([1, 2, 3, 4, 5]); // 3
```

---

## Multiple Type Parameters

```typescript
class Pair<A, B> {
  constructor(
    public readonly first: A,
    public readonly second: B
  ) {}

  swap(): Pair<B, A> {
    return new Pair(this.second, this.first);
  }

  mapFirst<NewA>(fn: (a: A) => NewA): Pair<NewA, B> {
    return new Pair(fn(this.first), this.second);
  }

  mapSecond<NewB>(fn: (b: B) => NewB): Pair<A, NewB> {
    return new Pair(this.first, fn(this.second));
  }

  toArray(): [A, B] {
    return [this.first, this.second];
  }
}

const pair = new Pair("hello", 42);
const swapped = pair.swap();         // Pair<number, string>
const mapped = pair.mapFirst((s) => s.length); // Pair<number, number>
```

### Multi-Generics with Constraints

```typescript
class Mapper<TInput, TOutput> {
  private transforms: Map<string, (item: TInput) => TOutput> = new Map();

  register(name: string, transform: (item: TInput) => TOutput): void {
    this.transforms.set(name, transform);
  }

  apply(name: string, input: TInput): TOutput {
    const fn = this.transforms.get(name);
    if (!fn) throw new Error(`Transform "${name}" not found`);
    return fn(input);
  }

  listTransforms(): string[] {
    return Array.from(this.transforms.keys());
  }
}

const stringToNumber = new Mapper<string, number>();
stringToNumber.register("length", (s) => s.length);
stringToNumber.register("charCode", (s) => s.charCodeAt(0));

console.log(stringToNumber.apply("length", "hello")); // 5
console.log(stringToNumber.apply("charCode", "A"));   // 65
```

---

## Real-World Examples

### Generic Queue

```typescript
class Queue<T> {
  private items: T[] = [];

  enqueue(item: T): void {
    this.items.push(item);
  }

  dequeue(): T | undefined {
    return this.items.shift();
  }

  peek(): T | undefined {
    return this.items[0];
  }

  size(): number {
    return this.items.length;
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }

  toArray(): T[] {
    return [...this.items];
  }

  clear(): void {
    this.items = [];
  }

  [Symbol.iterator](): Iterator<T> {
    let index = 0;
    const items = this.items;
    return {
      next(): IteratorResult<T> {
        if (index < items.length) {
          return { value: items[index++], done: false };
        }
        return { done: true, value: undefined };
      },
    };
  }
}

const numberQueue = new Queue<number>();
numberQueue.enqueue(1);
numberQueue.enqueue(2);
numberQueue.enqueue(3);

console.log(numberQueue.dequeue()); // 1
console.log(numberQueue.peek());    // 2
console.log(numberQueue.size());    // 2

// Iterable
for (const item of numberQueue) {
  console.log(item); // 2, 3
}
```

### Generic Stack

```typescript
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  size(): number {
    return this.items.length;
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }

  clear(): void {
    this.items = [];
  }

  toArray(): T[] {
    return [...this.items].reverse();
  }
}

const callStack = new Stack<string>();
callStack.push("main()");
callStack.push("getUser()");
callStack.push("fetchData()");
console.log(callStack.pop()); // "fetchData()"
console.log(callStack.peek()); // "getUser()"
```

### Generic Doubly-Linked List

```typescript
class DoublyLinkedList<T> {
  private head: ListNode<T> | null = null;
  private tail: ListNode<T> | null = null;
  private count = 0;

  append(value: T): void {
    const node: ListNode<T> = { value, next: null, prev: this.tail };
    if (this.tail) {
      this.tail.next = node;
    } else {
      this.head = node;
    }
    this.tail = node;
    this.count++;
  }

  prepend(value: T): void {
    const node: ListNode<T> = { value, next: this.head, prev: null };
    if (this.head) {
      this.head.prev = node;
    } else {
      this.tail = node;
    }
    this.head = node;
    this.count++;
  }

  remove(value: T): boolean {
    let current = this.head;
    while (current) {
      if (current.value === value) {
        if (current.prev) current.prev.next = current.next;
        else this.head = current.next;

        if (current.next) current.next.prev = current.prev;
        else this.tail = current.prev;

        this.count--;
        return true;
      }
      current = current.next;
    }
    return false;
  }

  find(predicate: (value: T) => boolean): T | undefined {
    let current = this.head;
    while (current) {
      if (predicate(current.value)) return current.value;
      current = current.next;
    }
    return undefined;
  }

  size(): number {
    return this.count;
  }

  toArray(): T[] {
    const result: T[] = [];
    let current = this.head;
    while (current) {
      result.push(current.value);
      current = current.next;
    }
    return result;
  }
}

interface ListNode<T> {
  value: T;
  next: ListNode<T> | null;
  prev: ListNode<T> | null;
}

const list = new DoublyLinkedList<number>();
list.append(1);
list.append(2);
list.append(3);
list.prepend(0);

console.log(list.toArray()); // [0, 1, 2, 3]
list.remove(2);
console.log(list.toArray()); // [0, 1, 3]
```

### Generic Observable (Reactive Pattern)

```typescript
type Observer<T> = (value: T) => void;
type Unsubscribe = () => void;

class Observable<T> {
  private observers = new Set<Observer<T>>();
  private currentValue: T;

  constructor(initialValue: T) {
    this.currentValue = initialValue;
  }

  get value(): T {
    return this.currentValue;
  }

  set value(newValue: T) {
    this.currentValue = newValue;
    this.notify();
  }

  subscribe(observer: Observer<T>): Unsubscribe {
    this.observers.add(observer);
    // Emit current value immediately
    observer(this.currentValue);
    return () => {
      this.observers.delete(observer);
    };
  }

  private notify(): void {
    this.observers.forEach((observer) => observer(this.currentValue));
  }

  map<R>(transform: (value: T) => R): Observable<R> {
    const derived = new Observable(transform(this.currentValue));
    this.subscribe((value) => {
      derived.value = transform(value);
    });
    return derived;
  }
}

// Usage
const count = new Observable(0);
const unsubscribe = count.subscribe((value) => {
  console.log(`Count: ${value}`);
});
// Logs: Count: 0

count.value = 5;  // Logs: Count: 5
count.value = 10; // Logs: Count: 10

const doubled = count.map((n) => n * 2);
// doubled.value is 20

count.value = 15; // doubled.value is now 30
```

---

## Best Practices

1. **Let TypeScript infer** the generic type at the call site when possible.
2. **Use constraints** to prevent nonsensical instantiations.
3. **Remember static members** cannot use class-level type parameters — make them
   separately generic.
4. **Prefer composition** over deep generic class hierarchies.
5. **Use protected members** for state that subclasses need access to.
6. **Implement iteration protocols** (`Symbol.iterator`) for collection classes.

---

## Interview Questions

**Q1: Can static members of a generic class use the class's type parameter?**

No. Static members exist on the class constructor, not on instances. They cannot
access the instance-level type parameter. Make the static method separately generic.

**Q2: Can a generic class implement a generic interface without specifying the type?**

Yes. The class remains generic and defers the type to its callers.

**Q3: How do you constrain a generic class to only accept certain types?**

Use `extends`: `class SortedList<T extends Comparable<T>>` ensures `T` has a
`compare` method.

**Q4: What is the difference between `class Box<T>` and `class Box<T extends unknown>`?**

They are identical. `<T>` is shorthand for `<T extends unknown>`.

**Q5: When should you use a generic class vs a generic interface + regular class?**

Use a generic class when the type parameter is integral to the class's behavior. Use
an interface + regular class when you want to decouple the contract from the
implementation and allow multiple implementations.
