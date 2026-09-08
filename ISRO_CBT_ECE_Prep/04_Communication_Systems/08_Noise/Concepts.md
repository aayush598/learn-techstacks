# Noise in Communication Systems - Concepts

## Types of Noise
1. **Thermal (Johnson) noise**: random electron agitation, white, Gaussian
2. **Shot noise**: discrete charge carriers, junctions
3. **Flicker (1/f) noise**: low frequencies, semiconductors
4. **Burst/popcorn noise**: random jumps, defects
5. **Interference**: external sources (not random noise per se)

## Why Noise Matters
- Sets the minimum detectable signal level
- Limits SNR, BER performance
- Determines receiver sensitivity
- Guides LNA placement (first stage!)

## Thermal/White Noise
```
Pn = k T B (Watts)
Independent of resistance (only depends on T, B)
N0 = kT (one-sided PSD)
Green (thermal) noise is white: flat PSD, Gaussian amplitude
```

## SNR, Eb/N0, Probability
```
SNR = signal power/noise power
Eb/N0 (energy per bit / noise density)
Eb/N0 (dB) = SNR(dB) + 10log10(BW/Rb)
Higher Eb/N0 -> lower BER
```

## Noise Figure & Temperature Chain
```
F = (SNR_in)/(SNR_out)
NF (dB) = 10log10(F)
Te = (F-1)*290 K
Cascade: F = F1 + (F2-1)/G1 + (F3-1)/(G1G2)+...
FIRST stage dominates -> put low-NF amp first
```

## Noise Calculations for Receiver
```
Total noise power at receiver input: N = kT B F
Sensitivity: min signal = kT B F * (required SNR)
kT at 290K = 4e-21 W/Hz = -174 dBm/Hz
At 300K: -173.9 dBm/Hz
```

## Effects in Modulation
```
AM: amplitude noise directly corrupts (envelope)
FM: noise triangular spectrum, pre/de-emphasis helps
Digital: noise -> wrong symbol decisions -> BER
```

## Noise Bandwidth (B)
- Defined as: B = effective noise bandwidth (assumes rectangular PSD)
- For a LPF with cutoff fc: B ~ fc * (pi/2) for single-pole
- For ideal rectangular filter: B = filter bandwidth

## Constellation & Noise
- Thermal noise (Gaussian) forms circular cloud around each symbol
- BER determined by distance (d_min) vs noise
- d_min = sqrt(2Eb) for BPSK -> Pb=Q(sqrt(2Eb/N0))

---

## ISRO Key Points
- Pn = kTB (independent of R!) - trick question
- Vn = sqrt(4kTRB) DOES depend on R
- Friis cascade: first stage dominates
- -174 dBm/Hz is thermal noise floor at 290K
- Te = (F-1)*290K
