# Plugin Architecture for FastAPI

## Table of Contents
1. [Plugin System Design](#design)
2. [Plugin Registry](#registry)
3. [Plugin Hooks](#hooks)
4. [Dynamic Route Registration](#dynamic-routes)
5. [Middleware Plugins](#middleware)
6. [Event Hooks](#event-hooks)
7. [Plugin Configuration](#configuration)

---

## Plugin System Design <a name="design"></a>

A plugin architecture allows extending the application without modifying core code. Plugins can add routes, middleware, event handlers, background tasks, and more.

### Core Concepts

```
Plugin: A self-contained module that extends the application
  - Has a defined interface (lifecycle methods)
  - Can register routes, middleware, event handlers
  - Has its own configuration
  - Can depend on other plugins

Plugin Manager: Manages plugin lifecycle
  - Discovers and loads plugins
  - Resolves dependencies between plugins
  - Calls lifecycle hooks in order
  - Handles plugin configuration

Hook Point: A specific point in the application lifecycle
  - startup, shutdown, before_request, after_request
  - custom hooks defined by the application
```

### Plugin Interface

```python
# app/plugins/base.py
from abc import ABC, abstractmethod
from fastapi import FastAPI

class Plugin(ABC):
    """Base class for all plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the plugin."""
        ...

    @property
    def version(self) -> str:
        return "0.1.0"

    @property
    def dependencies(self) -> list[str]:
        """List of plugin names this plugin depends on."""
        return []

    async def on_startup(self, app: FastAPI) -> None:
        """Called when the application starts."""
        pass

    async def on_shutdown(self, app: FastAPI) -> None:
        """Called when the application stops."""
        pass

    def register_routes(self, app: FastAPI) -> None:
        """Register routes with the application."""
        pass

    def register_middleware(self, app: FastAPI) -> None:
        """Register middleware with the application."""
        pass

    def register_exception_handlers(self, app: FastAPI) -> None:
        """Register exception handlers."""
        pass
```

---

## Plugin Registry <a name="registry"></a>

```python
# app/plugins/registry.py
from typing import Any
import importlib
import logging

logger = logging.getLogger(__name__)

class PluginRegistry:
    def __init__(self):
        self._plugins: dict[str, Plugin] = {}
        self._loaded = False

    def register(self, plugin: Plugin) -> None:
        if plugin.name in self._plugins:
            raise ValueError(f"Plugin '{plugin.name}' is already registered")
        self._plugins[plugin.name] = plugin
        logger.info(f"Registered plugin: {plugin.name} v{plugin.version}")

    def unregister(self, name: str) -> None:
        if name in self._plugins:
            del self._plugins[name]
            logger.info(f"Unregistered plugin: {name}")

    def get(self, name: str) -> Plugin | None:
        return self._plugins.get(name)

    def get_all(self) -> list[Plugin]:
        return list(self._plugins.values())

    def resolve_order(self) -> list[Plugin]:
        """Topological sort based on dependencies."""
        visited = set()
        order = []

        def visit(plugin: Plugin):
            if plugin.name in visited:
                return
            visited.add(plugin.name)
            for dep_name in plugin.dependencies:
                dep = self._plugins.get(dep_name)
                if dep:
                    visit(dep)
            order.append(plugin)

        for plugin in self._plugins.values():
            visit(plugin)

        return order

    def load_from_entry_points(self, group: str = "fastapi_plugins"):
        """Discover plugins from Python entry points."""
        from importlib.metadata import entry_points
        for ep in entry_points().get(group, []):
            try:
                plugin_class = ep.load()
                plugin = plugin_class()
                self.register(plugin)
            except Exception as e:
                logger.error(f"Failed to load plugin {ep.name}: {e}")

    def load_from_module(self, module_path: str):
        """Load a plugin from a module path."""
        module = importlib.import_module(module_path)
        plugin_class = getattr(module, "plugin")
        self.register(plugin_class())

# Global registry
plugin_registry = PluginRegistry()
```

---

## Plugin Hooks <a name="hooks"></a>

### Hook Manager

```python
# app/plugins/hooks.py
from typing import Callable, Any
from collections import defaultdict
import asyncio
import logging

logger = logging.getLogger(__name__)

class HookManager:
    def __init__(self):
        self._hooks: dict[str, list[Callable]] = defaultdict(list)

    def register(self, hook_name: str, handler: Callable, priority: int = 0):
        self._hooks[hook_name].append((priority, handler))
        self._hooks[hook_name].sort(key=lambda x: x[0])

    def unregister(self, hook_name: str, handler: Callable):
        self._hooks[hook_name] = [
            (p, h) for p, h in self._hooks[hook_name] if h != handler
        ]

    async def trigger(self, hook_name: str, *args, **kwargs) -> list[Any]:
        results = []
        for priority, handler in self._hooks.get(hook_name, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    result = await handler(*args, **kwargs)
                else:
                    result = handler(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Hook {hook_name} handler {handler} failed: {e}")
        return results

    def get_hooks(self, hook_name: str) -> list[Callable]:
        return [h for _, h in self._hooks.get(hook_name, [])]

hook_manager = HookManager()
```

### Application Hook Points

```python
# app/hooks.py
from app.plugins.hooks import hook_manager

# Define standard hook points
PRE_REQUEST = "pre_request"
POST_REQUEST = "post_request"
USER_CREATED = "user_created"
ORDER_PLACED = "order_placed"
PAYMENT_RECEIVED = "payment_received"

# Example: trigger hooks in middleware
@app.middleware("http")
async def hook_middleware(request: Request, call_next):
    await hook_manager.trigger(PRE_REQUEST, request)
    response = await call_next(request)
    await hook_manager.trigger(POST_REQUEST, request, response)
    return response

# Example: trigger hooks in endpoint
@router.post("/users")
async def create_user(command: CreateUserCommand):
    user = await user_service.create(command)
    await hook_manager.trigger(USER_CREATED, user)
    return user
```

---

## Dynamic Route Registration <a name="dynamic-routes"></a>

```python
# app/plugins/registry.py
from fastapi import APIRouter

class RouterPlugin(Plugin):
    def __init__(self):
        self._routers: list[APIRouter] = []

    def add_router(self, router: APIRouter, prefix: str = "", tags: list[str] = None):
        self._routers.append({"router": router, "prefix": prefix, "tags": tags or []})

    def register_routes(self, app: FastAPI):
        for item in self._routers:
            app.include_router(
                item["router"],
                prefix=item["prefix"],
                tags=item["tags"],
            )

# Example: Analytics Plugin
class AnalyticsPlugin(Plugin):
    name = "analytics"
    version = "1.0.0"

    def __init__(self):
        self.router = APIRouter(prefix="/api/analytics", tags=["analytics"])

        @self.router.get("/events")
        async def list_events():
            return {"events": []}

        @self.router.get("/dashboard")
        async def dashboard():
            return {"metrics": {}}

    def register_routes(self, app: FastAPI):
        app.include_router(self.router)

    async def on_startup(self, app: FastAPI):
        print("Analytics plugin started")

# Example: Admin Plugin
class AdminPlugin(Plugin):
    name = "admin"
    version = "1.0.0"
    dependencies = ["auth"]

    def __init__(self):
        self.router = APIRouter(prefix="/admin", tags=["admin"])

        @self.router.get("/users")
        async def admin_list_users():
            return {"users": []}

        @self.router.get("/stats")
        async def admin_stats():
            return {"stats": {}}

    def register_routes(self, app: FastAPI):
        app.include_router(self.router)
```

---

## Middleware Plugins <a name="middleware"></a>

```python
# Rate Limiting Plugin
class RateLimitPlugin(Plugin):
    name = "rate_limit"
    version = "1.0.0"

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = {}

    def register_middleware(self, app: FastAPI):
        @app.middleware("http")
        async def rate_limit_middleware(request: Request, call_next):
            client_ip = request.client.host
            now = time.time()

            # Clean old entries
            if client_ip in self._requests:
                self._requests[client_ip] = [
                    t for t in self._requests[client_ip]
                    if now - t < self.window_seconds
                ]
            else:
                self._requests[client_ip] = []

            # Check rate limit
            if len(self._requests[client_ip]) >= self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"}
                )

            self._requests[client_ip].append(now)
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(self.max_requests)
            response.headers["X-RateLimit-Remaining"] = str(
                self.max_requests - len(self._requests[client_ip])
            )
            return response

# CORS Plugin
class CORSPlugin(Plugin):
    name = "cors"
    version = "1.0.0"

    def __init__(self, origins: list[str] = None):
        self.origins = origins or ["*"]

    def register_middleware(self, app: FastAPI):
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
```

---

## Event Hooks <a name="event-hooks"></a>

```python
# app/plugins/events.py
from typing import Any
import asyncio

class EventDrivenPlugin(Plugin):
    """Plugin that subscribes to application events."""

    def __init__(self):
        self._subscriptions: dict[str, list[Callable]] = {}

    def on(self, event_name: str, handler: Callable):
        if event_name not in self._subscriptions:
            self._subscriptions[event_name] = []
        self._subscriptions[event_name].append(handler)

    async def emit(self, event_name: str, *args, **kwargs):
        for handler in self._subscriptions.get(event_name, []):
            if asyncio.iscoroutinefunction(handler):
                await handler(*args, **kwargs)
            else:
                handler(*args, **kwargs)

# Notification Plugin
class NotificationPlugin(EventDrivenPlugin):
    name = "notifications"
    version = "1.0.0"

    def __init__(self):
        super().__init__()
        self.on("user.created", self.send_welcome_email)
        self.on("order.placed", self.send_order_confirmation)
        self.on("payment.received", self.send_receipt)

    async def send_welcome_email(self, user):
        print(f"Sending welcome email to {user.email}")
        # Send email logic here

    async def send_order_confirmation(self, order):
        print(f"Sending order confirmation for order {order.id}")

    async def send_receipt(self, payment):
        print(f"Sending receipt for payment {payment.id}")

    async def on_startup(self, app: FastAPI):
        # Register event handlers with the global event bus
        app.state.event_bus.subscribe("user.created", self.send_welcome_email)
        app.state.event_bus.subscribe("order.placed", self.send_order_confirmation)
```

---

## Plugin Configuration <a name="configuration"></a>

```python
# app/plugins/config.py
from pydantic import BaseModel
from typing import Any

class PluginConfig(BaseModel):
    enabled: bool = True
    settings: dict[str, Any] = {}

class AppConfig(BaseModel):
    plugins: dict[str, PluginConfig] = {}

# Loading plugin config
import yaml

def load_plugin_config(config_path: str) -> AppConfig:
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return AppConfig(**config)

# app/config.yaml
# plugins:
#   rate_limit:
#     enabled: true
#     settings:
#       max_requests: 100
#       window_seconds: 60
#   cors:
#     enabled: true
#     settings:
#       origins:
#         - https://myapp.com
#         - http://localhost:3000
#   analytics:
#     enabled: true
#     settings:
#       tracking_id: UA-XXXXX
```

### Plugin Loading in FastAPI

```python
# app/main.py
from fastapi import FastAPI
from app.plugins.registry import plugin_registry
from app.plugins.hooks import hook_manager

def create_app() -> FastAPI:
    app = FastAPI()

    # Load plugins
    plugin_registry.load_from_module("app.plugins.rate_limit")
    plugin_registry.load_from_module("app.plugins.analytics")
    plugin_registry.load_from_module("app.plugins.notifications")

    # Resolve dependency order
    ordered_plugins = plugin_registry.resolve_order()

    # Register routes
    for plugin in ordered_plugins:
        plugin.register_routes(app)
        plugin.register_middleware(app)
        plugin.register_exception_handlers(app)

    # Store registry in app state
    app.state.plugins = plugin_registry
    app.state.hooks = hook_manager

    @app.on_event("startup")
    async def startup():
        for plugin in ordered_plugins:
            await plugin.on_startup(app)

    @app.on_event("shutdown")
    async def shutdown():
        for plugin in reversed(ordered_plugins):
            await plugin.on_shutdown(app)

    return app

app = create_app()
```

---

## Interview Questions

1. **What is a plugin architecture and when should you use one?**
A plugin architecture allows extending an application through self-contained modules without modifying core code. Use it when you need extensibility, third-party integrations, or modularity. Examples: analytics plugins, payment gateways, authentication providers.

2. **How do you handle plugin dependencies?**
Use topological sorting based on declared dependencies. Each plugin declares what it depends on. The plugin manager resolves the correct loading and initialization order. Fail fast if circular dependencies are detected.

3. **How do plugins register routes dynamically?**
Plugins receive the FastAPI app instance during initialization. They create APIRouter instances and register them with `app.include_router()`. Routes can be conditionally registered based on configuration or environment.

4. **How do you isolate plugins from each other?**
Use dependency injection to provide plugins with their own database sessions, configurations, and state. Use separate namespaces for routes (e.g., `/plugin-name/api/...`). Use events for inter-plugin communication instead of direct imports.

5. **What are plugin hooks and how do they work?**
Hook points are specific locations in the application lifecycle where plugins can inject behavior. Common hooks: startup, shutdown, pre_request, post_request, error. Hooks are executed in priority order. Multiple plugins can register handlers for the same hook.
