# Saga Pattern for FastAPI

## Table of Contents
1. [What is the Saga Pattern](#what-is)
2. [Choreography vs Orchestration](#choreography-orchestration)
3. [Compensating Transactions](#compensating)
4. [Saga with FastAPI](#fastapi)
5. [Distributed Transactions](#distributed)
6. [Idempotency](#idempotency)

---

## What is the Saga Pattern <a name="what-is"></a>

The saga pattern manages distributed transactions across multiple services by breaking them into a sequence of local transactions. Each step has a compensating transaction that undoes its effect if a later step fails.

### Problem: Distributed Transactions

```
Scenario: Place an order
  1. Create order in Order Service
  2. Reserve inventory in Inventory Service
  3. Process payment in Payment Service
  4. Update user balance in Account Service

What if step 3 fails?
  - Order was created
  - Inventory was reserved
  - Payment failed
  - Need to undo steps 1 and 2
```

### Saga Solution

```
Forward transactions:
  T1: Create order → T2: Reserve inventory → T3: Process payment → T4: Confirm order

Compensating transactions (on failure):
  If T3 fails: C2: Release inventory → C1: Cancel order

Saga execution:
  T1 → T2 → T3 (FAIL) → C2 → C1 → Saga failed

  T1 → T2 → T3 → T4 (SUCCESS) → Saga completed
```

---

## Choreography vs Orchestration <a name="choreography-orchestration"></a>

### Choreography (Event-Driven)

Each service publishes events and reacts to events from other services. No central coordinator.

```
Order Service:
  1. Create order → Publish "OrderCreated"

Inventory Service (listens to "OrderCreated"):
  2. Reserve inventory → Publish "InventoryReserved"

Payment Service (listens to "InventoryReserved"):
  3. Process payment → Publish "PaymentProcessed"

Order Service (listens to "PaymentProcessed"):
  4. Confirm order → Publish "OrderConfirmed"

On failure (e.g., PaymentService fails):
  Payment Service → Publish "PaymentFailed"
  Inventory Service (listens) → Release inventory → Publish "InventoryReleased"
  Order Service (listens) → Cancel order → Publish "OrderCancelled"
```

### Orchestration (Central Coordinator)

A central saga orchestrator directs each step and handles failures.

```
Saga Orchestrator:
  1. Tell Order Service to create order
  2. Tell Inventory Service to reserve inventory
  3. Tell Payment Service to process payment
  4. Tell Order Service to confirm order

On failure (step 3 fails):
  Orchestrator:
    3a. Tell Inventory Service to release inventory (compensate step 2)
    3b. Tell Order Service to cancel order (compensate step 1)
```

### Comparison

| Aspect | Choreography | Orchestration |
|--------|-------------|---------------|
| Coupling | Loose (events) | Tighter (direct calls) |
| Complexity | Distributed, hard to trace | Centralized, easier to understand |
| Single Point of Failure | No | Yes (orchestrator) |
| Transaction Visibility | Hard to see full flow | Easy to see in orchestrator |
| Performance | No single bottleneck | Orchestrator can be bottleneck |
| Testing | Hard to test end-to-end | Easier to test orchestrator |

---

## Compensating Transactions <a name="compensating"></a>

```python
# Each step defines its own compensating action
class SagaStep:
    def __init__(self, name: str, execute: Callable, compensate: Callable):
        self.name = name
        self.execute = execute
        self.compensate = compensate

# Order saga steps
create_order_step = SagaStep(
    name="create_order",
    execute=lambda data: order_service.create(data),
    compensate=lambda order_id: order_service.cancel(order_id),
)

reserve_inventory_step = SagaStep(
    name="reserve_inventory",
    execute=lambda data: inventory_service.reserve(data),
    compensate=lambda reservation_id: inventory_service.release(reservation_id),
)

process_payment_step = SagaStep(
    name="process_payment",
    execute=lambda data: payment_service.charge(data),
    compensate=lambda payment_id: payment_service.refund(payment_id),
)

confirm_order_step = SagaStep(
    name="confirm_order",
    execute=lambda order_id: order_service.confirm(order_id),
    compensate=lambda order_id: None,  # No compensation needed
)
```

---

## Saga with FastAPI <a name="fastapi"></a>

### Saga Orchestrator

```python
# app/saga/orchestrator.py
from typing import Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class SagaStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

class SagaStep:
    def __init__(
        self,
        name: str,
        execute: Callable[..., Any],
        compensate: Callable[..., Any],
    ):
        self.name = name
        self.execute = execute
        self.compensate = compensate

class SagaResult:
    def __init__(self, saga_id: str, status: SagaStatus):
        self.saga_id = saga_id
        self.status = status
        self.results: dict[str, Any] = {}
        self.error: str | None = None

class SagaOrchestrator:
    def __init__(self):
        self._sagas: dict[str, list[SagaStep]] = {}

    def register_saga(self, name: str, steps: list[SagaStep]):
        self._sagas[name] = steps

    async def execute(self, saga_name: str, initial_data: dict) -> SagaResult:
        steps = self._sagas.get(saga_name)
        if not steps:
            raise ValueError(f"Unknown saga: {saga_name}")

        saga_id = str(uuid.uuid4())
        result = SagaResult(saga_id, SagaStatus.RUNNING)
        completed_steps: list[tuple[SagaStep, Any]] = []

        logger.info(f"Starting saga {saga_name} [{saga_id}]")

        try:
            data = initial_data
            for step in steps:
                logger.info(f"Executing step: {step.name}")
                step_result = await step.execute(data)
                completed_steps.append((step, step_result))
                result.results[step.name] = step_result

                # Pass result to next step
                if isinstance(step_result, dict):
                    data = {**data, **step_result}
                else:
                    data["step_result"] = step_result

            result.status = SagaStatus.COMPLETED
            logger.info(f"Saga {saga_name} [{saga_id}] completed")

        except Exception as e:
            logger.error(f"Saga {saga_name} [{saga_id}] failed at step: {step.name}")
            result.status = SagaStatus.COMPENSATING
            result.error = str(e)

            # Compensate in reverse order
            for completed_step, step_result in reversed(completed_steps):
                try:
                    logger.info(f"Compensating step: {completed_step.name}")
                    await completed_step.compensate(step_result)
                except Exception as comp_error:
                    logger.error(
                        f"Compensation failed for {completed_step.name}: {comp_error}"
                    )
                    # Log but continue with other compensations

            result.status = SagaStatus.FAILED

        return result

# Global orchestrator
saga_orchestrator = SagaOrchestrator()
```

### Order Saga

```python
# app/sagas/order_saga.py
from app.saga.orchestrator import SagaStep, saga_orchestrator

async def create_order(data: dict) -> dict:
    order = await order_service.create(
        user_id=data["user_id"],
        items=data["items"],
    )
    return {"order_id": order.id}

async def cancel_order(order_id: int) -> None:
    await order_service.cancel(order_id)

async def reserve_inventory(data: dict) -> dict:
    reservation = await inventory_service.reserve(
        items=data["items"],
        order_id=data["order_id"],
    )
    return {"reservation_id": reservation.id}

async def release_inventory(reservation_id: int) -> None:
    await inventory_service.release(reservation_id)

async def process_payment(data: dict) -> dict:
    payment = await payment_service.charge(
        user_id=data["user_id"],
        amount=data["total"],
        order_id=data["order_id"],
    )
    return {"payment_id": payment.id}

async def refund_payment(payment_id: int) -> None:
    await payment_service.refund(payment_id)

async def confirm_order(data: dict) -> dict:
    await order_service.confirm(data["order_id"])
    return {"confirmed": True}

# Register the saga
saga_orchestrator.register_saga("place_order", [
    SagaStep("create_order", create_order, cancel_order),
    SagaStep("reserve_inventory", reserve_inventory, release_inventory),
    SagaStep("process_payment", process_payment, refund_payment),
    SagaStep("confirm_order", confirm_order, lambda _: None),
])
```

### FastAPI Endpoint

```python
# app/routers/orders.py
from fastapi import APIRouter, BackgroundTasks

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/", status_code=202)
async def place_order(
    command: PlaceOrderCommand,
    background_tasks: BackgroundTasks,
):
    # Execute saga asynchronously
    result = await saga_orchestrator.execute("place_order", {
        "user_id": command.user_id,
        "items": command.items,
        "total": sum(item["price"] * item["quantity"] for item in command.items),
    })

    if result.status == SagaStatus.COMPLETED:
        return {
            "saga_id": result.saga_id,
            "status": "completed",
            "order_id": result.results["create_order"]["order_id"],
        }
    else:
        return JSONResponse(
            status_code=422,
            content={
                "saga_id": result.saga_id,
                "status": "failed",
                "error": result.error,
            }
        )
```

---

## Distributed Transactions <a name="distributed"></a>

### Two-Phase Commit (2PC) vs Saga

```
2PC (Two-Phase Commit):
  Phase 1 (Prepare): All services prepare but don't commit
  Phase 2 (Commit): All services commit

  Pros: Strong consistency
  Cons: Blocking, single point of failure, poor performance

Saga:
  Each step commits immediately
  Compensating transactions handle failures

  Pros: Non-blocking, better performance, eventual consistency
  Cons: Eventual consistency, complex compensation logic
```

### Outbox Pattern

```python
# Ensure events are published atomically with database writes
class OutboxPattern:
    async def execute_with_outbox(self, session: AsyncSession, operation: Callable):
        # 1. Execute business operation
        result = await operation(session)

        # 2. Write event to outbox table (same transaction)
        outbox_entry = OutboxEntry(
            aggregate_type="order",
            aggregate_id=result["order_id"],
            event_type="order.created",
            payload=json.dumps(result),
            created_at=datetime.utcnow(),
        )
        session.add(outbox_entry)

        # 3. Commit (both business data and event are atomic)
        await session.commit()

        # 4. Publish event (separate process)
        await self.publish_outbox_events()

    async def publish_outbox_events(self):
        async with outbox_session() as session:
            entries = await session.execute(
                select(OutboxEntry).where(OutboxEntry.published == False)
            )
            for entry in entries.scalars():
                await event_bus.publish(entry.event_type, entry.payload)
                entry.published = True
            await session.commit()
```

---

## Idempotency <a name="idempotency"></a>

Idempotency ensures that retrying an operation produces the same result as executing it once.

```python
# app/saga/idempotency.py
import hashlib

class IdempotencyKey:
    def __init__(self, operation: str, **params):
        key_string = f"{operation}:{json.dumps(params, sort_keys=True)}"
        self.key = hashlib.sha256(key_string.encode()).hexdigest()

class IdempotencyStore:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def is_duplicate(self, key: IdempotencyKey) -> bool:
        result = await self.redis.setnx(f"idempotent:{key.key}", "1")
        if not result:
            return True  # Duplicate
        await self.redis.expire(f"idempotent:{key.key}", 86400)  # 24h TTL
        return False

# Usage in saga steps
async def process_payment(data: dict) -> dict:
    key = IdempotencyKey(
        "process_payment",
        user_id=data["user_id"],
        order_id=data["order_id"],
        amount=data["total"],
    )
    if await idempotency_store.is_duplicate(key):
        logger.info(f"Duplicate payment detected for order {data['order_id']}")
        return {"payment_id": "existing", "duplicate": True}

    payment = await payment_service.charge(...)
    return {"payment_id": payment.id}
```

### Idempotent API Endpoints

```python
from fastapi import Header
from typing import Annotated

@router.post("/payments", status_code=201)
async def create_payment(
    command: CreatePaymentCommand,
    idempotency_key: Annotated[str | None, Header()] = None,
):
    if idempotency_key:
        key = IdempotencyKey("create_payment", **command.model_dump())
        if await idempotency_store.is_duplicate(key):
            existing = await payment_service.find_by_idempotency_key(idempotency_key)
            return existing

    payment = await payment_service.create(command)
    if idempotency_key:
        await payment_service.set_idempotency_key(payment.id, idempotency_key)
    return payment
```

---

## Interview Questions

1. **What is the saga pattern and when would you use it?**
The saga pattern manages distributed transactions by breaking them into a sequence of local transactions, each with a compensating transaction. Use it when you need to maintain consistency across multiple services without distributed locks or 2PC. Common in microservices for order processing, payments, and inventory management.

2. **What is the difference between choreography and orchestration in sagas?**
Choreography: Each service publishes events and reacts to events. No central coordinator. Loose coupling but hard to trace. Orchestration: A central coordinator directs each step. Easier to understand and test but introduces a single point of failure. Use orchestration for complex sagas, choreography for simple ones.

3. **How do compensating transactions work?**
Compensating transactions are the inverse of forward transactions. If step 3 of a saga fails, you execute the compensating transactions for steps 2 and 1 in reverse order. They must be idempotent and handle cases where compensation itself fails.

4. **How do you ensure idempotency in distributed transactions?**
Use idempotency keys (UUIDs) sent with requests. Store processed keys in a database or Redis with TTL. Before processing, check if the key exists. If it does, return the cached result. This prevents duplicate processing during retries.

5. **What is the outbox pattern and why is it needed?**
The outbox pattern ensures that database writes and event publishing happen atomically. Write the event to an outbox table in the same transaction as the business data. A separate process polls the outbox and publishes events. This prevents data inconsistency where the DB is updated but the event isn't published.
