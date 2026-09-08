# Digital Filter Design - Concepts

## Digital vs Analog Filters
- Digital: operate on sampled discrete-time signals
- Advantages: stable (no drift), programmable, no component tolerance, high accuracy
- Implemented with DSP (adds, multiplies, delays)

## FIR vs IIR Filters

### FIR (Finite Impulse Response)
```
y[n] = Sum[k=0..M-1] b[k] x[n-k]
- All zeros, no feedback
- Always stable (no poles except at origin)
- Linear phase possible (symmetric coefficients)
- More taps needed than IIR for same sharpness
- Poles: at z=0 only
```
Advantages: stable, linear phase, simple
Disadvantages: more computation, more memory

### IIR (Infinite Impulse Response)
```
y[n] = Sum b[k] x[n-k] - Sum a[k] y[n-k]
- Has poles (feedback)
- Can be unstable if poles outside unit circle
- Nonlinear phase possible
- Fewer coefficients than FIR
- Derived from analog prototypes (Butterworth, Chebyshev)
```
Advantages: fewer coefficients, sharper roll-off
Disadvantages: potential instability, nonlinear phase

## Comparison
| Property | FIR | IIR |
|----------|-----|-----|
| Stability | Always | Condition needed |
| Linear phase | Yes (symmetry) | No (usually) |
| Coefficients | Many | Few |
| Design | Window/frequency sampling | Bilinear/impulse-invariance |
| Feedback | No | Yes |
| This is important for ISRO |

## Window-Based FIR Design
1. Specify desired frequency response
2. Compute ideal impulse response (inverse DTFT)
3. Multiply by window function
4. Result: h[n] = h_ideal[n] * w[n]

Common windows (tradeoff sidelobes vs main lobe):
| Window | Sidelobe | Main lobe width |
|--------|----------|-----------------|
| Rectangular | -13.3 dB | 4pi/N (narrow) |
| Hann | -31.5 dB | 8pi/N |
| Hamming | -43 dB | 8pi/N |
| Blackman | -58 dB | 12pi/N |

## Analog-to-Digital Filter Mapping

### Impulse Invariance
- Maps H(s) -> H(z) by sampling h(t)
- Frequency alias possible (not band-limited)
- Poles map: s=p -> z=e^(pT)
- Preserves impulse response

### Bilinear Transform
```
s = (2/T) * (1 - z^(-1))/(1 + z^(-1))
Mapping: entire LHP -> inside unit circle
Frequency warping: w = (2/T)*tan(w_analog*T/2)
- Prewarp: design analog at prewarped frequency
- No aliasing (one-to-one mapping)
MOST COMMON in practice
```

## Filter Types
1. **Butterworth**: maximally flat passband, no ripple
   - Slope: 20n dB/decade (n = order)
   - Pole locations: equally spaced on circle
2. **Chebyshev I**: ripple in passband, monotonic stopband
   - Sharper rolloff than Butterworth same order
3. **Chebyshev II**: monotonic passband, ripple in stopband
4. **Elliptic**: ripple in both, sharpest yet

## Filter Specifications
```
Fp = passband edge, Fs = stopband edge
Apass (dB): max passband ripple
Astop (dB): min stopband attenuation
Transition width: Fs - Fp
Order determines rolloff/sharpness
```

## FIR Linear Phase
- Symmetric: h[n] = h[M-1-n] -> linear phase
- Anti-symmetric: h[n] = -h[M-1-n] -> linear phase + 90 degree
- Group delay = (M-1)/2 samples

---

## ISRO Key Points
- FIR always stable, IIR may be unstable - common
- FIR linear phase, IIR not necessarily
- Bilinear transform: no aliasing, prewarping needed
- Window sidelobe vs main lobe tradeoff
- Butterworth: flat, Chebyshev: ripple
