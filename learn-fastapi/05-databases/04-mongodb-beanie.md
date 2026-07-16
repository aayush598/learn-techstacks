# MongoDB with Beanie ODM and FastAPI

## Table of Contents

1. [Beanie ODM Setup](#beanie-odm-setup)
2. [Document Models](#document-models)
3. [CRUD Operations](#crud-operations)
4. [MongoDB Relationships](#mongodb-relationships)
5. [Indexing](#indexing)
6. [Aggregation](#aggregation)
7. [Beanie with FastAPI Lifespan](#beanie-with-fastapi-lifespan)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## Beanie ODM Setup

### What is Beanie?

Beanie is an asynchronous Python ODM (Object Document Mapper) for MongoDB, built on top of Motor (async MongoDB driver) and Pydantic. It provides a clean, Pythonic interface for MongoDB operations.

### Installation

```bash
pip install beanie
# Also need motor (installed automatically)
pip install motor
```

### Project Structure

```
myapp/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py          # Beanie initialization
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   └── routers/
│       └── ...
```

### Database Connection

```python
# db.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models.user import User
from .models.item import Item

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "myapp"

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]

async def init_db():
    await init_beanie(
        database=database,
        document_models=[User, Item],
    )
```

### Application Startup

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Beanie
    await init_db()
    yield
    # Cleanup
    client.close()

app = FastAPI(lifespan=lifespan)
```

---

## Document Models

### Basic Document

```python
from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class User(Document):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=255)
    hashed_password: str
    is_active: bool = True
    role: str = "user"
    tags: list[str] = []
    metadata: dict = {}
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"  # Collection name
        use_state_management = True  # Track changes

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
```

### Document with Nested Models

```python
from pydantic import BaseModel
from beanie import Document
from typing import Optional

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "US"

class UserProfile(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    address: Optional[Address] = None

class User(Document):
    name: str
    email: str
    profile: UserProfile = UserProfile()

    class Settings:
        name = "users"
```

### Document with Custom ID

```python
from beanie import Document
from pydantic import Field

class Product(Document):
    # Custom ID field
    sku: str = Field(..., alias="_id")
    name: str
    price: float

    class Settings:
        name = "products"

# Or use default ObjectId
class Order(Document):
    # Uses default MongoDB ObjectId
    order_number: str
    total: float

    class Settings:
        name = "orders"
```

---

## CRUD Operations

### Create

```python
from beanie import Document

class User(Document):
    name: str
    email: str

# Create single document
user = User(name="Alice", email="alice@example.com")
await user.insert()

# Create with class method
user = await User(name="Bob", email="bob@example.com").insert()

# Create many
users = [
    User(name=f"User {i}", email=f"user{i}@example.com")
    for i in range(100)
]
await User.insert_many(users)
```

### Read

```python
# Find by ID
user = await User.get(user_id)

# Find one
user = await User.find_one(User.email == "alice@example.com")

# Find many
users = await User.find(User.is_active == True).to_list()

# Find with pagination
users = await User.find(
    User.is_active == True
).skip(0).limit(20).to_list()

# Find with sorting
users = await User.find(
    User.is_active == True
).sort(User.created_at.desc()).to_list()

# Find with projection
users = await User.find(
    User.is_active == True,
    projection_model=UserListItem,  # Pydantic model for output
).to_list()

# Count
count = await User.find(User.is_active == True).count()

# Check existence
exists = await User.find_one(User.email == "alice@example.com") is not None
```

### Update

```python
# Update single document
user = await User.get(user_id)
user.name = "New Name"
await user.save()

# Update with set
await User.find_one(User.email == "alice@example.com").update(
    {"$set": {"name": "Alice Updated"}}
)

# Update many
await User.find(User.is_active == False).update(
    {"$set": {"is_active": True}}
)

# Upsert
await User.find_one(User.email == "alice@example.com").upsert(
    {"$set": {"name": "Alice", "email": "alice@example.com"}},
)

# Atomic increment
await User.find_one(User._id == user_id).update(
    {"$inc": {"login_count": 1}}
)
```

### Delete

```python
# Delete single document
user = await User.get(user_id)
await user.delete()

# Delete one
await User.find_one(User.email == "alice@example.com").delete()

# Delete many
await User.find(User.is_active == False).delete()

# Delete all
await User.delete_all()
```

---

## MongoDB Relationships

### Document References

```python
from beanie import Document, Link
from typing import Optional

class Team(Document):
    name: str
    members: list[Link["User"]] = []

class User(Document):
    name: str
    team: Optional[Link[Team]] = None

    class Settings:
        name = "users"

# Create with reference
team = Team(name="Avengers")
await team.insert()

user = User(name="Iron Man", team=team)
await user.insert()

# Fetch with reference (eager loading)
user = await User.get(user_id)
await user.fetch_link(User.team)  # team is now populated
print(user.team.name)  # "Avengers"

# Find with references
users = await User.find(
    User.team == team.id
).to_list()
```

### Embedding (Denormalization)

```python
from pydantic import BaseModel
from beanie import Document
from datetime import datetime

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    price: float

class Order(Document):
    user_id: str
    items: list[OrderItem] = []
    total: float
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "orders"

# Create with embedded documents
order = Order(
    user_id="user123",
    items=[
        OrderItem(product_name="Widget", quantity=2, price=9.99),
        OrderItem(product_name="Gadget", quantity=1, price=24.99),
    ],
    total=44.97,
)
await order.insert()
```

---

## Indexing

### Single Field Index

```python
from beanie import Document, Indexed
from pydantic import Field

class User(Document):
    name: str
    email: str = Indexed(unique=True)  # Unique index
    is_active: bool = Indexed()  # Regular index

    class Settings:
        name = "users"
```

### Compound Index

```python
class User(Document):
    name: str
    email: str
    role: str
    is_active: bool

    class Settings:
        name = "users"
        indexes = [
            # Compound index
            [
                ("role", 1),  # ascending
                ("is_active", 1),
            ],
            # Text index
            [
                ("name", "text"),
                ("email", "text"),
            ],
            # TTL index (auto-delete after time)
            [
                ("created_at", 1),
                {"expireAfterSeconds": 86400 * 30},  # 30 days
            ],
        ]
```

### Geospatial Index

```python
class Location(Document):
    name: str
    coordinates: dict = {"type": "Point", "coordinates": [0, 0]}

    class Settings:
        name = "locations"
        indexes = [
            [("coordinates", "2dsphere")],
        ]

# Find near locations
locations = await Location.find(
    Location.coordinates.geo_within({
        "$centerSphere": [[-73.99, 40.73], 5 / 6378.1]  # 5km radius
    })
).to_list()
```

---

## Aggregation

### Basic Aggregation Pipeline

```python
from beanie import Document

class Order(Document):
    user_id: str
    total: float
    status: str
    created_at: datetime

    class Settings:
        name = "orders"

# Aggregate: Average order value by status
pipeline = [
    {"$group": {
        "_id": "$status",
        "avg_total": {"$avg": "$total"},
        "count": {"$sum": 1},
    }},
    {"$sort": {"avg_total": -1}},
]

results = await Order.aggregate(pipeline).to_list()
```

### Complex Aggregation

```python
# Revenue by user with order count
pipeline = [
    {"$match": {"status": "completed"}},
    {"$group": {
        "_id": "$user_id",
        "total_revenue": {"$sum": "$total"},
        "order_count": {"$sum": 1},
        "avg_order_value": {"$avg": "$total"},
        "max_order": {"$max": "$total"},
        "min_order": {"$min": "$total"},
    }},
    {"$lookup": {
        "from": "users",
        "localField": "_id",
        "foreignField": "_id",
        "as": "user",
    }},
    {"$unwind": "$user"},
    {"$project": {
        "user_name": "$user.name",
        "total_revenue": 1,
        "order_count": 1,
        "avg_order_value": {"$round": ["$avg_order_value", 2]},
    }},
    {"$sort": {"total_revenue": -1}},
    {"$limit": 10},
]

results = await Order.aggregate(pipeline).to_list()
```

### Date Aggregation

```python
# Monthly revenue
pipeline = [
    {"$match": {
        "created_at": {"$gte": start_date, "$lte": end_date}
    }},
    {"$group": {
        "_id": {
            "year": {"$year": "$created_at"},
            "month": {"$month": "$created_at"},
        },
        "revenue": {"$sum": "$total"},
        "orders": {"$sum": 1},
    }},
    {"$sort": {"_id.year": 1, "_id.month": 1}},
]

results = await Order.aggregate(pipeline).to_list()
```

---

## Beanie with FastAPI Lifespan

### Complete Example

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client["myapp"],
        document_models=[User, Item, Order],
    )
    yield
    # Shutdown
    client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/users/")
async def list_users():
    users = await User.find_all().to_list()
    return users

@app.post("/users/")
async def create_user(user: UserCreate):
    user_doc = User(**user.model_dump())
    await user_doc.insert()
    return user_doc
```

### With Connection Pooling

```python
from motor.motor_asyncio import AsyncIOMotorClient

# Connection pooling configuration
client = AsyncIOMotorClient(
    "mongodb://localhost:27017",
    maxPoolSize=50,
    minPoolSize=10,
    maxIdleTimeMS=30000,
    waitQueueTimeoutMS=5000,
)
```

---

## Best Practices

### 1. Use Indexes for Query Performance

```python
class User(Document):
    email: str = Indexed(unique=True)
    name: str = Indexed()

    class Settings:
        indexes = [
            [("created_at", -1)],  # Sort by creation date
        ]
```

### 2. Embed When Accessed Together

```python
# GOOD: Embed address in user (always accessed together)
class User(Document):
    name: str
    address: Address  # Embedded

# BAD: Separate collection for address (accessed separately)
class Address(Document):
    user_id: str
    street: str
```

### 3. Reference When Data is Shared

```python
# GOOD: Reference product in order items (product data is shared)
class OrderItem(BaseModel):
    product_id: str  # Reference
    quantity: int

# BAD: Embed full product in each order item (duplicate data)
class OrderItem(BaseModel):
    product_name: str  # Duplicated
    product_price: float  # Duplicated
```

### 4. Use Projection Models

```python
class UserListItem(BaseModel):
    name: str
    email: str

# Only fetch what you need
users = await User.find(
    projection_model=UserListItem
).to_list()
```

---

## Interview Questions

### Q1: What is Beanie and why use it over raw Motor?
**Answer:** Beanie provides Pydantic-based document models, automatic schema validation, relationship handling, and a clean query API. Raw Motor requires manual BSON handling and has no validation.

### Q2: When should you embed vs reference in MongoDB?
**Answer:** Embed when data is always accessed/updated together and the embedded data is small. Reference when data is shared across documents, grows unboundedly, or needs independent access.

### Q3: How does Beanie handle relationships?
**Answer:** Beanie uses `Link` type for references and `Document.insert()` for embedding. `fetch_link()` eagerly loads referenced documents. No JOIN operations — MongoDB uses `$lookup` for aggregation.

### Q4: What is the N+1 problem in MongoDB?
**Answer:** When fetching a list of documents and then individually fetching their references. Beanie's `fetch_link()` can cause N+1. Use aggregation pipelines or batch fetching to solve it.

### Q5: How do you handle schema evolution in MongoDB?
**Answer:** MongoDB is schema-flexible, but Beanie models provide validation. Use `model_validate()` for backward compatibility. For major changes, migrate data with scripts.

---

## Summary

Beanie ODM provides a clean, async-native way to work with MongoDB in FastAPI. It combines Pydantic validation with MongoDB's flexible document model. Use embedding for closely coupled data and references for shared data. Always create indexes for query performance.
