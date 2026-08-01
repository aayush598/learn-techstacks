# Chapter: Transport Layer Fundamentals

## What you'll learn
- The transport layer's two jobs: **end-to-end delivery** between processes (multiplexing/demultiplexing via ports) and **process-to-process communication** — layered between the application and the network.
- The full menu of transport services: reliability, ordering, flow control, congestion control, connection orientation — and how TCP vs UDP pick different subsets.
- Ports and sockets: the (IP, port) tuple, well-known/registered/ephemeral ports, and how a socket demultiplexes millions of connections.

## Prerequisites (linked)
- [Part 01: OSI/TCP-IP models](../../part-01-network-fundamentals/chapter-02-osi-and-tcp-ip-models/README.md) — transport is OSI L4 / TCP-IP Transport layer.
- [Part 02: HTTP](../../part-02-application-layer/chapter-01-http/README.md) — real protocols that ride TCP/UDP.

## Sections (linked table)
- [section-01-transport-layer-role-and-services](section-01-transport-layer-role-and-services.md)
- [section-02-ports-and-sockets](section-02-ports-and-sockets.md)

## One-paragraph narrative connecting all sections
Section 01 answers the big question: what does transport *do*? It takes the network layer's best-effort, per-packet, host-to-host IP delivery and gives *processes* a channel — choosing the service mix (reliable/ordered/flow/congestion-controlled for TCP; minimal for UDP). Section 02 then makes it concrete: the port number is what selects the *process*, and the four-tuple (srcIP, srcPort, dstIP, dstPort) is what identifies each *socket* — the exact structure that lets one server host 100k simultaneous connections. Together they build the vocabulary for everything in the rest of this part.

## Common interview trap in this chapter
Trap: "The transport layer is only TCP and UDP." — there's also SCTP, DCCP, and the internet's Protocol field includes many. Also: "UDP is always unreliable" — UDP *can* carry reliability (QUIC adds it; the application can too); UDP's *protocol* is just minimal. And: "a port identifies a process" — a port identifies a *service end-point* (socket), which can be shared by many connections (and one process can hold many sockets).

## Checklist before moving on
- [ ] I can list the six transport services and which TCP/UDP provides each.
- [ ] I can explain multiplexing/demultiplexing with a concrete example.
- [ ] I know the port ranges (well-known 0-1023, registered 1024-49151, dynamic 49152-65535).
- [ ] I can describe the four-tuple and how the OS demultiplexes a packet to the right socket.
- [ ] I can define "socket" precisely (end-point, not the connection).
- [ ] I can explain the UDP checksum and the TCP pseudo-header reason.
