# Part: Network Fundamentals

## What this part covers
Part 01 answers the most basic question in networking: **what is a network and what are its building blocks?** Before you can talk about TCP congestion control, BGP routing, or TLS handshakes, you must understand what a network *is*, how it's *structured* (topologies), how it's *scaled* (LAN/MAN/WAN), how the layers *organize* all protocols (OSI and TCP/IP models), how data *moves* through those layers (encapsulation/PDUs), and what *hardware* does the moving (hubs, switches, routers). This part is the foundation — every later part (application, transport, network layer) assumes you know these concepts cold.

## Chapter map
| Chapter | Sections | Key skills |
|---|---|---|
| chapter-01: Network Basics | What is a network / Topologies / LAN-MAN-WAN-PAN | Define a network; compare topologies; classify networks by scope |
| chapter-02: OSI & TCP/IP Models | OSI 7 layers / TCP/IP 4 layers / OSI vs TCP/IP / Encapsulation | Name layers in order; map protocols to layers; explain PDU chaining |
| chapter-03: Network Devices | Repeaters/Hubs/Switches/Routers/Gateways / Collision & Broadcast domains | Choose the right device; explain collision vs broadcast domains |

## Study order
1. **chapter-01**: Build vocabulary (node, link, topology, LAN/WAN).
2. **chapter-02**: Learn the *framework* — layers are how all networking is reasoned about.
3. **chapter-03**: Learn the *hardware* that implements the layers.

Read in this order; each chapter's concepts are used by the next.

## Interview importance
⭐⭐⭐⭐ (4/5). The OSI model and the difference between a switch and a router are *guaranteed* warm-up questions in virtually every networking interview. Even at FAANG (Meta, Amazon, Google), interviewers open with "Explain the OSI model" or "What happens when you type google.com?" — Part 01 gives you the layers, Part 02+ gives you the deep protocol detail to answer the full chain.

## How the parts connect (roadmap)
- Part 01 gives you the **map** (layers) and **terrain** (devices).
- Part 02 (Application Layer) walks the top of the stack: HTTP, DNS, email, DHCP.
- Part 03 (Transport Layer) dives into TCP/UDP/QUIC — the reliability machinery.
- Part 04 (Network Layer) covers IP addressing, subnetting, routing, NAT, VPNs, CDNs, QoS.
- Parts 05-08 add Security, Wireless, Data-link/physical details, and an interview question bank.
