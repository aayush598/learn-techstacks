# WebSocket Rooms and Broadcasting

## Table of Contents
1. [WebSocket Rooms Concept](#websocket-rooms-concept)
2. [ConnectionManager Class](#connectionmanager-class)
3. [Broadcasting to All Clients](#broadcasting-to-all-clients)
4. [Targeted Messages](#targeted-messages)
5. [Group Chat Implementation](#group-chat-implementation)
6. [Pub/Sub with Redis](#pubsub-with-redis)
7. [Scaled WebSockets](#scaled-websockets)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## WebSocket Rooms Concept

Rooms are logical groupings of WebSocket connections. Messages can be broadcast to all connections in a room, enabling features like group chats, live events, and collaborative workspaces.

### Why Rooms?

- **Efficiency**: Send message once, receive by many
- **Organization**: Group users by context (chat room, document, game)
- **Targeting**: Send messages to specific groups
- **Scaling**: Distribute message handling across instances

### Room Implementation Patterns

```
Room: "chat:general"
├── Connection 1 (User A)
├── Connection 2 (User B)
└── Connection 3 (User C)

Room: "chat:engineering"
├── Connection 4 (User D)
└── Connection 5 (User E)

User A sends message → Server → All connections in "chat:general"
```

---

## ConnectionManager Class

### Basic ConnectionManager

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # room_id -> list of websockets
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_text(message)
                except:
                    # Connection might be closed
                    pass

manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}", room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
```

### Advanced ConnectionManager with User Tracking

```python
from pydantic import BaseModel
from typing import Optional
import uuid

class Connection(BaseModel):
    websocket: WebSocket
    user_id: str
    username: str
    connected_at: float

class AdvancedConnectionManager:
    def __init__(self):
        # room_id -> connection_id -> Connection
        self.rooms: dict[str, dict[str, Connection]] = {}
        # connection_id -> room_id
        self.connection_rooms: dict[str, str] = {}

    async def connect(
        self,
        websocket: WebSocket,
        room_id: str,
        user_id: str,
        username: str,
    ) -> str:
        await websocket.accept()

        connection_id = str(uuid.uuid4())
        connection = Connection(
            websocket=websocket,
            user_id=user_id,
            username=username,
            connected_at=time.time(),
        )

        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        self.rooms[room_id][connection_id] = connection
        self.connection_rooms[connection_id] = room_id

        # Notify room
        await self.broadcast(
            room_id,
            {
                "type": "user_joined",
                "user_id": user_id,
                "username": username,
                "users": self.get_room_users(room_id),
            }
        )

        return connection_id

    def disconnect(self, connection_id: str):
        room_id = self.connection_rooms.get(connection_id)
        if room_id and room_id in self.rooms:
            connection = self.rooms[room_id].pop(connection_id, None)
            self.connection_rooms.pop(connection_id, None)

            if connection:
                asyncio.create_task(
                    self.broadcast(
                        room_id,
                        {
                            "type": "user_left",
                            "user_id": connection.user_id,
                            "username": connection.username,
                            "users": self.get_room_users(room_id),
                        }
                    )
                )

    def get_room_users(self, room_id: str) -> list[dict]:
        if room_id not in self.rooms:
            return []
        return [
            {"user_id": c.user_id, "username": c.username}
            for c in self.rooms[room_id].values()
        ]

    async def broadcast(self, room_id: str, message: dict):
        if room_id not in self.rooms:
            return

        message_str = json.dumps(message)
        disconnected = []

        for conn_id, connection in self.rooms[room_id].items():
            try:
                await connection.websocket.send_text(message_str)
            except:
                disconnected.append(conn_id)

        # Clean up disconnected
        for conn_id in disconnected:
            self.disconnect(conn_id)

    async def send_to_user(self, user_id: str, message: dict):
        message_str = json.dumps(message)
        for room_id, connections in self.rooms.items():
            for conn_id, connection in connections.items():
                if connection.user_id == user_id:
                    try:
                        await connection.websocket.send_text(message_str)
                    except:
                        pass

manager = AdvancedConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    user_id: str = Query(...),
    username: str = Query(...),
):
    connection_id = await manager.connect(websocket, room_id, user_id, username)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            await manager.broadcast(room_id, {
                "type": "message",
                "user_id": user_id,
                "username": username,
                "content": message["content"],
                "timestamp": time.time(),
            })
    except WebSocketDisconnect:
        manager.disconnect(connection_id)
```

---

## Broadcasting to All Clients

### Global Broadcast

```python
class GlobalBroadcastManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.connections:
            try:
                await connection.send_text(message)
            except:
                disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)

manager = GlobalBroadcastManager()

@app.websocket("/ws/global")
async def global_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Global: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Selective Broadcast

```python
async def broadcast_to_users(
    manager: AdvancedConnectionManager,
    user_ids: list[str],
    message: dict,
):
    """Broadcast message to specific users across all rooms."""
    for room_id, connections in manager.rooms.items():
        for conn_id, connection in connections.items():
            if connection.user_id in user_ids:
                try:
                    await connection.websocket.send_text(json.dumps(message))
                except:
                    pass
```

---

## Targeted Messages

### Send to Specific User

```python
@app.websocket("/ws/{room_id}")
async def targeted_websocket(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)

    try:
        while True:
            data = json.loads(await websocket.receive_text())

            if data["type"] == "dm":
                # Direct message to specific user
                target_user_id = data["to"]
                await manager.send_to_user(target_user_id, {
                    "type": "dm",
                    "from": data["from"],
                    "content": data["content"],
                })
            elif data["type"] == "room":
                # Broadcast to room
                await manager.broadcast(room_id, {
                    "type": "message",
                    "from": data["from"],
                    "content": data["content"],
                })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Send to Multiple Users

```python
@app.websocket("/ws/{room_id}")
async def multi_target_websocket(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)

    try:
        while True:
            data = json.loads(await websocket.receive_text())

            if data["type"] == "group_message":
                target_user_ids = data["to"]  # List of user IDs
                for user_id in target_user_ids:
                    await manager.send_to_user(user_id, {
                        "type": "message",
                        "from": data["from"],
                        "content": data["content"],
                    })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## Group Chat Implementation

### Full Chat Room

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ChatMessage(BaseModel):
    type: str  # "join", "leave", "message", "typing"
    content: Optional[str] = None
    user_id: str
    username: str
    room_id: str
    timestamp: float = None

class ChatRoom:
    def __init__(self, room_id: str, name: str):
        self.room_id = room_id
        self.name = name
        self.messages: list[dict] = []
        self.connections: dict[str, Connection] = {}

    def add_connection(self, connection_id: str, connection: Connection):
        self.connections[connection_id] = connection

    def remove_connection(self, connection_id: str):
        self.connections.pop(connection_id, None)

    async def broadcast(self, message: dict, exclude: str = None):
        for conn_id, conn in self.connections.items():
            if conn_id != exclude:
                try:
                    await conn.websocket.send_text(json.dumps(message))
                except:
                    pass

class ChatManager:
    def __init__(self):
        self.rooms: dict[str, ChatRoom] = {}

    def get_or_create_room(self, room_id: str, name: str = None) -> ChatRoom:
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id, name or room_id)
        return self.rooms[room_id]

    async def join_room(
        self,
        room_id: str,
        user_id: str,
        username: str,
        websocket: WebSocket,
    ) -> ChatRoom:
        await websocket.accept()

        room = self.get_or_create_room(room_id)
        connection_id = str(uuid.uuid4())

        connection = Connection(
            websocket=websocket,
            user_id=user_id,
            username=username,
            connected_at=time.time(),
        )

        room.add_connection(connection_id, connection)

        # Send recent messages
        for msg in room.messages[-50:]:  # Last 50 messages
            await websocket.send_text(json.dumps(msg))

        # Notify room
        await room.broadcast({
            "type": "user_joined",
            "user_id": user_id,
            "username": username,
            "users": [c.username for c in room.connections.values()],
        })

        return room, connection_id

    async def leave_room(self, room_id: str, connection_id: str):
        room = self.rooms.get(room_id)
        if room:
            connection = room.connections.get(connection_id)
            if connection:
                room.remove_connection(connection_id)

                await room.broadcast({
                    "type": "user_left",
                    "user_id": connection.user_id,
                    "username": connection.username,
                })

chat_manager = ChatManager()

@app.websocket("/ws/chat/{room_id}")
async def chat_websocket(
    websocket: WebSocket,
    room_id: str,
    user_id: str = Query(...),
    username: str = Query(...),
):
    room, connection_id = await chat_manager.join_room(
        room_id, user_id, username, websocket
    )

    try:
        while True:
            data = json.loads(await websocket.receive_text())

            if data["type"] == "message":
                message = {
                    "type": "message",
                    "user_id": user_id,
                    "username": username,
                    "content": data["content"],
                    "room_id": room_id,
                    "timestamp": time.time(),
                }
                room.messages.append(message)
                await room.broadcast(message)

            elif data["type"] == "typing":
                await room.broadcast(
                    {"type": "typing", "user_id": user_id, "username": username},
                    exclude=connection_id,
                )
    except WebSocketDisconnect:
        await chat_manager.leave_room(room_id, connection_id)
```

---

## Pub/Sub with Redis

### Why Redis Pub/Sub?

- **Scalability**: Multiple server instances can share messages
- **Decoupling**: Publishers and subscribers don't need to know each other
- **Real-time**: Messages are delivered instantly

### Redis Pub/Sub Implementation

```python
import redis.asyncio as redis
import asyncio
import json

class RedisPubSubManager:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
        self.local_connections: dict[str, list[WebSocket]] = {}

    async def subscribe(self, room_id: str):
        await self.pubsub.subscribe(f"ws:room:{room_id}")

    async def unsubscribe(self, room_id: str):
        await self.pubsub.unsubscribe(f"ws:room:{room_id}")

    async def publish(self, room_id: str, message: dict):
        await self.redis.publish(f"ws:room:{room_id}", json.dumps(message))

    async def listen_for_messages(self, room_id: str, websocket: WebSocket):
        """Listen for Redis pub/sub messages and send to local WebSocket."""
        async for msg in self.pubsub.listen():
            if msg["type"] == "message":
                await websocket.send_text(msg["data"].decode())

    def add_local_connection(self, room_id: str, websocket: WebSocket):
        if room_id not in self.local_connections:
            self.local_connections[room_id] = []
        self.local_connections[room_id].append(websocket)

    def remove_local_connection(self, room_id: str, websocket: WebSocket):
        if room_id in self.local_connections:
            self.local_connections[room_id].remove(websocket)

pubsub_manager = RedisPubSubManager()

@app.websocket("/ws/{room_id}")
async def redis_pubsub_websocket(
    websocket: WebSocket,
    room_id: str,
    user_id: str = Query(...),
):
    await websocket.accept()

    # Subscribe to Redis channel
    await pubsub_manager.subscribe(room_id)
    pubsub_manager.add_local_connection(room_id, websocket)

    # Start listener task
    listener_task = asyncio.create_task(
        pubsub_manager.listen_for_messages(room_id, websocket)
    )

    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "type": "message",
                "user_id": user_id,
                "content": data,
                "timestamp": time.time(),
            }
            # Publish to Redis (all instances receive)
            await pubsub_manager.publish(room_id, message)
    except WebSocketDisconnect:
        listener_task.cancel()
        pubsub_manager.remove_local_connection(room_id, websocket)
        await pubsub_manager.unsubscribe(room_id)
```

---

## Scaled WebSockets

### Architecture for Multi-Instance Deployment

```
                    ┌─────────────┐
                    │   Client 1  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Instance 1 │◄──── Redis Pub/Sub
                    └──────┬──────┘
                           │
┌─────────────┐     ┌──────▼──────┐     ┌─────────────┐
│   Client 2  │◄───►│  Instance 2 │◄───►│   Redis     │
└─────────────┘     └──────┬──────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │  Instance 3 │
                    └─────────────┘
```

### Complete Scaled Implementation

```python
import redis.asyncio as redis
import asyncio
import json
import uuid

class ScaledWebSocketManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
        self.local_connections: dict[str, dict[str, WebSocket]] = {}
        self.instance_id = str(uuid.uuid4())

    async def connect(
        self,
        websocket: WebSocket,
        room_id: str,
        user_id: str,
    ) -> str:
        await websocket.accept()

        connection_id = str(uuid.uuid4())

        # Store locally
        if room_id not in self.local_connections:
            self.local_connections[room_id] = {}
        self.local_connections[room_id][connection_id] = websocket

        # Store in Redis for cross-instance tracking
        await self.redis.hset(
            f"ws:connections:{room_id}",
            connection_id,
            json.dumps({
                "user_id": user_id,
                "instance_id": self.instance_id,
            }),
        )

        # Subscribe to room channel
        await self.redis.subscribe(f"ws:room:{room_id}")

        return connection_id

    async def disconnect(self, room_id: str, connection_id: str):
        # Remove locally
        if room_id in self.local_connections:
            self.local_connections[room_id].pop(connection_id, None)

        # Remove from Redis
        await self.redis.hdel(f"ws:connections:{room_id}", connection_id)

    async def broadcast(self, room_id: str, message: dict):
        # Publish to Redis (all instances receive)
        await self.redis.publish(f"ws:room:{room_id}", json.dumps(message))

    async def send_local(self, room_id: str, connection_id: str, message: dict):
        websocket = self.local_connections.get(room_id, {}).get(connection_id)
        if websocket:
            try:
                await websocket.send_text(json.dumps(message))
            except:
                await self.disconnect(room_id, connection_id)

    async def listen(self, room_id: str):
        """Listen for messages from Redis and deliver to local connections."""
        async for msg in self.pubsub.listen():
            if msg["type"] == "message":
                message = json.loads(msg["data"].decode())

                # Deliver to all local connections in this room
                if room_id in self.local_connections:
                    for conn_id, ws in self.local_connections[room_id].items():
                        try:
                            await ws.send_text(json.dumps(message))
                        except:
                            await self.disconnect(room_id, conn_id)

scaled_manager = ScaledWebSocketManager("redis://localhost:6379")

@app.websocket("/ws/{room_id}")
async def scaled_websocket(
    websocket: WebSocket,
    room_id: str,
    user_id: str = Query(...),
):
    connection_id = await scaled_manager.connect(websocket, room_id, user_id)

    # Start listener
    listener = asyncio.create_task(scaled_manager.listen(room_id))

    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "type": "message",
                "user_id": user_id,
                "content": data,
                "timestamp": time.time(),
            }
            await scaled_manager.broadcast(room_id, message)
    except WebSocketDisconnect:
        listener.cancel()
        await scaled_manager.disconnect(room_id, connection_id)
```

---

## Best Practices

### 1. Use Connection Managers

```python
# Always use a ConnectionManager class
# It handles connections, disconnections, and broadcasting
```

### 2. Handle Disconnections Gracefully

```python
# Clean up connections on disconnect
# Notify other users in the room
# Remove from Redis tracking
```

### 3. Use Redis Pub/Sub for Scaling

```python
# For multi-instance deployments
# Redis pub/sub ensures all instances receive messages
```

### 4. Limit Room Size

```python
MAX_ROOM_SIZE = 100

async def join_room(websocket: WebSocket, room_id: str):
    current_size = get_room_size(room_id)
    if current_size >= MAX_ROOM_SIZE:
        await websocket.close(code=1013)  # Try Again Later
        return
```

### 5. Store Message History

```python
# Store messages in Redis or database
# Send recent messages to new connections
# Implement message pagination
```

### 6. Implement Typing Indicators

```python
await room.broadcast(
    {"type": "typing", "user_id": user_id},
    exclude=connection_id,
)
```

### 7. Use Async Tasks for Broadcasting

```python
# Don't block the main loop while broadcasting
asyncio.create_task(broadcast_to_all(message))
```

---

## Interview Questions

### Q1: What are WebSocket rooms?
**Answer:** Rooms are logical groupings of WebSocket connections. Messages broadcast to a room are received by all connections in that room. Useful for group chats, live events, and collaborative features.

### Q2: How do you implement a ConnectionManager?
**Answer:** A class that tracks active connections, handles connect/disconnect, and provides methods for broadcasting to rooms or specific users.

### Q3: Why use Redis pub/sub with WebSockets?
**Answer:** For multi-instance deployments. Redis pub/sub ensures all server instances receive messages, enabling broadcasting across multiple WebSocket servers.

### Q4: How do you send a message to a specific user?
**Answer:** Maintain a mapping of user IDs to connections. Iterate through connections to find the target user and send directly.

### Q5: How do you handle user joins and leaves?
**Answer:** On join: accept connection, add to room, notify others. On disconnect: remove from room, notify others, clean up resources.

### Q6: What is the difference between broadcast and targeted messages?
**Answer:** Broadcast sends to all connections in a room. Targeted sends to specific users or connections. Both are needed for different features.

### Q7: How do you scale WebSocket connections across multiple servers?
**Answer:** Use Redis pub/sub for message distribution, sticky sessions at the load balancer, and shared state in Redis for connection tracking.

### Q8: How do you implement message history?
**Answer:** Store messages in Redis or database. Send recent messages to new connections. Implement pagination for older messages.

### Q9: What are typing indicators?
**Answer:** Real-time notifications showing when a user is typing. Implemented by broadcasting "typing" events to other room members.

### Q10: How do you handle connection limits per room?
**Answer:** Track room size in Redis. Reject new connections when the limit is reached. Return appropriate close code (1013: Try Again Later).

### Q11: What is the difference between local and global connections?
**Answer:** Local connections are on the current server instance. Global connections include all instances. Redis pub/sub bridges local to global.

### Q12: How do you handle message ordering in rooms?
**Answer:** Use timestamps or sequence numbers. Messages may arrive out of order in distributed systems. Clients can reorder based on timestamps.

### Q13: How do you implement private rooms?
**Answer:** Store room access control in database. Check permissions before allowing join. Only invited users can connect.

### Q14: How do you clean up stale connections?
**Answer:** Use heartbeats/ping-pong. If no pong received within timeout, close the connection and clean up resources.

### Q15: How do you handle room deletion?
**Answer:** When all users leave, optionally delete the room. Clean up Redis keys, message history, and any associated resources.

### Q16: What is connection multiplexing?
**Answer:** A single TCP connection carrying multiple logical WebSocket connections. Reduces resource usage but adds complexity. Not commonly used.

### Q17: How do you implement read receipts?
**Answer:** When a user reads a message, send a "read" event with the message ID. Broadcast the receipt to other room members.

### Q18: How do you handle offline messages?
**Answer:** Store messages in Redis/database. When user reconnects, send any pending messages. Use message IDs for tracking.

### Q19: What is the role of sequence numbers?
**Answer:** Ensure message ordering in distributed systems. Clients can detect missing messages and request retransmission.

### Q20: How do you implement WebSocket message compression?
**Answer:** Use permessage-deflate extension. Configure compression level per connection. Trade off CPU for bandwidth.
