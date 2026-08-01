# Chapter: DNS

## What you'll learn
- The DNS hierarchy: root → TLD → authoritative servers, and the concept of a delegated, distributed database.
- The full resolution process: recursive vs iterative queries, caching, TTLs, and the "what happens when you type a URL" flow.
- All record types (A, AAAA, CNAME, MX, NS, TXT, SRV, SOA, PTR) and advanced topics (DNSSEC, DNS over HTTPS/TLS, anycast, round-robin, split-horizon).

## Prerequisites (linked)
- [Chapter 01: HTTP](../chapter-01-http/README.md) — DNS is the first step of every web request.
- [Part 01: TCP/IP model](../../part-01-network-fundamentals/chapter-02-osi-and-tcp-ip-models/README.md) — DNS is an application-layer protocol over UDP (mostly).

## Sections (linked table)
- [section-01-dns-hierarchy-and-name-spaces](section-01-dns-hierarchy-and-name-spaces.md)
- [section-02-dns-resolution-process](section-02-dns-resolution-process.md)
- [section-03-dns-record-types-and-advanced-dns](section-03-dns-record-types-and-advanced-dns.md)

## One-paragraph narrative connecting all sections
DNS exists because humans remember names and machines use numbers — section 01 establishes the *distributed, hierarchical database* (root/authoritative nameservers) that makes "namespace → IP" mapping work at planetary scale without a single point of failure. Section 02 traces *how* a name becomes an address (recursive resolver → root → TLD → authoritative, with caching/TTL), which is the canonical "type a URL" story. Section 03 covers the *records* that encode the answers (A/AAAA/CNAME/MX…), then the production hardening: DNSSEC (integrity), DoH/DoT (privacy), anycast/round-robin (scale/reliability), and split-horizon/GeoDNS (application-level routing).

## Common interview trap in this chapter
Trap: "DNS is a protocol that maps domain names to IP addresses." — half-true but shallow. DNS is a *distributed database and lookup system* (it stores MX for mail, TXT for SPF, CNAMEs, SRV for services), and the *resolution* is iterative+recursive with caching. Second trap: "UDP port 53 always." DNS also runs over TCP (zone transfers, large responses) and now TLS/HTTPS (DoT/DoH). Third trap: confusing authoritative vs recursive resolvers — one *owns* the answer, the other *finds* it.

## Checklist before moving on
- [ ] I can draw the DNS tree and explain delegation (root → TLD → authoritative).
- [ ] I can trace a full resolution (recursive vs iterative) with caching + TTL.
- [ ] I can explain A/AAAA/CNAME/MX/NS/TXT/SRV/SOA/PTR with one use each.
- [ ] I can explain DNSSEC's purpose and how DoH/DoT change the model.
- [ ] I can explain how anycast + round-robin + GeoDNS make DNS scale and route.
- [ ] I can answer the "type a URL" DNS portion end-to-end.
