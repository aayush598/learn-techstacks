# Filter Networks - Formulas

## First Order
```
RC LPF:  H(jw) = 1/(1 + j w RC),  fc = 1/(2 pi RC)
RC HPF:  H(jw) = j w RC/(1 + j w RC), fc = 1/(2 pi RC)
RL LPF:  fc = R/(2 pi L)
RL HPF:  fc = R/(2 pi L)
```

## Cutoff (-3dB)
```
|H(fc)| = 1/sqrt(2) = 0.707
Power = half. Attenuation = -3 dB.
```

## Roll-off
```
n-th order: -20n dB/decade
  1st: -20 dB/dec
  2nd: -40 dB/dec
  3rd: -60 dB/dec
```

## Butterworth
```
|H(jw)|^2 = 1/(1 + (w/wc)^2n)
n = order (integer), wc = cutoff
Maximally flat passband, monotonic
Poles: on circle radius wc in the LHP at angles:
  s_k = wc e^(j(pi(2k+n-1)/(2n))) for k=0..n-1
```

## Chebyshev Type I
```
|H(jw)|^2 = 1/(1 + eps^2 Cn^2(w/wc))
eps = ripple factor, Cn = Chebyshev polynomial
Ripple (dB): R = 10 log10(1+eps^2)  => eps = sqrt(10^(R/10)-1)
Order:
  n >= acosh( sqrt((10^(As/10)-1)/(10^(R/10)-1)) )/acosh(ws/wp)
Steeper than Butterworth at same n
```

## Sallen-Key (active LPF)
```
fc = 1/(2 pi sqrt(R1 R2 C1 C2))
  Unity gain (equal): fc = 1/(2 pi R C)
Q = sqrt(R1 R2 C1 C2)/(...)
```

## Resonance (LC)
```
f0 = 1/(2 pi sqrt(LC))
Q = f0/BW
  Series: Q = w0 L/R
  Parallel: Q = R/(w0 L)
BW = f0/Q
```

## dB conversions
```
20 dB/decade = 6.02 dB/octave
Output magnitude (V): -3dB -> 0.707, -6dB -> 0.5, -20dB->0.1, -40dB->0.01
```

## Quick Reference
| Filter | fc | Rolloff |
|--------|-----|---------|
| RC LPF | 1/2piRC | -20dB/dec |
| RC HPF | 1/2piRC | +20dB/dec |
| RL LPF | R/2piL | -20dB/dec |
| butterworth n | - | -20n dB/dec |
| Sallen-Key | 1/2piRC | -40dB/dec |
| LC BP | 1/2pisqrtLC | depends Q |
