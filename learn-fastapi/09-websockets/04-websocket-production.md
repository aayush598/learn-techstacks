# WebSocket Production

## Table of Contents
1. [WebSocket in Production](#websocket-in-production)
2. [Horizontal Scaling](#horizontal-scaling)
3. [Redis Pub/Sub for Multi-Instance](#redis-pubsub-for-multi-instance)
4. [Heartbeat/Ping-Pong](#heartbeatping-pong)
5. [Connection Limits](#connection-limits)
6. [WebSocket with Nginx](#websocket-with-nginx)
7. [WebSocket Security](#websocket-security)
8. [Monitoring and Observability](#monitoring-and-observability)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## WebSocket in Production

### Production Considerations

Running WebSockets in production requires addressing:
- **Scalability**: Multiple server instances
- **Reliability**: Connection recovery, message persistence
- **Performance**: Memory management, connection limits
- **Security**: Authentication, rate limiting, DoS protection
- **Monitoring**: Connection counts, message rates, errors

### Architecture Overview

```
                    ┌─────────────────┐
                    │   Load Balancer  │
                    │   (Sticky Session)│
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
        │ Instance 1 │ │ Instance 2 │ │ Instance 3 │
        └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │     Redis       │
                    │  (Pub/Sub + State)│
                    └─────────────────┘
```

---

## Horizontal Scaling

### Why Horizontal Scaling?

- **More connections**: Each instance handles a portion
- **Fault tolerance**: If one instance fails, others continue
- **Geographic distribution**: Instances closer to users

### Load Balancer Configuration

```nginx
# Nginx sticky session configuration
upstream websocket_servers {
    sticky cookie ws_route expires=1h;
    server instance1:8000;
    server instance2:8000;
    server instance3:8000;
}

server {
    listen 443 ssl;

    location /ws/ {
        proxy_pass http://websocket_servers;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # WebSocket timeout settings
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```

### Kubernetes Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: websocket-service
spec:
  selector:
    app: websocket-server
  ports:
    - port: 8000
      targetPort: 8000
  sessionAffinity: ClientIP  # Sticky sessions
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

---

## Redis Pub/Sub for Multi-Instance

### Complete Redis Pub/Sub Implementation

```python
import redis.asyncio as redis
import asyncio
import json
import uuid
from typing import Optional

class ProductionWebSocketManager:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.local_connections: dict[str, dict[str, 'WebSocket']] = {}
        self.instance_id = str(uuid.uuid4())[:8]
        self._listener_tasks: dict[str, asyncio.Task] = {}

    async def connect_redis(self):
        self.redis = redis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        self.pubsub = self.redis.pubsub()

    async def disconnect_redis(self):
        if self.redis:
            await self.redis.close()

    async def handle_connect(
        self,
        websocket: 'WebSocket',
        room_id: str,
        user_id: str,
    ) -> str:
        await websocket.accept()

        connection_id = str(uuid.uuid4())

        # Store locally
        if room_id not in self.local_connections:
            self.local_connections[room_id] = {}
        self.local_connections[room_id][connection_id] = websocket

        # Track in Redis
        await self.redis.hset(
            f"ws:room:{room_id}:connections",
            connection_id,
            json.dumps({
                "user_id": user_id,
                "instance_id": self.instance_id,
                "connected_at": time.time(),
            }),
        )

        # Start listener for this room
        if room_id not in self._listener_tasks:
            self._listener_tasks[room_id] = asyncio.create_task(
                self._listen_room(room_id)
            )

        return connection_id

    async def handle_disconnect(self, room_id: str, connection_id: str):
        # Remove locally
        if room_id in self.local_connections:
            self.local_connections[room_id].pop(connection_id, None)
            if not self.local_connections[room_id]:
                del self.local_connections[room_id]
                # Cancel listener if no local connections
                if room_id in self._listener_tasks:
                    self._listener_tasks[room_id].cancel()
                    del self._listener_tasks[room_id]

        # Remove from Redis
        await self.redis.hdel(f"ws:room:{room_id}:connections", connection_id)

    async def broadcast(self, room_id: str, message: dict):
        """Publish message to Redis channel for all instances."""
        await self.redis.publish(
            f"ws:room:{room_id}:messages",
            json.dumps(message),
        )

    async def _listen_room(self, room_id: str):
        """Listen for messages from Redis and deliver to local connections."""
        await self.pubsub.subscribe(f"ws:room:{room_id}:messages")

        try:
            async for msg in self.pubsub.listen():
                if msg["type"] == "message":
                    message = json.loads(msg["data"])

                    # Deliver to all local connections in this room
                    if room_id in self.local_connections:
                        disconnected = []
                        for conn_id, ws in self.local_connections[room_id].items():
                            try:
                                await ws.send_text(json.dumps(message))
                            except Exception:
                                disconnected.append(conn_id)

                        # Clean up disconnected
                        for conn_id in disconnected:
                            await self.handle_disconnect(room_id, conn_id)
        except asyncio.CancelledError:
            await self.pubsub.unsubscribe(f"ws:room:{room_id}:messages")

    async def get_room_users(self, room_id: str) -> list[dict]:
        """Get all users in a room across all instances."""
        connections = await self.redis.hgetall(f"ws:room:{room_id}:connections")
        users = []
        for conn_data in connections.values():
            data = json.loads(conn_data)
            users.append({
                "user_id": data["user_id"],
                "instance_id": data["instance_id"],
            })
        return users

    async def send_to_user(self, user_id: str, message: dict):
        """Send message to a specific user across all instances."""
        # Find which instance has the user
        for room_id, connections in self.local_connections.items():
            for conn_id, ws in connections.items():
                try:
                    await ws.send_text(json.dumps(message))
                except:
                    pass

# Global instance
ws_manager = ProductionWebSocketManager("redis://localhost:6379")

@app.on_event("startup")
async def startup():
    await ws_manager.connect_redis()

@app.on_event("shutdown")
async def shutdown():
    await ws_manager.disconnect_redis()
```

---

## Heartbeat/Ping-Pong

### Why Heartbeats?

- **Detect dead connections**: Identify connections that dropped without close frame
- **Keep connections alive**: Prevent NAT/firewall timeouts
- **Monitor connection health**: Track latency

### Server-Side Heartbeat

```python
import asyncio
import time

class HeartbeatManager:
    def __init__(self, interval: int = 30, timeout: int = 10):
        self.interval = interval  # Seconds between pings
        self.timeout = timeout    # Seconds to wait for pong

    async def start_heartbeat(self, websocket: WebSocket, connection_id: str):
        """Send periodic pings and check for pong responses."""
        last_pong = time.time()

        async def send_pings():
            nonlocal last_pong
            while True:
                await asyncio.sleep(self.interval)
                try:
                    await websocket.send_text(json.dumps({"type": "ping"}))

                    # Check if pong was received
                    if time.time() - last_pong > self.timeout:
                        print(f"Connection {connection_id} timed out")
                        await websocket.close(code=1001)
                        break
                except Exception:
                    break

        async def handle_pong():
            nonlocal last_pong
            while True:
                try:
                    data = await websocket.receive_text()
                    msg = json.loads(data)
                    if msg.get("type") == "pong":
                        last_pong = time.time()
                except:
                    break

        # Run both tasks
        ping_task = asyncio.create_task(send_pings())
        pong_task = asyncio.create_task(handle_pong())

        try:
            await asyncio.gather(ping_task, pong_task)
        finally:
            ping_task.cancel()
            pong_task.cancel()
```

### Ping-Pong Protocol

```python
@app.websocket("/ws/{room_id}")
async def websocket_with_heartbeat(
    websocket: WebSocket,
    room_id: str,
):
    await websocket.accept()
    heartbeat = HeartbeatManager(interval=30, timeout=10)

    # Start heartbeat in background
    heartbeat_task = asyncio.create_task(
        heartbeat.start_heartbeat(websocket, room_id)
    )

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)

            # Handle pong responses
            if msg.get("type") == "pong":
                continue

            # Handle regular messages
            await broadcast(room_id, {
                "type": "message",
                "content": msg.get("content"),
            })
    except WebSocketDisconnect:
        pass
    finally:
        heartbeat_task.cancel()
```

### Native WebSocket Ping/Pong

```python
@app.websocket("/ws")
async def native_pingpong(websocket: WebSocket):
    await websocket.accept()

    # FastAPI/Starlette supports native ping/pong
    # Use websocket.send_text with special frames or rely on ASGI layer

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
```

---

## Connection Limits

### Per-Server Limits

```python
class ConnectionLimitManager:
    def __init__(self, max_connections: int = 10000):
        self.max_connections = max_connections
        self.current_connections = 0

    def can_connect(self) -> bool:
        return self.current_connections < self.max_connections

    def increment(self):
        self.current_connections += 1

    def decrement(self):
        self.current_connections -= 1

limit_manager = ConnectionLimitManager(max_connections=10000)

@app.websocket("/ws/{room_id}")
async def limited_websocket(websocket: WebSocket, room_id: str):
    if not limit_manager.can_connect():
        await websocket.close(code=1013)  # Try Again Later
        return

    limit_manager.increment()
    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            # Process
    except WebSocketDisconnect:
        pass
    finally:
        limit_manager.decrement()
```

### Per-User Limits

```python
class PerUserLimitManager:
    def __init__(self, max_per_user: int = 5):
        self.max_per_user = max_per_user
        self.user_connections: dict[str, int] = {}

    def can_connect(self, user_id: str) -> bool:
        return self.user_connections.get(user_id, 0) < self.max_per_user

    def increment(self, user_id: str):
        self.user_connections[user_id] = self.user_connections.get(user_id, 0) + 1

    def decrement(self, user_id: str):
        if user_id in self.user_connections:
            self.user_connections[user_id] -= 1
            if self.user_connections[user_id] <= 0:
                del self.user_connections[user_id]

user_limit = PerUserLimitManager(max_per_user=5)

@app.websocket("/ws/{room_id}")
async def per_user_limited_websocket(
    websocket: WebSocket,
    room_id: str,
    user_id: str = Query(...),
):
    if not user_limit.can_connect(user_id):
        await websocket.close(code=1013)
        return

    user_limit.increment(user_id)
    try:
        await websocket.accept()
        # ...
    except WebSocketDisconnect:
        pass
    finally:
        user_limit.decrement(user_id)
```

---

## WebSocket with Nginx

### Basic Nginx Configuration

```nginx
http {
    upstream websocket_backend {
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
    }

    server {
        listen 443 ssl http2;
        server_name ws.example.com;

        ssl_certificate /etc/ssl/certs/example.com.crt;
        ssl_certificate_key /etc/ssl/private/example.com.key;

        # WebSocket location
        location /ws/ {
            proxy_pass http://websocket_backend;
            proxy_http_version 1.1;

            # WebSocket upgrade headers
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            # Preserve headers
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeout settings (keep connection alive)
            proxy_read_timeout 86400s;
            proxy_send_timeout 86400s;

            # Buffer settings
            proxy_buffering off;
            proxy_cache off;
        }

        # Regular API endpoints
        location /api/ {
            proxy_pass http://api_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

### Advanced Nginx with Sticky Sessions

```nginx
# Using ip_hash for sticky sessions
upstream websocket_backend {
    ip_hash;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

# Or using hash-based routing
upstream websocket_backend {
    hash $arg_user_id consistent;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}
```

---

## WebSocket Security

### Security Checklist

```python
# 1. Use WSS (TLS)
# Always use wss:// in production

# 2. Validate Origin
@app.websocket("/ws")
async def secure_websocket(websocket: WebSocket):
    origin = websocket.headers.get("origin")
    if origin not in ALLOWED_ORIGINS:
        await websocket.close(code=1008)
        return

# 3. Authenticate on Connect
@app.websocket("/ws")
async def auth_websocket(websocket: WebSocket, token: str = Query(...)):
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return

# 4. Rate Limiting
@app.websocket("/ws")
async def rate_limited_websocket(websocket: WebSocket):
    # Check rate limit before accepting
    if not rate_limiter.is_allowed(websocket.client.host):
        await websocket.close(code=1013)
        return
    await websocket.accept()

# 5. Input Validation
@app.websocket("/ws")
async def validated_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if len(data) > MAX_MESSAGE_SIZE:
            await websocket.send_text("Message too large")
            continue
        # Validate and sanitize
```

### CSRF Protection

```python
@app.websocket("/ws")
async def csrf_protected_websocket(
    websocket: WebSocket,
    token: str = Query(...),
    origin: str = Query(None),
):
    # Validate origin matches expected domain
    if origin and not origin.endswith(".example.com"):
        await websocket.close(code=1008)
        return

    # Validate token (should be a CSRF token, not just session)
    if not validate_csrf_token(token):
        await websocket.close(code=1008)
        return

    await websocket.accept()
```

---

## Monitoring and Observability

### Metrics to Track

```python
import prometheus_client

# Connection metrics
ws_connections_total = prometheus_client.Counter(
    'websocket_connections_total',
    'Total WebSocket connections',
    ['room_type']
)

ws_active_connections = prometheus_client.Gauge(
    'websocket_active_connections',
    'Current active WebSocket connections'
)

ws_messages_total = prometheus_client.Counter(
    'websocket_messages_total',
    'Total WebSocket messages',
    ['message_type', 'room_type']
)

ws_errors_total = prometheus_client.Counter(
    'websocket_errors_total',
    'Total WebSocket errors',
    ['error_type']
)

# Usage in WebSocket handler
@app.websocket("/ws/{room_id}")
async def monitored_websocket(websocket: WebSocket, room_id: str):
    ws_connections_total.labels(room_type="chat").inc()
    ws_active_connections.inc()

    try:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            ws_messages_total.labels(message_type="text", room_type="chat").inc()
            # Process message
    except WebSocketDisconnect:
        ws_active_connections.dec()
    except Exception as e:
        ws_errors_total.labels(error_type=type(e).__name__).inc()
        raise
```

### Logging

```python
import logging

ws_logger = logging.getLogger("websocket")

@app.websocket("/ws/{room_id}")
async def logged_websocket(websocket: WebSocket, room_id: str):
    client_ip = websocket.client.host
    ws_logger.info(f"Connection attempt from {client_ip} to room {room_id}")

    try:
        await websocket.accept()
        ws_logger.info(f"Connected: {client_ip} to room {room_id}")

        while True:
            data = await websocket.receive_text()
            ws_logger.debug(f"Message from {client_ip}: {len(data)} bytes")
    except WebSocketDisconnect:
        ws_logger.info(f"Disconnected: {client_ip} from room {room_id}")
    except Exception as e:
        ws_logger.error(f"Error for {client_ip}: {e}")
```

---

## Best Practices

### 1. Use Sticky Sessions

```nginx
# Nginx
ip_hash;

# Kubernetes
sessionAffinity: ClientIP
```

### 2. Implement Heartbeats

```python
# Detect dead connections
# Keep connections alive through NAT/firewalls
# Monitor connection health
```

### 3. Set Connection Limits

```python
# Per-server: Prevent overload
# Per-user: Prevent abuse
# Per-room: Prevent flooding
```

### 4. Use Redis for Shared State

```python
# Connection tracking
# Message history
# Pub/Sub for broadcasting
```

### 5. Monitor Everything

```python
# Connection counts
# Message rates
# Error rates
# Latency
# Memory usage
```

### 6. Handle Graceful Shutdown

```python
@app.on_event("shutdown")
async def shutdown():
    # Close all WebSocket connections
    # Drain message queues
    # Release resources
```

---

## Interview Questions

### Q1: How do you scale WebSocket connections in production?
**Answer:** Use horizontal scaling with multiple server instances, sticky sessions at the load balancer, Redis pub/sub for message distribution, and shared state in Redis.

### Q2: What are sticky sessions and why are they needed?
**Answer:** Sticky sessions route all requests from a client to the same server instance. Needed because WebSocket connections are persistent and state is stored locally.

### Q3: How does Redis pub/sub work with WebSockets?
**Answer:** Each server instance subscribes to Redis channels. When a message is published, all instances receive it and deliver to their local connections. This enables cross-instance broadcasting.

### Q4: Why are heartbeats important in production?
**Answer:** They detect dead connections, keep connections alive through NAT/firewalls, and allow monitoring connection health. Without heartbeats, zombie connections accumulate.

### Q5: What are the connection limits you should set?
**Answer:** Per-server (prevent overload), per-user (prevent abuse), per-room (prevent flooding), and global (infrastructure limits). Adjust based on resources.

### Q6: How do you configure Nginx for WebSocket connections?
**Answer:** Set `proxy_http_version 1.1`, add Upgrade/Connection headers, disable buffering, and set long read/send timeouts (86400s for 24 hours).

### Q7: What security measures are needed for WebSocket connections?
**Answer:** Use WSS (TLS), validate Origin, authenticate on connect, implement rate limiting, validate input, and set message size limits.

### Q8: How do you monitor WebSocket connections?
**Answer:** Track connection counts, message rates, error rates, latency, and memory usage using Prometheus metrics and Grafana dashboards.

### Q9: What is the difference between graceful and ungraceful shutdown?
**Answer:** Graceful: notify clients, drain messages, close connections properly. Ungraceful: close immediately, potentially losing messages. Always prefer graceful.

### Q10: How do you handle WebSocket connection failures?
**Answer:** Implement client-side reconnection with exponential backoff. Server-side: clean up resources, track failed connections, alert on high failure rates.

### Q11: How do you handle WebSocket connections behind a CDN?
**Answer:** Configure CDN to support WebSocket (Cloudflare, AWS CloudFront). Ensure CDN doesn't buffer or timeout WebSocket connections.

### Q12: What is the difference between WebSocket and long polling for scaling?
**Answer:** WebSocket: persistent connection, lower overhead, better for high message rates. Long polling: HTTP-based, simpler, but higher overhead per message.

### Q13: How do you handle geographic distribution of WebSocket connections?
**Answer:** Use edge servers or CDN with WebSocket support. Route connections to nearest server. Use global Redis for cross-region message distribution.

### Q14: How do you prevent WebSocket DoS attacks?
**Answer:** Rate limit connections per IP, limit message rate, validate message size, use CAPTCHA for connection, and implement connection limits.

### Q15: What is the memory impact of WebSocket connections?
**Answer:** Each connection uses ~10-50KB memory. 10,000 connections = ~100-500MB. Monitor memory usage and set appropriate limits.

### Q16: How do you handle WebSocket connections in Docker/Kubernetes?
**Answer:** Use sticky sessions, set appropriate resource limits, configure health checks, and use horizontal pod autoscaler based on connection count.

### Q17: How do you handle WebSocket connection draining during deployment?
**Answer:** Stop accepting new connections, wait for existing connections to close (with timeout), then shut down. Use preStop hooks in Kubernetes.

### Q18: What is the difference between WebSocket close codes?
**Answer:** 1000: Normal. 1001: Going away. 1008: Policy violation. 1009: Message too big. 1011: Internal error. Use appropriate codes for different scenarios.

### Q19: How do you test WebSocket connections in production?
**Answer:** Use load testing tools (k6, Artillery), monitor metrics, implement health checks, and use canary deployments.

### Q20: What are common production issues with WebSockets?
**Answer:** Connection leaks, memory exhaustion, message loss during failover, load balancer misconfiguration, and NAT/firewall timeouts.
