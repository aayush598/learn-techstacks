# Chapter: MAC and Access Control

## What you'll learn
- How hardware addressing works: the 48-bit MAC address format, unicast/multicast/broadcast bits, OUI allocation, and how ARP (RFC 826) maps IP → MAC, plus RARP/GARP and ARP security.
- How flow control paces senders at L2: Stop-and-Wait, Go-Back-N, and Selective Repeat, with utilization math you can compute in an interview.
- How shared media are arbitrated: ALOHA → slotted ALOHA → CSMA → CSMA/CD (Ethernet) and CSMA/CA (WiFi), including the 512-bit collision-window math.
- Ethernet in depth: the exact frame bytes, preamble/SFD, min/max frame sizes, 802.3 vs 802.2/LLC, and full-duplex evolution.
- WiFi (IEEE 802.11) in depth: DCF/CSMA/CA, RTS/CTS, frame formats, 802.11a/b/g/n/ac/ax/be differences.
- How L2 networks scale: transparent bridging, VLAN tagging (802.1Q), and Spanning Tree Protocol (802.1D) root-bridge election and loop prevention.

## Prerequisites (linked)
- [Chapter 01 — Data Link Fundamentals](../chapter-01-data-link-fundamentals/README.md): framing and error control give you the frame structure and CRC that every protocol here carries.
- Part 04 (Network Layer): ARP exists to bridge IP (L3) and MAC (L2); know IPv4/IPv6 basics first.
- Basic familiarity with the OSI model ([Part 01](../part-01-network-fundamentals/chapter-02-osi-and-tcp-ip-models/README.md)).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — MAC Addresses and Address Resolution](section-01-mac-addresses-and-address-resolution.md) | 48-bit MAC structure, OUI, unicast/multicast/broadcast, ARP/RARP/GARP packet walk, ARP cache, spoofing |
| [Section 02 — Flow Control: Stop-and-Wait, Go-Back-N, Selective Repeat](section-02-flow-control-stop-and-wait-go-back-n-selective-repeat.md) | Reliability + rate matching via windows; utilization formulas; sequence-number vs window-size constraints |
| [Section 03 — Multiple Access Protocols: ALOHA, CSMA, CSMA/CD](section-03-multiple-access-protocols-aloha-csma-csmacd.md) | Random access on shared media; throughput (1/2e, 1/e); collision detection, backoff, the 512-bit slot |
| [Section 04 — Ethernet in Depth](section-04-ethernet-in-depth.md) | Byte-level frame anatomy, EtherType vs length, minimum/maximum frames, duplex modes, cabling, real header hex dump |
| [Section 05 — WiFi and IEEE 802.11](section-05-wifi-and-ieee-802-11.md) | Wireless MAC: CSMA/CA, DCF/PCF, RTS/CTS, frame formats, a/b/g/n/ac/ax/be, security (WPA3/802.1X) |
| [Section 06 — Switching, VLAN, and STP](section-06-switching-vlan-and-stp.md) | Transparent learning bridges, MAC tables, 802.1Q VLAN tagging, trunking, STP/RSTP loop prevention, root bridge election |

## One-paragraph narrative connecting all sections
Every frame on a LAN must be addressed and admitted to the medium. Section 01 explains the address that frames carry — the 48-bit MAC — and how end hosts map the L3 address they care about (IP) to the L2 address the switch/Ethernet needs (ARP). Section 02 then shows how a sender paced by flow control can be reliable without flooding the receiver: Stop-and-Wait is simple but idle, and windowed schemes (Go-Back-N, Selective Repeat) fill the pipe — a theme TCP re-implements at L4. Because classic LANs share one wire, Section 03 covers *who gets to talk*: ALOHA's 18% efficiency, CSMA's listen-before-talk, and CSMA/CD's collision-detect-and-backoff that made 10 Mb/s Ethernet work; WiFi's half-duplex radio then forces CSMA/CA (Section 05). Section 04 nails down the exact Ethernet frame bytes and how 802.3 + full-duplex replaced shared-wire CSMA/CD at scale. Finally, Section 06 shows how real networks are actually built: switches learn MACs, VLANs segment broadcast domains with a 4-byte 802.1Q tag, and STP removes the loops that redundant cabling creates.

## Common interview trap in this chapter
1. **ARP vs DNS**: ARP maps L3 (IP) → L2 (MAC) on a *local* link; DNS maps names → IP *globally*. Mixing them up is an instant fail.
2. **CSMA/CD vs CSMA/CA**: Ethernet detects collisions *during* transmission (full duplex, no longer needed); WiFi *avoids* collisions before transmitting (can't detect while transmitting). Saying "WiFi uses CSMA/CD" is wrong.
3. **Stop-and-Wait utilization**: forgetting the factor of 2 for RTT (transmit time / (transmit + 2·propagation)) loses marks; also, window size must be ≤ 2^N − 1 for GBN, not 2^N.
4. **MAC addresses**: 48 bits, expressed as 12 hex digits, first 3 bytes = OUI, I/G bit is the *LSB of the first byte*; broadcast = all 0xFF. Also MAC addresses are *flat* (no hierarchy) — routing is impossible, only switching.
5. **VLAN tag**: inserted *after* the source MAC and *before* the EtherType, which becomes 0x8100; it's 4 bytes, not 2.

## Checklist before moving on
- [ ] I can decode a MAC address (OUI, I/G bit, unicast/multicast/broadcast) and explain why MACs are flat and unrouteable.
- [ ] I can walk an ARP request/reply packet byte by byte and explain GARP and ARP spoofing.
- [ ] I can compute Stop-and-Wait and GBN utilization given bandwidth, RTT, and frame size, and state the window/sequence-number constraint.
- [ ] I can derive ALOHA (1/2e), slotted ALOHA (1/e), and explain the 512-bit Ethernet collision window.
- [ ] I can lay out an Ethernet II frame byte by byte, including 802.1Q-tagged frames, and state min/max sizes.
- [ ] I can explain why WiFi uses CSMA/CA + RTS/CTS and how 802.11 retransmission works.
- [ ] I can explain how a switch learns MACs, how a VLAN tag is used, and how STP elects the root bridge and blocks ports.
