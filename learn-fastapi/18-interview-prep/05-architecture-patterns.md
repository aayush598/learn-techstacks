# Architecture Patterns for FastAPI

## Pattern 1: Clean Architecture

### Explanation
Clean Architecture separates concerns into concentric layers:
1. **Entities** (innermost) - Business objects and rules
2. **Use Cases** - Application-specific business logic
3. **Interface Adapters** - Controllers, gateways, presenters
4. **Frameworks & Drivers** (outermost) - FastAPI, databases, external services

The Dependency Rule: Source code dependencies must point inward. Outer layers depend on inner layers, never the reverse.

### Folder Structure

```
clean-architecture/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── order.py
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── email.py
│   │   │   └── money.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       └── user_repository.py
│   ├── application/
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── create_user.py
│   │   │   └── get_user.py
│   │   └── dto/
│   │       ├── __init__.py
│   │       └── user_dto.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── repositories/
│   │   │       └── user_repository_impl.py
│   │   ├── email/
│   │   │   └── smtp_email_service.py
│   │   └── cache/
│   │       └── redis_cache.py
│   └── interfaces/
│       ├── __init__.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── deps.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       └── users.py
│       └── schemas/
│           ├── __init__.py
│           └── user_schema.py
├── tests/
├── alembic/
└── pyproject.toml
```

### FastAPI Implementation

```python
# ── Domain Layer (Innermost - No dependencies) ──────────────

from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class UserEntity:
    """Domain entity - pure business logic, no framework dependencies."""
    id: int | None
    name: str
    email: str
    is_active: bool = True
    created_at: datetime | None = None

    def activate(self) -> "UserEntity":
        """Business rule: user activation."""
        return UserEntity(
            id=self.id, name=self.name, email=self.email,
            is_active=True, created_at=self.created_at,
        )

    def deactivate(self) -> "UserEntity":
        """Business rule: user deactivation."""
        if self.id is None:
            raise ValueError("Cannot deactivate unsaved user")
        return UserEntity(
            id=self.id, name=self.name, email=self.email,
            is_active=False, created_at=self.created_at,
        )

class UserRepositoryInterface(ABC):
    """Repository interface - defined in domain, implemented in infrastructure."""
    @abstractmethod
    async def get_by_id(self, user_id: int) -> UserEntity | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> UserEntity | None: ...

    @abstractmethod
    async def save(self, user: UserEntity) -> UserEntity: ...

    @abstractmethod
    async def delete(self, user_id: int) -> bool: ...

# ── Application Layer (Use Cases) ───────────────────────────

from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    name: str
    email: str

class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

class CreateUserUseCase:
    """Application use case - orchestrates domain entities and infrastructure."""

    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def execute(self, dto: CreateUserDTO) -> UserResponseDTO:
        existing = await self.user_repo.get_by_email(dto.email)
        if existing:
            raise ValueError(f"User with email {dto.email} already exists")

        user = UserEntity(id=None, name=dto.name, email=dto.email)
        saved_user = await self.user_repo.save(user)

        return UserResponseDTO(
            id=saved_user.id,
            name=saved_user.name,
            email=saved_user.email,
            is_active=saved_user.is_active,
        )

class GetUserUseCase:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def execute(self, user_id: int) -> UserResponseDTO:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        return UserResponseDTO(
            id=user.id, name=user.name, email=user.email, is_active=user.is_active,
        )

# ── Infrastructure Layer (Implementations) ──────────────────

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.database.models import UserModel

class SQLAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> UserEntity | None:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return UserEntity(
            id=model.id, name=model.name, email=model.email,
            is_active=model.is_active, created_at=model.created_at,
        )

    async def save(self, user: UserEntity) -> UserEntity:
        model = UserModel(
            name=user.name, email=user.email, is_active=user.is_active,
        )
        self.db.add(model)
        await self.db.flush()
        return UserEntity(
            id=model.id, name=model.name, email=model.email,
            is_active=model.is_active, created_at=model.created_at,
        )

    async def get_by_email(self, email: str) -> UserEntity | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return UserEntity(
            id=model.id, name=model.name, email=model.email,
            is_active=model.is_active, created_at=model.created_at,
        )

    async def delete(self, user_id: int) -> bool:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if model:
            await self.db.delete(model)
            return True
        return False

# ── Interface Layer (FastAPI Routes) ────────────────────────

from fastapi import FastAPI, Depends, HTTPException
from app.infrastructure.database import get_db
from app.domain.repositories.user_repository import UserRepositoryInterface
from app.infrastructure.database.repositories.user_repository_impl import SQLAlchemyUserRepository

app = FastAPI()

def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepositoryInterface:
    return SQLAlchemyUserRepository(db)

@app.post("/users", response_model=UserResponseDTO, status_code=201)
async def create_user(
    dto: CreateUserDTO,
    repo: UserRepositoryInterface = Depends(get_user_repository),
):
    use_case = CreateUserUseCase(repo)
    try:
        return await use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: int,
    repo: UserRepositoryInterface = Depends(get_user_repository),
):
    use_case = GetUserUseCase(repo)
    try:
        return await use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

### Trade-offs
| Pros | Cons |
|------|------|
| Highly testable (mock repositories) | More boilerplate code |
| Framework-independent domain | Steeper learning curve |
| Easy to swap infrastructure (DB, cache) | Over-engineered for simple CRUD |
| Clear separation of concerns | More files and layers to navigate |

---

## Pattern 2: Hexagonal Architecture (Ports & Adapters)

### Explanation
Ports & Adapters separates the application into:
- **Core** (hexagon): Business logic and port interfaces
- **Primary adapters**: Drive the application (HTTP controllers, CLI)
- **Secondary adapters**: Are driven by the application (DB, email, file system)

### Folder Structure

```
hexagonal/
├── app/
│   ├── core/
│   │   ├── domain/
│   │   │   ├── models/
│   │   │   ├── ports/
│   │   │   │   ├── incoming/
│   │   │   │   │   └── user_service_port.py
│   │   │   │   └── outgoing/
│   │   │   │       ├── user_repository_port.py
│   │   │   │       └── email_port.py
│   │   │   └── services/
│   │   │       └── user_domain_service.py
│   │   └── config.py
│   ├── adapters/
│   │   ├── incoming/
│   │   │   └── api/
│   │   │       ├── router.py
│   │   │       └── schemas.py
│   │   └── outgoing/
│   │       ├── database/
│   │       │   ├── models.py
│   │       │   └── sqlalchemy_user_repo.py
│   │       ├── email/
│   │       │   └── smtp_email_adapter.py
│   │       └── cache/
│   │           └── redis_adapter.py
│   └── main.py
└── tests/
```

### FastAPI Implementation

```python
# ── Ports (Interfaces in the core) ──────────────────────────

from abc import ABC, abstractmethod
from dataclasses import dataclass

# Incoming Port (driven by primary adapters)
class UserServicePort(ABC):
    @abstractmethod
    async def register(self, name: str, email: str) -> dict: ...

    @abstractmethod
    async def get_profile(self, user_id: int) -> dict: ...

    @abstractmethod
    async def deactivate(self, user_id: int) -> bool: ...

# Outgoing Ports (drive secondary adapters)
class UserRepositoryPort(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: int) -> dict | None: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> dict | None: ...

    @abstractmethod
    async def save(self, user_data: dict) -> dict: ...

    @abstractmethod
    async def delete(self, user_id: int) -> bool: ...

class NotificationPort(ABC):
    @abstractmethod
    async def send_welcome_email(self, email: str, name: str) -> bool: ...

# ── Core Service (Domain Logic) ─────────────────────────────

class UserDomainService(UserServicePort):
    """Core domain service - uses only port interfaces."""

    def __init__(self, user_repo: UserRepositoryPort, notifier: NotificationPort):
        self.user_repo = user_repo
        self.notifier = notifier

    async def register(self, name: str, email: str) -> dict:
        existing = await self.user_repo.find_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        user = await self.user_repo.save({
            "name": name,
            "email": email,
            "is_active": True,
        })

        await self.notifier.send_welcome_email(email, name)
        return user

    async def get_profile(self, user_id: int) -> dict:
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    async def deactivate(self, user_id: int) -> bool:
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            return False
        user["is_active"] = False
        await self.user_repo.save(user)
        return True

# ── Adapters (Implementations) ──────────────────────────────

# Secondary Adapter: PostgreSQL
from sqlalchemy.ext.asyncio import AsyncSession

class SQLAlchemyUserAdapter(UserRepositoryPort):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, user_id: int) -> dict | None:
        # Actual database implementation
        ...

    async def save(self, user_data: dict) -> dict:
        ...

    async def find_by_email(self, email: str) -> dict | None:
        ...

    async def delete(self, user_id: int) -> bool:
        ...

# Secondary Adapter: SMTP Email
class SMTPNotificationAdapter(NotificationPort):
    async def send_welcome_email(self, email: str, name: str) -> bool:
        # Actual email sending logic
        print(f"Sending welcome email to {email}")
        return True

# Primary Adapter: FastAPI Router
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserServicePort:
    """Wire adapters to ports via dependency injection."""
    user_repo = SQLAlchemyUserAdapter(db)
    notifier = SMTPNotificationAdapter()
    return UserDomainService(user_repo, notifier)

@router.post("/", status_code=201)
async def create_user(
    name: str, email: str,
    service: UserServicePort = Depends(get_user_service),
):
    try:
        return await service.register(name, email)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    service: UserServicePort = Depends(get_user_service),
):
    try:
        return await service.get_profile(user_id)
    except ValueError as e:
        raise HTTPException(404, str(e))
```

### Trade-offs
| Pros | Cons |
|------|------|
| Core is completely testable without infrastructure | More interfaces to maintain |
| Easy to add new adapters (new DB, new email provider) | Can feel abstract for simple apps |
| Clean separation between "what" and "how" | Learning curve for teams new to hexagonal |

---

## Pattern 3: Domain-Driven Design (DDD)

### Explanation
DDD focuses on modeling software around business domains using ubiquitous language shared between developers and domain experts. Key concepts:
- **Aggregates**: Consistency boundaries (e.g., Order + OrderItems)
- **Value Objects**: Immutable objects defined by attributes (e.g., Money, Email)
- **Domain Events**: Things that happened in the domain (e.g., OrderPlaced)
- **Bounded Contexts**: Boundaries within which a particular model applies

### FastAPI Implementation

```python
# ── Value Objects ────────────────────────────────────────────

from dataclasses import dataclass
from pydantic import BaseModel

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be 3-letter ISO code")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def multiply(self, factor: int) -> "Money":
        return Money(amount=self.amount * factor, currency=self.currency)

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Invalid email format")

# ── Aggregate Root ───────────────────────────────────────────

from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class OrderItem:
    product_id: str
    product_name: str
    quantity: int
    unit_price: Money

    @property
    def subtotal(self) -> Money:
        return self.unit_price.multiply(self.quantity)

@dataclass
class Order:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    customer_id: str = ""
    items: list[OrderItem] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    _events: list = field(default_factory=list, repr=False)

    @property
    def total(self) -> Money:
        if not self.items:
            return Money(0, "USD")
        result = self.items[0].subtotal
        for item in self.items[1:]:
            result = result.add(item.subtotal)
        return result

    def add_item(self, product_id: str, name: str, quantity: int, price: Money):
        if self.status != "pending":
            raise ValueError("Cannot modify a non-pending order")

        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                return

        self.items.append(OrderItem(product_id, product_id, quantity, price))

    def place(self):
        if not self.items:
            raise ValueError("Cannot place empty order")
        self.status = "placed"
        self._events.append(OrderPlacedEvent(self.id, self.customer_id, self.total))

    def cancel(self, reason: str = ""):
        if self.status not in ("pending", "placed"):
            raise ValueError(f"Cannot cancel order in status: {self.status}")
        self.status = "cancelled"
        self._events.append(OrderCancelledEvent(self.id, self.customer_id, reason))

    def get_events(self) -> list:
        events = self._events.copy()
        self._events.clear()
        return events

# ── Domain Events ────────────────────────────────────────────

@dataclass(frozen=True)
class OrderPlacedEvent:
    order_id: str
    customer_id: str
    total: Money
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class OrderCancelledEvent:
    order_id: str
    customer_id: str
    reason: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

# ── Repository (Aggregate Persistence) ──────────────────────

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, order: Order):
        # Save aggregate and its child entities
        model = OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status,
            total_amount=order.total.amount,
            total_currency=order.total.currency,
        )
        self.db.add(model)

        for item in order.items:
            item_model = OrderItemModel(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price.amount,
                currency=item.unit_price.currency,
            )
            self.db.add(item_model)

        await self.db.flush()

        # Publish domain events
        for event in order.get_events():
            await self._publish_event(event)

    async def _publish_event(self, event):
        # Publish to message broker (RabbitMQ, Kafka, etc.)
        print(f"Publishing event: {event}")

# ── Application Service ─────────────────────────────────────

class OrderService:
    def __init__(self, order_repo: OrderRepository, product_repo: ProductRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo

    async def create_order(self, customer_id: str) -> Order:
        order = Order(customer_id=customer_id)
        await self.order_repo.save(order)
        return order

    async def add_item_to_order(
        self, order_id: str, product_id: str, quantity: int
    ) -> Order:
        order = await self.order_repo.get(order_id)
        product = await self.product_repo.get(product_id)

        price = Money(amount=product["price"], currency="USD")
        order.add_item(product_id, product["name"], quantity, price)
        await self.order_repo.save(order)
        return order

    async def place_order(self, order_id: str) -> Order:
        order = await self.order_repo.get(order_id)
        order.place()
        await self.order_repo.save(order)
        return order

# ── FastAPI Integration ─────────────────────────────────────

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", status_code=201)
async def create_order(customer_id: str, service: OrderService = Depends(get_order_service)):
    order = await service.create_order(customer_id)
    return {"id": order.id, "status": order.status}

@router.post("/{order_id}/items")
async def add_item(order_id: str, product_id: str, quantity: int, service = Depends(get_order_service)):
    order = await service.add_item_to_order(order_id, product_id, quantity)
    return {"id": order.id, "total": order.total.amount}

@router.post("/{order_id}/place")
async def place_order(order_id: str, service = Depends(get_order_service)):
    order = await service.place_order(order_id)
    return {"id": order.id, "status": order.status}
```

---

## Pattern 4: Microservices with FastAPI

### Explanation
Microservices decompose a system into small, independently deployable services, each owning its data and business logic.

### Folder Structure

```
microservices/
├── gateway/                 # API Gateway
│   ├── app/
│   │   ├── main.py
│   │   ├── middleware/
│   │   └── routes/
│   └── Dockerfile
├── user-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── events/
│   │   └── clients/
│   └── Dockerfile
├── order-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── clients/
│   └── Dockerfile
├── notification-service/
│   ├── app/
│   │   ├── main.py
│   │   └── handlers/
│   └── Dockerfile
├── docker-compose.yml
└── k8s/
```

### FastAPI Implementation

```python
# ── API Gateway ─────────────────────────────────────────────

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="API Gateway")

SERVICE_REGISTRY = {
    "users": "http://user-service:8001",
    "orders": "http://order-service:8002",
    "products": "http://product-service:8003",
}

@app.middleware("http")
async def gateway_middleware(request: Request, call_next):
    # Auth check
    auth_header = request.headers.get("Authorization")
    if not auth_header and request.url.path not in ["/health", "/docs"]:
        return JSONResponse(401, {"detail": "Authorization required"})

    response = await call_next(request)
    response.headers["X-Gateway"] = "true"
    return response

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_proxy(service: str, path: str, request: Request):
    if service not in SERVICE_REGISTRY:
        raise HTTPException(404, f"Service '{service}' not found")

    target_url = f"{SERVICE_REGISTRY[service]}/{path}"
    body = await request.body()

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            content=body,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            params=dict(request.query_params),
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


# ── User Service (Independent FastAPI App) ──────────────────

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

user_app = FastAPI(title="User Service")

users_db: dict[str, dict] = {}

class UserCreate(BaseModel):
    name: str
    email: str

@user_app.post("/users", status_code=201)
def create_user(payload: UserCreate):
    user_id = str(uuid.uuid4())[:8]
    users_db[user_id] = {"id": user_id, **payload.model_dump()}
    # Publish UserCreated event
    publish_event("user.created", {"user_id": user_id, **payload.model_dump()})
    return users_db[user_id]

@user_app.get("/users/{user_id}")
def get_user(user_id: str):
    if user_id not in users_db:
        raise HTTPException(404)
    return users_db[user_id]

@user_app.get("/health")
def health():
    return {"status": "healthy", "service": "user-service"}


# ── Order Service (Independent FastAPI App) ─────────────────

from fastapi import FastAPI, HTTPException, BackgroundTasks
import httpx

order_app = FastAPI(title="Order Service")

orders_db: dict[str, dict] = {}

class OrderCreate(BaseModel):
    user_id: str
    items: list[dict]

@order_app.post("/orders", status_code=201)
async def create_order(payload: OrderCreate, background_tasks: BackgroundTasks):
    # Verify user exists via user service
    async with httpx.AsyncClient() as client:
        user_resp = await client.get(f"http://user-service:8001/users/{payload.user_id}")
        if user_resp.status_code != 200:
            raise HTTPException(400, "User not found")

    order_id = str(uuid.uuid4())[:8]
    orders_db[order_id] = {
        "id": order_id,
        "user_id": payload.user_id,
        "items": payload.items,
        "status": "pending",
    }

    # Async notification
    background_tasks.add_task(send_order_confirmation, order_id)
    return orders_db[order_id]

@order_app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(404)
    return orders_db[order_id]


# ── Event Bus (Message Passing Between Services) ────────────

class EventBus:
    def __init__(self):
        self.subscribers: dict[str, list[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        self.subscribers.setdefault(event_type, []).append(handler)

    async def publish(self, event_type: str, data: dict):
        for handler in self.subscribers.get(event_type, []):
            if asyncio.iscoroutinefunction(handler):
                await handler(data)
            else:
                handler(data)

event_bus = EventBus()

# Subscribe to events
@event_bus.subscribe("user.created")
async def on_user_created(data: dict):
    print(f"User created: {data}")

# ── docker-compose.yml ─────────────────────────────────────
# version: '3.8'
# services:
#   gateway:
#     build: ./gateway
#     ports: ["8000:8000"]
#     depends_on: [user-service, order-service]
#   user-service:
#     build: ./user-service
#     ports: ["8001:8001"]
#   order-service:
#     build: ./order-service
#     ports: ["8002:8002"]
#     depends_on: [user-service]
#   notification-service:
#     build: ./notification-service
#     depends_on: [rabbitmq]
#   rabbitmq:
#     image: rabbitmq:3-management
#     ports: ["5672:5672", "15672:15672"]
```

---

## Pattern 5: Monolith-First Approach

### Explanation
Start with a well-structured monolith, extract to microservices when you have clear service boundaries. This avoids premature decomposition.

### FastAPI Monolith Structure

```
monolith/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── events.py
│   │   └── exceptions.py
│   ├── modules/
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── services.py
│   │   │   └── events.py
│   │   ├── orders/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── services.py
│   │   │   └── events.py
│   │   └── products/
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── schemas.py
│   │       ├── routes.py
│   │       └── services.py
│   └── shared/
│       ├── __init__.py
│       ├── pagination.py
│       └── dependencies.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── migrations/
└── docker-compose.yml
```

```python
# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.modules.users.routes import router as users_router
from app.modules.orders.routes import router as orders_router
from app.modules.products.routes import router as products_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

# Register all module routers
app.include_router(users_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")

# When ready to extract to microservices:
# 1. Identify bounded context (e.g., users module)
# 2. Add event publishing to the module
# 3. Create a new FastAPI service
# 4. Add inter-service communication (HTTP or events)
# 5. Deploy independently
# 6. Add API gateway routing
```

---

## Pattern 6: API Gateway Pattern

### Explanation
API Gateway provides a single entry point for all client requests, handling cross-cutting concerns like auth, rate limiting, and routing.

```python
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import httpx
import time
from dataclasses import dataclass

app = FastAPI(title="API Gateway")

@dataclass
class ServiceRoute:
    prefix: str
    target_url: str
    strip_prefix: bool = True
    rate_limit: int = 1000
    auth_required: bool = True
    timeout: float = 30.0

ROUTES = {
    "users": ServiceRoute(prefix="/api/users", target_url="http://user-service:8001"),
    "orders": ServiceRoute(prefix="/api/orders", target_url="http://order-service:8002"),
    "products": ServiceRoute(prefix="/api/products", target_url="http://product-service:8003"),
    "analytics": ServiceRoute(prefix="/api/analytics", target_url="http://analytics-service:8004"),
}

class GatewayMiddleware:
    def __init__(self, routes: dict[str, ServiceRoute]):
        self.routes = routes
        self.rate_limits: dict[str, list[float]] = {}

    def find_route(self, path: str) -> tuple[str, ServiceRoute] | None:
        for name, route in self.routes.items():
            if path.startswith(route.prefix):
                return name, route
        return None

    def check_rate_limit(self, client_id: str, route: ServiceRoute) -> bool:
        now = time.time()
        key = f"{client_id}:{route.prefix}"
        if key not in self.rate_limits:
            self.rate_limits[key] = []

        self.rate_limits[key] = [t for t in self.rate_limits[key] if now - t < 60]
        if len(self.rate_limits[key]) >= route.rate_limit:
            return False
        self.rate_limits[key].append(now)
        return True

gateway = GatewayMiddleware(ROUTES)

@app.middleware("http")
async def api_gateway_middleware(request: Request, call_next):
    match = gateway.find_route(request.url.path)
    if not match:
        return await call_next(request)

    name, route = match
    client_id = request.client.host

    # Rate limiting
    if not gateway.check_rate_limit(client_id, route):
        return JSONResponse(429, {"detail": "Rate limit exceeded"})

    # Authentication check
    if route.auth_required:
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse(401, {"detail": "Authentication required"})

    # Proxy to backend service
    path = request.url.path
    if route.strip_prefix:
        path = path[len(route.prefix):]

    target_url = f"{route.target_url}{path}"
    body = await request.body()

    try:
        async with httpx.AsyncClient(timeout=route.timeout) as client:
            resp = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
                params=dict(request.query_params),
            )

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers),
        )
    except httpx.TimeoutException:
        return JSONResponse(504, {"detail": "Service timeout"})
    except httpx.ConnectError:
        return JSONResponse(503, {"detail": "Service unavailable"})

@app.get("/gateway/routes")
def list_routes():
    return {"routes": {name: {"prefix": r.prefix, "target": r.target_url} for name, r in ROUTES.items()}}
```

---

## Pattern Summary Comparison

| Pattern | Best For | Complexity | Testing |
|---------|----------|------------|---------|
| Clean Architecture | Complex business logic, long-lived projects | High | Excellent |
| Hexagonal | Multiple adapters, framework independence | High | Excellent |
| DDD | Complex domains, large teams | Very High | Excellent |
| Microservices | Large-scale systems, team autonomy | Very High | Good (integration) |
| Monolith-First | New projects, small teams, MVPs | Low | Good |
| API Gateway | Multi-service architectures | Medium | Good |

### Decision Framework

```
Start with Monolith-First if:
  - Building an MVP
  - Small team (< 5 developers)
  - Uncertain domain boundaries
  - Need to move fast

Use Clean/Hexagonal if:
  - Complex business logic
  - Long-lived project (3+ years)
  - Need to swap infrastructure easily
  - Strong testing requirements

Use DDD if:
  - Complex domain with many business rules
  - Large team with domain experts
  - Need ubiquitous language

Use Microservices if:
  - Clear service boundaries identified
  - Multiple teams working independently
  - Need to scale specific components
  - Different technology requirements per service

Use API Gateway if:
  - Multiple backend services
  - Need centralized auth, rate limiting, logging
  - Multiple client types (web, mobile, IoT)
