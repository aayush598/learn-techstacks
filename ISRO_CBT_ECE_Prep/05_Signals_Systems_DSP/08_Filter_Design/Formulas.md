# Digital Filter Design - Formulas

## FIR
```
y[n] = Sum[k=0..M-1] b[k] x[n-k]  (no feedback)
Transfer: H(z) = b0 + b1 z^-1 + ... + bM-1 z^-(M-1)  (all zeros)
Always stable (poles only at z=0)
```

## IIR
```
y[n] = Sum b[k]x[n-k] - Sum a[k]y[n-k]
H(z) = (b0 + b1 z^-1 + ...)/(1 + a1 z^-1 + a2 z^-2 + ...)
Stable iff all poles inside unit circle
```

## Frequency Response
```
H(e^jw) = |H| e^(j phi(w))
Group delay (FIR symmetric): tau_g = (M-1)/2
Linear phase condition: h[n] = h[M-1-n]
```

## Bilinear Transform
```
s = (2/T) (1 - z^-1)/(1 + z^-1)
z = (1 + sT/2)/(1 - sT/2)
Frequency warping: w = (2/T) tan(wa*T/2)
Prewarping: wa = (2/T) tan(w_d*T/2)
No aliasing, but nonlinear frequency mapping
```

## Impulse Invariance
```
h[n] = T * h_analog(nT)
Pole mapping: s = p -> z = e^(pT)
Has aliasing if h(t) not band-limited
```

## Butterworth Design
```
Magnitude: |H(jw)|^2 = 1/(1 + (w/wc)^2n)
Order: n >= log10([(10^(Astop/10)-1)/(10^(Apass/10)-1)]) / log10(ws/wp)

3dB cutoff at wc, flat passband, rolloff 20n dB/decade
```

## Chebyshev Type I
```
|H(jw)|^2 = 1/(1 + eps^2 Cn^2(w/wc))
C_n = Chebyshev polynomial of order n
Order: n >= acosh(sqrt((10^(Astop/10)-1)/(10^(Apass/10)-1))) / acosh(ws/wp)
Ripple in passband: 10log10(1+eps^2) dB
```

## Window Design Steps
```
1. Ideal impulse (e.g. ideal LPF):
   h[n] = wc/pi * sinc((wc/pi)(n - (M-1)/2))
2. Multiply by window w[n]
   h_final[n] = h_ideal[n] * w[n]
```

## Common Windows
| Window | Peak Sidelobe | Mainlobe Width |
|--------|---------------|----------------|
| Rect | -13.3 dB | 4pi/(M-1) |
| Bartlett | -25.5 dB | 8pi/(M-1) |
| Hann | -31.5 dB | 8pi/(M-1) |
| Hamming | -43.0 dB | 8pi/(M-1) |
| Blackman | -58.0 dB | 12pi/(M-1) |

## Quick Reference
| Item | FIR | IIR |
|------|-----|-----|
| Transfer | polynomial in z^-1 | rational |
| Poles | at 0 | inside unit circle |
| Stability | always | conditional |
| Linear phase | yes (sym) | no |
| Tap count | high | low |
| Design | window/sampling | bilinear/impulse |
