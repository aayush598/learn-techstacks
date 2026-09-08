# Sampling and Reconstruction - Concepts

## Sampling
```
x_s(t) = Sum x(nT) delta(t - nT)  [ideal impulse sampling]
x_s(t) = x(t) * Sum delta(t - nT)  [multiply by comb]
```
Nyquist rate: fs >= 2*fmax

## Spectrum After Sampling
```
Xs(f) = (1/T) Sum X(f - k fs)
Baseband copy at k=0, shifted copies at multiples of fs
No aliasing if fs >= 2 fmax
```

## Aliasing
- Occurs when fs < 2*fmax
- High frequency "folds" into low frequency band
- Cannot be removed after sampling
- Fix: anti-aliasing filter (LPF) before sampler

## Aliased Frequency
```
f_alias = |f - k*fs|   for integer k nearest
e.g. f=11kHz, fs=8kHz -> |11-8|=3kHz (folds to 3kHz)
```

## Reconstruction
- Ideal: sinc interpolation (LPF cutoff at fs/2)
- Practical: Zero-Order Hold (holds sample value constant)
- Practical: First-Order Hold (linear interpolation)

## Types of Sampling
1. Ideal: impulse train (theoretical)
2. Natural: rectangular pulses (amplitude follows signal)
3. Flat-top (sample-and-hold): value held constant for entire pulse

## Quantization after Sampling (for PCM)
- Sampling: time discretization
- Quantization: amplitude discretization
- Both steps require no information loss (within constraints)

## Sample-and-Hold Circuit
- Used in ADC
- Aperture time: time to acquire/hold sample
- Droop: capacitor discharges during hold (undesirable)
- Hold mode: track latest sample

## Practical Considerations
- Oversampling: fs >> 2*fmax (improves anti-alias filtering ease)
- Guard band: separation between signal and aliased copies
- fs must account for real (non-ideal) LPF roll-off

---

## ISRO Key Points
- fs >= 2 fmax (Nyquist) - fundamental
- Aliasing from undersampling folds frequency
- Anti-aliasing LPF before ADC
- fs/2 = folding frequency
- Zero-order hold: most common practical reconstruction in DAC
