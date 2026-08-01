# TCP Connection Termination (Four-Way Handshake)

> **TL;DR**: TCP closes gracefully with 4 segments — FIN, ACK, FIN, ACK — because **each direction closes independently** (half-close). The active closer then waits in TIME_WAIT for 2×MSL (~60 s) so stray segments can't corrupt a new connection reusing the same tuple; RST provides an abrupt, non-graceful abort instead.

## 1. Why Does This Exist?
TCP is a *full-duplex byte stream*: each direction is an independent, reliably delivered flow with its own sequence numbers. Graceful teardown must therefore be two independent one-way closes — "I'm done sending, but I'll still receive your remaining data" — which is exactly what FIN enables. The FIN+ACK exchange per direction is 4 segments. The second design problem: after close, *late packets* from the dead connection could arrive and be misdelivered to a *new* connection that happens to reuse the same (srcIP, srcPort, dstIP, dstPort) tuple. The TIME_WAIT state (2×MSL, ~60 s) exists precisely so any in-flight, duplicate, or misordered segments die before the tuple can be reused. RST exists for the non-graceful case (error, abort, refuse) where a FIN handshake is pointless or impossible.

## 2. How Does It Work?
```
Client (active closer)                 Server (passive closer)
        |                                    |
        |  FIN: seq = m                     |  1. Client has no more data to send
        |----------------------------------->|
        |                                    |  2. Server ACKs the FIN,
        |  ACK: ack = m+1                   |     but keeps sending its own data
        |<-----------------------------------|     (half-close: client done, server not)
        |          ... server data ...       |
        |                                    |  3. Server finishes its data, closes
        |  FIN: seq = n                      |
        |<-----------------------------------|
        |                                    |  4. Client ACKs; client enters TIME_WAIT
        |  ACK: ack = n+1                   |     (2×MSL), server closes immediately
        |----------------------------------->|
        |                                    |
        v        closed after 2×MSL          v
```
- **FIN**: "I have no more data to send." Consumes one sequence number. Both sides can send FIN independently.
- **Half-close**: after step 2, the *client* has stopped sending but can still *receive* the server's remaining data — the connection is half-open for the server's direction.
- **State transitions**: active closer ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED; passive closer ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED.
- **TIME_WAIT**: active closer waits 2×MSL (typically 2×30s = 60 s). This is *required*, not a bug.
- **RST abort**: any host can send RST to kill the connection instantly (no handshake, no TIME_WAIT) — used on errors, unsolicited data, or `SO_LINGER` with timeout 0.

## 3. When Is It Used?
- **Every normal connection close**: when a client is done (browser tab close, curl finish), or a server closes (connection: close). The 4-way FIN dance is invisible to apps — `close()`/`shutdown()` triggers it.
- **Half-close semantics**: a client that needs a "one-shot request/response" (e.g., HTTP/1.0, or `shutdown(SHUT_WR)`) uses FIN to say "my request is complete, now stream your response."
- **TIME_WAIT in production**: high-connection-churn servers (load balancers, proxies, web servers closing keep-alives) accumulate TIME_WAIT sockets → port exhaustion → engineers tune `tcp_tw_reuse`/`tcp_tw_recycle` (risky!) or `SO_REUSEADDR`.
- **Abort/errors**: protocol violations, half-open connections, or "connection reset by peer" (RST) — a *diagnostic*, not a graceful close.
- **`shutdown()` vs `close()`**: shutdown(SHUT_WR) = FIN only; close() = FIN on both directions (or RST with SO_LINGER 0).

## 4. Why Wasn't Another Approach Chosen?
- **Why 4 segments instead of 2 (FIN+ACK)?** Because the two directions are independent. A single FIN+ACK would imply both sides stop sending *simultaneously*, breaking half-close — but the whole point is that one side may still have data to deliver. Two one-way closes = 2 FINs + 2 ACKs = 4. (And in practice, when both sides close simultaneously, it can collapse to fewer, but the protocol's canonical form is 4.)
- **Why not skip ACK and just FIN both ways?** Without the ACKs, neither side would know the peer received the close — the same "two generals" problem as setup. Each FIN must be acknowledged.
- **Why TIME_WAIT at the *active* closer and for 2×MSL?** The active closer is the last to send; if the *final ACK is lost*, the passive closer will retransmit its FIN — and only the active closer can answer it. 2×MSL guarantees: (a) enough time for the peer's FIN retransmission + the active closer's ACK to complete, and (b) any stale segments from the old connection (max lifetime = MSL) expire before the tuple is reusable.
- **Why not just allow immediate tuple reuse?** A delayed old segment arriving at a *new* connection with the same tuple would be interpreted as part of the new stream (data corruption, seq confusion) — exactly what TIME_WAIT prevents.
- **Why RST for abort?** A graceful FIN needs both sides cooperative; on an error, a half-broken connection, or a resource crisis you can't wait — RST is a one-way, immediate kill that discards all in-flight data.

## 5. Intuition
Think of a **two-lane one-way bridge between two towns** (your upload lane, your download lane). Finishing a phone call *politely*: Town A says "I have nothing more to send across MY lane" (FIN), Town B says "got it, acknowledged" (ACK). But Town B might still be sending cars across ITS lane, so A keeps receiving. When B finishes its own lane, B says "now I'm done too" (FIN), and A confirms (ACK). Four messages, because two independent lanes each need a "done + confirm." Afterward, A — the one who said "I'm done" first — must wait at the intersection for 2×MSL to make sure no lost car (packet) from the old traffic is still cruising the road, because if a new delivery batch (new connection) starts with the same address labels, a stray car could crash into it. Waiting is the only way to guarantee the road is truly empty.

## 6. Real-World Analogy
**Ending a phone call the right way**: "I'm done talking — is there anything else?" (your FIN). "Got it — let me finish what I was saying" (ACK, and the other person keeps talking). They say everything they wanted, then: "Okay, I'm done too now" (their FIN). "Great, goodbye" (your ACK). Four utterances, because each side needs its own closing + acknowledgment. Then *you*, the one who hung up, wait 60 seconds before re-dialing the same number — because if the other person was mid-sentence (a lost FIN retransmission) and you reconnect, their "last words" (stray packets) could land on your *new* call. The wait makes it safe to reuse the phone line. Abrupt version: slamming down the phone (RST) — the line dies instantly, but whatever was being said is lost.

## 7. Formal Definition
TCP connection termination (RFC 793 §3.5): each end closes its send direction with a FIN segment (consuming one sequence number) acknowledged by the peer with an ACK. The active closer transitions ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED; the passive closer goes ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED. The active closer holds TIME_WAIT for 2×MSL (Max Segment Lifetime, typically 60 s) to allow retransmission of a lost final ACK and to expire stale segments before tuple reuse. Abrupt termination uses an RST segment, discarding all in-flight data without handshake or TIME_WAIT.

## 8. Example
Real teardown on an HTTP/1.0 connection (server closes after response):
```
$ sudo tcpdump -nn -i lo tcp port 8000 -vv
1: ... 10.0.0.5.8000 > 10.0.0.5.45000: Flags [F.], seq 101, ack 51, length 0
2: ... 10.0.0.5.45000 > 10.0.0.5.8000: Flags [.], ack 102, length 0
3: ... 10.0.0.5.45000 > 10.0.0.5.8000: Flags [F.], seq 51, ack 102, length 0
4: ... 10.0.0.5.8000 > 10.0.0.5.45000: Flags [.], ack 52, length 0
```
Server sent FIN first (seq=101, ack=51) → client ACKs (ack=102) → client closes its side with FIN (seq=51, ack=102) → server ACKs (ack=52). The client (active closer here) enters TIME_WAIT for 2×MSL. Note seq/ack arithmetic: each FIN consumes a sequence number, so acks are seq+1. If you see `Flags [F.]` only and no follow-up ACK, that's a *half-open* or stuck teardown.

## 9. Internal Working
1. **Initiation**: `close(fd)` (last ref) or `shutdown(fd, SHUT_WR)` → the kernel queues a FIN, sets the seq = current send_nxt, enters FIN_WAIT_1. The FIN is a normal segment (no payload) carrying the FIN flag.
2. **Passive side**: receives FIN → ACKs it (immediately, or piggybacked on data) → enters CLOSE_WAIT, notifying the app via a read() returning 0 (EOF). The app *decides* when to finish; the connection stays half-open (receiver still can send).
3. **App closes**: passive side's `close()` → sends its own FIN → LAST_ACK → on receiving the final ACK → CLOSED.
4. **Active side**: FIN_WAIT_1 → (FIN+ACK combined) → FIN_WAIT_2. It may still receive data (the server's remaining bytes) until the server's FIN arrives. On the server's FIN → sends final ACK → TIME_WAIT.
5. **TIME_WAIT (2×MSL)**: holds the tuple. If the final ACK was lost, the passive side retransmits its FIN; the active closer re-ACKs (the tuple is still reserved, so the retransmitted FIN finds the right socket). After 2×MSL, both directions' packets are guaranteed dead → CLOSED, tuple reusable.
6. **RST path**: on errors (unsolicited data to a closed socket, protocol violation, half-open discovery), either side sends RST and discards state immediately. `SO_LINGER=0` forces close() to send RST instead of FIN (drops pending send data).
7. **TIME_WAIT economics**: every active-close creates a 60 s TIME_WAIT socket. A proxy closing 10k conn/s accumulates 600k sockets → fd/port pressure → `tcp_tw_reuse` (risky semantics change) or better, keep-alives so clients close, or `SO_REUSEADDR` for the listening port.

## 10. Time Complexity
- **Latency**: 1 RTT for the FIN+ACK (each direction), so a graceful close = ~1-2 RTT. Irrelevant for most apps; it's TIME_WAIT that matters operationally.
- **Resource cost**: TIME_WAIT sockets hold the tuple + a small struct for 2×MSL (60 s). Sustained active-close churn → hundreds of thousands of TIME_WAIT sockets (each ~200-500 B) + fd exhaustion (`ulimit -n`). This is the classic production tuning pain point.
- **Queue cost**: none extra — FINs flow through the normal send queue; the ACK is immediate.
- **RST** is O(1), instant, zero lingering.

## 11. Advantages
- **Graceful, lossless shutdown**: in-flight data is fully delivered and acknowledged before close; the peer *knows* the connection ended cleanly (EOF semantics).
- **Half-close flexibility**: one side can finish sending while still receiving — the natural fit for request/response and streaming protocols.
- **Crash-safe ordering**: TIME_WAIT guarantees no stale segment corrupts a reused tuple; the ACK-retransmit path self-heals a lost final ACK.
- **Abort is cheap**: RST provides instant, well-defined failure semantics.

## 12. Disadvantages
- **4-way handshake cost**: a full graceful close = 2 RTTs + TIME_WAIT hold — overhead for short-lived, chatty connections (hence keep-alive/pooling).
- **TIME_WAIT accumulation**: high-close-rate servers burn ports/state for 60 s → exhaustion and `tcp_tw_reuse` hacks that subtly change semantics (RFC 7323-based reuse is safe-ish, but `tcp_tw_recycle` broke NAT and was removed).
- **Half-open blind spots**: crashes leave phantom connections in CLOSE_WAIT (app forgot to close) or FIN_WAIT_2 (peer gone) that only timeouts/keepalives clean.
- **RST data loss**: an abort discards unacknowledged data by design — a "connection reset" can silently truncate a transfer (classic NFS/Big-File corruption story).
- **FIN confusion**: a peer that "half-closes" but the app keeps reading sees EOF then may misbehave if it then tries to send.

## 13. Interview Questions
1. **Q: Describe the TCP 4-way teardown.** A: Active closer sends FIN; passive side ACKs (half-close); passive side later sends its own FIN; active closer ACKs and enters TIME_WAIT (2×MSL) then CLOSED. Passive closes after its FIN is ACKed.
2. **Q (tricky): Why 4 messages to close, not 2?** A: Because each direction is an independent byte stream (full-duplex). The FIN/ACK per direction means the passive side can keep *sending* after acknowledging the active side's FIN — half-close. Two closes × two acks = 4.
3. **Q: What is a half-close and when is it useful?** A: One side finished sending (FIN) but still receives. Useful for one-shot request/response (client sends request then shutdown(SHUT_WR); server streams the response back over the same connection).
4. **Q: What is TIME_WAIT and why 2×MSL?** A: The active closer's 60 s hold after sending the final ACK. Two reasons: (a) the final ACK may be lost and the passive side will retransmit its FIN, requiring a re-ACK; (b) 2×MSL guarantees every stale segment from this connection is dead before the tuple can be reused by a new connection.
5. **Q (FAANG): Why do production servers see lots of TIME_WAIT sockets? What do you do?** A: The server is often the *active closer* (or proxies/clients close too). Mitigations: keep-alives (fewer closes), connection pooling, `SO_REUSEADDR` for rebinding the listener, `tcp_tw_reuse` (safe-ish, ties reuse to timestamps), more source ports/IPs; never `tcp_tw_recycle` (removed — broke NAT). It's usually cosmetic, not fatal, if ports suffice.
6. **Q: What is the difference between FIN and RST?** A: FIN = graceful, data flushed + acknowledged, half-close possible, 4-way + TIME_WAIT. RST = abrupt abort, discards all in-flight data, no handshake, no TIME_WAIT, immediate state teardown. "Connection reset by peer" = RST.
7. **Q (tricky): Who is the active closer?** A: The side that sends the *first* FIN. It enters TIME_WAIT. The other side is the passive closer. Whichever app calls close() first is usually the active one.
8. **Q: What states does the active closer pass through?** A: ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED. Passive: ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED.
9. **Q: What is CLOSE_WAIT and why do servers get stuck in it?** A: The passive side's state *after* acknowledging the peer's FIN but *before* the app calls close(). Stuck CLOSE_WAIT = the application never closed the fd (leak) — a top production bug (curl/grpc/legacy code). Fix the app, not the kernel.
10. **Q: What happens if the final ACK is lost?** A: The passive closer retransmits its FIN (it's in LAST_ACK, still waiting). The active closer — still in TIME_WAIT — re-ACKs. Once received, the passive side closes. This is *why* TIME_WAIT is 2×MSL (time for the retransmit+re-ACK round trip).
11. **Q (production): "Connection reset by peer" — what happened?** A: The peer sent RST — an abrupt abort: the app/OS decided to kill the connection (crash, timeout, protocol error, or explicit close after SO_LINGER=0). Unlike FIN, buffered unacknowledged data is discarded — that's why interrupted transfers show this.
12. **Q: What does SO_LINGER(0) do?** A: close() sends RST instead of FIN, dropping pending send data and skipping TIME_WAIT. Useful to force-abort stuck connections, but it breaks graceful close and can corrupt streams — used sparingly (e.g., nginx "lingering_close" and load-balancer health checks).
13. **Q (tricky): Can the FIN and ACK of the two directions combine?** A: Yes — if both sides close simultaneously (both send FIN), or if the passive side's FIN piggybacks on data/ACK. The "4-way" is the canonical minimal graceful case; implementations often collapse segments. The *logical* handshake is still two independent close+confirm pairs.
14. **Q: How does the app see a graceful close?** A: read() returns 0 (EOF) when the FIN is received. Writes after FIN → RST (and possibly SIGPIPE). A well-behaved app uses EOF to know when to finish its own close().
15. **Q (FAANG): When would you use RST deliberately?** A: Health-check probes (check if a port accepts without completing a full connection — `SO_LINGER` or TCP probing), aborting poisoned half-open connections, or when a proxy decides a connection is stuck and needs immediate cleanup. It's the "kill switch."

## 14. Follow-Up Questions
1. **Q: What is the relationship between TIME_WAIT and port exhaustion?** A: Each active close pins a (srcIP, srcPort, dstIP, dstPort) for 2×MSL. A server actively closing to many clients burns source ports/ephemeral ranges for 60 s; at high close rates, ports run out → connect failures (EADDRNOTAVAIL). That's the real-world cost of the 4-way close.
2. **Q: What is the difference between `shutdown(SHUT_WR)` and `close()`?** A: `shutdown(SHUT_WR)` sends FIN on the write half only — the socket stays open for reading (half-close). `close()` closes both directions and frees the fd (FIN on both). shutdown enables the one-shot request/response pattern and lets the *other* side see EOF while still sending.
3. **Q: How does HTTP/2 and HTTP/3 avoid teardown cost?** A: HTTP/2 multiplexes many requests over one TCP connection (few closes, keep-alive); HTTP/3 (QUIC) has connection IDs and graceful close with its own close semantics + 0-RTT restart, so churn is minimal. Both exist partly to amortize the handshake *and* teardown cost.
4. **Q (tricky): What is the "passive open" close order in a typical HTTP/1.0 exchange?** A: Client requests → server responds → server typically closes (FIN) → client ACKs → client closes (FIN) → server ACKs → client holds TIME_WAIT. The server became active closer despite being the "server," because it initiated the close. Anyone can be the active closer.
5. **Q: What is a "simultaneous close"?** A: Both sides send FIN around the same time (rare). Each ends in TIME_WAIT, and the FINs cross — the state machine handles it via the CLOSING state (both in FIN_WAIT_1, both receive FIN). Four FIN+ACK pairs still logically occur.

## 15. Coding Example
```python
# Graceful vs abrupt close in code
import socket

def server():
    srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", 9001)); srv.listen(5)
    conn, addr = srv.accept()
    print(conn.recv(1024))
    conn.shutdown(socket.SHUT_WR)   # half-close: "my reply is done", but keep reading
    # ... could still recv() if client sends more
    conn.close()                    # full close -> FIN on both sides
    srv.close()

def client():
    c = socket.socket()
    c.connect(("127.0.0.1", 9001))
    c.sendall(b"ping")
    c.shutdown(socket.SHUT_WR)      # sends FIN: "request complete, stream the answer"
    print(c.recv(1024))             # read until EOF (FIN)
    c.close()

# Force an RST close (abrupt, discards data):
c = socket.socket(); c.connect(("127.0.0.1", 9001))
c.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))  # linger,timeout=0
c.close()                           # sends RST, not FIN — instant kill
```
```bash
# Observe the 4-way close and TIME_WAIT
$ sudo tcpdump -nn -i lo tcp port 9001 -vv | grep -E 'F|R'
$ ss -tan | grep 9001
# TIME-WAIT  0      0      127.0.0.1:9001      127.0.0.1:43000
# (the active closer holds TIME-WAIT for 2*MSL)
$ cat /proc/sys/net/ipv4/tcp_fin_timeout   # 60  (≈2*MSL in practice)
```

## 16. Industry Usage
- **Proxies / L4 load balancers (Envoy, HAProxy, nginx)**: front millions of client connections; their close() policy (keep-alive, lingering close, TIME_WAIT tuning, RST health checks) is a core ops concern — TIME_WAIT exhaustion is a classic proxy outage.
- **Microservices / gRPC**: gRPC keeps connections open (HTTP/2) and uses graceful shutdown with a deadline — "connection refused/reset during rolling deploy" is the classic half-close/abort symptom teams debug.
- **Cloud & CDN edge**: Cloudflare/AWS explicitly tune `tcp_fin_timeout`, `tcp_tw_reuse`, and use `SO_REUSEADDR` so hot listeners can restart through TIME_WAIT; health checks use RST-style probes (`tcpconnect` with linger 0).
- **Databases & message queues**: Postgres/MySQL/Kafka use long-lived connections + keepalives to avoid teardown churn; a "connection reset by peer" here usually means a crash or LB timeout — the standard DBA/ops diagnosis.
- **Mobile & real-time apps**: WebSocket/SSE apps handle server-initiated closes carefully; "half-close" (client shutdown(SHUT_WR) to signal request completion) is used by HTTP/1.0-style clients and some streaming RPC designs.

## 17. References
- RFC 793 §3.5 — Connection termination & TIME_WAIT: https://www.rfc-editor.org/rfc/rfc793
- RFC 9293 — TCP (current, §3.10.3 close): https://www.rfc-editor.org/rfc/rfc9293
- RFC 6191 — Reducing TIME-WAIT via timestamps (tcp_tw_reuse rationale).
- Linux: `man tcp` (SO_LINGER, TIME_WAIT, tcp_fin_timeout); `iproute2` ss/state tables.
- Kurose & Ross, *Computer Networking*, Ch. 3 §3.5.7 (closing a connection).

## 18. Cheat Sheet
- Graceful close: FIN → ACK → (data) → FIN → ACK; 4 segments, two half-closes.
- Active closer: ESTABLISHED→FIN_WAIT_1→FIN_WAIT_2→TIME_WAIT(2×MSL)→CLOSED.
- Passive closer: ESTABLISHED→CLOSE_WAIT→LAST_ACK→CLOSED.
- FIN consumes one seq number; ack = FIN_seq + 1.
- TIME_WAIT reasons: re-ACK lost final ACK + expire stale segments before tuple reuse.
- RST: abrupt abort, drops data, no TIME_WAIT; "connection reset by peer".
- Stuck CLOSE_WAIT = app never closed the fd (leak).
- SO_LINGER(0) → close() sends RST.
- shutdown(SHUT_WR) = FIN only (half-close); close() = both directions.
- High close rate → TIME_WAIT/port exhaustion → keep-alive, SO_REUSEADDR, tcp_tw_reuse (careful), never tcp_tw_recycle.

## 19. Quiz
1. Segments in graceful close: a) 2 b) 3 c) 4 d) 1 → **c**
2. FIN means: a) abort b) no more data to send c) reset d) window → **b**
3. Active closer's last state: a) CLOSE_WAIT b) TIME_WAIT c) LISTEN d) SYN_SENT → **b**
4. Passive side after ACK of FIN: a) FIN_WAIT_1 b) CLOSE_WAIT c) LAST_ACK d) TIME_WAIT → **b**
5. TIME_WAIT duration: a) 1×MSL b) 2×MSL c) 4×MSL d) 1 RTT → **b**
6. Why TIME_WAIT? a) latency b) ACK-retransmit + stale-segment expiry c) options d) NAT → **b**
7. RST: a) graceful b) drops data c) 4 segments d) TIME_WAIT → **b**
8. Stuck CLOSE_WAIT indicates: a) NAT b) app never closed c) RST d) MSS → **b**
9. SO_LINGER(0) makes close(): a) FIN b) RST c) wait d) retry → **b**
10. Half-close is enabled by: a) shutdown(SHUT_WR) b) close() c) RST d) keepalive → **a**

## 20. Flashcards
- **Q: 4-way close?** → **A:** FIN→ACK→FIN→ACK; two independent half-closes.
- **Q: Half-close?** → **A:** one side stops sending (FIN) but keeps receiving.
- **Q: TIME_WAIT?** → **A:** active closer, 2×MSL (~60 s); re-ACK lost FIN + expire stale packets.
- **Q: Active closer states?** → **A:** FIN_WAIT_1→FIN_WAIT_2→TIME_WAIT→CLOSED.
- **Q: Passive closer states?** → **A:** CLOSE_WAIT→LAST_ACK→CLOSED.
- **Q: CLOSE_WAIT leak?** → **A:** app never called close() (fd leak).
- **Q: FIN vs RST?** → **A:** graceful/confirmed vs abrupt/drops data.
- **Q: How to avoid TIME_WAIT pileup?** → **A:** keep-alives, pooling, SO_REUSEADDR, tcp_tw_reuse (careful).

## 21. Revision
TCP closes with a 4-way handshake (FIN→ACK→FIN→ACK) because each direction closes independently (half-close); FIN consumes one seq number. Active closer: FIN_WAIT_1→FIN_WAIT_2→TIME_WAIT (2×MSL, ~60 s)→CLOSED; passive: CLOSE_WAIT→LAST_ACK→CLOSED. TIME_WAIT re-ACKs a lost final FIN and expires stale segments before tuple reuse. RST is an abrupt abort (drops data, no TIME_WAIT) — "connection reset." Stuck CLOSE_WAIT = fd leak; TIME_WAIT pileup at high close rates → keep-alives, SO_REUSEADDR, careful tcp_tw_reuse. shutdown(SHUT_WR) = FIN (half-close), close() = both directions.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Describe the 4-way teardown." | 2 How It Works / 7 Formal Definition |
| "Why 4 segments and not 2?" | 13 Q&A / 4 Why Not Another Approach |
| "What is TIME_WAIT / why 2×MSL?" | 13 Q&A / 9 Internal Working |
| "TIME_WAIT exhaustion in production?" | 13 Q&A / 10 Time Complexity |
| "What is CLOSE_WAIT / stuck in it?" | 13 Q&A / 14 Follow-Up |
| "FIN vs RST / connection reset?" | 13 Q&A / 12 Disadvantages |
| "SO_LINGER / shutdown vs close?" | 13 Q&A / 15 Coding |
| "How do proxies/LBs manage closes?" | 16 Industry Usage / 13 Q&A |
