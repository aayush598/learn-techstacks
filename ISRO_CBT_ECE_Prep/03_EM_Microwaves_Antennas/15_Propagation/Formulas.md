# Radio Wave Propagation - Formulas

## MUF & Critical Frequency
```
MUF = f_crit / cos(theta)    (secant law)
  theta = angle of incidence from vertical
  f_crit = critical frequency at vertical incidence
OWF = 0.85 * MUF (optimal working freq)
```

## Radio Horizon (LOS)
```
Optical horizon: d_opt ~ sqrt(2 h Re) (approx)
Radio horizon (with 4/3 earth):
  d ~ 4.12 sqrt(h[km]) in km
Two stations heights h1, h2:
  d_total ~ 4.12(sqrt(h1)+sqrt(h2))
```

## Skip Distance
```
Minimum distance for sky-wave return
Depends on layer height, angle, frequency
Beyond skip zone (skip distance) only sky wave
```

## Frequencies bands (approx)
```
LF 30-300k, MF 300-3000k, HF 3-30M
VHF 30-300M, UHF 300-3000M, SHF 3-30G, EHF 30-300G
```

## Attenuation approximations
```
Free space path loss: L = (4piR/lambda)^2
  dB: 20log10(4piR/lambda)
Ground wave: attenuates rapidly, use for MF only nearby
Sky wave: MUF limits

## Fading distribution
```
Rayleigh (many paths, no LOS): fading envelope
Rician (strong LOS + paths): deeper but with direct
Nakagami: generalization
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| MUF | fcrit/cos theta |
| OWF | 0.85 MUF |
| Radio horizon | 4.12 sqrt(h km) km |
| fspl dB | 20log(4piR/lam) |
| Exponential decay of ground | depends sigma |
