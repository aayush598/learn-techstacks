# Maxwell's Equations - Formulas

## Differential Form (Time-Varying Fields)
```
1. div(D) = rho_v          [Gauss's Law - Electric]
2. div(B) = 0               [Gauss's Law - Magnetic]
3. curl(E) = -dB/dt         [Faraday's Law]
4. curl(H) = J + dD/dt      [Ampere-Maxwell Law]
```

## Integral Form
```
1. closed integral D.dA = Q_enc
2. closed integral B.dA = 0
3. closed integral E.dl = -d/dt(open integral B.dA)
4. closed integral H.dl = I_enc + d/dt(open integral D.dA)
```

## Constitutive Relations
```
D = epsilon * E    where epsilon = epsilon_r * epsilon_0
B = mu * H         where mu = mu_r * mu_0
J = sigma * E      (Ohm's law in point form)

epsilon_0 = 8.854e-12 F/m
mu_0 = 4*pi*10^-7 H/m
```

## Wave Equation (Derived from Maxwell's)
```
curl(curl(E)) = -mu * dJ/dt - mu * epsilon * d2E/dt2
In free space (J=0):
  nabla^2(E) = mu * epsilon * d2E/dt2
  nabla^2(H) = mu * epsilon * d2H/dt2
```

## Plane Wave in Free Space
```
Phase velocity: vp = 1/sqrt(mu*epsilon) = c = 3e8 m/s
Intrinsic impedance: eta = sqrt(mu/epsilon) = 377 ohms (free space)
Wavelength: lambda = vp/f
Phase constant: beta = omega*sqrt(mu*epsilon) = 2*pi/lambda
```

## Boundary Conditions Summary
```
D1n - D2n = rho_s (surface charge density)
E1t = E2t (tangential E continuous)
B1n = B2n (normal B continuous)
H1t - H2t = Js (surface current density)
```

## Quick Reference
| Equation | Relates | Key Feature |
|----------|---------|-------------|
| div(D) = rho | E and charge | Sources of E field |
| div(B) = 0 | B field | No monopoles |
| curl(E) = -dB/dt | E and changing B | Faraday's law |
| curl(H) = J + dD/dt | H and current | Ampere-Maxwell |
