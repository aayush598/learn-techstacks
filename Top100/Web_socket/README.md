# WebSocket Interview Questions and Answers

## Q1: What is WebSocket?
**A:** WebSocket is a communication protocol providing full-duplex, bidirectional communication channels over a single TCP connection. It enables real-time data exchange between client and server with low latency, persisting the connection after the initial HTTP handshake.

## Q2: How does WebSocket differ from HTTP?
**A:** HTTP is request-response based (client initiates, server responds) with connection overhead per request. WebSocket is bidirectional with persistent connections, allowing server-initiated messages, lower latency, and reduced overhead after initial handshake.

## Q3: What is the WebSocket handshake?
**A:** The WebSocket handshake upgrades an HTTP connection to WebSocket. The client sends an Upgrade request with headers including `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key`, and `Sec-WebSocket-Version`. The server responds with 101 Switching Protocols.

## Q4: What is the WebSocket URL scheme?
**A:** WebSocket uses `ws://` for unencrypted and `wss://` for encrypted (TLS) connections. WSS is the WebSocket equivalent of HTTPS, providing encryption over TLS. Most production systems require WSS.

## Q5: What is the difference between ws:// and wss://?
**A:** `ws://` is unencrypted WebSocket, transmitting data in plaintext. `wss://` uses TLS encryption, protecting data in transit. WSS is mandatory in browsers for secure contexts and is recommended for production to prevent eavesdropping.

## Q6: What is a WebSocket frame?
**A:** A WebSocket frame is the smallest unit of data transmission. Frames have an opcode (text, binary, close, ping, pong), payload length, masking key (client-to-server), and payload data. Multiple frames can form a single message.

## Q7: What are WebSocket opcodes?
**A:** Opcodes indicate frame type: 0x1 (text), 0x2 (binary), 0x8 (close), 0x9 (ping), 0xA (pong). Text frames contain UTF-8 encoded data. Binary frames contain raw bytes. Control frames (0x8-0xA) manage the connection lifecycle.

## Q8: What is masking in WebSocket frames?
**A:** Masking is a security mechanism where client-to-server frames XOR the payload with a 32-bit mask key. It prevents cache poisoning attacks by ensuring proxies cannot interpret intercepted WebSocket traffic as regular HTTP.

## Q9: Why must client-to-server frames be masked?
**A:** Masking prevents malicious scripts from poisoning HTTP caches. Without masking, an attacker could craft WebSocket data that looks like an HTTP response, tricking intermediaries into caching responses from non-HTTP origins.

## Q10: What is the WebSocket close frame?
**A:** The close frame (opcode 0x8) initiates connection termination. It can include a status code (1000-normal, 1001-going away, etc.) and optional reason string. Both sides must send and receive close frames for proper closure.

## Q11: What are common WebSocket close codes?
**A:** Key close codes: 1000 (Normal Closure), 1001 (Going Away), 1002 (Protocol Error), 1003 (Unsupported Data), 1005 (No Status Received), 1006 (Abnormal Closure), 1009 (Message Too Big), 1011 (Internal Error).

## Q12: What is the WebSocket ping/pong mechanism?
**A:** Ping frames (0x9) and pong frames (0xA) implement keep-alive health checks. The server sends a ping, and the client must respond with a pong. This detects dead connections and maintains proxy/NAT keep-alive.

## Q13: What is the maximum WebSocket message size?
**A:** The WebSocket protocol supports messages up to 2^63 bytes theoretically. In practice, implementations impose limits (e.g., 1MB default in Node.js `ws`, configurable). Larger messages should be fragmented or streamed.

## Q14: What is WebSocket fragmentation?
**A:** Fragmentation splits a large message into multiple frames. The first fragment has the FIN bit unset and opcode set. Intermediate fragments have FIN=0, opcode=0x0 (continuation). The final fragment has FIN=1. This enables streaming large messages.

## Q15: What is a WebSocket subprotocol?
**A:** Subprotocols are application-level protocols negotiated during the WebSocket handshake via the `Sec-WebSocket-Protocol` header. Examples include: WAMP (WAMP), MQTT over WebSocket, STOMP over WebSocket, and custom protocols.

## Q16: How does WebSocket perform compared to HTTP long-polling?
**A:** WebSocket eliminates HTTP overhead (headers, connection setup) for each message, reducing latency and bandwidth. Long-polling requires repeated HTTP requests, higher latency, and more server resources. WebSocket is superior for real-time applications.

## Q17: What is Server-Sent Events (SSE) vs WebSocket?
**A:** SSE is unidirectional server-to-client streaming over HTTP, simpler to implement, with automatic reconnection. WebSocket is bidirectional, more complex, and supports binary data. Choose SSE for server updates, WebSocket for interactive communication.

## Q18: What are the advantages of WebSocket?
**A:** Advantages include: full-duplex bidirectional communication, persistent connection, low latency, reduced bandwidth (minimal headers after handshake), server push capability, and cross-origin support via CORS.

## Q19: What are the disadvantages of WebSocket?
**A:** Disadvantages include: requires stateful servers (harder to scale), firewall/proxy issues (some proxies block WebSocket), no built-in reconnection, no built-in message acknowledgments (requires custom implementation), and NAT timeout management.

## Q20: What is WebSocket in Node.js?
**A:** Popular Node.js WebSocket libraries include: `ws` (lightweight, fast), `socket.io` (full-featured with fallbacks), and `uWebSockets.js` (high-performance C++ bindings). The `ws` library is the most common for raw WebSocket implementation.

## Q21: What is Socket.IO?
**A:** Socket.IO is a real-time engine that uses WebSocket as its primary transport with fallbacks (HTTP long-polling, etc.). It adds features like rooms, namespaces, automatic reconnection, acknowledgments, and broadcasting.

## Q22: How does Socket.IO differ from raw WebSocket?
**A:** Socket.IO adds: automatic reconnection, room/namespace abstraction, event-based messaging, acknowledgment callbacks, binary support, multiplexing, and transparent fallback to long-polling when WebSocket isn't available.

## Q23: What is the WebSocket API in browsers?
**A:** The browser WebSocket API provides the `WebSocket` object with: `send()` for outgoing messages, `onmessage` event for incoming data, `onopen`/`onclose`/`onerror` events, and `readyState` property (CONNECTING, OPEN, CLOSING, CLOSED).

## Q24: What are the WebSocket readyState values?
**A:** `0-CONNECTING` (connection not yet open), `1-OPEN` (ready to send/receive), `2-CLOSING` (close in progress), `3-CLOSED` (connection closed or failed to open). The state determines allowed operations.

## Q25: How do you handle WebSocket reconnection?
**A:** Custom reconnection logic includes: exponential backoff (1s, 2s, 4s...), max retry limit, jitter to prevent thundering herd, and state restoration. Libraries like Socket.IO and ReconnectingWebSocket provide built-in reconnection.

## Q26: What is exponential backoff for WebSocket?
**A:** Exponential backoff increases reconnection delay exponentially after each failed attempt (e.g., 1s, 2s, 4s, 8s...) to prevent overwhelming the server during outages. Jitter adds randomness to avoid synchronized reconnection storms.

## Q27: What is a WebSocket room or channel?
**A:** Rooms are logical groupings of WebSocket connections for targeted message broadcasting. Not built into raw WebSocket, but provided by libraries like Socket.IO (rooms) or custom implementations using connection registries.

## Q28: What is broadcasting in WebSocket?
**A:** Broadcasting sends a message to multiple connected clients simultaneously. Raw WebSocket requires iterating over all connections. Libraries like Socket.IO provide `io.emit()` for broadcasting and room-targeted emitting.

## Q29: How do you scale WebSocket connections?
**A:** Scaling strategies include: sticky sessions (load balancer routes by client), shared pub/sub (Redis, Kafka) for cross-server message passing, connection pooling, horizontal scaling with stateless authentication, and using WebSocket-proxies.

## Q30: What is sticky session (session affinity) for WebSocket?
**A:** Sticky sessions route a client to the same server for all requests using cookies or IP hashing. Necessary for WebSocket scaling because connections are stateful (tied to a specific server process).

## Q31: How does Redis Pub/Sub work with WebSocket?
**A:** Redis Pub/Sub enables cross-server WebSocket communication. When server A broadcasts a message, it publishes to Redis. Other servers subscribe to Redis and forward the message to their local WebSocket connections, enabling horizontal scaling.

## Q32: What is a WebSocket proxy?
**A:** WebSocket proxies (nginx, HAProxy, Envoy) handle WebSocket upgrade requests and maintain persistent connections. They must support the Upgrade mechanism, connection keep-alive, and proper header forwarding.

## Q33: How do you configure Nginx for WebSocket?
**A:** Nginx requires: `proxy_http_version 1.1;`, `proxy_set_header Upgrade $http_upgrade;`, `proxy_set_header Connection "upgrade";` in the location block to properly proxy WebSocket connections.

## Q34: What is the WebSocket lifecycle?
**A:** Lifecycle: 1) Client initiates HTTP upgrade handshake, 2) Server responds with 101 Switching Protocols, 3) Connection upgrades to WebSocket (OPEN), 4) Bidirectional messaging occurs, 5) Either side initiates close, 6) Connection terminates (CLOSED).

## Q35: What happens if a WebSocket connection drops?
**A:** On connection drop, the socket's `onclose` event fires with code 1006 (Abnormal Closure). The server sees the TCP connection close. The client must implement reconnection logic. In-flight messages may be lost.

## Q36: What is WebSocket rate limiting?
**A:** Rate limiting controls message frequency per connection to prevent abuse. Strategies include: tokens per second, message size limits, connection count limits per IP, and server-side throttling with backpressure signals.

## Q37: What is backpressure in WebSocket?
**A:** Backpressure occurs when the server can't send data as fast as it's producing it, causing buffer growth. Solutions include: monitoring buffer size, implementing flow control, dropping messages, or using write buffering with drain events.

## Q38: How do you authenticate WebSocket connections?
**A:** Authentication can use: token in the initial HTTP request (query string, cookie), token exchanged after connection via auth message, or session-based auth from the HTTP handshake. Tokens should be short-lived and validated server-side.

## Q39: What is the security risk of token in WebSocket URL?
**A:** Tokens in WebSocket URLs are logged by servers, proxies, and browsers (history). If leaked, attackers can hijack connections. Prefer cookies or auth messages after connection establishment for sensitive tokens.

## Q40: How do you handle CORS with WebSocket?
**A:** WebSocket has no same-origin policy like HTTP. The server validates the `Origin` header during the handshake and rejects connections from unauthorized origins. Browsers do not enforce CORS for WebSocket.

## Q41: What is WebSocket origin checking?
**A:** The server checks the `Origin` header in the upgrade request against a whitelist of allowed origins. Mismatched origins are rejected with a 403 response, preventing cross-site WebSocket hijacking attacks.

## Q42: What is WebSocket Secure (WSS) and TLS?
**A:** WSS runs WebSocket over TLS (Transport Layer Security), encrypting all data in transit. It uses the `wss://` scheme on port 443 by default. WSS prevents eavesdropping, tampering, and man-in-the-middle attacks.

## Q43: What is the worst-case latency for WebSocket?
**A:** Worst-case latency includes: network round-trip time, TLS handshake overhead (1-2 RTTs), server processing time, and buffering. Under normal conditions, WebSocket adds minimal overhead beyond TCP/TLS latency.

## Q44: What is a WebSocket ping interval?
**A:** A ping interval (e.g., 30 seconds) sends periodic ping frames to detect dead connections, maintain NAT/firewall mappings, and verify connection health. Interval timing balances responsiveness with network overhead.

## Q45: What is the WebSocket perframe-deflate extension?
**A:** The `permessage-deflate` extension enables per-message compression using DEFLATE. It reduces bandwidth for text-based protocols (JSON, XML) at the cost of CPU overhead for compression/decompression.

## Q46: What protocols can run over WebSocket?
**A:** Protocols that run over WebSocket include: STOMP (messaging), MQTT (IoT), AMQP (queuing), WAMP (RPC/pub-sub), XMPP (chat), JSON-RPC, and custom application protocols. The subprotocol is negotiated during handshake.

## Q47: What is STOMP over WebSocket?
**A:** STOMP (Simple Text Oriented Messaging Protocol) over WebSocket provides a messaging framework with destinations, subscriptions, and transactions. Used with message brokers like ActiveMQ and RabbitMQ via WebSocket transport.

## Q48: What is MQTT over WebSocket?
**A:** MQTT (Message Queuing Telemetry Transport) over WebSocket enables IoT messaging in browser environments. MQTT's pub/sub model with QoS levels runs over WebSocket transport for real-time IoT dashboards.

## Q49: What is WAMP (Web Application Messaging Protocol)?
**A:** WAMP is a subprotocol providing both RPC (Remote Procedure Call) and Pub/Sub over WebSocket. It's designed for microservice communication and real-time web applications requiring both messaging patterns.

## Q50: How does WebSocket work with HTTP/2?
**A:** HTTP/2 has its own server push and multiplexing but does not replace WebSocket's bidirectional streaming. The WebSocket-over-HTTP/2 specification (RFC 8441) enables tunneling WebSocket over HTTP/2 streams for efficient multiplexing.

## Q51: What is HTTP/2 and WebSocket coexistence?
**A:** HTTP/2 and WebSocket serve different purposes. HTTP/2 optimizes request-response multiplexing. WebSocket provides full-duplex streaming. They can coexist: HTTP/2 for REST APIs, WebSocket for real-time features, with separate ports or multiplexed tunneling.

## Q52: What is a WebSocket load balancer?
**A:** WebSocket load balancers (HAProxy, Nginx, AWS ALB, GCP TCP LB) distribute connections across servers. They must support long-lived TCP connections, proper Upgrade header handling, and either sticky sessions or shared state.

## Q53: How does AWS ALB handle WebSocket?
**A:** AWS ALB natively supports WebSocket. It passes through Upgrade headers, maintains sticky sessions via cookies, and supports health checks for target groups. Connection idle timeout is configurable (default 60s).

## Q54: How do you monitor WebSocket connections?
**A:** Monitoring includes: active connections count, message throughput, latency, error rates (close codes), reconnection rates, buffer sizes, CPU/memory per connection, and custom health check pings with response time tracking.

## Q55: What is the maximum concurrent WebSocket connections?
**A:** Browser limits vary (~200 per domain). Server limits depend on: file descriptors (ulimit -n), memory per connection (2-20KB), CPU, network bandwidth, and architecture. Single servers can handle 100K-1M connections with proper tuning.

## Q56: What is the C10K problem in WebSocket?
**A:** The C10K problem (handling 10,000+ concurrent connections) applies to WebSocket servers. Solutions include: event-driven architectures (epoll, kqueue), asynchronous I/O (Node.js, asyncio), lightweight threads (goroutines), and proper resource management.

## Q57: How does WebSocket consume server resources?
**A:** Each WebSocket connection consumes: a TCP socket, file descriptor, memory for send/receive buffers (typically 64KB+), connection state, and application-level data. Connections are "idle but alive," consuming resources even when inactive.

## Q58: What is the WebSocket Autobahn test suite?
**A:** Autobahn is a comprehensive WebSocket protocol compliance test suite. It tests: handshake, framing, fragmentation, close behavior, ping/pong, compression, and edge cases. Servers should pass Autobahn fuzzing tests for spec compliance.

## Q59: What is a WebSocket fuzzing test?
**A:** Fuzzing tests send malformed, unexpected, or boundary-case WebSocket frames to verify server robustness. Autobahn includes fuzzing tests for invalid opcodes, oversized payloads, incorrect masking, and protocol violations.

## Q60: What is a WebSocket extension?
**A:** WebSocket extensions are negotiated during the handshake via `Sec-WebSocket-Extensions` header. The primary extension is `permessage-deflate` (compression). Extensions modify frame processing, adding features like compression or multiplexing.

## Q61: What is the `Sec-WebSocket-Key` header?
**A:** A random 16-byte base64-encoded value sent by the client in the upgrade request. The server concatenates it with a fixed GUID, SHA-1 hashes it, and returns the base64 result in `Sec-WebSocket-Accept` to confirm the upgrade.

## Q62: What is the `Sec-WebSocket-Accept` header?
**A:** The server's response header containing the computed hash: `base64(SHA1(Sec-WebSocket-Key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"))`. Proves the server understands the WebSocket protocol and agrees to the upgrade.

## Q63: What is the `Sec-WebSocket-Version` header?
**A:** Indicates the WebSocket protocol version. The current standard is version 13. Clients send their supported version. If the server doesn't support it, it responds with an error and lists supported versions.

## Q64: What happens during a WebSocket handshake failure?
**A:** Handshake failures occur due to: unsupported version, invalid key, missing headers, origin rejection, or CORS issues. The server returns an HTTP error (4xx/5xx) instead of 101. The client's `onerror` and `onclose` events fire.

## Q65: Can you send binary data over WebSocket?
**A:** Yes, WebSocket supports binary frames (opcode 0x2). Binary data (ArrayBuffer, Blob in browsers, Buffer in Node.js) is more efficient than base64-encoded text. The receiver checks the frame type via `event.binary` or instance type.

## Q66: How do you handle large messages in WebSocket?
**A:** Large messages should be fragmented (built-in), streamed, or split into chunks. Set appropriate max payload sizes. Consider using streaming APIs (`sender.replace()` for Node.js streams). Implement compression for text payloads.

## Q67: What is the WebSocket `message` event structure?
**A:** In browsers, `MessageEvent.data` contains the payload (string for text, Blob/ArrayBuffer for binary). `event.origin` is the server URL. `event.source` is null for WebSocket. `event.lastEventId` is empty (SSE-specific).

## Q68: How do you handle different data types in WebSocket?
**A:** Check `event.data` type (string vs. Blob vs. ArrayBuffer). For binary, use `event.data instanceof ArrayBuffer` or configure `socket.binaryType = 'arraybuffer'` in browsers. Server-side libraries provide Buffer objects.

## Q69: How does WebSocket handle flow control?
**A:** WebSocket lacks native flow control. Implementations: monitor `bufferedAmount` (queued data not yet sent), use drain events when buffer empties, apply backpressure by pausing data production, and implement application-level ACKs.

## Q70: What is `bufferedAmount` in WebSocket?
**A:** `bufferedAmount` (read-only) returns the bytes queued for transmission but not yet sent to the network. Applications check this to avoid overwhelming the socket with data, implementing flow control at the application level.

## Q71: What is the WebSocket GC behavior?
**A:** Abandoned WebSocket objects without proper `close()` lead to memory leaks (open sockets, pending callbacks). Browser GC does not close connections. Always call `close()` and nullify references. Use connection pools with cleanup.

## Q72: What is the WebSocket connection timeout?
**A:** Timed out connections: TCP connections have OS-level timeouts (hours). Proxy/NAT timeouts (30-120s common). Application-level ping/pong keeps connections alive. Configure proxy idle timeout higher than ping interval.

## Q73: What is the difference between WebSocket and Socket.IO?
**A:** Socket.IO is built on WebSocket but adds: auto-reconnection, room/namespace abstractions, event-based messaging, fallback transports, ACKs, and middleware. Raw WebSocket is lower-level, more control, no built-in features.

## Q74: What is Socket.IO adapter?
**A:** Socket.IO adapters enable horizontal scaling by sharing events across servers. The Redis adapter is most common: it publishes events to Redis, and all Socket.IO servers receive and forward to their local connections.

## Q75: What is a WebSocket cluster?
**A:** A WebSocket cluster horizontally distributes connections across multiple servers with shared state (Redis/Kafka) for cross-server messaging, sticky sessions for connection routing, and load balancers for distribution.

## Q76: How do you debug WebSocket connections?
**A:** Chrome DevTools Network tab shows WebSocket frames (time, direction, payload, length). Browser `socket.onmessage`/`onerror` logging. Server-side frame logging. Tools: Wireshark, Charles Proxy, and WebSocket echo servers.

## Q77: What is a WebSocket echo server?
**A:** An echo server immediately sends back any received message. Used for testing WebSocket implementations, latency measurement, and connection health verification. WebSocket.org provides a public echo server at `wss://echo.websocket.org`.

## Q78: What is Wireshark WebSocket analysis?
**A:** Wireshark can capture and analyze WebSocket frames including: handshake headers, frame types (text, binary, ping, pong, close), masking status, payload content, and reassembled messages for deep protocol debugging.

## Q79: What is the challenge with WebSocket in serverless?
**A:** Serverless (AWS Lambda, CloudFlare Workers) has short execution time limits. WebSocket connections are stateful and long-lived, conflicting with serverless statelessness. AWS API Gateway WebSocket provides managed WebSocket with Lambda integration.

## Q80: How does AWS API Gateway WebSocket work?
**A:** AWS API Gateway WebSocket manages persistent connections. Routes: `$connect` (auth), `$disconnect`, `$default` (messages), and custom routes. Lambda handles each event. The `@connections` API sends messages to connected clients.

## Q81: What are the limitations of WebSocket in serverless?
**A:** Limitations include: idle timeout (10min-1hr), 128KB max message payload per frame (in some implementations), no built-in broadcasting (must iterate connections), cold start latency, and connection limits per API Gateway.

## Q82: How do you broadcast in serverless WebSocket?
**A:** Broadcasting requires tracking connections in a database (DynamoDB). On broadcast, retrieve all connection IDs and call API Gateway `PostToConnection` for each. Consider batching and handling stale connections (410 Gone).

## Q83: What is WebSocket in Python?
**A:** Popular Python WebSocket libraries: `websockets` (asyncio-based), `fastapi` (with WebSocket support), `channels` (Django WebSocket), `aiohttp` (client/server), and `socket.io` (python-socketio for Socket.IO server).

## Q84: What is FastAPI WebSocket?
**A:** FastAPI provides WebSocket support via `WebSocket` and `WebSocketEndpoint` classes. Supports `websocket_connect`, `websocket_receive`, `websocket_send`, and `websocket_disconnect` event handlers with dependency injection.

## Q85: What is Django Channels?
**A:** Django Channels extends Django to handle WebSocket, async HTTP, and other protocols. It uses ASGI (Asynchronous Server Gateway Interface) with a channel layer (Redis) for cross-process communication and consumer classes.

## Q86: What is WebSocket in Go?
**A:** Go WebSocket libraries: `gorilla/websocket` (widely used, stable), `nhooyr.io/websocket` (modern, context-aware), and `gobwas/ws` (low-level). Go's goroutine model handles concurrent connections efficiently.

## Q87: What is WebSocket in Java?
**A:** Java WebSocket support includes: JSR 356 standard API (`@ServerEndpoint`, `@ClientEndpoint`), Spring WebSocket (STOMP, raw WebSocket), Netty (high-performance), Tyrus (reference implementation), and Jetty WebSocket.

## Q88: What is Spring WebSocket?
**A:** Spring WebSocket provides: `WebSocketHandler` for raw WebSocket, STOMP messaging over WebSocket, `@MessageMapping` annotated handlers, `SimpMessagingTemplate` for broadcasting, and integration with Spring Security.

## Q89: What is STOMP for Spring WebSocket?
**A:** STOMP over WebSocket in Spring provides a pub/sub messaging model with destinations (`/topic/`, `/queue/`), `@MessageMapping` for handling, `@SendTo` for responses, and `SimpMessagingTemplate` for server-side broadcasting.

## Q90: What is WebSocket in .NET?
**A:** .NET WebSocket support includes: ASP.NET Core SignalR (high-level), native `WebSocket` class (low-level), `WebSocketMiddleware` in the pipeline, and `ClientWebSocket` for client connections. SignalR adds hubs, groups, and fallbacks.

## Q91: What is SignalR?
**A:** SignalR is ASP.NET Core's real-time framework using WebSocket with fallbacks. Features: Hubs (strongly-typed RPC), groups, streaming, automatic reconnection, and scaling with Redis/SignalR backplane.

## Q92: What is WebSocket in Rust?
**A:** Rust WebSocket libraries: `tokio-tungstenite` (async, tokio-based), `tungstenite` (blocking), `actix-web` with WebSocket support. Rust's zero-cost abstractions and memory safety make it suitable for high-performance WebSocket servers.

## Q93: What is the WebSocket ABR (Adaptive Bitrate) protocol?
**A:** ABR over WebSocket adapts streaming quality based on network conditions. The server monitors round-trip time and throughput, adjusting video/audio quality dynamically. Used in live streaming and real-time communication apps.

## Q94: How does WebSocket handle mobile connectivity changes?
**A:** Mobile network changes (WiFi to cellular) drop TCP connections. WebSocket detects disconnection via close event or failed ping. Mobile apps implement aggressive reconnection with state restoration and idempotency.

## Q95: What is WebSocket in IoT?
**A:** WebSocket in IoT: browser-dashboard integration (MQTT over WebSocket), real-time device control, sensor data streaming, and firmware update status. Constraints: resource-limited devices may use lightweight MQTT with WebSocket bridges.

## Q96: What is the memory footprint of WebSocket libraries?
**A:** Memory per connection varies: Node.js `ws` ~5-10KB, Go gorilla ~2-5KB, Rust tokio-tungstenite ~1-2KB, C++ uWebSockets ~0.5-1KB. Application state significantly increases per-connection memory.

## Q97: What is the future of WebSocket?
**A:** WebSocket remains dominant for real-time web. Trends: WebTransport (HTTP/3-based, UDP with reliability) as potential future alternative, continued adoption in microservices, improved HTTP/2 WebSocket tunneling, and enhanced security standards.

## Q98: What is WebTransport?
**A:** WebTransport is an emerging protocol using HTTP/3 (QUIC/UDP) providing: low-latency bidirectional streaming, unreliable (UDP-like) and reliable (TCP-like) modes, native multiplexing, and no head-of-line blocking.

## Q99: How does WebTransport compare to WebSocket?
**A:** WebTransport offers: lower latency (QUIC 0-RTT), multiple streams per connection, unreliable data support, native multiplexing without subprotocols, and better performance on lossy networks. WebSocket has wider current adoption and simpler API.

## Q100: What are common WebSocket interview scenarios?
**A:** Scenarios include: designing a real-time chat system, implementing live dashboards, building collaborative editing, handling multiplayer game state sync, creating a notification system, and architecting scalable WebSocket infrastructure.
