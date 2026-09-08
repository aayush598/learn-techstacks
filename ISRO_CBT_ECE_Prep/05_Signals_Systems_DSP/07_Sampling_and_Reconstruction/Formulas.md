# Sampling and Reconstruction - Formulas

## Sampling
```
Perfect: fs >= 2*fmax
Nyquist rate: fs = 2*fmax
Folding frequency: fs/2

Oversampling ratio: M = fs/(2*fmax)
```

## Aliased Frequency
```
f_alias = |f - k*fs|, choose integer k to satisfy 0<=f_alias<=fs/2
Example: f = 5 kHz, fs = 4 kHz -> |5-4| = 1 kHz
Example: f = 7 kHz, fs = 4 kHz -> |7-8| = 1 kHz
```

## Sampled Spectrum
```
Xs(f) = (1/T) Sum[k] X(f - k*fs),  fs = 1/T
```

## Ideal Reconstruction
```
x(t) = Sum x(nT) sinc((t-nT)/T)
sinc(x) = sin(pi x)/(pi x)
Equivalent LPF: H(f) = T for |f|<fs/2, else 0
```

## Zero-Order Hold
```
h(t) = 1 for 0<t<T, 0 otherwise
H(s) = (1-e^(-sT))/s
H(jw) = T sinc(wT/2) e^(-jwT/2)
|H(jw)| = T|sinc(wT/2)|
```

## DTFT of Sampled Signal
```
X(e^jw) = (1/T) Sum X((w - 2pi k)/T)   [DTFT of samples]
```

## SNR with Quantization (PCM)
```
SQNR = 6.02n + 1.76 dB (full-scale sine)
```

## Data Rate from Sampling
```
Rb = fs * n  (n = bits/sample)
For telephone: fs=8000, n=8 -> 64000 bps
```

## Quick Reference
| Value | Formula |
|-------|---------|
| Nyquist rate | 2 fmax |
| Folding freq | fs/2 |
| Aliased freq | |f-k fs| |
| ZOH H(s) | (1-e^-sT)/s |
| ZOH mag | T sinc(wT/2) |
| Quant SNR | 6.02n+1.76 |
