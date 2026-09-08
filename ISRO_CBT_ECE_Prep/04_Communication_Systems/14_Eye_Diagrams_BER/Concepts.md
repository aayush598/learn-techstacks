# Eye Diagram and BER - Concepts

## Eye Diagram
- Oscilloscope display showing overlapped waveforms of received symbols
- Triggered on symbol period, overlaid traces
- Visualizes: noise, ISI (inter-symbol interference), timing jitter, distortion

## What the Eye Shows
| Feature | Meaning |
|---------|---------|
| Eye opening (height) | Noise margin (signal amplitude) |
| Eye width | Time margin (sampling tolerance) |
| Eye height | Distortion sensitivity |
| Eye closure | ISI, noise |
| Transition thickness | Jitter |
| Center crossing | Timing sampling point |

## BER (Bit Error Rate)
```
BER = number of bit errors / total bits transmitted
For AWGN BPSK: Pb = Q(sqrt(2Eb/N0))
Lower Eb/N0 -> higher BER
```
- BER is the key quality metric for digital links

## Q Function and Error
```
Q(x) = 0.5 erfc(x/sqrt2)
As Eb/N0 increases by 1 dB, BPSK BER improves dramatically (exponential)
```

## BER for Common Schemes (AWGN)
```
BPSK: Pb = Q(sqrt(2Eb/N0))
QPSK: Pb = Q(sqrt(2Eb/N0)) (same bit error)
Coherent FSK: Pb = Q(sqrt(Eb/N0))
Noncoherent FSK: Pb = (1/2)e^(-Eb/2N0)
DPSK: Pb = (1/2)e^(-Eb/N0)
For high Eb/N0, PSK outperforms FSK
```

## Inter-Symbol Interference (ISI)
- Caused by channel/timing spreading of symbols into neighbors
- Widens transitions in eye diagram, closes eye
- Reduced by:
  - Nyquist pulse shaping (raised cosine)
  - Equalization (channel equalizer)
  - Zero-forcing/MMSE equalizers

## Nyquist Criterion (Zero ISI)
- Raised cosine spectrum
- Roll-off factor (alpha): 0 <= alpha <= 1
- Bandwidth: B = (1+alpha) Rs/2
- Alpha=0: sinc, min BW (impractical)
- Alpha=1: 2x BW, easy filters

## Timing Jitter
- Random variation of symbol timing
- Closes eye horizontally
- Caused by: clock recovery noise, phase noise

## Sampling Point
- Best sampling at center of eye (maximum opening)
- Errors if sampled near transitions
- Clock recovery aligns sampling to center

## BER Curve Interpretation
- x-axis: Eb/N0 (dB), y-axis: BER (log scale)
- Steeper curve = more robust scheme (BPSK better than many)
- Coding gain: shift left (lower Eb/N0 for same BER)

---

## ISRO Key Points
- Eye opening = noise immunity
- Eye closure = ISI
- Jitter = timing variation (eye narrowing)
- BPSK BER = Q(sqrt(2Eb/N0))
- Raised cosine: alpha controls BW, zero ISI at sample instants
