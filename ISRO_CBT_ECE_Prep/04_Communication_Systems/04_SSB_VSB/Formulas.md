# SSB-SC and VSB - Formulas

## SSB Signal
```
USB: s(t) = (1/2)[m(t) cos wc t - mh(t) sin wc t]
LSB: s(t) = (1/2)[m(t) cos wc t + mh(t) sin wc t]
mh(t) = Hilbert transform of m(t)
```

## Hilbert Transform
```
H{w(t)} = (1/pi) integral m(tau)/(t-tau) dtau
Frequency: Hm(f) = -j*sgn(f)*M(f)  (90 deg phase shift)
```

## Bandwidth Comparison
```
AM/DSB-SC: BW = 2 fm
SSB: BW = fm
VSB: BW = fm + (vestige bandwidth)
```

## Power Comparison
```
AM: Pt = Pc(1 + mu^2/2)
DSB-SC: Psb = Pc mu^2/2
SSB: Pssb = Pc mu^2/4  (one sideband only)
(Each sideband = Pc mu^2/4; SSB transmits just 1)
```

## Efficiency
```
AM max: 33.3%
DSB-SC: theoretically all power in sidebands
SSB: only 1/4 Pc mu^2 (but all signal-bearing)
Relative SNR (SSB vs AM):
  SSB has benefit: 1/2 bandwidth compared to AM,
  so receiver noise halves → SSB SNR ~ 2x (3dB) better than DSB/AM
```

## Demodulation (coherent)
```
s_SSB(t) * cos(wc t) -> after LPF -> (1/2) m(t)
Requires local oscillator at carrier frequency, phase-locked
```

## SSB SNR Improvement
```
SSB does NOT have wideband FM's SNR improvement
But narrow BW (fm) means less noise captured:
  3 dB less noise than AM (BW half)
```

## Quick Reference
| Parameter | AM | DSB | SSB | VSB |
|-----------|----|----|-----|-----|
| BW | 2fm | 2fm | fm | fm+vg |
| coherent? | no | yes | yes | no(ok) |
| carrier | yes | no | no | partial |
| efficiency | 33% | high | high | high |
