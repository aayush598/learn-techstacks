# Structured Logging for FastAPI

## Table of Contents
1. [Python Logging Module](#logging-module)
2. [Structlog](#structlog)
3. [JSON Logging](#json-logging)
4. [Log Levels](#log-levels)
5. [Log Context](#log-context)
6. [Correlation IDs](#correlation-ids)
7. [Request Context Logging](#request-context)
8. [Log Formatters](#formatters)
9. [Log Handlers](#handlers)
10. [Logging Best Practices](#best-practices)

---

## Python Logging Module <a name="logging-module"></a>

The standard Python logging module provides the foundation for all logging in FastAPI.

### Basic Configuration

```python
import logging

# Basic setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}
```

### Logger Hierarchy

```
root (logging)
  └── app
      ├── app.main
      ├── app.routes
      │   └── app.routes.users
      ├── app.services
      │   └── app.services.auth
      └── app.database

# Setting level on parent affects all children
logging.getLogger("app").setLevel(logging.DEBUG)
# All app.* loggers now use DEBUG level
```

### Logger Configuration Per Module

```python
# app/routes/users.py
import logging

logger = logging.getLogger(__name__)

@router.get("/users")
async def list_users():
    logger.info("Listing users")
    try:
        users = await db.fetch_all("SELECT * FROM users")
        logger.debug(f"Found {len(users)} users")
        return {"users": users}
    except Exception as e:
        logger.error(f"Failed to list users: {e}", exc_info=True)
        raise
```

---

## Structlog <a name="structlog"></a>

Structlog provides structured, context-rich logging that outputs JSON.

### Installation

```bash
pip install structlog
```

### Configuration

```python
# app/logging_config.py
import structlog
import logging
import sys

def setup_structlog():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

setup_structlog()
```

### Usage

```python
import structlog

logger = structlog.get_logger()

@router.get("/users")
async def list_users():
    log = logger.bind(endpoint="list_users")
    log.info("request_started")

    users = await user_service.list_all()
    log.info("users_fetched", count=len(users))

    return {"users": users}

# Output:
# {"event": "request_started", "endpoint": "list_users", "level": "info", "timestamp": "2025-01-15T10:30:00Z"}
# {"event": "users_fetched", "count": 5, "level": "info", "timestamp": "2025-01-15T10:30:00Z"}
```

### Structlog Processors

```python
structlog.configure(
    processors=[
        # Merge context vars (for async context)
        structlog.contextvars.merge_contextvars,

        # Add log level
        structlog.processors.add_log_level,

        # Add timestamp
        structlog.processors.TimeStamper(fmt="iso"),

        # Add stack info on WARNING+
        structlog.processors.StackInfoRenderer(),

        # Format exceptions
        structlog.processors.format_exc_info,

        # Add caller info
        structlog.processors.CallsiteParameterAdder(
            [structlog.processors.CallsiteParameter.FILENAME,
             structlog.processors.CallsiteParameter.LINENO]
        ),

        # Final renderer (JSON or console)
        structlog.processors.JSONRenderer(),
    ],
)
```

---

## JSON Logging <a name="json-logging"></a>

JSON logs are machine-readable and easy to parse by log aggregation tools.

### Custom JSON Formatter

```python
import json
import logging
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.thread,
        }

        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        return json.dumps(log_data, default=str)

# Setup
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)
```

### JSON Logging Output

```json
{
    "timestamp": "2025-01-15T10:30:00.123456+00:00",
    "level": "INFO",
    "logger": "app.routes.users",
    "message": "Listing users",
    "module": "users",
    "function": "list_users",
    "line": 25,
    "process": 12345,
    "thread": 140234567890
}
```

### JSON with Extra Fields

```python
logger = logging.getLogger(__name__)

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    logger.info(
        "Fetching user",
        extra={
            "user_id": user_id,
            "endpoint": "get_user",
            "method": "GET",
        }
    )
    user = await user_service.get_by_id(user_id)
    logger.info(
        "User fetched",
        extra={
            "user_id": user_id,
            "user_email": user.email,
        }
    )
    return user
```

---

## Log Levels <a name="log-levels"></a>

### Level Hierarchy

```
CRITICAL (50): System error, data loss, service down
ERROR (40): Request failed, operation error
WARNING (30): Unexpected condition, deprecated usage
INFO (20): Important business events, request/response
DEBUG (10): Detailed diagnostic information
```

### When to Use Each Level

```python
logger.critical("Database connection pool exhausted")  # Service-affecting
logger.error("Failed to process payment", exc_info=True)  # Request failure
logger.warning("Rate limit exceeded for user")  # Unexpected but handled
logger.info("User logged in", user_id=123)  # Business event
logger.debug("SQL query executed", query="SELECT * FROM users")  # Diagnostic
```

### Environment-Based Levels

```python
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
)

# Development: DEBUG
# Staging: INFO
# Production: INFO or WARNING
```

---

## Log Context <a name="log-context"></a>

### Structlog Context Variables

```python
import structlog

# Bind context for the current request
structlog.contextvars.clear_contextvars()
structlog.contextvars.bind_contextvars(
    request_id="abc-123",
    user_id=456,
    endpoint="/api/users",
)

# All subsequent log calls include this context
logger.info("Processing request")  # Includes request_id, user_id, endpoint
logger.info("Database query")  # Same context
```

### Context in FastAPI Middleware

```python
import structlog
import uuid

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    # Bind context for this request
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host,
    )

    # Add request_id to response header
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response
```

---

## Correlation IDs <a name="correlation-ids"></a>

Correlation IDs track requests across service boundaries.

```python
import uuid
from contextvars import ContextVar

# Context variable for correlation ID
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")

def get_correlation_id() -> str:
    return correlation_id_var.get()

def set_correlation_id(cid: str):
    correlation_id_var.set(cid)

@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    # Extract or generate correlation ID
    cid = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    set_correlation_id(cid)

    # Bind to structlog context
    structlog.contextvars.bind_contextvars(correlation_id=cid)

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid

    return response

# In service layer
async def process_order(order_id: int):
    cid = get_correlation_id()
    logger.info("processing_order", order_id=order_id, correlation_id=cid)

    # Pass correlation ID to downstream services
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://payment-service/charge",
            json={"order_id": order_id},
            headers={"X-Correlation-ID": cid},
        )
```

---

## Request Context Logging <a name="request-context"></a>

### Full Request/Response Logging

```python
import time
import structlog

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=str(request.url.path),
        query=str(request.query_params),
        client_ip=request.client.host,
        user_agent=request.headers.get("user-agent", ""),
    )

    logger.info("request_started")

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        "request_completed",
        status_code=response.status_code,
        duration_ms=round(duration * 1000, 2),
    )

    response.headers["X-Request-ID"] = request_id
    return response
```

### Structured Request Log Output

```json
{
    "event": "request_completed",
    "request_id": "abc-123",
    "method": "GET",
    "path": "/api/users",
    "query": "page=1&limit=20",
    "client_ip": "192.168.1.1",
    "user_agent": "Mozilla/5.0...",
    "status_code": 200,
    "duration_ms": 45.23,
    "level": "info",
    "timestamp": "2025-01-15T10:30:00.123456+00:00"
}
```

---

## Log Formatters <a name="formatters"></a>

### Console Formatter (Development)

```python
class ConsoleFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        return (
            f"{color}[{record.levelname}]{self.RESET} "
            f"{record.name}: {record.getMessage()}"
        )
```

### Production Formatter

```python
class ProductionFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "lvl": record.levelname[0],
            "msg": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            log_data["err"] = self.formatException(record.exc_info)
        return json.dumps(log_data, default=str)
```

---

## Log Handlers <a name="handlers"></a>

### Multiple Handlers

```python
def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Console handler (stdout)
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(JSONFormatter())
    root.addHandler(console)

    # File handler
    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=10_000_000,  # 10MB
        backupCount=5,
    )
    file_handler.setFormatter(JSONFormatter())
    root.addHandler(file_handler)

    # Error file handler
    error_handler = RotatingFileHandler(
        "error.log",
        maxBytes=10_000_000,
        backupCount=5,
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    root.addHandler(error_handler)

    # Syslog handler (for centralized logging)
    syslog = SysLogHandler(address="/dev/log")
    syslog.setFormatter(JSONFormatter())
    root.addHandler(syslog)
```

### Queue Handler (Non-Blocking)

```python
import logging.handlers

queue = multiprocessing.Queue(-1)

# Queue listener runs in a separate thread
listener = logging.handlers.QueueListener(
    queue,
    logging.StreamHandler(),
    logging.FileHandler("app.log"),
)
listener.start()

# Queue handler is non-blocking
handler = logging.handlers.QueueHandler(queue)
root = logging.getLogger()
root.addHandler(handler)
```

---

## Logging Best Practices <a name="best-practices"></a>

1. **Use structured logging** — JSON format for production, human-readable for development
2. **Include correlation IDs** — Track requests across services
3. **Never log sensitive data** — Passwords, tokens, credit cards, PII
4. **Use appropriate log levels** — DEBUG for dev, INFO for business events, ERROR for failures
5. **Log in the right place** — Log at service boundaries, not in utility functions
6. **Include context** — Request ID, user ID, operation name
7. **Use async-safe context** — structlog.contextvars for async/await
8. **Set log levels per module** — Quieter for libraries, verbose for your code
9. **Use log rotation** — Prevent disk exhaustion
10. **Test your logging** — Verify logs are correct and complete
11. **Use logger names** — `logging.getLogger(__name__)` for module-level loggers
12. **Avoid string formatting in log calls** — Use `logger.info("msg", extra={"key": val})` instead of f-strings
13. **Separate access logs from application logs** — Different handlers and formats
14. **Monitor log volumes** — Sudden changes indicate issues
15. **Use log aggregation** — Centralize logs with ELK, Datadog, or CloudWatch
