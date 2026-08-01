# Chapter: Network Basics

## What you'll learn
- The precise definition of a computer network and *why* networks exist (resource sharing, communication, distribution).
- The four key characteristics that define network quality: performance, reliability, security, scalability.
- Network topologies (bus, star, ring, mesh, hybrid, tree) and how to compare them on cost, fault tolerance, and scalability.
- How networks are classified by geographic scope: PAN, LAN, MAN, WAN, and (bonus) CAN, SAN, VPN.

## Prerequisites (linked)
- [Part 01 README](../README.md) — understand the part structure and study order.

## Sections (linked table)
- [section-01-what-is-a-computer-network-and-why-networks-exist](section-01-what-is-a-computer-network-and-why-networks-exist.md)
- [section-02-network-topologies](section-02-network-topologies.md)
- [section-03-lan-man-wan-pan-and-network-types](section-03-lan-man-wan-pan-and-network-types.md)

## One-paragraph narrative connecting all sections
A network exists to share resources and move data between devices (section 01). *How* those devices are physically or logically wired together is the topology (section 02) — it determines cost, resilience, and how collisions scale. *How big* the network is, geographically and organizationally, determines which protocols and devices are appropriate (section 03): a PAN uses Bluetooth, a LAN uses switches + Ethernet, a WAN uses routers + leased lines. The three sections build one mental model: **purpose → structure → scale**.

## Common interview trap in this chapter
Trap: "The Internet is a WAN." — **Wrong.** The Internet is a *network of networks* (an internetwork / inter-network), not a single WAN. A WAN is one large network (e.g., a bank's nationwide backbone). The Internet connects thousands of LANs, WANs, and MANs using routers and a common IP protocol. Also a common trap: calling a hub a "switch" — they behave completely differently (hub = shared collision domain, switch = per-port collision domain).

## Checklist before moving on
- [ ] I can define a network and list 4 reasons networks exist.
- [ ] I can draw bus/star/ring/mesh/topologies and state each one's single point of failure.
- [ ] I can map the order of *least→most expensive* topologies: bus → star → ring → mesh.
- [ ] I can classify PAN/LAN/MAN/WAN by range and give a real example of each.
- [ ] I can explain why the Internet is NOT a WAN.
- [ ] I can answer "What happens when you type google.com?" at a layer-1/2/3 level.
