# Digital Modulation (ASK, PSK, FSK, QAM) - Concepts

## Why Digital Modulation
- Better noise immunity (discrete levels)
- Regeneration capability (error-free along repeaters)
- Efficient use of power/bandwidth
- Robustness to channel imperfections

---

## ASK (Amplitude Shift Keying)
- 1 -> carrier present, 0 -> carrier absent (or reduced amplitude)
- Simplest form, like AM (bandwidth: 2*Rb)
- Very susceptible to noise (amplitude affected)
- OOK (On-Off Keying) is special case

## FSK (Frequency Shift Keying)
- 1 -> f1, 0 -> f2
- Noncoherent FSK: error = 0.5*exp(-Eb/(2N0))
- Coherent FSK: error = Q(sqrt(Eb/N0))
- Bandwidth: delta_f + 2*Rb (larger than PSK)
- Used in Bluetooth, GSM

## PSK (Phase Shift Keying)
- Phase changes encode bits
- BPSK: 2 phases (0, 180), 1 bit/symbol
- QPSK: 4 phases (0, 90, 180, 270), 2 bits/symbol
- 8PSK: 3 bits/symbol, 16PSK: 4 bits/symbol
- Constant amplitude (good for nonlinear amps)

### BPSK
```
s(t) = Ac*cos(2*pi*fc*t + phi), phi in {0, pi}
Error: Pb = Q(sqrt(2Eb/N0))  [same as 2-PAM]
Bandwidth: 2*Rb (main lobe)
```

### QPSK
```
4 symbols: phases 0, 90, 180, 270 (or 45,135,225,315 for OQPSK)
2 bits per symbol: Rb = 2*Rs (symbol rate halves)
Bandwidth: Rb (half of BPSK)
Error: same as BPSK at same Eb/N0
```

## QAM (Quadrature Amplitude Modulation)
- Combines amplitude AND phase (more efficient)
- 16-QAM: 4 bits/symbol, 64-QAM: 6 bits/symbol
- Used in cable TV, DSL, Wi-Fi, LTE
- 16-QAM constellation: 4x4 grid
- Peak-to-average power ratio higher (non-constant envelope)

## Constellation Diagrams
- **BPSK**: 2 points on axis
- **QPSK**: 4 points (square)
- **16-QAM**: 16 points (4x4)
- **8-PSK**: 8 points on circle (constant radius)
- **16-PSK**: 16 points on circle

## Error Probability (AWGN)
```
BPSK: Pb = Q(sqrt(2Eb/N0))
QPSK: Pb = Q(sqrt(2Eb/N0)) (bit error same as BPSK)
FSK coherent: Pb = Q(sqrt(Eb/N0))
FSK noncoherent: Pb = 0.5*exp(-Eb/(2N0))
QAM: depends on constellation, roughly Pb = Q(sqrt(2Eb/(N0*k)))
```

## Symbol vs Bit Error Rate
```
For M-ary (M = 2^k symbols):
  Symbol error: Pe(symbol) = 1 - (1 - Pe(bit))^k (approx for high SNR)
  Bit rate: Rb = Rs * log2(M)
  For Gray coding: Pb ~ Ps/log2(M)
```

## Spectral Efficiency
```
Efficiency = Rb/BW (bits/sec/Hz)
BPSK: 1 bps/Hz
QPSK: 2 bps/Hz
16-QAM: 4 bps/Hz
Higher QAM = more bits per Hz but worse noise immunity
```

---

## ISRO Key Points
- BPSK error: Q(sqrt(2Eb/N0)) - most tested
- QPSK = 2 bits/symbol - bandwidth halved
- Constellation diagrams
- Higher M = higher spectral efficiency but worse BER
- 16-QAM: 4 bits, 64-QAM: 6 bits
