# Pydantic Interview Questions — 35+ Questions with Detailed Answers

## Table of Contents

1. [Fundamentals](#fundamentals)
2. [Validation](#validation)
3. [Serialization](#serialization)
4. [Nested Models](#nested-models)
5. [Advanced Topics](#advanced-topics)
6. [Performance and Patterns](#performance-patterns)

---

## Fundamentals

### Q1: How does Pydantic validate data?

**Answer**: Pydantic uses Python **type hints** to define the expected shape of data. When you create a model instance, Pydantic:

1. **Parses** the input data (dict, kwargs, JSON, etc.)
2. **Validates** each field against its type annotation
3. **Coerces** values to the correct type when possible (lax mode)
4. **Applies constraints** (Field(ge=0), min_length, pattern, etc.)
5. **Runs validators** (field_validator, model_validator, BeforeValidator, AfterValidator)
6. **Returns** the validated model instance or raises `ValidationError`

The validation is powered by **pydantic-core** (written in Rust), making it extremely fast.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Pydantic: 1) parses kwargs, 2) validates types, 3) coerces "25" to 25
user = User(name="Alice", age="25")  # age is str, coerced to int
print(user.age)  # 25 (int)
```

---

### Q2: What is the difference between Pydantic V1 and V2?

**Answer**:

| Feature | V1 | V2 |
|---------|----|----|
| Core engine | Python | Rust (pydantic-core) |
| Config style | Inner `class Config` | `model_config = ConfigDict(...)` |
| Serialization | `.dict()` / `.json()` | `.model_dump()` / `.model_dump_json()` |
| Validation | `.parse_obj()` / `.parse_raw()` | `.model_validate()` / `.model_validate_json()` |
| Field validators | `@validator` | `@field_validator` |
| Model validators | `@root_validator` | `@model_validator` |
| Performance | ~10x slower | Baseline (fast) |

---

### Q3: What are the main methods of BaseModel?

**Answer**:

**Construction/Validation**:
- `__init__(**kwargs)` — Constructor with validation
- `model_validate(obj)` — Validate from dict/object
- `model_validate_json(json)` — Validate from JSON string
- `model_construct(**kwargs)` — Skip validation (fast)

**Serialization**:
- `model_dump()` — Export as Python dict
- `model_dump_json()` — Export as JSON string

**Schema**:
- `model_json_schema()` — Generate JSON Schema

**Other**:
- `model_copy(update={})` — Copy with updates
- `model_fields` — Field metadata dict
- `model_extra` — Extra fields dict
- `model_rebuild()` — Resolve forward references

---

### Q4: What is model_construct and when would you use it?

**Answer**: `model_construct()` creates a model instance **without running validation**. It's the fastest way to create a model.

**When to use**:
- Data is already validated elsewhere (e.g., from database)
- Performance-critical code paths
- Building partial models for updates

**When NOT to use**:
- Data from untrusted sources (user input, APIs)
- When you need guaranteed data integrity

```python
# Fast but dangerous — no validation
user = User.model_construct(name="Alice", age="not_a_number")
print(user.age)  # "not_a_number" — invalid but no error

# Safe but slower — full validation
user = User(name="Alice", age=30)  # Validates age is int
```

---

### Q5: What is the difference between model_dump and model_dump_json?

**Answer**:

- `model_dump()` returns a Python `dict` — useful for further manipulation in Python
- `model_dump_json()` returns a JSON `str` — useful for API responses, logging, storage

`model_dump_json()` is generally **faster** because it serializes directly to JSON without creating an intermediate dict.

```python
user = User(name="Alice", age=30)

# Dict — manipulate in Python
data = user.model_dump()
data['extra'] = 'value'

# JSON string — ready for HTTP response
json_str = user.model_dump_json()
```

---

## Validation

### Q6: What is the difference between field_validator and model_validator?

**Answer**:

- `field_validator` validates a **single field** — receives the field value
- `model_validator` validates the **entire model** — receives the full dict or model instance

Use `field_validator` for individual field constraints. Use `model_validator` for cross-field validation (e.g., ensuring end_date > start_date).

```python
class Event(BaseModel):
    start_date: str
    end_date: str

    # Field-level: validate individual dates
    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v):
        # v is a single date string
        return v

    # Model-level: validate relationship between fields
    @model_validator(mode='after')
    def validate_order(self):
        if self.start_date > self.end_date:
            raise ValueError('start_date must be before end_date')
        return self
```

---

### Q7: What is the difference between mode='before' and mode='after'?

**Answer**:

- `mode='before'` runs **before** Pydantic's type validation — input can be any type
- `mode='after'` (default) runs **after** Pydantic validates the type — input is guaranteed to be the annotated type

```python
@field_validator('age', mode='before')
@classmethod
def parse_age(cls, v):
    # v could be "25 years" (string), 25 (int), etc.
    if isinstance(v, str):
        v = v.split()[0]
    return v

@field_validator('email', mode='after')
@classmethod
def normalize_email(cls, v):
    # v is guaranteed to be str
    return v.lower()
```

---

### Q8: How do you handle nested validation?

**Answer**: Pydantic automatically validates nested models. For additional nested validation, use validators:

```python
class Address(BaseModel):
    street: str = Field(min_length=1)
    city: str = Field(min_length=1)

class User(BaseModel):
    name: str
    address: Address

    @model_validator(mode='after')
    def validate_address(self):
        if self.address and not self.address.city:
            raise ValueError("Address city required")
        return self
```

---

### Q9: What is the difference between Field(default=...) and Field(default_factory=...)?

**Answer**:

- `Field(default=value)` — static default, shared across instances (fine for immutables)
- `Field(default_factory=func)` — dynamic default, creates a new instance per model

For mutable defaults (list, dict, set), use `default_factory`:

```python
class Team(BaseModel):
    name: str
    members: list[str] = Field(default_factory=list)  # New list per instance
    config: dict = Field(default_factory=dict)
```

---

### Q10: What does Field(frozen=True) do?

**Answer**: Makes a single field immutable after model creation. The field can be set during construction but cannot be reassigned:

```python
class User(BaseModel):
    id: int = Field(frozen=True)  # Cannot be changed after creation
    name: str  # Can be changed

user = User(id=1, name="Alice")
user.name = "Bob"    # OK
# user.id = 2        # ValidationError — frozen field
```

---

## Serialization

### Q11: How do you customize serialization?

**Answer**: Three approaches:

1. **`@field_serializer`** — customize a single field:
```python
@field_serializer('email')
def mask_email(self, v):
    return v[:2] + "***" + v[v.index('@'):]
```

2. **`@model_serializer`** — customize entire model:
```python
@model_serializer(mode='wrap')
def serialize(self, default_serializer, info):
    data = default_serializer(self)
    data['_type'] = self.__class__.__name__
    return data
```

3. **`PlainSerializer`** — type-level serialization:
```python
score: Annotated[float, PlainSerializer(lambda v: f"{v:.2f}%")]
```

---

### Q12: What is the difference between exclude_none, exclude_unset, and exclude_defaults?

**Answer**:

- **`exclude_none`**: Removes fields where value is `None`
- **`exclude_unset`**: Removes fields not explicitly provided during construction
- **`exclude_defaults`**: Removes fields still at their default values

```python
class User(BaseModel):
    name: str
    age: int = 0
    email: str | None = None
    role: str = "user"

user = User(name="Alice", age=25)

user.model_dump(exclude_none=True)    # {'name': 'Alice', 'age': 25, 'role': 'user'}
user.model_dump(exclude_unset=True)   # {'name': 'Alice', 'age': 25}
user.model_dump(exclude_defaults=True) # {'name': 'Alice', 'age': 25}
```

---

### Q13: How do you serialize with aliases?

**Answer**: Use `model_dump(by_alias=True)`:

```python
class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_name: str = Field(serialization_alias="userName")

user = User(user_name="alice")
user.model_dump()                     # {'user_name': 'alice'}
user.model_dump(by_alias=True)        # {'userName': 'alice'}
user.model_dump_json(by_alias=True)   # '{"userName":"alice"}'
```

---

### Q14: What is the SerializationInfo parameter?

**Answer**: `SerializationInfo` provides context during serialization:

```python
@field_serializer('password')
def serialize(self, v, info: SerializationInfo):
    if info.mode == 'json':    # 'python' or 'json'
        return "***"
    if info.context and info.context.get('admin'):
        return v
    return "***"
```

---

## Nested Models

### Q15: How do you handle nested models?

**Answer**: Define models as field types. Pydantic validates and serializes them recursively:

```python
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    address: Address  # Nested — validated and serialized recursively

user = User(name="Alice", address={"street": "123 Main", "city": "NYC"})
user.model_dump()  # {'name': 'Alice', 'address': {'street': '123 Main', 'city': 'NYC'}}
```

---

### Q16: How do you handle circular references?

**Answer**: Use forward references (string annotations) and `model_rebuild()`:

```python
class Node(BaseModel):
    name: str
    parent: Optional['Node'] = None
    children: list['Node'] = []

Node.model_rebuild()  # Resolve forward references
```

During serialization, Pydantic breaks cycles by setting repeated references to `None`.

---

### Q17: What is model_rebuild() and when do you need it?

**Answer**: `model_rebuild()` resolves forward references in a model. You need it when:
- A model references itself (self-referencing)
- A model references a class defined later in the file
- You use `create_model()` with forward references

Without it, Pydantic raises `PydanticUserError: 'Model' has not been built`.

---

### Q18: How do you create a list of models from dicts?

**Answer**: Pydantic handles this automatically:

```python
class User(BaseModel):
    name: str
    age: int

class Team(BaseModel):
    members: list[User]

team = Team(members=[
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
])
# team.members is a list of User instances
```

---

## Advanced Topics

### Q19: How do you create dynamic models?

**Answer**: Use `create_model()`:

```python
from pydantic import create_model, Field

DynamicModel = create_model(
    'Dynamic',
    name=(str, Field(...)),
    age=(int, Field(ge=0))
)

instance = DynamicModel(name="Alice", age=30)
```

---

### Q20: What is TypeAdapter?

**Answer**: `TypeAdapter` validates and serializes standalone types without creating a model class:

```python
from pydantic import TypeAdapter

ta = TypeAdapter(list[int])
result = ta.validate_python([1, 2, 3])
schema = ta.json_schema()
```

Use it for simple type validation where you don't need a full model.

---

### Q21: How do you handle extra fields?

**Answer**: Use `ConfigDict(extra=...)`:

- `extra='ignore'` (default): Silently drop extra fields
- `extra='forbid'`: Raise `ValidationError` for extra fields
- `extra='allow'`: Store extra fields in `model_extra`

```python
class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str
```

---

### Q22: What is the difference between Annotated and conint/constr?

**Answer**: Both apply constraints. `Annotated` is the modern approach:

```python
# Modern (preferred)
age: Annotated[int, Field(ge=0, le=150)]

# Legacy (still works)
age: conint(ge=0, le=150)
```

`Annotated` is more readable, composable, and standard Python.

---

### Q23: How do discriminated unions work?

**Answer**: A discriminated union uses a discriminator field to determine which model to validate against:

```python
class Cat(BaseModel):
    type: Literal["cat"]
    meow: int

class Dog(BaseModel):
    type: Literal["dog"]
    bark: int

class Pet(BaseModel):
    animal: Annotated[Union[Cat, Dog], Field(discriminator="type")]
```

Instead of trying each model sequentially (slow), Pydantic reads the discriminator and jumps to the right model (fast).

---

### Q24: What are computed fields?

**Answer**: Computed fields are derived from other fields using `@computed_field`:

```python
class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

Computed fields are included in serialization and JSON schema.

---

### Q25: How do you use from_attributes (orm_mode)?

**Answer**: Enable it to create models from ORM objects:

```python
class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str

# Works with any object that has .name attribute
orm_user = SQLAlchemyUser(name="Alice")
schema = UserSchema.model_validate(orm_user)
```

---

### Q26: What is the difference between frozen and Field(frozen=True)?

**Answer**:

- `ConfigDict(frozen=True)`: **Entire model** is immutable
- `Field(frozen=True)`: Only **that specific field** is immutable

```python
class FrozenModel(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str  # Immutable

class PartiallyFrozen(BaseModel):
    id: int = Field(frozen=True)    # Immutable
    name: str                        # Mutable
```

---

### Q27: How do you handle secrets in Pydantic?

**Answer**: Use `SecretStr` and `SecretBytes`:

```python
class APIClient(BaseModel):
    api_key: SecretStr
    password: SecretStr

client = APIClient(api_key="sk-123", password="secret")
print(client.api_key)              # SecretStr('**********')
client.api_key.get_secret_value()  # 'sk-123'
```

Secrets are masked in repr, serialization, and logs.

---

### Q28: How do you generate JSON Schema?

**Answer**:

```python
schema = MyModel.model_json_schema()
# For TypeAdapter:
schema = ta.json_schema()
```

Customize with `Field(description=..., examples=...)` and `ConfigDict(json_schema_extra=...)`.

---

### Q29: What is validate_assignment?

**Answer**: When `True`, Pydantic re-validates field values when assigned after model creation:

```python
class User(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    age: int = Field(ge=0)

user = User(age=25)
user.age = 30     # OK
user.age = -5     # ValidationError
```

---

### Q30: How do you create a model from a dict at runtime?

**Answer**: Several approaches:

1. `create_model()` — for dynamic schema generation
2. `TypeAdapter(type).validate_python(data)` — for simple validation
3. `ExistingModel.model_validate(data)` — for dict → existing model

---

## Performance Patterns

### Q31: What is the fastest way to create a Pydantic model?

**Answer**: `model_construct()` — skips validation entirely. But only use it when data is pre-validated:

```python
# Fastest — no validation
user = User.model_construct(name="Alice", age=30)

# Fast — standard validation (uses Rust core)
user = User(name="Alice", age=30)
```

---

### Q32: When should you use model_dump_json() vs json.dumps(model_dump())?

**Answer**: Always prefer `model_dump_json()`:

```python
# GOOD — direct, fast, handles types
json_str = user.model_dump_json()

# BAD — slower, may fail on complex types
json_str = json.dumps(user.model_dump(), default=str)
```

---

### Q33: How do you minimize serialization output?

**Answer**: Combine exclude options:

```python
# Only include explicitly set, non-None fields
data = user.model_dump(exclude_unset=True, exclude_none=True)

# Exclude specific fields
data = user.model_dump(exclude={"password", "internal_id"})
```

---

### Q34: How do you handle large lists of models efficiently?

**Answer**:

1. Use `model_construct()` if data is pre-validated
2. Process in batches instead of all at once
3. Use `model_dump(mode='json')` for faster serialization
4. Consider pagination for large result sets

---

### Q35: What are private attributes and when do you use them?

**Answer**: Private attributes (prefixed with `_`) are not part of the schema or serialization:

```python
class User(BaseModel):
    name: str
    _cache: dict = PrivateAttr(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)
        self._cache = {}
```

Use them for internal state like caches, computed values, or connection handles.

---

### Q36: How do you handle Union types in Pydantic?

**Answer**: Pydantic tries each type in the union sequentially. For better performance, use discriminated unions:

```python
# Slow — tries each type
class Event(BaseModel):
    data: Union[ClickEvent, PageView, Purchase]

# Fast — uses discriminator field
class Event(BaseModel):
    data: Annotated[Union[ClickEvent, PageView, Purchase], Field(discriminator="type")]
```

---

### Q37: What is the difference between PlainValidator, AfterValidator, and WrapValidator?

**Answer**:

- **`BeforeValidator`**: Runs before Pydantic's type validation (input is unvalidated)
- **`AfterValidator`**: Runs after Pydantic's type validation (input is the correct type)
- **`PlainValidator`**: Replaces Pydantic's validation entirely
- **`WrapValidator`**: Wraps around Pydantic's validation with full control

```python
# BeforeValidator — type coercion
Annotated[str, BeforeValidator(lambda v: str(v).strip())]

# AfterValidator — normalization
Annotated[str, AfterValidator(str.lower)]

# PlainValidator — full custom validation
Annotated[int, PlainValidator(lambda v: int(v) if isinstance(v, str) else v)]

# WrapValidator — control around validation
Annotated[int, WrapValidator(lambda v, handler: handler(v) if v != "skip" else None)]
```

---

### Q38: How do you implement the Repository Pattern with Pydantic?

**Answer**:

```python
from pydantic import BaseModel, ConfigDict

# Schema for creation (no id)
class UserCreate(BaseModel):
    name: str
    email: str

# Schema for response (with id)
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str

# Repository converts between schemas
def create_user(data: UserCreate) -> UserResponse:
    db_user = save_to_db(data.model_dump())  # Save to database
    return UserResponse.model_validate(db_user)  # Convert to response
```

---

### Q39: How do you version API schemas with Pydantic?

**Answer**:

```python
# V1 schema
class UserV1(BaseModel):
    name: str
    email: str

# V2 schema (extends V1)
class UserV2(UserV1):
    age: int | None = None
    phone: str | None = None

# Use version-specific schemas in endpoints
@app.get("/v1/users", response_model=UserV1)
def get_user_v1(): ...

@app.get("/v2/users", response_model=UserV2)
def get_user_v2(): ...
```

---

### Q40: What are the best practices for Pydantic in production?

**Answer**:

1. **Always use type hints** — makes validation explicit
2. **Use `Field()` for constraints** — document expected values
3. **Use `model_dump_json()`** over `json.dumps(model_dump())`
4. **Use `SecretStr`** for sensitive data
5. **Use `from_attributes=True`** for ORM integration
6. **Use `ConfigDict(frozen=True)`** for value objects
7. **Use `ConfigDict(extra='forbid')`** for strict APIs
8. **Test JSON schema output** against your API contract
9. **Use `exclude_unset=True`** for PATCH operations
10. **Prefer `Annotated`** over `conint`/`constr` for constraints
11. **Use `validate_assignment=True`** when field mutation is needed
12. **Use discriminated unions** over plain unions for performance

---
