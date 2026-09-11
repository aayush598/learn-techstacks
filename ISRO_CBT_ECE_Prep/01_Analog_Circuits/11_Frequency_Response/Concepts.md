# Frequency Response of Amplifiers - Concepts

## Why Frequency Response Matters
- Amplifiers have gain that varies with frequency
- Capacitors (coupling, bypass, parasitic) create poles/zeros
- Determines bandwidth and stability

## Coupling & Bypass Capacitors (low-frequency response)
- Coupling capacitors (input/output) block DC, create high-pass
- Bypass capacitor (emitter/source) shapes low-freq gain
- Lower cutoff frequency (fL) created by these
- Below fL, gain rolls off (-20dB/dec per pole)

## Parasitic/Internal Capacitance (high-frequency response)
- Transistor internal capacitances (Cbc, Cbe, Cgs, Cgd)
- Miller effect multiplies Cgd/Cbc by (1+Av)
- Creates high-frequency roll-off
- Upper cutoff fH, above which gain falls

## Cutoff Frequencies
```
Gain drops to 0.707 (-3dB) at fL (low) and fH (high)
Bandwidth = fH - fL (approx fH - fL)
For audio amp: fL ~ few Hz, fH ~ 20kHz+
Gain-Bandwidth product relationship
```

## Common-Emitter High-Freq
```
Dominant pole from Miller capacitance:
  f_H ~ 1/(2pi R_eq C_m)
  C_m = Cbc(1+Av) (input Miller)
Miller effect dominates CE/CS high-freq response
```

## Gain-Bandwidth Product (GBW)
```
GBW = Av * BW (approximately constant)
  For op-amp: unity-gain bandwidth (GBW)
  Amplifier with gain 100, BW 1MHz -> GBW 100MHz
Boosting gain reduces bandwidth (fixed GBW)
```

## Op-Amp Frequency Response
```
Open-loop gain -20dB/dec (single dominant pole)
First-order roll-off from dominant pole
Closed-loop: BW inversely with gain (constant GBW)
```

## Bode Plot
```
Magnitude (dB) vs log frequency
Sloper: -20dB/dec per pole (high-freq), +20dB per zero
Phase: -90 deg per pole
Useful for stability analysis (gain/phase margin)
```

## Cascading Effects
```
Multiple stages: bandwidth reduces
  f_total ~ f_single * sqrt(2^(1/n)-1) (equal stages n)
  Each stage adds rolloff -> combined bandwidth lower
Overall GBW: single-stage GBW * ...
```

## Bandwidth Improvement
- Reduce Miller: cascode, neutralization
- Low parasitic cap: high fT transistors
- Trade gain for BW (constant GBW)
- Use high fT devices

## Definitions
```
Half-power point: -3dB (0.707)
Octave: factor 2 in frequency (6 dB)
Decade: factor 10 (20 dB)
```

---

## ISRO Key Points
- Coupling cap -> low-freq high-pass
- Miller cap -> high-freq rolloff, dominant in CE/CS
- BW = fH - fL
- GBW constant: gain*BW
- -20dB/dec per pole
- Cascode reduces Miller, higher BW
