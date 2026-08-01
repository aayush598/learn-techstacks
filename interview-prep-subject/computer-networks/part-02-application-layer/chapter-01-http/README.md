# Chapter: HTTP

## What you'll learn
- What HTTP is, its evolution (0.9 → 1.0 → 1.1 → 2 → 3), and why each version exists.
- The full HTTP request/response anatomy: methods, status codes, headers, and semantics.
- How HTTP/2 (multiplexing, HPACK) and HTTP/3 (QUIC over UDP) fix HTTP/1.1's problems.
- How HTTPS + TLS encrypt and authenticate web traffic, including the TLS 1.3 handshake.
- How cookies, sessions, and authentication (Bearer tokens, OAuth) work in practice.

## Prerequisites (linked)
- [Part 01: OSI & TCP/IP Models](../chapter-02-osi-and-tcp-ip-models/README.md) — HTTP is an application-layer protocol over TCP/IP.
- [Part 03: TCP three-way handshake](../../part-03-transport-layer/chapter-03-tcp/README.md) — HTTP/1.1 and HTTP/2 run over TCP; HTTP/3 over QUIC/UDP.

## Sections (linked table)
- [section-01-http-overview-and-versions](section-01-http-overview-and-versions.md)
- [section-02-http-methods-status-codes-and-headers](section-02-http-methods-status-codes-and-headers.md)
- [section-03-http2-http3-and-quic](section-03-http2-http3-and-quic.md)
- [section-04-https-and-tls-handshake](section-04-https-and-tls-handshake.md)
- [section-05-cookies-sessions-and-authentication](section-05-cookies-sessions-and-authentication.md)

## One-paragraph narrative connecting all sections
HTTP started as a trivial line-based protocol (0.9) and grew into HTTP/1.1 — the mature request/response protocol whose methods, status codes, and headers (section 02) define how the web works. Its flaw (head-of-line blocking, one request per connection) drove HTTP/2's multiplexing and HTTP/3's QUIC-over-UDP redesign (section 03). Meanwhile, the web needed confidentiality — HTTPS wraps HTTP in TLS (section 04). And because HTTP is stateless, cookies, sessions, and token auth (section 05) add the state that products need. Section 01 frames the whole journey.

## Common interview trap in this chapter
Trap: "HTTP/2 uses multiple TCP connections." — **Wrong.** HTTP/2 uses *one* TCP connection with multiplexed streams (and typically TLS). It's HTTP/3 that changes transports (QUIC over UDP). Also a trap: "HTTPS and TLS are the same thing" — TLS is the protocol; HTTPS is HTTP running inside TLS. And: "DELETE/PUT are idempotent so retries are safe" — PUT and DELETE are idempotent by definition, but only if your *application* implements them idempotently.

## Checklist before moving on
- [ ] I can walk a full HTTP/1.1 request through headers/status and explain each.
- [ ] I can list all standard methods, their safety/idempotency, and give curl examples.
- [ ] I can explain HTTP/2 multiplexing + HPACK and why HOL blocking exists in 1.1/2 but not 3.
- [ ] I can describe the TLS 1.3 handshake (1-RTT, key exchange, forward secrecy).
- [ ] I can design cookie/session/JWT auth and explain XSS/CSRF mitigations.
