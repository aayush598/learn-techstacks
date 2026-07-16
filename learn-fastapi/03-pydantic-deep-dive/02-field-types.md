# Pydantic Field Types — The Complete Reference

## Table of Contents

1. [Primitive Types](#primitive-types)
2. [String Types and Validators](#string-types)
3. [Numeric Types](#numeric-types)
4. [Boolean Type](#boolean-type)
5. [Bytes Type](#bytes-type)
6. [Date and Time Types](#datetime-types)
7. [UUID Types](#uuid-types)
8. [URL and Network Types](#url-network-types)
9. [Email and Secret Types](#email-secret-types)
10. [Payment and Special Types](#payment-special-types)
11. [Collection Types](#collection-types)
12. [Constrained Types (conint, constr, etc.)](#constrained-types)
13. [Literal and Enum Types](#literal-enum-types)
14. [Annotated with Constraints](#annotated-constraints)
15. [Discriminated Unions](#discriminated-unions)
16. [Best Practices](#best-practices)
17. [Interview Questions](#interview-questions)

---

## Primitive Types

### str

```python
from pydantic import BaseModel

class StringExample(BaseModel):
    name: str
    empty: str = ""
    with_whitespace: str = "  hello  "

m = StringExample(name="Alice", with_whitespace="  hello  ")
print(m.with_whitespace)  # "  hello  " — whitespace preserved by default

# To strip whitespace automatically:
from pydantic import BaseModel, ConfigDict

class StrippedModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str

m = StrippedModel(name="  Alice  ")
print(m.name)  # "Alice"
```

### int

```python
class IntExample(BaseModel):
    count: int
    positive: int = 0

# Auto-coercion from string
m = IntExample(count="42", positive="10")
print(m.count)      # 42 (int)
print(type(m.count)) # <class 'int'>

# Float truncation (not coercion — truncates!)
m = IntExample(count=42.9)
print(m.count)  # 42 — truncated, not rounded

# Hex, octal, binary strings
m = IntExample(count="0xFF")
print(m.count)  # 255

m = IntExample(count="0o10")
print(m.count)  # 8

m = IntExample(count="0b1100")
print(m.count)  # 12
```

### float

```python
class FloatExample(BaseModel):
    score: float
    pi: float = 3.14159

# Auto-coercion from string
m = FloatExample(score="95.5")
print(m.score)  # 95.5

# Float from int
m = FloatExample(score=100)
print(m.score)  # 100.0

# Special float values
import math

class SpecialFloat(BaseModel):
    value: float

m = SpecialFloat(value="inf")
print(m.value)  # inf

m = SpecialFloat(value="-inf")
print(m.value)  # -inf

m = SpecialFloat(value="nan")
print(math.isnan(m.value))  # True
```

### bool

```python
class BoolExample(BaseModel):
    active: bool
    verified: bool = False

# Truthy/Falsy coercion
m = BoolExample(active=1)
print(m.active)  # True

m = BoolExample(active=0)
print(m.active)  # False

m = BoolExample(active="yes")
print(m.active)  # True

m = BoolExample(active="")
print(m.active)  # False

m = BoolExample(active=None)
print(m.active)  # False

# List of truthy values (for int/str, Pydantic is strict about bool coercion)
# Only True/False, 0/1, and "true"/"false" are accepted
# "yes" → True, "no" → False are also accepted
```

### bytes

```python
class BytesExample(BaseModel):
    data: bytes
    raw: bytes = b""

# From string (encodes to UTF-8)
m = BytesExample(data="hello")
print(m.data)      # b'hello'
print(type(m.data)) # <class 'bytes'>

# From int list
m = BytesExample(data=[72, 101, 108, 108, 111])
print(m.data)  # b'Hello'

# From base64
m = BytesExample(data="aGVsbG8=")
print(m.data)  # b'hello'
```

---

## Date and Time Types

### datetime

```python
from datetime import datetime
from pydantic import BaseModel

class Event(BaseModel):
    created_at: datetime
    updated_at: datetime | None = None

# From ISO format string
event = Event(created_at="2025-06-15T14:30:00")
print(event.created_at)        # 2025-06-15 14:30:00
print(type(event.created_at))  # <class 'datetime.datetime'>

# From datetime object
event = Event(created_at=datetime(2025, 6, 15, 14, 30, 0))
print(event.created_at)  # 2025-06-15 14:30:00

# From date + time (separated)
event = Event(created_at="2025-06-15 14:30:00")
print(event.created_at)  # 2025-06-15 14:30:00

# With timezone
event = Event(created_at="2025-06-15T14:30:00+05:30")
print(event.created_at)  # 2025-06-15 14:30:00+05:30
```

### date

```python
from datetime import date
from pydantic import BaseModel

class Birthday(BaseModel):
    birth_date: date

# From ISO format
b = Birthday(birth_date="1990-05-15")
print(b.birth_date)        # 1990-05-15
print(type(b.birth_date))  # <class 'datetime.date'>

# From date object
b = Birthday(birth_date=date(1990, 5, 15))
print(b.birth_date)  # 1990-05-15
```

### time

```python
from datetime import time
from pydantic import BaseModel

class Schedule(BaseModel):
    alarm_time: time

s = Schedule(alarm_time="07:30:00")
print(s.alarm_time)        # 07:30:00
print(type(s.alarm_time))  # <class 'datetime.time'>

s = Schedule(alarm_time="07:30")
print(s.alarm_time)  # 07:30:00

s = Schedule(alarm_time=time(7, 30, 0))
print(s.alarm_time)  # 07:30:00
```

### timedelta

```python
from datetime import timedelta
from pydantic import BaseModel

class Duration(BaseModel):
    timeout: timedelta
    interval: timedelta = timedelta(seconds=30)

# From seconds
d = Duration(timeout=3600)
print(d.timeout)  # 1:00:00:00 (1 day)

# From string
d = Duration(timeout="1:00:00")
print(d.timeout)  # 1:00:00 (1 hour)

d = Duration(timeout="2h30m")
print(d.timeout)  # 2:30:00

d = Duration(timeout="P1DT12H")  # ISO 8601 duration
print(d.timeout)  # 1 day, 12:00:00

# From timedelta object
d = Duration(timeout=timedelta(hours=2, minutes=30))
print(d.timeout)  # 2:30:00
```

---

## UUID Types

```python
import uuid
from pydantic import BaseModel

class Item(BaseModel):
    id: uuid.UUID

# From string
item = Item(id="12345678-1234-5678-1234-567812345678")
print(item.id)        # 12345678-1234-5678-1234-567812345678
print(type(item.id))  # <class 'uuid.UUID'>

# Without hyphens
item = Item(id="12345678123456781234567812345678")
print(item.id)  # 12345678-1234-5678-1234-567812345678

# From UUID object
item = Item(id=uuid.uuid4())
print(item.id)  # Random UUID

# Hex only
item = Item(id="12345678123456781234567812345678")
```

---

## URL and Network Types

### HttpUrl

```python
from pydantic import BaseModel, HttpUrl

class Website(BaseModel):
    url: HttpUrl

w = Website(url="https://example.com")
print(w.url)        # https://example.com/
print(type(w.url))  # <class 'pydantic.networks.HttpUrl'>

# Validates URL scheme (http/https)
try:
    w = Website(url="ftp://example.com")
except Exception as e:
    print(e)  # URL scheme should be 'http' or 'https'
```

### AnyHttpUrl

```python
from pydantic import BaseModel, AnyHttpUrl

class AnySite(BaseModel):
    url: AnyHttpUrl

# Accepts both http and https
s = AnySite(url="http://example.com")
s = AnySite(url="https://example.com")
```

### IPvAnyAddress

```python
from pydantic import BaseModel, IPvAnyAddress

class Server(BaseModel):
    ip: IPvAnyAddress

s = Server(ip="192.168.1.1")
print(s.ip)        # 192.168.1.1
print(type(s.ip))  # <class 'ipaddress.IPv4Address'>

# IPv6
s = Server(ip="::1")
print(s.ip)  # ::1

# Also accepts integers
s = Server(ip=3232235777)
print(s.ip)  # 192.168.1.1
```

### IPvAnyNetwork

```python
from pydantic import BaseModel, IPvAnyNetwork

class Subnet(BaseModel):
    network: IPvAnyNetwork

s = Subnet(network="192.168.1.0/24")
print(s.network)        # 192.168.1.0/24
print(type(s.network))  # <class 'ipaddress.IPv4Network'>
```

### NameStr

```python
from pydantic import BaseModel, NameStr

class User(BaseModel):
    name: NameStr  # Validates that the string looks like a person's name

# Accepts alphabetic names
u = User(name="Alice Smith")
print(u.name)  # "Alice Smith"

# Rejects purely numeric or special character names
try:
    u = User(name="123")
except Exception as e:
    print(e)  # Name should contain at least two characters
```

---

## Email and Secret Types

### EmailStr

```python
from pydantic import BaseModel, EmailStr

class Contact(BaseModel):
    email: EmailStr

c = Contact(email="user@example.com")
print(c.email)  # "user@example.com"

# Validates email format
try:
    c = Contact(email="not-an-email")
except Exception as e:
    print(e)  # value is not a valid email address

# Requires email-validator package:
# pip install pydantic[email]
# or: pip install email-validator
```

### SecretStr

```python
from pydantic import BaseModel, SecretStr

class Login(BaseModel):
    username: str
    password: SecretStr

login = Login(username="alice", password="s3cret_p@ss")

# Direct access returns SecretStr object, NOT the string
print(login.password)           # ********** (masked in repr)
print(login.password.get_secret_value())  # "s3cret_p@ss"

# When serialized, secret values are hidden
print(login.model_dump())  # {'username': 'alice', 'password': 'SecretStr('**********')'}

# To include secret value in dump:
print(login.model_dump(exclude_unset=True))
# Still shows masked version

# Use get_secret_value() to access the actual value
actual_password = login.password.get_secret_value()
print(actual_password)  # "s3cret_p@ss"
```

### SecretBytes

```python
from pydantic import BaseModel, SecretBytes

class APIKey(BaseModel):
    key: SecretBytes

api = APIKey(key="my-secret-api-key-123")
print(api.key)                          # **********
print(api.key.get_secret_value())       # b'my-secret-api-key-123'
```

---

## Payment and Special Types

### PaymentCardNumber

```python
from pydantic import BaseModel, PaymentCardNumber

class Payment(BaseModel):
    card: PaymentCardNumber

# Validates card number format and Luhn check
p = Payment(card="4111111111111111")
print(p.card)           # 4111111111111111
print(p.card.brand)     # visa
print(p.card.card_brand)  # CardBrand.visa
print(p.card.card_masked)  # 411111******1111
print(p.card.card_number)  # 4111111111111111

# Invalid card number (fails Luhn check)
try:
    p = Payment(card="1234567890123456")
except Exception as e:
    print(e)  # Card number is not valid (Luhn check fails)

# Card type detection
p = Payment(card="5500000000000004")  # Mastercard
print(p.card.card_brand)  # CardBrand.mastercard
```

---

## Collection Types

### List

```python
from typing import List
from pydantic import BaseModel

class ShoppingList(BaseModel):
    items: List[str]
    quantities: list[int] = []

# From list
sl = ShoppingList(items=["apple", "banana", "cherry"])
print(sl.items)  # ['apple', 'banana', 'cherry']

# From tuple (auto-converted)
sl = ShoppingList(items=("apple", "banana"))
print(sl.items)  # ['apple', 'banana']

# Nested lists
class Matrix(BaseModel):
    data: list[list[int]]

m = Matrix(data=[[1, 2, 3], [4, 5, 6]])
print(m.data)  # [[1, 2, 3], [4, 5, 6]]
```

### Dict

```python
from typing import Dict
from pydantic import BaseModel

class Metadata(BaseModel):
    tags: Dict[str, int]
    config: dict[str, str | int] = {}

m = Metadata(tags={"python": 5, "pydantic": 3})
print(m.tags)  # {'python': 5, 'pydantic': 3}

# Nested dicts
class Config(BaseModel):
    nested: dict[str, dict[str, int]]

c = Config(nested={"a": {"x": 1}, "b": {"y": 2}})
```

### Set

```python
from typing import Set
from pydantic import BaseModel

class Tags(BaseModel):
    labels: Set[str]

t = Tags(labels={"python", "fastapi", "pydantic", "python"})
print(t.labels)  # {'python', 'fastapi', 'pydantic'} — duplicates removed
```

### Tuple

```python
from typing import Tuple
from pydantic import BaseModel

class Coordinate(BaseModel):
    point: Tuple[float, float]

c = Coordinate(point=(3.14, 2.71))
print(c.point)  # (3.14, 2.71)

# Fixed-length tuple
class RGB(BaseModel):
    color: Tuple[int, int, int]

rgb = RGB(color=(255, 128, 0))
print(rgb.color)  # (255, 128, 0)

# Variable-length tuple
class Flexible(BaseModel):
    values: Tuple[int, ...]

f = Flexible(values=(1, 2, 3, 4, 5))
print(f.values)  # (1, 2, 3, 4, 5)
```

### FrozenSet

```python
from typing import FrozenSet
from pydantic import BaseModel

class ImmutableTags(BaseModel):
    labels: FrozenSet[str]

it = ImmutableTags(labels={"a", "b", "c"})
# it.labels.add("d")  # AttributeError — frozen set is immutable
```

### Deque

```python
from collections import deque
from pydantic import BaseModel
from typing import Deque

class Queue(BaseModel):
    items: Deque[int]

q = Queue(items=deque([1, 2, 3]))
print(q.items)  # deque([1, 2, 3])
```

### Sequence

```python
from typing import Sequence
from pydantic import BaseModel

class FlexibleList(BaseModel):
    items: Sequence[str]  # Accepts list, tuple, or any sequence

fl = FlexibleList(items=("a", "b"))  # Tuple is OK
fl = FlexibleList(items=["a", "b"])  # List is also OK
```

### Optional and Union

```python
from typing import Optional, Union
from pydantic import BaseModel

class Flexible(BaseModel):
    value: Optional[str] = None        # str | None
    id: Union[int, str] = 0            # int | str
    data: int | str | None = None      # Python 3.10+ syntax

f = Flexible(value=None, id="abc", data=42)
print(f.value)  # None
print(f.id)     # "abc"
print(f.data)   # 42
```

---

## Constrained Types

Constrained types let you apply validation constraints directly to type annotations.

### conint

```python
from pydantic import BaseModel
from pydantic.types import conint

class PositiveIntModel(BaseModel):
    # Constrained integer: minimum 0, maximum 100
    score: conint(ge=0, le=100)
    # Strict integer: must be exactly int, no coercion
    strict_count: conint(strict=True)
    # Multiple of
    dozen: conint(multiple_of=12)

m = PositiveIntModel(score=50, strict_count=42, dozen=24)
print(m.score)        # 50
print(m.strict_count) # 42
print(m.dozen)        # 24

# Invalid
try:
    m = PositiveIntModel(score=150, strict_count=42, dozen=10)
except Exception as e:
    print(e)  # score: ensure this value is less than or equal to 100
    # dozen: ensure this value is a multiple of 12
```

### constr

```python
from pydantic import BaseModel
from pydantic.types import constr

class UsernameModel(BaseModel):
    # Constrained string
    username: constr(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')
    # Strict string (no coercion from bytes, etc.)
    name: constr(strict=True)

m = UsernameModel(username="alice_123", name="Alice")
print(m.username)  # "alice_123"

# Invalid
try:
    m = UsernameModel(username="ab", name="Alice")  # Too short
except Exception as e:
    print(e)  # String should have at least 3 characters

try:
    m = UsernameModel(username="alice@#$", name="Alice")  # Invalid pattern
except Exception as e:
    print(e)  # String should match pattern '^[a-zA-Z0-9_]+$'
```

### confloat

```python
from pydantic import BaseModel
from pydantic.types import confloat

class PriceModel(BaseModel):
    price: confloat(gt=0, le=1000000)
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)

m = PriceModel(price=29.99, latitude=40.7128, longitude=-74.0060)
```

### conbytes

```python
from pydantic import BaseModel
from pydantic.types import conbytes

class HashModel(BaseModel):
    sha256: conbytes(min_length=32, max_length=32)

m = HashModel(sha256=b"0" * 32)
print(len(m.sha256))  # 32
```

### conlist

```python
from pydantic import BaseModel
from pydantic.types import conlist

class ListModel(BaseModel):
    # List with min 1 item, max 10 items, each item is int with gt=0
    scores: conlist(int, min_length=1, max_length=10)

m = ListModel(scores=[1, 2, 3, 4, 5])
print(m.scores)  # [1, 2, 3, 4, 5]

try:
    m = ListModel(scores=[])  # Empty list
except Exception as e:
    print(e)  # List should have at least 1 item

try:
    m = ListModel(scores=[0])  # Item must be > 0
except Exception as e:
    print(e)  # Input should be greater than 0
```

### conset

```python
from pydantic import BaseModel
from pydantic.types import conset

class SetModel(BaseModel):
    tags: conset(str, min_length=1, max_length=5)

m = SetModel(tags={"python", "fastapi"})
print(m.tags)  # {'python', 'fastapi'}
```

---

## Literal and Enum Types

### Literal

```python
from typing import Literal
from pydantic import BaseModel

class Direction(BaseModel):
    heading: Literal["north", "south", "east", "west"]

d = Direction(heading="north")
print(d.heading)  # "north"

try:
    d = Direction(heading="up")
except Exception as e:
    print(e)  # Input should be 'north', 'south', 'east' or 'west'
```

### Enum

```python
from enum import Enum
from pydantic import BaseModel, ConfigDict

class Color(str, Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

class Painting(BaseModel):
    model_config = ConfigDict(use_enum_values=True)  # Store enum value, not enum object

    color: Color

p = Painting(color="red")
print(p.color)        # "red" (string, because use_enum_values=True)
print(type(p.color))  # <class 'str'>

# Without use_enum_values
class Painting2(BaseModel):
    color: Color

p2 = Painting2(color="red")
print(p2.color)        # Color.RED (enum object)
print(p2.color.value)  # "red"
```

### IntEnum and Flag

```python
from enum import IntEnum, Flag, auto

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

class Task(BaseModel):
    priority: Priority
    permissions: Permission

t = Task(priority=2, permissions=Permission.READ | Permission.WRITE)
print(t.priority)  # Priority.MEDIUM (2)
```

---

## Annotated with Constraints

The modern way to apply constraints using `Annotated`:

```python
from typing import Annotated
from pydantic import BaseModel, Field

# Using Annotated with Field constraints
class UserModel(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    age: Annotated[int, Field(ge=0, le=150)]
    score: Annotated[float, Field(ge=0.0, le=100.0)]
    email: Annotated[str, Field(pattern=r'^[\w.-]+@[\w.-]+\.\w+$')]

m = UserModel(name="Alice", age=30, score=95.5, email="alice@example.com")
```

### Annotated with Multiple Validators

```python
from typing import Annotated
from pydantic import BaseModel, Field, AfterValidator

def validate_even(v: int) -> int:
    if v % 2 != 0:
        raise ValueError("Must be even")
    return v

class Config(BaseModel):
    port: Annotated[int, Field(ge=1024, le=65535)]
    even_number: Annotated[int, AfterValidator(validate_even)]

m = Config(port=8080, even_number=42)
```

### Annotated with Specific Types

```python
from typing import Annotated
from pydantic import BaseModel, Field
from annotated_types import Ge, Le, Gt, Lt

class Measurement(BaseModel):
    # Using annotated_types for cleaner syntax
    width: Annotated[float, Gt(0), Le(1000)]
    height: Annotated[float, Gt(0), Le(1000)]
    weight: Annotated[float, Ge(0)]

m = Measurement(width=10.5, height=20.3, weight=5.0)
```

---

## Discriminated Unions

Discriminated unions use a "discriminator" field to determine which model to use for validation.

```python
from typing import Literal, Union, Annotated
from pydantic import BaseModel, Field

class Cat(BaseModel):
    type: Literal["cat"]
    meow_volume: int

class Dog(BaseModel):
    type: Literal["dog"]
    bark_volume: int

class Fish(BaseModel):
    type: Literal["fish"]
    swim_speed: float

# Discriminated union using Annotated + Field(discriminator=...)
class Pet(BaseModel):
    name: str
    pet: Annotated[
        Union[Cat, Dog, Fish],
        Field(discriminator="type")
    ]

# Valid — Pydantic knows which model to use based on 'type'
pet = Pet(name="Whiskers", pet={"type": "cat", "meow_volume": 5})
print(pet.pet)  # Cat(type='cat', meow_volume=5)

pet = Pet(name="Rex", pet={"type": "dog", "bark_volume": 8})
print(pet.pet)  # Dog(type='dog', bark_volume=8)

# Invalid — wrong discriminator value
try:
    pet = Pet(name="Nemo", pet={"type": "bird", "wingspan": 30})
except Exception as e:
    print(e)  # Input should be 'cat', 'dog' or 'fish'

# Invalid — missing required field for matched type
try:
    pet = Pet(name="Nemo", pet={"type": "fish"})
except Exception as e:
    print(e)  # Field required [type=missing ...]
```

### Nested Discriminated Unions

```python
from typing import Literal, Union, Annotated, List
from pydantic import BaseModel, Field

class TextMessage(BaseModel):
    type: Literal["text"]
    content: str

class ImageMessage(BaseModel):
    type: Literal["image"]
    url: str
    width: int
    height: int

class VideoMessage(BaseModel):
    type: Literal["video"]
    url: str
    duration: float

Message = Annotated[
    Union[TextMessage, ImageMessage, VideoMessage],
    Field(discriminator="type")
]

class Chat(BaseModel):
    messages: List[Message]

chat = Chat(messages=[
    {"type": "text", "content": "Hello!"},
    {"type": "image", "url": "https://example.com/img.jpg", "width": 800, "height": 600},
    {"type": "video", "url": "https://example.com/vid.mp4", "duration": 30.5},
])

for msg in chat.messages:
    if isinstance(msg, TextMessage):
        print(f"Text: {msg.content}")
    elif isinstance(msg, ImageMessage):
        print(f"Image: {msg.url} ({msg.width}x{msg.height})")
    elif isinstance(msg, VideoMessage):
        print(f"Video: {msg.url} ({msg.duration}s)")
```

---

## Best Practices

### 1. Use Modern Union Syntax (Python 3.10+)

```python
# PREFERRED (Python 3.10+)
def process(value: int | str | None) -> str | None:
    ...

# ALSO FINE (pre-3.10)
from typing import Union, Optional
def process(value: Union[int, str, None]) -> Optional[str]:
    ...
```

### 2. Prefer Annotated Over conint/constr

```python
from typing import Annotated
from pydantic import Field

# MODERN — preferred
class User(BaseModel):
    age: Annotated[int, Field(ge=0, le=150)]

# LEGACY — still works but less readable
from pydantic.types import conint
class User(BaseModel):
    age: conint(ge=0, le=150)
```

### 3. Use SecretStr for Sensitive Data

```python
from pydantic import BaseModel, SecretStr

class APIClient(BaseModel):
    api_key: SecretStr
    database_password: SecretStr

# The actual values are never printed in logs or repr
client = APIClient(api_key="sk-123", database_password="p@ss")
print(client)  # api_key=SecretStr('**********') ...
```

### 4. Use Discriminated Unions for Polymorphic Data

```python
# GOOD — discriminated union (fast, clear errors)
class Shape(BaseModel):
    kind: Annotated[
        Union[Circle, Rectangle, Triangle],
        Field(discriminator="kind")
    ]

# BAD — plain union (slower, less clear errors)
class Shape(BaseModel):
    kind: Union[Circle, Rectangle, Triangle]  # Tries each one sequentially
```

### 5. Use Literal for Fixed Sets of Values

```python
from typing import Literal

# GOOD — clear, validates at runtime
class Config(BaseModel):
    log_level: Literal["debug", "info", "warning", "error"]

# ALSO GOOD — uses Enum
class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class Config(BaseModel):
    log_level: LogLevel
```

---

## Interview Questions

### Q1: What is the difference between `str` and `EmailStr`?

**Answer**: `str` accepts any string. `EmailStr` validates that the string matches an email address format (requires `email-validator` package). `EmailStr` also normalizes the email (lowercase local part, etc.).

---

### Q2: When would you use `SecretStr`?

**Answer**: `SecretStr` is for sensitive data like passwords, API keys, and tokens. When the model is printed (repr), serialized to dict, or logged, the actual value is masked with `**********`. You access the real value only with `get_secret_value()`. This prevents accidental logging of secrets.

---

### Q3: What is the difference between `conint(ge=0)` and `Annotated[int, Field(ge=0)]`?

**Answer**: Functionally equivalent. `conint(ge=0)` is a constrained type (legacy approach from Pydantic V1). `Annotated[int, Field(ge=0)]` is the modern approach using Python's `Annotated` type hint. The `Annotated` approach is preferred because it's more readable, composable, and standard Python.

---

### Q4: How do discriminated unions work?

**Answer**: A discriminated union uses a **discriminator field** (a field with `Literal` type) to determine which model to validate against. Instead of trying each model in the union sequentially (slow), Pydantic reads the discriminator value first and jumps directly to the matching model. This is faster and produces clearer error messages.

---

### Q5: What is `model_config = ConfigDict(use_enum_values=True)`?

**Answer**: When `use_enum_values=True`, Pydantic stores the **value** of the enum member instead of the enum member itself. For example, if `Color.RED` has value `"red"`, the model stores `"red"` (string) instead of `Color.RED` (enum object). This makes serialization simpler but you lose enum methods.

---

### Q6: Can you use `Literal` with non-string values?

**Answer**: Yes. `Literal` works with any hashable type:
- `Literal[1, 2, 3]` — integers
- `Literal[True, False]` — booleans
- `Literal["a", "b", "c"]` — strings
- `Literal[1, "one", True]` — mixed types

---

### Q7: What is `PaymentCardNumber` and how does it validate?

**Answer**: `PaymentCardNumber` validates credit card numbers using the **Luhn algorithm**. It also detects the card brand (Visa, Mastercard, Amex, etc.) from the number prefix. It stores the number with a masked representation for safety.

---

### Q8: How do you handle nullable fields in Pydantic V2?

**Answer**: Use `str | None = None` (Python 3.10+) or `Optional[str] = None` (older). The `= None` default is required to make the field truly optional (accepts `None`). Without a default, the field is required even if the type annotation includes `None`.

---

### Q9: What is the difference between `list`, `List`, `Sequence`, and `tuple` in Pydantic?

**Answer**:
- `list[T]` / `List[T]`: Accepts any list-like input, validates each element
- `Sequence[T]`: Accepts any sequence type (list, tuple, deque, etc.)
- `tuple[T, ...]`: Variable-length tuple of T
- `tuple[T1, T2]`: Fixed-length tuple with specific types

---

### Q10: How does Pydantic handle `confloat(float('nan'))` and `confloat(float('inf'))`?

**Answer**: By default, Pydantic accepts `nan`, `inf`, and `-inf` for float fields. To reject them, use `ConfigDict(ser_json_inf_nan='constants')` or apply constraints like `gt=float('-inf')`. The `allow_inf_nan` config option (default `True`) controls this behavior.

---

### Q11: What is `NameStr` and when would you use it?

**Answer**: `NameStr` validates that a string looks like a person's name — it must contain at least two characters and cannot be purely numeric. Use it for form validation where you expect a human name, but be aware it's a basic heuristic and won't work for all cultures.

---

### Q12: Can you combine `conint` with `Annotated`?

**Answer**: You can, but it's redundant. `Annotated[conint(ge=0), Field(le=100)]` works but mixes two approaches. Prefer one or the other: either `Annotated[int, Field(ge=0, le=100)]` or `conint(ge=0, le=100)`.

---
