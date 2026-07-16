# Pydantic Field Validation — The Complete Reference

## Table of Contents

1. [Field() Options Overview](#field-options)
2. [default — Default Values](#field-default)
3. [alias — Field Aliasing](#field-alias)
4. [title and description — Documentation](#field-title-description)
5. [gt, ge, lt, le — Numeric Constraints](#field-numeric)
6. [min_length, max_length — String Constraints](#field-string)
7. [pattern — Regex Validation](#field-pattern)
8. [examples — Schema Examples](#field-examples)
9. [deprecated — Deprecated Fields](#field-deprecated)
10. [field_validator — Custom Field Validators](#field-validator)
11. [model_validator — Custom Model Validators](#model-validator)
12. [AfterValidator — Post-Validation](#after-validator)
13. [BeforeValidator — Pre-Validation](#before-validator)
14. [PlainValidator — Custom Validation](#plain-validator)
15. [WrapValidator — Wrapping Validation](#wrap-validator)
16. [Serializer Utilities](#serializer-utilities)
17. [Best Practices](#best-practices)
18. [Interview Questions](#interview-questions)

---

## Field() Options Overview

`Field()` is the primary way to add metadata and constraints to individual model fields.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(
        ...,                          # Required (explicit)
        alias="userName",             # JSON key alias
        title="User Name",            # Schema title
        description="The user's name",# Schema description
        min_length=1,                 # Minimum string length
        max_length=100,               # Maximum string length
        pattern=r"^[a-zA-Z\s]+$",    # Regex pattern
        examples=["Alice Smith"],     # Schema examples
        deprecated=False,             # Deprecation marker
        json_schema_extra={"custom": "metadata"}  # Extra schema data
    )
```

---

## field-default

### Static Default

```python
class Config(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=8000)
```

### Default Factory

```python
from pydantic import BaseModel, Field
from datetime import datetime

class Event(BaseModel):
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    tags: list[str] = Field(default_factory=list)

e = Event(name="Meeting")
print(e.created_at)  # Current datetime
print(e.tags)        # []
```

### Required (Ellipsis)

```python
class User(BaseModel):
    name: str = Field(...)  # Explicitly required
    age: int = Field(...)   # Same as no default
```

### Required with `required=True`

```python
class User(BaseModel):
    name: str = Field(required=True)  # Same as Field(...)
```

---

## field-alias

### Basic Alias

```python
class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_name: str = Field(alias="userName")
    first_name: str = Field(alias="firstName")

# Using alias
user = User.model_validate({"userName": "alice", "firstName": "Alice"})
print(user.user_name)  # "alice"

# Using original field name (with populate_by_name=True)
user = User(user_name="alice", firstName="Alice")
print(user.user_name)  # "alice"

# Serialization uses original field name by default
print(user.model_dump())  # {'user_name': 'alice', 'first_name': 'Alice'}

# To serialize with alias:
print(user.model_dump(by_alias=True))  # {'userName': 'alice', 'firstName': 'Alice'}
```

### Alias Generator

```python
from pydantic import BaseModel, ConfigDict

def to_camel(string: str) -> str:
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class User(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_name: str
    first_name: str
    email_address: str

user = User(user_name="alice", first_name="Alice", email_address="alice@x.com")
print(user.model_dump(by_alias=True))
# {'userName': 'alice', 'firstName': 'Alice', 'emailAddress': 'alice@x.com'}
```

### Validation Alias

```python
class User(BaseModel):
    # validation_alias is used for input validation only
    # serialization uses the field name
    name: str = Field(validation_alias="fullName")

user = User.model_validate({"fullName": "Alice Smith"})
print(user.name)  # "Alice Smith"
print(user.model_dump())  # {'name': 'Alice Smith'} — uses field name
```

### Alias Path

```python
from pydantic import BaseModel, Field

class Nested(BaseModel):
    value: int = Field(alias="data.value", validation_alias=AliasPath("data", "value"))

# This allows flattening nested JSON
data = {"data": {"value": 42}}
n = Nested.model_validate(data)
print(n.value)  # 42
```

---

## field-title-description

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(
        title="Product Name",
        description="The name of the product as displayed to users"
    )
    price: float = Field(
        title="Price in USD",
        description="The price of the product in US dollars, excluding tax"
    )

# These appear in JSON Schema and OpenAPI documentation
schema = Product.model_json_schema()
print(schema)
# {
#   "properties": {
#     "name": {"title": "Product Name", "description": "The name of the product as displayed to users", "type": "string"},
#     "price": {"title": "Price in USD", "description": "The price of the product in US dollars, excluding tax", "type": "number"}
#   },
#   ...
# }
```

---

## field-numeric

```python
from pydantic import BaseModel, Field

class Measurement(BaseModel):
    # gt = greater than
    positive: float = Field(gt=0)

    # ge = greater than or equal
    score: int = Field(ge=0)

    # lt = less than
    small: float = Field(lt=1)

    # le = less than or equal
    percentage: float = Field(ge=0, le=100)

    # multiple_of
    dozen: int = Field(multiple_of=12)

m = Measurement(positive=0.1, score=0, small=0.99, percentage=50, dozen=24)

# Invalid
try:
    m = Measurement(positive=0, score=-1, small=1.0, percentage=101, dozen=13)
except Exception as e:
    print(e)  # Multiple validation errors
```

### Combined Constraints

```python
class Range(BaseModel):
    # Multiple constraints
    value: float = Field(gt=0, lt=100, multiple_of=0.5)

    # Integer with specific range
    port: int = Field(ge=1024, le=65535)
```

---

## field-string

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    # min_length
    name: str = Field(min_length=1)

    # max_length
    bio: str = Field(max_length=500)

    # Both
    username: str = Field(min_length=3, max_length=50)

    # With default
    nickname: str = Field(default="", min_length=0, max_length=100)
```

---

## field-pattern

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    # Email-like pattern (simplified)
    email: str = Field(pattern=r'^[\w.-]+@[\w.-]+\.\w+$')

    # Phone number pattern
    phone: str = Field(pattern=r'^\+?[\d\s-]{10,}$')

    # Alphanumeric only
    username: str = Field(pattern=r'^[a-zA-Z0-9_]+$')

    # UUID pattern
    uuid: str = Field(pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

# Invalid patterns
try:
    User(email="not-an-email", phone="abc", username="user@name", uuid="not-a-uuid")
except Exception as e:
    print(e)  # String should match pattern '...'
```

---

## field-examples

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(examples=["Alice Smith", "Bob Johnson"])
    age: int = Field(ge=0, examples=[25, 30, 35])
    email: str = Field(examples=["alice@example.com"])

# These appear in JSON Schema and OpenAPI docs
schema = User.model_json_schema()
print(schema["properties"]["name"])
# {'title': 'Name', 'type': 'string', 'examples': ['Alice Smith', 'Bob Johnson']}
```

---

## field-deprecated

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    email: str
    old_field: str | None = Field(default=None, deprecated=True)
    legacy_id: int | None = Field(default=None, deprecated="Use 'id' instead")

# Deprecated fields are marked in schema but still accepted
user = User(name="Alice", email="alice@x.com", old_field="value")
print(user.old_field)  # "value"

# Schema shows deprecated
schema = User.model_json_schema()
print(schema["properties"]["old_field"])
# {'title': 'Old Field', 'type': 'string', 'deprecated': True, 'default': None}
```

---

## field-validator

### Basic Usage

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if len(v.strip()) == 0:
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip().title()  # Transform the value

user = User(name="  alice  ", age=30)
print(user.name)  # "Alice" — transformed by validator
```

### Validating Multiple Fields

```python
class User(BaseModel):
    name: str
    email: str

    @field_validator('name', 'email')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

user = User(name="  Alice  ", email="  alice@x.com  ")
print(user.name)   # "Alice"
print(user.email)  # "alice@x.com"
```

### Mode='before' — Pre-Validation

```python
class User(BaseModel):
    age: int

    @field_validator('age', mode='before')
    @classmethod
    def parse_age(cls, v):
        # Runs BEFORE Pydantic's type validation
        # Input could be any type
        if isinstance(v, str):
            # Handle "25 years" or "25y" format
            v = v.replace('years', '').replace('y', '').strip()
        return v

user = User(age="25 years")
print(user.age)  # 25

user = User(age=25)
print(user.age)  # 25
```

### Mode='after' — Post-Validation (Default)

```python
class User(BaseModel):
    email: str

    @field_validator('email', mode='after')  # 'after' is the default
    @classmethod
    def validate_email(cls, v: str) -> str:
        # Input is already validated as str by Pydantic
        return v.lower()  # Normalize email

user = User(email="ALICE@EXAMPLE.COM")
print(user.email)  # "alice@example.com"
```

### Mode='wrap' — Wrapping Validation

```python
from pydantic import CoreValidatorHandler

class User(BaseModel):
    score: int

    @field_validator('score', mode='wrap')
    @classmethod
    def validate_score(cls, v, handler: CoreValidatorHandler) -> int:
        # 'handler' calls the next validator in the chain
        # You can modify input, skip validation, or add logic around it

        if isinstance(v, str) and v.lower() == 'perfect':
            return 100  # Bypass normal validation

        # Delegate to default Pydantic validation
        return handler(v)

user = User(score="perfect")
print(user.score)  # 100

user = User(score=95)
print(user.score)  # 95
```

### Validators with `@classmethod` and `@staticmethod`

```python
class User(BaseModel):
    name: str
    email: str

    # @classmethod is the standard approach
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        return v.strip()

    # @staticmethod also works (no cls parameter)
    @field_validator('email')
    @staticmethod
    def validate_email(v):
        return v.lower()
```

### Field Validator with `always=True`

```python
class User(BaseModel):
    name: str
    nickname: str = ""

    # In Pydantic V2, validators run even with defaults
    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, v):
        return v.lower() if v else v

user = User(name="Alice")
print(user.nickname)  # "" — validator still runs on default
```

### Using `info` Parameter

```python
from pydantic import BaseModel, field_validator, ValidationInfo

class User(BaseModel):
    name: str
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v, info: ValidationInfo):
        # info.data contains already-validated fields
        if 'name' in info.data and info.data['name'] in v:
            raise ValueError('Email cannot contain name')
        return v

user = User(name="Alice", email="bob@x.com")  # Valid
try:
    user = User(name="alice", email="alice@x.com")  # Invalid
except Exception as e:
    print(e)  # Email cannot contain name
```

---

## model-validator

### Mode='before' — Pre-Model Validation

```python
from pydantic import BaseModel, model_validator

class User(BaseModel):
    name: str
    age: int

    @model_validator(mode='before')
    @classmethod
    def validate_model(cls, data):
        # 'data' is the raw input dict (before any field validation)
        # Can modify data before field validation runs

        if isinstance(data, dict):
            # Handle "name:age" format
            if 'name' in data and ':' in str(data['name']):
                parts = str(data['name']).split(':')
                data['name'] = parts[0]
                if len(parts) > 1:
                    data['age'] = int(parts[1])

        return data

user = User.model_validate({"name": "Alice:30"})
print(user.name)  # "Alice"
print(user.age)   # 30
```

### Mode='after' — Post-Model Validation

```python
from pydantic import BaseModel, model_validator

class User(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def validate_passwords_match(self) -> 'User':
        # 'self' is the fully validated model instance
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

user = User(password="secret", confirm_password="secret")
print(user.password)  # "secret"

try:
    user = User(password="secret", confirm_password="wrong")
except Exception as e:
    print(e)  # Passwords do not match
```

### Complex Model Validation

```python
from pydantic import BaseModel, model_validator, field_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v):
        from datetime import datetime
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @model_validator(mode='after')
    def validate_date_order(self) -> 'DateRange':
        from datetime import datetime
        start = datetime.strptime(self.start_date, '%Y-%m-%d')
        end = datetime.strptime(self.end_date, '%Y-%m-%d')
        if start > end:
            raise ValueError('Start date must be before end date')
        return self

dr = DateRange(start_date="2025-01-01", end_date="2025-12-31")
print(dr)  # Valid

try:
    dr = DateRange(start_date="2025-12-31", end_date="2025-01-01")
except Exception as e:
    print(e)  # Start date must be before end date
```

---

## AfterValidator

`AfterValidator` runs after Pydantic's built-in validation. Part of the `typing_extensions.Annotated` pattern.

```python
from typing import Annotated
from pydantic import BaseModel, AfterValidator

def strip_whitespace(v: str) -> str:
    return v.strip()

def lowercase(v: str) -> str:
    return v.lower()

class User(BaseModel):
    name: Annotated[str, AfterValidator(strip_whitespace), AfterValidator(lowercase)]
    email: Annotated[str, AfterValidator(lowercase)]

user = User(name="  Alice  ", email="  ALICE@X.COM  ")
print(user.name)   # "alice"
print(user.email)  # "alice@x.com"
```

### Chaining Multiple AfterValidators

```python
from typing import Annotated
from pydantic import BaseModel, AfterValidator

def not_empty(v: str) -> str:
    if not v:
        raise ValueError("Cannot be empty")
    return v

def min_length_3(v: str) -> str:
    if len(v) < 3:
        raise ValueError("Must be at least 3 characters")
    return v

def alphanumeric(v: str) -> str:
    if not v.isalnum():
        raise ValueError("Must be alphanumeric")
    return v

Username = Annotated[
    str,
    AfterValidator(not_empty),
    AfterValidator(min_length_3),
    AfterValidator(alphanumeric)
]

class User(BaseModel):
    username: Username

user = User(username="alice123")
print(user.username)  # "alice123"
```

---

## BeforeValidator

`BeforeValidator` runs before Pydantic's built-in type validation.

```python
from typing import Annotated
from pydantic import BaseModel, BeforeValidator

def parse_string(v) -> str:
    """Convert various types to string before validation."""
    if isinstance(v, bytes):
        return v.decode('utf-8')
    if isinstance(v, int):
        return str(v)
    return v

class FlexibleInput(BaseModel):
    value: Annotated[str, BeforeValidator(parse_string)]

m = FlexibleInput(value=123)
print(m.value)      # "123"
print(type(m.value)) # <class 'str'>

m = FlexibleInput(value=b"hello")
print(m.value)  # "hello"

m = FlexibleInput(value="world")
print(m.value)  # "world"
```

### BeforeValidator for Numeric Coercion

```python
from typing import Annotated
from pydantic import BaseModel, BeforeValidator

def coerce_number(v) -> float:
    """Parse numbers from strings."""
    if isinstance(v, str):
        v = v.replace(',', '').replace('$', '').strip()
    return v

class Price(BaseModel):
    amount: Annotated[float, BeforeValidator(coerce_number)]

p = Price(amount="$1,234.56")
print(p.amount)  # 1234.56

p = Price(amount="99.99")
print(p.amount)  # 99.99

p = Price(amount=50.0)
print(p.amount)  # 50.0
```

---

## PlainValidator

`PlainValidator` replaces Pydantic's default validation entirely.

```python
from typing import Annotated
from pydantic import BaseModel, PlainValidator
import json

def validate_json_string(v):
    """Validate that a string is valid JSON and parse it."""
    if isinstance(v, str):
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON: {v}")
    if isinstance(v, (dict, list)):
        return v
    raise ValueError(f"Expected JSON string or dict/list, got {type(v)}")

class Config(BaseModel):
    data: Annotated[dict | list, PlainValidator(validate_json_string)]

c = Config(data='{"key": "value"}')
print(c.data)  # {'key': 'value'}

c = Config(data='[1, 2, 3]')
print(c.data)  # [1, 2, 3]

c = Config(data={"key": "value"})  # Already a dict
print(c.data)  # {'key': 'value'}

try:
    c = Config(data="not json")
except Exception as e:
    print(e)  # Invalid JSON: not json
```

---

## WrapValidator

`WrapValidator` gives you full control over the validation process, allowing you to intercept, modify, or skip validation.

```python
from typing import Annotated
from pydantic import BaseModel, WrapValidator

def debug_validator(v, handler):
    """Log all validation calls."""
    print(f"Validating: {v!r}")
    result = handler(v)
    print(f"Result: {result!r}")
    return result

class User(BaseModel):
    name: Annotated[str, WrapValidator(debug_validator)]
    age: Annotated[int, WrapValidator(debug_validator)]

user = User(name="Alice", age=30)
# Output:
# Validating: 'Alice'
# Result: 'Alice'
# Validating: 30
# Result: 30
```

### Conditional Validation

```python
from typing import Annotated
from pydantic import BaseModel, WrapValidator

def conditional_required(v, handler, info):
    """Make field required only if 'mode' is 'strict'."""
    # info.data may not have 'mode' yet if it's not validated
    # This is a simplified example
    result = handler(v)
    return result

def skip_if_none(v, handler):
    """Skip validation if value is None."""
    if v is None:
        return None
    return handler(v)

class User(BaseModel):
    name: Annotated[str | None, WrapValidator(skip_if_none)]
    age: int | None = None

user = User(name=None)
print(user.name)  # None — validation skipped

user = User(name="Alice")
print(user.name)  # "Alice" — validation ran
```

---

## Serializer Utilities

### BeforeSerializer

```python
from typing import Annotated
from pydantic import BaseModel, BeforeSerializer

class User(BaseModel):
    name: str
    tags: Annotated[
        list[str],
        BeforeSerializer(lambda v: sorted(v))  # Sort before serialization
    ]

user = User(name="Alice", tags=["c", "a", "b"])
print(user.model_dump())  # {'name': 'Alice', 'tags': ['a', 'b', 'c']}
```

### AfterSerializer

```python
from typing import Annotated
from pydantic import BaseModel, AfterSerializer

class User(BaseModel):
    name: str
    score: Annotated[
        float,
        AfterSerializer(lambda v: round(v, 2))  # Round to 2 decimals
    ]

user = User(name="Alice", score=95.678)
print(user.model_dump())  # {'name': 'Alice', 'score': 95.68}
```

### WrapSerializer

```python
from typing import Annotated
from pydantic import BaseModel, WrapSerializer

def add_currency(v, handler, info):
    """Add currency symbol during JSON serialization."""
    if info.mode == 'json':
        return f"${v:.2f}"
    return handler(v)

class Product(BaseModel):
    name: str
    price: Annotated[float, WrapSerializer(add_currency)]

p = Product(name="Widget", price=9.99)
print(p.model_dump())           # {'name': 'Widget', 'price': 9.99}
print(p.model_dump(mode='json')) # {'name': 'Widget', 'price': '$9.99'}
```

---

## Best Practices

### 1. Use `mode='before'` for Type Coercion

```python
class User(BaseModel):
    age: int

    @field_validator('age', mode='before')
    @classmethod
    def parse_age(cls, v):
        # Handle string inputs like "25" or "25 years"
        if isinstance(v, str):
            v = v.split()[0]  # Take first part
        return v
```

### 2. Use `mode='after'` for Normalization

```python
class User(BaseModel):
    email: str

    @field_validator('email', mode='after')
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()
```

### 3. Use `mode='wrap'` for Complex Control Flow

```python
@field_validator('value', mode='wrap')
@classmethod
def flexible_validation(cls, v, handler):
    if v == "SKIP":
        return None  # Skip validation entirely
    return handler(v)
```

### 4. Prefer Annotated Validators for Reusable Logic

```python
# Create reusable validator types
CleanStr = Annotated[str, AfterValidator(str.strip), AfterValidator(str.lower)]

class User(BaseModel):
    name: CleanStr
    email: CleanStr
```

### 5. Use `info` for Cross-Field Validation in field_validator

```python
@field_validator('end_date')
@classmethod
def validate_after_start(cls, v, info: ValidationInfo):
    if 'start_date' in info.data and v < info.data['start_date']:
        raise ValueError('end_date must be after start_date')
    return v
```

### 6. Use model_validator for Complex Cross-Field Logic

```python
@model_validator(mode='after')
def validate_consistency(self):
    if self.start_date > self.end_date:
        raise ValueError('start_date must be before end_date')
    return self
```

---

## Interview Questions

### Q1: What is the difference between `field_validator` and `model_validator`?

**Answer**: `field_validator` validates a **single field** — it receives the field value and returns the validated value. `model_validator` validates the **entire model** — it receives the full input dict (mode='before') or the model instance (mode='after'). Use `field_validator` for individual field constraints, and `model_validator` for cross-field validation logic.

---

### Q2: What is the difference between `mode='before'` and `mode='after'`?

**Answer**: `mode='before'` runs **before** Pydantic's built-in type validation — the input can be any type. `mode='after'` (default) runs **after** Pydantic validates the type — the input is guaranteed to be the annotated type. Use `before` for type coercion and `after` for normalization.

---

### Q3: When would you use `mode='wrap'`?

**Answer**: When you need full control over the validation chain. `mode='wrap'` gives you a `handler` function that calls the next validator. You can:
- Skip validation entirely (return a value without calling handler)
- Modify the input before validation
- Modify the output after validation
- Add logging/debugging around validation
- Implement conditional validation

---

### Q4: What is the difference between `field_validator` and `AfterValidator`?

**Answer**: `field_validator` is a **decorator** that creates a validator function — it's more flexible and can access model info. `AfterValidator` is a **type annotation component** used with `Annotated` — it's more composable and works at the type level. Both run after Pydantic's validation. Prefer `AfterValidator` for reusable validation logic, `field_validator` for model-specific logic.

---

### Q5: How do you validate that two fields match (e.g., password and confirm_password)?

**Answer**: Use `model_validator(mode='after')`:

```python
@model_validator(mode='after')
def passwords_match(self):
    if self.password != self.confirm_password:
        raise ValueError('Passwords do not match')
    return self
```

---

### Q6: Can a field have multiple validators? What order do they run?

**Answer**: Yes. Validators run in this order:
1. `BeforeValidator` (if any)
2. Pydantic's built-in type validation
3. `AfterValidator` (if any) — in order of declaration
4. `field_validator` (if any) — in order of declaration

For `model_validator`:
1. `mode='before'` validators
2. All field validation
3. `mode='after'` validators

---

### Q7: What does `@classmethod` vs `@staticmethod` mean for field_validator?

**Answer**: Both work. `@classmethod` receives `cls` (the model class) as the first argument, while `@staticmethod` doesn't. Use `@classmethod` if you need access to the model class (e.g., to access class-level config). Use `@staticmethod` for stateless validators that don't need the class.

---

### Q8: How do you access other field values inside a field_validator?

**Answer**: Use the `info` parameter:

```python
@field_validator('email')
@classmethod
def validate(cls, v, info: ValidationInfo):
    if 'name' in info.data:
        # Access already-validated 'name' field
        if info.data['name'] in v:
            raise ValueError('Email contains name')
    return v
```

---

### Q9: What is `Field(deprecated=True)` used for?

**Answer**: Marks a field as deprecated in the JSON schema. The field still works — it's just marked for documentation purposes. OpenAPI generators and schema tools will show the field as deprecated. Use `deprecated="reason"` to provide a deprecation message.

---

### Q10: Can you use `pattern` with `constr`?

**Answer**: Yes, but they're different approaches:
- `constr(pattern=r'^[a-z]+$')` — legacy constrained type
- `Annotated[str, Field(pattern=r'^[a-z]+$')]` — modern approach

Both validate the same way. Prefer the `Annotated` approach.

---
