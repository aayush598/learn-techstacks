# Event-Driven Architecture in TypeScript

## Table of Contents

- [Typed Event Emitter](#typed-event-emitter)
- [Event Bus with Generics](#event-bus-with-generics)
- [Typed Pub/Sub](#typed-pubsub)
- [Domain Events](#domain-events)
- [Event Sourcing](#event-sourcing)
- [CQRS with Types](#cqrs-with-types)
- [Event Store](#event-store)
- [Event Handlers with Types](#event-handlers-with-types)
- [Interview Questions](#interview-questions)

---

## Typed Event Emitter

```typescript
// Full typed event emitter implementation
type EventMap = Record<string, unknown>;
type EventHandler<T> = (data: T) => void;

class TypedEventEmitter<Events extends EventMap> {
  private handlers = new Map<keyof Events, Set<EventHandler<any>>>();
  private onceHandlers = new Map<keyof Events, Set<EventHandler<any>>>();

  on<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);

    return () => this.off(event, handler);
  }

  once<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
    if (!this.onceHandlers.has(event)) {
      this.onceHandlers.set(event, new Set());
    }
    this.onceHandlers.get(event)!.add(handler);

    return () => this.onceHandlers.get(event)?.delete(handler);
  }

  off<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): void {
    this.handlers.get(event)?.delete(handler);
    this.onceHandlers.get(event)?.delete(handler);
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    // Regular handlers
    this.handlers.get(event)?.forEach((handler) => handler(data));

    // Once handlers (then remove)
    const onceHandlers = this.onceHandlers.get(event);
    if (onceHandlers) {
      onceHandlers.forEach((handler) => handler(data));
      onceHandlers.clear();
    }
  }

  removeAllListeners(event?: keyof Events): void {
    if (event) {
      this.handlers.delete(event);
      this.onceHandlers.delete(event);
    } else {
      this.handlers.clear();
      this.onceHandlers.clear();
    }
  }

  listenerCount(event: keyof Events): number {
    return (
      (this.handlers.get(event)?.size ?? 0) +
      (this.onceHandlers.get(event)?.size ?? 0)
    );
  }
}

// Usage
interface AppEvents {
  "user:created": { id: string; name: string; email: string };
  "user:updated": { id: string; changes: Partial<User> };
  "user:deleted": { id: string };
  "order:placed": { orderId: string; items: string[]; total: number };
  "payment:received": { transactionId: string; amount: number };
}

const emitter = new TypedEventEmitter<AppEvents>();

// Fully typed handlers
emitter.on("user:created", (data) => {
  console.log(data.name); // ✅ TypeScript knows name exists
});

emitter.on("order:placed", (data) => {
  console.log(data.total); // ✅ TypeScript knows total exists
});

// emitter.emit("user:created", { id: "1" }); // ❌ Error: name and email missing
```

---

## Event Bus with Generics

```typescript
// Global event bus
class EventBus<Events extends EventMap> {
  private static instance: EventBus<any>;
  private emitter = new TypedEventEmitter<Events>();

  static getInstance<T extends EventMap>(): EventBus<T> {
    if (!EventBus.instance) {
      EventBus.instance = new EventBus<T>();
    }
    return EventBus.instance as EventBus<T>;
  }

  on<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
    return this.emitter.on(event, handler);
  }

  once<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
    return this.emitter.once(event, handler);
  }

  off<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): void {
    this.emitter.off(event, handler);
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.emitter.emit(event, data);
  }

  // Async event emission with error handling
  async emitAsync<K extends keyof Events>(
    event: K,
    data: Events[K]
  ): Promise<void> {
    const handlers = this.emitter["handlers"].get(event) ?? new Set();
    const onceHandlers = this.emitter["onceHandlers"].get(event) ?? new Set();
    const allHandlers = [...handlers, ...onceHandlers];

    await Promise.allSettled(
      allHandlers.map(async (handler) => {
        try {
          await handler(data);
        } catch (error) {
          console.error(`Error in handler for ${String(event)}:`, error);
        }
      })
    );
  }
}

// Typed event bus usage
interface SystemEvents {
  "app:ready": void;
  "app:error": { error: Error; context: string };
  "data:saved": { entity: string; id: string };
  "user:action": { userId: string; action: string; metadata: Record<string, unknown> };
}

const systemBus = new EventBus<SystemEvents>();

// React hook for typed events
function useEvent<K extends keyof SystemEvents>(
  event: K,
  handler: EventHandler<SystemEvents[K]>
): void {
  useEffect(() => {
    const unsubscribe = systemBus.on(event, handler);
    return unsubscribe;
  }, [event, handler]);
}

// Usage in component
function DataDisplay() {
  const [lastSaved, setLastSaved] = useState<string | null>(null);

  useEvent("data:saved", (data) => {
    setLastSaved(`${data.entity}:${data.id}`);
  });

  return <div>Last saved: {lastSaved}</div>;
}
```

---

## Typed Pub/Sub

```typescript
// Decoupled pub/sub system
interface Subscription {
  unsubscribe(): void;
  closed: boolean;
}

class PubSub<Events extends EventMap> {
  private topics = new Map<keyof Events, Set<(data: any) => void>>();
  private wildcardHandlers = new Set<(event: string, data: unknown) => void>();

  subscribe<K extends keyof Events>(
    topic: K,
    handler: (data: Events[K]) => void
  ): Subscription {
    if (!this.topics.has(topic)) {
      this.topics.set(topic, new Set());
    }
    this.topics.get(topic)!.add(handler);

    return {
      unsubscribe: () => {
        this.topics.get(topic)?.delete(handler);
      },
      closed: false,
    };
  }

  publish<K extends keyof Events>(topic: K, data: Events[K]): void {
    this.topics.get(topic)?.forEach((handler) => handler(data));
    this.wildcardHandlers.forEach((handler) => handler(topic as string, data));
  }

  subscribeAll(handler: (event: string, data: unknown) => void): Subscription {
    this.wildcardHandlers.add(handler);
    return {
      unsubscribe: () => {
        this.wildcardHandlers.delete(handler);
      },
      closed: false,
    };
  }

  // Pattern-based subscription
  subscribePattern(
    pattern: RegExp,
    handler: (event: string, data: unknown) => void
  ): Subscription {
    return this.subscribeAll((event, data) => {
      if (pattern.test(event)) {
        handler(event, data);
      }
    });
  }
}

// Usage
interface OrderEvents {
  "order.created": { orderId: string; items: string[] };
  "order.confirmed": { orderId: string; confirmedAt: Date };
  "order.shipped": { orderId: string; trackingNumber: string };
  "order.delivered": { orderId: string; deliveredAt: Date };
}

const orderPubSub = new PubSub<OrderEvents>();

// Subscribe to specific events
const subscription = orderPubSub.subscribe("order.created", (data) => {
  console.log(`New order: ${data.orderId}`);
});

// Pattern-based subscription
orderPubSub.subscribePattern(/^order\./, (event, data) => {
  console.log(`Order event: ${event}`, data);
});

// Publish events
orderPubSub.publish("order.created", {
  orderId: "123",
  items: ["widget", "gadget"],
});
```

---

## Domain Events

```typescript
// Domain event system
interface DomainEvent<TPayload = unknown> {
  eventId: string;
  eventType: string;
  aggregateId: string;
  aggregateType: string;
  timestamp: Date;
  version: number;
  payload: TPayload;
  metadata?: Record<string, unknown>;
}

// Event factory
function createDomainEvent<TPayload>(
  eventType: string,
  aggregateId: string,
  aggregateType: string,
  payload: TPayload,
  version: number = 1
): DomainEvent<TPayload> {
  return {
    eventId: crypto.randomUUID(),
    eventType,
    aggregateId,
    aggregateType,
    timestamp: new Date(),
    version,
    payload,
  };
}

// Specific domain events
interface UserCreatedEvent extends DomainEvent<{
  name: string;
  email: string;
  role: string;
}> {
  eventType: "UserCreated";
  aggregateType: "User";
}

interface OrderPlacedEvent extends DomainEvent<{
  items: Array<{ productId: string; quantity: number; price: number }>;
  total: number;
}> {
  eventType: "OrderPlaced";
  aggregateType: "Order";
}

// Domain event handler
interface DomainEventHandler<TEvent extends DomainEvent> {
  handle(event: TEvent): Promise<void>;
}

// Aggregate root that emits events
abstract class AggregateRoot {
  private events: DomainEvent[] = [];

  protected addEvent<TPayload>(
    eventType: string,
    payload: TPayload
  ): void {
    const event = createDomainEvent(
      eventType,
      this.id,
      this.constructor.name,
      payload,
      this.version + 1
    );
    this.events.push(event);
    this.version++;
  }

  getUncommittedEvents(): DomainEvent[] {
    return [...this.events];
  }

  clearUncommittedEvents(): void {
    this.events = [];
  }

  abstract id: string;
  version: number = 0;
}

// User aggregate
class User extends AggregateRoot {
  id: string;
  private name: string;
  private email: string;

  constructor(id: string, name: string, email: string) {
    super();
    this.id = id;
    this.name = name;
    this.email = email;
  }

  static create(id: string, name: string, email: string): User {
    const user = new User(id, name, email);
    user.addEvent("UserCreated", { name, email, role: "user" });
    return user;
  }

  updateProfile(name?: string, email?: string): void {
    if (name) this.name = name;
    if (email) this.email = email;
    this.addEvent("UserProfileUpdated", { name, email });
  }
}
```

---

## Event Sourcing

```typescript
// Event sourcing store
class EventStore {
  private events: DomainEvent[] = [];
  private projections = new Map<string, (state: any, event: DomainEvent) => any>();

  append(event: DomainEvent): void {
    this.events.push(event);
    this.projectEvent(event);
  }

  getEvents(aggregateId: string): DomainEvent[] {
    return this.events.filter((e) => e.aggregateId === aggregateId);
  }

  getEventsByType(eventType: string): DomainEvent[] {
    return this.events.filter((e) => e.eventType === eventType);
  }

  getEventsAfter(timestamp: Date): DomainEvent[] {
    return this.events.filter((e) => e.timestamp > timestamp);
  }

  registerProjection<T>(
    name: string,
    reducer: (state: T, event: DomainEvent) => T
  ): void {
    this.projections.set(name, reducer as any);
  }

  private projectEvent(event: DomainEvent): void {
    for (const [, reducer] of this.projections) {
      reducer({}, event);
    }
  }

  // Replay events to rebuild state
  replay<T>(aggregateId: string, reducer: (state: T, event: DomainEvent) => T, initial: T): T {
    return this.getEvents(aggregateId).reduce(reducer, initial);
  }
}

// Event-sourced aggregate
class EventSourcedOrder {
  private state: OrderState = {
    id: "",
    items: [],
    total: 0,
    status: "pending",
  };

  constructor(private eventStore: EventStore) {}

  // Command: produces events
  placeOrder(items: Array<{ productId: string; quantity: number; price: number }>): void {
    const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

    this.eventStore.append(
      createDomainEvent("OrderPlaced", this.state.id, "Order", { items, total })
    );
  }

  // Command: produces events
  confirmOrder(): void {
    if (this.state.status !== "pending") {
      throw new Error("Order is not in pending state");
    }

    this.eventStore.append(
      createDomainEvent("OrderConfirmed", this.state.id, "Order", { confirmedAt: new Date() })
    );
  }

  // Query: reads events
  getState(): OrderState {
    return this.eventStore.replay(
      this.state.id,
      this.reducer.bind(this),
      { id: this.state.id, items: [], total: 0, status: "pending" }
    );
  }

  // Event reducer
  private reducer(state: OrderState, event: DomainEvent): OrderState {
    switch (event.eventType) {
      case "OrderPlaced":
        return { ...state, items: event.payload.items, total: event.payload.total, status: "pending" };
      case "OrderConfirmed":
        return { ...state, status: "confirmed" };
      case "OrderShipped":
        return { ...state, status: "shipped", trackingNumber: event.payload.trackingNumber };
      default:
        return state;
    }
  }
}
```

---

## CQRS with Types

```typescript
// Command Query Responsibility Segregation

// Command side
interface Command<TPayload = void> {
  type: string;
  payload: TPayload;
  timestamp: Date;
  userId: string;
}

interface CommandHandler<TCommand extends Command, TResult = void> {
  execute(command: TCommand): Promise<TResult>;
}

// Query side
interface Query<TParams, TResult> {
  type: string;
  params: TParams;
}

interface QueryHandler<TQuery extends Query<any, any>, TResult> {
  execute(query: TQuery): Promise<TResult>;
}

// CQRS application
class CQRSApplication {
  private commandHandlers = new Map<string, CommandHandler<any>>();
  private queryHandlers = new Map<string, QueryHandler<any, any>>();
  private eventBus = new EventBus<SystemEvents>();

  registerCommandHandler<TCommand extends Command>(
    type: string,
    handler: CommandHandler<TCommand>
  ): void {
    this.commandHandlers.set(type, handler);
  }

  registerQueryHandler<TQuery extends Query<any, any>>(
    type: string,
    handler: QueryHandler<TQuery, any>
  ): void {
    this.queryHandlers.set(type, handler);
  }

  async executeCommand<TCommand extends Command>(
    command: TCommand
  ): Promise<void> {
    const handler = this.commandHandlers.get(command.type);
    if (!handler) throw new Error(`Unknown command: ${command.type}`);
    await handler.execute(command);
  }

  async executeQuery<TQuery extends Query<any, TResult>, TResult>(
    query: TQuery
  ): Promise<TResult> {
    const handler = this.queryHandlers.get(query.type);
    if (!handler) throw new Error(`Unknown query: ${query.type}`);
    return handler.execute(query) as Promise<TResult>;
  }
}

// Command implementations
interface CreateUserCommand extends Command<{ name: string; email: string }> {
  type: "CreateUser";
}

class CreateUserHandler implements CommandHandler<CreateUserCommand> {
  constructor(private userRepo: UserRepository, private eventBus: EventBus<any>) {}

  async execute(command: CreateUserCommand): Promise<void> {
    const user = await this.userRepo.create(command.payload);
    this.eventBus.emit("user:created", { id: user.id, name: user.name, email: user.email });
  }
}

// Query implementations
interface GetUserQuery extends Query<{ id: string }, User | null> {
  type: "GetUser";
}

class GetUserHandler implements QueryHandler<GetUserQuery, User | null> {
  constructor(private userRepo: UserRepository) {}

  async execute(query: GetUserQuery): Promise<User | null> {
    return this.userRepo.findById(query.params.id);
  }
}
```

---

## Event Store

```typescript
// Persistent event store
interface StoredEvent {
  id: string;
  aggregateId: string;
  aggregateType: string;
  eventType: string;
  payload: unknown;
  metadata: Record<string, unknown>;
  timestamp: Date;
  version: number;
}

class PersistentEventStore {
  private events: StoredEvent[] = [];

  async append(event: DomainEvent): Promise<void> {
    const storedEvent: StoredEvent = {
      id: event.eventId,
      aggregateId: event.aggregateId,
      aggregateType: event.aggregateType,
      eventType: event.eventType,
      payload: event.payload,
      metadata: event.metadata ?? {},
      timestamp: event.timestamp,
      version: event.version,
    };

    this.events.push(storedEvent);
  }

  async getEvents(aggregateId: string, fromVersion?: number): Promise<StoredEvent[]> {
    return this.events
      .filter((e) =>
        e.aggregateId === aggregateId &&
        (fromVersion === undefined || e.version > fromVersion)
      )
      .sort((a, b) => a.version - b.version);
  }

  async getEventsByType(eventType: string): Promise<StoredEvent[]> {
    return this.events.filter((e) => e.eventType === eventType);
  }

  async getEventsAfter(timestamp: Date): Promise<StoredEvent[]> {
    return this.events.filter((e) => e.timestamp >= timestamp);
  }

  async getSnapshot(aggregateId: string): Promise<StoredEvent | null> {
    const events = await this.getEvents(aggregateId);
    return events.length > 0 ? events[events.length - 1] : null;
  }

  async subscribe(eventType: string, handler: (event: StoredEvent) => Promise<void>): Promise<() => void> {
    // Real implementation would use a message queue
    return () => {};
  }
}
```

---

## Event Handlers with Types

```typescript
// Typed event handler registry
class EventHandlerRegistry {
  private handlers = new Map<string, Array<(event: any) => Promise<void>>>();

  register<T>(
    eventType: string,
    handler: (event: DomainEvent<T>) => Promise<void>
  ): void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }
    this.handlers.get(eventType)!.push(handler);
  }

  async handle(event: DomainEvent): Promise<void> {
    const handlers = this.handlers.get(event.eventType) ?? [];
    await Promise.allSettled(
      handlers.map(async (handler) => {
        try {
          await handler(event);
        } catch (error) {
          console.error(`Error handling event ${event.eventType}:`, error);
        }
      })
    );
  }

  async handleWithRetry(
    event: DomainEvent,
    maxRetries: number = 3
  ): Promise<void> {
    const handlers = this.handlers.get(event.eventType) ?? [];

    for (const handler of handlers) {
      let attempt = 0;
      while (attempt < maxRetries) {
        try {
          await handler(event);
          break;
        } catch (error) {
          attempt++;
          if (attempt >= maxRetries) {
            console.error(
              `Failed to handle event ${event.eventType} after ${maxRetries} attempts:`,
              error
            );
          } else {
            await new Promise((r) => setTimeout(r, 1000 * attempt));
          }
        }
      }
    }
  }
}

// Usage
const registry = new EventHandlerRegistry();

registry.register<{ name: string; email: string }>(
  "UserCreated",
  async (event) => {
    console.log(`Sending welcome email to ${event.payload.email}`);
  }
);

registry.register<{ orderId: string }>(
  "OrderPlaced",
  async (event) => {
    console.log(`Processing order ${event.payload.orderId}`);
  }
);
```

---

## Interview Questions

1. **What is event-driven architecture?**
   A design pattern where components communicate through events rather than direct method calls, promoting loose coupling.

2. **What is the difference between events and commands?**
   Events are notifications that something happened. Commands are requests to do something. Events are broadcast; commands are directed.

3. **What is event sourcing?**
   A pattern where state changes are stored as a sequence of events rather than current state, enabling replay and audit.

4. **What is CQRS?**
   Command Query Responsibility Segregation - separating read and write models for better scalability and performance.

5. **What is an event store?**
   A persistence layer for events that supports append, query, and subscription operations.

6. **How do you handle event versioning?**
   Use event upcasting, upcasters, or store multiple versions of events with migration logic.

7. **What is eventual consistency?**
   A consistency model where all nodes will eventually have the same data, but not immediately. Common in event-driven systems.

8. **What are domain events?**
   Events that represent significant business occurrences within a domain, like OrderPlaced or UserRegistered.

9. **How do you handle event ordering?**
   Use sequence numbers, timestamps, or partitioning strategies. Some systems guarantee per-aggregate ordering.

10. **What are the challenges of event-driven architecture?**
    Eventual consistency, debugging complexity, event versioning, and ensuring idempotent handlers.
