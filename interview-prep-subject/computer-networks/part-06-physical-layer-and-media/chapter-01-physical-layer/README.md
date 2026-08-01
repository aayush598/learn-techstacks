# Chapter: The Physical Layer

## What you'll learn
- What a signal is (analog vs digital), signal properties (amplitude, frequency, phase, period), and how data becomes a physical signal in the first place.
- The fundamental limits of any channel: Nyquist's theorem (symbol-rate limit) and Shannon's theorem (capacity with noise) — with hand-computable numbers.
- How bits are mapped to signals: line coding (NRZ, Manchester, 4B5B, 8B10B, 64B66B) for baseband, and modulation (ASK/FSK/PSK/QAM) for passband/radio.
- The transmission media: guided (twisted pair, coax, fiber) and unguided (radio, microwave, infrared), with the real-world trade-off matrix.
- How multiple conversations share one medium: FDM/TDM/WDM/CDMA multiplexing, and circuit vs packet vs statistical switching.
- The performance vocabulary: bandwidth vs throughput vs goodput, latency = transmission + propagation + queueing + processing, and the bandwidth-delay product.

## Prerequisites (linked)
- A comfort with binary math and basic trigonometry concepts (frequency, phase, amplitude) — no calculus needed.
- [Part 05 — Data Link Layer](../part-05-data-link-layer/README.md): the framing and CRC that correct for the physical layer's noise. This chapter is where that noise comes from.
- Basic understanding of layering ([Part 01](../part-01-network-fundamentals/chapter-02-osi-and-tcp-ip-models/README.md)).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Signals: Analog, Digital, Data Communication](section-01-signals-analog-digital-and-data-communication.md) | What a signal is; analog vs digital; bandwidth, frequency, phase; why digital wins; serial/parallel; simplex/duplex |
| [Section 02 — Encoding and Modulation](section-02-encoding-and-modulation.md) | Line coding (NRZ/RZ/Manchester/4B5B/8B10B/64B66B) and modulation (ASK/FSK/PSK/QAM); mapping bits to waveforms |
| [Section 03 — Transmission Media: Guided and Unguided](section-03-transmission-media-guided-and-unguided.md) | Twisted pair, coax, fiber (SMF/MMF, WDM) and radio/microwave/IR; media selection trade-offs |
| [Section 04 — Multiplexing and Switching](section-04-multiplexing-and-switching.md) | FDM/TDM/WDM/CDMA; circuit vs packet switching; statistical multiplexing gains |
| [Section 05 — Bandwidth, Throughput, and Latency](section-05-bandwidth-throughput-and-latency.md) | Nyquist & Shannon capacity; throughput vs goodput; latency = trans + prop + queue + proc; BDP |

## One-paragraph narrative connecting all sections
The physical layer is where "data" (bits, frames) becomes physics — an electromagnetic wave or a photon. Section 01 establishes the raw materials: signals carry information via amplitude/frequency/phase, and digital signaling wins over analog because of noise immunity, even though real media are analog. Section 02 shows the actual conversion: line codes map bits to voltage levels on a wire (baseband), while modulation moves those bits onto a carrier wave for radio/fiber (passband) — and the encoding choice determines clock recovery and error tolerance. Section 03 introduces the media those signals traverse: copper (cheap, short, noisy), fiber (fast, long, immune), radio (mobile, lossy) — the noise and attenuation that Sections 01-02's codes must survive. Section 04 explains how the channel is shared: multiplexing divides a medium by frequency/time/wavelength/code, and switching decides how many users' traffic rides it — packet switching's statistical multiplexing is why the Internet works at all. Section 05 is the payoff: bandwidth, throughput, and latency are the numbers that drive every real network decision, and the Nyquist/Shannon formulas give the ceiling every design hits.

## Common interview trap in this chapter
1. **Bandwidth vs throughput**: bandwidth is the *capacity* of the channel (Hz, or the maximum bits/sec); throughput is the *achieved* rate. Saying "bandwidth is how fast data goes" invites the follow-up that splits them.
2. **Nyquist vs Shannon**: Nyquist limits *symbol rate* (2B symbols/sec, no noise); Shannon limits *bit rate* with noise (B·log₂(1+SNR)). Nyquist is about the medium's bandwidth; Shannon is about capacity given noise. Getting the "noise" attribution wrong is a classic fail.
3. **Bit rate vs baud**: bit rate = symbols/sec × bits-per-symbol (log₂(M)). 8-PSK on a 2400-baud line = 7200 b/s — not 2400 b/s.
4. **dB vs dBm vs dBW**: SNR in dB is 10·log₁₀(P_signal/P_noise); converting "30 dB SNR" means ratio 1000, not 30.
5. **Latency components**: propagation (light speed, ~5 µs/km in fiber) is *distance-bound* and can't be fixed with bandwidth — a 400 Gb/s link over 1000 km still has ~5 ms propagation delay. Candidates forget that throughput (bandwidth) and latency are orthogonal.

## Checklist before moving on
- [ ] I can compute the max symbol rate (Nyquist) and max bit rate with noise (Shannon) for a given channel.
- [ ] I can convert SNR dB↔linear, and bit rate↔baud with M-ary modulation.
- [ ] I can name a real encoding per purpose (Manchester for clock recovery, 4B5B/8B10B for DC balance, 64B66B for 10G+).
- [ ] I can choose the right medium for a scenario and justify it (rate, distance, cost, interference).
- [ ] I can explain FDM/TDM/WDM/CDMA and when packet switching beats circuit switching.
- [ ] I can compute throughput vs bandwidth, and decompose latency into transmission/propagation/queueing/processing.
