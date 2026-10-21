# Computer Networks — 100 Interview Q&A

---

## Q1: What is a computer network?
**A:** A computer network is a set of interconnected devices that communicate and share resources using protocols.

## Q2: What is a protocol?
**A:** A protocol is a set of rules governing communication between devices (for example, TCP, IP, HTTP).

## Q3: What is the OSI model?
**A:** A conceptual 7-layer model for network communication: Physical, Data Link, Network, Transport, Session, Presentation, Application.

## Q4: List the 7 OSI layers.
**A:** Physical, Data Link, Network, Transport, Session, Presentation, Application.

## Q5: What is the TCP slash IP model?
**A:** A 4-layer practical model: Network Interface, Internet, Transport, Application.

## Q6: Compare OSI and TCP slash IP.
**A:** OSI is theoretical with 7 layers; TCP slash IP is practical with 4 layers and is the basis of the internet.

## Q7: What is the Physical layer?
**A:** Transmits raw bits over a medium; deals with voltage, cables, and hardware interfaces.

## Q8: What is the Data Link layer?
**A:** Provides node-to-node delivery, framing, error detection, and MAC addressing.

## Q9: What is the Network layer?
**A:** Routes packets across networks using logical (IP) addresses.

## Q10: What is the Transport layer?
**A:** Provides reliable or unreliable end-to-end delivery (TCP, UDP) with segmentation and flow control.

## Q11: What is the Session layer?
**A:** Manages sessions or connections between applications.

## Q12: What is the Presentation layer?
**A:** Handles data translation, encryption, and compression.

## Q13: What is the Application layer?
**A:** Provides network services to user applications (HTTP, FTP, SMTP, DNS).

## Q14: What is an IP address?
**A:** A unique logical identifier assigned to a device on a network (IPv4 or IPv6).

## Q15: Difference between IPv4 and IPv6.
**A:** IPv4 is 32-bit (dotted decimal); IPv6 is 128-bit (hexadecimal) with larger address space.

## Q16: What is a MAC address?
**A:** A 48-bit hardware address burned into a NIC, used for local network identification.

## Q17: Difference between MAC and IP address.
**A:** MAC is physical or hardware layer (local), IP is logical or network layer (global routing).

## Q18: What is a subnet mask?
**A:** A subnet mask divides an IP address into network and host portions.

## Q19: What is subnetting?
**A:** Subnetting divides a network into smaller sub-networks to improve efficiency and security.

## Q20: What is CIDR?
**A:** Classless Inter-Domain Routing uses prefix notation (for example, /24) to allocate IP addresses flexibly.

## Q21: What is a default gateway?
**A:** The router interface that connects a local network to other networks or internet.

## Q22: What is DNS?
**A:** Domain Name System translates domain names into IP addresses.

## Q23: How does DNS work?
**A:** A resolver queries recursive, root, TLD, and authoritative servers to resolve a name to an IP.

## Q24: What is DHCP?
**A:** Dynamic Host Configuration Protocol automatically assigns IP addresses to devices.

## Q25: What is TCP?
**A:** Transmission Control Protocol is connection-oriented, reliable, ordered, and error-checked.

## Q26: What is UDP?
**A:** User Datagram Protocol is connectionless, fast, and unreliable (no guarantee of delivery).

## Q27: Difference between TCP and UDP.
**A:** TCP is reliable, ordered, slower; UDP is fast, connectionless, no delivery guarantee.

## Q28: What is a port number?
**A:** A 16-bit number identifying a specific process or service on a host (for example, 80 for HTTP).

## Q29: Name common port numbers.
**A:** HTTP 80, HTTPS 443, FTP 21, SSH 22, SMTP 25, DNS 53, Telnet 23.

## Q30: What is a socket?
**A:** A socket is an IP address + port number combination identifying an endpoint of communication.

## Q31: What is the three-way handshake?
**A:** TCP connection setup: SYN, SYN-ACK, ACK between client and server.

## Q32: What is a four-way handshake?
**A:** TCP connection termination: FIN, ACK, FIN, ACK.

## Q33: What is flow control?
**A:** Mechanisms (for example, sliding window) preventing a sender from overwhelming a slower receiver.

## Q34: What is congestion control?
**A:** Techniques (for example, slow start) to prevent network overload in TCP.

## Q35: What is sliding window protocol?
**A:** A flow control method allowing multiple packets before an acknowledgment.

## Q36: What is a checksum?
**A:** An error-detection value computed over data to detect corruption in transit.

## Q37: What is a router?
**A:** A device that forwards packets between networks based on IP addresses.

## Q38: What is a switch?
**A:** A device operating at Data Link layer that forwards frames based on MAC addresses.

## Q39: What is a hub?
**A:** A basic device that broadcasts incoming data to all ports (Physical layer).

## Q40: Difference between router and switch.
**A:** Router connects different networks (Layer 3); switch connects devices within a network (Layer 2).

## Q41: What is a gateway?
**A:** A device that translates between different protocols or networks.

## Q42: What is ARP?
**A:** Address Resolution Protocol maps an IP address to a MAC address on a local network.

## Q43: What is NAT?
**A:** Network Address Translation maps private IPs to a public IP for internet access.

## Q44: What is the difference between public and private IP?
**A:** Public IPs are globally routable; private IPs are for internal networks (RFC 1918).

## Q45: What is HTTP?
**A:** HyperText Transfer Protocol is an application-layer protocol for transferring web resources.

## Q46: What is HTTPS?
**A:** HTTP Secure uses TLS slash SSL encryption to protect data in transit.

## Q47: What are HTTP methods?
**A:** GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS.

## Q48: What is the difference between GET and POST?
**A:** GET appends data to URL and is cacheable; POST sends data in body and is not cached.

## Q49: What is an HTTP status code?
**A:** A 3-digit code indicating the result of an HTTP request (for example, 200, 404, 500).

## Q50: Common HTTP status codes.
**A:** 200 OK, 201 Created, 301 Moved, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Error.

## Q51: What is a cookie?
**A:** A small piece of data stored by the browser and sent to the server with requests.

## Q52: What is a session?
**A:** A server-side storage of user state across multiple requests.

## Q53: What is FTP?
**A:** File Transfer Protocol transfers files between client and server.

## Q54: What is SMTP?
**A:** Simple Mail Transfer Protocol sends and routes emails.

## Q55: What is POP3 and IMAP?
**A:** Email retrieval protocols; POP3 downloads and deletes, IMAP syncs and keeps messages on server.

## Q56: What is TTL?
**A:** Time To Live is a packet field limiting the number of hops to prevent infinite looping.

## Q57: What is ping?
**A:** A utility using ICMP to test reachability and measure round-trip time to a host.

## Q58: What is ICMP?
**A:** Internet Control Message Protocol reports errors and diagnostic info (used by ping or traceroute).

## Q59: What is traceroute?
**A:** A tool showing the path packets take to a destination, listing each hop.

## Q60: What is a firewall?
**A:** A security device that monitors and filters incoming or outgoing traffic based on rules.

## Q61: What is a proxy server?
**A:** An intermediary that forwards requests, providing anonymity, caching, or filtering.

## Q62: What is VPN?
**A:** Virtual Private Network creates an encrypted tunnel over a public network.

## Q63: What is encryption in networking?
**A:** Encoding data so only authorized parties can read it (for example, TLS, IPsec).

## Q64: What is SSL slash TLS?
**A:** Security protocols that provide encrypted communication over a network.

## Q65: What is a digital certificate?
**A:** An electronic document verifying ownership of a public key, issued by a CA.

## Q66: What is a man-in-the-middle attack?
**A:** An attacker intercepts communication between two parties to eavesdrop or alter data.

## Q67: What is DoS and DDoS?
**A:** Denial of Service overwhelms a target; Distributed DoS uses many sources.

## Q68: What is bandwidth?
**A:** The maximum data transfer rate of a network link, measured in bits per second.

## Q69: What is throughput?
**A:** Actual rate of successful data delivery over a network.

## Q70: What is latency?
**A:** The time delay for a packet to travel from source to destination.

## Q71: What is jitter?
**A:** Variation in packet arrival time, important for real-time traffic like VoIP.

## Q72: What is a packet?
**A:** A unit of data routed over a network, containing header and payload.

## Q73: What is a frame?
**A:** A Data Link layer unit encapsulating a packet with MAC addressing.

## Q74: What is a segment?
**A:** A Transport layer unit (TCP) containing data and port information.

## Q75: What is multiplexing?
**A:** Combining multiple signals or data streams into one channel.

## Q76: What is demultiplexing?
**A:** Separating a combined signal back into original streams at the receiver.

## Q77: What are the types of multiplexing?
**A:** TDM (time division), FDM (frequency division), WDM (wavelength), statistical.

## Q78: What is circuit switching?
**A:** A dedicated path is established for the entire communication (for example, traditional telephone).

## Q79: What is packet switching?
**A:** Data is broken into packets routed independently across the network (internet basis).

## Q80: Difference between circuit and packet switching.
**A:** Circuit switching reserves resources; packet switching shares resources dynamically.

## Q81: What is unicast, broadcast, multicast?
**A:** Unicast is one-to-one, broadcast one-to-all, multicast one-to-many (specific group).

## Q82: What is Ethernet?
**A:** A widely used LAN technology operating at Data Link and Physical layers.

## Q83: What is the difference between LAN, MAN, WAN?
**A:** LAN is local (office), MAN is metropolitan (city), WAN is wide (internet-scale).

## Q84: What is a topology?
**A:** The physical or logical arrangement of a network (bus, star, ring, mesh, hybrid).

## Q85: What is CSMA slash CD?
**A:** Carrier Sense Multiple Access with Collision Detection used in Ethernet to manage collisions.

## Q86: What is CSMA slash CA?
**A:** Collision Avoidance variant used in wireless networks (Wi-Fi).

## Q87: What is Wi-Fi?
**A:** Wireless networking based on IEEE 802.11 standards.

## Q88: What is Bluetooth?
**A:** Short-range wireless communication standard (IEEE 802.15.1).

## Q89: What is the difference between TCP and UDP in video streaming?
**A:** UDP is preferred for live streaming due to low latency; TCP for reliable file transfer.

## Q90: What is QoS?
**A:** Quality of Service prioritizes certain traffic to meet performance requirements.

## Q91: What is a VLAN?
**A:** Virtual LAN logically segments a network regardless of physical layout.

## Q92: What is STP (Spanning Tree Protocol)?
**A:** Prevents loops in bridged or switched networks by disabling redundant paths.

## Q93: What is OSPF?
**A:** Open Shortest Path First, a link-state interior routing protocol.

## Q94: What is BGP?
**A:** Border Gateway Protocol routes between autonomous systems on the internet.

## Q95: What is RIP?
**A:** Routing Information Protocol, a distance-vector interior routing protocol.

## Q96: What is a routing table?
**A:** A table stored in a router listing paths to network destinations.

## Q97: What is the difference between static and dynamic routing?
**A:** Static is manually configured; dynamic uses protocols to adapt automatically.

## Q98: What is network address translation types?
**A:** Static NAT, Dynamic NAT, PAT (Port Address Translation or overloading).

## Q99: What is a load balancer?
**A:** Distributes network traffic across multiple servers to improve availability and performance.

## Q100: What is the difference between HTTP slash 1.1 and HTTP slash 2?
**A:** HTTP slash 2 supports multiplexing, header compression, and server push; HTTP slash 1.1 is text-based and sequential.
