# Advanced Patterns Interview Questions

## Table of Contents
1. [API Versioning](#api-versioning)
2. [HATEOAS](#hateoas)
3. [CQRS](#cqrs)
4. [Event Sourcing](#event-sourcing)
5. [Saga Pattern](#saga-pattern)
6. [Plugin Architecture](#plugin-architecture)
7. [Trade-offs & Real-World Examples](#trade-offs--real-world-examples)

---

## API Versioning

### Q1: What are the different API versioning strategies?
**Answer:** URL versioning (`/v1/`, `/v2/`), header versioning (`API-Version: 1`), query parameter versioning (`?v=1`), and media type versioning (`Accept: application/vnd.api.v2+json`). URL versioning is most common because it's visible and cacheable. Header versioning keeps URLs clean.

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users")
async def get_users_v1():
    return {"users": [{"id": 1, "name": "John"}]}

@v2_router.get("/users")
async def get_users_v2():
    return {"data": [{"id": 1, "name": "John", "email": "john@example.com"}]}

app.include_router(v1_router)
app.include_router(v2_router)
```

```python
@app.middleware("http")
async def version_middleware(request: Request, call_next):
    version = request.headers.get("API-Version", "1")
    request.state.api_version = int(version)
    response = await call_next(request)
    response.headers["API-Version"] = version
    return response
```

### Q2: When should you create a new API version?
**Answer:** Create a new version for breaking changes: removing fields, changing data types, modifying authentication, or altering URL structure. Don't version for non-breaking changes like adding new endpoints, optional fields, or optional query parameters.

**Breaking changes that require versioning:** Removing or renaming response fields, changing field types, modifying authentication mechanisms, changing URL structure, altering error response format, changing business logic semantics.

**Non-breaking changes (no versioning needed):** Adding new optional query parameters, adding new response fields, adding new endpoints, adding new HTTP methods, adding new headers.

### Q3: How do you handle deprecation of an old API version?
**Answer:** Set `Deprecation` and `Sunset` HTTP headers, document a migration guide, notify consumers, monitor usage to identify remaining consumers, set a removal timeline (3-6 months), and return `410 Gone` after removal.

```python
from datetime import datetime

@app.middleware("http")
async def deprecation_middleware(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/api/v1/"):
        sunset_date = datetime(2025, 6, 1)
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = sunset_date.strftime("%a, %d %b %Y")
        response.headers["Link"] = '</api/v2/docs>; rel="successor-version"'
    return response
```

### Q4: How do you implement API versioning with FastAPI routers efficiently?
**Answer:** Use nested routers with version prefixes and share common dependencies:

```python
from fastapi import APIRouter, Depends

async def common_auth():
    return await verify_token()

v1 = APIRouter(prefix="/api/v1", dependencies=[Depends(common_auth)])
v2 = APIRouter(prefix="/api/v2", dependencies=[Depends(common_auth)])

@v1.get("/orders")
async def list_orders_v1():
    return {"orders": []}

@v2.get("/orders")
async def list_orders_v2():
    return {"data": [], "pagination": {"page": 1, "total": 0}}
```

### Q5: How do you version API response schemas without breaking clients?
**Answer:** Use Pydantic models with optional fields and field-level versioning. Return new fields alongside old ones. Use response_model_include/exclude to control which fields are visible per version. Migrate clients gradually by making new fields optional first.

```python
from pydantic import BaseModel, Field

class UserResponseV1(BaseModel):
    id: int
    name: str

class UserResponseV2(UserResponseV1):
    email: str = Field(..., description="Added in v2")
    preferences: dict = Field(default_factory=dict, description="Added in v2")

@app.get("/api/v1/users/{user_id}", response_model=UserResponseV1)
async def get_user_v1(user_id: int):
    user = await db.get(User, user_id)
    return user

@app.get("/api/v2/users/{user_id}", response_model=UserResponseV2)
async def get_user_v2(user_id: int):
    user = await db.get(User, user_id)
    return user
```

---

## HATEOAS

### Q6: What is HATEOAS and why does it matter?
**Answer:** HATEOAS (Hypermedia As The Engine Of Application State) means responses include links that tell clients what actions are available. The client discovers available actions from the response rather than hardcoding URLs. This decouples client and server, allowing the server to change URLs without breaking clients.

```python
def build_order_links(order) -> list[dict]:
    links = [{"href": f"/api/orders/{order.id}", "rel": "self"}]

    if order.status == "pending":
        links.append({"href": f"/api/orders/{order.id}/cancel", "method": "POST", "rel": "cancel"})
        links.append({"href": f"/api/orders/{order.id}/pay", "method": "POST", "rel": "pay"})
    elif order.status == "paid":
        links.append({"href": f"/api/orders/{order.id}/ship", "method": "POST", "rel": "ship"})
    elif order.status == "shipped":
        links.append({"href": f"/api/orders/{order.id}/track", "rel": "track"})

    return links

@app.get("/api/orders/{order_id}")
async def get_order(order_id: str):
    order = await db.get(Order, order_id)
    return {"id": order.id, "status": order.status, "total": order.total, "_links": build_order_links(order)}
```

### Q7: When is HATEOAS worth the implementation cost?
**Answer:** HATEOAS is worth it when API consumers are external and you need to evolve URLs without breaking clients, when you have complex workflows with state-dependent actions (order processing, approval chains), or for hypermedia-driven applications. It is NOT worth it for simple CRUD APIs, internal APIs where clients are tightly coupled, performance-critical APIs where link overhead matters, or when teams lack discipline to maintain link relations.

### Q8: What is HAL format and how do you implement it in FastAPI?
**Answer:** HAL (Hypertext Application Language) is a simple format for hypermedia APIs. Resources include `_links` (for navigation) and `_embedded` (for related resources).

```python
@app.get("/api/orders")
async def list_orders_hal(page: int = 1, size: int = 10):
    orders = await get_orders(page=page, size=size)
    total = await count_orders()
    return {
        "_links": {
            "self": {"href": f"/api/orders?page={page}&size={size}"},
            "next": {"href": f"/api/orders?page={page+1}&size={size}"} if page * size < total else None,
            "prev": {"href": f"/api/orders?page={page-1}&size={size}"} if page > 1 else None,
        },
        "count": total,
        "_embedded": {"orders": [order_to_dict(o) for o in orders]},
    }
```

---

## CQRS

### Q9: What is CQRS and when should you use it?
**Answer:** CQRS (Command Query Responsibility Segregation) separates read and write operations into different models. Use it when read and write workloads have different scaling needs, when read models need denormalization, or when multiple consumers need different data views. Don't use it for simple CRUD applications.

```python
# Write side (commands)
class CreateOrderCommand(BaseModel):
    user_id: str
    items: list[OrderItem]
    total: float

async def handle_create_order(cmd: CreateOrderCommand):
    order = Order(id=str(uuid.uuid4()), user_id=cmd.user_id, items=cmd.items, total=cmd.total, status="pending")
    await write_db.insert(order)
    await event_bus.publish(OrderCreatedEvent(order_id=order.id))

# Read side (queries) - denormalized view
@app.get("/api/orders/{order_id}")
async def get_order(order_id: str):
    return await read_db.get(OrderView, order_id)
```

### Q10: How does CQRS handle eventual consistency?
**Answer:** When a write occurs, it updates the write database and publishes an event. The read model is updated asynchronously. During propagation, reads may return stale data. Mitigate with read-your-writes patterns, version vectors, or waiting for projection completion.

```python
@app.post("/api/orders")
async def create_order(cmd: CreateOrderCommand):
    order = await handle_create_order(cmd)
    # Option 1: Return write model directly (no eventual consistency issue)
    return {"id": order.id, "status": order.status}
    # Option 2: Wait for read model projection
    # await wait_for_projection(order.id, timeout=1.0)
    # return await read_db.get(OrderView, order.id)
```

### Q11: What are the infrastructure requirements for CQRS?
**Answer:** Separate read and write databases (or schemas), an event bus (Redis, RabbitMQ, Kafka), and a read-optimized store (Elasticsearch, materialized views). Also add monitoring for projection lag, dead letter queues, and event replay capability.

### Q12: How do you handle read model lag in CQRS?
**Answer:** Monitor projection lag with metrics. Implement read-your-writes by checking if the read model is up-to-date before returning. For critical operations, read from the write model. Use synchronous projections for consistency-critical paths, async for everything else.

```python
@app.get("/api/orders/{order_id}")
async def get_order(order_id: str, request: Request):
    write_version = await write_db.get_version(order_id)
    read_version = await read_db.get_version(order_id)
    if write_version > read_version:
        wait = request.query_params.get("wait", "false") == "true"
        if wait:
            await wait_for_projection(order_id, timeout=2.0)
        else:
            order = await read_db.get(OrderView, order_id)
            return {**order.dict(), "_stale": True, "_write_version": write_version}
    return await read_db.get(OrderView, order_id)
```

---

## Event Sourcing

### Q13: What is event sourcing and how does it differ from CRUD?
**Answer:** Event sourcing stores every state change as an immutable event. CRUD overwrites current state. Event sourcing preserves complete history, enables temporal queries, and supports event replay. CRUD is simpler but loses history.

```python
class OrderAggregate:
    def __init__(self):
        self.id = None
        self.status = None
        self.items = []
        self.total = 0
        self.version = 0

    def apply(self, event):
        if event.event_type == "OrderCreated":
            self.id = event.data["order_id"]
            self.status = "pending"
            self.items = event.data["items"]
            self.total = event.data["total"]
        elif event.event_type == "OrderPaid":
            self.status = "paid"
        elif event.event_type == "OrderShipped":
            self.status = "shipped"
        self.version = event.version

    @classmethod
    def from_events(cls, events):
        aggregate = cls()
        for event in events:
            aggregate.apply(event)
        return aggregate
```

### Q14: What are snapshots in event sourcing?
**Answer:** Snapshots capture aggregate state at a point in time to avoid replaying all events. Use them when aggregates have many events. Create snapshots periodically (e.g., every 100 events) and load from snapshot + subsequent events.

```python
class SnapshotStore:
    async def save_snapshot(self, aggregate_id: str, state: dict, version: int):
        await redis.hset(f"snapshot:{aggregate_id}", mapping={"state": json.dumps(state), "version": version})

    async def load_snapshot(self, aggregate_id: str):
        data = await redis.hgetall(f"snapshot:{aggregate_id}")
        if data:
            return json.loads(data[b"state"]), int(data[b"version"])
        return None, 0

async def load_aggregate(aggregate_id: str):
    snapshot, snapshot_version = await snapshot_store.load_snapshot(aggregate_id)
    if snapshot:
        aggregate = OrderAggregate.from_snapshot(snapshot)
        events = await event_store.get_events(aggregate_id, after_version=snapshot_version)
    else:
        aggregate = OrderAggregate()
        events = await event_store.get_events(aggregate_id)
    for event in events:
        aggregate.apply(event)
    if aggregate.version - snapshot_version > 100:
        await snapshot_store.save_snapshot(aggregate_id, aggregate.to_dict(), aggregate.version)
    return aggregate
```

### Q15: How do you handle event schema evolution?
**Answer:** Use upcasters to transform old schemas. Add optional fields with defaults. Never remove or rename fields. Use versioned event types. For breaking changes, create new event types rather than modifying existing ones.

```python
EVENT_UPCASTERS = {
    ("OrderCreated", 1): lambda data: data,
    ("OrderCreated", 2): lambda data: {
        "order_id": data["order_id"], "user_id": data["user_id"],
        "items": data["items"], "total": data["total"],
        "currency": data.get("currency", "USD"),
    },
}

def upcast_event(event_type: str, version: int, data: dict) -> dict:
    upcaster = EVENT_UPCASTERS.get((event_type, version))
    if upcaster:
        return upcaster(data)
    raise ValueError(f"No upcaster for {event_type} v{version}")
```

### Q16: What is an aggregate root and why is it important?
**Answer:** An aggregate root is a consistency boundary that groups related entities. It enforces business rules, produces events, and maintains its own version. Events are applied to build current state. The aggregate root is the only entry point for modifying the aggregate.

```python
class OrderAggregate:
    def __init__(self):
        self.id = None
        self.status = None
        self.items = []
        self.total = 0
        self.version = 0
        self.pending_events = []

    def add_item(self, item):
        if self.status != "pending":
            raise ValueError("Cannot modify a non-pending order")
        self.items.append(item)
        self.total += item.price
        self.pending_events.append(Event(event_type="OrderItemAdded", data={"item": item.dict()}, version=self.version + 1))

    def cancel(self):
        if self.status not in ("pending", "paid"):
            raise ValueError(f"Cannot cancel order in status {self.status}")
        self.status = "cancelled"
        self.pending_events.append(Event(event_type="OrderCancelled", data={"reason": "user_cancelled"}, version=self.version + 1))

    async def save(self):
        for event in self.pending_events:
            await event_store.append(self.id, event)
        self.pending_events.clear()
```

### Q17: How do you handle version conflicts in event sourcing?
**Answer:** Use optimistic concurrency control. Each aggregate has a version number. When appending events, check that the expected version matches the current version. If there's a conflict, retry the operation. This prevents lost updates in concurrent scenarios.

```python
async def append_events(aggregate_id: str, events: list[Event], expected_version: int):
    current_version = await event_store.get_version(aggregate_id)
    if current_version != expected_version:
        raise ConcurrencyConflict(f"Expected version {expected_version}, got {current_version}")
    for event in events:
        await event_store.append(aggregate_id, event)
```

---

## Saga Pattern

### Q18: What is the saga pattern?
**Answer:** The saga pattern manages distributed transactions by breaking them into a sequence of local transactions. Each step has a compensating transaction. If a later step fails, earlier steps are compensated in reverse order.

```python
class OrderSaga:
    def __init__(self):
        self.steps = [
            SagaStep(action=self.reserve_inventory, compensate=self.release_inventory),
            SagaStep(action=self.process_payment, compensate=self.refund_payment),
            SagaStep(action=self.ship_order, compensate=self.cancel_shipment),
        ]

    async def execute(self, order_id: str):
        completed_steps = []
        for step in self.steps:
            try:
                await step.action(order_id)
                completed_steps.append(step)
            except Exception as e:
                for completed in reversed(completed_steps):
                    try:
                        await completed.compensate(order_id)
                    except Exception as comp_error:
                        logger.error(f"Compensation failed: {comp_error}")
                raise SagaFailed(f"Saga failed at step: {e}")
```

### Q19: What is the difference between choreography and orchestration sagas?
**Answer:** Choreography: Services publish and react to events. No central coordinator. Loose coupling but hard to trace. Orchestration: A central coordinator directs steps. Easier to understand but introduces a single point of failure.

```python
# Choreography - each service reacts to events
@app.post("/events/order-created")
async def on_order_created(event):
    await reserve_inventory(event.order_id)
    await event_bus.publish(InventoryReservedEvent(order_id=event.order_id))

# Orchestration - central coordinator
class OrderOrchestrator:
    async def execute(self, order_id):
        await self.step1_reserve_inventory(order_id)
        await self.step2_process_payment(order_id)
        await self.step3_ship_order(order_id)
```

### Q20: How do compensating transactions work?
**Answer:** They're the inverse of forward transactions. If step 3 fails, execute compensating transactions for steps 2 and 1 in reverse order. They must be idempotent and handle cases where compensation itself fails.

```python
async def compensate_payment(self, payment_id):
    payment = await db.get(Payment, payment_id)
    if payment.status == "refunded":
        return  # Already compensated (idempotent)
    if payment.status == "charged":
        await payment_gateway.refund(payment.external_id)
        payment.status = "refunded"
        await db.update(payment)
```

### Q21: What is the outbox pattern?
**Answer:** The outbox pattern ensures atomic database writes and event publishing. Write events to an outbox table in the same transaction as business data. A separate process publishes events. Prevents inconsistency where DB is updated but event isn't published.

```python
async def create_order_with_outbox(order_data: dict):
    async with db.transaction() as tx:
        order = Order(**order_data)
        await tx.insert(order)
        outbox_event = OutboxEvent(aggregate_type="Order", aggregate_id=order.id, event_type="OrderCreated", payload=json.dumps(order.dict()), created_at=datetime.utcnow())
        await tx.insert(outbox_event)
```

### Q22: How do you ensure idempotency in distributed systems?
**Answer:** Use idempotency keys (UUIDs) sent with requests. Store processed keys with TTL. Before processing, check if the key exists. Return cached result if duplicate. Prevents duplicate processing during retries.

```python
async def idempotent_handler(idempotency_key, handler_func, *args, **kwargs):
    cached = await redis.get(f"idempotent:{idempotency_key}")
    if cached:
        return json.loads(cached)
    result = await handler_func(*args, **kwargs)
    await redis.setex(f"idempotent:{idempotency_key}", 86400, json.dumps(result))
    return result
```

---

## Plugin Architecture

### Q23: What is a plugin architecture and when should you use one?
**Answer:** A plugin architecture allows extending an application through self-contained modules without modifying core code. Use it when you need extensibility, third-party integrations, or modularity. Common for analytics, payment gateways, and authentication providers.

```python
from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod
    def get_name(self) -> str: pass

    @abstractmethod
    async def on_startup(self, app: FastAPI): pass

    @abstractmethod
    async def on_shutdown(self, app: FastAPI): pass

class PluginManager:
    def __init__(self):
        self.plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin):
        self.plugins[plugin.get_name()] = plugin

    async def startup(self, app: FastAPI):
        for name, plugin in self.plugins.items():
            await plugin.on_startup(app)
            logger.info(f"Plugin {name} started")

    async def shutdown(self, app: FastAPI):
        for name, plugin in reversed(list(self.plugins.items())):
            await plugin.on_shutdown(app)
```

### Q24: How do you handle plugin dependencies?
**Answer:** Use topological sorting based on declared dependencies. Each plugin declares what it depends on. The plugin manager resolves loading and initialization order. Detect and fail on circular dependencies.

```python
class PluginManager:
    def resolve_load_order(self):
        graph = {name: set(p.get_dependencies()) for name, p in self.plugins.items()}
        visited = set()
        path = []
        sorted_nodes = []

        def dfs(node):
            if node in path:
                raise CircularDependencyError(f"Circular dependency: {node}")
            if node in visited:
                return
            visited.add(node)
            path.append(node)
            for dep in graph.get(node, []):
                dfs(dep)
            path.pop()
            sorted_nodes.append(node)

        for node in graph:
            dfs(node)
        return [self.plugins[name] for name in sorted_nodes]
```

### Q25: How do you isolate plugins from each other?
**Answer:** Use dependency injection for separate database sessions, configurations, and state. Use separate route namespaces. Use events for inter-plugin communication instead of direct imports. Each plugin should be self-contained.

```python
class AnalyticsPlugin(Plugin):
    def get_name(self): return "analytics"

    async def on_startup(self, app):
        self.db = await create_analytics_db()
        router = APIRouter(prefix="/analytics")

        @router.get("/events")
        async def get_events():
            return await self.db.query(AnalyticsEvent)

        app.include_router(router)
        event_bus.subscribe("order.created", self.track_order)
```

### Q26: How do you implement hot-reloading of plugins?
**Answer:** Monitor plugin directories for changes. When a plugin file changes, unload the old plugin, reload the new version, and re-register. Use importlib for dynamic imports. Handle state migration between versions.

---

## Trade-offs & Real-World Examples

### Q27: When would you use event sourcing + CQRS together?
**Answer:** Use both when you need complete audit trails, temporal queries, and different read models for different consumers. The write side stores events (event sourcing), and the read side builds projections from those events (CQRS). Common in financial systems, healthcare, and compliance-heavy domains.

### Q28: How do you test a saga with compensating transactions?
**Answer:** Test each step independently. Test the happy path (all steps succeed). Test failure at each step and verify compensations execute in correct order. Test compensation failures. Use integration tests with real services or mock the service boundaries.

```python
@pytest.mark.asyncio
async def test_saga_compensates_on_payment_failure():
    saga = OrderSaga()
    with patch.object(saga, "process_payment", side_effect=PaymentError("Card declined")):
        with patch.object(saga, "release_inventory") as mock_release:
            with pytest.raises(SagaFailed):
                await saga.execute("order-123")
            mock_release.assert_called_once_with("order-123")
```

### Q29: What are the trade-offs of event sourcing?
**Answer:** Advantages: Complete audit trail, temporal queries, event replay, natural fit for CQRS. Disadvantages: Complexity, eventual consistency, event schema evolution challenges, harder debugging, requires infrastructure (event store, projections). Don't use for simple CRUD apps.

### Q30: How do you debug a distributed saga?
**Answer:** Use correlation IDs to trace requests across services. Log each step and compensation. Maintain a saga execution log showing status of each step. Use distributed tracing (OpenTelemetry, Jaeger) to visualize the flow. Implement saga status endpoints for monitoring.

```python
class SagaExecutionLog:
    async def log_step(self, saga_id: str, step_name: str, status: str, error: str = None):
        await redis.hset(f"saga:{saga_id}:steps", step_name, json.dumps({
            "status": status, "timestamp": datetime.utcnow().isoformat(), "error": error,
        }))

    async def get_saga_status(self, saga_id: str) -> dict:
        steps = await redis.hgetall(f"saga:{saga_id}:steps")
        return {k.decode(): json.loads(v.decode()) for k, v in steps.items()}
```
