# PCM and Pulse Modulation - Formulas

## PCM Parameters
```
Number of levels: L = 2^n (n = bits)
Step size: Delta = Vpp/L = Vpp/2^n
Quantization noise power: Nq = Delta^2/12
Maximum quantization error: +/-(Delta/2)

SINAD/SQNR (dB) = 6.02n + 1.76 (full-scale sinusoid)
SQNR (dB) = 6.02n (uniform signal)
```

## Bit Rate
```
Rb = n * fs (bits/sec)
Rb = n * 2 * fmax (using Nyquist rate)
Minimum BW (Sinc): BW = Rb/2 = n * fmax
Practical BW (Rectangular): BW = Rb = 2 * n * fmax
```

## T1/E1 Carriers
```
T1: 24 channels * (8 bits + 1 framing bit) * 8000 = 1.544 Mbps
E1: 32 channels * 8 bits * 8000 = 2.048 Mbps
Voice channel: 64 kbps (8 kHz * 8 bits per sample)
```

## Delta Modulation
```
Slope overload condition:
  (Delta/Ts) >= max(dm/dt) = 2*pi*fm*Am
  where Delta = step size, Ts = sampling period
  
Granular noise: occurs when signal is flat (repeated +Delta and -Delta)
  Delta should be as small as possible for granular noise
  Delta must be large enough to avoid slope overload
```

## A-law Compression
```
y = A*x/(1+ln(A)) for 0 <= |x| <= 1/A
y = (1+ln(A*|x|))/(1+ln(A)) for 1/A <= |x| <= 1
Standard: A = 87.6
```

## mu-law Compression
```
y = ln(1 + mu*|x|)/ln(1+mu) for |x| <= 1
Standard: mu = 255
```

## Quick Reference
| Parameter | Formula |
|-----------|---------|
| SQNR (dB) | 6.02n + 1.76 |
| Quantization noise | Delta^2/12 |
| Step size | Vpp/2^n |
| Bit rate | n * fs |
| T1 rate | 1.544 Mbps |
| E1 rate | 2.048 Mbps |
| Voice channel | 64 kbps |
