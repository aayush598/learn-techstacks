# Part: Application Layer

## What this part covers
Part 02 goes to the **top of the stack** — the protocols you and your users actually see: HTTP (the web's transport of meaning), HTTPS/TLS (its security), DNS (the Internet's phone book), email protocols (SMTP/IMAP/POP3), DHCP (automatic configuration), and the modern real-time/specialized protocols (WebSockets, SSE, Webhooks, FTP/SSH). These are the protocols that power every product at FAANG — every web request, every API call, every authentication flow is built on them. If Part 01 is the *map*, Part 02 is the *language* spoken at the surface.

## Chapter map
| Chapter | Sections | Key skills |
|---|---|---|
| chapter-01: HTTP | HTTP versions / Methods-status-headers / HTTP2-3+QUIC / HTTPS+TLS / Cookies-sessions-auth | Explain a full HTTP transaction; compare HTTP/1.1, 2, 3; explain TLS handshake; design auth |
| chapter-02: DNS | Hierarchy / Resolution process / Record types + advanced | Trace a DNS lookup; explain caching/TTL; know all record types; explain DNSSEC, DoH |
| chapter-03: Email, DHCP & other protocols | SMTP/POP3/IMAP / DHCP / FTP-SSH-telnet / WebSockets-webhooks-SSE | Explain mail delivery chain; DORA DHCP; SSH vs telnet; real-time transport options |

## Study order
1. **chapter-01 (HTTP)**: the single most-asked protocol in interviews — start here.
2. **chapter-02 (DNS)**: needed to complete the "what happens when you type a URL" story.
3. **chapter-03**: fill in email, DHCP, and the real-time/webhook landscape.

## Interview importance
⭐⭐⭐⭐⭐ (5/5). The application layer *is* the interview: "What happens when you type google.com?", "Explain HTTP/2 vs HTTP/3", "How does HTTPS work?", "How do cookies work?", "Design DNS for a big site." Every FAANG system-design and networking interview opens here.

## How the parts connect (roadmap)
- Part 01 gave you the layers; Part 02 populates the **Application layer**.
- Part 03 (Transport) explains the TCP/UDP machinery that HTTP, DNS, and email *ride on*.
- Part 04 (Network) explains the IP addressing/routing/DNS-to-IP layer underneath.
- To answer "type a URL" fully you need: Part 02 (HTTP, DNS, TLS) + Part 03 (TCP handshake) + Part 04 (IP, routing).
