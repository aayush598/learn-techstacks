# WebSockets, Webhooks, and SSE

> **TL;DR**: WebSockets (full-duplex, persistent, over a single TCP/TLS connection), Server-Sent Events (SSE — one-way server push over plain HTTP), and Webhooks (server-to-server HTTP callbacks on events) are the three ways servers push data to clients/apps — they exist because plain request/response HTTP can't do *low-latency, event-driven* communication without polling.

## 1. Why Does This Exist?
HTTP is request/response: the *client* initiates, the server replies. That's wrong-shaped for real-time features — chat, notifications, live scores, stock tickers, dashboards, collaborative editing — where the *server* has new data and must reach the client *immediately*. The naive fix (client **polling** every few seconds) wastes bandwidth, adds latency, and hammers servers. The push ecosystem exists to answer: "how does the server deliver data the moment it exists, efficiently and reliably?"
- **WebSockets** (RFC 6455): full-duplex, bidirectional, persistent channel over a single TCP connection — chat, gaming, live updates where both sides talk.
- **SSE** (EventSource, HTML5): *one-way* server→client push over plain HTTP (a long-lived response) — notifications, live feeds, dashboards where only the server sends.
- **Webhooks**: *server-to-server* callbacks — when an event happens, *your* system calls *their* URL (e.g., Stripe → your endpoint on payment). The push is between machines, asynchronously.

## 2. How Does It Work?
- **WebSocket** (RFC 6455): starts as an HTTP request with `Upgrade: websocket` + `Connection: Upgrade` + `Sec-WebSocket-Key` (a random base64 nonce). Server replies `101 Switching Protocols` with `Sec-WebSocket-Accept` (SHA-1 of key + magic GUID `258EAFA5-E914-47DA-95CA-C5AB0DC85B11`). The TCP connection is then "upgraded" into a **full-duplex binary/text frame protocol** — no more HTTP semantics, both sides send at any time. Frames have opcodes (text, binary, ping/pong, close), masking (client→server), length. Ports 80/443 (wss = TLS). Multiplexing is *not* in the spec (subprotocols exist; STOMP, Socket.IO layer on top).
- **SSE** (EventSource API): the client opens a normal GET with `Accept: text/event-stream`; the server keeps the HTTP response open and streams `data: ...\n\n` lines (with optional `event:`, `id:`, `retry:`). One-way, auto-reconnect (the browser retries with `Last-Event-ID`), plain HTTP (works through proxies), no binary, text-only, can compress with gzip/br.
- **Webhooks**: *not* a protocol — a pattern: your service registers a URL; when an event fires, the service POSTs a JSON payload (signed with a secret for authenticity) to that URL. Delivery is HTTP, one-way, async, at-least-once (retries with backoff). Signature: `X-Signature` HMAC of body.

## 3. When Is It Used?
- **WebSocket**: live chat (Slack, Discord, WhatsApp Web), online gaming, collaborative editing (Google Docs), real-time dashboards, trading terminals, streaming telemetry, apps where both sides exchange messages at low latency.
- **SSE**: notification feeds, live scoreboards, activity/event streams, server logs streaming, social feeds (Twitter timeline), progress updates — anywhere the server pushes *to* the client and one-way suffices.
- **Webhook**: payment events (Stripe invoice.paid), CI/CD build notifications (GitHub push → build server), order/fulfillment events (Shopify), messaging integrations (Slack incoming webhooks), event-driven integrations between services.
- **Polling**: kept as the simple fallback for low-frequency checks (health probes, status badges) and when the client can't hold connections.

## 4. Why Wasn't Another Approach Chosen?
- **Why not just poll?** Polling wastes requests when nothing changed, adds latency (up to interval), and hammers the server/DB under load. Push eliminates idle polls. Polling survives only for low-frequency or stateless checks (or to *supplement* push).
- **Why WebSocket instead of two HTTP requests?** Long-polling (hold an HTTP request open until data) reuses HTTP but re-establishes connections repeatedly (headers/overhead) and still queues. WebSocket upgrades *once* and then speaks a lean binary/text frame protocol with negligible per-message overhead — and it's bidirectional.
- **Why SSE instead of WebSocket for server→client-only?** SSE is simpler, rides plain HTTP (proxies/CDNs/load balancers work with it, no upgrade handling), auto-reconnects with `Last-Event-ID` (a killer feature), and is text-stream friendly (gzip). WebSocket needs a WS-aware proxy, has no built-in reconnect-with-position, and its full-duplex is unneeded. Rule: **server→client only → SSE; bidirectional → WebSocket**.
- **Why Webhooks instead of WebSocket to servers?** Webhooks are *asynchronous, fire-and-forget HTTP callbacks* between long-lived servers — the caller doesn't need a persistent connection to each subscriber (which wouldn't scale to thousands of consumers). WebSocket to server farms implies stateful long-lived connections per subscriber = painful. HTTP callback + retry + signature = simple, scalable, idempotent.
- **Why not message queues?** Queues (Kafka/SQS) are the *backbone* for reliable internal async; webhooks are the *external* delivery mechanism. They compose: event → queue → worker → webhook POST.

## 5. Intuition
- **Polling** = calling a friend every 5 seconds to ask "any news?" — works but annoying and expensive.
- **Long-polling** = calling and *staying on the line* until they have news, hanging up, calling back — better, but you re-dial constantly.
- **WebSocket** = a **phone line that stays open in both directions** — you can talk any time, they can talk any time, no re-dialing (bidirectional live).
- **SSE** = a **radio broadcast** — you just *listen* (one-way); if you tune out, you can resume from where you left off (`Last-Event-ID`).
- **Webhook** = your **neighbor promises to text you** (POST to your URL) the moment something happens — you don't call, you get notified; if your phone's off, they retry (at-least-once).

## 6. Real-World Analogy
**The stock ticker at a brokerage**: Polling = you refresh the page every 5 seconds (expensive, laggy). SSE = the ticker tape scrolls on its own — the exchange streams updates, you watch (one-way push, resumes where you were). WebSocket = a live trader's terminal where *you* can also send orders while watching the tape (bidirectional). Webhooks = the exchange emails the *clearing firm* when a trade settles — a machine-to-machine notification, and if the clearing firm is down, the exchange retries. Different tools, same goal: "get the update without asking for it."

## 7. Formal Definition
- **WebSocket** (RFC 6455): a full-duplex, message-based protocol over a single TCP (or TLS) connection, established via an HTTP `Upgrade` handshake (`101 Switching Protocols`). Uses a frame format with opcodes (0x1 text, 0x2 binary, 0x8 close, 0x9/0xA ping/pong), 7-64-bit lengths, and client→server masking. Provides no reliability beyond TCP and no built-in multiplexing/subprotocols beyond negotiation.
- **SSE** (Server-Sent Events, HTML5 / WHATWG EventSource): a server-push mechanism over a single long-lived HTTP response with media type `text/event-stream`; messages are `data:`-lines (plus `event:`, `id:`, `retry:`), auto-reconnect via `Last-Event-ID`. One-way (server→client), text-based.
- **Webhook**: an HTTP POST (or callback) triggered by an event, sent from a provider's service to a subscriber's registered URL, typically JSON, signed (HMAC) for authenticity, delivered at-least-once with retry/backoff. Not a standardized protocol — a design pattern atop HTTP.

## 8. Example
**A live chat + a notification feed + a payment webhook**:
```
[WebSocket upgrade]
Client -> Server:  GET /chat HTTP/1.1
                   Host: app.example.com
                   Upgrade: websocket
                   Connection: Upgrade
                   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
                   Sec-WebSocket-Version: 13
Server -> Client:  HTTP/1.1 101 Switching Protocols
                   Upgrade: websocket
                   Connection: Upgrade
                   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
(Now both sides send masked/framed messages at any time; e.g., chat messages flow both ways.)
```
```
[SSE]
Client -> Server:  GET /events HTTP/1.1
                   Accept: text/event-stream
Server -> Client:  HTTP/1.1 200 OK
                   Content-Type: text/event-stream
                   Cache-Control: no-cache
                   Connection: keep-alive
                   data: {"type":"order","id":42}
                   id: 42
                   data: {"type":"system","msg":"deploy starting"}
```
```
[Webhook]
Stripe -> Your API:  POST https://you.example.com/webhooks/payment
  { "type": "invoice.paid", "data": { "id": "in_123", "amount": 5000 } }
  X-Stripe-Signature: t=...v1=... (HMAC-SHA256 of raw body + timestamp)
Your API: verify signature (constant-time), process idempotently, return 200.
```
Client sees live chat (WS), a scrolling notification feed (SSE), and the payment system notifies your backend (webhook) — three pushes, three mechanisms.

## 9. Internal Working
1. **WebSocket handshake**: the `Sec-WebSocket-Key` (random 16-byte base64) proves it's a fresh upgrade; server computes `Accept = base64(SHA1(key + magic))`. On `101`, the TCP connection is *reused* as the frame stream (the same socket that carried HTTP).
2. **WebSocket framing**: `FIN | RSV | opcode(4) | MASK | len(7/16/64) | masking-key | payload`. Client frames are masked (anti-cache-poisoning). Ping/pong keeps the connection alive through proxies; close handshake (close frame + echo) is graceful. No ordering/duplication guarantees beyond TCP.
3. **WS + load balancers**: LB must support the upgrade (many terminate WS and proxy the upgraded connection; some break it → subprotocol "Socket.IO"/"SockJS" add fallbacks). Idle timeouts need ping/pong + LB idle settings.
4. **SSE streaming**: the server *never ends the response*; it flushes lines. `id:` sets the event ID; on disconnect the browser reconnects sending `Last-Event-ID` so the server can resume. Compression (gzip) works. SSE is multiplexed with other HTTP requests on the same connection (HTTP/1.1 keep-alive or h2 multiplexing).
5. **SSE limits**: text-only (send JSON), one-way, and if the client is behind a proxy that buffers (nginx `X-Accel-Buffering: no`, flush) it breaks. h2 can multiplex several SSE streams per connection.
6. **Webhook reliability**: delivery is **at-least-once** — receivers must be **idempotent** (dedupe by event ID). Providers retry with exponential backoff (Stripe: up to ~3 days). Signatures: `t=timestamp,v1=HMAC_SHA256(secret, timestamp + '.' + raw_body)` — verify with a *constant-time* compare; reject old timestamps (replay).
7. **Scale patterns**: millions of WS connections need horizontal scaling + pub/sub (Redis) so any node can route a message to the node holding the socket; SSE scales similarly with connection affinity or a gateway; webhooks scale by queueing + worker pools.

## 10. Time Complexity
- **Polling**: O(1) requests but O(interval⁻¹) cost per client — N clients × frequency → wasteful (the *reason* push exists).
- **WebSocket**: one handshake (1-2 RTT) then O(1) per message with tiny headers (2-14 bytes frame overhead) — negligible vs HTTP headers (~500 B+). Massive savings at high message rates.
- **SSE**: O(1) connection; per-message is a line flush (O(payload)); reconnect logic O(1) with `Last-Event-ID`. Compression makes long messages cheap.
- **Webhook**: O(1) POST per event + retries; at-least-once means receivers do O(1) idempotency checks. The dominant cost is the *event producer's* fan-out (queue + workers).

## 11. Advantages
- **WebSocket**: true bidirectional low-latency; minimal per-message overhead; real-time; works over 80/443 (wss); browser-native API; binary + text.
- **SSE**: simplest server→client push; rides plain HTTP (works with proxies/CDNs/LBs, h2 multiplexing); auto-reconnect with Last-Event-ID (resume); text + gzip; no special infra.
- **Webhook**: async + decoupled (subscriber doesn't need a live connection); server-to-server; idempotency/retry patterns well-established; signature-based authenticity; works with standard HTTP stack.
- **All three**: avoid polling, enable event-driven architectures, compose with queues/proxies.

## 12. Disadvantages
- **WebSocket**: stateful (connection affinity on LBs — horizontal scale is harder), no built-in multiplexing/autoreconnect, proxy/load-balancer upgrade support needed, more complex lifecycle (close/ping/backpressure), can be blocked by strict proxies.
- **SSE**: one-way only, text-only (JSON-encode binary), streaming buffering pitfalls (proxies), connection-count limits per browser (older ~6/host limit), no true "send from client" (use fetch + SSE).
- **Webhook**: at-least-once requires idempotent receivers; signature/secret management; latency (no real-time, just event-driven); debugging is harder (async + third-party); redelivery ordering not guaranteed.
- **Polling still exists**: for very-low-frequency checks it's simpler — the "avoid it" mantra has caveats.

## 13. Interview Questions
1. **Q: What are the three server-push mechanisms?** A: WebSocket (bidirectional, full-duplex over TCP), SSE (one-way server→client over HTTP), Webhook (server→server HTTP callback). Plus long-polling as the legacy predecessor.
2. **Q: When do you choose SSE over WebSocket?** A: SSE when only the *server* pushes (notifications, feeds, dashboards, stock tickers) and you value simplicity, auto-reconnect with `Last-Event-ID`, and proxy/HTTP compatibility. WebSocket when *both* sides send (chat, games, collaborative editing) or you need binary.
3. **Q (tricky): Can you do client→server messaging over SSE?** A: Not through the SSE stream (it's one-way), but the client can send via normal `fetch`/`POST` on separate requests and still receive the SSE stream — "SSE for down, HTTP for up" is a valid pattern (simpler than WS when the up-link is rare).
4. **Q: How does the WebSocket upgrade work?** A: HTTP request with `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key` (random nonce). Server replies `101 Switching Protocols` with `Sec-WebSocket-Accept` (SHA-1(key + RFC 6455 magic GUID)). The same TCP connection then speaks the frame protocol.
5. **Q: What does the `Sec-WebSocket-Accept` prove?** A: That the server *understood* the handshake — it's a deterministic function of the client's key + a fixed GUID, so both sides know they're speaking the WebSocket protocol (and it can't be reused across connections/replayed).
6. **Q (production): Your WebSocket scale target is 1M concurrent connections. What's hard?** A: (1) Connection *affinity* — an LB must route a client's socket to the same node (sticky/consistent hashing); (2) fan-out — publishing to the node holding each socket (Redis pub/sub); (3) resource limits — file descriptors, memory per socket, heartbeat timeouts; (4) load-balancer idle timeouts (keep-alive); (5) graceful deploys (drain + reconnect). This is the classic scale question.
7. **Q: How does SSE auto-reconnect work?** A: The EventSource API reconnects automatically on error; it sends `Last-Event-ID` so the server can resume from the last delivered event. Combined with `retry:` (server-suggested delay), it gives reliable at-least-once server→client delivery with position tracking.
8. **Q: What's the difference between SSE and long-polling?** A: Long-polling: hold an HTTP response open until data, then *close and reconnect* — repeated handshake overhead and queueing, still "request/response shaped." SSE: one long-lived response streaming many events — persistent connection, no per-event setup, resume by ID.
9. **Q (scenario): You need live chat + a live feed + payment notifications. Choose technologies.** A: Chat → WebSocket (bidirectional). Live feed → SSE (one-way, resume). Payments → Webhook (async server-to-server, idempotent, signed). Rationale: match directionality and the endpoint relationship to each mechanism.
10. **Q: What is a webhook and how is it made trustworthy?** A: An HTTP POST from a provider to your URL on an event. Trust = **signature**: HMAC of `timestamp.body` with a shared secret (constant-time compare), reject stale timestamps; plus IP allowlists and TLS. Without verification, anyone can POST fake events.
11. **Q: Why must webhook receivers be idempotent?** A: Delivery is **at-least-once** — providers retry (backoff, days) on timeouts/5xx. Receivers must dedupe by event ID (or unique key) so a retried event isn't processed twice (double-payment, double-credit). Idempotency is the webhook contract.
12. **Q (tricky): Why do some load balancers/proxies break WebSockets?** A: The LB must (a) support the HTTP upgrade and (b) keep the upgraded connection alive without idle-timeout/HTTP-buffering logic. Old proxies re-parse HTTP, drop upgrade headers, buffer, or time out the long-lived connection. Solution: WS-aware LBs/gateways + configured timeouts + heartbeats.
13. **Q: Can HTTP/2 handle SSE better?** A: Yes — HTTP/2 multiplexes many SSE streams over one connection (no ~6-connection browser limit for many feeds) and compresses headers. But the browser API (EventSource) over h2 works transparently.
14. **Q: What is the `text/event-stream` format?** A: Lines: `event: name`, `data: payload`, `id: n`, `retry: ms`; a blank line dispatches an event; `data:` can span multiple lines. The browser delivers the assembled `event.data` to the handler. It's simple, text, gzip-friendly.
15. **Q (production): How do you monitor/debug webhook delivery?** A: Log every delivery + response + retry; track per-event-type latency/failure rates; use replay tooling; validate signatures in tests; alert on non-2xx persistence; and use a queue/worker (SQS) so webhook processing survives crashes.
16. **Q: WebSocket or SSE for a collaborative editor (Google Docs)?** A: WebSocket — editing needs low-latency *bidirectional* delta exchange (client sends ops, server broadcasts ops) with ordered delivery. SSE is one-way; you'd be POSTing constantly, which is fine but adds a round trip per op and halves the efficiency. (OT/CRDT needs a full-duplex channel.)

## 14. Follow-Up Questions
1. **Q: What is the RFC 6455 magic GUID and why is it fixed?** A: `258EAFA5-E914-47DA-95CA-C5AB0DC85B11` — a fixed GUID appended to the client's key before SHA-1. Fixed so the accept value is deterministic and predictable (both sides can compute it); it prevents cache-poisoning reuse of the handshake.
2. **Q: What is masking in WebSocket frames and why?** A: Client→server frames are XOR-masked with a random 4-byte key (RFC 6455 requirement) to prevent *cache poisoning* — an attacker can't craft a frame that proxies interpret as a valid HTTP response. Servers don't mask.
3. **Q: What is Socket.IO / SockJS and when do you use them?** A: Abstraction layers that negotiate WS → long-polling → SSE fallbacks, add rooms/namespaces/reconnect/acks. Use when you need fallback for old proxies/firewalls; the cost is protocol overhead and hidden magic.
4. **Q: What is the difference between "at-most-once" and "at-least-once" webhook delivery?** A: At-most-once: never retry (data may be lost). At-least-once: retry until 2xx (data may duplicate — receiver dedupes). Webhooks are at-least-once; exactly-once is impossible across async HTTP (requires idempotency + dedup).
5. **Q: How does a chat system route a message to the right WS node?** A: Every node holds a set of connections; the gateway publishes to a shared bus (Redis/Kafka) tagged by room; the node(s) holding the room's sockets forward to the clients. This decouples "who knows" from "who holds the socket."

## 15. Coding Example
```python
# Minimal WebSocket server (WebSocket handshake + echo) — see the frame protocol
import socket, base64, hashlib, struct, os

def ws_accept(key):
    return base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()

def decode_frame(data):
    fin, opcode = data[0] >> 7, data[0] & 0x0f
    masked = data[1] >> 7
    ln = data[1] & 0x7f
    off = 2
    if ln == 126:  ln = struct.unpack(">H", data[2:4])[0]; off = 4
    elif ln == 127: ln = struct.unpack(">Q", data[2:10])[0]; off = 10
    mask = data[off:off+4] if masked else None; off += 4 if masked else 0
    payload = data[off:off+ln]
    if mask: payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    return opcode, payload

srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 8765)); srv.listen(1)
conn, _ = srv.accept()
req = conn.recv(4096).decode()
key = [l.split(":")[1].strip() for l in req.split("\r\n") if l.lower().startswith("sec-websocket-key")][0]
conn.send(("HTTP/1.1 101 Switching Protocols\r\n"
           "Upgrade: websocket\r\nConnection: Upgrade\r\n"
           f"Sec-WebSocket-Accept: {ws_accept(key)}\r\n\r\n").encode())
op, msg = decode_frame(conn.recv(4096))
print("Got:", op, msg)
conn.close()
```
```python
# SSE server (Flask-like): stream events, client reconnects via Last-Event-ID
import time, json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class SSE(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        event_id = 0
        try:
            while True:
                event_id += 1
                self.wfile.write(f"id: {event_id}\ndata: {json.dumps({'tick': event_id})}\n\n".encode())
                self.wfile.flush()
                time.sleep(1)
        except (BrokenPipeError, ConnectionResetError):
            pass
```
```bash
# Webhook signature verification (Stripe-style HMAC) — the receiver contract
$ stripe listen --forward-to localhost:8000/hooks   # local webhook testing
# A client consuming SSE:
$ curl -N -H "Accept: text/event-stream" https://stream.example.com/events
# data: {"tick": 1}
# id: 1
# data: {"tick": 2}   ...streams forever
# WebSocket testing:
$ wscat -c wss://echo.websocket.org   # interactive WS client
```

## 16. Industry Usage
- **Slack/Discord**: WebSocket for real-time chat (persistent connections to gateways); Discord processes millions of concurrent WS connections with horizontal gateway sharding.
- **Twitter/X, Bloomberg**: SSE for live feeds (timeline updates, market data) — simple, resume-safe push to web clients.
- **Stripe/GitHub/Shopify**: webhooks for events (payments, pushes, orders) — signed, at-least-once, idempotent receivers; Stripe's webhook system is the reference implementation.
- **Google Docs / Figma**: WebSocket (or CRDT-over-WS) for collaborative editing — bidirectional op exchange with ordering.
- **AWS**: API Gateway supports WebSocket APIs; SNS/SQS → webhook fan-out (SNS → HTTP endpoint); CloudWatch + SNS = alert webhooks. Event-driven architecture is webhook-heavy at scale.

## 17. References
- RFC 6455 — The WebSocket Protocol: https://www.rfc-editor.org/rfc/rfc6455
- HTML Living Standard, "Server-Sent Events" (EventSource) — https://html.spec.whatwg.org/multipage/server-sent-events.html
- MDN — WebSocket API / Server-Sent Events: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
- Stripe Webhooks docs — https://docs.stripe.com/webhooks
- GitHub webhooks docs — https://docs.github.com/en/webhooks
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 2 (application-layer protocols).

## 18. Cheat Sheet
- WebSocket: full-duplex, TCP, `Upgrade` + `101`, frames (text/binary/ping/pong/close), client masks. Ports 80/443 (wss).
- SSE: one-way server→client, `text/event-stream`, `data:`/`id:`/`retry:`, auto-reconnect with `Last-Event-ID`.
- Webhook: async HTTP POST callback, signed (HMAC), at-least-once → receiver idempotent.
- Rule: bidirectional → WS; server→client only → SSE; machine→machine event → webhook.
- Polling = fallback of last resort (or for low-frequency checks).
- WS scale: affinity, pub/sub fan-out, fds/memory, heartbeats.
- WS-Accept = SHA1(key + magic GUID). Magic GUID = 258EAFA5-E914-47DA-95CA-C5AB0DC85B11.
- SSE over h2 = multiplexed streams; gzip works.
- Webhook retries: exponential backoff, dedupe by event ID.

## 19. Quiz
1. Which is bidirectional? a) SSE b) WebSocket c) Webhook d) Long-polling → **b**
2. WS upgrade reply code: a) 200 b) 101 c) 301 d) 426 → **b**
3. `Sec-WebSocket-Accept` is: a) random b) SHA1(key+magic) c) TLS key d) token → **b**
4. SSE media type: a) application/json b) text/event-stream c) multipart d) octet-stream → **b**
5. SSE resume uses: a) Cookie b) Last-Event-ID c) Range d) ETag → **b**
6. Webhook delivery model: a) at-most-once b) at-least-once c) exactly-once d) fire-forget no retry → **b**
7. Webhook authenticity uses: a) TLS only b) HMAC signature c) Basic auth d) cookies → **b**
8. Client→server frames in WS are: a) encrypted b) masked c) signed d) compressed → **b**
9. Which needs sticky/affinity LBs? a) SSE b) WebSocket c) Webhook d) polling → **b**
10. Why not poll? a) too fast b) wasteful + laggy c) insecure d) complex → **b**

## 20. Flashcards
- **Q: WS vs SSE vs webhook?** → **A:** WS = bidirectional live; SSE = one-way server→client; webhook = async server→server callback.
- **Q: WS handshake?** → **A:** HTTP Upgrade → 101 Switching Protocols.
- **Q: SSE reconnect?** → **A:** Auto via Last-Event-ID (resume position).
- **Q: Webhook reliability?** → **A:** At-least-once → receiver idempotent; signed with HMAC.
- **Q: When to choose SSE?** → **A:** Server→client only push (feeds, notifications) — simple, HTTP-native.
- **Q: Magic GUID?** → **A:** 258EAFA5-E914-47DA-95CA-C5AB0DC85B11 (WS accept).
- **Q: WS scale challenges?** → **A:** Affinity, pub/sub fan-out, fds/memory, heartbeats.

## 21. Revision
Three push mechanisms: WebSocket (bidirectional, TCP, HTTP Upgrade → 101, frames with masking; needs affinity LBs; chat/games), SSE (one-way server→client, text/event-stream, auto-reconnect via Last-Event-ID; feeds/notifications), Webhook (async server→server HTTP callback, HMAC-signed, at-least-once → idempotent receiver; Stripe-style). Rule: bidirectional → WS; one-way → SSE; machine events → webhook. Polling is the inefficient fallback. WS scale needs connection affinity + pub/sub; webhook reliability needs retries + dedup.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "WebSocket vs SSE vs webhook?" | 2 How It Works / 13 Q&A |
| "When to choose SSE over WS?" | 13 Q&A / 4 Why Another Approach |
| "How does the WS upgrade work?" | 9 Internal Working / 13 Q&A |
| "Scale WS to 1M connections?" | 13 Q&A / 14 Follow-Up |
| "How to secure webhooks?" | 13 Q&A / 15 Coding |
| "Why are webhook receivers idempotent?" | 13 Q&A / 10 Time Complexity |
| "Design live chat." | 13 Q&A / 16 Industry Usage |
| "What is Last-Event-ID?" | 13 Q&A / 9 Internal Working |
