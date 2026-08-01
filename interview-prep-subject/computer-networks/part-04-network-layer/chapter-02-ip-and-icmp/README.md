# IP and ICMP

> **TL;DR**: The IPv4 datagram is the network layer's packet format (20-60-byte header, fragmentation, TTL, protocol field); **ARP** maps IP→MAC for on-link delivery; **ICMP** is the control/error message protocol (ping, traceroute, errors, ECN echo) — the trio that makes "send to that IP" physically happen.

## Chapter Roadmap
- **IPv4 datagram format**: header fields (version, IHL, TOS/ECN, total length, identification/fragments, TTL, protocol, checksum, src/dst), fragmentation math, MTU.
- **ARP/RARP & helpers**: ARP request/reply, cache, gratuitous ARP, ARP spoofing defense; RARP/BOOTP (legacy); proxy ARP.
- **ICMP & traceroute**: ICMP message types (echo, unreachable, redirect, time-exceeded), ping, TTL-based traceroute internals, ICMP in security.

## Section Files
- `section-01-ipv4-datagram-format.md` — the 20-byte header field-by-field, fragmentation, TTL, protocol field, header checksum.
- `section-02-arp-rarp-and-ip-helper-protocols.md` — ARP lifecycle, cache, gratuitous/spoofing/proxy, RARP/BOOTP/DHCP lineage.
- `section-03-icmp-and-traceroute-internals.md` — ICMP messages, ping, traceroute's TTL trick, ICMP uses/abuses.

## Interview Q&A Preview
- **"What does TTL do?"** → Time-To-Live (now hop count) — each router decrements; at 0, the router drops the packet and sends ICMP Time-Exceeded. It bounds loops; traceroute *exploits* it (send TTL=1, 2, 3... and read the Time-Exceeded sources to map the path).
- **"How does ARP work?"** → Broadcast "who has 192.168.1.1? Tell 192.168.1.5"; the owner unicasts "I have 192.168.1.1, MAC 00:11:22:33:44:55"; both cache the mapping. Cached for ~minutes; also sends gratuitous ARP on startup/interface events.
- **"What is the purpose of ICMP?"** → Carrying *errors and control* for IP — unreachable destinations, TTL exceeded, redirects, plus the echo (ping) and the ECN feedback path. It's IP's "status/notification" channel, not for data transport.
