# SQLModel with FastAPI

## Table of Contents

1. [What is SQLModel](#what-is-sqlmodel)
2. [Installation](#installation)
3. [Table Models](#table-models)
4. [Field Options](#field-options)
5. [Relationships](#relationships)
6. [CRUD with SQLModel](#crud-with-sqlmodel)
7. [Session Dependency](#session-dependency)
8. [SQLModel and FastAPI Integration](#sqlmodel-and-fastapi-integration)
9. [Migration from SQLAlchemy](#migration-from-sqlalchemy)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## What is SQLModel

SQLModel is a library by Sebastián Ramírez (creator of FastAPI) that combines SQLAlchemy and Pydantic into a single class. It eliminates the need for separate ORM models and Pydantic schemas.

### The Problem SQLModel Solves

```python
# BEFORE SQLModel: Duplicate code

# SQLAlchemy model
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(255), unique=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

# Pydantic schema for request
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# Pydantic schema for response
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

# AFTER SQLModel: One class
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
```

### Benefits

1. **Single class** for database table AND Pydantic schema
2. **Type safety** with full IDE support
3. **Automatic validation** from Pydantic
4. **Full SQLAlchemy compatibility** under the hood
5. **Less code** — no duplication between ORM and schemas

---

## Installation

```bash
pip install sqlmodel
# Includes both SQLAlchemy and Pydantic dependencies
```

---

## Table Models

### Basic Table Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    # table=True makes this a database table
    # Without table=True, it's just a Pydantic model

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=255, unique=True, index=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
```

### Model Without Table (Pydantic Only)

```python
class UserCreate(SQLModel):
    # No table=True — pure Pydantic model
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)

class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
```

### Inheritance

```python
class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class User(TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

class Item(TimestampMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
```

---

## Field Options

### Common Field Options

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Product(SQLModel, table=True):
    # Primary key
    id: int | None = Field(default=None, primary_key=True)

    # String with constraints
    name: str = Field(
        max_length=200,
        min_length=1,
        description="Product name",
        index=True,
    )

    # Unique constraint
    sku: str = Field(
        max_length=50,
        unique=True,
        description="Stock keeping unit",
    )

    # Numeric with constraints
    price: float = Field(
        gt=0,           # greater than 0
        le=10000,        # less than or equal to 10000
        description="Price in USD",
    )

    # Optional field
    description: str | None = Field(
        default=None,
        max_length=2000,
    )

    # Default values
    stock: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)

    # Regex pattern
    barcode: str | None = Field(
        default=None,
        pattern=r"^\d{13}$",
    )

    # Foreign key
    category_id: int | None = Field(
        default=None,
        foreign_key="categories.id",
    )

    # Relationship (no DB column)
    # category: Optional["Category"] = Relationship(
    #     back_populates="products"
    # )

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
```

### Relationship Fields

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    members: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="members")
```

### Field Exclusion

```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    hashed_password: str = Field(exclude=True)  # Excluded from Pydantic output
```

---

## Relationships

### One-to-Many

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")

# Usage
team = Team(name="Avengers")
hero = Hero(name="Iron Man", team=team)
```

### Many-to-Many

```python
class Skill(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    heroes: list["Hero"] = Relationship(
        back_populates="skills",
        link_model="HeroSkill",
    )

class HeroSkill(SQLModel, table=True):
    # Association table
    hero_id: int = Field(foreign_key="hero.id", primary_key=True)
    skill_id: int = Field(foreign_key="skill.id", primary_key=True)
    proficiency: str = Field(default="intermediate")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    skills: list[Skill] = Relationship(
        back_populates="heroes",
        link_model=HeroSkill,
    )

# Usage
hero = Hero(name="Spider-Man")
skill1 = Skill(name="Web Slinging")
skill2 = Skill(name="Wall Crawling")
hero.skills = [skill1, skill2]
```

### One-to-One

```python
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False},
    )

class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    bio: str
    user_id: int = Field(foreign_key="user.id", unique=True)
    user: User = Relationship(back_populates="profile")
```

---

## CRUD with SQLModel

### Create

```python
from sqlmodel import Session, select

def create_hero(session: Session, hero_data: dict) -> Hero:
    hero = Hero(**hero_data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# Or with Pydantic model
def create_hero(session: Session, hero_create: HeroCreate) -> Hero:
    hero = Hero.model_validate(hero_create)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

### Read

```python
def get_hero(session: Session, hero_id: int) -> Hero | None:
    return session.get(Hero, hero_id)

def get_hero_by_name(session: Session, name: str) -> Hero | None:
    statement = select(Hero).where(Hero.name == name)
    result = session.exec(statement)
    return result.first()

def list_heroes(
    session: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Hero]:
    statement = select(Hero).offset(skip).limit(limit)
    result = session.exec(statement)
    return list(result.all())

def search_heroes(session: Session, name: str) -> list[Hero]:
    statement = select(Hero).where(Hero.name.contains(name))
    return list(session.exec(statement).all())
```

### Update

```python
def update_hero(
    session: Session,
    hero_id: int,
    hero_data: dict,
) -> Hero | None:
    hero = session.get(Hero, hero_id)
    if not hero:
        return None

    hero_data.pop("id", None)  # Don't update ID
    for key, value in hero_data.items():
        setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

def update_hero_partial(
    session: Session,
    hero_id: int,
    **kwargs,
) -> Hero | None:
    hero = session.get(Hero, hero_id)
    if not hero:
        return None

    for key, value in kwargs.items():
        if value is not None:
            setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero
```

### Delete

```python
def delete_hero(session: Session, hero_id: int) -> bool:
    hero = session.get(Hero, hero_id)
    if not hero:
        return False
    session.delete(hero)
    session.commit()
    return True
```

---

## Session Dependency

### Basic Session Dependency

```python
from sqlmodel import Session, create_engine
from fastapi import Depends

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/heroes/")
def list_heroes(session: Session = Depends(get_session)):
    statement = select(Hero)
    result = session.exec(statement)
    return result.all()
```

### Async Session with SQLModel

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

async_engine = create_async_engine("postgresql+asyncpg://...")
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/heroes/")
async def list_heroes(session: AsyncSession = Depends(get_async_session)):
    result = await session.exec(select(Hero))
    return result.scalars().all()
```

---

## SQLModel and FastAPI Integration

### Full CRUD Example

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel, Field, create_engine, select
from pydantic import EmailStr

# Models
class UserBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    id: int
    model_config = {"from_attributes": True}

class UserUpdate(SQLModel):
    name: str | None = None
    email: EmailStr | None = None

# Database
engine = create_engine("sqlite:///./app.db")

def get_session():
    with Session(engine) as session:
        yield session

# App
app = FastAPI()

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"status": "deleted"}
```

### Response Model Patterns

```python
# Separate read/create models for security
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    is_active: bool
    model_config = {"from_attributes": True}

class UserCreate(SQLModel):
    name: str
    email: str
    password: str  # Not exposed in response

class UserAdminRead(UserRead):
    """Admin sees more fields."""
    hashed_password: str
    last_login: datetime | None = None

@app.get("/users/{id}", response_model=UserRead)
def get_user(id: int, session: Session = Depends(get_session)):
    return session.get(User, id)

@app.get("/admin/users/{id}", response_model=UserAdminRead)
def get_user_admin(id: int, session: Session = Depends(get_session)):
    return session.get(User, id)
```

---

## Migration from SQLAlchemy

### Side-by-Side Comparison

```python
# SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

# SQLModel
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    is_active: bool = True
```

### Migration Steps

1. Install SQLModel: `pip install sqlmodel`
2. Replace `declarative_base()` with `SQLModel`
3. Replace `Column()` with `Field()`
4. Update type annotations
5. Add Pydantic model classes or use SQLModel directly
6. Update session usage (SQLModel works with SQLAlchemy sessions)
7. Test thoroughly

### Hybrid Approach

```python
# You can use SQLAlchemy AND SQLModel together
from sqlalchemy import Column, Integer
from sqlmodel import SQLModel, Field

# SQLModel for simple tables
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

# SQLAlchemy for complex tables (full control)
class ComplexTable(Base):
    __tablename__ = "complex"
    id = Column(Integer, primary_key=True)
    # Full SQLAlchemy column definitions
```

---

## Best Practices

### 1. Separate Read/Write Models

```python
class UserBase(SQLModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str  # Required for creation

class UserRead(UserBase):
    id: int
    model_config = {"from_attributes": True}

class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
```

### 2. Use Field Validators

```python
from pydantic import field_validator

class User(SQLModel, table=True):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.lower()
```

### 3. Keep Table Models Simple

```python
# Table model — minimal fields
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)

# Pydantic schemas — validation rules
class UserCreate(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)
```

### 4. Use `model_config` Correctly

```python
class UserResponse(SQLModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True,  # Enable ORM mode
    }
```

---

## Interview Questions

### Q1: What is SQLModel?
**Answer:** SQLModel is a library that combines SQLAlchemy and Pydantic into a single class. A SQLModel class can be both a database table and a Pydantic schema, eliminating code duplication.

### Q2: What does `table=True` do?
**Answer:** `table=True` tells SQLModel to create a database table from the class. Without it, the class is a pure Pydantic model with no database mapping.

### Q3: How does SQLModel handle relationships?
**Answer:** SQLModel uses SQLAlchemy relationships under the hood. Define them with `Relationship()` and back_populates. Support for one-to-many, many-to-many (with link models), and one-to-one.

### Q4: Can SQLModel use async sessions?
**Answer:** Yes. SQLModel provides `sqlmodel.ext.asyncio.session.AsyncSession` that works with async SQLAlchemy engines. Use it with FastAPI's async dependencies.

### Q5: When should you NOT use SQLModel?
**Answer:** When you need full SQLAlchemy control (complex column types, custom SQL, advanced mapping), when using existing SQLAlchemy codebases, or when Pydantic v2 features conflict with SQLModel's constraints.

### Q6: How do you handle password hashing with SQLModel?
**Answer:** Exclude passwords from responses using `Field(exclude=True)` or separate Pydantic models. Hash before storing, never store plaintext.

### Q7: What is the difference between `SQLModel` and `SQLModel(table=True)`?
**Answer:** `SQLModel` without `table=True` creates a Pydantic-only model (no database table). `SQLModel(table=True)` creates both a Pydantic model and a database table.

### Q8: How do you do partial updates with SQLModel?
**Answer:** Use `model_dump(exclude_unset=True)` to get only provided fields, then iterate and set attributes on the database object.

---

## Summary

SQLModel simplifies FastAPI development by unifying SQLAlchemy and Pydantic. Use it for straightforward CRUD applications. For complex database patterns, pure SQLAlchemy may still be needed. SQLModel is particularly effective for rapid prototyping and small-to-medium applications.
