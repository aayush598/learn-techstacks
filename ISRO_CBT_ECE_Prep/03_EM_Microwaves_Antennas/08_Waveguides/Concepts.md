# Waveguides - Concepts

## What is a Waveguide
- Hollow metal tube guiding EM waves (microwave frequencies)
- More efficient than transmission lines at high freq (low loss, high power)
- Cannot propagate TEM (needs two conductors) -> TE or TM modes
- Rectangular and circular geometry

## Modes
```
TEM: no propagation in hollow guide (needs center conductor)
TE (Transverse Electric): Ez=0, only transverse E
TM (Transverse Magnetic): Hz=0, only transverse H
TE/TM have cutoff frequency below which no propagation
Mode index (m,n): number of half-wave variations in x,y
```

## Cutoff Frequency
```
Rectangular guide (a x b):
  fc_mn = (1/(2 sqrt(mu eps))) * sqrt((m/a)^2 + (n/b)^2)

Dominant mode TE10 (a > b): lowest cutoff
  fc10 = 1/(2 a sqrt(mu eps))
  = c/(2a) (free space)
```

## Propagation Conditions
```
f > fc: propagating (real beta)
f < fc: evanescent (decays, no energy transfer)
f = fc: cutoff
Free-space wavelength vs guide: lambda_g = lambda/sqrt(1-(lambda/lambda_c)^2)
```

## Guide Wavelength & Velocity
```
Guide wavelength: lambda_g = lambda/sqrt(1 - (lambda/lambda_c)^2)
  ALWAYS > free-space lambda
Phase velocity: vp = c/sqrt(1 - (lambda/lambdac)^2)  (vp > c!)
Group velocity: vg = c*sqrt(1-(lambda/lambdac)^2)  (vg < c)
  vp * vg = c^2
```

## Rectangular Waveguide TE10
```
f_c = c/(2a)
Cutoff wavelength: lambda_c = 2a
Dominant (TE10) is single-mode over range:
  f_c(TE10) < f < f_c(TE20)
```

## Attenuation (losses)
- Conductor loss: from surface currents
- Dielectric loss: from medium
- Larger guide -> lower loss
- Operating frequency well above cutoff reduces loss

## Circular Waveguide
```
Uses Bessel functions
TE11 dominant (lowest cutoff)
Modes: TE_nm, TM_nm with Bessel roots
```

## Applications
```
- Microwave transmission (radar, satellite)
- Waveguide filters and resonators
- Antenna feeds
- Power combining/dividing
Note: higher freq smaller guide size
```

---

## ISRO Key Points
- TE10 dominant: fc = c/2a
- No TEM in hollow waveguide
- lambda_g > lambda0 (guide wavelength bigger)
- vp > c, vg < c, product = c^2
- f < fc: no propagation (evanescent)
- Dominant mode range: single-mode for TE10 only
