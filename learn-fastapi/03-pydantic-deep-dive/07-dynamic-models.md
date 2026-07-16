# Pydantic Dynamic Models — The Complete Reference

## Table of Contents

1. [Why Dynamic Models](#why-dynamic)
2. [create_model() Basics](#create-model-basics)
3. [Dynamic Field Creation](#dynamic-fields)
4. [TypeAdapter](#type-adapter)
5. [Model Serializer Patterns](#serializer-patterns)
6. [Runtime Model Generation](#runtime-generation)
7. [Dynamic API Schemas](#dynamic-api-schemas)
8. [model_from_dict Pattern](#model-from-dict)
9. [Extending Models at Runtime](#extending-models)
10. [Plugins and Dynamic Schemas](#plugins)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Why-dynamic

Dynamic models are useful when:
- Building admin panels or form generators from database schemas
- Creating models from external API specifications (OpenAPI, JSON Schema)
- Building plugin systems where schema is defined at runtime
- Generating validation models from configuration files
- Creating type-safe wrappers for dynamic data

---

## create-model-basics

### Basic Usage

```python
from pydantic import create_model, Field

# Create a model with fields
UserModel = create_model(
    'User',
    name=(str, Field(..., description="User name")),
    age=(int, Field(ge=0, description="User age")),
    email=(str, Field(..., description="Email address"))
)

# Use it like any Pydantic model
user = UserModel(name="Alice", age=30, email="alice@example.com")
print(user)  # User(name='Alice', age=30, email='alice@example.com')
print(user.model_dump())  # {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}
```

### Field Definition Syntax

```python
# Each field is defined as: (type, default_or_field_info)
# Tuple of (type, FieldInfo) or (type, default_value)

# Required field (use Field(...) or Ellipsis)
create_model('M', name=(str, ...))

# With Field metadata
create_model('M', name=(str, Field(..., min_length=1)))

# With default value
create_model('M', name=(str, "default_name"))

# With default_factory
from pydantic import Field
create_model('M', tags=(list[str], Field(default_factory=list)))
```

### With ConfigDict

```python
from pydantic import create_model, ConfigDict, Field

StrictModel = create_model(
    'StrictModel',
    __config__=ConfigDict(extra='forbid', frozen=True),
    name=(str, ...),
    age=(int, Field(ge=0))
)

m = StrictModel(name="Alice", age=30)
# m.new_field = "error"  # ValidationError — extra='forbid'
```

---

## dynamic-fields

### Building Fields from a Dict

```python
from pydantic import create_model, Field

def build_model_from_schema(schema: dict) -> type:
    """Create a Pydantic model from a JSON Schema-like dict."""
    fields = {}
    for name, props in schema.items():
        field_type = props.get('type', str)
        field_default = props.get('default', ...)
        field_desc = props.get('description', '')

        # Map JSON Schema types to Python types
        type_map = {
            'string': str,
            'integer': int,
            'number': float,
            'boolean': bool,
            'array': list,
            'object': dict,
        }

        python_type = type_map.get(field_type, str)

        fields[name] = (
            python_type,
            Field(default=field_default, description=field_desc)
        )

    return create_model('DynamicModel', **fields)

# Usage
schema = {
    'name': {'type': 'string', 'description': 'Full name'},
    'age': {'type': 'integer', 'description': 'Age in years'},
    'email': {'type': 'string', 'description': 'Email address'},
    'is_active': {'type': 'boolean', 'default': True, 'description': 'Active status'}
}

Model = build_model_from_schema(schema)
instance = Model(name="Alice", age=30, email="alice@x.com")
print(instance)
```

### Fields with Constraints

```python
from pydantic import create_model, Field

def build_validated_model(field_defs: list[dict]) -> type:
    """Create model with field constraints."""
    fields = {}
    for field in field_defs:
        name = field['name']
        python_type = {
            'string': str,
            'integer': int,
            'number': float,
            'boolean': bool
        }[field['type']]

        constraints = {}
        if 'min' in field:
            constraints['ge' if field['type'] != 'string' else 'min_length'] = field['min']
        if 'max' in field:
            constraints['le' if field['type'] != 'string' else 'max_length'] = field['max']
        if 'pattern' in field:
            constraints['pattern'] = field['pattern']

        fields[name] = (python_type, Field(**constraints))

    return create_model('ValidatedModel', **fields)

# Usage
fields = [
    {'name': 'username', 'type': 'string', 'min': 3, 'max': 50, 'pattern': r'^[a-z]+$'},
    {'name': 'age', 'type': 'integer', 'min': 0, 'max': 150},
    {'name': 'score', 'type': 'number', 'min': 0, 'max': 100}
]

Model = build_validated_model(fields)
m = Model(username="alice", age=25, score=95.5)
print(m)
```

---

## type-adapter

`TypeAdapter` provides validation and serialization without creating a full model class.

### Basic Usage

```python
from pydantic import TypeAdapter

# Validate a simple type
ta = TypeAdapter(int)
result = ta.validate_python("42")
print(result)  # 42

# Validate a string
ta = TypeAdapter(str)
result = ta.validate_python(123)
print(result)  # "123"
```

### With Constraints

```python
from pydantic import TypeAdapter, Field
from typing import Annotated

# Constrained integer
PositiveInt = TypeAdapter(Annotated[int, Field(ge=0)])

result = PositiveInt.validate_python(5)
print(result)  # 5

try:
    result = PositiveInt.validate_python(-1)
except Exception as e:
    print(e)  # Input should be greater than or equal to 0
```

### With Complex Types

```python
from pydantic import TypeAdapter
from typing import List

# List of strings
StringList = TypeAdapter(List[str])
result = StringList.validate_python(["a", "b", "c"])
print(result)  # ['a', 'b', 'c']

# Dict with specific types
from typing import Dict
IntDict = TypeAdapter(Dict[str, int])
result = IntDict.validate_python({"a": 1, "b": 2})
print(result)  # {'a': 1, 'b': 2}
```

### Serialization

```python
from pydantic import TypeAdapter
from datetime import datetime

# Serialize datetime
ta = TypeAdapter(datetime)
dt = datetime(2025, 6, 15, 9, 0)

# To Python
python_data = ta.dump_python(dt)
print(python_data)  # datetime(2025, 6, 15, 9, 0)

# To JSON
json_data = ta.dump_json(dt)
print(json_data)  # b'"2025-06-15T09:00:00"'

# From JSON
parsed = ta.validate_json(b'"2025-06-15T09:00:00"')
print(parsed)  # datetime(2025, 6, 15, 9, 0)
```

### JSON Schema Generation

```python
from pydantic import TypeAdapter, Field
from typing import Annotated

PositiveInt = TypeAdapter(Annotated[int, Field(ge=0, le=100)])
schema = PositiveInt.json_schema()
print(schema)  # {'type': 'integer', 'minimum': 0, 'maximum': 100}
```

### TypeAdapter vs BaseModel

```python
# TypeAdapter: For validating standalone types, no schema overhead
from pydantic import TypeAdapter
ta = TypeAdapter(list[int])
result = ta.validate_python([1, 2, 3])

# BaseModel: When you need a named type with fields and schema
from pydantic import BaseModel
class IntList(BaseModel):
    items: list[int]
result = IntList(items=[1, 2, 3])
```

---

## serializer-patterns

### Dynamic Serializer

```python
from pydantic import BaseModel, model_serializer

class DynamicSerializer(BaseModel):
    name: str
    data: dict

    @model_serializer(mode='wrap')
    def custom_serialize(self, default_serializer, info) -> dict:
        data = default_serializer(self)

        # Add computed fields based on context
        if info.context and info.context.get('verbose'):
            data['_type'] = 'DynamicSerializer'
            data['_fields'] = list(data.keys())

        return data

m = DynamicSerializer(name="test", data={"key": "value"})
print(m.model_dump(context={'verbose': True}))
# {'name': 'test', 'data': {'key': 'value'}, '_type': 'DynamicSerializer', '_fields': ['name', 'data']}
```

---

## runtime-generation

### Generating Models from API Responses

```python
from pydantic import create_model, Field
from typing import Any

def model_from_api_response(endpoint: str, response_schema: dict) -> type:
    """Dynamically create a model from an API response schema."""
    fields = {}
    for name, spec in response_schema.items():
        type_map = {
            'string': str,
            'integer': int,
            'number': float,
            'boolean': bool,
            'array': list,
            'object': dict,
            'null': type(None),
        }

        python_type = type_map.get(spec.get('type', 'string'), Any)
        required = spec.get('required', True)

        if not required:
            python_type = python_type | None
            fields[name] = (python_type, Field(default=None))
        else:
            fields[name] = (python_type, Field(...))

    return create_model(f'API_{endpoint}', **fields)

# Usage
response_schema = {
    'id': {'type': 'integer'},
    'name': {'type': 'string'},
    'email': {'type': 'string'},
    'is_active': {'type': 'boolean', 'required': False}
}

UserModel = model_from_api_response('users', response_schema)
user = UserModel(id=1, name="Alice", email="alice@x.com")
print(user)
```

### Generating Models from Database Schema

```python
from pydantic import create_model, Field

def model_from_db_columns(table_name: str, columns: list[dict]) -> type:
    """Create a Pydantic model from database column definitions."""
    fields = {}

    for col in columns:
        # Map DB types to Python types
        type_map = {
            'VARCHAR': str,
            'TEXT': str,
            'INTEGER': int,
            'BIGINT': int,
            'FLOAT': float,
            'DOUBLE': float,
            'BOOLEAN': bool,
            'DATE': str,  # Store as string
            'DATETIME': str,
        }

        python_type = type_map.get(col['type'], str)
        nullable = col.get('nullable', False)

        if nullable:
            python_type = python_type | None
            fields[col['name']] = (python_type, Field(default=None))
        else:
            fields[col['name']] = (python_type, Field(...))

    return create_model(table_name, **fields)

# Usage
columns = [
    {'name': 'id', 'type': 'INTEGER', 'nullable': False},
    {'name': 'name', 'type': 'VARCHAR', 'nullable': False},
    {'name': 'email', 'type': 'VARCHAR', 'nullable': False},
    {'name': 'bio', 'type': 'TEXT', 'nullable': True},
]

User = model_from_db_columns('users', columns)
user = User(id=1, name="Alice", email="alice@x.com", bio=None)
print(user)
```

---

## dynamic-api-schemas

### OpenAPI-Inspired Model Generation

```python
from pydantic import create_model, Field
from typing import Any

def openapi_to_pydantic(openapi_schema: dict) -> dict[str, type]:
    """Convert OpenAPI components/schemas to Pydantic models."""
    models = {}

    for name, schema in openapi_schema.get('components', {}).get('schemas', {}).items():
        fields = {}
        required_fields = set(schema.get('required', []))

        for prop_name, prop_spec in schema.get('properties', {}).items():
            prop_type = prop_spec.get('type', 'string')
            python_type = {
                'string': str,
                'integer': int,
                'number': float,
                'boolean': bool,
                'array': list,
                'object': dict,
            }.get(prop_type, Any)

            if prop_name not in required_fields:
                python_type = python_type | None
                fields[prop_name] = (python_type, Field(default=None, description=prop_spec.get('description', '')))
            else:
                fields[prop_name] = (python_type, Field(..., description=prop_spec.get('description', '')))

        models[name] = create_model(name, **fields)

    return models

# Usage
openapi = {
    'components': {
        'schemas': {
            'User': {
                'required': ['name', 'email'],
                'properties': {
                    'name': {'type': 'string', 'description': 'User name'},
                    'email': {'type': 'string', 'description': 'Email'},
                    'age': {'type': 'integer', 'description': 'Age'}
                }
            }
        }
    }
}

models = openapi_to_pydantic(openapi)
UserModel = models['User']
user = UserModel(name="Alice", email="alice@x.com", age=30)
print(user)
```

---

## model-from-dict

### Converting a Dict to a Model at Runtime

```python
from pydantic import create_model, Field
from typing import Any

def dict_to_model(data: dict, model_name: str = 'DynamicModel') -> type:
    """Create a Pydantic model from a sample data dict."""
    fields = {}
    for key, value in data.items():
        if isinstance(value, bool):
            fields[key] = (bool, ...)
        elif isinstance(value, int):
            fields[key] = (int, ...)
        elif isinstance(value, float):
            fields[key] = (float, ...)
        elif isinstance(value, str):
            fields[key] = (str, ...)
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                # Nested dict — create nested model
                nested = dict_to_model(value[0], f'{key.title()}Item')
                fields[key] = (list[nested], ...)
            else:
                fields[key] = (list[Any], ...)
        elif isinstance(value, dict):
            nested = dict_to_model(value, key.title())
            fields[key] = (nested, ...)
        elif value is None:
            fields[key] = (Any, Field(default=None))
        else:
            fields[key] = (Any, ...)

    return create_model(model_name, **fields)

# Usage
sample = {
    'name': 'Alice',
    'age': 30,
    'scores': [95, 87, 92],
    'address': {
        'street': '123 Main St',
        'city': 'NYC'
    }
}

Model = dict_to_model(sample, 'User')
instance = Model(name="Alice", age=30, scores=[95, 87, 92], address={'street': '123 Main St', 'city': 'NYC'})
print(instance)
```

---

## extending-models

### Adding Fields at Runtime

```python
from pydantic import create_model, Field

def extend_model(base_model: type, new_fields: dict) -> type:
    """Extend an existing model with new fields."""
    existing_fields = {k: (v.annotation, v.default if v.default is not None else ...) for k, v in base_model.model_fields.items()}
    all_fields = {**existing_fields, **new_fields}

    return create_model(
        f'{base_model.__name__}Extended',
        **all_fields
    )

# Usage
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

ExtendedUser = extend_model(User, {
    'email': (str, Field(..., description="Email address")),
    'role': (str, Field(default="user", description="User role"))
})

user = ExtendedUser(name="Alice", age=30, email="alice@x.com")
print(user)  # ExtendedUser(name='Alice', age=30, email='alice@x.com', role='user')
```

### Removing Fields at Runtime

```python
def remove_fields(model: type, field_names: set[str]) -> type:
    """Create a new model without specified fields."""
    fields = {
        k: (v.annotation, v.default if v.default is not None else ...)
        for k, v in model.model_fields.items()
        if k not in field_names
    }
    return create_model(f'{model.__name__}Reduced', **fields)

# Usage
ReducedUser = remove_fields(User, {'age'})
print(ReducedUser.model_fields.keys())  # dict_keys(['name'])
```

---

## plugins

### Plugin System with Dynamic Models

```python
from pydantic import create_model, BaseModel, Field
from typing import Any

class PluginRegistry:
    def __init__(self):
        self._schemas: dict[str, dict] = {}

    def register(self, name: str, fields: dict[str, tuple]):
        """Register a new plugin schema."""
        self._schemas[name] = fields

    def get_model(self, name: str) -> type:
        """Get a Pydantic model for a registered schema."""
        if name not in self._schemas:
            raise ValueError(f"Unknown schema: {name}")
        return create_model(name, **self._schemas[name])

    def validate(self, name: str, data: dict) -> Any:
        """Validate data against a registered schema."""
        model = self.get_model(name)
        return model.model_validate(data)

# Usage
registry = PluginRegistry()

# Register schemas from plugins
registry.register('UserPlugin', {
    'name': (str, Field(..., min_length=1)),
    'email': (str, Field(...)),
    'age': (int, Field(ge=0))
})

registry.register('ProductPlugin', {
    'name': (str, Field(...)),
    'price': (float, Field(gt=0)),
    'quantity': (int, Field(ge=0))
})

# Validate data
user = registry.validate('UserPlugin', {'name': 'Alice', 'email': 'alice@x.com', 'age': 30})
print(user)  # UserPlugin(name='Alice', email='alice@x.com', age=30)

product = registry.validate('ProductPlugin', {'name': 'Widget', 'price': 9.99, 'quantity': 100})
print(product)
```

### Dynamic Schema from Configuration File

```python
import json
from pydantic import create_model, Field
from pathlib import Path

def load_models_from_config(config_path: str) -> dict[str, type]:
    """Load Pydantic models from a JSON configuration file."""
    with open(config_path) as f:
        config = json.load(f)

    models = {}
    for model_name, model_config in config.get('models', {}).items():
        fields = {}
        for field_name, field_def in model_config.get('fields', {}).items():
            python_type = {
                'string': str,
                'integer': int,
                'number': float,
                'boolean': bool
            }.get(field_def.get('type', 'string'), str)

            fields[field_name] = (
                python_type,
                Field(
                    default=field_def.get('default', ...),
                    description=field_def.get('description', '')
                )
            )

        models[model_name] = create_model(model_name, **fields)

    return models
```

---

## Best Practices

### 1. Cache Dynamic Models

```python
# BAD — creates a new model class every time
def process(data: dict):
    Model = create_model('Dynamic', **fields)  # New class each call
    return Model.model_validate(data)

# GOOD — cache models
_model_cache: dict[str, type] = {}

def get_model(name: str, fields: dict) -> type:
    if name not in _model_cache:
        _model_cache[name] = create_model(name, **fields)
    return _model_cache[name]
```

### 2. Use TypeAdapter for Simple Validation

```python
# For validating standalone types, TypeAdapter is simpler
from pydantic import TypeAdapter

ta = TypeAdapter(list[int])
result = ta.validate_python([1, 2, 3])
```

### 3. Validate Schema Definitions

```python
# Always validate that your dynamic fields are correct
def safe_create_model(name: str, fields: dict) -> type:
    # Validate field definitions before creating model
    for field_name, (field_type, field_info) in fields.items():
        if not isinstance(field_type, type):
            raise ValueError(f"Invalid type for {field_name}: {field_type}")
    return create_model(name, **fields)
```

### 4. Use model_rebuild for Forward References

```python
# When creating recursive dynamic models
def create_tree_model(node_type: str = 'TreeNode') -> type:
    Model = create_model(node_type, value=(str, ...))
    # Add self-reference after creation
    Model.model_rebuild()
    return Model
```

### 5. Document Dynamic Models

```python
# Add descriptions to dynamic fields
Model = create_model(
    'User',
    name=(str, Field(..., description="User's full name")),
    age=(int, Field(..., ge=0, description="Age in years"))
)

# The schema will include these descriptions
print(Model.model_json_schema())
```

---

## Interview Questions

### Q1: When would you use create_model() over a regular class definition?

**Answer**: When the model's schema isn't known at compile time — e.g., building admin panels from database schemas, generating models from API specs, or creating models from configuration files. Regular classes are preferred when the schema is fixed.

---

### Q2: What is TypeAdapter and how does it differ from BaseModel?

**Answer**: `TypeAdapter` validates and serializes standalone types without creating a model class. It's simpler and has less overhead. Use it when you need to validate a single value (like `list[int]` or `str`) rather than a complex structure with named fields.

---

### Q3: How do you add constraints to dynamically created fields?

**Answer**: Use `Field()` with constraint parameters:

```python
fields = {
    'age': (int, Field(ge=0, le=150)),
    'name': (str, Field(min_length=1, max_length=100))
}
Model = create_model('User', **fields)
```

---

### Q4: Can you create nested dynamic models?

**Answer**: Yes, create inner models first and reference them:

```python
AddressModel = create_model('Address', street=(str, ...), city=(str, ...))
UserModel = create_model('User', name=(str, ...), address=(AddressModel, ...))
```

---

### Q5: How do you cache dynamic models?

**Answer**: Store created models in a dict keyed by their name or schema hash:

```python
cache: dict[str, type] = {}
if name not in cache:
    cache[name] = create_model(name, **fields)
return cache[name]
```

---

### Q6: What are the performance implications of dynamic models?

**Answer**: Creating a dynamic model has overhead (model class creation, schema compilation). Caching models mitigates this. For validation-only use cases, `TypeAdapter` is faster than creating a full `BaseModel`.

---

### Q7: How do you handle recursive dynamic models?

**Answer**: Create the model first, then call `model_rebuild()` to resolve forward references:

```python
Tree = create_model('Tree', value=(str, ...))
Tree.model_rebuild()
```

---

### Q8: Can you dynamically add fields to an existing model?

**Answer**: Not directly — Pydantic models are immutable after creation. But you can create a new model that includes all fields from the original plus new ones using `create_model()`.

---

### Q9: How do you generate models from JSON Schema?

**Answer**: Parse the JSON Schema, extract properties and types, map JSON Schema types to Python types, and use `create_model()` with the extracted fields. Handle `$ref` by resolving references first.

---

### Q10: What is the advantage of TypeAdapter over json.loads()?

**Answer**: `TypeAdapter` provides **type-safe validation and parsing** — it validates the data against the type constraints, coerces types when appropriate, and raises detailed errors. `json.loads()` only parses JSON without any validation.

---
