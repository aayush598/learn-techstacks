# WebSocket Authentication

## Table of Contents
1. [Authentication Challenges](#authentication-challenges)
2. [Token Validation on Connect](#token-validation-on-connect)
3. [Token in Query Parameters](#token-in-query-parameters)
4. [Token in First Message](#token-in-first-message)
5. [Session Management](#session-management)
6. [Reconnection Handling](#reconnection-handling)
7. [WebSocket Middleware](#websocket-middleware)
8. [Security Best Practices](#security-best-practices)
9. [Interview Questions](#interview-questions)

---

## Authentication Challenges

WebSockets don't support custom headers during the initial HTTP upgrade in browsers, making traditional header-based authentication impossible. This requires alternative approaches.

### Why It's Different

```python
# HTTP: Can use Authorization header
headers = {"Authorization": "Bearer token123"}
response = httpx.get("https://api.example.com/data", headers=headers)

# WebSocket: Can't set custom headers in browser WebSocket API
ws = WebSocket("wss://api.example.com/ws")  # No headers option!
```

### Common Solutions

1. **Query parameter**: Pass token in URL
2. **Cookie-based**: Use session cookies
3. **First message**: Send token as first WebSocket message
4. **Ticket system**: Generate temporary ticket for WebSocket connection

---

## Token Validation on Connect

### Basic Token Validation

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from jose import JWTError, jwt

app = FastAPI()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    # Validate token before accepting
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)  # Policy Violation
        return

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{user['sub']}: {data}")
    except WebSocketDisconnect:
        pass
```

### JWT Validation with User Data

```python
from fastapi import FastAPI, WebSocket, Query
from jose import JWTError, jwt
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str

async def get_user_from_token(token: str) -> User | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None

        # Fetch user from database
        user = await get_user_by_id(user_id)
        return user
    except JWTError:
        return None

@app.websocket("/ws/{room_id}")
async def authenticated_websocket(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
):
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    # Store user in WebSocket state
    websocket.state.user = user
    websocket.state.room_id = room_id

    try:
        while True:
            data = await websocket.receive_text()
            # User is authenticated
            await broadcast(room_id, f"{user.name}: {data}")
    except WebSocketDisconnect:
        pass
```

---

## Token in Query Parameters

### Pros and Cons

```python
# PROS:
# - Works with browser WebSocket API
# - Simple implementation
# - Token validated before connection

# CONS:
# - Token visible in URL (logs, browser history)
# - Less secure than headers
# - Limited token size

@app.websocket("/ws")
async def ws_with_query_token(
    websocket: WebSocket,
    token: str = Query(...),
):
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    # ...
```

### Mitigating URL Exposure

```python
# Use short-lived tokens for WebSocket connections
# Use HTTPS to prevent network sniffing
# Log token only in masked form

@app.websocket("/ws")
async def ws_secure_token(
    websocket: WebSocket,
    token: str = Query(...),
):
    # Log masked token
    masked_token = token[:4] + "..." + token[-4:]
    logger.info(f"WebSocket connection with token: {masked_token}")

    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    # ...
```

---

## Token in First Message

### Implementation

```python
@app.websocket("/ws")
async def ws_token_in_message(websocket: WebSocket):
    await websocket.accept()

    # Wait for first message with token
    try:
        first_message = await websocket.receive_text()
        data = json.loads(first_message)

        if data.get("type") != "auth" or "token" not in data:
            await websocket.send_text(json.dumps({"type": "error", "message": "Authentication required"}))
            await websocket.close(code=1008)
            return

        user = verify_token(data["token"])
        if not user:
            await websocket.send_text(json.dumps({"type": "error", "message": "Invalid token"}))
            await websocket.close(code=1008)
            return

        # Send auth success
        await websocket.send_text(json.dumps({"type": "auth_success", "user_id": user["sub"]}))

        # Now handle regular messages
        while True:
            msg = await websocket.receive_text()
            # Process message...
    except WebSocketDisconnect:
        pass
```

### Client Implementation

```javascript
const ws = new WebSocket("wss://api.example.com/ws");

ws.onopen = () => {
    // Send auth message first
    ws.send(JSON.stringify({
        type: "auth",
        token: "jwt-token-here"
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "auth_success") {
        // Now can send regular messages
        ws.send(JSON.stringify({type: "chat", content: "Hello!"}));
    }
};
```

---

## Cookie-Based Authentication

### Using Session Cookies

```python
from fastapi import FastAPI, WebSocket, Cookie
from typing import Optional

app = FastAPI()

@app.websocket("/ws")
async def ws_cookie_auth(
    websocket: WebSocket,
    session_id: Optional[str] = Cookie(None),
):
    if not session_id:
        await websocket.close(code=1008)
        return

    user = await get_user_by_session(session_id)
    if not user:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    # ...
```

### WebSocket with Cookie from FastAPI

```python
# Browser automatically sends cookies with WebSocket connections
# if the WebSocket is on the same domain

@app.get("/login")
async def login(response: Response):
    # Set session cookie
    response.set_cookie(
        "session_id",
        "abc123",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return {"message": "Logged in"}

@app.websocket("/ws")
async def ws_with_cookie(websocket: WebSocket):
    # Cookie is available automatically
    session_id = websocket.cookies.get("session_id")
    # ...
```

---

## Session Management

### Session Store

```python
import redis.asyncio as redis

class WebSocketSessionManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def create_session(
        self,
        user_id: str,
        websocket: WebSocket,
        ttl: int = 3600,
    ) -> str:
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "connected_at": time.time(),
            "last_active": time.time(),
        }

        await self.redis.hset(
            f"ws:session:{session_id}",
            mapping=session_data,
        )
        await self.redis.expire(f"ws:session:{session_id}", ttl)

        return session_id

    async def get_session(self, session_id: str) -> dict | None:
        data = await self.redis.hgetall(f"ws:session:{session_id}")
        return data if data else None

    async def delete_session(self, session_id: str):
        await self.redis.delete(f"ws:session:{session_id}")

    async def update_activity(self, session_id: str):
        await self.redis.hset(
            f"ws:session:{session_id}",
            "last_active",
            time.time(),
        )
```

### Session-Based WebSocket

```python
@app.websocket("/ws")
async def ws_with_session(
    websocket: WebSocket,
    token: str = Query(...),
):
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    # Create session
    session_id = await session_manager.create_session(
        user_id=user["sub"],
        websocket=websocket,
    )

    try:
        while True:
            data = await websocket.receive_text()
            await session_manager.update_activity(session_id)
            # Process message...
    except WebSocketDisconnect:
        await session_manager.delete_session(session_id)
```

---

## Reconnection Handling

### Token Refresh for Reconnection

```python
@app.websocket("/ws")
async def ws_reconnection(
    websocket: WebSocket,
    token: str = Query(...),
    last_message_id: str = Query(None),
):
    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    # If reconnecting, send missed messages
    if last_message_id:
        missed_messages = await get_messages_since(last_message_id)
        for msg in missed_messages:
            await websocket.send_text(json.dumps(msg))

    try:
        while True:
            data = await websocket.receive_text()
            # Process and store message
            msg_id = await store_message(data, user["sub"])
            await websocket.send_text(json.dumps({"id": msg_id, "data": data}))
    except WebSocketDisconnect:
        pass
```

### Client-Side Reconnection

```javascript
class WebSocketClient {
    constructor(url, getToken) {
        this.url = url;
        this.getToken = getToken;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.lastMessageId = null;
    }

    connect() {
        const token = this.getToken();
        const ws = new WebSocket(
            `${this.url}?token=${token}&last_message_id=${this.lastMessageId || ""}`
        );

        ws.onopen = () => {
            this.reconnectAttempts = 0;
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.lastMessageId = data.id;
        };

        ws.onclose = () => {
            this.reconnect();
        };

        this.ws = ws;
    }

    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            const delay = Math.pow(2, this.reconnectAttempts) * 1000;
            this.reconnectAttempts++;
            setTimeout(() => this.connect(), delay);
        }
    }
}
```

---

## WebSocket Middleware

### Authentication Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.websockets import WebSocket

class WebSocketAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            # Extract token from query params
            query_string = scope.get("query_string", b"").decode()
            params = dict(parse_qsl(query_string))
            token = params.get("token")

            if not token:
                # Reject connection
                response = WebSocket(scope, receive, send)
                await response.close(code=1008)
                return

            user = verify_token(token)
            if not user:
                response = WebSocket(scope, receive, send)
                await response.close(code=1008)
                return

            # Add user to scope
            scope["user"] = user

        await self.app(scope, receive, send)

# Usage
app = FastAPI()
app.add_middleware(WebSocketAuthMiddleware)
```

### Rate Limiting Middleware

```python
class WebSocketRateLimitMiddleware:
    def __init__(self, app, max_messages: int = 100, window: int = 60):
        self.app = app
        self.max_messages = max_messages
        self.window = window
        self.connections: dict[str, list[float]] = {}

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            # Rate limit check would go here
            # For WebSocket, we limit messages, not connections
            pass

        await self.app(scope, receive, send)
```

---

## Security Best Practices

### 1. Always Use WSS (WebSocket Secure)

```python
# Production: Use wss://
# Development: Can use ws:// for local testing

@app.websocket("/ws")
async def secure_ws(websocket: WebSocket):
    # In production, ensure HTTPS/WSS is used
    if not websocket.url.scheme == "wss":
        # Redirect or reject
        pass
```

### 2. Validate Origin

```python
@app.websocket("/ws")
async def validate_origin(websocket: WebSocket):
    origin = websocket.headers.get("origin")
    if origin not in ALLOWED_ORIGINS:
        await websocket.close(code=1008)
        return

    await websocket.accept()
```

### 3. Implement Rate Limiting

```python
class RateLimiter:
    def __init__(self, max_per_minute: int = 60):
        self.max_per_minute = max_per_minute
        self.messages: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        window_start = now - 60
        self.messages[user_id] = [
            t for t in self.messages[user_id] if t > window_start
        ]
        if len(self.messages[user_id]) >= self.max_per_minute:
            return False
        self.messages[user_id].append(now)
        return True
```

### 4. Sanitize Input

```python
import bleach

def sanitize_message(message: str) -> str:
    return bleach.clean(message, tags=[], strip=True)

@app.websocket("/ws")
async def safe_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        clean_data = sanitize_message(data)
        await websocket.send_text(f"Echo: {clean_data}")
```

### 5. Limit Message Size

```python
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB

@app.websocket("/ws")
async def limited_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if len(data) > MAX_MESSAGE_SIZE:
            await websocket.send_text("Message too large")
            continue
        # Process message
```

---

## Interview Questions

### Q1: Why is WebSocket authentication different from HTTP?
**Answer:** Browsers don't support custom headers in the WebSocket API. This means traditional Authorization headers can't be used during the initial handshake.

### Q2: What are the common ways to authenticate WebSocket connections?
**Answer:** Token in query parameters, token in first message, cookie-based authentication, and ticket-based systems (generate temporary ticket for connection).

### Q3: What are the security risks of passing tokens in query parameters?
**Answer:** Tokens are visible in URLs, logged in server access logs, visible in browser history, and potentially exposed in referrer headers. Mitigate with short-lived tokens and HTTPS.

### Q4: How do you validate a WebSocket connection before accepting it?
**Answer:** Extract the token from query params, validate it, and close with code 1008 if invalid. FastAPI's `websocket.accept()` can be called after validation.

### Q5: What is a ticket-based authentication system for WebSockets?
**Answer:** Client makes an HTTP request to get a short-lived ticket. The ticket is used once to establish a WebSocket connection. This avoids exposing the JWT in the URL.

### Q6: How do you handle token refresh for WebSocket connections?
**Answer:** The client refreshes the token via HTTP before the WebSocket token expires. If the WebSocket disconnects, the client reconnects with a fresh token.

### Q7: How do you handle session management for WebSockets?
**Answer:** Store session data in Redis with TTL. Update activity timestamp on each message. Clean up session on disconnect. Track connected users for broadcasting.

### Q8: What is reconnection handling in WebSockets?
**Answer:** When a WebSocket disconnects, the client attempts to reconnect with exponential backoff. Optionally send the last message ID to retrieve missed messages.

### Q9: How do you implement WebSocket middleware for authentication?
**Answer:** Use ASGI middleware to intercept WebSocket connections, extract and validate tokens from query params, and reject invalid connections before they're accepted.

### Q10: How do you secure WebSocket connections in production?
**Answer:** Use WSS (TLS), validate Origin headers, implement rate limiting, sanitize input, limit message size, and use short-lived authentication tokens.

### Q11: What is the difference between WebSocket and HTTP authentication?
**Answer:** HTTP uses Authorization headers. WebSocket can't use custom headers in browsers, so tokens go in query params, cookies, or the first message.

### Q12: How do you prevent Cross-Site WebSocket Hijacking?
**Answer:** Validate the Origin header against allowed origins. Use CSRF tokens. Ensure WebSocket connections are only initiated from trusted domains.

### Q13: Can you use OAuth with WebSockets?
**Answer:** Yes, but the OAuth flow happens via HTTP. The resulting access token is then passed to the WebSocket connection via query params or first message.

### Q14: How do you handle authentication failures in WebSocket middleware?
**Answer:** Close the connection with code 1008 (Policy Violation) and optionally send an error message before closing.

### Q15: What are WebSocket close codes?
**Answer:** 1000: Normal closure. 1001: Going away. 1008: Policy violation (auth failure). 1009: Message too big. 1011: Internal error.

### Q16: How do you implement WebSocket rate limiting?
**Answer:** Track messages per user/IP in Redis. Check count against limit before processing each message. Close connection or send error when limit exceeded.

### Q17: How do you handle multiple devices per user?
**Answer:** Store multiple connections per user ID in the connection manager. Broadcast messages to all user connections. Track connection metadata (device type, last active).

### Q18: What is the samesite cookie attribute's role in WebSocket auth?
**Answer:** `SameSite=Lax` cookies are sent with WebSocket connections from the same site. `SameSite=Strict` cookies may not be sent. Use `Lax` for WebSocket auth.

### Q19: How do you implement WebSocket connection limits?
**Answer:** Track active connections per user/IP in Redis. Reject new connections when the limit is reached. Close oldest connections if necessary.

### Q20: How do you log WebSocket authentication events?
**Answer:** Log connection attempts (success/failure), disconnections, and authentication errors. Include user ID, IP, and timestamp. Never log tokens.
