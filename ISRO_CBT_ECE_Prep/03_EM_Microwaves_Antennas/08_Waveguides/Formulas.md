# Waveguides - Formulas

## Rectangular Waveguide Modes
```
Mode index (m,n): variations along a (x) and b (y)
fc_mn = (1/(2 sqrt(mu eps))) sqrt((m/a)^2 + (n/b)^2)
  free space: fc_mn = (c/2) sqrt((m/a)^2+(n/b)^2)
```

## Dominant Mode TE10
```
fc10 = c/(2a)
lambda_c10 = 2a
Single-mode bandwidth: fc10 < f < fc20 = c/a
  (fc20 = c*sqrt((2/a)^2) / 2 ... = c/a)
```

## Propagation / Cutoff
```
beta = (2 pi/lambda) sqrt(1 - (f_c/f)^2)  (real if f>f_c)
Propagates: f > fc
Evanescent: f < fc
At cutoff: beta = 0
```

## Guide Wavelength
```
lambda_g = lambda0 / sqrt(1 - (lambda0/lambda_c)^2)
Always > lambda0 (guide wavelength larger than free space)
```

## Velocities
```
vp = c / sqrt(1 - (lambda/lambda_c)^2)   (vp > c, phase velocity)
vg = c * sqrt(1 - (lambda/lambda_c)^2)   (vg < c, group)
vp * vg = c^2
```

## Attenuation constants
```
Conductor (approx):
  alpha_c ~ (Rs/(a^3 b eta k)) ... (complex; don't memorize exact)
  Know: loss higher for smaller guide, higher f
Dielectric: alpha_d = (k tan_delta)/2  (~ k/2 tan delta)
```

## Circular Waveguide (roots)
```
TE11: lowest = 1.841 (first root of J1')
TM01: first TM root 2.405 (of J0)
fc = root/(2 pi a sqrt(mu eps))
```

## Power handling
```
P_max ~ area relation, limited by breakdown voltage
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| fc(TE10) | c/(2a) |
| lambda_c(TE10) | 2a |
| lambda_g | lambda0/sqrt(1-(lam/lamc)^2) |
| vp | c/sqrt(1-(lam/lamc)^2) |
| vg | c sqrt(1-(lam/lamc)^2) |
| vp*vg | c^2 |
| TE20 | c/a |
