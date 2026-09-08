# Sampling Theorem - Concepts

## Nyquist-Shannon Sampling Theorem
A band-limited signal with maximum frequency fmax can be completely reconstructed from its samples if sampled at:
```
fs >= 2*fmax  [Nyquist rate]
```
Sampling at exactly 2*fmax is the Nyquist rate (marginal).
Sampling above 2*fmax is oversampling (practical requirement).

---

## Aliasing
- Occurs when fs < 2*fmax
- Higher frequency components "fold" into lower frequencies
- Original signal cannot be recovered
- Anti-aliasing filter is used before sampler (LPF at fmax)

## Aliased Frequency
```
f_alias = |f - k*fs| where k = integer chosen to bring f into range
Example: f = 8 kHz sampled at 6 kHz
  f_alias = |8 - 6| = 2 kHz (folded down)
```

---

## Reconstruction
- Ideal reconstruction: sinc interpolation (LPF with cutoff fmax)
- Zero-Order Hold (ZOH): Holds value constant between samples
  ZOH transfer function: H(s) = (1-e^(-sT))/s
- First-Order Hold: Linear interpolation
- Reconstruction error increases with: higher freq, larger sampling period

## Sampling Types
1. **Ideal (Impulse) Sampling:** Multiply signal by impulse train
2. **Natural Sampling:** Multiply by pulse train with finite width
3. **Flat-top (Sample and Hold):** Sample held constant (practical)

---

## ISRO Key Points
- fs >= 2*fmax is the fundamental requirement
- Aliasing: undersampling causes spectral folding
- Anti-aliasing filter is essential
- Reconstruction uses LPF with cutoff at fmax
- Practical sampling: fs > 2*fmax (margin for filter non-ideality)
