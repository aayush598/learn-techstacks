# Pydantic V1 vs V2 Migration Guide for FastAPI

## Table of Contents

1. [Overview of Pydantic V2](#overview-of-pydantic-v2)
2. [BaseModel Changes](#basemodel-changes)
3. [Field() vs Field()](#field-vs-field)
4. [validator vs field_validator](#validator-vs-field_validator)
5. [root_validator vs model_validator](#root_validator-vs-model_validator)
6. [schema_extra vs json_schema_extra](#schema_extra-vs-json_schema_extra)
7. [Config class vs model_config](#config-class-vs-model_config)
8. [arbitrary_types_allowed](#arbitrary_types_allowed)
9. [from_attributes (orm_mode)](#from_attributes-orm_mode)
10. [Type Coercion Differences](#type-coercion-differences)
11. [Performance Improvements in V2](#performance-improvements-in-v2)
12. [V1 Compatibility Layer](#v1-compatibility-layer)
13. [Migration Checklist](#migration-checklist)
14. [Common Migration Pitfalls](#common-migration-pitfalls)

---

## Overview of Pydantic V2

Pydantic V2 is a ground-up rewrite with a Rust core (pydantic-core) for validation.
It's 5-50x faster than V1 and has a cleaner API.

### Key Changes Summary

| Feature | V1 | V2 |
|---|---|---|
| Validation core | Python | Rust (pydantic-core) |
| Field definition | `field()` | `Field()` |
| Validators | `@validator` | `@field_validator` |
| Root validators | `@root_validator` | `@model_validator` |
| Config | `class Config:` | `model_config = ConfigDict(...)` |
| Schema extras | `schema_extra` | `json_schema_extra` |
| ORM mode | `orm_mode = True` | `from_attributes = True` |
| Arbitrary types | `arbitrary_types_allowed = True` | `arbitrary_types_allowed = True` |

### Installation

```bash
# Pydantic V2 (default)
pip install pydantic>=2.0

# V1 compatibility layer (if migrating gradually)
pip install "pydantic[v1]"
# OR
pip install pydantic.v1  # Separate package
```

---

## BaseModel Changes

### V1 BaseModel

```python
from pydantic import BaseModel, validator, Field
from typing import Optional, List

# V1 style
class UserV1(BaseModel):
    name: str
    age: int
    email: Optional[str] = None
    tags: List[str] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 30,
                "email": "john@example.com",
                "tags": ["admin"],
            }
        }

    @validator("age")
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("age must be positive")
        return v

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()
```

### V2 BaseModel

```python
from pydantic import BaseModel, field_validator, model_validator, ConfigDict, Field
from typing import Optional

# V2 style
class UserV2(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "John Doe",
                    "age": 30,
                    "email": "john@example.com",
                    "tags": ["admin"],
                }
            ]
        },
    )

    name: str
    age: int
    email: str | None = None
    tags: list[str] = []

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("age must be positive")
        return v

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()
```

### Key BaseModel Differences

```python
# V1 - model_fields is a dict of FieldInfo
print(UserV1.model_fields.keys())  # Works in both

# V2 - new methods
user = UserV2(name="Alice", age=25)

# Serialization
user.model_dump()                    # V2: returns dict
user.model_dump_json()               # V2: returns JSON string
user.model_dump(exclude_none=True)   # V2: exclude None values
user.model_dump(include={"name", "email"})  # V2: include specific fields

# V1 equivalents
user.dict()                          # V1: returns dict
user.json()                          # V1: returns JSON string
user.dict(exclude_none=True)         # V1: exclude None values

# Validation
UserV2.model_validate({"name": "Bob", "age": 30})  # V2
UserV1.parse_obj({"name": "Bob", "age": 30})       # V1

UserV2.model_validate_json('{"name": "Bob", "age": 30}')  # V2
UserV1.parse_raw('{"name": "Bob", "age": 30}')             # V1

# Copy with modifications
user.model_copy(update={"name": "Updated"})  # V2
user.copy(update={"name": "Updated"})        # V1
```

---

## field() vs Field()

### V1 field()

```python
from pydantic import BaseModel, Field

class ProductV1(BaseModel):
    # V1 uses Field with default value
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, description="Product price")
    quantity: int = Field(default=0, ge=0)
    description: str = Field(default="", max_length=500)
    sku: str = Field(..., regex=r"^[A-Z]{3}-\d{4}$")  # V1 uses 'regex'

    class Config:
        schema_extra = {
            "example": {"name": "Widget", "price": 9.99, "sku": "ABC-1234"}
        }
```

### V2 Field()

```python
from pydantic import BaseModel, Field, ConfigDict

class ProductV2(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"name": "Widget", "price": 9.99, "sku": "ABC-1234"}]
        }
    )

    # V2 uses Field directly
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, description="Product price")
    quantity: int = Field(default=0, ge=0)
    description: str = Field(default="", max_length=500)
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$")  # V2 uses 'pattern'

    # New V2 features
    frozen: bool = Field(default=False, description="If true, product is frozen")
    alias: str | None = Field(default=None, alias="sku_code")
    validation_alias: str | None = Field(default=None, validation_alias="code")
    serialization_alias: str | None = Field(default=None, serialization_alias="code")

    # Deprecated fields
    old_field: str | None = Field(default=None, deprecated="Use new_field instead")
```

### Field() Migration Details

```python
# V1 Field exclusions
class ModelV1(BaseModel):
    # V1 exclusions using Field
    internal: str = Field(exclude=True)         # V1
    computed: int = Field(exclude=True)          # V1

# V2 Field exclusions
class ModelV2(BaseModel):
    # V2 exclusions using Field
    internal: str = Field(exclude=True)          # V2 - same
    computed: int = Field(exclude=True)           # V2 - same

    # V2 new features
    sensitive: str = Field(repr=False)           # Exclude from repr
    read_only: str = Field(read_only=True)       # Read-only in OpenAPI
    write_only: str = Field(write_only=True)     # Write-only in OpenAPI

# V1 regex -> V2 pattern
class RegexExample(BaseModel):
    code: str = Field(regex=r"^[A-Z]+$")         # V1
    # becomes
    code: str = Field(pattern=r"^[A-Z]+$")       # V2
```

---

## validator vs field_validator

### V1 @validator

```python
from pydantic import BaseModel, validator

class UserModelV1(BaseModel):
    name: str
    email: str
    password: str
    age: int

    # V1 validators
    @validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip().title()

    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.lower()

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    # Pre and post validators
    @validator("age", pre=True)
    def parse_age(cls, v):
        """Runs before type validation."""
        if isinstance(v, str):
            return int(v)
        return v

    # Multiple field validation
    @validator("name", "email", each_item=False)
    def validate_strings(cls, v):
        return v.strip()

    # always=True runs even on Optional fields
    @validator("age", always=True)
    def validate_age(cls, v):
        if v is not None and v < 0:
            raise ValueError("Age must be positive")
        return v
```

### V2 @field_validator

```python
from pydantic import BaseModel, field_validator

class UserModelV2(BaseModel):
    name: str
    email: str
    password: str
    age: int

    # V2 field_validator
    @field_validator("name")
    @classmethod  # V2 REQUIRES @classmethod decorator
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip().title()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    # V2 uses mode parameter instead of pre/post
    @field_validator("age", mode="before")  # V2 equivalent of pre=True
    @classmethod
    def parse_age(cls, v: int | str) -> int:
        if isinstance(v, str):
            return int(v)
        return v

    @field_validator("age", mode="after")   # V2 equivalent of post behavior
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Age must be positive")
        return v

    # V2 uses 'info' parameter for context
    @field_validator("name")
    @classmethod
    def validate_name_with_info(cls, v: str, info) -> str:
        # info.data contains other field values
        if "email" in info.data and v.lower() in info.data["email"]:
            raise ValueError("Name cannot be in email")
        return v

    # V2 field_validator supports multiple fields
    @field_validator("name", "email")
    @classmethod
    def validate_strings(cls, v: str) -> str:
        return v.strip()
```

### validator Migration Summary

```python
# V1 -> V2 validator migration

# V1: @validator("field")
# V2: @field_validator("field") + @classmethod

# V1: pre=True
# V2: mode="before"

# V1: post=True (default)
# V2: mode="after" (default)

# V1: always=True
# V2: mode="wrap" or use model_validator

# V1: each_item=True (for lists)
# V2: @field_validator("field", mode="each_item")

# V1: whole=True (validates entire model)
# V2: Use @model_validator(mode="after")

# V1: @validator("field1", "field2")
# V2: @field_validator("field1", "field2")

# V1: cls (no @classmethod needed)
# V2: MUST use @classmethod decorator

# V1: no info about other fields
# V2: info parameter contains field data
```

---

## root_validator vs model_validator

### V1 @root_validator

```python
from pydantic import BaseModel, root_validator

class PasswordResetV1(BaseModel):
    password: str
    password_confirm: str
    old_password: str | None = None

    @root_validator(pre=True)
    def check_passwords_match_pre(cls, values):
        """Runs BEFORE field validation."""
        if values.get("password") != values.get("password_confirm"):
            raise ValueError("Passwords do not match")
        return values

    @root_validator
    def check_passwords_match_post(cls, values):
        """Runs AFTER field validation (default)."""
        if values["password"] != values["password_confirm"]:
            raise ValueError("Passwords do not match")
        return values

    @root_validator(pre=True)
    def strip_whitespace(cls, values):
        """Pre-processing: strip whitespace from all string fields."""
        return {k: v.strip() if isinstance(v, str) else v for k, v in values.items()}
```

### V2 @model_validator

```python
from pydantic import BaseModel, model_validator

class PasswordResetV2(BaseModel):
    password: str
    password_confirm: str
    old_password: str | None = None

    @model_validator(mode="before")
    @classmethod
    def check_passwords_match_pre(cls, data: dict) -> dict:
        """Runs BEFORE field validation. Must use @classmethod."""
        if data.get("password") != data.get("password_confirm"):
            raise ValueError("Passwords do not match")
        return data

    @model_validator(mode="after")
    def check_passwords_match_post(self) -> "PasswordResetV2":
        """Runs AFTER field validation. Receives model instance."""
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self

    @model_validator(mode="before")
    @classmethod
    def strip_whitespace(cls, data: dict) -> dict:
        """Pre-processing: strip whitespace from all string fields."""
        return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}

    # V2: mode="wrap" gives you control over validation
    @model_validator(mode="wrap")
    @classmethod
    def validate_model(cls, data: dict, handler) -> "PasswordResetV2":
        """Wrap validator - calls handler to continue validation."""
        # Pre-processing
        data = {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}
        # Call standard validation
        instance = handler(data)
        # Post-processing
        if instance.password != instance.password_confirm:
            raise ValueError("Passwords do not match")
        return instance
```

### model_validator Migration Summary

```python
# V1 -> V2 root_validator migration

# V1: @root_validator(pre=True)
# V2: @model_validator(mode="before") + @classmethod

# V1: @root_validator (default, post)
# V2: @model_validator(mode="after")

# V1: receives dict of values
# V2 mode="before": receives dict, must use @classmethod
# V2 mode="after": receives model instance (self)

# V1: returns dict
# V2 mode="before": returns dict
# V2 mode="after": returns model instance

# V2: @model_validator(mode="wrap")
# - Calls handler() to continue validation
# - Gives full control over validation flow
```

---

## schema_extra vs json_schema_extra

### V1 schema_extra

```python
from pydantic import BaseModel

class UserV1(BaseModel):
    name: str
    age: int
    email: str

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 30,
                "email": "john@example.com",
            },
            "description": "A user model",
            "title": "User",
        }
```

### V2 json_schema_extra

```python
from pydantic import BaseModel, ConfigDict

class UserV2(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "John Doe",
                    "age": 30,
                    "email": "john@example.com",
                }
            ],
            "description": "A user model",
            "title": "User",
        }
    )

    name: str
    age: int
    email: str

# V2: also supports json_schema_extra on Field
from pydantic import Field

class ProductV2(BaseModel):
    name: str = Field(
        json_schema_extra={
            "examples": ["Widget", "Gadget"],
            "title": "Product Name",
        }
    )
    price: float = Field(
        json_schema_extra={
            "examples": [9.99, 19.99],
            "minimum": 0,
        }
    )
```

### Schema Generation Differences

```python
# V1: generates JSON Schema Draft 7
schema_v1 = UserV1.model_json_schema()
# {
#     "title": "User",
#     "description": "A user model",
#     "type": "object",
#     "properties": {...},
#     "example": {...}
# }

# V2: generates JSON Schema 2020-12
schema_v2 = UserV2.model_json_schema()
# {
#     "$defs": {...},
#     "description": "A user model",
#     "examples": [...],
#     "properties": {...},
#     "title": "User",
#     "type": "object"
# }

# V2: more control over schema
class AdvancedModel(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "$schema": "http://json-schema.org/draft-07/schema#",
            "additionalProperties": False,
        }
    )
```

---

## Config class vs model_config

### V1 Config Class

```python
from pydantic import BaseModel

class UserV1(BaseModel):
    name: str
    age: int
    email: str

    class Config:
        # ORM mode
        orm_mode = True

        # Validation
        validate_assignment = True
        arbitrary_types_allowed = True

        # Schema
        schema_extra = {"example": {...}}
        title = "User"
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: float(v),
        }

        # Field naming
        fields = {
            "email": {"alias": "user_email"},
            "age": {"ge": 0, "le": 150},
        }

        # Error messages
        error_msg_templates = {
            "value_error.email": "Invalid email address",
        }

        # Import/Export
        use_enum_values = True
        allow_population_by_field_name = True
```

### V2 ConfigDict

```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal

class UserV2(BaseModel):
    # V2 uses model_config dict
    model_config = ConfigDict(
        # ORM/Attributes mode
        from_attributes=True,  # was orm_mode=True

        # Validation
        validate_assignment=True,
        arbitrary_types_allowed=True,
        strict=True,  # V2: strict type checking

        # Schema
        json_schema_extra={
            "examples": [{"name": "John", "age": 30, "email": "john@example.com"}]
        },
        title="User",

        # Field naming
        alias_generator=lambda field_name: field_name.upper(),
        populate_by_name=True,  # was allow_population_by_field_name

        # Serialization
        ser_json_timedelta="iso8601",
        ser_json_bytes="base64",
        use_enum_values=True,

        # Error handling
        errors_include_url=False,
        errors_include_input=False,

        # Performance
        cache_strings=True,  # V2: cache string validation
    )

    name: str
    age: int
    email: str
```

### Config Migration Table

| V1 Config | V2 ConfigDict | Notes |
|---|---|---|
| `orm_mode = True` | `from_attributes = True` | Renamed |
| `allow_population_by_field_name = True` | `populate_by_name = True` | Renamed |
| `schema_extra = {...}` | `json_schema_extra = {...}` | Renamed |
| `json_encoders = {...}` | Removed | Use custom serializer |
| `fields = {"name": {...}}` | Use `Field()` | Moved to field level |
| `error_msg_templates` | Custom error handlers | Different API |
| New | `strict = True` | Strict type checking |
| New | `cache_strings = True` | Performance optimization |

---

## arbitrary_types_allowed

### V1 and V2 (Same Concept)

```python
from pydantic import BaseModel, ConfigDict

# Allow arbitrary (non-Pydantic) types
class CustomType:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"CustomType({self.value!r})"

# V1
class ModelV1(BaseModel):
    custom: CustomType

    class Config:
        arbitrary_types_allowed = True

# V2
class ModelV2(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    custom: CustomType

# V2: Better approach with __get_pydantic_core_schema__
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class CustomType:
    def __init__(self, value: str):
        self.value = value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda v: v.value
            ),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return cls(v)
        raise ValueError("Expected string")

# Now works without arbitrary_types_allowed
class ModelV2(BaseModel):
    custom: CustomType  # No Config needed!
```

---

## from_attributes (orm_mode)

### V1 orm_mode

```python
from pydantic import BaseModel

# V1 ORM mode
class UserV1(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True

# Usage with ORM objects
class UserORM:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

orm_user = UserORM(name="Alice", email="alice@example.com")
user = UserV1.from_orm(orm_user)  # V1 method
```

### V2 from_attributes

```python
from pydantic import BaseModel, ConfigDict

# V2 from_attributes
class UserV2(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: str

# Usage with ORM objects
orm_user = UserORM(name="Alice", email="alice@example.com")
user = UserV2.model_validate(orm_user)  # V2 method

# V2 also works with dataclasses
from dataclasses import dataclass

@dataclass
class UserDC:
    name: str
    email: str

dc_user = UserDC(name="Bob", email="bob@example.com")
user = UserV2.model_validate(dc_user)

# V2 also works with dicts
user = UserV2.model_validate({"name": "Charlie", "email": "charlie@example.com"})

# V2: lazy loading support
class LazyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def load_related(self):
        # Access lazy-loaded attributes
        if hasattr(self, "_sa_instance_state"):
            # SQLAlchemy lazy loading
            pass
        return self
```

---

## Type Coercion Differences

### V1 Type Coercion

```python
from pydantic import BaseModel

# V1: Permissive type coercion
class ModelV1(BaseModel):
    count: int
    price: float
    active: bool
    name: str

# V1 coerces types aggressively
m = ModelV1(count="42", price="19.99", active="true", name=123)
print(m.count)      # 42 (str -> int)
print(m.price)      # 19.99 (str -> float)
print(m.active)     # True (str -> bool)
print(m.name)       # "123" (int -> str)

# V1 bool coercion is very permissive
class BoolModelV1(BaseModel):
    flag: bool

# All of these work in V1
BoolModelV1(flag=1)          # True
BoolModelV1(flag="1")        # True
BoolModelV1(flag="true")     # True
BoolModelV1(flag="yes")      # True
BoolModelV1(flag=[])         # False
BoolModelV1(flag="")         # False
```

### V2 Type Coercion

```python
from pydantic import BaseModel, ConfigDict

# V2: Stricter type coercion by default
class ModelV2(BaseModel):
    count: int
    price: float
    active: bool
    name: str

# V2 default mode (lax) - still coerces but less aggressively
m = ModelV2(count="42", price="19.99", active="true", name=123)
print(m.count)      # 42 (str -> int still works)
print(m.price)      # 19.99 (str -> float still works)
print(m.active)     # True (str -> bool still works)
print(m.name)       # "123" (int -> str still works)

# V2 STRICT mode - no type coercion
class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)

    count: int
    price: float
    active: bool
    name: str

# StrictModel(count="42")  # ValidationError! str != int
# StrictModel(price="19.99")  # ValidationError! str != float
StrictModel(count=42, price=19.99, active=True, name="Alice")  # OK

# V2 bool coercion - stricter than V1
class StrictBoolModel(BaseModel):
    model_config = ConfigDict(strict=True)
    flag: bool

# Only these work in V2 strict:
StrictBoolModel(flag=True)     # OK
StrictBoolModel(flag=False)    # OK
# StrictBoolModel(flag=1)      # ValidationError!
# StrictBoolModel(flag="true") # ValidationError!

# V2: Custom coercion with mode="before"
class FlexibleModel(BaseModel):
    value: int

    @field_validator("value", mode="before")
    @classmethod
    def coerce_int(cls, v):
        if isinstance(v, str):
            return int(v)
        return v

FlexibleModel(value="42")  # Works because of custom validator
```

### V2 Validation Modes

```python
from pydantic import BaseModel, ConfigDict

# Lax mode (default) - permissive coercion
class LaxModel(BaseModel):
    model_config = ConfigDict(strict=False)  # default
    number: int

LaxModel(number="42")  # OK, coerces str to int

# Strict mode - no coercion
class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)
    number: int

# StrictModel(number="42")  # ValidationError!

# Custom mode per field
from pydantic import Field

class MixedModel(BaseModel):
    strict_field: int = Field(strict=True)      # No coercion
    lax_field: int = Field(strict=False)         # Coercion allowed
    default_field: int                            # Follows model default
```

---

## Performance Improvements in V2

### Benchmark Comparison

```python
# V2 is 5-50x faster than V1 due to Rust core

import time
from pydantic import BaseModel

# Simple model benchmark
class SimpleModel(BaseModel):
    name: str
    age: int
    email: str

# V1 equivalent (using pydantic.v1)
from pydantic.v1 import BaseModel as BaseModelV1

class SimpleModelV1(BaseModelV1):
    name: str
    age: int
    email: str

data = {"name": "John", "age": 30, "email": "john@example.com"}

# V1 validation time: ~0.5ms per 1000 validations
# V2 validation time: ~0.05ms per 1000 validations
# That's roughly 10x faster for simple models

# Complex model with validators
class ComplexModel(BaseModel):
    name: str
    age: int
    email: str
    tags: list[str]
    metadata: dict[str, str | int]

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v.strip()

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("Invalid age")
        return v

# Complex model improvements are even more dramatic:
# V1: ~2ms per 1000 validations
# V2: ~0.1ms per 1000 validations
# That's roughly 20x faster

# Serialization performance
user = ComplexModel(
    name="John",
    age=30,
    email="john@example.com",
    tags=["admin", "user"],
    metadata={"role": "admin", "level": 5}
)

# V1: user.dict() - Python serialization
# V2: user.model_dump() - Rust serialization (much faster)

# JSON serialization
# V1: user.json() - Python JSON encoder
# V2: user.model_dump_json() - Rust JSON encoder (much faster)
```

### Why V2 is Faster

```python
# 1. Rust core (pydantic-core) handles validation
#    - C-level string operations
#    - Optimized memory allocation
#    - Zero-copy parsing where possible

# 2. Lazy validation
#    - Fields validated only when accessed (with model_config lazy=True)
#    - Reduces unnecessary computation

# 3. Schema compilation
#    - V2 compiles validation schemas once
#    - Reuses compiled schemas for subsequent validations

# 4. Better caching
#    - String validation results cached
#    - Reduces repeated computations

# 5. Optimized serialization
#    - Rust-based JSON serialization
#    - Direct bytes output (model_dump_json returns str directly)

# Performance tips for V2
class OptimizedModel(BaseModel):
    model_config = ConfigDict(
        cache_strings=True,      # Cache string validation
        validate_default=True,   # Validate default values
        str_strip_whitespace=True,  # Strip whitespace automatically
    )

    name: str
    email: str
```

---

## V1 Compatibility Layer

### Using V1 Compatibility

```python
# Option 1: Import from pydantic.v1
from pydantic.v1 import BaseModel, Field, validator

class LegacyModel(BaseModel):
    name: str
    age: int

    class Config:
        orm_mode = True

    @validator("age")
    def validate_age(cls, v):
        if v < 0:
            raise ValueError("Age must be positive")
        return v

# Option 2: Install separate package
# pip install pydantic.v1
from pydantic.v1 import BaseModel

# Option 3: Gradual migration - use both in same project
from pydantic import BaseModel as BaseModelV2
from pydantic.v1 import BaseModel as BaseModelV1

class NewModel(BaseModelV2):
    model_config = ConfigDict(from_attributes=True)
    name: str

class LegacyModel(BaseModelV1):
    name: str
    class Config:
        orm_mode = True

# Option 4: Use migration script
# pydantic supports automatic migration with:
# pip install bump-pydantic
# bump-pydantic migrate .
```

### Migration Script

```bash
# Install migration tool
pip install bump-pydantic

# Run migration
bump-pydantic migrate .

# This automatically:
# 1. Converts Config class to model_config
# 2. Converts @validator to @field_validator
# 3. Converts @root_validator to @model_validator
# 4. Converts schema_extra to json_schema_extra
# 5. Converts orm_mode to from_attributes
# 6. Updates imports
```

---

## Migration Checklist

```markdown
## Pydantic V2 Migration Checklist

### Imports
- [ ] Replace `from pydantic import validator` with `field_validator`
- [ ] Replace `from pydantic import root_validator` with `model_validator`
- [ ] Add `ConfigDict` import
- [ ] Add `@classmethod` decorator to all validators

### BaseModel
- [ ] Replace `class Config:` with `model_config = ConfigDict(...)`
- [ ] Replace `orm_mode = True` with `from_attributes=True`
- [ ] Replace `allow_population_by_field_name` with `populate_by_name`
- [ ] Replace `schema_extra` with `json_schema_extra`
- [ ] Replace `json_encoders` with custom serializers

### Validators
- [ ] Replace `@validator` with `@field_validator` + `@classmethod`
- [ ] Replace `pre=True` with `mode="before"`
- [ ] Replace `always=True` with appropriate mode
- [ ] Replace `@root_validator` with `@model_validator`
- [ ] Update root_validator to use self (mode="after") or @classmethod (mode="before")

### Field Definitions
- [ ] Replace `regex` with `pattern` in Field()
- [ ] Update Field exclusions if using complex logic
- [ ] Check for new V2 Field features (frozen, read_only, write_only)

### Methods
- [ ] Replace `.dict()` with `.model_dump()`
- [ ] Replace `.json()` with `.model_dump_json()`
- [ ] Replace `.parse_obj()` with `.model_validate()`
- [ ] Replace `.parse_raw()` with `.model_validate_json()`
- [ ] Replace `.copy()` with `.model_copy()`
- [ ] Replace `.schema()` with `.model_json_schema()`

### Type Coercion
- [ ] Test strict mode if needed
- [ ] Verify bool coercion behavior
- [ ] Check numeric type coercion

### Testing
- [ ] Run full test suite
- [ ] Verify API responses match expected format
- [ ] Check OpenAPI schema generation
- [ ] Test ORM model loading
```

---

## Common Migration Pitfalls

### 1. Missing @classmethod

```python
# V1 - no @classmethod needed
@validator("name")
def validate_name(cls, v):
    return v.strip()

# V2 - @classmethod is REQUIRED
@field_validator("name")
@classmethod  # This decorator is mandatory in V2
def validate_name(cls, v: str) -> str:
    return v.strip()
```

### 2. root_validator Self vs Classmethod

```python
# V1 root_validator always receives dict
@root_validator
def check(cls, values):
    return values

# V2 model_validator mode="after" receives self (model instance)
@model_validator(mode="after")
def check(self) -> "Model":
    # self is the model instance, not a dict
    if self.field1 != self.field2:
        raise ValueError("Fields must match")
    return self

# V2 model_validator mode="before" receives dict
@model_validator(mode="before")
@classmethod
def check(cls, data: dict) -> dict:
    # data is a dict (like V1)
    return data
```

### 3. Default Values

```python
# V1: Optional fields with defaults
class ModelV1(BaseModel):
    name: str | None = None  # Optional, defaults to None

# V2: Same behavior, but be careful with validators
class ModelV2(BaseModel):
    name: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        # V2: validator may not run for default values
        # Use mode="after" or model_validator if needed
        return v.upper() if v else v
```

### 4. JSON Schema Changes

```python
# V1 generates Draft 7
# V2 generates 2020-12

# If you need V1 schema format:
class Model(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "$schema": "http://json-schema.org/draft-07/schema#"
        }
    )
```
