# Error Detection: Parity, Checksum, and CRC

> **TL;DR**: Error detection appends redundant bits to a frame so the receiver can tell with high probability that the bits it received differ from what was sent — parity is the cheapest single-bit detector, the Internet checksum catches word-level errors in software, and CRC (cyclic redundancy check) is the industrial-grade polynomial detector used in Ethernet, WiFi, and storage.

## 1. Why Does This Exist?
The physical layer (Part 06) delivers a bit pipe that *corrupts* bits: electromagnetic interference, crosstalk, thermal noise, and signal attenuation flip 0↔1 at measurable rates (BER of 10⁻¹² on clean fiber up to 10⁻⁴–10⁻⁶ on WiFi/cellular). A receiver cannot tell whether a received bit is correct without *redundancy* — extra information that the sender computes from the data and the receiver re-computes. Error detection exists because silent corruption is unacceptable: a flipped bit in a financial transfer, a medical record, or a TCP ACK is a correctness bug you can never see. Detection turns "I received these bits" into "I received these bits **and they are almost certainly the bits that were sent**," which is the prerequisite for retransmission (TCP does the same thing at a higher level with its checksum) and for FEC correction (Hamming code, next section).

## 2. How Does It Work?
The sender computes a function `f(data)` producing a small, fixed-size *check value* (1 bit for parity, 16 bits for Internet checksum, 32 bits for CRC-32) and appends it to the frame. The receiver recomputes `f` over the received data. If the recomputed value equals the received check value, the frame is accepted (with high probability); if not, it is dropped. The key design choice is *which* errors are detectable: parity detects all odd numbers of bit errors, the checksum detects all single-bit and most multi-bit errors in a word-oriented way, and a degree-*r* CRC guarantees detection of all single-bit errors, all double-bit errors, all odd numbers of errors, and all *bursts* of length ≤ *r* — with miss probability ≈ 2⁻ʳ for other patterns.

## 3. When Is It Used?
- **CRC-32**: the Ethernet FCS (IEEE 802.3), WiFi's frame check sequence, SATA/PCIe links, PNG/zip archives, GZIP, MPEG. It is the detection workhorse at L2 and in storage.
- **CRC-16/CRC-CCITT**: HDLC, PPP, XMODEM, USB token packets, Bluetooth.
- **Internet Checksum (RFC 1071)**: one's-complement sum of 16-bit words — used in IP, TCP, UDP, ICMP. It is *weaker* than CRC but cheap to compute in software and catches word-transposition errors.
- **Parity (VRC)**: single-bit vertical redundancy check in early UART/serial links and memory (RAM ECC uses more, but parity alone appears in legacy links); parity in NICs' LRC-style horizontal checks.
- **Hamming/ECC**: where correction, not just detection, is needed — RAM, NAND flash, and high-rate links with no retransmission budget (next section).

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: send the data twice and compare.* Detects many errors but costs 100% overhead and misses the rare case where both copies corrupt identically. Parity costs 1 bit per 8.
- *Alternative: a simple sum of bytes (arithmetic checksum).* Byte-swap and transposition errors (bytes moved) can produce the same sum. The Internet checksum's one's-complement addition plus end-around carry makes it order-sensitive across words; CRC is *also* order-sensitive because polynomial division shifts bits through registers in sequence.
- *Alternative: CRC for everything.* CRC is superior in burst detection but needs hardware shift registers to hit line rate; the Internet checksum was chosen for IP/TCP because it runs in software cheaply on any CPU and the transport layer already retransmits (so strong burst detection is less critical). Ethernet has silicon for CRC-32, so it uses the stronger code. The engineering rule: *match the code strength to the medium's noise and to whether hardware is available*.
- *Alternative: error correction everywhere (FEC).* Correcting costs many more redundant bits and decoding latency; when a back-channel exists and errors are rare, detect-and-retransmit (ARQ) is cheaper. FEC wins only when retransmission is impossible or too costly (satellite, multicast, storage, real-time media).

## 5. Intuition
A check value is a **fingerprint** of the data. Like a bank counting cash and writing the total on the deposit slip: if the count at the bank differs from the count on the slip, something changed in transit — but a *very* unlucky error (one bill removed, one added) can keep the total identical. CRC is a better fingerprint because it mixes the bits position-by-position through a shift register, so a *burst* of noise that corrupts N adjacent bits changes the fingerprint in a way a plain sum would often miss. Parity is the cheapest fingerprint: just "is the number of 1s odd or even?"

## 6. Real-World Analogy
A **delivery courier with a scale**: you weigh each package before dispatch and write the weight on the label. At the destination, the receiving clerk re-weighs. If the label weight and the re-weighed weight differ, the package is suspect and gets re-sent. Parity is the crude "count of items" check; the checksum is "sum of prices"; CRC is the courier's *dimension + weight + bar-code* hash — it catches the case where one heavy item was replaced by a light one (a burst) that a simple sum would miss.

## 7. Formal Definition
Error detection coding adds *redundancy* to a message so that a receiver can determine whether errors occurred during transmission. A code with Hamming distance *d_min* can detect up to *d_min − 1* bit errors in any codeword. **Single-bit parity** appends one bit so the total number of 1s is even (even parity) or odd; it detects all patterns with an odd number of errors. The **Internet checksum** is the 16-bit one's-complement sum of all 16-bit words in the message (RFC 1071), complemented before transmission. A **CRC** treats the message as a binary polynomial *M(x)*, appends *r* zero bits, divides by a fixed generator polynomial *G(x)* of degree *r* over GF(2), and transmits the original message followed by the remainder *R(x)* = xʳM(x) mod G(x); the receiver accepts if the full received polynomial is divisible by *G(x)*.

## 8. Example
**Parity.** Message `1011010` (7 bits). Even parity: count of 1s = 4 (even) → parity bit 0 → codeword `10110100`. If one bit flips to `10111100`, count = 5 (odd) → error detected. If two bits flip to `10111110`, count = 6 (even) → error *missed*.

**Internet checksum.** Words: `0x1234, 0xABCD, 0x5432`. Sum (16-bit): `0x1234 + 0xABCD = 0xBE01`, `+ 0x5432 = 0x11233` → take end-around carry: `0x1233 + 0x0001 = 0x1234`. Checksum = complement = `0xEDCB`. Receiver re-sums all four words including the checksum: `0x1234 + 0xABCD + 0x5432 + 0xEDCB = 0x1FFFF` → fold carry → `0xFFFF` → valid.

**CRC-3 with G(x) = x³ + x + 1 (`1011`).** Message `1101`. Append 3 zeros → `1101000`. Divide by `1011` (mod-2, XOR):
```
1011) 1101000
      1011
      01110
       1011
       01010
        1011
        0001  → remainder 001 (r=3 → 3 bits)
```
Transmit `1101000 | 001` = `1101001`. Receiver divides the whole `1101001` by `1011`; remainder 0 → accepted. Any single-bit error, any burst ≤ 3 bits → nonzero remainder → detected.

## 9. Internal Working
1. **CRC polynomial arithmetic (GF(2))**: addition and subtraction are XOR (no carries). Choose generator degree *r*; the CRC-32 used by Ethernet (IEEE 802.3, reflected `0xEDB88320`) has degree 32 and a specific bit-reversal convention so hardware can shift right instead of left.
2. **Hardware implementation**: an *r*-bit shift register (LFSR). Bits of the message shift in MSB-first; at each step, if the shifted-out bit is 1, XOR the register with the generator. After all message bits, the register holds the remainder, which is appended.
3. **Receiver**: shifts the whole received frame (data + remainder) through the same register; the register ends at 0 if and only if the frame is a valid codeword.
4. **Internet checksum**: 16-bit one's-complement addition implemented with `addc`-style instructions; used by IP (RFC 1071), TCP, UDP, ICMP over the whole segment/datagram header+payload. TCP checksum also covers a 96-bit *pseudo-header* (source/dest IP, protocol, length) to catch misdelivery.
5. **Parity at the link**: a NIC may compute per-byte parity (LRC) for early detection before the stronger CRC, or memory-style parity in buffers.
6. **Position in the stack**: all three run at different layers — parity legacy/L1, CRC at L2/storage, Internet checksum at L3/L4 — because each layer has different error characteristics and computing budgets.

## 10. Time Complexity
- **Parity**: O(n) XORs, 1 bit per byte.
- **Internet checksum**: O(n) 16-bit adds — ~1 addition per 2 bytes; on modern CPUs it runs in the ~1-2 ns/10KB range and can be offloaded to NIC hardware.
- **CRC**: O(n · r/word) bit operations, or ~1 shift-register step per input bit — linear. In silicon, CRC-32 runs at line rate (400 GbE = 400 Gbps) with a handful of lookahead tables; a software table-driven CRC-32 computes ~1 byte per 4-6 instructions.
- Detection math is *always* linear in message length — the interesting metric is **overhead ratio** (r/n) and **miss probability** (≈ 2⁻ʳ for random patterns, 0 for the guaranteed classes).

## 11. Advantages
- **Cheap**: parity is 1 redundant bit per data unit; CRC-32 is 4 bytes per ≤1500-byte frame (~0.26% overhead); the checksum is 2 bytes per segment.
- **Guaranteed classes**: a degree-*r* CRC detects *every* error burst ≤ *r* bits, all single- and double-bit errors, all odd-count errors — a formally provable guarantee, not just probability.
- **Fast in hardware and software**: LFSRs are a handful of XOR gates; table-driven software CRCs run at GB/s.
- **Layer-appropriate**: each layer's detection is sized to its noise and computing budget (CRC for noisy links in silicon, checksum for end-to-end in software).
- **No retransmission cost when correct**: detection alone costs nothing on good links; correctness is verified on every frame.

## 12. Disadvantages
- **Detection only**: a bad frame is *dropped*; recovery requires ARQ (retransmission) at a higher layer or the data is lost — not suitable when no back-channel exists (one-way broadcast, storage).
- **Miss probability**: for random multi-bit patterns, a degree-*r* CRC accepts a corrupt frame with probability ≈ 2⁻ʳ (CRC-32 ≈ 1 in 4.3 billion). The Internet checksum is much weaker (miss ~1 in 2¹⁶ for random errors and it cannot detect some word-swap patterns).
- **Parity is weak**: misses all even-count errors, no burst detection.
- **Not tamper-proof**: all three are *error*-detectors, not *attack*-detectors; an adversary who knows the polynomial can forge a valid CRC/checksum (that's what MACs/HMACs in Part 07 fix).
- **Endianness/implementation bugs**: the Internet checksum has famous historical bugs (e.g., UDP checksum offload mishandling, zero checksum meaning "not computed" in IPv4 UDP).

## 13. Interview Questions
1. **Q: What's the difference between error detection and error correction?** A: Detection (parity/checksum/CRC) only tells you a frame is bad — you drop and retransmit. Correction (Hamming/Reed-Solomon) adds enough redundancy to reconstruct the original bits in place — used when retransmission is impossible or too slow. Correction is a superset: a code that corrects *t* errors also detects *2t*.

2. **Q: What errors does single-bit parity detect, and what does it miss?** A: It detects every pattern with an *odd* number of bit errors and misses every pattern with an *even* number. So it's a "is the count of 1s wrong by parity" test, not a general detector.

3. **Q: How does CRC work in one sentence?** A: Treat the message as a binary polynomial, divide it (mod-2) by a fixed generator polynomial, and transmit the message followed by the remainder; the receiver re-divides and accepts iff the remainder is zero.

4. **Q: Why can CRC detect all bursts shorter than the polynomial degree?** A: A burst of length *b* ≤ *r* has a leading 1 and at most *r* bits, so its error polynomial *E(x)* is not divisible by any generator *G(x)* of degree *r* unless *E(x)* = *G(x)* exactly — and *E(x)*'s degree is < *G(x)*'s, so it can't be. Hence the remainder is always nonzero.

5. **Q: What is the miss probability of CRC-32?** A: For error patterns not in the guaranteed-detectable classes, roughly 2⁻³² ≈ 2.3 × 10⁻¹⁰ per frame. That's why Ethernet trusts a 32-bit FCS.

6. **Q: TRICKY — CRC detects all single-bit errors. Why?** A: A single-bit error has error polynomial *E(x)* = xⁱ. A degree-*r* generator is never a factor of xⁱ unless the generator's constant term is 0 (which valid generators avoid) — so xⁱ mod *G(x)* ≠ 0 always.

7. **Q: Why does the Internet checksum use one's-complement addition and an end-around carry?** A: One's complement is cheap (adds produce carry that must wrap), is endian-agnostic (sum is the same regardless of byte order when checking), and the complement-before-send convention lets the receiver compute one sum and test for 0xFFFF. It also catches the all-zeros case differently from two's complement.

8. **Q: What is the 96-bit pseudo-header in TCP/UDP checksums, and why does it exist?** A: The pseudo-header repeats source/dest IP addresses, protocol, and length into the checksum input so the receiver can detect a segment delivered to the wrong host or port. It is not transmitted — it is reconstructed at both ends.

9. **Q: SCENARIO — A NIC reports `rx_crc_errors` climbing. Which layer is failing?** A: Almost always the *physical* layer — bad SFP/optics, dirty fiber, faulty cable, or duplex mismatch — because CRC errors at L2 mean corrupted bits, which come from the medium. Check optics power (`ethtool -S`, `mii-tool`), swap the cable, verify duplex on both ends, then suspect a bad NIC or driver offload bug.

10. **Q: PRODUCTION — Why does Ethernet use CRC-32 at L2 while TCP uses a weak 16-bit checksum at L4?** A: Ethernet has dedicated silicon that can do a strong 32-bit CRC at 400 Gbps at essentially zero cost, and L2 catches noise on the physical hop. TCP runs on general-purpose CPUs and retransmits anyway, so a cheap 16-bit software checksum is the cost/benefit sweet spot; TCP also gets *extra* protection because every underlying link (Ethernet) already ran CRC-32.

11. **Q: What is the difference between VRC and LRC?** A: VRC (vertical redundancy check) is a parity bit per *character* (column); LRC (longitudinal redundancy check) is a parity bit per *row/block*. Together they form a 2D parity grid that can even *locate* a single bit error (row+column point to it) — the seed idea behind Hamming code.

12. **Q: TRICKY — Your frame passes the CRC but the payload is wrong. What happened?** A: An undetected error — the corruption pattern's polynomial happened to be a multiple of the generator (probability ≈ 2⁻³² for CRC-32). Detection is probabilistic at the tail; this is why critical data adds end-to-end checksums (TLS record MAC) on top of link-layer CRC.

13. **Q: Can a checksum detect that two 16-bit words were swapped?** A: The Internet checksum *mostly* does because one's-complement addition is commutative... **wait, no** — addition is commutative, so swapping two words yields the same sum! This is a known weakness: the Internet checksum cannot detect word-transposition. CRC does detect transposition because polynomial shifting is order-sensitive.

14. **Q: What polynomial does Ethernet's CRC-32 use, and what's the practical reflection?** A: IEEE 802.3 uses a 33-bit generator (0x04C11DB7) applied in *reflected* form (0xEDB88320) with the bits processed LSB-first for convenient hardware; the remainder is XORed with 0xFFFFFFFF before append. These reflection conventions mean you must match the exact table/register setup to interoperate.

15. **Q: SCENARIO — Over a link with BER 10⁻⁶, frame 1500 bytes. CRC-32 with detection of all bursts ≤32. How many frames per second are silently corrupt?** A: Frame ≈ 12016 bits. Probability of any error ≈ 1 − (1 − 10⁻⁶)^12016 ≈ 1.2% → ~1 in 83 frames corrupt. Of those, 2⁻³² are missed → effective silent-corruption rate ≈ 1.2% × 2.3×10⁻¹⁰ ≈ 2.8×10⁻¹² per frame — at 1 Gbps (~81k fps) ≈ 0.23 silent-corrupt frames *per year*. That's why CRC-32 is trusted.

16. **Q: Why is the generator polynomial's constant term required to be 1?** A: So that *G(x)* does not divide xⁱ — guaranteeing single-bit-error detection. More generally, generators are chosen (mathematically studied) so the code has the largest minimum Hamming distance for its degree.

17. **Q: What's the difference between a CRC and an MD5/SHA hash used for integrity?** A: Both are "fingerprints," but CRC is a *linear* polynomial code designed to catch random transmission noise with specific burst guarantees, while SHA-2/SHA-3 are *cryptographic* hashes designed so that even a malicious attacker cannot craft two messages with the same digest. CRC is fast and hardware-friendly; hashes are slow but tamper-resistant.

18. **Q: PRODUCTION — You're designing a 1000-km undersea fiber link with no retransmission possible at the physical layer. Which detector and why?** A: Use a strong FEC code (Reed-Solomon or LDPC) for *correction*, since a single retransmission costs the whole one-way propagation delay (~5 ms per 1000 km) and light-level transients corrupt long bursts. Detection-only (ARQ) would need an end-to-end retransmission loop that is far too slow; forward error correction rides through the burst.

## 14. Follow-Up Questions
1. **Q: How does a table-driven CRC-32 achieve byte-at-a-time speed?** A: Precompute a 256-entry table of remainders for each possible byte at the top of the register; process each input byte by XORing it into the high byte and looking up the remainder — turning 8 shift steps into ~1 lookup + 3 XORs per byte.

2. **Q: Why does UDP's checksum field being 0 mean "not computed"?** A: A valid one's-complement sum of a segment can't be 0x0000 unless the sender sent a zero payload, so IPv4 UDP treats 0x0000 as "no checksum" (frequently disabled for fast paths; IPv6 mandates it always be computed).

3. **Q: Can two different messages produce the same CRC-32?** A: Yes — pigeonhole principle: 2^32 CRCs vs infinitely many messages. But *near* duplicates are exponentially unlikely; the danger is adversarial crafting, which is why CRC is never used for security.

4. **Q: What does "burst error" mean and why is it CRC's specialty?** A: A contiguous run of corrupted bits (from impulse noise, e.g., lightning or a cable zap). CRC catches any burst ≤ *r* bits; parity and simple checksums have no burst guarantee.

## 15. Coding Example
```python
# CRC-3 (G = 0b1011, degree 3) — full worked implementation
def crc3(msg: int, nbits: int) -> int:
    gen = 0b1011
    reg = msg << 3                  # append 3 zeros
    for i in range(nbits + 3 - 1):  # run over top bit down to LSB
        if (reg >> (nbits + 3 - 1)) & 1:
            reg ^= gen << (nbits + 3 - 1 - 3)
        reg <<= 1
    return (reg >> 3) & 0b111        # 3-bit remainder

msg = 0b1101
rem = crc3(msg, 4)
tx = (msg << 3) | rem
print(f"msg={msg:04b} rem={rem:03b} tx={tx:07b}")

# CRC-32 as used by Ethernet (via zlib; same polynomial family)
import zlib
frame_payload = b"hello ethernet"
fcs = zlib.crc32(frame_payload) & 0xffffffff
print(f"CRC-32 of {frame_payload!r}: {fcs:08x}")

# Internet checksum (RFC 1071)
def inet_checksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    s = sum(int.from_bytes(data[i:i+2], "big") for i in range(0, len(data), 2))
    while s >> 16:
        s = (s & 0xffff) + (s >> 16)
    return (~s) & 0xffff

payload = b"\x12\x34\xab\xcd\x54\x32"
ck = inet_checksum(payload)
print(f"Internet checksum: {ck:04x}")
```
```bash
# Detect corruption in practice on Linux
sudo ethtool -S eth0 | grep -E "crc|fcs|bad"   # NIC CRC error counters
tcpdump -i eth0 -nn -c 5                        # frames that survived L2 CRC
ip link set eth0 txqueuelen 1000                # e.g., link tuning (CRC offload set via ethtool)
ethtool -k eth0 | grep checksum                 # verify offload of TCP/UDP checksums
```

## 16. Industry Usage
- **Ethernet (IEEE 802.3)**: 32-bit FCS CRC computed in every NIC at up to 400 GbE line rates in silicon.
- **WiFi (IEEE 802.11)**: 32-bit FCS per frame with *retransmission* because the air is lossy.
- **TCP/IP (RFC 1071, RFC 793)**: 16-bit one's-complement checksums, often NIC-offloaded (`NETIF_F_CHECKSUM_OFFLOAD`), protecting every segment end-to-end plus the pseudo-header.
- **Storage**: ext4/APFS use checksums (CRC-32c) on metadata blocks; ZFS uses checksums on every block and *self-heals* from parity drives.
- **PCIe/SATA**: CRC-32/CRC-16 on every TLP/frame for link reliability.
- **Cloud/NIC vendors**: Intel/AMD/Mellanox offload CRC and checksum in silicon; DPDK bypasses the kernel and still relies on NIC-computed FCS.
- **Cloudflare/Google edge**: line-rate packet processing (XDP/DPDK) assumes NIC-computed CRC-32 dropped bad frames before the software stack sees them.

## 17. References
- Kurose & Ross, *Computer Networking: A Top-Down Approach*, 8th ed., Ch. 6.2 (Error Detection and Correction).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., Ch. 3.2 (Error Detection and Correction).
- IEEE Std 802.3-2022 (Ethernet), §3.2.8 CRC/FCS — https://standards.ieee.org/ieee/802.3/10422/
- RFC 1071 (Computing the Internet Checksum) — https://datatracker.ietf.org/doc/html/rfc1071
- Ross N. Williams, *A Painless Guide to CRC Error Detection Algorithms* — https://archive.org/details/PainlessGuideToCrcErrorDetectionAlgorithms
- Wikipedia, Cyclic Redundancy Check (polynomial math) — https://en.wikipedia.org/wiki/Cyclic_redundancy_check

## 18. Cheat Sheet
- Detection adds redundancy; correction reconstructs. Detect d errors → need d_min ≥ d+1; correct t → d_min ≥ 2t+1.
- Parity: 1 bit, detects odd-count errors only.
- Internet checksum: 16-bit one's-complement sum, fold carries, complement before send; receiver checks for 0xFFFF. Detects ~all single-bit/word errors, misses transpositions (addition is commutative).
- CRC: message = polynomial; append r zeros; divide mod-2 by degree-r generator; append remainder. Receiver divides, wants remainder 0.
- CRC-r detects: all single, double, odd-count, and bursts ≤ r; miss ≈ 2⁻ʳ.
- CRC-32 generator (Ethernet): 0x04C11DB7, reflected 0xEDB88320, final XOR 0xFFFFFFFF.
- CRC catches byte *transposition*; Internet checksum does not.
- CRC = error + attack-vulnerable; SHA/MAC = tamper-resistant.

## 19. Quiz
1. Single-bit parity detects: a) all errors b) odd-count errors c) even-count errors d) bursts → **b**
2. A degree-r CRC guarantees detection of bursts of length: a) any b) ≤ r c) > r d) exactly r → **b**
3. CRC miss probability for random patterns is ≈: a) 2⁻¹⁶ b) 2⁻ʳ c) 2⁻³² always d) 0 → **b**
4. The Internet checksum is a: a) 32-bit CRC b) 16-bit one's-complement sum c) parity d) hash → **b**
5. Which does the Internet checksum NOT reliably detect? a) single-bit b) word-swap c) burst ≤ 16 d) odd-count → **b**
6. Ethernet's FCS is: a) CRC-16 b) Internet checksum c) CRC-32 d) SHA-256 → **c**
7. To detect 5 errors you need minimum Hamming distance: a) 5 b) 6 c) 4 d) 10 → **b**
8. The TCP checksum covers: a) TCP header b) TCP+IP c) TCP + pseudo-header + data d) payload only → **c**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-c, 7-b, 8-c.

## 20. Flashcards
- **Q: What does parity detect vs miss?** → **A:** Detects odd-count errors; misses even-count errors.
- **Q: How does a receiver validate a CRC frame?** → **A:** Re-divides the whole frame (data+remainder) by the generator; remainder must be 0.
- **Q: What are CRC's guaranteed detections?** → **A:** All single, double, odd-count, and bursts ≤ degree; miss ≈ 2⁻ʳ.
- **Q: Why was the Internet checksum chosen over CRC for IP/TCP?** → **A:** Cheap in software (16-bit adds), end-to-end where retransmission exists; CRC needs silicon.
- **Q: What is the pseudo-header for?** → **A:** To include source/dest IP + port/length in the TCP/UDP checksum so misdelivery is caught.
- **Q: Which detector catches byte-swap errors?** → **A:** CRC (order-sensitive shifts); the Internet checksum (commutative addition) does not.

## 21. Revision
Error detection makes a noisy bit pipe trustworthy by appending a fingerprint. **Parity** (1 bit) is the cheapest and detects only odd-count errors. The **Internet checksum** is a 16-bit one's-complement sum over words (RFC 1071), used end-to-end by IP/TCP/UDP/ICMP with a pseudo-header; it's fast in software but weak (misses transpositions). The **CRC** is a GF(2) polynomial division by a degree-*r* generator; a degree-*r* CRC provably detects every single-bit, double-bit, odd-count, and ≤*r*-bit-burst error, missing others with probability ≈ 2⁻ʳ. Ethernet runs CRC-32 in NIC silicon; WiFi runs CRC-32 + retransmission. Order-of-strength to memorize: parity < Internet checksum < CRC-16 < CRC-32; and remember detection ≠ security — CRC is linear and forgeable, which is why TLS/SSH use cryptographic MACs on top.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Difference between error detection and correction?" | 1 / 7 |
| "Compute the parity/checksum/CRC for this input" | 8 / 15 |
| "What errors can CRC miss, with what probability?" | 8 / 13-Q5 |
| "Why does CRC catch bursts ≤ r?" | 13-Q4 / 14 |
| "Why is the Internet checksum weak?" | 4 / 13-Q13 |
| "What is the TCP pseudo-header?" | 13-Q8 |
| "CRC error counters are climbing — what do you check?" | 13-Q9 |
| "Why CRC-32 at L2 but checksum at L4?" | 13-Q10 |
| "Can CRC be forged / is it security?" | 13-Q17 / 21 |
