# Electromagnetic Plane Wave Propagation - Concepts

## Uniform Plane Wave
- Wave with constant phase and amplitude over planes perpendicular to travel
- E and H are perpendicular to each other and to direction of propagation
- TEM (Transverse Electromagnetic) wave

## Propagation Medium
```
Free space: 
  eta0 = sqrt(mu0/eps0) = 377 ohms (intrinsic impedance)
  c = 1/sqrt(mu0 eps0) = 3e8 m/s
Lossless dielectric:
  eta = sqrt(mu/eps), v = 1/sqrt(mu eps)
Lossy medium: complex quantities
```

## Wave Equation
```
d2E/dz2 - mu eps d2E/dt2 = 0
Solution: E = E0 e^(j(wt - gamma z))
gamma = alpha + j beta (propagation constant)
alpha = attenuation constant (Np/m)
beta = phase constant (rad/m)
```

## Key Parameters
```
Phase velocity: vp = w/beta
Wavelength: lambda = 2 pi / beta
For lossless: beta = w sqrt(mu eps), vp = 1/sqrt(mu eps)
Intrinsic impedance: eta = sqrt(mu/eps) = |E|/|H|
```

## Lossy Medium (conductor/saline)
```
gamma = alpha + j beta
For good conductor:
  alpha = beta = sqrt(pi f mu sigma)
  eta = sqrt(j w mu/sigma) -> 45 deg phase shift between E,H
  Skin depth: delta = 1/alpha = 1/sqrt(pi f mu sigma)
```

## Polarization
```
Linear: E oscillates along a line
Circular: E rotates, constant magnitude
Elliptical: general case
Orientation: vertical (perpendicular to ground), horizontal
```

## Energy & Power
```
Poynting vector: S = E x H  (W/m^2, points in propagation direction)
Time-average: S_avg = (1/2) Re(E x H*) = |E0|^2 / (2 eta)
```

## Reflection/Refraction at Interface
```
Reflection coefficient: Gamma = (eta2 - eta1)/(eta2 + eta1)
Transmission: T = 1 + Gamma = 2 eta2/(eta1+eta2)
For normal incidence, at boundary
```

## Frequency Relations
```
v = f lambda
In medium: lambda = lambda0/sqrt(mu_r eps_r)
Refractive index: n = sqrt(mu_r eps_r) = c/v
```

---

## ISRO Key Points
- Intrinsic impedance 377 ohms in free space
- E perpendicular H, both perpendicular to direction
- S = E x H (Poynting)
- Skin depth delta = 1/sqrt(pi f mu sigma)
- Good conductor: E and H 45 deg out of phase, alpha=beta
- Gamma = (eta2-eta1)/(eta2+eta1)
