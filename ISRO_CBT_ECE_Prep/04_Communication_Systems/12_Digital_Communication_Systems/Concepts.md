# Digital Communication Systems - Overview

## Block Diagram
```
Source -> Source Encoder -> Channel Encoder -> Modulator -> CHANNEL
                                                        |
Source <- Source Decoder <- Channel Decoder <- Demodulator <-
```

## Key Stages
| Stage | Function |
|-------|----------|
| Source encoder | Removes redundancy (compression) |
| Channel encoder | Adds redundancy (FEC) |
| Modulator | Maps bits to waveforms |
| Channel | Can add noise, distortion, attenuation |
| Demodulator | Recovers decision statistics |
| Channel decoder | Corrects/removes additive errors |
| Source decoder | Expands back to user data |

## Design Trade-offs
- **Power efficiency**: SNR (Eb/N0) required for target BER
- **Bandwidth efficiency**: bps/Hz achievable
- **Complexity**: cost of implementation
- Fundamental: avoid exceeding Shannon capacity C
- Trade power for bandwidth (or vice versa) via modulation order

## Bandwidth-Power Frontier
- Low-order (BPSK): low BW efficiency, low power requirement
- High-order (256-QAM): high BW efficiency, high power needed
- Coding: adds redundancy, lowers BW eff, greatly improves power eff

## Example Systems & Their Modulations
| System | Modulation |
|--------|------------|
| WiFi (802.11) | BPSK, QPSK, 16/64/256-QAM + OFDM |
| LTE/5G | QPSK, 16/64/256-QAM, OFDM |
| DVB-T | QPSK, 16/64-QAM, OFDM |
| Satellite TV | QPSK |
| GSM | GMSK |
| Bluetooth | GFSK |
| Legacy telephone | 64 kbps PCM |

## Multiple Access
- FDMA (frequency), TDMA (time), CDMA (code)
- OFDMA for modern systems
- Spatial multiplexing (MIMO)

## Performance Metrics
- BER, throughput, latency, spectral efficiency
- Link budget: power needed vs available
- Outage probability (fading channels)

## Sampling & Quantization Recall
- Telephone PCM: 8kHz sampling, 8 bits -> 64 kbps
- Nyquist & quantization set the fundamental data rate

## Summary Priorities for ISRO
1. Modulation types & their BER/BW
2. Block diagram understanding
3. Trade-offs (power vs bandwidth)
4. Capacity concepts
5. Matched filter / MAP receiver
