# Signals: Analog, Digital, and Data Communication

> **TL;DR**: Data communication turns information into signals — analog signals vary continuously (perfect for a real physical medium) while digital signals use discrete levels (immune to noise) — and the physical layer's whole job is converting between the two while managing bandwidth, noise, and clocking so a receiver can reconstruct the exact bits that were sent.

## 1. Why Does This Exist?
Computers produce discrete bits (0/1), but every real medium — a copper wire's voltage, a fiber's light, a radio's electromagnetic wave — is an *analog* phenomenon that varies continuously over time. Information must be encoded onto a physical signal for transmission, and the receiver must decode it back into bits. This is the fundamental problem the physical layer exists for: **turning data into signals and back**, reliably, fast, and cheaply. If this conversion is done badly, everything above (Part 05's framing, Part 03's TCP) operates on garbage. The physics imposes hard limits (noise, bandwidth, attenuation), and understanding signals is what makes those limits — and the Nyquist/Shannon bounds — intuitive rather than magic formulas.

## 2. How Does It Work?
A signal is a function of time with measurable properties: **amplitude** (strength/height), **frequency** (cycles per second, Hz), **phase** (offset of the cycle), and **period** (time per cycle). Data is encoded by varying one or more of these — amplitude modulation, frequency shift, phase shift. A **digital signal** is a discrete-level approximation (e.g., 0 V = 0, 5 V = 1) built from many constituent frequencies; **analog signaling** (like a phone voice) carries continuous values. The sender converts bits → electrical/optical/radio signal (encoding), the channel carries it, and the receiver samples + decodes (with clock recovery from transitions). Because noise adds random voltage to the signal, the *distance between levels* (and the receiver's decision threshold) determines how many errors occur.

## 3. When Is It Used?
- **Every physical link**: Ethernet PHY converts bits to voltage/light; WiFi converts bits to RF modulation; cellular converts to QAM over air; DSL over twisted pair; satellite over microwave.
- **Telephony/audio**: the classic analog-to-digital case — POTS voice is sampled at 8 kHz (Nyquist for 4 kHz voice) into 8-bit PCM → 64 kbps (the "digital signal" of T1/E1).
- **Serial data**: USB, PCIe, SATA, UART all use line-coded digital signals with clock recovery.
- **Sensor/control**: industrial 4-20 mA loops, telemetry — where analog sensors feed ADCs.
- **Broadcast**: analog radio/TV (legacy) vs digital (DVB, ATSC, digital radio) — the move to digital everywhere is precisely the noise-immunity argument.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: transmit data purely digitally as is.* The world is analog: a wire carrying 0 V/5 V still encounters capacitance, inductance, attenuation, and noise that smear the levels. "Digital" transmission is really analog *with discrete levels* and regenerators — digital won because it's easier to make reliable at scale.
- *Alternative: stay analog (like legacy telephone).* Analog signals degrade cumulatively — each repeater adds noise, and there's no way to distinguish "signal" from "noise" after enough hops. Digital signaling lets every repeater *regenerate* a clean 0/1 (noise does not accumulate), and it allows error correction (Part 05). This is why virtually everything digitized.
- *Alternative: no sampling/quantization (pure analog to digital conversion without loss).* Infinite precision is impossible; quantization (approximating to discrete levels) is the mandatory trade-off, balanced by choosing enough levels/bits that the quantization noise is below the channel noise.
- *Alternative: ignore bandwidth and send any waveform.* Physics forbids it: a real channel is a *low-pass filter* — it only passes frequencies below its bandwidth — so the signal's frequency content is bounded, and that bound (Nyquist) limits symbol rate. You *must* respect the channel bandwidth.

## 5. Intuition
Think of a signal as a **wave on a lake**. The height is amplitude, how often a crest passes is frequency, and where the crest is when you start timing is phase. Data is a message written on the wave by wiggling one of those three knobs. Digital signaling is the trick of writing only two *very distinct* wave shapes (tall wave = 1, flat = 0) so that even when rain (noise) ripples the lake, you can always tell a tall wave from a flat one. If you tried to write 100 subtly different heights, the rain would make them indistinguishable. That tension — "how many distinct levels can I distinguish in the noise?" — is literally the Shannon capacity formula.

## 6. Real-World Analogy
A **semaphore flag system**. The flag can be up (1) or down (0) — a digital signal. Rain and wind (noise) blur the position, but as long as up vs down is unambiguous, the message survives. Now imagine a 64-level system: the flag could be at 64 different angles — much more information per move (6 bits), but a gust of wind makes adjacent angles look the same (bit errors). Carriers of the message are physical (a wire's voltage, a radio's wave), and the *trick* is choosing how many levels to use — few enough to survive noise, many enough to be fast.

## 7. Formal Definition
A **signal** s(t) is a time-varying physical quantity (voltage, current, light intensity, EM field) used to convey information; its fundamental properties are amplitude, frequency (Hz), phase (radians), and period (s). An **analog signal** varies continuously; a **digital signal** takes discrete values (levels) over time. **Bandwidth** of a channel is the range of frequencies it passes without significant attenuation (Hz); the **bit rate** is bits/second; the **symbol (baud) rate** is signal-elements/second. **Data communication** is the exchange of data between devices via such signals over media; it is characterized by directionality (simplex/half-duplex/full-duplex), serial vs parallel, and clocking (synchronous/asynchronous). **Sampling theorem (Nyquist-Shannon)**: to reconstruct a band-limited signal of bandwidth B, sample at ≥ 2B.

## 8. Example
**POTS voice digitization** — the canonical numbers: voice bandwidth ≈ 300–3400 Hz, so use B = 4000 Hz. Nyquist says sample at 2B = 8000 samples/s. Quantize each sample to 8 bits (256 levels — enough for ~48 dB SNR of speech) → bit rate = 8000 × 8 = **64,000 bps** = the 64 kbps "DS0" channel that every T1/E1 and ISDN channel is built from. That one calculation explains why a phone call is 64 kbps, why VoIP sounds like a phone call, and why T1 = 24 × 64 kbps = 1.544 Mbps.

## 9. Internal Working
1. **Source → digital**: an ADC samples an analog waveform at ≥ 2B and quantizes to levels (PCM); the bit stream is the digitized source.
2. **Digital → signal (line coding)**: bits are mapped to voltage levels (NRZ, Manchester, etc.) — a baseband signal on the wire.
3. **Signal → carrier (modulation)**: for passband/radio, the baseband stream modulates a carrier's amplitude/frequency/phase.
4. **Channel**: the medium attenuates high frequencies (acts as a low-pass filter of bandwidth B), adds noise (thermal/thermal-like), and distorts.
5. **Receiver**: samples the received signal at the symbol rate, recovers the clock from transitions, decides the level per symbol (with an eye-diagram decision threshold), decodes to bits, and passes clean bits to the data link layer (Part 05).
6. **Regeneration**: digital repeaters/amplifiers restore clean levels after attenuation — the key advantage over analog amplification, which amplifies noise too.

## 10. Time Complexity / Limits
- **Nyquist**: max symbol rate = 2B symbols/s (a hard limit from the channel's bandwidth, independent of noise). With M levels per symbol: max bit rate = 2B·log₂(M) b/s.
- **Shannon**: max bit rate = B·log₂(1 + SNR) b/s — the absolute capacity ceiling including noise; you cannot exceed it with *any* coding.
- **Practical data rates**: real systems sit 1-3 dB below Shannon (coding gap); line-rate Ethernet is set by physical-layer standards, not by software — the "complexity" is constant per symbol.
- The relevant "algorithm" is the modulation/coding scheme, not a data structure — the interview math is Nyquist/Shannon and unit conversions (dB↔linear, Mbps↔MB/s).

## 11. Advantages
- **Digital's noise immunity**: levels are regenerated at each hop; errors don't accumulate like analog noise.
- **Error correction enabled**: digital bits permit CRC/FEC (Part 05, Hamming section) — impossible for continuous analog values.
- **Flexible representation**: the same digital data can ride any medium (copper/fiber/radio) with the right encoding.
- **Multiplexing & compression**: digitized data is trivially multiplexed and compressed (the entire modern internet depends on it).
- **Deterministic limits**: Nyquist/Shannon give provable ceilings, letting engineers size systems before building.

## 12. Disadvantages
- **Quantization loss**: converting analog → digital loses information (quantization noise) unless levels are fine enough.
- **Sampling overhead**: high-fidelity digital needs high sample rates and bandwidth (raw digital video is huge — hence codecs).
- **Synchronization**: digital receivers need precise clock recovery; async links add start/stop bits (overhead).
- **Bandwidth hungry**: naive digital signaling needs wide bandwidth (that's why line codes are engineered — DC balance, transitions).
- **Media still analog**: the physical limitations (attenuation, dispersion, interference) still apply — digital doesn't remove physics, it copes better.

## 13. Interview Questions
1. **Q: What is the difference between an analog and a digital signal?** A: An analog signal varies continuously (e.g., voice voltage); a digital signal takes discrete levels (0/1). Digital is favored because noise doesn't accumulate — repeaters regenerate clean levels — and it enables error detection/correction, compression, and multiplexing.

2. **Q: What are the four properties of a signal?** A: Amplitude (strength), frequency (cycles/sec, Hz), phase (cycle offset), period (time per cycle). Modulation encodes data by varying one or more of them.

3. **Q: What is the Nyquist sampling theorem, and what does it mean for a 4 kHz voice channel?** A: To reconstruct a signal of bandwidth B, sample at ≥ 2B. For voice (4 kHz), 8,000 samples/s; at 8 bits/sample → 64 kbps — the DS0/PCM rate. Sampling below 2B causes aliasing (irrecoverable distortion).

4. **Q: What is bit rate vs baud (symbol rate)?** A: Bit rate = baud × bits-per-symbol = baud × log₂(M), where M is the number of levels. 8-PSK on a 2400-baud link: 2400 × 3 = 7200 b/s. Baud is signal-elements/sec; bit rate is information/sec.

5. **Q: Why does digital signaling "win" over analog despite the real world being analog?** A: Noise immunity: a digital level only needs to be distinguished from the others; a regenerator restores a clean signal, so noise doesn't compound across hops. Analog amplification boosts noise along with signal, so quality degrades with distance.

6. **Q: TRICKY — "Digital transmission doesn't suffer from noise" — true or false?** A: False. Digital transmission *suffers* from noise the same way; what it wins is that the *decision* between discrete levels is robust, and it can regenerate. Noise above the decision margin still causes bit errors (BER), which is exactly why Part 05's CRC exists.

7. **Q: What is serial vs parallel transmission, and why is parallel tricky?** A: Serial sends bits one at a time on one line; parallel sends multiple bits simultaneously on many lines (faster but requires synchronization, suffers skew, more pins — that's why PCIe and USB are serial even though SATA/parallel ATA was parallel).

8. **Q: What is the difference between simplex, half-duplex, and full-duplex?** A: Simplex: one direction only (radio/TV broadcast). Half-duplex: both directions but one at a time (walkie-talkie, classic Ethernet). Full-duplex: both directions simultaneously (modern switched Ethernet, phone).

9. **Q: SCENARIO — A 3 kHz telephone channel with SNR 30 dB. What's the max bit rate?** A: Shannon: 3000 × log₂(1+1000) = 3000 × 9.97 ≈ **29.9 kbps**. Real modems (V.34) hit 33.6 kbps — a 3-5 kbps *above* the naive calculation because they use more than 3.4 kHz of the line's actual response. (The 30 dB SNR ↔ ratio 1000 conversion is the trap.)

10. **Q: What is quantization noise and how do you reduce it?** A: Quantization replaces continuous values with discrete levels, introducing error (half a level width on average). Reduce by more bits/levels (finer granularity) — at the cost of bandwidth; the sweet spot is when quantization noise ≈ channel noise.

11. **Q: PRODUCTION — Why is voice still "telephony quality" over VoIP?** A: Because VoIP uses G.711 PCM: 8 kHz sampling, 8-bit quantization → 64 kbps. The digitization was standardized decades ago (ITU-T), so all phone networks are 64 kbps DS0s — the Nyquist math hasn't changed.

12. **Q: What is aliasing and when does it happen?** A: When a signal is sampled below 2× its bandwidth, high-frequency content folds down into low frequencies (aliasing) and can't be recovered. Mitigated by anti-aliasing low-pass filters before the ADC — why audio cards and data converters filter input first.

13. **Q: TRICKY — Can a 3 kHz channel carry 64 kbps?** A: Only with very high SNR: Shannon = 3000·log₂(1+SNR) ≥ 64000 → log₂(1+SNR) ≥ 21.3 → SNR ≥ ~2.6M ≈ 64 dB. In practice phone lines can't sustain that, so 64 kbps voice needs the *8 kHz sampling* treatment, not the 3 kHz passband — different framing of the question.

14. **Q: What is an eye diagram and what does it tell you?** A: An oscilloscope overlay of many received symbols; the "eye" opening shows noise margin, jitter, and ISI. A closed eye = decision errors; an open eye = clean decisions. It's the physical-layer equivalent of "can the receiver tell a 0 from a 1?"

15. **Q: SCENARIO — Your 100 m Cat6 link shows a high BER but the cable test passed. Where do you look?** A: Physical-signal issues beyond cable integrity: interference (EMI from power lines, other cables), a marginal connector, duplex/negotiation mismatch, or the *encoding* (some NICs use weaker line codes). Re-test with a network analyzer (eye diagram), check cable routing, and swap the NIC/port.

16. **Q: What is the relationship between bandwidth, bit rate, and SNR?** A: Bandwidth bounds *how many symbol changes* per second (2B); SNR bounds *how many distinguishable levels* each symbol can carry (log₂(1+SNR)); the product is the channel capacity. More bandwidth or more SNR (either) raises capacity.

17. **Q: Why does DSL (over telephone wire) differ from ISDN (also telephone wire)?** A: Both use the same copper, but DSL treats the line's *entire* spectrum (up to ~1-30 MHz) with VDSL modulation, while ISDN/POTS used only the 4 kHz voice band. Same medium, different bandwidth exploitation → orders-of-magnitude rate difference.

18. **Q: What is the difference between synchronous and asynchronous transmission?** A: Synchronous: a shared clock (or embedded clock via transitions) times every bit — efficient, used by PCIe/Ethernet. Asynchronous: start/stop bits delimit each byte and the receiver resyncs per byte — simple, robust to clock drift, but ~20% overhead (UART).

## 14. Follow-Up Questions
1. **Q: Why is clock recovery so important in digital signaling?** A: The receiver must sample at exactly the right instants; clock is recovered from signal *transitions*. Long runs of identical bits (e.g., 000000) have no transitions → clock drift → mis-sampling. That's why line codes (Manchester, 4B5B, 8B10B) guarantee transitions — a direct link to Section 02.

2. **Q: What is inter-symbol interference (ISI) and how do you fight it?** A: Channel dispersion smears each symbol into its neighbors. Fought by limiting symbol rate to < 2B (Nyquist), using pulse shaping (raised-cosine filters), and equalization at the receiver (DSP). This is why higher rates need better media/encoding.

3. **Q: How does the Shannon limit change if noise is added?** A: Capacity drops logarithmically with 1+SNR; doubling noise halves SNR by 3 dB → capacity falls ~B·log₂(1.5) per 3 dB. This is why link budgets (dB of margin) are designed before deployment.

4. **Q: What does "bandwidth-limited" vs "noise-limited" mean in link design?** A: Bandwidth-limited: raising rate requires more spectrum or more levels (Nyquist governs). Noise-limited: raising rate requires better SNR (Shannon governs). Optical links are often noise/power-limited; copper links are bandwidth/attenuation-limited.

## 15. Coding Example
```python
import math

def nyquist_rate(bandwidth_hz: float, levels: int) -> float:
    """Max symbol rate = 2B; bit rate = 2B*log2(M)."""
    return 2 * bandwidth_hz * math.log2(levels)

def shannon_capacity(bandwidth_hz: float, snr_ratio: float) -> float:
    return bandwidth_hz * math.log2(1 + snr_ratio)

def db_to_ratio(db: float) -> float:
    return 10 ** (db / 10)

print(f"Nyquist 3 kHz 2 levels: {nyquist_rate(3000, 2):.0f} bps")       # 6000
print(f"Nyquist 3 kHz 16 levels: {nyquist_rate(3000, 16):.0f} bps")     # 24000
print(f"Shannon 3 kHz SNR 30dB: {shannon_capacity(3000, db_to_ratio(30)):.0f} bps")  # ~29900
print(f"PCM voice: 8000 samples/s * 8 bits = {8000*8} bps")              # 64000

# Sample-and-quantize a sine (tiny PCM encoder)
import wave, struct, array
def pcm_encode(freq=1000, rate=8000, dur=0.5, bits=8):
    n = int(rate * dur)
    samples = [round(127 + 100 * math.sin(2*math.pi*freq*i/rate)) for i in range(n)]
    return array.array("B", [max(0, min(255, s)) for s in samples])  # 8-bit PCM

buf = pcm_encode()
print(f"PCM bytes generated: {len(buf)} (={len(buf)*8} bits at 8kHz)")
```
```bash
# Observe physical-layer parameters on a live link
ethtool eth0 | grep -E "Speed|Duplex|Link detected"      # negotiated rate/duplex
ethtool -S eth0 | grep -Ei "symbol|fcs|align"            # physical-layer error counters
mii-tool eth0                                             # legacy media info
ip -s link show eth0                                      # per-device error stats
# Noise/interference check via wireless (radio is 'unguided'):
iw dev wlan0 link | grep signal
sudo iw dev wlan0 survey dump | grep -E "noise|busy"      # channel noise (dBm)
```

## 16. Industry Usage
- **Ethernet PHYs**: 100BASE-TX (4B5B), 1000BASE-T (PAM-5), 10GBASE-T (PAM-16) — each a specific signal/encoding/bandwidth solution in silicon.
- **Optical transport**: coherent QPSK/16-QAM for 400G/800G; DSP equalization; WDM — Section 02/03 in production.
- **Cellular/5G**: 256-QAM, massive MIMO, OFDM — the modulation (Section 02) on unguided media (Section 03).
- **Telephony**: PCM G.711 64 kbps DS0 — the Nyquist example in the field for 50 years.
- **PCIe/USB/SATA**: high-speed serial line codes with clock recovery and equalization — data-center link budgets are physical-layer engineering.
- **Cloud DCs**: DAC/AOC transceivers, SFP+ optics, fiber types chosen by reach/cost — every cloud network build starts with physical-layer choices.

## 17. References
- Kurose & Ross, *Computer Networking*, 8th ed., §1.2 (Network Edge), §1.5 (Throughput/Latency).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §2.2 (Bandwidth and Latency), §2.3 (Media).
- C. E. Shannon, "A Mathematical Theory of Communication," Bell System Technical Journal, 1948.
- H. Nyquist, "Certain Topics in Telegraph Transmission Theory," 1928.
- ITU-T G.711 (PCM voice coding) — https://www.itu.int/rec/T-REC-G.711
- Stallings, *Data and Computer Communications*, Ch. 3-5 (data transmission).

## 18. Cheat Sheet
- Signal properties: amplitude, frequency, phase, period.
- Analog = continuous; digital = discrete levels; digital wins on noise immunity (regeneration).
- Nyquist: max symbol rate 2B; bit rate = 2B·log₂(M).
- Shannon: capacity = B·log₂(1+SNR); SNR linear ↔ dB = 10·log₁₀.
- PCM voice: 8 kHz × 8 bits = 64 kbps DS0.
- Serial vs parallel: serial for speed/distance today (PCIe, USB); parallel suffers skew.
- Simplex / half-duplex / full-duplex.
- Sampling below 2B → aliasing; anti-alias filter first.
- Eye diagram = noise margin / ISI at the receiver.
- Bit rate = baud × log₂(M).

## 19. Quiz
1. A signal's cycles per second is its: a) amplitude b) frequency c) phase d) period → **b**
2. Which wins on noise immunity? a) analog b) digital c) neither d) depends on media → **b**
3. To sample a 4 kHz signal, minimum rate: a) 4 kHz b) 8 kHz c) 2 kHz d) 16 kHz → **b**
4. 8-PSK on a 2400-baud link gives: a) 2400 bps b) 7200 bps c) 4800 bps d) 9600 bps → **b**
5. Shannon capacity of 3 kHz at 30 dB SNR ≈: a) 6 kbps b) 30 kbps c) 64 kbps d) 1.5 Mbps → **b**
6. 30 dB SNR as a ratio is: a) 30 b) 100 c) 1000 d) 3000 → **c**
7. PCM voice bit rate: a) 32 kbps b) 64 kbps c) 128 kbps d) 8 kbps → **b**
8. Sampling below the Nyquist rate causes: a) noise b) aliasing c) jitter d) attenuation → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-c, 7-b, 8-b.

## 20. Flashcards
- **Q: What are the signal properties?** → **A:** Amplitude, frequency, phase, period.
- **Q: Why does digital beat analog?** → **A:** Noise doesn't accumulate — regeneration restores clean levels; enables error correction, compression, multiplexing.
- **Q: Nyquist theorem?** → **A:** Max symbol rate = 2B; bit rate = 2B·log₂(M).
- **Q: Shannon theorem?** → **A:** Capacity = B·log₂(1+SNR) bps — the absolute limit including noise.
- **Q: How is voice 64 kbps?** → **A:** 4 kHz bandwidth → 8 kHz sampling × 8-bit quantization = 64 kbps DS0.
- **Q: Bit rate vs baud?** → **A:** baud × log₂(M); more levels = more bits per symbol.
- **Q: What is aliasing?** → **A:** Sampling < 2B folds high frequencies into low — unrecoverable; prevent with anti-alias filter.

## 21. Revision
Data communication is analog-physics with digital discipline: signals vary in amplitude/frequency/phase; digital signaling uses discrete levels so noise never accumulates (regenerators rebuild clean bits). The channel acts as a low-pass filter of bandwidth B, giving Nyquist's limit (symbol rate ≤ 2B, bit rate = 2B·log₂(M)) and Shannon's ceiling with noise (B·log₂(1+SNR)). PCM voice = 8 kHz sampling × 8 bits = 64 kbps DS0. Know the directionality modes (simplex/half/full), serial vs parallel, synchronous vs asynchronous, and the dB↔ratio conversion (30 dB = 1000×). Anchor numbers: Nyquist 2B, Shannon B·log₂(1+SNR), voice 64 kbps, symbol rate vs bit rate = baud × log₂(M). Every digital transmission still rides an analog medium — the encoding just makes 0/1 robust against that physics.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Analog vs digital signals?" | 7 / 13-Q1 |
| "What are signal properties / modulation?" | 7 / 13-Q2 |
| "Nyquist sampling theorem?" | 13-Q3 / 7 |
| "Bit rate vs baud?" | 13-Q4 |
| "Max rate over a noisy channel (Shannon)?" | 13-Q9 / 8 |
| "What is quantization noise / aliasing?" | 13-Q10,12 |
| "Why is voice 64 kbps?" | 8 / 13-Q11 |
| "Eye diagram / BER diagnosis?" | 13-Q14,15 |
| "Serial vs parallel / duplex modes?" | 13-Q7,8 |
