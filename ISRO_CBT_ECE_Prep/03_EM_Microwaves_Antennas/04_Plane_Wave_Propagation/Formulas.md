# Electromagnetic Plane Wave Propagation - Formulas

## Intrinsic Impedance
```
eta = sqrt(mu/eps) = |E|/|H|  (ohms)
Free space: eta0 = sqrt(mu0/eps0) = 120*pi ~ 377 ohms
In dielectric: eta = eta0 * sqrt(mu_r/eps_r)
```

## Wave Speed
```
v = 1/sqrt(mu eps) = 1/(sqrt(mu_r eps_r) * sqrt(mu0 eps0)) = c/sqrt(eps_r mu_r)
c = 3e8 m/s (free space)
```

## Propagation Constant
```
Lossless: gamma = j beta, beta = w sqrt(mu eps) = w/v
Lossy: gamma = alpha + j beta

Combined: E(z) = E0 e^(-alpha z) e^(j(wt-beta z))
  alpha -> amplitude decays
  beta -> phase advances
```

## Good Conductor (high sigma)
```
alpha = beta = sqrt(pi f mu sigma) = 1/delta
Skin depth: delta = 1/alpha = 1/sqrt(pi f mu sigma)
Intrinsic impedance: eta = sqrt(j w mu/sigma) = (1+j)*sqrt(w mu/(2 sigma))
  |E|/|H| small, E leads H by 45 deg
```

## Wavelength
```
Free space: lambda0 = c/f
Medium: lambda = lambda0/sqrt(mu_r eps_r)
```

## Poynting Vector
```
S = E x H  (instantaneous, W/m^2)
S_avg = (1/2) Re(E x H*) = |E0|^2/(2 eta) (for traveling wave)
Direction: of energy flow
```

## Reflection (Normal Incidence)
```
Gamma = (eta2 - eta1)/(eta2 + eta1)
T = 1 + Gamma = 2 eta2/(eta1+eta2)
Power reflected: |Gamma|^2
Power transmitted: 1 - |Gamma|^2
```

## Standing Wave (with reflection)
```
VSWR = (1+|Gamma|)/(1-|Gamma|)  (transmission-line terminology)
```

## Polarization Formula
```
Polarization vector: direction of E
Linear: E along constant direction
Right-hand circular: E_r = E0(cos wt xhat + sin wt yhat) ... 
```

## Quick Reference
| Quantity | Free Space | Lossy/Conductor |
|----------|-----------|-----------------|
| eta | 377 | (1+j)sqrt(wmu/2sigma) |
| alpha | 0 | sqrt(pi f mu sigma) |
| beta | w/v | same as alpha (cond) |
| v | c | - |
| skin depth | - | 1/alpha |
| S avg | E^2/2eta | - |
