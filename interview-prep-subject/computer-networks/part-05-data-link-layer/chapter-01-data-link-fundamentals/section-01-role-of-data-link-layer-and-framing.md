# Role of the Data Link Layer and Framing

> **TL;DR**: The data link layer (Layer 2) converts an unreliable stream of raw bits into structured, error-checked *frames* that travel over one physical link, using three mechanisms — framing (delimiting), error control (detection/correction), and flow control (rate matching).

## 1. Why Does This Exist?
The Physical layer (Part 06) delivers a raw bit pipe: a continuous, undifferentiated sequence of bits that can be flipped by noise, lose bits, or add phantom bits. A receiver looking at that stream cannot tell where one unit of data ends and the next begins, cannot know if the bits it received are the bits that were sent, and cannot slow the sender down if it is swamped. The data link layer exists to solve exactly these three problems on a *single hop*: it wraps raw bits into **frames** (structure), attaches redundant bits so corruption is *detectable* (error control), and paces the sender (flow control). It exists because networks are built by concatenating many unreliable point-to-point links, and every one of those links must be made trustworthy before higher layers (IP, TCP) can assume anything about the path.

## 2. How Does It Work?
The sender's data link layer takes an IP packet (the payload) and encapsulates it in a **frame**: a header (addressing/control fields) + payload + a trailer (error-detection bits, e.g., CRC). It then transmits the frame's bits onto the physical medium. The receiver's data link layer reads the stream, *finds* frame boundaries, checks the error-detection field, and — if valid — strips the header/trailer and hands the payload up to the network layer. If invalid, the frame is dropped (or corrected, if error-correction coding is used). The layer is implemented in firmware/hardware on the **NIC (Network Interface Card)** for the common case, which is why it is extremely fast — the OS is mostly bypassed except for queueing and protocol handling.

## 3. When Is It Used?
- On **every packet you send**: Ethernet frames over a LAN, WiFi frames over the air, PPP frames over a dialup/broadband link, VLAN-tagged frames in data centers.
- **Anywhere a point-to-point or broadcast link needs reliability**: leased lines between routers, DOCSIS cable access, cellular backhaul, data-center top-of-rack links.
- In **switches and bridges**: they are pure Layer 2 devices that forward *frames*, not IP packets — they read only the MAC header.
- In **WiFi**: the 802.11 frame adds a *Frame Check Sequence* (CRC-32) and is retransmitted on failure because the air medium is so lossy.
- In **tunnels and VPNs**: protocols like PPPoE and VLAN tagging still use framing as the transport primitive over the new medium.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: put framing/reliability in the network layer instead.* Rejected because an IP packet often traverses many heterogeneous links, each with different error characteristics; reliability must be *per-link*, where the error actually occurs, so each hop can detect and drop bad frames cheaply and the endpoint sees a clean pipe. This is the "hop-by-hop vs end-to-end" design debate resolved by layering.
- *Alternative: skip framing and just send IP packets back-to-back.* Rejected because then a lost bit or a burst of noise would cause the receiver to misinterpret the *next* packet's boundaries, corrupting an arbitrarily long run of data. Framing gives the receiver a resync point.
- *Alternative: no error detection at all.* Rejected because corruption is not rare — on noisy media (WiFi, cellular) bit error rates of 10⁻⁴–10⁻⁶ are common, and silent corruption of, say, a financial transaction is unacceptable.
- *Alternative: make every link fully reliable with retransmission (reliable link layer).* Rejected as over-engineering for wired links (Ethernet does NOT retransmit — it just detects and drops, leaving retransmission to TCP). The "error control" choice is a cost/benefit: wired links are clean enough that detection-only is optimal; wireless adds retransmission.

## 5. Intuition
A frame is a **letter in an envelope**. The letter (IP packet) is written by a higher layer. The data link layer is the postal clerk who puts it in an envelope, writes the sender/receiver addresses on the front, puts a checksum on the back, and hands it to the courier (physical layer). The courier moves envelopes, not letters. The clerk at the destination opens the envelope, verifies the checksum, and forwards the letter upstairs. If the checksum fails, the envelope is thrown away — the sender's clerk will notice the missing acknowledgment and resend. The entire game is about making sure that when an envelope arrives, the receiver can tell (a) where it starts and ends, (b) that it wasn't damaged.

## 6. Real-World Analogy
Think of **numbered shipping containers on a cargo train**. Containers (frames) are discrete, numbered, have manifest tags (headers), and a total weight/seal (checksum). The train is the physical medium moving all containers as one stream. If a container is damaged in transit, the receiving yard detects it by the broken seal and the manifest — it doesn't try to guess what was inside; it flags the shipment for a resend. Without containerization, cargo (bits) would arrive as one indistinguishable heap, and a single damaged crate could destroy the interpretation of the entire shipment.

## 7. Formal Definition
The data link layer is the second layer of the OSI model (Layer 2) that provides functional and procedural means to transfer data between network entities over a physical link. Its protocol data unit is the **frame**. Its standard functions are: (1) **framing/synchronization** — establishing and maintaining frame boundaries; (2) **error control** — detecting and optionally correcting bit errors via redundant bits; (3) **flow control** — regulating transmission rate so a fast sender does not overrun a slow receiver; and (4) **access control** — coordinating use of a shared medium (when applicable).

## 8. Example
Consider a simple **Ethernet II frame** carrying one small IP packet:
- Preamble (7 bytes, `0x55...`) + SFD (1 byte `0xD5`) — physical-layer sync, not counted in the frame.
- Destination MAC `AA:BB:CC:DD:EE:01` (6 bytes), Source MAC `11:22:33:44:55:66` (6 bytes).
- EtherType `0x0800` (2 bytes) = "IPv4 follows".
- Payload: IP packet, say 46 bytes.
- Frame Check Sequence (FCS): 4 bytes CRC-32 over everything from dest MAC through payload.
The receiver scans for the SFD, then counts 14 + payload bytes, computes CRC-32 over those bytes, compares to the transmitted FCS. Match → hand the 46-byte payload to IP. Mismatch → drop the frame silently (Ethernet performs no retransmission at L2; upper-layer TCP will detect the loss).

## 9. Internal Working
1. **Receive from network layer**: the IP module passes a packet (up to MTU, e.g., 1500 bytes) down.
2. **Encapsulate**: NIC driver prepends dest MAC, source MAC, EtherType (14-byte header).
3. **Compute FCS**: CRC-32 computed over header+payload in hardware, appended as 4-byte trailer.
4. **Send**: frame handed to the MAC sublayer, which enforces the medium access rules (e.g., CSMA/CD for Ethernet, CSMA/CA for WiFi — Chapter 02), then to the physical layer which serializes bits.
5. **Receive**: physical layer deserializes bits; the NIC looks for the SFD to lock onto frame start.
6. **Check FCS**: NIC hardware computes CRC-32 over the received header+payload and compares to the received FCS.
7. **Validate**: on success, DMA the frame to a kernel socket buffer (`sk_buff` in Linux) and hand to the IP layer; on failure, discard and increment the `rx_crc_errors` counter.
8. **Framing choice matters for the medium**: for a *byte-stream* medium (PPP over a serial line), framing uses byte stuffing; for a *block-oriented* medium (Ethernet), length-based framing; for *bit-oriented* links (HDLC), bit stuffing.

## 10. Time Complexity
- **Framing/encapsulation**: O(1) amortized — fixed header/trailer work per frame regardless of payload length.
- **CRC computation**: O(n) bit operations over the frame — linear in frame size, but done in *hardware* on the NIC, so ~1 cycle per 32/64 bits in practice.
- **Receive path**: O(n) to copy the frame into memory (plus interrupt/DMA overhead).
- Note: there is no "algorithmic" complexity here — it is a data-path throughput question. The real constraint is frames-per-second (FPS) at line rate; e.g., 64-byte frames on 10 GbE = ~14.88 M frames/sec, each needing ~67 ns of budget.

## 11. Advantages
- **Per-link error isolation**: a bad frame is dropped at the link where it occurred; corruption does not propagate up the stack or across links.
- **Cheap and fast**: detection (CRC) and framing run in NIC silicon, so they add nanoseconds, not system calls.
- **Works over any medium**: framing + CRC is media-agnostic — it is applied identically to copper, fiber, and radio.
- **Simple to debug**: `tcpdump -e`, `ethtool -S`, and switch counters make frame-level issues observable.
- **Enables higher layers to stay simple**: IP/TCP can assume the link delivers clean bytes (mostly) without checking boundaries.

## 12. Disadvantages
- **Overhead**: header + trailer bytes reduce payload efficiency (minimum Ethernet frame is 64 bytes for 46 payload bytes ≈ 72% efficiency at the extreme).
- **Detection, not protection**: Ethernet only detects; a flipped bit pattern can (rarely) pass a CRC (CRC-32 misses ~1 in 2³² corruptions — about 1 in 4.3 billion).
- **No per-frame accountability at L2**: a dropped frame gives no signal to the sender at L2 (Ethernet has no ACK), so reliability is silently deferred to TCP.
- **Limited reach**: a frame's addresses are only meaningful on its own LAN; frames cannot be routed across the Internet (that is L3's job).
- **Framing fragility**: on very noisy channels, even frame *boundaries* can be lost, requiring resynchronization logic.

## 13. Interview Questions
1. **Q: What are the three functions of the data link layer?** A: Framing (delimiting the bit stream into frames with known boundaries), error control (detecting/correcting corrupted frames via redundancy), and flow control (matching sender rate to receiver capacity). On shared media it adds a fourth: access control.

2. **Q: Why is framing necessary? Can't the receiver just know where packets start?** A: The physical layer is a continuous bit stream with no structure. Without framing, the receiver cannot distinguish data from boundaries; if one packet loses a bit, all subsequent packet boundaries drift and everything is garbage. Framing gives a resync point and a unit of error checking.

3. **Q: Name the framing techniques and give an example of each.** A: (a) Byte/character-oriented framing with byte stuffing — PPP uses flag byte `0x7E` and escapes data `0x7E`→`0x7D 0x5E`, `0x7D`→`0x7D 0x5D`. (b) Bit-oriented framing with bit stuffing — HDLC sends flags `01111110` and stuffs a 0 after five consecutive 1s in data. (c) Length-based framing — Ethernet's type/length field tells the receiver where the payload ends. (d) Clock-based framing — SONET has fixed 125 µs frames aligned by a physical clock.

4. **Q: What is byte stuffing and why is it needed in PPP?** A: A flag byte (`0x7E`) marks frame boundaries on a byte-stream medium. If user data itself contains `0x7E`, the sender inserts an escape byte `0x7D` before it; the receiver strips the escape. This prevents data from being misread as a frame delimiter.

5. **Q: Why does Ethernet not retransmit lost/corrupted frames at Layer 2?** A: Wired links are very reliable (BER ~10⁻¹²), so corruption is rare; retransmission at L2 would add latency and duplicate TCP's job. Ethernet detects (CRC) and drops, and relies on upper layers (TCP) for reliability. WiFi, whose medium is lossy, *does* retransmit at L2 because the cost of losing a frame over the air is high.

6. **Q: What is the maximum size of an Ethernet frame payload, and why is it capped?** A: 1500 bytes (MTU) for classic Ethernet. It is capped to bound (a) the latency that one station can hog the shared medium, (b) the receive buffer requirements, and (c) the error-detection sensitivity (longer frames are more likely to contain an undetectable error pattern). Jumbo frames (9K) are a non-standard option on switched full-duplex networks.

7. **Q: What happens if a frame arrives with a bad FCS?** A: The NIC discards it silently at the hardware level and increments a counter (e.g., `rx_crc_errors` in `ethtool -S`). No ACK/NACK is sent at L2 for Ethernet. The sender eventually discovers the loss via TCP retransmission timeout or the application.

8. **Q: Where is the data link layer implemented — hardware or software?** A: Mostly in the NIC hardware/firmware (framing, CRC, MAC address matching), with the device driver and kernel network stack handling the rest (buffer management, protocol dispatch). This is why L2 is fast; the OS only sees the frame after the NIC validates it.

9. **Q: What's the difference between a frame and a packet?** A: A *packet* is the PDU of the network layer (IP), carrying source/dest IP addresses for end-to-end routing. A *frame* is the PDU of the data link layer, carrying source/dest MAC addresses for hop-by-hop delivery on a single link. An IP packet is *encapsulated* (carried as payload) inside a frame.

10. **Q: Explain the difference between a MAC sublayer and LLC sublayer.** A: IEEE 802 splits L2 into MAC (Medium Access Control: addressing, frame handling, access protocol — CSMA/CD or CA) and LLC (Logical Link Control: multiplexing protocols via SAP/DSAP, providing a uniform interface, optional flow/error control). In practice, Ethernet frames use an EtherType field (DIX format) instead of LLC, which is why `0x0800` vs `0x8100` (VLAN) matters.

11. **Q: TRICKY — If a frame's FCS passes but the payload is still wrong, what do you call that?** A: An *undetected error*, also a false negative of the CRC. It happens because CRC detection is probabilistic: a corrupted frame whose bit pattern happens to produce the same CRC remainder passes. CRC-32's miss probability is ~2⁻³² ≈ 2.3×10⁻¹⁰ per frame.

12. **Q: PRODUCTION — A datacenter switch shows millions of CRC errors on one uplink. What do you check first?** A: Physical-layer issues are the prime suspect, not the switch software: faulty SFP/optics, dirty fiber or damaged copper, cable too long, impedance mismatch, or a bad transceiver on the far end. Next, check for duplex mismatch (both sides must be auto-negotiated or identically forced), then bad NIC drivers/offload settings (TSO/GRO can produce false counts).

13. **Q: SCENARIO — You have a link with a 10⁻⁵ bit error rate and MTU 1500. Roughly what fraction of frames are corrupted?** A: Frame of ~12000 bits (1500×8 + 48 + overhead), so expected corrupted frames per transmitted = 1 − (1−10⁻⁵)^12000 ≈ 1 − e^(−0.12) ≈ 11%. At this error rate you would see about one bad frame in every ~9 — which is why such links need FEC or retransmission, not just detection.

14. **Q: Why is a minimum frame size (64 bytes) required on Ethernet?** A: So that a sender is still transmitting when the first bit of its own frame returns after a collision — the "round-trip time" bound. If frames were shorter than the collision window (512 bit-times at 10 Mb/s), a station could finish sending before detecting a collision and would not back off. The minimum is 64 bytes (or 512 bits including preamble).

15. **Q: What does "MTU" mean and where does it live in the frame?** A: Maximum Transmission Unit — the largest payload the link can carry inside one frame. For Ethernet it's 1500 bytes (EtherType field). IP must fragment packets larger than the path MTU; `ping -M do -s 1472` probes the MTU by sending the largest unfragmented payload.

16. **Q: Can a switch read and forward an IP packet?** A: A classic L2 switch only reads the MAC header (up to the EtherType) and forwards frames by destination MAC learned from the source-MAC table. It does *not* inspect the IP header. An L3 switch/router additionally reads the IP header to route across subnets.

17. **Q: What is the difference between "reliable" links and "best-effort" links at L2?** A: Reliable L2 links (WiFi 802.11) send ACKs at the frame level and retransmit; best-effort (Ethernet) sends once and forgets. Reliability at L2 is a local decision; TCP provides *end-to-end* reliability regardless.

18. **Q: TRICKY — Why does HDLC use bit stuffing with five consecutive 1s, not four or six?** A: The HDLC flag is `01111110` — six 1s. Stuffing at *five* consecutive 1s guarantees data can never contain six 1s, so the flag is unique. Five is chosen because any pattern with fewer than five 1s cannot form the flag even if bits shift. Bit stuffing trades ~1% overhead for guaranteed frame delimiter uniqueness.

## 14. Follow-Up Questions
1. **Q: How does a receiver distinguish a genuine flag from a stuffed sequence during a bit-stuffing receiver?** A: On receiving five consecutive 1s, the receiver checks the next bit: if 0, it is a stuffed 0 and is removed; if 1, look at the bit after: if `10` it's a flag (7E), if `11` it's an abort (7F) — the flag/abort distinction resolves ambiguity.

2. **Q: Why is Ethernet's preamble separate from the frame?** A: The 56-bit `1010...` preamble lets the receiver's clock synchronize to the sender's bit timing (recovery of the clock), and the SFD `10101011` marks the actual start of frame data. They are physical-layer artifacts and are *not* counted in the 64-byte minimum frame or the FCS.

3. **Q: What is the "head-of-line blocking" implication of frames of fixed maximum size?** A: Large payloads monopolize a slow link; small frames amortize overhead poorly. This trade-off is why TCP MSS (1460) exists and why latency-sensitive apps use small frames and jumbo-frame networks are tuned separately.

4. **Q: Where does the data link layer sit relative to a VLAN tag?** A: A VLAN tag (802.1Q, 4 bytes) is inserted between the source MAC and the EtherType, re-marking EtherType to `0x8100`. The switch uses the tag for port isolation; the frame is still an L2 frame.

5. **Q: What modern protocols add reliability/retransmission *below* IP (at L2.5)?** A: PPPoE for DSL, and L2 retransmission in DOCSIS and WiFi. Also, G.Fast and some PON technologies use L2 retransmission/FEC. The principle: add reliability exactly where the error rate is high.

## 15. Coding Example
```python
# Framing simulation: byte stuffing (PPP-style) encode/decode
FLAG = 0x7E
ESC = 0x7D

def frame(payload: bytes) -> bytes:
    out = bytearray([FLAG])
    for b in payload:
        if b == FLAG:
            out += bytes([ESC, 0x5E])
        elif b == ESC:
            out += bytes([ESC, 0x5D])
        else:
            out.append(b)
    out.append(FLAG)
    return bytes(out)

def deframe(framed: bytes) -> bytes:
    assert framed[0] == FLAG and framed[-1] == FLAG
    inner = framed[1:-1]
    out = bytearray()
    i = 0
    while i < len(inner):
        b = inner[i]
        if b == ESC:
            nxt = inner[i+1]
            out.append(0x7E if nxt == 0x5E else 0x7D)
            i += 2
        else:
            out.append(b)
            i += 1
    return bytes(out)

payload = b"\x7E data with flag \x7D and more"
framed = frame(payload)
assert payload == deframe(framed)
print(f"Original({len(payload)}B) -> Framed({len(framed)}B)")
# CRC-32 trailer (as Ethernet uses) — computed over the deframed payload
import zlib
print(f"CRC-32 of payload: {zlib.crc32(payload):08x}")
```
```bash
# See frames on the wire (L2 visibility)
sudo tcpdump -i eth0 -e -nn -c 3          # -e prints Ethernet header (src/dst MAC, EtherType)
sudo ethtool -S eth0 | grep -E "crc|fcs"  # frame-level error counters
```

## 16. Industry Usage
- **Ethernet (IEEE 802.3)**: the dominant L2 — every datacenter, office, and ISP backbone runs it. NICs implement framing + CRC-32 in silicon at 100 GbE and 400 GbE line rates.
- **WiFi (IEEE 802.11)**: framing + CRC-32 + *frame-level retransmission* because the air is lossy.
- **PPP**: used for DSL (PPP over Ethernet — PPPoE) and traditional dialup; framing via byte stuffing.
- **HDLC**: WAN links, Frame Relay, and satellite links; bit-oriented framing.
- **Linux networking**: the entire receive path is frame-first — `struct sk_buff` holds a frame; `ethtool`, `ip link`, and `tcpdump -e` expose frame-level detail; `CONFIG_BPF`/XDP lets you drop or rewrite frames at line rate before the stack sees them.
- **Cloud**: AWS VPC endpoints, Google Cloud VPC — tenants share L2 fabrics where VLAN/overlay tags (VXLAN, Geneve) re-frame packets; Cloudflare's edge uses raw Ethernet frames with custom headers (MSS clamping, etc.).

## 17. References
- Kurose & Ross, *Computer Networking: A Top-Down Approach*, 8th ed., Ch. 6 (Link Layer and LANs).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., Ch. 3 (The Data Link Layer).
- IEEE Std 802.3-2022 (Ethernet) — https://standards.ieee.org/ieee/802.3/10422/
- IEEE Std 802.11-2020 (WiFi) — https://standards.ieee.org/ieee/802.11/7028/
- RFC 1661 (PPP), RFC 1662 (PPP in HDLC-like Framing) — https://datatracker.ietf.org/doc/html/rfc1662
- RFC 894 (Transmission of IP datagrams over Ethernet) — https://datatracker.ietf.org/doc/html/rfc894

## 18. Cheat Sheet
- DLL jobs = **frame + detect/correct errors + flow control** (access control on shared media).
- Frame = dest MAC + src MAC + EtherType + payload + FCS(CRC-32).
- Byte stuffing (PPP): `7E`→`7D 5E`, `7D`→`7D 5D`; flag `0x7E`.
- Bit stuffing (HDLC): flag `01111110`; stuff a 0 after 5 consecutive 1s.
- Ethernet preamble: 7×`0x55` + SFD `0xD5`; not part of the frame.
- Min Ethernet frame 64 B, payload ≤ 1500 B (MTU), FCS 4 B CRC-32.
- CRC detects all single/double/odd/≤r-bit-burst errors; misses ~2⁻³².
- Ethernet = detect-and-drop; WiFi = detect-and-retransmit.
- Framing done in NIC hardware; software sees validated frames.

## 19. Quiz
1. Which is NOT a function of the data link layer? a) Framing b) Routing across the Internet c) Error detection d) Flow control → **b**
2. In PPP byte stuffing, the byte `0x7D` in data is transmitted as: a) `0x7E` b) `0x7D 0x7D` c) `0x7D 0x5D` d) `0x5E` → **c**
3. HDLC flag is: a) `01111110` b) `01111111` c) `0x7E` repeated d) `11111111` → **a**
4. Ethernet minimum frame size is: a) 46 B b) 64 B c) 1500 B d) 1518 B → **b**
5. A CRC-32 frame-level false-acceptance probability is approximately: a) 2⁻¹⁶ b) 2⁻³² c) 2⁻⁶⁴ d) 0 → **b**
6. The Ethernet FCS is computed over: a) payload only b) header only c) header+payload d) preamble+header+payload → **c**
7. Which layer's PDU is the *packet*? a) Link b) Network c) Transport d) Physical → **b**

**Answers**: 1-b, 2-c, 3-a, 4-b, 5-b, 6-c, 7-b.

## 20. Flashcards
- **Q: Why does the data link layer exist?** → **A:** To make an unreliable raw bit pipe reliable and structured: framing, error control, flow control.
- **Q: What are the 4 framing approaches?** → **A:** Byte-stuffing (PPP), bit-stuffing (HDLC), length-based (Ethernet), clock-based (SONET).
- **Q: What is the PPP escape sequence for a flag byte?** → **A:** `0x7D 0x5E` (0x7E escaped as 0x7D followed by 0x5E).
- **Q: What does Ethernet do when a frame's FCS is bad?** → **A:** Drops it silently, increments a counter; no L2 retransmission.
- **Q: Where are frame/packet defined?** → **A:** Frame = L2 PDU with MAC addresses; Packet = L3 PDU with IP addresses.
- **Q: Why is there a minimum 64-byte Ethernet frame?** → **A:** To bound the collision-detection window on shared media (512 bit-times).
- **Q: Why is framing done in the NIC?** → **A:** Speed — line-rate framing needs silicon, not OS scheduling.

## 21. Revision
The data link layer exists because a physical bit pipe is unstructured and unreliable. It fixes this with (1) **framing** — carving bits into discrete frames with boundaries enforced by byte stuffing (PPP `0x7E`), bit stuffing (HDLC `01111110`), or length fields (Ethernet); (2) **error control** — a CRC-32 FCS computed over header+payload and checked in NIC hardware, so bad frames are dropped, not forwarded; (3) **flow control** — pacing the sender. Ethernet is a *best-effort* L2: detect-and-drop, relying on TCP for reliability; WiFi retransmits at L2 because air is lossy. Memory anchors: frame = envelope, packet = letter; preamble is physical, not frame; min frame 64 B for collision detection; CRC-32 has a ~2⁻³² blind spot. Before an interview, be ready to compute a CRC remainder by hand and to name real L2 protocols (802.3, 802.11, PPP, HDLC).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What are the functions of the data link layer?" | 1 / 7 |
| "How does byte stuffing work in PPP?" | 8 / 9 |
| "Why is framing necessary?" | 1 / 5 |
| "What happens when a frame has a bad FCS?" | 9 / 13-Q7 |
| "Why doesn't Ethernet retransmit?" | 4 / 13-Q5 |
| "What is the minimum Ethernet frame size and why?" | 13-Q14 |
| "Where is the DLL implemented?" | 9 / 13-Q8 |
| "Frame vs packet?" | 13-Q9 |
| "You see CRC errors in production, what do you check?" | 13-Q12 |
