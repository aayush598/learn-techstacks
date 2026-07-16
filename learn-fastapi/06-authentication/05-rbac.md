# Role-Based Access Control (RBAC) with FastAPI

## Table of Contents

1. [RBAC Fundamentals](#rbac-fundamentals)
2. [Role Models](#role-models)
3. [Permission Checking](#permission-checking)
4. [Dependency-Based RBAC](#dependency-based-rbac)
5. [Policy-Based Access Control](#policy-based-access-control)
6. [Admin/User/Moderator Patterns](#adminusermoderator-patterns)
7. [Row-Level Security](#row-level-security)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## RBAC Fundamentals

RBAC assigns permissions to roles, and roles to users. Users inherit permissions through their roles.

### Core Concepts

```
User → has Role → has Permissions → grants Access to Resources

Example:
Alice → Admin → [users:read, users:write, users:delete, items:read, items:write]
Bob → Editor → [items:read, items:write]
Charlie → Viewer → [items:read]
```

### Why RBAC?

- **Scalability**: Manage permissions via roles, not per-user
- **Auditability**: Clear trail of who has what access
- **Least privilege**: Users get only what they need
- **Separation of duties**: Different roles for different tasks

---

## Role Models

### Simple Role Enum

```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    VIEWER = "viewer"

class User(Base):
    id: int = mapped_column(primary_key=True)
    name: str
    role: UserRole = mapped_column(default=UserRole.USER)
```

### Role Table (Many-to-Many)

```python
# Association table
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"

    id: int = mapped_column(primary_key=True)
    name: str = mapped_column(unique=True)
    permissions: Mapped[list["Permission"]] = relationship(
        secondary="role_permissions",
        back_populates="roles",
    )

class Permission(Base):
    __tablename__ = "permissions"

    id: int = mapped_column(primary_key=True)
    name: str = mapped_column(unique=True)  # e.g., "users:read"
    description: str

class User(Base):
    __tablename__ = "users"

    id: int = mapped_column(primary_key=True)
    name: str
    roles: Mapped[list[Role]] = relationship(
        secondary="user_roles",
        back_populates="users",
    )

    def has_permission(self, permission_name: str) -> bool:
        return any(
            permission.name == permission_name
            for role in self.roles
            for permission in role.permissions
        )
```

### Permission Names Convention

```python
# resource:action format
PERMISSIONS = [
    # User management
    "users:read",
    "users:write",
    "users:delete",
    "users:admin",

    # Item management
    "items:read",
    "items:write",
    "items:delete",

    # Order management
    "orders:read",
    "orders:write",
    "orders:cancel",

    # Admin
    "admin:read",
    "admin:write",
    "admin:users",
    "admin:settings",
]
```

---

## Permission Checking

### Simple Permission Check

```python
def require_permission(permission: str):
    async def checker(current_user: User = Depends(get_current_user)):
        if not current_user.has_permission(permission):
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied: {permission}",
            )
        return current_user
    return checker

@app.get("/users/")
async def list_users(
    user: User = Depends(require_permission("users:read")),
):
    ...

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_permission("users:delete")),
    db: Session = Depends(get_db),
):
    ...
```

### Multiple Permission Check

```python
def require_any_permission(*permissions: str):
    async def checker(current_user: User = Depends(get_current_user)):
        user_permissions = {p.name for r in current_user.roles for p in r.permissions}
        if not any(p in user_permissions for p in permissions):
            raise HTTPException(
                status_code=403,
                detail=f"Requires one of: {', '.join(permissions)}",
            )
        return current_user
    return checker

def require_all_permissions(*permissions: str):
    async def checker(current_user: User = Depends(get_current_user)):
        user_permissions = {p.name for r in current_user.roles for p in r.permissions}
        missing = set(permissions) - user_permissions
        if missing:
            raise HTTPException(
                status_code=403,
                detail=f"Missing permissions: {', '.join(missing)}",
            )
        return current_user
    return checker

@app.get("/admin/")
async def admin_route(
    user: User = Depends(require_any_permission("admin:read", "admin:write")),
):
    ...

@app.post("/advanced/")
async def advanced_route(
    user: User = Depends(require_all_permissions("users:read", "items:write")),
):
    ...
```

---

## Dependency-Based RBAC

### Complete RBAC System

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Permission constants
class Permissions:
    USER_READ = "users:read"
    USER_WRITE = "users:write"
    USER_DELETE = "users:delete"
    ITEM_READ = "items:read"
    ITEM_WRITE = "items:write"
    ITEM_DELETE = "items:delete"
    ADMIN_READ = "admin:read"
    ADMIN_WRITE = "admin:write"

# Role definitions
ROLE_PERMISSIONS = {
    "admin": [
        Permissions.USER_READ, Permissions.USER_WRITE, Permissions.USER_DELETE,
        Permissions.ITEM_READ, Permissions.ITEM_WRITE, Permissions.ITEM_DELETE,
        Permissions.ADMIN_READ, Permissions.ADMIN_WRITE,
    ],
    "moderator": [
        Permissions.USER_READ,
        Permissions.ITEM_READ, Permissions.ITEM_WRITE, Permissions.ITEM_DELETE,
    ],
    "user": [
        Permissions.USER_READ,
        Permissions.ITEM_READ, Permissions.ITEM_WRITE,
    ],
    "viewer": [
        Permissions.ITEM_READ,
    ],
}

# Dependencies
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(401, "User not found")
    return user

def require_role(*roles: str):
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Required role: {', '.join(roles)}",
            )
        return user
    return role_checker

def require_permission(*required_permissions: str):
    async def perm_checker(user: User = Depends(get_current_user)):
        user_permissions = set()
        for role in user.roles:
            user_permissions.update(ROLE_PERMISSIONS.get(role.name, []))

        missing = set(required_permissions) - user_permissions
        if missing:
            raise HTTPException(
                status_code=403,
                detail=f"Missing permissions: {', '.join(missing)}",
            )
        return user
    return perm_checker

# Usage
@app.get("/users/")
async def list_users(
    user: User = Depends(require_permission(Permissions.USER_READ)),
):
    ...

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    user: User = Depends(require_permission(Permissions.USER_DELETE)),
):
    ...

@app.get("/admin/")
async def admin_dashboard(
    user: User = Depends(require_role("admin")),
):
    ...
```

---

## Policy-Based Access Control

### Simple Policy Engine

```python
from typing import Callable

class PolicyEngine:
    def __init__(self):
        self.policies: dict[str, Callable] = {}

    def register(self, resource: str, action: str, policy: Callable):
        key = f"{resource}:{action}"
        self.policies[key] = policy

    def check(self, resource: str, action: str, user: User, resource_obj=None) -> bool:
        key = f"{resource}:{action}"
        policy = self.policies.get(key)
        if not policy:
            return False
        return policy(user, resource_obj)

policy_engine = PolicyEngine()

# Register policies
def owner_or_admin_policy(user: User, item) -> bool:
    return user.role == "admin" or item.owner_id == user.id

policy_engine.register("item", "update", owner_or_admin_policy)
policy_engine.register("item", "delete", owner_or_admin_policy)

# Usage
def require_policy(resource: str, action: str):
    async def checker(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
        # For policies that check ownership
        item = await db.get(Item, resource_id)
        if not policy_engine.check(resource, action, user, item):
            raise HTTPException(403, "Access denied")
        return user
    return checker
```

---

## Admin/User/Moderator Patterns

### Role Hierarchy

```python
ROLE_HIERARCHY = {
    "superadmin": ["admin", "moderator", "user"],
    "admin": ["moderator", "user"],
    "moderator": ["user"],
    "user": [],
}

def has_role_or_higher(user_role: str, required_role: str) -> bool:
    """Check if user has the required role or a higher one."""
    if user_role == required_role:
        return True
    higher_roles = ROLE_HIERARCHY.get(user_role, [])
    return required_role in higher_roles

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    if not has_role_or_higher(current_user.role, "admin"):
        raise HTTPException(403, "Admin access required")
    ...
```

### Admin-Only Endpoints

```python
admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_role("admin"))],
)

@admin_router.get("/users/")
async def admin_list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@admin_router.delete("/users/{user_id}")
async def admin_delete_user(user_id: int, db: Session = Depends(get_db)):
    ...
```

### Moderator Permissions

```python
moderator_router = APIRouter(
    prefix="/mod",
    dependencies=[Depends(require_any_role("admin", "moderator"))],
)

@moderator_router.post("/users/{user_id}/ban")
async def ban_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Moderators can't ban other moderators
    target_user = db.query(User).get(user_id)
    if target_user.role in ("admin", "moderator"):
        if current_user.role != "admin":
            raise HTTPException(403, "Can't ban staff members")

    target_user.is_banned = True
    db.commit()
    return {"message": f"User {user_id} banned"}
```

---

## Row-Level Security

### Ownership-Based Access

```python
def get_own_items(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Only return items owned by the current user."""
    return db.query(Item).filter(Item.owner_id == current_user.id).all()

@app.get("/my-items/")
async def my_items(items=Depends(get_own_items)):
    return items
```

### Shared Resources

```python
def can_access_item(user: User, item: Item) -> bool:
    """Check if user can access a specific item."""
    if user.role == "admin":
        return True
    if item.owner_id == user.id:
        return True
    if item.is_public:
        return True
    if item.shared_with and user.id in item.shared_with:
        return True
    return False

@app.get("/items/{item_id}")
async def get_item(
    item_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(404, "Item not found")
    if not can_access_item(user, item):
        raise HTTPException(403, "Access denied")
    return item
```

### Team-Based Access

```python
def can_access_team_resource(user: User, resource_team_id: int) -> bool:
    """Check if user belongs to the resource's team."""
    if user.role == "admin":
        return True
    return any(team.id == resource_team_id for team in user.teams)

@app.get("/teams/{team_id}/projects/")
async def list_team_projects(
    team_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not can_access_team_resource(user, team_id):
        raise HTTPException(403, "Not a team member")

    return db.query(Project).filter(Project.team_id == team_id).all()
```

---

## Best Practices

### 1. Follow Least Privilege

```python
# BAD: Give everyone admin access
@app.get("/users/")
async def list_users(user=Depends(require_role("admin"))):
    # This should be accessible to moderators too!
    ...

# GOOD: Minimum required role
@app.get("/users/")
async def list_users(
    user=Depends(require_any_role("admin", "moderator")),
):
    ...
```

### 2. Check Permissions at Every Level

```python
# API level
@app.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    user: User = Depends(require_permission("items:delete")),
):
    # Service level
    item = await item_service.get(item_id)
    if item.owner_id != user.id and user.role != "admin":
        raise HTTPException(403)
```

### 3. Audit Access Attempts

```python
import logging

logger = logging.getLogger("access")

def audit_access(resource: str, action: str, allowed: bool):
    logger.info(
        f"Access {'granted' if allowed else 'denied'}: "
        f"resource={resource}, action={action}"
    )
```

### 4. Cache Permissions

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_user_permissions(user_id: int) -> set[str]:
    """Cache user permissions to avoid repeated DB queries."""
    db = SessionLocal()
    try:
        user = db.query(User).get(user_id)
        permissions = set()
        for role in user.roles:
            for perm in role.permissions:
                permissions.add(perm.name)
        return permissions
    finally:
        db.close()
```

### 5. Use Declarative Permissions

```python
# Readable, maintainable permission declarations
PERMISSION_MATRIX = {
    "items": {
        "read": ["admin", "moderator", "user", "viewer"],
        "write": ["admin", "moderator", "user"],
        "delete": ["admin", "moderator"],
    },
    "users": {
        "read": ["admin", "moderator"],
        "write": ["admin"],
        "delete": ["admin"],
    },
}

def check_permission(resource: str, action: str, role: str) -> bool:
    allowed_roles = PERMISSION_MATRIX.get(resource, {}).get(action, [])
    return role in allowed_roles
```

---

## Interview Questions

### Q1: What is RBAC?
**Answer:** Role-Based Access Control assigns permissions to roles and roles to users. Users inherit permissions through their roles. It simplifies permission management and follows the principle of least privilege.

### Q2: What is the difference between RBAC and ABAC?
**Answer:** RBAC assigns permissions based on roles. ABAC (Attribute-Based Access Control) uses attributes (user, resource, environment) for fine-grained decisions. RBAC is simpler; ABAC is more flexible.

### Q3: How do you implement RBAC in FastAPI?
**Answer:** Create dependency functions that check user roles/permissions. Use `Depends()` to apply checks to routes. Store roles in the database with many-to-many relationships.

### Q4: What is row-level security?
**Answer:** Restricting data access based on the user's identity. Users can only see/modify their own data or data they have explicit access to. Implemented via query filters in the application layer.

### Q5: How do you handle role hierarchies?
**Answer:** Define role relationships (admin > moderator > user). When checking permissions, consider if the user's role is equal to or higher than the required role. Implement with a hierarchy dictionary.

### Q6: What is the principle of least privilege?
**Answer:** Give users only the minimum permissions they need to perform their job. Reduces the impact of compromised accounts and limits accidental damage.

### Q7: How do you audit access control?
**Answer:** Log all access attempts (granted and denied). Track who accessed what and when. Use centralized logging. Regularly review access patterns for anomalies.

### Q8: How do you handle permissions across microservices?
**Answer:** Use a centralized authorization service. Propagate permissions via JWT claims. Or use a policy engine (Open Policy Agent) for distributed authorization.

---

## Summary

RBAC in FastAPI is implemented through dependency functions that check user roles and permissions. Use role hierarchies, permission matrices, and row-level security for comprehensive access control. Always follow least privilege and audit access attempts.
