# Pydantic Serializers — The Complete Reference

## Table of Contents

1. [Serialization Overview](#overview)
2. [model_dump() Options](#model-dump)
3. [model_dump_json() Options](#model-dump-json)
4. [field_serializer](#field-serializer)
5. [model_serializer](#model-serializer)
6. [PlainSerializer](#plain-serializer)
7. [WrapSerializer](#wrap-serializer)
8. [BeforeSerializer and AfterSerializer](#before-after-serializer)
9. [Serialization Modes](#modes)
10. [Serialization Aliases](#aliases)
11. [exclude_none, exclude_unset, exclude_defaults](#exclude-options)
12. [include and exclude Parameters](#include-exclude)
13. [Custom JSON Encoders](#json-encoders)
14. [orjson Integration](#orjson)
15. [Best Practices](#best-practices)
16. [Interview Questions](#interview-questions)

---

## Overview

Serialization converts Pydantic model instances into Python dicts or JSON strings. Pydantic V2 uses Rust-based serialization under the hood, making it extremely fast.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

user = User(name="Alice", age=30)

# To dict
user.model_dump()          # {'name': 'Alice', 'age': 30}

# To JSON string
user.model_dump_json()     # '{"name":"Alice","age":30}'
```

---

## model-dump

### Basic Usage

```python
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    age: int
    created_at: datetime

user = User(name="Alice", age=30, created_at=datetime(2025, 1, 1, 12, 0))

# Default: Python types preserved
data = user.model_dump()
print(type(data['created_at']))  # <class 'datetime.datetime'>

# mode='json': JSON-serializable types
data = user.model_dump(mode='json')
print(type(data['created_at']))  # <class 'str'>
print(data['created_at'])         # '2025-01-01T12:00:00'
```

### exclude_none

```python
class User(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None

user = User(name="Alice", email="alice@x.com")

print(user.model_dump())
# {'name': 'Alice', 'email': 'alice@x.com', 'phone': None}

print(user.model_dump(exclude_none=True))
# {'name': 'Alice', 'email': 'alice@x.com'}
```

### exclude_unset

```python
class Settings(BaseModel):
    host: str = "localhost"
    port: int = 8000
    debug: bool = False
    log_level: str = "info"

settings = Settings(host="0.0.0.0", debug=True)

# All fields
print(settings.model_dump())
# {'host': '0.0.0.0', 'port': 8000, 'debug': True, 'log_level': 'info'}

# Only explicitly set fields
print(settings.model_dump(exclude_unset=True))
# {'host': '0.0.0.0', 'debug': True}
```

### exclude_defaults

```python
class User(BaseModel):
    name: str
    age: int = 0
    is_active: bool = True
    role: str = "user"

user = User(name="Alice", age=25)

# Exclude fields at their default values
print(user.model_dump(exclude_defaults=True))
# {'name': 'Alice', 'age': 25}
```

### Deep Dump

```python
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    address: Address

user = User(name="Alice", address=Address(street="123 Main", city="NYC"))
data = user.model_dump()
# Nested Address becomes a dict: {'street': '123 Main', 'city': 'NYC'}
```

---

## model-dump-json

### Basic Usage

```python
from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    name: str
    start: datetime

event = Event(name="Conference", start=datetime(2025, 6, 15, 9, 0))
json_str = event.model_dump_json()
# '{"name":"Conference","start":"2025-06-15T09:00:00"}'
```

### Pretty Print

```python
print(event.model_dump_json(indent=2))
# {
#   "name": "Conference",
#   "start": "2025-06-15T09:00:00"
# }
```

### Exclude Options

```python
class User(BaseModel):
    name: str
    email: str | None = None
    password: str

user = User(name="Alice", email="alice@x.com", password="secret")

user.model_dump_json(exclude={"password"})
# '{"name":"Alice","email":"alice@x.com"}'

user.model_dump_json(exclude_none=True)
# '{"name":"Alice","email":"alice@x.com","password":"secret"}'
```

---

## field-serializer

### Basic Usage

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    start: datetime

    @field_serializer('start')
    def serialize_start(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%d %H:%M")

event = Event(name="Meeting", start=datetime(2025, 6, 15, 14, 30))
print(event.model_dump())  # {'name': 'Meeting', 'start': '2025-06-15 14:30'}
```

### Multiple Fields

```python
class User(BaseModel):
    name: str
    email: str
    password: str

    @field_serializer('email')
    def mask_email(self, v: str) -> str:
        local, domain = v.split('@')
        return f"{local[0]}***{local[-1]}@{domain}"

    @field_serializer('password')
    def hide_password(self, v: str) -> str:
        return "***"

user = User(name="Alice", email="alice@example.com", password="s3cret")
print(user.model_dump())
# {'name': 'Alice', 'email': 'a***e@example.com', 'password': '***'}
```

### Using SerializationInfo (Context)

```python
from pydantic import BaseModel, field_serializer, SerializationInfo

class User(BaseModel):
    name: str
    password: str

    @field_serializer('password')
    def serialize_password(self, v: str, info: SerializationInfo) -> str:
        if info.context and info.context.get('admin'):
            return v
        return "***"

user = User(name="Alice", password="secret")

print(user.model_dump())  # {'name': 'Alice', 'password': '***'}
print(user.model_dump(context={'admin': True}))
# {'name': 'Alice', 'password': 'secret'}
```

### when_used Parameter

```python
class User(BaseModel):
    name: str
    score: float

    @field_serializer('score', when_used='json')
    def format_score(self, v: float) -> str:
        return f"{v:.2f}%"

user = User(name="Alice", score=95.5)

print(user.model_dump())            # {'name': 'Alice', 'score': 95.5}
print(user.model_dump(mode='json'))  # {'name': 'Alice', 'score': '95.50%'}
```

---

## model-serializer

Serializes the entire model, overriding default field-level serialization.

### mode='plain'

```python
from pydantic import BaseModel, model_serializer

class User(BaseModel):
    first_name: str
    last_name: str
    age: int

    @model_serializer
    def serialize_model(self) -> dict:
        return {
            "full_name": f"{self.first_name} {self.last_name}",
            "age": self.age,
            "is_adult": self.age >= 18
        }

user = User(first_name="Alice", last_name="Smith", age=30)
print(user.model_dump())
# {'full_name': 'Alice Smith', 'age': 30, 'is_adult': True}
```

### mode='wrap'

```python
from pydantic import BaseModel, model_serializer

class User(BaseModel):
    name: str
    email: str
    password: str

    @model_serializer(mode='wrap')
    def custom_serialize(self, default_serializer, info) -> dict:
        data = default_serializer(self)
        if not (info.context and info.context.get('admin')):
            data.pop('password', None)
        return data

user = User(name="Alice", email="alice@x.com", password="secret")

print(user.model_dump())
# {'name': 'Alice', 'email': 'alice@x.com', 'password': 'secret'}

print(user.model_dump(context={'admin': True}))
# {'name': 'Alice', 'email': 'alice@x.com', 'password': 'secret'}
```

### Adding Metadata with mode='wrap'

```python
from pydantic import BaseModel, model_serializer
from datetime import datetime

class User(BaseModel):
    name: str
    email: str

    @model_serializer(mode='wrap')
    def add_metadata(self, default_serializer, info) -> dict:
        data = default_serializer(self)
        data['_metadata'] = {
            'serialized_at': datetime.now().isoformat(),
            'model': 'User'
        }
        return data

user = User(name="Alice", email="alice@x.com")
data = user.model_dump()
print('_metadata' in data)  # True
```

---

## plain-serializer

Type-level serializer that replaces default serialization.

```python
from typing import Annotated
from pydantic import BaseModel, PlainSerializer

class User(BaseModel):
    name: str
    score: Annotated[
        float,
        PlainSerializer(lambda v: f"{v:.2f}%")
    ]

user = User(name="Alice", score=95.5)
print(user.model_dump())  # {'name': 'Alice', 'score': '95.50%'}
```

### PlainSerializer with when_used

```python
from typing import Annotated
from pydantic import BaseModel, PlainSerializer

class User(BaseModel):
    name: str
    score: Annotated[
        float,
        PlainSerializer(lambda v: f"{v:.2f}%", when_used='json')
    ]

user = User(name="Alice", score=95.5)
print(user.model_dump())            # {'name': 'Alice', 'score': 95.5}
print(user.model_dump(mode='json'))  # {'name': 'Alice', 'score': '95.50%'}
```

---

## wrap-serializer

Type-level serializer with full control.

```python
from typing import Annotated
from pydantic import BaseModel, WrapSerializer

def format_currency(v, handler, info):
    if info.mode == 'json':
        return f"${v:.2f}"
    return handler(v)

class Product(BaseModel):
    name: str
    price: Annotated[float, WrapSerializer(format_currency)]

p = Product(name="Widget", price=9.99)
print(p.model_dump())            # {'name': 'Widget', 'price': 9.99}
print(p.model_dump(mode='json'))  # {'name': 'Widget', 'price': '$9.99'}
```

---

## before-after-serializer

### BeforeSerializer

Runs before default serialization.

```python
from typing import Annotated
from pydantic import BaseModel, BeforeSerializer

class User(BaseModel):
    name: str
    tags: Annotated[
        list[str],
        BeforeSerializer(lambda v: sorted(v))
    ]

user = User(name="Alice", tags=["c", "a", "b"])
print(user.model_dump())  # {'name': 'Alice', 'tags': ['a', 'b', 'c']}
```

### AfterSerializer

Runs after default serialization.

```python
from typing import Annotated
from pydantic import BaseModel, AfterSerializer

class User(BaseModel):
    name: str
    score: Annotated[
        float,
        AfterSerializer(lambda v: round(v, 2))
    ]

user = User(name="Alice", score=95.678)
print(user.model_dump())  # {'name': 'Alice', 'score': 95.68}
```

---

## modes

### 'python' Mode (Default)

Returns Python native types (datetime objects, UUID objects, etc.).

```python
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class User(BaseModel):
    name: str
    created_at: datetime
    id: UUID

user = User(name="Alice", created_at=datetime.now(), id=UUID('12345678-1234-5678-1234-567812345678'))

data = user.model_dump()
print(type(data['created_at']))  # <class 'datetime.datetime'>
print(type(data['id']))          # <class 'uuid.UUID'>
```

### 'json' Mode

Returns JSON-serializable types (strings for datetime, etc.).

```python
data = user.model_dump(mode='json')
print(type(data['created_at']))  # <class 'str'>
print(data['created_at'])         # '2025-01-15T12:00:00'
print(type(data['id']))          # <class 'str'>
```

---

## aliases

```python
from pydantic import BaseModel, Field, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_name: str = Field(serialization_alias="userName")
    first_name: str = Field(serialization_alias="firstName")

user = User(user_name="alice", first_name="Alice")

# Default: uses field names
print(user.model_dump())  # {'user_name': 'alice', 'first_name': 'Alice'}

# With by_alias: uses serialization aliases
print(user.model_dump(by_alias=True))  # {'userName': 'alice', 'firstName': 'Alice'}
print(user.model_dump_json(by_alias=True))  # '{"userName":"alice","firstName":"Alice"}'
```

### Alias Generator for Serialization

```python
from pydantic import BaseModel, ConfigDict

def to_camel(s: str) -> str:
    parts = s.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])

class User(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_name: str
    first_name: str

user = User(user_name="alice", first_name="Alice")
print(user.model_dump(by_alias=True))  # {'userName': 'alice', 'firstName': 'Alice'}
```

---

## exclude-options

### Comparison

```python
class User(BaseModel):
    name: str
    age: int = 0
    email: str | None = None
    role: str = "user"
    is_active: bool = True

user = User(name="Alice", age=25)

# exclude_none: removes None values
print(user.model_dump(exclude_none=True))
# {'name': 'Alice', 'age': 25, 'role': 'user', 'is_active': True}

# exclude_unset: removes fields not explicitly set
print(user.model_dump(exclude_unset=True))
# {'name': 'Alice', 'age': 25}

# exclude_defaults: removes fields at their default values
print(user.model_dump(exclude_defaults=True))
# {'name': 'Alice', 'age': 25}
```

### Combining Options

```python
# Combine multiple options
print(user.model_dump(exclude_none=True, exclude_unset=True))
# {'name': 'Alice', 'age': 25}
```

---

## include-exclude

### include — Only These Fields

```python
class User(BaseModel):
    name: str
    age: int
    email: str
    password: str

user = User(name="Alice", age=30, email="alice@x.com", password="secret")

print(user.model_dump(include={"name", "age"}))
# {'name': 'Alice', 'age': 30}
```

### exclude — Remove These Fields

```python
print(user.model_dump(exclude={"password"}))
# {'name': 'Alice', 'age': 30, 'email': 'alice@x.com'}
```

### Nested Include/Exclude

```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address

user = User(name="Alice", address=Address(street="123 Main", city="NYC", zip_code="10001"))

# Exclude specific nested fields
print(user.model_dump(exclude={"address": {"zip_code"}}))
# {'name': 'Alice', 'address': {'street': '123 Main', 'city': 'NYC'}}
```

---

## json-encoders

### Pydantic V2 Approach

In Pydantic V2, custom JSON encoding is done through serializers, not `json_encoders` (which is deprecated).

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime
from pathlib import Path

class Config(BaseModel):
    name: str
    created_at: datetime
    config_path: Path

    @field_serializer('created_at')
    def serialize_datetime(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer('config_path')
    def serialize_path(self, v: Path) -> str:
        return str(v)
```

### Custom JSON Function

```python
import json
from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    name: str
    start: datetime

event = Event(name="Meeting", start=datetime(2025, 6, 15, 9, 0))

# Use model_dump_json instead of json.dumps
json_str = event.model_dump_json()
print(json_str)
```

---

## orjson

### Installation

```bash
pip install orjson
```

### Integration with Pydantic

```python
import orjson
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    age: int
    created_at: datetime

user = User(name="Alice", age=30, created_at=datetime.now())

# Method 1: Use model_dump_json (Pydantic uses orjson internally if available)
json_bytes = user.model_dump_json().encode()

# Method 2: Explicit orjson with model_dump
data = user.model_dump()
json_bytes = orjson.dumps(data)
print(json_bytes)  # b'{"name":"Alice","age":30,...}'

# Method 3: Parse JSON with orjson, then validate
json_str = '{"name":"Bob","age":25,"created_at":"2025-01-01T00:00:00"}'
data = orjson.loads(json_str)
user = User.model_validate(data)
```

### orjson Performance

```python
import orjson
import json
from pydantic import BaseModel

class LargeModel(BaseModel):
    items: list[dict]

data = {"items": [{"key": f"value_{i}"} for i in range(10000)]}
model = LargeModel.model_validate(data)

# orjson is significantly faster than standard json
%timeit json.dumps(model.model_dump())      # ~5ms
%timeit orjson.dumps(model.model_dump())    # ~0.5ms
%timeit model.model_dump_json()             # ~0.3ms (Pydantic uses Rust internally)
```

### orjson with Pydantic Types

```python
import orjson
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class User(BaseModel):
    id: UUID
    name: str
    created_at: datetime

user = User(id=UUID('12345678-1234-5678-1234-567812345678'), name="Alice", created_at=datetime.now())

# orjson handles Pydantic types natively
json_bytes = orjson.dumps(user.model_dump(mode='json'))
print(json_bytes)
```

---

## Best Practices

### 1. Use model_dump_json() Over json.dumps(model_dump())

```python
# GOOD — faster, handles types correctly
json_str = user.model_dump_json()

# SLOWER — may fail on complex types
json_str = json.dumps(user.model_dump(), default=str)
```

### 2. Use exclude_unset for PATCH Operations

```python
# Only update fields that were explicitly provided
update_data = user.model_dump(exclude_unset=True)
# Send only changed fields to the database
```

### 3. Use Context for Conditional Serialization

```python
# Control serialization behavior via context
data = user.model_dump(context={"admin": True, "verbose": True})
```

### 4. Use field_serializer for Sensitive Data

```python
class User(BaseModel):
    password: str

    @field_serializer('password')
    def hide_password(self, v: str) -> str:
        return "***"
```

### 5. Use by_alias=True for External APIs

```python
# When sending data to external services that expect camelCase
data = user.model_dump(by_alias=True)
```

---

## Interview Questions

### Q1: What is the difference between model_dump() and model_dump_json()?

**Answer**: `model_dump()` returns a Python `dict`, `model_dump_json()` returns a JSON `str`. `model_dump_json()` is faster because it serializes directly to JSON without creating an intermediate dict.

---

### Q2: What is the difference between exclude_none, exclude_unset, and exclude_defaults?

**Answer**:
- `exclude_none`: Removes fields with `None` values
- `exclude_unset`: Removes fields not explicitly provided during construction
- `exclude_defaults`: Removes fields that still have their default values

---

### Q3: How do you customize serialization for a single field?

**Answer**: Use `@field_serializer('field_name')` decorator:

```python
@field_serializer('email')
def mask_email(self, v: str) -> str:
    return v[:2] + "***" + v[v.index('@'):]
```

---

### Q4: What is the difference between @field_serializer and @model_serializer?

**Answer**: `@field_serializer` customizes serialization for a **single field**. `@model_serializer` customizes serialization for the **entire model**, overriding all field-level serialization. Use `@model_serializer(mode='wrap')` to call the default serializer and modify its output.

---

### Q5: How do you serialize with aliases?

**Answer**: Use `model_dump(by_alias=True)` or `model_dump_json(by_alias=True)`. Configure aliases with `Field(serialization_alias="...")` or `alias_generator` in `ConfigDict`.

---

### Q6: What is the `info` parameter in field_serializer?

**Answer**: `SerializationInfo` provides context about the serialization. Key attributes:
- `info.mode`: Either `'python'` or `'json'`
- `info.context`: The context dict passed via `model_dump(context={...})`
- `info.include`: The set of fields to include (if specified)
- `info.exclude`: The set of fields to exclude (if specified)

---

### Q7: How does orjson improve Pydantic serialization?

**Answer**: Pydantic V2 uses a Rust-based serializer internally. `orjson` provides even faster JSON encoding. For most cases, `model_dump_json()` is already optimal. Use `orjson` when you need custom JSON encoding options or are working with data outside Pydantic models.

---

### Q8: What is PlainSerializer?

**Answer**: A type annotation component that replaces the default serialization for a type. Applied via `Annotated[Type, PlainSerializer(func)]`. The function receives the field value and returns the serialized form.

---

### Q9: How do you exclude nested fields during serialization?

**Answer**: Use nested exclude dicts:

```python
user.model_dump(exclude={"address": {"zip_code"}})
```

---

### Q10: What happens to computed fields during serialization?

**Answer**: Computed fields (decorated with `@computed_field`) are **included** in serialization. They're computed from other fields and appear in both `model_dump()` and `model_dump_json()`.

---
