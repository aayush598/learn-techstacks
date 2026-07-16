# Dataclasses as Pydantic Models for FastAPI

## Table of Contents

1. [Python Dataclasses Recap](#python-dataclasses-recap)
2. [Dataclass Performance](#dataclass-performance)
3. [Frozen Dataclasses](#frozen-dataclasses)
4. [dataclass_validator](#dataclass_validator)
5. [Dataclasses in FastAPI](#dataclasses-in-fastapi)
6. [Pydantic Dataclasses vs BaseModel](#pydantic-dataclasses-vs-basemodel)
7. [When to Use Which](#when-to-use-which)
8. [Performance Comparison](#performance-comparison)
9. [Migration Patterns](#migration-patterns)
10. [Interview Questions](#interview-questions)

---

## Python Dataclasses Recap

### Basic Dataclass Usage

```python
from dataclasses import dataclass, field
from typing import ClassVar
from datetime import datetime

# Basic dataclass
@dataclass
class User:
    name: str
    email: str
    age: int
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

# Auto-generates:
# - __init__(self, name, email, age, is_active=True, created_at=...)
# - __repr__(self) -> User(name='...', email='...', ...)
# - __eq__(self, other) -> compares all fields
# - __hash__ (if frozen=True)

# Usage
user = User(name="Alice", email="alice@example.com", age=30)
print(user)  # User(name='Alice', email='alice@example.com', age=30, is_active=True, ...)

# Equality
user1 = User(name="Alice", email="alice@example.com", age=30)
user2 = User(name="Alice", email="alice@example.com", age=30)
print(user1 == user2)  # True (same field values)
```

### Field Options

```python
from dataclasses import dataclass, field
from typing import ClassVar, Any

@dataclass
class Product:
    # Basic fields
    name: str
    price: float

    # Default value
    description: str = ""

    # Default factory (for mutable defaults)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    # Field exclusions
    internal_id: int = field(init=False)  # Not in __init__
    _cache: dict = field(repr=False, compare=False)  # Not in repr or eq

    # Class variable (not a field at all)
    category: ClassVar[str] = "general"

    # Post-init processing
    def __post_init__(self):
        self.internal_id = hash(self.name) % 10000
        self._cache = {}

    # Custom validation in __post_init__
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

# Usage
product = Product(name="Widget", price=9.99, tags=["sale"])
print(product)  # Product(name='Widget', price=9.99, description='', tags=['sale'], metadata={})
print(product.internal_id)  # Generated ID
```

### Dataclass Configuration

```python
from dataclasses import dataclass, field, asdict, astuple
import json

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    workers: int = 4

    # Custom methods
    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        return cls(**data)

# asdict - converts to dictionary
config = Config(host="0.0.0.0", port=9000)
config_dict = asdict(config)
print(config_dict)  # {'host': '0.0.0.0', 'port': 9000, 'debug': False, 'workers': 4}

# astuple - converts to tuple
config_tuple = astuple(config)
print(config_tuple)  # ('0.0.0.0', 9000, False, 4)

# from_dict
config2 = Config.from_dict({"host": "127.0.0.1", "port": 3000})
print(config2)  # Config(host='127.0.0.1', port=3000, debug=False, workers=4)
```

---

## Dataclass Performance

### Memory Usage

```python
import sys
from dataclasses import dataclass

@dataclass
class RegularDataclass:
    name: str
    age: int
    email: str

@dataclass(slots=True)
class SlottedDataclass:
    name: str
    age: int
    email: str

# Memory comparison
regular = RegularDataclass("Alice", 30, "alice@example.com")
slotted = SlottedDataclass("Alice", 30, "alice@example.com")

print(f"Regular: {sys.getsizeof(regular.__dict__)} bytes")
print(f"Slotted: {sys.getsizeof(slotted)} bytes")

# Regular dataclass: ~232 bytes (has __dict__)
# Slotted dataclass: ~48 bytes (no __dict__)
# ~80% memory reduction with slots!
```

### Creation Speed

```python
import timeit

@dataclass
class Point:
    x: float
    y: float

# Benchmark creation
setup = "from __main__ import Point"
stmt = "Point(1.0, 2.0)"

regular_time = timeit.timeit(stmt, setup=setup, number=1000000)
print(f"Regular dataclass: {regular_time:.3f}s for 1M creations")

# Typical results:
# Regular dataclass: ~0.3s for 1M creations
# Pydantic BaseModel: ~1.5s for 1M creations
# Dataclass is ~5x faster for creation
```

### Attribute Access

```python
import timeit

@dataclass
class RegularPoint:
    x: float
    y: float

@dataclass(slots=True)
class SlottedPoint:
    x: float
    y: float

# Benchmark attribute access
regular_setup = "from __main__ import RegularPoint; p = RegularPoint(1.0, 2.0)"
slotted_setup = "from __main__ import SlottedPoint; p = SlottedPoint(1.0, 2.0)"

regular_time = timeit.timeit("p.x", setup=regular_setup, number=1000000)
slotted_time = timeit.timeit("p.x", setup=slotted_setup, number=1000000)

print(f"Regular: {regular_time:.3f}s")
print(f"Slotted: {slotted_time:.3f}s")

# Slotted is ~20% faster for attribute access
```

---

## Frozen Dataclasses

### Immutable Data

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

# Cannot modify
point = Point(1.0, 2.0)
# point.x = 3.0  # AttributeError: cannot assign to field 'x'

# Hashable (can be dict keys or set members)
points = {
    Point(1, 2): "first",
    Point(3, 4): "second",
}

point_set = {Point(1, 2), Point(3, 4), Point(1, 2)}
print(len(point_set))  # 2 (duplicates removed)

# Hash is auto-generated
print(hash(Point(1, 2)))  # -3550055125443633663
```

### Frozen with Slots

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class OptimizedPoint:
    x: float
    y: float

# Benefits:
# 1. Immutable (frozen=True)
# 2. Hashable (auto-generated hash)
# 3. Memory efficient (slots=True)
# 4. Fast attribute access (slots=True)
# 5. Can be used as dict keys

# Usage in FastAPI context
@dataclass(frozen=True, slots=True)
class GeoLocation:
    latitude: float
    longitude: float

    def distance_to(self, other: "GeoLocation") -> float:
        # Haversine formula
        import math
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return 2 * 6371 * math.asin(math.sqrt(a))
```

### Frozen with Default Values

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Config:
    host: str = "localhost"
    port: int = 8000
    debug: bool = False

    # Cannot use mutable defaults in frozen dataclasses
    # tags: list[str] = []  # ERROR: unhashable type

    # Must use field(default_factory=...) for mutable defaults
    # But even then, the list itself is mutable
    # tags: list[str] = field(default_factory=list)

    # Better: Use tuple for immutable sequence
    allowed_hosts: tuple[str, ...] = ("localhost", "127.0.0.1")

# Config is hashable
configs = {
    Config(port=8000): "default",
    Config(port=9000): "alternative",
}
```

---

## dataclass_validator

### Pydantic's dataclass_validator

```python
from pydantic import dataclasses, field, ValidationError

# Pydantic dataclass with validation
@dataclasses.dataclass
class User:
    name: str = field(min_length=1, max_length=100)
    email: str = field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
    age: int = field(ge=0, le=150)
    tags: list[str] = field(default_factory=list, max_length=10)

    # Custom validator
    def __post_init_post_parse__(self):
        # This runs AFTER Pydantic validation
        if self.age < 18:
            raise ValueError("User must be 18 or older")

# Usage
try:
    user = User(name="Alice", email="alice@example.com", age=30)
    print(user)  # User(name='Alice', email='alice@example.com', age=30, tags=[])

    # Validation error
    bad_user = User(name="", email="invalid", age=-1)
except ValidationError as e:
    print(e)
    # 2 validation errors for User
    #   - Value error, String should have at least 1 character [type=string_too_short, ...]
    #   - Value error, Input should be a valid email address [type=value_error, ...]
    #   - Value error, Input should be greater than or equal to 0 [type=greater_than_equal, ...]
```

### field() Options in Pydantic Dataclasses

```python
from pydantic import dataclasses, field
from typing import Annotated

@dataclasses.dataclass
class Product:
    # String validation
    name: str = field(min_length=1, max_length=200)
    description: str = field(default="", max_length=5000)

    # Numeric validation
    price: float = field(gt=0, le=1000000)
    quantity: int = field(ge=0, default=0)

    # Pattern validation
    sku: str = field(pattern=r"^[A-Z]{3}-\d{4}$")

    # Default factory
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    # Exclude from serialization
    internal_id: int = field(init=False, exclude=True)

    # Custom serializer
    price_cents: int = field(init=False, exclude=True)

    def __post_init_post_parse__(self):
        self.internal_id = hash(self.name) % 10000
        self.price_cents = int(self.price * 100)

# Usage
product = Product(
    name="Widget",
    price=9.99,
    sku="WID-0001",
)
print(product)  # Product(name='Widget', description='', price=9.99, ...)
print(product.price_cents)  # 999
```

### Advanced Validators

```python
from pydantic import dataclasses, field, model_validator
from typing import Annotated

@dataclasses.dataclass
class PasswordReset:
    password: str = field(min_length=8)
    password_confirm: str = field(min_length=8)
    old_password: str | None = None

    # Model-level validation
    @model_validator(mode="after")
    def check_passwords_match(self) -> "PasswordReset":
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        if self.old_password and self.old_password == self.password:
            raise ValueError("New password must differ from old password")
        return self

    # Field-level validation with info
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v

# Usage
try:
    reset = PasswordReset(
        password="StrongPass123",
        password_confirm="StrongPass123",
    )
    print(reset)

    # Passwords don't match
    bad_reset = PasswordReset(
        password="StrongPass123",
        password_confirm="DifferentPass123",
    )
except ValidationError as e:
    print(e)  # Passwords do not match
```

---

## Dataclasses in FastAPI

### Using Pydantic Dataclasses

```python
from pydantic import dataclasses, field
from fastapi import FastAPI, HTTPException
from typing import AsyncGenerator

app = FastAPI()

# Request model
@dataclasses.dataclass
class UserCreate:
    name: str = field(min_length=1, max_length=100)
    email: str = field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
    age: int = field(ge=0, le=150)
    password: str = field(min_length=8, exclude=True)  # Exclude from response

# Response model
@dataclasses.dataclass
class UserResponse:
    id: int
    name: str
    email: str
    age: int

# Pydantic dataclass works with FastAPI
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate) -> UserResponse:
    # user is validated by Pydantic
    new_user = await save_user(user)
    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        age=new_user.age,
    )

# List response
@app.get("/users", response_model=list[UserResponse])
async def list_users() -> list[UserResponse]:
    users = await get_all_users()
    return [UserResponse(**u.model_dump()) for u in users]

# Error handling
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.model_dump())
```

### Native Dataclasses in FastAPI

```python
from fastapi import FastAPI
from dataclasses import dataclass
from pydantic import TypeAdapter

app = FastAPI()

# Native dataclass
@dataclass
class Item:
    name: str
    price: float
    description: str = ""

# Wrap with TypeAdapter for FastAPI
item_adapter = TypeAdapter(Item)

@app.post("/items")
async def create_item(item: Item):
    # FastAPI can handle native dataclasses with TypeAdapter
    # But Pydantic dataclass is more seamless
    return {"name": item.name, "price": item.price}

# Better: Use Pydantic dataclass
from pydantic import dataclasses as pydantic_dataclasses

@pydantic_dataclasses.dataclass
class BetterItem:
    name: str
    min_length=1
    price: float
    gt=0

@app.post("/items")
async def create_item(item: BetterItem):
    # Pydantic validation happens automatically
    return {"name": item.name, "price": item.price}
```

### Dependency Injection with Dataclasses

```python
from fastapi import FastAPI, Depends
from pydantic import dataclasses, field
from typing import Annotated

app = FastAPI()

@dataclasses.dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    db_name: str = "mydb"
    pool_size: int = 10

    def get_url(self) -> str:
        return f"postgresql://{self.host}:{self.port}/{self.db_name}"

@dataclasses.dataclass
class CacheConfig:
    host: str = "localhost"
    port: int = 6379
    ttl: int = 300

# Dependencies
async def get_db_config() -> DatabaseConfig:
    return DatabaseConfig(
        host="db.example.com",
        port=5432,
        db_name="production",
    )

async def get_cache_config() -> CacheConfig:
    return CacheConfig(
        host="cache.example.com",
        port=6379,
        ttl=600,
    )

@app.get("/config")
async def get_config(
    db: DatabaseConfig = Depends(get_db_config),
    cache: CacheConfig = Depends(get_cache_config),
) -> dict:
    return {
        "database": {"url": db.get_url(), "pool": db.pool_size},
        "cache": {"host": cache.host, "ttl": cache.ttl},
    }
```

---

## Pydantic Dataclasses vs BaseModel

### Side-by-Side Comparison

```python
from pydantic import BaseModel, dataclasses, field, ValidationError

# Pydantic BaseModel
class UserBaseModel(BaseModel):
    name: str
    email: str
    age: int

    def greet(self) -> str:
        return f"Hello, {self.name}!"

# Pydantic Dataclass
@dataclasses.dataclass
class UserPydanticDC:
    name: str
    email: str
    age: int

    def greet(self) -> str:
        return f"Hello, {self.name}!"

# Both work similarly
user_bm = UserBaseModel(name="Alice", email="alice@example.com", age=30)
user_dc = UserPydanticDC(name="Alice", email="alice@example.com", age=30)

# Both have validation
try:
    bad_bm = UserBaseModel(name="", email="invalid", age=-1)
except ValidationError as e:
    print(f"BaseModel error: {e}")

try:
    bad_dc = UserPydanticDC(name="", email="invalid", age=-1)
except ValidationError as e:
    print(f"Dataclass error: {e}")
```

### Key Differences

```python
# 1. Inheritance
class BaseModelChild(UserBaseModel):
    role: str = "user"

# Pydantic dataclass inheritance is limited
@dataclasses.dataclass
class ParentDataclass:
    name: str

# @dataclasses.dataclass
# class ChildDataclass(ParentDataclass):  # This doesn't work well
#     role: str = "user"

# 2. Configuration
class ConfiguredModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )
    name: str

@dataclasses.dataclass
class ConfiguredDC:
    name: str
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,
    )

# 3. Field customization
class FieldModel(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)

@dataclasses.dataclass
class FieldDC:
    name: str = field(min_length=1, max_length=100)
    age: int = field(ge=0, le=150)

# 4. Serialization methods
user_bm = UserBaseModel(name="Alice", email="alice@example.com", age=30)
print(user_bm.model_dump())  # BaseModel method
print(user_bm.model_dump_json())  # BaseModel method

user_dc = UserPydanticDC(name="Alice", email="alice@example.com", age=30)
# Dataclasses use Pydantic's serialization through TypeAdapter
from pydantic import TypeAdapter
adapter = TypeAdapter(UserPydanticDC)
print(adapter.dump_python(user_dc))
print(adapter.dump_json(user_dc))
```

### Performance Comparison

```python
import timeit

# Creation performance
bm_setup = "from __main__ import UserBaseModel; data = {'name': 'Alice', 'email': 'alice@example.com', 'age': 30}"
dc_setup = "from __main__ import UserPydanticDC; data = {'name': 'Alice', 'email': 'alice@example.com', 'age': 30}"

bm_time = timeit.timeit(
    "UserBaseModel(**data)",
    setup=bm_setup,
    number=100000,
)

dc_time = timeit.timeit(
    "UserPydanticDC(**data)",
    setup=dc_setup,
    number=100000,
)

print(f"BaseModel: {bm_time:.3f}s")
print(f"Dataclass: {dc_time:.3f}s")

# Typical results:
# BaseModel: ~0.8s for 100K creations
# Dataclass: ~0.5s for 100K creations
# Dataclass is ~40% faster for creation

# Serialization performance
user_bm = UserBaseModel(name="Alice", email="alice@example.com", age=30)
user_dc = UserPydanticDC(name="Alice", email="alice@example.com", age=30)

bm_ser_time = timeit.timeit(
    "user_bm.model_dump()",
    setup="from __main__ import user_bm",
    number=100000,
)

adapter = TypeAdapter(UserPydanticDC)
dc_ser_time = timeit.timeit(
    "adapter.dump_python(user_dc)",
    setup="from __main__ import adapter, user_dc",
    number=100000,
)

print(f"BaseModel serialization: {bm_ser_time:.3f}s")
print(f"Dataclass serialization: {dc_ser_time:.3f}s")

# Serialization performance is similar
```

---

## When to Use Which

### Decision Matrix

```python
# Use Pydantic BaseModel when:
# 1. Complex validation logic
# 2. Multiple inheritance needed
# 3. Custom JSON schema generation
# 4. ORM integration (from_attributes)
# 5. Complex serialization rules
# 6. Field aliases
# 7. Computed fields

# Use Pydantic Dataclass when:
# 1. Simple models with basic validation
# 2. Want dataclass syntax (init, repr, eq)
# 3. Performance is critical
# 4. Don't need complex inheritance
# 5. Want cleaner code with less boilerplate

# Use Native Dataclass when:
# 1. Internal data structures (not API models)
# 2. No validation needed
# 3. Maximum performance needed
# 4. Simple data containers
# 5. Used as dict keys (frozen=True)
```

### Example: When to Use What

```python
# BASEMODEL: Complex API model with relationships
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    profile: ProfileResponse
    posts: list[PostResponse]
    created_at: datetime

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

# PYDANTIC DATACLASS: Simple request model
@dataclasses.dataclass
class LoginRequest:
    email: str = field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
    password: str = field(min_length=8)

# NATIVE DATACLASS: Internal data structure
@dataclass(frozen=True, slots=True)
class Coordinates:
    latitude: float
    longitude: float

@dataclass
class CacheEntry:
    key: str
    value: Any
    expires_at: float
```

### Migration Patterns

```python
# Pattern 1: BaseModel -> Pydantic Dataclass
# Before
class UserModel(BaseModel):
    name: str
    email: str

# After (simpler)
@dataclasses.dataclass
class UserModel:
    name: str
    email: str

# Pattern 2: Native Dataclass -> Pydantic Dataclass
# Before
@dataclass
class Item:
    name: str
    price: float

# After (with validation)
@dataclasses.dataclass
class Item:
    name: str = field(min_length=1)
    price: float = field(gt=0)

# Pattern 3: Mixed usage
# Keep BaseModel for complex models
# Use Pydantic dataclass for simple models
# Use native dataclass for internal structures
```

---

## Performance Comparison

### Full Benchmark

```python
import timeit
from pydantic import BaseModel, dataclasses as pydantic_dc, field
from dataclasses import dataclass, asdict

# Models
@dataclass
class NativeDC:
    name: str
    age: int
    email: str

@dataclass(slots=True)
class SlottedDC:
    name: str
    age: int
    email: str

@pydantic_dc.dataclass
class PydanticDC:
    name: str
    age: int
    email: str

class BaseModelClass(BaseModel):
    name: str
    age: int
    email: str

data = {"name": "Alice", "age": 30, "email": "alice@example.com"}

# Creation benchmark
def benchmark_creation():
    results = {}

    results["native_dc"] = timeit.timeit(
        "NativeDC(**data)",
        globals={"NativeDC": NativeDC, "data": data},
        number=1000000,
    )

    results["slotted_dc"] = timeit.timeit(
        "SlottedDC(**data)",
        globals={"SlottedDC": SlottedDC, "data": data},
        number=1000000,
    )

    results["pydantic_dc"] = timeit.timeit(
        "PydanticDC(**data)",
        globals={"PydanticDC": PydanticDC, "data": data},
        number=1000000,
    )

    results["base_model"] = timeit.timeit(
        "BaseModelClass(**data)",
        globals={"BaseModelClass": BaseModelClass, "data": data},
        number=1000000,
    )

    return results

# Expected results (1M iterations):
# native_dc: ~0.25s
# slotted_dc: ~0.20s
# pydantic_dc: ~0.35s
# base_model: ~0.80s

# Serialization benchmark
def benchmark_serialization():
    native = NativeDC(name="Alice", age=30, email="alice@example.com")
    slotted = SlottedDC(name="Alice", age=30, email="alice@example.com")
    pydantic = PydanticDC(name="Alice", age=30, email="alice@example.com")
    base = BaseModelClass(name="Alice", age=30, email="alice@example.com")

    results = {}

    results["native_dc"] = timeit.timeit(
        "asdict(native)",
        globals={"asdict": asdict, "native": native},
        number=1000000,
    )

    results["pydantic_dc"] = timeit.timeit(
        "adapter.dump_python(pydantic)",
        globals={"adapter": TypeAdapter(PydanticDC), "pydantic": pydantic},
        number=1000000,
    )

    results["base_model"] = timeit.timeit(
        "base.model_dump()",
        globals={"base": base},
        number=1000000,
    )

    return results
```

---

## Interview Questions

### Q1: What is the difference between native dataclasses and Pydantic dataclasses?

**Answer:** Native dataclasses (Python stdlib) generate `__init__`, `__repr__`, `__eq__` but no validation. Pydantic dataclasses add validation, serialization, and JSON schema generation. Pydantic dataclasses use `__post_init_post_parse__` instead of `__post_init__` for post-validation logic.

### Q2: When should you use dataclasses over Pydantic BaseModel?

**Answer:** Use dataclasses for simple models with basic validation, when you want dataclass syntax (init, repr, eq), or when performance is critical. Use BaseModel for complex validation, multiple inheritance, computed fields, or when you need advanced features like aliases and custom serializers.

### Q3: What are the benefits of frozen dataclasses?

**Answer:** Frozen dataclasses are immutable (can't modify attributes), hashable (can be dict keys or set members), and thread-safe. They're useful for value objects, configuration, or any data that shouldn't change. Use `frozen=True` parameter.

### Q4: What does `slots=True` do in dataclasses?

**Answer:** `slots=True` (Python 3.10+) uses `__slots__` instead of `__dict__` for attribute storage. Benefits: ~80% less memory per instance, faster attribute access, prevents dynamic attribute creation. Required for frozen dataclasses to work properly.

### Q5: How do you add validation to a dataclass?

**Answer:** Use Pydantic's `@dataclasses.dataclass` decorator with `field()` options for validation rules. For custom validation, use `__post_init_post_parse__` or `@field_validator`/`@model_validator`. Native dataclasses only support validation in `__post_init__`.

### Q6: What is `__post_init__` vs `__post_init_post_parse__`?

**Answer:** `__post_init__` runs after native dataclass `__init__`. `__post_init_post_parse__` runs after Pydantic validation. Use `__post_init_post_parse__` in Pydantic dataclasses for post-validation logic. Use `__post_init__` in native dataclasses.

### Q7: How do you serialize a dataclass to JSON?

**Answer:** For native dataclasses: use `dataclasses.asdict()` then `json.dumps()`. For Pydantic dataclasses: use `TypeAdapter(MyClass).dump_json(instance)`. Pydantic dataclasses support all Pydantic serialization methods through TypeAdapter.

### Q8: Can you inherit from Pydantic dataclasses?

**Answer:** Yes, but with limitations. Pydantic dataclasses support single inheritance but not multiple inheritance. The child class inherits validation rules. For complex inheritance patterns, Pydantic BaseModel is more flexible.

### Q9: What is `field(init=False)`?

**Answer:** `field(init=False)` creates a field that's not included in `__init__`. It must be set in `__post_init__` or `__post_init_post_parse__`. Useful for computed fields or fields derived from other fields.

### Q10: What is `field(exclude=True)`?

**Answer:** `field(exclude=True)` excludes the field from serialization (model_dump, JSON). The field still exists in the model but won't appear in serialized output. Useful for internal fields that shouldn't be exposed.

### Q11: When should you use native dataclasses over Pydantic?

**Answer:** Use native dataclasses for internal data structures that don't need validation, when maximum performance is needed, when you need to use instances as dict keys (frozen=True), or when you want to avoid Pydantic dependency.

### Q12: What is `default_factory`?

**Answer:** `default_factory` is a function that returns the default value for mutable fields. It's used instead of mutable defaults (like `[]` or `{}`) which would be shared across instances. Example: `field(default_factory=list)`.

### Q13: How do you make a dataclass hashable?

**Answer:** Use `frozen=True` to make it hashable. This makes it immutable and auto-generates `__hash__`. Without `frozen=True`, dataclasses are unhashable by default (because they're mutable).

### Q14: What is the performance difference between dataclasses and BaseModel?

**Answer:** Dataclasses are typically 3-5x faster for creation and 2-3x faster for serialization than BaseModel. The difference comes from Pydantic's validation overhead. Use dataclasses for performance-critical paths, BaseModel for complex validation.

### Q15: How do you handle optional fields in dataclasses?

**Answer:** Use `field(default=None)` or `field(default_factory=lambda: None)`. For Pydantic dataclasses, you can use `str | None = None` syntax. Example: `name: str | None = field(default=None)`.
