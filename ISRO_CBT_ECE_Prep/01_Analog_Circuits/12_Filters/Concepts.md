# Analog Filters - Concepts

## Filter Types
| Type | Passes | Cutoff |
|------|--------|--------|
| Low-pass | f < fc | -3dB at fc |
| High-pass | f > fc | -3dB at fc |
| Band-pass | fc1<f<fc2 | -3dB both |
| Band-stop | blocks fc1-fc2 | - |

## First-Order Active LPF
```
Op-amp + RC, gain > 1 possible (amplifying)
fc = 1/(2pi RC)
Rolloff: -20 dB/decade
Non-inverting (Sallen-Key): K = 1 + Rf/R1
```

## Second-Order (Sallen-Key) LPF
```
fc = 1/(2 pi sqrt(R1 R2 C1 C2))
Gain at fc: depends on Q
Rolloff: -40 dB/decade
Better: sharper cutoff than 1st order
```

## Filter Response Types
| Type | Features |
|------|----------|
| Butterworth | Maximally flat, no ripple, moderate rolloff |
| Chebyshev I | Ripple in passband, steeper rolloff |
| Chebyshev II | Ripple in stopband |
| Elliptic | Ripple both, sharpest |
| Bessel | Linear phase (flat delay), gentle rolloff |

## Butterworth
```
Maximally flat magnitude in passband
Monotonic (no ripple)
Order n: steeper rolloff (-20n dB/dec)
Good general-purpose
```

## Chebyshev
```
Equiripple passband (Type I)
Sharper cutoff than Butterworth for same order
Trade off: ripple vs sharpness
Chebyshev II: ripple in stopband
```

## Active Filter Advantages
- No inductors (bulky, lossy)
- Gain possible (active)
- Buffered (drivers)
- Tunable via R, C
- IC-friendly

## Applications
- Anti-aliasing (LPF before ADC)
- Smoothing (after DAC)
- Audio equalization (band-pass)
- Signal conditioning
- Instrumentation

## Filter Design Software/IC
- Switched-capacitor filters (integrator-based)
- Biquad / universal
- State-variable filters
- Realized with op-amp RC

## Order & Rolloff
```
Order = number of reactive elements = poles
Rolloff = 20*order dB/decade
  1st: -20 dB/dec
  2nd: -40 dB/dec
Higher order: steeper, more complex
```

---

## ISRO Key Points
- Active LPF: fc=1/2piRC, can amplify
- Sallen-Key: fc=1/2pi sqrt(R1R2C1C2)
- Butterworth: flat, no ripple
- Chebyshev: ripple, sharper
- Higher order = steeper rolloff
- Anti-aliasing is key application
