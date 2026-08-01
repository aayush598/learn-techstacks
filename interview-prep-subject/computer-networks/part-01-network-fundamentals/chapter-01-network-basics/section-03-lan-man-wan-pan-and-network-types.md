# LAN, MAN, WAN, PAN, and Network Types

> **TL;DR**: Networks are classified by geographic scope — PAN (personal), LAN (building/campus), MAN (city), WAN (country/planet) — and the classification exists because the *distance a network spans dictates its physics, latency, ownership, and technology*.

## 1. Why Does This Exist?
Distance changes everything in networking. A network spanning a room, a building, a city, or a continent faces different *physics* (propagation delay), different *ownership* (you own your LAN; nobody owns the Internet), different *technologies* (Ethernet vs leased line vs satellite), and different *failure modes*. Classification gives engineers a vocabulary and a set of design defaults: "this is a WAN" immediately implies routers, leased circuits, WAN protocols, and high latency budgets. It exists to guide technology selection and set expectations about performance.

## 2. How Does It Work?
The taxonomy is by **geographic reach** (primary axis) plus ownership and technology (secondary axes):
- **PAN (Personal Area Network)**: ~1-10 m, one person's devices — Bluetooth, USB, NFC, IR. Wireless PAN (WPAN) is IEEE 802.15.
- **LAN (Local Area Network)**: a room/building/campus, ≤ few km — Ethernet (IEEE 802.3) over twisted pair/fiber, Wi-Fi (802.11). Privately owned, high speed (Gbps), low latency (sub-ms).
- **MAN (Metropolitan Area Network)**: a city, 5-50 km — metro fiber rings (SONET/SDH, Ethernet-over-fiber, WDM), cable TV networks, WiMAX (legacy), municipal Wi-Fi. Often carrier-provided.
- **WAN (Wide Area Network)**: countries/continents — leased lines, MPLS, VPNs over the Internet, satellite. High latency (tens-hundreds of ms), moderate speed, owned by carriers or enterprises.
- Related types: **CAN** (Campus Area Network, ~1-5 km), **SAN** (Storage Area Network — high-speed block-storage network, Fibre Channel/iSCSI), **VPN** (Virtual Private Network — logical overlay on any physical network), and **Internet** (internetwork, not a single type).

## 3. When Is It Used?
- **PAN**: wireless earbuds (Bluetooth), smartwatch↔phone, NFC payments, wireless keyboard/mouse.
- **LAN**: office/enterprise Ethernet + Wi-Fi, home Wi-Fi, datacenter networks (though DCs are arguably private high-speed LANs/campus networks).
- **MAN**: city-wide broadband, cable ISPs' metro fiber, university campus backbones, local government networks.
- **WAN**: enterprise HQ↔branch connectivity (MPLS/VPN), cloud provider backbones (Google's B4, AWS global network), international Internet backbone links, satellite links.

## 4. Why Wasn't Another Approach Chosen?
The alternative to distance-based classification would be classifying by *ownership* (private vs public) or *technology* (Ethernet vs leased-line) alone. Those are useful secondary axes but fail to capture the *physical constraint*: you cannot use 100 m Ethernet segment limits on a city link. Why weren't MANs just "small WANs"? Because metro areas have distinct economics (shared dark fiber, municipal rights-of-way, ring topologies) and distinct tech (WDM metro rings) — a MAN is its own engineering problem. Why not call everything a LAN? Because WAN links run *leased circuits between routers* — protocol stacks, addressing, and latency budgets all differ. The distance axis is the one that drives every other design decision.

## 5. Intuition
Distance = physics. Within a building, light/fiber delays are microseconds — Ethernet's entire design (short frames, fast retransmit) assumes tiny round-trip times. Across a continent, the speed-of-light cap alone gives ~40-70 ms one-way; TCP must have big windows and timers to fill that pipe. The classification is really about: *how long does the round trip take, and who owns the road?* PAN = your hand; LAN = your house/office; MAN = your city; WAN = the planet.

## 6. Real-World Analogy
**Courier services**: PAN = handing a note to the person next to you (Bluetooth). LAN = internal office mail (you control the building, cheap and fast). MAN = city courier (you pay a courier company, cross-town, ~minutes). WAN = international shipping (you lease a container slot on planes/ships, slow, expensive, third-party owned). The Internet = using all couriers worldwide with a universal address system.

## 7. Formal Definition
By scope (Tanenbaum; Kurose & Ross):
- **PAN**: a network for communication between personal devices, typically within a range of about 10 meters (IEEE 802.15.1 Bluetooth; ZigBee 802.15.4).
- **LAN**: a network connecting devices within a limited area such as a home, office, or campus, characterized by private ownership, high data rates (≥1 Gbps), and low propagation delay; typically Ethernet (802.3) or Wi-Fi (802.11).
- **MAN**: a network spanning a metropolitan area (roughly 5-50 km), interconnecting multiple LANs, typically via fiber-optic ring or backbone technologies.
- **WAN**: a network spanning large geographic areas (states/countries/continents), interconnecting multiple LANs/MANs via leased lines, MPLS, or the Internet; latency dominated by speed-of-light in long-haul fiber (~5 µs/km).

## 8. Example
Concrete numbers for a file transfer across each scope (1 GB = 8×10⁹ bits, ideal, no overhead):
| Type | Typical link | Speed | Ideal time for 1 GB | One-way latency |
|---|---|---|---|---|
| PAN | Bluetooth 5.2 | 2 Mbps | ~67 min | <1 ms |
| LAN | Gigabit Ethernet | 1 Gbps | ~8 s | <0.5 ms |
| LAN | Wi-Fi 6 (client) | ~600 Mbps effective | ~13 s | ~1-5 ms |
| MAN | Metro fiber (10 GbE) | 10 Gbps | ~0.8 s | ~1-5 ms |
| WAN | Trans-Atlantic fiber | 100 Gbps | ~0.08 s (ideal) | ~65 ms (NY↔London) |
| WAN | Satellite (GEO) | 50 Mbps down | ~160 s | ~240-280 ms |

The WAN row is the key insight: the *propagation delay* (~65 ms one-way, ~130 ms RTT NY↔London) dwarfs transmission time. TCP throughput is capped by RTT (see TCP section): `Throughput ≈ Window/RTT`. To push 100 Gbps over 130 ms RTT you need a window of 100 Gbps × 0.13 s ≈ 13 Gb = 1.6 GB — huge windows are why TCP has scaling options (window scale, RFC 7323).

## 9. Internal Working
1. **PAN** (Bluetooth): 2.4 GHz ISM band, frequency-hopping (79 channels, 1600 hops/s), master-slave piconet (up to 7 active slaves), L2CAP/ACL/ALM protocols. Range ~10 m (Class 2). Bluetooth LE uses 40 channels + advertising.
2. **LAN** (Ethernet): hosts ↔ switch over Cat5e/6 twisted pair (100 m limit) or fiber. MAC addressing, CSMA/CD historically, now full-duplex point-to-point. Broadcast domain = LAN (ARP, DHCP broadcast). Routers connect LANs.
3. **MAN** (metro): fiber rings using WDM (multiple wavelengths per fiber, 40-160 ch × 100 Gbps) with SONET/SDH or Ethernet protection switching (~50 ms failover). City offices connect to PoPs via fiber drops.
4. **WAN**: sites connect via leased line (T1/E1, DS3, 100G circuits) or IPsec/MPLS VPN over the Internet. Routers at each site speak BGP/OSPF; traffic transits carrier backbones. Latency = distance/speed-of-light (~5 µs/km in fiber) + switching overhead.
5. **VPN overlay**: a "virtual WAN" — tunnels (IPsec/GRE/WireGuard) ride on top of any physical network, giving private addressing + encryption to remote sites (SD-WAN).

## 10. Time Complexity
- **Propagation latency** = distance / (2×10⁸ m/s in fiber) — O(distance), linear.
- **Speed of light cap**: Earth circumference ~40,000 km → worst-case one-way ~200 ms. This is the hard physical bound on all WAN latency.
- **LAN**: RTT ~ µs-ms (a few km). **WAN**: RTT 20-300 ms. TCP throughput ∝ 1/RTT (halve RTT → double throughput for fixed window).
- **Bandwidth-delay product** (BDP) = RTT × bandwidth — the "pipe size" in bits; governs buffer sizes and TCP windows. Grows linearly in distance; a 100 Gbps × 130 ms link needs ~1.6 GB of in-flight data.

## 11. Advantages
- **PAN**: zero-config, low power, secure pairing (Bluetooth), personal device integration.
- **LAN**: private ownership → control, no metering, very high speed, low latency, easy management, cheap per bit.
- **MAN**: high-capacity metro coverage without long-haul cost; enables city ISPs, campus backbones; ring redundancy.
- **WAN**: global reach; allows enterprises to connect offices worldwide; shared carrier infra amortizes cost.
- **VPN**: security and private addressing over public infra; flexible, cheap "virtual WAN."

## 12. Disadvantages
- **PAN**: tiny range, low throughput, interference on 2.4 GHz, master-slave constraints.
- **LAN**: limited reach (100 m copper, ~fiber segment limits), cabling cost, broadcast scale limits (VLANs needed).
- **MAN**: carrier dependence, rights-of-way, ring failure risk if not dual, cost of metro fiber.
- **WAN**: high latency, high cost per bit, third-party dependence, congestion across shared backbones, physical speed-of-light cap, more failure surface.
- **VPN**: encryption overhead, added latency, tunnel misconfiguration risk, performance dependent on the public underlay.

## 13. Interview Questions
1. **Q: List the network types by size.** A: PAN (1-10 m) → LAN (building/campus, ≤ few km) → MAN (city, 5-50 km) → WAN (global). Plus CAN, SAN, VPN.
2. **Q: Why does a WAN have higher latency than a LAN?** A: Propagation delay = distance/speed-of-signal. Light in fiber ≈ 2×10⁸ m/s, so 1000 km ≈ 5 ms one-way. A WAN spans thousands of km; a LAN spans meters.
3. **Q (tricky): Can a LAN have lower speed than a WAN?** A: Yes. Speed and scope are independent. A congested 100 Mbps LAN is slower than a 10 Gbps dedicated WAN circuit. But *typical* LANs are faster. Also, speed-of-light latency is what you can't buy your way out of on a WAN.
4. **Q: What's the difference between a LAN and a WAN beyond size?** A: Ownership (private vs carrier), technology (Ethernet/Wi-Fi vs leased lines/MPLS), latency budget, error rates (WAN higher), and routing (LAN: default gateway; WAN: full routing protocols).
5. **Q (production): Why is RTT so important in TCP performance?** A: TCP throughput ≈ Window/RTT. Doubling RTT halves throughput at fixed window. The bandwidth-delay product (RTT × BW) determines how much in-flight data the pipe can hold — buffers and windows must be ≥ BDP to saturate a link.
6. **Q: What is a VPN and what does "virtual" mean?** A: A VPN is a logical (virtual) private network built as encrypted tunnels over a public/shared underlay (the Internet). "Virtual" = you get private-address space + encryption without owning the physical links.
7. **Q (scenario): Your company has offices in NYC, London, and Tokyo. Design a WAN.** A: MPLS/VPN or SD-WAN over dedicated circuits; IPsec tunnels; local internet egress at each site; BGP for path selection; possibly a private backbone (like Google's) for critical traffic.
8. **Q: What is a SAN and how is it different from a LAN?** A: A SAN is a high-speed network carrying *block-level storage* traffic (Fibre Channel, iSCSI), not general-purpose user traffic. A LAN carries file/print/web traffic. SANs have dedicated, lossless (priority flow control, DCB) fabrics.
9. **Q (tricky): Is a datacenter a LAN?** A: Roughly — it's a private, high-speed campus-scale network (often called a *datacenter network*). Modern DCs use leaf-spine fabrics and 400G links; they're LAN-scale in distance but engineered like a WAN core in terms of routing (OSPF/BGP/EVPN).
10. **Q: Why is GEO satellite latency ~240-280 ms?** A: GEO orbit ≈ 35,786 km. Uplink+downlink ≈ 2×35,786 km ≈ 71,600 km; at 3×10⁸ m/s that's ≈ 240 ms one-way, ~500 ms RTT. LEO constellations (Starlink, ~550 km) cut this to ~25-40 ms one-way — the reason for LEO's rise.
11. **Q: What is the difference between a PAN and a LAN?** A: Scope (1-10 m vs building), technology (Bluetooth/NFC vs Ethernet/Wi-Fi), and use (personal device pairing vs shared resource access). PANs are ad-hoc and personal; LANs are organizational.
12. **Q: What does "private ownership" mean for a LAN and why does it matter?** A: The org owns the cables/switch — it can run any protocol, any speed, no metering, full QoS control. On a WAN you *rent* capacity from a carrier with SLA terms.
13. **Q (practical): How do you connect two LANs into one network?** A: Via a router (layer 3) — a WAN link or VPN tunnel between the two routers. Simply bridging the LANs (a switch, layer 2) doesn't scale and breaks broadcast domains.
14. **Q: What technologies distinguish a MAN?** A: Metro fiber rings, WDM, Ethernet-over-fiber, cable DOCSIS, WiMAX (legacy). MANs are typically carrier-operated with SLA-based metro Ethernet services.
15. **Q (FAANG): How would you measure the latency between a client and your service?** A: `ping`/ICMP for RTT, TCP connect time (SYN→SYN-ACK), first-byte-to-last-byte (TTFB), and at scale: distributed RUM (real user monitoring) or active probing (like Google's gRPC health checks). Distinguish propagation from queueing/jitter.

## 14. Follow-Up Questions
1. **Q: Why is the bandwidth-delay product important for WAN design?** A: It's the amount of data in flight needed to fill the pipe (bits). If buffers/windows < BDP, the link idles. It drives TCP window sizing, router buffer sizing, and whether you need multiple parallel streams.
2. **Q: Why do metro networks use rings?** A: Fiber is expensive and rights-of-way scarce; a ring lets two fibers serve many sites with 50 ms protection switching on failure. Dual counter-rotating rings give self-healing.
3. **Q: What is the "speed of light problem" for cloud?** A: Physics caps one-way latency at distance/2×10⁸ m/s (fiber) or 3×10⁸ (vacuum). Edge computing (moving compute to the user) exists precisely because you can't beat this — distance is the only lever.
4. **Q: What's the difference between SD-WAN and traditional WAN?** A: SD-WAN uses software control + commodity internet links + tunnels, with centralized policy and dynamic path selection over multiple transports (MPLS + broadband + LTE), vs. static dedicated circuits. Cheaper and more agile.
5. **Q: What is jitter and why does WAN/VoIP care?** A: Variation in packet delay. Voice needs <30 ms jitter typically; WAN queueing creates jitter. Buffers (jitter buffers) smooth it at the cost of added latency.

## 15. Coding Example
```python
import math

C = 2e8  # speed of light in fiber, m/s

def one_way_prop_delay(km):
    return (km * 1000) / C

def rtt(km):
    return 2 * one_way_prop_delay(km)

def bandwidth_delay_product(bw_bps, km):
    return bw_bps * rtt(km)  # bits in flight to fill the pipe

cases = [("LAN", 0.1), ("MAN", 20), ("WAN(NYC-LON)", 5600), ("WAN(round earth)", 20000)]
for name, km in cases:
    print(f"{name:16s} RTT={rtt(km)*1000:8.1f} ms  "
          f"BDP@10Gbps={bandwidth_delay_product(10e9, km)/1e6:10.0f} Mbit "
          f"({bandwidth_delay_product(10e9, km)/8e6:.2f} MB)")
# LAN            RTT=     0.0 ms  BDP@10Gbps=     0 Mbit (0.00 MB)
# MAN            RTT=     0.4 ms  BDP@10Gbps=     4 Mbit (0.50 MB)
# WAN(NYC-LON)   RTT=   112.0 ms  BDP@10Gbps=  1120 Mbit (140.00 MB)
# WAN(round)     RTT=   400.0 ms  BDP@10Gbps=  4000 Mbit (500.00 MB)
```
```
# Practical: measuring RTT (Linux)
$ ping -c 3 8.8.8.8
# round-trip min/avg/max/stddev = 1.234/1.456/1.789/0.100 ms
$ mtr -n 8.8.8.8   # shows per-hop latency along the WAN path (traceroute+ping)
```

## 16. Industry Usage
- **AWS**: Regions = WAN-scale clusters of availability zones (AZs) linked by private fiber (~1-2 ms RTT between AZs in a region); Global Accelerator and CloudFront use Anycast to bring users closer. Data transfer between AZs uses the private backbone, not the public Internet.
- **Google**: B4 — a private WAN backbone that carries all Google internal traffic between DCs over software-defined networking (SDN, OpenFlow); users benefit because Google controls the path.
- **Meta**: connects DCs and PoPs via a global fiber backbone; uses BGP + their own routing and CDN (edge caches) to cut intercontinental latency.
- **Netflix**: Open Connect caches in ISP networks — effectively turning a WAN problem into a LAN problem by pushing content to the edge.
- **Enterprises**: MPLS/VPN/SD-WAN for branch connectivity; SD-WAN (Cisco, VMware, Fortinet) is the modern WAN on-ramp — multi-link, centralized management, app-aware steering.

## 17. References
- Kurose & Ross, *Computer Networking: A Top-Down Approach*, 8th ed., Ch. 1.2 (The Network Edge).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., Ch. 1.2 (Networks).
- Forouzan, *Data Communications and Networking*, 5th ed., Ch. 1 (network categories).
- IEEE 802.11 (Wi-Fi LAN), IEEE 802.3 (Ethernet LAN), IEEE 802.15 (WPAN), IEEE 802.16 (WiMAX MAN).
- RFC 1918 (private addressing), https://www.rfc-editor.org/rfc/rfc1918
- RFC 7323 (TCP Window Scale), https://www.rfc-editor.org/rfc/rfc7323
- Starlink / LEO latency analysis — https://starlink.com / public Kuiper/OneWeb docs.

## 18. Cheat Sheet
- Size ladder: PAN (10 m) → LAN (≤2 km) → MAN (50 km) → WAN (global).
- LAN: private, Ethernet/Wi-Fi, Gbps, sub-ms. WAN: leased lines/MPLS/VPN, 20-300 ms RTT, per-bit cost.
- Propagation ≈ 5 µs per km in fiber (2×10⁸ m/s).
- GEO satellite RTT ≈ 500 ms; LEO ≈ 25-40 ms one-way.
- TCP throughput ≈ Window/RTT; BDP = RTT × BW.
- Datacenter ≈ private LAN-scale fabric; Internet = internetwork, not a WAN.
- VPN = logical private network (tunnels) over a shared underlay.
- CAN = campus; SAN = block-storage network; MAN = metro rings (WDM).

## 19. Quiz
1. Correct size order: a) PAN>LAN>WAN b) LAN>MAN>WAN c) WAN>MAN>LAN>PAN d) MAN>WAN → **c**
2. Bluetooth is a: a) PAN b) LAN c) MAN d) WAN → **a**
3. Propagation delay in fiber per km: a) 5 µs b) 50 µs c) 500 µs d) 5 ms → **a**
4. A VPN is: a) a physical network b) a logical/overlay network c) a protocol for routing d) a cable type → **b**
5. BDP for a 10 Gbps link with 100 ms RTT: a) 1 Mbit b) 100 Mbit c) 1 Gbit d) 100 Gbit → **c** (10e9×0.1 = 1e9)
6. GEO satellite one-way latency ≈: a) 10 ms b) 50 ms c) 240 ms d) 1000 ms → **c**
7. A SAN carries: a) web traffic b) block-level storage c) voice d) broadcast → **b**
8. Which is typically owned by a carrier? a) LAN b) PAN c) WAN links d) home Wi-Fi → **c**
9. Metro networks often use: a) rings b) buses c) full mesh d) no redundancy → **a**
10. Which does NOT grow with distance? a) propagation delay b) BDP c) RTT d) LAN port speed → **d**

## 20. Flashcards
- **Q: Network types in order?** → **A:** PAN → LAN → MAN → WAN.
- **Q: LAN vs WAN ownership?** → **A:** LAN private; WAN carrier/leased.
- **Q: Propagation per km in fiber?** → **A:** ~5 µs/km.
- **Q: TCP throughput formula?** → **A:** Window/RTT.
- **Q: Bandwidth-delay product?** → **A:** RTT × BW (bits in flight to fill the pipe).
- **Q: GEO vs LEO latency?** → **A:** GEO ~240-280 ms one-way; LEO ~25-40 ms.
- **Q: What's a VPN?** → **A:** Encrypted logical overlay/tunnel over shared infra.

## 21. Revision
Networks are classified by scope because distance determines physics, latency, ownership, and tech. PAN (Bluetooth, ~10 m), LAN (Ethernet/Wi-Fi, private, Gbps, sub-ms), MAN (metro fiber rings, 5-50 km), WAN (leased lines/MPLS/VPN, 20-300 ms RTT). Fiber propagation ≈ 5 µs/km; GEO satellites ≈ 500 ms RTT (why LEO wins). TCP throughput ≈ Window/RTT, so BDP = RTT × BW sets window/buffer sizes. The Internet is an internetwork; a datacenter is LAN-scale with WAN-style routing; a VPN is a logical overlay. 

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Types of networks by size?" | 7 Formal Definition / 13 Q&A |
| "Why is WAN latency higher?" | 8 Example / 13 Q&A |
| "Why does RTT matter for TCP performance?" | 8 Example / 10 Time Complexity |
| "What is a VPN?" | 9 Internal Working / 13 Q&A |
| "What is the bandwidth-delay product?" | 10 Time Complexity / Follow-Up |
| "Why GEO satellite is slow / why LEO?" | 13 Q&A / 10 Time Complexity |
| "Design a WAN for a company." | 13 Q&A / 16 Industry Usage |
