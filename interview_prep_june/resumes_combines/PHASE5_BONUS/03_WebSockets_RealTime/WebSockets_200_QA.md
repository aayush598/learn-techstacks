# WebSockets & Real-Time - 150+ Interview Q&A

### Q1: What are WebSockets?
**Answer:** Full-duplex communication protocol over TCP. Single persistent connection. HTTP upgrade handshake. No polling needed. Used for real-time apps: chat, notifications, live updates, gaming.

### Q2: WebSocket vs SSE vs Polling?
**Answer:** Polling: client periodically requests. Long-polling: hold connection until data available. SSE: server → client only, auto-reconnect. WebSocket: bidirectional, lower overhead. Use WebSocket for chat/games, SSE for notifications.

### Q3: How to implement WebSocket in FastAPI?
**Answer:** `@app.websocket("/ws")` with `websocket: WebSocket`. Accept/close connection. `await websocket.send_json()` and `await websocket.receive_json()`. Manage connections with WebSocket connection manager class.

### Q4: WebSocket connection manager?
**Answer:** Class that tracks active connections (list of WebSocket objects). Methods: connect (add + broadcast join), disconnect (remove + broadcast leave), send_personal_message, broadcast (iterate all connections). Handle cleanup on disconnect.

### Q5: Scaling WebSockets?
**Answer:** Single server: simple. Multiple servers: use Redis pub/sub. Server receives message → publishes to Redis channel → other servers receive → forward to their connected clients. Socket.IO handles this.

### Q6: Socket.IO vs native WebSocket?
**Answer:** Socket.IO: fallback to polling, auto-reconnect, rooms, namespaces, easier API. Native WebSocket: lower-level, better performance, less overhead. Use Socket.IO for convenience, native for performance-critical.

### Q7: WebSocket authentication?
**Answer:** Token in query string during connection: `new WebSocket("ws://host?token=jwt")`. Validate token in websocket.connect handler. Don't rely on cookies for WebSocket auth (browser behavior varies).

### Q8: WebSocket security considerations?
**Answer:** Validate Origin header. Authenticate on connect. Implement rate limiting per connection. Handle disconnection gracefully. Input sanitization. WSS (TLS) required. Close malformed connections.
