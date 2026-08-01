# Ethernet in Depth

> **TL;DR**: Ethernet (IEEE 802.3) is the dominant Layer 2 technology — a frame format (preamble/SFD + MACs + type + payload + FCS) and a MAC protocol that runs at 10 Mb/s to 400 Gb/s over copper and fiber, evolving from a shared CSMA/CD bus to full-duplex switched point-to-point links while keeping one backward-compatible frame layout.

## 1. Why Does This Exist?
In 1973 Bob Metcalfe needed a cheap, scalable way to connect Xerox's office computers and printers on one cable. Ethernet's bet was *simplicity over guarantees*: a single shared medium, carrier-sense with collision detection, and a fixed frame format — no fancy token passing, no central controller. That bet won because Ethernet (a) is **cheap** — commodity silicon, unshielded twisted pair, no licensing; (b) **scales** — from 2.94 Mb/s coax to 400 Gb/s per lane; (c) **is simple enough to keep compatibility** — the 1973 frame is byte-compatible with today's 802.3 frame; (d) **never trusted the wire** — with reliable upper layers (TCP) and an ever-cleaner medium, detect-and-drop beats elaborate L2 reliability. Ethernet exists because LANs needed a standard everyone could build to, and standardization — IEEE 802.3 — turned a research hack into the world's universal LAN/DC fabric.

## 2. How Does It Work?
A NIC encapsulates an IP packet (payload) in an **Ethernet frame**: Preamble (7 bytes) + SFD (1 byte) for clock sync; Destination MAC (6) + Source MAC (6); an EtherType (2 bytes, e.g., `0x0800` IPv4, `0x86DD` IPv6, `0x8100` VLAN) or a length (802.3 frame); the payload (46–1500 bytes); and a 4-byte FCS (CRC-32) trailer. The NIC's MAC sublayer enforces access: legacy shared-media used CSMA/CD; modern full-duplex links just transmit and rely on the switch. The receiver locks on the SFD, reads the MACs (filtering unicast/multicast/broadcast), checks CRC-32, and delivers the payload to IP. Everything above the FCS is the NIC's job — hardware framing at line rate.

## 3. When Is It Used?
- **Everywhere**: home LANs, office floors, data-center racks, ISP access (EPON/GPON transport IPoE), storage fabrics (iSCSI/NVMe-oF), metro/backbone links.
- **All modern speeds**: 100 Mb/s, 1 GbE, 10/25/40/100/200/400 GbE; single-pair automotive Ethernet (100BASE-T1) in cars.
- **As the physical layer for higher-layer protocols**: PPPoE over Ethernet (DSL), IP over Ethernet for everything IP, VXLAN/Geneve overlays encapsulate L2-in-L3 over Ethernet fabrics.
- **Time-Sensitive Networking (TSN)**: 802.1Qbv scheduled traffic, 802.1Qbu frame preemption for industrial/AVB real-time on Ethernet.
- **Anywhere you need *predictable, line-rate, cheap* framing** — which is nearly all of networking outside radio.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: Token Ring (IBM, IEEE 802.5).* Deterministic (no collisions, latency-bounded) but a single point of failure (broken ring/token), complex, expensive, and slower to evolve; Ethernet's stateless CSMA/CD was cheaper and "good enough," and its failure modes degrade gracefully.
- *Alternative: FDDI (100 Mb/s fiber token ring).* Same token determinism appeal, but expensive and niche; Ethernet ate it via copper 100BASE-TX + later fiber Fast/Gigabit.
- *Alternative: reliable L2 with retransmission (like HDLC).* Ethernet chose detect-and-drop, pushing reliability to TCP — dramatically simpler silicon (no ACK state, no sequence numbers, no timers) and perfectly adequate on clean links. WiFi, where the medium is lossy, *did* add L2 ACKs (802.11), proving the design is a per-medium choice.
- *Alternative: keep CSMA/CD forever.* Impossible at scale — shared media don't scale past ~100 Mb/s and collide-bound distances; full-duplex switched Ethernet (1997, 802.3x) removed the shared medium entirely, turning Ethernet into a simple point-to-point framing + flow-control layer.
- *Alternative: a fully centralized LAN (ATM).* ATM (53-byte cells, per-VC QoS) promised telco-grade guarantees but was complex and died; Ethernet won on cost, simplicity, and speed of innovation. The lesson: *good enough and universal beats perfect and proprietary*.

## 5. Intuition
An Ethernet frame is a **postcard**: a fixed-length header with a "to" address, a "from" address, a label saying what kind of content follows (type field), the message, and a check digit. The NIC is the postal clerk who writes the addresses, sums the check digit, and drops the postcard into the mail slot (medium). Switches are sorting machines: they read only the "to" address and hand the card to the right port. The preamble is the mail truck's "beep-beep" that lets the sorting machine sync its clock to the truck's pace. Because a postcard has a maximum size (1500 bytes payload), big letters must be torn into multiple postcards (IP fragmentation — though TCP MSS usually avoids that).

## 6. Real-World Analogy
A **highway with lanes and exit ramps**: frames are cars; the preamble/SFD is the driver syncing to the road markings; the destination MAC is the exit ramp; source MAC is the entrance; the EtherType is the cargo manifest (are you carrying passengers or freight — IPv4 or IPv6 or VLAN?); the payload is the cargo; the FCS is the weigh-station check that catches damaged cars. Switches are interchange hubs that read only the "exit" sign and route the car to the right ramp without ever reading the cargo manifest.

## 7. Formal Definition
Ethernet is a family of L2 LAN standards defined by IEEE 802.3 (originally DIX Ethernet — DEC, Intel, Xerox, 1980). The **Ethernet II (DIX) frame**: Preamble (7 × 0x55, 56 bits of alternating 1/0 for receiver clock sync) + SFD (0xD5, `10101011`) + Destination MAC (6 octets) + Source MAC (6 octets) + EtherType/Length (2 octets) + Payload (46–1500 octets) + FCS (4 octets CRC-32). Total 64–1518 bytes (add 4 bytes for an 802.1Q VLAN tag → 68–1522; add 8 for the preamble/SFD). The **802.3 frame** differs by using a Length field with an LLC sublayer (802.2) instead of EtherType; values > 0x0600 are EtherType (type field), values ≤ 0x05DC are length — the two formats are distinguished by the field value. Minimum inter-frame gap (IFG) = 96 bit-times; full-duplex (802.3x) uses PAUSE flow control; auto-negotiation (802.3ab/clause 28) selects speed/duplex.

## 8. Example
A minimal **Ethernet II frame carrying 46 bytes of IPv4 payload** (the shortest legal frame), byte by byte:
```
Preamble:     55 55 55 55 55 55 55      (7 bytes, physical)
SFD:          D5                       (1 byte)
Dest MAC:     AA BB CC DD EE 01
Src MAC:      11 22 33 44 55 66
EtherType:    08 00                   (IPv4)
Payload:      45 00 00 2C ...          (46 bytes: IPv4 header + data)
FCS:          0C 1B 2A 3D             (CRC-32, any 4 bytes here)
```
Total on wire: 7+1+6+6+2+46+4 = 72 bytes (64-byte frame + 8-byte preamble). The receiver: NIC locks to preamble, reads `AA BB CC DD EE 01` (matches its MAC → keep), computes CRC-32 over the 64 frame bytes and compares with the FCS → match → strips header/trailer and hands 46 bytes to IP via EtherType `0x0800`.

## 9. Internal Working
1. **Transmit**: OS passes `sk_buff` → driver builds frame (adds MACs, EtherType, FCS in hardware via DMA descriptors) → MAC sublayer enforces min gap/backoff if needed → PHY serializes bits (PCS encodes — 4B5B for 100BASE-TX, 8B10B for 1G, 64B66B for 10G+).
2. **Receive**: PHY recovers clock → NIC checks dest MAC against its filter (unicast match, or multicast hash/broadcast accept, or promiscuous) → computes CRC → on pass, DMAs frame into a ring of descriptors and raises an interrupt / NAPI polling → kernel parses EtherType to dispatch (IP, ARP, VLAN, etc.).
3. **Flow control (full duplex)**: if the receive ring overflows, the NIC sends a PAUSE frame (802.3x) telling the peer to hold off for X quanta — receiver-driven flow control at the link (rarely used at DC scale because it head-of-line-blocks; DCs prefer ECN/PFC).
4. **Jumbo frames**: payloads up to ~9000 bytes (needs MTU 9000 + `ip link set mtu 9000` on *all* path devices + switch ports) — increases efficiency for large transfers, breaks if any hop caps at 1500.
5. **Offloads**: TSO/GSO (TCP segmentation offload — the NIC splits a 64 KB TCP segment into 1500-byte frames), GRO (reassembly on receive), checksum offload, RSS (receive-side scaling across queues) — these make Ethernet *line-rate* practical.
6. **Errors**: CRC error → drop + counter; alignment/runts (shorter than 64) → drop; oversize >1522 → drop; all counted in `ethtool -S`.

## 10. Time Complexity / Performance
- **Line rate**: a 10 GbE link is ~14.88 M frames/sec at minimum 64-byte frames → ~67 ns/frame budget; NIC pipelines handle this in hardware.
- **Framing**: O(1) per frame — fixed header/trailer work regardless of payload.
- **CRC**: O(n) in frame size but silicon-parallel → ~1 cycle/byte with lookahead.
- **Offloads**: TSO turns O(n) software segmentation into O(1) NIC work → this is why kernel throughput scales to hundreds of Gbps with fast paths.
- **Frame-rate math to know**: line_rate / (8 × (64+20)) = max FPS (20 bytes = preamble+IFG); 10 GbE → 10×10⁹/(8×84) ≈ 14.88 Mpps.

## 11. Advantages
- **Universal and interoperable**: one frame format across 40 years, every vendor, every speed — huge ecosystem, commoditized silicon.
- **Cheap**: twisted pair + commodity ASICs; cabling options from Cat5e to single-mode fiber.
- **Fast**: line-rate framing in silicon; offloads push the OS out of the data path.
- **Simple MAC**: no token/controller state; full-duplex needs almost no access logic.
- **Scales**: 10 Mb/s → 400 Gb/s with the same frame; link aggregation (LACP) and multi-lane (25×N) packaging.
- **Debuggable**: `tcpdump -e`, `ethtool -S`, switch counters expose every layer of the frame.

## 12. Disadvantages
- **No L2 reliability**: drops on CRC error silently — depends on TCP; unsuitable without an upper reliable layer.
- **Frame-size ceiling**: 1500-byte MTU wastes up to ~1.7% on headers for small packets (fine at large scale but real on 64-byte-heavy workloads); jumbo frames fragment the ecosystem.
- **Flat addressing**: 48-bit MACs don't scale to huge flat LANs (hence VLANs/overlays); MAC-table flooding attacks.
- **Half-duplex legacy**: shared-media mode is slow and distance-limited; all modern deployments are full-duplex, so CSMA/CD is dead weight in the spec.
- **Not QoE-guaranteed**: best-effort delivery; QoS needs TSN/802.1Q priorities layered on top.
- **Broadcast storms**: without STP (Section 06) or storm control, a loop can flood the LAN with broadcast frames.

## 13. Interview Questions
1. **Q: Lay out an Ethernet II frame byte by byte.** A: Preamble 7×0x55, SFD 0xD5, Dest MAC 6, Src MAC 6, EtherType 2 (e.g. 0x0800), Payload 46–1500, FCS 4 (CRC-32). Minimum 64 bytes (frame only), maximum 1518; with VLAN tag 68–1522; with preamble 72/1526 on the wire.

2. **Q: What's the difference between Ethernet II and IEEE 802.3 frames?** A: Ethernet II uses a 2-byte EtherType field; 802.3 uses a 2-byte Length field plus an 802.2 LLC header. You can tell them apart by value: ≤0x05DC = length (802.3), ≥0x0600 = type (Ethernet II). In practice Ethernet II dominates; 802.3+LLC is legacy/PPPoE-era.

3. **Q: Why is the preamble separate from the frame?** A: The 56-bit alternating pattern synchronizes the receiver's clock to the sender's bit timing (clock/data recovery); the SFD (`10101011`) marks the last preamble bit and the start of frame data. Neither counts toward the 64-byte minimum or the FCS.

4. **Q: What is the minimum and maximum Ethernet frame size and why?** A: Min 64 bytes (46 payload) — so CSMA/CD collision detection works (sender still transmitting when its collision returns = 512-bit slot). Max 1518 (1500 payload) — bounds latency, receive buffers, and CRC sensitivity on a shared medium. Both persist in full-duplex Ethernet for compatibility.

5. **Q: What does EtherType `0x8100` mean?** A: A VLAN tag follows: the tag's first 2 bytes are TPID `0x8100`, next 2 bytes are priority (3 bits) + DEI + VID (12 bits); the *real* EtherType comes after the 4-byte tag. Frame grows by 4 bytes; max becomes 1522.

6. **Q: TRICKY — Why is the FCS not part of the payload and how is it validated?** A: The CRC-32 is computed over dest MAC through payload (not the preamble — those bytes aren't counted). The receiver recomputes over the received frame bytes; a match means "valid with probability ~1−2⁻³²." The FCS is the trailer precisely so the whole frame can be validated in one pass.

7. **Q: PRODUCTION — How does TSO/GRO make Ethernet fast?** A: TSO lets the stack hand the NIC a 64 KB TCP segment and the NIC splits it into 1500-byte frames in hardware, generating headers + CRCs itself — the OS does O(1) work per large send. GRO reverses it on receive (merge frames before IP). This is why Linux can push tens of Gbps without per-frame syscalls.

8. **Q: SCENARIO — `ethtool -S eth0` shows `rx_crc_errors` increasing but the link is "up." What's wrong?** A: Physical-layer issues — bad SFP/optics, dirty/damaged fiber, poor cable, marginal connector, or duplex/speed mismatch; also possible: NIC/driver bugs with offloads, or a faulty transceiver on the far end. Check optics power (`ethtool -m`), swap cables/ports, verify auto-negotiation, then isolate to the NIC.

9. **Q: What is auto-negotiation and why does it matter?** A: 802.3 clause 28: link partners exchange ability "words" (clocks/signals) and agree on the best common speed+duplex. A mismatch (one side forced, other auto) causes *duplex mismatch* → late collisions, terrible throughput — a classic production outage cause. Always let both ends auto-negotiate.

10. **Q: What is a jumbo frame and when is it useful?** A: Payload up to ~9000 bytes with MTU 9000 — fewer frames/headers for big transfers (higher efficiency, less CPU). Useful on closed, controlled paths (DC, storage, backup). Fragile: any hop at 1500 silently fragments or drops (needs `ip link set mtu 9000` + matching switch ports + proper `df` handling).

11. **Q: TRICKY — Why can't you just set MTU 9000 and forget it?** A: Every hop on the path (host NIC, switch ports, L3 devices, sometimes load balancers) must run MTU 9000; a single 1500 hop forces fragmentation (bad for TCP — fragments dropped by many middleboxes) or black-holing. This is why DCs run a "jumbo everywhere" or "1500 everywhere" policy, never a mix.

12. **Q: What is the PAUSE frame and why do data centers disable it?** A: 802.3x flow control: a receiver sends PAUSE to stop a sender's transmission. It works but *head-of-line blocks* the whole link (not per-flow), so DCs prefer ECN + PFC (Priority Flow Control, per-priority pause) and lossless Ethernet for RoCE — still hotly debated.

13. **Q: SCENARIO — Frames with a valid FCS arrive at the switch but get dropped. Why?** A: Layer 3+ reasons the switch doesn't act on: the dest MAC is unknown and the port's MAC table is full (flood policy), the frame is filtered by a port ACL, storm control limits broadcast/multicast, or the ingress/egress MTU is smaller. FCS-valid does not mean the switch forwards it.

14. **Q: What's the maximum frames-per-second on a 10 GbE link with 64-byte frames?** A: Each frame occupies 64 + 20 (preamble+SFD+IFG) = 84 bytes on the wire → 10×10⁹/(8×84) ≈ 14.88 Mpps. This is the "packet rate problem": 10G line rate at min frames needs ~67 ns per frame — why NICs have multiple queues and offloads.

15. **Q: Why is Ethernet called a "best-effort" L2?** A: It provides framing + error detection + (full-duplex) flow control, but no ACK and no retransmission — a frame dropped on CRC error is simply gone. Reliability is delegated to TCP. Compare WiFi (802.11) which ACKs and retransmits at L2.

16. **Q: TRICKY — Why did Fast Ethernet cap the collision domain at ~200 m while 10BASE-T allowed 2.5 km?** A: The 512-bit slot time must cover 2× worst-case propagation. At 100 Mb/s, 512 bits = 5.12 µs → ~200 m max. Speed up ⇒ diameter shrinks; that's why Gigabit uses full-duplex or carrier extension and why 10 GbE+ is full-duplex-only (no shared-medium mode exists).

17. **Q: What are the differences between 100BASE-TX, 1000BASE-T, and 10GBASE-T?** A: 100BASE-TX: 2 pairs Cat5, 4B5B+MLT-3; 1000BASE-T: 4 pairs Cat5e, PAM-5, echo cancellation on all pairs; 10GBASE-T: Cat6a, PAM-16, heavy DSP (high power). Short reach dominates: SFP+/DAC for 10G in DCs because optical/DAC is cheaper and cooler.

18. **Q: PRODUCTION — A 10G host shows low throughput. List the top-5 non-obvious causes.** A: (1) RSS queue imbalance (single queue saturated); (2) TSO/GRO/checksum offload disabled; (3) interrupt coalescing too aggressive; (4) bufferbloat / `net.core.rmem_max` too small for high BDP; (5) a 1500-MTU bottleneck hop forcing segmentation or drops. Check `ethtool -l`, `-k`, `ss -tin`, and `ip -s link`.

## 14. Follow-Up Questions
1. **Q: Why does the SFD end with `11`?** A: The 7 preamble bytes are `10101010`×7; the SFD is `10101011` — the final `11` is the "last bit before data" marker so the receiver knows where byte alignment begins.

2. **Q: What is the minimum inter-frame gap (IFG) and why?** A: 96 bit-times between frames so the receiver's hardware (FIFOs, DMA) can finish one frame before the next; shrinking it violates spec and causes dropped frames on some NICs.

3. **Q: How does a switch distinguish a VLAN-tagged frame's real EtherType?** A: The 4-byte 802.1Q tag carries TPID 0x8100; the byte *after* the VID is the real EtherType (0x0800, 0x86DD, 0x0806…), so the switch strips the tag before forwarding into the untagged VLAN.

4. **Q: What happens to broadcast frames at a switch?** A: They're flooded out every port (except ingress) in the VLAN — that's how ARP reaches everyone — which is why broadcast storms and loops (STP, Section 06) matter so much.

## 15. Coding Example
```python
import struct, zlib

def build_eth_frame(dst, src, ethertype, payload: bytes) -> bytes:
    """Assemble an Ethernet II frame with CRC-32 FCS (bytes on the wire, no preamble)."""
    assert 46 <= len(payload) <= 1500
    eth = bytes.fromhex(dst.replace(":", "")) + bytes.fromhex(src.replace(":", ""))
    eth += struct.pack("!H", ethertype) + payload
    fcs = zlib.crc32(eth) & 0xffffffff
    return eth + struct.pack("!I", fcs)

def parse_eth_frame(frame: bytes) -> dict:
    dst, src = frame[0:6].hex(":"), frame[6:12].hex(":")
    etype = int.from_bytes(frame[12:14], "big")
    payload, fcs = frame[14:-4], frame[-4:]
    ok = (zlib.crc32(frame[:-4]) & 0xffffffff) == int.from_bytes(fcs, "big")
    return {"dst": dst, "src": src, "ethertype": hex(etype),
            "payload_len": len(payload), "fcs_valid": ok}

frame = build_eth_frame("aa:bb:cc:dd:ee:01", "11:22:33:44:55:66", 0x0800, b"\x45\x00" + b"\x00"*44)
print(parse_eth_frame(frame))
print(f"total frame bytes: {len(frame)} (should be 64)")
```
```bash
# See raw Ethernet frames
sudo tcpdump -i eth0 -e -nn -c 5                       # -e prints MACs + EtherType
sudo tcpdump -i eth0 -xx -c 1                          # hex dump of one frame
sudo ethtool -S eth0 | grep -Ei "crc|runt|oversize|collision"   # frame-level errors
sudo ethtool -k eth0 | grep -E "tcp-segmentation-offload|rx-checksumming"  # offloads
sudo ethtool -l eth0                                    # RSS queue count
ip link show eth0 | head -1                             # MTU, MAC, state
```

## 16. Industry Usage
- **Every data center**: 100G/400G Ethernet is the fabric backbone; 25G leaf links; DCs run lossless Ethernet (PFC) or RoCEv2 for storage/ML (NVIDIA/Meta/AWS topologies are 100% Ethernet).
- **Cloud**: AWS/GCP/Azure VPCs are built on Ethernet fabrics (custom switches, e.g., Amazon's, Juniper, Arista, Cisco); tenant isolation via VLAN/VXLAN over Ethernet.
- **Content/CDN edge**: Cloudflare/Fastly/Google serve TLS over Ethernet-attached servers; load balancers forward frames at line rate.
- **Consumer**: every home router/switch/modem speaks 802.3; GPON/EPON carry Ethernet frames to the premises.
- **Linux networking**: the entire stack is Ethernet-first (`net_device`, `sk_buff`, `ethtool`, `ip link`); XDP/DPDK drop or rewrite frames before the kernel; NIC vendors (Intel/AMD/Mellanox/Netronome) ship 100-400G NICs with full offload.

## 17. References
- IEEE Std 802.3-2022 (Ethernet) — https://standards.ieee.org/ieee/802.3/10422/
- R. Metcalfe & D. Boggs, "Ethernet: Distributed Packet Switching for Local Computer Networks," CACM 19(7), 1976.
- RFC 894 (IP over Ethernet) — https://datatracker.ietf.org/doc/html/rfc894
- Kurose & Ross, *Computer Networking*, 8th ed., §6.4 (Ethernet).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §4.2 (Ethernet) — full frame/medium details.
- Linux kernel docs: `Documentation/networking/ethtool-netlink.rst` — https://docs.kernel.org/networking/ethtool-netlink.html

## 18. Cheat Sheet
- Frame: Preamble 7×0x55, SFD 0xD5, DstMAC 6, SrcMAC 6, Type 2, Payload 46–1500, FCS 4.
- Min 64 B / Max 1518 B; +4 for VLAN (68/1522); preamble+IFG add 20 on the wire.
- EtherType: 0x0800 IPv4, 0x86DD IPv6, 0x0806 ARP, 0x8100 VLAN.
- Ethernet II = type field; 802.3 = length field (value ≤0x05DC).
- FCS = CRC-32 over dst→payload, checked in NIC silicon; miss ~2⁻³².
- Full duplex = no CSMA/CD, PAUSE flow control, no collisions.
- Min frame 64 B ← 512-bit slot for collision detection.
- 10 GbE min-frames ≈ 14.88 Mpps (84 B/frame incl. preamble+IFG).
- Offloads: TSO/GRO/checksum/RSS make line rate practical.
- Duplex mismatch → late collisions → terrible throughput.

## 19. Quiz
1. Preamble length and bytes: a) 7×0x55 b) 7×0xD5 c) 8×0x55 d) 4×0x55 → **a**
2. Ethernet II minimum frame size: a) 46 B b) 64 B c) 1500 B d) 128 B → **b**
3. EtherType for IPv4: a) 0x0806 b) 0x8100 c) 0x0800 d) 0x86DD → **c**
4. The FCS is: a) CRC-16 b) checksum c) CRC-32 d) parity → **c**
5. A value of 0x0500 in the type/length field means: a) IP b) length (802.3) c) ARP d) VLAN → **b**
6. Full-duplex Ethernet uses which flow control? a) CSMA/CD b) PAUSE c) sliding window d) backpressure → **b**
7. Max frames/sec on 10 GbE at 64 B frames ≈: a) 1.49 M b) 14.88 M c) 148 M d) 1.4 M → **b**
8. Which adds 4 bytes to a frame? a) SFD b) VLAN tag c) preamble d) LLC → **b**

**Answers**: 1-a, 2-b, 3-c, 4-c, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: Ethernet II frame layout?** → **A:** Preamble+SFD | DstMAC | SrcMAC | Type | Payload | FCS(CRC-32).
- **Q: Min/max frame sizes?** → **A:** 64/1518 B; VLAN-tagged 68/1522; +20 B preamble/IFG on wire.
- **Q: How to tell Ethernet II from 802.3?** → **A:** Type field >0x0600 = EtherType; ≤0x05DC = length.
- **Q: What's in the preamble/SFD for?** → **A:** Receiver clock sync + start-of-frame marker; not counted in the frame.
- **Q: Why 64-byte minimum?** → **A:** 512-bit slot time for CSMA/CD collision detection.
- **Q: What does PAUSE do?** → **A:** 802.3x flow control — receiver tells sender to pause; head-of-line blocks (hence PFC).
- **Q: Why is modern Ethernet full duplex?** → **A:** Switched point-to-point links have no shared medium → no collisions → no CSMA/CD.

## 21. Revision
Ethernet (IEEE 802.3) is the universal L2: a frame of Preamble(7×0x55)+SFD(0xD5)+DstMAC+SrcMAC+EtherType+Payload(46–1500)+FCS(CRC-32), sized 64–1518 bytes. The EtherType tells the receiver what follows (0x0800 IPv4, 0x86DD IPv6, 0x8100 VLAN); the FCS is checked in NIC silicon. Modern Ethernet is full-duplex switched point-to-point (no CSMA/CD, PAUSE-based flow control), and the 64-byte minimum survives from the shared-medium slot time. Offloads (TSO/GRO/checksum/RSS) are why Linux can push tens of Gbps; 10 GbE at min frames is ~14.88 Mpps. EtherType-vs-length distinguishes Ethernet II from 802.3; the VLAN tag adds 4 bytes before the type; jumbo frames (MTU 9000) need every hop aligned. Anchor: *frame = envelope; FCS = CRC-32; switch reads only MACs; everything past the FCS is NIC hardware.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Lay out the Ethernet frame" | 7 / 13-Q1 |
| "Ethernet II vs 802.3 frame" | 13-Q2 / 7 |
| "Why the preamble/SFD?" | 13-Q3 |
| "Why min 64 / max 1518?" | 13-Q4 |
| "What does 0x8100 mean / VLAN tag?" | 13-Q5 |
| "How is the FCS validated?" | 13-Q6 |
| "How do TSO/GRO speed things up?" | 13-Q7 |
| "rx_crc_errors rising — diagnose" | 13-Q8 |
| "Duplex mismatch / auto-negotiation" | 13-Q9 / 14 |
| "Max frames per second on 10G?" | 13-Q14 |
