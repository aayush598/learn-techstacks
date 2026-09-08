# Sampling Theorem - Formulas

## Nyquist Criteria
```
Nyquist rate (minimum): fs_min = 2*fmax
Nyquist frequency (max): fmax_max = fs/2
Practical: fs = (2.2 to 2.5) * fmax (for real filters)
```

## Aliasing
```
f_alias = |f_signal - k*fs|
  k is chosen such that f_alias is in the range [0, fs/2]

Example: fs = 10 kHz
  15 kHz signal folds to |15-10| = 5 kHz
  25 kHz signal folds to |25-20| = 5 kHz
  8 kHz signal: no aliasing (8 < 5? No: 8 > 5, so aliases to |8-10|=2 kHz)
```

## Sampling Spectrum
```
Sampled signal spectrum: Xs(f) = (1/T)*Sum X(f - k*fs)
Copies spaced at intervals of fs
No overlap (no aliasing) when fs >= 2*fmax
```

## Reconstruction (Ideal)
```
x(t) = Sum x(nT) * sinc((t-nT)/T)
sinc(x) = sin(pi*x)/(pi*x)
Equivalent to: LPF with transfer function:
  H(f) = T for |f| < fmax, 0 otherwise
```

## Zero-Order Hold
```
ZOH impulse response: h(t) = 1 for 0 <= t < T, 0 otherwise
ZOH transfer function: H(s) = (1 - e^(-sT))/s
ZOH frequency response: H(jw) = T*sinc(wT/2)*e^(-jwT/2)
```

## Spectral Interpolation
```
For band-limited signal, perfect reconstruction:
  Maximum frequency that can be recovered = fs/2
  This is the folding frequency
```

## Quick Reference
| Scenario | Condition | Result |
|----------|-----------|--------|
| Adequate sampling | fs >= 2*fmax | No aliasing, perfect reconstruction |
| Marginal | fs = 2*fmax | Theoretical limit, needs ideal filter |
| Undersampling | fs < 2*fmax | Aliasing, signal corrupted |
| Oversampling | fs >> 2*fmax | Easy filtering, higher data rate |
