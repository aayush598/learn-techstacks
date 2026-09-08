# Eye Diagram and BER - Formulas

## BER (AWGN)
```
BPSK:  Pb = Q(sqrt(2Eb/N0))
QPSK:  Pb = Q(sqrt(2Eb/N0))   (bit error, same as BPSK)
Coherent FSK: Pb = Q(sqrt(Eb/N0))
Noncoherent FSK: Pb = 0.5 e^(-Eb/2N0)
DPSK:  Pb = 0.5 e^(-Eb/N0)
2-PAM same as BPSK
```

## Q Function
```
Q(x) = (1/sqrt(2pi)) int_x^inf e^(-t^2/2) dt = 0.5 erfc(x/sqrt2)
Large x: Q(x) ~ (1/(x sqrt(2pi))) e^(-x^2/2)
Q(0)=0.5
```

## Symbol vs Bit Error
```
Ps = 1 - (1 - Pb)^k  (M=2^k, approx, orthogonal)
With Gray coding: Ps ~ k * Pb  (bit error ~ symbol error / k)
```

## Nyquist (Raised Cosine) Zero-ISI
```
Bandwidth: B = (1+alpha) * Rs/2
  Rs = symbol rate, alpha = roll-off (0 to 1)
alpha = 0: B = Rs/2 (min, ideal Nyquist sinc)
alpha = 1: B = Rs (full)
Excess bandwidth = alpha * Rs/2
```

## Eye Metrics
```
Eye height = amplitude margin (noise immunity)
Eye width = timing margin
Eye opening factor = (V_th_max - V_th_min)/(2*V_pp)
```

## Sample Error / ISI Interference
```
Worst-case ISI = Sum of all adjacent symbol contributions at sampling time
Zero ISI: pulse p(nT) = 0 for n != 0
Nyquist: Sum p(kT - T) ... pulse satisfies p(0)=1, p(nT)=0
```

## Coding Gain
```
Gain(dB) = Eb/N0_uncoded - Eb/N0_coded (at same BER)
E.g. a code needing 3 dB less power
```

## Quick Reference
| Scheme | Pb (AWGN) |
|--------|-----------|
| BPSK | Q(sqrt(2Eb/N0)) |
| QPSK | Q(sqrt(2Eb/N0)) |
| co-FSK | Q(sqrt(Eb/N0)) |
| nc-FSK | 0.5 e^(-Eb/2N0) |
| DPSK | 0.5 e^(-Eb/N0) |
| RC BW | (1+alpha)Rs/2 |
