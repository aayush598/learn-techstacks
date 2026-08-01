# Ports and Sockets

> **TL;DR**: A **port** is a 16-bit number (0-65535) identifying a process/service end-point on a host; a **socket** is the OS abstraction for one end-point of a communication channel — and the four-tuple (srcIP, srcPort, dstIP, dstPort) is what uniquely identifies each connection, letting one server host millions of simultaneous connections.

## 1. Why Does This Exist?
IP addresses identify *hosts*, but hosts run many processes — a server with web, mail, and DNS on one IP needs to route each packet to the right process. Ports exist for **process addressing**: the destination port selects the process (demultiplexing), the source port tells the receiver where to reply. Sockets exist because the OS must *manage* these end-points: each open network connection is a socket with state (buffers, address, connection state), and the OS must uniquely identify and schedule among them. Without ports/sockets, you couldn't run HTTP, SSH, and DNS on one machine, and servers couldn't serve thousands of clients simultaneously.

## 2. How Does It Work?
- **Ports**: 16-bit field in TCP/UDP headers. Ranges: 0-1023 well-known (server services), 1024-49151 registered, 49152-65535 dynamic/ephemeral (client source ports).
- **Socket** (BSD): the end-point created by `socket()`. On the server: `bind()` (local port), `listen()` (passive), `accept()` (yields a *connected socket* per client). On the client: `connect()` (binds an ephemeral port + remote address).
- **Four-tuple** = (src IP, src port, dst IP, dst port). TCP connections are uniquely identified by the full four-tuple; UDP sockets can match on (dst IP, dst port) + optionally src.
- **Demultiplexing**: the OS hashes the tuple → finds the exact socket → delivers. A listening socket (e.g., *:443) accepts the SYN; then a *child connected socket* (with the specific remote tuple) handles that connection's traffic.
- **Socket types**: stream (TCP), datagram (UDP), raw (IP); plus `SO_REUSEADDR`, buffers (`SO_RCVBUF`/`SO_SNDBUF`), options (TCP_NODELAY).

## 3. When Is It Used?
- **Every TCP/UDP interaction**: HTTP (443/80), DNS (53), SSH (22), email (25/587/110/143), databases (5432, 3306), games, VoIP (RTP).
- **Server scaling**: a server socket on port 443 accepts N connections → N connected sockets sharing the same local port.
- **NAT/load balancers**: they *rewrite* tuples (DNAT/SNAT) — ports are the NAT translation keys.
- **Debugging**: `netstat -an`, `ss -tulnp`, `lsof -i` — all read the OS socket tables.
- **Firewalls**: allow/deny by (protocol, port) — security groups are port-based filters.

## 4. Why Wasn't Another Approach Chosen?
- **Why 16-bit ports instead of a process-ID-based scheme?** Process IDs change per machine/session and leak information; ports are *stable, agreed, and machine-independent* — a fixed service contract (80 = web everywhere). Ports also decouple service identity from process identity.
- **Why not one connection per IP?** A host must serve *many* clients to the same IP+port — the four-tuple's *source* part differentiates them. Without it, one client at a time per server.
- **Why a socket abstraction instead of direct protocol calls?** The socket API (introduced in BSD, 1983) provides a uniform, OS-managed interface: buffers, blocking/non-blocking, multiplexing (`select`/`epoll`), and reuse — apps never touch the raw headers. It won because it's simple and portable.
- **Why ephemeral source ports (49152-65535)?** Clients need a *unique source* so multiple connections from one IP to the same server don't collide; the OS auto-assigns them. Static client ports would break multiplexing and NAT.
- **Why reuse/2-tuple for UDP?** UDP is connectionless — the receiver can match on dst alone; binding to a specific remote (like a connected UDP socket) is optional optimization.

## 5. Intuition
Think of an **apartment building with one street address (IP)**. The port is the *apartment number* — mail (packets) must know which unit (process). The socket is the *mailbox at that unit*: a box in the lobby wall with an address label, a slot for incoming, an outgoing pile. A server = the building's management office (listening socket) that assigns each new guest a private mailbox (connected socket) while the office box stays shared. The four-tuple = "which building, which unit, and *from which building and unit* did this letter come" — enough to tell every mailbag apart, even when 10,000 letters are in flight.

## 6. Real-World Analogy
**Hotel with one phone switchboard**: The hotel's phone number is the IP; the *extension* is the port. "Call the front desk on extension 0" = the well-known port (443). When you check in, the switchboard gives you a *private extension* (ephemeral source port) and connects calls between your room and the front desk. Each active call is a *socket*: (your room, your extension) ↔ (front desk, extension 0). The switchboard (OS) tracks every active call by that tuple — the same front-desk extension can be in a thousand calls because each has a different *room/extension* on the caller side. Without extensions, every guest would ring every room.

## 7. Formal Definition
A **port** is a 16-bit identifier (0-65535) used by TCP and UDP to address *processes/services* within a host. Well-known ports (0-1023) are assigned by IANA (e.g., 80 HTTP, 443 HTTPS, 53 DNS, 22 SSH); registered ports (1024-49151) for vendor apps; dynamic/ephemeral ports (49152-65535) for client-side use. A **socket** is the OS-level abstraction of a communication end-point, defined by the local IP address, local port, and (for connected sockets) the remote IP and port; the **four-tuple** `(srcIP, srcPort, dstIP, dstPort)` uniquely identifies a TCP connection. Multiplexing/demultiplexing is performed by the OS using this tuple.

## 8. Example
Two clients to one server (numbers):
```
Server 10.0.0.5:443 (web, listening socket)
Client A 192.168.1.10:54321 -> 10.0.0.5:443
Client B 192.168.1.11:59234 -> 10.0.0.5:443
Sockets on server:
  LISTEN  10.0.0.5:443                      (listening socket)
  ESTAB   10.0.0.5:443 | 192.168.1.10:54321 (connected socket A)
  ESTAB   10.0.0.5:443 | 192.168.1.11:59234 (connected socket B)
Four-tuples:
  (192.168.1.10, 54321, 10.0.0.5, 443)  <- conn A
  (192.168.1.11, 59234, 10.0.0.5, 443)  <- conn B
The OS tells them apart purely by the source half of the tuple.
```
Client side: source ports are ephemeral (54321, 59234 from 49152-65535) so two apps on one client can connect to the same server without colliding.

## 9. Internal Working
1. **Server startup**: `socket()` → `bind(("0.0.0.0", 443))` (all interfaces, well-known port) → `listen(backlog)` → OS opens a listening socket, adds it to the port hash table. `SO_REUSEADDR` allows fast restart after TIME_WAIT.
2. **Connection establishment**: client sends SYN (src = ephemeral port). The OS looks up the listening socket by (dst IP, dst port), completes the handshake, and creates a **child connected socket** with the four-tuple filled in — the listening socket stays untouched.
3. **Demultiplexing on arrival**: for each incoming segment, the OS hashes `(srcIP, srcPort, dstIP, dstPort)` against the connection table (O(1) hash) → finds the exact socket → wakes its waiters → enqueues data. Unknown tuple → RST (TCP) or ICMP port unreachable.
4. **UDP demux**: lookup key is (dst IP, dst port) (and src if the socket is "connected"); multiple datagrams from different senders hit the same socket — apps read `recvfrom` to learn the sender. Unconnected sockets receive all.
5. **Buffers**: each socket has kernel send/recv queues (`SO_SNDBUF`/`SO_RCVBUF`, autotuned). Flow control advertises the recv buffer as `rwnd`.
6. **Lifecycle**: `accept()` returns a *new fd* per connection; `close()` on both ends terminates; the OS cleans the tuple. `ss`/`netstat`/`lsof` introspect all of this.
7. **Many connections to one port**: the port table maps to the listening socket; the *connection* table maps tuples → connected sockets. That's how 1M clients share port 443.

## 10. Time Complexity
- **Lookup**: O(1) hash on the four-tuple (kernel connection hash); with tens of millions of sockets, memory + hash-table sizing is the constraint, not lookup.
- **Memory per socket**: connected socket struct + buffers ≈ 10-100s KB (autotuned); a million connections ≈ GBs → hence C10K/C100K engineering (epoll, kernel tuning, `rmem_max`/`wmem_max`, jumbo buffers).
- **Port exhaustion**: ~28-64k ephemeral ports per (src IP, dst IP) without `net.ipv4.ip_local_port_range` extension → NAT/load-balancer ports are a classic bottleneck (solution: more IPs, or source-port reuse with full-tuple uniqueness).
- **FD cost**: each socket = a file descriptor; limits (`ulimit -n`, `fs.file-max`) cap connections.

## 11. Advantages
- **Process addressing**: many services per host, stable well-known ports.
- **Scalability**: millions of connections per server via tuple demultiplexing.
- **NAT/port-forwarding**: ports make address translation and in-bound service publishing possible.
- **Simple API**: BSD sockets (stream/datagram) are universal, portable, and tuneable.
- **Observability**: `ss`/`netstat`/`lsof` give full connection visibility for debugging.

## 12. Disadvantages
- **Port exhaustion**: 65535 limit per address; NAT clients and high-concurrency servers hit ceilings (mitigated by tuples + IP ranges).
- **Security surface**: open ports = attack surface; port scanning is the recon step. "Security through obscurity" (moving SSH to 2222) doesn't hide anything.
- **Well-known port conflicts**: two services wanting 80/443 need name-based virtual hosting or separate IPs.
- **Abuse**: port knocking/firewall bypass tricks, UDP port-flood DDoS, and NAT/PAT complexity with protocols that embed ports (FTP ALG).

## 13. Interview Questions
1. **Q: What is a port and what is it used for?** A: A 16-bit number (0-65535) identifying a process/service end-point on a host. The destination port demultiplexes incoming data to the right process; the source port lets replies return.
2. **Q: What is a socket?** A: The OS abstraction of a communication end-point: local (IP, port) + optionally remote (IP, port) + state (buffers, connection state). `socket()` creates it; a listening socket accepts; a connected socket carries a specific connection.
3. **Q (tricky): How can a server accept a million connections to port 443?** A: The listening socket is one end-point; each accepted connection gets its own *connected socket* identified by the full four-tuple. The local (IP, port) is shared; the *source* (IP, port) differs per client — the tuple uniquely disambiguates.
4. **Q: What is the four-tuple?** A: (srcIP, srcPort, dstIP, dstPort). For TCP it uniquely identifies a connection; the OS hashes it to demultiplex segments to the right socket.
5. **Q: Name the port ranges.** A: 0-1023 well-known (web 80/443, DNS 53, SSH 22); 1024-49151 registered (Postgres 5432, MySQL 3306); 49152-65535 dynamic/ephemeral (client source ports).
6. **Q (production): Why do source ports matter for NAT?** A: NAT maps many private (IP, port) to one public IP; it rewrites both source IP *and* source port (PAT) so return traffic can be demultiplexed back to the right private host. Ephemeral ports are the translation "slots." Port exhaustion under NAT is a real scaling limit.
7. **Q: What happens when a packet arrives for a port nobody is listening on?** A: TCP → the receiver sends an RST (connection refused) or drops with ICMP port-unreachable; UDP → ICMP port-unreachable. Port scanners detect services this way.
8. **Q: What is the difference between `bind`, `listen`, `accept`, and `connect`?** A: `bind` assigns the local address/port; `listen` marks a TCP socket as accepting (passive); `accept` pulls a *new connected socket* for each client from the queue; `connect` (client) initiates to a remote address and binds an ephemeral source port.
9. **Q: What is `SO_REUSEADDR` and why is it needed?** A: It lets a server restart and rebind to a port while old connections sit in TIME_WAIT — without it, restart fails with "Address already in use." (Common gotcha in dev/ops.)
10. **Q (scenario): Your client can't reach a service but the server listens on the port. What's wrong?** A: Check the firewall/security group (port blocked), the bind address (0.0.0.0 vs 127.0.0.1 vs wrong NIC), NAT/port-forward rules, the tuple being rewritten, or the service bound to a *different* interface. Port reachability = firewall + bind + routing, not just listening.
11. **Q: What is an ephemeral port?** A: The source port the OS auto-assigns to a client connection (49152-65535 by default, configurable via `ip_local_port_range`). It identifies the client end of the tuple and must be unique per (local IP, remote IP, remote port) to avoid collisions.
12. **Q: How does UDP demultiplex without connection state?** A: By (dst IP, dst port) alone (and src if the socket is "connected"). All datagrams to a bound port reach that socket; the app reads sender info from `recvfrom`. This is why UDP scales trivially — no per-connection tuple table required.
13. **Q (tricky): Can two TCP connections have the same four-tuple?** A: No — the tuple *defines* uniqueness (RFC 793). Identical tuples would be the same connection. Reuse only happens after TIME_WAIT cleanup (with sequence-number safeguards).
14. **Q: What is a "listening socket" vs a "connected socket"?** A: A listening socket is bound to (IP, well-known port) and accepts SYNs; a connected socket results from `accept()` and has the full four-tuple + per-connection state. One listening socket spawns many connected sockets.
15. **Q (production): How do you debug "too many open files" on a server?** A: It's fd exhaustion: each socket = an fd; raise `ulimit -n`, check `fs.file-max`, look for fd leaks (sockets not closed), and count with `ss`/`lsof`. Millions of connections require tuning limits + epoll + careful close logic.
16. **Q: What does `ss -tn state established` show?** A: TCP connections in ESTABLISHED state with their four-tuples — the OS's live view of every socket. `ss -ltnp` shows listening sockets + the owning process. The everyday production diagnostics.
17. **Q (FAANG): Why do load balancers need to rewrite ports (DNAT/SNAT)?** A: They translate the tuple: DNAT maps the VIP:port → backend IP:port; SNAT maps the client's (IP, port) → LB's (IP, port) so replies return through the LB. Both are tuple rewrites — ports are the identity keys of connection tracking.
18. **Q: What is a "raw socket"?** A: A socket that bypasses TCP/UDP to read/write IP packets directly (used by ping/ICMP tools, traceroute, routing daemons, packet sniffers). It's a different *type* (`SOCK_RAW`) addressing IP, not process ports.

## 14. Follow-Up Questions
1. **Q: What is the C10K problem and how does it relate to sockets?** A: C10K = handling 10,000 concurrent connections on one server. It pushed `epoll`/`kqueue` (event-driven I/O) instead of one-thread-per-socket, and socket-buffer/kernel tuning. Sockets are the resource being scaled.
2. **Q: How does the TCP TIME_WAIT state affect ports?** A: A closed connection stays in TIME_WAIT (2×MSL, ~60 s) so late packets die; this *pins* the tuple, and a server closing many connections can exhaust ephemeral ports. Mitigations: `SO_REUSEADDR`, socket reuse, more IPs, or shorter MSL tuning.
3. **Q: What is the difference between a "connection-oriented" port and a UDP "bound" port?** A: TCP: a port participates in connections (tuple-based). UDP: a port is just a destination key; a socket can receive from anyone. The word "bound" means the local (IP, port) assignment either way.
4. **Q: Can a process use port 80 without root?** A: Binding ports <1024 (well-known) requires root/CAP_NET_BIND_SERVICE — a Linux security rule. Solutions: run as root then drop privileges (nginx/apache), set `cap_net_bind_service`, or use systemd `AmbientCapabilities`. The rule exists so unprivileged users can't squat on service ports.
5. **Q: What is port forwarding and when is it used?** A: A NAT rule publishing an internal service on a public port (WAN:443 → 192.168.1.5:443). It's how home servers/IoT devices are reachable from outside — DNAT at the router. Security warning: it exposes a service to the Internet (the primary home-network attack vector).

## 15. Coding Example
```python
# A server socket's lifecycle — ports & sockets in code
import socket

# Server side: bind to a well-known port, listen, accept
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # restart-safe
srv.bind(("0.0.0.0", 8000))          # all interfaces, port 8000 (registered range)
srv.listen(128)                       # accept backlog

conn, addr = srv.accept()            # NEW connected socket per client
print("Accepted:", addr)             # ('192.168.1.10', 54321)  <- client's ephemeral port
data = conn.recv(1024)
conn.sendall(b"echo: " + data)
conn.close(); srv.close()

# Client side: connect() picks an ephemeral source port automatically
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(("127.0.0.1", 8000))
print("Local end:", c.getsockname())  # ('127.0.0.1', 54322)  ephemeral source
```
```bash
# The OS's socket tables — the four-tuple in the wild
$ ss -tn state established
# Recv-Q Send-Q Local Address:Port   Peer Address:Port
# 0      0      10.0.0.5:443         192.168.1.10:54321
# 0      0      10.0.0.5:443         192.168.1.11:59234     (same local port, 2 conns)
$ ss -tulnp | grep -E ':80|:443|:53'    # who's listening (pid + port)
$ lsof -i :8000                         # which process owns a socket
```

## 16. Industry Usage
- **nginx/Envoy/HAProxy**: the server-socket pattern (listen on 80/443, accept millions, epoll-driven) — sockets are their core resource.
- **AWS**: security groups filter by (protocol, port); NLBs track tuples in a connection table; target groups + listeners are port-based. `SO_REUSEADDR`/tuning matter at scale.
- **Kubernetes**: Service → port → pod (ClusterIP:port → targetPort); kube-proxy does tuple-based DNAT. NodePort/LoadBalancer = port publishing semantics.
- **Telecom/core**: BGP (179), OSPF (89 raw), and NTP (123) all bind well-known ports; every control-plane protocol is a socket pair.
- **Observability platforms**: Datadog/New Relic read socket tables (`/proc/net/tcp`, `ss`) to map connections → processes — the "which process owns this port" question is a daily production debugging task.

## 17. References
- RFC 9293 — TCP (socket semantics, tuples): https://www.rfc-editor.org/rfc/rfc9293
- RFC 768 — UDP: https://www.rfc-editor.org/rfc/rfc768
- RFC 6335 — IANA Service Name and Port Number procedures.
- Stevens, *UNIX Network Programming* (the BSD socket API bible), Ch. 4.
- Linux man pages: `socket(2)`, `bind(2)`, `listen(2)`, `accept(2)`, `ss(8)`, `netstat(8)`.

## 18. Cheat Sheet
- Port = 16-bit process address; ranges: 0-1023 well-known, 1024-49151 registered, 49152-65535 ephemeral.
- Socket = end-point; listening (accepting) vs connected (per-client) sockets.
- Four-tuple (srcIP, srcPort, dstIP, dstPort) = TCP connection identity.
- Demux: O(1) tuple hash → socket. Unknown port → RST / ICMP unreachable.
- UDP demux: (dst IP, dst port) — no connection state.
- bind→listen→accept (server); connect (client, auto ephemeral port).
- SO_REUSEADDR for TIME_WAIT restart. Ports <1024 need root/CAP.
- NAT = tuple rewriting (DNAT/SNAT/PAT); ports are translation slots.
- C10K/C100K: epoll + socket tuning + fd limits.

## 19. Quiz
1. A port identifies: a) a host b) a process/service end-point c) an interface d) a route → **b**
2. Well-known port range: a) 49152-65535 b) 1024-49151 c) 0-1023 d) 1-65535 → **c**
3. TCP connection identity: a) dst port b) four-tuple c) src IP d) MAC → **b**
4. `accept()` returns: a) the listening socket b) a new connected socket per client c) the port d) an IP → **b**
5. Unknown TCP port → a) RST b) nothing c) retransmit d) ACK → **a**
6. Ephemeral source ports: a) 0-1023 b) 1024-49151 c) 49152-65535 d) 1-100 → **c**
7. UDP demux key: a) four-tuple b) (dst IP, dst port) c) src only d) none → **b**
8. SO_REUSEADDR helps with: a) NAT b) TIME_WAIT rebind c) port scanning d) congestion → **b**
9. NAT/PAT rewrites: a) only IPs b) IPs + ports c) only ports d) MAC → **b**
10. Binding port <1024 requires: a) nothing b) root/CAP_NET_BIND_SERVICE c) sudo always d) a firewall rule → **b**

## 20. Flashcards
- **Q: What is a port?** → **A:** 16-bit process/service address (0-65535).
- **Q: Four-tuple?** → **A:** (srcIP, srcPort, dstIP, dstPort) — TCP connection identity.
- **Q: Port ranges?** → **A:** 0-1023 well-known, 1024-49151 registered, 49152-65535 ephemeral.
- **Q: Listening vs connected socket?** → **A:** Listening accepts; connected = one specific client tuple.
- **Q: How does the OS demultiplex?** → **A:** O(1) hash of the tuple to the exact socket.
- **Q: What is SO_REUSEADDR?** → **A:** Rebind after TIME_WAIT without "address in use."
- **Q: What does NAT rewrite?** → **A:** IPs + ports (DNAT/SNAT/PAT).

## 21. Revision
Ports (16-bit, 0-65535: well-known/registered/ephemeral) address processes; sockets are OS end-points (listening vs connected). TCP connections are identified by the four-tuple; the OS demultiplexes with an O(1) tuple hash. bind→listen→accept for servers; connect for clients (auto ephemeral port). Unknown ports → RST/ICMP unreachable. SO_REUSEADDR handles TIME_WAIT rebind; ports <1024 need root. NAT rewrites IPs+ports (PAT); connection tables scale to millions via tuples. Debug with `ss`.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a socket vs a port?" | 2 How It Works / 13 Q&A |
| "How does a server serve 1M connections?" | 13 Q&A / 8 Example |
| "What is the four-tuple?" | 13 Q&A / 7 Formal Definition |
| "Port ranges / ephemeral ports?" | 13 Q&A / 9 Internal Working |
| "Why does NAT need source ports?" | 13 Q&A / 14 Follow-Up |
| "How do you debug 'address in use'?" | 13 Q&A / 15 Coding |
| "What is C10K / fd exhaustion?" | 13 Q&A / 10 Time Complexity |
