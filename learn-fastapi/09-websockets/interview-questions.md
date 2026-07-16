# WebSocket Interview Questions

## Table of Contents
1. [Fundamentals](#fundamentals)
2. [Implementation](#implementation)
3. [Rooms and Broadcasting](#rooms-and-broadcasting)
4. [Authentication](#authentication)
5. [Scaling & Distribution](#scaling--distribution)
6. [Connection Management](#connection-management)
7. [Heartbeat & Reconnection](#heartbeat--reconnection)
8. [Security](#security)
9. [Production Deployment](#production-deployment)
10. [WebSocket vs SSE](#websocket-vs-sse)
11. [Scenario-Based](#scenario-based)

---

## Fundamentals

### Q1: What are WebSockets and how do they differ from HTTP?
**Answer:** WebSockets provide full-duplex, bidirectional communication over a single TCP connection. Unlike HTTP's request-response model, both client and server can send messages at any time with low latency. The connection is established via an HTTP upgrade handshake, then switches to the WebSocket protocol (RFC 6455) for persistent communication.

Key differences:
- HTTP: Request-response, stateless, header overhead on every request, connection per request (HTTP/1.1) or multiplexed (HTTP/2)
- WebSocket: Bidirectional, persistent connection, minimal frame overhead (2-14 bytes vs hundreds of bytes for HTTP headers), server can push to client

### Q2: When should you use WebSockets over REST APIs or SSE?
**Answer:** Use WebSockets for:
- Real-time bidirectional communication (chat, gaming, collaborative editing)
- Low-latency updates where both sides need to initiate messages
- Applications requiring sub-100ms message delivery
- Stateful connections with ongoing dialogue

Use REST for:
- Traditional CRUD operations
- One-time data fetches
- Caching-friendly workloads
- Simple request-response patterns

Use SSE for:
- Server-to-client streaming (live feeds, notifications)
- Simpler implementation when bidirectional isn't needed
- Better HTTP infrastructure compatibility

### Q3: What is the WebSocket handshake and what can go wrong?
**Answer:** The client sends an HTTP upgrade request with headers: `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key`, `Sec-WebSocket-Version: 13`. The server responds with `101 Switching Protocols` and `Sec-WebSocket-Accept`. After this, the connection switches to WebSocket protocol.

Common failures:
- Load balancer stripping Upgrade headers
- Proxy servers not supporting HTTP upgrade
- CORS issues during handshake
- Authentication failing before upgrade
- TLS termination issues with wss://

### Q4: What are WebSocket frames and their overhead?
**Answer:** WebSocket frames are the units of data transmission. They contain:
- Fin bit (1 byte): indicates final fragment
- Opcode (1 byte): text (0x01), binary (0x02), close/ping/pong (0x08/0x9/0xA)
- Mask bit + payload length (1-9 bytes): 0-125 bytes inline, 126=2-byte extended, 127=8-byte extended
- Masking key (0 or 4 bytes): client-to-server masking
- Payload data (0-2^63 bytes)

Total overhead: 2-14 bytes per frame vs 200+ bytes for HTTP headers. This makes WebSockets efficient for frequent small messages.

### Q5: What is the difference between WebSocket and HTTP/2 Server Push?
**Answer:** HTTP/2 Server Push is limited: server can push resources the client hasn't requested yet, but it's still fundamentally request-response. The client initiates all communication. WebSocket provides true bidirectional communication where either side can send at any time. HTTP/2 multiplexing shares the TCP connection but doesn't provide persistent bidirectional streams.

### Q6: What protocols do WebSockets use for security?
**Answer:** `ws://` (unencrypted) and `wss://` (encrypted/TLS). Always use wss:// in production. WebSocket security also includes: Origin validation, authentication tokens, rate limiting, message size limits, and input validation. The WebSocket protocol itself has no built-in security beyond framing.

---

## Implementation

### Q7: How do you create a WebSocket endpoint in FastAPI?
**Answer:** Use the `@app.websocket("/path")` decorator with an async function accepting a WebSocket object:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
```

### Q8: How do you implement a ConnectionManager?
**Answer:** A ConnectionManager tracks active connections, handles connect/disconnect, and provides broadcasting:

```python
from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = set()
        self.active_connections[room].add(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active_connections:
            self.active_connections[room].discard(websocket)

    async def broadcast(self, message: str, room: str):
        if room in self.active_connections:
            dead = set()
            for connection in self.active_connections[room]:
                try:
                    await connection.send_text(message)
                except Exception:
                    dead.add(connection)
            self.active_connections[room] -= dead

    def get_room_count(self, room: str) -> int:
        return len(self.active_connections.get(room, set()))
```

### Q9: How do you handle WebSocket JSON messages with validation?
**Answer:** Use Pydantic models for validation:

```python
from pydantic import BaseModel, ValidationError

class WSMessage(BaseModel):
    type: str
    payload: dict

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            raw = await websocket.receive_json()
            message = WSMessage(**raw)

            if message.type == "chat":
                await handle_chat(websocket, message.payload)
            elif message.type == "ping":
                await websocket.send_json({"type": "pong"})
        except ValidationError as e:
            await websocket.send_json({"type": "error", "detail": str(e)})
        except WebSocketDisconnect:
            break
```

### Q10: How do you send binary data over WebSocket?
**Answer:** Use `send_bytes()` and `receive_bytes()` for binary data. Useful for file transfers, images, or custom binary protocols:

```python
@app.websocket("/ws/binary")
async def binary_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        processed = process_binary(data)
        await websocket.send_bytes(processed)
```

### Q11: How do you implement WebSocket query parameters and path parameters?
**Answer:** Path parameters work like HTTP endpoints. Query parameters use Query():

```python
@app.websocket("/ws/{room_id}")
async def ws_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(None),
):
    if token:
        user = await verify_token(token)
    await websocket.accept()
```

### Q12: How do you handle WebSocket close codes?
**Answer:** Close codes indicate why the connection was closed:

```python
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect as e:
        # e.code: 1000=normal, 1001=going away, 1002=protocol error,
        # 1003=unsupported, 1006=abnormal, 1008=policy, 1009=too big
        if e.code == 1006:
            logger.warning("Abnormal WebSocket closure")
```

### Q13: How do you implement WebSocket middleware in FastAPI?
**Answer:** BaseHTTPMiddleware doesn't handle WebSockets. Use pure ASGI middleware:

```python
class WebSocketAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            token = self._extract_token(scope)
            if not token:
                await send({"type": "websocket.close", "code": 1008})
                return
            user = await verify_ws_token(token)
            scope["user"] = user
        return await self.app(scope, receive, send)
```

---

## Rooms and Broadcasting

### Q14: How do you implement WebSocket rooms?
**Answer:** Rooms are logical groupings managed by ConnectionManager:

```python
class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    async def join(self, room: str, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if room not in self.rooms:
            self.rooms[room] = {}
        self.rooms[room][user_id] = websocket
        await self.broadcast(room, {"type": "join", "user_id": user_id})

    async def leave(self, room: str, user_id: str):
        if room in self.rooms and user_id in self.rooms[room]:
            del self.rooms[room][user_id]
            if not self.rooms[room]:
                del self.rooms[room]

    async def broadcast(self, room: str, message: dict, exclude: str = None):
        if room in self.rooms:
            dead = []
            for uid, ws in self.rooms[room].items():
                if uid != exclude:
                    try:
                        await ws.send_json(message)
                    except Exception:
                        dead.append(uid)
            for uid in dead:
                del self.rooms[room][uid]
```

### Q15: How do you broadcast messages to all users efficiently?
**Answer:** For single-server, iterate through connections. For multi-server, use Redis pub/sub:

```python
import asyncio

async def broadcast_all(manager: RoomManager, message: dict):
    tasks = []
    for room_id, users in manager.rooms.items():
        for user_id, ws in users.items():
            tasks.append(safe_send(ws, message))
    await asyncio.gather(*tasks, return_exceptions=True)

async def safe_send(ws: WebSocket, message: dict):
    try:
        await ws.send_json(message)
    except Exception:
        pass
```

### Q16: How do you implement Redis pub/sub for scaled WebSockets?
**Answer:** Each server instance subscribes to Redis channels for message distribution:

```python
import redis.asyncio as redis

class RedisPubSubManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()

    async def subscribe(self, channel: str, callback):
        await self.pubsub.subscribe(channel)
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                await callback(message["data"])

    async def publish(self, channel: str, message: str):
        await self.redis.publish(channel, message)

    async def broadcast_to_room(self, room_id: str, message: str, local_connections):
        await self.publish(f"room:{room_id}", message)
        for ws in local_connections:
            try:
                await ws.send_text(message)
            except Exception:
                pass
```

### Q17: How do you implement typing indicators?
**Answer:** Broadcast typing events with timeout:

```python
import asyncio

class TypingManager:
    def __init__(self):
        self.typing_users: Dict[str, Set[str]] = {}
        self.timers: Dict[str, asyncio.Task] = {}

    async def start_typing(self, room: str, user_id: str, broadcast_func):
        if room not in self.typing_users:
            self.typing_users[room] = set()
        self.typing_users[room].add(user_id)

        await broadcast_func(room, {"type": "typing", "user_id": user_id, "is_typing": True})

        key = f"{room}:{user_id}"
        if key in self.timers:
            self.timers[key].cancel()

        self.timers[key] = asyncio.create_task(
            self._stop_after(room, user_id, broadcast_func)
        )

    async def _stop_after(self, room, user_id, broadcast_func):
        await asyncio.sleep(3)
        await self.stop_typing(room, user_id, broadcast_func)

    async def stop_typing(self, room, user_id, broadcast_func):
        if room in self.typing_users:
            self.typing_users[room].discard(user_id)
        await broadcast_func(room, {"type": "typing", "user_id": user_id, "is_typing": False})
```

### Q18: How do you store and retrieve message history?
**Answer:** Use Redis for recent messages, database for persistence:

```python
class MessageStore:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def save(self, room_id: str, message: dict):
        await self.redis.lpush(f"room:{room_id}:messages", json.dumps(message))
        await self.redis.ltrim(f"room:{room_id}:messages", 0, 99)
        await db.messages.insert(message)

    async def get_history(self, room_id: str, limit: int = 50) -> list:
        messages = await self.redis.lrange(f"room:{room_id}:messages", 0, limit - 1)
        return [json.loads(m) for m in reversed(messages)]

    async def get_history_since(self, room_id: str, since_message_id: str) -> list:
        messages = await self.get_history(room_id, limit=200)
        return [m for m in messages if m["id"] > since_message_id]
```

---

## Authentication

### Q19: Why is WebSocket authentication different from HTTP?
**Answer:** Browsers don't support custom headers in the WebSocket API. The `new WebSocket()` constructor cannot set Authorization headers. This means traditional Bearer token authentication can't be used during the initial handshake, requiring alternative approaches.

### Q20: What are the common ways to authenticate WebSocket connections?
**Answer:**

**Token in query parameters** (simplest, less secure):
```python
@app.websocket("/ws")
async def ws(websocket: WebSocket, token: str = Query(...)):
    user = await verify_token(token)
    await websocket.accept()
```

**Token in first message** (more secure):
```python
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    auth_msg = await websocket.receive_json()
    if auth_msg.get("type") != "auth":
        await websocket.close(code=1008)
        return
    user = await verify_token(auth_msg["token"])
```

**Cookie-based** (for same-origin):
```python
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    session_id = websocket.cookies.get("session_id")
    user = await verify_session(session_id)
    await websocket.accept()
```

**Ticket-based** (most secure):
```python
@app.get("/ws-ticket")
async def get_ws_ticket(user = Depends(get_current_user)):
    ticket = await create_short_lived_ticket(user.id)
    return {"ticket": ticket}

@app.websocket("/ws")
async def ws(websocket: WebSocket, ticket: str = Query(...)):
    user = await verify_ticket(ticket)
    await websocket.accept()
```

### Q21: What are the security risks of tokens in query parameters?
**Answer:** Tokens in URLs are visible in:
- Server access logs
- Browser history
- Proxy logs
- Referrer headers
- Network monitoring tools

Mitigations:
- Use HTTPS/WSS only
- Use short-lived tokens (minutes, not hours)
- Don't log query parameters in access logs
- Prefer ticket-based auth for production
- Rotate tokens frequently

### Q22: How do you validate WebSocket connections before accepting?
**Answer:** Extract and validate the token BEFORE calling accept():

```python
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Missing token")
        return

    user = await verify_token(token)
    if not user:
        await websocket.close(code=1008, reason="Invalid token")
        return

    await websocket.accept()
    websocket.scope["user"] = user
```

### Q23: How do you handle token refresh for long-lived WebSocket connections?
**Answer:** Tokens may expire during a WebSocket session. Options:

1. **Reconnect with fresh token**: Client detects 401/1008, refreshes token via HTTP, reconnects
2. **Proactive refresh**: Client refreshes token before expiry via HTTP, sends new token over WebSocket
3. **Long-lived session tokens**: Use session-based auth instead of JWT
4. **Token exchange**: Server issues long-lived WebSocket tokens after initial auth

```python
@app.websocket("/ws")
async def ws(websocket: WebSocket, token: str = Query(...)):
    user = await verify_token(token)
    await websocket.accept()

    async def token_refresher():
        while True:
            await asyncio.sleep(300)
            new_token = await refresh_token(user.id)
            await websocket.send_json({"type": "token_refresh", "token": new_token})

    asyncio.create_task(token_refresher())
```

---

## Scaling & Distribution

### Q24: How do you scale WebSocket connections across multiple instances?
**Answer:** Use Redis pub/sub for message distribution, sticky sessions for connection routing, and shared state in Redis:

```python
redis_pubsub = RedisPubSubManager(settings.REDIS_URL)

async def handle_message(websocket, message):
    result = process_message(message)
    await redis_pubsub.publish(f"room:{room_id}", json.dumps(result))

async def room_listener(room_id, local_connections):
    async for message in redis_pubsub.subscribe(f"room:{room_id}"):
        for ws in local_connections:
            await ws.send_text(message)
```

### Q25: What are sticky sessions and why are they needed?
**Answer:** Sticky sessions route all requests from a client to the same server instance. Needed because WebSocket connections are persistent and state is stored locally (in-memory connection maps). Without sticky sessions, a client might connect to instance A but subsequent HTTP requests go to instance B, losing context.

Configuration:
- Nginx: `ip_hash` or `sticky` directive
- AWS ALB: Enable stickiness with target group
- Kubernetes: Use `sessionAffinity: ClientIP`

### Q26: Why are heartbeats important for WebSocket connections?
**Answer:** They detect dead connections (zombie connections that consume resources), keep connections alive through NAT/firewalls (which timeout idle connections), and allow monitoring connection health. Without heartbeats, zombie connections accumulate and exhaust server resources.

```python
async def heartbeat_handler(websocket: WebSocket):
    while True:
        try:
            await websocket.send_json({"type": "ping"})
            pong = await asyncio.wait_for(
                websocket.receive_json(), timeout=30
            )
            if pong.get("type") != "pong":
                await websocket.close(code=1008)
                break
        except asyncio.TimeoutError:
            await websocket.close(code=1000)
            break
```

### Q27: How do you handle WebSocket connections across multiple data centers?
**Answer:** Use global Redis for cross-DC message distribution, or use a global message broker (Kafka). Route users to nearest DC for low latency. Accept that cross-DC messages have higher latency. Use conflict resolution for concurrent edits.

### Q28: What is the maximum number of WebSocket connections a server can handle?
**Answer:** Theoretical limit: one TCP connection per file descriptor. Practical limit depends on:
- Memory per connection (~10-50KB) → 10K-100K connections per server
- CPU for message processing
- File descriptor limits (ulimit -n, default 1024)
- Network bandwidth

Typical production numbers: 10K-50K concurrent connections per server. Scale horizontally with Redis pub/sub.

```bash
# Increase file descriptor limits
ulimit -n 65536

# Linux kernel tuning
sysctl -w net.core.somaxconn=65535
sysctl -w net.ipv4.ip_local_port_range="1024 65535"
```

---

## Connection Management

### Q29: How do you handle WebSocket disconnections gracefully?
**Answer:**

```python
@app.websocket("/ws/{user_id}")
async def ws(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, room="general")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, room="general")
    except WebSocketDisconnect:
        manager.disconnect(websocket, room="general")
        await manager.broadcast(
            json.dumps({"type": "leave", "user_id": user_id}),
            room="general"
        )
    except Exception as e:
        logger.exception("WebSocket error", user_id=user_id, error=str(e))
        manager.disconnect(websocket, room="general")
```

### Q30: How do you implement connection limits?
**Answer:**

```python
class ConnectionLimiter:
    def __init__(self, max_per_user=5, max_total=10000):
        self.user_counts: Dict[str, int] = {}
        self.total = 0
        self.max_per_user = max_per_user
        self.max_total = max_total

    def can_connect(self, user_id: str) -> bool:
        user_count = self.user_counts.get(user_id, 0)
        if user_count >= self.max_per_user:
            return False
        if self.total >= self.max_total:
            return False
        return True

    def on_connect(self, user_id: str):
        self.user_counts[user_id] = self.user_counts.get(user_id, 0) + 1
        self.total += 1

    def on_disconnect(self, user_id: str):
        self.user_counts[user_id] = self.user_counts.get(user_id, 1) - 1
        if self.user_counts[user_id] <= 0:
            del self.user_counts[user_id]
        self.total -= 1
```

### Q31: How do you implement connection state tracking?
**Answer:** Store connection metadata in Redis for distributed tracking:

```python
class ConnectionTracker:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def register(self, user_id: str, server_id: str, metadata: dict):
        key = f"ws:conn:{user_id}"
        await self.redis.hset(key, mapping={
            "server_id": server_id,
            "connected_at": datetime.utcnow().isoformat(),
            "metadata": json.dumps(metadata),
        })
        await self.redis.expire(key, 3600)

    async def unregister(self, user_id: str):
        await self.redis.delete(f"ws:conn:{user_id}")

    async def get_connection_info(self, user_id: str) -> dict:
        data = await self.redis.hgetall(f"ws:conn:{user_id}")
        return {k.decode(): v.decode() for k, v in data.items()}
```

---

## Heartbeat & Reconnection

### Q32: How do you implement server-side heartbeat?
**Answer:**

```python
async def websocket_with_heartbeat(websocket: WebSocket):
    await websocket.accept()
    heartbeat_task = asyncio.create_task(heartbeat(websocket))

    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        heartbeat_task.cancel()
    finally:
        heartbeat_task.cancel()

async def heartbeat(websocket: WebSocket, interval: int = 30):
    while True:
        await asyncio.sleep(interval)
        try:
            await websocket.send_json({"type": "ping"})
        except Exception:
            break
```

### Q33: How do you implement client-side reconnection with state sync?
**Answer:**

```javascript
class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.reconnectAttempts = 0;
        this.lastMessageId = null;
        this.maxReconnectDelay = 30000;
    }

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            this.reconnectAttempts = 0;
            if (this.lastMessageId) {
                this.ws.send(JSON.stringify({
                    type: "sync",
                    last_message_id: this.lastMessageId
                }));
            }
        };

        this.ws.onclose = () => {
            const delay = Math.min(
                1000 * Math.pow(2, this.reconnectAttempts),
                this.maxReconnectDelay
            );
            this.reconnectAttempts++;
            setTimeout(() => this.connect(), delay);
        };

        this.ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            this.lastMessageId = msg.id;
        };
    }
}
```

### Q34: How do you detect and clean up zombie connections?
**Answer:** Use heartbeat with timeout detection:

```python
class ZombieDetector:
    def __init__(self, timeout: int = 90):
        self.last_seen: Dict[str, float] = {}
        self.timeout = timeout

    def mark_alive(self, connection_id: str):
        self.last_seen[connection_id] = time.time()

    def is_zombie(self, connection_id: str) -> bool:
        last = self.last_seen.get(connection_id, 0)
        return time.time() - last > self.timeout

    async def cleanup_loop(self, manager: ConnectionManager):
        while True:
            await asyncio.sleep(30)
            for conn_id in list(self.last_seen.keys()):
                if self.is_zombie(conn_id):
                    await manager.force_disconnect(conn_id)
                    del self.last_seen[conn_id]
```

---

## Security

### Q35: What security measures are needed for WebSocket connections?
**Answer:**
- **WSS (TLS)**: Always use encrypted connections in production
- **Origin validation**: Check the Origin header to prevent cross-site WebSocket hijacking
- **Authentication**: Validate tokens before accepting connections
- **Rate limiting**: Limit connection attempts per IP/user
- **Input validation**: Validate all incoming messages (type, size, content)
- **Message size limits**: Prevent memory exhaustion from large messages
- **Connection limits**: Per-server, per-user, per-room
- **Content-Type validation**: Ensure proper message format

### Q36: How do you prevent WebSocket DoS attacks?
**Answer:**

```python
class WebSocketRateLimiter:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def check_connection_rate(self, ip: str) -> bool:
        key = f"ws:rate:{ip}"
        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, 60)
        return count <= 10

    async def check_message_rate(self, user_id: str) -> bool:
        key = f"ws:msg:{user_id}"
        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, 1)
        return count <= 100
```

Additional protections:
- Maximum message size (e.g., 64KB)
- Maximum connection duration
- CAPTCHA for connection establishment
- IP-based blocking for abuse

### Q37: How do you prevent cross-site WebSocket hijacking?
**Answer:** Validate the Origin header during handshake:

```python
ALLOWED_ORIGINS = {"https://app.example.com", "https://admin.example.com"}

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    origin = websocket.headers.get("origin", "")
    if origin not in ALLOWED_ORIGINS:
        await websocket.close(code=1008)
        return

    await websocket.accept()
```

---

## Production Deployment

### Q38: How do you configure Nginx for WebSocket connections?
**Answer:**

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

location /ws/ {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;

    proxy_buffering off;
    proxy_read_timeout 86400s;
    proxy_send_timeout 86400s;

    proxy_set_header Connection $connection_upgrade;
}
```

### Q39: How do you implement graceful shutdown for WebSocket servers?
**Answer:**

```python
import signal

class GracefulWebSocketServer:
    def __init__(self):
        self.connections: Set[WebSocket] = set()
        self.shutting_down = False

    async def shutdown(self):
        self.shutting_down = True
        for ws in list(self.connections):
            try:
                await ws.send_json({"type": "server_shutdown", "reason": "Deployment"})
                await ws.close(code=1001, reason="Server shutting down")
            except Exception:
                pass
        await asyncio.sleep(5)

    def setup_signals(self, loop):
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.shutdown()))
```

### Q40: How do you monitor WebSocket connections in production?
**Answer:** Track key metrics with Prometheus:

```python
from prometheus_client import Counter, Gauge, Histogram

ws_connections = Gauge("ws_active_connections", "Active WebSocket connections")
ws_messages_sent = Counter("ws_messages_sent_total", "Messages sent", ["type"])
ws_message_size = Histogram("ws_message_size_bytes", "Message size", ["direction"])
ws_errors = Counter("ws_errors_total", "WebSocket errors", ["error_type"])
ws_connection_duration = Histogram("ws_connection_duration_seconds", "Connection duration")
```

Metrics to track:
- Connection count (per server, per room)
- Message rate (messages/second)
- Message size distribution
- Error rate (failed sends, disconnects)
- Memory usage per connection
- Latency (time from send to delivery)

### Q41: How do you handle WebSocket load balancing?
**Answer:**
- Use sticky sessions (ALB, Nginx ip_hash)
- For message broadcasting: Redis pub/sub across instances
- For connection state: Redis shared state
- For presence: Redis with TTL
- Consider dedicated WebSocket servers separate from HTTP API servers
- Use connection draining during deployments

---

## WebSocket vs SSE

### Q42: When should you choose SSE over WebSockets?
**Answer:**

| Feature | WebSocket | SSE |
|---------|-----------|-----|
| Direction | Bidirectional | Server-to-client only |
| Protocol | Custom (ws://) | HTTP |
| Reconnection | Manual | Built-in |
| Event IDs | Manual | Built-in |
| HTTP/2 | Separate connection | Multiplexed |
| Proxy support | Sometimes problematic | Works through proxies |
| Maximum connections | ~65K per domain | ~6 HTTP/2 connections |
| Load balancer | Needs sticky sessions | Standard HTTP LB |
| Browser support | Modern browsers | Modern browsers (EventSource) |

Choose SSE when:
- Server needs to push updates to client (notifications, live feeds)
- You want automatic reconnection
- HTTP infrastructure compatibility matters
- You don't need client-to-server real-time

Choose WebSocket when:
- Both sides need to send messages in real-time
- Low latency bidirectional communication
- Binary data transfer needed
- Gaming or collaborative editing

### Q43: How do you implement SSE with FastAPI?
**Answer:**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

@app.get("/events")
async def event_stream():
    async def generate():
        while True:
            data = {"message": "update", "timestamp": time.time()}
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )
```

---

## Scenario-Based

### Q44: Design a real-time chat application with WebSockets.
**Answer:** Use ConnectionManager for room management, Redis pub/sub for scaling, message history in Redis/database, authentication on connect (ticket-based), typing indicators, presence system, and read receipts. Implement message ordering with sequence numbers. Use separate channels for different event types (messages, presence, typing).

### Q45: How do you implement a live notification system?
**Answer:** Create per-user WebSocket connections. When an event occurs, find the user's connection(s) and send the notification. Store pending notifications in Redis for offline users. On reconnect, deliver missed notifications. Use different channels for notification types (mentions, follows, system).

```python
class NotificationManager:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def send_notification(self, user_id: str, notification: dict):
        # Try online delivery first
        if await self.is_online(user_id):
            await self.deliver_to_user(user_id, notification)
        else:
            # Store for later delivery
            await self.redis.lpush(
                f"notifications:{user_id}",
                json.dumps(notification)
            )

    async def on_connect(self, user_id: str):
        # Deliver pending notifications
        pending = await self.redis.lrange(f"notifications:{user_id}", 0, -1)
        for notif in reversed(pending):
            await self.deliver_to_user(user_id, json.loads(notif))
        await self.redis.delete(f"notifications:{user_id}")
```

### Q46: How do you implement collaborative editing with WebSockets?
**Answer:** Use Operational Transformation (OT) or CRDTs for conflict resolution. Broadcast operations to all connected editors. Handle concurrent edits with sequence numbers and transformation. Persist document state periodically. Implement undo/redo with operation history.

### Q47: How do you handle WebSocket connections in a microservices architecture?
**Answer:** Use a dedicated WebSocket gateway service. Other services publish events to Kafka/Redis. WebSocket gateway subscribes and delivers to connected clients. Each service doesn't manage WebSocket connections directly. The gateway handles authentication, connection management, and message routing.

### Q48: How do you implement a real-time dashboard with WebSockets?
**Answer:**

```python
@app.websocket("/ws/dashboard")
async def dashboard_ws(websocket: WebSocket, token: str = Query(...)):
    user = await verify_token(token)
    await websocket.accept()

    # Subscribe to relevant data channels
    channels = get_user_channels(user)

    async def listen_redis():
        pubsub = redis.pubsub()
        await pubsub.subscribe(*channels)
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_json(json.loads(message["data"]))

    redis_task = asyncio.create_task(listen_redis())

    try:
        while True:
            data = await websocket.receive_json()
            # Handle client messages (filter changes, subscriptions)
            if data["type"] == "subscribe":
                await redis_task  # Handle subscription changes
    except WebSocketDisconnect:
        redis_task.cancel()
```

### Q49: How do you test WebSocket functionality?
**Answer:** Use WebSocket client libraries (websockets, websocket-client) for unit tests. Test: connection establishment, message send/receive, disconnection handling, authentication, room management, broadcasting, and error handling. Load test with tools like k6 or Artillery. Test reconnection behavior and message delivery guarantees.

```python
import websockets
import pytest

@pytest.mark.asyncio
async def test_websocket_echo():
    async with websockets.connect("ws://localhost:8000/ws/test") as ws:
        await ws.send("Hello")
        response = await ws.recv()
        assert response == "Echo: Hello"

@pytest.mark.asyncio
async def test_websocket_auth():
    # Should reject unauthenticated connection
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        response = await ws.recv()
        assert "error" in response.lower()
```

### Q50: How do you handle message ordering guarantees in WebSockets?
**Answer:** Use sequence numbers attached to each message. Clients can detect gaps and request retransmission. Server maintains a message log with sequence numbers. On reconnection, client sends last received sequence number and server sends missed messages. For strict ordering, use a single partition per room (limits throughput but guarantees order).

```python
class OrderedMessageManager:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def send_ordered(self, room_id: str, message: dict):
        seq = await self.redis.incr(f"room:{room_id}:seq")
        message["seq"] = seq
        await self.redis.lpush(f"room:{room_id}:log", json.dumps(message))
        await self.redis.ltrim(f"room:{room_id}:log", 0, 9999)
        await self.broadcast(room_id, message)

    async def get_missed_messages(self, room_id: str, since_seq: int) -> list:
        log = await self.redis.lrange(f"room:{room_id}:log", 0, -1)
        messages = [json.loads(m) for m in reversed(log)]
        return [m for m in messages if m["seq"] > since_seq]
```
