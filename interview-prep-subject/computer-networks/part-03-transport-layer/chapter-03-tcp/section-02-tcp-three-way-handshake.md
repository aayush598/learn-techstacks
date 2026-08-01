# TCP Three-Way Handshake

> **TL;DR**: TCP establishes a connection with exactly 3 segments — client SYN, server SYN+ACK, client ACK — synchronizing both sides' **initial sequence numbers** (random 32-bit ISNs) and exchanging MSS/window-scaling/SACK options. It costs 1 RTT before any data, and is the single most-asked TCP interview topic.

## 1. Why Does This Exist?
Two processes need to agree, before exchanging data, on a set of shared, unambiguous state: *which byte numbers each side starts from* (sequence synchronization — both directions must be in sync), *how much data each side can send at once* (initial window), and *which capabilities are enabled* (MSS, window scaling, SACK, timestamps). If two sides just started blasting bytes, a lost first segment or a confused sequence number would corrupt the entire stream with no way to recover. The handshake exists to make connection state **explicit, ordered, and crash-safe**: each side confirms it can *both* send and receive, and both agree on the starting points — all before a single payload byte travels. It's also the mechanism that detects "peer exists and is listening" (SYN → RST on a closed port).

## 2. How Does It Work?
```
Client                            Server
  |                                  |
  |  SYN: seq = x (ISN_client)       |  1. Client initiates
  |--------------------------------->|
  |                                  |  2. Server accepts: picks its own ISN y,
  |  SYN+ACK: seq = y, ack = x+1     |     acknowledges client's ISN (x+1)
  |<---------------------------------|
  |                                  |  3. Client confirms: acknowledges server's
  |  ACK: seq = x+1, ack = y+1       |     ISN (y+1); now both sides are ready
  |--------------------------------->|
  |                                  |
  v       Connection ESTABLISHED     v
```
- **SYN (client → server)**: `seq = x` (random ISN), no payload, SYN flag, SYN consumes one sequence number. Client → server send path is announced.
- **SYN+ACK (server → client)**: `seq = y` (server's random ISN), `ack = x+1` ("I received your byte x [the SYN]; I expect your next byte at x+1"). Server → client path announced, client's path acknowledged.
- **ACK (client → server)**: `seq = x+1`, `ack = y+1` — client acknowledges server's ISN. After this both directions are synchronized; both sides move to ESTABLISHED.
- **State transitions**: LISTEN → SYN_RCVD (server) / SYN_SENT (client) → ESTABLISHED. SYN retransmission: if no SYN+ACK, client retries (1s, 2s, 4s, ... backoff, ~2 min).
- **The handshake carries options**: MSS, Window Scale, SACK-permitted, Timestamps — exchanged in SYN/SYN-ACK; the connection's negotiated parameters are locked in.

## 3. When Is It Used?
- **Every TCP connection**: every HTTPS page load, SSH session, database connection — the 3-way handshake happens before any data.
- **SYN flood attacks / mitigation**: the handshake's SYN → SYN+ACK → ACK flow is exactly what DDoS attackers abuse (SYN flood: send SYNs, never ACK → server exhausts SYN queue). SYN cookies counter this.
- **Service reachability testing**: `nc -vz host port`, `curl -v` — a completed handshake means the port is open; RST/ICMP-unreachable means closed.
- **TCP Fast Open (RFC 7413)**: *reduces* the handshake to 0 RTT for repeat connections (cached cookie + data piggybacked on the SYN).
- **Debugging**: tcpdump shows the 3 segments as `Flags [S]`, `[S.]`, `[.]`; an incomplete handshake (only `[S]` retransmitting) = server down or blocked.

## 4. Why Wasn't Another Approach Chosen?
- **Why 3 segments instead of 2?** A 2-way handshake (SYN, SYN+ACK) leaves the *server* unsure whether the client received the SYN+ACK — if that segment is lost, the server would start sending data to a client that isn't ready (and both would have *different* beliefs about sequence numbers). The third ACK is the client's *confirmation*, making both sides agree — the classic "two generals problem" minimum that works for connection setup. Two segments can't establish *bidirectional* agreement on *both* sequence spaces.
- **Why not 4+?** Three is provably sufficient for both parties to know their peer is alive and synchronized, while minimizing latency (1 RTT). More rounds would add delay with no benefit.
- **Why random ISNs?** A predictable ISN lets an attacker *spoof* a connection (sequence-number guessing attack, classic 1985 Morris attack). Random ISNs make off-path spoofing astronomically unlikely and prevent "old connection segments" (from a previous incarnation of the same tuple) from being accepted — the half-open connection ambiguity.
- **Why not just send data immediately?** Without synchronized seq numbers and options, the receiver can't reassemble or acknowledge correctly. The handshake *is* the synchronization step.

## 5. Intuition
It's the **"Can you hear me? — Yes, can you hear me? — Yes"** of networking. Actually it's smarter: each side announces its *starting page number* for a book they'll send, and the other side says "Got it, I'll start counting from *your* page N+1." The trick is that both announcements must be *confirmed*. If the server just said "my starting page is 500" and never heard back, it wouldn't know whether the client heard it — so a third message ("I heard your 500, and I'll send you my page 501 next") closes the loop. One direction needs a one-way confirmation, the other needs a one-way confirmation, and they overlap into exactly three messages. It's the minimal dance that gets two people to agree "we're both here, and here's where we both start."

## 6. Real-World Analogy
**Two chefs starting a relay dinner**: Chef B's kitchen is open for deliveries (LISTEN). Chef A calls (SYN): "I'm starting! My first dish is labeled #1000." Chef B answers (SYN+ACK): "Got it — your #1000 is confirmed, I'll expect #1001 next. My first dish to you is labeled #9000." Chef A replies (ACK): "Confirmed — your #9000, I expect #9001." Now *both* know: the line is open, each knows the other's numbering, and food can start flowing. If Chef A never answers the confirmation call, Chef B never starts cooking (no state, no assumption). And they don't bother choosing a secret handshake (random ISN) that a stranger could guess — that's how someone could crash a party pretending to be Chef A.

## 7. Formal Definition
The TCP three-way handshake (RFC 793 §3.4, RFC 9293) is the connection-establishment procedure in which the initiating host sends a SYN segment (`seq = ISN_c`, no payload), the responding host replies with a SYN+ACK (`seq = ISN_s, ack = ISN_c+1`), and the initiator sends an ACK (`ack = ISN_s+1`). Both ISNs are unpredictable (randomized). The handshake synchronizes sequence numbers in both directions, negotiates options (MSS, Window Scale, SACK, Timestamps, TFO), and transitions the connection from SYN_SENT/SYN_RCVD to ESTABLISHED. It costs exactly one round trip time (1 RTT) before data can flow and requires no data in the SYN segment in the standard case.

## 8. Example
A full handshake captured live:
```
$ sudo tcpdump -nn -i eth0 tcp port 443 -c 3 -v
1: 17:32:01.000000 IP 10.0.0.5.54321 > 93.184.216.34.443: Flags [S],
      seq 2918802364, win 64240, options [mss 1460,sackOK,
      TS val 1000 ecr 0,nop,wscale 7], length 0
2: 17:32:01.001200 IP 93.184.216.34.443 > 10.0.0.5.54321: Flags [S.],
      seq 4067849132, ack 2918802365, win 65535, options [mss 1460,
      sackOK,TS val 2000 ecr 1000,nop,wscale 7], length 0
3: 17:32:01.001350 IP 10.0.0.5.54321 > 93.184.216.34.443: Flags [.],
      ack 4067849133, win 514, length 0
```
Time analysis: 1 RTT = 1.2 ms (segments 1→2). Segment 3's `ack = 4067849133` = `4067849132 + 1` (SYN counts as one byte). After segment 3, both are ESTABLISHED and data flows (segment 4+). The window scale 7 negotiated means both will scale their window advertisements ×128. Note: the whole dance took ~1.35 ms before TLS even started.

## 9. Internal Working
1. **Client**: `connect()` → kernel allocates the TCP control block, picks a random ISN (RFC 6528: time + secret hash), sends SYN (with options: MSS from the route's MTU, wscale, sackOK, timestamps), enters SYN_SENT. Starts the SYN retransmission timer (initial RTO ≈ 1 s, doubling per retry).
2. **Server**: in LISTEN, receives the SYN → looks up the listening socket → allocates a request-socket in SYN_RCVD, sends SYN+ACK. Adds the entry to the *SYN queue* (half-open queue, `tcp_max_syn_backlog`).
3. **Client**: receives SYN+ACK → validates ack (== ISN_c+1), records the server's ISN, options, and RTT sample (TSecr) → sends the final ACK → ESTABLISHED.
4. **Server**: receives the ACK → moves the connection from SYN_RCVD to ESTABLISHED, from the SYN queue to the accept queue → `accept()` returns a new fd. Until the final ACK arrives, the server holds the connection in a half-open state (SYN_RCVD) with a limited timeout.
5. **SYN flood defense**: when the SYN queue overflows, the server computes a *SYN cookie* (hash of addresses/ports/ISN/time) and sends SYN+ACK without allocating any state; a legit client's ACK echoes the cookie, letting the server reconstruct the connection statelessly (Linux `net.ipv4.tcp_syncookies=1`).
6. **Retransmission**: lost SYN → retry with backoff (1s, 2s, 4s, ..., typically ~127 s total, `tcp_syn_retries`); the connect() call eventually fails with ETIMEDOUT. Lost SYN+ACK → client retries SYN.
7. **Fast Open (TFO)**: repeat clients send a TFO cookie in the SYN + initial data — the server ACKs and the first payload arrives in the same RTT as the handshake (0 RTT data for repeats).

## 10. Time Complexity
- **Latency**: exactly 1 RTT (two way-trips worth of segments, compressed: SYN + SYNACK back-to-back + ACK). On 100 ms WAN, 100 ms added before data; on 10 ms DC, 10 ms. This is *the* connection cost.
- **State**: each half-open SYN costs the server a connection control block (~1 KB) until the final ACK (or timeout). SYN flood → memory/CPU exhaustion → SYN cookies.
- **Retransmission**: exponential backoff (1,2,4,8... s) bounded by `tcp_syn_retries` (default 6 → ~127 s) — worst case connect() latency on a dead peer.
- **O(1) per connection**; handshake throughput on servers: thousands of SYN/s sustained (SYN cookies scale it beyond).

## 11. Advantages
- **Both parties confirmed**: after the handshake, each side knows the peer is alive, listening, and sequence-synchronized — *no* ambiguity about the connection's starting state.
- **Negotiation point**: options (MSS, wscale, SACK, timestamps, TFO) are agreed before data — the connection is configured correctly from byte one.
- **DoS-hardened**: random ISNs + SYN cookies defeat spoofed-SYN and sequence-guessing attacks.
- **A single, clean 1-RTT cost**: predictable startup latency; TFO/TLS 1.3 (0-RTT) remove it entirely for repeats.
- **Failure visibility**: RST on closed port, timeout on dead peer — clear diagnostics for tools like `nc`/`curl`.

## 12. Disadvantages
- **Latency tax**: 1 RTT before any data — on a 300 ms satellite link that's 300 ms added to every new connection. This is *the* motivation for HTTP keep-alive, connection pooling, TLS 1.3 0-RTT, and TFO.
- **SYN flood vulnerability**: stateless handshake means a malicious client can open half-open connections and exhaust server memory (mitigated by cookies, but a real historical attack).
- **Half-open connection ambiguity**: if the final ACK is lost, the server holds a phantom connection (SYN_RCVD) for a while and may even accept it later — edge-case cleanup is fiddly.
- **Overhead for tiny messages**: for a 1-packet request/response, the handshake is 2× the data — DNS chose UDP partly for this.

## 13. Interview Questions
1. **Q: Describe the three-way handshake.** A: Client sends SYN (seq = ISN_c), server replies SYN+ACK (seq = ISN_s, ack = ISN_c+1), client sends ACK (ack = ISN_s+1). Both sides become ESTABLISHED. 1 RTT, no data in standard SYNs.
2. **Q (tricky): Why exactly 3 messages and not 2?** A: With 2, the server couldn't be sure the client got the SYN+ACK (its sequence numbers would be unconfirmed), so it might send data to a client that never synchronized — an inconsistent, half-open belief. The third ACK is the client's confirmation, closing the loop for both directions.
3. **Q: What are ISNs and why random?** A: Initial sequence numbers — where each side's byte numbering starts. Random (RFC 6528) so an off-path attacker can't guess sequence numbers and spoof/hijack, and to prevent old segments from a recycled tuple being accepted.
4. **Q: What happens if the server port is closed?** A: The server replies with RST (connection refused); the client's connect() fails immediately with ECONNREFUSED. This is how `nc -vz` probes ports.
5. **Q: What happens if the SYN is lost?** A: The client retransmits with exponential backoff (1s, 2s, 4s...) until `tcp_syn_retries` (default 6, ~127 s), then fails with ETIMEDOUT. Same for a lost SYN+ACK.
6. **Q (FAANG): What is a SYN flood and how is it defended?** A: Attackers send many SYNs without finishing → the server's SYN queue fills with half-open connections → legit connections starve. Defense: SYN cookies (stateless SYN+ACK — the server encodes connection state in the ISN and reconstructs it from the ACK), plus `tcp_max_syn_backlog`, rate limiting.
7. **Q: What does each side know after the handshake?** A: Both know the peer is listening (alive), their own and the peer's ISNs, negotiated MSS/window scaling/SACK/timestamps, and the initial RTT — everything needed for reliable data exchange.
8. **Q (tricky): Does the SYN segment consume a sequence number?** A: Yes — SYN (and FIN) each consume one. That's why the server ACKs x+1, not x: the SYN *is* byte x. Subsequent data starts at x+1.
9. **Q: How does TCP Fast Open change the handshake?** A: A repeat client presents a cached TFO cookie in the SYN and can include data immediately; the server validates the cookie and responds, achieving 0-RTT data (data sent in the same trip as the SYN). RFC 7413.
10. **Q (production): You see only `[S]` retransmissions in tcpdump. What's wrong?** A: The client can't reach the server or get a response — server down, firewall dropping (SYN+ACK never returns), routing/security-group issue, or a blackhole. No SYN+ACK in N retries = connectivity problem, not an app problem.
11. **Q: What is a half-open connection?** A: One side believes the connection exists (SYN_RCVD or ESTABLISHED) while the other doesn't — e.g., final ACK lost, or a crash after the handshake. TCP cleans these via timeouts, RST, or TCP keepalive.
12. **Q (tricky): Why is the handshake "1 RTT" if it's 3 segments?** A: Because segment 2 (SYN+ACK) travels *back* along the same path as segment 1, and segment 3 (ACK) travels *forward* — the three segments span two one-way trips = one round trip. Data can't start until the client's ACK leaves, so the cost is 1 RTT.
13. **Q: What does the handshake negotiate?** A: MSS (segment size), Window Scale (flow-control window multiplier), SACK-permitted, Timestamps (RTTM/PAWS), and TFO cookie — agreed bidirectionally before any data.
14. **Q (FAANG): How would you reduce connection latency for a chat service?** A: Keep-alive/connection pooling (no per-request handshake), TLS 1.3 0-RTT for idempotent requests, TCP Fast Open, and moving to HTTP/3/QUIC (0-RTT handshake built-in). Each removes an RTT of startup.
15. **Q: What is `tcp_max_syn_backlog`?** A: The server's SYN-queue capacity — the number of half-open connections it will remember before the SYN cookie mechanism kicks in. Raising it helps under SYN floods, but the real defense is syncookies.
16. **Q (tricky): Can two hosts start a connection simultaneously (simultaneous open)?** A: Yes — each sends SYN, each replies SYN+ACK, each ACKs. It's handled by the RFC 793 FSM, but in practice it's astronomically rare (both must call connect() at the same moment).

## 14. Follow-Up Questions
1. **Q: What is the relationship between the handshake and TLS?** A: TLS runs *after* TCP — a full HTTPS connection = TCP handshake (1 RTT) + TLS handshake (1-2 RTTs) = 2-3 RTTs total. TLS 1.3 (1 RTT, or 0-RTT with session resumption) and QUIC (TLS inside the handshake, 1 RTT total) attack exactly this compounding cost.
2. **Q: How do SYN cookies actually work?** A: When the SYN queue is full, the server replies to each SYN with a SYN+ACK whose *ISN* is a MAC of (srcIP, srcPort, dstIP, dstPort, secret, timestamp-bucket). A legit client echoes it back (ack = cookie+1); the server recomputes the MAC and, if valid + fresh, reconstructs the connection with *zero* stored state. Stateless DoS mitigation.
3. **Q: What is the difference between the SYN queue and the accept queue?** A: SYN queue = half-open connections awaiting the final ACK (bounded by `tcp_max_syn_backlog`). Accept queue = ESTABLISHED connections awaiting `accept()` (bounded by listen() backlog). Queue overflow shows as drops/congestion in `ss`/`netstat`.
4. **Q: When would you disable SYN cookies?** A: They prevent some TCP options from being fully negotiated on the *very first* SYN+ACK (cookie encodes less). In practice leave them on (`net.ipv4.tcp_syncookies=1`); scaling the backlog + vertical scaling handles most legitimate load.
5. **Q (tricky): Why does the client ACK in step 3 carry a sequence number?** A: Every TCP segment carries a seq (this one = x+1, since the client consumed byte x on the SYN). It carries no new data, so it just reflects where the client's byte stream is; it doesn't advance anything.

## 15. Coding Example
```python
# A handshake, in code — connect() does all 3 segments for you
import socket

# Server
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 9999)); srv.listen(5)
conn, addr = srv.accept()          # <-- handshake complete; conn is ESTABLISHED
conn.sendall(b"handshake done\n")
conn.close()

# Client — the SYN/SYNACK/ACK happen inside connect()
c = socket.socket()
c.settimeout(2.0)
c.connect(("127.0.0.1", 9999))     # <-- returns only after the final ACK is sent
print(c.recv(128))

# Probing reachability without an app: the handshake IS the test
#   $ nc -vz 93.184.216.34 443        # SYN -> SYN+ACK -> ACK == open
#   $ nc -vz 93.184.216.34 81         # RST == closed
```
```bash
# Verify the handshake bytes with tcpdump (3 segments, 2 flags)
$ sudo tcpdump -nn -i lo tcp port 9999 -vv
#  [S]  seq 2918802364            (1. client SYN)
#  [S.] seq 4067849132, ack 2918802365   (2. server SYN+ACK)
#  [.]  ack 4067849133            (3. client ACK -> ESTABLISHED)
```

## 16. Industry Usage
- **Every L4 load balancer / proxy (nginx, HAProxy, Envoy)**: they *front* the handshake for millions of clients, terminate TCP, and open fresh backend connections — handshake handling is their core CPU/buffer cost, and they implement SYN-cookie-style protection at the edge.
- **Cloud CDNs & origins**: Cloudflare/AWS offload and optimize the handshake (TFO, 0-RTT, tunable backlogs) because connection setup is a measurable % of page-load time.
- **DDoS protection (Cloudflare, AWS Shield, Akamai)**: SYN-flood mitigation at the edge — edge nodes absorb SYNs, reply with cookies/CHALLENGE, only forward proven clients. The handshake is the weapon and the defense.
- **Mobile/embedded stacks**: the 1-RTT cost is why mobile apps use connection pooling, keep-alives, and HTTP/2 multiplexing — one handshake per connection is expensive on 100+ ms cellular RTTs.
- **Datacenter fabric**: even at 10 μs RTT, handshake cost × connection churn (microservices, gRPC) motivated gRPC's connection reuse and HTTP/2's connection multiplexing.

## 17. References
- RFC 793 §3.4 — Connection establishment: https://www.rfc-editor.org/rfc/rfc793
- RFC 9293 — TCP (current, §3.10.1 handshake): https://www.rfc-editor.org/rfc/rfc9293
- RFC 6528 — ISN randomization: https://www.rfc-editor.org/rfc/rfc6528
- RFC 7413 — TCP Fast Open: https://www.rfc-editor.org/rfc/rfc7413
- Bernstein, "SYN cookies": https://cr.yp.to/syncookies.html
- Kurose & Ross, *Computer Networking*, Ch. 3 §3.5.6.

## 18. Cheat Sheet
- Handshake: SYN(seq=x) → SYN+ACK(seq=y, ack=x+1) → ACK(ack=y+1). 1 RTT, then ESTABLISHED.
- ISNs random (RFC 6528); SYN/FIN consume one seq number.
- Options negotiated: MSS, wscale, sackOK, timestamps, TFO.
- Lost SYN/SYN+ACK → exponential backoff retry (1,2,4,...s, ~127 s max).
- Closed port → RST (ECONNREFUSED); filtered → timeout (ETIMEDOUT).
- SYN flood → fill SYN queue → SYN cookies (stateless) defend.
- Backlogs: SYN queue (`tcp_max_syn_backlog`) vs accept queue (listen()).
- tcpdump flags: `[S]`=SYN, `[S.]`=SYN+ACK, `[.]`=ACK.
- TFO: 0-RTT for repeat clients. TLS 1.3: another RTT after this.
- `nc -vz host port` = handshake-based port probe.

## 19. Quiz
1. How many segments in the handshake? a) 2 b) 3 c) 4 d) 1 → **b**
2. Client's SYN carries: a) ack number b) seq = ISN_c c) data d) window → **b**
3. Server's SYN+ACK ack value: a) ISN_c b) ISN_c+1 c) ISN_s d) 0 → **b**
4. Why 3 messages, not 2? a) TLS needs it b) confirm both directions/seq sync c) options d) latency → **b**
5. ISNs should be: a) 0 b) predictable c) random d) the port number → **c**
6. Cost of the handshake: a) 2 RTT b) 1 RTT c) 0 RTT d) 3 RTT → **b**
7. Closed port response: a) SYN+ACK b) RST c) nothing d) FIN → **b**
8. SYN flood defense: a) raise MSS b) SYN cookies c) window scaling d) FIN → **b**
9. SYN consumes how many seq numbers? a) 0 b) 1 c) 2 d) half → **b**
10. TFO enables: a) bigger windows b) 0-RTT data for repeats c) SACK d) pacing → **b**

## 20. Flashcards
- **Q: 3-way handshake messages?** → **A:** SYN(seq=x), SYN+ACK(seq=y,ack=x+1), ACK(ack=y+1).
- **Q: Why 3, not 2?** → **A:** server needs client confirmation; both seq spaces synchronized.
- **Q: ISN?** → **A:** random initial seq (RFC 6528) — anti-spoofing.
- **Q: Cost?** → **A:** 1 RTT before data.
- **Q: Closed port?** → **A:** RST → ECONNREFUSED.
- **Q: SYN flood defense?** → **A:** SYN cookies (stateless).
- **Q: What consumes a seq without data?** → **A:** SYN and FIN.
- **Q: tcpdump flags?** → **A:** `[S]` SYN, `[S.]` SYN+ACK, `[.]` ACK.

## 21. Revision
TCP connects via 3 segments: SYN (seq=ISN_c) → SYN+ACK (seq=ISN_s, ack=ISN_c+1) → ACK (ack=ISN_s+1), costing 1 RTT and negotiating MSS/wscale/SACK/timestamps/TFO. ISNs are random (anti-spoofing); SYN consumes one seq number. Lost SYNs retry with exponential backoff; closed ports RST (refused), filtered ports time out. SYN floods exhaust the SYN queue → SYN cookies (stateless handshake) defend. TFO gives repeat clients 0-RTT data. Debug with tcpdump (`[S]`/`[S.]`/`[.]`) and `nc -vz`.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Describe the three-way handshake." | 2 How It Works / 7 Formal Definition |
| "Why 3 segments and not 2?" | 13 Q&A / 4 Why Not Another Approach |
| "Why random ISNs?" | 13 Q&A / 6 Real-World Analogy |
| "What is a SYN flood / SYN cookies?" | 13 Q&A / 9 Internal Working |
| "Cost of the handshake / how to reduce it?" | 13 Q&A / 10 Time Complexity |
| "Half-open connections?" | 13 Q&A / 14 Follow-Up |
| "What does the handshake negotiate?" | 13 Q&A / 8 Example |
| "Debug: only [S] retransmissions?" | 13 Q&A / 15 Coding |
