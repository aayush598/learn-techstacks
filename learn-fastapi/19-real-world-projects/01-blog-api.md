# Complete Blog API Blueprint

## Project Overview

A production-grade REST API for a blogging platform with authentication, content management, search, and caching.

## Feature List

- JWT Authentication with refresh tokens
- User registration, login, profile management
- CRUD for posts, categories, tags, comments
- Rich text content support (Markdown)
- Image upload with processing
- Full-text search
- Pagination, filtering, sorting
- Caching with Redis
- Rate limiting
- API documentation (auto-generated)
- Comment threading
- Post likes/favorites
- View counting

## Folder Structure

```
blog-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── events.py
│   │   └── exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── category.py
│   │   ├── tag.py
│   │   └── comment.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── category.py
│   │   ├── tag.py
│   │   ├── comment.py
│   │   ├── auth.py
│   │   └── common.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── posts.py
│   │       ├── categories.py
│   │       ├── tags.py
│   │       └── comments.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── post_service.py
│   │   ├── search_service.py
│   │   └── upload_service.py
│   └── utils/
│       ├── __init__.py
│       ├── pagination.py
│       ├── cache.py
│       └── validators.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_posts.py
│   └── test_comments.py
├── migrations/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pyproject.toml
```

## Data Models

```python
# app/models/user.py
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(100))
    bio: Mapped[str | None] = mapped_column(Text)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    liked_posts: Mapped[list["Post"]] = relationship("Post", secondary="post_likes", back_populates="liked_by")
    favorite_posts: Mapped[list["Post"]] = relationship("Post", secondary="post_favorites", back_populates="favorited_by")


# app/models/post.py
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Table, Column, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

post_likes = Table(
    "post_likes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)

post_favorites = Table(
    "post_favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    excerpt: Mapped[str | None] = mapped_column(String(500))
    cover_image_url: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, published, archived
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author: Mapped["User"] = relationship(back_populates="posts")
    category: Mapped["Category | None"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    liked_by: Mapped[list["User"]] = relationship(secondary=post_likes, back_populates="liked_posts")
    favorited_by: Mapped[list["User"]] = relationship(secondary=post_favorites, back_populates="favorite_posts")


# app/models/category.py
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    posts: Mapped[list["Post"]] = relationship(back_populates="category")
    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent")
    parent: Mapped["Category | None"] = relationship("Category", back_populates="children", remote_side="Category.id")


# app/models/tag.py
class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")


# app/models/comment.py
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
    replies: Mapped[list["Comment"]] = relationship("Comment", back_populates="parent")
    parent: Mapped["Comment | None"] = relationship("Comment", back_populates="replies", remote_side="Comment.id")
```

## Authentication System

```python
# app/core/security.py
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_token_pair(user_id: int, email: str) -> TokenPair:
    access = create_access_token({"sub": str(user_id), "email": email})
    refresh = create_refresh_token({"sub": str(user_id), "email": email})
    return TokenPair(
        access_token=access,
        refresh_token=refresh,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None


# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = int(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

async def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

async def get_current_superuser(user: User = Depends(get_current_user)) -> User:
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user
```

## Authentication Endpoints

```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import (
    hash_password, verify_password, create_token_pair, decode_token,
)
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check existing
    existing = await db.execute(
        select(User).where((User.email == payload.email) | (User.username == payload.username))
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Email or username already taken")

    user = User(
        email=payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    tokens = create_token_pair(user.id, user.email)
    return {
        "user": {"id": user.id, "email": user.email, "username": user.username},
        **tokens.model_dump(),
    }

@router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")

    if not user.is_active:
        raise HTTPException(403, "Account is deactivated")

    tokens = create_token_pair(user.id, user.email)
    return {
        "user": {"id": user.id, "email": user.email, "username": user.username},
        **tokens.model_dump(),
    }

@router.post("/refresh")
async def refresh_token(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    token_data = decode_token(payload.refresh_token)
    if not token_data or token_data.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")

    user_id = int(token_data["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(401, "User not found")

    tokens = create_token_pair(user.id, user.email)
    return tokens.model_dump()

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "bio": user.bio,
        "avatar_url": user.avatar_url,
    }
```

## Post Endpoints

```python
# app/api/v1/posts.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.post import Post
from app.models.user import User
from app.api.deps import get_current_active_user, get_current_user
from app.schemas.post import PostCreate, PostUpdate, PostResponse
import re

router = APIRouter(prefix="/posts", tags=["Posts"])

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text[:255]

@router.get("/", response_model=dict)
async def list_posts(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: str | None = None,
    tag: str | None = None,
    author: str | None = None,
    search: str | None = None,
    sort: str = Query("newest", regex="^(newest|oldest|popular)$"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Post).options(
        selectinload(Post.author),
        selectinload(Post.category),
        selectinload(Post.tags),
    ).where(Post.status == "published")

    if category:
        query = query.join(Post.category).where(Post.category.has(slug=category))
    if tag:
        query = query.join(Post.tags).where(Tag.slug == tag)
    if author:
        query = query.join(Post.author).where(User.username == author)
    if search:
        search_term = f"%{search}%"
        query = query.where(
            Post.title.ilike(search_term) | Post.content.ilike(search_term)
        )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # Sorting
    if sort == "newest":
        query = query.order_by(desc(Post.published_at))
    elif sort == "oldest":
        query = query.order_by(Post.published_at)
    elif sort == "popular":
        query = query.order_by(desc(Post.view_count))

    # Pagination
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    posts = result.scalars().all()

    return {
        "posts": [PostResponse.model_validate(p).model_dump() for p in posts],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, -(-total // per_page)),
    }

@router.get("/{slug}", response_model=PostResponse)
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post)
        .options(selectinload(Post.author), selectinload(Post.category), selectinload(Post.tags))
        .where(Post.slug == slug)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Post not found")

    post.view_count += 1
    await db.commit()

    return PostResponse.model_validate(post)

@router.post("/", status_code=201, response_model=PostResponse)
async def create_post(
    payload: PostCreate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    slug = slugify(payload.title)

    existing = await db.execute(select(Post).where(Post.slug == slug))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "A post with this title already exists")

    post = Post(
        title=payload.title,
        slug=slug,
        content=payload.content,
        excerpt=payload.excerpt or payload.content[:200],
        status=payload.status or "draft",
        author_id=user.id,
        category_id=payload.category_id,
        published_at=datetime.utcnow() if payload.status == "published" else None,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return PostResponse.model_validate(post)

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    payload: PostUpdate,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Post not found")
    if post.author_id != user.id and not user.is_superuser:
        raise HTTPException(403, "Not your post")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)

    if payload.title:
        post.slug = slugify(payload.title)
    if payload.status == "published" and not post.published_at:
        post.published_at = datetime.utcnow()

    await db.commit()
    await db.refresh(post)
    return PostResponse.model_validate(post)

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(404)
    if post.author_id != user.id and not user.is_superuser:
        raise HTTPException(403)

    await db.delete(post)
    await db.commit()
    return {"status": "deleted"}
```

## Comment Endpoints

```python
# app/api/v1/comments.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])

@router.get("/")
async def list_comments(
    post_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Comment)
        .options(selectinload(Comment.author), selectinload(Comment.replies))
        .where(Comment.post_id == post_id, Comment.parent_id == None)
        .order_by(desc(Comment.created_at))
    )

    total = (await db.execute(select(func.count()).select_from(Comment).where(Comment.post_id == post_id))).scalar()
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    comments = result.scalars().all()

    return {
        "comments": [CommentResponse.model_validate(c) for c in comments],
        "total": total,
        "page": page,
    }

@router.post("/", status_code=201)
async def create_comment(
    post_id: int,
    content: str,
    parent_id: int | None = None,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify post exists
    post = (await db.execute(select(Post).where(Post.id == post_id))).scalar_one_or_none()
    if not post:
        raise HTTPException(404, "Post not found")

    if parent_id:
        parent = (await db.execute(select(Comment).where(Comment.id == parent_id))).scalar_one_or_none()
        if not parent or parent.post_id != post_id:
            raise HTTPException(400, "Invalid parent comment")

    comment = Comment(
        content=content,
        author_id=user.id,
        post_id=post_id,
        parent_id=parent_id,
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return CommentResponse.model_validate(comment)
```

## Search Service

```python
# app/services/search_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.post import Post
from app.models.tag import Tag

class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_posts(self, query: str, limit: int = 20) -> list[dict]:
        search = f"%{query}%"
        result = await self.db.execute(
            select(Post)
            .where(
                Post.status == "published",
                or_(
                    Post.title.ilike(search),
                    Post.content.ilike(search),
                    Post.excerpt.ilike(search),
                ),
            )
            .order_by(Post.view_count.desc())
            .limit(limit)
        )
        posts = result.scalars().all()
        return [
            {
                "id": p.id,
                "title": p.title,
                "slug": p.slug,
                "excerpt": p.excerpt,
                "view_count": p.view_count,
                "published_at": p.published_at.isoformat() if p.published_at else None,
            }
            for p in posts
        ]

    async def search_tags(self, query: str, limit: int = 20) -> list[dict]:
        result = await self.db.execute(
            select(Tag).where(Tag.name.ilike(f"%{query}%")).limit(limit)
        )
        return [{"id": t.id, "name": t.name, "slug": t.slug} for t in result.scalars().all()]
```

## Cache Utility

```python
# app/utils/cache.py
import json
import hashlib
from functools import wraps
from typing import Callable

class CacheManager:
    def __init__(self, redis_client):
        self.redis = redis_client

    def key(self, prefix: str, *args, **kwargs) -> str:
        raw = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return f"cache:{hashlib.md5(raw.encode()).hexdigest()}"

    async def get(self, key: str):
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict, ttl: int = 300):
        await self.redis.set(key, json.dumps(value, default=str), ex=ttl)

    async def invalidate(self, pattern: str):
        keys = await self.redis.keys(f"cache:{pattern}*")
        if keys:
            await self.redis.delete(*keys)

    def cached(self, prefix: str, ttl: int = 300):
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = self.key(prefix, *args, **kwargs)
                result = await self.get(cache_key)
                if result is not None:
                    return result
                result = await func(*args, **kwargs)
                await self.set(cache_key, result, ttl)
                return result
            return wrapper
        return decorator
```

## Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://blog:secret@db:5432/blogdb
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: blogdb
      POSTGRES_USER: blog
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api

volumes:
  pgdata:
```

## Caching Strategy

```
Cache Layers:
1. Response Cache (Redis): Cache entire API responses
   - GET /posts: 60s TTL
   - GET /posts/{slug}: 120s TTL
   - GET /categories: 300s TTL

2. Database Query Cache: Cache expensive queries
   - Search results: 30s TTL
   - Analytics: 300s TTL

3. CDN Cache (nginx/CloudFlare):
   - Static assets: 1 year
   - API responses: varies

Invalidation:
- On post create/update: invalidate posts list cache
- On comment create: invalidate post detail cache
- On tag/category change: invalidate related caches
```

## Requirements (requirements.txt)

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy[asyncio]==2.0.35
asyncpg==0.29.0
alembic==1.13.0
pydantic[email]==2.9.0
pydantic-settings==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
httpx==0.27.0
redis[hiredis]==5.1.0
Pillow==10.4.0
python-slugify==8.0.0
bleach==6.1.0
```
