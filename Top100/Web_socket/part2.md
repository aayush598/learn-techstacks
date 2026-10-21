# WebSocket Interview Questions and Answers - Part 2

## Q1: What are the exact byte-level details of a WebSocket frame structure?
**A:** A WebSocket frame starts with: 1 bit FIN, 3 bits RSV (reserved for extensions), 4 bits opcode, 1 bit MASK, 7 bits payload length (or 7+16 if 126, or 7+64 if 127), optionally extended payload length (16 or 64 bits), optionally 4 bytes masking key (if MASK=1), then payload data. Total minimum overhead: 2 bytes for unmasked frames with small payloads.

## Q2: How does the WebSocket masking algorithm work at the bit level and why was the 32-bit mask key chosen?
**A:** The 32-bit mask key is XORed cyclically with the payload bytes: transformed_byte[i] = original_byte[i] XOR mask_key[i % 4]. The 32-bit size was chosen because it's a common word size, provides sufficient randomness, and avoids overhead of larger keys. The mask prevents DNS rebinding attacks on transparent proxies.

## Q3: What is the exact behavior of WebSocket close codes 1005 vs 1006 vs 1011 and when does each occur?
**A:** 1005 (No Status Received): sent when one side receives a close frame without a status code. 1006 (Abnormal Closure): the connection was closed abnormally without sending or receiving a close frame (e.g., TCP RST, timeout). 1011 (Internal Error): the server encountered an unexpected condition that prevented it from fulfilling the request. These are typically set by the implementation, not user code.

## Q4: How do you implement a WebSocket server that correctly handles the 101 Switching Protocols handshake with custom headers?
**A:** Listen for HTTP upgrade request. Validate: `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Version: 13`. Compute accept: `base64(SHA1(Sec-WebSocket-Key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"))`. Return: `HTTP/1.1 101 Switching Protocols`, `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Accept: <hash>`, plus custom headers. After response, switch to WebSocket frame mode.

## Q5: How do Cross-Site WebSocket Hijacking (CSWSH) attacks work and what defenses are effective?
**A:** CSWSH: a malicious page at evil.com opens a WebSocket to your-server.com. Browsers don't enforce same-origin for WebSocket (no CORS-like preflight). The attacker can read messages if authentication is cookie-based. Defenses: (1) validate Origin header server-side, (2) use token-based auth (not cookies), (3) require a CSRF token in the initial handshake, (4) use WSS to prevent network-level attacks.

## Q6: How do you implement token-based WebSocket authentication that survives reconnection?
**A:** During handshake, the client provides a JWT in a custom header or query parameter: `new WebSocket("wss://server.com?token=jwt")`. Server validates the JWT, extracts user identity, and associates it with the connection. For reconnection, use a short-lived access token with a long-lived refresh token. The client can exchange refresh token for new access token before reconnecting.

## Q7: How do load balancers handle WebSocket connections and what are the pros/cons of ALB, NLB, and HAProxy?
**A:** ALB (AWS): native WebSocket support, sticky sessions via cookie, health checks, but 60s idle timeout (configurable), 1M concurrent max. NLB: lower latency, no HTTP inspection, passes raw TCP, handles millions of connections, but no native WebSocket-aware routing. HAProxy: full WebSocket support, fine-grained control, ACLs, rate limiting, but requires manual configuration. Choose ALB for simplicity, NLB for scale, HAProxy for control.

## Q8: How do you implement WebSocket scaling using a Redis Pub/Sub backplane where messages must be delivered exactly once?
**A:** Each WebSocket server subscribes to Redis channels. When server A needs to broadcast, it publishes to Redis. All servers receive and forward to their local connections. For exactly-once: (1) deduplicate messages on the receiving end using message IDs, (2) use Redis Streams with consumer groups for acknowledgment, (3) handle server crashes with pending message replay. Redis Pub/Sub is at-most-once; use Streams for reliability.

## Q9: What is the optimal exponential backoff strategy for WebSocket reconnection including full jitter?
**A:** Compute delay = min(cap, base * 2^attempt) * random(0.5, 1.5) for full jitter. Example: base=1s, cap=60s, attempt=0 => ~1s, attempt=4 => 16s, attempt=6 => max 60s. Add randomization to prevent thundering herd. Reset on successful connection. Consider adding "immediate reconnect" for first attempt and "lazy reconnect" (longer wait) after N consecutive failures.

## Q10: How do you implement a WebSocket heartbeat that correctly distinguishes between a dead connection and a slow network?
**A:** Send ping frames at fixed interval (e.g., 30s). Expect pong response within a timeout (e.g., 10s). Track RTT from ping-pong. A missed pong could be: dead connection (TCP RST/fin), slow network (>timeout), or overloaded server (can't respond). Distinguish by: (1) monitoring TCP state (if OS reports connection closed, no need to wait), (2) using multiple missed pongs before declaring dead, (3) trying a data frame send and checking for error.

## Q11: WebSocket vs. SSE vs. WebRTC vs. gRPC streaming - what are the precise trade-offs for real-time applications?
**A:** WebSocket: bidirectional, persistent TCP, any payload, universal browser support. SSE: unidirectional server-to-client, HTTP, auto-reconnect, text-only, simpler. WebRTC: peer-to-peer UDP, low latency, audio/video optimized, complex setup (STUN/TURN/SDP). gRPC streaming: bidirectional HTTP/2, protobuf, typed streams, good for service-to-service. Choose: SSE for server updates, WebSocket for interactive, WebRTC for media, gRPC for microservices.

## Q12: How does Socket.IO's multiplexing with namespaces work under the hood compared to raw WebSocket?
**A:** Socket.IO multiplexes multiple logical channels (namespaces) over a single WebSocket connection. It prepends a packet type and namespace identifier to each message (e.g., `2["chat", "message", {...}]` means EngineIO packet type 2, namespace "chat", event "message"). Raw WebSocket would require separate connections per channel or manual routing. Socket.IO's approach reduces connection overhead but adds ~5-10 bytes per message.

## Q13: How do you test WebSocket APIs at scale with automated load testing?
**A:** Use tools: (1) k6 with WebSocket extensions for concurrent virtual users, (2) Artillery with WebSocket support, (3) custom scripts using ws library with asyncio. Test: connection rate (connections/sec), message throughput (msg/sec), concurrent connection capacity, latency under load, reconnection behavior under server stress, and memory leak detection. Monitor server-side metrics during tests.

## Q14: How do you monitor WebSocket connections in production including active connections, message rate, and latency?
**A:** Metrics to track: (1) active connections gauge, (2) connection rate (counter/min), (3) disconnection rate with close codes breakdown, (4) message throughput (in/out), (5) message size distribution, (6) round-trip latency from ping-pong, (7) connection duration distribution, (8) per-route/message-type metrics. Export via Prometheus/Grafana. Alert on: high disconnection rate, latency spikes, connection pool exhaustion.

## Q15: How does WebSocket work in serverless environments (AWS Lambda + API Gateway WebSocket) and what are the scaling characteristics?
**A:** API Gateway WebSocket manages connections. Lambda functions handle `$connect`, `$disconnect`, `$default`, and custom routes. Scaling: API Gateway auto-scales to millions of connections. Lambda scales per request. Limitations: (1) 128KB payload per message, (2) 10-min idle timeout, (3) 30s Lambda timeout per invocation, (4) broadcasting requires DynamoDB for connection tracking, (5) cold start adds latency.

## Q16: How do you send binary data efficiently over WebSocket (ArrayBuffer vs Blob vs Buffer)?
**A:** For binary: (1) Node.js Buffer (server-side) with `socket.send(buffer)`, (2) browser ArrayBuffer with `socket.send(arrayBuffer)`, (3) Blob for file-like data. Set `socket.binaryType = 'arraybuffer'` in browser for consistent type. Binary is more efficient than base64 text (33% overhead reduction). For large binary, use streaming or fragmentation.

## Q17: How does WebSocket compression (permessage-deflate) affect latency and CPU usage?
**A:** Permessage-deflate compresses each message with DEFLATE. Pros: reduces bandwidth by 50-80% for text/JSON. Cons: (1) CPU overhead for compression/decompression per message, (2) increased memory for compression context, (3) added latency (compression time). For high-throughput systems, benchmark compressed vs. uncompressed throughput. For low-bandwidth connections (mobile), compression usually wins. Disable for binary data.

## Q18: How do you deploy WebSocket servers on Kubernetes with proper scaling and session affinity?
**A:** Use: (1) Service with `sessionAffinity: ClientIP` for sticky sessions, (2) Ingress controller with WebSocket support (nginx-ingress with `upgrade` headers), (3) HorizontalPodAutoscaler based on active connections or CPU, (4) readiness probes that check WebSocket handshake, (5) preStop hooks for graceful draining (send close frames, wait for drain). Consider using a dedicated WebSocket proxy like Envoy for advanced routing.

## Q19: What is the WebSocket "message boundary" problem and how does framing solve it?
**A:** TCP is a stream protocol with no message boundaries. WebSocket framing adds message boundaries via: FIN bit (last frame of message), opcode (first frame type), and continuation frames (for fragmented messages). This allows the receiver to reassemble multi-frame messages correctly. Without framing, the application would need delimiters or length-prefixing in the payload.

## Q20: How do WebSocket extensions like `permessage-deflate` negotiate parameters during the handshake?
**A:** Client includes: `Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits=15; server_max_window_bits=15`. Server responds with its accepted parameters: `Sec-WebSocket-Extensions: permessage-deflate; server_no_context_takeover`. Parameters: `client_max_window_bits`/`server_max_window_bits` (compression window size), `client_no_context_takeover`/`server_no_context_takeover` (reset context per message, reduces compression ratio but saves memory).

## Q21: How do you implement a WebSocket client-side reconnection strategy with state restoration?
**A:** On disconnect: (1) save pending messages to a queue, (2) attempt reconnect with exponential backoff, (3) on reconnect: re-authenticate, re-subscribe to channels/rooms, replay queued messages (with dedup IDs), restore UI state. Use a state machine: CONNECTED -> DISCONNECTED -> RECONNECTING -> CONNECTED. Track reconnect attempts to distinguish temporary blips from permanent failures.

## Q22: What are the security implications of not validating the Origin header in WebSocket handshakes?
**A:** Without Origin validation, any website can open a WebSocket connection to your server. Attackers can: (1) read messages if auth is cookie-based (CSWSH), (2) send commands on behalf of users, (3) perform data exfiltration. Always validate Origin against a whitelist. For public APIs, use token-based auth (per-connection tokens) so compromised connections don't affect other sessions.

## Q23: How does WebSocket behave through HTTP proxies that don't support the Upgrade mechanism?
**A:** If a proxy doesn't support WebSocket: (1) it may strip the Upgrade header, causing the server to respond with a non-101 status, (2) it may buffer the response and prevent full-duplex communication, (3) some proxies terminate idle connections aggressively. Solutions: (1) use WSS (TLS encrypts the Upgrade, less likely to be intercepted), (2) use a known WebSocket-friendly proxy, (3) implement long-polling fallback.

## Q24: How do you implement a WebSocket server that handles 100,000 concurrent connections with Node.js?
**A:** Key configurations: (1) increase ulimit -n to 200K+, (2) use `cluster` module for multi-core, (3) set `maxPayload` to prevent memory abuse, (4) use `perMessageDeflate: false` to reduce CPU, (5) send ping frames to detect dead connections, (6) avoid per-connection memory leaks (clean up on close), (7) use `ws` library with `noServer` mode for HTTP server sharing, (8) monitor event loop lag.

## Q25: What is the WebSocket `close` frame format including status code and reason?
**A:** Close frame: opcode 0x8, FIN=1. Payload: optional 2-byte status code (unsigned 16-bit integer, network byte order), optional reason string (UTF-8 encoded, max 123 bytes). Example: `[0x03, 0xE8]` (1000=Normal Closure), `[0x03, 0xE9, 0x53, 0x65, 0x72, 0x76, 0x65, 0x72, 0x20, 0x65, 0x72, 0x72, 0x6F, 0x72]` (1001 + "Server error").

## Q26: How do you implement WebSocket rate limiting per connection using a token bucket algorithm?
**A:** Per connection: maintain a token bucket with capacity (e.g., 100 tokens) and refill rate (e.g., 10 tokens/sec). On each incoming message, consume a token. If no tokens, drop the message or send a 1009 (Message Too Big) close frame. For fairness, implement weighted tokens (large messages consume more tokens). Use a background interval to refill tokens. In clustered environments, distribute rate limit state via Redis.

## Q27: What are WebSocket subprotocol negotiation mechanics and how do you implement custom subprotocols?
**A:** Client sends `Sec-WebSocket-Protocol: mqtt, wamp, my-protocol`. Server picks one: `Sec-WebSocket-Protocol: my-protocol`. The chosen subprotocol defines the message format and semantics. To implement a custom subprotocol: define message types (request, response, event, error), serialization (JSON, MessagePack, CBOR), and rules (e.g., "client must send auth message first"). The subprotocol is purely application-level; the server validates messages per protocol rules.

## Q28: How does WebSocket's TCP congestion control interaction affect real-time performance?
**A:** WebSocket runs over TCP, which has: (1) congestion control (slow start, AIMD), (2) head-of-line blocking (lost packet blocks all subsequent data), (3) retransmission on loss. For real-time apps, this means: message delays during packet loss, throughput reduction during congestion, and increased latency jitter. Mitigate by: (1) keeping messages small, (2) using WebRTC (UDP-based) for latency-critical data, (3) implementing application-level sequencing to handle out-of-order.

## Q29: How do you implement a WebSocket server that supports both text and binary messages with different handling logic?
**A:** Check the frame opcode: text (0x1) -> parse as UTF-8 string, binary (0x2) -> treat as raw bytes. Use a message router: on `message` event, check `typeof data === 'string'` vs. `Buffer.isBuffer(data)` (Node.js) or `event.data instanceof ArrayBuffer` (browser). Route to different handlers. For mixed protocols (e.g., JSON text for control, binary for media), define clear protocol rules.

## Q30: What is the WebSocket "slow consumer" problem and how do you implement backpressure?
**A:** Slow consumer: the server produces data faster than the client can consume, causing server-side buffer growth and memory exhaustion. Solutions: (1) monitor `bufferedAmount` and pause data production when it exceeds a threshold, (2) use `socket.writable` (false if backpressure), (3) implement flow control with application-level ACKs, (4) drop non-critical messages when buffer is full, (5) set a maximum buffer size and disconnect abusive clients.

## Q31: How do you implement WebSocket connection pooling on the client side for multiplexing?
**A:** Instead of one connection per task, maintain a pool of WebSocket connections. Applications: (1) create N connections on startup, (2) assign messages to connections via round-robin or least-loaded, (3) handle per-connection ordering guarantees, (4) retry failed messages on another connection. For HTTP/2 environments, investigate WebSocket-over-HTTP/2 (RFC 8441) which natively multiplexes.

## Q32: What is the difference between `socket.io` and `uWebSockets.js` in terms of performance and features?
**A:** uWebSockets.js: C++ addon, ~8-10x faster than `ws`, supports HTTP/WebSocket in one server, minimal memory (~1KB per connection), no built-in reconnection/rooms. Socket.IO: JavaScript, built on Engine.IO with WebSocket + long-polling fallback, rooms, namespaces, auto-reconnection, acknowledgments, middleware. Choose uWebSockets for raw performance, Socket.IO for developer experience and fallback support.

## Q33: How do you implement WebSocket authentication with short-lived tokens and automatic rotation?
**A:** On connect, the client provides an access token (JWT, valid 15 min). Server validates and stores token expiry. Mid-session, the server sends a "token_expiring" event before expiry. Client requests new token from auth endpoint, sends it via an "auth_update" message. Server validates new token. If token expires without renewal, server disconnects with custom close code. This prevents session hijacking from leaked tokens.

## Q34: How does WebSocket handle the case where the client sends a close frame but the server is mid-write?
**A:** When the server receives a close frame while mid-write: (1) the server should flush any pending writes that are already in the send buffer, (2) then send its own close frame, (3) wait for the TCP FIN. Some implementations choose to immediately close (send TCP RST) to abort pending data. The correct behavior per spec is to send close after completing the current message.

## Q35: What is the WebSocket AutoBahn Test Suite and what edge cases does it test?
**A:** AutoBahn is the de-facto WebSocket compliance test suite. It tests: (1) basic framing (text, binary, fragmentation), (2) control frames (ping, pong, close with various codes/reasons), (3) masking (with valid/invalid keys), (4) opcode handling (valid, reserved, invalid), (5) payload lengths (0, 125, 126, 127 boundaries), (6) continuation frames, (7) UTF-8 validation (valid, invalid byte sequences), (8) compression negotiation.

## Q36: How do you implement WebSocket message ordering guarantees across multiple server instances?
**A:** Use a consistent hash on a message ordering key (e.g., user ID, conversation ID) to route all related messages to the same server instance. Within an instance, use a per-key message queue. For cross-instance ordering, use a distributed queue (Kafka partition per key) that preserves order per partition. WebSocket messages from the same producer on the same connection are ordered by TCP, but across connections ordering requires application-level sequence numbers.

## Q37: How do you implement a WebSocket server that can gracefully handle a rolling restart with zero message loss?
**A:** On SIGTERM: (1) stop accepting new connections, (2) send a close frame with code 1001 (Going Away) to all connections, (3) set a drain timeout (e.g., 30s), (4) process queued outgoing messages, (5) close connections gracefully, (6) persist pending messages to a durable queue, (7) shutdown. New instances start and pick up queued messages. The load balancer detects the draining instance via health check failures.

## Q38: What is the WebSocket attack surface beyond CSWSH and how do you harden it?
**A:** Attack surface: (1) CSWSH (origin check), (2) message injection (validate message format server-side), (3) payload size attacks (set maxPayload), (4) resource exhaustion (rate limit connections per IP), (5) SQL injection via WebSocket messages (parameterize all DB queries), (6) SSRF (validate URIs in messages), (7) side-channel via timing (constant-time comparisons). Defense: treat WebSocket as untrusted input, validate everything.

## Q39: How do you implement WebSocket federation where messages route between different WebSocket clusters?
**A:** WebSocket clusters connect via a message bus (Kafka, RabbitMQ, NATS). Each cluster publishes: (1) connection events (user online/offline), (2) messages addressed to specific users/channels. Other clusters subscribe and route to their local connections. Use a global routing table (user -> cluster mapping) stored in a distributed KV store (Redis, etcd). Messages destined for users on other clusters are routed via the message bus.

## Q40: How do you handle WebSocket connection draining when scaling down a Kubernetes pod?
**A:** Use preStop hook: (1) remove pod from service endpoints (readiness probe fails), (2) send close frame with code 1001 to all connections, (3) set a `terminationGracePeriodSeconds` (e.g., 60s), (4) process pending messages, (5) wait for active requests to complete, (6) shutdown. The load balancer/proxy should detect the draining state and stop routing new connections.

## Q41: How do you implement WebSocket with end-to-end encryption beyond WSS?
**A:** WSS encrypts between client and server (TLS termination). For end-to-end encryption (server can't read messages): (1) client encrypts payload with a shared secret (e.g., ECDH key exchange), (2) sends encrypted binary frame, (3) server routes but can't decrypt, (4) receiving client decrypts. The WebSocket frame itself is opaque to the server. Use libsodium or Web Crypto API for encryption.

## Q42: What is the WebSocket "gradual disconnection" pattern for notifying clients before maintenance?
**A:** Before maintenance: (1) broadcast a "maintenance" event with estimated downtime, (2) wait for acknowledgment or a timeout, (3) send close frames with code 1001 (Going Away), (4) clients display maintenance message and reconnect after expected duration. This is better than abrupt disconnection where clients show "connection lost" errors.

## Q43: How do you implement WebSocket with zero-downtime deployment on AWS ECS/Fargate?
**A:** Use: (1) Application Load Balancer with target group, (2) configure health check on WebSocket endpoint, (3) during deployment: ECS starts new tasks, ALB registers them, starts routing new connections, (4) old tasks receive SIGTERM, drain connections, (5) use connection draining timeout (ALB setting) to match graceful shutdown window. Configure auto-scaling to pre-warm new tasks.

## Q44: How do you implement WebSocket with custom frame-level logging for debugging?
**A:** Log: (1) raw frame metadata (FIN, opcode, mask, length), (2) first N bytes of payload (truncate for privacy), (3) direction (incoming/outgoing), (4) timestamp with microsecond precision, (5) connection ID. Use a ring buffer per connection to avoid memory explosion. For production, sample logging (log 1% of frames). For debugging, enable full logging per session.

## Q45: How does WebSocket's `permessage-deflate` window size affect memory and compression ratio?
**A:** Window size (bits): 8 (256 bytes) to 15 (32KB). Larger window = better compression but more memory. Each connection requires 2x window + overhead per direction (compress + decompress). For 100K connections with window 15: 100K * 2 * 32KB = ~6.4GB just for compression context. Use `server_no_context_takeover` to reset context per message (reduces memory but hurts compression).

## Q46: How do you implement an echo WebSocket server in C using libwebsockets for ultra-low latency?
**A:** Use libwebsockets with: (1) `LWS_CALLBACK_RECEIVE` to get incoming data, (2) `lws_write()` with `LWS_WRITE_TEXT` to echo back, (3) `LWS_CALLBACK_WSI_DESTROY` for cleanup. Configure: threadpool mode, TLS with OpenSSL, epoll for event handling. libwebsockets provides: ~0.5ms per message latency, ~1KB per connection memory, and HTTP/WebSocket multiplexing.

## Q47: How does WebSocket handle the 1000 (Normal) close exchange timing?
**A:** The close handshake: (1) either side sends close frame, (2) the other side sends close frame in response, (3) the initiator waits for the response close, then closes TCP. If the initiator doesn't receive the response close within a timeout, it closes TCP anyway. The side that receives the first close should send its close and then wait to receive TCP FIN before closing.

## Q48: How do you implement WebSocket client-side automatic reconnection in React with state recovery?
**A:** Create a custom hook `useWebSocket(url, options)`: (1) maintains connection state (connecting/connected/disconnected), (2) implements reconnect with backoff, (3) queues messages sent while disconnected, (4) replays queued messages on reconnect, (5) restores subscriptions/topics, (6) exposes `send()`, `onMessage`, `connectionState`, `reconnectAttempt`. Use a ref to track connection instance and avoid stale closures.

## Q49: What are the exact scenarios where a WebSocket connection receives close code 1006 (Abnormal Closure)?
**A:** 1006 occurs when: (1) TCP RST received (server crashed, process killed), (2) TCP FIN received without prior WebSocket close frame, (3) network timeout (heartbeat not received), (4) TLS connection terminated abnormally, (5) proxy/server closed the underlying TCP connection. 1006 is never sent in a close frame; it's generated locally when the connection terminates abnormally.

## Q50: How do you implement WebSocket with message acknowledgment similar to TCP ACKs?
**A:** Each message gets a unique message ID (UUID or incrementing int). The sender expects an ACK message with that ID within a timeout. If not received: retransmit (with deduplication via message ID). Track unACKed messages in a queue. This provides reliable delivery over WebSocket. For ordered delivery, block sending until previous message is ACKed. For unordered, allow parallel unACKed messages with a limit.

## Q51: How does WebSocket work with HTTP/2 (RFC 8441) tunneling and what are the benefits?
**A:** RFC 8441 defines a way to tunnel WebSocket over HTTP/2 streams. The client sends a CONNECT request with `:protocol: websocket`. The server opens a stream and WebSocket frames are encapsulated in HTTP/2 DATA frames. Benefits: (1) multiplex multiple WebSocket connections over one HTTP/2 connection, (2) leverage HTTP/2's flow control, (3) avoid per-connection TCP overhead.

## Q52: How do you implement a WebSocket server that dynamically adjusts ping interval based on connection quality?
**A:** Track ping-pong RTT per connection. If RTT is low (<100ms), use standard ping interval (30s). If RTT is high (>500ms), increase interval (60s) to avoid adding latency. If connection shows packet loss (missing pongs), decrease interval (15s) for faster detection. Adaptive interval balances timely failure detection with network overhead.

## Q53: What is the WebSocket security model for browser vs. non-browser environments?
**A:** Browsers enforce: (1) same-origin policy (no cross-origin WebSocket to `ws://` from HTTPS page), (2) mixed content blocking (no `ws://` from HTTPS page), (3) no custom headers in handshake (only cookies, basic auth). Non-browser clients (Node.js, mobile) have no restrictions: any URL, any headers, any port. This means browser WebSocket is inherently safer against certain attacks.

## Q54: How do you implement a WebSocket server that supports multiple protocols (STOMP, MQTT, custom) on the same port?
**A:** Use path-based routing: `wss://server.com/stomp` routes to STOMP handler, `/mqtt` to MQTT handler. Or use subprotocol negotiation: the client sends `Sec-WebSocket-Protocol: stomp, mqtt, custom`. The server routes based on the chosen subprotocol. Each handler interprets messages per its protocol. Common in IoT and messaging platforms.

## Q55: How do you implement WebSocket with Kubernetes Ingress (nginx-ingress) and what are the known issues?
**A:** nginx-ingress config: `nginx.ingress.kubernetes.io/websocket-services: <service-name>`, `nginx.ingress.kubernetes.io/proxy-read-timeout: 3600`, `nginx.ingress.kubernetes.io/proxy-send-timeout: 3600`. Known issues: (1) default 60s timeout causes disconnections, (2) nginx may buffer WebSocket frames, (3) sticky sessions require custom configuration, (4) nginx can't load balance WebSocket to multiple backends without session affinity.

## Q56: How do you implement WebSocket connection throttling globally across a cluster?
**A:** Use a distributed counter (Redis) to track active connections. On new connection: increment counter. If above limit, reject with 101 response failure or close with 1008 (Policy Violation). On disconnect: decrement. Handle edge cases: (1) atomic increment with TTL (in case the connection isn't properly closed), (2) periodic reconciliation (count actual connections vs. counter), (3) per-IP limits alongside global.

## Q57: What is the WebSocket "message fragmentation" use case for streaming large payloads?
**A:** Fragmentation splits a single logical message into multiple frames. Use cases: (1) streaming a large file without buffering the entire payload, (2) sending data as it becomes available (real-time sensor data), (3) interleaving control frames between fragments (e.g., send a ping during a large message). The first fragment has opcode set, intermediate/continuation have opcode 0x0, last has FIN=1.

## Q58: How do you implement WebSocket with mutual TLS (mTLS) for server-to-server communication?
**A:** Both server and client present certificates. Configure: (1) server: `requestCert: true`, `rejectUnauthorized: true`, `ca: [clientCA]`, (2) client: `cert: clientCert`, `key: clientKey`, `ca: [serverCA]`. The WebSocket server verifies the client certificate during TLS handshake, extracting the client identity from the certificate CN/SAN. This provides strong authentication without tokens.

## Q59: How do you implement a WebSocket server that handles the case where the client never sends a close frame?
**A:** Implement: (1) ping/pong heartbeat (send ping, expect pong within timeout), (2) if no pong after N retries, close with 1001 (Going Away), (3) set a maximum connection lifetime (e.g., 24 hours), (4) on server shutdown, send close frames, (5) detect dead connections via epoll/kqueue (OS signals when connection is reset). Never rely on clients to initiate close.

## Q60: How do you implement WebSocket with Redis Streams for reliable message delivery across server restarts?
**A:** Incoming messages are written to Redis Streams with a consumer group. Workers consume from the stream and forward to WebSocket connections. If a server crashes mid-send, the message stays pending in the stream. On restart, the worker reads pending messages, checks if the target connection is still alive, and re-sends or discards. This ensures at-least-once delivery.

## Q61: How does WebSocket interact with Content Delivery Networks (CDNs) like Cloudflare?
**A:** Cloudflare supports WebSocket with: (1) no additional configuration needed for WSS, (2) auto-negotiation of upgrades, (3) 100-second idle timeout (configurable), (4) no caching (WebSocket is dynamic). Limitations: (1) Cloudflare Workers can't forward WebSocket to arbitrary backends (only to the origin), (2) some Cloudflare features (WAF, transform rules) don't apply to WebSocket traffic.

## Q62: How do you implement WebSocket with differential updates (sending only changes, not full state)?
**A:** Instead of sending full state, send a "diff" (JSON Patch, RFC 6902, or custom diff format). The client applies the diff to its local state. This reduces bandwidth significantly for large state objects. The server must track state versions and ensure the client has the correct base version before applying diffs. Use OT (Operational Transformation) or CRDT for collaborative editing.

## Q63: What is the WebSocket behavior with HTTP redirects (3xx status codes)?
**A:** The WebSocket specification says clients should follow HTTP redirects during the opening handshake. For 301/302/307/308, the client should: (1) close the original connection, (2) open a new WebSocket connection to the redirect target, (3) include the same handshake headers. Most browser implementations follow redirects automatically. Server-side, use redirects for load balancing or protocol upgrades.

## Q64: How do you implement WebSocket "connection coalescing" where multiple browser tabs share one connection?
**A:** Use a SharedWorker (browser): (1) the SharedWorker creates a single WebSocket connection, (2) all tabs post messages to the SharedWorker, (3) the SharedWorker multiplexes messages from/to tabs. This reduces server connections per user from N (tabs) to 1. For ServiceWorker: intercept WebSocket creation and route through a shared connection. Elegant but complex, use SharedWorker for simplicity.

## Q65: How do you implement WebSocket with Kafka integration for real-time event streaming?
**A:** WebSocket server subscribes to Kafka topics. On message from Kafka -> broadcast to WebSocket clients subscribed to that topic. On message from WebSocket client -> publish to Kafka topic. Use consumer groups for horizontal scaling (each server instance is a consumer). Handle: consumer rebalancing (temporary message lag), offset management (commit after client acknowledges), and message serialization (Avro/Protobuf).

## Q66: How do you implement WebSocket with a circuit breaker pattern for external API calls triggered by messages?
**A:** Each external API call (triggered by WebSocket messages) goes through a circuit breaker. States: CLOSED (normal), OPEN (failing, reject immediately), HALF_OPEN (test). If API errors exceed threshold, trip to OPEN, send error response to client, and retry after timeout. On success in HALF_OPEN, return to CLOSED. This protects both the external API from overload and the WebSocket client from waiting on failing calls.

## Q67: How do you implement WebSocket binary protocol with Protocol Buffers or MessagePack for efficiency?
**A:** Define message schemas in Protobuf (`.proto` files) or MessagePack. Client and server share schemas. Each WebSocket message: (1) first byte = message type ID, (2) rest = serialized payload. On receive: (1) read type ID, (2) deserialize with correct schema, (3) route to handler. Benefits: ~10x smaller than JSON, typed, versionable. Use binary frames (opcode 0x2).

## Q68: How do you implement a WebSocket server that respects the TCP_NODELAY setting?
**A:** Enable `TCP_NODELAY` on the TCP socket to disable Nagle's algorithm. Without it, TCP may buffer small writes to combine them into larger packets, adding ~40ms delay. For WebSocket (many small messages), disable it: `socket.setNoDelay(true)` (Node.js), `setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, 1)` (C), `TCP_NODELAY=1` (env var in some servers).

## Q69: How do you implement WebSocket with a backpressure signal using TCP Window manipulation?
**A:** When server is overloaded: (1) stop reading from the TCP socket (pause `socket.resume()` in Node.js), (2) the TCP receive window fills up, (3) the sender's send buffer fills and they experience backpressure. This is a form of "stop-and-wait" flow control. For fine-grained control, use application-level flow control (send/receive tokens) rather than TCP-level manipulation.

## Q70: How do you implement WebSocket with "last will" functionality (notify others when a client disconnects)?
**A:** When a client connects, it registers a "last will" message and targets (e.g., "when I disconnect, notify room X"). On disconnect (either clean or abnormal): (1) trigger the last will, (2) send the predefined message to the target channel. This is similar to MQTT's Last Will and Testament. Use cases: presence detection, "user went offline" notifications, cleanup of user resources.

## Q71: How do you implement WebSocket with STOMP protocol for message queuing semantics?
**A:** STOMP over WebSocket: frames have COMMAND (CONNECT, SUBSCRIBE, SEND, ACK, DISCONNECT) and headers (destination, receipt, content-type). Client sends: `SEND\ndestination:/queue/orders\ncontent-type:application/json\n\n{"orderId":123}\n\0`. Server routes to message brokers. STOMP provides: destination-based routing, message acknowledgments, transactions, and queue semantics on top of WebSocket.

## Q72: How do you implement a WebSocket server with dynamic compression (enable per-message based on content type)?
**A:** Check message content type before compression: (1) text/JSON -> compress with permessage-deflate, (2) binary (already compressed format like JPEG/MP4) -> skip compression, (3) small messages (<100 bytes) -> skip compression (overhead outweighs benefit). Dynamic selection optimizes CPU usage: only compress when it actually reduces size. Check compressed size and send uncompressed if larger.

## Q73: How do you implement WebSocket with QUIC (HTTP/3) using WebTransport as an alternative?
**A:** WebTransport uses HTTP/3 (QUIC/UDP) for bidirectional streams. Unlike WebSocket (single ordered stream), WebTransport has: multiple independent streams (no HOL blocking), unreliable datagrams, 0-RTT connection establishment, native multiplexing. Use WebTransport when: (1) low latency on lossy networks matters, (2) you need multiple streams, (3) you want unordered delivery. API: `new WebTransport(url)`, create bidirectional streams, send datagrams.

## Q74: How do you implement WebSocket server logging with structured JSON and correlation IDs?
**A:** Each connection gets a correlation ID (UUID). All logs include: connection ID, user ID (if authenticated), message type, duration. Log format: `{"ts":"2025-01-15T10:30:00Z","level":"info","conn":"abc123","user":"user_456","event":"message_received","type":"chat","size":1024,"duration_ms":5}`. Use structured logging libraries (pino, winston) with WebSocket transport. Ship to ELK/Datadog for analysis.

## Q75: How do you implement WebSocket with "connection affinity" (message ordering per user across reconnections)?
**A:** Map user ID to a consistent hash slot. Route all WebSocket connections from the same user to the same server instance (using sticky sessions or consistent hash load balancer). This ensures messages for a user are processed in order on one server. On server failure: (1) connections redirect to a new server, (2) the new server catches up from a shared event log (Kafka, database), (3) messages are replayed in order.

## Q76: How do you implement a WebSocket server that rejects connections based on geographic location?
**A:** Use GeoIP lookup on the client's IP during the handshake. If the location is outside allowed regions: (1) respond with HTTP 403 Forbidden, (2) include a reason in the body. For compliance (GDPR, export controls), reject connections from restricted regions. For performance, route to the nearest regional server. GeoIP databases (MaxMind) are updated regularly.

## Q77: How do you implement WebSocket and co-exist with REST API on the same HTTP server?
**A:** Use path-based routing: (1) `/api/*` -> REST handler, (2) `/ws/*` -> WebSocket upgrade handler. In Node.js (http + ws): create an HTTP server, detect Upgrade header, and route WebSocket connections to the ws library. For non-upgrade requests, route to Express/Koa. This shares port 80/443 between REST and WebSocket, simplifying deployment.

## Q78: How do you implement WebSocket with a "presence" system (who's online)?
**A:** Maintain a presence store (Redis Set per channel/room). On connect: add user to channel's set, broadcast "user_online" event. On disconnect: remove from set, broadcast "user_offline". On reconnect: detect existing entry, don't re-broadcast. Use heartbeats to detect zombie connections (user appears online but client is dead). Publish presence changes to subscribers.

## Q79: How do you implement WebSocket message validation with JSON Schema before processing?
**A:** Define JSON Schema for each message type. On receive: parse JSON, validate against schema using a validator (ajv, zod). If invalid: (1) send error message back with validation errors, (2) log the violation, (3) optionally disconnect if violations exceed threshold. This prevents malformed data from crashing downstream handlers and protects against injection.

## Q80: How do you implement WebSocket with "graceful degradation" when WSS certificate expires?
**A:** Monitor certificate expiry. Before expiry (e.g., 30 days): (1) alert operations team, (2) if expiry is imminent and renewal fails, fall back to WS (insecure) with a warning to clients, (3) clients decide whether to accept WS or disconnect. In practice: automate certificate renewal (Let's Encrypt, cert-manager) to avoid expiry. Fallback is only for emergency.

## Q81: How do you implement WebSocket with custom DNS-based load balancing (SRV records)?
**A:** Use DNS SRV records to advertise WebSocket servers: `_websocket._tcp.example.com. 3600 IN SRV 10 20 80 server1.example.com.` Priority/weight for selection. Client library: resolve SRV record, select server (lowest priority, weighted random), connect. Benefits: simpler than load balancer, location-aware routing, no single point of failure. Used in XMPP and Matrix protocols.

## Q82: How do you implement WebSocket "slow client" detection and disconnection?
**A:** Monitor: (1) `bufferedAmount` growth rate, (2) time between receiving ACKs (if using ACK protocol), (3) time to consume sent data. Thresholds: if bufferedAmount exceeds 1MB, if no ACKs received for 30s, if client consumes < 1KB/s. On detection: (1) send warning event, (2) reduce message rate, (3) if no improvement, disconnect with 1009 (Message Too Big) or custom code.

## Q83: How do you implement WebSocket with dynamic rate limiting based on server load?
**A:** When server CPU/memory exceeds thresholds: (1) reduce per-connection rate limits (less throughput per client), (2) increase ping interval to reduce overhead, (3) disable compression to save CPU, (4) reject new connections, (5) disconnect lowest-priority connections. When load normalizes, restore settings. This provides graceful degradation under stress.

## Q84: How do you implement WebSocket message encryption at the application layer (end-to-end)?
**A:** Use Web Crypto API (browser) and crypto (Node.js) for AES-256-GCM encryption. Client encrypts payload before sending: (1) generate random IV, (2) encrypt with shared key, (3) send `{iv_base64, ciphertext_base64}`. Receiver decrypts. Key exchange: ECDH (Elliptic Curve Diffie-Hellman) during initial handshake. This provides end-to-end security even if the WebSocket server is compromised.

## Q85: How do you implement WebSocket with "message deduplication" at the server level?
**A:** Use a message ID (UUID, server-assigned sequence). Track recently processed message IDs in a sliding window cache (Redis Set with TTL, e.g., 5 min). On receiving a message, check if ID exists in cache. If yes, ignore (duplicate). If no, process and add to cache. This handles retransmissions from clients that send messages multiple times due to connection issues.

## Q86: How do you implement WebSocket with a "drain" event handling for backpressure in Node.js?
**A:** When `socket.send()` returns `false` (internal buffer is full), wait for the `drain` event before sending more. Pause the readable stream (if reading from a source) and resume on `drain`. Track pending sends with a counter; don't exceed a watermark (e.g., 64KB pending). Example: `if (!socket.send(data)) { socket.once('drain', sendNext); } else { sendNext(); }`

## Q87: How do you implement WebSocket with shared state across cluster nodes without Redis?
**A:** Alternatives to Redis: (1) PostgreSQL LISTEN/NOTIFY for pub/sub, (2) NATS for lightweight messaging, (3) gRPC streams between server instances, (4) Hazelcast/Ignite for distributed data grids, (5) etcd for coordination. Redis is most common because of its pub/sub speed, but PostgreSQL is a good choice if you're already using it (no additional infrastructure).

## Q88: How do you implement WebSocket with IPv6 and handle dual-stack scenarios?
**A:** Listen on both IPv4 and IPv6 (Node.js: `server.listen(8080, '::')` binds both). For clients: (1) resolve DNS to both A and AAAA records, (2) prefer IPv6 if available, (3) handle IPv6 addresses in connection tracking. Be aware: IPv6 addresses contain colons, so standardize format for storage. Load balancers must support IPv6 termination.

## Q89: How do you implement WebSocket with "message batching" for high-throughput scenarios?
**A:** Buffer outgoing messages per connection for a short interval (e.g., 10ms or 100 messages). Flush as a single batch (newline-delimited JSON, array of messages, or custom framing). Reduces: (1) TCP packet count, (2) system call overhead, (3) TLS record overhead. Increases: (1) latency (up to batch interval), (2) throughput (2-10x). Tune batch interval for latency/throughput trade-off.

## Q90: How do you implement a WebSocket server that can switch between text and binary modes dynamically?
**A:** The server can send text frames (opcode 0x1) or binary frames (opcode 0x2) at any time. The client checks `event.data instanceof ArrayBuffer` or `typeof event.data === 'string'` to determine type. Use text for structured data (JSON), binary for blobs, images, or serialized objects. The message type can change per-message. This is inherent in the protocol, no special configuration needed.

## Q91: How do you implement WebSocket with TLS session resumption for faster reconnection?
**A:** Configure TLS session cache on the server: (1) enable session IDs or session tickets, (2) set session timeout (e.g., 300s), (3) configure session cache size. On reconnection, the client presents the cached session, reducing TLS handshake from 2-RTT to 1-RTT (abbreviated handshake). For 0-RTT, use TLS 1.3 early data (but beware of replay attacks).

## Q92: How do you implement WebSocket with "connection metadata" stored at the server?
**A:** Each connection has associated metadata: user ID, session ID, subscribed channels, client info (user agent, IP, protocol version), connection time, last activity. Store in a Map/object keyed by connection ID. Use WeakRef for automatic cleanup (if available). In clustered environments, store metadata in Redis Hash per connection ID. Metadata enables targeted message routing and connection management.

## Q93: How do you implement WebSocket with a "thundering herd" prevention strategy for reconnections?
**A:** After a server restart, thousands of clients reconnect simultaneously, overwhelming the server. Prevention: (1) random delay before reconnection (0-5s jitter), (2) server-side connection queue (accept but delay processing), (3) progressive registration (stagger connection setup), (4) use a "connection readiness" signal (clients wait for server-ready event before reconnecting), (5) rate-limit new connections server-side.

## Q94: How do you implement WebSocket message routing based on pub/sub topics natively (without Socket.IO)?
**A:** Each connection subscribes to topics via a "subscribe" message. Maintain a Map<topic, Set<connection>>. On publish: look up the topic's connections and send to each. Use a trie for wildcard topics (chat.*, chat.room.123). For broadcast: send to all connections. This is essentially implementing a minimal message broker on top of WebSocket. Use Redis for cross-server topic routing.

## Q95: How do you implement WebSocket with "cold standby" failover?
**A:** Primary WebSocket server handles all connections. A standby server is ready but idle. Use a health-check/voting mechanism (etcd, Consul, keepalived). On primary failure: (1) standby takes over the IP/LB, (2) all connections are lost (need client reconnection), (3) standby loads the last known state from persistent storage, (4) standby starts accepting connections. Clients reconnect and restore state.

## Q96: How do you implement WebSocket with HTTP/2 Server-Sent Events (SSE) hybrid for different message priorities?
**A:** Use WebSocket for high-priority, bidirectional messages (user commands, real-time updates). Use SSE for low-priority, unidirectional pushes (background notifications, non-critical updates). SSE benefits: (1) automatic reconnection built-in, (2) HTTP/2 multiplexing, (3) works through all proxies. This hybrid approach optimizes resource usage: WebSocket for interactive, SSE for broadcast.

## Q97: How do you implement WebSocket with message size negotiation for adaptive streaming?
**A:** Clients report their bandwidth/latency via a "capabilities" message. Server adapts: (1) high bandwidth -> larger, fewer messages (batched), (2) low bandwidth -> smaller, compressed messages, (3) high latency -> smaller messages to avoid head-of-line blocking. Dynamically update message size based on observed network conditions. This is similar to adaptive bitrate streaming for WebSocket.

## Q98: How do you implement a WebSocket server that uses Epoll/Kqueue/IOCP for maximum performance?
**A:** Use an event loop library (libuv for Node.js, asyncio for Python, epoll for C/C++). Configuration: (1) edge-triggered epoll for accurate event notification, (2) large event buffer (e.g., 1024 events per poll), (3) accept connections in batch, (4) use non-blocking I/O everywhere, (5) use a thread pool for blocking operations. uWebSockets.js and libwebsockets use these primitives for high performance.

## Q99: How do you implement WebSocket with message-level compression (not permessage-deflate)?
**A:** Instead of per-frame compression, compress individual message payloads: (1) for large JSON payloads, compress with gzip/brotli before sending, (2) add a flag to indicate compression (e.g., first byte = 0x00 uncompressed, 0x01 gzip, 0x02 brotli), (3) client decompresses based on flag. Benefits: you control which messages compress (avoid overhead on small messages), works with binary data. Downside: no standard negotiation.

## Q100: How do you implement a WebSocket "health check" endpoint that validates both HTTP and WebSocket functionality?
**A:** Health check endpoint `/health` returns: (1) HTTP 200 with server status, (2) optionally, a WebSocket echo test: the client connects, sends "ping", expects "pong" within timeout. For load balancers: (1) TCP health check (port is listening), (2) HTTP health check (validate handshake response), (3) custom health check agent that validates WebSocket message round-trip. The third is most accurate but heavyweight.
