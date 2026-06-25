# Network Topology & Protocols

## Topologies
| Topology | Pros | Cons |
|----------|------|------|
| **Star** | Simple, easy to manage | Single point of failure (hub) |
| **Ring** | Deterministic, fair | Single break disrupts all |
| **Bus** | Cheap, simple | Collisions, limited length |
| **Mesh** | Fault-tolerant, redundant | Expensive wiring |
| **Fully connected** | Max redundancy | O(n²) links |
| **Tree** | Hierarchical, scalable | Root bottleneck |

## TCP/IP Stack
| Layer | Protocols | PDU |
|-------|-----------|-----|
| **Application** | HTTP, FTP, SMTP, DNS | Message |
| **Transport** | TCP, UDP | Segment/Datagram |
| **Network** | IP, ICMP, ARP | Packet |
| **Link** | Ethernet, Wi-Fi | Frame |

## TCP (Transmission Control Protocol)
- **Connection-oriented**: 3-way handshake (SYN → SYN-ACK → ACK)
- **Reliable**: acknowledgments, retransmission on timeout
- **In-order delivery**: sequence numbers reassemble data
- **Flow control**: receiver's window (advertised window)
- **Congestion control**: slow start, congestion avoidance, fast retransmit
- **Stateful**: maintains connection state

## UDP (User Datagram Protocol)
- **Connectionless**: no handshake
- **Unreliable**: no ACK, no retransmission
- **Low overhead**: minimal header (8 bytes vs TCP's 20)
- Uses: DNS, video streaming, VoIP, DHCP

## RPC (Remote Procedure Call)
- Client calls remote function as if local
- **Stub**: client stub marshals args → network → server stub unmarshals → calls procedure
- IDL (Interface Definition Language) for data representation
- **Marshaling**: converting structured data to byte stream
- Sun RPC, DCE/RPC, JSON-RPC

## Modern Alternatives
- **REST**: HTTP methods (GET, POST, PUT, DELETE), stateless, JSON
- **gRPC**: HTTP/2 + Protocol Buffers, bi-directional streaming, typed contracts
- **GraphQL**: client queries exact data needed
