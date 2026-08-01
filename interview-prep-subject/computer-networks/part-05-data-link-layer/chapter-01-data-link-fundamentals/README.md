# Chapter: Data Link Fundamentals

## What you'll learn
- Why a "raw bit pipe" is not enough — the data link layer's three jobs: framing, error control, and flow control.
- How framing works in practice: bit-oriented (HDLC), character-oriented (PPP), length-based (Ethernet), and how stuffing prevents data from being mistaken for delimiters.
- How error *detection* works: parity, checksums, and CRC (with hand-computable polynomial division math).
- How error *correction* works: Hamming distance, Hamming code with a full worked single-bit-correction example, and when to correct vs. retransmit.

## Prerequisites (linked)
- Basic understanding of the OSI/TCP-IP models and the idea of *layering* (Part 01, [OSI and TCP/IP Models](../part-01-network-fundamentals/chapter-02-osi-and-tcp-ip-models/README.md)).
- Comfort with binary arithmetic and XOR (everything in this chapter is XOR + polynomial arithmetic).
- Part 06 (Physical Layer) describes the noisy bit pipe this chapter compensates for.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Role of Data Link Layer and Framing](section-01-role-of-data-link-layer-and-framing.md) | Why the layer exists; the frame as the L2 protocol data unit; framing + stuffing techniques |
| [Section 02 — Error Detection: Parity, Checksum, CRC](section-02-error-detection-parity-checksum-crc.md) | Detection vs correction, VRC/LRC parity, Internet checksum, CRC with worked polynomial division |
| [Section 03 — Error Correction and Hamming Code](section-03-error-correction-and-hamming-code.md) | Hamming distance, minimum distance bounds, Hamming code encode/decode/correct workflow |

## One-paragraph narrative connecting all sections
The Physical layer (Part 06) delivers only an unreliable stream of bits — a "bit pipe" that flips bits, loses them, and gives no notion of message boundaries. The data link layer's first job is to impose *structure* on that bit pipe: framing carves the stream into frames with start/end boundaries and stuffing rules (Section 01). Because the medium flips bits, the sender and receiver must agree on how to detect — and optionally correct — corruption: parity and checksums are cheap detectors, while CRC gives guaranteed detection guarantees for bursts (Section 02). When retransmission is too expensive or impossible, Hamming code goes one step further and *corrects* single-bit errors using redundant parity bits (Section 03). All three sections together define "reliability at link level," which is what every later topic (flow control, Ethernet, WiFi) assumes.

## Common interview trap in this chapter
Candidates confuse **error detection** with **error correction** and then mix up **flow control** (rate management) with **error control** (detection/correction). Flow control is NOT in this chapter — it is Section 02 of Chapter 02. Also, a frequent wrong answer: "CRC detects all errors." Correct answer: CRC-32 detects all single-bit errors, all double-bit errors, all odd numbers of errors, and all error *bursts* of length ≤ 32 bits; it *cannot* detect every possible corruption. And a very common bug: Hamming code parity positions are powers of two (1, 2, 4, 8...), NOT sequential positions.

## Checklist before moving on
- [ ] I can explain the 3 jobs of the data link layer and give the failure mode each one fixes.
- [ ] I can name 3 framing approaches and explain stuffing with a concrete 0x7E/0x7D example.
- [ ] I can compute parity, the Internet checksum of a short byte string, and a CRC-3 remainder by hand (polynomial division).
- [ ] I can state the Hamming distance of `1011010` vs `1101001` and the detect/correct bounds for a given d_min.
- [ ] I can encode a 4-bit message with Hamming(7,4), simulate a 1-bit flip, locate and correct it.
- [ ] I know when a system chooses detection+retransmission vs. forward error correction (FEC).
