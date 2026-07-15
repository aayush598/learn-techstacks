# WebSocket with TypeScript

## Overview

WebSockets provide real-time, bidirectional communication between client and server. TypeScript adds type safety to events, messages, rooms, and middleware in both Socket.io and native WebSocket implementations.

---

## 1. Socket.io Server Setup

```typescript
import { Server, Socket } from 'socket.io';
import { createServer } from 'http';
import express from 'express';

const app = express();
const httpServer = createServer(app);

// Typed server
const io = new Server(httpServer, {
  cors: {
    origin: 'http://localhost:3000',
    methods: ['GET', 'POST'],
  },
});

// Event type definitions
interface ServerToClientEvents {
  'message:received': (message: ChatMessage) => void;
  'user:joined': (data: { userId: string; username: string }) => void;
  'user:left': (data: { userId: string }) => void;
  'typing:start': (data: { userId: string; username: string }) => void;
  'typing:stop': (data: { userId: string }) => void;
  'notification': (notification: Notification) => void;
}

interface ClientToServerEvents {
  'message:send': (data: { content: string; room: string }) => void;
  'room:join': (data: { roomId: string }) => void;
  'room:leave': (data: { roomId: string }) => void;
  'typing:start': (data: { room: string }) => void;
  'typing:stop': (data: { room: string }) => void;
}

interface InterServerEvents {
  'ping': () => void;
}

interface SocketData {
  userId: string;
  username: string;
  rooms: Set<string>;
}

// Typed socket
type TypedSocket = Socket<ClientToServerEvents, ServerToClientEvents, InterServerEvents, SocketData>;
type TypedServer = Server<ClientToServerEvents, ServerToClientEvents, InterServerEvents, SocketData>;

// Chat message type
interface ChatMessage {
  id: string;
  content: string;
  sender: {
    id: string;
    username: string;
  };
  room: string;
  timestamp: Date;
}

interface Notification {
  id: string;
  type: 'info' | 'warning' | 'success';
  message: string;
  timestamp: Date;
}

// Middleware for authentication
io.use((socket: TypedSocket, next) => {
  const token = socket.handshake.auth.token;
  if (!token) {
    return next(new Error('Authentication required'));
  }

  try {
    const payload = verifyToken(token);
    socket.data.userId = payload.userId;
    socket.data.username = payload.username;
    socket.data.rooms = new Set();
    next();
  } catch {
    next(new Error('Invalid token'));
  }
});

// Connection handler
io.on('connection', (socket: TypedSocket) => {
  console.log(`User connected: ${socket.data.username}`);

  socket.on('room:join', (data) => {
    socket.join(data.roomId);
    socket.data.rooms.add(data.roomId);

    // Notify others in the room
    socket.to(data.roomId).emit('user:joined', {
      userId: socket.data.userId,
      username: socket.data.username,
    });
  });

  socket.on('room:leave', (data) => {
    socket.leave(data.roomId);
    socket.data.rooms.delete(data.roomId);

    socket.to(data.roomId).emit('user:left', {
      userId: socket.data.userId,
    });
  });

  socket.on('message:send', (data) => {
    const message: ChatMessage = {
      id: crypto.randomUUID(),
      content: data.content,
      sender: {
        id: socket.data.userId,
        username: socket.data.username,
      },
      room: data.room,
      timestamp: new Date(),
    };

    // Broadcast to the room
    io.to(data.room).emit('message:received', message);
  });

  socket.on('typing:start', (data) => {
    socket.to(data.room).emit('typing:start', {
      userId: socket.data.userId,
      username: socket.data.username,
    });
  });

  socket.on('typing:stop', (data) => {
    socket.to(data.room).emit('typing:stop', {
      userId: socket.data.userId,
    });
  });

  socket.on('disconnect', () => {
    // Notify all rooms this user was in
    for (const roomId of socket.data.rooms) {
      socket.to(roomId).emit('user:left', {
        userId: socket.data.userId,
      });
    }
  });
});
```

---

## 2. Socket.io Client

```typescript
import { io, Socket } from 'socket.io-client';

// Same event types (shared between client and server)
interface ServerToClientEvents {
  'message:received': (message: ChatMessage) => void;
  'user:joined': (data: { userId: string; username: string }) => void;
  'user:left': (data: { userId: string }) => void;
  'typing:start': (data: { userId: string; username: string }) => void;
  'typing:stop': (data: { userId: string }) => void;
  'notification': (notification: Notification) => void;
}

interface ClientToServerEvents {
  'message:send': (data: { content: string; room: string }) => void;
  'room:join': (data: { roomId: string }) => void;
  'room:leave': (data: { roomId: string }) => void;
  'typing:start': (data: { room: string }) => void;
  'typing:stop': (data: { room: string }) => void;
}

// Typed client socket
type TypedClientSocket = Socket<ServerToClientEvents, ClientToServerEvents>;

// Create connection
const socket: TypedClientSocket = io('http://localhost:3000', {
  auth: {
    token: localStorage.getItem('token'),
  },
});

// Type-safe event emission
socket.emit('message:send', {
  content: 'Hello, world!',
  room: 'general',
});

// Type-safe event listening
socket.on('message:received', (message) => {
  // message is fully typed as ChatMessage
  console.log(`${message.sender.username}: ${message.content}`);
});

socket.on('user:joined', (data) => {
  console.log(`${data.username} joined the room`);
});

socket.on('notification', (notification) => {
  console.log(`[${notification.type}] ${notification.message}`);
});

// React hook for typed socket
function useSocket() {
  const [socket, setSocket] = useState<TypedClientSocket | null>(null);

  useEffect(() => {
    const newSocket: TypedClientSocket = io('http://localhost:3000', {
      auth: { token: localStorage.getItem('token') },
    });
    setSocket(newSocket);

    return () => { newSocket.disconnect(); };
  }, []);

  return socket;
}

// Usage in React component
function ChatRoom({ roomId }: { roomId: string }) {
  const socket = useSocket();
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  useEffect(() => {
    if (!socket) return;

    socket.emit('room:join', { roomId });

    socket.on('message:received', (message) => {
      setMessages((prev) => [...prev, message]);
    });

    return () => {
      socket.emit('room:leave', { roomId });
      socket.off('message:received');
    };
  }, [socket, roomId]);

  const sendMessage = (content: string) => {
    socket?.emit('message:send', { content, room: roomId });
  };

  return (
    <div>
      {messages.map((msg) => (
        <div key={msg.id}>
          <strong>{msg.sender.username}</strong>: {msg.content}
        </div>
      ))}
      <MessageInput onSend={sendMessage} />
    </div>
  );
}
```

---

## 3. Typed Rooms

```typescript
// Room management with types
interface RoomState {
  users: Map<string, { userId: string; username: string; joinedAt: Date }>;
  messages: ChatMessage[];
}

class TypedRoomManager {
  private rooms = new Map<string, RoomState>();

  joinRoom(roomId: string, user: { userId: string; username: string }): void {
    if (!this.rooms.has(roomId)) {
      this.rooms.set(roomId, { users: new Map(), messages: [] });
    }

    const room = this.rooms.get(roomId)!;
    room.users.set(user.userId, {
      ...user,
      joinedAt: new Date(),
    });
  }

  leaveRoom(roomId: string, userId: string): void {
    const room = this.rooms.get(roomId);
    if (room) {
      room.users.delete(userId);
      if (room.users.size === 0) {
        this.rooms.delete(roomId);
      }
    }
  }

  getUsers(roomId: string): Array<{ userId: string; username: string }> {
    const room = this.rooms.get(roomId);
    if (!room) return [];
    return Array.from(room.users.values());
  }

  addMessage(roomId: string, message: ChatMessage): void {
    const room = this.rooms.get(roomId);
    if (room) {
      room.messages.push(message);
      // Keep only last 100 messages
      if (room.messages.length > 100) {
        room.messages.shift();
      }
    }
  }

  getMessages(roomId: string, limit: number = 50): ChatMessage[] {
    const room = this.rooms.get(roomId);
    if (!room) return [];
    return room.messages.slice(-limit);
  }
}
```

---

## 4. Native WebSocket with TypeScript

```typescript
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';

// Typed WebSocket server
interface WSServer extends WebSocket {
  userId?: string;
  username?: string;
  isAlive: boolean;
}

// Message types
type WSMessage =
  | { type: 'auth'; token: string }
  | { type: 'message'; content: string; room: string }
  | { type: 'join'; room: string }
  | { type: 'leave'; room: string }
  | { type: 'ping' };

type WSResponse =
  | { type: 'message'; id: string; content: string; sender: string; room: string; timestamp: string }
  | { type: 'user_joined'; userId: string; username: string; room: string }
  | { type: 'user_left'; userId: string; room: string }
  | { type: 'error'; message: string }
  | { type: 'pong' };

const wss = new WebSocketServer({ port: 8080 });

wss.on('connection', (ws: WSServer, req: IncomingMessage) => {
  ws.isAlive = true;

  ws.on('pong', () => { ws.isAlive = true; });

  ws.on('message', (data: Buffer) => {
    try {
      const message: WSMessage = JSON.parse(data.toString());
      handleMessage(ws, message);
    } catch {
      sendError(ws, 'Invalid message format');
    }
  });

  ws.on('close', () => {
    if (ws.userId) {
      broadcast({ type: 'user_left', userId: ws.userId, room: 'general' });
    }
  });
});

function handleMessage(ws: WSServer, message: WSMessage): void {
  switch (message.type) {
    case 'auth':
      try {
        const payload = verifyToken(message.token);
        ws.userId = payload.userId;
        ws.username = payload.username;
      } catch {
        sendError(ws, 'Authentication failed');
      }
      break;

    case 'message':
      if (!ws.userId) {
        sendError(ws, 'Not authenticated');
        return;
      }
      broadcast({
        type: 'message',
        id: crypto.randomUUID(),
        content: message.content,
        sender: ws.username!,
        room: message.room,
        timestamp: new Date().toISOString(),
      });
      break;

    case 'join':
      broadcast({
        type: 'user_joined',
        userId: ws.userId!,
        username: ws.username!,
        room: message.room,
      });
      break;
  }
}

function sendError(ws: WSServer, message: string): void {
  const response: WSResponse = { type: 'error', message };
  ws.send(JSON.stringify(response));
}

function broadcast(response: WSResponse): void {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(response));
    }
  });
}

// Heartbeat
const interval = setInterval(() => {
  wss.clients.forEach((ws: WSServer) => {
    if (!ws.isAlive) return ws.terminate();
    ws.isAlive = false;
    ws.ping();
  });
}, 30000);

wss.on('close', () => clearInterval(interval));
```

---

## 5. Best Practices

1. **Define event types centrally** — share between client and server.
2. **Use discriminated unions** for message types.
3. **Always authenticate** WebSocket connections.
4. **Type room state** for complex multi-user scenarios.
5. **Use DataLoaders** for database queries triggered by WebSocket events.
6. **Implement heartbeat** to detect disconnected clients.
7. **Handle errors gracefully** — always send typed error responses.
8. **Clean up listeners** — remove event handlers on disconnect.
9. **Use rooms** for targeted broadcasting.
10. **Validate all incoming messages** — never trust the client.

---

## Interview Questions

1. How do you type Socket.io events in TypeScript?
2. What is the difference between `broadcast` and `to().emit()`?
3. How do you share event types between client and server?
4. Explain the authentication middleware pattern for WebSockets.
5. How do you handle reconnection in typed WebSocket clients?
6. What are the advantages of Socket.io over native WebSockets?
7. How do you type WebSocket rooms?
8. How do you handle scaling WebSockets across multiple servers?
9. What is the heartbeat pattern and why is it needed?
10. How do you test WebSocket event handlers with TypeScript?
