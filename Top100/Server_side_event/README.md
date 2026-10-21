# Server-Sent Events Interview Questions and Answers

## Q1: What are Server-Sent Events (SSE)?
**A:** Server-Sent Events (SSE) is a push technology that enables servers to send real-time updates to clients over a single, long-lived HTTP connection. Unlike WebSockets, SSE is unidirectional (server to client) and uses standard HTTP, making it simpler to implement for scenarios like notifications, feeds, and live updates.

## Q2: How does SSE differ from WebSockets?
**A:** SSE is unidirectional (server → client only), uses standard HTTP/HTTPS, and is simpler to implement. WebSockets are bidirectional, require a protocol upgrade (ws://wss://), and support full-duplex communication. SSE is better for one-way data pushing; WebSockets are better for interactive applications like chat.

## Q3: What is the EventSource API?
**A:** EventSource is a browser API that creates a persistent connection to a server for receiving SSE. It automatically handles reconnection, tracks the last received event ID, and fires events as data arrives. Usage: new EventSource('/events'). It is the standard client interface for SSE.

## Q4: What is the MIME type for SSE?
**A:** The MIME type for SSE is text/event-stream. The server must set the Content-Type header to text/event-stream for the client's EventSource to recognize and process the response correctly.

## Q5: What is the SSE event stream format?
**A:** The SSE format uses UTF-8 text with fields separated by newlines. Each event consists of field:value pairs. Key fields: data: (payload), event: (event type), id: (last event ID), retry: (reconnection time in ms). Events are separated by double newlines (\n\n).

## Q6: What is the purpose of the retry field in SSE?
**A:** The retry field tells the browser how long (in milliseconds) to wait before attempting to reconnect after a connection loss. For example, retry: 3000 means wait 3 seconds. If not specified, browsers default to 2-3 seconds.

## Q7: What is the purpose of the id field in SSE?
**A:** The id field assigns a unique identifier to each event. If the connection drops, the browser sends the Last-Event-ID HTTP header with the last received id on reconnection. The server can use this to resume from where it left off, preventing duplicate or missed events.

## Q8: What is the Last-Event-ID header?
**A:** The Last-Event-ID is an HTTP header sent by the browser when reconnecting after an SSE connection loss. Its value is the last event: id received. Servers use this to replay missed events. It ensures at-least-once delivery semantics.

## Q9: Can SSE send binary data?
**A:** No, SSE natively supports only UTF-8 text. Binary data must be encoded (e.g., Base64) before sending. This increases payload size. For binary streaming, WebSockets or raw HTTP chunks are more appropriate. However, SSE can send ArrayBuffer by encoding as Base64 data URLs.

## Q10: How many concurrent SSE connections can a browser handle?
**A:** Most browsers limit concurrent connections per domain to 6-8 for HTTP/1.1. HTTP/2 multiplexing allows many more (default 100+). SSE connections count toward this limit, so opening multiple SSE streams from the same domain may exhaust the connection pool.

## Q11: What happens when an SSE connection drops?
**A:** The browser's EventSource automatically detects the drop (via TCP timeout or HTTP error) and attempts reconnection after the retry delay. It sends Last-Event-ID to allow the server to resume. The onerror event fires on the EventSource object.

## Q12: How do you close an SSE connection from the client?
**A:** Call eventSource.close() on the EventSource instance. This terminates the connection and prevents automatic reconnection. The server may detect the close via TCP connection termination or a timeout on its side.

## Q13: How do you close an SSE connection from the server?
**A:** The server can close the connection by: (1) ending the response stream, (2) sending a terminal event or custom close event, (3) letting the connection idle until timeout. The server should clean up resources when the connection closes.

## Q14: What is the difference between SSE and long polling?
**A:** SSE maintains a persistent connection for continuous streaming; long polling makes repeated HTTP requests, each of which the server holds open until data is available. SSE has lower latency (no repeated handshake) and less overhead. Long polling works in older browsers without EventSource.

## Q15: How do you handle CORS with SSE?
**A:** SSE is subject to CORS. The server must include Access-Control-Allow-Origin header. For credentials (cookies), use Access-Control-Allow-Credentials: true and the withCredentials option in EventSource: new EventSource(url, { withCredentials: true }).

## Q16: What are named events in SSE?
**A:** Named events use the event: field to specify a type. The client listens with eventSource.addEventListener('eventname', callback) instead of the generic onmessage. This allows multiplexing different event types (e.g., "notification", "price_update", "status_change") over a single connection.

## Q17: How does SSE handle event multiplexing?
**A:** SSE multiplexes multiple event types over one connection using named events (event: field). The client registers separate listeners per event type. This avoids opening multiple connections. For example, a single stream can send "chat_message", "typing_indicator", and "user_online" events.

## Q18: What happens if the server sends an invalid SSE format?
**A:** The browser's EventSource parser ignores lines that do not match the field:value format (without colon). Lines starting with a colon (:) are treated as comments and ignored. This makes SSE resilient to formatting errors. The EventSource.onerror event fires on connection issues.

## Q19: How do you implement SSE in Node.js?
**A:** In Node.js (Express): set headers (Content-Type: text/event-stream, Cache-Control: no-cache, Connection: keep-alive), write data with res.write(), and handle req.on('close') for cleanup. Libraries like `express-sse` or raw http.createServer with streaming response work.

## Q20: How do you implement SSE in Python (FastAPI/Flask)?
**A:** FastAPI: use StreamingResponse with a generator. Flask: use Response with stream_template. Django: use StreamingHttpResponse. Set Content-Type: text/event-stream. The generator yields formatted SSE strings (f"data: {json.dumps(data)}\n\n") and runs in a loop until client disconnects.

## Q21: How do you implement SSE in Go?
**A:** In Go, set response headers (Content-Type: text/event-stream), use http.Flusher to flush after each write, and use a loop with fmt.Fprintf(w, "data: %s\n\n", message). Detect client disconnect via r.Context().Done(). The http.CloseNotifier interface is deprecated.

## Q22: How does SSE work with HTTP/2?
**A:** HTTP/2's multiplexed streams eliminate the browser's 6-8 connection limit per domain. SSE over HTTP/2 allows many concurrent streams without exhausting connections. However, HTTP/2's server push is different from SSE — SSE remains the application-level mechanism.

## Q23: What is the difference between SSE and HTTP/2 Server Push?
**A:** SSE is an application-level API for the server to push events to the client over a persistent connection. HTTP/2 Server Push is a transport-level mechanism that proactively sends resources (CSS, JS, images) before the client requests them. They serve different purposes.

## Q24: What are the limitations of SSE?
**A:** Limitations: (1) unidirectional — client cannot send data over the same connection, (2) text-only (binary must be encoded), (3) browser connection limits on HTTP/1.1, (4) no native support in older browsers (IE), (5) proxies may buffer or drop long-lived connections, (6) no built-in compression for headers.

## Q25: Which browsers support SSE?
**A:** SSE is supported in all modern browsers: Chrome, Firefox, Safari, Edge, Opera. Internet Explorer does not support EventSource. Mobile browsers (iOS Safari, Chrome for Android) also support it. Polyfills are available for IE using XHR streaming.

## Q26: How do you implement SSE for IE compatibility?
**A:** Internet Explorer lacks EventSource. Solutions: (1) use a polyfill library that emulates EventSource via XHR streaming or iframe, (2) fall back to long polling for IE, (3) use a library like Yaffle (EventSource polyfill) that works across browsers including IE.

## Q27: What is the eventSource.readyState?
**A:** readyState indicates connection status: 0 (CONNECTING) — attempting to connect, 1 (OPEN) — connected and receiving events, 2 (CLOSED) — connection closed. It changes automatically on connection events. Use eventSource.onopen, onmessage, onerror for state change detection.

## Q28: How do you handle SSE authentication?
**A:** SSE authentication methods: (1) cookies — EventSource automatically includes cookies if withCredentials is set, (2) URL query parameters — token appended to the SSE endpoint URL (less secure), (3) custom headers — EventSource does not support custom headers directly; use fetch-based SSE or a wrapper.

## Q29: Why can't EventSource send custom headers?
**A:** The browser's EventSource API does not support custom headers — it only allows URL and withCredentials. This is a security restriction. Workarounds: use the fetch API with ReadableStream for SSE with custom headers, or pass tokens via URL query parameters or cookies.

## Q30: How do you use fetch() for SSE with custom headers?
**A:** Use fetch() with custom headers to get a ReadableStream, then read the stream and parse SSE manually. This requires manual reconnection logic but allows authentication headers. Libraries like `@microsoft/fetch-event-source` wrap this pattern with reconnection support.

## Q31: How do you handle SSE reconnection with backoff?
**A:** Custom EventSource implementations can implement exponential backoff for reconnection: start with short delay (1s), multiply by 2 after each failure (up to max 30s), add jitter. Override the retry field from the server or manage timing manually in a custom wrapper.

## Q32: What is the comment line in SSE?
**A:** Lines starting with a colon (:) are SSE comments. They are ignored by the parser but can be used to keep the connection alive (heartbeat). Example: : heartbeat\n\n. Sending a comment every 30-60 seconds prevents proxies and load balancers from timing out the connection.

## Q33: How do you keep an SSE connection alive?
**A:** Use a heartbeat mechanism: the server sends a comment (: heartbeat\n\n) or a keepalive event every 30-60 seconds. This prevents proxies, load balancers, and NAT gateways from closing what appears to be an idle TCP connection.

## Q34: How do SSE and WebSockets compare in terms of overhead?
**A:** SSE has lower overhead per connection because it uses standard HTTP without the WebSocket upgrade handshake. SSE messages are plain text with minimal framing. WebSockets have a binary framing protocol but are more efficient for high-frequency bidirectional traffic.

## Q35: When should you choose SSE over WebSockets?
**A:** Choose SSE when: (1) updates are unidirectional (server to client), (2) you want simplicity with standard HTTP, (3) you need automatic reconnection, (4) you're behind proxies/firewalls that allow HTTP but block WebSockets, (5) you want to use existing HTTP infrastructure.

## Q36: When should you choose WebSockets over SSE?
**A:** Choose WebSockets when: (1) you need bidirectional communication, (2) you need to send binary data efficiently, (3) you need very low latency for gaming or real-time collaboration, (4) you need custom protocols or sub-protocols, (5) you have many concurrent connections from one client.

## Q37: Can SSE and WebSockets be used together?
**A:** Yes, they are complementary. SSE can handle server-to-client updates (notifications, live scores) while WebSockets handle bidirectional features (chat, collaborative editing). This hybrid approach uses each technology for its strengths.

## Q38: How do you test SSE endpoints?
**A:** Testing methods: (1) curl — `curl -N http://localhost/events` streams SSE data, (2) browser — visit the SSE URL and observe the stream, (3) automated tests — use libraries like supertest (Node.js) or httpx with streaming (Python), (4) dedicated tools like Postman with SSE support.

## Q39: How do you debug SSE connections in the browser?
**A:** Browser DevTools: Network tab shows SSE connections as "eventsource" or "text/event-stream" type. Click to view event data, response headers, and timing. Console: use eventSource.onmessage, onerror to log events. Chrome DevTools shows SSE frames in the Response tab.

## Q40: What happens to SSE when the page is in background?
**A:** Browsers may throttle or pause SSE connections for background tabs to save resources (CPU, network). Chrome deprioritizes but typically keeps the connection alive. For critical updates, use the Page Visibility API or Web Workers to maintain responsiveness.

## Q41: How do you use SSE in a Web Worker?
**A:** SSE can be initiated in a Web Worker (DedicatedWorker or SharedWorker) to offload connection management from the main thread. The worker opens the EventSource, processes events, and posts messages back to the main thread. This prevents UI blocking.

## Q42: How does SSE work with service workers?
**A:** Service workers can intercept SSE connections but cannot directly use EventSource (not available in SW scope). Use fetch() within a service worker to proxy SSE. Service workers can cache SSE responses for offline support or transform event data.

## Q43: How do you handle high-frequency events with SSE?
**A:** Strategies: (1) batch multiple updates into a single event, (2) throttle events on the server side, (3) use a buffering strategy — collect events over a short interval (100ms) and send combined, (4) use compression (gzip) for large payloads, (5) filter events on the server to avoid sending unnecessary data.

## Q44: How does compression work with SSE?
**A:** SSE benefits from HTTP compression (gzip, brotli) since the server writes a streaming response. The Content-Encoding header indicates compression. Each chunk is compressed before sending. This is transparent to the EventSource API but significantly reduces bandwidth.

## Q45: What is the SSE data format for JSON?
**A:** JSON is sent by stringifying the object and using the data field. For multi-line JSON, use multiple data: lines:
```
event: update
data: {"name": "John",
data: "age": 30}
\n\n
```
The browser concatenates consecutive data: lines with newlines.

## Q46: How do you concatenate multiple data lines in SSE?
**A:** Multiple consecutive data: lines are concatenated by the browser with a newline character between each line. The EventSource strips the "data: " prefix and joins the lines. This is useful for sending large JSON payloads split across lines.

## Q47: What is the maximum size of an SSE message?
**A:** SSE has no protocol-level message size limit. Practically, browser limits apply (e.g., Chrome has a ~256KB limit per HTTP response chunk). For large payloads, consider splitting data across multiple events or using compression.

## Q48: How do you implement SSE with a message queue (e.g., Redis Pub/Sub, RabbitMQ)?
**A:** Architecture: (1) server subscribes to a message queue (Redis Pub/Sub, RabbitMQ, Kafka), (2) receives messages from the queue, (3) forwards them to connected SSE clients. Each client connection corresponds to a subscriber. Use unique channels per user for personalized events.

## Q49: How do you handle SSE in a serverless environment (AWS Lambda)?
**A:** SSE in serverless is challenging because Lambda functions have short timeouts (15 min max) and cannot maintain persistent connections with API Gateway HTTP API directly. Solutions: (1) use Lambda with API Gateway WebSocket API instead, (2) use a dedicated service like AWS IoT Core for MQTT, (3) use CloudFront with origin-facing persistent connections.

## Q50: How do you scale SSE to thousands of concurrent connections?
**A:** Scaling strategies: (1) use a dedicated server or process per CPU core (cluster/fork), (2) use an event-driven architecture (Node.js, Python asyncio) for non-blocking I/O, (3) use Redis Pub/Sub for inter-process event broadcasting, (4) use a load balancer with sticky sessions, (5) use HTTP/2 multiplexing.

## Q51: What is the backpressure problem in SSE?
**A:** Backpressure occurs when the server produces events faster than the client can consume them. This fills TCP send buffers, causing memory growth. Solutions: (1) implement flow control — monitor the socket buffer and slow down production, (2) use stream backpressure APIs (Node.js backpressure, Go's write deadline).

## Q52: How do you detect a disconnected SSE client on the server?
**A:** Methods: (1) listen for the connection close event (req.on('close') in Express, request.Context().Done() in Go), (2) check if the socket is writable before sending, (3) send periodic heartbeats and detect write errors, (4) use a timeout to clean up stale connections.

## Q53: How do you implement SSE with sticky sessions?
**A:** Sticky sessions (session affinity) ensure a client always connects to the same server. Configure the load balancer to route based on a cookie or source IP. This maintains SSE connection continuity. For stateless failover, use a shared message bus (Redis) to restore state on any server.

## Q54: How do you implement SSE without sticky sessions?
**A:** Without sticky sessions, a shared pub/sub layer (Redis, Kafka) broadcasts events to all servers, which forward to their connected clients. This allows any server to handle any client. On reconnection, the client may land on a different server but still receives all events.

## Q55: How do you handle SSE with HTTP proxies?
**A:** HTTP proxies may buffer responses, breaking SSE streaming. Mitigations: (1) set Cache-Control: no-cache, (2) set X-Accel-Buffering: no (for nginx), (3) use chunked transfer encoding, (4) flush the response buffer after each event, (5) use HTTPS to prevent proxy buffering.

## Q56: What is X-Accel-Buffering and why is it important for SSE?
**A:** X-Accel-Buffering: no is an nginx directive that disables proxy buffering for SSE endpoints. Without it, nginx may buffer entire responses before forwarding, breaking real-time delivery. It tells nginx to stream data immediately to the client.

## Q57: How do you configure nginx for SSE?
**A:** nginx SSE configuration:
```
proxy_buffering off;
proxy_cache off;
chunked_transfer_encoding on;
proxy_http_version 1.1;
proxy_set_header Connection '';
```
These settings prevent buffering, enable streaming, and maintain the persistent connection needed for SSE.

## Q58: How do you configure Apache for SSE?
**A:** Apache SSE configuration: disable mod_deflate (buffering) or configure it for streaming, enable mod_proxy with ProxyPass, set ProxyPass force-proxy-request-1.1 on, and disable output buffering with `SetEnv no-gzip` for the SSE endpoint.

## Q59: What is the security model of SSE?
**A:** SSE is subject to the Same-Origin Policy. Cross-origin requests require CORS headers. The connection is HTTP(S) based, so standard web security applies (CSRF protection, authentication). Data must be encrypted via HTTPS for confidentiality.

## Q60: How do you prevent CSRF attacks on SSE endpoints?
**A:** SSE does not support custom headers (which are typical CSRF tokens), but: (1) use same-site cookies (SameSite=Strict/Lax), (2) use query parameter tokens that are validated server-side, (3) use Origin/Referer header validation, (4) use POST-based SSE via fetch.

## Q61: How do you implement SSE with authentication tokens?
**A:** Since EventSource does not support custom headers: (1) use httpOnly cookies with SameSite, (2) append the token as a query parameter (less secure but works), (3) use a short-lived token in the URL that redirects to the SSE endpoint after validation, (4) use fetch-based SSE with Authorization header.

## Q62: How do you implement SSE in Django?
**A:** Django supports SSE via StreamingHttpResponse. Use a view that returns StreamingHttpResponse with a generator. The generator yields SSE-formatted strings and runs a loop checking for new data. Use Django channels for async SSE or a library like django-eventstream.

## Q63: How do you implement SSE in Spring Boot?
**A:** Spring Boot supports SSE via: SseEmitter class — create and return from a controller endpoint, call emitter.send() with event data, handle completion/timeout callbacks. Use @Async for non-blocking. WebFlux provides Flux<ServerSentEvent> for reactive SSE.

## Q64: How do you implement SSE in ASP.NET Core?
**A:** ASP.NET Core: return a response with Content-Type: text/event-stream, use await Response.WriteAsync() for each event, call Response.Body.FlushAsync(). Use HttpContext.RequestAborted to detect disconnection. SignalR is the preferred alternative for complex real-time scenarios.

## Q65: How do you implement SSE in Ruby on Rails?
**A:** Rails SSE: use ActionController::Live module, set response.headers['Content-Type'] = 'text/event-stream', use response.stream.write() in a loop, handle client disconnect. The live streaming module requires a threaded server (Puma with threads).

## Q66: How do you implement SSE in PHP?
**A:** PHP SSE: set headers (Content-Type: text/event-stream, Cache-Control: no-cache), disable output buffering (ob_flush, flush), use a loop with sleep() to check for new data. PHP is not ideal for SSE due to per-request process overhead — consider using ReactPHP or Swoole.

## Q67: What is the difference between SSE and Server-Sent Events over HTTP/2?
**A:** SSE semantics are identical over HTTP/1.1 and HTTP/2. HTTP/2 provides multiplexing (multiple SSE streams over one connection), stream prioritization, and more efficient framing. The EventSource API behavior is unchanged regardless of HTTP version.

## Q68: What is the role of EventSource.onopen?
**A:** EventSource.onopen fires when the connection is successfully established. It indicates the server accepted the connection and the client is ready to receive events. Use it for logging, updating connection status UI, or resetting reconnection state.

## Q69: How do you handle SSE errors gracefully?
**A:** Error handling: (1) implement onerror to detect failures, (2) check readyState to determine connection status, (3) implement exponential backoff for reconnection, (4) show a "disconnected" UI indicator, (5) buffer events on the client during disconnection for replay, (6) fall back to polling if SSE repeatedly fails.

## Q70: What are SSE polyfills and how do they work?
**A:** SSE polyfills provide EventSource-like API for browsers that lack native support (IE). They work by: (1) using XHR with streaming (responseText parsing), (2) using hidden iframe with chunked encoding, (3) falling back to long polling. Libraries: Yaffle, EventSource polyfill.

## Q71: How do you implement SSE with React?
**A:** React SSE: useEffect to create EventSource on mount, set up event listeners, update state with useState/useReducer, return cleanup function that calls eventSource.close(). Use useRef for the EventSource instance to avoid recreating on re-renders.

## Q72: How do you implement SSE with Vue.js?
**A:** Vue.js SSE: create the EventSource in mounted() or onMounted (Composition API), set up listeners, update reactive data, destroy in beforeUnmount. For reactive reconnection, use a watcher on connection status. Libraries like vue-sse provide declarative SSE components.

## Q73: How do you implement SSE with Angular?
**A:** Angular SSE: use the @angular/core EventSource wrapper or native EventSource inside a service, manage as an Observable, subscribe/unsubscribe in components. Use the async pipe for automatic subscription management. Use ngOnDestroy for cleanup.

## Q74: What is the EventSource readyState polyfill behavior?
**A:** Polyfills mimic the readyState property: 0 (CONNECTING), 1 (OPEN), 2 (CLOSED). They also implement the same event interface (onopen, onmessage, onerror) and the close() method. Behavior may have slight differences (e.g., reconnection granularity).

## Q75: How do you simulate SSE events for testing?
**A:** Testing simulation: (1) write a mock server script that sends SSE at intervals, (2) use test libraries that create EventSource stubs, (3) use curl -N for manual testing, (4) create a Node.js script with EventSource mock (or use the real EventSource in a test browser).

## Q76: How do you load test SSE connections?
**A:** Load testing tools and approaches: (1) custom scripts with socket connections handling SSE format, (2) tools like k6 (with WebSocket, not SSE natively — need custom script), (3) artillery with SSE plugin, (4) Locust (Python) with custom SSE client, (5) wrk or bombardier for connection-level testing.

## Q77: How does SSE work behind a CDN?
**A:** Most CDNs (Cloudflare, Fastly, Akamai) support SSE but require configuration: (1) disable caching for the SSE endpoint, (2) disable response buffering, (3) enable chunked transfer encoding, (4) configure appropriate timeouts. Cloudflare requires "SSE" or "streaming" enabled.

## Q78: How does Cloudflare handle SSE?
**A:** Cloudflare supports SSE but: (1) disables buffering automatically for text/event-stream, (2) has a default 100-second timeout for non-HTTP/2 connections, (3) HTTP/2 connections can be longer-lived, (4) requires Argo Smart Routing or other features to be compatible. Use HTTP/2 for longer sessions.

## Q79: How do you implement SSE with PostgreSQL LISTEN/NOTIFY?
**A:** PostgreSQL's LISTEN/NOTIFY enables real-time notifications. The server subscribes to a PostgreSQL channel using LISTEN, receives notifications via NOTIFY from triggers or application code, and forwards them to SSE clients. Use pg_notify from PostgreSQL triggers.

## Q80: How do you ensure ordered event delivery with SSE?
**A:** SSE guarantees ordering per connection because it uses a single TCP stream — events arrive in the order they are sent. For guaranteed at-least-once delivery, use event IDs. For exactly-once semantics, deduplicate on the client using event IDs.

## Q81: What is event ID deduplication in SSE?
**A:** The client can use event IDs to deduplicate messages: store processed IDs, compare new events against stored IDs, and skip duplicates. This is especially useful after reconnection when the server may resend events from before the disconnect.

## Q82: How do you handle SSE in a microservices architecture?
**A:** Microservices SSE pattern: (1) a dedicated SSE gateway/service maintains connections with clients, (2) internal services publish events to a message broker (Kafka, Redis), (3) the SSE gateway subscribes to the broker and forwards to appropriate clients, (4) use consistent hashing or sticky routing for scalability.

## Q83: What is the difference between SSE and Server Push (Push API)?
**A:** SSE is a server-to-client streaming protocol using HTTP. The Push API (Service Worker Push) is a browser API for sending push notifications even when the page is not open, using service workers. Push API requires user permission, works when the page is closed, and goes through a push service.

## Q84: How do you combine SSE with Service Workers for offline support?
**A:** The service worker can intercept SSE connections and: (1) cache the last N events, (2) serve cached events when offline, (3) replay missed events on reconnection, (4) manage reconnection logic. The service worker acts as a proxy between the EventSource and the network.

## Q85: How do you implement SSE with Express.js and TypeScript?
**A:** Express + TypeScript SSE: define route handler with Request, Response types, set headers (Content-Type, Cache-Control), use res.write() with formatted strings, use req.on('close', ...) for cleanup. Optionally use a helper class for connection management.

## Q86: How do you implement SSE with FastAPI and asyncio?
**A:** FastAPI SSE: create an async generator that yields SSE-formatted strings, use StreamingResponse(generator(), media_type="text/event-stream"). The generator loops checking for new data (e.g., from asyncio.Queue). FastAPI handles concurrency and cleanup automatically.

## Q87: What is the EventSource's onmessage vs addEventListener difference?
**A:** onmessage is a handler for unnamed events (no event: field). addEventListener('eventname', handler) handles named events. Both can coexist. Unnamed events trigger onmessage; named events trigger addEventListener('name'). Use onmessage for generic data and addEventListener for typed events.

## Q88: How do you handle SSE with multiple browser tabs?
**A:** Each tab opens its own SSE connection. To share a single connection: (1) use a SharedWorker that maintains one SSE connection across tabs, (2) use BroadcastChannel API to distribute events from one tab's SSE connection, (3) use localStorage events for simple coordination.

## Q89: How does SSE handle the Connection header?
**A:** The server should set Connection: keep-alive to maintain the persistent connection. Some servers send Connection: close, which would break SSE. The browser's EventSource handles this automatically by reopening the connection if closed.

## Q90: What are the performance characteristics of SSE vs polling?
**A:** SSE: persistent connection, low latency, minimal headers per message, no HTTP handshake overhead. Polling: new HTTP connection per request (even with keep-alive), higher latency (polling interval), more server load (handling frequent requests). SSE is significantly more efficient.

## Q91: How does SSE memory usage compare to WebSockets?
**A:** Both maintain a TCP connection with similar memory overhead for the socket. SSE has slightly less overhead as it uses HTTP framing. On the server, each connection requires memory for buffers and connection state. SSE connections are typically idle-specific but memory usage is comparable.

## Q92: How do you implement SSE with a connection pool?
**A:** Maintain a Map on the server mapping user IDs or session IDs to their SSE response objects. Add entries on new connections, remove on disconnect. Use the pool to broadcast events: iterate entries, write to each connection, handle write errors (disconnected clients).

## Q93: How do you broadcast SSE events to all connected clients?
**A:** Maintain a global list of active SSE response objects. When a broadcast event occurs, iterate the list and write the event to each. Handle write errors by removing disconnected clients. For multi-process setups, use Redis Pub/Sub to broadcast across processes.

## Q94: How do you implement room/channel-based SSE subscriptions?
**A:** Maintain a Map of rooms to sets of SSE connections. Clients subscribe to rooms (via URL path or initial event). Broadcast events only to connections in the target room. Leave room on client disconnect. Cross-process rooms require a shared pub/sub system.

## Q95: What is the difference between SSE and chunked transfer encoding?
**A:** SSE uses chunked transfer encoding as the transport mechanism but adds an application-level protocol (event:, data:, id:, retry: fields). Chunked transfer encoding alone is just a way to send HTTP response in chunks without SSE semantics.

## Q96: How do you handle streaming JSON over SSE with large payloads?
**A:** For large JSON payloads: (1) split across multiple data: lines, (2) use compression (gzip), (3) paginate — send summary first, then fetch details via separate request, (4) stream the JSON itself as multiple events, each containing a portion of the data.

## Q97: What are security considerations for SSE in production?
**A:** Security measures: (1) always use HTTPS to prevent eavesdropping, (2) authenticate connections, (3) validate event IDs to prevent replay attacks, (4) set appropriate CORS policies, (5) rate-limit connections per user/IP, (6) sanitize event data before sending, (7) timeout idle connections.

## Q98: How do you monitor SSE connections in production?
**A:** Monitoring: (1) track active connection count (gauge metric), (2) log connection/disconnection events, (3) monitor message throughput (events/sec), (4) track reconnection rates as health indicator, (5) measure latency between server send and client receive, (6) use application performance monitoring (APM) tools.

## Q99: What are the alternatives to SSE for real-time web communication?
**A:** Alternatives: (1) WebSockets (bidirectional, full-duplex), (2) WebRTC DataChannels (peer-to-peer, low latency), (3) Long Polling (compatible, high overhead), (4) HTTP/2 Server Push (resource pushing), (5) gRPC streaming (bidirectional, binary), (6) MQTT over WebSockets (IoT-friendly).

## Q100: Design a real-time notification system using SSE for a social media platform with 1 million concurrent users. What's your architecture?
**A:** Architecture: (1) **Load Balancers** with HTTP/2 support (ALB/HAProxy) routing to SSE gateway cluster, (2) **SSE Gateway** (Node.js/Go) — stateless servers maintaining persistent connections, (3) **Redis Pub/Sub** — broadcasts events across gateway instances (pub/sub per user channel), (4) **Notification Service** — produces notifications (likes, comments, follows) to Redis, (5) **Connection Management** — Map<userId, Set<response>> per gateway instance, (6) **Heartbeat** — comment line every 30s to keep connections alive, (7) **Reconnection** — EventSource auto-reconnect with Last-Event-ID, server replays missed events from a short-term buffer (Redis sorted sets), (8) **Rate Limiting** — max 10 SSE connections per user, (9) **Backpressure** — detect slow consumers and drop non-critical events, (10) **Monitoring** — Prometheus metrics for active connections, event throughput, reconnection rate; Grafana dashboards, (11) **Fallback** — if EventSource fails, fall back to periodic polling, (12) **HTTPS** — mandatory for security, with HSTS preload.
