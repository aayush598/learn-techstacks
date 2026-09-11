# Antenna Types - Formulas

## Dipole
```
Half-wave: L = lambda/2
  Rr ~ 73 ohm, D ~ 1.64 (2.15 dBi)
  HPBW ~ 78 deg
Full-wave: Rr ~ 200 ohm (high)
```

## Monopole (quarter-wave over ground)
```
L = lambda/4, Rr ~ 36.5 ohm
G ~ 2x dipole (~3.28 or 5.15 dBi)
(Z_image theory doubles gain)
```

## Parabolic Dish
```
Gain: G = eta * (pi D/lambda)^2
  eta = aperture efficiency (0.5-0.75 typical)
  D = dish diameter
HPBW ~ 70 lambda/D (degrees)
F/D ratio geometry
```

## Horn
```
Gain determined by aperture & efficiency
Standard gain horn used as measurement reference
```

## Yagi
```
Gain increases with more directors (saturates)
Directional, uses reflector + directors
```

## Phased Array
```
Steering: phase shift delta = k d sin(theta)
  k = 2pi/lambda, d = element spacing, theta = scan angle
Grating lobes avoided when d < lambda/2
Directivity ~ N (array factor gain)
```

## Helical (axial)
```
Circular polarization
Gain ~ 10 log10(C^2 n lambda/(S)) approx
C = circumference, n = turns, S = spacing
```

## Patch
```
Width/len control freq & impedance
Gain ~ 5-8 dBi, BW ~ 1-5%
```

## Quick Reference
| Antenna | Key value |
|---------|-----------|
| Half-wave dipole | 73 ohm, 2.15 dBi |
| Monopole | 36.5 ohm, +3dB |
| Dish G | eta(piD/lam)^2 |
| Dish HPBW | 70 lam/D deg |
| Folded dipole | ~300 ohm |
| Array spacing | < lam/2 |
