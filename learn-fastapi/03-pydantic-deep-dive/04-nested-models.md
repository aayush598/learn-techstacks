# Pydantic Nested Models — The Complete Reference

## Table of Contents

1. [Basic Nested Models](#basic-nested)
2. [List of Models](#list-of-models)
3. [Dict of Models](#dict-of-models)
4. [Deeply Nested Structures](#deeply-nested)
5. [Forward References (ForwardRef)](#forward-ref)
6. [model_rebuild()](#model-rebuild)
7. [Dynamic Model Creation with create_model()](#create-model)
8. [Computed Fields](#computed-fields)
9. [Private Attributes](#private-attributes)
10. [Models with __slots__](#slots)
11. [Circular Reference Handling](#circular-references)
12. [Best Practices](#best-practices)
13. [Interview Questions](#interview-questions)

---

## Basic Nested Models

A nested model is simply a model used as a field type in another model.

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class User(BaseModel):
    name: str
    age: int
    address: Address  # Nested model

# Creating nested instances
user = User(
    name="Alice",
    age=30,
    address={
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62701"
    }
)

print(user.address.city)  # "Springfield"
print(type(user.address))  # <class '__main__.Address'>
```

### Nested Model Validation

```python
# Pydantic validates nested models too
try:
    user = User(
        name="Bob",
        age=25,
        address={
            "street": "456 Oak Ave",
            "city": "",       # Invalid — empty string
            "state": "CA",
            "zip_code": "12345"
        }
    )
except Exception as e:
    print(e)  # Validation error for address.city

# You can pass a dict or an Address instance
addr = Address(street="789 Pine Rd", city="Portland", state="OR", zip_code="97201")
user = User(name="Charlie", age=35, address=addr)
print(user.address)  # Address(street='789 Pine Rd', city='Portland', ...)
```

### Nested Model with Defaults

```python
class Settings(BaseModel):
    debug: bool = False
    log_level: str = "info"

class AppConfig(BaseModel):
    app_name: str
    settings: Settings = Settings()  # Default nested model instance

config = AppConfig(app_name="MyApp")
print(config.settings.debug)  # False

config = AppConfig(
    app_name="MyApp",
    settings={"debug": True, "log_level": "warning"}
)
print(config.settings.debug)  # True
```

---

## List of Models

### Basic List of Models

```python
from pydantic import BaseModel
from typing import List

class Tag(BaseModel):
    name: str
    color: str = "blue"

class Article(BaseModel):
    title: str
    tags: List[Tag]

# Creating with dicts
article = Article(
    title="Pydantic Guide",
    tags=[
        {"name": "python", "color": "blue"},
        {"name": "pydantic", "color": "green"},
        {"name": "validation", "color": "red"}
    ]
)

for tag in article.tags:
    print(f"{tag.name} ({tag.color})")
# python (blue)
# pydantic (green)
# validation (red)

# Access individual items
print(article.tags[0].name)  # "python"
print(len(article.tags))     # 3
```

### List with Validation

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)

class Order(BaseModel):
    items: list[Item] = Field(min_length=1)  # At least one item

# Valid
order = Order(items=[
    {"name": "Widget", "price": 9.99},
    {"name": "Gadget", "price": 19.99}
])

# Invalid — empty list
try:
    order = Order(items=[])
except Exception as e:
    print(e)  # List should have at least 1 item

# Invalid — item validation fails
try:
    order = Order(items=[{"name": "", "price": -5}])
except Exception as e:
    print(e)  # Multiple errors
```

### Empty List Default

```python
class Post(BaseModel):
    title: str
    comments: list[str] = []  # Empty list by default
    tags: list[str] = Field(default_factory=list)

post = Post(title="Hello World")
print(post.comments)  # []
print(post.tags)      # []
```

---

## Dict of Models

### Basic Dict of Models

```python
from pydantic import BaseModel

class ServerConfig(BaseModel):
    host: str
    port: int
    healthy: bool = True

class Cluster(BaseModel):
    name: str
    servers: dict[str, ServerConfig]  # Dict with string keys and model values

cluster = Cluster(
    name="production",
    servers={
        "web-01": {"host": "10.0.0.1", "port": 8080},
        "web-02": {"host": "10.0.0.2", "port": 8080},
        "db-01": {"host": "10.0.0.3", "port": 5432, "healthy": False}
    }
)

# Access nested dict of models
print(cluster.servers["web-1"].host)  # "10.0.0.1"
print(cluster.servers["db-01"].healthy)  # False

# Iterate
for name, config in cluster.servers.items():
    print(f"{name}: {config.host}:{config.port} (healthy={config.healthy})")
```

### Dynamic Keys

```python
from pydantic import BaseModel
from typing import Dict

class Metric(BaseModel):
    value: float
    unit: str
    timestamp: str

class Dashboard(BaseModel):
    name: str
    metrics: Dict[str, Metric]

dashboard = Dashboard(
    name="Server Metrics",
    metrics={
        "cpu_usage": {"value": 75.5, "unit": "%", "timestamp": "2025-01-01T00:00:00"},
        "memory_usage": {"value": 60.2, "unit": "%", "timestamp": "2025-01-01T00:00:00"},
        "disk_io": {"value": 120.0, "unit": "MB/s", "timestamp": "2025-01-01T00:00:00"}
    }
)

for name, metric in dashboard.metrics.items():
    print(f"{name}: {metric.value}{metric.unit}")
```

---

## Deeply Nested Structures

### Three Levels Deep

```python
from pydantic import BaseModel

class Coordinate(BaseModel):
    lat: float
    lng: float

class Location(BaseModel):
    name: str
    coordinates: Coordinate

class Business(BaseModel):
    name: str
    locations: list[Location]

class City(BaseModel):
    name: str
    businesses: list[Business]

# Create deeply nested structure
city = City(
    name="Springfield",
    businesses=[
        {
            "name": "Acme Corp",
            "locations": [
                {
                    "name": "HQ",
                    "coordinates": {"lat": 39.7817, "lng": -89.6501}
                },
                {
                    "name": "Branch",
                    "coordinates": {"lat": 39.7900, "lng": -89.6440}
                }
            ]
        }
    ]
)

# Access deeply nested data
print(city.businesses[0].locations[0].coordinates.lat)  # 39.7817
```

### Recursive Nesting

```python
from pydantic import BaseModel
from typing import Optional

class TreeNode(BaseModel):
    value: str
    children: list['TreeNode'] = []

# Build a tree
tree = TreeNode(
    value="root",
    children=[
        TreeNode(
            value="child1",
            children=[
                TreeNode(value="grandchild1"),
                TreeNode(value="grandchild2")
            ]
        ),
        TreeNode(
            value="child2",
            children=[]
        )
    ]
)

# Recursive traversal
def print_tree(node: TreeNode, indent: int = 0):
    print("  " * indent + node.value)
    for child in node.children:
        print_tree(child, indent + 1)

print_tree(tree)
# root
#   child1
#     grandchild1
#     grandchild2
#   child2
```

### Complex Nested with Mixed Types

```python
from pydantic import BaseModel
from typing import Union, Literal

class TextBlock(BaseModel):
    type: Literal["text"]
    content: str

class ImageBlock(BaseModel):
    type: Literal["image"]
    url: str
    caption: str = ""

class CodeBlock(BaseModel):
    type: Literal["code"]
    language: str
    code: str

ContentBlock = Union[TextBlock, ImageBlock, CodeBlock]

class Section(BaseModel):
    title: str
    blocks: list[ContentBlock]

class Page(BaseModel):
    title: str
    sections: list[Section]

# Create a complex document
page = Page(
    title="Documentation",
    sections=[
        {
            "title": "Introduction",
            "blocks": [
                {"type": "text", "content": "Welcome to our docs."},
                {"type": "image", "url": "logo.png", "caption": "Our Logo"},
                {"type": "code", "language": "python", "code": "print('Hello')"}
            ]
        }
    ]
)
```

---

## Forward References (ForwardRef)

When a model references itself or another model defined later in the file, you need forward references.

### Self-Referencing Models

```python
from pydantic import BaseModel
from typing import Optional

# Forward reference as string
class Employee(BaseModel):
    name: str
    manager: Optional['Employee'] = None  # Forward reference
    reports: list['Employee'] = []        # Forward reference

# IMPORTANT: Call model_rebuild() to resolve forward references
Employee.model_rebuild()

# Now it works
ceo = Employee(name="CEO")
vp = Employee(name="VP", manager=ceo)
dev = Employee(name="Developer", manager=vp)

print(dev.manager.name)  # "VP"
print(dev.manager.manager.name)  # "CEO"
```

### Cross-Model References

```python
from pydantic import BaseModel
from typing import Optional

# Model B references Model A, but Model A is defined first
class Department(BaseModel):
    name: str
    head: Optional['Employee'] = None

class Employee(BaseModel):
    name: str
    department: Optional[Department] = None

# Resolve forward references
Department.model_rebuild()
Employee.model_rebuild()

# Create instances
dept = Department(name="Engineering")
emp = Employee(name="Alice", department=dept)
print(emp.department.name)  # "Engineering"
```

### Forward References with Generics

```python
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Container(BaseModel, Generic[T]):
    value: T
    next: Optional['Container[T]'] = None

Container.model_rebuild()

# Usage
c1 = Container(value=1)
c2 = Container(value=2, next=c1)
c3 = Container(value=3, next=c2)

# Linked list: 3 -> 2 -> 1
current = c3
while current:
    print(current.value, end=" -> ")
    current = current.next
print("None")
# 3 -> 2 -> 1 -> None
```

---

## model_rebuild()

`model_rebuild()` resolves forward references in a model. You **must** call it after defining all referenced models.

```python
from pydantic import BaseModel
from typing import Optional

class Node(BaseModel):
    value: int
    children: list['Node'] = []  # Forward reference
    parent: Optional['Node'] = None  # Forward reference

# Without model_rebuild(), this would fail
Node.model_rebuild()

# Now create instances
root = Node(value=1)
child = Node(value=2, parent=root)
root.children.append(child)

print(root.children[0].value)  # 2
```

### When to Call model_rebuild

```python
# SCENARIO 1: Self-referencing (ALWAYS needed)
class TreeNode(BaseModel):
    value: str
    children: list['TreeNode'] = []

TreeNode.model_rebuild()  # Required

# SCENARIO 2: Forward reference to later-defined model
class First(BaseModel):
    ref: 'Second'

class Second(BaseModel):
    value: str

First.model_rebuild()  # Required
Second.model_rebuild()  # May also be needed if Second references First

# SCENARIO 3: No forward references (NOT needed)
class Simple(BaseModel):
    name: str
    age: int
# No model_rebuild() needed
```

### _parents Parameter

```python
# model_rebuild can accept _parents to resolve references in parent models
class A(BaseModel):
    b: 'B'

class B(BaseModel):
    value: int

A.model_rebuild()
B.model_rebuild()
```

---

## create_model()

`create_model()` creates Pydantic models dynamically at runtime.

### Basic Usage

```python
from pydantic import create_model, Field

# Create a model dynamically
DynamicModel = create_model(
    'DynamicModel',
    name=(str, Field(..., description="User name")),
    age=(int, Field(ge=0, description="User age")),
    email=(str, Field(..., description="Email address"))
)

# Use it like any Pydantic model
instance = DynamicModel(name="Alice", age=30, email="alice@example.com")
print(instance)  # DynamicModel(name='Alice', age=30, email='alice@example.com')
```

### Dynamic Model with Defaults

```python
DynamicModel = create_model(
    'Config',
    host=(str, Field(default="localhost")),
    port=(int, Field(default=8000)),
    debug=(bool, Field(default=False))
)

config = DynamicModel()  # All defaults
print(config)  # Config(host='localhost', port=8000, debug=False)
```

### Dynamic Model from Dict

```python
def create_model_from_dict(name: str, fields: dict) -> type:
    """Create a Pydantic model from a field definition dict."""
    field_definitions = {}
    for field_name, field_info in fields.items():
        field_type = field_info.get('type', str)
        field_default = field_info.get('default', ...)
        field_desc = field_info.get('description', '')

        field_definitions[field_name] = (
            field_type,
            Field(default=field_default, description=field_desc)
        )

    return create_model(name, **field_definitions)

# Usage
UserModel = create_model_from_dict('User', {
    'name': {'type': str, 'description': 'User name'},
    'age': {'type': int, 'description': 'User age'},
    'email': {'type': str, 'description': 'Email'}
})

user = UserModel(name="Alice", age=30, email="alice@example.com")
print(user)
```

### Dynamic Model with Nested Models

```python
from pydantic import create_model, Field

# Create nested models dynamically
AddressModel = create_model(
    'Address',
    street=(str, ...),
    city=(str, ...),
    zip_code=(str, ...)
)

UserModel = create_model(
    'User',
    name=(str, ...),
    age=(int, Field(ge=0)),
    address=(AddressModel, ...)
)

user = UserModel(
    name="Bob",
    age=25,
    address={"street": "123 Main", "city": "NYC", "zip_code": "10001"}
)
print(user.address.city)  # "NYC"
```

---

## Computed Fields

Computed fields are derived from other fields using `@computed_field`.

```python
from pydantic import BaseModel, computed_field
from datetime import datetime

class User(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def age(self) -> int:
        today = datetime.now()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

user = User(
    first_name="Alice",
    last_name="Smith",
    birth_date=datetime(1990, 5, 15)
)

print(user.full_name)  # "Alice Smith"
print(user.age)        # 35 (computed)

# Computed fields are included in serialization
print(user.model_dump())
# {'first_name': 'Alice', 'last_name': 'Smith', 'birth_date': datetime(1990, 5, 15, 0, 0),
#  'full_name': 'Alice Smith', 'age': 35}

print(user.model_dump_json())
# {"first_name":"Alice","last_name":"Smith","birth_date":"1990-05-15T00:00:00","full_name":"Alice Smith","age":35}
```

### Computed Field with caching

```python
from pydantic import BaseModel, computed_field
from functools import cached_property

class ExpensiveModel(BaseModel):
    data: list[int]

    @computed_field
    @property
    def sorted_data(self) -> list[int]:
        # Expensive computation — result is cached
        return sorted(self.data, reverse=True)

m = ExpensiveModel(data=[3, 1, 4, 1, 5, 9, 2, 6])
print(m.sorted_data)  # [9, 6, 5, 4, 3, 2, 1, 1]
print(m.sorted_data)  # Cached — same object
```

### Computed Field in JSON Schema

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

    @computed_field
    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

schema = Rectangle.model_json_schema()
print(schema)
# Shows width, height as properties
# area and perimeter are computed fields
```

---

## Private Attributes

Private attributes (prefixed with `_`) are not part of the model's schema or serialization.

```python
from pydantic import BaseModel, PrivateAttr

class User(BaseModel):
    name: str
    email: str
    _id: int = PrivateAttr(default=0)  # Private attribute
    _cache: dict = PrivateAttr(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)
        # Private attributes are set in __init__
        self._id = id(self)
        self._cache = {}

user = User(name="Alice", email="alice@x.com")

# Public fields
print(user.name)   # "Alice"
print(user.email)  # "alice@x.com"

# Private attributes
print(user._id)    # Some memory address
print(user._cache) # {}

# Not in serialization
print(user.model_dump())  # {'name': 'Alice', 'email': 'alice@x.com'} — no _id, _cache

# Not in JSON schema
schema = User.model_json_schema()
print("_id" in schema.get("properties", {}))  # False
```

### Private Attributes with Validation

```python
from pydantic import BaseModel, PrivateAttr

class CachedModel(BaseModel):
    value: int
    _computed: int = PrivateAttr(default=0)

    def __init__(self, **data):
        super().__init__(**data)
        self._computed = self.value * 2  # Computed once

    @property
    def computed_value(self) -> int:
        return self._computed

m = CachedModel(value=21)
print(m.computed_value)  # 42
print(m._computed)       # 42
```

---

## Models with __slots__

Using `__slots__` can improve memory efficiency for models with many instances.

```python
from pydantic import BaseModel

class SlottedModel(BaseModel):
    __slots__ = ('_cache',)
    name: str
    age: int

    def __init__(self, **data):
        super().__init__(**data)
        self._cache = {}

m = SlottedModel(name="Alice", age=30)
print(m.name)  # "Alice"
```

> **Note**: In Pydantic V2, `__slots__` handling has changed. The recommended approach is to use `PrivateAttr` instead.

---

## Circular Reference Handling

### Basic Circular Reference

```python
from pydantic import BaseModel
from typing import Optional

class Node(BaseModel):
    name: str
    left: Optional['Node'] = None
    right: Optional['Node'] = None

Node.model_rebuild()

# Create circular structure
root = Node(name="root")
left = Node(name="left")
right = Node(name="right")
root.left = left
root.right = right
left.left = Node(name="left-left")  # Deep nesting

# Serialization handles circular references
# But be careful — very deep circular structures can cause issues
```

### Parent-Child Circular Reference

```python
from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    name: str
    parent: Optional['Category'] = None
    children: list['Category'] = []

Category.model_rebuild()

# Build category tree
root = Category(name="Electronics")
phones = Category(name="Phones", parent=root)
root.children.append(phones)

iphone = Category(name="iPhone", parent=phones)
phones.children.append(iphone)

print(root.children[0].name)  # "Phones"
print(root.children[0].children[0].name)  # "iPhone"
```

### Avoiding Infinite Recursion in Serialization

```python
from pydantic import BaseModel
from typing import Optional

class Node(BaseModel):
    name: str
    parent: Optional['Node'] = None
    children: list['Node'] = []

Node.model_rebuild()

# Create tree
root = Node(name="root")
child = Node(name="child", parent=root)
root.children.append(child)

# Serialization with circular references
# Pydantic V2 handles this by NOT including the full circular reference
# The 'parent' field will be None or excluded to prevent infinite recursion
data = root.model_dump()
print(data)
# {'name': 'root', 'parent': None, 'children': [{'name': 'child', 'parent': None, 'children': []}]}
# Note: parent is None in serialization to avoid infinite loop
```

---

## Best Practices

### 1. Keep Nesting Reasonable (Max 3-4 Levels)

```python
# GOOD — reasonable nesting
class Company(BaseModel):
    name: str
    departments: list[Department]

class Department(BaseModel):
    name: str
    employees: list[Employee]

class Employee(BaseModel):
    name: str
    skills: list[str]

# BAD — too deep (5+ levels)
# Company > Division > Department > Team > Employee > Skill > SkillDetail > ...
```

### 2. Use model_rebuild() for Forward References

```python
class Node(BaseModel):
    children: list['Node'] = []

# ALWAYS call this after defining self-referencing models
Node.model_rebuild()
```

### 3. Use Computed Fields for Derived Values

```python
class Order(BaseModel):
    items: list[Item]

    @computed_field
    @property
    def total(self) -> float:
        return sum(item.price * item.quantity for item in self.items)
```

### 4. Use Private Attributes for Internal State

```python
class User(BaseModel):
    name: str
    _cache: dict = PrivateAttr(default_factory=dict)
```

### 5. Validate Nested Models at Construction

```python
# Pydantic automatically validates nested models
# But you can add additional validation with model_validator
@model_validator(mode='after')
def validate_nested(self):
    if self.address and not self.address.city:
        raise ValueError("Address city cannot be empty")
    return self
```

### 6. Consider Performance for Large Nested Structures

```python
# For large lists of models, consider:
# 1. Using model_construct() if data is pre-validated
# 2. Lazy loading patterns
# 3. Pagination instead of loading all at once
```

---

## Interview Questions

### Q1: How do you handle self-referencing models?

**Answer**: Use a forward reference (string annotation) like `'Node'` and call `model_rebuild()` after the model class is defined. Pydantic resolves the forward references during rebuild.

```python
class Node(BaseModel):
    children: list['Node'] = []
Node.model_rebuild()
```

---

### Q2: What is `model_rebuild()` and when do you need it?

**Answer**: `model_rebuild()` resolves forward references in a model. You need it when:
- A model references itself (self-referencing)
- A model references another model defined later in the file
- You're using `create_model()` with forward references

Without it, Pydantic can't resolve the string annotations and will raise an error when creating instances.

---

### Q3: How do you create a model dynamically at runtime?

**Answer**: Use `pydantic.create_model()`:

```python
from pydantic import create_model, Field
DynamicModel = create_model('Dynamic', name=(str, ...), age=(int, Field(ge=0)))
```

Or use `TypeAdapter` for simpler validation without a full model class.

---

### Q4: What is the difference between `computed_field` and a regular `@property`?

**Answer**: `computed_field` is a Pydantic decorator that:
- Automatically includes the field in serialization (`model_dump()`, `model_dump_json()`)
- Includes the field in JSON schema generation
- Is validated as part of the model

A regular `@property` is just a Python property — it doesn't participate in serialization or schema generation.

---

### Q5: How do you handle circular references during serialization?

**Answer**: Pydantic V2 handles circular references by breaking the cycle during serialization. When a model has a circular reference (e.g., parent → child → parent), the second reference is typically serialized as `None` or excluded. This prevents infinite recursion.

---

### Q6: What are private attributes and how do they differ from regular fields?

**Answer**: Private attributes (defined with `PrivateAttr`) are:
- Not included in the model schema
- Not serialized (not in `model_dump()`)
- Not validated by Pydantic
- Set manually in `__init__`

They're for internal model state (caches, computed values, etc.) that shouldn't be exposed.

---

### Q7: Can you nest models inside `Dict[str, Model]`?

**Answer**: Yes. `dict[str, MyModel]` is fully supported. Pydantic validates each value in the dict against the model type. The keys must be strings (or the specified type).

---

### Q8: How do you create a model from a dictionary at runtime?

**Answer**: Several approaches:
1. `create_model()` — for dynamic schema generation
2. `TypeAdapter` — for simple validation
3. `BaseModel.model_validate(dict_data)` — for dict → existing model

---

### Q9: What happens if you forget to call `model_rebuild()`?

**Answer**: Pydantic will raise a `PydanticUserError` when you try to instantiate the model, saying that the model has not been built. The forward references remain as strings and can't be resolved.

---

### Q10: How do you add validation to nested models?

**Answer**: Add validators to the nested model class itself, or use `model_validator` on the parent model to validate the nested structure. Pydantic validates nested models during construction, so field constraints on nested models are automatically enforced.

---

### Q11: Can you have a list of discriminated unions in a nested model?

**Answer**: Yes:

```python
from typing import Annotated, Union
from pydantic import BaseModel, Field

class Cat(BaseModel):
    type: Literal["cat"]
    meow: int

class Dog(BaseModel):
    type: Literal["dog"]
    bark: int

Pet = Annotated[Union[Cat, Dog], Field(discriminator="type")]

class Household(BaseModel):
    pets: list[Pet]

h = Household(pets=[{"type": "cat", "meow": 5}, {"type": "dog", "bark": 8}])
```

---

### Q12: How do you handle deeply nested JSON (e.g., from MongoDB)?

**Answer**: Create nested Pydantic models that match the document structure. Use `model_validate(json_data)` to parse the nested JSON. For variable schemas, consider using `dict[str, Any]` for unknown nested structures, or dynamic models with `create_model()`.

---
