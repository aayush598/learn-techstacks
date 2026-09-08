# EM/Microwaves/Antennas - Quick Solving Shortcuts

## Transmission Line Quick Formulas
```
Z0 = sqrt(L/C)                    [lossless]
Gamma = (ZL-Z0)/(ZL+Z0)          [reflection coeff]
VSWR = (1+|Gamma|)/(1-|Gamma|)    [standing wave ratio]
Zin = Z0^2/ZL                     [quarter-wave transformer]
Zin = ZL                          [half-wave line]
lambda = vp/f                     [wavelength]
vp = c/sqrt(epsilon_r)            [in dielectric]
```

## Waveguide Quick Formulas
```
Cutoff frequency (TE10 rectangular):
  fc = c/(2a) where a = wider dimension

Phase velocity: vp = f/sqrt(f^2 - fc^2) = c/sqrt(1-(fc/f)^2)
Group velocity: vg = c*sqrt(1-(fc/f)^2)
vp * vg = c^2 (always)

Guide wavelength: lambda_g = lambda/sqrt(1-(fc/f)^2)
lambda_g > lambda always
```

## S-Parameter Quick Facts
```
S11 = input reflection (0 = matched, 1 = all reflected)
S21 = forward transmission (1 = lossless through)
Reciprocal: S12 = S21
Lossless: |S11|^2 + |S21|^2 = 1
3-port: Cannot be reciprocal, lossless, AND matched simultaneously
```

## Antenna Quick Formulas
```
EIRP = Pt * Gt                        [dBW = dBW + dBi]
Friis: Pr = Pt*Gt*Gr*(lambda/4piR)^2  [power received]
HPBW = 0.886*lambda/L (linear array)  [beamwidth in radians]
Half-wave dipole Rr = 73 ohms
Quarter-wave monopole Rr = 36.5 ohms
G = eta * D                           [gain = efficiency * directivity]
```

## Microwave Device Quick Reference
```
Gunn diode: Negative resistance (Transferred Electron Effect)
IMPATT: Impact ionization avalanche transit time
TRAPATT: Trapped plasma avalanche triggered transit
TWT: Traveling wave tube (broadband amplifier)
Klystron: Cavity-based narrowband high-power amplifier
HEMT: High electron mobility transistor (low noise)
```

## Material Quick Reference
```
Free space: epsilon_r = 1, mu_r = 1, eta = 377 ohms
Copper: sigma = 5.8e7 S/m
Silicon: epsilon_r = 11.7
GaAs: epsilon_r = 12.9
FR4: epsilon_r = 4.4 (PCB substrate)
```
