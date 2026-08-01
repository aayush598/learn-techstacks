# Advanced Transport — QUIC and Beyond

> **TL;DR**: QUIC is the modern transport — TCP's reliability + UDP's pass-through + TLS 1.3 built-in + multiplexed streams without head-of-line blocking + 0-RTT — deployed as the HTTP/3 basis everywhere; SCTP, DCCP, and others round out the "non-TCP transport" zoo with special-purpose semantics.

## Chapter Roadmap
- **Why QUIC exists**: TCP's head-of-line blocking, kernel lock-in, 1-RTT handshake, and connection migration — the four problems QUIC was built to solve.
- **QUIC internals**: packets, streams, frames, connection IDs, 0-RTT, loss recovery, congestion control in user space.
- **HTTP/3**: QUIC as the web transport — mapping HTTP semantics, QPACK, and what it changes for CDNs/browsers.
- **Other transports**: SCTP (multihoming, partial reliability), DCCP (congestion-controlled unreliable), and when you'd pick each.

## Section Files
- `section-01-quic-protocol-in-depth.md` — packets/streams/frames, handshake (1-RTT/0-RTT), migration, loss recovery, HTTP/3, deployment reality.
- `section-02-sctp-and-other-transport-protocols.md` — SCTP (RFC 9260), DCCP, and the transport design space.

## Interview Q&A Preview
- **"Why did Google build QUIC on UDP?"** → TCP is kernel-bound and middlebox-frozen; a new IP protocol number would never traverse the Internet. UDP is the one header every network forwards — QUIC hides its protocol inside it and ships in userspace.
- **"What is head-of-line blocking and how does QUIC fix it?"** → A lost TCP segment stalls the *whole* byte stream (all subsequent HTTP/2 streams wait). QUIC has *independent streams* — each with its own reliability — so one stream's loss never blocks another.
- **"What is 0-RTT in QUIC?"** → A repeat connection sends encrypted app data in the first flight (using a cached session key) — the client's request arrives in the same RTT as the connection setup. Security caveat: replayable, so only for idempotent/safe requests.

## Key Diagrams to Recreate
1. **TCP vs QUIC connection model**: one byte stream (TCP) vs many independent streams in one connection (QUIC).
2. **QUIC packet**: header (short/long form, Connection ID) + frames (STREAM, ACK, CRYPTO, PING, NEW_CONNECTION_ID...).
3. **Handshake**: 1-RTT (full, like TLS 1.3-in-TCP) vs 0-RTT (replay token).
4. **Migration**: connection ID lets the connection survive an IP change (mobile wifi→LTE) — the tuple changes, the connection doesn't.
