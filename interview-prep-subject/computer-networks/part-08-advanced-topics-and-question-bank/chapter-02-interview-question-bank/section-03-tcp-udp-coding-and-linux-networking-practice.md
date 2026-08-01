# TCP/UDP Coding and Linux Networking Practice

> **TL;DR**: Write real TCP and UDP socket programs (Python/C/Go) — servers, clients, non-blocking I/O with select/poll/epoll, HTTP-over-sockets — and master the Linux network toolbox (`ss`, `netstat`, `tcpdump`, `ip`, `iperf`, `sysctl`) to debug and tune like a production engineer.

## 1. Why Does This Exist?
Interviews for infra/SRE/network roles increasingly include *hands-on* network work: "write a TCP server", "what's the backlog?", "how do you find a dropped-packet problem?" — and the difference between a junior and senior candidate is fluency with the real tools. This section exists to close the gap between theory (Parts 01-07) and practice: you'll write sockets that exercise the very mechanisms you studied (handshake, seq/ack, backlog, non-blocking, TIME_WAIT), and you'll use `ss`/`tcpdump`/`iperf` to *see* them. The Linux networking stack is the reference implementation of everything in this roadmap — knowing it is knowing the roadmap.

## 2. How Does It Work?
1. **Write sockets**: start with blocking TCP server/client; then UDP; then concurrency (`threading`, `select`, `poll`, `epoll`); then HTTP over raw sockets; then a small QUIC/HTTP3-aware design (conceptually).
2. **Observe**: run `ss -t`, `tcpdump -i lo`, `strace`/`lsof` alongside your program to see SYN/ACK, backlog behavior, TIME_WAIT, and buffer states.
3. **Tune**: use `sysctl` (`tcp_rmem/wmem`, `tcp_max_syn_backlog`, `netdev_max_backlog`, `somaxconn`) and explain each knob with the mechanism it changes.
4. **Debug**: given a symptom (retransmits, drops, connection resets), reproduce with the tools and correlate with the protocol behavior.
Every example is runnable; the "verify" commands let you confirm the mechanism you just coded.

## 3. When Is It Used?
- **Coding-in-networking rounds** at infra/SRE/network-engineer roles (Amazon, Cloudflare, Arista, big-cloud teams).
- **Take-homes** with "TCP server / UDP ping / packet-capture" tasks.
- **On-the-job** (the real point): debugging latency, tuning kernels, reading captures, understanding why a service drops connections.
- Pair with Section 01 (theory recall) and Section 02 (design) for the full stack.

## 4. Why Wasn't Another Approach Chosen?
- *Just theory:* interviews and production both demand tool fluency — knowing "TIME_WAIT = 2×MSL" without being able to *see* it in `ss` is half-competence.
- *Only high-level languages/frameworks:* frameworks hide the socket layer (backlog, non-blocking, buffers) — the interview and the debugging job are about that layer. Raw `socket` in Python/C is the right depth.
- *Only C:* Python/Go get you 90% of the teaching value with 10% of the friction; C is shown for the `struct`/syscall view. Both are covered.
- *Just reading man pages:* you need to run, observe, break, and fix — active, not passive.

## 5. Intuition
A socket is **a door with two locks and a mailbox**. The server installs a door (`socket` → `bind` → `listen`); the kernel queues visitors in the listening queue (`backlog`); the server lets visitors in (`accept`), giving each their own private room (a connected socket). `select`/`epoll` is the **front-desk clerk** who watches many doors at once and tells you when a visitor knocks — so you don't have to stand at every door. UDP is **no door at all**: you just shout into the street (`sendto`) with the address on the envelope and hope it arrives — anyone can shout back. `tcpdump`/`ss` are the **security cameras** showing every knock, every handshake, and every dropped letter in real time.

## 6. Real-World Analogy
A **restaurant with a host and a waiter**. The host (`listen` + `accept`) stands at the door; when a guest arrives (`SYN`), they get seated (the backlog queue holds waiting guests), and each seated party gets a dedicated waiter (a connected socket + thread). A host with too-small a waiting area (`backlog`) turns guests away when it's full (SYN drops / connection refused). `epoll` is a **maître d' with a clipboard**: instead of the manager polling each table (busy-loop), the clipboard rings only when a table needs attention (event-driven, O(1) per event). UDP is a **food delivery to a street address with no signature** — the package might be left at the wrong place, might arrive twice, or might never arrive; you put the tracking number (sequence) in your own app if it matters. `tcpdump` is the **security camera**: it records every handshake and every dropped packet, and you replay it to find who was lost.

## 7. Formal Definition
- **Socket**: an endpoint of a two-way communication link; identified by (IP, port) for TCP, by (IP, port, src IP, src port) for the connection.
- **POSIX socket API**: `socket(domain, type, proto)`; `bind` (assign addr); `listen(fd, backlog)` (mark passive + queue length); `accept` (dequeue a pending connection → new fd); `connect`; `send/recv`; `close`; `shutdown`.
- **Backlog**: two-part (in Linux): the *request* (SYN) queue and the *established* queue (completed handshakes awaiting `accept`); `somaxconn` caps it (default 4096); applications use `listen(fd, 128)`+ but the kernel caps at `somaxconn`.
- **Non-blocking I/O**: `O_NONBLOCK`/`SOCK_NONBLOCK` — operations return immediately with `EAGAIN/EWOULDBLOCK`; multiplexers watch readiness.
- **select/poll/epoll**: readiness multiplexing. select: FD_SETSIZE-limited (1024), O(n) scan. poll: no hard cap, O(n). epoll: kernel event table, O(events) — the Linux production standard (`epoll_wait`).
- **UDP**: `sendto/recvfrom`; no connection, no ordering, no reliability; checksum + length (8-byte header).
- **Linux net tools**: `ss` (socket stats), `netstat` (legacy), `tcpdump` (capture), `ip` (addr/route/link), `iperf3` (throughput), `ss -ti` (TCP internals: cwnd/rwnd/RTT), `sysctl net.*` (kernel params), `ethool -S` (NIC counters), `nc`/`ncat` (swiss-army client/server).

## 8. Example
**Minimal TCP echo server (Python) — and what each line does:**
```python
import socket, threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # bind TIME_WAIT ports quickly
server.bind(("0.0.0.0", 9999))
server.listen(128)                       # backlog (kernel caps at somaxconn)
print("listening on :9999")

def handle(conn, addr):
    while data := conn.recv(4096):        # blocks until data
        conn.sendall(b"echo: " + data)    # sendall = loop until all sent
    conn.close()

while True:
    conn, addr = server.accept()          # dequeue an ESTABLISHED connection
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
```
Verify: `nc 127.0.0.1 9999` then type; watch with `ss -tn` and `tcpdump -i lo port 9999`.

## 9. Internal Working
1. **listen/backlog**: kernel keeps a completed-connection queue (handshake done) + a SYN queue (half-open); `accept` pops the completed queue. If the queue is full, SYN retries get dropped/timed out — clients see slowness or "connection refused/timeout".
2. **connect**: sends SYN, waits for SYN+ACK (retransmits per `tcp_syn_retries`), then ACKs; a successful `connect` = the completed handshake. Non-blocking connect returns `EINPROGRESS`; wait for writability in epoll.
3. **recv/send**: return bytes available/buffered; 0 from recv = EOF (peer closed); `EAGAIN` on non-blocking = no data ready. Buffers: `SO_RCVBUF/SO_SNDBUF` (kernel doubles), floor'd by `tcp_rmem/tcp_wmem`.
4. **select/poll/epoll**: register fds, wait for readable/writable/error events; epoll uses a kernel-backed interest table with edge/level triggering (EPOLLET = edge) — the standard high-concurrency model (nginx, Redis).
5. **close vs shutdown**: `close` decrements refcount (shared fds) and sends FIN when 0; `shutdown(SHUT_WR)` sends FIN immediately (half-close) — useful for "I'm done sending, keep receiving".
6. **TIME_WAIT**: the side that sends the first FIN stays in TIME_WAIT for 2×MSL (~60 s); `SO_REUSEADDR` allows rebinding in TIME_WAIT; too many TIME_WAIT sockets exhaust ports/fds → tune `tcp_tw_reuse` or use keep-alive/connection pooling.
7. **Kernel tuning**: `tcp_rmem/tcp_wmem` (buffer floors/defaults/ceilings), `net.core.somaxconn` (listen backlog cap), `net.core.rmem_max/wmem_max` (UDP buffers), `tcp_congestion_control` (cubic/bbr), `tcp_fastopen` (0/1/2), `tcp_sack` (selective acks), `ip_local_port_range` (client port pool).

## 10. Time Complexity / Performance
- **select**: O(n) scan per call; cap 1024 → not for high-fd.
- **poll**: O(n) but no 1024 cap; fine to ~10k.
- **epoll**: O(events) — the kernel notifies only ready fds; supports 100k+ connections (nginx/Redis scale).
- **syscall cost**: one `recv` per event vs busy-polling — event-driven saves CPU at scale.
- **TCP throughput**: bounded by cwnd/RTT (BDP, Section 01-Q25/84) and buffers — tune `tcp_rmem/wmem` ≥ BDP for fat pipes.
- **UDP**: no connection setup — lowest latency; but no loss recovery — the app (or QUIC) adds it.

## 11. Advantages
Write-it-and-see-it validates the theory (handshake in `tcpdump` is unforgettable); the tools transfer directly to production debugging; event-driven patterns (epoll) are exactly what nginx/Redis/netty use — the interview "code + explain" answer matches production reality; kernel-tuning knowledge is a senior-signal.

## 12. Disadvantages
Linux-specific (macOS/Windows differ in tooling; epoll is Linux-only — kqueue elsewhere); deep tuning needs root + careful testing; sockets/C-level topics can be a time sink if you over-rotate vs theory and design.

## 13. Interview Questions
1. **Q: Write a TCP echo server in Python.** A: See Example: socket → setsockopt(SO_REUSEADDR) → bind → listen(128) → accept loop → per-connection thread; `sendall` for complete writes; `recv` loop until EOF. Explain backlog = completed-queue size.
2. **Q: What is the `listen` backlog and what happens when it's full?** A: Kernel queue of completed (ESTABLISHED) connections awaiting `accept`; capped by `net.core.somaxconn`. When full: new SYNs are dropped/retried (client stalls) and established connections may get RST — the classic "connection refused under load." Fix: raise backlog, scale accepters, or shorten accept time.
3. **Q: How do you handle 10,000 concurrent connections in Python?** A: Not with a thread per connection at that scale — use non-blocking sockets + `selectors` (epoll) and an event loop; or use asyncio. Explain epoll O(events) vs select O(n); thread-per-conn costs ~8 MB stack each.
4. **Q: What's the difference between `close` and `shutdown`?** A: `close` decrements the fd refcount and sends FIN only when the count hits 0 (shared fds still open → no FIN). `shutdown(SHUT_WR)` sends FIN immediately (half-close: I'm done sending, you can still send to me). Use shutdown for clean half-close protocols.
5. **Q: What does SO_REUSEADDR do and why do servers need it?** A: Allows a socket to bind to an address/port still in TIME_WAIT — otherwise a restarting server can't rebind for ~60 s. (Note: it does NOT allow two *active* binds; SO_REUSEPORT does, for multi-worker LBs.)
6. **Q: TRICKY — How do you debug "connection refused" vs "connection timeout"?** A: Refused = RST — something actively refused (port closed, firewall reject, backlog-full RST). Timeout = SYN dropped with no reply (firewall drop, host down, SYN queue full, routing). `tcpdump` shows RST vs nothing; `ss -t state syn-sent` shows the client stuck. Different causes → different fixes.
7. **Q: What is a SYN flood and how do SYN cookies work?** A: Attackers send SYN without completing — fills the SYN queue. SYN cookies: instead of storing state, the kernel encodes the connection in the SYN+ACK's seq (a cookie derived from addr+time+secret); on the client's ACK, state is *reconstructed* — no queue needed. Enabled by default when under pressure (`net.ipv4.tcp_syncookies`).
8. **Q: How do you find dropped packets on Linux?** A: (1) NIC counters (`ethtool -S` for rx_dropped/rx_missed); (2) `netstat -s`/`ss -s` (TCP resets, retransmits); (3) `tcpdump` (see the drop on the wire) + `netdev_max_backlog` for receive-drop under bursts; (4) check `rmem` overflow (`UdpRcvbufErrors`); (5) eBPF tracing (`bpftrace`) for kernel-path drops. Correlate with `ss -ti` (cwnd collapse = loss).
9. **Q: What is epoll and why is it better than select/poll?** A: epoll registers fds once with the kernel and returns *only ready* fds on wait — O(events), not O(fds); no FD_SETSIZE cap; edge/level triggering; scales to 100k+ connections. select: O(n) scan + 1024 cap; poll: O(n) without the cap.
10. **Q: PRODUCTION — `ss -tn` shows thousands of TIME_WAIT sockets. Is that bad and what do you do?** A: Normal for short-lived client connections (2×MSL each) but can exhaust ports/fds or slow rebinding. Fixes: enable keep-alive/connection pooling (reuse), tune `tcp_tw_reuse` + `ip_local_port_range`, or (for servers) SO_REUSEADDR; ensure the pool of ephemeral ports is big enough for the connect rate (RATE × TIME_WAIT duration).
11. **Q: How do you measure throughput and find the limit?** A: `iperf3 -s` / `iperf3 -c host` (bandwidth); watch with `ss -ti` (cwnd, rwnd, RTT) and `tcpdump` (window shrinks = buffer bound). If iperf hits line rate but your app doesn't: check TLS, per-request RTTs, Nagle/delayed-ACK, and buffer sizes (BDP).
12. **Q: TRICKY — What causes the ~40 ms "latency" on small TCP writes?** A: Nagle (batch small segments until ACKed) + delayed ACK (receiver waits ~40 ms to piggyback) — together they stall small back-and-forth traffic ~40-200 ms. Fix: disable Nagle (`TCP_NODELAY`) on the client side for interactive protocols (or use `TCP_QUICKACK` server-side when appropriate).
13. **Q: How do you write a non-blocking TCP client?** A: Set SOCK_NONBLOCK, call `connect` → returns EINPROGRESS; register the fd for writability in epoll; on writable, check `SO_ERROR` for the connect result; then proceed with send/recv (handling EAGAIN). This is how high-scale clients avoid blocking threads on connects.
14. **Q: What is a "connection reset by peer" and common causes?** A: Peer sent RST — from: app-level close without reading all data (`SO_LINGER` 0 forces RST), backlog-full refusal, firewall RST, or protocol violation (data on closed socket). Check `ss -ti` for the reset source and `tcpdump` for who sent the RST.
15. **Q: SCENARIO — Your service has high retransmits but the app is idle. Where do you look?** A: (1) Network loss (router/drop) — `tcpdump` + NIC counters; (2) buffer collapse (cwnd small) — `ss -ti`; (3) MTU/MSS mismatch (fragmented/dropped) — check ICMP frag-needed + `ss -ti` mss; (4) host receive queue overflow under bursts — `netstat -s` rcv_errors; (5) congestion control reacting to ECN. The retransmit count alone doesn't say *where* — the captures do.
16. **Q: How do you size kernel buffers for a fat network?** A: Buffers ≥ BDP = bandwidth × RTT. E.g., 10 Gbps × 50 ms = 62.5 MB in flight — set `tcp_rmem/wmem` max ≥ ~64 MB and app's `SO_RCVBUF/SO_SNDBUF` accordingly; else the window caps throughput far below line rate.
17. **Q: PRODUCTION — Design a high-throughput UDP ingest and debug its drops.** A: (1) size `net.core.rmem_max`/`SO_RCVBUF` to the burst (else kernel drops silently); (2) use `recvmmsg` (batch) to reduce syscalls; (3) multithreaded/multi-queue with `SO_REUSEPORT` for NIC RSS fan-out; (4) monitor `UdpRcvbufErrors`/`RcvbufErrors` — those are your drop count; (5) app-level sequence numbers + gap detection for loss; (6) if still dropping, move to a lossless fabric (RoCE/PFC) or TCP/QUIC.

## 14. Follow-Up Questions
1. **Q: What's the difference between a listening socket and a connected socket?** A: Listening = passive, from `listen`, accepts new connections, has a backlog. Connected = active, from `accept`/`connect`, full-duplex byte stream. One listening socket → many connected sockets. A common mental-model bug in interviews.
2. **Q: What is EAGAIN and how should you handle it?** A: "Would block" on non-blocking I/O — the operation would block if it weren't non-blocking. Correct handling: *don't* treat it as an error; wait for readiness in epoll and retry. Treating EAGAIN as a hard error is a classic bug.
3. **Q: What is the receive path in the kernel (in one breath)?** A: NIC DMA → ring buffer → interrupt/NIC IRQ → softirq `net_rx_action` → `netif_receive_skb` → protocol (IP/TCP) → socket receive queue → user `recv`. Drops can occur at the ring (`rx_dropped`), softirq (`netdev_max_backlog`), or socket queue (rmem) — which is exactly where `ss`/`netstat -s` numbers point.
4. **Q: What is TCP Fast Open?** A: TLS-like 0-RTT for TCP: the client sends data in the SYN (TFO cookie required after the first connection). `tcp_fastopen` sysctl (0/1/2); saves one RTT for repeat connections — the TCP cousin of TLS 1.3 0-RTT.

## 15. Coding Example
```python
# epoll-based non-blocking TCP server (the production pattern: nginx/Redis-style)
import socket, selectors, types

sel = selectors.DefaultSelector()      # epoll on Linux
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 9998)); server.listen(128)
server.setblocking(False)
sel.register(server, selectors.EVENT_READ, data=None)

def accept_wrapper(key):
    conn, addr = key.fileobj.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, data=types.SimpleNamespace(buf=b""))

def service(key):
    data = key.fileobj.recv(1024)
    if data: key.fileobj.sendall(data)          # echo
    else: sel.unregister(key.fileobj); key.fileobj.close()

while True:
    for key, _ in sel.select():                 # O(events) wakeup
        fn = accept_wrapper if key.data is None else service
        fn(key)
```
```bash
# The Linux toolbox — verify every claim in this section
ss -tn state established             # see ESTABLISHED sockets + their addresses
ss -tn state time-wait | wc -l       # count TIME_WAIT (2*MSL ~60s)
ss -ti | grep -E "cwnd|rtt|mss"      # TCP internals: congestion window, RTT, MSS
sudo tcpdump -i lo port 9999 -c 10   # watch SYN/SYN-ACK/ACK live
sudo tcpdump -i lo -w /tmp/x.pcap    # capture for analysis
ip link show; ethtool -S eth0 | grep -iE "drop|err"   # NIC counters
sysctl net.ipv4.tcp_rmem net.ipv4.tcp_wmem net.core.somaxconn net.ipv4.tcp_syncookies
iperf3 -s & sleep 1; iperf3 -c 127.0.0.1 -t 5        # measure loopback throughput
nc -l 4000 < /dev/null &              # quick test server
```

## 16. Industry Usage
- **nginx/Redis/HAProxy** — the epoll event loop IS the product (this section's pattern).
- **SRE/infra interviews**: Amazon (TCP tuning, `ss`/`tcpdump`), Cloudflare (packet capture, kernel), big-cloud teams.
- **Networking vendors**: Cisco/Arista/NVIDIA (data-plane coding, RDMA).
- **On-call reality**: every latency/drop incident is debugged with exactly these commands.
- **Performance engineering**: `ss -ti`, `iperf3`, `ethtool -S`, eBPF are the daily toolkit.

## 17. References
- `man 7 socket`, `man 7 tcp`, `man 2 epoll`, `man 5 tcpdump`, `man 8 iperf3`.
- RFC 793 (TCP), 768 (UDP), 9293 (TCP: Modern), and Linux kernel docs (`Documentation/networking/ip-sysctl.rst`).
- Python docs: `socket`, `selectors`, `asyncio`; Go `net` package; Beej's Guide to Network Programming.
- Brendan Gregg's Linux performance / networking talks (drop points, receive path).

## 18. Cheat Sheet
- Server: socket → setsockopt(SO_REUSEADDR) → bind → listen(backlog ≤ somaxconn) → accept loop → per-conn worker.
- Non-blocking: set non-block, register in epoll; EAGAIN = "wait, not an error".
- epoll > poll > select (O(events) vs O(n); no 1024 cap; the nginx/Redis model).
- close vs shutdown: close = refcount+FIN at 0; shutdown(SHUT_WR) = FIN now (half-close).
- TIME_WAIT 2×MSL ~60s; fix with SO_REUSEADDR (server), pooling/tw_reuse (client).
- Nagle + delayed ACK = ~40ms stalls → TCP_NODELAY.
- Drop points: NIC ring → netdev_max_backlog → socket rmem; check ethtool -S / netstat -s / ss.
- SYN flood → SYN cookies (tcp_syncookies).
- Buffers ≥ BDP = BW × RTT or window caps throughput.
- UDP: sendto/recvfrom, no order/reliability; use recvmmsg + SO_REUSEPORT at scale.

## 19. Quiz
1. `listen` backlog caps: a) client count b) completed-connections waiting for accept c) buffer d) threads → **b**
2. On Linux, the production multiplexer is: a) select b) poll c) epoll d) fork → **c**
3. EAGAIN on non-blocking means: a) error b) would block — wait c) closed d) timeout → **b**
4. `close` sends FIN when: a) always b) fd refcount reaches 0 c) buffer empty d) never → **b**
5. TIME_WAIT lasts: a) 1 s b) 2×MSL ~60 s c) 24 h d) 0 → **b**
6. Which fixes small-write latency stalls? a) bigger buffers b) TCP_NODELAY c) backlog d) syncookies → **b**
7. UDP drops are visible via: a) RcvbufErrors b) SYN count c) backlog d) mss → **a**
8. SYN flood defense: a) TCP_NODELAY b) SYN cookies c) SO_REUSEADDR d) keepalive → **b**

**Answers**: 1-b, 2-c, 3-b, 4-b, 5-b, 6-b, 7-a, 8-b.

## 20. Flashcards
- **Q: Server setup order** → **A:** socket → SO_REUSEADDR → bind → listen(backlog) → accept → per-conn handler.
- **Q: epoll vs select** → **A:** O(events) vs O(n); no 1024 cap; kernel-ready fds.
- **Q: EAGAIN means?** → **A:** would block — wait for readiness in epoll, not an error.
- **Q: close vs shutdown** → **A:** close = refcount→FIN; shutdown(SHUT_WR) = immediate FIN half-close.
- **Q: Small-write stall cause/fix** → **A:** Nagle + delayed ACK → TCP_NODELAY.
- **Q: Where do packets drop?** → **A:** NIC ring → netdev_max_backlog → socket rmem; check ethtool -S/netstat -s.
- **Q: Buffer sizing rule** → **A:** buffers ≥ BDP (bandwidth × RTT).

## 21. Revision
Hands-on networking = sockets + kernel + tools. Server pattern: socket→REUSEADDR→bind→listen(backlog≤somaxconn)→accept loop; per-connection via epoll (O(events), EAGAIN is "wait"), not threads at scale. Half-close with shutdown; TIME_WAIT (2×MSL) handled by SO_REUSEADDR/pooling; Nagle+delayed-ACK stalls fixed by TCP_NODELAY; SYN floods by cookies. Drops: NIC ring→netdev_max_backlog→rmem — correlate `ethtool -S`, `netstat -s`, `ss -ti`. Tune buffers ≥ BDP. UDP: sendto/recvfrom, no reliability, recvmmsg+REUSEPORT at scale. Anchors: *listen backlog = completed-queue, full = refusals; epoll for 100k conns; EAGAIN ≠ error; drops have a specific kernel point — find it; buffers ≥ BDP or the window caps you.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Write a TCP echo server" | 8 / 13-Q1 |
| "What is the backlog?" | 13-Q2 |
| "How do you handle 10k conns?" | 13-Q3 |
| "close vs shutdown" | 13-Q4 |
| "SO_REUSEADDR" | 13-Q5 |
| "Connection refused vs timeout" | 13-Q6 |
| "SYN flood / cookies" | 13-Q7 |
| "How do you find dropped packets?" | 13-Q8 |
| "What is epoll?" | 13-Q9 |
| "TIME_WAIT problem + fix" | 13-Q10 |
| "40 ms Nagle/delayed-ACK stall" | 13-Q12 |
| "Connection reset causes" | 13-Q14 |
| "High retransmits — debug path" | 13-Q15 |
| "Buffer sizing for fat pipes" | 13-Q16 |
