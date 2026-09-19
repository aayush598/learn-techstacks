# Protocol Comparison Questions — 100 Interview Q&A

## Q1: What are the key differences between TCP and UDP?

**A:** TCP is a connection-oriented protocol that establishes a reliable, ordered delivery of data through a three-way handshake, while UDP is connectionless and provides no guarantees for delivery, ordering, or error correction. TCP uses sequence numbers, acknowledgments, and retransmission to ensure reliability, whereas UDP simply sends packets without tracking their arrival.

TCP includes flow control through sliding windows and congestion control mechanisms like slow start and congestion avoidance to prevent network overwhelming. UDP has no built-in flow or congestion control, making it simpler and faster but potentially causing network congestion if not managed at the application layer.

TCP headers are larger (20-60 bytes) compared to UDP headers (8 bytes), introducing more overhead. This makes TCP better suited for applications requiring data integrity like web browsing, email, and file transfers, while UDP excels in real-time applications like video streaming, gaming, and DNS lookups where speed and low latency outweigh the need for perfect reliability.

## Q2: When would you choose UDP over TCP in a production environment?

**A:** UDP is preferred in scenarios where low latency is critical and some data loss is acceptable. Real-time multimedia applications like video conferencing (Zoom, Teams), live streaming (Twitch), and VoIP (Skype) benefit from UDP because retransmitting lost packets would cause noticeable delays and jitter that degrade user experience.

Gaming applications, both casual and competitive, use UDP because players need immediate feedback and can tolerate occasional dropped updates rather than waiting for retransmissions. DNS resolution also uses UDP for queries under 512 bytes because the request-response pattern is simple and the overhead of TCP's connection setup would unnecessarily slow down name resolution.

IoT and telemetry applications often use UDP when sending sensor readings where occasional missing data points are acceptable, and the battery savings from reduced protocol overhead matter. However, if an application needs UDP's speed but also requires reliability, developers implement custom reliability mechanisms at the application layer, as seen in protocols like QUIC which builds reliable communication on top of UDP.

## Q3: How does HTTP/1.1 differ from HTTP/2 in terms of performance?

**A:** HTTP/1.1 uses one request per TCP connection (or pipelining which is rarely used) and requires multiple connections for parallel requests, leading to head-of-line blocking at the HTTP level. HTTP/2 introduces multiplexing, allowing multiple requests and responses to be transmitted simultaneously over a single TCP connection using streams, eliminating the need for multiple connections.

HTTP/2 also provides header compression through HPACK, reducing the overhead of repetitive header data that HTTP/1.1 sends with every request. Additionally, HTTP/2 supports server push, enabling servers to proactively send resources to clients before they request them, reducing round trips for critical assets.

However, HTTP/2 still operates over TCP, so it inherits TCP's head-of-line blocking at the transport layer. A single lost packet in HTTP/2 blocks all streams on that connection, whereas HTTP/1.1's multiple connections allow unaffected streams to continue. This limitation is addressed by HTTP/3, which uses QUIC over UDP instead.

## Q4: What problem does HTTP/3 solve that HTTP/2 cannot?

**A:** HTTP/3's primary innovation is eliminating head-of-line blocking at the transport layer by using QUIC (built on UDP) instead of TCP. In HTTP/2, while streams can be multiplexed at the application layer, TCP treats all data as a single byte stream, so a lost packet blocks all streams until retransmission completes. HTTP/3 gives each stream independent reliability, so lost packets only affect their specific stream.

QUIC integrates TLS 1.3 directly into the handshake, reducing connection setup time. While TCP requires one round trip for the three-way handshake plus another for TLS, QUIC combines these into a single round trip for new connections and supports zero round trip resumption for returning clients, significantly improving connection establishment speed.

HTTP/3 also provides built-in connection migration. When a client switches networks (e.g., from WiFi to cellular), TCP connections break because they're tied to IP and port pairs. QUIC connections use connection IDs instead, allowing seamless network transitions without re-establishing connections, which is particularly valuable for mobile applications.

## Q5: Compare TCP's three-way handshake with QUIC's handshake process.

**A:** TCP's three-way handshake involves three steps: the client sends a SYN, the server responds with SYN-ACK, and the client completes with an ACK, taking one full round trip before data can be transmitted. If TLS is involved, an additional round trip occurs for the TLS handshake after the TCP connection is established, totaling two round trips minimum.

QUIC's handshake combines transport and cryptographic setup into a single process. For new connections, QUIC sends an initial packet with key material, the server responds with its certificate and key exchange, and the client can immediately send encrypted data, achieving connection establishment in one round trip. This matches TCP's data transmission start time while also providing encryption.

For repeat connections to the same server, QUIC achieves zero round trip connection resumption. The client caches cryptographic parameters from previous connections and can send encrypted data immediately in its first packet, eliminating connection setup latency entirely. This is particularly beneficial for HTTP request/response patterns where clients frequently reconnect to the same servers.

## Q6: What are the main differences between IPv4 and IPv6?

**A:** IPv4 uses 32-bit addresses providing approximately 4.3 billion unique addresses, while IPv6 uses 128-bit addresses offering approximately 340 undecillion addresses, effectively solving IPv4 address exhaustion. IPv6 addresses are written in hexadecimal with colons separating groups, whereas IPv4 uses dotted decimal notation.

IPv6 simplifies the header structure by removing fields like checksum and fragment offset from the base header, relying on extension headers instead. This makes IPv6 router processing more efficient. IPv6 also eliminates the need for NAT by providing enough addresses for direct end-to-end connectivity, though NAT64 exists for transition scenarios.

IPv6 includes built-in features like IPsec support (though optional in practice), stateless address autoconfiguration (SLAAC) for automatic address assignment without DHCP, and neighbor discovery protocol replacing ARP. IPv6 also supports more efficient multicast routing and anycast addressing natively, improving content delivery and service discovery.

## Q7: How does TLS 1.3 improve upon TLS 1.2?

**A:** TLS 1.3 reduces the handshake from two round trips to one by allowing clients to send key exchange parameters with their initial ClientHello, enabling servers to compute and send the master secret immediately. TLS 1.3 also removes support for weak cryptographic algorithms like RSA key transport, CBC mode ciphers, RC4, and MD5, enforcing only secure algorithms like AES-GCM and ChaCha20.

TLS 1.3 encrypts more of the handshake, including the server certificate, by using ephemeral Diffie-Hellman key exchange for forward secrecy by default. In TLS 1.2, the server certificate was sent in cleartext, potentially leaking information about which sites a client was visiting.

The protocol simplification in TLS 1.3 reduces attack surface and makes implementations easier to secure. It also adds 0-RTT resumption, allowing clients to send application data immediately when reconnecting, though this comes with replay attack considerations that implementations must address.

## Q8: What is the difference between TLS and IPsec for securing network traffic?

**A:** TLS operates at the transport layer (or application layer when wrapping TCP connections), securing individual application protocols like HTTP, SMTP, or FTP. It establishes secure sessions between specific endpoints, making it ideal for web traffic, email, and application-specific encryption where end-to-end security between client and server is needed.

IPsec operates at the network layer, securing all IP traffic between two network endpoints regardless of the application. It uses two main protocols: AH (Authentication Header) for integrity and authentication, and ESP (Encapsulating Security Payload) for encryption, authentication, and integrity. IPsec is commonly used for site-to-site VPNs and can secure entire network connections transparently.

The choice depends on use case: TLS is preferred for web applications and client-server communication where application-layer visibility is important. IPsec is better for network-level security like connecting entire office networks, securing all traffic from a device regardless of application, or when you need to encrypt traffic that cannot be modified at the application layer.

## Q9: Compare connection-oriented and connectionless network services with examples.

**A:** Connection-oriented services establish a dedicated communication path before data transfer, maintaining state throughout the session. TCP is the classic example, requiring the three-way handshake to set up a connection, tracking sequence numbers and acknowledgments, and tearing down with FIN packets. Virtual circuits in ATM and Frame Relay also provide connection-oriented services at the data link and network layers.

Connectionless services send packets without establishing a session, treating each packet independently. UDP exemplifies this at the transport layer, while IP provides connectionless network layer delivery. Each packet is routed independently, with no guarantee of order, delivery, or duplicate prevention. Datagram networks like the traditional Internet are built on connectionless principles.

The trade-off is reliability versus efficiency. Connection-oriented services provide guaranteed delivery, ordering, and flow control but incur setup overhead and resource commitment. Connectionless services are faster and more resilient to network changes since packets can take different routes, but applications must handle reliability if needed. Modern networks often use connectionless transport with application-layer reliability (like QUIC) to get the best of both approaches.

## Q10: What are the differences between a hub, switch, and router?

**A:** A hub operates at Layer 1 (Physical) of the OSI model, simply repeating incoming electrical signals to all ports regardless of destination. It creates a single collision domain, meaning all connected devices share the same bandwidth and collisions can occur when multiple devices transmit simultaneously. Hubs are largely obsolete in modern networks.

A switch operates at Layer 2 (Data Link), using MAC addresses to forward frames only to the intended destination port. It maintains a MAC address table learned from incoming frame source addresses, creating separate collision domains per port. Switches provide full bandwidth to each port and can operate in full-duplex mode, eliminating collisions entirely in properly configured networks.

A router operates at Layer 3 (Network), using IP addresses to forward packets between different networks. It maintains routing tables and makes forwarding decisions based on destination IP addresses. Routers provide network segmentation, can implement access control lists for security, and handle protocol translation between different network types. They are essential for connecting different subnets and providing internet connectivity.

## Q11: Compare static routing and dynamic routing protocols.

**A:** Static routing involves manually configuring routes in a router's routing table, specifying the next hop or exit interface for each destination network. It provides complete control over traffic paths, consumes no router CPU or bandwidth for route exchanges, and is suitable for small, stable networks with predictable traffic patterns. However, static routes don't adapt to network changes and require manual reconfiguration when topology changes.

Dynamic routing protocols automatically exchange routing information between routers, adapting to network changes in real-time. Protocols like OSPF, EIGRP, and BGP build and maintain routing tables through regular updates and neighbor relationships. They detect link failures and recalculate optimal paths, providing fault tolerance and load balancing capabilities that static routing cannot match.

The choice depends on network size and complexity. Small networks with few routers benefit from static routing's simplicity and predictability. Large enterprise and service provider networks require dynamic routing to handle frequent changes, provide redundancy, and scale efficiently. Many production networks use a combination, with static routes for default gateways and specific policy routes, while dynamic protocols handle internal routing.

## Q12: What is the difference between symmetric and asymmetric encryption?

**A:** Symmetric encryption uses the same key for both encryption and decryption, requiring both parties to share the secret key securely. Algorithms like AES, ChaCha20, and 3DES are symmetric and provide fast encryption suitable for bulk data transfer. The challenge is key distribution—how do you securely share the key with the intended recipient without exposing it to others?

Asymmetric encryption uses a key pair: a public key for encryption and a private key for decryption. RSA, ECC, and Ed25519 are asymmetric algorithms. Anyone can encrypt data using the public key, but only the private key holder can decrypt it. This solves the key distribution problem but is computationally expensive, making it unsuitable for encrypting large amounts of data directly.

Modern protocols like TLS use both: asymmetric encryption establishes a secure channel and exchanges a symmetric session key, then symmetric encryption protects the actual data transfer. This hybrid approach combines asymmetric encryption's secure key exchange with symmetric encryption's performance, providing both security and efficiency for encrypted communications.

## Q13: How does DNS resolution differ between recursive and iterative queries?

**A:** In recursive queries, the client sends a DNS request to a resolver (typically provided by the ISP or a public DNS service like 8.8.8.8), which takes full responsibility for resolving the domain name. The resolver queries multiple DNS servers on behalf of the client, following the hierarchy from root servers to TLD servers to authoritative servers, and returns the final answer to the client in a single response.

In iterative queries, each DNS server responds with either the answer or a referral to the next server in the hierarchy. The client (or stub resolver) must follow each referral, querying each server in turn until reaching the authoritative server. This distributes the resolution work across multiple servers but requires the client to handle the iterative process.

Recursive queries are more common in practice because end-user devices typically configure a recursive resolver. This reduces load on authoritative DNS servers and provides caching benefits at the resolver level. However, recursive resolvers become single points of failure and can introduce privacy concerns since they can observe all DNS queries from their clients.

## Q14: Compare TCP flow control and congestion control mechanisms.

**A:** Flow control prevents a fast sender from overwhelming a slow receiver by using a sliding window mechanism. The receiver advertises its available buffer space in each ACK, and the sender limits its outstanding data to this window size. This is per-connection and prevents the receiver from being flooded regardless of network conditions.

Congestion control prevents senders from collectively overwhelming the network. TCP uses algorithms like slow start, congestion avoidance, fast retransmit, and fast recovery to probe available bandwidth. Starting with a small congestion window, TCP exponentially increases it during slow start until packet loss occurs, then reduces and probes more conservatively during congestion avoidance.

The key difference is scope: flow control is end-to-end between sender and receiver, while congestion control considers the entire network path. A connection might have ample receiver buffer (no flow control limitation) but still be congested because the network path cannot handle the data rate (congestion control limitation). Both work together to ensure efficient, fair, and stable data transfer across diverse network conditions.

## Q15: What are the differences between unicast, broadcast, and multicast communication?

**A:** Unicast represents one-to-one communication where a single source sends data to a specific destination identified by a unique address. This is the most common communication model in IP networks, used for web browsing, email, file transfers, and most client-server applications. Every packet has a specific source and destination IP address.

Broadcast represents one-to-all communication where a source sends data to all devices on a network segment. IPv4 uses the broadcast address (typically x.x.x.255 for /24 networks) to reach all hosts. Broadcast is used for ARP requests, DHCP discovery, and protocols that need to communicate with all local devices. Broadcast traffic is limited to the local broadcast domain and cannot cross routers by default.

Multicast represents one-to-many communication where a source sends data to a group of interested receivers. Using Class D IP addresses (224.0.0.0 to 239.255.255.255), multicast allows efficient distribution of content to multiple subscribers without sending separate unicast streams. Applications include video conferencing, IPTV, software updates, and financial data feeds. Multicast requires protocol support (IGMP, PIM) throughout the network infrastructure.

## Q16: Compare connection pooling and persistent connections in HTTP.

**A:** Persistent connections (HTTP keep-alive) allow multiple HTTP requests to reuse a single TCP connection, avoiding the overhead of opening new connections for each request. HTTP/1.1 enables persistent connections by default, while HTTP/1.0 required the Connection: keep-alive header. This reduces latency from TCP handshakes and improves performance for multiple sequential requests.

Connection pooling goes further by maintaining a pool of pre-established connections that can be immediately reused for new requests. Pooling manages connection lifecycle, including creation, reuse, and cleanup of idle connections. It typically includes configurable limits on total connections and per-server connections to prevent resource exhaustion while maximizing reuse benefits.

The distinction matters at scale: persistent connections help individual clients reuse connections to a server, while connection pooling manages server-side or proxy-side resources efficiently. A web server might maintain connection pools to databases, backend services, or upstream proxies, managing hundreds or thousands of connections efficiently. Connection pooling also handles connection health monitoring and automatic replacement of stale connections.

## Q17: What is the difference between a TCP socket and a UDP socket?

**A:** A TCP socket represents one endpoint of a TCP connection, identified by the tuple (source IP, source port, destination IP, destination port). TCP sockets maintain state including sequence numbers, acknowledgment numbers, window sizes, and congestion control variables. The socket API provides stream-oriented semantics, meaning data is treated as a continuous byte stream with no message boundaries.

A UDP socket is connectionless and can receive datagrams from any source. While UDP sockets can be "connected" to a specific remote address using connect(), this only filters incoming datagrams and doesn't establish a connection state like TCP. UDP sockets provide message-oriented semantics where each send/recv operation corresponds to a complete datagram.

From a programming perspective, TCP sockets use send() and recv() for stream I/O, while UDP sockets use sendto() and recvfrom() to specify or receive the peer address with each message. TCP sockets block or return errors on connection failures, while UDP sockets silently discard unsent datagrams when buffers are full, requiring application-level handling for reliability.

## Q18: Compare NAT (Network Address Translation) with proxy servers.

**A:** NAT operates at the network layer, translating private IP addresses to public addresses by modifying packet headers as they traverse the NAT device. It maintains a translation table mapping internal (private IP, port) pairs to external (public IP, port) pairs, allowing multiple internal hosts to share a single public IP address. NAT is transparent to applications and doesn't require client configuration.

Proxy servers operate at the application layer, receiving client requests and forwarding them to destination servers on behalf of clients. Proxies understand the application protocol (HTTP, FTP, etc.) and can inspect, modify, cache, or filter content. They provide anonymity by hiding client IPs and can implement access control, content filtering, and caching for performance improvement.

The key difference is transparency and capability. NAT is invisible to applications—they communicate normally, and NAT handles address translation transparently. Proxies require application awareness and often client configuration (proxy settings). NAT conserves public IP addresses but provides limited security, while proxies offer content control, caching, and logging but add complexity and potential performance overhead.

## Q19: What are the differences between IPv4 private address ranges and IPv6 unique local addresses?

**A:** IPv4 defines three private address ranges: 10.0.0.0/8 (10.0.0.0 to 10.255.255.255), 172.16.0.0/12 (172.16.0.0 to 172.31.255.255), and 192.168.0.0/16 (192.168.0.0 to 192.168.255.255). These addresses are not routable on the public Internet and require NAT for Internet access. They were defined in RFC 1918 to address IPv4 address exhaustion.

IPv6 unique local addresses (ULAs) use the prefix fc00::/7 (specifically fd00::/8 for locally assigned), designed for private networks that may never connect to the public Internet or need isolated address spaces. Unlike IPv4 private addresses, ULAs are meant to be globally unique through a pseudo-random generation algorithm, reducing the chance of collision when networks merge.

The practical difference is that IPv4 private addresses are workarounds for address scarcity, requiring NAT for Internet connectivity and introducing complications like double NAT and broken end-to-end connectivity. IPv6 ULAs serve a different purpose—providing stable, private addressing for internal networks while global unicast addresses handle Internet connectivity, eliminating the need for NAT and preserving true end-to-end connectivity.

## Q20: How does a CDN differ from a traditional web server architecture?

**A:** A traditional web server architecture centralizes all content on one or a few servers, requiring all users to connect to the same location regardless of geographic distance. This creates latency for distant users, single points of failure, and capacity limitations during traffic spikes. Content delivery is limited by the server's bandwidth and geographic reach.

A CDN distributes copies of static and dynamic content across multiple edge servers positioned in data centers worldwide (points of presence or PoPs). Users connect to the nearest edge server, dramatically reducing latency and load times. CDNs handle static assets (images, CSS, JavaScript) through caching, and increasingly support dynamic content through edge computing and intelligent routing.

CDNs provide additional benefits including DDoS protection through distributed architecture, improved availability through redundancy, reduced origin server load through caching and offloading, and analytics on traffic patterns. The CDN sits between users and origin servers, handling the majority of requests at the edge while forwarding cache misses to the origin, creating a scalable content delivery architecture.

## Q21: Compare HTTP cookies, tokens, and sessions for maintaining state.

**A:** HTTP cookies are small pieces of data stored in the browser and sent with every request to a domain. They can be session cookies (deleted when the browser closes) or persistent cookies (with expiration dates). Cookies are automatically managed by browsers and can store user preferences, authentication tokens, and tracking identifiers. They're limited to approximately 4KB per cookie and are sent with every request, adding overhead.

Sessions are server-side storage mechanisms that maintain user state across requests. The server generates a unique session ID, typically stored in a cookie, and associates it with server-side data (user info, shopping cart, etc.). The actual session data never leaves the server, providing better security than storing sensitive information in cookies. Sessions require server memory or external storage (Redis, database) and must handle expiration and cleanup.

Tokens (like JWTs) are self-contained, stateless credentials that encode user information and permissions. Unlike sessions, tokens carry all necessary data and don't require server-side storage, making them ideal for distributed systems and microservices. Tokens can be validated without database lookups but cannot be easily revoked, requiring additional mechanisms like token blacklists for logout functionality.

## Q22: What is the difference between a load balancer operating at Layer 4 versus Layer 7?

**A:** Layer 4 load balancers operate at the transport layer, routing traffic based on TCP/UDP connection information (source/destination IPs and ports). They make forwarding decisions without inspecting packet contents, providing high performance and low latency. Layer 4 load balancers can perform basic health checks and connection tracking but cannot make content-based routing decisions.

Layer 7 load balancers operate at the application layer, inspecting HTTP/HTTPS headers, cookies, URLs, and content to make intelligent routing decisions. They can route requests based on URL path, host headers, cookies, or application data. Layer 7 load balancers can perform SSL termination, compression, caching, and content transformation, providing more flexibility at the cost of higher processing overhead.

The choice depends on requirements: Layer 4 is ideal for high-throughput, low-latency applications where simple load distribution suffices, like database clusters or game servers. Layer 7 is necessary for web applications requiring content-based routing (e.g., routing /api requests to backend servers and /static requests to cache servers), SSL offloading, or request manipulation. Many deployments use Layer 4 in front of Layer 7 load balancers for tiered architecture.

## Q23: Compare TCP and SCTP (Stream Control Transmission Protocol).

**A:** TCP provides reliable, ordered byte-stream delivery over a single path between two endpoints. It uses a three-way handshake for connection establishment and supports features like flow control, congestion control, and urgent data. TCP's weakness is its single-path limitation and susceptibility to head-of-line blocking, where one lost packet blocks all subsequent data.

SCTP adds several features: multi-streaming (multiple independent message streams within one association preventing head-of-line blocking), multi-homing (supporting multiple IP addresses per endpoint for path redundancy), and message-oriented delivery (preserving message boundaries like UDP). SCTP also has a four-way handshake providing protection against SYN flood attacks and cookie-based authentication.

SCTP is used in telecom signaling (SS7 over IP), WebRTC data channels, and applications needing multi-path reliability. However, SCTP adoption is limited because TCP with QUIC addresses many of its innovations, and SCTP's unfamiliarity to developers and limited support in browsers and middleboxes restricts deployment. TCP remains dominant due to simplicity, widespread support, and continuous improvements like BBR congestion control.

## Q24: How does HTTP caching differ between browser caching and server-side caching?

**A:** Browser caching stores HTTP responses locally on the user's device, controlled by HTTP headers like Cache-Control, Expires, ETag, and Last-Modified. The browser checks its cache before making network requests, serving cached responses when valid without contacting the server. Browser cache reduces latency and bandwidth usage but is per-user and cannot share cached content across users.

Server-side caching stores responses on intermediate servers (CDNs, reverse proxies like Varnish, or application caches like Redis) shared among multiple users. Server caches can store pre-rendered pages, database query results, or computed responses. When a request arrives, the cache server checks its storage and returns cached content if available, reducing load on backend servers.

The key difference is scope and control. Browser caching is controlled by response headers and reduces individual user latency. Server-side caching provides shared benefits across all users accessing the cache and can implement more sophisticated invalidation strategies. Optimal architectures layer both: server caches reduce backend load while browser caches reduce even cache server load for repeat visitors.

## Q25: Compare IPv4 subnetting with IPv6 prefix delegation.

**A:** IPv4 subnetting divides networks into smaller subnets using subnet masks (e.g., /24, /25, /26), borrowing host bits for network identification. Subnet planning requires careful allocation to avoid waste, and variable-length subnet masks (VLSM) allow different-sized subnets within the same network. Subnetting decisions are permanent and require renumbering if requirements change.

IPv6 prefix delegation uses router advertisements and DHCPv6-PD to assign entire /64 prefixes (or other sizes) to downstream networks. Each subnet automatically receives a /64 prefix, which provides approximately 18 quintillion addresses per subnet, eliminating the need for careful host-address planning. The hierarchical structure (typically /48 site, /56 customer, /64 subnet) simplifies routing and management.

The fundamental difference is philosophy: IPv4 subnetting conserves addresses through careful division, while IPv6 prefix delegation embraces abundant addressing by providing generous prefixes. IPv6's automatic configuration and hierarchical addressing reduce administrative overhead, but organizations still need address management plans for security, compliance, and operational clarity in large deployments.

## Q26: Compare BGP and OSPF for routing between autonomous systems.

**A:** BGP (Border Gateway Protocol) is the standard protocol for routing between autonomous systems (AS) on the Internet. It's a path vector protocol that makes routing decisions based on AS path length, policies, and business relationships rather than just technical metrics. BGP handles massive routing tables (over 900,000 IPv4 prefixes) and supports complex policy-based routing for traffic engineering.

OSPF (Open Shortest Path First) is designed for routing within a single autonomous system (IGP). It's a link-state protocol that builds complete topology maps and calculates shortest paths using Dijkstra's algorithm. OSPF converges quickly after topology changes, supports hierarchical area design for scalability, and uses cost metrics based on link bandwidth for path selection.

The choice depends on scope: OSPF excels within enterprise networks and data centers where fast convergence and metric-based routing are priorities. BGP is essential for Internet connectivity and multi-homed networks where policy controls and AS-level routing decisions matter. Many large networks run OSPF internally and BGP at the edge, with redistribution between them.

## Q27: How does TCP's slow start algorithm differ from congestion avoidance?

**A:** Slow start begins when a TCP connection starts or after a timeout, exponentially increasing the congestion window (cwnd) from 1 segment, doubling it each round trip time (RTT). This rapid growth allows TCP to quickly probe available bandwidth while starting conservatively. Slow start continues until the cwnd reaches the slow start threshold (ssthresh) or packet loss occurs.

Congestion avoidance activates once cwnd reaches ssthresh, switching from exponential to linear growth. The cwnd increases by approximately one segment per RTT, providing more conservative bandwidth probing. This phase continues until packet loss occurs, indicating network congestion. Upon loss, TCP reduces cwnd and may trigger fast retransmit if duplicate ACKs are received.

The transition between these phases balances responsiveness and stability. Slow start quickly utilizes available bandwidth in initially empty networks, while congestion avoidance prevents oscillation and provides fairness among competing flows. Modern TCP variants like CUBIC and BBR modify these algorithms but maintain the core principle of aggressive initial probing followed by conservative steady-state behavior.

## Q28: What is the difference between TCP's FIN and RST for connection termination?

**A:** FIN (Finish) initiates a graceful connection shutdown. The sender transmits a FIN segment to indicate it has finished sending data, but can still receive data. The receiver acknowledges the FIN and continues sending until it's ready to close, then sends its own FIN. This four-way termination ensures all data is delivered and both sides agree to close, maintaining reliability guarantees until the end.

RST (Reset) immediately terminates a connection due to error conditions. It's sent when a host receives data for a connection that doesn't exist, when a host crashes and reboots losing connection state, or when a host rejects an incoming connection request. RST bypasses the normal termination sequence, discarding any queued data.

FIN is the normal, cooperative way to end connections, used in web browsers closing tabs or applications shutting down gracefully. RST is the emergency exit, signaling abnormal conditions. Applications that need immediate termination (like killing a process) or encounter errors send RST to avoid leaving half-open connections that consume resources.

## Q29: Compare static NAT, dynamic NAT, and PAT (Port Address Translation).

**A:** Static NAT creates a permanent one-to-one mapping between a private IP address and a public IP address. Internal servers that need consistent public addressing (like web servers or mail servers) use static NAT so external clients can always reach them at the same address. The mapping exists as long as the NAT configuration remains.

Dynamic NAT assigns public IP addresses from a pool to internal hosts on a first-come, first-served basis. When an internal host needs Internet access, it receives an available public IP from the pool. When the translation times out or the host disconnects, the public IP returns to the pool. Dynamic NAT provides no consistent external addressing for internal services.

PAT (Port Address Translation), also called NAT overload, maps multiple private IP addresses to a single public IP address by differentiating connections using port numbers. A unique (private IP, private port, public IP, public port) tuple identifies each connection. PAT is the most common form of NAT in home and small business routers, enabling hundreds of devices to share one public IP address.

## Q30: How does SSL/TLS certificate validation differ from certificate pinning?

**A:** Standard SSL/TLS certificate validation follows a chain of trust from the server certificate to a trusted Certificate Authority (CA) root certificate stored in the operating system or browser. The client verifies the certificate's validity period, domain name match, revocation status, and that the certificate chain traces back to a trusted CA. This provides general security but relies on all CAs being trustworthy.

Certificate pinning restricts connections to specific certificates or public keys rather than trusting any CA-signed certificate. The application stores (pins) the expected certificate or public key and rejects connections using different certificates, even if signed by a trusted CA. This protects against compromised CAs issuing fraudulent certificates for domains they don't control.

The trade-off is security versus flexibility. Standard validation provides broad compatibility and automatic protection as CAs are added or removed. Certificate pinning offers stronger protection against specific attack vectors but requires manual updates when certificates change, complicating rotation and increasing the risk of connectivity issues if pins aren't managed properly. Modern approaches like HPKP (HTTP Public Key Pinning) attempted to standardize pinning but were deprecated due to operational risks.

## Q31: Compare connection-oriented and datagram-oriented approaches in network programming.

**A:** Connection-oriented programming (like TCP sockets) establishes a dedicated communication channel before data transfer. The programming model uses stream semantics—data sent by one side appears as a continuous stream to the other, without message boundaries. This simplifies programming for applications that need reliable, ordered data delivery, as the socket handles retransmission and ordering.

Datagram-oriented programming (like UDP sockets) sends individual messages without establishing a connection. Each send/recv operation corresponds to one complete message, preserving message boundaries. The programmer must handle reliability, ordering, and fragmentation if needed. This model suits applications that need message-level semantics like DNS, VoIP, or gaming where individual messages have independent meaning.

The programming differences extend to error handling and buffering. TCP sockets block or error on connection failures, while UDP sockets silently discard data. TCP buffers incoming data, potentially coalescing multiple sends into larger receives. UDP preserves individual datagram boundaries, simplifying protocol design but requiring careful buffer management. Applications choose based on whether they need reliable streams or discrete messages.

## Q32: How does HTTP/1.1 pipelining differ from HTTP/2 multiplexing?

**A:** HTTP/1.1 pipelining allows clients to send multiple requests without waiting for responses, but responses must return in the same order requests were sent. This introduces head-of-line blocking—if the first response is large or delayed, subsequent responses queue behind it even if they're ready. Pipelining also required servers to handle out-of-order requests correctly, which many didn't implement properly.

HTTP/2 multiplexing sends multiple requests as independent streams within a single TCP connection. Responses can return in any order—small responses can complete before large ones even if requested later. Each stream has its own flow control and can be prioritized, allowing browsers to prioritize critical resources like CSS and JavaScript over images.

The practical difference is significant: pipelining provided marginal benefits due to head-of-line blocking and was rarely enabled by default. HTTP/2 multiplexing provides true parallelism, dramatically improving page load times for complex web pages with many resources. HTTP/2 also supports stream prioritization and server push, features pipelining lacked entirely.

## Q33: Compare ARP (Address Resolution Protocol) and NDP (Neighbor Discovery Protocol).

**A:** ARP resolves IPv4 addresses to MAC addresses on local networks. When a host needs to send a packet to an IP address on the same subnet, it broadcasts an ARP request asking "who has this IP address?" The owner responds with its MAC address, and the requester caches the mapping. ARP uses broadcast traffic and doesn't support IPv6.

NDP (Neighbor Discovery Protocol) in IPv6 replaces ARP and provides additional functionality. It uses ICMPv6 messages (neighbor solicitation and advertisement) instead of broadcasts, using multicast to reduce network noise. NDP also handles router discovery, prefix information, address autoconfiguration (SLAAC), and redirect messages, combining multiple IPv4 protocols (ARP, ICMP Router Discovery, DHCP for prefix info) into one.

NDP's multicast-based approach is more efficient than ARP's broadcast model, reducing unnecessary traffic on networks with many hosts. NDP also includes security features like Secure Neighbor Discovery (SEND) with cryptographic addresses, protecting against spoofing attacks that ARP is vulnerable to. The consolidation of multiple functions into NDP simplifies IPv6 network management.

## Q34: What is the difference between a TCP TIME_WAIT state and CLOSE_WAIT state?

**A:** TIME_WAIT occurs after a host actively closes a connection by sending a FIN and receiving the ACK. The host remains in TIME_WAIT for 2MSL (Maximum Segment Lifetime, typically 60 seconds on Linux) to ensure the final ACK reaches the remote host and to prevent delayed packets from old connections being accepted by new connections using the same port numbers.

CLOSE_WAIT occurs when a host receives a FIN from the remote host but hasn't closed its end of the connection. The remote host has indicated it's done sending, but the local application hasn't issued a close(). CLOSE_WAIT accumulates when applications don't properly close connections, indicating potential resource leaks or application bugs.

The difference is direction and responsibility: TIME_WAIT is normal after actively closing a connection and protects against stale packets. CLOSE_WAIT indicates the remote end closed but the local application hasn't, often signaling a bug where the application fails to close sockets. Excessive TIME_WAIT can be managed with socket options, while CLOSE_WAIT requires application fixes.

## Q35: Compare active and passive FTP modes.

**A:** In active FTP, the client sends a PORT command to the server specifying an IP address and port for the server to connect back to. The server establishes a separate data connection from its port 20 to the client's specified port. This requires the client to accept incoming connections, which often fails when clients are behind firewalls or NAT devices blocking unsolicited inbound connections.

Passive FTP reverses the connection direction. The client sends a PASV command, and the server responds with an IP address and port for the client to connect to. The client initiates both control and data connections to the server, which works better with firewalls and NAT because all connections originate from the client side.

Passive FTP is more common in modern environments due to firewall and NAT compatibility. However, passive FTP requires servers to open a range of ports for data connections, complicating firewall configuration. Active FTP is simpler from a server perspective but impractical for most client scenarios. FTPS (FTP over SSL) and SFTP (SSH File Transfer Protocol) have largely replaced both for secure file transfers.

## Q36: How does TCP's Nagle algorithm differ from UDP's immediate sending?

**A:** The Nagle algorithm in TCP buffers small outgoing segments, waiting until it has enough data to fill a maximum-sized segment or until an acknowledgment arrives for previous data. This reduces network overhead by eliminating many small packets that would add header overhead without significantly improving throughput. The algorithm is beneficial for interactive applications like Telnet where each keystroke would otherwise generate a separate packet.

UDP has no Nagle algorithm or equivalent buffering. Each sendto() call immediately transmits a datagram, regardless of size. This provides the lowest latency for individual messages but can flood the network with many small packets, each requiring IP and UDP headers (28+ bytes overhead per packet). Applications must manage their own buffering if they want to batch small messages.

The trade-off is latency versus efficiency. Nagle improves network efficiency for applications that can tolerate slight delays (bulk transfers, text-based protocols). UDP's immediate sending provides minimal latency for time-critical applications (gaming, VoIP) where every millisecond matters. Some TCP applications disable Nagle (TCP_NODELAY) for lower latency, accepting the overhead of small packets.

## Q37: Compare IPv6 SLAAC with IPv4 DHCP for address assignment.

**A:** SLAAC (Stateless Address Autoconfiguration) allows IPv6 hosts to generate their own addresses without a central server. The host receives router advertisements containing the network prefix and generates an interface identifier (often using EUI-64 or random values). SLAAC is truly stateless—no server tracks which addresses are in use, simplifying network management and reducing points of failure.

DHCP (Dynamic Host Configuration Protocol) in IPv4 requires a server to manage address assignments, tracking which addresses are allocated to which hosts. The server maintains a pool of available addresses and leases them to clients for specified durations. DHCP also provides additional configuration like default gateways, DNS servers, and domain names.

IPv6 also supports DHCPv6 for stateful address assignment when more control is needed, and Router Advertisements can combine with SLAAC to provide gateway and DNS information. The key difference is philosophy: SLAAC emphasizes simplicity and decentralization (good for large, simple networks), while DHCP provides centralized control and additional configuration options (good for managed enterprise environments).

## Q38: What is the difference between unicast flooding and multicast in switched networks?

**A:** Unicast flooding occurs when a switch receives a frame destined for an unknown unicast address (MAC address not in its forwarding table). The switch floods the frame to all ports except the source port, hoping the destination is reachable through one of those ports. This wastes bandwidth and can cause security issues by exposing traffic to unintended recipients.

Multicast is a deliberate one-to-many delivery mechanism where a source sends to a multicast group address, and switches and routers forward traffic only to ports with subscribed members. Managed switches support IGMP snooping to learn which ports have multicast subscribers, preventing unnecessary flooding. Multicast is efficient for group communications like video streaming or financial data feeds.

The difference is intent and efficiency: unicast flooding is an unintended consequence of unknown destinations, causing unnecessary traffic. Multicast is an intentional delivery mechanism that, with proper switch support, reaches only interested recipients. Proper network design minimizes unicast flooding through MAC address learning and static entries, while multicast requires protocol support (IGMP, PIM) throughout the infrastructure.

## Q39: Compare TCP Fast Open (TFO) with QUIC's 0-RTT connection resumption.

**A:** TCP Fast Open reduces latency by allowing data to be sent during the TCP handshake. After an initial connection, the server gives the client a cookie that enables data transmission with the SYN packet, eliminating the wait for handshake completion. TFO reduces latency by one round trip for repeat connections to the same server but still requires the initial connection for cookie exchange.

QUIC's 0-RTT allows clients to send encrypted data immediately when reconnecting to a previously visited server. The client caches cryptographic parameters from previous connections and includes them in the initial packet, enabling immediate encrypted data transmission. QUIC achieves this while maintaining full encryption, whereas TFO sends data before connection security is established.

The key difference is security and scope. TFO only saves one RTT and doesn't provide encryption for the early data (which is vulnerable to replay attacks). QUIC's 0-RTT provides encryption from the first packet and saves more latency when combined with QUIC's single-RTT new connection handshake. QUIC's approach is more comprehensive but requires the QUIC protocol stack rather than working with standard TCP.

## Q40: How does a web application firewall (WAF) differ from a network firewall?

**A:** A network firewall operates at Layers 3-4, filtering traffic based on IP addresses, ports, and protocols. It allows or blocks packets based on rules like "block port 23" or "allow traffic from subnet X." Network firewalls protect against unauthorized network access, port scanning, and protocol-level attacks but cannot inspect application-layer content.

A WAF operates at Layer 7, inspecting HTTP/HTTPS traffic for application-layer attacks. It analyzes request contents, headers, parameters, and payloads to detect SQL injection, cross-site scripting (XSS), file inclusion, and other web attacks. WAFs understand HTTP semantics and can enforce security policies specific to web applications, such as blocking requests exceeding certain sizes or containing suspicious patterns.

The key difference is inspection depth: network firewalls protect the network perimeter, while WAFs protect specific web applications. A network firewall might allow all HTTP traffic (port 80/443) to a web server, while a WAF inspects each HTTP request for malicious content. Most secure architectures use both: network firewalls for perimeter security and WAFs for application-layer protection.

## Q41: Compare connection-oriented multiplexing with message-oriented multiplexing.

**A:** Connection-oriented multiplexing, as seen in TCP, uses a single connection with multiple logical streams (as in HTTP/2) or multiple connections. TCP provides byte-stream semantics where data from different streams may interleave at the byte level. Stream multiplexing requires application-layer framing to distinguish message boundaries within the continuous byte stream.

Message-oriented multiplexing, as in SCTP or QUIC, preserves message boundaries within each stream. Each send operation corresponds to a complete message on the receiving end, regardless of other streams' activity. This simplifies application design because messages remain discrete units, avoiding the need for application-layer framing protocols.

The practical impact is on application design: TCP-based multiplexing requires careful protocol design to separate messages (length prefixes, delimiters, etc.). Message-oriented multiplexing is more natural for protocols with distinct message types (gaming commands, chat messages, RPC calls). QUIC combines message-oriented streams with reliable delivery, providing the benefits of both TCP reliability and UDP's message semantics.

## Q42: What is the difference between route aggregation and route summarization?

**A:** Route aggregation combines multiple specific routes into a single, less-specific route advertised to upstream routers. For example, aggregating 10.1.0.0/24, 10.1.1.0/24, ..., 10.1.255.0/24 into 10.1.0.0/16 reduces routing table size and update frequency. Aggregation is common at network boundaries where internal details don't need to be exposed to external networks.

Route summarization is a broader term encompassing aggregation and also includes techniques like default route substitution. Where aggregation creates a single prefix covering multiple subnets, summarization might replace specific routes with a default route pointing to a better-informed router. Both reduce routing table size and processing overhead.

The distinction is subtle: aggregation typically refers to combining adjacent prefixes into a supernet, while summarization is the general practice of reducing route table complexity. Both achieve the same goal of scalability—smaller routing tables, faster convergence, and reduced memory/CPU usage in routers. The main challenge is handling topology changes within aggregated ranges, which may require withdrawal and re-advertisement of summary routes.

## Q43: Compare HTTP/1.1 chunked transfer encoding with HTTP/2 data frames.

**A:** HTTP/1.1 chunked transfer encoding allows servers to send responses before knowing the total size. The response is divided into chunks, each prefixed with its size in bytes, followed by a zero-length chunk indicating completion. Chunked encoding enables streaming responses and reduces latency for dynamic content but adds overhead from chunk headers and requires the client to parse chunk boundaries.

HTTP/2 data frames provide more efficient framing. Each frame contains a 9-byte header with stream ID, length, and type information, followed by the payload. Multiple frames from different streams can interleave on the same connection, and frames can be prioritized. HTTP/2 also supports END_STREAM flags to indicate frame completion without requiring chunked encoding's special syntax.

The practical difference is efficiency and flexibility: HTTP/2 frames are more compact and support multiplexing natively. HTTP/1.1 chunked encoding is a workaround for the one-response-at-a-time limitation, adding overhead to achieve streaming. HTTP/2's frame-based approach is cleaner and more efficient, supporting true parallel streams without the limitations of chunked encoding's sequential nature.

## Q44: How does TCP's Selective Acknowledgment (SACK) differ from basic ACK?

**A:** Basic TCP acknowledgment (cumulative ACK) acknowledges all bytes up to a certain sequence number. If byte 1000 is ACKed, the sender assumes all bytes before 1000 were received correctly. This is simple but inefficient when multiple non-contiguous segments are lost—the sender must retransmit everything after the first loss, even if later segments arrived.

SACK (Selective Acknowledgment) allows receivers to acknowledge non-contiguous blocks of data. The receiver reports which specific segments were received out of order using SACK blocks in TCP options. The sender can then retransmit only the missing segments rather than everything after the first gap, significantly improving performance on lossy networks.

SACK is particularly valuable for high-bandwidth, high-latency connections (long fat networks) where retransmitting large amounts of already-received data wastes bandwidth and reduces throughput. SACK requires both endpoints to support it and is negotiated during the TCP handshake. Most modern TCP implementations support SACK by default.

## Q45: Compare symmetric multiprocessing (SMP) and asymmetric multiprocessing in network devices.

**A:** SMP network devices distribute processing across multiple identical processors that share memory and the operating system. All processors can handle any task, providing load balancing and fault tolerance—if one processor fails, others can take over. SMP is common in mid-range routers and switches where processing needs can vary and parallel processing improves throughput.

Asymmetric multiprocessing assigns specific processors to specific tasks. One processor might handle routing decisions, another handles management functions, and another handles packet forwarding. This specialized assignment can be more efficient for predictable workloads but creates single points of failure if a specialized processor fails.

The choice depends on requirements: SMP provides flexibility and resilience, making it suitable for general-purpose network devices that need to adapt to varying workloads. Asymmetric multiprocessing offers predictability and potentially higher efficiency for specialized tasks, used in high-end routers where different processing planes handle different functions (control plane vs. data plane).

## Q46: What is the difference between a stateful and stateless firewall?

**A:** A stateless firewall examines each packet independently, comparing it against a set of rules without considering connection context. Rules might specify "allow TCP port 80 from any source" or "block UDP port 53 from subnet X." Stateless firewalls are fast and simple but can't distinguish between legitimate return traffic and unsolicited inbound packets, potentially allowing more traffic than necessary.

A stateful firewall tracks active connections and maintains a state table mapping (source IP, source port, destination IP, destination port) tuples to connection states. It allows return traffic for established connections automatically while blocking unsolicited inbound traffic. Stateful inspection understands TCP handshakes, can detect invalid packets, and provides more granular security than stateless rules.

Stateful firewalls are the standard for perimeter security because they provide better protection with simpler rule sets. You can allow outbound HTTP and the firewall automatically permits return traffic without explicit inbound rules. Stateless firewalls are still used in high-performance scenarios where the processing overhead of state tracking is unacceptable, or as components within larger security architectures.

## Q47: Compare HTTP Strict Transport Security (HSTS) with certificate pinning.

**A:** HSTS instructs browsers to only connect to a domain using HTTPS, preventing HTTP downgrade attacks. Once a browser receives the HSTS header, it automatically redirects HTTP requests to HTTPS and rejects certificate warnings (within the max-age period). HSTS protects all subdomains when includeSubDomains is specified and can be preloaded into browsers for immediate protection.

Certificate pinning restricts connections to specific certificates or public keys, rejecting any other valid certificates. This protects against compromised CAs issuing fraudulent certificates. However, pinning creates operational complexity—if the pinned certificate expires or changes unexpectedly, the application breaks until pins are updated.

HSTS is domain-focused and protects against protocol downgrade, while certificate pinning is certificate-focused and protects against CA compromise. HSTS is simpler to implement and maintain, while pinning provides stronger but riskier protection. Many security experts recommend HSTS with preloading over certificate pinning due to pinning's operational risks and the improving CA ecosystem.

## Q48: How does TCP's Keep-Alive mechanism differ from HTTP's persistent connections?

**A:** TCP Keep-Alive sends periodic probe packets on idle connections to detect if the remote host is still reachable. If no response is received after a configured number of probes, the connection is considered dead and closed. Keep-alive prevents stale connections from consuming resources and detects network failures that might otherwise go unnoticed for long periods.

HTTP persistent connections (keep-alive) maintain TCP connections open for multiple HTTP requests, avoiding the overhead of establishing new connections for each request. HTTP persistent connections have timeout values and maximum request counts, closing connections after inactivity or too many requests. This is an application-layer optimization for HTTP performance.

The difference is purpose and layer: TCP Keep-Alive is a transport-layer mechanism for detecting dead connections, while HTTP persistent connections are an application-layer optimization for reducing connection setup overhead. HTTP persistent connections benefit from TCP Keep-Alive to detect failed connections, but they serve different purposes—performance optimization versus failure detection.

## Q49: Compare EIGRP and OSPF for internal routing protocols.

**A:** EIGRP (Enhanced Interior Gateway Routing Protocol) is a Cisco-proprietary (now partially open) hybrid routing protocol that combines distance-vector and link-state features. It uses the Diffusing Update Algorithm (DUAL) for loop-free calculations and maintains a topology table with feasible successors for rapid failover. EIGRP is simpler to configure and uses less bandwidth for updates than OSPF.

OSPF (Open Shortest Path First) is an open-standard link-state protocol that requires each router to build a complete topology map. It uses Dijkstra's algorithm for shortest path calculation and divides networks into areas for scalability. OSPF provides faster convergence in large networks, supports VLSM, and offers more granular traffic engineering through cost manipulation.

The choice depends on requirements and vendor environment: EIGRP is simpler to deploy in Cisco-only environments with minimal configuration. OSPF is preferred in multi-vendor environments and large networks requiring advanced features like NSSA, stub areas, and external route filtering. OSPF's open standard and widespread support make it the safer choice for long-term network design.

## Q50: What is the difference between a reverse proxy and a forward proxy?

**A:** A reverse proxy sits in front of backend servers, intercepting client requests and forwarding them to appropriate servers. Clients connect to the reverse proxy thinking it's the origin server, unaware of the backend infrastructure. Reverse proxies provide load balancing, SSL termination, caching, compression, and security features like WAF capabilities. Examples include Nginx, HAProxy, and AWS ALB.

A forward proxy sits in front of clients, forwarding their requests to destination servers. Clients are configured to use the proxy, which can provide anonymity (hiding client IPs), access control (blocking certain websites), caching (storing frequently accessed content), and content filtering. Corporate networks often use forward proxies to monitor and control employee internet usage.

The direction defines the role: reverse proxies protect and optimize servers, while forward proxies control and protect clients. Reverse proxies are server-side infrastructure components, while forward proxies are client-side or network-side intermediaries. Many organizations use both: forward proxies for employee internet access and reverse proxies for their web services.

## Q51: How does TCP's three-way handshake compare to QUIC's handshake in terms of latency?

**A:** TCP's three-way handshake requires three round trips (SYN, SYN-ACK, ACK) before any application data can be sent. If TLS is layered on top, the TLS handshake adds additional round trips—two more in TLS 1.2 (four total) or one more in TLS 1.3 (three total). This latency compounds on high-RTT links and is particularly noticeable for short-lived connections like API calls or page loads.

QUIC combines the transport and cryptographic handshake into a single operation. A new QUIC connection requires only one round trip before application data flows, and resumed connections achieve zero round trips (0-RTT) by deriving encryption keys from the previous session. The entire handshake—connection establishment, key exchange, and encryption setup—happens in a single flight.

In latency-sensitive scenarios like mobile apps, real-time gaming, and web page loads over cellular networks, QUIC's reduced handshake provides a measurable performance advantage. TCP's cumulative handshake overhead becomes increasingly painful as RTT grows, making QUIC the clear choice when connection setup latency is a bottleneck.

## Q52: When would you choose OSPF over BGP for routing?

**A:** OSPF is an interior gateway protocol (IGP) designed for routing within a single administrative domain. It uses Dijkstra's algorithm on link-state advertisements, converges quickly on topology changes, and supports hierarchical design through areas. OSPF is ideal when you control the entire network and need fast convergence and predictable path selection based on link cost.

BGP is the exterior gateway protocol for routing between autonomous systems. It supports policy-based routing using path attributes like AS-PATH, LOCAL_PREF, and MED. BGP scales to the global internet's routing table (over 900,000 prefixes) and provides the flexibility needed for inter-domain traffic engineering.

Choose OSPF for enterprise networks, data center fabrics, and campus environments where you need rapid convergence and fine-grained internal path control. Choose BGP at network edges where you connect to external partners or ISPs, or in large-scale environments (like internet-scale CDNs) where policy control outweighs convergence speed. Many large networks run OSPF internally and BGP at the boundary.

## Q53: Compare MPLS and SD-WAN for enterprise WAN connectivity.

**A:** MPLS provides carrier-managed, dedicated paths between sites with strict quality of service guarantees. It operates at layer 2.5, using labels to forward traffic along predetermined paths. MPLS offers predictable latency, jitter, and throughput with carrier-backed SLAs, but requires contracts with service providers, has fixed infrastructure, and is expensive to scale.

SD-WAN overlays virtual connections across multiple transport types—broadband, LTE, MPLS—using software-defined controllers. It dynamically selects the best path per application based on real-time network conditions, provides centralized management, and reduces costs by leveraging commodity internet links. SD-WAN can prioritize business-critical traffic over best-effort internet paths.

Choose MPLS for latency-sensitive, mission-critical applications (VoIP, real-time financial trading) where guaranteed performance SLAs are non-negotiable. Choose SD-WAN for branch connectivity, cloud-first architectures, and cost optimization where applications can tolerate minor latency variations. Many enterprises deploy hybrid models: MPLS for critical inter-site traffic and SD-WAN for internet-bound and cloud application traffic.

## Q54: What is the difference between an HTTP 301 and 302 redirect from a protocol perspective?

**A:** A 301 (Moved Permanently) indicates the resource has been permanently relocated. The client is expected to update bookmarks and cached references to the new URL. Search engines transfer link equity to the new location. Browsers cache this redirect aggressively, so subsequent requests go directly to the new URL without contacting the original.

A 302 (Found) indicates a temporary redirect. The client should continue using the original URL for future requests. However, due to historical browser misbehavior—some browsers converted POST to GET on 302—the specification introduced 303 (See Other) for explicit POST-to-GET conversion and 307 (Temporary Redirect) for strict method preservation.

The protocol distinction matters: 301 changes client behavior permanently (it won't contact the original URL again), while 302 instructs the client to keep using the original. Choosing incorrectly can break caching, SEO rankings, or application state. Use 301 for permanent URL changes, 307 for temporary redirects that must preserve the HTTP method, and 302 for temporary redirects where POST-to-GET conversion is acceptable.

## Q55: How do TCP and QUIC handle connection migration differently?

**A:** TCP identifies connections by a four-tuple: source IP, source port, destination IP, destination port. When a device switches networks (Wi-Fi to cellular), this tuple changes and the TCP connection breaks entirely. The application must establish a new connection, losing all negotiated state, congestion windows, and security context.

QUIC uses a Connection ID that remains constant across network changes. When a client migrates to a new network, it continues sending packets with the same Connection ID on the new path. The server detects the migration and validates the client using address validation tokens, maintaining the connection without interruption.

This makes QUIC dramatically better for mobile and multi-homed environments. Applications using QUIC experience seamless handoffs during network transitions. TCP applications must implement custom reconnection logic, session resumption, and state recovery to handle the same scenario gracefully.

## Q56: Compare HTTP/1.1 pipelining with HTTP/2 multiplexing.

**A:** HTTP/1.1 pipelining allows the client to send multiple requests without waiting for each response, but the server must respond in the same order the requests were sent. This creates head-of-line blocking at the HTTP layer—if one response is slow, all subsequent responses are delayed. Pipelining also suffered from poor browser support and implementation bugs, leading to its de facto deprecation.

HTTP/2 multiplexing splits communication into independent streams, each with its own sequence of frames. Requests and responses are interleaved at the frame level, so a slow response on one stream does not block others. Each stream has independent flow control, and the binary framing layer enables efficient interleaving.

The practical difference is dramatic. HTTP/2 eliminates HTTP-layer head-of-line blocking entirely. While TCP-level head-of-line blocking remains (a lost TCP segment blocks all streams), HTTP/2 provides far better connection utilization. HTTP/3 goes further by using QUIC, which provides per-stream reliability and eliminates head-of-line blocking at both layers.

## Q57: When should you use a load balancer versus a reverse proxy?

**A:** A load balancer distributes incoming traffic across multiple backend servers using algorithms like round-robin, least connections, or IP hash. Its primary purpose is horizontal scaling and high availability. Load balancers perform health checks, remove failed servers from rotation, and handle SSL termination and session persistence.

A reverse proxy sits in front of web servers and handles requests on their behalf, providing caching, compression, SSL termination, security filtering, and request routing. It serves as a single entry point and can return cached content without touching the backend.

In practice, the distinction is blurred. Modern load balancers include reverse proxy features, and reverse proxies can distribute traffic. Use a dedicated load balancer when distributing traffic across many instances for scaling and failover. Use a reverse proxy when you need to offload common web server tasks, cache static content, or hide backend architecture. Most production deployments combine both: a load balancer performing reverse proxy functions.

## Q58: How does TLS 1.3 differ from TLS 1.2 in terms of handshake and security?

**A:** TLS 1.3 reduces the handshake from two round trips (TLS 1.2) to one by combining the ClientHello with key exchange in the first message. The server responds with its certificate, encrypted extensions, and Finished message in one flight. This eliminates separate ServerKeyExchange and ClientKeyExchange messages, significantly reducing connection setup latency.

TLS 1.3 removes all legacy cryptographic algorithms: RSA key exchange, static Diffie-Hellman, CBC mode, RC4, 3DES, and MD5/SHA-1. It mandates forward secrecy for all cipher suites using ephemeral Diffie-Hellman or ECDH. Even if a server's private key is compromised, past sessions cannot be decrypted.

The protocol also encrypts more of the handshake, hiding certificate contents from passive observers. TLS 1.3 supports 0-RTT resumption for previously connected clients, trading some replay protection for immediate data transmission. These changes make TLS 1.3 both faster and more secure, and it is now the recommended version for all deployments.

## Q59: Compare stateful and stateless packet filtering firewalls.

**A:** Stateless firewalls examine each packet in isolation, matching it against rules based on source/destination IP, port, and protocol. They do not track connection state, so they cannot distinguish between an established TCP connection and a new SYN packet on the same port. This makes them fast but vulnerable to spoofed packets that match rule patterns.

Stateful firewalls maintain a state table tracking active connections—SYN, SYN-ACK, ESTABLISHED, FIN states. They verify that incoming packets belong to established connections, reject unsolicited packets, and enforce connection-oriented policies. Stateful inspection provides significantly better security at the cost of memory and processing overhead.

Choose stateless firewalls for high-throughput, simple rule enforcement at network perimeters where connection tracking overhead is unacceptable (router ACLs). Choose stateful firewalls for enterprise security where tracking connection context is essential for blocking unauthorized access and enforcing granular access policies. Modern firewalls typically combine both approaches.

## Q60: How do OSPF and IS-IS compare for large-scale network routing?

**A:** Both OSPF and IS-IS are link-state protocols using Dijkstra's algorithm, but they differ architecturally. OSPF operates directly over IP (protocol 89) with a rigid area design centered on Area 0 as the backbone. IS-IS operates at the data link layer and uses Level 1, Level 2, and Level 1-2 designations for hierarchy, providing more flexible topology options.

IS-IS has a more extensible TLV (Type-Length-Value) structure that makes adding new features straightforward. This is why IS-IS was historically preferred by large service providers for MPLS and traffic engineering extensions. OSPF's area design can create scaling challenges in very large flat topologies.

In practice, IS-IS is favored in large service provider networks due to simpler implementation, faster convergence at scale, and extensibility. OSPF is more common in enterprise networks where its tighter IP integration and wider vendor tooling support make it easier to manage. Both scale well when properly designed with appropriate hierarchy.

## Q61: What is the difference between TCP Fast Open and QUIC's 0-RTT connection resumption?

**A:** TCP Fast Open (TFO) allows data to be sent during the TCP handshake by including application data in the initial SYN packet. The server caches a TFO cookie for each client, and on subsequent connections, the client includes both cookie and data in the SYN. This reduces repeated connection costs to effectively zero round trips for data delivery.

QUIC's 0-RTT resumption works similarly but at the protocol level. When reconnecting, the client encrypts early data using keys derived from the previous session's PSK and sends it immediately with the ClientHello. No round trip is needed before application data flows.

Both suffer from replay attack vulnerabilities: 0-RTT data can be replayed by an attacker. TFO mitigates this with server-side cookies, while QUIC relies on application-level idempotency. QUIC's approach is more comprehensive because it also restores cryptographic context and connection state, whereas TFO only accelerates the TCP layer without addressing TLS handshake overhead.

## Q62: Compare DNS over UDP versus DNS over TCP.

**A:** Traditional DNS primarily uses UDP on port 53 for queries and responses. UDP's connectionless nature avoids handshake overhead, making it efficient for the small packet sizes typical of DNS queries (under 512 bytes). UDP's simplicity enables the high-volume, low-latency query pattern DNS servers handle.

DNS over TCP is required when responses exceed 512 bytes, when DNSSEC is in use (which produces larger responses), or when zone transfers occur between primary and secondary servers. TCP provides reliable delivery, ensuring large or fragmented responses arrive intact.

Modern implementations use both: UDP for standard queries, TCP as a fallback for large responses. With the rise of DNS over HTTPS (DoH) and DNS over TLS (DoT), both of which run over TCP, the balance is shifting toward TCP as encrypted DNS becomes standard. UDP remains the default for performance-sensitive, non-encrypted resolution.

## Q63: When would you pick IPsec over TLS for securing communications?

**A:** IPsec operates at the network layer (layer 3) and can encrypt all IP traffic between two endpoints without application changes. This makes it ideal for site-to-site VPNs where entire network segments need encrypted communication. IPsec's tunnel mode encapsulates entire IP packets, making it transparent to applications and operating systems.

TLS operates at the transport layer and secures specific application connections—HTTPS, SMTP over TLS, or any TCP-based protocol. TLS requires each application to implement it but provides finer-grained control over what is encrypted. It benefits from a mature ecosystem of certificates and trust chains.

Choose IPsec for network-wide encryption without modifying applications (enterprise VPNs, private cloud connectivity, IoT communication). Choose TLS for securing specific application protocols (web traffic, APIs, email). IPsec provides broader protection but is more complex to configure; TLS is more targeted but easier to manage and scale.

## Q64: How do connection-oriented and connectionless protocols differ in error recovery?

**A:** Connection-oriented protocols like TCP use acknowledgments, sequence numbers, and retransmission for error recovery. When a segment is lost, TCP detects the gap in sequence numbers, requests retransmission via duplicate ACKs or timeouts, and reorders out-of-sequence data. This guarantees a complete, ordered byte stream to the application.

Connectionless protocols like UDP provide no error recovery. If a packet is lost, corrupted, or arrives out of order, UDP delivers what it receives or drops silently. The application must implement its own reliability—application-layer ACKs, checksums, or forward error correction—if needed.

The trade-off is clear: TCP trades latency and overhead for guaranteed delivery, while UDP trades reliability for speed. File transfer, email, and web browsing require TCP's guarantees. Real-time applications like VoIP, live streaming, and gaming prefer UDP because retransmitting stale data is worse than missing it entirely.

## Q65: Compare multicast and broadcast at the network layer.

**A:** Broadcast sends packets to all devices on the local network segment (255.255.255.255 for limited broadcast). Every host must process the packet, creating unnecessary overhead when only some hosts need the data. Broadcast is confined to a single subnet by routers.

Multicast sends to a specific group of interested hosts using Class D IP addresses (224.0.0.0 through 239.255.255.255). Only hosts that have joined the multicast group receive the traffic. Routers use PIM (Protocol Independent Multicast) to forward traffic only along branches where group members exist.

Use broadcast for small networks where all hosts need every packet (ARP, DHCP discovery). Use multicast for one-to-many communication where only some hosts need the data (video conferencing, IPTV, stock tickers, database replication). Multicast is more efficient at scale but requires group management infrastructure and is more complex to deploy.

## Q66: How does TCP congestion control compare to QUIC's congestion control approach?

**A:** TCP congestion control (CUBIC, BBR) operates on a single connection's congestion window. Loss-based algorithms like CUBIC reduce the window on packet loss, while BBR models bandwidth and RTT to estimate optimal sending rates. TCP's congestion state is tied to the connection and must be relearned after connection breakdown.

QUIC implements congestion control in userspace, allowing updates without OS kernel changes. QUIC's congestion control operates per-connection like TCP, but because QUIC connections survive network migrations, congestion state is preserved across network changes. QUIC also supports more sophisticated loss detection with independent packet number spaces.

The practical advantage is that QUIC can iterate on congestion control algorithms faster—new algorithms deploy by updating the application, not the OS. QUIC benefits from connection migration, allowing congestion state to persist across network changes that would reset TCP's congestion window entirely, giving QUIC a significant advantage in mobile environments.

## Q67: What is the difference between symmetric and asymmetric encryption in network protocols?

**A:** Symmetric encryption uses the same key for encryption and decryption (AES, ChaCha20). It is fast and efficient for bulk data transfer, but requires both parties to securely share the secret key before communication. In network protocols, symmetric encryption protects the actual data payload after the initial handshake.

Asymmetric encryption uses a key pair—public and private (RSA, ECDH). It is computationally expensive but solves key distribution: anyone can encrypt with the public key, but only the private key holder can decrypt. In TLS, asymmetric encryption is used during the handshake to exchange symmetric keys and authenticate identities.

Network protocols combine both: asymmetric encryption establishes trust and exchanges keys during the handshake, while symmetric encryption protects ongoing data transfer. TLS, IPsec, and SSH all follow this hybrid approach. The asymmetry overhead is acceptable for a short handshake but prohibitive for millions of bytes exchanged during a session.

## Q68: Compare HTTP/2 server push with preloading for resource delivery.

**A:** HTTP/2 server push proactively sends resources the server predicts the client will need, without waiting for the client to request them. When sending HTML, the server can push CSS, JavaScript, or images in the same connection. The client receives these resources earlier than parsing the HTML and issuing separate requests.

Preloading uses `<link rel="preload">` to tell the client to fetch a resource early, before the parser discovers it. The client still makes the request, but the browser prioritizes it. Preloading keeps resource prioritization client-side, while server push makes the decision on the server side.

In practice, server push has been largely deprecated in browsers due to complexity and frequent misuse. Pushing unneeded resources wastes bandwidth, and servers often lack the context to predict needs accurately. Preloading is preferred because it keeps decisions client-side, works better with caching, and avoids unnecessary push overhead.

## Q69: When would you choose RDP over VNC for remote desktop access?

**A:** RDP (Remote Desktop Protocol) transmits abstract drawing commands rather than raw pixel data, making it bandwidth-efficient. It sends graphical primitives and updates that are compressed and optimized for the Windows rendering pipeline. RDP also supports clipboard sharing, drive redirection, audio forwarding, and printer redirection.

VNC uses the RFB (Remote Framebuffer) protocol, transmitting the screen as bitmap images. VNC sends pixel-level changes between frames, which is less efficient but platform-independent. VNC works on any operating system and requires minimal client software.

Choose RDP for Windows-to-Windows access where bandwidth efficiency, multimedia support, and peripheral redirection matter. Choose VNC for cross-platform environments, quick remote support, or situations where RDP licensing or client availability is a constraint. VNC is simpler to set up but delivers lower performance on high-resolution or multimedia-heavy desktops.

## Q70: How do synchronous and asynchronous I/O models affect network protocol implementation?

**A:** Synchronous I/O blocks the calling thread until the operation completes. A thread blocks on `read()` or `write()` until data arrives or is sent. This model is simple but does not scale—one thread per connection consumes significant memory and creates context-switching overhead under high concurrency.

Asynchronous I/O (epoll, kqueue, io_uring, asyncio) allows initiating I/O operations and continuing processing while waiting. The OS notifies the application when operations complete via events or callbacks. A single thread handles thousands of concurrent connections efficiently.

Modern network servers—Nginx, Node.js, Rust's Tokio—use asynchronous I/O for high concurrency. QUIC's userspace implementation is inherently asynchronous, managing multiple streams and connections concurrently. TCP servers using synchronous I/O require thread-per-connection models that limit scalability. The shift to async I/O has fundamentally changed high-performance networked software design.

## Q71: Compare static and dynamic NAT for outbound connectivity.

**A:** Static NAT creates a one-to-one mapping between a private IP and a public IP. The mapping is permanent—traffic destined for a specific public IP always translates to the same private IP. Static NAT is useful when external hosts need to initiate connections to internal servers (web servers, email servers behind firewalls).

Dynamic NAT maps private IPs to a pool of public IPs on a first-come, first-served basis. When an internal host sends traffic, it is assigned an available public IP from the pool. When the mapping expires, the public IP returns to the pool. Dynamic NAT provides outbound connectivity without permanently reserving public IPs.

Choose static NAT for consistent, predictable public addresses for inbound services. Choose dynamic NAT for internet access to many internal hosts using a limited pool of public IPs, without requiring inbound connections. Dynamic NAT conserves public IP space but cannot support inbound-initiated connections without port forwarding.

## Q72: How do flow control and congestion control differ in TCP, and why does it matter?

**A:** Flow control prevents the sender from overwhelming the receiver. The receiver advertises a receive window (rwnd) in each ACK, indicating buffer space available. The sender limits outstanding data to this window size. Flow control is a point-to-point mechanism protecting the slower endpoint.

Congestion control prevents the sender from overwhelming the network itself. The sender maintains a congestion window (cwnd) and limits outstanding data to min(rwnd, cwnd). Algorithms like CUBIC and BBR estimate network capacity and adjust rates based on loss or bandwidth estimation.

Both operate simultaneously and independently. Flow control ensures the receiver can process incoming data; congestion control ensures the network can carry it. Neglecting flow control causes receiver buffer overflow and dropped data; neglecting congestion control causes network-wide packet loss, retransmissions, and congestion collapse—the scenario that motivated TCP's congestion control in the late 1980s.

## Q73: Compare HTTP long polling with WebSockets for real-time communication.

**A:** HTTP long polling has the client send an HTTP request that the server holds open until new data is available or a timeout occurs. The server responds, the client immediately reconnects, and the cycle repeats. Long polling works over standard HTTP, requiring no special server configuration, and degrades gracefully through proxies.

WebSockets establish a persistent, full-duplex TCP connection after an HTTP upgrade handshake. Once upgraded, both client and server send messages independently at any time. WebSockets eliminate repeated HTTP headers, connection setup, and polling cycles, providing true bidirectional communication.

Choose long polling for simplicity, broad compatibility with existing HTTP infrastructure, and infrequent updates. Choose WebSockets for low-latency, high-frequency bidirectional communication (chat, gaming, collaborative editing, live dashboards). WebSockets are more efficient but require persistent connections that complicate load balancing. Long polling is stateless between requests, making horizontal scaling simpler.

## Q74: How do TCP and UDP differ in handling broadcast and multicast traffic?

**A:** TCP is inherently unicast—it establishes a one-to-one connection using a four-tuple. TCP cannot broadcast or multicast because its connection state, sequence numbers, and reliability mechanisms are designed for a single peer. Sending TCP data to a broadcast or multicast address violates TCP's design and is unsupported.

UDP naturally supports broadcast and multicast because it is connectionless and stateless. A UDP datagram can be addressed to a broadcast address (all hosts on the subnet) or a multicast group (all hosts that joined the group). The OS handles delivery without per-peer state. Applications like DHCP use UDP broadcast; video streaming uses UDP multicast.

This fundamental difference means reliable, ordered communication with multiple recipients must be implemented at the application layer on top of UDP, or use multiple TCP connections. Multicast file transfer, group video conferencing, and distributed systems protocols use UDP because TCP's point-to-point model is incompatible with one-to-many delivery.

## Q75: Compare TCP CUBIC and BBR for wide-area network performance.

**A:** CUBIC is a loss-based algorithm that uses a cubic function to compute congestion window growth after loss. It aggressively probes for bandwidth by increasing the window rapidly, then backing off on loss. CUBIC performs well where packet loss reliably signals congestion and is the default in Linux and Windows.

BBR (Bottleneck Bandwidth and Round-trip propagation time) models the network path by measuring bottleneck bandwidth and minimum RTT. Instead of reacting to loss, BBR estimates the optimal operating point without excessive buffering. This makes BBR significantly better on paths with random loss (wireless, satellite) or bufferbloat, where loss-based algorithms throttle unnecessarily.

Choose CUBIC for stable wired networks with low random loss, where aggressive probing efficiently fills available bandwidth. Choose BBR for wide-area, lossy, or bufferbloat-prone paths where loss is unreliable. BBR reduces latency by avoiding buffer bloat and maintains higher throughput on lossy links. BBR v2 addresses fairness concerns and is increasingly deployed at scale.

## Q76: When would you choose TLS over DTLS for securing UDP communications?

**A:** TLS is designed for TCP and requires a reliable, ordered byte stream. Its record layer assumes in-order delivery and uses TCP's stream abstraction for fragmentation and reassembly. TLS cannot run directly over UDP because UDP provides no ordering or reliability guarantees that TLS depends on for handshakes and record processing.

DTLS (Datagram TLS) is specifically designed for UDP. It adds its own reliability layer for the handshake using retransmission timers, uses explicit sequence numbers in each record to handle reordering, and processes individual datagrams rather than a continuous byte stream. Each datagram can be independently encrypted and authenticated.

Choose TLS for TCP-based protocols (HTTPS, SMTP, SSH) where the reliable transport underpins TLS's design assumptions. Choose DTLS for UDP-based protocols (SRTP for VoIP, WebRTC, CoAP for IoT) where you need encryption without the latency and overhead of TCP. DTLS 1.3 brings TLS 1.3's security improvements to datagram transports.

## Q77: Compare HTTP/1.1 chunked transfer encoding with HTTP/2 framing.

**A:** HTTP/1.1 chunked transfer encoding lets the server send response data in chunks without knowing the total size upfront. Each chunk is prefixed with its size in hex, and the response ends with a zero-length chunk. This enables streaming responses but operates within a single TCP connection where responses are sent sequentially.

HTTP/2 replaces chunked encoding with binary framing. Each HTTP message is split into frames, each tagged with a stream identifier and length. Multiple messages interleave on the same TCP connection, and each frame is independent in type and length.

The key differences: HTTP/2 framing eliminates HTTP/1.1's sequential model, supports multiplexed streams, and provides built-in header compression (HPACK). HTTP/2 also adds server push. HTTP/1.1 chunked encoding handles one response at a time per connection; HTTP/2 framing supports concurrent streams, making it more efficient and eliminating the workarounds HTTP/1.1 required.

## Q78: How do anycast and unicast addressing compare for DNS and CDN architectures?

**A:** Unicast assigns a unique IP address to a single interface. When a client sends traffic to a unicast address, the packet reaches exactly one server. DNS traditionally uses unicast—the client queries a specific server IP and gets a response from that single server. Unicast is predictable and easy to troubleshoot.

Anycast assigns the same IP address to multiple geographically distributed servers. BGP routes each client's request to the nearest or best-path instance. When a client queries an anycast DNS address, BGP naturally routes it to the closest data center. The same IP resolves to different physical servers depending on the client's location.

Choose unicast for deterministic routing to a specific server (authoritative DNS, application-specific endpoints). Choose anycast for distributed services where geographic proximity and redundancy matter (root DNS servers, CDN edge nodes, DDoS mitigation). Anycast provides automatic load distribution and failover through BGP, but troubleshooting is harder because the same IP maps to different servers.

## Q79: Compare SYN cookies with SYN proxies for SYN flood mitigation.

**A:** SYN cookies encode connection state in the initial SYN-ACK sequence number itself. Instead of storing half-open connection state in a table, the server encodes a cryptographic hash of the client's IP, port, and timestamp into the sequence number. When the ACK returns, the server verifies the hash and reconstructs state. SYN cookies require no memory per connection and scale to massive floods.

SYN proxies act as intermediaries that complete the TCP handshake with the client, then establish a separate connection with the server. The proxy absorbs SYN floods by holding connection state and forwarding only validated connections to the server. This protects the server but consumes proxy resources.

Choose SYN cookies for kernel-level protection with zero memory overhead per half-open connection—the standard Linux defense. Choose SYN proxies when an intermediate device must absorb and filter traffic before it reaches the server, often as part of a DDoS mitigation appliance. SYN proxies can inspect more deeply but add a hop and complexity. Most systems use SYN cookies as the primary defense with upstream scrubbing for volumetric attacks.

## Q80: How does TCP Fast Retransmit differ from QUIC's loss detection mechanism?

**A:** TCP Fast Retransmit triggers retransmission after three duplicate ACKs, indicating a segment was likely lost without waiting for the full retransmission timeout (RTO). This reduces recovery time to roughly one to two RTTs. However, TCP maintains a single loss detection timer for the entire connection, so one lost segment can delay others.

QUIC implements per-packet acknowledgment with independent number spaces (handshake, 0-RTT, application data). Loss is detected using time thresholds rather than duplicate ACK counts, providing more precise detection. Lost packets are identified exactly, and each stream recovers independently.

QUIC's approach enables faster, more accurate loss recovery without head-of-line blocking. Time-based detection catches loss earlier than duplicate-ACK waiting. Because QUIC runs in userspace, loss detection algorithms can be updated without OS changes, enabling rapid iteration on recovery mechanisms.

## Q81: When would you choose a VPN over an MPLS circuit for site-to-site connectivity?

**A:** A site-to-site VPN creates encrypted tunnels over the public internet between sites. It is cost-effective—no dedicated circuits or carrier contracts—and can be deployed rapidly on existing internet connections. VPNs scale easily; adding a site is a configuration change. They suit organizations with many small branches or remote offices.

MPLS provides carrier-managed private paths with guaranteed bandwidth, low latency, and strict SLAs. Traffic is isolated from the public internet, and QoS is enforced end-to-end by the carrier. MPLS is more expensive but delivers predictable performance for real-time applications.

Choose VPN for cost-sensitive deployments, rapidly expanding networks, and traffic tolerating latency variation (file sharing, email, general internet). Choose MPLS for latency-sensitive, high-availability requirements (VoIP, video conferencing, real-time transactions). Many enterprises deploy hybrid: MPLS for critical headquarters-to-major-site traffic, VPN for branches and cloud connectivity.

## Q82: Compare HTTP Digest authentication with HTTP Bearer token authentication.

**A:** HTTP Digest authentication (RFC 7616) uses a challenge-response mechanism. The server challenges with a nonce, and the client responds with a hash of the password, nonce, and other parameters. The password never crosses the wire in plaintext. But Digest does not provide mutual authentication and is vulnerable to offline dictionary attacks with weak passwords.

Bearer token authentication presents a token (typically JWT) with each request representing identity and permissions. Tokens do not protect themselves in transit—they require HTTPS. Tokens are short-lived, and the server validates them against a signing key or store without holding the user's password.

Choose Digest for password-based auth without TLS where plaintext transmission is unacceptable. Choose Bearer tokens for modern APIs where token auth integrates with OAuth 2.0, supports scopes, enables stateless validation, and avoids storing passwords. Bearer tokens are the industry standard for API authentication.

## Q83: How do connection pooling and connection multiplexing differ in HTTP clients?

**A:** Connection pooling maintains a cache of reusable TCP connections to a server. When a new request arrives, the client reuses an idle pooled connection instead of opening a new one. This avoids TCP handshake and TLS negotiation overhead for repeated requests. Each request still uses a dedicated connection from the pool.

Connection multiplexing (HTTP/2) sends multiple concurrent requests over a single TCP connection. Requests and responses interleave using the protocol's framing layer, so one connection handles the full workload. This eliminates both handshake overhead and the overhead of maintaining multiple concurrent connections.

Pooling is the performance optimization for HTTP/1.1, where a single request occupies a connection. Multiplexing is the HTTP/2 optimization that reduces the need for pooling—with truly concurrent streams, pooling returns diminish. Pooling still matters for distributing load across backends and in environments where multiplexing is unavailable.

## Q84: Compare TCP window scaling with TCP window sizing for high-bandwidth networks.

**A:** TCP window scaling (RFC 7323) extends the receive window field from 16 bits to 30 bits using a shift count negotiated in the handshake. Without it, the maximum window is 64 KB, which severely limits throughput on high-bandwidth, high-latency links. Scaling enables windows up to 1 GB, allowing TCP to fill large pipes.

Window sizing refers to the OS's configured TCP buffer sizes, tunable by administrators. Even with scaling enabled, the actual window is bounded by allocated buffers. On a 10 Gbps link with 100ms RTT, the bandwidth-delay product is 125 MB—far exceeding default buffers.

Window scaling provides the protocol mechanism for large windows; proper sizing ensures the system allocates sufficient buffers. Both are necessary. Without scaling, no buffer tuning helps because the protocol cannot advertise windows above 64 KB. Without sizing, the extension is unused and bandwidth is wasted. Modern OSes auto-tune buffers dynamically based on observed conditions.

## Q85: When would you choose HTTP/1.0 over HTTP/1.1?

**A:** HTTP/1.0 establishes a new TCP connection for each request-response pair. There is no persistent connection, no chunked transfer encoding, and no required Host header. Each request opens a connection, transfers data, and closes it, creating significant overhead for pages with multiple resources.

There are very few legitimate reasons to choose HTTP/1.0 today. Legacy embedded systems, very old devices, or extremely constrained environments that cannot handle persistent connections might still use it. Some low-memory devices benefit from the simplicity when concurrent request counts are very small.

In practice, HTTP/1.1 should be preferred for all but the most constrained environments. Its persistent connections, Host header (enabling virtual hosting), and chunked encoding are universally beneficial. If HTTP/1.1 is unavailable, upgrading the client or server is usually better than accepting the performance penalty. HTTP/2 is now the default for TLS connections and improves further.

## Q86: Compare OSPF areas with BGP autonomous systems for network segmentation.

**A:** OSPF areas subdivide a single autonomous system, reducing the scope of link-state advertisements and Dijkstra computation. Area 0 is the backbone; all other areas connect to it through area border routers (ABRs) that summarize routes. Areas reduce memory, CPU, and convergence time within a large OSPF domain.

BGP autonomous systems (ASes) represent independently administered routing domains with independent policies. Each AS has a unique AS number, and BGP routes between ASes based on policy attributes (AS-PATH, LOCAL_PREF, MED). ASes provide complete administrative separation—each runs its own internal protocol and makes independent routing decisions.

OSPF areas optimize a single administrative domain by limiting the blast radius of topology changes. BGP ASes provide inter-domain policy control and independence. Use OSPF areas to scale one IGP across many routers. Use BGP ASes when connecting to external networks or when departments require independent routing policies on shared infrastructure.

## Q87: How does TCP's Nagle algorithm interact with delayed acknowledgments?

**A:** The Nagle algorithm buffers small outgoing segments, sending only when a full segment can be formed or all prior data is acknowledged. This reduces network overhead from many small packets. Delayed ACKs (RFC 1122) cause the receiver to wait up to 200-500ms before ACKing, hoping to piggyback on outgoing data.

When both are active, a stall occurs. The sender buffers data waiting for an ACK (Nagle), while the receiver delays the ACK waiting for data to piggyback on (delayed ACK). The result is a 200-500ms delay on every small message—serious latency for interactive protocols like SSH, database queries, and gaming.

The standard solution is TCP_NODELAY, disabling Nagle to send small segments immediately. Interactive applications almost universally enable it. Modern stacks implement more sophisticated Nagle/delayed-ACK interactions. QUIC avoids the problem entirely because its stream design and ACK mechanisms don't exhibit the same pattern.

## Q88: Compare HTTP/2 stream priority with HTTP/3 stream priority.

**A:** HTTP/2 uses a priority tree where streams have parent streams and weights. Servers use it to allocate bandwidth across active streams, signaled via PRIORITY frames. However, implementations vary widely across servers and browsers, and the tree model proved complex to use effectively.

HTTP/3 introduces HTTP Extensible Priorities (RFC 9218). Instead of a tree, each stream carries a priority field with urgency (0-7) and an incremental boolean flag. Urgency sets ordering; incremental indicates whether the resource can be partially used (incremental=true for HTML/CSS, false for images). This replaces the tree with a flat, explicit system.

HTTP/3's model is easier to implement correctly, more predictable across implementations, and better aligned with real usage. HTTP/2's tree allowed fine-grained dependencies but was poorly understood and inconsistently implemented. HTTP/3's approach is pragmatic and has achieved better cross-implementation consistency.

## Q89: When would you choose a TCP-based protocol over a UDP-based protocol for a distributed system?

**A:** Choose TCP when the system requires reliable, ordered communication—database replication, RPC frameworks, configuration management, leader election. TCP's guarantees simplify application logic: messages arrive exactly once, in order, without application-layer retry logic. Strong consistency models depend on reliable ordered delivery.

Choose UDP when the system prioritizes low latency and tolerates loss—gossip protocols, real-time presence, metrics collection, eventually consistent systems. UDP avoids head-of-line blocking, enabling faster failure detection and state propagation. CRDTs handle loss and reordering gracefully.

The decision hinges on whether the system needs exactly-once, in-order delivery (TCP) or can tolerate at-most-once, unordered delivery with lower latency (UDP). Many systems use TCP for control plane operations (consensus, leader election) and UDP for the data plane (membership gossip, heartbeats). QUIC offers a middle ground: reliable per-stream delivery without cross-stream head-of-line blocking.

## Q90: Compare DNS caching at the recursive resolver versus at the client (stub resolver).

**A:** The recursive resolver caches DNS responses from authoritative servers for the TTL. When multiple clients query the same domain, the resolver serves from cache without repeating the full resolution chain. This reduces DNS traffic, lowers latency, and reduces load on authoritative servers.

The client (stub resolver) caches responses from the local resolver. The client cache is typically small, respects TTLs, and is often cleared on reboot. Applications (browsers, OS DNS services) maintain their own caches with independent TTL handling.

Resolver-level caching is more impactful because it serves many clients and performs the expensive recursive resolution. Client-level caching eliminates the RTT to the resolver for subsequent lookups. Aggressive TTLs at the resolver level benefit all clients behind it. Overly aggressive caching at either level causes stale-data problems during DNS updates or failovers.

## Q91: How do TCP and QUIC handle encryption differently in their protocol stacks?

**A:** TCP has no built-in encryption. Security is added as a separate TLS layer on top, creating a TCP+TLS stack. The TCP header (sequence numbers, ports, flags) remains visible to network intermediaries. Middleboxes inspect and modify TCP headers, which can interfere with protocol evolution.

QUIC integrates TLS 1.3 directly into the transport. The QUIC header is partially encrypted, hiding connection IDs and control information from intermediaries. Even the initial handshake uses encrypted fields. QUIC mandates encryption—there is no unencrypted mode.

This changes the economics of protocol deployment. TCP's visible headers let middleboxes break extensions (as happened with TCP Fast Open and ECN). QUIC's encrypted headers prevent interference, enabling faster evolution. The trade-off is operational visibility: encrypted headers make network troubleshooting harder.

## Q92: Compare HTTP/1.1 keep-alive with HTTP/2 persistent connections.

**A:** HTTP/1.1 keep-alive lets multiple requests and responses share one TCP connection sequentially. The connection remains open after a response, and subsequent requests reuse it. But HTTP/1.1 processes one request at a time per connection—pipelining was designed to fix this but rarely worked due to head-of-line blocking.

HTTP/2 persistent connections carry multiplexed streams over a single TCP connection. Multiple requests and responses are in flight simultaneously, interleaved at the frame level. The connection persists by default—no keep-alive headers needed—and is the only operating mode.

The difference is concurrency: HTTP/1.1 keep-alive is sequential, while HTTP/2 is concurrent. HTTP/1.1 workarounds opened multiple connections for parallelism, wasting handshakes and server resources. HTTP/2 provides true multiplexing, making the connection more efficient and reducing latency for resource-heavy pages.

## Q93: When would you use GRE tunneling instead of IPsec tunneling?

**A:** GRE (Generic Routing Encapsulation) encapsulates a wide variety of network layer protocols inside IP tunnels. It supports multicast, broadcast, and non-IP protocols, making it versatile for protocol transport. GRE provides no encryption or authentication—it is pure encapsulation with minimal overhead.

IPsec tunnel mode provides encryption, authentication, and integrity checking. It is designed for secure communication but natively supports only IP traffic. IPsec is heavier than GRE due to encryption processing and more complex key management.

Choose GRE when you need to tunnel non-IP protocols, run routing protocols over a tunnel (OSPF, EIGRP), or need encapsulation without encryption on trusted networks. Choose IPsec when security is required—site-to-site VPNs over untrusted networks, compliance-driven encryption. In practice the two are combined: GRE provides encapsulation and multicast support; IPsec encrypts the GRE tunnel, giving both flexibility and security.

## Q94: Compare horizontal and vertical scaling in the context of network protocol design.

**A:** Vertical scaling adds resources—CPU, memory, bandwidth—to a single server. Protocols affect this: HTTP/1.1 with long-lived connections benefits because each connection consumes server state; bigger buffers and more connections fit the tallest machines. Vertical scaling has hard limits and single-point-of-failure risks.

Horizontal scaling distributes load across many servers. Protocols designed for it must support stateless request handling (HTTP), load distribution (DNS round-robin, anycast), and connection distribution. HTTP/2 multiplexing complicates horizontal scaling because load balancers must maintain session affinity or handle connection state.

Protocol choices shape scaling. UDP's statelessness makes horizontal scaling trivial. TCP's connection state requires load balancers to use sticky sessions or consistent hashing. QUIC's connection migration improves horizontal scaling by allowing clients to reconnect to different servers without dropping application state. The protocol directly influences how well a system scales in either dimension.

## Q95: How do link-state and distance-vector routing protocols differ in convergence behavior?

**A:** Link-state protocols (OSPF, IS-IS) give every router a complete topology map. On a link failure, routers flood link-state advertisements and each independently runs Dijkstra's algorithm. Convergence is fast and simultaneous because every router computes new paths from full topology without iterative exchange.

Distance-vector protocols (RIP, EIGRP) share routing tables with directly connected neighbors, propagating summaries hop by hop. Convergence is slower because each router learns of a failure only when a neighbor's updated table arrives, potentially creating counting-to-infinity.

Link-state convergence is faster and more predictable—all routers converge together after the flood. Distance-vector is slower but simpler to implement and troubleshoot. EIGRP (advanced distance-vector) mitigates slow convergence with feasible-successor calculations, approaching link-state speeds without full-topology flooding. Choose link-state for larger networks needing fast convergence; distance-vector for small, simple topologies.

## Q96: Compare HTTP content negotiation with gRPC service discovery.

**A:** HTTP content negotiation uses headers (Accept, Content-Type, Accept-Language) to select the resource representation. The client declares supported formats, and the server responds with the best match. This is resource-oriented—the same URL serves different representations based on client capabilities.

gRPC uses Protocol Buffers for definitions and HTTP/2 for transport. Service discovery maps service names to endpoints, typically via a registry (Consul, etcd, Kubernetes DNS). Clients look up available servers and connect by service name with load balancing at the connection level.

Content negotiation optimizes heterogeneous clients accessing the same resource in different formats—ideal for RESTful APIs. gRPC discovery optimizes microservices where clients must find servers, balance load, and handle topology changes. REST uses HTTP semantics for negotiation; gRPC uses registry-based discovery for dynamic, polyglot service ecosystems.

## Q97: When would you pick TLS 1.3 over IPsec for protecting a network service?

**A:** TLS 1.3 protects a specific application connection end to end. It integrates cleanly with HTTP, databases, and APIs, and certificate-based trust is well understood. TLS 1.3 offers forward secrecy for all cipher suites, 0-RTT resumption, and is frequently deployed at edges (CDN, load balancers) without network-layer changes.

IPsec protects the entire network path between two gateways. It works below applications, securing all traffic regardless of protocol or application behavior. IPsec is natural for site-to-site tunnels between offices or cloud VPC connections.

Pick TLS when you protect a specific service or protocol, need per-application controls, or operate in a multi-tenant environment where IPsec would tunnel unrelated users unnecessarily. Pick IPsec when you must secure whole networks, non-HTTP protocols, or traffic that cannot be individually instrumented. Enterprises commonly use IPsec between sites and TLS for application-facing services.

## Q98: Compare TCP flow control to application-layer backpressure in message brokers.

**A:** TCP flow control limits sender data to the receiver's advertised window (rwnd), protecting the receiver's kernel buffers. It is automatic at the transport level but knows nothing about application processing capacity—the kernel buffers can fill while the application is slow.

Application-layer backpressure (in message brokers like Kafka, RabbitMQ) is explicit: producers pause consuming when consumers fall behind. It propagates load conditions through the system—consumer lag, queue depth, or credit-based flow control—and prevents unbounded buffering at the application layer.

TCP flow control happens at the byte level per connection, invisible to the application; broker backpressure is semantic, reflecting application capacity. Both prevent overload, but application-level signals are far more useful for distributed systems, where consumers have finite processing capacity independent of transport windows.

## Q99: Compare per-connection encryption (TLS) with network-layer encryption (IPsec) for zero-trust architectures.

**A:** TLS encrypts each application connection individually, which is well suited to zero-trust: every flow is authenticated and authorized, lateral movement is restricted, and per-connection policy applies. Certificates and mTLS provide strong identity per service.

IPsec encrypts whole network segments or tunnels, creating encrypted channels between explicit network boundaries. It is easier to deploy wholesale but can provide a false sense of perimeter separation, since anything inside the tunnel is shared infrastructure.

Zero-trust favors TLS/mTLS: identity is per service, authorization per request, and the security model matches the microservice topology. IPsec remains valuable for gateway-to-gateway segments or legacy workloads that cannot implement per-connection TLS, bridging the gap while zero-trust adoption proceeds.

## Q100: Compare single-path (TCP/UDP) with multi-path (MPTCP/MPQUIC) transport for mobile networks.

**A:** Single-path transports (TCP, UDP) bind a flow to one network path—be it Wi-Fi or cellular. When the path changes, the connection breaks (TCP) or must re-adapt; the flow cannot use both interfaces simultaneously to aggregate bandwidth.

MPTCP (Multipath TCP) and MPQUIC use multiple subflows over distinct networks, aggregating bandwidth and providing seamless failover. A mobile client can use Wi-Fi and cellular together, transferring in-flight data across paths on handover and surviving individual path failures.

Multi-path transports dramatically improve mobile experience: higher aggregate throughput and uninterrupted connections across interface changes. MPQUIC extends QUIC's connection migration with multiple paths and independent stream handling. The trade-off is complexity—path management, scheduling, and reordering—but for bandwidth-hungry, mobile-first applications the reliability and aggregation benefits are compelling.
