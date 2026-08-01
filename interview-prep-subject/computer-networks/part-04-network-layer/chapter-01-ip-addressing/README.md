# IP Addressing

> **TL;DR**: IP addressing is how every device on the Internet gets a unique locator — IPv4's 32-bit address space (classes → CIDR → subnetting) is nearly exhausted and IPv6's 128-bit space replaces it; understanding addressing, masks, and subnet math is the non-negotiable foundation of the network layer.

## Chapter Roadmap
- **IPv4 addressing & classes**: the 32-bit address, classful A/B/C boundaries, private vs public ranges, special addresses (loopback, link-local, multicast, broadcast).
- **Subnetting & CIDR**: subnet masks, prefix lengths, VLSM, subnet math, and why CIDR ended classful waste.
- **IPv6 addressing**: 128-bit space, hex notation, address types (unicast/multicast/anycast), SLAAC, transition mechanisms, and the reason we needed it.

## Section Files
- `section-01-ipv4-addressing-and-classes.md` — 32-bit structure, classful addressing, private/special ranges, address exhaustion story.
- `section-02-subnetting-and-cidr.md` — masks, prefix length, subnet math (the number-crunching interview topic), VLSM, CIDR aggregation.
- `section-03-ipv6-addressing.md` — notation, types, SLAAC/DHCPv6, transition (NAT64/464XLAT, dual-stack), deployment.

## Interview Q&A Preview
- **"What is the difference between classful and CIDR addressing?"** → Classful (A/B/C) fixed 8/16/24-bit network boundaries wasted huge address blocks; CIDR (RFC 4632) uses arbitrary prefix lengths (e.g., /20, /27) so address space is allocated and summarized exactly as needed — the Internet's routing table runs on CIDR + route aggregation.
- **"How do you subnet a network?"** → Determine hosts needed → choose prefix (hosts = 2^(32−prefix) − 2) → enumerate subnets by incrementing the network bits → derive network/broadcast/first/last host per subnet.
- **"Why is IPv6 needed?"** → 32-bit IPv4 = ~4.3B addresses, exhausted in 2011 (IANA) / 2019 (RIRs). IPv6's 128-bit space (~340 undecillion) plus stateless autoconfiguration (SLAAC), no NAT, and built-in security fixes the exhaustion and end-to-end problems.
