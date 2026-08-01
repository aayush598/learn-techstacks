# Part: Transport Layer

## What this part covers
Part 03 is the **heart of the Internet** — the transport layer that decides whether data gets there *reliably* (TCP), *fast* (UDP), or *both* (QUIC, SCTP). This is where interviews get deep: the TCP three-way handshake, sequence numbers, flow control (sliding window), congestion control (slow start, AIMD, fast retransmit), timers, the TCP state machine, Nagle/Delayed-ACK — plus the modern story of QUIC replacing much of it. If Parts 01-02 are the map and the language, Part 03 is the *engine*.

## Chapter map
| Chapter | Sections | Key skills |
|---|---|---|
| chapter-01: Transport Fundamentals | Role & services / Ports & sockets | Explain multiplexing; TCP vs UDP services; port/socket semantics |
| chapter-02: UDP | UDP in depth | Segment format, checksum, use cases, when to pick UDP |
| chapter-03: TCP | Segment structure / Handshake / Termination / Flow control / Congestion control / Reliability & timers / State machine & Nagle | Walk every TCP mechanism with numbers |
| chapter-04: Advanced Transport | QUIC in depth / SCTP & others | Compare QUIC vs TCP; SCTP/DCCP roles |

## Study order
1. **chapter-01**: transport's role + ports (the vocabulary).
2. **chapter-02**: UDP — the simple baseline.
3. **chapter-03**: TCP — the 80% of interview weight. Master it one section at a time.
4. **chapter-04**: QUIC/SCTP — the modern + exotic.

## Interview importance
⭐⭐⭐⭐⭐ (5/5). TCP is *the* most-tested protocol in FAANG networking interviews. Congestion control (slow start, AIMD, BBR), the handshake, and "why does TCP throttle throughput?" come up constantly. HTTP/3/QUIC questions are the modern flavor. Expect both concept and math questions (window/RTT/throughput calculations).

## How the parts connect (roadmap)
- Part 01 gave the layers; Part 03 fills **Transport (L4)**.
- Part 02's HTTP/DNS/email ride *on* TCP/UDP from this part.
- Part 04's IP layer is what TCP/UDP run *over*; the TCP checksum even covers IP addresses (pseudo-header).
- QUIC (Part 03) actually *replaces* TCP+parts of TLS for HTTP/3 — the transport's future.
