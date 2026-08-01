# Chapter: Network Devices

## What you'll learn
- The full ladder of network devices — repeater, hub, switch, router, gateway — and exactly which layer each operates at and why.
- How each device makes forwarding decisions (bits broadcast / MAC learning / IP longest-prefix match).
- The critical production concepts of **collision domains** and **broadcast domains**, and how each device shrinks/expands them.
- When to pick each device in a real network design (office, datacenter, WAN).

## Prerequisites (linked)
- [Chapter 01: Network Basics](../chapter-01-network-basics/README.md) — topologies (star, bus) directly drive the collision/broadcast-domain discussion.
- [Chapter 02: OSI & TCP/IP Models](../chapter-02-osi-and-tcp-ip-models/README.md) — devices are defined *by layer*; you must know hub=L1, switch=L2, router=L3.

## Sections (linked table)
- [section-01-repeaters-hubs-switches-routers-gateways](section-01-repeaters-hubs-switches-routers-gateways.md)
- [section-02-networking-topologies-practice-and-collision-vs-broadcast-domains](section-02-networking-topologies-practice-and-collision-vs-broadcast-domains.md)

## One-paragraph narrative connecting all sections
Section 01 builds the device ladder from the dumbest to the smartest: repeaters and hubs just regenerate bits (L1) — they extend reach but *merge* collision domains. Switches (L2) learn MAC addresses and forward selectively, giving every port its own collision domain. Routers (L3) forward by IP and bound broadcast domains, connecting separate networks. Gateways translate between completely different protocol stacks. Section 02 then applies this: in real topologies (star LANs, datacenter fabrics, office networks), the *practical* questions are "how many hosts can collide?" and "how far do broadcasts reach?" — answered by counting collision vs broadcast domains and choosing devices accordingly.

## Common interview trap in this chapter
Trap: "A switch is faster than a router because it's L2." — half-true. Switches forward in hardware at line rate because they make a simple decision (exact MAC match), but modern routers also forward at line rate (TCAM longest-prefix-match, 400G). The real difference is *decision logic*, not speed. Second trap: "A router is just a switch with more brains" — no, they solve different problems: a router joins *separate IP networks*, a switch joins hosts *within one network*. Third: calling a hub "a shared medium like the old bus" — correct, but note a hub is a *physical* star that is a *logical* bus (one collision domain).

## Checklist before moving on
- [ ] I can order devices by intelligence: repeater → hub → bridge → switch → router → gateway.
- [ ] I can state the layer and forwarding decision for each device.
- [ ] I can define collision domain and broadcast domain and say which devices create/remove them.
- [ ] I can explain why switches don't stop broadcasts but routers do.
- [ ] I can answer "hub vs switch vs router — when to use each?" with a concrete topology.
- [ ] I can explain MAC learning and the difference between unknown-unicast flooding and broadcast.
