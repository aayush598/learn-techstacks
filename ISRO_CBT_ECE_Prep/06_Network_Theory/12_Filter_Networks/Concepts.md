# Filter Networks - Concepts

## Filter Classification
| Type | Passes | Bandwidth concept |
|------|--------|-------------------|
| Low-pass | f < fc | -3dB at fc |
| High-pass | f > fc | -3dB at fc |
| Band-pass | fc1 < f < fc2 | f2 - f1 |
| Band-stop | blocks fc1-fc2 | center f0 |

## RC Low-Pass Filter
```
Cutoff: fc = 1/(2 pi R C)
Gain (dB) at fc = -3 dB (output = 0.707 of input)
Response: H(jw) = 1/(1 + jwRC)
Slope above cutoff: -20 dB/decade (1st order)
```

## RC High-Pass Filter
```
Cutoff: fc = 1/(2 pi R C)
H(jw) = jwRC/(1+jwRC)
Slope below cutoff: +20 dB/decade
```

## RL Filters
```
RL low-pass: fc = R/(2 pi L)
RL high-pass: fc = R/(2 pi L)
(Same form - fc = R/2piL)
```

## Resonant (LC) Band-pass
```
f0 = 1/(2 pi sqrt(LC))
Q = f0/BW = w0 L/R (series) or R sqrt(C/L) (parallel)
Higher Q = narrower BW
```

## Filter Order & Roll-off
```
Order n: roll-off = 20n dB/decade
  1st order: -20 dB/decade
  2nd order: -40 dB/decade
  Butterworth: maximally flat (no ripple)
```

## Butterworth (maximally flat)
```
|H|^2 = 1/(1+(w/wc)^2n)
Order needed for required attenuation determines n
All-pole, monotonic response
Poles on circle radius wc in LHP
```

## Chebyshev (equiripple)
```
Type I: ripple in passband, steeper rolloff than Butterworth same n
Poles on ellipse
Sharper but ripple (undesired for audio)
```

## Passive vs Active
```
Passive: only R, L, C. No gain (<=1), loading effects
Active: op-amp + RC. Can amplify, no inductors, buffered
Butterworth/Chebyshev implementations common as active (Sallen-Key)
```

## Sallen-Key (2nd order active LPF)
```
fc = 1/(2 pi sqrt(R1 R2 C1 C2))
Q controlled by gain/component ratios
Unity gain version: equal R, C
```

## dB and Decade
```
20 dB/decade = 6 dB/octave
-3 dB point = output 0.707 V, half power
```

---

## ISRO Key Points
- RC LPF: fc = 1/2piRC - most used
- RL LPF: fc = R/2piL
- -20dB/decade per order
- Butterworth flat, Chebyshev ripple
- Active filters: op-amp based, no inductors
