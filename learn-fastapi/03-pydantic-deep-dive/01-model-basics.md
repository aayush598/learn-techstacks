# Pydantic BaseModel Basics — The Complete Reference

## Table of Contents

1. [What is BaseModel](#what-is-basemodel)
2. [Creating Your First Model](#creating-your-first-model)
3. [Field Types](#field-types)
4. [Default Values](#default-values)
5. [Required vs Optional Fields](#required-vs-optional-fields)
6. [Model Initialization](#model-initialization)
7. [model_dump() — Exporting Data](#model_dump)
8. [model_dump_json() — JSON String Output](#model_dump_json)
9. [model_validate() — Class Method Validation](#model_validate)
10. [model_validate_json() — Parsing JSON Strings](#model_validate_json)
11. [model_json_schema() — Schema Generation](#model_json_schema)
12. [model_copy() — Cloning Models](#model_copy)
13. [model_construct() — Skip Validation](#model_construct)
14. [model_fields — Field Introspection](#model_fields)
15. [model_extra — Extra Data Access](#model_extra)
16. [Best Practices](#best-practices)
17. [Interview Questions](#interview-questions)

---

## What is BaseModel

Pydantic's `BaseModel` is the foundation of data validation in Python. It uses **type hints** to define the expected shape of data, and **validates and coerces** incoming data at runtime. If validation fails, it raises a `ValidationError` with detailed error messages.

```python
from pydantic import BaseModel

# Every Pydantic model inherits from BaseModel
class User(BaseModel):
    name: str
    age: int
```

### Why Pydantic?

- **Type safety** — enforces types at runtime, not just in static analysis
- **Auto-coercion** — `"42"` becomes `42` for `int` fields automatically
- **Serialization** — export models as dicts or JSON with one method call
- **JSON Schema** — auto-generate OpenAPI-compatible schemas
- **Integration** — FastAPI uses Pydantic models for request/response validation

---

## Creating Your First Model

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True  # default value

# Valid construction — auto-coerces string to float
p = Product(name="Laptop", price="999.99")
print(p.name)       # "Laptop"
print(p.price)      # 999.99 (float, not string)
print(p.in_stock)   # True

# Invalid construction — raises ValidationError
try:
    p = Product(name=123, price="not_a_number")
except Exception as e:
    print(e)
    # 2 validation errors for Product
    #   Input should be a valid string [type=string_type ...]
    #   Input should be a valid number [type=number_parsing ...]
```

### Key Behavior: Models are Immutable by Default

```python
p = Product(name="Laptop", price=999.99)

try:
    p.price = 500.00  # AttributeError — models are frozen by default... NOT!
except AttributeError as e:
    print(e)
else:
    print("Pydantic V2 allows mutation by default!")
    # In Pydantic V2, models are mutable by default
    # To make immutable, use: model_config = ConfigDict(frozen=True)
```

> **Pydantic V2 change**: Models are mutable by default. In V1, they were immutable. Use `ConfigDict(frozen=True)` for immutability.

---

## Field Types

Pydantic supports all Python standard library types plus custom types:

```python
from pydantic import BaseModel
from datetime import datetime, date, time, timedelta
from uuid import UUID
from enum import Enum
from typing import Optional, List, Dict, Set, Tuple

class AllTypes(BaseModel):
    # Primitives
    name: str
    age: int
    score: float
    active: bool
    raw_data: bytes

    # Date/Time
    created_at: datetime
    birth_date: date
    alarm_time: time
    session_duration: timedelta

    # UUID
    id: UUID

    # Collections
    tags: List[str]
    metadata: Dict[str, int]
    unique_ids: Set[int]
    coordinates: Tuple[float, float]

    # Optional (None allowed)
    nickname: Optional[str] = None
    middle_name: str | None = None  # Python 3.10+ syntax

    # Enum
    class Role(str, Enum):
        ADMIN = "admin"
        USER = "user"

    role: Role = Role.USER
```

---

## Default Values

### Static Defaults

```python
class Config(BaseModel):
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    version: str = "1.0.0"
```

### Default None (Optional)

```python
class UserProfile(BaseModel):
    name: str
    email: str
    phone: str | None = None       # Optional, defaults to None
    bio: str | None = None
```

### Using `Field()` for Defaults

```python
from pydantic import BaseModel, Field

class Server(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080, description="Port to listen on")
    workers: int = Field(default=1, ge=1, le=32)
```

### Default Factories (Mutable Defaults)

```python
from pydantic import BaseModel, Field

class Team(BaseModel):
    name: str
    members: list[str] = Field(default_factory=list)  # NOT []
    scores: dict[str, int] = Field(default_factory=dict)  # NOT {}
    tags: set[str] = Field(default_factory=lambda: {"default"})
```

> **Critical Rule**: Never use mutable defaults directly (`list`, `dict`, `set`). Always use `Field(default_factory=...)`. Pydantic handles this for you — using `[]` directly would actually work in Pydantic (it creates a new instance per model), but `default_factory` is the explicit, recommended pattern.

---

## Required vs Optional Fields

### Pydantic V2 Field Classification

```python
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    # REQUIRED — no default value
    name: str
    email: str
    age: int

    # OPTIONAL — has a default value (including None)
    nickname: str = ""           # Optional with empty string default
    bio: str | None = None       # Optional with None default
    score: float = 0.0           # Optional with numeric default

    # Using Field() with default
    role: str = Field(default="user")
    is_active: bool = Field(default=True)
```

### Explicitly Required with `Field(...)` Ellipsis

```python
class Product(BaseModel):
    # The `...` (Ellipsis) explicitly marks a field as required
    name: str = Field(...)
    price: float = Field(...)
    description: str = Field(default="No description")
    quantity: int = Field(default=0, ge=0)
```

### Required with `Field(required=True)` — Same as `...`

```python
class Order(BaseModel):
    item_id: str = Field(required=True)
    quantity: int = Field(required=True, gt=0)
    notes: str = Field(default="")
```

### Optional Fields in Python 3.10+ (PEP 604 Union Syntax)

```python
# These are equivalent:
class A(BaseModel):
    name: Optional[str] = None    # Pre-3.10 style
    name: str | None = None       # 3.10+ style

# Neither requires a value — both default to None
a = A()  # Valid: A(name=None)
```

---

## Model Initialization

### From Keyword Arguments

```python
class User(BaseModel):
    name: str
    age: int
    email: str

user = User(name="Alice", age=30, email="alice@example.com")
print(user)  # User(name='Alice', age=30, email='alice@example.com')
```

### From a Dictionary (Unpacking)

```python
data = {"name": "Bob", "age": 25, "email": "bob@example.com"}

# Option 1: Unpack with **
user = User(**data)

# Option 2: Use model_validate
user = User.model_validate(data)

# Both produce the same result
```

### From a Dictionary with Extra Keys

```python
data = {
    "name": "Charlie",
    "age": 35,
    "email": "charlie@example.com",
    "extra_field": "this will be ignored or cause error"
}

# Default behavior: extra fields are IGNORED (silently dropped)
user = User.model_validate(data)
# user.extra_field does NOT exist

# If you want to FORBID extra fields:
from pydantic import ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
    age: int
    email: str

try:
    user = StrictUser.model_validate(data)
except Exception as e:
    print(e)  # Error: Extra inputs are not permitted
```

### From JSON String

```python
import json

json_str = '{"name": "Dave", "age": 28, "email": "dave@example.com"}'

# Parse JSON and validate
user = User.model_validate_json(json_str)
print(user.name)  # "Dave"
```

### From ORM Object (from_attributes)

```python
from pydantic import BaseModel, ConfigDict

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    age: int
    email: str

# Simulating an ORM object (e.g., SQLAlchemy)
class FakeORMUser:
    def __init__(self):
        self.name = "Eve"
        self.age = 32
        self.email = "eve@example.com"

orm_user = FakeORMUser()
schema = UserSchema.model_validate(orm_user)
print(schema.name)  # "Eve"
```

---

## model_dump()

Converts a model instance into a Python dictionary.

### Basic Usage

```python
class User(BaseModel):
    name: str
    age: int
    email: str
    score: float = 0.0

user = User(name="Alice", age=30, email="alice@example.com", score=95.5)

# Basic dump
data = user.model_dump()
print(data)
# {'name': 'Alice', 'age': 30, 'email': 'alice@example.com', 'score': 95.5}
```

### Excluding Fields

```python
# Exclude specific fields
data = user.model_dump(exclude={"email"})
print(data)  # {'name': 'Alice', 'age': 30, 'score': 95.5}

# Exclude multiple fields
data = user.model_dump(exclude={"email", "score"})
print(data)  # {'name': 'Alice', 'age': 30}
```

### Including Only Specific Fields

```python
# Include only specific fields
data = user.model_dump(include={"name", "age"})
print(data)  # {'name': 'Alice', 'age': 30}
```

### Excluding None Values

```python
class UserWithOptional(BaseModel):
    name: str
    age: int
    nickname: str | None = None
    bio: str | None = None

user = UserWithOptional(name="Bob", age=25)

data = user.model_dump(exclude_none=True)
print(data)  # {'name': 'Bob', 'age': 25} — None fields removed
```

### Excluding_unset (Only Changed Fields)

```python
class Settings(BaseModel):
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    log_level: str = "info"

# Only set some fields
settings = Settings(host="0.0.0.0", debug=True)

# Exclude_unset shows only what was explicitly provided
data = settings.model_dump(exclude_unset=True)
print(data)  # {'host': '0.0.0.0', 'debug': True}
# 'port' and 'log_level' excluded because they were not explicitly set
```

### Deep Dump (Nested Models)

```python
class Address(BaseModel):
    street: str
    city: str

class UserWithAddress(BaseModel):
    name: str
    address: Address

user = UserWithAddress(
    name="Charlie",
    address=Address(street="123 Main St", city="Springfield")
)

# Deep dump — nested models are also converted
data = user.model_dump()
print(data)
# {'name': 'Charlie', 'address': {'street': '123 Main St', 'city': 'Springfield'}}
```

### Mode Parameter

```python
# mode='python' (default) — returns Python native types
# mode='json' — returns JSON-serializable types (datetimes as strings, etc.)

from datetime import datetime

class Event(BaseModel):
    name: str
    start: datetime

event = Event(name="Conference", start=datetime(2025, 6, 15, 9, 0))

# Default python mode — datetime object remains
python_data = event.model_dump()
print(type(python_data['start']))  # <class 'datetime.datetime'>

# JSON mode — datetime converted to ISO string
json_data = event.model_dump(mode='json')
print(type(json_data['start']))  # <class 'str'>
print(json_data['start'])         # '2025-06-15T09:00:00'
```

---

## model_dump_json()

Returns a JSON string directly — no intermediate dict needed.

```python
from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    name: str
    start: datetime

event = Event(name="Conference", start=datetime(2025, 6, 15, 9, 0))

# model_dump_json() — returns a JSON string
json_str = event.model_dump_json()
print(json_str)
# '{"name":"Conference","start":"2025-06-15T09:00:00"}'

# With exclude_none
class User(BaseModel):
    name: str
    email: str | None = None

user = User(name="Alice")
print(user.model_dump_json(exclude_none=True))
# '{"name":"Alice"}'

# With indent for readability
print(event.model_dump_json(indent=2))
# {
#   "name": "Conference",
#   "start": "2025-06-15T09:00:00"
# }
```

### Performance Tip

```python
# SLOW (two steps, intermediate dict):
json_str = json.dumps(user.model_dump())

# FAST (one step, direct serialization):
json_str = user.model_dump_json()

# model_dump_json() is significantly faster for large models
# because it avoids creating the intermediate Python dict
```

---

## model_validate()

A class method that validates a dictionary (or other mapping) and returns a model instance.

```python
class User(BaseModel):
    name: str
    age: int
    email: str

# From a dictionary
data = {"name": "Alice", "age": 30, "email": "alice@example.com"}
user = User.model_validate(data)
print(user)  # User(name='Alice', age=30, email='alice@example.com')

# With type coercion
data = {"name": "Bob", "age": "25", "email": "bob@example.com"}  # age is string!
user = User.model_validate(data)
print(user.age)  # 25 (int, auto-coerced from string)
```

### From OrderedDict

```python
from collections import OrderedDict

data = OrderedDict([("name", "Charlie"), ("age", 35), ("email", "charlie@x.com")])
user = User.model_validate(data)
```

### From Another Model Instance

```python
class UserCreate(BaseModel):
    name: str
    age: int
    email: str
    password: str  # Extra field

class UserResponse(BaseModel):
    name: str
    age: int
    email: str

# Convert one model to another
create_user = UserCreate(name="Dave", age=28, email="dave@x.com", password="secret")
response = UserResponse.model_validate(create_user)
print(response)  # UserResponse(name='Dave', age=28, email='dave@x.com')
```

---

## model_validate_json()

Validates a JSON string and returns a model instance.

```python
json_str = '{"name": "Eve", "age": 32, "email": "eve@example.com"}'

user = User.model_validate_json(json_str)
print(user.name)  # "Eve"
```

### Handling Encoding

```python
# If JSON is bytes, it also works
json_bytes = b'{"name": "Frank", "age": 40, "email": "frank@example.com"}'
user = User.model_validate_json(json_bytes)
```

### Strict vs Lax Mode

```python
from pydantic import BaseModel

class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)
    count: int

# Lax mode (default): coerces "5" → 5
m = StrictModel.model_validate({"count": "5"})
print(m.count)  # 5

# Strict mode: rejects "5" for int field
try:
    m = StrictModel.model_validate({"count": "5"})
except Exception as e:
    print(e)  # Input should be a valid integer
```

---

## model_json_schema()

Generates a JSON Schema for the model — essential for OpenAPI documentation.

```python
class User(BaseModel):
    name: str
    age: int
    email: str
    score: float = 0.0
    is_active: bool = True

schema = User.model_json_schema()
print(schema)
```

Output:

```json
{
  "properties": {
    "name": {"title": "Name", "type": "string"},
    "age": {"title": "Age", "type": "integer"},
    "email": {"title": "Email", "type": "string"},
    "score": {"default": 0.0, "title": "Score", "type": "number"},
    "is_active": {"default": true, "title": "Is Active", "type": "boolean"}
  },
  "required": ["name", "age", "email"],
  "title": "User",
  "type": "object"
}
```

### Schema with Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class UserWithAddress(BaseModel):
    name: str
    address: Address

schema = UserWithAddress.model_json_schema()
print(schema)
```

### Schema Customization

```python
class Product(BaseModel):
    name: str = Field(description="Product name", examples=["Widget"])
    price: float = Field(description="Price in USD", gt=0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Widget", "price": 9.99}
            ]
        }
    }

schema = Product.model_json_schema()
print(schema)
```

---

## model_copy()

Creates a copy of a model, optionally overriding specific fields.

```python
class User(BaseModel):
    name: str
    age: int
    email: str

user = User(name="Alice", age=30, email="alice@example.com")

# Simple copy
copied = user.model_copy()
print(copied)  # Same as original

# Copy with updates (like dataclasses.replace)
updated = user.model_copy(update={"age": 31, "email": "alice_new@example.com"})
print(updated)  # User(name='Alice', age=31, email='alice_new@example.com')
print(user)     # Original unchanged: User(name='Alice', age=30, email='alice@example.com')
```

### Use Case: Creating Variants

```python
class Product(BaseModel):
    name: str
    price: float
    quantity: int

base_product = Product(name="Widget", price=9.99, quantity=100)

# Create sale variant
sale_product = base_product.model_copy(update={"price": 7.99})
```

> **Note**: `model_copy` performs a shallow copy. For deep copies, use `copy.deepcopy()`.

---

## model_construct()

Creates a model instance **without validation**. This is the fastest way to create a model, but you must ensure the data is already valid.

```python
class User(BaseModel):
    name: str
    age: int
    email: str

# Normal construction (validates)
user = User(name="Alice", age=30, email="alice@example.com")

# model_construct — NO validation
user = User.model_construct(name="Bob", age=25, email="bob@example.com")
print(user.name)  # "Bob"

# Can set arbitrary attributes (no validation!)
user = User.model_construct(name="Charlie", age="not_a_number", extra_field="anything")
print(user.age)  # "not_a_number" — WRONG, but no error raised
print(user.extra_field)  # "anything" — extra fields allowed without validation
```

### When to Use model_construct

```python
# 1. Performance-critical code where you've already validated
validated_data = complex_validation(data)
user = User.model_construct(**validated_data)  # Skip double validation

# 2. Creating models from trusted internal sources
user = User.model_construct(
    name=get_name_from_db(),
    age=get_age_from_db(),
    email=get_email_from_db()
)

# 3. Building partial models for updates
partial_user = User.model_construct(name="Alice")  # age and email are None
```

### Dangers of model_construct

```python
# WRONG — no validation means garbage in, garbage out
user = User.model_construct(name=123, age="hello", email=None)
# No error! But model is in an invalid state

# model_dump() will also skip validation on nested models
# This can propagate invalid data through your system
```

---

## model_fields

A dictionary containing the field information for the model.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(description="User's full name")
    age: int = Field(ge=0, description="Age in years")
    email: str = Field(description="Email address")
    score: float = Field(default=0.0, description="Test score")

# Access model_fields
print(User.model_fields)
# {'name': FieldInfo(description='User's full name', ...),
#  'age': FieldInfo(ge=0, description='Age in years', ...),
#  'email': FieldInfo(description='Email address', ...),
#  'score': FieldInfo(default=0.0, description='Test score', ...)}

# Get specific field info
name_field = User.model_fields['name']
print(name_field.description)  # "User's full name"
print(name_field.annotation)  # <class 'str'>

# Check if a field has a default
print('score' in [f for f, info in User.model_fields.items() if info.default is not None])
```

### Iterating Over Fields

```python
for field_name, field_info in User.model_fields.items():
    print(f"{field_name}: {field_info.annotation} (default={field_info.default})")
```

### Use Case: Dynamic Form Generation

```python
def generate_form(model_class):
    """Generate HTML form from Pydantic model fields."""
    form_html = "<form>"
    for name, info in model_class.model_fields.items():
        field_type = "text"
        if info.annotation == int:
            field_type = "number"
        elif info.annotation == bool:
            field_type = "checkbox"

        required = "required" if info.default is None else ""
        form_html += f'<input type="{field_type}" name="{name}" {required}>'
    form_html += "</form>"
    return form_html
```

---

## model_extra

Contains any extra data that was passed to the model but isn't defined as a field.

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(extra='allow')  # Allow extra fields

    name: str
    age: int

user = StrictUser(name="Alice", age=30, role="admin", department="engineering")

# Defined fields are normal attributes
print(user.name)    # "Alice"
print(user.age)     # 30

# Extra fields are in model_extra
print(user.model_extra)  # {'role': 'admin', 'department': 'engineering'}

# Access them directly (also works)
print(user.role)        # "admin"
print(user.department)  # "engineering"
```

### Extra Field Modes

```python
# extra='ignore' (default) — extra fields are silently discarded
class IgnoreModel(BaseModel):
    model_config = ConfigDict(extra='ignore')
    name: str

m = IgnoreModel(name="Alice", extra="gone")
print(m.model_extra)  # None

# extra='forbid' — extra fields cause ValidationError
class ForbidModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str

try:
    m = ForbidModel(name="Alice", extra="error")
except Exception as e:
    print(e)  # Extra inputs are not permitted

# extra='allow' — extra fields are stored
class AllowModel(BaseModel):
    model_config = ConfigDict(extra='allow')
    name: str

m = AllowModel(name="Alice", extra="kept")
print(m.model_extra)  # {'extra': 'kept'}
```

---

## Best Practices

### 1. Use Type Hints Consistently

```python
# GOOD — explicit types
class User(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True

# BAD — avoid Any and loose types
class BadUser(BaseModel):
    name: Any
    age: Any
```

### 2. Prefer `Field(default_factory=...)` for Mutable Defaults

```python
# GOOD
class Config(BaseModel):
    tags: list[str] = Field(default_factory=list)

# ALSO WORKS (Pydantic handles it internally)
class Config(BaseModel):
    tags: list[str] = []
```

### 3. Use `model_validate` Over Constructor for External Data

```python
# For external/dict data, use model_validate
data = get_data_from_api()
user = User.model_validate(data)

# For keyword args, constructor is fine
user = User(name="Alice", age=30)
```

### 4. Use `model_dump_json()` Instead of `json.dumps(model_dump())`

```python
# GOOD — faster, more correct
json_str = user.model_dump_json()

# SLOWER — creates intermediate dict
json_str = json.dumps(user.model_dump(), default=str)
```

### 5. Document Your Models

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    """Represents an authenticated user in the system."""

    name: str = Field(min_length=1, max_length=100, description="Full name")
    age: int = Field(ge=0, le=150, description="Age in years")
    email: str = Field(description="Primary email address")
```

### 6. Use ConfigDict for Model-Wide Settings

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
    )

    name: str
    email: str
```

### 7. Prefer Frozen Models for Value Objects

```python
from pydantic import BaseModel, ConfigDict

class Money(BaseModel):
    model_config = ConfigDict(frozen=True)  # Immutable

    amount: float
    currency: str

# Money instances are hashable and can be used in sets/dicts
m1 = Money(amount=10.0, currency="USD")
m2 = Money(amount=10.0, currency="USD")
print(m1 == m2)  # True
```

---

## Interview Questions

### Q1: What is Pydantic's BaseModel?

**Answer**: `BaseModel` is the core class in Pydantic that provides data validation using Python type hints. When you instantiate a model, Pydantic validates and coerces the input data according to the field type annotations. If validation fails, it raises a `ValidationError` with detailed error messages indicating which fields failed and why.

---

### Q2: How does Pydantic handle type coercion?

**Answer**: Pydantic performs **coercion by default** (lax mode). For example, a string `"42"` will be coerced to `int(42)` for an `int` field, and `42` will be coerced to `"42"` for a `str` field. To disable coercion, use `ConfigDict(strict=True)` which requires the exact type.

---

### Q3: What is the difference between `model_dump()` and `model_dump_json()`?

**Answer**: `model_dump()` returns a Python `dict`, while `model_dump_json()` returns a JSON `str`. `model_dump_json()` is generally **faster** because it serializes directly to JSON without creating an intermediate dict. Use `model_dump()` when you need to manipulate the data in Python, and `model_dump_json()` when you need the JSON string (e.g., for API responses).

---

### Q4: When would you use `model_construct()`?

**Answer**: `model_construct()` creates a model **without validation**. Use it when:
- You've already validated the data elsewhere and want to avoid double validation
- You're in a performance-critical path where validation overhead matters
- You're building partial models for incremental updates
- You're constructing models from trusted internal sources

**Never use it** when data comes from untrusted sources (user input, API calls).

---

### Q5: How do you handle extra fields?

**Answer**: Pydantic provides three `extra` modes via `ConfigDict`:
- `extra='ignore'` (default): Extra fields are silently discarded
- `extra='forbid'`: Extra fields raise a `ValidationError`
- `extra='allow'`: Extra fields are stored in `model_extra`

Use `extra='allow'` when you need to preserve unknown fields (e.g., webhook payloads), `extra='forbid'` for strict APIs, and `extra='ignore'` when you only care about known fields.

---

### Q6: What does `model_copy(update={})` do?

**Answer**: `model_copy()` creates a shallow copy of the model. The `update` parameter accepts a dict of field overrides, allowing you to create a new model with modified values while keeping the rest unchanged. This is similar to `dataclasses.replace()`. The original model is not mutated.

---

### Q7: How does `model_validate()` differ from the constructor?

**Answer**: Both validate and create model instances. The difference:
- **Constructor**: `User(name="Alice", age=30)` — keyword arguments
- **model_validate**: `User.model_validate({"name": "Alice", "age": 30})` — dict input

`model_validate()` is preferred when working with dicts (e.g., from databases, APIs, JSON). It also works with ORM objects when `from_attributes=True` is configured.

---

### Q8: What is `model_fields` used for?

**Answer**: `model_fields` is a class attribute (dict) containing `FieldInfo` objects for each model field. It's useful for:
- Dynamically generating forms or documentation
- Inspecting field metadata at runtime
- Building serializers or validators dynamically
- Framework integration (FastAPI uses it for OpenAPI schema generation)

---

### Q9: Can you create a model without defining a class?

**Answer**: Yes, using `pydantic.create_model()` or `TypeAdapter`. These are covered in detail in the Dynamic Models section. For simple cases, `TypeAdapter` is the recommended approach for validating data without a full model class.

---

### Q10: What happens if you pass a string to an `int` field?

**Answer**: In **lax mode** (default), Pydantic coerces the string to an integer: `"42"` becomes `42`. If the string isn't a valid integer (e.g., `"hello"`), it raises a `ValidationError`. In **strict mode** (`ConfigDict(strict=True)`), it rejects the string entirely and raises a `ValidationError`.

---
