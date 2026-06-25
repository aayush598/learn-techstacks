# Operating Systems & Networking - 200+ Interview Q&A

## Operating Systems (Q1-Q100)
### Q1: Process vs Thread - detailed comparison?
**Answer:** Process: independent execution unit with own virtual address space, file descriptors, process ID. Thread: lightweight unit within process, shares address space, file descriptors. Context switching processes is expensive (TLB flush, page table switch). Threads cheaper to switch. Communication: processes need IPC (pipes, sockets, shared memory), threads use shared memory. Use processes for isolation, threads for performance.

### Q2: What is a context switch?
**Answer:** OS saves state (registers, program counter, stack pointer, memory map) of current thread/process, loads saved state of another. Triggered by interrupts, system calls, or scheduler preemption. Cost: CPU cycles (saving/loading registers), cache misses (warm cache invalidated). Too many context switches = thrashing (system spends more time switching than doing actual work).

### Q3: Deadlock - four necessary conditions?
**Answer:** (1) Mutual Exclusion - resources cannot be shared. (2) Hold and Wait - process holds resources while waiting for others. (3) No Preemption - resources can't be forcibly taken. (4) Circular Wait - circular chain of processes each waiting for resource held by next. Prevention: break any condition. Avoidance: Banker's algorithm. Detection: resource allocation graph.

### Q4: Virtual memory and paging explained?
**Answer:** Virtual addresses mapped to physical pages via page tables. Pages (typically 4KB) swapped between RAM and disk (swap file). TLB (Translation Lookaside Buffer) caches recent page table entries. Benefits: each process has virtual address space, memory isolation, more memory usable than physically available, shared memory via mapping same physical page.

### Q5: Inter-Process Communication (IPC) methods?
**Answer:** Pipes (unnamed: parent-child, named/FIFO: unrelated processes), Shared Memory (fastest, via mmap/shmget), Message Queues (System V/POSIX), Sockets (network, also local Unix sockets), Signals (async notifications), Semaphores (synchronization). Choose: shared memory for speed, sockets for flexibility, pipes for simplicity.

### Q6: Scheduling algorithms?
**Answer:** FCFS (First-Come First-Served), SJF (Shortest Job First - optimal avg wait), Round Robin (time quantum), Priority Scheduling, Multilevel Queue (different queues for different priority), Multilevel Feedback Queue (processes can move between queues). Linux uses CFS (Completely Fair Scheduler) - virtual runtime, red-black tree.

### Q7: What is thrashing?
**Answer:** System spends majority of time paging/swapping instead of executing. Causes: too many processes, insufficient RAM, high degree of multiprogramming. Symptoms: high disk I/O, low CPU utilization, system unresponsive. Solutions: reduce multiprogramming, add more RAM, adjust working set model.

## Networking (Q101-Q200)
### Q8: OSI vs TCP/IP model - layers and protocols?
**Answer:** OSI (7): Physical (bits, cables), Data Link (frames, MAC, Ethernet, WiFi), Network (packets, IP, routing), Transport (segments, TCP/UDP), Session (dialog control), Presentation (encryption/encoding), Application (HTTP, DNS, SMTP). TCP/IP (4): Network Interface (physical+link), Internet (IP, routing), Transport (TCP/UDP), Application (HTTP, DNS, etc). OSI is conceptual/reference, TCP/IP is practical.

### Q9: TCP vs UDP in detail?
**Answer:** TCP: connection-oriented (3-way handshake), reliable (ACKs, retransmission), ordered (sequence numbers), flow control (sliding window), congestion control (slow start, congestion avoidance). UDP: connectionless, no reliability, no ordering, no retransmission. TCP for reliability-critical (web, email, file transfer). UDP for speed-critical (DNS, streaming, gaming, VoIP).

### Q10: TCP 3-way handshake and 4-way termination?
**Answer:** Connection: (1) Client→SYN→Server. (2) Server→SYN+ACK→Client. (3) Client→ACK→Server. Termination: (1) Client→FIN→Server. (2) Server→ACK→Client. (3) Server→FIN→Client. (4) Client→ACK→Server. TIME_WAIT state (2*MSL) ensures ACK reaches server, handles delayed packets.

### Q11: HTTP/1.1 vs HTTP/2 vs HTTP/3?
**Answer:** HTTP/1.1: text protocol, one request per connection, head-of-line blocking, keep-alive for connection reuse. HTTP/2: binary, multiplexed (multiple streams over single connection), server push, header compression (HPACK), prioritized streams. HTTP/3: over QUIC (UDP-based), 0-RTT connection, built-in encryption (TLS 1.3), no head-of-line blocking at transport level, better loss handling.

### Q12: What happens when you type google.com in browser?
**Answer:** (1) Browser checks cache (DNS, page resources). (2) DNS resolution (browser → OS → router → ISP DNS → root → TLD → authoritative → IP). (3) TCP 3-way handshake (or QUIC for HTTP/3). (4) TLS handshake (certificate verification, key exchange). (5) HTTP request (GET /, headers). (6) Server processes, returns HTML. (7) Browser parses HTML, builds DOM, loads resources (CSS, JS, images). (8) Renders page.

### Q13: CORS - what is it and how does it work?
**Answer:** Cross-Origin Resource Sharing. Browser security that blocks cross-origin requests by default. Server must include `Access-Control-Allow-Origin` header. Simple requests (GET, POST with simple content types) sent directly. Preflight requests (OPTIONS) for non-simple requests (PUT, DELETE, custom headers, non-simple content types). Preflight checks allowed methods (`Access-Control-Allow-Methods`) and headers.

### Q14: Load balancer types and algorithms?
**Answer:** Types: Layer 4 (TCP/UDP - faster, less intelligent), Layer 7 (HTTP/HTTPS - can route based on URL, cookies, headers). Algorithms: Round Robin, Least Connections, IP Hash (sticky sessions), Weighted (different capacity servers), Random. Health checks required (active or passive). Examples: Nginx, HAProxy, AWS ALB/NLB.

### Q15: DNS record types?
**Answer:** A (IPv4 address), AAAA (IPv6), CNAME (alias to another domain), MX (mail server), TXT (text, SPF, DKIM), NS (nameserver), SOA (start of authority), PTR (reverse lookup), SRV (service location). CNAME cannot point to another CNAME (CNAME flattening solves this).

### Q16: CDN - how does it work?
**Answer:** Content Delivery Network - distributed servers at edge locations. User requests content → routed to nearest edge server. Static content cached at edge (TTL-based). Dynamic content routed to origin, cached edge-side. Benefits: lower latency, origin offload, DDoS protection. Providers: CloudFlare, Akamai, AWS CloudFront, Fastly.

### Q17: What is a reverse proxy?
**Answer:** Server that sits between clients and backend servers. Handles: load balancing, SSL termination, caching, compression, security (hide backend identity), request routing. Examples: Nginx, HAProxy, Traefik, Caddy. Compare to forward proxy (used by clients to access internet).
