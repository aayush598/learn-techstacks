# Network Fundamentals Rapid Fire — 100 Interview Q&A

## Q1: How many layers are in the OSI model?

**A:** The OSI (Open Systems Interconnection) model defines 7 layers: Physical (Layer 1), Data Link (Layer 2), Network (Layer 3), Transport (Layer 4), Session (Layer 5), Presentation (Layer 6), and Application (Layer 7). This was standardized by ISO in 1984 as a reference framework for networking protocols.

Each layer communicates with its peer layer on the remote system through protocols, and with adjacent layers through service access points. The model enables vendor interoperability by defining clear boundaries between functions.

## Q2: What is the TCP/IP model and how many layers does it have?

**A:** The TCP/IP model is the practical networking model used on the Internet with 4 layers: Link (combines OSI Layers 1-2), Internet (Layer 3), Transport (Layer 4), and Application (combines OSI Layers 5-7). Some implementations describe 5 layers by separating Physical from Data Link.

The TCP/IP model was developed by DARPA in the 1970s and is the foundation of the Internet. Unlike OSI, it was designed around actual protocols (TCP, IP) rather than theoretical reference points.

## Q3: What is a PDU at each OSI layer?

**A:** PDU stands for Protocol Data Unit and changes name at each layer. Layer 1: Bit (raw signal). Layer 2: Frame. Layer 3: Packet (or Datagram). Layer 4: Segment (TCP) or Datagram (UDP). Layer 5-7: Data (sometimes called Message).

Understanding PDU names is critical for troubleshooting because they indicate which layer is being discussed. When someone says "frame error" they mean Layer 2; "packet loss" means Layer 3.

## Q4: What is the difference between a hub, switch, and router?

**A:** A hub operates at Layer 1 and broadcasts incoming signals to all ports—it has no intelligence about destinations. A switch operates at Layer 2, using MAC addresses to forward frames only to the intended port. A router operates at Layer 3, using IP addresses to route packets between different networks.

Switches reduce collisions by creating separate collision domains per port. Routers separate broadcast domains and provide inter-network connectivity. Modern "Layer 3 switches" combine switching and routing functions.

## Q5: What are the well-known port numbers for HTTP, HTTPS, DNS, and SSH?

**A:** HTTP uses port 80, HTTPS uses port 443, DNS uses port 53 (both TCP and UDP), and SSH uses port 22. These are IANA-assigned "well-known" ports in the range 0-1023.

Additional critical ports: FTP-data=20, FTP-control=21, Telnet=23, SMTP=25, DHCP=67/68, POP3=110, IMAP=143, RDP=3389, SNMP=161/162. Port numbers are essential for firewall rules and network troubleshooting.

## Q6: What is the three-way handshake in TCP?

**A:** TCP connection establishment uses a three-way handshake: the client sends a SYN segment, the server responds with SYN-ACK, and the client completes with an ACK. This synchronizes sequence numbers and establishes initial window sizes for both directions.

The handshake ensures both sides are ready to communicate and agree on initial parameters. Without it, segments could arrive out of order or before either side is prepared to process them.

## Q7: What does a TCP SYN flag indicate?

**A:** The SYN (Synchronize) flag is set in the first segment of the TCP three-way handshake. It indicates the sender wants to establish a connection and includes an initial sequence number for synchronizing data transmission.

SYN is also used in SYN flood attacks where an attacker sends many SYN segments without completing the handshake, exhausting server resources. SYN cookies and SYN proxies are common mitigations.

## Q8: What is the purpose of the TCP FIN flag?

**A:** The FIN (Finish) flag indicates that the sender has finished sending data and wants to close the connection gracefully. When a host sends FIN, it enters the FIN-WAIT state and will not send more data but can still receive.

TCP connection termination is a four-step process: FIN → ACK → FIN → ACK. This graceful shutdown ensures all data is delivered before the connection closes. RST is used for immediate/abnormal termination.

## Q9: What does the TCP RST flag mean?

**A:** The RST (Reset) flag indicates an abrupt connection termination. It is sent when a host receives a segment for a connection that does not exist, when a connection is refused, or when an error requires immediate termination.

RST is used to reject connections (e.g., when no service is listening on a port), terminate connections after timeouts, and as a security mechanism to kill suspicious sessions. Firewalls often inject RST to block connections.

## Q10: What is the difference between TCP and UDP?

**A:** TCP is connection-oriented, reliable, and ordered—it uses acknowledgments, retransmissions, and flow/congestion control. UDP is connectionless, unreliable, and unordered—it sends packets without confirmation. TCP overhead is higher but guarantees delivery.

UDP is used for real-time applications (VoIP, video streaming, gaming, DNS) where speed matters more than perfect reliability. TCP is used for web browsing, email, file transfer, and any application requiring guaranteed data delivery.

## Q11: What is the role of ARP?

**A:** Address Resolution Protocol (ARP) resolves IP addresses to MAC addresses on a local network. When a host needs to send a frame, it broadcasts an ARP Request asking "who has this IP?" and the owner responds with its MAC address.

ARP operates at the boundary between Layers 2 and 3. ARP poisoning/spoofing is a common attack where an attacker sends fake ARP replies to intercept traffic. Dynamic ARP Inspection (DAI) on switches mitigates this.

## Q12: What is the purpose of DHCP?

**A:** Dynamic Host Configuration Protocol (DHCP) automatically assigns IP addresses, subnet masks, default gateways, DNS servers, and other network parameters to clients. It uses a four-step process: Discover (broadcast), Offer, Request, Acknowledge (DORA).

DHCP eliminates manual IP configuration, prevents IP conflicts, and enables efficient address pool management. DHCP reservations allow specific devices to always receive the same IP address.

## Q13: What is a subnet mask?

**A:** A subnet mask divides an IP address into network and host portions. In IPv4, it's a 32-bit number where 1s represent network bits and 0s represent host bits. For example, 255.255.255.0 (/24) means the first 24 bits identify the network.

Subnetting creates smaller networks from a larger address space, reducing broadcast domains and improving security. CIDR (Classless Inter-Domain Routing) replaced classful addressing for more efficient IP allocation.

## Q14: What is the difference between unicast, broadcast, and multicast?

**A:** Unicast is one-to-one communication—one sender to one specific receiver (e.g., web browsing). Broadcast is one-to-all communication—one sender to all devices on a network (e.g., ARP request, DHCP discover). Multicast is one-to-many communication—one sender to a group of interested receivers (e.g., video streaming).

Broadcast is limited to a broadcast domain (Layer 3 boundary). Multicast uses IGMP for group membership and protocols like PIM for routing. Anycast (not part of traditional trio) is one-to-nearest—routing directs to the closest instance (used by CDNs and DNS root servers).

## Q15: What is NAT and why is it used?

**A:** Network Address Translation (NAT) maps private IP addresses to public IP addresses, allowing multiple devices to share a single public IP. NAT conserves IPv4 addresses and provides security by hiding internal network topology.

Types include: Static NAT (1:1 mapping), Dynamic NAT (pool of public IPs assigned on demand), and PAT (Port Address Translation/NAT Overload—many private IPs mapped to one public IP using port numbers). PAT is most common in home routers.

## Q16: What is the difference between static and dynamic routing?

**A:** Static routing uses manually configured routes—administrators define next-hop addresses for each destination. Dynamic routing uses protocols (OSPF, BGP, EIGRP) to automatically discover and maintain routes. Static is simpler but doesn't scale; dynamic adapts to topology changes.

Static routes are preferred for small, stable networks and default routes. Dynamic routing is essential for large enterprise and ISP networks where link failures and topology changes require automatic convergence.

## Q17: What is the difference between distance-vector and link-state routing protocols?

**A:** Distance-vector protocols (RIP, EIGRP) share routing tables with neighbors periodically and use hop count or composite metrics. They are simpler but prone to slow convergence and routing loops (counting to infinity). Link-state protocols (OSPF, IS-IS) flood link-state information to all routers and compute shortest paths independently.

Link-state protocols converge faster, scale better, and have complete topology knowledge. Distance-vector protocols are easier to configure and use less memory. EIGRP (advanced distance-vector) combines features of both.

## Q18: What is the difference between OSPF and BGP?

**A:** OSPF is an interior gateway protocol (IGP) that uses link-state information and Dijkstra's algorithm for shortest path calculation within an autonomous system. BGP is an exterior gateway protocol (EGP) that manages routing between autonomous systems using path-vector routing.

OSPF converges quickly and is ideal for internal network routing. BGP is policy-based, making routing decisions based on business relationships, path attributes, and prefixes. BGP is the protocol that holds the Internet together.

## Q19: What is a MAC address?

**A:** A Media Access Control (MAC) address is a 48-bit (6-byte) hardware address burned into every network interface card (NIC). It's written in hexadecimal (e.g., 00:1A:2B:3C:4D:5E). The first 24 bits identify the manufacturer (OUI), and the last 24 bits are device-specific.

MAC addresses operate at Layer 2 and are used within the same broadcast domain (LAN). Switches learn MAC addresses and build a CAM table to forward frames to specific ports. MAC addresses can be spoofed for attacks.

## Q20: What is the difference between a LAN and a WAN?

**A:** A Local Area Network (LAN) connects devices within a limited area (home, office, campus) using Ethernet, Wi-Fi, or similar technologies. A Wide Area Network (WAN) connects geographically dispersed LANs over long distances using leased lines, MPLS, or Internet-based VPNs.

LANs typically offer higher speeds (1 Gbps+) with lower latency. WANs have higher latency, lower throughput, and higher cost per bit. SD-WAN modernizes WAN connectivity by using software-defined networking over multiple transport types.

## Q21: What is the OSI Layer 2?

**A:** Layer 2 (Data Link) provides node-to-node data transfer between two directly connected nodes. It handles framing, error detection (CRC), flow control, and MAC addressing. Sublayers include LLC (Logical Link Control) and MAC (Media Access Control).

Protocols at Layer 2 include Ethernet (IEEE 802.3), Wi-Fi (IEEE 802.11), PPP, and Frame Relay. VLAN tagging (IEEE 802.1Q) operates at Layer 2 to logically segment networks within the same physical infrastructure.

## Q22: What is a VLAN?

**A:** A Virtual Local Area Network (VLAN) logically segments a physical network into separate broadcast domains. Devices on different VLANs cannot communicate without a Layer 3 device (router or Layer 3 switch). VLANs are configured using IEEE 802.1Q tagging.

VLANs improve security (isolate sensitive traffic), reduce broadcast domains, and provide flexibility in network design without physical rewiring. Voice VLANs separate phone traffic from data, and management VLANs isolate network management traffic.

## Q23: What is the role of the DNS?

**A:** Domain Name System (DNS) translates human-readable domain names (google.com) to IP addresses (142.250.80.46). DNS uses a hierarchical distributed database: root servers → TLD servers (.com, .org) → authoritative servers for specific domains.

DNS is critical for virtually all Internet services. Types include recursive resolvers (client-side), authoritative servers (domain-side), and caching servers. DNSSEC adds cryptographic signatures to prevent DNS spoofing.

## Q24: What is ICMP and what is ping?

**A:** Internet Control Message Protocol (ICMP) is a network layer protocol used for diagnostics and error reporting. Ping uses ICMP Echo Request/Reply to test connectivity and measure round-trip time. Traceroute uses ICMP Time Exceeded to map the path to a destination.

ICMP is also used for Path MTU Discovery (Fragmentation Needed message), redirect messages, and destination unreachable notifications. ICMP flood (Smurf attack) is a DDoS technique that amplifies ICMP traffic.

## Q25: What is the difference between IPv4 and IPv6?

**A:** IPv4 uses 32-bit addresses (4.3 billion addresses) while IPv6 uses 128-bit addresses (340 undecillion addresses). IPv6 eliminates NAT by providing sufficient addresses for every device. IPv6 also has simplified headers, built-in IPSec, and no broadcast (uses multicast and anycast instead).

IPv4 header has 12+ fields with optional headers; IPv6 has 8 fixed fields for faster processing. IPv6 uses Neighbor Discovery Protocol (NDP) replacing ARP, and SLAAC (Stateless Address Autoconfiguration) for automatic address assignment.

## Q26: What is TCP window size?

**A:** TCP window size determines how much data a sender can transmit before receiving an acknowledgment. It's advertised by the receiver in each ACK and represents the available buffer space. The sender cannot exceed the receiver's advertised window to prevent overflow.

The congestion window (cwnd) limits sending based on network conditions (slow start, congestion avoidance). The effective window is the minimum of the receiver window and congestion window. TCP window scaling (RFC 7323) allows windows larger than 64 KB.

## Q27: What is the purpose of the TCP sequence number?

**A:** Sequence numbers identify the byte position of data in the TCP stream. Each segment carries the sequence number of its first byte. This enables the receiver to reassemble data in correct order, detect missing segments, and send selective acknowledgments.

TCP sequence numbers start at a random initial value (ISN) for security—to prevent TCP hijacking and session prediction attacks. The sequence number space wraps around after 2^32 bytes (~4 GB).

## Q28: What is a TCP socket?

**A:** A TCP socket is one endpoint of a TCP connection, identified by the tuple (source IP, source port, destination IP, destination port). Sockets are the programming interface (API) applications use for network communication (Berkeley sockets API).

A single server can handle multiple simultaneous connections by creating a unique socket for each client. The listening socket accepts new connections and spawns connected sockets. The `TIME_WAIT` state prevents old segments from interfering with new connections.

## Q29: What is the difference between connection-oriented and connectionless?

**A:** Connection-oriented protocols (TCP) establish a connection before data transfer (three-way handshake), maintain state, and provide reliability. Connectionless protocols (UDP, ICMP) send data without prior connection setup—each packet is independent and routed independently.

Connection-oriented offers reliability, ordering, and flow control but with higher overhead. Connectionless offers lower latency and overhead but no delivery guarantee. Some protocols like SCTP provide connection-oriented service with multi-homing.

## Q30: What is the maximum size of an Ethernet frame?

**A:** The maximum Ethernet frame size is 1518 bytes (including 14-byte header, 4-byte FCS, and 1500-byte payload). Jumbo frames extend this to 9000 bytes for higher throughput on modern networks. The minimum frame size is 64 bytes (padding is added if necessary).

Frames smaller than 64 bytes are called runt frames and indicate collisions or errors. Frames larger than 1518 bytes (without VLAN tag) are called giants. VLAN-tagged frames can be 1522 bytes.

## Q31: What is the difference between a switch and a bridge?

**A:** Both operate at Layer 2 and use MAC addresses for forwarding. A bridge typically has 2-4 ports and connects network segments. A switch is a multi-port bridge with many ports (8-48+), performing the same function at higher performance.

Modern networks use switches exclusively—bridges are largely obsolete. Both learn MAC addresses dynamically and forward frames only to the appropriate port, reducing unnecessary broadcast traffic.

## Q32: What is the role of STP (Spanning Tree Protocol)?

**A:** STP (IEEE 802.1D) prevents Layer 2 loops in networks with redundant links. It elects a root bridge and blocks redundant paths, creating a loop-free topology. If an active link fails, STP unblocks an alternate path to restore connectivity.

RSTP (Rapid STP, 802.1w) improves convergence time from 30-50 seconds to under 6 seconds. MSTP (Multiple STP, 802.1s) maps multiple VLANs to a single spanning tree instance for better load balancing.

## Q33: What is a default gateway?

**A:** A default gateway is the router interface that connects a local network to other networks. When a host needs to send data to an IP outside its subnet, it sends the packet to the default gateway, which routes it toward the destination.

The default gateway is configured via DHCP or manually. It must be in the same subnet as the host. Without a default gateway, a host can only communicate within its local network.

## Q34: What is the difference between half-duplex and full-duplex?

**A:** Half-duplex allows data transmission in only one direction at a time (like a walkie-talkie). Full-duplex allows simultaneous bidirectional communication (like a telephone). Ethernet switched networks operate in full-duplex, eliminating collisions.

Half-duplex uses CSMA/CD (Collision Detection) to manage shared media access. Full-duplex doubles effective throughput and is standard on all modern Ethernet connections. Wireless networks are inherently half-duplex due to shared medium.

## Q35: What is a broadcast domain?

**A:** A broadcast domain is the set of all devices that will receive a broadcast frame (destination MAC FF:FF:FF:FF:FF:FF) originating from any device within the domain. Routers (Layer 3 devices) break broadcast domains—switches and hubs extend them.

Broadcast domains are limited for performance—large broadcast domains create excessive broadcast traffic that consumes bandwidth and CPU on all devices. VLANs are the primary method for segmenting broadcast domains within a Layer 2 network.

## Q36: What is the purpose of the TCP checksum?

**A:** The TCP checksum verifies the integrity of the TCP header and data. It's a 16-bit one's complement of the one's complement sum of all 16-bit words in the header and data. If the calculated checksum doesn't match the received checksum, the segment is discarded.

TCP checksums protect against bit errors introduced during transmission. Combined with link-layer CRC (which protects the Ethernet frame), TCP checksums provide end-to-end integrity verification. UDP also has a checksum, though it's optional in IPv4.

## Q37: What is an IP address class?

**A:** Classful IP addressing divided IPv4 into classes: Class A (0-127, /8), Class B (128-191, /16), Class C (192-223, /24), Class D (224-239, multicast), and Class E (240-255, experimental). Class A had 16M hosts per network, Class B had 65K, Class C had 254.

Classful addressing was replaced by CIDR (Classless Inter-Domain Routing) in 1993 for more efficient address allocation. CIDR uses variable-length subnet masks (e.g., /21, /27) instead of fixed class boundaries.

## Q38: What is the loopback address?

**A:** The loopback address is 127.0.0.1 (IPv4) or ::1 (IPv6). Packets sent to loopback never reach the network—they are processed within the local TCP/IP stack. It's used for testing, troubleshooting, and local services.

If ping to 127.0.0.1 fails, the TCP/IP stack is misconfigured. The entire 127.0.0.0/8 range is reserved for loopback in IPv4. Applications binding to localhost (127.0.0.1) are only accessible from the same machine.

## Q39: What is the difference between an IP address and a MAC address?

**A:** A MAC address is a physical hardware address (Layer 2) burned into the NIC—used for local network communication. An IP address is a logical address (Layer 3) assigned by configuration or DHCP—used for routing across networks.

MAC addresses are flat (no hierarchical structure beyond OUI), while IP addresses are hierarchical (network + host portions). MAC addresses don't change between networks; IP addresses change when a device moves to a different network.

## Q40: What is ARP table/ARP cache?

**A:** The ARP table (or ARP cache) is a temporary in-memory table mapping IP addresses to MAC addresses. When a host needs to send data, it checks the ARP cache first; if the entry is missing, it broadcasts an ARP request.

ARP entries are dynamic and expire after a timeout (typically 15-20 minutes). The command `arp -a` displays the ARP cache. ARP spoofing attacks poison this cache to redirect traffic—Dynamic ARP Inspection (DAI) on managed switches prevents this.

## Q41: What is the function of the TCP SYN-ACK?

**A:** SYN-ACK is the second step of the TCP three-way handshake. The server responds to the client's SYN with SYN-ACK, acknowledging the client's sequence number (ACK) and sending its own initial sequence number (SYN).

The SYN-ACK establishes bidirectional communication parameters—both sides now know each other's starting sequence numbers and can begin reliable data transfer after the final ACK.

## Q42: What is a port scan?

**A:** A port scan is a technique to discover open ports on a target host. Tools like Nmap send packets to various ports and analyze responses to determine which ports are open (service listening), closed (port reachable but no service), or filtered (firewall blocking).

Common scan types include SYN scan (half-open, sends SYN and analyzes response), TCP connect scan (completes three-way handshake), and UDP scan (sends UDP packets and looks for ICMP unreachable). Port scanning is a reconnaissance technique used by both administrators and attackers.

## Q43: What is the TIME_WAIT state in TCP?

**A:** TIME_WAIT occurs after a TCP connection is closed (both sides sent FIN). The socket waits for 2MSL (Maximum Segment Lifetime, typically 60 seconds) to ensure any delayed segments from the old connection are discarded before the port can be reused.

TIME_WAIT prevents old duplicate segments from being accepted as part of a new connection. Excessive TIME_WAIT can exhaust port resources on high-traffic servers. Solutions include SO_REUSEADDR socket option and load balancing across multiple IPs.

## Q44: What is slow start in TCP congestion control?

**A:** Slow start is the initial phase of TCP congestion control where the congestion window (cwnd) starts at 1 MSS and doubles every RTT (exponential growth). This quickly probes for available bandwidth without overwhelming the network.

When cwnd reaches the slow start threshold (ssthresh), TCP transitions to congestion avoidance (linear growth). Slow start also restarts after a timeout, resetting cwnd to 1 MSS. Fast recovery (RFC 5681) avoids slow start after triple duplicate ACK.

## Q45: What is the purpose of ICMP Redirect?

**A:** ICMP Redirect tells a host that a better first-hop router exists for a specific destination. When a router forwards a packet and realizes the sending host should use a different router on the same subnet, it sends an ICMP Redirect to the host.

This optimizes routing by allowing hosts to learn better paths. However, ICMP Redirect can be exploited for man-in-the-middle attacks, so it's often disabled on production networks and firewalls.

## Q46: What is the difference between TCP MSS and MTU?

**A:** MTU (Maximum Transmission Unit) is the maximum packet size at Layer 3, including the IP header (typically 1500 bytes for Ethernet). MSS (Maximum Segment Size) is the maximum data in a TCP segment, excluding TCP and IP headers—MTU minus 40 bytes (20-byte TCP + 20-byte IP headers) = 1460 bytes typically.

MSS is negotiated during the three-way handshake (TCP Options). Path MTU Discovery (PMTUD) discovers the smallest MTU along the path to avoid fragmentation. IPv6 requires a minimum MTU of 1280 bytes.

## Q47: What is the purpose of TCP Options?

**A:** TCP Options are variable-length fields in the TCP header that extend TCP functionality. Common options include: MSS (Maximum Segment Size), Window Scale (RFC 7323, for windows >64KB), SACK (Selective Acknowledgment, RFC 2018), and Timestamps (RFC 7323, for RTT measurement and PAWS).

TCP Options are negotiated during the three-way handshake—the SYN segment lists supported options, and the peer acknowledges the ones it supports. The NOP option is used for padding to align options on 32-bit boundaries.

## Q48: What is the difference between an active and passive FTP connection?

**A:** In active FTP, the client connects to the server's control port (21), and the server initiates the data connection back to the client's port (20). This requires the client to accept incoming connections, which is problematic with firewalls.

Passive FTP reverses the data connection—the client initiates both control and data connections to the server. The server tells the client which port to use for data. Passive mode is preferred for clients behind NAT/firewalls.

## Q49: What is the role of the SSL/TLS handshake?

**A:** The TLS handshake establishes a secure connection: the client sends ClientHello (supported ciphers, TLS version), the server responds with ServerHello (chosen cipher, certificate), the client verifies the certificate, key exchange occurs (ECDHE, RSA), and both derive session keys.

TLS provides confidentiality (encryption), integrity (MAC/HMAC), and authentication (digital certificates). TLS 1.3 simplified the handshake to 1-RTT (0-RTT for resumption) and removed legacy algorithms.

## Q50: What is the difference between symmetric and asymmetric encryption?

**A:** Symmetric encryption uses the same key for encryption and decryption (AES, DES, ChaCha20). It's fast but requires secure key distribution. Asymmetric encryption uses a key pair—public key for encryption, private key for decryption (RSA, ECC, Ed25519). It's slower but solves the key distribution problem.

TLS uses both: asymmetric encryption for key exchange (establishing a shared secret) and symmetric encryption for data transfer (using the derived session key). This combines the security of asymmetric with the performance of symmetric encryption.

## Q51: What is an IP subnet and CIDR notation?

**A:** CIDR notation (e.g., 192.168.1.0/24) represents an IP subnet with the prefix length indicating how many bits identify the network. A /24 subnet has 256 addresses (254 usable hosts), a /25 has 128 (126 usable), and a /30 has 4 (2 usable, for point-to-point links).

CIDR replaced classful addressing for efficient IP allocation. Supernetting aggregates multiple subnets (e.g., combining four /24s into a /22). Route summarization in routing protocols uses CIDR to reduce routing table size.

## Q52: What is the difference between TCP Flow Control and Congestion Control?

**A:** Flow Control prevents the sender from overwhelming the receiver—managed by the receiver's advertised window (rwnd). Congestion Control prevents the sender from overwhelming the network—managed by the congestion window (cwnd) using algorithms like slow start, congestion avoidance, fast retransmit, and fast recovery.

Flow control is end-to-end between sender and receiver. Congestion control responds to network conditions (packet loss, delay). The effective window is min(rwnd, cwnd). BBR (Google's congestion control) uses delay measurements instead of loss signals.

## Q53: What is IGMP (Internet Group Management Protocol)?

**A:** IGMP manages multicast group membership on local networks. Hosts send IGMP Join messages to join a multicast group and periodic IGMP Query messages from routers maintain membership. Versions: IGMPv1 (basic join), IGMPv2 (leave message), IGMPv3 (source-specific multicast).

IGMP operates at Layer 3 but only on the local link. Multicast routing protocols (PIM-SM, PIM-DM) extend multicast across routers. IGMP snooping on switches limits multicast flooding to only interested ports.

## Q54: What is the difference between TCP and UDP checksums?

**A:** TCP checksum is mandatory and covers the TCP pseudo-header (source IP, destination IP, protocol, TCP length), TCP header, and data. UDP checksum is optional in IPv4 (but recommended) and mandatory in IPv6. Both use the same 16-bit algorithm.

The pseudo-header ensures the segment reaches the correct destination IP, not just the correct port. A failed checksum causes the segment to be silently discarded—TCP retransmits, UDP simply drops the packet.

## Q55: What is the purpose of the TCP PSH flag?

**A:** The PSH (Push) flag tells the receiving TCP stack to immediately deliver data to the application layer rather than buffering it. When PSH is set, the receiver should not wait for more data before passing the segment to the receiving process.

PSH is typically set on the last segment of a write operation (e.g., when an application calls `send()` with the `MSG_PUSH` flag). In practice, most TCP implementations set PSH on every segment to ensure low-latency delivery.

## Q56: What is an ARP request and ARP reply?

**A:** An ARP Request is a broadcast frame (destination FF:FF:FF:FF:FF:FF) asking "who has IP address X.X.X.X? Tell Y.Y.Y.Y." Every device on the subnet receives it. The device with the matching IP sends an ARP Reply (unicast) containing its MAC address.

ARP requests are broadcast because the sender doesn't know the target's MAC address yet. ARP replies are unicast because the responder learned the sender's MAC from the request. Gratuitous ARP (unsolicited reply) is used for duplicate IP detection.

## Q57: What is the difference between Layer 2 and Layer 3 switches?

**A:** Layer 2 switches forward frames based on MAC addresses and support VLANs, STP, and link aggregation. Layer 3 switches add routing capabilities—they can route between VLANs and subnets using IP addresses without needing an external router.

Layer 3 switches are common in enterprise networks for inter-VLAN routing. They combine the speed of hardware-based switching with the intelligence of IP routing. Most enterprise switches are Layer 3 capable today.

## Q58: What is a multicast address range in IPv4?

**A:** Class D addresses (224.0.0.0 to 239.255.255.255) are reserved for multicast. Special ranges include: 224.0.0.0/24 (local link, e.g., 224.0.0.1 = all hosts), 224.0.1.0-238.255.255.255 (globally scoped), 239.0.0.0/8 (administratively scoped, private).

IGMP manages group membership. Source-Specific Multicast (SSM) uses (S,G) pairs. Any-Source Multicast (ASM) uses (*,G) pairs. PIM-SM and PIM-DM route multicast traffic between routers.

## Q59: What is the purpose of TCP Keep-Alive?

**A:** TCP Keep-Alive sends empty probe segments at periodic intervals to detect if the connection is still alive. If no response is received after a configured number of probes, the connection is considered dead and closed. Default interval varies by OS (typically 2 hours).

Keep-alive prevents stale connections from consuming resources and detects dead peers (e.g., crashed hosts, severed links). It's particularly important for long-lived connections like database connections, SSH sessions, and VPN tunnels.

## Q60: What is the difference between a protocol and a standard?

**A:** A protocol is a set of rules governing data exchange between devices (e.g., TCP, HTTP, OSPF). A standard is a formal specification published by a standards body (IEEE, IETF, ISO, ITU-T) that defines how a protocol or technology should be implemented.

Protocols can be proprietary (before standardization) or standardized. Standards ensure interoperability between different vendors. Examples: Ethernet (IEEE 802.3), Wi-Fi (IEEE 802.11), TCP/IP (IETF RFCs).

## Q61: What is the HTTP method GET vs POST?

**A:** GET retrieves data from a specified resource and should be idempotent—repeated identical requests return the same result without side effects. Parameters are passed in the URL query string. POST submits data to be processed, may create server-side changes, and carries data in the request body.

GET responses can be cached and bookmarked; POST responses typically cannot. GET has length limits (URL length varies by browser/server); POST has practical limits only on body size. GET should never modify server state.

## Q62: What is the role of the TCP Urgent flag?

**A:** The URG flag indicates that the segment contains urgent data. When set, the Urgent Pointer field specifies the offset from the sequence number where urgent data ends. The receiving application should prioritize processing this data.

URG is rarely used in modern applications—telnet used it for interrupt signals (Ctrl+C). Most implementations treat URG as informational. SSH and modern protocols handle out-of-band signaling differently.

## Q63: What is the difference between a protocol port and a physical port?

**A:** A protocol port (logical port) is a 16-bit number (0-65535) identifying a process or service at the transport layer (e.g., port 80 for HTTP). A physical port is a hardware interface on a device (e.g., RJ-45 Ethernet port, SFP fiber port).

Multiple logical ports can share one physical port. A server with one Ethernet port can simultaneously serve HTTP (80), HTTPS (443), SSH (22), and hundreds of other services, each on a different port.

## Q64: What is the difference between a routable and non-routable protocol?

**A:** Routable protocols (IP, IPX) can be forwarded across multiple networks by routers because they contain network-layer addresses. Non-routable protocols (NetBIOS, Broadcast-only protocols) are limited to the local broadcast domain.

To use non-routable protocols across networks, bridging or tunneling is required. NetBIOS over TCP/IP (NBT) encapsulates NetBIOS within IP to enable cross-network communication.

## Q65: What is the maximum TTL value in IPv4?

**A:** TTL (Time to Live) is an 8-bit field in the IPv4 header, so the maximum value is 255. Each router decrements TTL by 1; when it reaches 0, the packet is discarded and an ICMP Time Exceeded message is sent to the source.

TTL prevents infinite routing loops. Traceroute exploits TTL by sending packets with incrementing TTL values to discover each router along the path. Common default TTL values: 64 (Linux), 128 (Windows), 255 (some network devices).

## Q66: What is the purpose of the TCP ACK number?

**A:** The ACK number indicates the next byte the receiver expects to receive, cumulatively acknowledging all bytes up to that point. If ACK number is 1000, the receiver has successfully received bytes 0-999 and expects byte 1000 next.

Selective ACK (SACK, RFC 2018) allows receivers to acknowledge non-contiguous blocks of received data, reducing unnecessary retransmissions. SACK is negotiated during the three-way handshake via TCP Options.

## Q67: What is a network backbone?

**A:** A backbone is the high-speed central connection linking different network segments, subnets, or LANs. It carries the aggregated traffic from multiple network segments and typically uses higher bandwidth technologies (fiber optics, 10/40/100 GbE).

Backbones can be flat (single high-speed link) or hierarchical (core-distribution-access model). The three-tier model uses Core, Distribution, and Access layers; the collapsed two-tier model combines Core and Distribution.

## Q68: What is the difference between BGP and OSPF?

**A:** OSPF is an interior gateway protocol using link-state routing and cost-based metrics within an autonomous system. It converges quickly (sub-second with BFD) and uses Dijkstra's SPF algorithm. BGP is an exterior gateway protocol using path-vector routing between autonomous systems with policy-based decisions.

OSPF is for internal routing; BGP is for inter-domain routing. BGP carries path attributes (AS-PATH, LOCAL-PREF, MED) used for policy decisions. The Internet is a collection of ASes connected by BGP.

## Q69: What is a network protocol analyzer?

**A:** A protocol analyzer (packet sniffer) captures and decodes network traffic for analysis. Wireshark (GUI), tcpdump (CLI), and tshark are popular tools. They capture at the packet level, showing headers, payloads, and timing information.

Analyzers are used for troubleshooting (identifying misconfigurations, protocol errors), security analysis (detecting suspicious traffic), and performance analysis (latency measurement, throughput analysis). Promiscuous mode captures all traffic on a network segment.

## Q70: What is the OSI Layer 1?

**A:** Layer 1 (Physical) handles the transmission and reception of raw bit streams over a physical medium. It defines electrical signals, optical signaling, connector types, cable specifications, and data rates. Examples include Ethernet (Cat5/6), fiber optics, and wireless (802.11 RF).

Layer 1 specifications include voltage levels, timing of signal changes, physical data rates, maximum transmission distances, and connector pinouts. Problems at Layer 1 include cable faults, signal degradation, and electromagnetic interference.

## Q71: What is the purpose of VLSM?

**A:** Variable Length Subnet Masking (VLSM) allows different subnet masks within the same network class, enabling efficient IP address allocation. Instead of using the same mask for all subnets, VLSM assigns shorter masks to subnets needing more hosts and longer masks to point-to-point links.

VLSM reduces IP address waste. For example, a /30 subnet (4 addresses, 2 usable) for a point-to-point link instead of a /24 (256 addresses) saves 252 addresses. Route summarization aggregates VLSM subnets for efficient routing.

## Q72: What is a broadcast storm?

**A:** A broadcast storm occurs when broadcast frames circulate endlessly in a Layer 2 network, consuming all available bandwidth and overwhelming switches. This happens with loops (no STP) or misconfigurations, causing network-wide disruption.

Broadcast storms can be caused by: redundant links without STP, faulty NICs, DHCP storms, or malicious activity. Storm control on switches limits broadcast/multicast/unknown-unicast traffic per port to prevent disruption.

## Q73: What is the difference between TCP Fast Open and standard TCP?

**A:** TCP Fast Open (TFO, RFC 7413) allows data to be sent during the initial SYN packet (with a TFO cookie), reducing connection setup latency by one RTT. The server validates the cookie and processes the application data immediately.

TFO is particularly beneficial for HTTP/HTTPS where short-lived connections are common. The client receives a TFO cookie on first connection and reuses it on subsequent connections, enabling 0-RTT data transfer for repeat connections.

## Q74: What is the role of NTP?

**A:** Network Time Protocol (NTP) synchronizes clocks across network devices to a reference time source (atomic clock, GPS). NTP uses UDP port 123 and provides accuracy from milliseconds (LAN) to tens of milliseconds (WAN).

Accurate time is critical for log correlation, certificate validation, authentication protocols (Kerberos), and forensic analysis. NTP uses a hierarchical stratum system: Stratum 0 (reference clocks), Stratum 1 (servers directly connected), Stratum 2+ (clients).

## Q75: What is a network topology?

**A:** Topology describes the physical or logical arrangement of network devices. Physical topologies include bus, star, ring, mesh, and tree. Logical topologies describe how data flows regardless of physical layout (e.g., Ethernet uses logical bus, FDDI uses logical ring).

Modern networks predominantly use star (switched Ethernet) or extended star topologies. Full mesh provides maximum redundancy (n(n-1)/2 links) but is expensive. Partial mesh balances redundancy and cost.

## Q76: What is the difference between TCP Nagle algorithm and corking?

**A:** The Nagle algorithm (RFC 896) buffers small TCP segments until a full MSS can be sent or an ACK is received, reducing network overhead from tiny segments. It improves efficiency for interactive applications sending small amounts of data.

TCP corking (Linux) or write aggregation explicitly prevents small sends by buffering application writes until a threshold is reached. Unlike Nagle, corking is application-controlled and deterministic—useful for protocols that send header-then-body (like HTTP).

## Q77: What is the meaning of a /32 subnet?

**A:** A /32 subnet (255.255.255.255) represents a single host address with no host portion. It's used for host routes in routing tables (routing to a specific host) and for loopback interfaces on routers (e.g., 10.0.0.1/32 on Loopback0).

A /32 host route takes precedence over longer prefix routes in routing table lookups due to longest prefix matching. It's commonly used in OSPF router IDs and BGP next-hop specifications.

## Q78: What is the HTTP status code 404?

**A:** HTTP 404 (Not Found) indicates the server cannot find the requested resource. The URL may be incorrect, the resource may have been deleted, or the server may not have permission to reveal its existence.

404 is a client-side error (4xx family). Similar codes: 403 (Forbidden), 401 (Unauthorized), 400 (Bad Request), 405 (Method Not Allowed). Proper 404 handling is important for user experience and SEO.

## Q79: What is the TCP window scaling option?

**A:** Window scaling (RFC 7323) extends the TCP window size beyond the 16-bit field limit (65,535 bytes). The scaling factor (0-14) multiplies the advertised window, allowing windows up to ~1 GB. This is essential for high-bandwidth, high-latency links (long fat networks).

Window scaling is negotiated during the three-way handshake via TCP Options. Without it, throughput is limited by bandwidth-delay product. For a 1 Gbps link with 100 ms RTT, the BDP is ~12.5 MB—far exceeding the unscaled window.

## Q80: What is a network management protocol?

**A:** SNMP (Simple Network Management Protocol) is the standard protocol for managing network devices. Agents on devices respond to manager queries and send traps (asynchronous alerts). SNMP versions: v1 (community strings, cleartext), v2c (improved, still cleartext), v3 (authentication, encryption).

Other management protocols include NETCONF/YANG (configuration management), syslog (log collection), sFlow/NetFlow/IPFIX (traffic monitoring), and ICMP (connectivity monitoring). The OSI FCAPS model defines Management, Fault, Configuration, Accounting, Performance, and Security.

## Q81: What is the difference between a wildcard mask and a subnet mask?

**A:** A wildcard mask is the inverse of a subnet mask—used in ACLs and OSPF configurations to match specific IP addresses. Where a subnet mask has 1s for network bits, a wildcard mask has 0s. For example, /24 (255.255.255.0) has wildcard 0.0.0.255.

Wildcard masks are more flexible—they can match non-contiguous bit patterns (e.g., 0.0.255.0 matches any value in the third octet). Subnet masks must be contiguous. Wildcard masks are essential for OSPF area definitions and access control lists.

## Q82: What is the purpose of the TCP FIN-WAIT-1 state?

**A:** FIN-WAIT-1 is the state entered after sending a FIN segment—the socket is closing but may still receive data. It transitions to FIN-WAIT-2 after receiving ACK for the FIN, then to TIME_WAIT after receiving the peer's FIN.

If the peer doesn't send FIN promptly, FIN-WAIT-1 can persist. Some OSes implement a timeout (e.g., 30 seconds on Linux) to abort connections stuck in FIN-WAIT-1. This state is part of TCP's graceful connection termination.

## Q83: What is the difference between a WAN link and a LAN cable?

**A:** LAN cables (Cat5e, Cat6, Cat6a) support distances up to 100 meters and speeds up to 10 Gbps. WAN links use long-haul technologies: MPLS, leased lines, fiber optics, microwave, or satellite, spanning kilometers to intercontinental distances.

WAN technologies include: MPLS (multi-protocol label switching for traffic engineering), Metro Ethernet, DWDM (dense wavelength division multiplexing for fiber capacity), and SD-WAN (software-defined overlay over multiple transports).

## Q84: What is the role of the TCP URG pointer?

**A:** The Urgent Pointer is a 16-bit field that works with the URG flag to identify the position of urgent data within the segment. It specifies the sequence number offset where urgent data ends—everything before the pointer is considered urgent data.

In modern practice, URG and Urgent Pointer are rarely used. SSH, HTTP, and most application protocols handle priority data within the normal data stream. The urgent mechanism was more relevant for protocols like telnet.

## Q85: What is an IANA-assigned port?

**A:** IANA (Internet Assigned Numbers Authority) manages the global port number registry. Port ranges: 0-1023 (well-known, require root/admin on Unix), 1024-49151 (registered, assigned for specific applications), 49152-65535 (dynamic/private, used for ephemeral connections).

IANA registration ensures no two applications use the same port number. Well-known ports are restricted for security—only privileged processes can bind to them. Registered ports are assigned by IANA upon application.

## Q86: What is the purpose of the TCP Selective Acknowledgment (SACK)?

**A:** SACK (RFC 2018) allows the receiver to specify non-contiguous blocks of received data, enabling the sender to retransmit only the missing segments. Without SACK, the sender must retransmit all data from the first lost segment (go-back-N).

SACK is negotiated during the three-way handshake and included in TCP options of ACK segments. It significantly improves performance on lossy networks by reducing unnecessary retransmissions. SACK is now widely supported and enabled by default.

## Q87: What is the difference between a port and a socket?

**A:** A port is a 16-bit number (0-65535) identifying a network service or application at the transport layer. A socket is a complete endpoint of a connection, defined by the 5-tuple: (protocol, source IP, source port, destination IP, destination port).

One port can have multiple sockets—different clients connecting to the same server port create different sockets. The server's listening socket accepts connections and creates a new connected socket for each client.

## Q88: What is the effect of a small MTU on network performance?

**A:** A smaller MTU means more packets per unit of data (more headers, more processing), increasing overhead and reducing throughput. However, smaller MTUs reduce latency for individual packets and improve performance on lossy links (less retransmission overhead).

Path MTU Discovery discovers the smallest MTU along the path. If a router can't forward a packet due to MTU, it fragments (IPv4) or drops and sends ICMP Fragmentation Needed (both IPv4/IPv6). fragmentation is avoided in IPv6 by source fragmentation.

## Q89: What is the HTTP header Host?

**A:** The Host header specifies the domain name (and optionally port) of the server being requested. It's mandatory in HTTP/1.1 and enables virtual hosting—one IP address serving multiple domains. The server uses it to route requests to the correct virtual host.

Without the Host header, a server with multiple domains on one IP couldn't determine which website to serve. This is fundamental to shared hosting, CDNs, and reverse proxies. HTTP/2 uses the :authority pseudo-header instead.

## Q90: What is a Layer 2 tunnel?

**A:** A Layer 2 tunnel extends a Layer 2 network across a Layer 3 infrastructure. Protocols include L2TP (Layer 2 Tunneling Protocol), VXLAN (Virtual Extensible LAN, overlay network using UDP encapsulation), GRE (Generic Routing Encapsulation), and QinQ (802.1Q in 802.1Q).

L2 tunnels are used for VPNs (connecting remote offices), data center overlays (VXLAN), and service provider L2VPNs (VPLS). They encapsulate Layer 2 frames within IP packets, allowing transparent Layer 2 connectivity over any IP network.

## Q91: What is the purpose of the TCP PUSH flag?

**A:** The PSH flag instructs the receiver to immediately deliver accumulated data to the application without waiting for more data. This reduces latency for interactive applications. Without PSH, the receiver might buffer data to fill its buffer before delivering.

In practice, most TCP implementations set PSH on every segment. Applications can explicitly request PSH using socket options. PSH is especially important for protocols where low-latency data delivery matters (SSH, interactive shells, real-time protocols).

## Q92: What is the difference between a private and public IP address?

**A:** Private IP addresses are non-routable on the Internet (RFC 1918): 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. They're used within LANs and require NAT for Internet access. Public IP addresses are globally routable and unique across the Internet.

IPv6 unique local addresses (fc00::/7) serve the same purpose as IPv4 private addresses. Carrier-grade NAT (CGNAT) extends private addressing when public IPv4 is exhausted, adding another NAT layer.

## Q93: What is the purpose of ICMP Echo?

**A:** ICMP Echo Request (Type 8) and Echo Reply (Type 0) implement the ping command. It measures round-trip time, tests connectivity, and verifies that a destination is reachable and responding. Ping uses ICMP, not TCP or UDP.

Ping results show RTT and packet loss percentage. Extended ping can specify payload size, TTL, and interval. Path MTU Discovery uses ping with Don't Fragment bit set and increasing payload sizes to discover the path MTU.

## Q94: What is a network packet capture filter?

**A:** Capture filters (BPF—Berkeley Packet Filter syntax) limit which packets are captured at the NIC level, reducing capture file size and improving performance. Examples: `host 10.0.0.1`, `port 80`, `tcp port 443`, `net 192.168.1.0/24`.

Display filters in Wireshark work on already-captured packets and are more flexible. Capture filters are applied before capture starts, making them more efficient for high-traffic environments. Both use similar syntax but serve different purposes.

## Q95: What is the role of the TCP MSS Option?

**A:** The MSS option (kind=2, 4 bytes) advertises the maximum segment size the sender is willing to receive, set during the three-way handshake in SYN segments. MSS is typically MTU minus 40 bytes (20-byte TCP + 20-byte IP headers).

MSS clamping is used in NAT/VPN scenarios where encapsulation reduces effective MTU. The firewall/proxy adjusts the MSS value in SYN segments to prevent fragmentation. Default MSS for Ethernet is 1460 bytes.

## Q96: What is the difference between connection reset and connection refusal?

**A:** Connection reset (RST) terminates an established connection abruptly—data may be lost. Connection refusal (RST in response to SYN) indicates no service is listening on the target port. Both use the RST flag but in different contexts.

Connection reset happens when one side sends RST (e.g., application crash, firewall kill). Connection refusal happens when the server sends RST to reject the SYN. Port scanners distinguish open (SYN-ACK), closed (RST), and filtered (no response/ICMP unreachable) ports.

## Q97: What is a network address space?

**A:** The address space is the total range of addresses available for assignment within a particular address family or protocol. IPv4 has approximately 4.3 billion addresses (2^32). IPv6 has 3.4×10^38 addresses (2^128).

Address space exhaustion was a major driver for IPv6 adoption. Private addressing, NAT, and CIDR temporarily extended IPv4's useful life. IPv6 provides sufficient addresses for every device on Earth with addresses to spare.

## Q98: What is TCP Retransmission Timeout (RTO)?

**A:** RTO is the time a TCP sender waits for an ACK before retransmitting a segment. It's dynamically calculated based on the measured RTT and its variance (Jacobson's algorithm). RTO = SRTT + 4 × RTTVAR, with minimum 200ms and maximum 60s typically.

If a retransmission isn't acknowledged, RTO doubles exponentially (exponential backoff) to avoid congestion. The initial RTO is typically 1-3 seconds. RTO must be carefully tuned—too short causes unnecessary retransmissions, too long delays loss recovery.

## Q99: What is the purpose of a network load balancer?

**A:** A load balancer distributes incoming traffic across multiple servers to optimize resource utilization, maximize throughput, minimize response time, and avoid overload. Load balancers operate at Layer 4 (TCP/UDP) or Layer 7 (HTTP/HTTPS) and use algorithms like round-robin, least connections, or IP hash.

L4 load balancers forward packets based on IP/port without inspecting content. L7 load balancers make routing decisions based on HTTP headers, URLs, cookies, or content type. Health checks determine which servers are available to receive traffic.

## Q100: What is the TCP Initial Sequence Number (ISN)?

**A:** The ISN is the starting sequence number chosen by each side during the three-way handshake. It should be random (RFC 6528) to prevent TCP spoofing and hijacking attacks. Predictable ISNs allow attackers to inject segments into established connections.

ISN is generated using a hash of source/destination IPs, ports, and a secret value that increments by ~64,000 per second. This makes ISNs difficult to predict while ensuring they don't wrap around within the Maximum Segment Lifetime (MSL).
