# Pydantic JSON Schema Generation — The Complete Reference

## Table of Contents

1. [JSON Schema Basics](#basics)
2. [Generating Schema from Models](#generating)
3. [Schema Structure](#structure)
4. [Customizing Schema with schema_extra](#schema-extra)
5. [json_schema_extra on ConfigDict](#json-schema-extra)
6. [Field-Level Schema Customization](#field-schema)
7. [Schema References ($ref)](#schema-refs)
8. [Schema Decomposition](#decomposition)
9. [OpenAPI Schema Integration](#openapi)
10. [Testing JSON Schema Output](#testing)
11. [Schema-Driven Development](#schema-driven)
12. [Advanced Schema Patterns](#advanced)
13. [Best Practices](#best-practices)
14. [Interview Questions](#interview-questions)

---

## basics

JSON Schema is a standard for describing the structure and validation rules of JSON data. Pydantic can auto-generate JSON Schema from model definitions.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

schema = User.model_json_schema()
print(schema)
```

Output:

```json
{
  "properties": {
    "name": {"title": "Name", "type": "string"},
    "age": {"title": "Age", "type": "integer"}
  },
  "required": ["name", "age"],
  "title": "User",
  "type": "object"
}
```

### Why JSON Schema Matters

- **API Documentation**: OpenAPI (Swagger) uses JSON Schema for request/response models
- **Client Generation**: Tools like `openapi-generator` use schemas to generate typed clients
- **Validation**: JSON Schema can validate data in non-Python systems
- **Testing**: Verify your API contracts match expectations

---

## generating

### Basic Generation

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True
    score: float = 0.0

schema = User.model_json_schema()
```

### With Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address

schema = User.model_json_schema()
print(schema)
```

Output:

```json
{
  "$defs": {
    "Address": {
      "properties": {
        "street": {"title": "Street", "type": "string"},
        "city": {"title": "City", "type": "string"},
        "zip_code": {"title": "Zip Code", "type": "string"}
      },
      "required": ["street", "city", "zip_code"],
      "title": "Address",
      "type": "object"
    }
  },
  "properties": {
    "name": {"title": "Name", "type": "string"},
    "address": {"$ref": "#/$defs/Address"}
  },
  "required": ["name", "address"],
  "title": "User",
  "type": "object"
}
```

### With TypeAdapter

```python
from pydantic import TypeAdapter, Field
from typing import Annotated

ta = TypeAdapter(Annotated[int, Field(ge=0, le=100)])
schema = ta.json_schema()
print(schema)  # {'type': 'integer', 'minimum': 0, 'maximum': 100}
```

---

## structure

### Common Schema Properties

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class CompleteExample(BaseModel):
    # String with constraints
    name: str = Field(min_length=1, max_length=100, pattern=r'^[a-zA-Z]+$')

    # Integer with constraints
    age: int = Field(ge=0, le=150)

    # Float with constraints
    score: float = Field(ge=0.0, le=100.0)

    # Boolean
    active: bool = True

    # Optional string
    email: Optional[str] = None

    # List of strings
    tags: List[str] = []

    # Literal values
    status: str = Field(default="active")

schema = CompleteExample.model_json_schema()
```

### Schema Type Mapping

| Python Type | JSON Schema Type |
|------------|-----------------|
| `str` | `{"type": "string"}` |
| `int` | `{"type": "integer"}` |
| `float` | `{"type": "number"}` |
| `bool` | `{"type": "boolean"}` |
| `list` | `{"type": "array"}` |
| `dict` | `{"type": "object"}` |
| `None` | `{"type": "null"}` |
| `Optional[X]` | Union of X and null |
| `Literal[...]` | `{"enum": [...]}` |
| `datetime` | `{"type": "string", "format": "date-time"}` |
| `UUID` | `{"type": "string", "format": "uuid"}` |

---

## schema-extra

### Using json_schema_extra on Model

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"name": "Alice", "age": 30}
            ],
            "externalDocs": {
                "description": "User API documentation",
                "url": "https://docs.example.com/api/users"
            }
        }
    )

    name: str
    age: int

schema = User.model_json_schema()
print(schema.get("examples"))
# [{'name': 'Alice', 'age': 30}]
```

### Using json_schema_extra as Function

```python
def add_metadata(schema: dict) -> dict:
    """Add custom metadata to schema."""
    schema["description"] = "A user in the system"
    schema["properties"]["_id"] = {"type": "string", "format": "uuid"}
    return schema

class User(BaseModel):
    model_config = ConfigDict(json_schema_extra=add_metadata)

    name: str
    age: int

schema = User.model_json_schema()
print(schema.get("description"))  # "A user in the system"
```

### Field-Level Examples

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(examples=["Alice Smith", "Bob Johnson"])
    age: int = Field(ge=0, examples=[25, 30, 35])
    email: str = Field(examples=["alice@example.com"])

schema = User.model_json_schema()
print(schema["properties"]["name"])
# {'title': 'Name', 'type': 'string', 'examples': ['Alice Smith', 'Bob Johnson']}
```

---

## json-schema-extra

### On ConfigDict

```python
from pydantic import BaseModel, ConfigDict

class APIResponse(BaseModel):
    model_config = ConfigDict(
        title="API Response",
        json_schema_extra={
            "x-internal": True,
            "x ratelimit": {"limit": 100, "window": 60}
        }
    )

    data: dict
    status: str

schema = APIResponse.model_json_schema()
print(schema.get("x-internal"))  # True
```

### On FieldInfo

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(
        json_schema_extra={
            "x-custom": "value",
            "description": "User's full name"
        }
    )

schema = User.model_json_schema()
print(schema["properties"]["name"].get("x-custom"))  # "value"
```

---

## field-schema

### Custom Field Schema

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    # Field with custom schema extras
    name: str = Field(
        ...,
        title="Full Name",
        description="The user's full legal name",
        min_length=1,
        max_length=200,
        examples=["Alice Smith"],
        json_schema_extra={
            "x-field-group": "personal",
            "x-searchable": True
        }
    )

schema = User.model_json_schema()
name_schema = schema["properties"]["name"]
print(name_schema)
# {
#   'title': 'Full Name',
#   'description': "The user's full legal name",
#   'type': 'string',
#   'minLength': 1,
#   'maxLength': 200,
#   'examples': ['Alice Smith'],
#   'x-field-group': 'personal',
#   'x-searchable': True
# }
```

### Field with Deprecated

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    old_field: str | None = Field(default=None, deprecated="Use 'new_field' instead")
    new_field: str | None = None

schema = User.model_json_schema()
print(schema["properties"]["old_field"])
# {'title': 'Old Field', 'type': 'string', 'deprecated': "Use 'new_field' instead", 'default': None}
```

---

## schema-refs

### How $ref Works

When a model contains nested models or types used multiple times, Pydantic uses `$ref` to avoid duplication.

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    home_address: Address
    work_address: Address

schema = User.model_json_schema()
print(schema)
```

```json
{
  "$defs": {
    "Address": {
      "properties": {
        "street": {"title": "Street", "type": "string"},
        "city": {"title": "City", "type": "string"}
      },
      "required": ["street", "city"],
      "title": "Address",
      "type": "object"
    }
  },
  "properties": {
    "name": {"title": "Name", "type": "string"},
    "home_address": {"$ref": "#/$defs/Address"},
    "work_address": {"$ref": "#/$defs/Address"}
  },
  ...
}
```

### Resolving $ref

```python
def resolve_ref(schema: dict, ref: str) -> dict:
    """Resolve a $ref pointer within a schema."""
    if not ref.startswith('#/'):
        raise ValueError("Only local $refs supported")

    parts = ref[2:].split('/')
    current = schema
    for part in parts:
        current = current[part]
    return current

# Usage
address_schema = resolve_ref(schema, schema["properties"]["home_address"]["$ref"])
print(address_schema)
```

---

## decomposition

### Breaking Down Complex Schemas

```python
from pydantic import BaseModel
from typing import Union

class TextMessage(BaseModel):
    content: str

class ImageMessage(BaseModel):
    url: str
    width: int
    height: int

class Message(BaseModel):
    id: int
    message: Union[TextMessage, ImageMessage]

schema = Message.model_json_schema()

# The schema decomposes into:
# - Message (main)
# - TextMessage (in $defs)
# - ImageMessage (in $defs)
# - OneOf for the Union type
print(schema)
```

### Using allOf, oneOf, anyOf

```python
from pydantic import BaseModel, Field
from typing import Union, Annotated, Literal

class Cat(BaseModel):
    type: Literal["cat"]
    meow_volume: int

class Dog(BaseModel):
    type: Literal["dog"]
    bark_volume: int

class Pet(BaseModel):
    name: str
    animal: Annotated[Union[Cat, Dog], Field(discriminator="type")]

schema = Pet.model_json_schema()
print(schema)
# Shows discriminated union with oneOf and discriminator
```

---

## openapi

### Pydantic in FastAPI (OpenAPI Generation)

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., description="User email")
    age: int = Field(ge=0, le=150)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    is_active: bool = True

app = FastAPI()

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """Create a new user."""
    return {"id": 1, **user.model_dump()}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Get a user by ID."""
    return {"id": user_id, "name": "Alice", "email": "alice@x.com", "age": 30, "is_active": True}

# Access OpenAPI schema
schema = app.openapi()
print(schema["components"]["schemas"]["UserCreate"])
print(schema["components"]["schemas"]["UserResponse"])
```

### Customizing OpenAPI Schema

```python
from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"name": "Alice"}]
        }
    }

app = FastAPI()

@app.get("/users", response_model=list[User])
def list_users():
    return [{"name": "Alice"}]

# Modify OpenAPI schema
schema = app.openapi()
schema["info"]["x-logo"] = {"url": "https://example.com/logo.png"}
```

---

## testing

### Testing Schema Output

```python
import pytest
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0)
    email: str

def test_user_schema():
    schema = User.model_json_schema()

    # Check required fields
    assert "name" in schema["required"]
    assert "age" in schema["required"]
    assert "email" in schema["required"]

    # Check types
    assert schema["properties"]["name"]["type"] == "string"
    assert schema["properties"]["age"]["type"] == "integer"

    # Check constraints
    assert schema["properties"]["age"]["minimum"] == 0
    assert schema["properties"]["name"]["minLength"] == 1

def test_schema_with_nested_model():
    class Address(BaseModel):
        street: str
        city: str

    class User(BaseModel):
        name: str
        address: Address

    schema = User.model_json_schema()

    # Check nested model is in $defs
    assert "Address" in schema["$defs"]

    # Check $ref is used
    assert schema["properties"]["address"]["$ref"] == "#/$defs/Address"
```

### Schema Snapshot Testing

```python
import json

def test_api_schema_matches_contract():
    """Verify API schema matches the expected contract."""
    from fastapi.testclient import TestClient
    from your_app import app

    client = TestClient(app)
    response = client.get("/openapi.json")
    schema = response.json()

    # Load expected contract
    with open("contracts/api_schema.json") as f:
        expected = json.load(f)

    # Compare (or use a snapshot testing library)
    assert schema == expected
```

---

## schema-driven

### Schema-First Development

```python
# Define expected schema first
EXPECTED_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "age": {"type": "integer", "minimum": 0},
    },
    "required": ["name", "age"]
}

# Then implement the model
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0)

# Verify schema matches
actual = User.model_json_schema()
assert actual["properties"]["name"]["type"] == "string"
assert actual["properties"]["age"]["minimum"] == 0
```

### Generating Client Code from Schema

```python
def generate_typescript_interface(schema: dict, name: str) -> str:
    """Generate a TypeScript interface from a Pydantic JSON schema."""
    lines = [f"interface {name} {{"]
    for field_name, field_schema in schema.get("properties", {}).items():
        ts_type = {
            "string": "string",
            "integer": "number",
            "number": "number",
            "boolean": "boolean",
        }.get(field_schema.get("type", "string"), "any")

        optional = "?" if field_name not in schema.get("required", []) else ""
        lines.append(f"  {field_name}{optional}: {ts_type};")
    lines.append("}")
    return "\n".join(lines)

# Usage
schema = User.model_json_schema()
ts_code = generate_typescript_interface(schema, "User")
print(ts_code)
```

---

## advanced

### Schema with Discriminated Unions

```python
from pydantic import BaseModel, Field
from typing import Annotated, Union, Literal

class CreditCard(BaseModel):
    type: Literal["credit"]
    number: str
    cvv: str

class BankTransfer(BaseModel):
    type: Literal["bank"]
    account_number: str
    routing_number: str

class Payment(BaseModel):
    amount: float
    method: Annotated[Union[CreditCard, BankTransfer], Field(discriminator="type")]

schema = Payment.model_json_schema()
print(schema)
# Shows discriminated union with oneOf + discriminator
```

### Schema with Custom Types

```python
from pydantic import BaseModel, Field
from typing import Annotated
from pydantic.types import conint

class Config(BaseModel):
    port: conint(ge=1024, le=65535)
    max_connections: conint(ge=1)

schema = Config.model_json_schema()
print(schema["properties"]["port"])
# {'type': 'integer', 'minimum': 1024, 'maximum': 65535, 'title': 'Port'}
```

### Schema with Computed Fields

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

schema = Rectangle.model_json_schema()
print(schema)
# 'area' appears as a computed field in the schema
```

### Refining Schema Output

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        title="API User",
        str_strip_whitespace=True,
        json_schema_extra={
            "description": "A user object",
            "x-internal": False,
        }
    )

    name: str = Field(description="Full name")
    age: int = Field(description="Age in years", ge=0)

schema = User.model_json_schema()
# schema includes title, description, and custom extensions
```

---

## Best Practices

### 1. Always Test Your Schema

```python
# Verify schema matches your API contract
schema = MyModel.model_json_schema()
assert "name" in schema["required"]
assert schema["properties"]["age"]["type"] == "integer"
```

### 2. Use Field Descriptions for Documentation

```python
class User(BaseModel):
    name: str = Field(description="The user's full name")
    email: str = Field(description="Primary email address")
```

### 3. Add Examples for API Docs

```python
class User(BaseModel):
    name: str = Field(examples=["Alice Smith"])
    age: int = Field(ge=0, examples=[30])
```

### 4. Use $ref for Reusable Types

```python
# Pydantic automatically uses $ref for nested models
# This avoids duplication in the schema
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    address: Address  # Will be $ref in schema
```

### 5. Validate Schema Compatibility

```python
# Use jsonschema library to validate data against your schema
from jsonschema import validate

schema = MyModel.model_json_schema()
validate(instance={"name": "Alice", "age": 30}, schema=schema)
```

---

## Interview Questions

### Q1: How do you generate JSON Schema from a Pydantic model?

**Answer**: Use `Model.model_json_schema()`. It returns a dict representing the JSON Schema. For `TypeAdapter`, use `ta.json_schema()`.

---

### Q2: What is $ref in JSON Schema?

**Answer**: `$ref` is a JSON Schema reference mechanism. When a type is used multiple times, Pydantic defines it once in `$defs` and references it with `$ref`. This avoids duplication and keeps schemas clean.

---

### Q3: How do you add examples to a model's schema?

**Answer**: Two ways:
- Field-level: `Field(examples=["example"])`
- Model-level: `ConfigDict(json_schema_extra={"examples": [...]})`

---

### Q4: How does Pydantic handle Union types in JSON Schema?

**Answer**: Pydantic generates `oneOf` for discriminated unions (with a `discriminator` field). For regular unions, it may use `anyOf`. Discriminated unions are more efficient and produce clearer schemas.

---

### Q5: How do you customize the model title in the schema?

**Answer**: Use `ConfigDict(title="CustomTitle")`. The title appears at the top level of the schema and in OpenAPI docs.

---

### Q6: What is the difference between json_schema_extra and schema_extra?

**Answer**: In Pydantic V2, `schema_extra` is deprecated. Use `json_schema_extra` in `ConfigDict` instead. It works the same way — adds extra properties to the JSON schema.

---

### Q7: How do you test that your schema matches an API contract?

**Answer**: Generate the schema with `model_json_schema()`, then use assertions or a JSON Schema validator to verify it matches your expected contract. You can also use snapshot testing.

---

### Q8: How does FastAPI use Pydantic's JSON Schema?

**Answer**: FastAPI takes Pydantic models used in `response_model` and `Body/Query/Path` parameters, calls `model_json_schema()`, and includes the results in the OpenAPI schema at `/openapi.json`.

---

### Q9: Can you use JSON Schema to validate data in non-Python systems?

**Answer**: Yes. JSON Schema is a language-agnostic standard. Libraries exist for JavaScript, Go, Java, etc. You can generate the schema with Pydantic and validate data in any language.

---

### Q10: How do you handle optional fields in JSON Schema?

**Answer**: Optional fields (with `None` default) are not listed in `required`. The schema shows the field type as a union with `null`:

```json
{"anyOf": [{"type": "string"}, {"type": "null"}]}
```

---
