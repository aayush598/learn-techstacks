# Request Logging in FastAPI

## Table of Contents
1. [Structured Logging](#structured-logging)
2. [Request ID Tracking](#request-id-tracking)
3. [Correlation IDs](#correlation-ids)
4. [Logging Middleware](#logging-middleware)
5. [Access Logs](#access-logs)
6. [Error Logs](#error-logs)
7. [JSON Log Format](#json-log-format)
8. [Log Levels](#log-levels)
9. [Log Aggregation](#log-aggregation)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Structured Logging

Structured logging outputs logs in a machine-parseable format (typically JSON) instead of plain text. This makes logs searchable, filterable, and analyzable.

### Unstructured vs Structured

```python
import logging

# UNSTRUCTURED: Hard to parse and search
logger.info(f"User {user_id} made {method} request to {path} - status {status}")

# STRUCTURED: Easy to parse and search
logger.info(
    "Request processed",
    extra={
        "user_id": user_id,
        "method": method,
        "path": path,
        "status": status,
    }
)
```

### JSON Formatter

```python
import json
import logging
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields
        if hasattr(record, "extra_data"):
            log_entry.update(record.extra_data)

        # Add exception info
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        return json.dumps(log_entry, default=str)

# Configure
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("app")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

### Using python-json-logger

```python
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
    rename_fields={"levelname": "level", "asctime": "timestamp"},
)
handler.setFormatter(formatter)

logger = logging.getLogger("app")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

### Using structlog

```python
import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger()
log.info("user_logged_in", user_id=123, method="oauth")
```

---

## Request ID Tracking

### Implementation with ContextVar

```python
import uuid
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging

# Context variable for request ID
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Use existing request ID or generate new one
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())

        # Set in context variable
        request_id_ctx.set(request_id)

        # Store in request state
        request.state.request_id = request_id

        # Process request
        response = await call_next(request)

        # Add to response headers
        response.headers["X-Request-ID"] = request_id

        return response
```

### Request ID in All Logs

```python
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get("-")
        return True

# Configure logging with request ID
handler = logging.StreamHandler()
handler.addFilter(RequestIDFilter())
formatter = logging.Formatter(
    '{"timestamp":"%(asctime)s","level":"%(levelname)s",'
    '"request_id":"%(request_id)s","logger":"%(name)s",'
    '"message":"%(message)s"}'
)
handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(logging.INFO)
```

### Request ID in Dependencies

```python
from fastapi import Depends, Request

async def get_db(request: Request):
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Opening database connection")
    db = await create_connection()
    try:
        yield db
    finally:
        logger.info(f"[{request_id}] Closing database connection")
        await db.close()
```

---

## Correlation IDs

### Cross-Service Correlation

```python
import uuid
from contextvars import ContextVar

# Correlation ID spans across multiple services
correlation_id_ctx: ContextVar[str] = ContextVar(
    "correlation_id", default=""
)

class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Get or create correlation ID
        correlation_id = request.headers.get(
            "X-Correlation-ID",
            request.headers.get("X-Request-ID", str(uuid.uuid4()))
        )

        correlation_id_ctx.set(correlation_id)
        request.state.correlation_id = correlation_id

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response
```

### Passing Correlation ID to External Services

```python
import httpx

async def call_external_service(data: dict):
    correlation_id = correlation_id_ctx.get()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://other-service.com/api/data",
            json=data,
            headers={
                "X-Correlation-ID": correlation_id,
                "X-Request-ID": str(uuid.uuid4()),
            }
        )
        return response.json()
```

### Structured Logging with Correlation

```python
import structlog

def add_correlation_id(logger, method_name, event_dict):
    event_dict["correlation_id"] = correlation_id_ctx.get("-")
    return event_dict

structlog.configure(
    processors=[
        add_correlation_id,
        structlog.processors.JSONRenderer(),
    ]
)
```

---

## Logging Middleware

### Comprehensive Logging Middleware

```python
import time
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse

logger = logging.getLogger("app.access")

class ComprehensiveLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        # Log request
        logger.info(
            "request_started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.url.query),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
                "content_type": request.headers.get("content-type"),
                "content_length": request.headers.get("content-length"),
            }
        )

        request.state.request_id = request_id
        request.state.start_time = start_time

        try:
            response = await call_next(request)
            duration = time.perf_counter() - start_time

            logger.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                    "response_size": response.headers.get("content-length"),
                }
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{duration:.4f}"

            return response

        except Exception as e:
            duration = time.perf_counter() - start_time
            logger.exception(
                "request_failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "duration_ms": round(duration * 1000, 2),
                }
            )
            raise
```

### Request Body Logging

```python
class RequestBodyLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Read request body
        body = await request.body()

        # Log body (be careful with sensitive data!)
        if body:
            logger.debug(
                "request_body",
                extra={
                    "request_id": getattr(request.state, "request_id", "-"),
                    "body_size": len(body),
                    "body": body.decode("utf-8", errors="replace")[:1000],  # Limit size
                }
            )

        # Rebuild request with body for downstream
        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive
        response = await call_next(request)
        return response
```

---

## Access Logs

### Apache-Style Access Logs

```python
class ApacheAccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        client_ip = request.client.host if request.client else "-"
        timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S %z")

        response = await call_next(request)
        duration = time.time() - start_time

        # Apache Combined Log Format
        log_line = (
            f'{client_ip} - - [{timestamp}] '
            f'"{request.method} {request.url.path} HTTP/1.1" '
            f'{response.status_code} '
            f'{response.headers.get("content-length", "-")} '
            f'"{request.headers.get("referer", "-")}" '
            f'"{request.headers.get("user-agent", "-")}" '
            f'{duration:.3f}'
        )

        access_logger.info(log_line)
        return response
```

### Nginx-Style Access Logs

```python
class NginxAccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        client_ip = request.client.host if request.client else "-"

        response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            f'{client_ip} - - '
            f'[{datetime.now().strftime("%d/%b/%Y:%H:%M:%S")}] '
            f'"{request.method} {request.url.path} HTTP/1.1" '
            f'{response.status_code} {response.headers.get("content-length", "0")} '
            f'"{request.headers.get("x-forwarded-for", client_ip)}" '
            f'"{request.headers.get("user-agent", "-")}" '
            f'rt={duration:.3f}'
        )
        return response
```

---

## Error Logs

### Error Logging Middleware

```python
import traceback
import logging

error_logger = logging.getLogger("app.error")

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))

        try:
            return await call_next(request)
        except Exception as e:
            error_logger.error(
                "Unhandled exception",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "client_ip": request.client.host if request.client else None,
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
            raise
```

### HTTP Error Logging

```python
from fastapi.exceptions import HTTPException

class HTTPErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)

        if response.status_code >= 400:
            log_method = logger.warning if response.status_code < 500 else logger.error
            log_method(
                "HTTP error response",
                extra={
                    "request_id": getattr(request.state, "request_id", "-"),
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "client_ip": request.client.host if request.client else None,
                }
            )

        return response
```

---

## JSON Log Format

### Production JSON Logger

```python
import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

class ProductionJSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
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

        # Add request context if available
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if hasattr(record, "correlation_id"):
            log_entry["correlation_id"] = record.correlation_id
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id

        # Add exception info
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        # Add any extra fields
        for key in ["method", "path", "status_code", "duration_ms",
                     "client_ip", "user_agent", "body_size"]:
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        return json.dumps(log_entry, default=str, ensure_ascii=False)

# Configure
def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ProductionJSONFormatter())

    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.INFO)

    # Suppress noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
```

### Pretty Printing JSON Logs (Development)

```python
class DevJSONFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",    # Cyan
        "INFO": "\033[32m",     # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",    # Red
        "CRITICAL": "\033[35m", # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        log_entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "level": f"{color}{record.levelname}{self.RESET}",
            "msg": record.getMessage(),
        }
        if hasattr(record, "request_id"):
            log_entry["req_id"] = record.request_id[:8]
        return json.dumps(log_entry, default=str)
```

---

## Log Levels

### Appropriate Levels for Different Events

```python
logger = logging.getLogger("app")

# DEBUG: Detailed diagnostic information
logger.debug("Database query executed", extra={"query": query, "duration_ms": 5})

# INFO: Normal operation messages
logger.info("User logged in", extra={"user_id": 123})
logger.info("Request processed", extra={"path": "/api/users", "status": 200})

# WARNING: Unexpected but handled situations
logger.warning("Rate limit approaching", extra={"client_ip": "1.2.3.4", "remaining": 5})
logger.warning("Slow query detected", extra={"query": query, "duration_ms": 5000})

# ERROR: Error conditions that need attention
logger.error("Database connection failed", extra={"error": str(e)})
logger.error("Payment processing failed", extra={"order_id": 123, "error": str(e)})

# CRITICAL: Fatal errors that cause the application to crash
logger.critical("Database is unreachable", extra={"error": str(e)})
```

### Dynamic Log Level Adjustment

```python
import logging
from fastapi import FastAPI, Query

app = FastAPI()

@app.post("/admin/log-level")
async def set_log_level(level: str = Query(...)):
    numeric_level = getattr(logging, level.upper())
    logging.getLogger("app").setLevel(numeric_level)
    return {"level": level}

@app.get("/admin/log-level")
async def get_log_level():
    logger = logging.getLogger("app")
    return {"level": logging.getLevelName(logger.level)}
```

---

## Log Aggregation

### Sending Logs to External Services

```python
# ELK Stack (Elasticsearch, Logstash, Kibana)
import logging
from logging.handlers import SocketHandler

class ELKHandler(SocketHandler):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.setFormatter(ProductionJSONFormatter())

# Configure
elk_handler = ELKHandler("logstash-host", 5000)
logging.getLogger("app").addHandler(elk_handler)

# Fluentd
import logging
from fluent import handler as fluent_handler

fluent_handler.FluentHandler(
    "app.access",
    host="fluentd-host",
    port=24224,
)

# CloudWatch Logs
import boto3
from watchtower import CloudWatchHandler

cloudwatch_handler = CloudWatchHandler(
    boto3.client("logs"),
    log_group_name="/fastapi/production",
    stream_name="api-server",
)
```

### Structured Log Pipeline

```python
# 1. Application generates structured logs
# 2. Fluentd/Logstash collects and transforms
# 3. Elasticsearch indexes
# 4. Kibana visualizes

# Application side (already shown above)
# Fluentd config
FLUENTD_CONFIG = """
<source>
  @type forward
  port 24224
</source>

<filter app.**>
  @type parser
  key_name log
  <parse>
    @type json
  </parse>
</filter>

<match app.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
</match>
"""
```

---

## Best Practices

### 1. Never Log Sensitive Data

```python
import re

def sanitize_log_data(data: dict) -> dict:
    sensitive_keys = {"password", "token", "secret", "api_key", "credit_card"}
    sanitized = {}

    for key, value in data.items():
        if any(s in key.lower() for s in sensitive_keys):
            sanitized[key] = "***REDACTED***"
        elif isinstance(value, str):
            # Redact credit card numbers
            sanitized[key] = re.sub(
                r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
                '****-****-****-****',
                value
            )
        else:
            sanitized[key] = value

    return sanitized
```

### 2. Use Log Rotation

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
)
```

### 3. Set Appropriate Log Levels

```python
# Production
logging.getLogger("app").setLevel(logging.INFO)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

# Development
logging.getLogger("app").setLevel(logging.DEBUG)
```

### 4. Use Structured Logging in Production

```python
# Always use JSON format in production
# Human-readable format only in development
```

### 5. Include Context in Every Log

```python
# Every log should include:
# - Request ID
# - User ID (if authenticated)
# - Timestamp
# - Relevant business context
```

### 6. Monitor Log Volume and Errors

```python
# Set up alerts for:
# - Error rate spikes
# - Unusual log volume
# - Missing expected logs
```

---

## Interview Questions

### Q1: What is structured logging?
**Answer:** Structured logging outputs logs in a machine-parseable format (typically JSON) with consistent fields, making them searchable and analyzable, unlike plain text logs.

### Q2: Why use request IDs in logging?
**Answer:** Request IDs allow tracing a single request through multiple services, log entries, and debugging tools. They're essential for debugging in distributed systems.

### Q3: What is a correlation ID vs a request ID?
**Answer:** A request ID is unique to a single request within a service. A correlation ID spans across multiple services, allowing you to trace a complete user journey across the system.

### Q4: How do you implement request ID propagation?
**Answer:** Use `ContextVar` to store the request ID, pass it in middleware, add it to response headers, include it in all log entries via a logging Filter, and pass it to downstream services in headers.

### Q5: What log levels should you use in production?
**Answer:** INFO for normal operations, WARNING for unexpected but handled situations, ERROR for failures needing attention. DEBUG should be disabled in production to reduce volume.

### Q6: Why should you never log sensitive data?
**Answer:** Logs can be accessed by operations teams, stored in centralized logging systems, or potentially exposed in breaches. Passwords, tokens, and PII should be redacted.

### Q7: What is the difference between access logs and error logs?
**Answer:** Access logs record every request (method, path, status, duration) for monitoring. Error logs record failures and exceptions for debugging. They often go to different files/streams.

### Q8: How do you handle logging in async code?
**Answer:** Use `ContextVar` instead of thread-local storage. Ensure logging doesn't block the event loop. Use async-compatible log handlers for external services.

### Q9: What is log aggregation?
**Answer:** Log aggregation collects logs from multiple services into a central system (ELK, Datadog, CloudWatch) for searching, analysis, alerting, and visualization.

### Q10: How do you handle log rotation?
**Answer:** Use `RotatingFileHandler` or container log drivers. In Kubernetes, rely on the logging driver. In cloud environments, use managed logging services that handle rotation automatically.

### Q11: What information should every log entry contain?
**Answer:** Timestamp, log level, logger name, message, and request ID at minimum. Additional context like user ID, path, method, and status code should be included when relevant.

### Q12: How do you test logging?
**Answer:** Use `assertLogs` context manager to capture and assert log output. Mock log handlers to verify correct log calls. Check that sensitive data is never logged.

### Q13: What are log enrichment processors?
**Answer:** Processors that automatically add contextual information (request ID, user ID, timestamp) to every log entry without manually including them in each log call.

### Q14: How do you implement centralized logging in microservices?
**Answer:** Each service writes structured JSON logs. A log shipper (Fluentd, Filebeat) collects them. A log aggregator (Elasticsearch, Loki) indexes them. A visualization tool (Kibana, Grafana) displays them.

### Q15: What is the performance impact of logging?
**Answer:** Logging adds I/O overhead. Synchronous logging blocks the event loop. Use async handlers or buffer logs. Avoid excessive DEBUG logging in production. Consider log sampling for high-traffic endpoints.

### Q16: How do you handle logging across time zones?
**Answer:** Always store logs in UTC. Convert to local time only for display. Use ISO 8601 format with timezone offset.

### Q17: What is log sampling?
**Answer:** Log sampling records only a percentage of requests for high-volume endpoints. It reduces log volume while maintaining visibility. Common strategies: 1% of successful requests, 100% of errors.

### Q18: How do you structure logs for debugging?
**Answer:** Include enough context to reproduce the issue: request ID, input parameters, user context, timing information, and stack traces for errors.

### Q19: What is the difference between logging and monitoring?
**Answer:** Logging records discrete events for debugging and audit. Monitoring tracks metrics and trends for alerting. Logs provide detail; metrics provide overview. They complement each other.

### Q20: How do you implement audit logging?
**Answer:** Record who did what, when, and where. Include user ID, action, resource, timestamp, and IP address. Store in tamper-proof storage. Never allow deletion.

### Q21: What are the challenges of logging in async applications?
**Answer:** Context loss between async tasks, ContextVar propagation, log ordering, and ensuring logging doesn't block the event loop are the main challenges.

### Q22: How do you handle log format changes in production?
**Answer:** Use feature flags to switch formats gradually. Deploy new format to a subset of instances. Validate the new format works with your log aggregation pipeline before full rollout.

### Q23: What is the role of logging in security?
**Answer:** Security logging tracks authentication events, authorization failures, suspicious activities, and data access. It's essential for incident response, compliance, and forensics.

### Q24: How do you implement log-based alerting?
**Answer:** Set up alerts for error rate spikes, unusual log patterns, missing expected logs, or specific error messages. Use tools like Elasticsearch Watcher, Datadog Monitors, or CloudWatch Alarms.

### Q25: What are common logging anti-patterns?
**Answer:** Logging sensitive data, using string formatting instead of lazy evaluation, logging in tight loops, not including context, using print() instead of logger, and mixing business logic with logging.
