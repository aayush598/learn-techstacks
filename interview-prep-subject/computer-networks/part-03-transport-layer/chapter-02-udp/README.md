# UDP — User Datagram Protocol

> **TL;DR**: The connectionless, fire-and-forget transport protocol — no handshake, no reliability, no ordering, just datagrams (up to 65507 bytes payload) delivered best-effort with a checksum. Tiny header (8 bytes), minimal latency, and used where real-time freshness beats guaranteed delivery: DNS, DHCP, VoIP, gaming, video, and QUIC's payload.

## Chapter Roadmap
- **UDP overview**: datagram service, 8-byte header, multiplexing by port, checksum, segmentation vs fragmentation.
- **Why no reliability**: TCP overhead vs latency; what UDP gives up and why apps accept it.
- **UDP vs TCP in practice**: which one for which workload.
- **Building reliability on UDP**: retransmit layers (QUIC, RTP+RTCP, TFTP, custom app protocols).
- **Interview answers**: UDP in DNS, DHCP, streaming, gaming; the "reliability at the app layer" argument.

## Section Files
- `section-01-udp-in-depth.md` — everything: header layout, checksum math, fragmentation, IPv6/UDP (UDP Lite, UDP over IPv6), QUIC-over-UDP, real tcpdump captures, and the full 22-block treatment.

## Interview Q&A Preview
- **"Why use UDP when TCP is reliable?"** → Because reliability costs latency and head-of-line blocking; UDP gives the *app* control over retransmission and pacing — QUIC proves the model.
- **"What guarantees does UDP provide?"** → Exactly one: checksummed, port-delivered datagrams. No delivery, ordering, or duplicate guarantee.
- **"How does DNS use UDP?"** → Single-question/single-answer datagrams that fit in one MTU; retransmit with timeout on the app side; fall back to TCP when responses exceed 512 bytes (or for zone transfers). A UDP+timeout is cheaper than a TCP handshake for every query.
- **"Why does video streaming prefer UDP?"** → A dropped frame is *supposed* to be dropped — retransmitting old frames wastes bandwidth and adds latency; real-time freshness wins. (Reality: Netflix/YouTube often use TCP for on-demand; UDP for live/WebRTC.)

## Key Diagrams to Recreate
1. **UDP datagram header**: [SrcPort 16][DstPort 16][Length 16][Checksum 16] = 8 bytes.
2. **Checksum coverage**: pseudo-header (srcIP+dstIP+zero+proto+udpLen) + UDP header + data — one layer's "free" integrity check.
3. **IP fragmentation of one large datagram**: MTU 1500 → fragments reassembled at the destination (fragmentation is IP's job, not UDP's).
4. **UDP multiplexing**: all senders → one socket (dstIP, dstPort); the app demultiplexes via `recvfrom`'s sender address.
