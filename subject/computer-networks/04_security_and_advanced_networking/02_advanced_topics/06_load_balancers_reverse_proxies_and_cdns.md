# Load Balancers, Reverse Proxies and CDNs — 100 Interview Q&A

## Q1: What is a load balancer and why is it necessary?

**A:** A load balancer is a device or software that distributes incoming network traffic across multiple backend servers (targets) to ensure no single server is overwhelmed. It sits in front of the servers and acts as a reverse proxy from the client's perspective — clients connect to the load balancer's IP address, never to the individual servers directly. The load balancer then selects a backend based on its algorithm and forwards the connection.

The necessity arises from three constraints. First, scalability: a single server cannot handle infinite traffic, so multiple servers are deployed and the load balancer distributes requests across them. Second, availability: if one server fails, the load balancer routes traffic to the remaining healthy servers, making the failure transparent to users. Third, flexibility: servers can be added or removed without changing any client configuration — the load balancer abstracts the server pool.

A senior answer emphasizes that the load balancer is more than a traffic splitter: it is the single point of policy control for the entire server pool. Health checks, session handling, SSL termination, rate limiting, and observability all converge at the load balancer. Choosing the wrong type or misconfiguring it creates a bottleneck or a single point of failure that negates the purpose of having multiple servers.

## Q2: What is the difference between L4 and L7 load balancing?

**A:** Layer 4 (L4) load balancing operates at the transport layer — it makes routing decisions based on IP address and TCP/UDP port numbers without inspecting the content of the connection. L4 load balancers are typically stateless packet-forwarding devices: they receive a packet, select a backend based on the 4-tuple (source IP, source port, destination IP, destination port), and forward it — often using NAT or DSR (Direct Server Return) to bypass themselves on the return path. Because they do not inspect payload, L4 balancers are extremely fast and throughput-oriented.

Layer 7 (L7) load balancing operates at the application layer — it inspects HTTP headers, cookies, URLs, TLS SNI, or other application-layer data to make routing decisions. An L7 load balancer terminates the TCP connection from the client, inspects the request, and creates a new connection to the appropriate backend. This enables content-based routing (route `/api` to API servers and `/static` to CDN servers), header-based routing, and request manipulation (rewrite headers, inject cookies, compress responses).

The trade-off is performance versus intelligence. L4 balancers have lower latency and higher throughput because they do not parse application data; L7 balancers are slower per request but can make far more sophisticated routing decisions. A common production architecture uses L4 at the edge (handling raw throughput, DDoS absorption) and L7 behind it (handling application-aware routing, SSL offload, caching).

## Q3: What are the common load balancing algorithms?

**A:** Round Robin distributes requests sequentially across servers — server 1 gets request 1, server 2 gets request 2, and so on. It is the simplest algorithm and works well when all servers are roughly equal in capacity and all requests are roughly equal in cost. Weighted Round Robin assigns each server a weight proportional to its capacity, so a server with weight 3 receives three times as many requests as a server with weight 1.

Least Connections sends each new request to the server with the fewest active connections at that moment. This adapts to uneven request durations — a server handling long-lived WebSocket connections naturally accumulates fewer new connections than one handling short HTTP requests. Least Connections is the default recommendation for workloads where request duration varies significantly.

Least Response Time selects the server with the lowest average response time and fewest active connections, combining latency awareness with load awareness. It is the most responsive algorithm but requires the load balancer to track per-server latency metrics, adding overhead. Other algorithms include IP Hash (hashing the client IP to consistently route the same client to the same server — useful for session affinity without cookies), Random (selecting a backend at random — statistically even at scale), and Resource-Based (querying servers for their current load via an agent and making real-time decisions).

## Q4: What are health checks and why are they critical?

**A:** Health checks are periodic probes the load balancer sends to each backend server to determine whether it is alive and capable of serving traffic. A simple TCP health check verifies that the server's port is accepting connections. An HTTP health check sends a request to a specific path (e.g., `/health`) and validates the response code (200 OK) and optionally the response body. An advanced check can validate application-specific state (database connectivity, cache warm-up, disk space).

Health checks are critical because without them, the load balancer sends traffic to dead or degraded servers. A server that has crashed but whose TCP port still appears open (or whose process is hung) would receive traffic and cause user-visible errors. Health checks detect this and remove the server from the pool until it recovers — typically after a configurable number of consecutive failures (to avoid flapping on transient issues) and a recovery threshold (to ensure the server is truly stable before returning to the pool).

The senior design question is the check's endpoint: `/health` must be lightweight, fast, and reflect real readiness. A health endpoint that always returns 200 regardless of backend state is useless. A health endpoint that queries the database adds latency to every check cycle and can itself become a failure source. The best practice is a tiered health model: a lightweight liveness check (is the process alive?) and a deeper readiness check (can the server accept new connections?) with separate thresholds.

## Q5: What is session affinity (sticky sessions) and when should it be used?

**A:** Session affinity (sticky sessions) ensures that all requests from a particular client are routed to the same backend server for the duration of a session. The load balancer inspects a session identifier — typically a cookie (e.g., `SERVERID=server3`), a session token, or the client's IP address — and consistently routes to the same server. This solves the problem of server-side session state: if a user logs in and the session data is stored locally on server 2, subsequent requests must reach server 2 to access that session.

When it should be used: legacy applications that store session state locally and cannot be refactored to use shared session stores (Redis, database). When session data is critical to the request (shopping carts in e-commerce, multi-step forms) and the application cannot tolerate session loss from server failover. In these cases, sticky sessions are a pragmatic bridge that enables load balancing without rewriting the application.

The senior caveat is that sticky sessions undermine the core benefits of load balancing. They create uneven load distribution (long-lived sessions accumulate on one server), make scaling uneven (adding a server does not help existing sessions), and create a dependency on specific servers for failover (if the sticky server dies, the session is lost). The preferred architecture is stateless backends with shared session storage — every server can handle every request, and sticky sessions become unnecessary. Use sticky sessions as a temporary measure while migrating to a stateless design, not as a permanent architecture.

## Q6: What is a reverse proxy and how does it differ from a forward proxy?

**A:** A reverse proxy sits in front of servers and intercepts client requests on behalf of the servers. From the client's perspective, the reverse proxy IS the server — it receives the request, processes it (terminating SSL, caching, filtering, rate-limiting), and forwards it to an appropriate backend server. The client never sees the backend servers' IP addresses. Common reverse proxies include Nginx, HAProxy, Envoy, and cloud load balancers (ALB, Cloudflare LB).

A forward proxy sits in front of clients and intercepts outbound requests on behalf of the clients. It acts on behalf of the client — routing their requests, filtering content, caching, or anonymizing their identity. Corporate web proxies, VPN concentrators, and Tor exit nodes are forward proxies. The server never sees the original client — it sees the forward proxy's address.

The architectural distinction: a reverse proxy protects and manages servers; a forward proxy protects and manages clients. A reverse proxy enables server-side scalability, security (hiding backend topology), and performance (caching, compression). A forward proxy enables client-side policy enforcement (URL filtering, DLP), privacy (masking client IP), and access control (allowing/denying outbound traffic). Both are intermediaries, but they serve opposite ends of the connection.

## Q7: What is SSL/TLS offloading and why is it done at the load balancer?

**A:** SSL/TLS offloading is the process of terminating the TLS handshake and decrypting client traffic at the load balancer (or reverse proxy) rather than on every backend server. The load balancer handles the computationally expensive operations — key exchange, certificate management, encryption/decryption — and forwards plain HTTP to the backend servers. This reduces the CPU burden on each server and centralizes certificate management to a single point.

The benefits are both performance and operational. SSL/TLS handshakes are CPU-intensive (asymmetric cryptography for key exchange, symmetric cryptography for bulk data). Offloading concentrates this cost on a device designed for it (hardware-accelerated SSL) rather than spreading it across application servers. Centralized certificate management means one place to renew certificates, configure cipher suites, and enforce TLS versions — rather than configuring TLS on dozens or hundreds of servers.

The security trade-off: traffic between the load balancer and backends is unencrypted (plain HTTP) unless re-encrypted (HTTPS to the backends). If the backend network is trusted (same VLAN, private cloud), this is usually acceptable. If the traffic traverses untrusted networks, re-encryption (TLS pass-through or TLS from LB to backend) is necessary. A senior design always considers the trust boundary: where does encryption need to exist, and who holds the keys?

## Q8: What is CDN edge caching and how does it improve performance?

**A:** A Content Delivery Network (CDN) distributes copies of static (and increasingly dynamic) content to edge servers located in data centers close to end users. When a user requests a cached asset (image, CSS, JavaScript, video), the CDN serves it from the nearest edge location rather than from the origin server — dramatically reducing latency (round-trip time) and offloading bandwidth from the origin.

The performance improvement comes from two physics: distance and congestion. Latency is dominated by propagation delay (speed of light in fiber, ~5 ms per 1000 km), so a user in Mumbai accessing a server in Virginia adds ~150 ms round-trip just for distance. A CDN edge in Mumbai serves the same content in <5 ms. CDN edge servers also absorb traffic spikes (viral content, DDoS) that would otherwise hit the origin directly.

A senior CDN architecture considers cache hierarchy: edge cache → regional cache → origin shield → origin. Each tier reduces origin load. The cache's freshness model (TTL, ETags, Cache-Control headers, stale-while-revalidate) determines how content stays current. Cache invalidation (purge, tag-based purge) is the hardest problem — a stale cache serving incorrect content is worse than no cache. Modern CDNs also cache dynamic content (API responses, HTML pages) using edge compute (Workers, Lambda@Edge), blurring the line between CDN and application platform.

## Q9: What is origin shielding in a CDN?

**A:** Origin shielding is a CDN architecture pattern where a dedicated intermediate cache (the "shield") sits between the CDN's edge caches and the origin server. Instead of every edge location pulling content directly from the origin on a cache miss, the edge fetches from the shield, which fetches from the origin. The shield absorbs the thundering-herd effect — when a popular asset expires from all edge caches simultaneously, only one request reaches the origin rather than hundreds.

The benefit is origin protection and cost reduction. Origin servers (especially those backed by databases, dynamic rendering, or compute) have finite capacity and cost per request. Without shielding, a cache miss at every edge location generates a proportional number of origin requests. With shielding, the origin sees requests from only the shield locations (typically 3-10 globally), regardless of how many edge locations exist. This reduces origin bandwidth costs, origin server CPU load, and database query volume.

The senior design trade-off is latency versus origin load. Shielding adds one extra hop (edge → shield → origin) on a cache miss, increasing the latency for the first request after expiration. The trade-off is almost always worth it: the shield amortizes origin load across thousands of edges, and the latency penalty is a few milliseconds on miss (the shield is on a fast backbone). The key is selecting shield locations strategically — placing them in regions with high edge density and low-latency paths to the origin.

## Q10: What is the difference between a load balancer and a reverse proxy?

**A:** The terms overlap significantly in practice, but the distinction is scope and primary purpose. A load balancer's primary function is distributing traffic across multiple backends for scalability and availability. A reverse proxy's primary function is mediating between clients and servers for security, performance, and protocol transformation — it may forward to a single server or a pool, but its value is the mediation layer, not the distribution.

In practice, modern load balancers ARE reverse proxies (Nginx, HAProxy, Envoy, ALB all terminate SSL, cache, compress, and route). And most reverse proxies can distribute across backends (Nginx's upstream blocks, HAProxy's backend pools). The terms are functionally interchangeable in most architectures. The difference is emphasis: when someone says "load balancer," they mean scaling and availability; when someone says "reverse proxy," they mean protocol mediation, caching, and security.

A senior answer recognizes that the tool's value is in its configuration, not its label. An Nginx instance used as a reverse proxy with SSL termination, caching, and rate limiting is performing load-balancer functions. An ALB performing content-based routing is performing reverse-proxy functions. The design question is not "load balancer or reverse proxy?" but "what capabilities do I need at the edge?" — and the answer is usually both, implemented in the same device or in a layered architecture (L4 LB at the edge, L7 reverse proxy behind it).

## Q11: What is DDoS protection and how do load balancers contribute?

**A:** Distributed Denial of Service (DDoS) attacks overwhelm a target with traffic from many sources — volumetric floods (UDP, DNS amplification), protocol attacks (SYN floods, ICMP floods), and application-layer attacks (HTTP floods, slowloris). Load balancers contribute to DDoS defense at multiple layers: L4 load balancers can absorb volumetric attacks through bandwidth capacity and rate limiting; L7 load balancers can detect and filter application-layer attacks by inspecting request patterns, rate limiting per-IP, and challenging suspicious traffic (CAPTCHA, JavaScript challenges).

At L4, techniques include SYN cookies (responding to SYN floods without allocating state), connection rate limiting per source IP, and dropping traffic from known-bad sources (threat intelligence feeds). At L7, techniques include request rate limiting per IP/API key, detecting slowloris (incomplete connections held open), validating HTTP headers and user agents, and using challenge-response mechanisms to distinguish humans from bots.

The senior architectural point is that no single device stops a DDoS attack at scale. The layered defense is: CDN/Anycast at the edge (absorb volumetric), cloud DDoS protection (Cloudflare, Akamai Prolexic) scrubbing upstream, load balancer at the data center (application-layer filtering), and WAF (web application firewall) for deep request inspection. A load balancer alone cannot stop a 1 Tbps volumetric flood — it lacks the bandwidth. The load balancer's role is the last line of defense at L7, where it sees application traffic patterns that volumetric scrubbers miss.

## Q12: What is connection draining and why is it important?

**A:** Connection draining (also called graceful shutdown or in-flight request completion) is the process by which a load balancer stops sending new connections to a server that is being removed from the pool while allowing existing (in-flight) connections to complete naturally. When a server is marked for removal — either manually (maintenance window) or automatically (health check failure) — the load balancer stops routing new traffic to it but does not abruptly terminate active connections.

This is important because abruptly killing active connections causes user-visible errors: HTTP requests return 502/503, database transactions fail mid-operation, file uploads are corrupted, and WebSocket connections drop. Connection draining gives existing requests time to complete — typically with a configurable timeout (e.g., 300 seconds) — after which any remaining connections are forcibly terminated. New requests are routed to remaining healthy servers.

A senior operational practice: connection draining is essential during rolling deployments and maintenance windows. During a deployment, the old server is placed in draining state; once all in-flight requests complete (or the timeout expires), the server is removed, updated, and re-added to the pool. This achieves zero-downtime deployments — but only if the drain timeout is long enough for the longest expected request. A drain timeout shorter than the longest request duration causes premature termination; too long delays the deployment.

## Q13: What is the difference between active-passive and active-active load balancing?

**A:** Active-passive load balancing has one server (or group) handling all traffic while the other stands by, ready to take over if the active fails. The passive server receives no traffic during normal operation — it exists solely for failover. This simplifies configuration (no need to synchronize traffic splitting) but wastes the passive server's capacity. Health checks monitor the active; if it fails, the passive is promoted and begins receiving traffic. Protocols like VRRP/HSRP implement this at the gateway level.

Active-active load balancing has all servers (or groups) handling traffic simultaneously. Traffic is distributed across all active servers by the load balancer, utilizing the full capacity of every server. This provides both scalability (more aggregate throughput) and resilience (if one server fails, the others absorb its traffic). Active-active is the standard for production deployments where capacity and availability are both priorities.

The senior design consideration is state: active-active requires that every server can handle any request, which means session state must be shared (Redis, database) or stateless (JWT tokens, no server-side session). Active-passive avoids this constraint because the passive server can maintain its own state — but at the cost of half-wasted capacity. The trend is overwhelmingly toward active-active with shared state, because idle capacity is a cost that scales linearly with redundancy.

## Q14: What is a health check endpoint and how should it be designed?

**A:** A health check endpoint is a URL on the backend server that the load balancer periodically requests to determine the server's health. A well-designed health check endpoint is lightweight (no heavy database queries, no external API calls), fast (returns in <100ms), and reflects real readiness (returns 200 only if the server can actually serve traffic). A bad health check endpoint is either too shallow (always returns 200 even when the server is degraded) or too deep (queries the database, causing health checks to themselves become a load problem).

Design principles: separate liveness (is the process running?) from readiness (can it accept new connections?). Liveness should be a simple in-memory check — return 200 if the process is up. Readiness can validate dependencies — return 200 only if the database connection pool is warm, the cache is populated, and the disk is writable. The load balancer should use the readiness endpoint for routing decisions and the liveness endpoint for restart decisions.

A senior anti-pattern is the "always healthy" health check — where developers set the endpoint to always return 200 to avoid health-check-related restarts. This defeats the purpose entirely: a server that returns 200 but cannot serve requests (database connection exhausted, disk full) will receive traffic and fail. The health endpoint must be honest about the server's ability to do work, even if that means the server is removed from the pool. Better to have fewer healthy servers than broken servers receiving traffic.

## Q15: What is a CDN cache hit ratio and how do you optimize it?

**A:** The cache hit ratio (CHR) is the percentage of requests served from CDN edge cache (cache hit) versus the percentage that required a fetch from the origin (cache miss). A CHR of 95% means 95% of requests were served from cache without touching the origin. CHR directly correlates with origin load reduction, latency improvement, and cost savings (CDN egress and origin bandwidth are both cheaper when served from cache).

Optimizing CHR requires understanding cacheability. Static assets (images, CSS, JavaScript, fonts) are highly cacheable — long TTLs (days to months) with immutable content. Dynamic content (API responses, HTML pages) can be cacheable if the response varies only by URL and is not user-specific. Strategies include: setting appropriate Cache-Control headers (max-age, s-maxage for CDN), using ETags for conditional requests, stale-while-revalidate (serving slightly stale content while refreshing in the background), and cache key design (ensuring query parameters that change content are included in the cache key).

The senior operational point: a high CHR is good, but an excessively high CHR may indicate stale content being served. The optimization is not "maximize CHR" but "maximize CHR while maintaining freshness." Cache purging (instant invalidation), short TTLs for time-sensitive content, and cache-control headers that balance freshness with cacheability are the knobs. Monitoring CHR alongside origin latency and origin error rates gives the complete picture — a 99% CHR with rising origin errors means the 1% of misses is causing problems.

## Q16: What is Global Server Load Balancing (GSLB)?

**A:** Global Server Load Balancing (GSLB) distributes traffic across geographically dispersed data centers or regions. Unlike a local load balancer that manages servers in one data center, GSLB makes routing decisions at the DNS or Anycast layer to direct users to the nearest or most available data center. GSLB is the mechanism that enables multi-region deployment, disaster recovery, and geographic latency optimization.

GSLB implementations: DNS-based (the GSLB appliance answers DNS queries with the IP of the best data center, based on health, proximity, and load), Anycast-based (multiple data centers advertise the same IP prefix via BGP, and routing naturally directs users to the nearest data center), and HTTP-redirect-based (the edge server redirects the client to the best data center URL). Each approach has trade-offs: DNS-based is simple but subject to DNS caching; Anycast is fast but complex to operate; HTTP-redirect is application-aware but adds latency.

The senior design consideration is that GSLB is not just load balancing — it is a business-continuity architecture. It must handle data center failures (route all traffic to surviving DCs), regional outages (shift traffic away from affected regions), and capacity overflow (send users to the least-loaded DC). The GSLB health model must monitor not just server health but data center health — connectivity to databases, storage, and inter-DC links. A GSLB that routes users to a healthy-looking DC whose database is actually down has failed.

## Q17: What is Anycast and how is it used for load balancing?

**A:** Anycast is a network addressing and routing methodology where multiple servers in different geographic locations share the same IP address. BGP advertises the same prefix from each location, and the Internet's routing infrastructure directs each client to the topologically nearest server. This achieves natural load distribution — users in Tokyo reach the Tokyo server, users in London reach the London server — without any application-layer logic.

Anycast is used for DNS (every DNS root server uses Anycast), CDN edge delivery (Cloudflare, Akamai, Fastly all Anycast their edge IPs), and DDoS absorption (attack traffic is distributed across all Anycast locations rather than concentrated at one). The fundamental advantage is that Anycast distributes traffic at the network layer, which is orders of magnitude faster and more scalable than application-layer load balancing.

The senior limitation: Anycast provides geographic distribution and DDoS resilience but not fine-grained load balancing. If one Anycast location is overloaded while another is idle, BGP does not automatically redirect traffic — BGP routing is based on path length, not server load. True load-aware Anycast requires additional mechanisms (application-layer redirects, BGP community manipulation). Anycast also requires that the service be stateless or have location-local state, because a user's next request may reach a different Anycast location.

## Q18: What is the difference between a hardware and software load balancer?

**A:** Hardware load balancers are dedicated physical appliances with custom ASICs or FPGAs designed for high-throughput packet processing. They offer guaranteed performance (measured in Gbps, concurrent connections, transactions per second), hardware-accelerated SSL offload, and often include advanced features (DDoS protection, WAF, GSLB). F5 BIG-IP, Citrix ADC, and A10 Networks are examples. They are expensive but predictable in performance.

Software load balancers run as applications on commodity servers (physical or virtual). They leverage the server's CPU and NIC for packet processing and are deployed as VMs, containers, or bare-metal processes. Nginx, HAProxy, Envoy, Traefik, and cloud-native solutions (Kubernetes Services, ALB) are examples. They are cheaper, more flexible, and more cloud-native, but their performance depends on the underlying hardware.

The senior trend: software load balancers have largely displaced hardware in cloud and container environments because they are programmable, API-driven, and scale horizontally. Hardware load balancers retain their place in high-throughput, low-latency on-premises environments where predictable performance matters (financial trading, telecom). The hybrid reality is that most enterprises run software LBs in the cloud and hardware LBs on-prem, with the management complexity of operating both. The cost-performance crossover point shifts toward software every year as commodity hardware improves.

## Q19: What is rate limiting and how is it implemented at a load balancer?

**A:** Rate limiting restricts the number of requests a client (identified by IP, API key, session, or user) can make within a time window. It prevents abuse (credential stuffing, scraping, DDoS), protects backend servers from being overwhelmed, and enforces fair usage across clients. When the rate limit is exceeded, the load balancer returns a 429 Too Many Requests response (or drops the connection) and does not forward the request to the backend.

Implementation approaches: fixed window (count requests in fixed time buckets — simple but allows bursts at window boundaries), sliding window (tracks requests over a rolling time window — smoother but more memory-intensive), token bucket (each client gets tokens at a fixed rate; each request consumes a token; requests are rejected when the bucket is empty — allows controlled bursts), and leaky bucket (requests enter a queue and are processed at a fixed rate — smooths bursts but adds latency).

A senior design choice is the rate limit key: per-IP limits are easy but penalize users behind NAT (entire office behind one IP gets one limit). Per-user or per-API-key limits are fairer but require authentication. Tiered limits (free tier = 100 req/min, paid tier = 1000 req/min) require integration with the billing system. The rate limiter must also handle distributed rate limiting across multiple load balancer instances — a single LB's counter is meaningless when traffic is distributed across 20 LBs. Centralized rate-limit state (Redis, shared memory) solves this at the cost of added latency.

## Q20: What is a circuit breaker pattern in load balancing?

**A:** The circuit breaker pattern protects backend services from cascading failures by detecting when a backend is failing and temporarily stopping requests to it. It works like an electrical circuit breaker: when failures exceed a threshold (e.g., 50% error rate in 30 seconds), the circuit "opens" and all requests are immediately failed (or routed elsewhere) without attempting the backend. After a configurable cooldown period, the circuit enters "half-open" state and allows a limited number of probe requests through — if they succeed, the circuit closes; if they fail, it opens again.

The purpose is fail-fast behavior. Without a circuit breaker, when a backend starts failing, every request to it adds to the queue, increases latency (waiting for timeout), consumes connection pool resources, and potentially overwhelms the backend further — a cascading failure. The circuit breaker stops this by failing fast and routing traffic to healthy backends or returning cached/default responses.

A senior implementation considers: the failure threshold (too low causes flapping; too high allows sustained errors), the cooldown period (too short causes premature reconnection; too long delays recovery), and the fallback behavior (return cached data, return a default response, queue for retry). The circuit breaker is also a可观测性 tool — its state transitions (closed → open → half-open) are critical operational signals that should be monitored and alerted.

## Q21: What is a load balancer's connection table and why does it matter?

**A:** The connection table (also called session table or NAT table) tracks all active connections passing through the load balancer. Each entry maps the client-side tuple (source IP, source port, destination IP, destination port) to the backend-side tuple (backend IP, backend port), enabling the load balancer to forward return traffic to the correct client. For L4 load balancers, this table is the core state; for L7 load balancers, it also tracks HTTP session state (if sticky sessions are enabled).

The table matters for three reasons. First, capacity: the table has finite size (hardware LBs allocate millions of entries; software LBs are limited by memory). If the table fills, new connections are dropped. Second, performance: table lookups must be fast (hardware LBs use TCAM for O(1) lookups; software LBs use hash tables with varying performance). Third, security: the table is a target for exhaustion attacks (SYN floods that fill the table with half-open connections).

A senior monitoring practice: the connection table utilization should be tracked as a key metric. A table at 80% capacity is a warning; at 95% is an emergency. Table growth also correlates with connection rate and duration — long-lived connections (WebSocket, database) consume table entries for extended periods. Tuning connection timeouts (idle timeout, established timeout) balances table capacity against legitimate long-lived connections.

## Q22: What is TCP connection multiplexing and how does it optimize load balancing?

**A:** TCP connection multiplexing (also called connection pooling or keep-alive reuse) is the technique where the load balancer reuses existing TCP connections to backend servers rather than creating a new connection for each client request. When a client request arrives, the load balancer checks if an existing connection to the selected backend is idle and available — if so, it reuses that connection. If not, it creates a new one. This reduces the overhead of TCP handshakes (3-way handshake, SYN/ACK) and TLS handshakes (if TLS is terminated at the backend).

The optimization is most significant for short-lived HTTP/1.1 connections. Without multiplexing, every HTTP request creates a new TCP connection: SYN, SYN-ACK, ACK, request, response, FIN — all for a single request. With multiplexing and HTTP keep-alive, multiple requests share one TCP connection, eliminating the handshake overhead. For HTTP/2, multiplexing is built into the protocol — multiple streams share one TCP connection — and the load balancer's connection pool extends this efficiency.

The senior tuning consideration: the load balancer's connection pool size (connections per backend) must be sized for the expected concurrency. Too few connections cause queuing (requests wait for an available connection); too many connections overwhelm the backend (each TCP connection consumes memory and file descriptors on the backend). Monitoring backend connection counts, connection wait times, and connection reuse rates helps right-size the pool.

## Q23: What is WebSocket load balancing and what challenges does it present?

**A:** WebSocket connections are persistent, full-duplex connections that start as an HTTP upgrade request and then maintain a long-lived bidirectional channel. Load balancing WebSockets differs from HTTP because: (1) the connection is long-lived (minutes, hours, or days), so sticky sessions are often required to maintain state; (2) the connection is bidirectional — the server can push data to the client at any time; (3) the initial HTTP upgrade must be routed to the correct backend, and all subsequent WebSocket frames on that connection must follow the same path.

Challenges: connection draining becomes critical — a server being removed must wait for all its WebSocket connections to close (which may never happen if clients do not disconnect). Health checks must account for WebSocket connections (a server may be "healthy" for HTTP health checks but its WebSocket connections may be degraded). And scaling WebSocket servers requires careful session management — a user connected to server 1 via WebSocket cannot be seamlessly moved to server 2 without losing state.

A senior architecture for WebSocket load balancing: use L7 load balancers that can inspect the HTTP upgrade request and route based on headers (e.g., a session token in the query string). Enable sticky sessions at the load balancer. Use connection draining with generous timeouts during deployments. For horizontal scaling, design the application to support WebSocket connection migration (share session state externally) or accept that reconnection is part of the scaling event.

## Q24: What is a WAF (Web Application Firewall) and how does it relate to load balancing?

**A:** A Web Application Firewall (WAF) inspects HTTP/HTTPS traffic at the application layer and filters requests based on security rules — blocking SQL injection, cross-site scripting (XSS), path traversal, file inclusion, and other OWASP Top 10 threats. A WAF operates as a reverse proxy in front of the application, analyzing each request and response for malicious patterns before forwarding them to the backend.

The relationship to load balancing is layered: the WAF typically sits behind the load balancer (or is integrated into the same device). The load balancer handles L4 distribution and SSL termination; the WAF handles L7 security inspection. In cloud environments, WAF and load balancer are often the same service (AWS ALB + WAF, Cloudflare LB + WAF). In on-premises deployments, the WAF may be a separate appliance (F5 ASM, Imperva) placed behind the load balancer.

A senior architecture decision is WAF placement and mode: inline (all traffic passes through the WAF — can block but adds latency) versus monitoring (WAF inspects but does not block — useful for tuning rules without impact). The WAF must be tuned to avoid false positives (legitimate requests blocked) which cause outages as severe as the attacks it prevents. Rule sets must be updated regularly, and the WAF must handle TLS inspection (decryption, inspection, re-encryption) without becoming a performance bottleneck.

## Q25: What is server-side load balancing versus client-side load balancing?

**A:** Server-side load balancer places the load balancer between the client and the server pool — the client connects to the load balancer's IP, and the load balancer distributes requests to backends. This is the standard model for HTTP, HTTPS, and most application traffic. The client has no awareness of individual servers; the load balancer is the single entry point.

Client-side load balancing distributes the load balancing intelligence to the client application itself. The client maintains a list of available servers and selects one for each request using a local load balancing algorithm (round robin, least connections, random). gRPC's built-in load balancing, Netflix Ribbon, and custom client-side LB libraries implement this model. The client makes direct connections to servers — no intermediary load balancer.

The trade-off: server-side LB centralizes policy (easier to manage, update, and monitor) but adds a hop (latency, potential bottleneck). Client-side LB eliminates the intermediary hop and potential bottleneck but distributes policy to every client (harder to update, inconsistent versions, client-side bugs affect routing). A senior architecture uses both: server-side LB for external-facing traffic (public Internet, where the LB also handles SSL, DDoS, and WAF), client-side LB for internal service-to-service traffic (microservices, where the overhead of an LB hop per call is unacceptable).


## Q26: What is a CDN cache key and why does its design matter?

**A:** A CDN cache key is the identifier used to look up and store cached content on the edge. By default, the cache key is the full request URL (including path, query string, and sometimes the host header). Two requests with different URLs are cached separately — even if the content is identical. The cache key design determines what gets cached, what is deduplicated, and what causes cache misses.

The design matters because naive cache keys waste cache space and increase miss rates. For example, a URL with a session-tracking query parameter (`?session=abc123`) causes every user's request to be cached separately — even though the content is the same. Stripping non-functional query parameters from the cache key (normalizing the URL) improves hit ratio. Conversely, query parameters that change content (e.g., `?lang=fr` vs. `?lang=en`) must be included in the cache key to avoid serving wrong-language content.

A senior CDN cache key strategy: normalize URLs (remove tracking parameters, sort query parameters), include content-variant parameters (language, device type, region) when they affect the response, use cache key prefixes or tags for programmatic invalidation, and test cache key behavior under real traffic patterns. The cache key is the DNA of the CDN's caching behavior — a poorly designed cache key causes either cache bloat (too many unique keys) or stale content (too few keys).

## Q27: What is cache invalidation and why is it called the hardest problem?

**A:** Cache invalidation is the process of removing or refreshing cached content before its TTL expires — because the origin has changed and the cached version is now stale. When content is updated (a product page changes, a news article is corrected, a user uploads a new profile picture), the CDN's cached copy must be purged or refreshed to serve the updated content. Without invalidation, users see stale content until the TTL naturally expires.

The approaches: TTL-based (content expires automatically after a configured time — simple but introduces staleness), purge-by-URL (explicitly delete a specific URL from all edge locations — fast but requires knowing every URL that changed), purge-by-tag (invalidate all content tagged with a specific label — more flexible but requires tagging infrastructure), and surrogate-key purge (purge a set of keys that map to multiple URLs — the most granular and powerful). Each approach trades speed, granularity, and operational complexity.

It is called the hardest problem because: (1) CDN caches are globally distributed — a purge must propagate to every edge location (potentially hundreds) within seconds; (2) intermediate caches (browser cache, ISP cache, regional CDN cache) may serve stale content even after the CDN purge; (3) timing is critical — purging too early causes cache misses that overload the origin; purging too late serves stale content. The operational discipline is designing content with invalidation in mind: use unique URLs for non-cacheable content, tag cacheable content for bulk invalidation, and test purge propagation times with real traffic.

## Q28: What is a CDN's TTL (Time to Live) and how should it be configured?

**A:** TTL (Time to Live) is the duration for which cached content is considered fresh and served from cache without checking the origin. It is set by the origin server via HTTP headers: `Cache-Control: max-age=3600` (content is fresh for 1 hour), `Cache-Control: s-maxage=86400` (CDN-specific TTL of 1 day), or `Expires: <date>` (legacy). When the TTL expires, the next request triggers a cache miss — the CDN fetches the content from the origin and caches it again with a new TTL.

TTL configuration is a freshness-versus-staleness trade-off. Long TTLs (hours, days) maximize cache hit ratio and minimize origin load, but serve stale content longer if the origin changes. Short TTLs (seconds, minutes) keep content fresh but increase cache misses and origin load. For static assets (images, CSS, JavaScript with hashed filenames), long TTLs (months) are safe because the URL changes with content. For dynamic content (API responses, HTML pages), shorter TTLs or stale-while-revalidate strategies are necessary.

A senior TTL strategy: use `immutable` for versioned static assets (hashed filenames that change when content changes — cache indefinitely until the URL changes). Use `stale-while-revalidate=60` for semi-dynamic content (serve the cached version for up to 60 seconds after expiration while refreshing in the background — eliminating the latency penalty of cache misses). Use `no-cache` for content that must always be revalidated (personalized pages, real-time data). The TTL is not a single number — it is a per-content-type policy that balances freshness, performance, and cost.

## Q29: What is SSL/TLS termination and how does it work at a CDN edge?

**A:** SSL/TLS termination at the CDN edge means the CDN terminates the TLS handshake from the client, decrypts the request, and serves cached or origin-fetched content over TLS to the client. The CDN manages the TLS certificate (provisioned via the CDN dashboard or API), performs the key exchange (handling modern cipher suites, TLS 1.3, and client certificate validation), and re-encrypts responses to the client. The origin server may receive plain HTTP (if the CDN terminates TLS at the edge) or HTTPS (if the CDN re-encrypts to the origin).

The benefit is global TLS termination without deploying certificates to every origin server. The CDN handles certificate renewal, cipher suite management, HSTS headers, and TLS version enforcement — all centrally. Clients connect to the nearest edge via TLS, and the edge communicates with the origin over the CDN's private backbone (which may or may not be encrypted).

A senior design considerations: (1) Certificate management — the CDN must provision and renew TLS certificates for all domains and subdomains; wildcard and SAN certificates simplify this. (2) Origin security — if the CDN terminates TLS and sends plain HTTP to the origin, the origin is vulnerable to attacks on the CDN-to-origin path. Use HTTPS to the origin (CDN re-encryption) in untrusted environments. (3) Client certificate authentication — if the origin requires client certs, the CDN must forward them (mTLS from CDN to origin) or the CDN must validate them at the edge. The CDN is the TLS termination point — its configuration determines the security of the entire client-to-origin path.

## Q30: What is a CDN's Anycast IP and how does it improve availability?

**A:** A CDN's Anycast IP is a single IP address announced from multiple edge locations simultaneously via BGP. When a client connects to this IP, BGP routing directs them to the topologically nearest edge location. If one edge location fails (hardware failure, network outage, DDoS), BGP withdraws the route from that location and traffic is rerouted to the next-nearest edge — without any client-side changes.

Anycast improves availability by providing automatic geographic failover. Unlike DNS-based failover (which requires TTL expiry and DNS propagation — minutes to hours), Anycast failover happens at the routing layer (BGP convergence — seconds to minutes). If a CDN edge in Frankfurt goes down, traffic from European users shifts to the next-nearest edge (Amsterdam, Paris) with no client awareness.

The senior operational consideration: Anycast provides network-layer availability but not application-layer availability. If the edge is reachable but its application is broken (cache corruption, memory exhaustion), Anycast does not help — the route is still announced, but the edge serves errors. Health checks at the CDN's control plane must complement Anycast: if the application at an edge is unhealthy, the CDN must withdraw the route or mark the edge as degraded. Anycast is the transport-level safety net; application-level health is the service-level safety net.

## Q31: What is a CDN shield and how does it differ from origin shielding?

**A:** A CDN shield (or edge shield) is a CDN-managed intermediary layer between the CDN's edge locations and the customer's origin. The CDN itself manages the shield — the customer does not deploy or operate it. When an edge location experiences a cache miss, it fetches from the CDN's shield rather than directly from the origin. The shield aggregates requests from multiple edges, reducing origin load.

Origin shielding is a similar concept but may be customer-deployed: the customer places a reverse proxy or cache (Nginx, Varnish) between the CDN and the origin as a shield. This gives the customer control over the shield's behavior, caching rules, and monitoring. CDN-managed shields are simpler to operate (the CDN handles it) but offer less customization. Customer-deployed shields offer full control but add operational complexity.

The distinction matters for architecture decisions: CDN-managed shields (Cloudflare Origin Shield, Akamai Origin Shield) are the simpler choice for most deployments — the CDN handles cache hierarchy, health checks, and failover. Customer-deployed shields are justified when the origin has special requirements (custom cache warming, request transformation, authentication logic at the shield layer). Both reduce origin load; the choice is between operational simplicity and operational control.

## Q32: What is a load balancer's health check interval and how should it be tuned?

**A:** The health check interval is the frequency at which the load balancer probes backend servers to determine their health. A typical default is every 5-10 seconds. The interval, combined with the failure threshold (number of consecutive failures before removing a server) and recovery threshold (number of consecutive successes before re-adding a server), determines how quickly the load balancer detects and responds to server failures.

Tuning depends on the application's tolerance for failed requests. A 5-second interval with a failure threshold of 3 means a server is removed after 15 seconds of failure — during those 15 seconds, requests to the failed server return errors. Reducing the interval to 1 second with a threshold of 2 removes the server in 2 seconds — fewer failed requests but more health check traffic. Increasing the interval to 30 seconds reduces health check overhead but allows 90 seconds of failed requests.

A senior tuning approach: set the interval based on the acceptable error window. For user-facing HTTP APIs with a 99.9% SLA, the total allowed error window is ~8.7 seconds per day — the health check interval + failure threshold must be less than 8.7 seconds to stay within SLA. Monitor the health check overhead itself — too-frequent checks can consume backend resources (health endpoint CPU, database queries). The ideal is a fast liveness check (TCP connect or simple HTTP 200) at 1-2 second intervals, with a deeper readiness check at 5-10 second intervals.

## Q33: What is a CDN edge function and how does it extend CDN capabilities?

**A:** CDN edge functions (Cloudflare Workers, Lambda@Edge, Fastly Compute, Akamai EdgeWorkers) are serverless compute environments that run customer code at the CDN's edge locations, close to users. Instead of caching static content and forwarding dynamic requests to the origin, edge functions execute code that can modify requests, generate responses, transform headers, call APIs, and interact with edge-side storage — all without contacting the origin.

Use cases: A/B testing at the edge (rewrite URLs to serve different variants without origin involvement), authentication and authorization (validate JWT tokens at the edge, reject unauthorized requests before they reach the origin), personalization (serve personalized content by fetching user data from edge KV storage), and request routing (dynamically select the origin based on request characteristics). Edge functions blur the line between CDN and application platform.

The senior architectural consideration: edge functions are powerful but constrained — they run in a stateless, short-lived execution environment (typically <30 seconds CPU time, <128MB memory). They are not suitable for long-running processes, heavy computation, or stateful workflows. The design pattern is to offload lightweight, latency-sensitive logic to the edge (auth, routing, personalization, transformation) while keeping business logic at the origin. The edge is the "first mile" of processing; the origin is the "last mile" of business logic.

## Q34: What is a reverse proxy cache and how does it differ from a CDN cache?

**A:** A reverse proxy cache (Varnish, Nginx, HAProxy with caching) is a server-side cache deployed in front of origin servers, typically within the same data center or network. It caches responses from the origin and serves them to subsequent requests without hitting the origin again. The reverse proxy cache is operated by the application team and has full control over caching rules, TTLs, and invalidation.

A CDN cache is distributed across hundreds of edge locations worldwide. It caches content at the network edge, close to users, reducing both latency and origin load. The CDN cache is operated by the CDN provider, and the customer configures caching rules via the CDN's control plane.

The key difference is scope and distance. A reverse proxy cache is local — one data center, one cache layer. It reduces origin load but does not reduce latency for distant users. A CDN cache is global — many edge locations, reducing both origin load and user latency. A senior architecture uses both: CDN for global distribution and edge caching, reverse proxy cache at the origin for origin shielding and protection against cache misses from all CDN edges. The reverse proxy cache is the last line of defense before the origin.

## Q35: What is cache warming and why is it important?

**A:** Cache warming is the process of pre-populating CDN or reverse proxy caches with content before it is requested by users. Instead of waiting for the first user request to trigger a cache miss (cold start), warming proactively pushes content into the cache. This is critical after deployments (new code may change response content), after cache invalidations (purged content must be re-cached), and during capacity planning (pre-warming caches before traffic spikes).

Methods: automated warming scripts that crawl the application and fetch key URLs, CDN APIs that pre-fetch content from the origin, and background jobs that generate content and push it to the cache. For dynamic content, warming may involve generating the response (running the database queries, rendering the page) and storing the result in the cache before users request it.

A senior warming strategy: prioritize warming for high-traffic pages (homepage, product pages, popular articles), time warming for off-peak hours (avoid competing with user traffic for origin resources), and monitor warming effectiveness (compare cache hit ratios before and after warming). Warming is especially critical for CDNs after a purge — without warming, the first wave of user requests after purge all miss the cache simultaneously (thundering herd), potentially overwhelming the origin.

## Q36: What is a load balancer's rate limiting algorithm and how do you choose one?

**A:** Fixed window counting divides time into fixed buckets (e.g., 1-minute windows) and counts requests per client within each bucket. It is simple to implement but allows bursts at window boundaries — a client can send 100 requests in the last second of one window and 100 in the first second of the next, achieving 200 requests in 2 seconds despite a 100/minute limit. Sliding window log retains a timestamp for every request in the window, providing accurate counting but requiring significant memory.

Sliding window counter is a practical compromise: it maintains a count per window and interpolates based on the elapsed time in the current window, providing smoother limiting than fixed window without the memory overhead of sliding window log. Token bucket allows controlled bursts — tokens are added at a fixed rate (e.g., 10 tokens/second) and each request consumes one token; requests are rejected when the bucket is empty. Leaky bucket processes requests at a fixed rate regardless of arrival rate, smoothing bursts but adding latency.

The choice depends on the traffic pattern and acceptable burstiness. Token bucket is the most common for API rate limiting — it allows short bursts (useful for legitimate traffic patterns) while enforcing average rates. Fixed window is sufficient for simple use cases where burstiness is not a concern. Sliding window counter provides accuracy without excessive memory. Leaky bucket is appropriate when strict rate enforcement is required (regulatory compliance, SLA enforcement).

## Q37: What is connection persistence in a load balancer?

**A:** Connection persistence (keep-alive) is the load balancer's ability to maintain backend connections open for reuse across multiple client requests, rather than opening and closing a new connection per request. When a client request completes, the connection to the backend is kept open (up to a configurable idle timeout) and reused for the next request to the same backend. This eliminates TCP handshake overhead (and TLS handshake overhead if TLS is terminated at the backend) for subsequent requests.

Connection persistence is critical for HTTP/1.1 (which uses keep-alive by default), HTTP/2 (which multiplexes streams over a single connection), and WebSocket (which is inherently persistent). Without persistence, every request incurs connection setup overhead — for high-frequency API calls, this overhead dominates request latency.

A senior tuning parameter: the idle timeout (how long an idle connection stays open) balances connection reuse against resource consumption. Too short (1 second) forces frequent reconnections; too long (300 seconds) holds connections open even for clients that have disconnected, consuming backend resources. For HTTP/1.1, 15-60 seconds is typical. For WebSocket, the timeout is effectively the connection lifetime. The load balancer's connection pool size (total open connections per backend) must also be sized for the expected concurrency — too few connections cause queuing; too many overwhelm the backend.

## Q38: What is a CDN's cache purge propagation time?

**A:** Cache purge propagation time is the duration between issuing a purge request and the content being removed from all CDN edge locations. During this window, some edge locations may still serve stale content. Propagation time depends on the CDN's architecture: Cloudflare claims <30 seconds globally; Fastly achieves <150 ms for real-time purges; Akamai varies from seconds to minutes depending on configuration.

The propagation mechanism: the purge request is sent to the CDN's control plane, which distributes the purge指令 to all edge locations. Each edge location processes the purge and removes the affected content from its local cache. The speed depends on the CDN's internal network, the number of edge locations, and the purge mechanism (URL purge is faster than tag purge because it requires less processing).

A senior operational practice: never assume instant purge — always test purge propagation in production. For time-sensitive content (breaking news, price updates), use short TTLs as a fallback (the content expires naturally within seconds even if purge is delayed). For A/B testing or feature flags, use edge functions to determine variants dynamically rather than relying on cache purge for variant switching. Purge propagation time is a measurable SLA — the CDN should document and guarantee it.

## Q39: What is a load balancer's DSR (Direct Server Return) mode?

**A:** Direct Server Return (DSR) is a load balancing method where the load balancer handles only inbound traffic (client → server), and the server responds directly to the client without routing back through the load balancer (server → client). The load balancer modifies the destination IP (NAT) to the selected backend's IP, and the backend sends its response directly to the client using its own IP as the source. This halves the load balancer's throughput requirement — it only handles the inbound half of the traffic.

DSR is used when the response payload is much larger than the request payload (file downloads, video streaming, static content serving) — the load balancer would otherwise become a bottleneck processing all the response data. With DSR, the load balancer only processes the small request; the large response bypasses it entirely. The trade-off is complexity: the backend must be configured to use the load balancer's VIP as its own (via a loopback interface or ARP manipulation) so that the client's TCP connection appears to be with the VIP, not the backend's real IP.

A senior DSR consideration: DSR breaks stateful inspection at the load balancer (it never sees the response), which means features like response-based health checks, response logging, and response rewriting are unavailable. DSR also requires the backend and load balancer to be on the same Layer 2 segment (the backend must be able to reach the client directly). For most modern HTTP workloads, L7 load balancing with connection multiplexing is more practical — DSR is a niche optimization for extremely high-throughput, asymmetric traffic patterns.

## Q40: What is a CDN's cache hit ratio optimization and what techniques improve it?

**A:** Cache hit ratio (CHR) optimization is the process of maximizing the percentage of requests served from CDN cache rather than requiring origin fetches. Techniques include: appropriate Cache-Control headers (long TTLs for static assets, stale-while-revalidate for semi-dynamic content), URL normalization (stripping tracking parameters, sorting query strings), cache key optimization (including only content-variant parameters), pre-warming (populating caches before traffic spikes), and origin shielding (reducing redundant origin fetches).

Advanced techniques: cache partitioning (separating cache spaces for different content types to prevent one type from evicting another), edge-side includes (ESI) for fragment-level caching (cache parts of a page independently), and stale-while-revalidate/stale-if-error (serve slightly stale content while refreshing in background or when origin is unavailable). Monitoring CHR alongside origin latency and error rates provides context — a 95% CHR with low origin latency is healthy; a 95% CHR with high origin latency means the 5% miss rate is causing origin overload.

A senior CHR target depends on content type: static assets should achieve >99% CHR; HTML pages may achieve 50-80% depending on personalization; API responses vary widely. The target is not "maximize CHR" but "achieve the CHR that meets performance and freshness requirements at minimum origin cost." Over-optimizing CHR (extremely long TTLs) risks serving stale content; under-optimizing (no caching) wastes origin resources and user patience.

## Q41: What is a load balancer's sticky session timeout and how is it configured?

**A:** The sticky session timeout determines how long a client remains pinned to a specific backend after their first request. After the timeout expires, the client may be routed to a different backend on their next request. The timeout is configured per load balancer or per backend pool and is typically set to match the application's session lifetime — if the application session expires after 30 minutes, the sticky timeout should be 30 minutes or less.

Configuration approaches: cookie-based (the load balancer injects a cookie with the backend identifier; the cookie's lifetime determines the sticky duration), IP-based (the client IP is hashed to a backend; the timeout is the ARP/neighbor table timeout — typically 30 minutes), and header-based (a session token in the request header determines the backend; the timeout is the session token's validity period).

The senior consideration is the interaction between sticky timeout and application session timeout. If the sticky timeout is longer than the application session, the client is pinned to a backend that has no session data (session expired on the backend) — causing errors. If shorter, the client may migrate to a backend that has the session data — but may also migrate to one that does not. The correct configuration is: sticky timeout ≤ application session timeout, and the application stores session data externally (Redis/database) so any backend can handle any session. Sticky sessions are a routing optimization, not a session persistence mechanism.

## Q42: What is a CDN's origin pull model and how does it differ from origin push?

**A:** In the origin pull model, the CDN edge does not proactively fetch content from the origin. Instead, it waits for a client request — if the content is not in cache (miss), the edge pulls it from the origin, caches it, and serves it. Pull is the default and most common CDN model because it requires no pre-configuration of content to cache — the CDN caches whatever is requested.

In the origin push model, the CDN proactively fetches content from the origin and distributes it to edge locations before any client requests it. Push is used when content must be pre-positioned at the edge (live event streaming, scheduled content releases, large file distribution). Push requires configuration (which URLs to push, which edges to push to) and proactive management.

The senior deployment pattern: pull for most content (web pages, API responses, images) because it is self-correcting (popular content is cached automatically; unpopular content is not cached, saving origin bandwidth). Push for time-critical content (live event manifests, breaking news assets) where the latency of the first pull request would be unacceptable. Hybrid: push the initial version, then let pull handle subsequent updates. The push model's limitation is predicting what to push — if you push the wrong content, you waste edge cache space; if you miss content, the first request still triggers a pull.

## Q43: What is a load balancer's maximum connection limit and what happens when it's reached?

**A:** The maximum connection limit is the total number of concurrent connections the load balancer can maintain simultaneously — both client-side connections and backend-side connections. Hardware load balancers have hard limits (F5 BIG-IP can handle millions of concurrent connections); software load balancers are limited by the server's CPU, memory, and file descriptor limits. When the limit is reached, new connections are either rejected (connection refused or timeout) or queued (waiting for an existing connection to close).

What happens at the limit depends on the load balancer's behavior: some drop new connections silently (causing client timeouts); some return a 503 Service Unavailable; some queue connections up to a configurable queue depth. In all cases, the user experience degrades — connections fail, page loads time out, and API calls error.

A senior monitoring practice: track connection count as a percentage of maximum — 80% utilization is a warning; 90% is an emergency. Connection count growth correlates with traffic growth and connection duration — long-lived connections (WebSocket, database, keep-alive) consume connection slots for extended periods. Capacity planning must account for peak concurrent connections, not just requests per second. A site handling 10,000 requests/second with 100ms average response time needs 1,000 concurrent connections; with 1-second average response time, it needs 10,000.

## Q44: What is a CDN's cache partitioning and why is it used?

**A:** Cache partitioning divides the CDN's cache space into isolated segments for different content types, tenants, or applications. Instead of one shared cache where all content competes for space, each partition has its own cache allocation. For example, a partition for static assets (images, CSS, JavaScript) and a partition for API responses prevents a surge in API traffic from evicting popular images from cache.

The motivation is cache isolation: without partitioning, a single popular or pathological content type can dominate the cache and evict everything else (cache pollution). A video file that is requested once and cached for an hour displaces thousands of smaller, frequently-requested objects. Partitioning prevents this by confining each content type to its own cache space.

A senior partitioning strategy: partition by content type (static vs. dynamic), by tenant (multi-tenant CDN deployments), by application (different microservices), or by criticality (high-priority content gets a dedicated partition with strict eviction policies). The trade-off is cache efficiency versus isolation — a shared cache achieves higher overall utilization (any content can use any cache space), while a partitioned cache guarantees isolation but may waste space in under-utilized partitions. The right answer depends on traffic patterns and the cost of cache misses for each content type.

## Q45: What is a CDN's cache stale-while-revalidate directive?

**A:** The `stale-while-revalidate` Cache-Control directive tells the CDN (and browser) to serve the cached (potentially stale) version of content immediately while fetching a fresh copy from the origin in the background. The user receives the stale response without waiting for the origin to respond, and the next request after the background fetch completes receives the fresh version. This eliminates the latency penalty of cache misses for semi-dynamic content.

The directive is configured with a time window: `stale-while-revalidate=60` means the CDN may serve stale content for up to 60 seconds after the TTL expires while refreshing in the background. If the origin is unavailable during the revalidation window, the stale content is served without error — providing resilience.

A senior usage pattern: `stale-while-revalidate` is ideal for content that changes frequently but not instantly — news articles, product listings, social media feeds. It provides a latency floor (the user always gets a cached response) while maintaining freshness (the cache refreshes in the background). It is not suitable for content that must never be stale (authentication tokens, real-time financial data). The complementary directive `stale-if-error` serves stale content when the origin is unavailable (error condition), providing resilience beyond the normal revalidation window.

## Q46: What is a CDN's cache purging mechanism and what are the purge types?

**A:** CDN cache purging removes cached content from edge locations before its TTL expires. Purge types: purge-by-URL (deletes a specific URL from all edges — precise but requires knowing every URL that changed), purge-by-tag (deletes all content associated with a specific tag — flexible but requires tagging infrastructure on the origin), purge-by-Cache-Key (deletes based on the CDN's internal cache key — the most granular), and purge-all (flushes the entire cache — nuclear option, used sparingly).

Tag-based purging is the most operationally efficient: the origin tags each response with a tag (e.g., `product-123`, `category-shoes`), and when the product is updated, the CDN purges all content tagged with `product-123`. This handles cases where a single origin change affects multiple cached URLs (product page, product images, product API response).

A senior purge design: (1) tag content at the origin with meaningful identifiers (product ID, category, article ID). (2) Use purge-by-tag as the primary invalidation mechanism — it is more reliable than purge-by-URL (you do not need to enumerate every URL). (3) Monitor purge propagation time (verify that all edges have purged within the expected window). (4) Have a fallback TTL-based expiration for content that purge may miss. (5) Test purge mechanisms regularly — a purge that does not propagate is worse than no purge because it creates false confidence.

## Q47: What is a load balancer's idle timeout and how does it affect connections?

**A:** The idle timeout is the duration after which an inactive (no data transferred) connection is closed by the load balancer. When neither the client nor the backend sends data for the timeout period, the load balancer terminates the connection to free resources (connection table slots, memory). The timeout applies to both client-side and backend-side idle connections.

The impact on connections: too short (e.g., 30 seconds) closes connections that are legitimately idle (a user reading a page for 2 minutes, a WebSocket waiting for events), causing the client to reconnect (latency spike, potential data loss). Too long (e.g., 3600 seconds) holds connections open long after clients have disconnected, consuming load balancer resources and backend resources (thread pools, memory).

A senior tuning approach: set the idle timeout based on the application's idle behavior. For HTTP APIs (short-lived requests), 30-60 seconds is typical. For WebSocket connections (long-lived, event-driven), 300-600 seconds (or disable idle timeout and rely on application-level pings). For database connections (persistent, long-lived), 600+ seconds. The idle timeout should be shorter than the backend server's idle timeout to prevent the backend from closing the connection before the load balancer does (which causes 502 errors on the next request).

## Q48: What is a CDN's cache key design for multi-tenant environments?

**A:** In multi-tenant CDN deployments (SaaS platforms, hosting providers, marketplace platforms), each tenant's content must be isolated — Tenant A's cached content must not be served to Tenant B. The cache key must include a tenant identifier (tenant ID, API key, domain) to ensure per-tenant cache isolation. Without tenant isolation in the cache key, a request from Tenant A could be served Tenant B's cached response.

Design approaches: prefix the cache key with the tenant ID (`tenant-123:/path/to/resource`), include the tenant-specific domain in the cache key (if each tenant has a custom domain), or use separate CDN configurations per tenant (separate cache spaces entirely). The approach depends on the CDN's capabilities and the isolation requirements.

A senior multi-tenant cache design: use tenant ID as a cache key prefix for complete isolation. Implement per-tenant cache TTL policies (some tenants need real-time content; others can tolerate staleness). Monitor per-tenant cache hit ratios to identify tenants with poor cacheability (high miss rates suggest content that is too personalized or dynamic to cache). Consider per-tenant cache limits (prevent one tenant's high-traffic content from consuming cache space that affects other tenants' hit ratios).

## Q49: What is a CDN's origin connection pool and how is it sized?

**A:** The origin connection pool is the set of persistent connections that the CDN edge maintains to the origin server. Instead of opening a new connection to the origin for every cache miss (expensive — TCP handshake, TLS handshake), the edge reuses existing connections from the pool. Pool sizing determines how many concurrent origin fetches the edge can handle — a pool of 100 connections can serve 100 concurrent cache misses; additional misses must wait for a connection to become available.

Sizing depends on the expected cache miss rate and the origin's capacity. A high miss rate (dynamic content, short TTLs) requires a larger pool; a low miss rate (static assets, long TTLs) requires a smaller pool. The pool must also account for origin latency — a slow origin holds connections longer, reducing pool availability. Monitoring pool utilization (active connections / total pool size) and pool wait time (time requests spend waiting for a connection) informs sizing decisions.

A senior tuning approach: start with a conservative pool size (50-100 connections per edge location), monitor utilization and wait times during peak traffic, and scale the pool if wait times exceed acceptable thresholds. The pool is a per-edge resource — each edge location has its own pool, so the total origin connections from the CDN is pool size × number of edge locations. The origin must be able to handle the aggregate connection count from all edges.

## Q50: What is a load balancer's connection rate limit and how is it different from request rate limiting?

**A:** Connection rate limiting restricts the number of new connections per second from a single source — it limits how fast a client can establish new TCP connections, not how many total requests they make. This is different from request rate limiting (which limits total requests, including those on existing connections). Connection rate limiting defends against SYN floods, connection-based DDoS, and clients that open excessive connections (connection exhaustion attacks).

A client opening 1000 new connections per second is suspicious — legitimate clients reuse connections (HTTP keep-alive, HTTP/2 multiplexing). A client establishing a new connection for every request is either misbehaving or attacking. Connection rate limiting caps this behavior (e.g., 10 new connections per second per IP) while allowing unlimited requests on established connections.

The senior design combines both: connection rate limiting (10 new connections/second/IP) for transport-layer protection, and request rate limiting (100 requests/minute/key) for application-layer protection. Connection rate limiting catches SYN floods and connection exhaustion; request rate limiting catches API abuse and scraping. The two are complementary, not redundant — a client can stay within connection rate limits but exceed request rate limits (many requests on few connections) or vice versa (many short-lived connections with few requests each).


## Q51: What is a CDN's cache partitioning by content type and how does it improve performance?

**A:** Cache partitioning by content type divides the CDN cache into isolated segments based on the type of content — static assets (images, CSS, JavaScript), dynamic content (HTML pages, API responses), and media (video, audio). Each partition has its own eviction policy, TTL strategy, and storage allocation. Static assets use long TTLs and LRU (Least Recently Used) eviction; dynamic content uses short TTLs or stale-while-revalidate; media uses specialized storage optimized for large sequential reads.

The performance improvement comes from preventing cross-type pollution: a viral video (large, single-object, long cache duration) would evict thousands of small, frequently-accessed CSS files from a shared cache. Partitioning confines the video to its own cache space, preserving the CSS hit ratio. Similarly, a surge in API requests (dynamic, short TTL) would evict static assets if the cache were shared.

A senior partitioning implementation: define partitions at the CDN configuration level (each partition has its own cache key namespace, TTL defaults, and storage limits). Monitor per-partition hit ratios and eviction rates to identify partitions that are over or under-sized. Adjust partition sizes based on observed traffic patterns — a partition with low eviction and high hit ratio is well-sized; a partition with high eviction needs more space. The trade-off is cache utilization efficiency versus isolation — a shared cache maximizes overall utilization; partitioned caches trade some efficiency for predictable performance per content type.

## Q52: What is a load balancer's active health check passive mode and when is it preferred?

**A:** Passive health check mode (also called observational or runtime health monitoring) evaluates backend health based on real user traffic rather than synthetic probes. The load balancer monitors the responses from actual client requests — tracking error rates (5xx responses), latency (response time exceeding a threshold), and connection failures (TCP resets, timeouts). If a backend's error rate exceeds a threshold (e.g., 50% of requests returning 5xx), the load balancer removes it from the pool.

Passive mode is preferred when: the health endpoint does not reflect real application health (the health endpoint returns 200 but the application is degraded), when synthetic probes add unacceptable overhead (high-traffic APIs where health check requests are significant), or when the application has complex dependencies that cannot be simulated in a health check (database connection pool, external API availability).

The limitation of passive mode is that it detects failures only after user requests have been affected — a user who hits a degraded backend gets an error before the load balancer detects the problem. The optimal approach combines both: active checks for hard failures (server down, port closed) caught proactively, passive checks for soft failures (degraded application, exhausted resources) caught through real traffic observation. The two modes cover different failure modes — active catches transport failures; passive catches application failures.

## Q53: What is a CDN's cache key normalization and why is it important?

**A:** Cache key normalization is the process of standardizing URLs before using them as cache keys, ensuring that semantically identical content with different URL representations is served from the same cache entry. Without normalization, `https://example.com/page`, `https://example.com/page/`, `https://example.com/Page`, and `https://example.com/page?utm_source=email` are all different cache keys — even though they may serve identical content.

Normalization techniques: case normalization (lowercase the URL path — `/Page` → `/page`), trailing-slash normalization (`/page` → `/page/` or vice versa), query parameter sorting (`?a=1&b=2` → `?a=1&b=2` regardless of parameter order), query parameter stripping (remove tracking parameters like `utm_*`, `fbclid`, `gclid`), and URL encoding normalization (`/café` → `/caf%C3%A9` or vice versa).

A senior normalization strategy: define a normalization policy that reflects the application's URL semantics. If the application serves different content for `/page` and `/Page`, do not normalize case. If `/page` and `/page/` serve the same content, normalize the trailing slash. If tracking parameters do not affect content, strip them. The normalization policy is application-specific — there is no universal correct answer. Test normalization against real traffic patterns to verify that the cache key correctly identifies unique content.

## Q54: What is a CDN's origin shield cache hierarchy and how does it reduce origin load?

**A:** The origin shield cache hierarchy is a multi-tier caching architecture within the CDN: edge cache → regional cache → origin shield → origin. Each tier serves as a cache for the tier below it. When an edge location experiences a cache miss, it checks its regional cache; if the regional cache has the content, it is served without contacting the origin shield or origin. The regional cache checks the origin shield on its miss; the origin shield checks the origin on its miss.

The hierarchy reduces origin load multiplicatively: with 100 edge locations, 10 regional caches, and 1 origin shield, a popular asset that expires simultaneously at all 100 edges results in at most 10 requests to the regional caches, at most 1 request to the origin shield, and at most 1 request to the origin. Without shielding, the origin would receive 100 simultaneous requests (thundering herd).

A senior hierarchy design: the number of tiers and their geographic distribution should match the edge topology. Regions with many edges benefit from a dedicated regional cache (reduces origin shield load). Regions with few edges can share a regional cache with adjacent regions. The origin shield is typically 2-3 globally distributed locations. The hierarchy's effectiveness depends on cache hit ratios at each tier — a regional cache with a 90% hit ratio reduces origin shield load by 90% from the edges.

## Q55: What is a CDN's cache tag-based purge and how does it work?

**A:** Tag-based purge allows CDN customers to associate one or more tags with each cached response (via HTTP headers like `Cache-Tag: product-123,category-shoes`). When content is updated, the customer issues a purge request for a specific tag — `purge:product-123` — and the CDN removes all cached responses that carry that tag, regardless of their URL. This enables bulk invalidation without enumerating every URL.

The mechanism: when the CDN caches a response, it stores the tags alongside the content. When a purge-by-tag request arrives, the CDN scans its tag index (an inverted index mapping tags to cached responses) and removes all matching entries. The purge propagates to all edge locations just like a URL purge.

A senior tag-based purge strategy: tag every cacheable response with identifiers that reflect its dependencies. A product page should carry tags for the product ID, category, and any other entity it depends on. When the product is updated, purge by product ID tag — all pages, images, and API responses tagged with that ID are invalidated. When a category's products change, purge by category tag. Tag-based purge is the most operationally scalable invalidation mechanism for applications with complex content dependencies.

## Q56: What is a load balancer's connection rate limiting versus request rate limiting?

**A:** Connection rate limiting restricts the number of new TCP connections per second from a single source. It is a transport-layer defense — it limits how fast a client can open new connections, not how many requests they make on established connections. A client opening 1000 new connections per second is suspicious (legitimate clients reuse connections via HTTP keep-alive or HTTP/2). Connection rate limiting caps this behavior (e.g., 10 new connections/second/IP).

Request rate limiting restricts the total number of requests per second (or per minute) from a single source, regardless of whether those requests are on existing connections or new connections. A client making 500 API requests per minute on a single established connection is an API abuse scenario — connection rate limiting would not catch it (only one connection), but request rate limiting would.

The two are complementary: connection rate limiting catches SYN floods and connection exhaustion attacks; request rate limiting catches API abuse, scraping, and application-layer DDoS. A client can stay within connection rate limits while exceeding request rate limits (many requests on few connections) or vice versa (many short-lived connections with few requests each). A comprehensive rate-limiting strategy deploys both layers.

## Q57: What is a CDN's cache stale-if-error directive and how does it improve resilience?

**A:** The `stale-if-error` Cache-Control directive tells the CDN to serve cached (stale) content when the origin returns an error (5xx status code) or is unreachable. Normally, a cache miss that results in an origin error returns the error to the client. With `stale-if-error`, the CDN serves the last cached version instead — providing degraded but functional service during origin outages.

Configuration: `Cache-Control: max-age=3600, stale-if-error=86400` means the content is fresh for 1 hour, and for up to 24 hours after expiration, stale content is served if the origin errors. The directive is a resilience mechanism — it trades freshness for availability during outages.

A senior resilience design: `stale-if-error` is most valuable for critical pages (homepage, login, product pages) where serving stale content is better than serving an error. It is less valuable for personalized content (user-specific data cannot be served stale to a different user) and real-time data (stale financial data is worse than no data). The directive should be configured per content type based on the staleness tolerance. Combined with `stale-while-revalidate`, it provides a complete availability strategy: serve stale while refreshing in the background, and serve stale when the origin is unavailable.

## Q58: What is a CDN's edge compute model and how does it change the traditional CDN paradigm?

**A:** Edge compute (Cloudflare Workers, Lambda@Edge, Fastly Compute) transforms the CDN from a passive caching layer into an active compute platform. Instead of caching static content and forwarding dynamic requests to the origin, edge compute executes customer code at the CDN's edge — modifying requests, generating responses, calling APIs, and interacting with edge storage — all within the request path and close to the user.

The paradigm shift: traditional CDNs are reactive (cache hit → serve; cache miss → forward to origin). Edge compute is proactive (intercept every request, execute logic, decide whether to cache, forward, or generate a response). This enables: A/B testing at the edge (rewrite URLs to serve variants), authentication at the edge (validate JWTs without origin round-trip), personalization at the edge (fetch user data from edge KV, serve personalized content), and request routing at the edge (dynamically select origin based on request characteristics).

The senior architectural consideration: edge compute is constrained (short execution time, limited memory, no persistent local state) and should be used for lightweight, latency-sensitive operations — not for heavy business logic or database-intensive processing. The pattern is: edge handles auth, routing, personalization, and transformation; origin handles business logic, database queries, and complex computation. The edge is the "first mile" of processing; the origin is the "last mile" of business logic.

## Q59: What is a CDN's cache warming strategy for high-traffic events?

**A:** Cache warming for high-traffic events (product launches, flash sales, breaking news, live events) proactively populates CDN caches before the anticipated traffic spike. Without warming, the first wave of users all trigger cache misses simultaneously (thundering herd), overwhelming the origin. Warming pre-populates caches so the first user request is a cache hit.

Strategies: pre-fetching (scripts that crawl the application and fetch key URLs into cache before the event), CDN API pre-fetch (using the CDN's API to pull content from origin to edges), and background rendering (generating dynamic content in advance and pushing to cache). For events with known URLs (product launch page), pre-fetching is straightforward. For events with unpredictable URLs (breaking news with many articles), warming is harder — use short TTLs and `stale-while-revalidate` as the fallback.

A senior event warming plan: identify the critical URLs (homepage, product pages, search results), warm them 30-60 minutes before the event, verify cache hit ratios at each edge location, and monitor origin load during the event. Have a fallback: if origin load exceeds thresholds, enable rate limiting at the edge and serve stale content. The warming plan should be tested before the event — a warming script that fails silently is worse than no warming (it gives false confidence).

## Q60: What is a CDN's cache key design for personalized content?

**A:** Personalized content (user-specific pages, authenticated dashboards, targeted recommendations) poses a cache challenge: each user sees different content at the same URL, so a naive cache key (URL-only) either caches the wrong user's content or misses the cache entirely. The cache key must include a user identifier (session cookie, user ID, authentication token) to ensure per-user caching.

Design approaches: include the session cookie in the cache key (`user-abc123:/dashboard`), use edge compute to detect personalization and bypass cache for personalized responses, or use fragment-level caching (Edge-Side Includes) where the page skeleton is cached and personalized fragments are assembled at the edge. The approach depends on the CDN's capabilities and the degree of personalization.

A senior personalization cache strategy: cache non-personalized fragments aggressively (page layout, navigation, common content) and assemble personalized fragments at the edge. This maximizes cache hit ratio for the shared fragments while serving personalized content correctly. For fully personalized pages, use `no-cache` or `private` directives to bypass CDN caching entirely — the browser cache handles per-user caching. The design question is always: "What fraction of this page is shared across users?" — cache that fraction.

## Q61: What is a load balancer's health check depth and how does it affect detection accuracy?

**A:** Health check depth refers to how thoroughly a health check evaluates the backend's health — from a simple TCP connection check (shallowest) to a deep application-level check (deepest). A TCP check verifies that the port is open — it detects a crashed server but not a hung application. An HTTP check requests a specific endpoint and validates the status code — it detects application errors but not degraded dependencies. A deep check validates end-to-end functionality (database connectivity, external API availability, disk space, cache warmth).

Shallow checks (TCP, HTTP 200) are fast, lightweight, and detect hard failures. Deep checks (application-level validation) are slower, heavier, and detect soft failures. The trade-off is accuracy versus overhead: deep checks are more accurate but consume backend resources on every check cycle.

A tiered health check approach: shallow liveness checks (every 2 seconds, TCP or simple HTTP) detect transport-level failures; medium readiness checks (every 5 seconds, HTTP with status code and basic body validation) detect application-level failures; deep dependency checks (every 30 seconds, database/cache validation) detect infrastructure failures. The load balancer uses liveness and readiness for routing decisions; deep checks trigger alerts for operational investigation.

## Q62: What is a CDN's cache optimization for mobile devices?

**A:** Mobile devices have different characteristics than desktops: smaller screens (requiring different image sizes), variable bandwidth (3G/4G/5G/Wi-Fi), higher latency (wireless last-mile), and battery constraints. CDN cache optimization for mobile includes: device-aware caching (different cache entries for mobile vs. desktop versions of the same URL), adaptive image delivery (serving appropriately sized images based on device capability), and protocol optimization (HTTP/2, QUIC/HTTP/3 for mobile's high-latency, lossy networks).

Techniques: separate cache keys for mobile and desktop (via Vary header or device-detection at the edge), responsive image serving (edge functions detect User-Agent and serve the appropriate image format/size — WebP for modern devices, JPEG for legacy), and edge-side rendering (generating mobile-optimized HTML at the edge rather than at the origin). CDNs like Cloudflare offer Mobile Optimization features that automatically rewrite images and optimize delivery for mobile.

A senior mobile cache strategy: cache mobile-specific variants with appropriate TTLs (mobile content may change more frequently due to different ad insertion), use `Vary: Accept-Encoding` to serve compressed content appropriately (Brotli for supported clients, Gzip for others), and monitor mobile-specific metrics (cache hit ratio from mobile User-Agents, mobile-specific latency). Mobile users are often on higher-latency, lower-bandwidth connections — cache hits matter more for mobile than for desktop because the latency penalty of a miss is higher.

## Q63: What is a CDN's cache key design for multi-language content?

**A:** Multi-language content (content served in different languages based on user locale) requires cache keys that distinguish between language variants. Without language in the cache key, a French user's request might be served cached English content. The cache key must include the language identifier — typically the `Accept-Language` header, the URL path (`/en/page`, `/fr/page`), or a cookie/session parameter indicating the user's language preference.

Approaches: path-based (`/en/page`, `/fr/page`) — the simplest and most cacheable because each language is a unique URL; header-based (include `Accept-Language` in the cache key) — flexible but creates many unique cache keys for the same URL; cookie-based (language stored in a cookie, included in cache key) — works for personalized language preferences. Path-based is preferred for SEO (separate URLs per language) and cacheability (each language is a unique, cacheable URL).

A senior multi-language cache design: use path-based language prefixes for content that is published in fixed languages (e.g., `example.com/en/about`, `example.com/fr/about`). Use header-based or cookie-based for dynamically translated content where the language is determined at request time. Monitor cache hit ratios per language — low hit ratios for a specific language may indicate insufficient cache space or too many unique keys.

## Q64: What is a load balancer's TLS version enforcement and why is it important?

**A:** TLS version enforcement is the load balancer's configuration of which TLS versions are accepted from clients. TLS 1.0 and 1.1 are deprecated (vulnerable to BEAST, POODLE, and other attacks); TLS 1.2 is the minimum acceptable version; TLS 1.3 is the preferred version (faster handshake, stronger ciphers, no legacy algorithm support). The load balancer rejects connections from clients that attempt to negotiate a deprecated TLS version.

The importance is security: allowing deprecated TLS versions exposes the application to known vulnerabilities. PCI DSS compliance requires TLS 1.2 minimum for cardholder data environments. Modern browsers have removed support for TLS 1.0/1.1, but older clients (embedded systems, legacy IoT, older mobile apps) may still attempt them.

A senior enforcement policy: configure the load balancer to accept TLS 1.2 and 1.3 only. Disable TLS 1.0/1.1 completely unless there is a documented business requirement for legacy client support (and even then, only on specific virtual servers with compensating controls). Configure cipher suites to prefer TLS 1.3 (which has a mandatory, limited cipher suite) and AES-GCM with PFS (Perfect Forward Secrecy) for TLS 1.2. Test the configuration with tools like `nmap --script ssl-enum-ciphers` or `testssl.sh` to verify that only the intended versions and ciphers are accepted.

## Q65: What is a CDN's cache key design for API responses?

**A:** API responses present unique caching challenges: they may contain personalized data, real-time data, or data that changes frequently. The cache key for API responses must include all parameters that affect the response — not just the URL path, but query parameters, headers (Accept, Authorization), and request body (for POST/PUT). Including non-differentiating parameters (tracking IDs, timestamps) creates unnecessary unique cache keys and wastes cache space.

Design considerations: use normalized query parameters (strip non-differentiating parameters, sort remaining), include authentication context (a cached response for User A must not be served to User B — include session token or user ID in the cache key), and handle pagination (page 1 and page 2 are different cache entries). Cache-Control headers for APIs should be explicit: `Cache-Control: private, max-age=0` for personalized data (browser cache only), `Cache-Control: public, max-age=60` for shareable data (CDN cache for 60 seconds).

A senior API cache strategy: cache at the response level for simple APIs (GET requests with URL-based parameters), cache at the fragment level for complex APIs (Edge-Side Includes for assembling cached and non-cached fragments), and use edge compute for dynamic API responses (execute logic at the edge, call origin only for data not available at the edge). The key question is always: "Can two users with the same request get the same response?" If yes, cache it. If no, bypass cache or use per-user caching with user-specific keys.

## Q66: What is a CDN's cache behavior for POST requests and non-cacheable methods?

**A:** HTTP POST, PUT, DELETE, and PATCH requests are non-cacheable by default — they modify server state and should not be served from cache. A CDN correctly forwards these methods to the origin without caching. However, some CDNs and reverse proxies can be configured to cache POST responses (rarely useful) or to convert POST to GET (dangerous — violates HTTP semantics).

The correct behavior: POST/PUT/DELETE requests pass through the CDN to the origin; only GET and HEAD requests are eligible for caching. The CDN may cache the response to a GET request that follows a POST (e.g., POST to a form, redirect to a GET result page — the GET result page is cacheable). CDN configuration must not cache POST responses — doing so could serve a user's submitted data to another user, causing data leakage.

A senior CDN method handling: configure the CDN to explicitly not cache POST, PUT, DELETE, PATCH requests. Verify this behavior with test requests. For GraphQL APIs (which typically use POST for all operations), use persisted queries (pre-registered query hashes sent as GET requests) to enable caching of read-only operations while correctly forwarding mutations. The CDN's method handling is a security boundary — misconfigured caching of POST responses can cause data leakage and compliance violations.

## Q67: What is a CDN's edge location density and how does it affect performance?

**A:** Edge location density is the number of CDN points of presence (PoPs) and their geographic distribution. A CDN with 200+ edge locations (Cloudflare, Akamai, Fastly) has a PoP within 50ms of most users globally. A CDN with 10 edge locations may have users 150ms+ from the nearest PoP. Edge density directly affects latency (cache hit response time) and availability (failover options).

Higher density provides: lower latency (users connect to a nearby PoP), better failover (more redundant paths and PoPs to absorb failures), higher availability (a regional outage affects fewer users), and better DDoS absorption (attack traffic is distributed across more locations). The diminishing returns: beyond ~200 PoPs, adding more locations provides marginal latency improvement (most users are already <50ms from a PoP) but increases operational complexity and cost.

A senior CDN selection consideration: edge density matters most for latency-sensitive applications (real-time APIs, gaming, financial trading) and global audiences. For a US-only audience, a CDN with 10 US PoPs may perform identically to one with 200 global PoPs. For a global audience, the CDN with denser coverage in your user's regions (Asia, Europe, Latin America) is more important than total PoP count. Test latency from representative user locations before committing to a CDN.

## Q68: What is a load balancer's graceful shutdown and how does it handle in-flight connections?

**A:** Graceful shutdown is the load balancer's process for shutting down without dropping active connections. When the load balancer is restarted (for a software update, configuration change, or maintenance), it stops accepting new connections, drains existing connections (waits for in-flight requests to complete), and then shuts down after a configurable timeout. This prevents the abrupt termination of active sessions, which would cause user-visible errors.

The process: stop accepting new connections (new SYN packets are rejected or redirected to a standby load balancer), enable connection draining (existing connections continue to be forwarded to backends), wait for a configurable drain period (e.g., 300 seconds), and forcibly close any remaining connections after the timeout. The drain period must be long enough for the longest expected request to complete.

A senior graceful shutdown practice: pair graceful shutdown with connection draining in the load balancer pool. During a rolling restart of a load balancer cluster, each node is drained before restart — its connections are moved to other nodes. The drain timeout must account for the longest request duration in the application (a 10-second API timeout, a 60-second WebSocket heartbeat, or a 300-second file upload). The shutdown procedure should be tested — a shutdown that does not drain properly causes outages during maintenance windows.

## Q69: What is a CDN's cache optimization for video content?

**A:** Video content (VOD, live streaming) uses specialized CDN caching strategies due to its large file sizes, sequential access patterns, and high bandwidth requirements. Video is segmented into small chunks (2-10 seconds each, in formats like HLS or DASH), and each segment is a separate cacheable object. The CDN caches individual segments rather than entire video files — enabling partial caching and adaptive bitrate delivery.

Cache strategies for video: segment-level caching (each chunk is cached independently — a popular video has its segments cached across many edges), manifest/playlist caching (the HLS/DASH manifest is cached with short TTLs to reflect new segments), and pre-fetching (for live events, the CDN pre-fetches upcoming segments from the encoder before they are requested by clients). CDN-specific video features include origin shielding for video (reducing redundant origin fetches from many edges), token-based access control (preventing hotlinking and unauthorized access), and adaptive bitrate streaming (the CDN serves the appropriate quality based on client bandwidth).

A senior video cache design: use a CDN with purpose-built video delivery features (Akamai Media Delivery, Cloudflare Stream, Fastly Video). Configure segment TTLs to balance freshness and cacheability (live content requires short TTLs; VOD can use long TTLs). Monitor cache hit ratios per video — popular videos should have near-100% hit ratios at the edge; unpopular videos may only be cached at regional or origin-shield tiers. Pre-warm caches before major events (live sports, product launches) to avoid cache misses at event start.

## Q70: What is a CDN's cache optimization for JavaScript/CSS assets?

**A:** JavaScript and CSS assets are highly cacheable because they change infrequently and their filenames can be versioned (content-hash-based filenames: `app.3fa2b1c.js`). When the content changes, the filename changes — so the old cached version expires naturally (the old URL is no longer requested) and the new version is cached under the new URL. This eliminates the need for cache invalidation — the CDN caches indefinitely (`Cache-Control: immutable, max-age=31536000`) until the filename changes.

Optimization techniques: content-hash filenames (bust the cache by changing the filename, not by purging), minification (remove whitespace, comments, and dead code to reduce file size — smaller files cache better and transfer faster), compression (Brotli for JavaScript/CSS — 15-20% smaller than Gzip), and bundling (combine multiple files into one to reduce HTTP requests — though HTTP/2 multiplexing reduces this need). Tree-shaking (removing unused code) further reduces file size.

A senior JavaScript/CSS cache strategy: use content-hash filenames with immutable cache headers (indefinite caching — the browser and CDN cache the file until the URL changes). Serve pre-compressed Brotli files from the origin (compress once, serve many times). Use a CDN that supports Brotli at the edge. Monitor cache hit ratios — if the hit ratio for versioned assets is below 99%, investigate whether the CDN's cache key includes the full URL (including the hash) correctly.

## Q71: What is a CDN's cache key design for GraphQL APIs?

**A:** GraphQL APIs present a unique caching challenge: all requests go to the same endpoint (`/graphql`) via POST, with the query in the request body. The cache key cannot be derived from the URL alone — it must include the query content, variables, and operation name. Without body-aware caching, all GraphQL requests share one cache key (the URL) and are either all cached or all bypassed.

Approaches: persisted queries (register queries server-side with unique IDs; the client sends the ID instead of the full query — the cache key is the ID, enabling URL-like caching), automatic persisted queries (APQ — the client sends a hash of the query; the server registers it on first request and subsequent requests use the hash), and edge-side query parsing (the CDN or edge function parses the GraphQL body and constructs a cache key from the query and variables).

A senior GraphQL cache strategy: use persisted queries for all read-only operations — this converts GraphQL POST requests into cacheable, URL-like identifiers. For mutations, bypass cache entirely. For subscriptions, use WebSocket (not cacheable). The cache key for persisted queries is the query ID (unique, deterministic, cacheable). Monitor which queries are most frequently executed and optimize their caching — popular queries benefit most from edge caching; rarely-executed queries may not justify the cache space.

## Q72: What is a CDN's cache optimization for HTML pages?

**A:** HTML pages are the most challenging content to cache because they are often dynamic (generated per-request), personalized (different content per user), and the entry point for all other resources (the HTML references CSS, JavaScript, images). Caching HTML incorrectly serves stale or incorrect content; not caching HTML at all increases origin load and latency.

Strategies: short TTLs (cache HTML for 5-60 seconds — reduces origin load while keeping content relatively fresh), stale-while-revalidate (serve cached HTML for a few seconds while refreshing in background — eliminates latency penalty of cache misses), edge-side rendering (generate HTML at the edge using cached data and edge compute — the HTML never touches the origin), and fragment caching (cache the non-personalized parts of the HTML via Edge-Side Includes and assemble personalized parts at the edge).

A senior HTML cache strategy: distinguish between personalized HTML (dashboards, user profiles — `Cache-Control: private, no-cache`) and non-personalized HTML (product pages, articles — cache with short TTL + stale-while-revalidate). For high-traffic pages, pre-render at the edge and cache the result. For pages with mixed personalization, use ESI to cache shared fragments and assemble personalized fragments at the edge. Monitor cache hit ratios for HTML separately from static assets — a low HTML hit ratio may indicate excessive personalization or insufficient TTL.

## Q73: What is a CDN's cache behavior for authentication cookies and tokens?

**A:** Authentication cookies and tokens (JWT, session cookies) create a caching challenge: requests with different authentication tokens may receive different content (personalized pages), but the CDN cannot know whether two tokens represent the same user without validating them. Naive caching may serve one user's personalized content to another user (cache key does not include the token), or may never cache personalized content (cache key includes the token, creating unique entries per user).

The correct behavior: CDN caches should not cache responses that depend on authentication unless the cache key includes the session identifier. For public content (no authentication required), cache without regard to cookies. For authenticated content, either: include the session cookie in the cache key (per-user caching — low hit ratio but correct), or bypass cache for authenticated requests (no CDN caching for personalized content). For mixed content (public layout with personalized fragments), use ESI.

A senior authentication-aware caching design: use `Cache-Control: private` for personalized responses (bypasses CDN cache, uses browser cache only), `Cache-Control: public` for shared responses (CDN caches and serves to all users), and ESI for mixed content (cache the public layout at the CDN, assemble personalized fragments at the edge). The CDN should strip cookies from cache key for static assets (images, CSS, JS — cookies are irrelevant to these resources) to maximize their hit ratio.

## Q74: What is a load balancer's request buffering and why is it used?

**A:** Request buffering is the load balancer's ability to receive the complete client request (headers and body) before forwarding it to the backend. Without buffering, the load balancer streams the request to the backend as it arrives — the backend starts receiving the request before the load balancer has received the complete request. With buffering, the load balancer accumulates the full request, then sends it to the backend in one burst.

Request buffering is used for: request validation (inspecting the full request body before forwarding — e.g., validating a JSON payload against a schema), request transformation (modifying headers, rewriting URLs, or injecting headers based on the full request), and SSL offload (decrypting the full request before forwarding to the backend in plain HTTP). It also protects backends from slow clients — a slow client sending a large body slowly does not tie up a backend connection for the entire duration.

The trade-off: buffering adds latency (the backend must wait for the full request before it can start processing) and consumes load balancer memory (holding the full request in memory). For large file uploads, buffering the entire body may exhaust load balancer memory. The configuration should buffer headers and small bodies, but stream large bodies (configurable body size threshold) to the backend.

## Q75: What is a CDN's cache optimization for e-commerce applications?

**A:** E-commerce applications have a unique combination of caching needs: product pages (semi-dynamic, cacheable with short TTLs), user-specific content (carts, wishlists — not cacheable at CDN), static assets (images, CSS, JS — highly cacheable), search results (personalized, not cacheable), and API responses (mixed cacheability). The CDN configuration must handle each content type differently.

Strategies: static assets with long TTLs and content-hash filenames (near-100% cache hit ratio), product pages cached with short TTLs + stale-while-revalidate (serves cached product info while refreshing in background), search results and personalized content bypassing CDN cache (served from origin or edge compute), and API responses cached selectively (product listings cached; cart and checkout bypassed). Price updates and inventory changes require cache invalidation — use tag-based purge to invalidate all pages referencing a specific product.

A senior e-commerce CDN design: separate cache policies per content type (static assets: immutable, long TTL; product pages: short TTL, stale-while-revalidate; user content: private, no-cache). Use edge compute for A/B testing and personalization at the edge (avoids origin round-trips for variant testing). Implement origin shielding to protect the e-commerce origin (database, inventory system) from thundering herd during sales events. Monitor cache hit ratios per content type — a drop in product page hit ratio may indicate a TTL that is too short; a drop in static asset hit ratio may indicate a cache key issue.


## Q76: What is a CDN's cache optimization for news and media websites?

**A:** News and media websites have rapidly changing content (articles published frequently, breaking news, updated stories) combined with high traffic spikes (breaking news events, trending stories). The CDN must balance freshness (serving the latest article) with performance (serving cached content fast). The challenge is that articles change after publication (corrections, updates, featured placement) — requiring cache invalidation.

Strategies: short TTLs for article pages (60-300 seconds — content is fresh enough for most readers), stale-while-revalidate (serve cached article while refreshing in background — eliminates latency penalty), tag-based purge (tag articles by category, author, or breaking-news status — purge all articles in a category when the category page changes), and edge compute (personalize article recommendations at the edge based on reading history). Static assets (article images, fonts, JS) use long TTLs with content-hash filenames.

A senior news CDN design: pre-warm caches before scheduled events (planned press conferences, known article publication times), use surge protection (rate limiting at the edge to prevent traffic spikes from overwhelming the origin), and implement cache partitioning (separate partitions for breaking news — high priority, low TTL — and archived content — lower priority, high TTL). Monitor cache hit ratios during breaking news events — the hit ratio will drop as new content is published; the goal is to stabilize quickly as the content is cached after the first request.

## Q77: What is a load balancer's SSL client certificate authentication and how does it work?

**A:** SSL client certificate authentication (mutual TLS, mTLS) is a security mechanism where the client presents a TLS certificate during the TLS handshake, and the server validates it before establishing the connection. The load balancer terminates the client's TLS connection, extracts the client certificate, validates it against a trusted CA list, and forwards the certificate details (subject, issuer, serial number) to the backend via HTTP headers (e.g., `X-Client-Cert-Subject`).

The workflow: the client is provisioned with a certificate signed by a CA trusted by the load balancer. During the TLS handshake, the load balancer requests the client certificate (via CertificateRequest in TLS 1.2/1.3), the client presents it, and the load balancer validates: is the certificate signed by a trusted CA? Is it expired? Is it revoked (via CRL or OCSP)? If valid, the connection proceeds; if invalid, the handshake fails.

A senior mTLS deployment: use mTLS for service-to-service authentication (microservices communicating internally), IoT device authentication (devices proving identity before connecting), and API client authentication (partner systems accessing APIs). The operational overhead is certificate lifecycle management — provisioning, renewal, and revocation for every client. Use short-lived certificates (hours to days) with automated renewal (via ACME or internal PKI) to reduce the risk of compromised certificates. The load balancer must also handle certificate revocation checking (CRL/OCSP) — otherwise a revoked certificate remains valid until expiration.

## Q78: What is a CDN's cache optimization for SaaS applications?

**A:** SaaS applications present a complex caching landscape: shared application resources (CSS, JS, fonts — cacheable), user-specific dashboards (personalized — not cacheable at CDN), API responses (mixed — some cacheable, some not), and multi-tenant data (each tenant sees different content — cache keys must be tenant-aware). The CDN must navigate these constraints to maximize cache hit ratio without serving incorrect or stale content.

Strategies: static assets with long TTLs and content-hash filenames (shared across all tenants), tenant-specific API responses with tenant ID in the cache key (per-tenant caching), personalized content bypassing CDN cache (served from origin or edge compute), and fragment caching (ESI for shared page layouts with tenant-specific fragments). For multi-tenant SaaS, the cache key must include the tenant identifier to prevent cross-tenant cache poisoning.

A senior SaaS CDN design: separate cache policies per content tier — Tier 1 (static assets: immutable, long TTL, global cache), Tier 2 (shared templates/layouts: short TTL, shared cache), Tier 3 (tenant-specific data: tenant ID in cache key, per-tenant cache), Tier 4 (personalized/user-specific: bypass CDN cache, use browser cache). Monitor per-tenant cache hit ratios — a tenant with a consistently low hit ratio may have excessively personalized content or a cache key issue. Use edge compute for tenant context detection (extract tenant ID from JWT at the edge, include in cache key).

## Q79: What is a CDN's edge DNS and how does it improve resolution performance?

**A:** Edge DNS is a CDN's globally distributed DNS resolution service. Instead of resolving DNS from a single authoritative server (adding 50-200ms of latency for each DNS lookup), the CDN serves DNS responses from edge locations close to the resolver. Edge DNS reduces DNS resolution time from 100+ ms to <10 ms for most users, which is critical because DNS resolution is the first step in every HTTP request — slow DNS means slow everything.

Edge DNS also provides: DDoS protection for DNS (the CDN's edge absorbs DNS amplification attacks), global anycast (DNS queries are routed to the nearest edge), and DNS-based load balancing (responding with different IPs based on the client's location, server health, or load). For high-traffic sites, DNS resolution itself becomes a performance bottleneck — edge DNS eliminates this.

A senior edge DNS deployment: use the CDN's edge DNS as the primary authoritative DNS for the application's domains. Configure DNS records with short TTLs for records that change frequently (CDN edge IPs, failover targets) and long TTLs for stable records (MX, TXT). Monitor DNS resolution time from representative locations — if resolution exceeds 20 ms, investigate edge DNS configuration. Edge DNS is a force multiplier: improving DNS resolution improves every subsequent HTTP request's latency.

## Q80: What is a CDN's cache key design for A/B testing?

**A:** A/B testing requires serving different content variants to different users — the same URL must produce different responses based on the user's assigned variant. The cache key must include the variant identifier to prevent cross-variant cache poisoning (User A in variant 1 should not receive variant 2's cached response).

Approaches: cookie-based (the A/B testing tool sets a cookie indicating the variant; include the cookie in the cache key), header-based (the variant is passed in a custom header; include the header in the cache key), URL-based (rewrite the URL to include the variant — `/page?variant=a`; straightforward but impacts SEO and analytics), and edge-based (the edge function determines the variant and serves the correct response without caching variant-specific content — bypass cache for personalized variants).

A senior A/B testing cache design: use edge compute to determine the variant at the edge (check cookie, assign variant if not set, route to the correct content). For static variants (different images, different CSS), cache each variant separately with the variant in the cache key. For dynamic variants (different API responses), bypass cache or use per-user cache keys. The key challenge is statistical validity — the cache must not bias variant assignment. If the cache serves variant A to most users because it was cached first, the test results are skewed. Edge-side variant assignment ensures consistent, unbiased assignment regardless of caching.

## Q81: What is a load balancer's response buffering and when is it used?

**A:** Response buffering is the load balancer's ability to receive the complete response from the backend before forwarding it to the client. Without buffering, the load balancer streams the response to the client as it arrives from the backend. With buffering, the load balancer accumulates the full response, then sends it to the client in one burst.

Response buffering is used for: response transformation (modifying headers, rewriting content, injecting scripts before sending to the client), response validation (checking the response body for errors or compliance before forwarding), and compression (compressing the response at the load balancer with a more efficient algorithm than the backend uses). It also protects slow clients — the backend sends the complete response to the load balancer quickly, freeing backend resources; the load balancer handles the slow delivery to the client.

The trade-off: buffering holds the complete response in load balancer memory before sending to the client, adding latency and consuming memory. For large responses (file downloads, video streams), buffering the entire response is impractical — use streaming instead. The configuration should buffer headers and small responses, but stream large responses (configurable threshold).

## Q82: What is a CDN's cache optimization for real-time data and live events?

**A:** Real-time data (stock prices, live scores, chat messages) and live events (live streaming, live auctions) are inherently non-cacheable because the data changes continuously. The CDN's role is not caching but delivery optimization — using edge compute, WebSockets, or Server-Sent Events (SSE) to deliver real-time data efficiently.

Strategies: WebSocket connections through the CDN (the CDN terminates WebSocket at the edge and maintains persistent connections to clients — reducing origin connection load), Server-Sent Events (one-way real-time push from server to client — the CDN edge maintains the connection), and edge compute for event aggregation (the edge function aggregates multiple events and sends batched updates to clients — reducing client connection count and bandwidth). For live video streaming, segment-based caching (HLS/DASH segments cached with very short TTLs) provides near-real-time delivery with cache efficiency.

A senior real-time CDN design: use WebSockets or SSE through the CDN's edge compute platform (Cloudflare Durable Objects, Fastly Compute) for bidirectional or unidirectional real-time communication. The edge maintains connection state and forwards events from the origin — reducing origin WebSocket connection count from millions (one per client) to thousands (one per edge). For live video, use a CDN with low-latency live streaming support (Cloudflare Stream, Akamai Adaptive Media Delivery) and configure segment duration for the desired latency (2-second segments for low latency; 10-second segments for stability).

## Q83: What is a CDN's cache behavior for cookies and how should cookies be handled?

**A:** Cookies carry session state, personalization data, and tracking information. By default, CDNs include cookies in the cache key — meaning two requests with different cookies are cached separately, even if the URL and content are identical. This dramatically reduces cache hit ratio for personalized content while correctly handling session-dependent responses.

Cookie handling strategies: strip all cookies for static assets (images, CSS, JS — cookies are irrelevant to these resources and should not affect the cache key), include session cookies for authenticated content (to prevent cross-user cache poisoning), strip tracking cookies (utm_*, _ga, fbclid — these do not affect content and waste cache space), and selectively include only cookies that affect the response (configure the CDN to include only specific cookies in the cache key).

A senior cookie handling policy: configure the CDN to strip cookies from cache key for static resources (increase hit ratio from ~60% to >99%). For dynamic content, configure the CDN to include only cookies that affect the response (session cookie, user preference cookie) and strip all others. Use `Cache-Control: private` for responses that depend on cookies and should not be cached by the CDN. Monitor the impact of cookie stripping/inclusion on cache hit ratios — each site's cookie behavior is unique.

## Q84: What is a load balancer's HTTP/2 support and how does it improve performance?

**A:** HTTP/2 support at the load balancer enables multiplexing (multiple requests and responses over a single TCP connection), header compression (HPACK — reducing repeated header overhead), and server push (the server proactively sends resources the client will need). HTTP/2 eliminates the head-of-line blocking problem of HTTP/1.1 (where one slow request blocks all subsequent requests on the same connection).

The load balancer's role in HTTP/2: it terminates HTTP/2 from the client (decrypting TLS and decoding the HTTP/2 frames) and can either maintain HTTP/2 to the backend (end-to-end HTTP/2) or convert to HTTP/1.1 (HTTP/2 from client to LB, HTTP/1.1 from LB to backend). End-to-end HTTP/2 provides the best performance; conversion mode provides compatibility with backends that do not support HTTP/2.

A senior HTTP/2 deployment: enable HTTP/2 on all client-facing virtual servers (modern clients expect it — HTTP/2 is the default in all modern browsers). For internal service-to-service communication, enable HTTP/2 where the backend supports it. Monitor HTTP/2 adoption — if a significant fraction of clients still use HTTP/1.1, investigate whether the load balancer's HTTP/2 configuration is correct (ALPN negotiation, TLS configuration). HTTP/2's multiplexing reduces latency for multiplexed requests (pages with many resources) but does not improve single-stream throughput (limited by TCP congestion control).

## Q85: What is a CDN's cache optimization for healthcare applications?

**A:** Healthcare applications (EHR systems, telemedicine platforms, patient portals) have strict compliance requirements (HIPAA, HITECH) that constrain CDN caching. Protected Health Information (PHI) cannot be cached by third-party CDNs without a Business Associate Agreement (BAA). Non-PHI content (public health information, marketing pages, static assets) can be cached normally.

Strategies: route PHI through a HIPAA-compliant CDN (with BAA) or bypass CDN caching entirely for PHI endpoints, cache non-PHI content (public pages, static assets) with standard CDN policies, use edge compute for access control (validate patient identity at the edge before routing to PHI endpoints), and implement audit logging (every access to PHI is logged — CDN access logs feed into the compliance audit trail).

A senior healthcare CDN design: classify all endpoints as PHI or non-PHI. PHI endpoints: bypass CDN cache, route directly to the application (or use a HIPAA-compliant CDN with BAA). Non-PHI endpoints: cache normally. Use edge compute for access control and audit logging at the edge (every request is logged with user identity, timestamp, and resource accessed). The CDN configuration must be auditable — every rule, cache policy, and edge function must be documented and reviewed for HIPAA compliance.

## Q86: What is a CDN's cache optimization for financial services?

**A:** Financial services (trading platforms, banking applications, payment processing) require low latency, high availability, and strict data integrity. Caching financial data (stock prices, account balances, transaction history) is risky because stale data can cause financial loss or regulatory violations. The CDN must optimize for latency without compromising data accuracy.

Strategies: cache static assets aggressively (logos, fonts, CSS — no financial data), never cache sensitive financial data (account balances, transaction history, trading positions — `Cache-Control: no-store, private`), cache market data with very short TTLs (stock quotes cached for 1-5 seconds — stale quotes are better than slow quotes, but 5-second-old quotes may be unacceptable for high-frequency trading), and use edge compute for authentication and authorization (validate JWTs at the edge — reject unauthorized requests before they reach the origin).

A senior financial services CDN design: separate traffic into tiers — Tier 1 (static assets: cache aggressively), Tier 2 (market data: cache with short TTLs, stale-while-revalidate), Tier 3 (account data: bypass CDN cache, route directly to origin), Tier 4 (trading execution: bypass CDN entirely, use direct, low-latency connections). The CDN is the first layer of defense and performance optimization — but for trading-critical paths, the CDN may be bypassed entirely in favor of dedicated, low-latency network paths.

## Q87: What is a load balancer's HTTP/3 (QUIC) support and why does it matter?

**A:** HTTP/3 runs over QUIC (RFC 9000) instead of TCP, eliminating TCP's head-of-line blocking (a lost packet blocks all streams on the connection), enabling 0-RTT connection establishment (returning clients can send data immediately without a handshake), and providing built-in encryption (QUIC integrates TLS 1.3 — encryption is mandatory, not optional). HTTP/3 improves performance on lossy networks (mobile, Wi-Fi) where TCP's retransmission delays are most impactful.

The load balancer's role: terminate QUIC from the client (UDP port 443), decode HTTP/3 frames, and forward requests to the backend over HTTP/1.1, HTTP/2, or HTTP/3. The load balancer must support UDP processing (QUIC runs over UDP, not TCP) and handle QUIC-specific features (connection migration, 0-RTT, loss recovery). Cloudflare, Google Cloud Load Balancer, and Akamai support HTTP/3 natively.

A senior HTTP/3 deployment: enable HTTP/3 on client-facing virtual servers (modern browsers negotiate QUIC via Alt-Svc header or HTTPS DNS records). Monitor HTTP/3 adoption (browser support is widespread — Chrome, Firefox, Safari, Edge all support it). The performance benefit is most significant for mobile users and users on lossy networks — for users on stable, low-latency connections (desktop, wired), the improvement is marginal. HTTP/3 is a progressive enhancement — enable it without making it a requirement.

## Q88: What is a CDN's cache behavior for API gateways and how should it be configured?

**A:** API gateways aggregate multiple backend services and expose a unified API surface. CDN caching for API gateways must navigate: read-only endpoints (GET /products, GET /articles — cacheable), write endpoints (POST /orders, PUT /profile — not cacheable), and mixed endpoints (GET /user/{id} — personalized, not cacheable at CDN). The CDN must distinguish between cacheable and non-cacheable endpoints.

Configuration: `Cache-Control: public, max-age=60` for public, read-only endpoints (cache for 60 seconds), `Cache-Control: private, no-cache` for personalized endpoints (bypass CDN cache), `Cache-Control: no-store` for sensitive endpoints (never cache), and `Cache-Control: public, max-age=0, must-revalidate` for endpoints that should always check the origin (conditional caching — CDN sends conditional request to origin, avoiding transfer if unchanged).

A senior API gateway CDN design: use cache-control headers from the API gateway to instruct the CDN on cacheability per endpoint. The gateway knows which endpoints are cacheable (static reference data) and which are not (user-specific, transactional). The CDN respects these headers and caches accordingly. Monitor per-endpoint cache hit ratios — a low hit ratio on a cacheable endpoint may indicate the endpoint is returning `no-cache` headers unnecessarily; a high hit ratio on a non-cacheable endpoint may indicate incorrect cache configuration.

## Q89: What is a CDN's origin retry and failover mechanism?

**A:** Origin retry is the CDN's behavior when the origin returns an error or is unreachable on a cache miss. Instead of immediately returning the error to the client, the CDN retries the request — either to the same origin (retry on transient failure) or to an alternate origin (failover to a secondary origin). Retry logic includes: retry count (how many attempts), retry delay (wait time between attempts), retry status codes (which errors trigger retry — 502, 503, 504; not 404 or 400), and failover targets (alternate origins in different regions or data centers).

The retry mechanism handles transient failures: a momentary network glitch between CDN and origin, a brief origin overload, or a temporary DNS resolution failure. Without retry, these transient failures cause user-visible errors. With retry, the CDN automatically recovers without user impact.

A senior retry and failover design: configure retry for 5xx errors (server-side failures — transient and potentially recoverable) and connection timeouts, but not for 4xx errors (client-side errors — retrying will not fix a bad request). Set a reasonable retry count (2-3 retries with exponential backoff) to avoid cascading failures (retry storms overwhelming an already-struggling origin). Configure failover origins in geographically diverse locations (different data centers, different clouds). Test failover by deliberately disabling the primary origin and verifying that the CDN routes to the alternate. Monitor failover frequency — frequent failovers indicate an unreliable primary origin that needs investigation.

## Q90: What is a CDN's cache optimization for social media applications?

**A:** Social media applications have extreme variability in content popularity (viral posts receive millions of views; most posts receive few), real-time updates (feeds, notifications, messages), and personalization (each user's feed is unique). The CDN must handle flash crowds (viral content causing massive traffic spikes) while serving personalized feeds (each user sees different content).

Strategies: aggressive caching for viral content (the first request misses, all subsequent requests hit cache — the CDN absorbs the viral spike), edge compute for feed assembly (fetch user's feed data from edge KV, render at the edge — avoiding origin round-trips), and short TTLs for feed content (feeds change frequently — 30-60 second TTLs with stale-while-revalidate). Static assets (profile pictures, media thumbnails) are cached aggressively with long TTLs.

A senior social media CDN design: use edge compute for personalized feed rendering (the edge fetches user's follow list from KV, queries cached post data, and assembles the feed without touching the origin). Implement aggressive origin shielding (viral content hits the shield, not the origin). Use cache partitioning (separate partitions for viral content — high priority, large storage — and long-tail content — lower priority, smaller storage). Monitor cache hit ratios and origin load during viral events — the CDN should absorb >99% of viral traffic at the edge.

## Q91: What is a load balancer's connection migration and why is it important for WebSocket?

**A:** Connection migration is the ability to maintain a logical connection when the underlying transport connection changes — for example, when a mobile client switches from Wi-Fi to cellular (IP address changes) or when a load balancer failover moves the connection to a different backend. For HTTP/1.1 and HTTP/2 (TCP-based), connection migration is not possible — a changed IP means a new TCP connection. QUIC (HTTP/3) supports connection migration natively — the connection is identified by a connection ID, not the 4-tuple (source IP, source port, dest IP, dest port).

For WebSocket: connection migration is application-level — the WebSocket connection is bound to a TCP connection, and if the TCP connection breaks (network change, load balancer failover), the WebSocket disconnects. The client must reconnect and re-subscribe to channels. The load balancer can facilitate this by: maintaining session affinity (sticky sessions keep the connection on the same backend), supporting WebSocket connection draining (gracefully closing WebSocket connections during backend removal), and forwarding connection state during failover (if the backend stores WebSocket state externally, the new backend can resume the session).

A senior WebSocket migration design: store WebSocket session state externally (Redis, database) so any backend can resume a session after reconnection. Use application-level heartbeats to detect disconnections quickly. Implement client-side reconnection logic with exponential backoff. For mobile clients, detect network changes and proactively reconnect before the WebSocket times out. The load balancer's role is to support connection draining and to maintain sticky sessions during normal operation.

## Q92: What is a CDN's cache optimization for gaming applications?

**A:** Gaming applications have unique CDN requirements: large asset downloads (game patches, updates — gigabytes), low-latency asset loading (in-game textures, models — sub-100ms), real-time state synchronization (player positions, game events — real-time, non-cacheable), and anti-cheat integrity (game assets must not be tampered with — integrity verification required).

Strategies: large asset delivery via CDN with range requests (partial content delivery — resume interrupted downloads, serve specific byte ranges for patching), small asset caching (textures, models cached at edge with long TTLs), real-time state via WebSocket or UDP (not cached — real-time delivery), and integrity verification (SHA-256 checksums for downloaded assets — the client verifies after download). CDN features for gaming: token-based access control (prevent unauthorized downloads), geo-blocking (comply with regional release restrictions), and DDoS protection (protect game servers from volumetric attacks).

A senior gaming CDN design: use the CDN for asset delivery (patches, updates, in-game assets) and bypass for real-time game state (gameplay traffic). Configure large file delivery with resumable downloads (HTTP Range requests) and chunked transfer (breaking large files into manageable chunks for CDN caching). Implement integrity verification (each downloaded asset has a known hash — the client verifies after download). Use edge compute for authentication (validate player tokens at the edge before granting access to download servers).

## Q93: What is a CDN's cache optimization for educational platforms?

**A:** Educational platforms (LMS, MOOCs, video lectures, interactive exercises) have content that is highly cacheable (course materials, lecture videos, textbook PDFs) but combined with user-specific progress tracking (completion status, grades, personalized recommendations). The CDN must cache the shared content aggressively while respecting per-user data.

Strategies: course materials (PDFs, slides, images) cached with long TTLs and content-hash filenames, lecture videos cached at edge with segment-based caching (HLS/DASH), interactive exercises (HTML/JS) cached with moderate TTLs (updated infrequently), and user progress data bypassing CDN cache (served from origin or edge compute with user-specific cache keys). Pre-warm caches before course start dates (when thousands of students access the same materials simultaneously).

A senior educational platform CDN design: separate static course materials (highly cacheable, long TTL) from dynamic progress data (per-user, no CDN cache). Use edge compute for course material recommendations (the edge fetches user's progress from KV, suggests next materials, all at the edge). Monitor cache hit ratios per course — a course with a low hit ratio may have excessive personalization; a course with a high hit ratio is well-optimized. For live lectures (synchronous learning), use a live streaming CDN with low-latency delivery (WebRTC, LL-HLS).

## Q94: What is a CDN's cache optimization for government and public sector websites?

**A:** Government websites have strict accessibility requirements (WCAG compliance), security requirements (FedRAMP, FISMA), and availability requirements (99.9%+ uptime — government services must be available to citizens). Caching must balance performance with security and compliance — sensitive citizen data cannot be cached by third-party CDNs without authorization.

Strategies: public information pages (government services, public records — cache aggressively), authenticated services (tax filing, benefits applications — bypass CDN cache for authenticated sessions), security headers (CSP, HSTS, X-Frame-Options — enforced at the CDN edge), and DDoS protection (government websites are frequent DDoS targets — CDN absorbs attacks at the edge). FedRAMP-authorized CDNs (Cloudflare Federal, Akamai Government) are required for handling Controlled Unclassified Information (CUI).

A senior government CDN design: use FedRAMP-authorized CDN for all traffic (including public pages — the CDN must be authorized to process any incidental CUI in headers or URLs). Configure strict security headers at the edge (CSP, HSTS, X-Content-Type-Options). Cache public content aggressively; bypass cache for authenticated services. Implement real-time threat monitoring (detect and block attacks at the edge). Ensure the CDN's compliance documentation is current and auditable.

## Q95: What is a load balancer's WebSocket support and how does it differ from HTTP handling?

**A:** WebSocket connections start as HTTP upgrade requests and then transition to a persistent, full-duplex protocol. The load balancer must: (1) recognize the HTTP upgrade request (Upgrade: websocket header), (2) route it to the correct backend (based on URL, headers, or session affinity), (3) upgrade the connection (change from HTTP to WebSocket mode), and (4) forward WebSocket frames bidirectionally for the connection's lifetime.

The differences from HTTP: WebSocket connections are long-lived (minutes to hours vs. seconds for HTTP), bidirectional (server can push to client at any time), stateful (the connection carries session state — reconnection requires re-establishing state), and not amenable to traditional load balancing (round-robin across long-lived connections creates uneven load — some connections carry more data than others).

A senior WebSocket load balancing design: use L7 load balancers that understand the HTTP upgrade and WebSocket frames. Enable sticky sessions (route the same client's WebSocket connections to the same backend). Configure generous idle timeouts (WebSocket connections may be idle for extended periods waiting for events). Use application-level heartbeats (ping/pong frames) to detect dead connections. Monitor WebSocket connection count, connection duration, and messages per connection — long-lived connections consume load balancer resources differently than short-lived HTTP connections.

## Q96: What is a CDN's cache behavior for server-side rendered (SSR) applications?

**A:** Server-side rendered applications (Next.js SSR, Nuxt.js, Remix) generate HTML on the server for each request — providing faster first contentful paint (FCP) and better SEO than client-side rendering. However, SSR responses are often dynamic (personalized per user, data-dependent) and challenge traditional CDN caching strategies.

Strategies: `ISR` (Incremental Static Regeneration — Next.js feature where pages are statically generated and revalidated in the background at configurable intervals — the CDN caches the static page for the revalidation period), `stale-while-revalidate` (CDN serves cached page while refreshing in background), `edge rendering` (generate the page at the edge using edge compute — the origin is only consulted for data not available at the edge), and hybrid rendering (static pages cached at CDN, dynamic pages bypass cache). The choice depends on the page's personalization level and freshness requirements.

A senior SSR CDN design: use ISR or stale-while-revalidate for pages with moderate personalization (product pages, articles — personalized by URL, not by user). Use edge rendering for pages with light personalization (user name in header, recommendations — the edge fetches user data from KV and renders). Bypass cache for fully personalized pages (dashboards, settings — `Cache-Control: private`). Monitor SSR-specific metrics: time to first byte (TTFB), first contentful paint (FCP), and cache hit ratio for SSR pages.

## Q97: What is a CDN's cache optimization for IoT data and APIs?

**A:** IoT applications generate high volumes of small, frequent data updates (sensor readings every second, device status updates every minute) and serve data to dashboards and analytics platforms. Caching IoT data requires balancing freshness (dashboard data should be near-real-time) with origin load (thousands of devices reporting every second generates enormous write traffic to the origin).

Strategies: cache aggregated analytics data (1-minute, 5-minute, 15-minute aggregates — cached with appropriate TTLs), bypass cache for raw sensor data (real-time, per-device data — not cacheable), use edge compute for data aggregation (aggregate sensor readings at the edge, forward aggregates to origin — reducing origin write volume), and cache dashboard assets (charts, maps, static UI — cached aggressively). For IoT API queries (GET /devices/{id}/readings), use short TTLs (5-30 seconds) to balance freshness and cache efficiency.

A senior IoT CDN design: separate the data path (device → origin: high-volume, low-latency writes — not CDN-cached) from the query path (origin → dashboard: aggregated reads — CDN-cached). Use edge compute for real-time aggregation (the edge receives device data, aggregates over time windows, and forwards aggregates to origin — reducing origin write volume by 10-100x). Cache aggregated dashboard data at the edge with short TTLs. The CDN's role is to optimize the read path (dashboard queries), not the write path (device telemetry).

## Q98: What is a load balancer's cookie-based session affinity implementation and how does it work?

**A:** Cookie-based session affinity (also called cookie-based sticky sessions) uses an HTTP cookie to track which backend a client is connected to. When the client's first request hits the load balancer, the load balancer selects a backend, and injects a cookie into the response (e.g., `Set-Cookie: LBID=server3; Path=/`). On subsequent requests, the load balancer reads the cookie and routes to the same backend.

Two implementation approaches: insert cookie (the load balancer inserts a cookie into the response — the application does not need to modify its code) and application cookie (the application sets its own session cookie, and the load balancer reads it to determine the backend — the application controls session management). Insert cookie is simpler (no application changes) but the cookie is managed by the load balancer (must be configured to match the application's path and domain requirements). Application cookie integrates with the application's session management but requires the load balancer to parse application cookies.

A senior cookie affinity configuration: set the cookie's Path to `/` (or the appropriate application path), Domain to the application's domain, HttpOnly flag (prevent JavaScript access — security), and Secure flag (HTTPS only). Configure the cookie's lifetime to match the application's session duration — if the application session expires in 30 minutes, the cookie should expire in 30 minutes or less. Monitor the affinity distribution — if the cookie is not being sent (client blocks cookies, cookie domain mismatch), the client falls back to round-robin, breaking affinity.

## Q99: What is a CDN's cache optimization for single-page applications (SPAs)?

**A:** Single-page applications (React, Angular, Vue) load one HTML shell (index.html) and then dynamically render content via JavaScript. The HTML shell is the same for all users and is highly cacheable; the dynamic content is fetched via API calls and rendered client-side. The CDN must cache the HTML shell aggressively while correctly handling API caching and asset versioning.

Strategies: cache the HTML shell with long TTLs and serve via `Cache-Control: max-age=300, stale-while-revalidate=3600` (5-minute TTL with 1-hour stale-while-revalidate — the shell is updated in the background), cache static assets (JS, CSS, images) with content-hash filenames and immutable headers (indefinite caching), and handle API calls appropriately (public APIs cached with short TTLs; authenticated APIs bypassed). Use service workers for offline support and client-side caching.

A senior SPA CDN design: use `Cache-Control: no-cache` or `must-revalidate` for the HTML shell (the CDN must always check with the origin — using ETags or Last-Modified headers — before serving the cached version). This ensures the HTML always references the latest asset hashes. Cache all referenced assets with content-hash filenames and immutable headers. For API calls, use `Cache-Control` headers per endpoint (public data: short TTL; private data: `no-cache`). The SPA's cache strategy is split: the HTML shell is revalidated on every request; the assets are cached indefinitely until the URL changes.

## Q100: What is a CDN's cache behavior for WebSocket connections and how does it differ from HTTP caching?

**A:** WebSocket connections are not cacheable by CDN caches — they are persistent, bidirectional, and stateful, with no concept of cache hit or miss. The CDN's role for WebSocket is not caching but transport optimization: terminating WebSocket at the edge, maintaining persistent connections to clients, and forwarding messages to backends. The CDN may use connection pooling to reduce backend connection count (many client connections at the edge, fewer backend connections).

The differences from HTTP caching: HTTP is request-response (cache stores responses keyed by request); WebSocket is a persistent bidirectional stream (no request-response pattern to cache). HTTP caching reduces origin load by serving cached responses; WebSocket caching is not applicable — every message is unique and real-time. HTTP caching improves latency (cache hit is faster than origin fetch); WebSocket latency is determined by the edge-to-client connection quality, not caching.

A senior WebSocket CDN deployment: use the CDN's WebSocket support (Cloudflare, Akamai, Fastly all support WebSocket proxying) for connection management and DDoS protection at the edge. Configure the CDN to proxy WebSocket connections to backends — the CDN handles TLS termination, connection management, and rate limiting. For pub/sub patterns, use edge compute (Cloudflare Durable Objects, Fastly Compute) to manage channel subscriptions at the edge — each edge node handles its connected clients' subscriptions and receives messages from the origin only for channels it manages. The CDN optimizes WebSocket delivery by reducing round-trips (edge-to-client is short; edge-to-origin may be long).

