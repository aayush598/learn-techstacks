# Pydantic Model Configuration (ConfigDict) — The Complete Reference

## Table of Contents

1. [What is ConfigDict](#configdict)
2. [title — Model Title](#title)
3. [str_strip_whitespace](#str-strip-whitespace)
4. [validate_assignment](#validate-assignment)
5. [extra — Extra Field Handling](#extra)
6. [from_attributes (orm_mode)](#from-attributes)
7. [populate_by_name](#populate-by-name)
8. [use_enum_values](#use-enum-values)
9. [frozen — Immutability](#frozen)
10. [json_schema_extra](#json-schema-extra)
11. [alias_generator](#alias-generator)
12. [arbitrary_types_allowed](#arbitrary-types-allowed)
13. [json_encoders (Deprecated)](#json-encoders)
14. [Other ConfigDict Options](#other-options)
15. [Best Practices](#best-practices)
16. [Interview Questions](#interview-questions)

---

## Configdict

`ConfigDict` is the modern way to configure Pydantic models (Pydantic V2). It replaces the old inner `class Config` approach.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid',
        frozen=True,
    )

    name: str
    age: int
```

### Old Style (V1 Compatibility — Deprecated)

```python
# OLD STYLE — still works but deprecated
class User(BaseModel):
    class Config:
        str_strip_whitespace = True
        validate_assignment = True

    name: str
```

---

## title

Sets the model title in the JSON schema.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(title="UserAccount")

    name: str
    email: str

schema = User.model_json_schema()
print(schema.get("title"))  # "UserAccount"
```

---

## str-strip-whitespace

Strips leading/trailing whitespace from all string fields.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    email: str

user = User(name="  Alice  ", email="  alice@x.com  ")
print(user.name)   # "Alice"
print(user.email)  # "alice@x.com"

# Without str_strip_whitespace (default)
class Unstripped(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False)
    name: str

user = Unstripped(name="  Alice  ")
print(user.name)  # "  Alice  "
```

---

## validate-assignment

Validates field values when they are assigned after model creation.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    name: str
    age: int

user = User(name="Alice", age=30)
user.age = 31  # Valid assignment
print(user.age)  # 31

# Invalid assignment — raises ValidationError
try:
    user.age = -5  # Validation runs on assignment
except Exception as e:
    print(e)  # Input should be greater than 0

# Without validate_assignment (default), invalid values are accepted
class NoValidation(BaseModel):
    age: int

user = NoValidation(age=30)
user.age = "not a number"  # No validation, type is "str" not "int"
```

### With Constraints

```python
from pydantic import BaseModel, ConfigDict, Field

class Account(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    username: str = Field(min_length=3, max_length=50)
    balance: float = Field(ge=0)

account = Account(username="alice", balance=100.0)
account.balance = 200.0  # Valid

try:
    account.username = "ab"  # Too short
except Exception as e:
    print(e)  # String should have at least 3 characters

try:
    account.balance = -50  # Negative
except Exception as e:
    print(e)  # Input should be greater than or equal to 0
```

---

## extra

Controls how extra fields (not defined in the model) are handled.

### extra='ignore' (Default)

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: str

user = User(name="Alice", extra_field="gone")
print(user.model_extra)  # None — extra field silently dropped
```

### extra='forbid'

```python
class StrictUser(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str

try:
    user = StrictUser(name="Alice", extra_field="error")
except Exception as e:
    print(e)  # Extra inputs are not permitted
```

### extra='allow'

```python
class FlexibleUser(BaseModel):
    model_config = ConfigDict(extra='allow')

    name: str

user = FlexibleUser(name="Alice", role="admin", dept="eng")
print(user.model_extra)  # {'role': 'admin', 'dept': 'eng'}
print(user.role)         # "admin" — accessible as attribute
```

### Use Cases

| Mode | Use Case |
|------|----------|
| `ignore` | APIs where unknown fields should be silently ignored |
| `forbid` | Strict APIs where unknown fields indicate a bug |
| `allow` | Webhooks, event payloads where schema may evolve |

---

## from-attributes

Enables creating models from ORM objects (formerly `orm_mode`).

```python
from pydantic import BaseModel, ConfigDict

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    age: int
    email: str

# Simulating a SQLAlchemy model
class SQLAlchemyUser:
    def __init__(self):
        self.name = "Alice"
        self.age = 30
        self.email = "alice@example.com"

orm_user = SQLAlchemyUser()
schema = UserSchema.model_validate(orm_user)
print(schema.name)  # "Alice"
```

### With FastAPI and SQLAlchemy

```python
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# SQLAlchemy model
class Base(DeclarativeBase):
    pass

class DBUser(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

# Pydantic schema
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str

app = FastAPI()

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    db_user = DBUser(id=1, name="Alice", email="alice@x.com")
    return db_user  # FastAPI uses from_attributes to convert
```

### Nested ORM Objects

```python
from pydantic import BaseModel, ConfigDict

class AddressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    street: str
    city: str

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    address: AddressSchema  # Nested ORM object

# Simulated ORM
class FakeAddress:
    def __init__(self):
        self.street = "123 Main St"
        self.city = "Springfield"

class FakeUser:
    def __init__(self):
        self.name = "Alice"
        self.address = FakeAddress()

schema = UserSchema.model_validate(FakeUser())
print(schema.address.city)  # "Springfield"
```

---

## populate-by-name

Allows using either the field name or the alias to construct a model.

```python
from pydantic import BaseModel, Field, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_name: str = Field(alias="userName")
    first_name: str = Field(alias="firstName")

# Using alias
user = User.model_validate({"userName": "alice", "firstName": "Alice"})
print(user.user_name)  # "alice"

# Using original field name (with populate_by_name=True)
user = User(user_name="bob", firstName="Bob")
print(user.user_name)  # "bob"

# Without populate_by_name, only alias works
class StrictAlias(BaseModel):
    user_name: str = Field(alias="userName")

# StrictAlias(user_name="alice")  # Would fail
user = StrictAlias(userName="alice")  # Only alias works
```

### Important for FastAPI

```python
from pydantic import BaseModel, Field, ConfigDict

# In FastAPI, you often want both camelCase (JSON) and snake_case (Python)
class CreateUserRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_name: str = Field(alias="userName")
    email: str = Field(alias="emailAddress")

# Both work in FastAPI:
# POST /users {"userName": "alice", "emailAddress": "alice@x.com"}
# POST /users {"user_name": "alice", "email": "alice@x.com"}
```

---

## use-enum-values

Stores enum values instead of enum members.

```python
from enum import Enum
from pydantic import BaseModel, ConfigDict

class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

# Without use_enum_values (default)
class Painting1(BaseModel):
    color: Color

p1 = Painting1(color="red")
print(p1.color)        # Color.RED
print(p1.color.value)  # "red"
print(type(p1.color))  # <enum 'Color'>

# With use_enum_values
class Painting2(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    color: Color

p2 = Painting2(color="red")
print(p2.color)        # "red"
print(type(p2.color))  # <class 'str'>
```

### Use Cases

```python
# Good for: APIs where you want plain string values
# Good for: Database serialization (no enum object issues)
# Bad for: When you need enum methods/properties

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    status: Status

user = User(status="active")
print(user.status)  # "active" (plain string)
```

---

## frozen

Makes the model immutable (all fields become frozen/readonly).

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    age: int

user = User(name="Alice", age=30)

try:
    user.name = "Bob"  # Raises error
except Exception as e:
    print(type(e).__name__)  # ValidationError

# Frozen models are hashable (can be used in sets/dicts)
user1 = User(name="Alice", age=30)
user2 = User(name="Alice", age=30)
print(user1 == user2)  # True

# Can use as dict keys
user_set = {user1, user2}
print(len(user_set))  # 1 (same model)
```

### frozen vs frozen_model

```python
# ConfigDict(frozen=True) — whole model immutable
class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str

# Individual frozen fields — use Field(frozen=True)
from pydantic import BaseModel, Field

class PartiallyFrozen(BaseModel):
    immutable_id: int = Field(frozen=True)
    mutable_name: str  # Can be changed

m = PartiallyFrozen(immutable_id=1, mutable_name="Alice")
m.mutable_name = "Bob"   # OK
# m.immutable_id = 2     # ValidationError
```

---

## json-schema-extra

Adds extra metadata to the JSON schema.

### As a Dict

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"name": "Alice", "age": 30}
            ],
            "externalDocs": {
                "description": "User API docs",
                "url": "https://docs.example.com/users"
            }
        }
    )

    name: str
    age: int

schema = User.model_json_schema()
print(schema.get("examples"))
# [{'name': 'Alice', 'age': 30}]
```

### As a Callable

```python
def add_timestamp(schema: dict) -> dict:
    schema["properties"]["_schema_version"] = {"type": "string", "default": "1.0"}
    return schema

class User(BaseModel):
    model_config = ConfigDict(json_schema_extra=add_timestamp)

    name: str
    age: int

schema = User.model_json_schema()
print("_schema_version" in schema.get("properties", {}))  # True
```

---

## alias-generator

Automatically generates aliases for all fields.

```python
from pydantic import BaseModel, ConfigDict

def to_camel(string: str) -> str:
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True  # Allow using original names too
    )

    user_name: str
    first_name: str
    email_address: str

# Use original names
user = User(user_name="alice", first_name="Alice", email_address="alice@x.com")

# Serialize with aliases
print(user.model_dump(by_alias=True))
# {'userName': 'alice', 'firstName': 'Alice', 'emailAddress': 'alice@x.com'}

# Serialize with original names
print(user.model_dump())
# {'user_name': 'alice', 'first_name': 'Alice', 'email_address': 'alice@x.com'}
```

### Other Alias Generators

```python
# kebab-case
def to_kebab(s: str) -> str:
    return s.replace('_', '-')

# UPPER_SNAKE_CASE
def to_upper_snake(s: str) -> str:
    return s.upper()

# lowercase
def to_lower(s: str) -> str:
    return s.lower()
```

---

## arbitrary-types-allowed

Allows arbitrary types as field types.

```python
from pydantic import BaseModel, ConfigDict

class CustomClass:
    def __init__(self, value: int):
        self.value = value

class MyModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    custom: CustomClass
    name: str

obj = CustomClass(42)
m = MyModel(custom=obj, name="test")
print(m.custom.value)  # 42
```

### Use with numpy, pandas, etc.

```python
import numpy as np
from pydantic import BaseModel, ConfigDict

class ArrayModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: np.ndarray
    name: str

arr = ArrayModel(data=np.array([1, 2, 3]), name="test")
print(arr.data)  # [1 2 3]
```

---

## json-encoders (Deprecated)

> **Deprecated in Pydantic V2**. Use `field_serializer` or `PlainSerializer` instead.

```python
# OLD STYLE (V1) — DEPRECATED
from pydantic import BaseModel

class User(BaseModel):
    name: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d"),
            Decimal: lambda v: float(v),
        }

# NEW STYLE (V2) — Use serializers instead
from pydantic import BaseModel, field_serializer
from datetime import datetime
from decimal import Decimal

class User(BaseModel):
    name: str
    created_at: datetime
    amount: Decimal

    @field_serializer('created_at')
    def serialize_dt(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%d")

    @field_serializer('amount')
    def serialize_decimal(self, v: Decimal) -> float:
        return float(v)
```

---

## other-options

### str_to_lower

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(str_to_lower=True)
    name: str

user = User(name="ALICE")
print(user.name)  # "alice"
```

### str_to_upper

```python
class Code(BaseModel):
    model_config = ConfigDict(str_to_upper=True)
    country_code: str

c = Code(country_code="us")
print(c.country_code)  # "US"
```

### allow_inf_nan

```python
from pydantic import BaseModel, ConfigDict

class MathModel(BaseModel):
    model_config = ConfigDict(allow_inf_nan=True)
    value: float

m = MathModel(value=float('inf'))
print(m.value)  # inf

# With allow_inf_nan=False (default in strict mode)
class StrictMath(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)
    value: float

try:
    m = StrictMath(value=float('inf'))
except Exception as e:
    print(e)
```

### ser_json_timedelta

```python
from pydantic import BaseModel, ConfigDict
from datetime import timedelta

class Duration(BaseModel):
    model_config = ConfigDict(ser_json_timedelta='iso8601')  # Default
    timeout: timedelta

d = Duration(timeout=timedelta(hours=1))
print(d.model_dump(mode='json'))  # {'timeout': 'PT1H'}
```

### ser_json_bytes

```python
from pydantic import BaseModel, ConfigDict

class Data(BaseModel):
    model_config = ConfigDict(ser_json_bytes='base64')  # or 'hex'
    raw: bytes

d = Data(raw=b"hello")
print(d.model_dump(mode='json'))  # {'raw': 'aGVsbG8='}
```

---

## Best Practices

### 1. Always Use ConfigDict Over Inner Config Class

```python
# GOOD — modern V2 style
class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str

# DEPRECATED — old V1 style
class User(BaseModel):
    class Config:
        str_strip_whitespace = True
    name: str
```

### 2. Use from_attributes=True for ORM Integration

```python
# Always enable from_attributes when working with ORMs
class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
```

### 3. Use frozen=True for Value Objects

```python
# Immutable models are safer and hashable
class Money(BaseModel):
    model_config = ConfigDict(frozen=True)
    amount: float
    currency: str
```

### 4. Use extra='forbid' for Strict APIs

```python
# Reject unexpected fields in production APIs
class APIRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
```

### 5. Use validate_assignment for Mutable Models

```python
# Ensure validation on field assignment
class User(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    name: str
    age: int = Field(ge=0)
```

### 6. Combine populate_by_name with alias_generator

```python
class APIModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
    # Best of both worlds: camelCase for API, snake_case for Python
```

---

## Interview Questions

### Q1: What is ConfigDict and why use it over class Config?

**Answer**: `ConfigDict` is the modern (V2) way to configure Pydantic models. It's a function that returns a dict, providing type checking and IDE support. The old `class Config` approach is deprecated and may be removed in future versions.

---

### Q2: What is the difference between extra='ignore', 'forbid', and 'allow'?

**Answer**:
- `ignore` (default): Extra fields are silently dropped
- `forbid`: Extra fields raise a `ValidationError`
- `allow`: Extra fields are stored in `model_extra` and accessible as attributes

---

### Q3: What does validate_assignment do?

**Answer**: When `True`, Pydantic re-validates field values when they're assigned after model creation. Without it, you can set a field to any value (even invalid types) after construction.

---

### Q4: What is from_attributes (formerly orm_mode)?

**Answer**: When `True`, allows creating model instances from ORM objects using `model_validate(orm_object)`. Pydantic accesses object attributes instead of dict keys. Essential for FastAPI with SQLAlchemy.

---

### Q5: When would you use frozen=True?

**Answer**: Use `frozen=True` for:
- Value objects (Money, Coordinates, etc.)
- Models that should be immutable
- Models used as dict keys or in sets (frozen models are hashable)
- Thread-safety when sharing model instances

---

### Q6: What does populate_by_name do?

**Answer**: When `True`, allows constructing a model using either the field's original name or its alias. Without it, only the alias is accepted for input.

---

### Q7: Why is json_encoders deprecated?

**Answer**: In Pydantic V2, `json_encoders` is replaced by `@field_serializer`, `PlainSerializer`, and `WrapSerializer`. These provide more control, better performance, and clearer semantics than the old encoder dict.

---

### Q8: How does use_enum_values affect serialization?

**Answer**: When `True`, Pydantic stores the enum member's **value** (e.g., `"red"`) instead of the enum object (`Color.RED`). This simplifies serialization but means you lose access to enum methods and properties.

---

### Q9: What is arbitrary_types_allowed?

**Answer**: When `True`, allows using any Python class as a field type (not just Pydantic-supported types). Required for fields with types like `numpy.ndarray`, custom classes, or third-party types.

---

### Q10: How do you add examples to a model's JSON schema?

**Answer**: Use `json_schema_extra` in `ConfigDict`:

```python
model_config = ConfigDict(
    json_schema_extra={"examples": [{"name": "Alice", "age": 30}]}
)
```

Or use `Field(examples=[...])` on individual fields.

---
