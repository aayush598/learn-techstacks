# FM and Angle Modulation - Concepts

## Angle Modulation Basics
- Information carried in the **angle** (frequency or phase) of carrier
- Amplitude is constant (advantage: noise immunity, efficient amplifiers)
- Two types: **PM** (Phase Modulation) and **FM** (Frequency Modulation)

## FM Signal
```
Carrier: c(t) = Ac*cos(2*pi*fc*t)
Modulating: m(t)
FM: s(t) = Ac*cos(2*pi*fc*t + 2*pi*kf*integral m(tau)dt)
PM: s(t) = Ac*cos(2*pi*fc*t + kp*m(t))
```

## Instantaneous Frequency
```
For FM: f_inst = fc + kf*m(t)  (frequency varies with message)
For PM: f_inst = fc + (kp/2pi)*dm/dt  (frequency varies with derivative)
```

## Frequency Deviation (delta_f)
```
Delta_f = kf*Am (maximum deviation)
For single tone m(t) = Am*cos(2*pi*fm*t):
  FM: delta_f = kf*Am
  PM: delta_f = kp*fm*Am  (depends on fm!)
```

## Modulation Index (beta)
```
FM: beta = delta_f/fm   (deviation ratio, dimensionless)
PM: beta = kp*Am  (phase deviation, also dimensionless)
```

## Narrowband vs Wideband FM
```
Narrowband (beta << 1): BW ~ 2*fm
  Simpler, similar to AM spectrum but with phase quadrature carrier
Wideband (beta > 1): BW = 2*(delta_f + fm)
  Uses Bessel functions for spectrum
```

## Carson's Rule (BW)
```
BW = 2*(delta_f + fm) = 2*fm*(beta + 1)
Covers ~98% of total power
```

## Pre-emphasis and De-emphasis
- **Pre-emphasis**: boost high-frequencies at transmitter (high-pass filter)
- **De-emphasis**: attenuate high-frequencies at receiver (low-pass filter)
- Improves SNR for high-frequency voice signals (6 dB/octave)
- FM noise has triangular spectrum (increases with frequency)

## FM Advantages over AM
1. Constant amplitude -> immune to amplitude noise
2. Can use class C amplifiers (efficient)
3. Better SNR (for wideband FM)
4. FM capture effect (stronger signal suppresses weaker)

## FM Disadvantages
1. Requires more bandwidth (for wideband)
2. Complex demodulation
3. Demodulation noise increases with frequency

---

## ISRO Key Points
- **delta_f vs beta**: FM beta = delta_f/fm
- **Carson's rule**: BW = 2*(delta_f + fm) - MOST TESTED
- Pre/de-emphasis: high-pass at TX, low-pass at RX
- FM SNR improvement: FM is "wideband trades bandwidth for SNR"
- Capture effect is unique to FM
