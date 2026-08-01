# Error Correction and Hamming Code

> **TL;DR**: Hamming code is a forward error correction (FEC) scheme that adds carefully placed parity bits (at positions that are powers of two) so the receiver can not only detect but *locate and fix* a single flipped bit — trading a small amount of bandwidth for the ability to correct in place without retransmission.

## 1. Why Does This Exist?
Detection (previous section) tells you a frame is bad but forces you to drop it and hope for retransmission — which is impossible or cripplingly slow in three big situations: (1) **one-way links** (satellite downlink, multicast/broadcast, live video) where no back-channel exists; (2) **high-latency links** (geostationary satellite ≈ 240–280 ms RTT) where retransmission costs an entire round trip per error; (3) **storage** (RAM, NAND flash) where a memory cell flips and "resending" is not an option. In these cases the sender must add *enough* redundancy that the receiver can mathematically reconstruct the corrupted bits itself. Hamming code exists to give the *minimum redundancy* that still corrects single-bit errors — it is the baseline every fancier FEC (Reed-Solomon, LDPC) generalizes.

## 2. How Does It Work?
Place parity bits at positions that are **powers of two** (1, 2, 4, 8, …). Each parity bit covers all data positions whose binary index has that parity position's bit set. At the receiver, recompute the parity bits; the pattern of mismatches — read as a binary number — gives the *position* of the error (0 = no error, 5 = error at position 5). Flip that bit and you have corrected a single-bit error. Hamming distance is the underlying guarantee: the code's minimum Hamming distance is 3, so it can detect up to 2 errors and correct 1.

## 3. When Is It Used?
- **Hamming(7,4)** and Hamming(15,11), (31,26): classic textbook schemes; the SECDED extension (add 1 overall parity) is the *industry* variant.
- **ECC RAM** (memory): every 64-bit DIMM word carries ~8 bits of SECDED Hamming code so a single flipped cell is corrected silently and double errors are reported (machine check exception).
- **NAND flash / SSD**: ECC per page (often BCH or LDPC, both descendants of block codes like Hamming); without it, flash bit error rates (10⁻⁴–10⁻⁷) would make SSDs unusable.
- **Deep-space and satellite links**: Voyager used a (255, 223) Reed-Solomon code; Hamming was the intellectual ancestor that made on-board correction practical.
- **Early modems and error-correcting protocols** and where retransmission is too costly.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: detection + retransmission (ARQ).* Perfectly good on clean, low-latency links — it's what Ethernet/TCP do. Rejected for Hamming's use cases because there is no back-channel (satellite one-way), retransmission latency is unacceptable, or "retransmission" doesn't exist for stored data.
- *Alternative: send each bit 3 times (triple modular redundancy) and take majority.* Corrects 1 error per 3 bits but costs 200% overhead. Hamming(7,4) corrects 1 error per 7 bits = 43% overhead for 4 data bits (and overhead falls as the block grows: Hamming(31,26) is only 16%). Hamming is *optimal*: it achieves the Hamming bound — you cannot correct 1 bit per block with less redundancy for a given block size.
- *Alternative: more powerful FEC (Reed-Solomon, LDPC, turbo codes).* Superior for long bursts and high error rates, but dramatically more complex and needed only when errors exceed single-bit-per-block. Hamming is the "minimum viable correction" chosen when errors are rare but must never be silently passed.
- *Alternative: 2D parity (VRC+LRC).* Corrects single-bit errors at 2·√n overhead and can't generalize cleanly to longer blocks. Hamming's binary-position trick is both cheaper and scalable.

## 5. Intuition
Think of **binary coordinates**. If you label bit positions in binary (1=`001`, 2=`010`, 3=`011`, …), a single flipped bit changes its own coordinates. Each parity bit is an independent "witness" that guards one coordinate bit across a subset of positions. When the receiver re-runs the witnesses, the set of witnesses that disagree forms the binary coordinates of the guilty position. So you never need to know *which* bit is wrong a priori — the disagreement pattern literally *spells out* the error position in binary.

## 6. Real-World Analogy
A **jury with question-specific witnesses**. For a 4-suspect case you convene three committees: committee P1 questions suspects {1,3,5,7}, P2 questions {2,3,6,7}, P4 questions {4,5,6,7} — each committee reports whether its group is "consistent." When one suspect lies, the *pattern* of committees that cry foul (say P2 and P4, = binary `110` = 6) uniquely identifies suspect #6. No one checks everyone; the overlapping witness design triangulates the liar from just the disagreeing committees.

## 7. Formal Definition
A linear block code where a message of *m* data bits is encoded into an *n*-bit codeword with *r = n − m* parity bits placed at positions 1, 2, 4, …, 2^(r−1). Parity bit *pᵢ* at position 2ⁱ covers all codeword positions *j* whose binary representation has bit *i* set. This yields minimum Hamming distance *d_min = 3*, so the code corrects all single-bit errors (and detects all double-bit errors when used in SECDED with one extra parity bit). The general forms Hamming(2^r − 1, 2^r − 1 − r) achieve the Hamming bound: 2^r − 1 ≥ n bits of syndrome space cover n error positions plus the no-error case.

## 8. Example
Encode message **1011** (m=4) with Hamming(7,4). Positions 1,2,4 are parity (p1,p2,p4); positions 3,5,6,7 are data (d1=1,d2=0,d3=1,d4=1):
```
pos:  1  2  3  4  5  6  7
      p1 p2 d1 p4 d2 d3 d4
bits: ?  ?  1  ?  0  1  1
```
- p1 covers pos {1,3,5,7} = 1,0,1 → even parity → **p1=0**.
- p2 covers pos {2,3,6,7} = 1,1,1 → three 1s → **p2=1**.
- p4 covers pos {4,5,6,7} = 0,1,1 → two 1s → **p4=0**.
Codeword = `0 1 1 0 0 1 1`. Now transmit and flip bit 6: received `0110011`→`0110111` (pos6 1→0). Receiver recomputes:
- p1 recalc covers {1,3,5,7}=0,1,0,1 → even → OK (0) → syndrome bit0=0.
- p2 recalc covers {2,3,6,7}=1,1,0,1 → three 1s → mismatch (1) → syndrome bit1=1.
- p4 recalc covers {4,5,6,7}=0,0,0,1 → one 1 → mismatch (1) → syndrome bit2=1.
Syndrome = `110`₂ = **6** → error at position 6 → flip it back to 1 → decoded data 1011. One bit corrected in place; no retransmission.

## 9. Internal Working
1. **Choose parameters**: for *m* data bits, smallest *r* with 2^r ≥ m + r + 1. m=4→r=3 (Hamming 7,4); m=11→r=4 (15,11); m=26→r=5 (31,26).
2. **Encode**: write data bits into non-power-of-two positions; compute each parity bit over its covering set (position's bit is set in index); transmit.
3. **Receive**: recompute all parity bits over the received codeword.
4. **Syndrome**: assemble mismatches as a binary number (P1 = LSB). 0 → accept; else flip the bit at that position.
5. **SECDED**: add an 8th overall parity bit covering the entire codeword. If syndrome = 0 and total parity OK → no error; syndrome ≠ 0 and total parity bad → single error (correct it); syndrome ≠ 0 but total parity OK → two errors (report, do NOT correct — correcting would introduce a third error).
6. **Hardware**: ECC RAM implements encode/check in the memory controller (or DIMM) — one extra clock of latency; the CPU never sees corrected single-bit errors.

## 10. Time Complexity
- Encode/check: O(n) — one XOR per covered bit per parity, i.e., r·(n/2) ≈ O(n) total, but in hardware it's a fixed fan-in XOR tree: constant time.
- Syndrome decode: O(1) in hardware (parallel parity trees) — ECC RAM adds ~1–2% latency.
- Overhead ratio: r/m → 3/4 = 75% for (7,4) but falls to 11/26 ≈ 42%, 5/26 ≈ 19% for (31,26). Trade-off: bigger blocks = lower overhead but only still correct 1 error per block.
- Correcting capacity: 1 bit per block always (for these basic Hamming codes) regardless of block size.

## 11. Advantages
- **No retransmission**: corrects in place — ideal for one-way, high-latency, and storage channels.
- **Optimal for its job**: achieves the Hamming bound; you cannot correct 1 error with fewer bits for a given block size.
- **Blazing fast in hardware**: parallel parity XOR trees make ECC nearly free (a few ns).
- **Transparent**: ECC RAM corrects silently; system performance is unaffected; only *double*-bit errors surface.
- **Simple, well-understood math**: linear algebra over GF(2); easy to implement and verify.
- **Easily extended**: SECDED (single-error-correct, double-error-detect) is the production form.

## 12. Disadvantages
- **Corrects only 1 bit per block**: two bit errors within one block are mis-corrected to a *third* wrong bit (without the SECDED extra parity) — arguably worse than no correction.
- **No burst protection**: adjacent errors (a burst of 2+) defeat it; real media (flash, radio) have bursts, so industry upgrades to Reed-Solomon/LDPC.
- **Overhead at small block sizes**: (7,4) wastes 75% extra; only efficient for large blocks.
- **Fixed block, not adaptive**: error rate higher than the code's capacity → silent mis-correction or data loss.
- **Detection-only is often enough**: on reliable links, the extra latency/complexity buys nothing over ARQ.

## 13. Interview Questions
1. **Q: What is Hamming distance and why does it matter?** A: The number of bit positions where two codewords differ. For a code, the *minimum* Hamming distance d_min bounds capability: detect up to d_min−1 errors, correct up to ⌊(d_min−1)/2⌋. Hamming code has d_min=3 → correct 1, detect 2.

2. **Q: Why are Hamming parity bits placed at powers of two?** A: So the syndrome — the binary number formed by which parity checks fail — directly encodes the error *position*. Power-of-two placement means each parity bit's coverage set = "positions whose index has this bit set," making the mismatch pattern equal to the error's binary address.

3. **Q: What is the Hamming bound / why is Hamming(7,4) optimal?** A: With *r* parity bits you get 2^r syndrome patterns; you need one for "no error" plus one per correctable position. For n=7, 2³=8 ≥ 1+7 → exactly tight: Hamming(7,4) achieves the bound, meaning no (7,4) code can do better.

4. **Q: Encode 1001 with Hamming(7,4) and show the codeword.** A: Data at pos 3,5,6,7 = 1,0,0,1. p1 covers {1,3,5,7}=1,0,1→p1=0. p2 covers {2,3,6,7}=1,0,1→p2=0. p4 covers {4,5,6,7}=0,0,1→p4=1. Codeword = `0010011`.

5. **Q: You receive `1010110` (Hamming 7,4). Is it valid? If not, fix it.** A: Recompute: p1 over {1,3,5,7}=1,1,1,0→odd→mismatch (1). p2 over {2,3,6,7}=0,1,1,0→even→ok(0). p4 over {4,5,6,7}=0,1,1,0→even→ok(0). Syndrome = `001`=1 → flip position 1 → valid codeword `0010110`, data = pos3,5,6,7 = 1,0,1,0.

6. **Q: TRICKY — A Hamming(7,4) codeword suffers two bit errors. What happens?** A: The syndrome will point to a *third* position (a "mis-correction"): the decoder flips the wrong bit, making three errors — worse than if it had detected and discarded. That's exactly why production memory uses SECDED: an overall parity bit distinguishes "1 real error" from "2 errors," and it *reports* (never corrects) the double error.

7. **Q: What is SECDED and where is it used?** A: Single-Error-Correct Double-Error-Detect: Hamming code + one overall parity bit (e.g., (72,64) ECC DIMMs). Syndrome zero + parity OK = clean; syndrome ≠ 0 + parity bad = single error (correct); syndrome ≠ 0 + parity OK = double error (panic/machine-check). Used in all ECC RAM.

8. **Q: SCENARIO — Your SSD's read error rate climbs. Why can't it just retransmit like Ethernet?** A: NAND flash is a storage medium: the "channel" is the cell array, and the only recovery is reading a block again (still may fail). With 1M cells per page and BER ~10⁻⁵, retry alone is hopeless; the controller must *correct* via on-die ECC. FEC is mandatory wherever the medium has no sender to resend from.

9. **Q: PRODUCTION — Why does ECC RAM add so little latency?** A: Because encode/check is a parallel XOR tree in the memory controller — O(1) depth, a couple of gate delays. The cost is mostly the extra bits (12.5% overhead on 64-bit words) and slightly more pins, not time.

10. **Q: How does Hamming distance change between "detect 3" and "correct 1"?** A: To detect up to *d* errors you need d_min ≥ d+1; to correct *t* you need d_min ≥ 2t+1. d_min=4 (SECDED) detects 3 or corrects 1 *and* detects 2. There's no code that corrects 1 and detects 3 with d_min=3.

11. **Q: TRICKY — A Hamming(7,4) system sends 4 data bits; why do 3 parity bits suffice for 7 positions?** A: 3 bits → 8 syndromes. Need 1 for "no error" + 7 for "error in position 1..7" = 8. Exactly enough — the count of *positions* matters, not the count of *data bits*, which is why the code is optimal.

12. **Q: What happens to correction when the medium produces bursts of errors?** A: Hamming's "1 bit per block" budget is blown; a burst of length b spanning a block mis-corrects or fails. Industry switches to Reed-Solomon (corrects byte/burst errors via polynomial evaluation) or LDPC (near-Shannon performance on flash/radio) for bursty channels.

13. **Q: SCENARIO — Live video over a geostationary satellite link (240 ms RTT) with occasional single-bit errors. ARQ or FEC, and why?** A: FEC. A single retransmission costs 480 ms of playback stall and jitter; Hamming-style or Reed-Solomon correction keeps the stream smooth. You'd still layer a small ARQ for catastrophic losses.

14. **Q: What's the trade-off between Hamming(7,4) and Hamming(31,26)?** A: Overhead: 75% vs 16%. But *both* correct only one error per block — a (31,26) block is more likely to contain 2+ errors under the same BER, so for a given bit error rate the big-block code may actually fail more often per data bit. This is the classic FEC block-size tension.

15. **Q: Can Hamming code detect more errors than it corrects?** A: Yes — with d_min=3 it detects up to 2 errors, corrects 1. Detection capacity is always d_min−1; correction capacity is ⌊(d_min−1)/2⌋. Used in *detect-only* mode (SECDED parity) it becomes a double-error detector.

16. **Q: How is Hamming code related to linear block codes and generator matrices?** A: Hamming codes are linear block codes: encoding is multiplication by a generator matrix G (n×m), and checking uses the parity-check matrix H (r×n). The syndrome is H·received. The "power-of-two parity" description is the classical manual form of the same linear algebra.

17. **Q: PRODUCTION — You see "Corrected error" counters climbing on a server's ECC DIMMs. Concern?** A: It's the ECC working as designed, but a climbing single-bit correction rate signals *aging hardware* — increasingly flaky DRAM cells, marginal voltage, or overheating. Watch the trend; when corrected errors accelerate or double-bit (UNCORRECTABLE) errors appear, replace the DIMM before data corruption.

18. **Q: Why do we say Hamming "corrects in place" — what are the alternatives at the protocol level?** A: Alternatives are retransmission (ARQ — costs RTT, needs back-channel) or "accept and pray" (drop or forward corrupt). In-place correction costs only the redundancy bits and decoder latency, making it the right tool for real-time and one-way channels.

## 14. Follow-Up Questions
1. **Q: How does a syndrome of `011` (binary) map to an error position?** A: Bit 0 (LSB) = P1 mismatch, bit 1 = P2, bit 2 = P4. `011` = 2+1 = 3 → error at position 3. The syndrome *is* the binary address of the error.

2. **Q: What is the (n,k,d) notation for Hamming(7,4)?** A: (7,4,3) — 7-bit codewords, 4 data bits, minimum distance 3.

3. **Q: Why does doubling block size keep overhead falling but correction power flat?** A: Parity bits grow logarithmically (need ~log₂ n positions), so r/n shrinks; but the code only guarantees one error per *block*, so longer blocks need a higher-quality medium.

4. **Q: In ECC memory, who performs the correction — CPU or controller?** A: The memory controller (integrated in the CPU for modern server CPUs), transparently; the CPU typically never learns about corrected single-bit errors unless you read the error counters.

## 15. Coding Example
```python
def hamming74_encode(msg: int) -> int:  # msg = 4-bit data, returns 7-bit codeword
    # place data at positions 3,5,6,7
    cw = [0]*8
    cw[3], cw[5], cw[6], cw[7] = (msg >> 3)&1, (msg >> 2)&1, (msg >> 1)&1, msg & 1
    cw[1] = cw[3] ^ cw[5] ^ cw[7]      # P1 covers {1,3,5,7}
    cw[2] = cw[3] ^ cw[6] ^ cw[7]      # P2 covers {2,3,6,7}
    cw[4] = cw[5] ^ cw[6] ^ cw[7]      # P4 covers {4,5,6,7}
    out = 0
    for i in range(1, 8):
        out |= cw[i] << (i - 1)
    return out

def hamming74_correct(cw: int) -> tuple[int, int]:  # returns (corrected, position or 0)
    bits = [(cw >> (i - 1)) & 1 for i in range(8)]
    s1 = bits[1] ^ bits[3] ^ bits[5] ^ bits[7]
    s2 = bits[2] ^ bits[3] ^ bits[6] ^ bits[7]
    s4 = bits[4] ^ bits[5] ^ bits[6] ^ bits[7]
    pos = s1 | (s2 << 1) | (s4 << 2)
    if pos:
        cw ^= (1 << (pos - 1))          # flip the guilty bit
    data = ((cw >> 2) & 8) | ((cw >> 3) & 4) | ((cw >> 3) & 2) | (cw & 1)
    return cw, pos

msg = 0b1011
cw = hamming74_encode(msg)
received = cw ^ (1 << 5)                 # flip bit position 6 (index 5)
fixed, pos = hamming74_correct(received)
assert fixed == cw and pos == 6
print(f"encoded={cw:07b} corrupted={received:07b} syndrome={pos} fixed={fixed:07b}")
```
```python
# 2D parity grid — the intuition behind Hamming (VRC + LRC)
grid = [[1, 0, 1, 0], [1, 1, 0, 1], [0, 1, 1, 0]]  # 3 rows x 4 cols data
rows = [sum(r) % 2 for r in grid]      # row parities
cols = [sum(grid[r][c] for r in range(3)) % 2 for c in range(4)]  # col parities
# flip cell (1,2) and re-detect: mismatched row 1 AND column 2 → error at (1,2)
```
```bash
# See ECC corrections on a Linux server
edac-util --status | head                          # EDAC corrected/uncorrected error counts
dmesg | grep -i "mce\|machine check\|edac"         # machine-check events
sudo dmidecode -t memory | grep -i ecc             # is the DIMM ECC-capable?
grep -c "mce: \[Hardware Error\]" /var/log/kern.log
```

## 16. Industry Usage
- **ECC RAM (all servers)**: 64-bit words + 8 ECC bits (72-bit DIMMs) implement SECDED in the memory controller; corrected single-bit errors are invisible, uncorrectable ones raise machine-check exceptions. Google/Meta/AWS run *all* production memory with ECC.
- **NAND flash/SSDs**: on-die + controller ECC (BCH/LDPC) per 4-16KB page; raw cell BER ~10⁻⁵ is reduced to ~10⁻¹⁵ end-to-end by correction.
- **Satellite/deep-space**: Voyager/New Horizons use Reed-Solomon + convolutional concatenated codes — direct descendants of Hamming's block-coding idea.
- **Error-correcting codes in high-speed links**: PCIe Gen4/Gen5, DDR5 use on-die ECC and link FEC.
- **Telecom (OTN/SDH)**: Reed-Solomon FEC on long-haul optical spans where regenerators can't retransmit.

## 17. References
- Kurose & Ross, *Computer Networking: A Top-Down Approach*, 8th ed., §6.2 (Error Detection and Correction).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §3.2.3 (Forward Error Correction).
- R. W. Hamming, "Error Detecting and Error Correcting Codes," *Bell System Technical Journal*, 1950.
- Intel, *ECC Memory — A Guide for R&D Managers* — https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/ecc-memory-paper.pdf
- Microchip AN594, "Hamming Code for Error Correction" — https://ww1.microchip.com/downloads/en/AppNotes/00594c.pdf
- Wikipedia, Hamming Code — https://en.wikipedia.org/wiki/Hamming_code

## 18. Cheat Sheet
- d_min=3 → correct 1 / detect 2; d_min=4 (SECDED) → correct 1 + detect 2.
- Parity bits at positions 1,2,4,8… (powers of two); data in the rest.
- Pᵢ covers all positions with bit i set in their index.
- Syndrome (receiver) = binary number formed by failed parity checks = error position.
- To fix: flip the bit at the syndrome position. Syndrome 0 = clean.
- Parameters: smallest r with 2^r ≥ m + r + 1 → (7,4),(15,11),(31,26).
- Hamming(7,4) is optimal (Hamming bound); overhead r/m falls as block grows.
- Production form: SECDED in ECC RAM (72-bit DIMMs = 64 data + 8 ECC).
- Hamming corrects 1 error/block; bursts and 2+ errors need Reed-Solomon/LDPC.
- Hamming is a *linear block code* = generator matrix G, parity-check H, syndrome = H·r.

## 19. Quiz
1. Hamming(7,4) places parity at: a) positions 1,2,3 b) positions 1,2,4 c) positions 2,4,6 d) end of block → **b**
2. Minimum distance of plain Hamming code: a) 2 b) 3 c) 4 d) 5 → **b**
3. To correct t errors you need d_min ≥: a) t+1 b) 2t+1 c) 2t d) t → **b**
4. SECDED means: a) correct 1, detect 1 b) correct 1, detect 2 c) correct 2 d) detect only → **b**
5. Syndrome `101` in Hamming(7,4) means error at position: a) 5 b) 4 c) 7 d) 3 → **a**
6. A syndrome of 0 means: a) one error b) no error c) two errors d) parity wrong → **b**
7. Which is the production ECC scheme in server memory? a) parity b) Hamming(7,4) c) SECDED (72,64) d) MD5 → **c**
8. Hamming(31,26) has overhead ≈: a) 75% b) 19% c) 50% d) 6% → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-a, 6-b, 7-c, 8-b.

## 20. Flashcards
- **Q: Why are Hamming parity bits at powers of two?** → **A:** The failed-parity pattern (syndrome) then equals the binary position of the error.
- **Q: What can a d_min=3 code do?** → **A:** Detect 2 errors or correct 1.
- **Q: How do you correct from a syndrome?** → **A:** Flip the bit at the syndrome's position; syndrome 0 = no error.
- **Q: What is SECDED?** → **A:** Hamming + 1 overall parity: correct single, detect double errors (ECC RAM).
- **Q: Why not use Hamming for bursts?** → **A:** It corrects only 1 bit/block; bursts need Reed-Solomon/LDPC.
- **Q: Why is (7,4) optimal?** → **A:** 3 parity bits give 8 syndromes = 1 (no error) + 7 (positions) → Hamming bound met.

## 21. Revision
Hamming code is the canonical forward error correction: it corrects one bit error per block in place, eliminating retransmission for one-way, high-latency, and storage channels. Parity bits sit at power-of-two positions; each guards a subset of positions (those whose index has that bit set). The receiver recomputes the parities and the mismatch pattern — the **syndrome** — is the binary address of the error; flip that bit. d_min = 3 gives correct-1/detect-2; SECDED adds an overall parity for production ECC RAM (72-bit DIMMs), where a nonzero syndrome with valid total parity means "double error, report, don't correct." Overhead falls from 75% ((7,4)) to ~19% ((31,26)) as blocks grow, but correction power stays 1 bit/block, so bursty media upgrade to Reed-Solomon/LDPC. Anchor: *syndrome = binary position of the flipped bit*.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is Hamming distance and what can d_min=3 do?" | 7 / 13-Q1 |
| "Encode/decode/correct a Hamming(7,4) codeword" | 8 / 13-Q4,5 |
| "Why powers of two for parity bits?" | 13-Q2 |
| "What is SECDED and where is it used?" | 13-Q7 / 16 |
| "What happens with two errors in one block?" | 13-Q6 |
| "Why can't storage just retransmit?" | 13-Q8 / 4 |
| "Why is (7,4) optimal?" | 13-Q3 |
| "FEC vs ARQ — when to use each?" | 4 / 13-Q13 |
| "ECC error counters rising — what does it mean?" | 13-Q17 |
