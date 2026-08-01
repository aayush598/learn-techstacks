# Encoding and Modulation

> **TL;DR**: Encoding (line coding) maps bits to voltage/light levels on a wire for *baseband* transmission, while modulation maps bits onto a carrier's amplitude/frequency/phase for *passband*/radio transmission — both exist to make the signal survive the channel's bandwidth, noise, and clock-recovery constraints, with the trade-off between more levels (faster) and robustness (safer).

## 1. Why Does This Exist?
A stream of bits doesn't just transmit itself: you must choose *which physical states* represent 0 and 1 and *how to keep the receiver's clock aligned*. This is the physical layer's conversion step. Without good encoding, you get (a) **no clock**: runs of identical bits give the receiver no transitions to lock onto, so sampling drifts; (b) **DC/baseline wander**: long runs of 0s or 1s shift the average voltage, confusing the decision threshold; (c) **wasted bandwidth**: naive signaling uses more spectrum than necessary; (d) **noise sensitivity**: adjacent levels too close → bit errors. Modulation exists because baseband signals can't ride a radio carrier or fiber's light *directly* — you must move the information onto a high-frequency carrier (passband). Encoding and modulation are the two ways bits become waveforms, and choosing them is the core of every PHY standard.

## 2. How Does It Work?
**Line coding (baseband)**: map each bit/group of bits to a voltage level over one symbol period — NRZ (level = bit), RZ (pulse returns to zero), Manchester (transition encodes bit — guarantees clock), 4B5B/8B10B (map 4→5 or 8→10 bits to guarantee transitions and DC balance), 64B66B (10G Ethernet — 2 sync bits + 64 scrambled data). **Modulation (passband)**: vary a carrier wave — ASK (amplitude), FSK (frequency), PSK (phase), QAM (amplitude+phase combined, e.g., 16-QAM = 4 levels × 4 phases = 16 points = 4 bits/symbol). The receiver does the inverse: demodulate (extract baseband from carrier) and decode (map levels to bits), using clock recovery and equalization.

## 3. When Is It Used?
- **NRZ/NRZI**: USB 1.x, SATA, and simple serial links (with scrambling for balance).
- **Manchester**: classic 10BASE-T Ethernet and RFID — self-clocking, robust but 50% bandwidth efficiency.
- **4B5B**: 100BASE-TX (Fast Ethernet) and FDDI — guarantees transitions, ~20% overhead.
- **8B10B**: 1 GbE, PCIe 1.x, SATA, Fibre Channel, USB 3.0 — DC balance + transitions, 25% overhead.
- **64B66B**: 10/25/40/100 GbE — 3% overhead with scrambling + a sync header.
- **PAM-5/PAM-4**: 1000BASE-T (5 levels), 400G optical / 50G+ SerDes (4 levels = 2 bits/symbol).
- **QAM**: DSL (VDSL2 up to 4096-QAM), cable (DOCSIS), WiFi (up to 1024/4096-QAM), cellular (256-QAM) — the workhorse for squeezing bits/Hz.
- **PSK/FSK**: BLE, Bluetooth, RFID, satellite — robust where SNR is marginal.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: no encoding — send raw voltage per bit.* Raw NRZ is the simplest but a long run of 0s destroys clock recovery and causes DC wander; real standards add transitions (Manchester, 4B5B, 8B10B, 64B66B) at the cost of overhead. Encoding is the price of reliability.
- *Alternative: always encode with more bits for guaranteed transitions (Manchester everywhere).* Manchester needs 2 symbols/bit → halves throughput; 8B10B needs 25% overhead. As media improved, cheaper encodings with scrambling (64B66B: 3% overhead) won — the evolution tracks the SNR/bandwidth of the channel.
- *Alternative: just use more levels (bigger M-QAM) instead of more bandwidth.* Tempting (more bits/symbol) but level separation shrinks → more BER for the same SNR; and Shannon caps total bits. The optimum balances levels vs SNR — real systems pick the largest M-QAM the link's SNR supports (adaptive modulation in cellular/DSL).
- *Alternative: put the data on a carrier without shaping.* Modulation isn't optional for radio/fiber — a baseband signal's spectrum doesn't match the medium's passband; you *must* translate frequencies. The choice is which carrier scheme uses the channel best.

## 5. Intuition
Encoding is **writing in Morse code**: you have only two states (dot/dash = level), but you must make sure the reader can tell when one letter ends and the next begins (transitions = clock). Manchester writes every bit as a *change* (up-to-down = 1) so the reader never loses the beat. 8B10B is like padding messages so no word is ever all dots (DC balance). Modulation is **switching radio stations**: the baseband signal (your voice) must be placed on a carrier frequency so it can travel far; AM/PM/FM differ in *what you wiggle*. QAM wiggles both volume and phase simultaneously — like sending information in both the loudness and the timing of a drum, getting 2 dimensions of data per beat.

## 6. Real-World Analogy
Encoding = **a drummer keeping a beat**. If you play only "long silence" (all 0s), the dancers lose the rhythm (clock drift). So you add a tap every so often (scrambling/stuffing), or make every note move (Manchester), so the beat is always findable. Modulation = **a chef seasoning a dish on different pans**: the same recipe (data) is cooked on a copper pan, a fiber pan, or a radio pan — the "heat level" (carrier frequency) and "seasoning style" (AM/FM/PM/QAM) change, but the recipe is the same. QAM is seasoning with both salt *and* pepper at once to carry more flavor per taste.

## 7. Formal Definition
**Line encoding** (baseband): a one-to-one mapping from bit sequences to sequences of signal levels over symbol periods; quality criteria: DC balance (zero average), transition density (clock recovery), spectral efficiency, and error margin. Examples: NRZ (level = bit), NRZI (transition = 1), RZ (return to zero), Manchester (XOR of NRZ with clock; mid-bit transition always), 4B5B (4→5-bit block code), 8B10B (8→10, 6/5 weight to guarantee ≤5 or ≤4 consecutive identical bits), 64B66B (2-bit sync + 64 scrambled bits, run length ≤ 65). **Modulation** (passband): encoding bits onto a carrier c(t) = A·cos(2πft + φ): ASK varies A, FSK varies f, PSK varies φ (e.g., BPSK/QPSK = 1/2 bits/symbol), QAM combines A and φ into a constellation of M points (M-QAM → log₂(M) bits/symbol). **Baud (symbol) rate** = number of symbols/sec; **bit rate** = baud × log₂(M); bandwidth roughly ∝ baud for the scheme.

## 8. Example
**Manchester vs NRZ for the bit sequence 010.** 
- NRZ: `0` = low, `1` = high, `0` = low → waveform: low, high, low. Problem: a long run (000...) has no transitions.
- Manchester: each bit gets a mid-bit transition: `1` = low→high, `0` = high→low. For `010`: high→low | low→high | high→low — a transition every half-bit → clock always recoverable. Cost: 2 symbols/bit (50% efficiency).

**8B10B example.** Encode the byte `0x80` (`10000000`): 8B10B looks up the 10-bit codepoint (e.g., `1001110100` + running disparity) so the count of 1s and 0s stays balanced and no run exceeds 4 identical bits. Cost: 25% overhead but robust DC + clock.

**16-QAM.** Constellation = 4 amplitudes × 4 phases = 16 points = 4 bits/symbol. On a 6 MHz cable channel at 6.75 Mbaud → 6.75 × 4 = 27 Mbps (classic DOCSIS number).

## 9. Internal Working
1. **Scrambling**: long bit runs are XORed with a pseudo-random sequence to break patterns before encoding (keeps DC balance without full block coding overhead).
2. **Block coding (4B5B/8B10B)**: lookup table maps input bits to coded words; running disparity (cumulative excess of 1s over 0s) selects alternate codepoints to balance the line.
3. **Serialization + clock**: parallel data → serial stream with the chosen line code; the receiver's PLL locks to the transitions (clock/data recovery, CDR).
4. **Modulation chain (radio/fiber)**: bits → symbol mapping (constellation) → pulse shaping (raised cosine) → I/Q mixing onto carrier → power amplifier; receiver: demodulation (mix down), matched filter, decision (nearest constellation point), demap → bits.
5. **Adaptive modulation**: measure SNR (BER, error vector magnitude) and drop to a smaller M-QAM (fewer bits/symbol) when the channel degrades — the system trades rate for reliability continuously.
6. **Equalization**: DSP removes ISI (channel memory) at the receiver — why modern SerDes/coherent optics need heavy DSP rather than just better levels.

## 10. Time Complexity / Performance
- Encoding/decoding: O(n) bits, but in *silicon* at line rate (1 ns/symbol at 1 Gbaud). Block codes are LUT lookups: O(1) per byte.
- **Overhead**: Manchester 100%, 4B5B 25%, 8B10B 25%, 64B66B ~3%, QAM 0% (no redundancy, relies on SNR).
- **Spectral efficiency**: bits/sec per Hz — BPSK 1, QPSK 2, 16-QAM 4, 64-QAM 6, 256-QAM 8, 4096-QAM 12 (before FEC).
- **BER vs SNR**: higher M-QAM → BER rises steeply at the same SNR (needs ~3 dB more per doubling of bits) — the trade-off table every PHY standard balances.

## 11. Advantages
- **Clock recovery**: Manchester/block codes guarantee transitions → reliable sampling.
- **DC balance**: 8B10B/64B66B prevent baseline wander — important for AC-coupled receivers.
- **Higher throughput**: QAM packs multiple bits per symbol → spectral efficiency (cable/DSL/WiFi/cellular hit hundreds of Mbps on narrow channels).
- **Robustness options**: FSK/PSK survive low SNR (Bluetooth, satellite); adaptive modulation adjusts in real time.
- **Standardized, interoperable**: PHYs are hard specs — any two compliant devices link automatically.

## 12. Disadvantages
- **Overhead**: Manchester (100%), 4B5B/8B10B (25%) reduce effective rate.
- **Complexity**: 8B10B/64B66B/QAM need serious DSP (equalization, FEC) in silicon.
- **SNR hunger**: high-order QAM needs clean channels; a 3 dB SNR drop forces a 2× rate cut (cellular handovers, DSL fading).
- **Latency**: coding/decoding and interleaving add delay (bad for real-time voice/control on heavy FEC).
- **Not a silver bullet**: beyond Shannon, no encoding helps; adding levels without SNR is pointless.

## 13. Interview Questions
1. **Q: What's the difference between encoding and modulation?** A: Encoding (line coding) maps bits to levels on a *baseband* wire/light signal. Modulation maps bits onto a *carrier wave* (amplitude/frequency/phase) so the data can ride a passband channel (radio, fiber DWDM, cable). Encoding shapes the baseband; modulation moves it to a band.

2. **Q: Why is Manchester encoding "self-clocking"?** A: Every bit has a mid-bit transition (1 = low→high, 0 = high→low), so the receiver always has a transition to lock its clock to — no long runs of identical bits. Cost: 2 symbols/bit → 50% bandwidth efficiency.

3. **Q: What problem does 8B10B solve and what's its overhead?** A: It maps 8-bit groups to 10-bit codes with ≤5 (or ≤4) consecutive identical bits and balanced 1s/0s (running disparity) — guaranteeing clock transitions and DC balance. Overhead 25%; used in 1 GbE, PCIe 1.x, SATA.

4. **Q: Why does 10G Ethernet use 64B66B instead of 8B10B?** A: 8B10B's 25% overhead would be 2.5 Gbaud of waste at 10G; 64B66B uses just 2 sync bits + 64 scrambled data bits (~3% overhead) while still bounding run length and enabling clock recovery via scrambling + sync header.

5. **Q: What is the difference between ASK, FSK, PSK, and QAM?** A: ASK varies amplitude, FSK varies frequency, PSK varies phase, QAM varies amplitude AND phase together (a constellation grid) — QAM packs more bits/symbol (16-QAM = 4 bits). BPSK=1, QPSK=2, 16QAM=4, 256QAM=8 bits/symbol.

6. **Q: TRICKY — 256-QAM needs how much more SNR than QPSK for the same BER?** A: Each doubling of constellation size costs roughly 3 dB SNR. 256-QAM (8 bits) vs QPSK (2 bits) is 3 doublings of bits → ~6-9 dB more, and practically the SNR requirement scales ~2^(n) for the outermost points. That's why high-order QAM is only used on clean links.

7. **Q: What is "baud" and how does it relate to bit rate?** A: Baud = symbol changes/sec. Bit rate = baud × log₂(M). 2400 baud with 16-QAM (4 bits) = 9600 bps. Bandwidth is roughly ∝ baud, so more bits/symbol = more efficient use of spectrum.

8. **Q: SCENARIO — A 100BASE-TX link (4B5B) is failing BER on a long cable run. Why might the encoding matter?** A: 4B5B's MLT-3 signaling is bandwidth-efficient but sensitive to attenuation/ISI; at the edge of reach, symbols blur and the receiver's eye closes. Diagnosis: cable quality/length, crosstalk (nearby pairs), and check the eye diagram — the encoding is fine, the *channel* is the problem.

9. **Q: What does "DC balance" mean and why does a receiver care?** A: Over time the signal's average should be zero (equal 1s/0s). Without balance, an AC-coupled receiver's decision threshold drifts (baseline wander) and misreads bits. 8B10B enforces balance via running disparity.

10. **Q: What is adaptive modulation and where is it used?** A: The transmitter picks the largest M-QAM the current SNR supports and drops to a smaller one when SNR falls. Used in cellular (CQI feedback), WiFi (MCS selection), DSL, and cable — trading rate for reliability in real time.

11. **Q: PRODUCTION — Your WiFi link drops from 1300 Mbps to 70 Mbps a few meters from the AP. What's the mechanism?** A: The link's adaptive modulation (MCS) drops as SNR falls: fewer spatial streams, lower-order QAM, and the AP may add protection. Check channel interference and RSSI; the rate you see is the negotiated MCS, not the "speed" — distance + attenuation + interference drive the encoding down.

12. **Q: What is QPSK and how does it differ from BPSK?** A: QPSK encodes 2 bits per symbol using 4 phase states (0°, 90°, 180°, 270°); BPSK encodes 1 bit with 2 phases. QPSK doubles spectral efficiency for ~the same bandwidth but is more SNR-sensitive.

13. **Q: TRICKY — Manchester has 100% overhead. When is it still used today?** A: Where robustness trumps throughput: classic 10BASE-T Ethernet, RFID, and low-power serial links where clock recovery must be foolproof without a PLL. It's the "guaranteed clock" trade-off.

14. **Q: What is the relationship between bandwidth and baud rate?** A: Bandwidth is roughly proportional to baud (for a given pulse shape); Nyquist says max baud = 2B. So bandwidth caps symbols/sec, and modulation (bits/symbol) caps how many bits ride each symbol — together giving the capacity.

15. **Q: How does QAM encode both amplitude and phase?** A: Each constellation point = (amplitude, phase) pair = an I/Q vector; the receiver measures the received I/Q and chooses the nearest point. 16-QAM has 16 points (4 amplitudes × 4 phases) = 4 bits/symbol. More points = closer spacing = more BER at fixed SNR.

16. **Q: SCENARIO — You must carry 1 Gbps over existing Cat5e. What's the encoding trick?** A: 1000BASE-T: 4 pairs in parallel, PAM-5 (5 levels = ~2.3 bits/symbol), 125 Mbaud per pair, with echo cancellation and equalization. It exploits parallel pairs + DSP rather than raw bandwidth — the answer is "multi-level, multi-pair, heavily equalized."

17. **Q: What is scrambling in the context of line codes?** A: XORing the data with a pseudo-random sequence to break up long runs of identical bits *before* encoding — so the encoder sees a "random-looking" stream with plenty of transitions, without adding block-code overhead (used in 64B66B and PCIe).

18. **Q: Why does FEC always accompany high-order QAM in real systems?** A: High-order QAM's BER curve is steep; FEC (Reed-Solomon/LDPC) adds a few % overhead but flattens the error rate, letting the system push to the Shannon limit. Without FEC, 256/4096-QAM would be unusable at the SNR real channels provide.

## 14. Follow-Up Questions
1. **Q: What is a constellation diagram and what does the "eye" tell you?** A: A scatter plot of received I/Q symbols; tight clusters = good decisions, spread/rotated = noise/phase error. The eye diagram (time domain) shows ISI/clock margin. Both are the physical-layer health checks.

2. **Q: What is "run length" and why cap it?** A: The maximum consecutive identical bits; long runs = no transitions = clock drift and DC drift. 8B10B caps at 5 (or 4 with running disparity); 64B66B caps at 65 after scrambling.

3. **Q: What's the difference between a block code (8B10B) and a convolutional/FEC code?** A: 8B10B is *line coding* — for clock/DC, no error correction. FEC (convolutional/LDPC) adds parity for *error correction* (Part 05's Hamming section). They're orthogonal layers of the PHY.

4. **Q: Why do fiber links use QAM (coherent 16-QAM) but Ethernet copper uses PAM?** A: Both are "more levels per symbol," but fiber uses phase too (coherent I/Q on the optical carrier) while copper uses amplitude-only PAM because phase is unstable on twisted pair. Same goal, medium-appropriate implementation.

## 15. Coding Example
```python
import math

def bits_per_symbol(scheme: str) -> int:
    return {"BPSK":1, "QPSK":2, "8PSK":3, "16QAM":4, "64QAM":6, "256QAM":8, "1024QAM":10, "4096QAM":12}[scheme]

def bit_rate(baud: float, scheme: str) -> float:
    return baud * bits_per_symbol(scheme)

print(f"6.75 Mbaud 16-QAM: {bit_rate(6.75e6, '16QAM')/1e6:.1f} Mbps")   # 27.0
print(f"1200 baud BPSK: {bit_rate(1200, 'BPSK')} bps")

def manchester_encode(bits: str) -> str:
    """Manchester: 1 = low->high, 0 = high->low (mid-bit transition)."""
    out = []
    for b in bits:
        out.append("LH" if b == "1" else "HL")
    return "".join(out)

def manchester_decode(wave: str) -> str:
    bits, i = "", 0
    while i < len(wave):
        pair = wave[i:i+2]
        bits += "1" if pair == "LH" else "0"
        i += 2
    return bits

enc = manchester_encode("010")
print(f"Manchester('010') = {enc} (transitions every half-bit)")
assert manchester_decode(enc) == "010"

# Simplified 8B10B balance check: 1s vs 0s must stay within 1
def balanced(word: str) -> bool:
    return abs(word.count("1") - word.count("0")) <= 2
print("8B10B sample balanced:", balanced("1010110100"))
```
```bash
# See the negotiated PHY encoding/mode on real links
ethtool eth0 | grep -E "Speed|Duplex"                  # negotiated rate (implies PAM/QAM)
sudo ethtool -S eth0 | grep -Ei "symbol|signal"         # physical-layer error counters
# WiFi modulation in use:
iw dev wlan0 link | grep -E "tx bitrate|MCS"            # e.g., MCS 9 = 256-QAM 3/4
iw phy phy0 info | grep -A2 "VHT" | head                # supported MCS/modulation
# PCIe encoding (8B10B / 128B130B):
lspci -vv | grep -i "LnkSta:" | head -2                 # negotiated width/speed
```
```bash
# Spectrum / noise check (unguided channel)
iw dev wlan0 survey dump | grep -E "noise|busy"         # channel noise floor (dBm)
```

## 16. Industry Usage
- **Ethernet PHY silicon**: 100BASE-TX (4B5B+MLT-3), 1000BASE-T (PAM-5 + echo cancel), 10GBASE-T (PAM-16 + DSP), 400G optical (PAM-4, 64B66B).
- **Coherent optics**: 400G/800G use QPSK/16-QAM with DSP — the physical limit push in long-haul.
- **Cellular**: 5G NR uses OFDM + adaptive 256-QAM with LDPC FEC; massive MIMO multiplies spatial streams.
- **WiFi**: 802.11ac/ax/be up to 1024/4096-QAM with MCS-index rate adaptation and LDPC FEC.
- **Cable/DSL**: DOCSIS 3.1 (4096-QAM), VDSL2/G.fast (4096-QAM) with FEC — squeezing bits/Hz on legacy copper.
- **Storage/compute interconnects**: PCIe 5.0 (128B130B, PAM-4), NVMe over PCIe — the same encoding choices in the data center.

## 17. References
- IEEE Std 802.3-2022 (Ethernet PHYs: 4B5B, 8B10B, 64B66B, PAM) — https://standards.ieee.org/ieee/802.3/10422/
- IEEE Std 802.11-2020 (OFDM/QAM/MCS) — https://standards.ieee.org/ieee/802.11/7028/
- Kurose & Ross, *Computer Networking*, 8th ed., §1.3 (Physical Media), §6 (link).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §2.4 (Encoding) — detailed line-code table.
- Stallings, *Data and Computer Communications*, Ch. 5 (Signal Encoding Techniques), Ch. 6 (Digital Data Communication Techniques).
- PCI-SIG, PCIe Base Spec (128B/130B, PAM-4) — https://pcisig.com/

## 18. Cheat Sheet
- Encoding = baseband levels (NRZ, RZ, Manchester, 4B5B, 8B10B, 64B66B, PAM). Modulation = carrier (ASK/FSK/PSK/QAM).
- Manchester: self-clocking, 100% overhead. 8B10B: 25% overhead, DC balance, runs ≤ 5. 64B66B: 3% overhead.
- QAM bits/symbol: BPSK 1, QPSK 2, 16QAM 4, 64QAM 6, 256QAM 8, 4096QAM 12.
- Bit rate = baud × log₂(M).
- Scrambling breaks long runs; block codes guarantee transitions/balance.
- High M-QAM needs ~3 dB more SNR per extra bit/symbol → adaptive modulation.
- 1000BASE-T: 4 pairs × PAM-5 × 125 Mbaud. 10GBASE-T: PAM-16 + DSP.
- Every real QAM system uses FEC (LDPC/RS) to reach near-Shannon.
- Eye diagram/constellation = PHY health; equalization fights ISI.

## 19. Quiz
1. Manchester encoding cost: a) 25% b) 50% c) 100% d) 0% → **c**
2. 8B10B overhead: a) 10% b) 25% c) 3% d) 50% → **b**
3. 64B66B overhead: a) 25% b) 3% c) 10% d) 0% → **b**
4. 16-QAM bits per symbol: a) 2 b) 3 c) 4 d) 6 → **c**
5. 64-QAM bits per symbol: a) 4 b) 6 c) 8 d) 12 → **b**
6. 2400 baud × 16-QAM =: a) 2400 bps b) 4800 c) 9600 d) 19200 → **c**
7. Which guarantees clock via mid-bit transition? a) NRZ b) Manchester c) 8B10B d) QAM → **b**
8. Higher M-QAM requires: a) less SNR b) more SNR c) same SNR d) less bandwidth only → **b**

**Answers**: 1-c, 2-b, 3-b, 4-c, 5-b, 6-c, 7-b, 8-b.

## 20. Flashcards
- **Q: Encoding vs modulation?** → **A:** Encoding maps bits to baseband levels; modulation puts them on a carrier (passband) for radio/fiber/cable.
- **Q: Why Manchester?** → **A:** Self-clocking (mid-bit transition), guaranteed clock; costs 100% overhead.
- **Q: What does 8B10B guarantee?** → **A:** Transitions + DC balance (runs ≤ 5), 25% overhead; 1 GbE/PCIe/SATA.
- **Q: Why 64B66B at 10G+?** → **A:** ~3% overhead vs 8B10B's 25%; uses scrambling + sync header.
- **Q: Bits per symbol for QPSK / 16-QAM / 256-QAM?** → **A:** 2 / 4 / 8.
- **Q: Why does QAM need FEC?** → **A:** Steep BER curve; FEC flattens it and reaches near-Shannon capacity.
- **Q: What is adaptive modulation?** → **A:** Pick the largest M-QAM the SNR supports, drop on bad channels (cellular/WiFi/DSL).

## 21. Revision
Encoding shapes the *baseband* signal (NRZ, Manchester for guaranteed clock, 4B5B/8B10B for transitions + DC balance at 25% overhead, 64B66B at 3%, PAM for multilevel). Modulation moves bits onto a *carrier*: ASK/FSK/PSK and QAM (amplitude+phase), where bits/symbol = log₂(M): BPSK 1, QPSK 2, 16-QAM 4, 64-QAM 6, 256-QAM 8. Bit rate = baud × log₂(M); higher order needs ~3 dB more SNR per bit/symbol, so systems use adaptive modulation + FEC (LDPC/RS) to reach near-Shannon. Real-world anchors: Manchester = 10BASE-T/RFID; 8B10B = 1 GbE/PCIe/SATA; 64B66B = 10G+ Ethernet; PAM-5 = 1000BASE-T; 256-QAM = WiFi/cellular. Anchor: *encoding = how bits look on the wire; modulation = how they ride a carrier; more levels = faster but more fragile.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Encoding vs modulation?" | 13-Q1 / 7 |
| "Why Manchester / self-clocking?" | 13-Q2 |
| "What does 8B10B / 64B66B do?" | 13-Q3,4 |
| "ASK/FSK/PSK/QAM differences?" | 13-Q5 |
| "Baud vs bit rate?" | 13-Q7 |
| "Why does 256-QAM need more SNR?" | 13-Q6,12 |
| "What is adaptive modulation?" | 13-Q10 |
| "WiFi rate drop near the AP — why?" | 13-Q11 |
| "How does 1 GbE fit on Cat5e?" | 13-Q16 |
| "Why FEC with high-order QAM?" | 13-Q18 |
