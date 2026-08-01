# Part: Physical Layer and Media

## What this part covers
Layer 1 of the OSI model — the actual physics of moving bits: how analog signals represent data, how bits are encoded onto signals (line coding, encoding, modulation), what media carries them (copper, fiber, radio), how channels are shared and switched (FDM/TDM/statistical multiplexing, circuit vs packet switching), and the fundamental performance math (Nyquist, Shannon, bandwidth, throughput, latency). This is the layer that explains *why* the data link layer (Part 05) needs framing and CRC: the medium is a lossy, bandwidth-limited, noise-affected physical channel. Interviews probe this part with the Nyquist and Shannon theorem computations, bandwidth-delay-product reasoning, and the physical-media trade-offs behind real links (Cat cabling, SFP+ optics, WiFi bands).

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Physical Layer | Signals (Analog/Digital/Data Comm), Encoding & Modulation, Transmission Media (Guided/Unguided), Multiplexing & Switching, Bandwidth/Throughput/Latency | Distinguish analog vs digital signals, compute data rate via Nyquist & Shannon, explain line coding vs modulation, choose copper vs fiber vs radio by context, walk FDM/TDM/CDMA/WDM, compute throughput vs bandwidth and latency budgets |
| (see Part 05 for Data Link layer tie-ins) | Framing/CRC (P5), CSMA/CD (P5) | Frame the bits this layer delivers |

## Study order
1. **Signals first** — you can't talk about speed or encoding without defining the signal, its bandwidth, and noise (Section 01).
2. **Encoding & modulation** — how bits become signal states, and why you need both line codes and passband modulation (Section 02).
3. **Transmission media** — where those signals physically travel; the copper/fiber/radio trade-off matrix (Section 03).
4. **Multiplexing & switching** — how many conversations share one medium and one network; circuit vs packet (Section 04).
5. **Bandwidth/throughput/latency** — the capstone metrics that tie everything to real interview math (Section 05).

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐ (3/5)** — lower frequency than TCP/IP, but the *computable* questions are asked: "What's the max data rate over a 3 kHz channel with SNR 30 dB?" (Shannon), "Why is Nyquist the limit on symbol rate?" "What is the bandwidth-delay product?" "Fiber vs copper for a DC backhaul?" These are strong filters for network-hardware and infrastructure roles.
- **Emphasized by**: hardware/physical-infra teams (NVIDIA networking, Arista, Cisco, Ciena, cloud DC teams at AWS/GCP/Azure, telco vendors), and any "fundamentals" round testing whether you understand *why* a 10G link can't do more than its theoretical max.
- Typical asked: "Derive the max channel capacity (Shannon)", "What's the difference between bandwidth and throughput?", "Why does fiber win over copper at long distance?", "What is FDM vs TDM vs statistical multiplexing?", "Why is latency dominated by propagation and not bandwidth on long links?"

## How the parts connect (roadmap)
- **Part 05 (Data Link) sits directly on top**: framing and CRC exist precisely because this layer's medium corrupts bits — the physical channel's BER, bandwidth, and noise define the error rates the data link must absorb.
- **Part 03/04 (Transport/Network)**: TCP's throughput limits (window/BDP), MTU sizing, and route metrics all depend on physical-layer properties (RTT, link speed, optical span lengths).
- **Part 07 (Security)**: side-channel attacks (EM emanation), jamming, and physical security sit at Layer 1; also fiber-tap and radio-eavesdropping threats.
- **Part 08 (Advanced)**: anycast/multicast/broadcast, DC networking (optic fabric, DAC, transceivers), and global load balancing all depend on physical-layer latency and bandwidth.

## Checklist before moving on
- [ ] I can explain the difference between analog and digital signals and why digital wins on noise immunity.
- [ ] I can compute maximum data rate given bandwidth and SNR (Shannon) and the symbol-rate limit (Nyquist).
- [ ] I can differentiate line encoding (NRZ, Manchester, 4B5B, 8B10B, 64B66B) from modulation (ASK/FSK/PSK/QAM) and give a real use for each.
- [ ] I can choose twisted pair vs coax vs fiber vs radio for a scenario with reasoning (distance, rate, cost, interference).
- [ ] I can explain FDM, TDM, WDM, and CDMA with examples, and compare circuit vs packet switching.
- [ ] I can compute throughput vs bandwidth, propagation vs transmission latency, and the bandwidth-delay product.
