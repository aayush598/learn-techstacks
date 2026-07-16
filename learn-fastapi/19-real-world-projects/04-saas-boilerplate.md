# Complete SaaS Boilerplate

## Project Overview

A production-ready SaaS boilerplate with multi-tenancy, RBAC, billing, API keys, rate limiting, audit logging, webhooks, email system, and admin dashboard API.

## Feature List

- Multi-tenancy (team-based isolation)
- JWT + OAuth2 authentication
- Role-based access control (RBAC)
- Subscription management (Stripe)
- API key management
- Rate limiting (per-tenant)
- Audit logging
- Webhook system with delivery tracking
- Email system with templates
- Admin dashboard API
- Team management
- Usage tracking and billing
- Feature flags

## Folder Structure

```
saas-boilerplate/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── redis.py
│   │   ├── events.py
│   │   └── exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── team.py
│   │   ├── subscription.py
│   │   ├── api_key.py
│   │   ├── audit_log.py
│   │   ├── webhook.py
│   │   └── feature_flag.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── team.py
│   │   ├── subscription.py
│   │   ├── api_key.py
│   │   └── webhook.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   ├── middleware.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── teams.py
│   │       ├── subscriptions.py
│   │       ├── api_keys.py
│   │       ├── webhooks.py
│   │       ├── admin.py
│   │       └── usage.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── team_service.py
│   │   ├── billing_service.py
│   │   ├── email_service.py
│   │   ├── webhook_service.py
│   │   ├── audit_service.py
│   │   ├── rate_limiter.py
│   │   └── feature_flag_service.py
│   └── utils/
│       ├── __init__.py
│       ├── pagination.py
│       ├── cache.py
│       └── id_generator.py
├── tests/
├── migrations/
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Data Models

```python
# app/models/user.py
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(100))
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    email_verified: Mapped[bool] = mapped_column(default=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    team_memberships: Mapped[list["TeamMember"]] = relationship(back_populates="user")
    api_keys: Mapped[list["ApiKey"]] = relationship(back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user")


# app/models/team.py
import enum
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class PlanType(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    logo_url: Mapped[str | None] = mapped_column(String(500))
    plan: Mapped[PlanType] = mapped_column(default=PlanType.FREE)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    stripe_subscription_id: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    settings: Mapped[str | None] = mapped_column(Text)  # JSON
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    owner: Mapped["User"] = relationship(foreign_keys=[owner_id])
    members: Mapped[list["TeamMember"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    api_keys: Mapped[list["ApiKey"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    webhooks: Mapped[list["Webhook"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="team")

    PLAN_LIMITS = {
        PlanType.FREE: {"members": 3, "api_calls": 1000, "webhooks": 1, "storage_mb": 100},
        PlanType.STARTER: {"members": 10, "api_calls": 10000, "webhooks": 5, "storage_mb": 1000},
        PlanType.PRO: {"members": 50, "api_calls": 100000, "webhooks": 20, "storage_mb": 10000},
        PlanType.ENTERPRISE: {"members": -1, "api_calls": -1, "webhooks": -1, "storage_mb": -1},
    }

    @property
    def limits(self) -> dict:
        return self.PLAN_LIMITS.get(self.plan, self.PLAN_LIMITS[PlanType.FREE])


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(20), default="member")  # owner, admin, member, viewer
    is_active: Mapped[bool] = mapped_column(default=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    team: Mapped["Team"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="team_memberships")


# app/models/subscription.py
class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    stripe_subscription_id: Mapped[str] = mapped_column(String(255), unique=True)
    stripe_price_id: Mapped[str] = mapped_column(String(255))
    plan: Mapped[PlanType] = mapped_column()
    status: Mapped[str] = mapped_column(String(30))  # active, past_due, canceled, trialing
    current_period_start: Mapped[datetime] = mapped_column(DateTime)
    current_period_end: Mapped[datetime] = mapped_column(DateTime)
    cancel_at: Mapped[datetime | None] = mapped_column(DateTime)
    canceled_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# app/models/api_key.py
import secrets
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class ApiKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(100))
    key_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    key_prefix: Mapped[str] = mapped_column(String(10))  # First 8 chars for identification
    scopes: Mapped[str] = mapped_column(String(500), default="*")  # Comma-separated
    rate_limit: Mapped[int] = mapped_column(Integer, default=1000)  # Per minute
    is_active: Mapped[bool] = mapped_column(default=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    team: Mapped["Team"] = relationship(back_populates="api_keys")
    user: Mapped["User"] = relationship(back_populates="api_keys")

    @staticmethod
    def generate_key() -> str:
        return f"sk_live_{secrets.token_urlsafe(32)}"

    @staticmethod
    def hash_key(key: str) -> str:
        import hashlib
        return hashlib.sha256(key.encode()).hexdigest()


# app/models/audit_log.py
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100))  # e.g., "team.member.invited"
    resource_type: Mapped[str | None] = mapped_column(String(50))
    resource_id: Mapped[str | None] = mapped_column(String(50))
    details: Mapped[str | None] = mapped_column(Text)  # JSON
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    team: Mapped["Team"] = relationship(back_populates="audit_logs")
    user: Mapped["User"] = relationship(back_populates="audit_logs")


# app/models/webhook.py
class Webhook(Base):
    __tablename__ = "webhooks"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(500))
    secret: Mapped[str] = mapped_column(String(255))
    events: Mapped[str] = mapped_column(String(500))  # Comma-separated event types
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    team: Mapped["Team"] = relationship(back_populates="webhooks")


class WebhookDelivery(Base):
    __tablename__ = "webhook_deliveries"

    id: Mapped[int] = mapped_column(primary_key=True)
    webhook_id: Mapped[int] = mapped_column(ForeignKey("webhooks.id"))
    event_type: Mapped[str] = mapped_column(String(100))
    payload: Mapped[str] = mapped_column(Text)  # JSON
    status: Mapped[str] = mapped_column(String(20))  # pending, delivered, failed
    response_status: Mapped[int | None] = mapped_column()
    response_body: Mapped[str | None] = mapped_column(Text)
    attempts: Mapped[int] = mapped_column(default=0)
    max_attempts: Mapped[int] = mapped_column(default=5)
    last_error: Mapped[str | None] = mapped_column(Text)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


# app/models/feature_flag.py
class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    is_enabled: Mapped[bool] = mapped_column(default=False)
    allowed_plans: Mapped[str] = mapped_column(String(200), default="free,starter,pro,enterprise")
    percentage_rollout: Mapped[int] = mapped_column(default=100)  # 0-100
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

## Authentication System

```python
# app/core/security.py
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None

def create_token_pair(user_id: int, email: str, team_id: int | None = None) -> dict:
    access = create_access_token({"sub": str(user_id), "email": email, "team_id": team_id})
    refresh = create_refresh_token({"sub": str(user_id), "email": email})
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
```

## Dependencies and RBAC

```python
# app/api/deps.py
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from app.models.team import Team, TeamMember
from app.models.api_key import ApiKey

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(401, "Invalid or expired token")

    user_id = int(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(401, "User not found or inactive")
    return user

async def get_current_team(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Team:
    """Get the user's current team from JWT or query param."""
    result = await db.execute(
        select(Team)
        .join(TeamMember)
        .where(TeamMember.user_id == user.id, TeamMember.is_active == True)
        .limit(1)
    )
    team = result.scalar_one_or_none()
    if not team:
        raise HTTPException(400, "No team found. Create or join a team first.")
    return team

async def get_team_membership(
    user: User = Depends(get_current_user),
    team: Team = Depends(get_current_team),
    db: AsyncSession = Depends(get_db),
) -> TeamMember:
    result = await db.execute(
        select(TeamMember).where(
            TeamMember.user_id == user.id,
            TeamMember.team_id == team.id,
        )
    )
    membership = result.scalar_one_or_none()
    if not membership or not membership.is_active:
        raise HTTPException(403, "Not a member of this team")
    return membership

def require_role(*allowed_roles: str):
    async def dependency(membership: TeamMember = Depends(get_team_membership)):
        if membership.role not in allowed_roles:
            raise HTTPException(
                403,
                f"Required role: {', '.join(allowed_roles)}. Your role: {membership.role}",
            )
        return membership
    return dependency

async def verify_api_key(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> tuple[ApiKey, Team]:
    """Verify API key from X-API-Key header."""
    api_key_str = request.headers.get("X-API-Key")
    if not api_key_str:
        raise HTTPException(401, "X-API-Key header required")

    key_hash = ApiKey.hash_key(api_key_str)
    result = await db.execute(
        select(ApiKey).where(ApiKey.key_hash == key_hash, ApiKey.is_active == True)
    )
    api_key = result.scalar_one_or_none()

    if not api_key:
        raise HTTPException(401, "Invalid API key")

    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        raise HTTPException(401, "API key expired")

    # Update last used
    api_key.last_used_at = datetime.utcnow()
    await db.flush()

    # Get team
    team = (await db.execute(select(Team).where(Team.id == api_key.team_id))).scalar_one_or_none()
    return api_key, team
```

## Rate Limiter (Per-Tenant)

```python
# app/services/rate_limiter.py
import time
from collections import defaultdict
from dataclasses import dataclass, field
from fastapi import Request, HTTPException

@dataclass
class SlidingWindowRateLimiter:
    """Per-tenant sliding window rate limiter using Redis or in-memory."""

    def __init__(self):
        self.windows: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str, max_requests: int, window_seconds: int = 60) -> tuple[bool, dict]:
        now = time.time()
        cutoff = now - window_seconds

        self.windows[key] = [t for t in self.windows[key] if t > cutoff]
        count = len(self.windows[key])
        remaining = max(0, max_requests - count)

        headers = {
            "X-RateLimit-Limit": str(max_requests),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(int(now + window_seconds)),
        }

        if count >= max_requests:
            retry_after = self.windows[key][0] + window_seconds - now if self.windows[key] else window_seconds
            headers["Retry-After"] = str(int(retry_after) + 1)
            return False, headers

        self.windows[key].append(now)
        return True, headers


rate_limiter = SlidingWindowRateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    """Middleware that applies per-team rate limiting."""
    # Skip for internal endpoints
    if request.url.path.startswith("/internal"):
        return await call_next(request)

    # Extract team_id from token or API key
    team_id = "anonymous"
    auth_header = request.headers.get("Authorization")
    api_key = request.headers.get("X-API-Key")

    if api_key:
        team_id = f"apikey:{api_key[:8]}"
    elif auth_header:
        from app.core.security import decode_token
        token = auth_header.replace("Bearer ", "")
        payload = decode_token(token)
        if payload:
            team_id = f"user:{payload.get('sub', 'unknown')}"

    # Get team limits (default to free tier)
    limits = {"requests_per_minute": 60}  # Default
    key = f"ratelimit:{team_id}"

    allowed, headers = rate_limiter.is_allowed(
        key,
        limits["requests_per_minute"],
        window_seconds=60,
    )

    if not allowed:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
            headers=headers,
        )

    response = await call_next(request)
    response.headers.update(headers)
    return response
```

## Audit Logging Service

```python
# app/services/audit_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
import json

class AuditService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log(
        self,
        team_id: int,
        user_id: int,
        action: str,
        resource_type: str | None = None,
        resource_id: str | None = None,
        details: dict | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ):
        entry = AuditLog(
            team_id=team_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id) if resource_id else None,
            details=json.dumps(details) if details else None,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(entry)
        await self.db.flush()

    async def get_logs(
        self,
        team_id: int,
        action: str | None = None,
        resource_type: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[AuditLog]:
        from sqlalchemy import select, desc
        query = select(AuditLog).where(AuditLog.team_id == team_id)

        if action:
            query = query.where(AuditLog.action == action)
        if resource_type:
            query = query.where(AuditLog.resource_type == resource_type)

        query = query.order_by(desc(AuditLog.created_at)).offset(offset).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
```

## Webhook Service

```python
# app/services/webhook_service.py
import httpx
import hashlib
import hmac
import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.webhook import Webhook, WebhookDelivery

class WebhookService:
    VALID_EVENTS = [
        "team.member.invited",
        "team.member.joined",
        "team.member.removed",
        "subscription.created",
        "subscription.updated",
        "subscription.canceled",
        "api_key.created",
        "api_key.revoked",
    ]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def emit(self, team_id: int, event_type: str, payload: dict):
        """Emit a webhook event to all matching webhooks."""
        result = await self.db.execute(
            select(Webhook).where(
                Webhook.team_id == team_id,
                Webhook.is_active == True,
            )
        )
        webhooks = result.scalars().all()

        for webhook in webhooks:
            if event_type in webhook.events or "*" in webhook.events:
                delivery = WebhookDelivery(
                    webhook_id=webhook.id,
                    event_type=event_type,
                    payload=json.dumps(payload),
                    status="pending",
                )
                self.db.add(delivery)
                await self.db.flush()

                # Deliver asynchronously
                asyncio.create_task(self._deliver(webhook, delivery))

    async def _deliver(self, webhook: Webhook, delivery: WebhookDelivery):
        payload_bytes = delivery.payload.encode()
        signature = hmac.new(webhook.secret.encode(), payload_bytes, hashlib.sha256).hexdigest()

        for attempt in range(delivery.max_attempts):
            delivery.attempts = attempt + 1
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(
                        webhook.url,
                        content=payload_bytes,
                        headers={
                            "Content-Type": "application/json",
                            "X-Webhook-Signature": f"sha256={signature}",
                            "X-Webhook-Event": delivery.event_type,
                            "X-Webhook-Attempt": str(attempt + 1),
                        },
                    )
                    delivery.response_status = response.status_code
                    delivery.response_body = response.text[:1000]

                    if response.status_code < 400:
                        delivery.status = "delivered"
                        from datetime import datetime
                        delivery.delivered_at = datetime.utcnow()
                        await self.db.commit()
                        return

            except Exception as e:
                delivery.last_error = str(e)

            # Exponential backoff
            await asyncio.sleep(min(2 ** attempt * 5, 300))

        delivery.status = "failed"
        await self.db.commit()

    async def get_deliveries(self, webhook_id: int, limit: int = 20) -> list[WebhookDelivery]:
        result = await self.db.execute(
            select(WebhookDelivery)
            .where(WebhookDelivery.webhook_id == webhook_id)
            .order_by(WebhookDelivery.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
```

## Feature Flag Service

```python
# app/services/feature_flag_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.feature_flag import FeatureFlag
from app.models.team import PlanType

class FeatureFlagService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def is_enabled(self, flag_name: str, team_plan: PlanType, team_id: int) -> bool:
        result = await self.db.execute(
            select(FeatureFlag).where(FeatureFlag.name == flag_name)
        )
        flag = result.scalar_one_or_none()

        if not flag or not flag.is_enabled:
            return False

        if team_plan.value not in flag.allowed_plans.split(","):
            return False

        if flag.percentage_rollout < 100:
            # Deterministic hash-based rollout
            import hashlib
            hash_val = int(hashlib.md5(f"{flag_name}:{team_id}".encode()).hexdigest(), 16)
            if (hash_val % 100) >= flag.percentage_rollout:
                return False

        return True

    async def get_all_for_team(self, team_plan: PlanType, team_id: int) -> dict[str, bool]:
        result = await self.db.execute(select(FeatureFlag))
        flags = result.scalars().all()

        return {
            flag.name: await self.is_enabled(flag.name, team_plan, team_id)
            for flag in flags
        }
```

## Team Management

```python
# app/api/v1/teams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.team import Team, TeamMember, PlanType
from app.models.user import User
from app.api.deps import get_current_user, get_current_team, require_role
from app.services.audit_service import AuditService

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", status_code=201)
async def create_team(
    name: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    slug = name.lower().replace(" ", "-")[:50]

    existing = (await db.execute(select(Team).where(Team.slug == slug))).scalar_one_or_none()
    if existing:
        raise HTTPException(400, "Team name already taken")

    team = Team(name=name, slug=slug, owner_id=user.id, plan=PlanType.FREE)
    db.add(team)
    await db.flush()

    membership = TeamMember(team_id=team.id, user_id=user.id, role="owner")
    db.add(membership)

    audit = AuditService(db)
    await audit.log(team.id, user.id, "team.created", "team", team.id)

    await db.commit()
    return {"id": team.id, "name": team.name, "slug": team.slug, "plan": team.plan}

@router.get("/current")
async def get_current_team_info(team: Team = Depends(get_current_team)):
    return {
        "id": team.id,
        "name": team.name,
        "slug": team.slug,
        "plan": team.plan,
        "limits": team.limits,
        "created_at": team.created_at.isoformat(),
    }

@router.post("/invite")
async def invite_member(
    email: str,
    role: str = "member",
    team: Team = Depends(get_current_team),
    membership: TeamMember = Depends(require_role("owner", "admin")),
    db: AsyncSession = Depends(get_db),
):
    # Check plan limits
    current_count = (await db.execute(
        select(TeamMember).where(TeamMember.team_id == team.id, TeamMember.is_active == True)
    )).scalars().all()

    if team.limits["members"] != -1 and len(current_count) >= team.limits["members"]:
        raise HTTPException(400, f"Team member limit reached for {team.plan.value} plan")

    # Find or create user
    user = (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if not user:
        # In production: send invitation email
        raise HTTPException(400, "User not found. Invitation email would be sent.")

    existing = (await db.execute(
        select(TeamMember).where(TeamMember.team_id == team.id, TeamMember.user_id == user.id)
    )).scalar_one_or_none()

    if existing:
        raise HTTPException(400, "User is already a team member")

    new_member = TeamMember(team_id=team.id, user_id=user.id, role=role)
    db.add(new_member)

    audit = AuditService(db)
    await audit.log(team.id, membership.user_id, "team.member.invited", "member", user.id, {"email": email, "role": role})

    await db.commit()
    return {"status": "invited", "email": email, "role": role}

@router.get("/members")
async def list_members(
    team: Team = Depends(get_current_team),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TeamMember).where(TeamMember.team_id == team.id).selectinload(TeamMember.user)
    )
    members = result.scalars().all()

    return [{
        "user_id": m.user.id,
        "email": m.user.email,
        "name": m.user.full_name,
        "role": m.role,
        "joined_at": m.joined_at.isoformat(),
    } for m in members]

@router.delete("/members/{user_id}")
async def remove_member(
    user_id: int,
    team: Team = Depends(get_current_team),
    membership: TeamMember = Depends(require_role("owner", "admin")),
    db: AsyncSession = Depends(get_db),
):
    if user_id == membership.user_id:
        raise HTTPException(400, "Cannot remove yourself")

    target = (await db.execute(
        select(TeamMember).where(TeamMember.team_id == team.id, TeamMember.user_id == user_id)
    )).scalar_one_or_none()

    if not target:
        raise HTTPException(404, "Member not found")

    if target.role == "owner":
        raise HTTPException(403, "Cannot remove the team owner")

    target.is_active = False

    audit = AuditService(db)
    await audit.log(team.id, membership.user_id, "team.member.removed", "member", user_id)

    await db.commit()
    return {"status": "removed"}
```

## API Key Management

```python
# app/api/v1/api_keys.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.api_key import ApiKey
from app.models.team import Team, TeamMember
from app.api.deps import get_current_user, get_current_team, require_role
from app.services.audit_service import AuditService

router = APIRouter(prefix="/api-keys", tags=["API Keys"])

class ApiKeyCreate(BaseModel):
    name: str
    scopes: str = "*"
    rate_limit: int = 1000
    expires_in_days: int | None = None

@router.post("/", status_code=201)
async def create_api_key(
    payload: ApiKeyCreate,
    user = Depends(get_current_user),
    team: Team = Depends(get_current_team),
    membership: TeamMember = Depends(require_role("owner", "admin")),
    db = Depends(get_db),
):
    raw_key = ApiKey.generate_key()
    key_hash = ApiKey.hash_key(raw_key)

    api_key = ApiKey(
        team_id=team.id,
        user_id=user.id,
        name=payload.name,
        key_hash=key_hash,
        key_prefix=raw_key[:12],
        scopes=payload.scopes,
        rate_limit=payload.rate_limit,
    )

    if payload.expires_in_days:
        from datetime import datetime, timedelta
        api_key.expires_at = datetime.utcnow() + timedelta(days=payload.expires_in_days)

    db.add(api_key)

    audit = AuditService(db)
    await audit.log(team.id, user.id, "api_key.created", "api_key", None, {"name": payload.name})

    await db.commit()

    return {
        "id": api_key.id,
        "name": api_key.name,
        "key": raw_key,  # Only shown once!
        "key_prefix": api_key.key_prefix,
        "scopes": api_key.scopes,
        "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
    }

@router.get("/")
async def list_api_keys(
    team: Team = Depends(get_current_team),
    user = Depends(get_current_user),
    db = Depends(get_db),
):
    from sqlalchemy import select
    result = await db.execute(
        select(ApiKey).where(ApiKey.team_id == team.id, ApiKey.is_active == True)
    )
    keys = result.scalars().all()

    return [{
        "id": k.id,
        "name": k.name,
        "key_prefix": k.key_prefix,
        "scopes": k.scopes,
        "last_used_at": k.last_used_at.isoformat() if k.last_used_at else None,
        "expires_at": k.expires_at.isoformat() if k.expires_at else None,
        "created_at": k.created_at.isoformat(),
    } for k in keys]

@router.delete("/{key_id}")
async def revoke_api_key(
    key_id: int,
    team: Team = Depends(get_current_team),
    user = Depends(get_current_user),
    membership: TeamMember = Depends(require_role("owner", "admin")),
    db = Depends(get_db),
):
    from sqlalchemy import select
    key = (await db.execute(
        select(ApiKey).where(ApiKey.id == key_id, ApiKey.team_id == team.id)
    )).scalar_one_or_none()

    if not key:
        raise HTTPException(404)

    key.is_active = False

    audit = AuditService(db)
    await audit.log(team.id, user.id, "api_key.revoked", "api_key", key_id, {"name": key.name})

    await db.commit()
    return {"status": "revoked"}
```

## Webhook Management Endpoints

```python
# app/api/v1/webhooks.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.webhook import Webhook
from app.models.team import Team, TeamMember
from app.api.deps import get_current_user, get_current_team, require_role
from app.services.webhook_service import WebhookService
from app.services.audit_service import AuditService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

class WebhookCreate(BaseModel):
    url: str
    events: list[str] = ["*"]

@router.post("/", status_code=201)
async def create_webhook(
    payload: WebhookCreate,
    user = Depends(get_current_user),
    team: Team = Depends(get_current_team),
    membership: TeamMember = Depends(require_role("owner", "admin")),
    db = Depends(get_db),
):
    import secrets
    secret = secrets.token_hex(32)

    webhook = Webhook(
        team_id=team.id,
        url=payload.url,
        secret=secret,
        events=",".join(payload.events),
    )
    db.add(webhook)

    audit = AuditService(db)
    await audit.log(team.id, user.id, "webhook.created", "webhook", None, {"url": payload.url})

    await db.commit()

    return {
        "id": webhook.id,
        "url": webhook.url,
        "secret": secret,  # Only shown once!
        "events": payload.events,
    }

@router.get("/")
async def list_webhooks(
    team: Team = Depends(get_current_team),
    db = Depends(get_db),
):
    from sqlalchemy import select
    result = await db.execute(select(Webhook).where(Webhook.team_id == team.id))
    webhooks = result.scalars().all()

    return [{"id": w.id, "url": w.url, "events": w.events.split(","), "is_active": w.is_active} for w in webhooks]

@router.get("/{webhook_id}/deliveries")
async def get_webhook_deliveries(
    webhook_id: int,
    team: Team = Depends(get_current_team),
    db = Depends(get_db),
):
    service = WebhookService(db)
    deliveries = await service.get_deliveries(webhook_id)
    return [{"id": d.id, "event": d.event_type, "status": d.status, "attempts": d.attempts, "created_at": d.created_at.isoformat()} for d in deliveries]
```

## Admin Dashboard API

```python
# app/api/v1/admin.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.user import User
from app.models.team import Team, PlanType
from app.models.audit_log import AuditLog
from app.api.deps import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

async def require_superuser(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(403, "Superuser access required")
    return user

@router.get("/dashboard")
async def admin_dashboard(
    user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db),
):
    total_users = (await db.execute(select(func.count()).select_from(User))).scalar()
    total_teams = (await db.execute(select(func.count()).select_from(Team))).scalar()
    active_teams = (await db.execute(select(func.count()).select_from(Team).where(Team.is_active == True))).scalar()

    plan_distribution = {}
    for plan in PlanType:
        count = (await db.execute(select(func.count()).select_from(Team).where(Team.plan == plan))).scalar()
        plan_distribution[plan.value] = count

    return {
        "total_users": total_users,
        "total_teams": total_teams,
        "active_teams": active_teams,
        "plan_distribution": plan_distribution,
    }

@router.get("/teams")
async def list_all_teams(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    plan: str | None = None,
    user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db),
):
    query = select(Team)
    if plan:
        query = query.where(Team.plan == plan)
    query = query.order_by(Team.created_at.desc()).offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    teams = result.scalars().all()

    return [{
        "id": t.id, "name": t.name, "plan": t.plan,
        "is_active": t.is_active, "created_at": t.created_at.isoformat(),
    } for t in teams]

@router.get("/audit-logs")
async def list_audit_logs(
    team_id: int | None = None,
    action: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db),
):
    query = select(AuditLog).options(selectinload(AuditLog.user))
    if team_id:
        query = query.where(AuditLog.team_id == team_id)
    if action:
        query = query.where(AuditLog.action == action)

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    query = query.order_by(AuditLog.created_at.desc()).offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    logs = result.scalars().all()

    return {
        "logs": [{
            "id": l.id, "action": l.action, "resource_type": l.resource_type,
            "user": l.user.email, "team_id": l.team_id, "ip_address": l.ip_address,
            "created_at": l.created_at.isoformat(),
        } for l in logs],
        "total": total,
        "page": page,
    }

@router.put("/teams/{team_id}/plan")
async def update_team_plan(
    team_id: int,
    new_plan: PlanType,
    user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db),
):
    team = (await db.execute(select(Team).where(Team.id == team_id))).scalar_one_or_none()
    if not team:
        raise HTTPException(404)

    old_plan = team.plan
    team.plan = new_plan

    audit = AuditService(db)
    await audit.log(team_id, user.id, "team.plan_changed", "team", team_id, {"old_plan": old_plan.value, "new_plan": new_plan.value})

    await db.commit()
    return {"team_id": team_id, "old_plan": old_plan, "new_plan": new_plan}

@router.get("/feature-flags")
async def list_feature_flags(
    user: User = Depends(require_superuser),
    db: AsyncSession = Depends(get_db),
):
    from app.models.feature_flag import FeatureFlag
    result = await db.execute(select(FeatureFlag))
    flags = result.scalars().all()
    return [{"id": f.id, "name": f.name, "enabled": f.is_enabled, "plans": f.allowed_plans, "rollout": f.percentage_rollout} for f in flags]
```

## Email Service

```python
# app/services/email_service.py
import aiosmtplib
from email.mime.text import MIMEText
from jinja2 import Template
from app.core.config import settings

TEMPLATES = {
    "welcome": "<h1>Welcome, {{ name }}!</h1><p>Your account has been created.</p>",
    "team_invite": "<h1>You've been invited!</h1><p>{{ inviter }} invited you to join {{ team_name }}.</p><p><a href='{{ invite_url }}'>Accept Invitation</a></p>",
    "subscription_change": "<h1>Subscription Updated</h1><p>Your plan has been changed to <strong>{{ new_plan }}</strong>.</p>",
    "api_key_created": "<h1>API Key Created</h1><p>A new API key '<strong>{{ key_name }}</strong>' was created for your team.</p><p>Save this key: <code>{{ key }}</code></p>",
}

class EmailService:
    @staticmethod
    async def send(to: str, subject: str, template_name: str, context: dict):
        html = Template(TEMPLATES.get(template_name, "")).render(**context)
        msg = MIMEText(html, "html")
        msg["Subject"] = subject
        msg["To"] = to
        msg["From"] = settings.EMAIL_FROM

        try:
            await aiosmtplib.send(msg, hostname=settings.SMTP_HOST, port=settings.SMTP_PORT)
        except Exception as e:
            print(f"Email send failed: {e}")

    @staticmethod
    async def send_team_invite(email: str, inviter_name: str, team_name: str, invite_url: str):
        await EmailService.send(email, f"Join {team_name} on {settings.APP_NAME}", "team_invite", {
            "inviter": inviter_name, "team_name": team_name, "invite_url": invite_url,
        })
```

## Rate Limiting Middleware

```python
# app/api/middleware.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.rate_limiter import rate_limiter

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip for docs and health
        if request.url.path in ["/docs", "/openapi.json", "/health"]:
            return await call_next(request)

        # Determine rate limit key
        team_id = None
        api_key = request.headers.get("X-API-Key")

        if api_key:
            team_id = f"apikey:{api_key[:8]}"
        else:
            auth = request.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                from app.core.security import decode_token
                payload = decode_token(auth[7:])
                if payload:
                    team_id = f"user:{payload.get('sub')}"

        if not team_id:
            team_id = f"ip:{request.client.host}"

        key = f"global:{team_id}"
        allowed, headers = rate_limiter.is_allowed(key, max_requests=60, window_seconds=60)

        if not allowed:
            from starlette.responses import JSONResponse
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"}, headers=headers)

        response = await call_next(request)
        for k, v in headers.items():
            response.headers[k] = v
        return response
```

## Main Application

```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.router import api_router
from app.api.middleware import RateLimitMiddleware
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(RateLimitMiddleware)

# CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "healthy", "version": settings.VERSION}
```

## Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    env_file: .env
    ports: ["8000:8000"]
    depends_on: [db, redis]

  celery-beat:
    build: .
    command: celery -A app.core.celery_app beat -l info
    env_file: .env
    depends_on: [db, redis]

  celery-worker:
    build: .
    command: celery -A app.core.celery_app worker -l info -c 4
    env_file: .env
    depends_on: [db, redis]

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: saas_db
      POSTGRES_USER: saas
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: [pgdata:/var/lib/postgresql/data]
    ports: ["5432:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/ssl/certs
    depends_on: [api]

volumes:
  pgdata:
```

## Requirements

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
stripe==10.0.0
httpx==0.27.0
redis[hiredis]==5.1.0
celery[redis]==5.4.0
aiosmtplib==3.0.0
Jinja2==3.1.0
python-multipart==0.0.9
```
