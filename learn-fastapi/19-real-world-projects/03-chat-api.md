# Complete Real-Time Chat API

## Project Overview

A production-grade WebSocket-based chat application with rooms, direct messaging, presence tracking, typing indicators, read receipts, file sharing, and Redis pub/sub for scaling.

## Feature List

- JWT WebSocket authentication
- 1-on-1 direct messaging
- Group chat rooms
- Public and private rooms
- Typing indicators
- Read receipts
- Online presence tracking
- File/image sharing
- Message history with pagination
- Message search
- User profiles
- Room management (create, join, leave, mute)
- Push notifications for offline users
- Redis pub/sub for multi-server scaling

## Folder Structure

```
chat-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── redis.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── room.py
│   │   ├── message.py
│   │   └── membership.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── room.py
│   │   └── message.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── auth.py
│   │       ├── rooms.py
│   │       ├── messages.py
│   │       └── users.py
│   ├── ws/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── handlers.py
│   │   ├── events.py
│   │   └── presence.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── message_service.py
│   │   ├── room_service.py
│   │   └── notification_service.py
│   └── utils/
│       ├── __init__.py
│       ├── pagination.py
│       └── upload.py
├── tests/
├── migrations/
├── Dockerfile
└── docker-compose.yml
```

## Data Models

```python
# app/models/user.py
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(100))
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    status_text: Mapped[str | None] = mapped_column(String(200))
    is_online: Mapped[bool] = mapped_column(default=False)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    memberships: Mapped[list["Membership"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    sent_messages: Mapped[list["Message"]] = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")


# app/models/room.py
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base
import enum

class RoomType(str, enum.Enum):
    DIRECT = "direct"
    GROUP = "group"
    PUBLIC = "public"

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    room_type: Mapped[RoomType] = mapped_column(default=RoomType.GROUP)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    max_members: Mapped[int] = mapped_column(default=500)
    is_archived: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    creator: Mapped["User"] = relationship(foreign_keys=[created_by])
    memberships: Mapped[list["Membership"]] = relationship(back_populates="room", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship(back_populates="room", cascade="all, delete-orphan")


# app/models/message.py
from sqlalchemy import String, DateTime, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    message_type: Mapped[str] = mapped_column(String(20), default="text")  # text, image, file, system
    file_url: Mapped[str | None] = mapped_column(String(500))
    file_name: Mapped[str | None] = mapped_column(String(255))
    reply_to_id: Mapped[int | None] = mapped_column(ForeignKey("messages.id"))
    is_edited: Mapped[bool] = mapped_column(default=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)

    room: Mapped["Room"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship(foreign_keys=[sender_id], back_populates="sent_messages")
    reply_to: Mapped["Message | None"] = relationship("Message", remote_side="Message.id")
    read_receipts: Mapped[list["ReadReceipt"]] = relationship(back_populates="message", cascade="all, delete-orphan")


# app/models/membership.py
class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(20), default="member")  # owner, admin, member
    is_muted: Mapped[bool] = mapped_column(default=False)
    is_pinned: Mapped[bool] = mapped_column(default=False)
    last_read_at: Mapped[datetime | None] = mapped_column(DateTime)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="memberships")
    room: Mapped["Room"] = relationship(back_populates="memberships")


class ReadReceipt(Base):
    __tablename__ = "read_receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    read_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    message: Mapped["Message"] = relationship(back_populates="read_receipts")
```

## WebSocket Manager (Core)

```python
# app/ws/manager.py
from fastapi import WebSocket
from dataclasses import dataclass, field
from collections import defaultdict
import asyncio
import json
import time

@dataclass
class ConnectionInfo:
    websocket: WebSocket
    user_id: int
    connected_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)


class ConnectionManager:
    """Manages WebSocket connections, rooms, and message broadcasting."""

    def __init__(self):
        # user_id -> list of connections (supports multiple devices)
        self.connections: dict[int, list[ConnectionInfo]] = defaultdict(list)
        # room_id -> set of user_ids currently connected to the room
        self.room_users: dict[int, set[int]] = defaultdict(set)
        # user_id -> set of room_ids the user is subscribed to
        self.user_rooms: dict[int, set[int]] = defaultdict(set)
        # typing tracking: room_id -> set of user_ids currently typing
        self.typing_users: dict[int, set[int]] = defaultdict(set)
        # Presence tracking
        self.online_users: dict[int, float] = {}  # user_id -> last_heartbeat
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: int) -> ConnectionInfo:
        await websocket.accept()
        conn = ConnectionInfo(websocket=websocket, user_id=user_id)

        async with self._lock:
            self.connections[user_id].append(conn)
            self.online_users[user_id] = time.time()

        # Broadcast presence update
        await self._broadcast_presence(user_id, "online")
        return conn

    async def disconnect(self, websocket: WebSocket, user_id: int):
        async with self._lock:
            conns = self.connections.get(user_id, [])
            self.connections[user_id] = [c for c in conns if c.websocket != websocket]

            if not self.connections[user_id]:
                del self.connections[user_id]
                self.online_users.pop(user_id, None)
                await self._broadcast_presence(user_id, "offline")

    async def join_room(self, user_id: int, room_id: int):
        async with self._lock:
            self.room_users[room_id].add(user_id)
            self.user_rooms[user_id].add(room_id)

    async def leave_room(self, user_id: int, room_id: int):
        async with self._lock:
            self.room_users[room_id].discard(user_id)
            self.user_rooms[user_id].discard(room_id)

    async def send_to_user(self, user_id: int, message: dict):
        """Send message to all connections of a user."""
        conns = self.connections.get(user_id, [])
        dead = []
        for conn in conns:
            try:
                await conn.websocket.send_json(message)
            except Exception:
                dead.append(conn)
        for conn in dead:
            self.connections[user_id].remove(conn)

    async def send_to_room(self, room_id: int, message: dict, exclude_user: int | None = None):
        """Send message to all users in a room."""
        user_ids = self.room_users.get(room_id, set())
        for uid in user_ids:
            if uid != exclude_user:
                await self.send_to_user(uid, message)

    async def broadcast(self, message: dict):
        """Send message to all connected users."""
        for user_id in list(self.connections.keys()):
            await self.send_to_user(user_id, message)

    async def handle_typing(self, user_id: int, room_id: int, is_typing: bool):
        async with self._lock:
            if is_typing:
                self.typing_users[room_id].add(user_id)
            else:
                self.typing_users[room_id].discard(user_id)

        typing_user_ids = list(self.typing_users[room_id])
        await self.send_to_room(room_id, {
            "type": "typing",
            "room_id": room_id,
            "users": typing_user_ids,
        }, exclude_user=user_id)

    async def _broadcast_presence(self, user_id: int, status: str):
        """Notify all rooms about user presence change."""
        room_ids = self.user_rooms.get(user_id, set())
        for room_id in room_ids:
            await self.send_to_room(room_id, {
                "type": "presence",
                "user_id": user_id,
                "status": status,
                "timestamp": time.time(),
            }, exclude_user=user_id)

    def get_online_users(self) -> list[int]:
        return list(self.online_users.keys())

    def get_room_users(self, room_id: int) -> list[int]:
        return list(self.room_users.get(room_id, set()))

    def get_typing_users(self, room_id: int) -> list[int]:
        return list(self.typing_users.get(room_id, set()))

    async def heartbeat(self, user_id: int):
        async with self._lock:
            self.online_users[user_id] = time.time()


# Singleton
manager = ConnectionManager()
```

## WebSocket Event Handlers

```python
# app/ws/handlers.py
from app.ws.manager import manager
from app.core.security import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import async_session
from app.models.message import Message, ReadReceipt
from app.models.room import Room
from app.models.membership import Membership
from sqlalchemy import select
import json

async def handle_ws_message(user_id: int, data: dict):
    """Route incoming WebSocket messages to appropriate handlers."""
    msg_type = data.get("type")

    handlers = {
        "message": handle_send_message,
        "typing": handle_typing,
        "read_receipt": handle_read_receipt,
        "join_room": handle_join_room,
        "leave_room": handle_leave_room,
        "history": handle_fetch_history,
        "ping": handle_ping,
    }

    handler = handlers.get(msg_type)
    if handler:
        await handler(user_id, data)
    else:
        await manager.send_to_user(user_id, {
            "type": "error",
            "message": f"Unknown message type: {msg_type}",
        })


async def handle_send_message(user_id: int, data: dict):
    room_id = data.get("room_id")
    content = data.get("content", "").strip()
    message_type = data.get("message_type", "text")
    reply_to_id = data.get("reply_to_id")

    if not room_id or not content:
        await manager.send_to_user(user_id, {"type": "error", "message": "room_id and content required"})
        return

    # Verify membership
    async with async_session() as db:
        membership = await db.execute(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.room_id == room_id,
            )
        )
        if not membership.scalar_one_or_none():
            await manager.send_to_user(user_id, {"type": "error", "message": "Not a member of this room"})
            return

        # Save message to DB
        message = Message(
            room_id=room_id,
            sender_id=user_id,
            content=content,
            message_type=message_type,
            file_url=data.get("file_url"),
            file_name=data.get("file_name"),
            reply_to_id=reply_to_id,
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)

    # Broadcast to room
    broadcast_data = {
        "type": "message",
        "id": message.id,
        "room_id": room_id,
        "sender_id": user_id,
        "content": content,
        "message_type": message_type,
        "file_url": message.file_url,
        "file_name": message.file_name,
        "reply_to_id": message.reply_to_id,
        "created_at": message.created_at.isoformat(),
    }
    await manager.send_to_room(room_id, broadcast_data)


async def handle_typing(user_id: int, data: dict):
    room_id = data.get("room_id")
    is_typing = data.get("is_typing", False)
    if room_id:
        await manager.handle_typing(user_id, room_id, is_typing)


async def handle_read_receipt(user_id: int, data: dict):
    message_id = data.get("message_id")
    room_id = data.get("room_id")
    if not message_id or not room_id:
        return

    async with async_session() as db:
        # Save read receipt
        receipt = ReadReceipt(message_id=message_id, user_id=user_id)
        db.add(receipt)

        # Update membership last_read_at
        membership = await db.execute(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.room_id == room_id,
            )
        )
        mem = membership.scalar_one_or_none()
        if mem:
            from datetime import datetime
            mem.last_read_at = datetime.utcnow()

        await db.commit()

    # Broadcast read receipt to room
    await manager.send_to_room(room_id, {
        "type": "read_receipt",
        "message_id": message_id,
        "user_id": user_id,
        "room_id": room_id,
    }, exclude_user=user_id)


async def handle_join_room(user_id: int, data: dict):
    room_id = data.get("room_id")
    if room_id:
        await manager.join_room(user_id, room_id)
        await manager.send_to_user(user_id, {
            "type": "system",
            "message": f"Joined room {room_id}",
            "online_users": manager.get_room_users(room_id),
        })


async def handle_leave_room(user_id: int, data: dict):
    room_id = data.get("room_id")
    if room_id:
        await manager.leave_room(user_id, room_id)
        await manager.send_to_user(user_id, {
            "type": "system",
            "message": f"Left room {room_id}",
        })


async def handle_fetch_history(user_id: int, data: dict):
    room_id = data.get("room_id")
    limit = min(data.get("limit", 50), 100)
    before_id = data.get("before_id")

    if not room_id:
        return

    async with async_session() as db:
        query = (
            select(Message)
            .where(Message.room_id == room_id, Message.is_deleted == False)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )

        if before_id:
            msg = await db.execute(select(Message.created_at).where(Message.id == before_id))
            before_time = msg.scalar_one_or_none()
            if before_time:
                query = query.where(Message.created_at < before_time)

        result = await db.execute(query)
        messages = result.scalars().all()

    await manager.send_to_user(user_id, {
        "type": "history",
        "room_id": room_id,
        "messages": [
            {
                "id": m.id,
                "sender_id": m.sender_id,
                "content": m.content,
                "message_type": m.message_type,
                "file_url": m.file_url,
                "reply_to_id": m.reply_to_id,
                "created_at": m.created_at.isoformat(),
            }
            for m in reversed(messages)
        ],
    })


async def handle_ping(user_id: int, data: dict):
    await manager.heartbeat(user_id)
    await manager.send_to_user(user_id, {"type": "pong"})
```

## WebSocket Endpoint

```python
# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from app.ws.manager import manager
from app.ws.handlers import handle_ws_message
from app.core.security import decode_token

app = FastAPI(title="Chat API")

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    # Authenticate
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        await websocket.close(code=4001, reason="Invalid token")
        return

    user_id = int(payload["sub"])
    conn = await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            await handle_ws_message(user_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, user_id)
```

## REST API for Chat

```python
# app/api/v1/rooms.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.room import Room, RoomType
from app.models.membership import Membership
from app.models.user import User
from app.api.deps import get_current_active_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("/", status_code=201)
async def create_room(
    name: str,
    room_type: str = "group",
    description: str | None = None,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    room = Room(
        name=name,
        description=description,
        room_type=room_type,
        created_by=user.id,
    )
    db.add(room)
    await db.flush()

    membership = Membership(user_id=user.id, room_id=room.id, role="owner")
    db.add(membership)
    await db.commit()

    # Join via WebSocket
    from app.ws.manager import manager
    await manager.join_room(user.id, room.id)

    return {"id": room.id, "name": room.name, "type": room.room_type}

@router.get("/")
async def list_rooms(
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Room)
        .join(Membership)
        .where(Membership.user_id == user.id)
        .options(selectinload(Room.memberships).selectinload(Membership.user))
    )
    rooms = result.scalars().all()

    return [{
        "id": r.id,
        "name": r.name,
        "type": r.room_type,
        "member_count": len(r.memberships),
        "created_at": r.created_at.isoformat(),
    } for r in rooms]

@router.post("/{room_id}/join")
async def join_room(
    room_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    room = (await db.execute(select(Room).where(Room.id == room_id))).scalar_one_or_none()
    if not room:
        raise HTTPException(404, "Room not found")

    existing = (await db.execute(
        select(Membership).where(Membership.user_id == user.id, Membership.room_id == room_id)
    )).scalar_one_or_none()

    if existing:
        return {"status": "already_member"}

    if room.room_type == RoomType.DIRECT:
        raise HTTPException(400, "Cannot join direct messages")

    membership = Membership(user_id=user.id, room_id=room_id)
    db.add(membership)
    await db.commit()

    from app.ws.manager import manager
    await manager.join_room(user.id, room_id)

    return {"status": "joined"}

@router.post("/{room_id}/leave")
async def leave_room(
    room_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    membership = (await db.execute(
        select(Membership).where(Membership.user_id == user.id, Membership.room_id == room_id)
    )).scalar_one_or_none()

    if not membership:
        raise HTTPException(400, "Not a member")

    if membership.role == "owner":
        raise HTTPException(400, "Owner cannot leave. Transfer ownership first.")

    await db.delete(membership)
    await db.commit()

    from app.ws.manager import manager
    await manager.leave_room(user.id, room_id)

    return {"status": "left"}

@router.get("/{room_id}/members")
async def list_members(
    room_id: int,
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    membership = (await db.execute(
        select(Membership).where(Membership.user_id == user.id, Membership.room_id == room_id)
    )).scalar_one_or_none()

    if not membership:
        raise HTTPException(403, "Not a member")

    result = await db.execute(
        select(Membership)
        .where(Membership.room_id == room_id)
        .options(selectinload(Membership.user))
    )
    memberships = result.scalars().all()

    from app.ws.manager import manager
    online = manager.get_room_users(room_id)

    return [{
        "user_id": m.user.id,
        "username": m.user.username,
        "display_name": m.user.display_name,
        "avatar_url": m.user.avatar_url,
        "role": m.role,
        "is_online": m.user.id in online,
        "joined_at": m.joined_at.isoformat(),
    } for m in memberships]
```

## Presence Tracker

```python
# app/ws/presence.py
import time
import asyncio
from app.ws.manager import manager

class PresenceTracker:
    """Tracks user presence with heartbeats and cleanup."""

    def __init__(self, heartbeat_interval: int = 30, offline_timeout: int = 90):
        self.heartbeat_interval = heartbeat_interval
        self.offline_timeout = offline_timeout

    async def start_cleanup_loop(self):
        """Periodically clean up stale presence entries."""
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            now = time.time()
            stale_users = [
                uid for uid, last_beat in manager.online_users.items()
                if now - last_beat > self.offline_timeout
            ]
            for uid in stale_users:
                await manager._broadcast_presence(uid, "offline")
                async with manager._lock:
                    manager.online_users.pop(uid, None)

presence_tracker = PresenceTracker()

@app.on_event("startup")
async def start_presence_tracker():
    asyncio.create_task(presence_tracker.start_cleanup_loop())
```

## Message Search

```python
# app/api/v1/messages.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.get("/search")
async def search_messages(
    q: str = Query(..., min_length=2),
    room_id: int | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Message)
        .join(Membership)
        .where(
            Membership.user_id == user.id,
            Message.is_deleted == False,
            Message.content.ilike(f"%{q}%"),
        )
    )

    if room_id:
        query = query.where(Message.room_id == room_id)

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar()
    query = query.order_by(desc(Message.created_at)).offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    messages = result.scalars().all()

    return {
        "messages": [
            {"id": m.id, "room_id": m.room_id, "content": m.content, "sender_id": m.sender_id, "created_at": m.created_at.isoformat()}
            for m in messages
        ],
        "total": total,
        "page": page,
    }
```

## Scaling with Redis Pub/Sub

```python
# app/core/redis_pubsub.py
import asyncio
import json
import redis.asyncio as aioredis
from app.ws.manager import manager

class RedisPubSub:
    """Redis-based pub/sub for multi-server WebSocket broadcasting."""

    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()

    async def subscribe(self, channel: str):
        await self.pubsub.subscribe(channel)

    async def publish(self, channel: str, message: dict):
        await self.redis.publish(channel, json.dumps(message, default=str))

    async def listen(self, channel: str):
        await self.subscribe(channel)
        async for msg in self.pubsub.listen():
            if msg["type"] == "message":
                data = json.loads(msg["data"])
                await self._handle_message(data)

    async def _handle_message(self, data: dict):
        """Route Redis messages to local WebSocket connections."""
        msg_type = data.get("type")

        if msg_type == "room_broadcast":
            room_id = data["room_id"]
            user_ids = manager.room_users.get(room_id, set())
            for uid in user_ids:
                await manager.send_to_user(uid, data["payload"])

        elif msg_type == "user_message":
            user_id = data["user_id"]
            await manager.send_to_user(user_id, data["payload"])

        elif msg_type == "presence_update":
            user_id = data["user_id"]
            await manager._broadcast_presence(user_id, data["status"])

    async def broadcast_to_room(self, room_id: int, message: dict):
        """Publish to Redis so all servers can deliver to their local connections."""
        await self.publish("chat:rooms", {
            "type": "room_broadcast",
            "room_id": room_id,
            "payload": message,
        })

    async def send_to_user(self, user_id: int, message: dict):
        """Send to a specific user across all servers."""
        await self.publish("chat:users", {
            "type": "user_message",
            "user_id": user_id,
            "payload": message,
        })

    async def start_listener(self):
        """Background listener for Redis pub/sub."""
        await self.pubsub.subscribe("chat:rooms", "chat:users")
        async for msg in self.pubsub.listen():
            if msg["type"] == "message":
                data = json.loads(msg["data"])
                await self._handle_message(data)


redis_pubsub = RedisPubSub("redis://localhost:6379")

@app.on_event("startup")
async def start_redis_listener():
    asyncio.create_task(redis_pubsub.start_listener())
```

## File Upload

```python
# app/api/v1/files.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import uuid
import os

UPLOAD_DIR = "/tmp/chat_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = {
    "image/jpeg", "image/png", "image/gif", "image/webp",
    "application/pdf", "text/plain",
    "application/zip",
}

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_active_user),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"File type {file.content_type} not allowed")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")

    ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(content)

    is_image = file.content_type.startswith("image/")

    return {
        "url": f"/files/{filename}",
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "message_type": "image" if is_image else "file",
    }
```

## Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql+asyncpg://chat:secret@db:5432/chatdb
      - REDIS_URL=redis://redis:6379/0
    depends_on: [db, redis]

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: chatdb
      POSTGRES_USER: chat
      POSTGRES_PASSWORD: secret
    volumes: [pgdata:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on: [api]

volumes:
  pgdata:
```

```nginx
# nginx.conf
upstream api {
    server api:8000;
}

server {
    listen 80;

    location / {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }
}
```

## Requirements

```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy[asyncio]==2.0.35
asyncpg==0.29.0
alembic==1.13.0
pydantic[email]==2.9.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
redis[hiredis]==5.1.0
python-multipart==0.0.9
Pillow==10.4.0
websockets==12.0
aiofiles==24.1.0
```
