# TCP State Machine, Nagle, and Friends

> **TL;DR**: TCP is a 11-state finite state machine (LISTEN→SYN_SENT/SYN_RCVD→ESTABLISHED→FIN_WAIT/TIME_WAIT/CLOSE_WAIT/LAST_ACK→CLOSED), and on top of it sit the little algorithms engineers love to ask about: **Nagle** (coalesce tiny writes), **delayed ACK** (batch acknowledgments), **keepalive** (detect dead peers), **persist** (survive zero-window), and **timestamps/TFO** (0-RTT + precise RTT).

## 1. Why Does This Exist?
TCP's correctness depends on each side tracking *exactly* which state it's in — a connection is an agreement, and the agreement must be ordered and recoverable. The **finite state machine (FSM)** is the formal contract of that agreement: every transition is a specific (event → state) pair (send SYN, receive FIN, timeout...), which is what lets a kernel handle thousands of connections without ambiguity, and lets us debug exactly what went wrong from a single `ss` state. The *ancillary algorithms* solve real-world efficiency and reliability problems the core protocol left open: **Nagle** stops the "tiny packet problem" (many small writes → 41-byte packets saturating a link with headers), **delayed ACK** reduces ACK traffic and improves throughput, **keepalive** surfaces silent dead peers (crashed hosts, closed laptops), and **persist** keeps zero-window connections alive through probes. Understanding the FSM + these algorithms is the difference between "knowing TCP" and *operating* TCP.

## 2. How Does It Work?
**The 11 states (RFC 9293)**: `CLOSED`, `LISTEN`, `SYN_SENT`, `SYN_RCVD`, `ESTABLISHED`, `FIN_WAIT_1`, `FIN_WAIT_2`, `CLOSE_WAIT`, `CLOSING`, `LAST_ACK`, `TIME_WAIT`. Transitions are driven by sends, receives, and timeouts (the diagram every interview question re-derives).
- **Nagle** (RFC 896): if there's unacknowledged data in flight, a new small write is *buffered* until (a) the ACK for the previous data arrives, or (b) the buffer reaches a full segment (MSS). Net effect: at most one small segment in flight. Disabled with `TCP_NODELAY`.
- **Delayed ACK** (RFC 1122): the receiver delays its ACK up to 200-500 ms, waiting to piggyback it on outgoing data, or to ACK a burst at once. Linux `tcp_delack_min=40 ms` (up to 500 ms).
- **Keepalive** (RFC 1122): if idle for `tcp_keepalive_time` (7200 s), send 1-byte probes every `tcp_keepalive_intvl` (75 s); after `tcp_keepalive_probes` (9) unanswered → connection dead → close + error. Can't detect a *half-open* (peer rebooted) reliably without it.
- **Persist timer** (RFC 793): while rwnd=0, send 1-byte *window probes* every `tcp_keepalive...` no — every ~5-60 s (backoff) to verify the receiver's window reopened (a lost window-update ACK would otherwise deadlock the connection).
- **Timestamps + TFO**: timestamps (RFC 7323) give precise RTT + PAWS; TCP Fast Open (RFC 7413) lets repeat clients send data with the SYN (0-RTT).
- **ECN / CWR flags**: ECN marks congestion without drops (see congestion control section).
- **SYN cookies**: stateless SYN defense (see handshake section).

## 3. When Is It Used?
- **Diagnosing states**: `ss -tan` / `netstat -an` — every state is a fingerprint: `SYN_RCVD` = half-open attack or server overload; `CLOSE_WAIT` = app leak; `FIN_WAIT_2` = peer gone; `TIME_WAIT` = normal, churn at scale.
- **Latency debugging**: "40 ms per request" is the *delayed ACK × Nagle* interaction (HTTP/1.0 + small requests + no TCP_NODELAY); "tty_talk" lag and SSH interactivity are Nagle symptoms → `TCP_NODELAY`.
- **Keepalive in infra**: load balancers, proxies, and databases set `tcp_keepalive_time` (60-300 s) so dead backends are evicted fast; the default 2 hours is useless for automated health.
- **TFO/0-RTT**: repeat connections to CDNs/APIs (fast TLS-free bootstrap) — where handshake RTTs are the dominant cost.
- **Persist probes**: long idle zero-window flows (a slow consumer) — the probes keep them alive instead of silently dying.
- **WAN acceleration**: Nagle + delayed-ACK tuning is the bread-and-butter of HTTP/2 and QUIC's connection pooling.

## 4. Why Wasn't Another Approach Chosen?
- **Why an FSM at all?** Every protocol needs *state agreement*; an explicit FSM with enumerated states and transitions is the only way to make connection handling deterministic, testable, and debuggable (each state = a concrete kernel struct + timer). A looser design ("just check flags") can't handle simultaneous events or recover from crashes.
- **Why Nagle when `TCP_NODELAY` exists?** Because most applications *don't* need interactive immediacy — they need throughput, and the tiny-packet problem is real: 100 × 1-byte writes = 100 × 41 bytes of header overhead. Nagle's default-on coalescing trades latency for efficiency; the app opts *out* only when it knows better (interactive, RPCs).
- **Why delayed ACK instead of ACKing every segment?** Fewer ACKs = less reverse traffic + piggybacking efficiency, and ACKs are redundant (cumulative). 500 ms ceiling bounds the added latency. The cost (Nagle interaction) is managed by coalescing.
- **Why keepalive probes at all (vs just timeouts)?** Timeouts can't distinguish "peer is quiet but alive" from "peer died." Keepalive actively *probes* to make silence meaningful — a finite-state, explicit liveness check. TCP can't rely on app-level heartbeats (they don't exist for most protocols).
- **Why timestamps over a sequence-based approach?** Unambiguous RTT samples + PAWS in one option; TFO's cookie-based 0-RTT exists because the 1-RTT handshake is provably needed for *new* connections but wasteful for repeats — a cookie replaces the re-handshake.

## 5. Intuition
The FSM is the **relationship status tracker**: "off the market (LISTEN), asking them out (SYN_SENT), they said yes but I haven't confirmed (SYN_RCVD), we're dating (ESTABLISHED), I said goodbye (FIN_WAIT_1), waiting for their goodbye (FIN_WAIT_2), they said goodbye and I'm lingering so I can catch any last words (TIME_WAIT), they said goodbye but won't leave my side (CLOSE_WAIT)." Every date (connection) is exactly one of these statuses at any instant — that's how the OS tracks thousands without mixing them up. The algorithms are **etiquette rules**: Nagle = "don't send a word at a time over a telegram when a full letter is coming anyway; wait, batch it" (except in an emergency — TCP_NODELAY); delayed ACK = "don't reply to every single text instantly; wait a moment in case they say more" — until it's polite to answer; keepalive = "if someone's been silent for two hours, send a 'you still there?' poke" to find out if they died; persist = "if they said 'I'm full, don't send,' keep gently knocking until they say 'room freed up.'"

## 6. Real-World Analogy
**Radio operators on a naval fleet**: Each radio is a connection with an explicit state (silent / handshake in progress / talking / saying goodbye / lingering to catch last transmissions). Every transmission changes state in a defined way, and every operator's console shows the exact same state table — that's how a fleet of thousands coordinates without confusion (the FSM). Now the traffic rules: the *Nagle* rule says "if you're mid-transmission and I type a short message, wait until my current burst is acknowledged, then send the whole batch" — otherwise a fleet sending 1-char signals would drown the channel in overhead. The *delayed ACK* rule says the receiving operator confirms messages in batches a half-second later, not each one individually — saving channel time (until the sender gets twitchy). The *keepalive* rule: the commander pings a silent ship every so often — if no answer, they mark it lost (dead peer), rather than waiting forever. And if a ship reports "my cargo deck is full," the sender knocks gently at intervals to know when it's cleared (persist).

## 7. Formal Definition
TCP state machine (RFC 9293 §3.2): states {CLOSED, LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, LAST_ACK, TIME_WAIT}, with transitions defined by (send X / receive Y / timeout Z). Established side paths: connect→SYN_SENT→ESTABLISHED; accept→SYN_RCVD→ESTABLISHED; close→FIN_WAIT_1→FIN_WAIT_2→(recv FIN)→TIME_WAIT→(2MSL)→CLOSED; passive: (recv FIN)→CLOSE_WAIT→(send FIN)→LAST_ACK→(recv ACK)→CLOSED; simultaneous close: FIN_WAIT_1→CLOSING→TIME_WAIT. Nagle (RFC 896): allow at most one small outstanding segment; coalesce subsequent small writes until ACK/MSS. Delayed ACK (RFC 1122): ACK within ≤500 ms. Keepalive (RFC 1122 §4.2.3.6): probes after idle time, intvl, N probes; on failure close. Persist (RFC 793): 1-byte window probes during zero window. TFO (RFC 7413): cookie-authenticated data-with-SYN.

## 8. Example
A complete lifecycle, states annotated (`ss -tan` output is basically this):
```
1. Client connect():              client: SYN_SENT → ESTABLISHED
2. Server accept():               server: LISTEN → SYN_RCVD → ESTABLISHED
3. Data flows for 300 s            (both ESTABLISHED)
4. Client closes (active):         client: FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT
   Server gets FIN (passive):      server: CLOSE_WAIT → LAST_ACK → CLOSED
5. After 2×MSL:                    client: CLOSED

$ ss -tan | grep 9000
# LISTEN    0 128  0.0.0.0:9000                 (waiting for connections)
# ESTAB     0 0    10.0.0.5:9000 192.168.1.10:50000   (dating)
# TIME-WAIT 0 0    10.0.0.5:9000 192.168.1.10:50001   (lingering after close)
```
Every one of those lines is a state; `ss` just reads the FSM. If a connection is stuck in CLOSE_WAIT, it means the app received FIN but never closed (fd leak) — the FSM *tells you where the bug is*.

## 9. Internal Working
1. **FSM implementation**: each connection's control block stores `state`; every received segment and user API call runs through a transition table (accept/reject per state). Invalid transitions (e.g., data in SYN_RCVD without handshake) are dropped or trigger RST.
2. **Nagle**: on send, if `SND.NXT - SND.UNA > 0` (unacked data in flight) and the pending write < MSS → buffer it. The buffered data flushes when the ACK arrives or a full MSS accumulates. `TCP_NODELAY` sets a flag to skip coalescing (send immediately).
3. **Delayed ACK**: on receiving data, start `tcp_delack_min` timer (40 ms Linux); send the ACK when (a) timer fires, (b) a full segment worth of data is pending, or (c) outgoing data piggybacks an ACK. Half-open edge: keepalive fills the gap for dead peers.
4. **Keepalive**: only after `tcp_keepalive_time` (default 7200 s) of *no traffic* does the timer arm; then 1-byte probes (seq = last ack - 1, so the peer must reply with a DUPACK/ACK) every `intvl`, up to `probes`; on failure, the socket errors (ETIMEDOUT/ECONNRESET). Configurable per-socket via `SO_KEEPALIVE` + `TCP_KEEPIDLE/KEEPINTVL/KEEPCNT`.
5. **Persist**: when rwnd=0 and sendable data pending, the persist timer fires window probes (1-byte, oldest unacked) with exponential backoff (5,10,20...60 s), stopping only on a nonzero-window ACK — preventing deadlock from a lost window update.
6. **Timestamps**: TSval = sender clock, echoed TSecr in the ACK → the RTT sample (see reliability); also PAWS: reject segments whose TSval is older than the newest seen → wrapped-seq protection.
7. **TFO**: client stores the server's cookie from a prior connection; a new SYN carries the cookie + initial data; the server validates (stateless) and streams data without waiting for the ACK — 0 RTT for repeats, 1 RTT for first contact.
8. **Half-open / half-closed**: a peer that rebooted leaves the other side in ESTABLISHED (half-open) — only keepalive or a send-triggered RTO/RST exposes it. Half-closed = one direction FINed (legit half-close).

## 10. Time Complexity
- **FSM per-segment**: O(1) — one state read + transition lookup. The kernel's per-connection state is ~1 KB; a million connections = ~1 GB of control blocks.
- **Nagle/delayed-ACK cost**: bounded delay ≤ 500 ms per ACK; with Nagle the *worst* latency for a small request ≈ delayed-ACK time + RTT (the 40 ms "Nagle×delayedACK" tax — fixed by TCP_NODELAY or by HTTP/2 batching).
- **Keepalive cost**: zero traffic normally; 1-byte probe every 75 s only on idle dead connections. The *detection* latency (2 h + 9×75 s) is why infra overrides defaults.
- **Persist**: probes every 5-60 s while rwnd=0 — negligible bandwidth, but keeps zero-window flows alive indefinitely.
- **TFO**: saves a full RTT per repeat connection — at scale (CDNs) that's the difference between 20 ms and 40 ms page latency.
- **TIME_WAIT churn**: 60 s of tuple hold per active close — the state-machine cost that shows up in ops (see teardown section).

## 11. Advantages
- **Deterministic, debuggable correctness**: the FSM makes every connection's status explicit — `ss`/`netstat` turn "what's wrong?" into a single state name (CLOSE_WAIT = leak, SYN_RCVD = attack/backlog).
- **Efficiency defaults**: Nagle + delayed ACK cut packet count and ACK traffic dramatically on typical workloads — free wins for the 95% of apps that write chunky data.
- **Liveness without app help**: keepalive/persist handle dead peers and zero-window flows automatically — the app doesn't need heartbeats for the socket to fail cleanly.
- **Optional, negotiated power-ups**: timestamps/TFO/window-scaling are options — old stacks interoperate, new stacks go fast.
- **Kernel-mature**: every algorithm is decades-tuned; defaults are sensible on most links.

## 12. Disadvantages
- **Latency traps**: Nagle × delayed ACK interaction adds up to ~40-500 ms to small interactive requests (the classic "why is my RPC slow?"); apps must know to set TCP_NODELAY.
- **Keepalive defaults are useless**: 2-hour idle threshold means dead peers linger half-open for hours unless infra tunes it — automated health depends on *changing* the default.
- **FSM edge cases**: half-open connections, simultaneous close, and lost final ACKs produce states apps don't expect; misreading states causes wasted debugging time.
- **Buffer/latency coupling**: delayed ACK + Nagle interact badly with bufferbloat (extra queueing latency); turning off Nagle trades throughput for latency.
- **TFO deployment friction**: middleboxes historically blocked SYN-with-data; TFO's 0-RTT data is limited to small payloads (up to ~1440 B) and cookie management adds state.
- **Not a silver bullet**: keepalive can't detect a *peer reboot* fast, and no TCP setting fixes an app that never reads (zero-window forever).

## 13. Interview Questions
1. **Q: List the TCP states.** A: CLOSED, LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, CLOSE_WAIT, CLOSING, LAST_ACK, TIME_WAIT.
2. **Q (tricky): Trace the active-close states.** A: ESTABLISHED → FIN_WAIT_1 (sent FIN) → FIN_WAIT_2 (got ACK) → TIME_WAIT (got peer's FIN) → CLOSED (after 2×MSL).
3. **Q: Trace the passive-close states.** A: ESTABLISHED → CLOSE_WAIT (got FIN, app must close) → LAST_ACK (sent own FIN) → CLOSED (got final ACK).
4. **Q: What is Nagle's algorithm?** A: Coalesce small writes while unacknowledged data is in flight — at most one small segment outstanding — sending the batch when the ACK arrives or a full MSS accumulates. RFC 896. Disable with `TCP_NODELAY` when interactive latency matters.
5. **Q (FAANG): When would you disable Nagle (TCP_NODELAY)?** A: Interactive/RPC workloads where a single small request's latency matters more than bandwidth (SSH, gaming, chat, API calls); when delayed ACK × Nagle adds 40 ms+ per round trip. Disable when you have few, small, latency-sensitive messages.
6. **Q: What is delayed ACK and why does it exist?** A: The receiver delays ACKs up to 500 ms (Linux ~40 ms) to piggyback them on outgoing data or ACK a burst at once — fewer ACKs, less reverse traffic, better throughput. RFC 1122.
7. **Q (tricky): What's the Nagle × delayed ACK interaction?** A: Nagle holds the small write waiting for an ACK; delayed ACK holds the ACK waiting for a small write → each waits for the other → up to ~40-500 ms per round trip. The classic 40 ms latency bug on request/response protocols without TCP_NODELAY.
8. **Q: What does TCP keepalive do?** A: After `keepalive_time` of idle (default 7200 s), sends 1-byte probes every `intvl` (75 s); after `probes` (9) unanswered → connection considered dead, closed with error. Detects crashed/unreachable peers the app would otherwise wait on forever.
9. **Q (production): Your LB sees dead backends linger for 2 hours. What's wrong?** A: Default keepalive = 7200 s idle before *any* probe. Set per-socket `SO_KEEPALIVE` + `TCP_KEEPIDLE`/`KEEPINTVL`/`KEEPCNT` (or 60-300 s idle) so dead peers are evicted in seconds — infra always overrides the kernel default.
10. **Q: What is the persist timer?** A: The timer that, while rwnd=0, sends 1-byte *window probes* with backoff (5-60 s) to learn when the receiver's window reopened — preventing deadlock if the "window update" ACK was lost.
11. **Q (tricky): What is a half-open connection and how is it detected?** A: One side ESTABLISHED, the other gone (crash/reboot without FIN). Detection: the surviving side's *send* triggers RTO → retransmit → RST or timeout; keepalive eventually fires; there's no *instant* detection without app-level heartbeats.
12. **Q: What is TCP Fast Open and when does it help?** A: A cookie-authenticated SYN that can carry data (RFC 7413) — repeat connections get 0-RTT data (vs 1 RTT). Big win for CDNs/APIs with many repeat requests; first connection still costs a full handshake.
13. **Q (FAANG): `ss -tan` shows many CLOSE_WAIT sockets. Diagnosis?** A: The app received FIN but never called close() — an fd leak or a bug (e.g., a loop that reads EOF but doesn't close). NOT a network problem: the app must close; the kernel can't. Top "production bug" fingerprint.
14. **Q: What is the CLOSING state?** A: Both sides sent FIN simultaneously and each got the other's FIN before its own FIN was ACKed — FIN_WAIT_1 → CLOSING → TIME_WAIT. Rare (simultaneous close) but the FSM covers it.
15. **Q (production): What does SYN_RCVD in bulk indicate?** A: Many half-open connections awaiting the final ACK — a SYN flood (or a client that can't complete). Check `tcp_max_syn_backlog`, syncookies, and the actual connection pattern.
16. **Q: What is the difference between `TCP_NODELAY` and `TCP_CORK`?** A: NODELAY disables Nagle (send small writes immediately); CORK buffers until uncorked/MSS (aggressive batching, often via `sendfile`). NODELAY = low latency, CORK = max batching; both manage the same coalescing trade-off.
17. **Q (tricky): Can Nagle cause a deadlock?** A: Not by itself — delayed ACK + Nagle adds latency, not deadlock (the receiver's delayed ACK *does* eventually fire; keepalive/probes cover the pathological zero-window case). The classic "deadlock" story is delayed-ACK-waiting-for-data when the app never sends more — bounded by the delayed-ACK timeout.

## 14. Follow-Up Questions
1. **Q: How do HTTP/2 and QUIC avoid Nagle/delayed-ACK issues?** A: HTTP/2 multiplexes many requests over one connection (large, batched writes — Nagle never triggers) and both use TCP_NODELAY-style settings; QUIC reimplements the whole thing in user space (its own pacing/ACK batching) so it can batch *per-stream* without the global Nagle trap.
2. **Q: When is the default 2-hour keepalive actually fine?** A: For long-lived, app-heartbeated protocols (databases, Kafka consumers that already ping) — the kernel keepalive is a backstop, not the primary liveness signal. It's the *absence* of app heartbeats that makes tuning it essential (raw sockets, legacy TCP clients).
3. **Q (tricky): What's the relationship between keepalive, half-open, and dead-peer detection?** A: Keepalive is the *only* automatic detector of a half-open (peer rebooted) connection — FIN/RST never come. Its 2-hour default is why production infra shrinks it; RTO-on-send is the *other* path, but only fires if the app actually sends.
4. **Q: How do load balancers combine these algorithms?** A: They set TCP_NODELAY + tuned keepalive on both sides, enable TFO, and use delayed-ACK-friendly buffer sizes; they also *terminate* TCP (short-lived, batched) vs *pass-through* (Nagle runs on both legs) — the "keep connections at 40 ms" tuning playbook.
5. **Q (FAANG): Design a health check that detects a hung but alive peer.** A: Not keepalive alone — it only detects *dead* peers. Combine TCP keepalive (fast idle, 30 s) with app-level heartbeat/health RPC and a watchdog: keepalive catches death, heartbeat catches *hung* (alive but not responding), watchdog closes on both.

## 15. Coding Example
```python
# The algorithms you actually set on a socket
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)      # enable keepalive
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)    # idle 30 s before probing
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)   # probe every 10 s
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)      # 3 missed -> dead
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)      # disable Nagle (low latency)

# With Nagle ON, this 3-write burst may be coalesced/delayed by an RTT:
s.sendall(b"H")
s.sendall(b"e")
s.sendall(b"llo")            # with NODELAY: 3 small segments, ~1 RTT each, 0 extra wait

# TFO hint (Linux): the OS can use TFO if both sides support it
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_FASTOPEN_CONNECT, 1)
```
```bash
# Read the state machine + algorithm state on a live box
$ ss -tan state established '( sport = :80 or sport = :443 )'   # states filter
$ ss -tin | grep -E 'cwnd|rtt|rto'      # live cwnd/rtt/rto
$ cat /proc/sys/net/ipv4/tcp_keepalive_time      # 7200
$ cat /proc/sys/net/ipv4/tcp_keepalive_intvl     # 75
$ cat /proc/sys/net/ipv4/tcp_keepalive_probes    # 9
$ sysctl net.ipv4.tcp_sack net.ipv4.tcp_timestamps   # reliability features
```

## 16. Industry Usage
- **Every proxy/LB (nginx, Envoy, HAProxy, AWS ALB)**: TCP_NODELAY + tuned keepalive + TFO are standard config; their health checks are exactly "keepalive-speed dead-peer detection" with an app-level probe.
- **Databases & cache (Postgres, MySQL, Redis, Kafka)**: keepalive tuned to 60-300 s so failed replicas/leaders are evicted fast; Nagle typically disabled for latency-sensitive queries (Redis famously uses TCP_NODELAY).
- **CDNs & edge (Cloudflare, Akamai, Google)**: TFO + 0-RTT are core page-latency levers (40 ms saves on repeat visits); Nagle/delayed-ACK interplay is a documented part of their edge tuning.
- **Mobile & IoT stacks**: keepalive tuning on cellular (radio is the bottleneck, probe costs RRC state) and Nagle-off for interactive apps; battery-vs-liveness trade-offs are real engineering.
- **Gaming/netcode**: TCP_NODELAY always, keepalive tuned low — every ms counts; the "40 ms Nagle tax" is a known netcode pitfall (many games ship raw UDP for this reason).
- **Monitoring/SRE practice**: `ss -tan` state distributions (CLOSE_WAIT spikes, SYN_RCVD floods, TIME_WAIT churn) are standard golden signals in every NOC.

## 17. References
- RFC 9293 §3.2 — TCP state machine: https://www.rfc-editor.org/rfc/rfc9293
- RFC 896 — Nagle: https://www.rfc-editor.org/rfc/rfc896
- RFC 1122 §4.2.3 — host requirements (delayed ACK, keepalive): https://www.rfc-editor.org/rfc/rfc1122
- RFC 7413 — TCP Fast Open: https://www.rfc-editor.org/rfc/rfc7413
- RFC 7323 — timestamps/PAWS/window scale: https://www.rfc-editor.org/rfc/rfc7323
- Linux: `man tcp` (TCP_NODELAY, TCP_KEEPIDLE, TCP_FASTOPEN_CONNECT), `Documentation/networking/ip-sysctl.rst`.
- Stevens, *TCP/IP Illustrated Vol. 1*, Ch. 13 (Nagle), Ch. 17 (keepalive), Ch. 18 (FSM).

## 18. Cheat Sheet
- 11 states: CLOSED, LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT_1/2, CLOSE_WAIT, CLOSING, LAST_ACK, TIME_WAIT.
- Active close: FIN_WAIT_1→FIN_WAIT_2→TIME_WAIT(2×MSL)→CLOSED. Passive: CLOSE_WAIT→LAST_ACK→CLOSED.
- Nagle: ≤1 small segment in flight; flush on ACK/MSS. NODELAY disables.
- Delayed ACK: ≤500 ms (Linux 40 ms); batches/piggybacks.
- Nagle × delayed ACK = up to 40-500 ms latency per RTT (fix: TCP_NODELAY).
- Keepalive: idle 7200 s → 1-byte probes every 75 s ×9; tune for infra (30-300 s).
- Persist: 1-byte window probes (5-60 s backoff) while rwnd=0.
- TFO: cookie + data in SYN → 0-RTT repeats.
- Half-open: peer rebooted; only keepalive/send-RTO detects.
- CLOSE_WAIT pileup = app never closed (fd leak). SYN_RCVD pileup = flood.

## 19. Quiz
1. Number of TCP states: a) 7 b) 9 c) 11 d) 13 → **c**
2. Passive closer's state after receiving FIN: a) FIN_WAIT_1 b) CLOSE_WAIT c) LAST_ACK d) TIME_WAIT → **b**
3. Nagle limits: a) window b) small segments in flight c) cwnd d) ACKs → **b**
4. Disable Nagle with: a) SO_REUSEADDR b) TCP_NODELAY c) TCP_KEEPALIVE d) SO_LINGER → **b**
5. Delayed ACK max delay: a) 40 ms b) 500 ms c) 1 s d) 2 s → **b**
6. Default keepalive idle: a) 30 s b) 300 s c) 7200 s d) 1 h → **c**
7. Persist probes during: a) rwnd=0 b) cwnd=0 c) TIME_WAIT d) SYN_RCVD → **a**
8. TFO gives: a) bigger windows b) 0-RTT repeats c) SACK d) pacing → **b**
9. CLOSE_WAIT pileup means: a) attack b) app fd leak c) NAT d) MSS → **b**
10. Simultaneous close passes through: a) CLOSING b) LAST_ACK c) SYN_RCVD d) LISTEN → **a**

## 20. Flashcards
- **Q: 11 TCP states?** → **A:** CLOSED, LISTEN, SYN_SENT, SYN_RCVD, ESTABLISHED, FIN_WAIT_1/2, CLOSE_WAIT, CLOSING, LAST_ACK, TIME_WAIT.
- **Q: Active close path?** → **A:** FIN_WAIT_1→FIN_WAIT_2→TIME_WAIT→CLOSED.
- **Q: Nagle?** → **A:** ≤1 small segment in flight; coalesce; TCP_NODELAY disables.
- **Q: Delayed ACK?** → **A:** ≤500 ms batch/piggyback; × Nagle = 40 ms tax.
- **Q: Keepalive?** → **A:** 7200 s idle → probes (75 s ×9); tune for infra.
- **Q: Persist?** → **A:** window probes while rwnd=0.
- **Q: TFO?** → **A:** cookie+data in SYN → 0-RTT repeats.
- **Q: CLOSE_WAIT?** → **A:** passive closer waiting for app close() = leak.

## 21. Revision
TCP's 11-state FSM (CLOSED/LISTEN/SYN_SENT/SYN_RCVD/ESTABLISHED/FIN_WAIT_1/2/CLOSE_WAIT/CLOSING/LAST_ACK/TIME_WAIT) drives all connection handling; states are diagnosable via `ss -tan`. Nagle coalesces small writes (≤1 in flight) — disable with TCP_NODELAY for latency; delayed ACK batches (≤500 ms) — their interaction adds up to 40-500 ms. Keepalive (7200 s idle → 75 s×9 probes) detects dead peers — tune to 30-300 s in infra. Persist probes (5-60 s) survive zero-window. TFO gives 0-RTT repeats. CLOSE_WAIT = fd leak; SYN_RCVD flood = attack; half-open = only keepalive/send-RTO detects.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "List/describe TCP states." | 2 How It Works / 7 Formal Definition |
| "Trace active/passive close paths." | 13 Q&A / 8 Example |
| "What is Nagle / when disable it?" | 13 Q&A / 5 Intuition |
| "What is delayed ACK / the 40 ms interaction?" | 13 Q&A / 6 Real-World Analogy |
| "How does keepalive work / tune it?" | 13 Q&A / 9 Internal Working |
| "What is the persist timer?" | 13 Q&A / 9 Internal Working |
| "What is TFO / 0-RTT?" | 13 Q&A / 11 Advantages |
| "Debug CLOSE_WAIT / SYN_RCVD." | 13 Q&A / 16 Industry Usage |
| "Half-open connections?" | 13 Q&A / 14 Follow-Up |
