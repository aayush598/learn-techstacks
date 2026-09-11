# Analog Filters - Formulas

## First-Order Active LPF
```
fc = 1/(2 pi R C)
Rolloff: -20 dB/decade
DC gain: K = 1 + Rf/R1 (non-inverting)
Transfer: H(s) = K/(1 + s/wc)  (wc = 2pi fc)
```

## First-Order HPF
```
fc = 1/(2 pi R C)
Gain high-freq: K
Transfer: H(s) = K s/ (1 + s/wc)
```

## Second-Order (Sallen-Key) LPF
```
fc = 1/(2 pi sqrt(R1 R2 C1 C2))
  Unity gain (R1=R2=R, C1=C2=C): fc = 1/(2pi RC)
Rolloff: -40 dB/decade
Quality factor & gain from resistors
K = 1 + Rb/Ra
Q = (1/3-K) ... (for equal RC with gain control)
```

## Butterworth
```
|H(jw)|^2 = 1/(1+(w/wc)^2n)
n = order
Rolloff = 20n dB/decade
Order for req'd atten:
  n >= log10(((10^(As/10)-1)/(10^(Ap/10)-1)))/(2 log10(ws/wp))  approx
```

## Chebyshev I
```
|H|^2 = 1/(1 + eps^2 Cn^2(w/wc))
Ripple (dB) = 10 log10(1+eps^2)
eps = sqrt(10^(R/10)-1)
Order:
  n >= acosh(sqrt((10^(As/10)-1)/(10^(R/10)-1)))/acosh(ws/wp)
```

## dB / rolloff
```
Normalized frequency: w/wc
For n-th order filter: attenuation 20n dB/decade
  1st = 20 dB/dec, 2nd = 40 dB/dec, 3rd = 60 dB/dec
```

## Cutoff definition
```
-3dB point: |H| = 0.707 (half power)
At fc: phase = -45 deg (first order), -90 (second)
```

## Practical Design formulas
```
Given fc and C: R = 1/(2pi fc C)
For Butterworth 2nd: R1=R2=R, C1=C2=C (equal) -> fc=1/2piRC, Q=0.5
  (Sallen-Key equal RC gives Q=1/3 for unity gain, butterworth needs specific ratios)
```

## Quick Reference
| Filter | fc | Rolloff |
|--------|-----|---------|
| 1st LPF/HPF | 1/2piRC | -20 dB/dec |
| 2nd Sallen-Key | 1/2pi sqrt(R1R2C1C2) | -40 dB/dec |
| n-th order | - | -20n dB/dec |
