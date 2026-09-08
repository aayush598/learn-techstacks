# FM and Angle Modulation - Formulas

## FM/PM Signal
```
FM: s(t) = Ac*cos(2*pi*fc*t + beta*sin(2*pi*fm*t))
PM: s(t) = Ac*cos(2*pi*fc*t + kp*Am*cos(2*pi*fm*t))
```

## Modulation Index
```
FM: beta = delta_f/fm = (kf*Am)/fm
PM: beta = kp*Am
```

## Frequency Deviation
```
FM: delta_f = kf*Am (independent of fm)
PM: delta_f = kp*fm*Am (depends on fm)
```

## Bandwidth
```
Carson's rule: BW = 2*(delta_f + fm) = 2*fm*(beta+1)
Narrowband FM (beta << 1): BW ~ 2*fm
```
This is the single most important FM formula for ISRO.

## Bessel Function Spectrum (Wideband FM)
```
s(t) = Ac * Sum[n=-inf to inf] Jn(beta)*cos(2*pi*(fc+n*fm)*t)
Jn(beta) = nth order Bessel function
Carrier amplitude: J0(beta)
Number of significant sidebands: n ~ beta + 1
Carson BW: covers power in Jn(beta) for n <= beta+1
Key: J0(beta) can be ZERO for certain beta (carrier suppressed)
  First zero at beta ~ 2.405
```

## FM SNRi/SNRo Improvement
```
SNRo/SNRi = 3*beta^2*(beta+1)  [for single tone, FM]
FM figure of merit = 3*beta^2*(beta+1)
AM figure of merit = 1/3
Ratio = 9*beta^2*(beta+1)
```

## Noise in PM vs FM
```
PM noise output: proportional to m'(t) (derivative), triangular
FM noise output: proportional to m(t), triangular
Pre-emphasis counteracts high-frequency noise (6 dB/octave)
```

## Capture Effect
```
FM receiver locks onto stronger signal and suppresses weaker
Occurs when both signals within IF bandwidth
Threshold effect: when SNR falls below ~10 dB, output SNR collapses
```

## Quick Reference
| Parameter | FM | PM |
|-----------|----|----|
| Signal | Ac cos(2pi fc t + beta sin 2pi fm t) | Ac cos(2pi fc t + kp m(t)) |
| delta_f | kf*Am | kp*fm*Am |
| beta | delta_f/fm | kp*Am |
| BW | 2(delta_f+fm) | 2(delta_f+fm) |
| f_inst | fc + kf*m(t) | fc + (kp/2pi)dm/dt |
