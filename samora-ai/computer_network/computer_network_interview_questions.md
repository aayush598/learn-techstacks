# Computer Networks Interview Questions (Top 100)

## 1. What is a computer network?
A computer network is a set of interconnected devices that communicate and share resources using protocols.

## 2. What is a protocol?
A protocol is a set of rules governing communication between devices (for example, TCP, IP, HTTP).

## 3. What is the OSI model?
A conceptual 7-layer model for network communication: Physical, Data Link, Network, Transport, Session, Presentation, Application.

## 4. List the 7 OSI layers.
Physical, Data Link, Network, Transport, Session, Presentation, Application.

## 5. What is the TCP slash IP model?
A 4-layer practical model: Network Interface, Internet, Transport, Application.

## 6. Compare OSI and TCP slash IP.
OSI is theoretical with 7 layers; TCP slash IP is practical with 4 layers and is the basis of the internet.

## 7. What is the Physical layer?
Transmits raw bits over a medium; deals with voltage, cables, and hardware interfaces.

## 8. What is the Data Link layer?
Provides node-to-node delivery, framing, error detection, and MAC addressing.

## 9. What is the Network layer?
Routes packets across networks using logical (IP) addresses.

## 10. What is the Transport layer?
Provides reliable or unreliable end-to-end delivery (TCP, UDP) with segmentation and flow control.

## 11. What is the Session layer?
Manages sessions or connections between applications.

## 12. What is the Presentation layer?
Handles data translation, encryption, and compression.

## 13. What is the Application layer?
Provides network services to user applications (HTTP, FTP, SMTP, DNS).

## 14. What is an IP address?
A unique logical identifier assigned to a device on a network (IPv4 or IPv6).

## 15. Difference between IPv4 and IPv6.
IPv4 is 32-bit (dotted decimal); IPv6 is 128-bit (hexadecimal) with larger address space.

## 16. What is a MAC address?
A 48-bit hardware address burned into a NIC, used for local network identification.

## 17. Difference between MAC and IP address.
MAC is physical or hardware layer (local), IP is logical or network layer (global routing).

## 18. What is a subnet mask?
A subnet mask divides an IP address into network and host portions.

## 19. What is subnetting?
Subnetting divides a network into smaller sub-networks to improve efficiency and security.

## 20. What is CIDR?
Classless Inter-Domain Routing uses prefix notation (for example, /24) to allocate IP addresses flexibly.

## 21. What is a default gateway?
The router interface that connects a local network to other networks or internet.

## 22. What is DNS?
Domain Name System translates domain names into IP addresses.

## 23. How does DNS work?
A resolver queries recursive, root, TLD, and authoritative servers to resolve a name to an IP.

## 24. What is DHCP?
Dynamic Host Configuration Protocol automatically assigns IP addresses to devices.

## 25. What is TCP?
Transmission Control Protocol is connection-oriented, reliable, ordered, and error-checked.

## 26. What is UDP?
User Datagram Protocol is connectionless, fast, and unreliable (no guarantee of delivery).

## 27. Difference between TCP and UDP.
TCP is reliable, ordered, slower; UDP is fast, connectionless, no delivery guarantee.

## 28. What is a port number?
A 16-bit number identifying a specific process or service on a host (for example, 80 for HTTP).

## 29. Name common port numbers.
HTTP 80, HTTPS 443, FTP 21, SSH 22, SMTP 25, DNS 53, Telnet 23.

## 30. What is a socket?
A socket is an IP address + port number combination identifying an endpoint of communication.

## 31. What is the three-way handshake?
TCP connection setup: SYN, SYN-ACK, ACK between client and server.

## 32. What is a four-way handshake?
TCP connection termination: FIN, ACK, FIN, ACK.

## 33. What is flow control?
Mechanisms (for example, sliding window) preventing a sender from overwhelming a slower receiver.

## 34. What is congestion control?
Techniques (for example, slow start) to prevent network overload in TCP.

## 35. What is sliding window protocol?
A flow control method allowing multiple packets before an acknowledgment.

## 36. What is a checksum?
An error-detection value computed over data to detect corruption in transit.

## 37. What is a router?
A device that forwards packets between networks based on IP addresses.

## 38. What is a switch?
A device operating at Data Link layer that forwards frames based on MAC addresses.

## 39. What is a hub?
A basic device that broadcasts incoming data to all ports (Physical layer).

## 40. Difference between router and switch.
Router connects different networks (Layer 3); switch connects devices within a network (Layer 2).

## 41. What is a gateway?
A device that translates between different protocols or networks.

## 42. What is ARP?
Address Resolution Protocol maps an IP address to a MAC address on a local network.

## 43. What is NAT?
Network Address Translation maps private IPs to a public IP for internet access.

## 44. What is the difference between public and private IP?
Public IPs are globally routable; private IPs are for internal networks (RFC 1918).

## 45. What is HTTP?
HyperText Transfer Protocol is an application-layer protocol for transferring web resources.

## 46. What is HTTPS?
HTTP Secure uses TLS slash SSL encryption to protect data in transit.

## 47. What are HTTP methods?
GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS.

## 48. What is the difference between GET and POST?
GET appends data to URL and is cacheable; POST sends data in body and is not cached.

## 49. What is an HTTP status code?
A 3-digit code indicating the result of an HTTP request (for example, 200, 404, 500).

## 50. Common HTTP status codes.
200 OK, 201 Created, 301 Moved, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Error.

## 51. What is a cookie?
A small piece of data stored by the browser and sent to the server with requests.

## 52. What is a session?
A server-side storage of user state across multiple requests.

## 53. What is FTP?
File Transfer Protocol transfers files between client and server.

## 54. What is SMTP?
Simple Mail Transfer Protocol sends and routes emails.

## 55. What is POP3 and IMAP?
Email retrieval protocols; POP3 downloads and deletes, IMAP syncs and keeps messages on server.

## 56. What is TTL?
Time To Live is a packet field limiting the number of hops to prevent infinite looping.

## 57. What is ping?
A utility using ICMP to test reachability and measure round-trip time to a host.

## 58. What is ICMP?
Internet Control Message Protocol reports errors and diagnostic info (used by ping or traceroute).

## 59. What is traceroute?
A tool showing the path packets take to a destination, listing each hop.

## 60. What is a firewall?
A security device that monitors and filters incoming or outgoing traffic based on rules.

## 61. What is a proxy server?
An intermediary that forwards requests, providing anonymity, caching, or filtering.

## 62. What is VPN?
Virtual Private Network creates an encrypted tunnel over a public network.

## 63. What is encryption in networking?
Encoding data so only authorized parties can read it (for example, TLS, IPsec).

## 64. What is SSL slash TLS?
Security protocols that provide encrypted communication over a network.

## 65. What is a digital certificate?
An electronic document verifying ownership of a public key, issued by a CA.

## 66. What is a man-in-the-middle attack?
An attacker intercepts communication between two parties to eavesdrop or alter data.

## 67. What is DoS and DDoS?
Denial of Service overwhelms a target; Distributed DoS uses many sources.

## 68. What is bandwidth?
The maximum data transfer rate of a network link, measured in bits per second.

## 69. What is throughput?
Actual rate of successful data delivery over a network.

## 70. What is latency?
The time delay for a packet to travel from source to destination.

## 71. What is jitter?
Variation in packet arrival time, important for real-time traffic like VoIP.

## 72. What is a packet?
A unit of data routed over a network, containing header and payload.

## 73. What is a frame?
A Data Link layer unit encapsulating a packet with MAC addressing.

## 74. What is a segment?
A Transport layer unit (TCP) containing data and port information.

## 75. What is multiplexing?
Combining multiple signals or data streams into one channel.

## 76. What is demultiplexing?
Separating a combined signal back into original streams at the receiver.

## 77. What are the types of multiplexing?
TDM (time division), FDM (frequency division), WDM (wavelength), statistical.

## 78. What is circuit switching?
A dedicated path is established for the entire communication (for example, traditional telephone).

## 79. What is packet switching?
Data is broken into packets routed independently across the network (internet basis).

## 80. Difference between circuit and packet switching.
Circuit switching reserves resources; packet switching shares resources dynamically.

## 81. What is unicast, broadcast, multicast?
Unicast is one-to-one, broadcast one-to-all, multicast one-to-many (specific group).

## 82. What is Ethernet?
A widely used LAN technology operating at Data Link and Physical layers.

## 83. What is the difference between LAN, MAN, WAN?
LAN is local (office), MAN is metropolitan (city), WAN is wide (internet-scale).

## 84. What is a topology?
The physical or logical arrangement of a network (bus, star, ring, mesh, hybrid).

## 85. What is CSMA slash CD?
Carrier Sense Multiple Access with Collision Detection used in Ethernet to manage collisions.

## 86. What is CSMA slash CA?
Collision Avoidance variant used in wireless networks (Wi-Fi).

## 87. What is Wi-Fi?
Wireless networking based on IEEE 802.11 standards.

## 88. What is Bluetooth?
Short-range wireless communication standard (IEEE 802.15.1).

## 89. What is the difference between TCP and UDP in video streaming?
UDP is preferred for live streaming due to low latency; TCP for reliable file transfer.

## 90. What is QoS?
Quality of Service prioritizes certain traffic to meet performance requirements.

## 91. What is a VLAN?
Virtual LAN logically segments a network regardless of physical layout.

## 92. What is STP (Spanning Tree Protocol)?
Prevents loops in bridged or switched networks by disabling redundant paths.

## 93. What is OSPF?
Open Shortest Path First, a link-state interior routing protocol.

## 94. What is BGP?
Border Gateway Protocol routes between autonomous systems on the internet.

## 95. What is RIP?
Routing Information Protocol, a distance-vector interior routing protocol.

## 96. What is a routing table?
A table stored in a router listing paths to network destinations.

## 97. What is the difference between static and dynamic routing?
Static is manually configured; dynamic uses protocols to adapt automatically.

## 98. What is network address translation types?
Static NAT, Dynamic NAT, PAT (Port Address Translation or overloading).

## 99. What is a load balancer?
Distributes network traffic across multiple servers to improve availability and performance.

## 100. What is the difference between HTTP slash 1.1 and HTTP slash 2?
HTTP slash 2 supports multiplexing, header compression, and server push; HTTP slash 1.1 is text-based and sequential.
