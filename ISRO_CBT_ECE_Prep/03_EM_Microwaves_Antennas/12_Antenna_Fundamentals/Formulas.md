# Antenna Fundamentals - Formulas

## Directivity & Gain
```
D = 4pi U_max / P_rad (U in W/steradian)
G = 4pi U_max / P_in = eta_rad * D
D(dBi) = 10 log10(D)
G(dBi) = 10 log10(G)
```

## Effective Aperture
```
Ae = lambda^2 G / (4 pi)
Ae (max) = lambda^2 D/(4 pi)  (lossless)
[Ae in m^2, lambda in m]
```

## Friis Transmission
```
Pr = Pt * Gt * Gr * (lambda/(4 pi R))^2
(Space loss factor = (lambda/4piR)^2)
Free-space path loss (dB) = 20 log10(4 pi R/lambda)
EIRP = Pt * Gt
```

## Beamwidth / Directivity approximation
```
D ~ 4 pi / (Theta_HPBW_pi * Phi_HPBW_pi)  (radians)
  For pencil beam (small angles)
D ~ 1/(beam solid angle)
```

## Radiation resistance
```
Dipole (half-wave): Rr ~ 73 ohms
Monopole (quarter-wave): Rr ~ 36.5 ohms
Short dipole: Rr = 80 pi^2 (L/lambda)^2  (small L)
```

## Pattern
```
HPBW = angle between half-power (-3dB) points of main lobe
Radiation intensity: U = r^2 * P_avg (power per steradian)
```

## Loss / Polarization mismatch
```
Polarization loss factor = cos^2(delta angle between polarizations)
Available power at receiver = (power density)*(Ae) 
```

## Efficiency
```
eta_rad = P_rad/P_in = Rr/(Rr + R_loss)
Antenna efficiency often good (lossless for most)
```

## Quick Reference
| Quantity | Formula |
|----------|---------|
| G | eta*D |
| Ae | lambda^2 G/4pi |
| Friis Pr | Pt Gt Gr (lam/4piR)^2 |
| D | 4pi/theta phi (approx) |
| Dipole Rr | 73 ohm |
| Monopole Rr | 36.5 ohm |
| Path loss | (4piR/lam)^2 |
