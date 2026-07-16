# WebSocket Basics in FastAPI

## Table of Contents
1. [What are WebSockets?](#what-are-websockets)
2. [WebSocket Endpoint](#websocket-endpoint)
3. [WebSocket Protocol](#websocket-protocol)
4. [Connect/Disconnect Events](#connectdisconnect-events)
5. [Sending/Receiving Data](#sendingreceiving-data)
6. [JSON over WebSocket](#json-over-websocket)
7. [Binary Data](#binary-data)
8. [WebSocket vs SSE vs Polling](#websocket-vs-sse-vs-polling)
9. [When to Use WebSockets](#when-to-use-websockets)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## What are WebSockets?

WebSockets provide full-duplex, bidirectional communication over a single TCP connection. Unlike HTTP, which is request-response, WebSockets allow both client and server to send messages at any time.

### Key Characteristics

- **Bidirectional**: Both client and server can send messages
- **Persistent**: Connection stays open
- **Low latency**: No HTTP header overhead per message
- **Full-duplex**: Simultaneous read/write

### When to Use WebSockets

- Real-time chat applications
- Live notifications
- Collaborative editing
- Multiplayer games
- Live dashboards/monitoring
- Financial tickers
- IoT device communication

---

## WebSocket Endpoint

### Basic WebSocket Endpoint

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
```

### WebSocket with Path Parameters

```python
@app.websocket("/ws/{room_id}")
async def websocket_room(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await websocket.send_text(f"Connected to room: {room_id}")
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"[Room {room_id}] {data}")
```

### WebSocket with Query Parameters

```python
@app.websocket("/ws")
async def websocket_with_query(
    websocket: WebSocket,
    token: str = None,
):
    await websocket.accept()

    if not token:
        await websocket.close(code=1008)  # Policy Violation
        return

    user = verify_token(token)
    if not user:
        await websocket.close(code=1008)
        return

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"{user.name}: {data}")
```

---

## WebSocket Protocol

### Connection Lifecycle

```
1. Client sends HTTP upgrade request
   GET /ws HTTP/1.1
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: dGhlIHNhbXBsZQ==
   Sec-WebSocket-Version: 13

2. Server responds with 101 Switching Protocols
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

3. WebSocket connection established
   Both sides can now send messages

4. Connection closed by either side
   Close frame sent
```

### WebSocket Frames

```
WebSocket frames contain:
- Opcode: Text (0x1), Binary (0x2), Close (0x8), Ping (0x9), Pong (0xA)
- Payload: The actual data
- Mask: Client-to-server frames are masked for security
```

---

## Connect/Disconnect Events

### Handling Connection Events

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Client connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total: {len(self.active_connections)}")

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
```

### Connection Events with User Info

```python
@app.websocket("/ws/{user_id}")
async def websocket_with_user(websocket: WebSocket, user_id: str):
    await websocket.accept()
    logger.info(f"User {user_id} connected")

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"[{user_id}] {data}")
    except WebSocketDisconnect:
        logger.info(f"User {user_id} disconnected")
    except Exception as e:
        logger.error(f"Error for user {user_id}: {e}")
```

---

## Sending/Receiving Data

### Text Data

```python
@app.websocket("/ws/text")
async def text_websocket(websocket: WebSocket):
    await websocket.accept()

    # Receive text
    data = await websocket.receive_text()
    print(f"Received: {data}")

    # Send text
    await websocket.send_text("Hello, client!")

    # Send JSON as text
    import json
    await websocket.send_text(json.dumps({"type": "message", "content": "Hello"}))
```

### Binary Data

```python
@app.websocket("/ws/binary")
async def binary_websocket(websocket: WebSocket):
    await websocket.accept()

    # Receive binary
    data = await websocket.receive_bytes()
    print(f"Received {len(data)} bytes")

    # Send binary
    await websocket.send_bytes(b"Hello, binary!")

    # Send file
    with open("file.bin", "rb") as f:
        await websocket.send_bytes(f.read())
```

### Sending Multiple Messages

```python
@app.websocket("/ws/stream")
async def stream_websocket(websocket: WebSocket):
    await websocket.accept()

    # Send multiple messages
    for i in range(10):
        await websocket.send_text(f"Message {i}")
        await asyncio.sleep(1)  # Simulate delay

    await websocket.close()
```

---

## JSON over WebSocket

### Sending and Receiving JSON

```python
from pydantic import BaseModel
import json

class WSMessage(BaseModel):
    type: str
    content: str
    timestamp: float = None

@app.websocket("/ws/json")
async def json_websocket(websocket: WebSocket):
    await websocket.accept()

    while True:
        # Receive JSON
        data = await websocket.receive_text()
        message = WSMessage.model_validate_json(data)

        # Process message
        response = WSMessage(
            type="response",
            content=f"Echo: {message.content}",
            timestamp=time.time(),
        )

        # Send JSON
        await websocket.send_text(response.model_dump_json())
```

### Typed WebSocket Messages

```python
from enum import Enum
from pydantic import BaseModel

class MessageType(str, Enum):
    CHAT = "chat"
    JOIN = "join"
    LEAVE = "leave"
    TYPING = "typing"

class ChatMessage(BaseModel):
    type: MessageType
    content: str = None
    room_id: str = None

@app.websocket("/ws/chat")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        message = ChatMessage.model_validate_json(data)

        if message.type == MessageType.JOIN:
            await websocket.send_text(f"Joined room {message.room_id}")
        elif message.type == MessageType.LEAVE:
            await websocket.send_text(f"Left room {message.room_id}")
        elif message.type == MessageType.CHAT:
            await websocket.send_text(f"Chat: {message.content}")
```

---

## Binary Data

### File Transfer

```python
@app.websocket("/ws/upload")
async def upload_websocket(websocket: WebSocket):
    await websocket.accept()

    # Receive file info
    info = await websocket.receive_text()
    file_info = json.loads(info)

    # Receive file data
    file_data = await websocket.receive_bytes()

    # Save file
    with open(f"uploads/{file_info['filename']}", "wb") as f:
        f.write(file_data)

    await websocket.send_text("File uploaded successfully")
```

### Streaming Binary Data

```python
@app.websocket("/ws/stream-file")
async def stream_file(websocket: WebSocket, file_id: str):
    await websocket.accept()

    # Send file in chunks
    chunk_size = 4096
    with open(f"files/{file_id}", "rb") as f:
        while chunk := f.read(chunk_size):
            await websocket.send_bytes(chunk)

    # Signal end of file
    await websocket.send_bytes(b"")
    await websocket.close()
```

---

## WebSocket vs SSE vs Polling

### Comparison

| Feature | WebSocket | SSE | Polling |
|---------|-----------|-----|---------|
| Direction | Bidirectional | Server → Client | Client → Server |
| Protocol | WebSocket | HTTP | HTTP |
| Real-time | Yes | Yes | No (delayed) |
| Connection | Persistent | Persistent | New per request |
| Browser Support | All modern | Most modern | All |
| Complexity | Higher | Lower | Lowest |
| Use Case | Chat, gaming | Notifications | Simple updates |

### When to Use Each

```python
# Use WebSocket when:
# - Client needs to send data to server
# - Bidirectional communication needed
# - Low latency is critical
# - Example: Chat, multiplayer games, collaborative editing

# Use SSE when:
# - Only server needs to push data to client
# - Simpler implementation is preferred
# - Automatic reconnection is needed
# - Example: News feeds, notifications, live dashboards

# Use Polling when:
# - Updates are infrequent
# - Simplicity is paramount
# - Real-time is not critical
# - Example: Status checks, periodic updates
```

### SSE Implementation for Comparison

```python
from fastapi.responses import StreamingResponse
import asyncio
import json

@app.get("/sse/events")
async def sse_events():
    async def event_generator():
        while True:
            data = {"timestamp": time.time(), "value": "update"}
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
```

---

## When to Use WebSockets

### Good Use Cases

```python
# 1. Real-time Chat
@app.websocket("/ws/chat/{room_id}")
async def chat(websocket: WebSocket, room_id: str):
    # Multiple users sending/receiving messages
    pass

# 2. Live Notifications
@app.websocket("/ws/notifications/{user_id}")
async def notifications(websocket: WebSocket, user_id: str):
    # Server pushing notifications to client
    pass

# 3. Collaborative Editing
@app.websocket("/ws/document/{doc_id}")
async def document(websocket: WebSocket, doc_id: str):
    # Multiple users editing same document
    pass

# 4. Live Dashboard
@app.websocket("/ws/dashboard")
async def dashboard(websocket: WebSocket):
    # Real-time metrics and updates
    pass

# 5. Multiplayer Games
@app.websocket("/ws/game/{game_id}")
async def game(websocket: WebSocket, game_id: str):
    # Game state synchronization
    pass
```

### Bad Use Cases

```python
# Don't use WebSockets for:
# 1. Simple CRUD operations (use REST)
# 2. One-time data fetch (use REST)
# 3. File uploads (use multipart form)
# 4. When SSE would suffice (simpler)
```

---

## Best Practices

### 1. Handle Disconnections Gracefully

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        # Handle disconnect
        pass
    except Exception as e:
        # Handle other errors
        pass
    finally:
        # Cleanup
        pass
```

### 2. Implement Heartbeats

```python
import asyncio

@app.websocket("/ws")
async def websocket_with_heartbeat(websocket: WebSocket):
    await websocket.accept()

    async def heartbeat():
        while True:
            await asyncio.sleep(30)
            try:
                await websocket.send_text("ping")
            except:
                break

    heartbeat_task = asyncio.create_task(heartbeat())

    try:
        while True:
            data = await websocket.receive_text()
            if data == "pong":
                continue
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass
    finally:
        heartbeat_task.cancel()
```

### 3. Validate Input

```python
from pydantic import BaseModel, validator

class WSMessage(BaseModel):
    type: str
    content: str

    @validator("type")
    def validate_type(cls, v):
        if v not in ["chat", "join", "leave"]:
            raise ValueError("Invalid message type")
        return v
```

### 4. Use Connection Manager

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        self.active_connections[room_id].remove(websocket)

    async def broadcast(self, message: str, room_id: str):
        for connection in self.active_connections.get(room_id, []):
            await connection.send_text(message)
```

### 5. Limit Message Size

```python
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB

@app.websocket("/ws")
async def websocket_with_limits(websocket: WebSocket):
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

### Q1: What are WebSockets?
**Answer:** WebSockets provide full-duplex, bidirectional communication over a single TCP connection. Unlike HTTP's request-response model, both client and server can send messages at any time.

### Q2: When should you use WebSockets over REST?
**Answer:** Use WebSockets for real-time, bidirectional communication (chat, gaming, collaboration). Use REST for traditional request-response (CRUD operations, data fetching).

### Q3: What is the WebSocket handshake?
**Answer:** The client sends an HTTP upgrade request. The server responds with 101 Switching Protocols. After this, the connection switches from HTTP to WebSocket protocol.

### Q4: What is the difference between WebSocket and SSE?
**Answer:** WebSocket is bidirectional (client and server can send). SSE is unidirectional (server pushes to client). SSE is simpler but limited. WebSocket is more flexible but complex.

### Q5: How do you handle WebSocket disconnections?
**Answer:** Use try/except to catch `WebSocketDisconnect`. Clean up resources, remove from connection managers, and optionally notify other users.

### Q6: What is a ConnectionManager?
**Answer:** A class that tracks active WebSocket connections, handles connecting/disconnecting clients, and provides methods for broadcasting messages to specific users or rooms.

### Q7: How do you authenticate WebSocket connections?
**Answer:** Validate tokens during the WebSocket handshake (in query params or initial message). Check authentication before accepting the connection or in the first message.

### Q8: What are WebSocket heartbeats?
**Answer:** Periodic ping/pong messages to keep connections alive and detect dead connections. The server sends pings, and the client responds with pongs.

### Q9: What is the maximum WebSocket message size?
**Answer:** The WebSocket protocol doesn't define a maximum, but implementations do. Browsers typically support up to 100MB, but it's best to limit to a reasonable size (e.g., 1MB).

### Q10: How do you send binary data over WebSocket?
**Answer:** Use `await websocket.send_bytes(data)` for binary and `await websocket.receive_bytes()` to receive. Useful for file transfers or binary protocols.

### Q11: Can WebSocket connections go through load balancers?
**Answer:** Yes, but the load balancer must support WebSocket (sticky sessions or connection-aware routing). Most modern load balancers (Nginx, HAProxy, cloud LBs) support WebSocket.

### Q12: What is the difference between WebSocket and HTTP/2?
**Answer:** HTTP/2 supports multiplexing but is still request-response. WebSocket is persistent and bidirectional. HTTP/2 Server Push is limited and not the same as WebSocket.

### Q13: How do you handle WebSocket errors?
**Answer:** Wrap WebSocket operations in try/except. Handle `WebSocketDisconnect`, `WebSocketException`, and other exceptions. Log errors and clean up resources.

### Q14: What are WebSocket subprotocols?
**Answer:** Application-level protocols negotiated during the handshake. The client specifies supported protocols, and the server selects one. Used for standardized message formats.

### Q15: Can you use WebSockets with HTTPS?
**Answer:** Yes, WebSocket Secure (WSS) uses TLS. The connection starts with `wss://` instead of `ws://`. Most production deployments use WSS.

### Q16: How do you scale WebSocket connections?
**Answer:** Use multiple server instances with Redis pub/sub for message broadcasting. Implement sticky sessions at the load balancer. Use connection pooling.

### Q17: What is WebSocket compression?
**Answer:** The WebSocket protocol supports per-message compression (permessage-deflate). It reduces bandwidth but uses more CPU. Configurable per connection.

### Q18: How do you test WebSocket endpoints?
**Answer:** Use `websocket_connect` from httpx, `pytest-asyncio` for async tests, and WebSocket client libraries. Test connection, message sending/receiving, and disconnection.

### Q19: What are common WebSocket security issues?
**Answer:** Cross-Site WebSocket Hijacking (CSWSH), lack of authentication, no rate limiting, and sensitive data exposure. Mitigate with origin checking, auth, and encryption.

### Q20: What is the difference between WebSocket close codes?
**Answer:** 1000: Normal closure. 1001: Going away. 1002-1003: Protocol errors. 1006-1015: Various error conditions. Used to indicate why the connection was closed.

### Q21: How do you handle WebSocket reconnection?
**Answer:** Implement exponential backoff on the client. The client should attempt to reconnect with increasing delays. Handle state synchronization after reconnection.

### Q22: Can WebSocket connections be load balanced?
**Answer:** Yes, but require sticky sessions or consistent hashing. The load balancer must maintain the WebSocket connection state. Cloud load balancers typically support this.

### Q23: What is the WebSocket API in browsers?
**Answer:** The browser WebSocket API provides `WebSocket` class for creating connections, sending/receiving messages, and handling events (open, message, close, error).

### Q24: How do you broadcast messages in WebSocket?
**Answer:** Maintain a list of active connections. Iterate through the list and send to each connection. Use connection managers for room-based broadcasting.

### Q25: What are the alternatives to WebSockets?
**Answer:** Server-Sent Events (SSE) for server-to-client, HTTP/2 Server Push, long polling, WebRTC for peer-to-peer, and GraphQL subscriptions.
